"""Exact fixed-high potential basis and sparse original connecting-image regression."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / (
    "problems/commutative-algebra/huneke-wiegand/experiments/"
    "EXP-059-potential-connecting-map"
)


@pytest.fixture(scope="module")
def runner():
    spec = importlib.util.spec_from_file_location("hw059_test_runner", EXPERIMENT / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def modules(runner):
    return runner.dependencies()


@pytest.mark.parametrize("p,u,r", [(8, 0, 2), (8, 0, 4), (8, 3, 7),
                                    (11, 1, 10), (16, 13, 15), (100, 0, 99)])
def test_complete_original_boundary_and_mutations(runner, modules, p, u, r):
    result = runner.check_unit(p, u, r, modules)
    assert result["source_support"] <= 3 * p - 5
    assert result["coefficient_height"] == 1
    assert result["boundary_support"] <= 7
    assert result["full_D_zero"] and result["independent_agreement"]
    assert result["potential_recovered"]
    assert result["wrong_beta_sign_rejected"] and result["coefficient_mutation_rejected"]


def test_integral_coordinate_minor_is_identity(runner):
    p = 8
    pairs = runner.basis_pairs(p)
    assert len(pairs) == math.comb(p - 1, 2)
    for u, r in pairs:
        source, _, _ = runner.unit_chain(p, u, r)
        assert [runner.recovered_potential(p, v, s, source) for v, s in pairs] == [
            int((u, r) == (v, s)) for v, s in pairs]


def test_frozen_campaign_has_861_distinct_chains(runner):
    cases = [(p, u, r) for p in range(8, 101) for u, r in runner.campaign_pairs(p)]
    assert len(cases) == len(set(cases)) == 861
    assert sum(p <= 16 for p, _, _ in cases) == 525


def test_replay_is_deterministic_and_temporary(runner, tmp_path):
    first = runner.run(tmp_path / "first.json", maximum=8)
    second = runner.run(tmp_path / "second.json", maximum=8)
    assert first == second
    assert first["status"] == "COMPLETE" and first["completed_chains"] == 21
    assert json.loads((tmp_path / "first.json").read_text()) == first


def test_resource_stop_preserves_checkpoint(runner, tmp_path):
    path = tmp_path / "stopped.json"
    with pytest.raises(RuntimeError, match="time budget exhausted"):
        runner.run(path, maximum=8, budget=1e-12)
    result = json.loads(path.read_text())
    assert result["status"] == "RESOURCE_STOP"
    assert result["completed_chains"] == 0
    assert result["first_failure"]["case"] == [8, 0, 2]


@pytest.mark.parametrize("p,u,r", [(7, 0, 2), (8, 0, 1), (8, 6, 7), (8, 0, 8)])
def test_invalid_unit_parameters_are_rejected(runner, p, u, r):
    with pytest.raises(ValueError):
        runner.unit_chain(p, u, r)


@pytest.mark.parametrize("budget", [0, -1, 61, float("inf"), float("nan")])
def test_invalid_budget_is_rejected(runner, tmp_path, budget):
    with pytest.raises(ValueError, match="budget must"):
        runner.run(tmp_path / "invalid.json", budget=budget)


def test_canonical_certificate_integrity_and_scope(runner, modules):
    result = json.loads((EXPERIMENT / "artifacts/results.json").read_text())
    payload = {key: value for key, value in result.items() if key != "artifact_hash"}
    assert modules["producer"].digest(payload) == result["artifact_hash"]
    assert result["status"] == "COMPLETE" and result["completed_chains"] == 861
    assert result["p11_original_source_accessed"] is False
    assert result["claims"]["uniform_eta_order_two_or_nonvanishing"] == "NOT_ESTABLISHED"
    assert [row["p"] for row in result["rows"]] == list(range(8, 101))
    assert all(len(row["chains"]) == len(runner.campaign_pairs(row["p"]))
               for row in result["rows"])
