"""Fast tests for EXP-144 (exact in-house check of Long's rank-two Poisson counterexample)."""

import importlib.util
import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
EXP = (
    ROOT / "problems" / "algebraic-geometry" / "jacobian-conjecture" / "experiments"
    / "EXP-144-long-poisson-exact-check"
)


def load(name):
    if str(EXP) not in sys.path:
        sys.path.insert(0, str(EXP))
    spec = importlib.util.spec_from_file_location(name, EXP / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def lg():
    return load("exp144_long")


def test_R_expands_to_lemma_3_1(lg):
    x, q = lg.x, lg.q
    assert sp.expand(lg.R - x * (2 - 3 * x * q)) == 0


def test_checker_reports_control_C1_as_failure(lg):
    ok, _ = lg.poisson_symbolic(lg.R, lg.T, lg.D0_poly_as_D(), lg.S)
    assert ok is False
    # {D0, R} = 1 still holds (the paper's (44))
    assert sp.expand(lg.bracket(lg.D0, lg.R) - 1) == 0


def test_printed_fiber_point_satisfies_four_equations(lg):
    pt = {lg.x: 1, lg.q: sp.Rational(2, 3), lg.p: sp.Rational(247, 96), lg.z: -sp.Rational(89, 64)}
    vals = [lg.R.subs(pt), (lg.T - sp.Rational(1, 8)).subs(pt), lg.D.subs(pt), lg.S.subs(pt)]
    assert vals == [0, 0, 0, 0]


def test_P2_symbolic_bracket_matrix_of_RTDS_equals_canonical(lg):
    got = lg.bracket_matrix((lg.R, lg.T, lg.D, lg.S))
    want = lg.target_matrix()
    assert all(sp.expand(got[i][j] - want[i][j]) == 0 for i in range(4) for j in range(4))
    ok, bad = lg.poisson_symbolic(lg.R, lg.T, lg.D, lg.S)
    assert ok is True and bad == []


def test_control_C2_constant_126_makes_P2_checker_fail(lg):
    assert lg.D_C2 != lg.D
    ok, bad = lg.poisson_symbolic(lg.R, lg.T, lg.D_C2, lg.S)
    assert ok is False and len(bad) > 0
