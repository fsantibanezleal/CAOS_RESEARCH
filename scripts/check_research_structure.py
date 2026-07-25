"""Validate the CAOS Research per-problem persistence contract.

The portfolio is the registry. Every opened or later problem must have the operational
handoff files and primary-evidence directories required by methodology 01, 02, 07, and 08.
The parser is intentionally stdlib-only so the guard runs in a clean CI checkout.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "program" / "portfolio.yaml"
ACTIVE_STATES = {
    "opened",
    "exploring",
    "consolidating",
    "published",
    "dormant",
    "closed",
}
PROGRAM_FILES = ("RESUME.md", "plan.md", "state.md", "backlog.md")
PROBLEM_DIRS = ("context", "history", "code", "experiments", "wiki")
PROBLEM_FILES = ("history/log.md", "wiki/README.md")
RESUME_SECTIONS = (
    "State in one screen",
    "The objects table",
    "Experiment index",
    "In flight",
    "Next actions",
    "Where everything lives",
    "Gotchas",
)


def parse_inline_mapping(line: str) -> dict[str, str]:
    """Parse the repository's simple one-line YAML mappings without a YAML dependency."""
    return {
        match.group(1): (match.group(2) if match.group(2) is not None else match.group(3).strip())
        for match in re.finditer(r"([a-z_]+):\s*(?:\"([^\"]*)\"|([^,}]+))", line)
    }


def load_problem_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_problems = False
    for line in PORTFOLIO.read_text(encoding="utf-8").splitlines():
        if line.strip() == "problems:":
            in_problems = True
            continue
        if in_problems and line.lstrip().startswith("- {"):
            rows.append(parse_inline_mapping(line))
    return rows


def main() -> int:
    errors: list[str] = []
    if not PORTFOLIO.is_file():
        print(f"research structure: FAIL: missing {PORTFOLIO.relative_to(ROOT)}")
        return 1

    rows = load_problem_rows()
    if not rows:
        errors.append("program/portfolio.yaml contains no problem rows")

    slugs: set[str] = set()
    active_slugs: set[str] = set()
    expected_problem_paths: set[Path] = set()

    for row in rows:
        missing_keys = {"slug", "area", "state"} - row.keys()
        if missing_keys:
            errors.append(f"portfolio row missing keys {sorted(missing_keys)}: {row}")
            continue

        slug = row["slug"]
        area = row["area"]
        state = row["state"]
        if slug in slugs:
            errors.append(f"duplicate portfolio slug: {slug}")
        slugs.add(slug)

        program_dir = ROOT / "program" / slug
        problem_dir = ROOT / "problems" / area / slug
        if state not in ACTIVE_STATES:
            continue

        active_slugs.add(slug)
        expected_problem_paths.add(problem_dir)
        for name in PROGRAM_FILES:
            path = program_dir / name
            if not path.is_file():
                errors.append(f"{slug}: missing {path.relative_to(ROOT)}")
        for name in PROBLEM_DIRS:
            path = problem_dir / name
            if not path.is_dir():
                errors.append(f"{slug}: missing directory {path.relative_to(ROOT)}")
        for name in PROBLEM_FILES:
            path = problem_dir / name
            if not path.is_file():
                errors.append(f"{slug}: missing {path.relative_to(ROOT)}")

        resume = program_dir / "RESUME.md"
        if resume.is_file():
            resume_text = resume.read_text(encoding="utf-8")
            for heading in RESUME_SECTIONS:
                pattern = rf"^##\s+\d+[a-z]?\.\s+{re.escape(heading)}"
                if not re.search(pattern, resume_text, re.MULTILINE):
                    errors.append(f"{slug}: RESUME.md missing required section '{heading}'")

    actual_program_slugs = {
        path.name for path in (ROOT / "program").iterdir() if path.is_dir()
    }
    for slug in sorted(actual_program_slugs - slugs):
        errors.append(f"program/{slug}: directory has no portfolio row")

    actual_problem_paths = {
        problem
        for area in (ROOT / "problems").iterdir()
        if area.is_dir()
        for problem in area.iterdir()
        if problem.is_dir()
    }
    for path in sorted(actual_problem_paths - expected_problem_paths):
        rel = path.relative_to(ROOT)
        if path.name not in slugs:
            errors.append(f"{rel}: problem directory has no portfolio row")
        elif path.name not in active_slugs:
            errors.append(f"{rel}: full problem tree exists but portfolio state is not opened or later")

    if errors:
        print("research structure: FAIL")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "research structure: OK: "
        f"{len(rows)} portfolio rows, {len(active_slugs)} durable active problem records"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
