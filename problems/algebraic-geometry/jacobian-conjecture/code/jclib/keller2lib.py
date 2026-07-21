"""jclib.keller2lib: shared planar-Keller utilities (library, graded tops, radicals)."""
from __future__ import annotations

from sympy import Poly, Rational, expand, factor_list, symbols

x, y = symbols("x y")


def jac2(P, Q):
    return expand(P.diff(x) * Q.diff(y) - P.diff(y) * Q.diff(x))


COEFS = [Rational(1), Rational(-2), Rational(1, 2), Rational(3), Rational(-1, 3), Rational(2)]

SPECS = [
    [("ey", [0, 2]), ("ex", [1, 3])],
    [("ex", [2]), ("ey", [0, 0, 1]), ("aff", None)],
    [("ey", [1, 0, 2]), ("ex", [0, 3]), ("ey", [2])],
    [("aff", None), ("ex", [0, 0, 4]), ("ey", [1, 2])],
    [("ey", [0, 5]), ("ex", [3, 0, 1]), ("aff", None), ("ey", [0, 0, 0, 2])],
    [("ex", [0, 1, 0, 2]), ("ey", [4])],
    [("ey", [0, 0, 3]), ("ex", [0, 2]), ("ey", [1, 1])],
    [("ex", [5, 1]), ("ey", [0, 2, 2]), ("ex", [0, 0, 1])],
]


def library():
    """Deterministic real Keller maps: compositions of elementary and unimodular affine maps."""
    maps = []
    ci = 0
    for spec in SPECS:
        P, Q = x, y
        for kind, dat in spec:
            if kind == "ex":
                pol = sum(Rational(d) * y**i for i, d in enumerate(dat))
                P = P.subs({x: x + pol}, simultaneous=True)
                Q = Q.subs({x: x + pol}, simultaneous=True)
            elif kind == "ey":
                pol = sum(Rational(d) * x**i for i, d in enumerate(dat))
                P = P.subs({y: y + pol}, simultaneous=True)
                Q = Q.subs({y: y + pol}, simultaneous=True)
            else:
                a1, a2 = COEFS[ci % 6], COEFS[(ci + 1) % 6]
                ci += 2
                b2 = Rational(1)
                b1 = (a1 * b2 - 1) / a2
                Pn = a1 * x + a2 * y
                Qn = b1 * x + b2 * y + 2
                P = P.subs({x: Pn, y: Qn}, simultaneous=True)
                Q = Q.subs({x: Pn, y: Qn}, simultaneous=True)
        maps.append((expand(P), expand(Q)))
    return maps


def graded_piece(expr, s):
    """Total-degree-s homogeneous piece."""
    p = Poly(expand(expr), x, y)
    return expand(sum(co * x**i * y**j for (i, j), co in p.terms() if i + j == s))


def top_form(expr):
    p = Poly(expand(expr), x, y)
    d = p.total_degree()
    return graded_piece(expr, d), d


def sqf_radical(expr):
    _, facs = factor_list(expand(expr), x, y)
    out = Rational(1)
    for f, _ in facs:
        out *= f
    return expand(out)
