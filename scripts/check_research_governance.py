"""Validate strategic focus and manuscript routing for governed research programs.

The guard is intentionally stdlib-only. A governance record is required only for
programs that have adopted methodology 13; once present, it must be complete and
consistent with the experiment archive and published manuscript metadata.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM_ROOT = ROOT / "program"
GLOBAL_MANUSCRIPT_INDEX = ROOT / "manuscripts" / "README.md"

TOP_LEVEL_KEYS = {
    "schema_version",
    "problem",
    "updated",
    "original_problem",
    "mission",
    "current_focus",
    "stop_policy",
    "focuses",
    "manuscripts",
    "experiment_dispositions",
}
FOCUS_KEYS = {
    "id",
    "title",
    "status",
    "priority",
    "target",
    "value",
    "success_gate",
    "stop_conditions",
    "novelty_status",
    "manuscript_route",
    "first_bounded_action",
}
MANUSCRIPT_KEYS = {
    "slug",
    "path",
    "version",
    "version_doi",
    "concept_doi",
    "status",
    "split_action",
}
DISPOSITION_KEYS = {"start", "end", "classification", "manuscripts"}


def text(path: Path, errors: list[str], label: str) -> str:
    if not path.is_file():
        errors.append(f"{label}: missing {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def require_keys(
    value: object, required: set[str], label: str, errors: list[str]
) -> dict[str, object]:
    if not isinstance(value, dict):
        errors.append(f"{label}: expected an object")
        return {}
    missing = required - value.keys()
    if missing:
        errors.append(f"{label}: missing keys {sorted(missing)}")
    return value


def experiment_ids(problem: str, errors: list[str]) -> set[int]:
    matches = list((ROOT / "problems").glob(f"*/{problem}/experiments"))
    if len(matches) != 1:
        errors.append(
            f"{problem}: expected exactly one problems/*/{problem}/experiments directory, "
            f"found {len(matches)}"
        )
        return set()

    ids: set[int] = set()
    for directory in matches[0].iterdir():
        if not directory.is_dir() or not (directory / "verdict.md").is_file():
            continue
        match = re.match(r"EXP-(\d{3})-", directory.name)
        if match is None:
            errors.append(f"{problem}: malformed experiment directory {directory.name}")
            continue
        experiment_id = int(match.group(1))
        if experiment_id in ids:
            errors.append(f"{problem}: duplicate closed experiment EXP-{experiment_id:03d}")
        ids.add(experiment_id)
    return ids


def validate_record(path: Path, global_index: str, errors: list[str]) -> None:
    label = str(path.relative_to(ROOT))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: cannot load JSON: {exc}")
        return

    record = require_keys(data, TOP_LEVEL_KEYS, label, errors)
    problem = record.get("problem")
    if not isinstance(problem, str) or not problem:
        errors.append(f"{label}: problem must be a non-empty string")
        return
    if path.parent.name != problem:
        errors.append(f"{label}: problem does not match program directory")

    focuses_value = record.get("focuses")
    if not isinstance(focuses_value, list) or not focuses_value:
        errors.append(f"{label}: focuses must be a non-empty list")
        focuses: list[object] = []
    else:
        focuses = focuses_value

    focus_ids: set[str] = set()
    active_focus_ids: set[str] = set()
    for index, value in enumerate(focuses):
        focus = require_keys(value, FOCUS_KEYS, f"{label}: focuses[{index}]", errors)
        focus_id = focus.get("id")
        if not isinstance(focus_id, str) or not focus_id:
            errors.append(f"{label}: focuses[{index}].id must be a non-empty string")
            continue
        if focus_id in focus_ids:
            errors.append(f"{label}: duplicate focus id {focus_id}")
        focus_ids.add(focus_id)
        if str(focus.get("status", "")).startswith("active"):
            active_focus_ids.add(focus_id)
        stop_conditions = focus.get("stop_conditions")
        if not isinstance(stop_conditions, list) or not stop_conditions:
            errors.append(f"{label}: {focus_id} requires at least one stop condition")

    current_focus = record.get("current_focus")
    if current_focus not in focus_ids:
        errors.append(f"{label}: current_focus {current_focus!r} is not a declared focus")
    if current_focus not in active_focus_ids:
        errors.append(f"{label}: current_focus {current_focus!r} is not active")
    if active_focus_ids != {current_focus}:
        errors.append(
            f"{label}: exactly current_focus must be active; found {sorted(active_focus_ids)}"
        )

    map_path = path.parent / "manuscript-map.md"
    map_text = text(map_path, errors, label)
    if isinstance(current_focus, str) and current_focus not in map_text:
        errors.append(f"{label}: manuscript-map.md does not name current focus {current_focus}")

    manuscripts_value = record.get("manuscripts")
    if not isinstance(manuscripts_value, list) or not manuscripts_value:
        errors.append(f"{label}: manuscripts must be a non-empty list")
        manuscripts: list[object] = []
    else:
        manuscripts = manuscripts_value

    manuscript_slugs: set[str] = set()
    for index, value in enumerate(manuscripts):
        manuscript = require_keys(
            value, MANUSCRIPT_KEYS, f"{label}: manuscripts[{index}]", errors
        )
        slug = manuscript.get("slug")
        rel_path = manuscript.get("path")
        version = manuscript.get("version")
        version_doi = manuscript.get("version_doi")
        concept_doi = manuscript.get("concept_doi")
        if not all(isinstance(item, str) and item for item in (slug, rel_path, version, version_doi, concept_doi)):
            errors.append(f"{label}: manuscripts[{index}] has empty or non-string identity fields")
            continue
        assert isinstance(slug, str)
        assert isinstance(rel_path, str)
        assert isinstance(version, str)
        assert isinstance(version_doi, str)
        assert isinstance(concept_doi, str)
        if slug in manuscript_slugs:
            errors.append(f"{label}: duplicate manuscript slug {slug}")
        manuscript_slugs.add(slug)

        manuscript_path = ROOT / rel_path
        main_text = text(manuscript_path / "main.tex", errors, label)
        readme_text = text(manuscript_path / "README.md", errors, label)
        expected_version = f"v{version}"
        checks = (
            (main_text, rf"\newcommand{{\docversion}}{{{expected_version}}}", "main.tex version"),
            (main_text, rf"\newcommand{{\versiondoi}}{{{version_doi}}}", "main.tex version DOI"),
            (main_text, rf"\newcommand{{\conceptdoi}}{{{concept_doi}}}", "main.tex concept DOI"),
            (readme_text, expected_version, "README version"),
            (readme_text, version_doi, "README version DOI"),
            (global_index, expected_version, "global manuscript index version"),
            (global_index, version_doi, "global manuscript index DOI"),
            (map_text, slug, "manuscript map slug"),
            (map_text, version_doi, "manuscript map DOI"),
        )
        for haystack, needle, field in checks:
            if needle not in haystack:
                errors.append(f"{label}: {slug} missing {field}: {needle}")

    dispositions_value = record.get("experiment_dispositions")
    if not isinstance(dispositions_value, list) or not dispositions_value:
        errors.append(f"{label}: experiment_dispositions must be a non-empty list")
        dispositions: list[object] = []
    else:
        dispositions = dispositions_value

    covered: dict[int, int] = {}
    for index, value in enumerate(dispositions):
        disposition = require_keys(
            value, DISPOSITION_KEYS, f"{label}: experiment_dispositions[{index}]", errors
        )
        start = disposition.get("start")
        end = disposition.get("end")
        routed = disposition.get("manuscripts")
        if not isinstance(start, int) or not isinstance(end, int) or start > end:
            errors.append(f"{label}: disposition {index} has invalid integer range")
            continue
        if not isinstance(routed, list) or any(slug not in manuscript_slugs for slug in routed):
            errors.append(f"{label}: disposition {index} routes to an unknown manuscript")
        for experiment_id in range(start, end + 1):
            covered[experiment_id] = covered.get(experiment_id, 0) + 1

    closed_ids = experiment_ids(problem, errors)
    missing_ids = sorted(closed_ids - covered.keys())
    duplicate_ids = sorted(experiment_id for experiment_id in closed_ids if covered.get(experiment_id, 0) > 1)
    if missing_ids:
        errors.append(f"{label}: closed experiments lack a disposition: {missing_ids}")
    if duplicate_ids:
        errors.append(f"{label}: closed experiments have multiple dispositions: {duplicate_ids}")


def main() -> int:
    errors: list[str] = []
    records = sorted(PROGRAM_ROOT.glob("*/research-governance.json"))
    if not records:
        print("research governance: FAIL: no governance records found")
        return 1

    global_index = text(GLOBAL_MANUSCRIPT_INDEX, errors, "global manuscript index")
    for path in records:
        validate_record(path, global_index, errors)

    if errors:
        print("research governance: FAIL")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"research governance: OK: {len(records)} governed program(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
