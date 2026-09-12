"""Cheap exact Riemann baseline certificates; no downloaded PDFs are required."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest
from flint import ctx

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "problems/number-theory/riemann-hypothesis/experiments/EXP-001-source-and-constant-audit"
SPEC = importlib.util.spec_from_file_location("riemann_baseline_runner", EXPERIMENT / "run.py")
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


@pytest.fixture(scope="module")
def math_result():
    # A nonexistent source location must be harmless only in explicit math-only mode.
    return RUNNER.run(EXPERIMENT / "nonexistent-ci-source-cache", math_only=True)


@pytest.mark.parametrize(
    "name,decimal_prefix",
    [
        ("c0", "0.672500703679411645734379790803"),
        ("c1", "0.836250351839705822867189895401"),
        ("c2", "0.887620008173354339866075859447"),
        ("c_three_quarters", "0.419075012975424333734553610698"),
    ],
)
def test_exact_intervals_reproduce_reference_constants(math_result, name, decimal_prefix):
    result = math_result["constants"][name]
    lo, hi = Fraction(result["exact"]["lower"]), Fraction(result["exact"]["upper"])
    decimal_floor = Fraction(decimal_prefix)
    assert decimal_floor < lo <= hi < decimal_floor + Fraction(1, 10**30)
    assert hi - lo == Fraction(result["exact"]["width"])
    assert hi - lo < Fraction(1, 10**95)
    arb = result["arb_comparison"]
    assert Fraction(arb["lower"]) <= lo <= hi <= Fraction(arb["upper"])
    assert arb["exact_bracket_contained"] is True


def test_symbolic_identity_and_normalization_certificates(math_result):
    audits = math_result["symbolic_audits"]
    assert all(audit["status"] == "PASS" for audit in audits.values())
    identity = audits["triple_numerator"]
    assert identity["expanded_residual"] == identity["circle_ideal_remainder"] == "0"
    assert identity["circle_constraints_needed"] is False
    correction = audits["dyadic_normalization"]
    assert "(2*log(2)-1)*T/(2*pi)+O(log(T))" in correction["corrected_formula"]
    assert "O(T)=o(N)" in correction["theorem_impact"]
    assert "X*Y=q^2" in audits["tangent_obstruction"]["excluded_denominator_case"]


def test_math_only_status_is_explicit_and_matches_recorded_mathematics(math_result):
    recorded = json.loads((EXPERIMENT / "artifacts/result.json").read_text(encoding="utf-8"))
    assert math_result["status"] == "PASS_MATH_ONLY"
    assert math_result["math_status"] == "PASS"
    assert math_result["source_verification"]["status"] == "NOT_PERFORMED"
    assert math_result["sources"] == []
    assert math_result["constants"] == recorded["constants"]
    assert math_result["symbolic_audits"] == recorded["symbolic_audits"]


def test_math_replay_is_deterministic_and_restores_arb_precision(math_result):
    old_precision = ctx.prec
    try:
        ctx.prec = 137
        repeated = RUNNER.run(math_only=True)
        assert ctx.prec == 137
    finally:
        ctx.prec = old_precision
    assert json.dumps(repeated, sort_keys=True) == json.dumps(math_result, sort_keys=True)


def test_math_only_cli_works_without_source_manifest(tmp_path, math_result):
    destination = tmp_path / "certificate-output"
    completed = subprocess.run(
        [sys.executable, str(EXPERIMENT / "run.py"), "--math-only",
         "--source-dir", str(tmp_path / "missing"), "--output-dir", str(destination)],
        check=True, capture_output=True, text=True,
    )
    console_result = json.loads(completed.stdout)
    assert console_result["status"] == "PASS_MATH_ONLY"
    saved = json.loads((destination / "result.json").read_text())
    assert saved == math_result


@pytest.fixture
def source_fixture(tmp_path, monkeypatch):
    """Synthetic bytes exercise cache_path and integrity, not source mathematics."""
    directory = tmp_path / "context"
    cache = directory / "source-cache"
    cache.mkdir(parents=True)
    name, data = "fixture.pdf", b"synthetic integrity fixture; not a mathematical source"
    digest = hashlib.sha256(data).hexdigest()
    (cache / name).write_bytes(data)
    entry = {"filename": name, "cache_path": f"source-cache/{name}",
             "sha256": digest, "bytes": len(data), "source_url": "https://example.org/fixture.pdf",
             "license": {"status": "synthetic-test-only"}}
    manifest = {"schema": "riemann-source-manifest-v1", "documents": [entry]}
    (directory / "source-manifest.json").write_text(json.dumps(manifest))
    monkeypatch.setattr(RUNNER, "SOURCE_PINS", {name: digest})
    return directory, cache / name, manifest


def test_source_cache_relative_path_is_respected_and_changed_bytes_rejected(source_fixture):
    directory, cached, _ = source_fixture
    result = RUNNER.check_sources(directory)
    assert result[0]["status"] == "PASS"
    assert result[0]["cache_path"] == "source-cache/fixture.pdf"
    cached.write_bytes(b"modified source")
    with pytest.raises(ValueError, match="Source hash mismatch"):
        RUNNER.check_sources(directory)


def test_source_manifest_cannot_escape_cache_context(source_fixture):
    directory, _, manifest = source_fixture
    manifest["documents"][0]["cache_path"] = "../outside.pdf"
    (directory / "source-manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="escapes manifest directory"):
        RUNNER.check_sources(directory)


def test_default_source_directory_and_absent_sources_are_not_silent_passes(tmp_path):
    assert RUNNER.DEFAULT_SOURCE_DIR == ROOT / "problems/number-theory/riemann-hypothesis/context"
    with pytest.raises(FileNotFoundError):
        RUNNER.run(tmp_path / "missing")
