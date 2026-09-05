"""Exact sparse QQ image tests; no canonical artifacts are written by tests."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / (
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-058-local-endpoint-source"
)


@pytest.fixture(scope="module")
def runner():
    spec = importlib.util.spec_from_file_location("hw058_test_runner", EXPERIMENT / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tiny_matrix(columns):
    return {"row_labels": [["K", [1], 3], ["K", [2], 2]],
            "columns": [{"exact_label": ["K", [1, 2], index], "boundary": column}
                        for index, column in enumerate(columns)]}


def test_integral_provenance(runner):
    matrix = tiny_matrix([[[0, 1], [1, 1]], [[1, 1]]])
    target = {runner.label_key(matrix["row_labels"][0]): 2}
    solved = runner.image_solution(matrix, target, runner.Budget())
    assert solved["classification"] == "INTEGRAL_WITNESS"
    assert solved["residual"] == []
    assert {term["exact_label"][-1]: term["coefficient"] for term in solved["integral_witness"]} == {
        0: 2, 1: -2,
    }


def test_noninteger_particular_is_not_a_lattice_obstruction(runner):
    matrix = tiny_matrix([[[0, 2]]])
    target = {runner.label_key(matrix["row_labels"][0]): 1}
    solved = runner.image_solution(matrix, target, runner.Budget())
    assert solved["classification"] == "RATIONAL_SECTION"
    assert solved["integer_membership"] == "INCONCLUSIVE_NOT_A_LATTICE_OBSTRUCTION"
    assert solved["particular_solution"][0]["coefficient"] == [1, 2]
    assert solved["particular_denominator_lcm"] == 2


def test_qq_refutation_has_an_original_row_dual(runner):
    matrix = tiny_matrix([[[0, 1], [1, 1]]])
    target = {runner.label_key(matrix["row_labels"][0]): 1}
    solved = runner.image_solution(matrix, target, runner.Budget())
    assert solved["classification"] == "QQ_INCONSISTENT"
    dual = {runner.label_key(term["exact_label"]): term["coefficient"] for term in solved["dual"]}
    assert sum(dual.get(runner.label_key(matrix["row_labels"][row]), 0) * value
               for row, value in matrix["columns"][0]["boundary"]) == 0
    assert solved["dual_target_pairing"] == 1
    assert sum(dual.get(row, 0) * value for row, value in target.items()) == 1


def test_every_inverse_neighbor_has_its_queried_face(runner):
    modules = runner.dependencies()
    target = modules["endpoint"].eta_formula(8)[0]
    row = runner.label_key(target["exact_label"])
    neighbors = list(runner.inverse_sources(8, row, modules["algebra"], runner.Budget()))
    assert neighbors and len({source for source, _ in neighbors}) == len(neighbors)
    for source, sign in neighbors:
        actual = modules["primary"].multiply(
            8, [{"exact_label": runner.full_label(source), "coefficient": 1}], modules["algebra"])
        assert actual[row] == sign


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf"), 61])
def test_budget_cannot_exceed_the_declared_gate(runner, value):
    with pytest.raises(ValueError, match="at most 60"):
        runner.Budget(value)


def test_forbidden_parameters_and_caps_rejected(runner, tmp_path):
    with pytest.raises(ValueError, match="subset of 8,9,10"):
        runner.run(tmp_path / "no_holdout.json", parameters=(11,))
    with pytest.raises(ValueError, match="declared maxima"):
        runner.run(tmp_path / "too_large.json", max_columns=1201)


def test_capped_neighborhood_is_not_a_refutation(runner, tmp_path):
    result = runner.run(tmp_path / "cap.json", parameters=(8,), max_columns=1)
    row = result["rows"][0]
    assert row["status"] == "INCONCLUSIVE_CAP"
    assert row["p1_status"] == "INCONCLUSIVE"
    assert row["completed_radius"] == 0
    assert row["neighborhoods"] == []
    assert row["cap"]["partial_columns"] == 1
    assert result["old_hnf_source_accessed"] is False


def test_canonical_refutation_certificates(runner):
    result = json.loads((EXPERIMENT / "artifacts/results.json").read_text())
    assert runner.digest({key: value for key, value in result.items() if key != "artifact_hash"}) == (
        result["artifact_hash"])
    assert result["status"] == "STOPPED_ON_FIRST_REFUTATION"
    assert [row["p"] for row in result["rows"]] == [8]
    row = result["rows"][0]
    assert row["status"] == "QQ_REFUTED" and row["completed_radius"] == 2
    target = {runner.label_key(term["exact_label"]): term["coefficient"] for term in row["target"]}
    for neighborhood in row["neighborhoods"]:
        assert runner.digest({key: value for key, value in neighborhood.items()
                              if key not in ("incidence_hash", "solve")}) == neighborhood["incidence_hash"]
        assert neighborhood["columns_count"] <= 1200 and neighborhood["nnz"] <= 20000
        solved = neighborhood["solve"]
        assert solved["classification"] == "QQ_INCONSISTENT"
        dual = {runner.label_key(term["exact_label"]): term["coefficient"] for term in solved["dual"]}
        for column in neighborhood["columns"]:
            assert sum(dual.get(runner.label_key(neighborhood["row_labels"][index]), 0) * coefficient
                       for index, coefficient in column["boundary"]) == 0
        assert sum(dual.get(key, 0) * coefficient for key, coefficient in target.items()) == (
            solved["dual_target_pairing"])
        assert solved["dual_target_pairing"] > 0
