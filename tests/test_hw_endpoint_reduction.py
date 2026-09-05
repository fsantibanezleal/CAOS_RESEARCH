"""Exact original-coordinate regression for the endpoint reduction and its sign correction."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / (
    "problems/commutative-algebra/huneke-wiegand/experiments/"
    "EXP-057-four-row-kernel-normal-form"
)


@pytest.fixture(scope="module")
def runner():
    spec = importlib.util.spec_from_file_location("hw057_test_runner", EXPERIMENT / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def modules(runner):
    return runner.dependencies()


@pytest.mark.parametrize("p", [8, 9, 10, 11, 17, 24])
def test_original_endpoint_identities(runner, modules, p):
    row, counterexample = runner.check_parameter(p, modules, include_counterexample=True)
    assert row["eta_support"] == 4
    assert row["eta_odd_rows"] == 1
    assert row["q_boundary_support"] == p - 2
    assert row["corrected_plus_identity"] is True
    assert row["declared_minus_identity"] is False
    assert counterexample["difference_support"] == p - 2
    assert all(abs(term["coefficient"]) == 2 for term in counterexample["difference"])


def test_initial_refutation_is_a_persisted_stop(runner, tmp_path):
    output = tmp_path / "stopped.json"
    result = runner.run(output, maximum=10)
    assert result["status"] == "REFUTED_AT_SMOKE"
    assert result["claims"]["P3"] == "REFUTED"
    assert [row["p"] for row in result["rows"]] == [8]
    assert result["continuation_after_p3_refutation"] is False
    assert json.loads(output.read_text()) == result


def test_retained_continuation_is_deterministic(runner, tmp_path):
    first = runner.run(tmp_path / "first.json", maximum=10, continue_retained=True)
    second = runner.run(tmp_path / "second.json", maximum=10, continue_retained=True)
    assert first == second
    assert first["status"] == "COMPLETE"
    assert first["overall_verdict"] == "REFUTED"
    assert first["claims"]["P2"] == "PASS_FINITE"
    assert first["claims"]["P3"] == "REFUTED"
    assert [row["p"] for row in first["rows"]] == [8, 9, 10]
    assert first["p11_original_source_accessed"] is False


@pytest.mark.parametrize("p", [0, 4, 7])
def test_outside_declared_parameter_range_is_rejected(runner, p):
    with pytest.raises(ValueError, match="p>=8"):
        runner.eta_formula(p)


def test_invalid_budget_is_rejected(runner, tmp_path):
    with pytest.raises(ValueError, match="budget must be finite and positive"):
        runner.run(tmp_path / "invalid.json", budget=0)


def test_committed_certificate_integrity(runner, modules):
    result = json.loads((EXPERIMENT / "artifacts/results.json").read_text())
    payload = {key: value for key, value in result.items() if key != "artifact_hash"}
    assert modules["producer"].digest(payload) == result["artifact_hash"]
    assert result["status"] == "COMPLETE"
    assert result["overall_verdict"] == result["claims"]["P3"] == "REFUTED"
    assert [row["p"] for row in result["rows"]] == list(range(8, 101))
    assert all(row["eta_support"] == 4 and row["eta_odd_rows"] == 1 for row in result["rows"])
