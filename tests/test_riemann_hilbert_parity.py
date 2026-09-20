from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_PATH = (
    ROOT
    / "problems/number-theory/riemann-hypothesis/experiments"
    / "EXP-006-hilbert-parity-compression/run.py"
)
SPEC = importlib.util.spec_from_file_location("riemann_exp006", RUN_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_profile_conventions_cover_parity_and_conjugate_pairs() -> None:
    assert MODULE.profile_counts((1, 2, 3), (1, 3)) == {
        "N": 14,
        "S": 1,
        "O": 2,
        "d": 4,
    }
    triple = MODULE.profile_certificate((3,), ())
    assert triple["dimension_residual"] == 0
    assert Fraction(triple["hilbert_residual"]) == 0
    odd_five = MODULE.profile_certificate((5,), ())
    assert odd_five["dimension_residual"] == 2
    assert Fraction(odd_five["hilbert_residual"]) > 0
    all_simple = MODULE.profile_certificate((1, 1, 1), ())
    assert all_simple["d"] == 0 and all_simple["passed"] is True


def test_fraction_square_root_is_directed() -> None:
    value = Fraction(9999, 10000)
    lower, upper = MODULE.sqrt_fraction_interval(value)
    assert lower * lower <= value < upper * upper
    assert upper - lower == Fraction(1, 10**90)


def test_declared_target_and_root_bracket() -> None:
    sqrt2 = MODULE.sqrt_integer_interval(2)
    exp_bounds = MODULE.exp_one_interval()
    target = MODULE.theta_certificate(MODULE.THETA, sqrt2, exp_bounds)
    lower = MODULE.theta_certificate(MODULE.ROOT_LOWER_THETA, sqrt2, exp_bounds)
    upper = MODULE.theta_certificate(MODULE.ROOT_UPPER_THETA, sqrt2, exp_bounds)
    assert target.c_upper < 0
    assert target.old_linear_upper < 0
    assert target.weak_simple_lower > MODULE.SIMPLE_GATE
    assert target.strong_simple_lower > target.weak_simple_upper
    assert lower.root_function_upper < 0 < upper.root_function_lower


def test_scalar_headlines_retain_zero_simple_witness() -> None:
    target = MODULE.theta_certificate(
        MODULE.THETA,
        MODULE.sqrt_integer_interval(2),
        MODULE.exp_one_interval(),
    )
    witness = MODULE.scalar_headline_witness(target)
    assert witness["S"]["numerator"] == "0"
    assert witness["passed"] is True
    assert all(witness["checks"].values())


def test_finite_census_has_equality_strict_and_empty_dimension_cases() -> None:
    census = MODULE.finite_census()
    assert census["cases"] > 10000
    assert census["equality_cases"] > 0
    assert census["strict_cases"] > 0
    assert census["empty_dimension_cases"] > 0


def test_retained_simple_term_strengthens_the_finite_certificate() -> None:
    row = MODULE.profile_certificate((1, 2), ())
    assert Fraction(row["q_min"]) == Fraction(5)
    assert Fraction(row["hilbert_residual"]) == 0


def test_certificate_passes_with_pinned_inputs() -> None:
    result = MODULE.compute_certificate(ROOT)
    assert result["passed"] is True
    assert all(result["checks"].values())
    assert result["claim_boundary"]["rh_solved"] is False
