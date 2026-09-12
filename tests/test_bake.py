"""The export stage bakes valid CONTRACT-2 artifacts (writes to a tmp tree, never canonical)."""
import json
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data-pipeline"))

from researchlab.stages import export_registry  # noqa: E402


def test_bake_writes_valid_registry(tmp_path, monkeypatch):
    monkeypatch.setattr(export_registry, "DERIVED", tmp_path / "derived")
    monkeypatch.setattr(export_registry, "MANIFESTS", tmp_path / "derived" / "manifests")
    written = export_registry.run()
    assert written, "bake wrote nothing"
    assert all(b"\r\n" not in path.read_bytes() for path in written)
    idx = json.loads((tmp_path / "derived" / "manifests" / "index.json").read_text())
    assert {c["case_id"] for c in idx["cases"]} == {
        "portfolio", "experiments", "jacobian", "riemann",
    }
    for c in idx["cases"]:
        man = json.loads((tmp_path / "derived" / c["manifest_path"]).read_text())
        art = tmp_path / "derived" / man["artifact"]["path"]
        assert art.exists() and art.stat().st_size == man["artifact"]["bytes"]
        assert hashlib.sha256(art.read_bytes()).hexdigest() == man["artifact"]["sha256"]
        assert man["gate"]["lane"] == man["lane"] == "precompute"
    exps = json.loads((tmp_path / "derived" / "research" / "experiments.json").read_text())
    assert len(exps["experiments"]) >= 12
    jac = json.loads((tmp_path / "derived" / "research" / "jacobian.json").read_text())
    assert jac["map"]["det"] == -2 and len(jac["family"]) == 5
    riemann = json.loads((tmp_path / "derived" / "research" / "riemann.json").read_text())
    manifest = json.loads((tmp_path / "derived" / "manifests" / "riemann.json").read_text())
    assert manifest["sources"] == riemann["provenance"]
    assert {p["source_exp"] for p in manifest["sources"]} == {
        "EXP-001-source-and-constant-audit", "EXP-002-short-interval-stability", "source-review",
        "EXP-003-odd-frame-pressure",
    }


