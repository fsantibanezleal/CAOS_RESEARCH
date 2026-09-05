"""Original integral twice-endpoint sources, with lossless deterministic witness archives."""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / (
    "problems/commutative-algebra/huneke-wiegand/experiments/"
    "EXP-060-uniform-endpoint-annihilator"
)


@pytest.fixture(scope="module")
def runner():
    spec = importlib.util.spec_from_file_location("hw060_test_runner", EXPERIMENT / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def modules(runner):
    return runner.dependencies()


@pytest.mark.parametrize("p", [8, 9, 12])
def test_exact_original_annihilator_and_rejected_controls(runner, modules, p):
    row = runner.check_parameter(p, modules)
    assert row["P1"] and row["P2"] and row["P3"]
    assert row["M_V_equals_twice_eta"] and row["full_original_independent_agreement"]
    assert len(row["full_boundary"]) == 4
    assert row["source_coefficient_height"] == 5
    assert row["rejected_missing_delta02_formula_fails"]
    assert row["literal_earliest_wrong_F1_sign_and_missing_delta02_fails"]
    assert row["rejected_difference"] != row["literal_earliest_difference"]
    assert len(row["rejected_difference"]) == len(row["literal_earliest_difference"]) == 2
    assert row["sign_mutation_rejected"] and row["coefficient_mutation_rejected"]


def test_direct_potential_operator_is_integrally_linear(runner):
    p = 8
    first, second = runner.interval_potential(p, 1), runner.interval_potential(p, 2)
    combined = runner.combine_potentials((first, 2), (second, -3))
    direct = runner.potential_source(p, combined)
    expanded = runner.combine_sources((runner.potential_source(p, first), 2),
                                      (runner.potential_source(p, second), -3))
    assert direct == expanded


def test_q_sources_have_positive_unit_weight(runner):
    for a in (2, 3):
        source = runner.q_source(8, a)
        assert len(source) == 1 and source[0]["coefficient"] == 1
        assert source[0]["exact_label"][0] == "K"


def test_original_b_transfer_uses_only_frozen_formulas(runner, modules):
    p = 8
    prior = modules["endpoint"].dependencies()
    low_source, _ = prior["source"].source_and_gamma(p)
    target = prior["source"].target_from_candidate(p, prior["candidate"])
    source = runner.combine_sources((low_source, 2), (modules["endpoint"].q_source(p), 2),
                                    (runner.candidate_source(p), -1))
    expected = {key: 2 * value for key, value in runner.vector(target).items()}
    assert runner.multiply(p, source, modules) == expected
    assert runner.multiply(p, source, modules, independent=True) == expected


def test_smoke_replay_and_gzip_are_deterministic(runner, tmp_path):
    first_path = tmp_path / "one" / "results.json"
    second_path = tmp_path / "two" / "results.json"
    first = runner.run(first_path, smoke_only=True)
    second = runner.run(second_path, smoke_only=True)
    assert first == second
    assert first["status"] == "COMPLETE" and first["campaign"] == [8]
    name = first["full_source_archive"]["filename"]
    encoded = (first_path.parent / name).read_bytes()
    assert encoded == (second_path.parent / name).read_bytes()
    assert encoded[4:8] == b"\0\0\0\0" and not encoded[3] & 8
    payload = json.loads(gzip.decompress(encoded))
    assert len(payload["sources"][0]["full_source"]) == 110
    assert "full_source" not in first["rows"][0]


def test_archive_and_canonical_source_checksums(runner, modules):
    result = json.loads((EXPERIMENT / "artifacts/results.json").read_text())
    assert result["artifact_hash"] == modules["producer"].digest(
        {key: value for key, value in result.items() if key != "artifact_hash"})
    manifest = result["full_source_archive"]
    compressed = (EXPERIMENT / "artifacts" / manifest["filename"]).read_bytes()
    raw = gzip.decompress(compressed)
    assert hashlib.sha256(compressed).hexdigest() == manifest["gzip_sha256"]
    assert hashlib.sha256(raw).hexdigest() == manifest["raw_sha256"]
    assert len(compressed) == manifest["gzip_bytes"] and len(raw) == manifest["raw_bytes"]
    witnesses = json.loads(raw)["sources"]
    assert len(witnesses) == len(result["rows"]) == manifest["parameters"] == 18
    assert [row["p"] for row in result["rows"]] == list(runner.CAMPAIGN)
    for saved, witness in zip(result["rows"], witnesses, strict=True):
        assert saved["p"] == witness["p"]
        assert saved["source_hash"] == witness["source_hash"] == modules["producer"].digest(
            witness["full_source"])
        assert saved["source_support"] == len(witness["full_source"])
    first = witnesses[0]
    actual = runner.multiply(8, first["full_source"], modules, independent=True)
    eta = runner.vector(modules["endpoint"].eta_formula(8))
    assert actual == {key: 2 * value for key, value in eta.items()}
    assert result["old_hnf_source_accessed"] is False
    assert result["p11_original_source_accessed"] is False
    assert result["claims"]["uniform_nonvanishing_second_class_upper_bound"] == "NOT_ESTABLISHED"


def test_time_stop_preserves_failure_and_archive(runner, tmp_path):
    path = tmp_path / "results.json"
    with pytest.raises(RuntimeError, match="time budget exhausted"):
        runner.run(path, smoke_only=True, budget=1e-12)
    saved = json.loads(path.read_text())
    assert saved["status"] == "RESOURCE_STOP" and saved["first_failure"]["p"] == 8
    assert saved["rows"] == []
    assert (path.parent / saved["full_source_archive"]["filename"]).exists()


@pytest.mark.parametrize("potential", [{(0, 0): 1}, {(1, 1): -1}, {(0, 8): 1},
                                       {(7, 7): 1}, {(0, 2): 0.5}])
def test_invalid_potentials_are_rejected(runner, potential):
    with pytest.raises(ValueError, match="integral and vanish"):
        runner.potential_source(8, potential)


@pytest.mark.parametrize("budget", [0, -1, 61, float("inf"), float("nan")])
def test_invalid_budget_is_rejected(runner, tmp_path, budget):
    with pytest.raises(ValueError, match="budget must"):
        runner.run(tmp_path / "invalid.json", budget=budget)


def test_outside_parameter_range_is_rejected(runner):
    with pytest.raises(ValueError, match="p>=8"):
        runner.candidate_source(7)
