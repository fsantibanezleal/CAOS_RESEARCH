"""Adversarial metadata controls; these do not fabricate interval certificates."""

import copy
import importlib.util
from pathlib import Path

import pytest

PROBLEM = Path(__file__).resolve().parents[1]/"problems/number-theory/riemann-hypothesis"
PATH = PROBLEM/"experiments/EXP-019-nine-point-local-replay/audit.py"
SPEC = importlib.util.spec_from_file_location("independent_rh_cover_audit", PATH)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def counters():
    state = {"nodes": 9, "pruned": 6, "splits": 3, "initial_boxes": 3,
             "maximum_depth": 2, "pressure_pruned": 1, "interval_pruned": 2,
             "tangent_pruned": 3}
    report = {key: state[key] for key in
              ["nodes", "pruned", "splits", "initial_boxes", "maximum_depth"]}
    report["details"] = {key: state[key] for key in
                         ["pressure_pruned", "interval_pruned", "tangent_pruned"]}
    return state, report


def test_valid_tree_accounting():
    audit.validate_counters(*counters())


@pytest.mark.parametrize("invalid", [-1, True, 1.0, "1", None])
def test_noninteger_or_negative_counter_rejected(invalid):
    state, report = counters()
    state["maximum_depth"] = invalid
    report["maximum_depth"] = invalid
    with pytest.raises(ValueError, match="invalid tree counter"):
        audit.validate_counters(state, report)


def test_negative_pruning_counts_with_balanced_sum_rejected():
    state, report = counters()
    state["pressure_pruned"], state["interval_pruned"] = -1, 4
    report["details"]["pressure_pruned"], report["details"]["interval_pruned"] = -1, 4
    with pytest.raises(ValueError, match="invalid tree counter"):
        audit.validate_counters(state, report)


@pytest.mark.parametrize("which", ["report", "pruning", "tree"])
def test_disagreeing_accounting_rejected(which):
    state, report = copy.deepcopy(counters())
    if which == "report":
        report["nodes"] += 1
    elif which == "pruning":
        report["details"]["interval_pruned"] += 1
    else:
        state["nodes"] += 1
    with pytest.raises(ValueError):
        audit.validate_counters(state, report)


def test_boolean_report_count_rejected_even_when_equal_to_integer():
    state, report = counters()
    report["details"]["pressure_pruned"] = True
    with pytest.raises(ValueError, match="pruning counter mismatch"):
        audit.validate_counters(state, report)