@pytest.fixture
def committed_riemann(tmp_path, monkeypatch):
    """An isolated Git source demonstrates that dirty files never become public evidence."""
    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=tmp_path, check=True, capture_output=True,
        ).stdout

    git("init", "--quiet")
    problem = tmp_path / "problems/number-theory/riemann-hypothesis"
    exp_one = problem / "experiments/EXP-001-source-and-constant-audit"
    exp_two = problem / "experiments/EXP-002-short-interval-stability"
    exp_three = problem / "experiments/EXP-003-odd-frame-pressure"
    files = {
        exp_one / "artifacts/result.json": {"status": "PASS"},
        exp_two / "artifacts/result.json": {
            "audit": {"verified": True, "independent_sinc_taylor": True},
        },
        exp_two / "artifacts/triangle-certificate.json": {"tree": "E"},
        exp_two / "artifacts/exploration.json": {"rows": []},
        exp_two / "mathematical-proof.md": "# A committed proof\n",
        exp_two / "verdict.md": "# A committed verdict\n",
        problem / "context/source-manifest.json": {"reviewed_on": "2026-09-12"},
        exp_three / "mathematical-proof.md": "# The committed odd-frame proof\n",
        exp_three / "verdict.md": "# EXP-003 verdict: confirmed\n",
        exp_three / "adversarial-audit.md": "# The committed adversarial audit\n",
        exp_three / "hypothesis.md": "# The declaration\n",
        exp_three / "artifacts/candidates.json": {"candidates": []},
        exp_three / "run.py": "# The declared runner\n",
        exp_three / "explore.py": "# The bounded design pass\n",
        problem / "code/riemann_pressure.py": "# Pressure checker\n",
        problem / "code/riemann_certificates.py": "# Legacy checker\n",
    }
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content),
                        encoding="utf-8", newline="\n")

    def checksum(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    (exp_three / "artifacts/candidates.json").write_text(json.dumps({"candidates": [],
        "exploration_source_sha256": checksum(exp_three / "explore.py"),
        "prior_exploration_sha256": checksum(exp_two / "artifacts/exploration.json")}), encoding="utf-8")

    source_identity = {
        "hypothesis": {"sha256": checksum(exp_three / "hypothesis.md")},
        "certificate_code": {name: checksum(problem / "code" / name)
                             for name in ("riemann_pressure.py", "riemann_certificates.py")},
        "runner_sha256": checksum(exp_three / "run.py"),
        "reused_certificate": {"sha256": checksum(exp_two / "artifacts/triangle-certificate.json")},
    }
    (exp_three / "artifacts/result.json").write_text(json.dumps({
        "schema": "riemann-exp003-results-v1",
        "stage_a": {"arithmetic_status": "verified", "provenance": source_identity,
                    "replay": {"verified": True, "independent_sinc_taylor": True}},
        "stage_b": {"arithmetic_status": "not_confirmed", "outcomes": [],
                    "candidate_list_sha256": checksum(exp_three / "artifacts/candidates.json")},
    }), encoding="utf-8")

    def commit():
        git("add", ".")
        git("-c", "user.name=Replay test", "-c", "user.email=replay@example.invalid",
            "commit", "--quiet", "-m", "Fixture source")

    commit()
    monkeypatch.setattr(export_registry, "ROOT", tmp_path)
    return tmp_path, exp_two, git, commit


def test_riemann_export_ignores_uncommitted_source_bytes(committed_riemann):
    root, exp_two, git, _ = committed_riemann
    result_file = exp_two / "artifacts/result.json"
    committed = result_file.read_bytes()
    source_commit = git("rev-parse", "HEAD").decode().strip()
    result_file.write_text('{"audit":{"verified":false}}', encoding="utf-8")
    (exp_two / "mathematical-proof.md").write_text("Unreviewed replacement", encoding="utf-8")
    payload = export_registry._riemann_payload()
    assert payload["result"]["audit"]["verified"] is True
    source = next(p for p in payload["provenance"] if p["role"] == "result")
    assert source["sha256"] == hashlib.sha256(committed).hexdigest()
    assert source["bytes"] == len(committed)
    assert source["source_commit"] == source_commit
    assert source["path"] == result_file.relative_to(root).as_posix()


def test_riemann_export_rejects_untracked_certificate(committed_riemann):
    root, exp_two, git, _ = committed_riemann
    certificate = exp_two / "artifacts/triangle-certificate.json"
    git("rm", "--cached", certificate.relative_to(root).as_posix())
    git("-c", "user.name=Replay test", "-c", "user.email=replay@example.invalid",
        "commit", "--quiet", "-m", "Remove certificate from committed evidence")
    assert certificate.is_file()
    with pytest.raises(subprocess.CalledProcessError):
        export_registry._riemann_payload()


def test_riemann_export_rejects_failed_recorded_crosscheck(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    (exp_two / "artifacts/result.json").write_text(json.dumps({
        "audit": {"verified": True, "independent_sinc_taylor": False},
    }), encoding="utf-8")
    commit()
    with pytest.raises(ValueError, match="both recorded arithmetic checks"):
        export_registry._riemann_payload()


def test_pressure_export_ignores_worktree_replacement_and_binds_committed_code(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    code = exp_two.parent.parent / "code/riemann_pressure.py"
    expected = export_registry._riemann_payload()["pressure_result"]
    code.write_text("# Unreviewed checker replacement\n", encoding="utf-8", newline="\n")
    assert export_registry._riemann_payload()["pressure_result"] == expected
    commit()
    with pytest.raises(ValueError, match="committed input differs: pressure_code"):
        export_registry._riemann_payload()


def test_pressure_export_rejects_a_verified_stage_without_a_winning_certificate(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    result_file = exp_two.parent / "EXP-003-odd-frame-pressure/artifacts/result.json"
    value = json.loads(result_file.read_text(encoding="utf-8"))
    value["stage_b"]["arithmetic_status"] = "verified"
    result_file.write_text(json.dumps(value), encoding="utf-8")
    commit()
    with pytest.raises(ValueError, match="no complete certificate"):
        export_registry._riemann_payload()


def test_pressure_export_binds_frozen_candidates(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    candidates = exp_two.parent / "EXP-003-odd-frame-pressure/artifacts/candidates.json"
    candidates.write_text('{"candidates":[{"pressure":"1/2","epsilon":"1/4"}]}', encoding="utf-8")
    commit()
    with pytest.raises(ValueError, match="candidate list differs"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("tamper", ["none", "certificate", "audit", "strict_gain", "frozen_parameters"])
def test_pressure_export_requires_matching_complete_certificate(committed_riemann, tamper):
    _, exp_two, _, commit = committed_riemann
    exp_three = exp_two.parent / "EXP-003-odd-frame-pressure"
    result_file = exp_three / "artifacts/result.json"
    value = json.loads(result_file.read_text(encoding="utf-8"))
    certificate = {"theta": "3/4", "pressure": "1/100", "epsilon": "1/10", "cutoff": "10",
                   "tree": "V", "unresolved_boxes": 0}
    cert_file = exp_three / "artifacts/stage-b/candidate-1/pressure-certificate.json"
    cert_file.parent.mkdir(parents=True)
    cert_file.write_text(json.dumps(certificate), encoding="utf-8")
    identity = hashlib.sha256((json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
    candidates = exp_three / "artifacts/candidates.json"
    candidate_record = json.loads(candidates.read_text(encoding="utf-8"))
    candidate_record["candidates"] = [{"pressure": "1/100", "epsilon": "1/10"}]
    candidates.write_text(json.dumps(candidate_record), encoding="utf-8")
    candidates_hash = hashlib.sha256(candidates.read_bytes()).hexdigest()
    winner = {"candidate": 1, "status": "arithmetic_verified", **certificate,
        "certificate_sha256": identity, "strict_gain_gate": {"lower": "1/100000"},
        "audit": {"verified": True, "independent_sinc_taylor": True, "certificate_sha256": identity},
        "provenance": {**value["stage_a"]["provenance"], "candidate_list_sha256": candidates_hash}}
    if tamper == "certificate":
        cert_file.write_text(json.dumps({**certificate, "unresolved_boxes": 1}), encoding="utf-8")
    elif tamper == "audit":
        winner["audit"]["independent_sinc_taylor"] = False
    elif tamper == "strict_gain":
        winner["strict_gain_gate"]["lower"] = "0"
    elif tamper == "frozen_parameters":
        winner["pressure"] = "1/99"
    value["stage_b"] = {"arithmetic_status": "verified", "outcomes": [winner],
                        "candidate_list_sha256": candidates_hash}
    result_file.write_text(json.dumps(value), encoding="utf-8")
    commit()
    if tamper == "none":
        payload = export_registry._riemann_payload()
        assert any(p["role"] == "pressure_certificate_1" for p in payload["provenance"])
    else:
        with pytest.raises(ValueError):
            export_registry._riemann_payload()


def test_riemann_modal_records_ignore_dirty_and_staged_only_files(committed_riemann):
    root, exp_two, git, _ = committed_riemann
    verdict = exp_two / "verdict.md"
    original = git("show", f"HEAD:{verdict.relative_to(root).as_posix()}").decode()
    artifact = exp_two / "artifacts/result.json"
    committed_size = len(git("show", f"HEAD:{artifact.relative_to(root).as_posix()}"))
    verdict.write_text("# An unreviewed claim", encoding="utf-8")
    artifact.write_text("{}", encoding="utf-8")
    extra = exp_two / "hypothesis.md"
    extra.write_text("# An uncommitted hypothesis", encoding="utf-8")
    git("add", extra.relative_to(root).as_posix())
    record, = [item for item in export_registry._read_experiments()
               if item["slug"] == exp_two.name]
    assert record["verdict_md"] == original
    assert record["hypothesis_md"] == ""
    assert next(a for a in record["artifacts"] if a["name"] == "result.json")["bytes"] == committed_size


@pytest.mark.parametrize("missing_directory", ["experiments", "problem"])
def test_riemann_modal_records_survive_deleted_worktree_directories(
    committed_riemann, missing_directory,
):
    root, exp_two, _, _ = committed_riemann
    original = export_registry._read_experiments()
    source = exp_two.parent if missing_directory == "experiments" else exp_two.parent.parent
    destination = root / "removed-working-files"
    assert source.resolve().is_relative_to(root.resolve())
    assert destination.resolve().is_relative_to(root.resolve())
    source.rename(destination)
    assert export_registry._read_experiments() == original


@pytest.mark.parametrize("verdict", ["confirmed", "PASS"])
def test_registry_reads_lowercase_verdict_headers_and_body_dates(tmp_path, monkeypatch, verdict):
    relative = "problems/number-theory/parser-fixture/experiments/EXP-002-test/verdict.md"
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    path.write_text(f"# EXP-002 verdict: {verdict} for a bounded claim\n\nDate: 2026-09-12.\n")
    monkeypatch.setattr(export_registry, "ROOT", tmp_path)
    monkeypatch.setattr(export_registry, "_tracked_problem_paths", lambda: {relative})
    monkeypatch.setattr(export_registry, "_committed_riemann_paths", set)
    record, = export_registry._read_experiments()
    assert record["verdict"] == verdict.lower()
    assert record["date"] == "2026-09-12"
