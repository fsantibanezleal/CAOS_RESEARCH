"""Twelve original parity rows, complete K incidence, and frozen potential checks."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / (
    "problems/commutative-algebra/huneke-wiegand/experiments/"
    "EXP-061-uniform-parity-functional"
)


@pytest.fixture(scope="module")
def runner():
    spec = importlib.util.spec_from_file_location("hw061_test_runner", EXPERIMENT / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def modules(runner):
    return runner.dependencies()


@pytest.mark.parametrize("p", [8, 9, 12])
def test_original_inverse_incidence_and_adversarial_controls(runner, modules, p):
    functional = runner.parity_vector(runner.functional_records(p))
    row = runner.check_incidence(p, functional, modules)
    assert row["K_source_count"] == 13 and row["P1_complete_inverse_incidence_pass"]
    assert 10 * p - 3 in row["reachable_high_sectors"]
    assert row["removed_eta_pairing_row_rejected"] and row["support_index_mutation_rejected"]
    assert row["omitted_sector_diagnostic"]["K_pairing"] == 1
    assert row["omitted_sector_diagnostic"]["D_boundary_nonzero"]
    assert row["proper_local_subset_control"]["passing_K_columns"] > 0
    assert row["proper_local_subset_control"]["added_pairing"] == 1


@pytest.mark.parametrize("p,d,u,r", [(8, 2, 2, 2), (8, 2, 4, 4), (8, 3, 0, 1),
                                      (8, 4, 0, 2), (8, 9, 0, 7), (100, 2, 1, 1)])
def test_full_potential_boundaries_include_d2_free_diagonal(runner, modules, p, d, u, r):
    functional = runner.parity_vector(runner.functional_records(p))
    row = runner.check_unit(p, d, u, r, functional, modules, literal=True)
    assert row["full_D_zero"] and row["complete_high_face_identity"]
    assert row["C0_pairing"] == row["C2_pairing"]
    assert row["total_pairing"] == 0
    if p == 8 and d == 2 and u == r in (2, 4):
        assert row["C0_pairing"] == 1


def test_complete_sector_coordinate_minor_is_identity(runner):
    p = 8
    low = runner.low_set(p)
    for d in range(2, p + 2):
        pairs = runner.basis_pairs(p, d)
        for u, r in pairs:
            source = runner.parity_vector(runner.unit_potential_source(p, d, u, r))
            for v, s in pairs:
                label = ["S", sorted((low - {p, p - s, 3 * p + v}) | {6 * p, 8 * p - d}),
                         p + v + d - 2 - s]
                assert (runner.row_key(label) in source) == ((u, r) == (v, s))


def test_twelve_rows_eta_pairing_and_reflection(runner, modules):
    p = 8
    functional = runner.parity_vector(runner.functional_records(p))
    eta = runner.parity_vector(modules["endpoint"].eta_formula(p))
    assert len(functional) == 12 and runner.pairing(eta, functional) == 1
    for u in range(p - 1):
        for v in range(p - 1):
            assert runner.z_value(p, u, v) == runner.z_value(p, v, u)
            assert runner.z_value(p, u, v) == runner.z_value(p, u, p - 2 - u - v)
        if (p + u - 1) % 2 == 0:
            r = (p + u - 1) // 2
            assert runner.z_value(p, u, r - u) ^ runner.z_value(p, u, r - u - 1) == 0


def test_frozen_sampling_and_campaign_count(runner):
    count = 0
    for p in runner.CAMPAIGN:
        for d in range(2, p + 2):
            pairs = runner.sampled_pairs(p, d)
            assert len(pairs) == len(set(pairs))
            assert set(pairs) <= set(runner.basis_pairs(p, d))
            if p <= 12:
                assert pairs == runner.basis_pairs(p, d)
            if d == 2:
                assert (1, 1) in pairs
            count += len(pairs)
    assert count == 2123


def test_smoke_replay_is_deterministic_and_temporary(runner, tmp_path):
    first = runner.run(tmp_path / "first.json", smoke_only=True)
    second = runner.run(tmp_path / "second.json", smoke_only=True)
    assert first == second
    assert first["status"] == "COMPLETE" and first["total_potential_chains"] == 118


def test_resource_stop_preserves_checkpoint(runner, tmp_path):
    path = tmp_path / "stopped.json"
    with pytest.raises(RuntimeError, match="time budget exhausted"):
        runner.run(path, smoke_only=True, budget=1e-12)
    saved = json.loads(path.read_text())
    assert saved["status"] == "RESOURCE_STOP" and saved["first_failure"]["p"] == 8


@pytest.mark.parametrize("budget", [0, -1, 121, float("inf"), float("nan")])
def test_invalid_budget_is_rejected(runner, tmp_path, budget):
    with pytest.raises(ValueError, match="budget must"):
        runner.run(tmp_path / "invalid.json", budget=budget)


def test_invalid_sector_and_potential_are_rejected(runner):
    with pytest.raises(ValueError):
        runner.basis_pairs(7, 2)
    with pytest.raises(ValueError):
        runner.basis_pairs(8, 10)
    with pytest.raises(ValueError):
        runner.unit_potential_source(8, 2, 0, 0)


def test_canonical_artifact_integrity_and_scope(runner, modules):
    result = json.loads((EXPERIMENT / "artifacts/results.json").read_text())
    assert result["artifact_hash"] == modules["producer"].digest(
        {key: value for key, value in result.items() if key != "artifact_hash"})
    assert result["status"] == "COMPLETE" and result["total_potential_chains"] == 2123
    assert result["campaign"] == list(runner.CAMPAIGN)
    assert result["old_p11_hnf_source_accessed"] is False
    for row in result["rows"]:
        assert row["eta_pairing"] == 1 and row["valid_distinct_functional_rows"] == 12
        assert (row["incidence"] is not None) == (row["p"] <= 12)
    assert result["claims"]["complete_original_S_kernel_annihilation"] == (
        "SEPARATE_INDEPENDENT_AUDIT_AND_PROOF")
