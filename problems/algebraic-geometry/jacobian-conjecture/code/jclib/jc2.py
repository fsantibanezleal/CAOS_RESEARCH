"""jclib.jc2: the JC(2) certificate checker and the m = 1 bridge extractor (EXP-015).

Exact (sympy over QQ). The checker is the neutral verdict format for any claimed planar Keller
map or collision; the extractor executes the EXP-012 bridge: a collision in the 3D weighted
class o = (-1, -1, 1) over weights (1, -1, -1) yields a planar Keller counterexample.
"""
from __future__ import annotations

from sympy import Rational, expand, simplify, symbols

x, y = symbols("x y")
v, t = symbols("v t")


def check_keller2(P, Q) -> dict:
    """Exact verdict on a claimed planar Keller pair."""
    J = expand(P.diff(x) * Q.diff(y) - P.diff(y) * Q.diff(x))
    if not J.is_number:
        return {"keller": False, "reason": "det J is nonconstant", "det": str(J)}
    if J == 0:
        return {"keller": False, "reason": "det J is zero", "det": "0"}
    return {"keller": True, "det": J}


def check_collision2(P, Q, p1, p2) -> dict:
    """Exact verdict on a claimed collision certificate for (P, Q)."""
    base = check_keller2(P, Q)
    if not base["keller"]:
        return {"valid": False, **base}
    if tuple(p1) == tuple(p2):
        return {"valid": False, "reason": "points are equal"}
    i1 = tuple(simplify(c.subs({x: p1[0], y: p1[1]}, simultaneous=True)) for c in (P, Q))
    i2 = tuple(simplify(c.subs({x: p2[0], y: p2[1]}, simultaneous=True)) for c in (P, Q))
    if i1 != i2:
        return {"valid": False, "reason": "images differ", "images": (str(i1), str(i2))}
    return {"valid": True, "det": base["det"], "image": str(i1),
            "consequence": "JC(2) refuted by this certificate"}


def bridge_extract(f1_vt, f2_vt, f3_vt, X1, X2) -> dict:
    """EXP-012 m = 1 bridge: from a claimed 3D collision to the planar pair.

    Inputs: reduced data (f1, f2, f3) in (v, t) for the class F = (f1/x, f2/x, x f3) over
    weights (1, -1, -1) (invariants v = xy, t = xz), plus two claimed colliding 3D points.
    The planar pair is the reduced map (V', T') = (f1 f3, f2 f3) in the (v, t) plane; a genuine
    3D collision with distinct invariant coordinates yields a planar collision for it.
    """
    Vp = expand(f1_vt * f3_vt)
    Tp = expand(f2_vt * f3_vt)
    P2 = Vp.subs({v: x, t: y}, simultaneous=True)
    Q2 = Tp.subs({v: x, t: y}, simultaneous=True)
    pts = []
    for X in (X1, X2):
        xx, yy, zz = (Rational(X[0]), Rational(X[1]), Rational(X[2]))
        pts.append((xx * yy, xx * zz))
    if pts[0] == pts[1]:
        return {"extracted": False,
                "reason": "the two 3D points share invariants (no planar collision to extract)"}
    return {"extracted": True, "P": P2, "Q": Q2,
            "certificate": check_collision2(P2, Q2, pts[0], pts[1])}
