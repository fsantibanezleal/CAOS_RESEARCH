"""Repository-level, exact-arithmetic guard for the reconstructed published threshold.

Derivation (see problems/analysis-pde/navier-stokes/context/2026-09-14-threshold-reconstruction.md):
from the Cordoba-Martinez-Zoroa-Zheng exponent bookkeeping, with dissipation (D) and
self-interaction (S) saturated, the outer-velocity constraint (O, their Section 4.3.4)
is binding; optimizing it over the frequency ratio R reproduces the paper's own choice
R = sqrt(2/(7 alpha)) and the threshold (22 - 8 sqrt 7)/9, while the localization
constraint (L, 4.3.3) is slack. The paper's heuristic binds on L instead and gives
5 - 2 sqrt 6. Everything here is exact (sympy), so nothing passes on floating tolerance.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "problems/analysis-pde/navier-stokes/code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

sp = pytest.importorskip("sympy")

al, R, s, a, b = sp.symbols("alpha R s a b", positive=True)


def _b_from_self_interaction():
    return sp.solve(sp.Eq(2 * a - a / R + b + s - 1, 0), b)[0]


def _optimise(expr_in_R):
    crit = [r for r in sp.solve(sp.diff(expr_in_R, R), R) if r.is_positive is not False]
    assert len(crit) == 1
    return crit[0], sp.simplify(expr_in_R.subs(R, crit[0]))


def test_outer_velocity_budget_reproduces_the_published_theorem():
    bS = _b_from_self_interaction()
    c_O = sp.expand((a + 2 / R + s + 1 - 3 * b).subs(b, bS).subs(a, al * R))
    s_bound = sp.solve(sp.Eq(c_O, 0), s)[0]
    Rstar, smax = _optimise(s_bound)
    assert sp.simplify(al * Rstar**2 - sp.Rational(2, 7)) == 0          # the paper's R
    assert sp.simplify(smax - (2 + 3 * al - 2 * sp.sqrt(14 * al)) / 4) == 0
    roots = sp.solve(sp.Eq(smax, 0), al)
    assert any(sp.simplify(r - (22 - 8 * sp.sqrt(7)) / 9) == 0 for r in roots)


def test_localization_budget_reproduces_the_papers_heuristic():
    bS = _b_from_self_interaction()
    c_L = sp.expand((bS - (a + 1 / R + s)).subs(a, al * R))
    s_bound = sp.solve(sp.Eq(c_L, 0), s)[0]
    Rstar, smax = _optimise(s_bound)
    assert sp.simplify(al * Rstar**2 - sp.Rational(1, 3)) == 0
    assert sp.simplify(smax - ((1 + al) / 2 - sp.sqrt(3 * al))) == 0
    roots = sp.solve(sp.Eq(smax, 0), al)
    assert any(sp.simplify(r - (5 - 2 * sp.sqrt(6))) == 0 for r in roots)


def test_localization_is_slack_at_the_published_point():
    Rp = sp.sqrt(2 / (7 * al))
    ap = al * Rp
    sp_ = (2 + 3 * al - 2 * sp.sqrt(14 * al)) / 4
    bp = 1 + al - sp_ - 2 * ap
    slack = sp.simplify(bp - (ap + 1 / Rp + sp_))
    assert sp.simplify(slack - (sp.sqrt(2 * al / 7) - al) / 2) == 0
    a0 = (22 - 8 * sp.sqrt(7)) / 9
    assert sp.N(slack.subs(al, a0)) > 0


def test_round_one_calibration_is_tautological_along_the_family():
    """Under a = alpha R, ln M / ln(stretch) = 1/alpha for every alpha: p = 1/(2 alpha) always."""
    Rp = sp.sqrt(2 / (7 * al))
    ap = al * Rp
    assert sp.simplify(1 / (ap / Rp) - 1 / al) == 0
    # and the 'clean' inverse is automatic arithmetic in Q(sqrt 7): norm of 22 - 8 sqrt 7 is 36
    assert sp.expand((22 - 8 * sp.sqrt(7)) * (22 + 8 * sp.sqrt(7))) == 36


def test_the_admissible_frequency_ratios_close_exactly_at_the_threshold():
    """Exact statement: the interval of admissible R degenerates at alpha_0, and the
    geometric cascade R = 1 is excluded at every positive alpha.

    A positive force margin needs `7 alpha R^2 - (2 + 3 alpha) R + 2 < 0`. The
    discriminant of that quadratic in R is the SAME polynomial whose root is the
    published threshold, so the range of admissible frequency ratios closes to a point
    precisely where the theorem stops.
    """
    alpha, R = sp.symbols("alpha R", positive=True)
    quad = 7 * alpha * R**2 - (2 + 3 * alpha) * R + 2
    disc = sp.expand(sp.discriminant(quad, R))
    assert sp.simplify(disc - (9 * alpha**2 - 44 * alpha + 4)) == 0

    alpha0 = (22 - 8 * sp.sqrt(7)) / 9
    assert sp.simplify(disc.subs(alpha, alpha0)) == 0
    # and the single admissible ratio there is the paper's own choice. Compare squares,
    # which avoids asking sympy to denest sqrt(2/(7 (22 - 8 sqrt 7)/9)) by hand.
    double_root = (2 + 3 * alpha0) / (14 * alpha0)
    assert sp.simplify(double_root**2 - 2 / (7 * alpha0)) == 0
    assert sp.simplify(quad.subs({alpha: alpha0, R: double_root})) == 0

    # R = 1 is the geometric cascade: its margin is exactly -alpha, never positive
    s_at_one = (2 + 3 * alpha - 7 * alpha * 1 - 2 / sp.Integer(1)) / 4
    assert sp.simplify(s_at_one + alpha) == 0


def test_a_geometric_cascade_is_excluded_by_localization_against_self_interaction():
    """The same exclusion read off the two constraints directly, without the optimum.

    At R = 1 the dissipation constraint gives a = alpha, self-interaction allows
    b <= 1 - a - s, localization demands b >= a + 1 + s, and the two can only agree if
    alpha + s <= 0.
    """
    alpha, s, b = sp.symbols("alpha s b", positive=True)
    a = alpha                                  # D at R = 1
    self_interaction_upper = 1 - 2 * a + a - s  # S: b <= 1 - 2a + a/R - s at R = 1
    localization_lower = a + 1 + s             # L: b >= a + 1/R + s at R = 1
    gap = sp.simplify(self_interaction_upper - localization_lower)
    assert sp.simplify(gap + 2 * alpha + 2 * s) == 0
    assert sp.simplify(gap.subs({alpha: sp.Rational(1, 10), s: sp.Rational(1, 100)})) < 0
