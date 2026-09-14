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
