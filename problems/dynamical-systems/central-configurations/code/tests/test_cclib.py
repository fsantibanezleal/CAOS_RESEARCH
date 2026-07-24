"""Regression gates for cclib on the EXP-001 exact points (methodology/04).

Tests write NOTHING canonical (no artifact paths); pure in-memory checks.
Run: .venv/Scripts/python.exe -m pytest problems/dynamical-systems/central-configurations/code/tests -q
"""

import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cclib import (ac_asymmetric, ac_symmetric, cayley_menger_planar4,  # noqa: E402
                   census_positive, e_iu, rvar, strip_monomial_factors)


def test_lagrange_point_symbolic_masses():
    m1, m2, m3 = sp.symbols("m1 m2 m3", positive=True)
    F = ac_symmetric(3, [m1, m2, m3])
    sub = {rvar(1, 2): 1, rvar(1, 3): 1, rvar(2, 3): 1}
    assert all(sp.expand(f.subs(sub)) == 0 for f in F.values())
    G = ac_asymmetric(3, [m1, m2, m3])
    assert all(sp.expand(g.subs(sub)) == 0 for g in G.values())
    assert sp.expand(e_iu(3, [m1, m2, m3]).subs(sub)) == 0


def test_rhombus_stratum_census_square_and_tetrahedron():
    """EXP-001's load-bearing refutation, frozen as the census regression gate."""
    F4 = ac_symmetric(4, [1, 1, 1, 1])
    a, b = sp.symbols("a b", positive=True)
    subsq = {rvar(1, 2): a, rvar(2, 3): a, rvar(3, 4): a, rvar(1, 4): a,
             rvar(1, 3): b, rvar(2, 4): b}
    red = sorted({sp.expand(e.subs(subsq)) for e in F4.values()},
                 key=sp.default_sort_key)
    core = []
    for e in red:
        if e == 0:
            continue
        c, _ = strip_monomial_factors(e, [a, b])
        core.append(c)
    core = sorted(set(core), key=sp.default_sort_key)
    accepted, _meta = census_positive(core, [a, b])
    assert len(accepted) == 2
    got_square = got_tetra = False
    for (av, bv) in accepted:
        if (bv ** 2 - 2 * av ** 2).equals(0) is True:
            got_square = True
            assert sp.minimal_polynomial(av, sp.Symbol("x")) == sp.sympify(
                "32*x**6 - 32*x**3 + 7")
        if (av - bv).equals(0) is True and av == 1:
            got_tetra = True
    assert got_square and got_tetra


def test_cayley_menger_separates_square_from_tetrahedron():
    cm = cayley_menger_planar4()
    x = sp.Symbol("x")
    a = sp.CRootOf(32 * x ** 6 - 32 * x ** 3 + 7, 1)
    b2 = 2 * a ** 2
    sub_square = {rvar(1, 2): a, rvar(2, 3): a, rvar(3, 4): a, rvar(1, 4): a,
                  rvar(1, 3): sp.sqrt(b2), rvar(2, 4): sp.sqrt(b2)}
    assert cm.subs(sub_square).equals(0) is True
    sub_tetra = {rvar(i, j): 1 for i in range(1, 5) for j in range(i + 1, 5)}
    assert sp.expand(cm.subs(sub_tetra)) == 4


def test_euler_collinear_equal_masses_chart_value():
    """EXP-001 P3: the equal-mass 2-middle chart solution is r12 = r23 = 90^(1/3)/6."""
    F = ac_symmetric(3, [1, 1, 1])
    R12, R13, R23 = rvar(1, 2), rvar(1, 3), rvar(2, 3)
    eqs = [sp.expand(f.subs({R13: R12 + R23})) for f in F.values()]
    eqs = [e for e in eqs if e != 0]
    vars2 = sorted({s for e in eqs for s in e.free_symbols}, key=str)
    accepted, _ = census_positive(eqs, vars2)
    assert len(accepted) == 1
    val = sp.root(90, 3) / 6
    for x in accepted[0]:
        assert (x - val).equals(0) is True
