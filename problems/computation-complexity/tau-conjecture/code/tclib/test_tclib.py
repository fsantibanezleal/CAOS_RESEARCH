"""Tests for tclib. Run: python -m pytest problems/computation-complexity/tau-conjecture/code/tclib -q"""

from .enum import (
    census_integers,
    census_polynomials,
    integer_roots,
    padd,
    peval,
    pmul,
    psub,
    two_adic_valuations,
)


def test_poly_arithmetic_exact():
    x = (0, 1)
    x2 = pmul(x, x)
    assert x2 == (0, 0, 1)
    assert padd(x2, (-1,)) == (-1, 0, 1)
    assert psub(x2, x2) == ()
    assert pmul((-1, 1), (1, 1)) == (-1, 0, 1)  # (x-1)(x+1) = x^2 - 1
    assert peval((-1, 0, 1), 5) == 24


def test_integer_roots_known_cases():
    assert integer_roots((-1, 0, 1)) == {-1, 1}          # x^2 - 1
    assert integer_roots((0, -1, 0, 1)) == {-1, 0, 1}    # x^3 - x
    assert integer_roots((2, 1)) == {-2}                 # x + 2
    assert integer_roots((1,)) == set()                  # constant 1
    assert integer_roots((0, 0, 2)) == {0}               # 2x^2
    # (x-2)(x+1)x(x-1) = x^4 - 2x^3 - x^2 + 2x
    assert integer_roots((0, 2, -1, -2, 1)) == {-1, 0, 1, 2}


def test_two_adic_valuations():
    assert two_adic_valuations({-1, 1}) == {0}
    assert two_adic_valuations({2, 3, 8}) == {0, 1, 3}
    assert two_adic_valuations({0}) == set()


def test_integer_census_matches_markstrom_small():
    # Anchors from Markstroem arXiv:1306.3091v4 Figure 1 (verified EXP-001).
    rows = census_integers(5)
    expect = {1: (2, 2), 2: (4, 4), 3: (9, 6), 4: (26, 12), 5: (102, 40)}
    for k, (reached, interval) in expect.items():
        assert rows[k]["complete"]
        assert rows[k]["reached"] == reached
        assert rows[k]["interval"] == interval


def test_polynomial_census_small_depths():
    # Anchors established by EXP-001 (decision-complete tau <= 4).
    per_depth, first_seen, complete = census_polynomials(3)
    assert per_depth[1]["states"] == 9
    assert per_depth[2]["states"] == 98
    assert per_depth[3]["states"] == 1462
    zmax = {}
    best = 0
    for d in (1, 2, 3):
        polys = [p for p, fd in first_seen.items() if fd == d]
        best = max(best, max(len(integer_roots(p)) for p in polys))
        zmax[d] = best
    assert zmax == {1: 1, 2: 2, 3: 3}
