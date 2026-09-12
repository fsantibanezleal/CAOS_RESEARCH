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
    files = {
        exp_one / "artifacts/result.json": {"status": "PASS"},
        exp_two / "artifacts/result.json": {
            "audit": {"verified": True, "independent_sinc_taylor": True},
        },
        exp_two / "artifacts/triangle-certificate.json": {"tree": "E"},
        exp_two / "mathematical-proof.md": "# A committed proof\n",
        exp_two / "verdict.md": "# A committed verdict\n",
        problem / "context/source-manifest.json": {"reviewed_on": "2026-09-12"},
    }
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")

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
    record, = export_registry._read_experiments()
    assert record["verdict_md"] == original
    assert record["hypothesis_md"] == ""
    assert next(a for a in record["artifacts"] if a["name"] == "result.json")["bytes"] == committed_size


@pytest.mark.parametrize("verdict", ["confirmed", "PASS"])
def test_registry_reads_lowercase_verdict_headers_and_body_dates(tmp_path, monkeypatch, verdict):
    relative = "problems/number-theory/parser-fixture/experiments/EXP-002-test/verdict.md"
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    path.write_text(f"# EXP-002 verdict: {verdict} for a bounded claim\n\nDate: 2026-09-12.\n")
    monkeypatch.setattr(export_registry, "ROOT", tmp_path)
    monkeypatch.setattr(export_registry, "_tracked_problem_paths", lambda: {relative})
    record, = export_registry._read_experiments()
    assert record["verdict"] == verdict.lower()
    assert record["date"] == "2026-09-12"
