from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = (
    ROOT
    / "problems/number-theory/riemann-hypothesis/experiments"
    / "EXP-007-spectral-defect-parity"
)
RUN_PATH = EXPERIMENT / "run.py"
RESULT_PATH = EXPERIMENT / "artifacts/canonical/result.json"
SPEC = importlib.util.spec_from_file_location("riemann_exp007", RUN_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def as_fraction(record: dict[str, str]) -> Fraction:
    return Fraction(int(record["numerator"]), int(record["denominator"]))


def test_piecewise_spectral_identity_and_monotonicity() -> None:
    grid = (Fraction(0), Fraction(1), Fraction(2), Fraction(5, 2), Fraction(4))
    for t in (Fraction(2), Fraction(5, 2), Fraction(4)):
        for value in grid:
            assert MODULE.psi(t, value) == MODULE.gc(t, value) + (t - 2) * value + 1
            assert MODULE.psi(t, value) >= MODULE.psi(Fraction(2), value)


def test_multiplicity_census_covers_equality_strict_and_empty_cases() -> None:
    exp006 = MODULE.load_exp006(ROOT)
    census = MODULE.multiplicity_census(exp006)
    assert census["profiles"] == 18479
    assert census["equality_trials"] > 0
    assert census["strict_trials"] > 0
    assert census["empty_dimension_profiles"] > 0
    assert census["passed"] is True


def test_canonical_correlated_gain_and_control_boundary() -> None:
    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    target = result["target"]
    gain_lower = as_fraction(target["gain_H_minus_h3"]["lower"])
    h_lower = as_fraction(target["h3"]["lower"])
    strengthened_lower = as_fraction(target["H"]["lower"])
    assert result["passed"] is True
    assert all(result["checks"].values())
    assert gain_lower > 0
    assert strengthened_lower >= h_lower + gain_lower
    assert result["claim_boundary"]["onset_exponent_improved"] is False
    assert result["claim_boundary"]["rh_solved"] is False
    control = result["sensitivity"]["headline_control"]
    assert control["coupled_root_is_below_h3"] is True
    assert control["pressure_only_remains_stronger"] is True


def test_canonical_receipt_binds_result_and_clean_execution() -> None:
    receipt_path = EXPERIMENT / "artifacts/canonical/execution-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    observed = hashlib.sha256(RESULT_PATH.read_bytes()).hexdigest()
    assert receipt["status"] == "pass"
    assert receipt["result_sha256"] == observed
    assert receipt["git"]["tracked_clean_at_start"] is True
