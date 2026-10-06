from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_PATH = (
    ROOT
    / "problems/number-theory/riemann-hypothesis/experiments"
    / "EXP-005-local-selberg-transfer/run.py"
)
SPEC = importlib.util.spec_from_file_location("riemann_exp005", RUN_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_elementary_intervals_are_directed() -> None:
    sqrt_lower, sqrt_upper = MODULE.sqrt_integer_interval(2)
    assert sqrt_lower * sqrt_lower <= 2 < sqrt_upper * sqrt_upper
    e_lower, e_upper = MODULE.exp_one_interval()
    assert e_lower < e_upper
    assert e_upper - e_lower < Fraction(1, 10**150)


def test_taylor_intervals_nest_at_more_terms() -> None:
    x = Fraction(193, 500)
    sin_21 = MODULE.sin_interval(x, 21)
    sin_41 = MODULE.sin_interval(x, 41)
    cos_22 = MODULE.cos_interval(x, 22)
    cos_42 = MODULE.cos_interval(x, 42)
    assert sin_21[0] <= sin_41[0] <= sin_41[1] <= sin_21[1]
    assert cos_22[0] <= cos_42[0] <= cos_42[1] <= cos_22[1]


def test_declared_positive_and_negative_controls() -> None:
    sqrt2 = MODULE.sqrt_integer_interval(2)
    e_bounds = MODULE.exp_one_interval()
    positive = MODULE.theta_certificate(MODULE.THETA, sqrt2, e_bounds)
    negative = MODULE.theta_certificate(MODULE.NEGATIVE_THETA, sqrt2, e_bounds)
    assert positive.c_upper < 0
    assert positive.simple_curve_lower > MODULE.SIMPLE_GATE
    assert negative.simple_curve_upper < 0


def test_strict_mollifier_margin_and_boundary() -> None:
    margin = MODULE.THETA - Fraction(1, 2) - 2 * MODULE.MOLLIFIER_EXPONENT
    assert margin == Fraction(1, 50000)
    boundary = (MODULE.THETA - Fraction(1, 2)) / 2
    assert MODULE.THETA - Fraction(1, 2) - 2 * boundary == 0


def test_certificate_passes_with_pinned_sources() -> None:
    result = MODULE.compute_certificate(ROOT)
    assert result["passed"] is True
    assert all(result["checks"].values())
    assert result["claim_boundary"]["rh_solved"] is False
