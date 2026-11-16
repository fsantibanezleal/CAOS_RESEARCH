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
PORTFOLIO = PROGRAM_ROOT / "portfolio.yaml"

# Methodology 13, "Result and manuscript routing": the four dispositions.
CLASSIFICATIONS = {"primary-manuscript", "companion-manuscript", "research-record", "superseded"}
# Portfolio states of a long-running problem (methodology 01) for which a record is expected.
LONG_RUNNING_STATES = {"exploring", "analyzing", "consolidating", "published", "dormant"}
VERSION_RE = re.compile(r"\bv\d+\.\d+(?:\.\d+)?\b")
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s)\]`>,;]*[^\s)\]`>,;.]")

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


CURRENT_MARKER_RE = re.compile(r"\b(current|latest|public version|version on record)\b", re.IGNORECASE)


def current_version_statement(readme: str) -> tuple[str, str | None] | None:
    """Locate the README's current-version line.

    The phrasing varies across manuscripts, so the rule is: the first line (the title excluded)
    that carries a version token (v0.25) and either a currency marker ("current", "latest",
    "public version", "version on record") or opens with the word "Version". History lines
    are never reached first because the current statement precedes them. A README with no such
    line (a per-version folder) falls back to its first heading that names a version. Returns
    the line and the version DOI of that statement: the first DOI of the line's paragraph (up
    to the next blank line), else the first DOI of the first later line that names a
    "version DOI" or starts with "Published". None when no version line exists.
    """
    lines = readme.splitlines()
    # Pass 1: a statement line; pass 2 (a per-version folder README): the heading that names the version.
    candidates = [
        index
        for index, line in enumerate(lines)
        if not line.startswith("#")
        and VERSION_RE.search(line)
        and (CURRENT_MARKER_RE.search(line) or line.lstrip("-* ").startswith("Version"))
    ] or [
        index for index, line in enumerate(lines) if line.startswith("#") and VERSION_RE.search(line)
    ]
    if not candidates:
        return None
    start = candidates[0]
    line = lines[start]
    paragraph = []
    for item in lines[start:]:
        if not item.strip():
            break
        paragraph.append(item)
    match = DOI_RE.search(chr(10).join(paragraph))
    if match is None:
        for item in lines[start:]:
            lowered = item.lower()
            if ("version doi" in lowered or lowered.startswith("published")) and DOI_RE.search(item):
                match = DOI_RE.search(item)
                break
    return line, (match.group(0) if match else None)


def own_index_rows(index: str, rel_path: str) -> list[str]:
    """The lines of the global index that link this manuscript's own folder (a versions/ tail is dropped)."""
    prefix = "manuscripts/"
    folder = rel_path[len(prefix):] if rel_path.startswith(prefix) else rel_path
    folder = folder.split("/versions/")[0].strip("/") + "/"
    return [line for line in index.splitlines() if f"]({folder})" in line]


def unadopted_problems(portfolio: str, adopted: set[str]) -> list[str]:
    """Long-running portfolio problems without a governance record (information only)."""
    found = []
    for match in re.finditer(r"slug:\s*([\w-]+)[^}\n]*?state:\s*([\w-]+)", portfolio):
        slug, state = match.groups()
        if state in LONG_RUNNING_STATES and slug not in adopted:
            found.append(slug)
    return found


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
            (map_text, slug, "manuscript map slug"),
            (map_text, version_doi, "manuscript map DOI"),
        )
        for haystack, needle, field in checks:
            if needle not in haystack:
                errors.append(f"{label}: {slug} missing {field}: {needle}")

        # README: the version and version DOI of the current-version statement only.
        statement = current_version_statement(readme_text) if readme_text else None
        if readme_text and statement is None:
            errors.append(f"{label}: {slug} README has no current-version line (a line with a version and 'Current', 'Latest', 'Public version' or a leading 'Version')")
        elif statement is not None:
            line, readme_doi = statement
            first_version = VERSION_RE.search(line)
            if first_version is None or first_version.group(0) != expected_version:
                errors.append(
                    f"{label}: {slug} README current version is "
                    f"{first_version.group(0) if first_version else 'absent'}, expected {expected_version}"
                )
            if readme_doi != version_doi:
                errors.append(
                    f"{label}: {slug} README current version DOI is {readme_doi or 'absent'}, expected {version_doi}"
                )

        # Global index: the manuscript's own row only; its first version and first DOI.
        rows = own_index_rows(global_index, rel_path)
        if not rows:
            errors.append(f"{label}: {slug} has no row in the global manuscript index for {rel_path}")
        else:
            if len(rows) > 1:
                errors.append(f"{label}: {slug} has {len(rows)} rows in the global manuscript index")
            row_version = VERSION_RE.search(rows[0])
            row_doi = DOI_RE.search(rows[0])
            if row_version is None or row_version.group(0) != expected_version:
                errors.append(
                    f"{label}: {slug} global manuscript index row version is "
                    f"{row_version.group(0) if row_version else 'absent'}, expected {expected_version}"
                )
            if row_doi is None or row_doi.group(0) != version_doi:
                errors.append(
                    f"{label}: {slug} global manuscript index row DOI is "
                    f"{row_doi.group(0) if row_doi else 'absent'}, expected {version_doi}"
                )

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
        classification = disposition.get("classification")
        if classification not in CLASSIFICATIONS:
            errors.append(
                f"{label}: disposition {index} classification {classification!r} is not one of "
                f"{sorted(CLASSIFICATIONS)}"
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
    adopted = {path.parent.name for path in records}
    if PORTFOLIO.is_file():
        pending = unadopted_problems(PORTFOLIO.read_text(encoding="utf-8"), adopted)
        if pending:
            print(
                "  info: long-running problems that have not adopted methodology 13 "
                f"(a record is due at the next strategic review): {', '.join(pending)}"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
