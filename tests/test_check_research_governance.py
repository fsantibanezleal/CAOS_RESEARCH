"""Tests for scripts/check_research_governance.py: per-manuscript row checks, vocabulary, information line."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_research_governance.py"
spec = importlib.util.spec_from_file_location("check_research_governance", SCRIPT)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

BS = chr(92)
NL = chr(10)
DOI_A = "10.5281/zenodo.1000001"
DOI_B = "10.5281/zenodo.1000002"
CONCEPT = "10.5281/zenodo.999"


def readme(version: str, doi: str, history: str = "") -> str:
    return (
        f"# m\n\nCurrent public version: v{version}, published 2026-11-01 at\n"
        f"[{doi}](https://doi.org/{doi}), under concept DOI {CONCEPT}.\n\n{history}"
    )


def index_row(slug: str, version: str, doi: str) -> str:
    return f"| [prog](prog/) | [{slug}/](prog/{slug}/) | [{doi}](https://doi.org/{doi}) (v{version}) | summary |\n"


def build(tmp_path: Path, monkeypatch, *, readme_text: str, index_text: str, classification="primary-manuscript",
          sub="", parent_readme=None):
    prog = tmp_path / "program" / "prob"
    prog.mkdir(parents=True)
    mdir = tmp_path / "manuscripts" / "prog" / "a" / sub if sub else tmp_path / "manuscripts" / "prog" / "a"
    mdir.mkdir(parents=True)
    if parent_readme is not None:
        (tmp_path / "manuscripts" / "prog" / "a" / "README.md").write_text(parent_readme, encoding="utf-8")
    tex = "".join(
        "%snewcommand{%s%s}{%s}%s" % (BS, BS, name, value, NL)
        for name, value in (("docversion", "v0.02"), ("versiondoi", DOI_A), ("conceptdoi", CONCEPT))
    )
    (mdir / "main.tex").write_text(tex, encoding="utf-8")
    (mdir / "README.md").write_text(readme_text, encoding="utf-8")
    (prog / "manuscript-map.md").write_text(f"F1 a {DOI_A}\n", encoding="utf-8")
    exp = tmp_path / "problems" / "area" / "prob" / "experiments" / "EXP-001-x"
    exp.mkdir(parents=True)
    (exp / "verdict.md").write_text("v", encoding="utf-8")
    record = {
        "schema_version": 1, "problem": "prob", "updated": "x", "original_problem": {}, "mission": "m",
        "current_focus": "F1", "stop_policy": {},
        "focuses": [{k: "x" for k in guard.FOCUS_KEYS} | {"id": "F1", "status": "active", "stop_conditions": ["s"]}],
        "manuscripts": [{"slug": "a", "path": "manuscripts/prog/a" + ("/" + sub if sub else ""), "version": "0.02", "version_doi": DOI_A,
                         "concept_doi": CONCEPT, "status": "s", "split_action": "s"}],
        "experiment_dispositions": [{"start": 1, "end": 1, "classification": classification, "manuscripts": ["a"]}],
    }
    path = prog / "research-governance.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    monkeypatch.setattr(guard, "ROOT", tmp_path)
    monkeypatch.setattr(guard, "PROGRAM_ROOT", tmp_path / "program")
    errors: list[str] = []
    guard.validate_record(path, index_text, errors)
    return errors


GOOD_INDEX = index_row("a", "0.02", DOI_A)


def test_good_fixture_passes(tmp_path, monkeypatch):
    assert build(tmp_path, monkeypatch, readme_text=readme("0.02", DOI_A), index_text=GOOD_INDEX) == []


def test_other_manuscripts_row_cannot_satisfy_index(tmp_path, monkeypatch):
    other = index_row("b", "0.02", DOI_A)  # b carries the checked version and DOI, a's own row is stale
    index = index_row("a", "0.01", DOI_B) + other
    errors = build(tmp_path, monkeypatch, readme_text=readme("0.02", DOI_A), index_text=index)
    assert any("global manuscript index" in e for e in errors)


def test_missing_own_row_fails(tmp_path, monkeypatch):
    errors = build(tmp_path, monkeypatch, readme_text=readme("0.02", DOI_A), index_text=index_row("b", "0.02", DOI_A))
    assert any("no row" in e for e in errors)


def test_history_line_cannot_satisfy_readme(tmp_path, monkeypatch):
    text = readme("0.03", DOI_B, history=f"- v0.02 published at {DOI_A}\n")
    errors = build(tmp_path, monkeypatch, readme_text=text, index_text=GOOD_INDEX)
    assert any("README current version" in e for e in errors)
    assert any("README current version DOI" in e for e in errors)


def test_readme_without_current_line_is_an_error(tmp_path, monkeypatch):
    errors = build(tmp_path, monkeypatch, readme_text=f"# m\n\nv0.02 {DOI_A}\n", index_text=GOOD_INDEX)
    assert any("no current-version line" in e for e in errors)


def test_non_vocabulary_classification_fails(tmp_path, monkeypatch):
    errors = build(tmp_path, monkeypatch, readme_text=readme("0.02", DOI_A), index_text=GOOD_INDEX,
                   classification="primary-manuscript-or-essential-context")
    assert any("classification" in e for e in errors)


@pytest.mark.parametrize("value", sorted(["primary-manuscript", "companion-manuscript", "research-record", "superseded"]))
def test_vocabulary_values_pass(tmp_path, monkeypatch, value):
    assert build(tmp_path, monkeypatch, readme_text=readme("0.02", DOI_A), index_text=GOOD_INDEX, classification=value) == []


def test_unadopted_problems_listed(tmp_path):
    portfolio = (
        "problems:\n"
        "  - { slug: gov,    area: x, state: published, feasibility: A }\n"
        "  - { slug: open1,  area: x, state: exploring, feasibility: A }\n"
        "  - { slug: sleep,  area: x, state: dormant, feasibility: A }\n"
        "  - { slug: idea,   area: x, state: proposed, feasibility: A }\n"
        "  - { slug: scoped, area: x, state: scoped, feasibility: A }\n"
    )
    assert guard.unadopted_problems(portfolio, {"gov"}) == ["open1", "sleep"]


def test_main_prints_information_and_exit_code_unaffected(capsys):
    code = guard.main()
    out = capsys.readouterr().out
    assert "not adopted methodology 13" in out
    assert code == 0


def test_version_heading_readme_with_published_line(tmp_path, monkeypatch):
    text = f"# Paper v0.02\n\nPublished 4 October 2026: {DOI_A}, concept {CONCEPT}.\n"
    assert build(tmp_path, monkeypatch, readme_text=text, index_text=GOOD_INDEX) == []


def test_version_line_with_later_version_doi_line(tmp_path, monkeypatch):
    first, second = tmp_path / "one", tmp_path / "two"
    text = f"# m\n\nVersion `v0.02`, dated 1 November 2026.\n\n- Version DOI: {DOI_A}.\n"
    assert build(first, monkeypatch, readme_text=text, index_text=GOOD_INDEX) == []
    stale = f"# m\n\nVersion `v0.02`, dated 1 November 2026.\n\n- Version DOI: {DOI_B}.\n"
    errors = build(second, monkeypatch, readme_text=stale, index_text=GOOD_INDEX)
    assert any("README current version DOI" in e for e in errors)


def test_index_row_of_versions_folder_path():
    rows = guard.own_index_rows(index_row("a", "0.02", DOI_A), "manuscripts/prog/a/versions/v0.02")
    assert len(rows) == 1


def test_failing_run_still_prints_information(monkeypatch, capsys):
    monkeypatch.setattr(guard, "validate_record", lambda path, index, errors: errors.append("planted error"))
    code = guard.main()
    out = capsys.readouterr().out
    assert code == 1
    assert "FAIL" in out
    assert "not adopted methodology 13" in out


def test_marker_less_stale_statement_before_later_planned_line_fails(tmp_path, monkeypatch):
    text = f"# m\n\nPublic record v0.01 {DOI_B}.\n\nLatest planned version v0.02: {DOI_A} (reserved).\n"
    errors = build(tmp_path, monkeypatch, readme_text=text, index_text=GOOD_INDEX)
    assert any("first version line" in e and "no currency marker" in e for e in errors)
    assert not any("README current version is" in e for e in errors)


def test_current_line_under_early_heading_passes(tmp_path, monkeypatch):
    text = f"# m\n\n## Status\n\nCurrent public version: v0.02, published at [{DOI_A}](https://doi.org/{DOI_A}).\n"
    assert build(tmp_path, monkeypatch, readme_text=text, index_text=GOOD_INDEX) == []


def test_marker_removed_from_lead_statement_gives_new_message(tmp_path, monkeypatch):
    text = f"# m\n\nPublic record v0.02 {DOI_A}.\n\n## History\n\n- v0.01 (current in its day): {DOI_B}\n"
    errors = build(tmp_path, monkeypatch, readme_text=text, index_text=GOOD_INDEX)
    assert any("first version line (line 3" in e for e in errors)
    assert not any("README current version is v0.01" in e for e in errors)


def test_versions_folder_parent_readme_is_checked(tmp_path, monkeypatch):
    own = readme("0.02", DOI_A)
    ok = build(tmp_path / "ok", monkeypatch, readme_text=own, index_text=GOOD_INDEX, sub="versions/v0.02",
               parent_readme=readme("0.02", DOI_A))
    assert ok == []
    stale = build(tmp_path / "stale", monkeypatch, readme_text=own, index_text=GOOD_INDEX, sub="versions/v0.02",
                  parent_readme=readme("0.01", DOI_B))
    assert any("parent README" in e and "version" in e for e in stale)


def test_versions_folder_missing_parent_readme_names_path(tmp_path, monkeypatch):
    errors = build(tmp_path, monkeypatch, readme_text=readme("0.02", DOI_A), index_text=GOOD_INDEX, sub="versions/v0.02")
    assert any("parent README" in e and "manuscripts/prog/a/README.md" in e.replace(BS, "/") for e in errors)


def _record_without_manuscript(tmp_path: Path, monkeypatch, reason):
    prog = tmp_path / "program" / "prob"
    prog.mkdir(parents=True)
    (prog / "manuscript-map.md").write_text("F1" + NL, encoding="utf-8")
    exp = tmp_path / "problems" / "area" / "prob" / "experiments" / "EXP-001-x"
    exp.mkdir(parents=True)
    (exp / "verdict.md").write_text("v", encoding="utf-8")
    record = {
        "schema_version": 1, "problem": "prob", "updated": "x", "original_problem": {}, "mission": "m",
        "current_focus": "F1", "stop_policy": {},
        "focuses": [{k: "x" for k in guard.FOCUS_KEYS} | {"id": "F1", "status": "active", "stop_conditions": ["s"]}],
        "manuscripts": [],
        "experiment_dispositions": [{"start": 1, "end": 1, "classification": "research-record", "manuscripts": []}],
    }
    if reason is not None:
        record["no_manuscript_reason"] = reason
    path = prog / "research-governance.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    monkeypatch.setattr(guard, "ROOT", tmp_path)
    monkeypatch.setattr(guard, "PROGRAM_ROOT", tmp_path / "program")
    errors: list[str] = []
    guard.validate_record(path, "", errors)
    return errors


def test_empty_manuscripts_with_a_reason_passes(tmp_path, monkeypatch):
    assert _record_without_manuscript(tmp_path, monkeypatch, "no manuscript yet: decided at the next review") == []


def test_empty_manuscripts_without_a_reason_fails(tmp_path, monkeypatch):
    errors = _record_without_manuscript(tmp_path, monkeypatch, None)
    assert any("no_manuscript_reason" in e for e in errors)
    errors = _record_without_manuscript(tmp_path / "b", monkeypatch, "  ")
    assert any("no_manuscript_reason" in e for e in errors)

