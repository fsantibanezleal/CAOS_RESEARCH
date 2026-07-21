"""jclib: shared exact-arithmetic objects for the Jacobian-conjecture problem.

Everything here is sympy over QQ. The announced counterexample F (Alpoge/Fable, 2026-07-19) is
the founding object; the weighted-invariant machinery is OUR reconstruction (EXP-002/EXP-003).
"""
from sympy import Matrix, Poly, Rational, expand, simplify, symbols

x, y, z = symbols("x y z")
v, t, w, lam = symbols("v t w lam")

#: u = 1 + xy, the recurring unit-like factor.
u_xy = 1 + x * y
#: u in invariant coordinates (v = xy).
u_v = 1 + v

#: The announced counterexample F = (P, Q, R).
P = u_xy**3 * z + y**2 * u_xy * (4 + 3 * x * y)
Q = y + 3 * x * u_xy**2 * z + 3 * x * y**2 * (4 + 3 * x * y)
R = 2 * x - 3 * x**2 * y - x**3 * z
F = Matrix([P, Q, R])

#: Source weights (x, y, z) -> (1, -1, -2); output weights (P, Q, R) -> (-2, -1, 1).
SOURCE_WEIGHTS = (1, -1, -2)
OUTPUT_WEIGHTS = (-2, -1, 1)


def det_JF():
    """Exact Jacobian determinant of F (expanded)."""
    return expand(F.jacobian([x, y, z]).det())


def to_invariants(expr, xpow):
    """Return expr * x**xpow rewritten as a polynomial in (v, t), or raise if not polynomial.

    Uses the substitution y = v/x, z = t/x**2 and demands full cancellation of x.
    """
    e = expand(expr.subs({y: v / x, z: t / x**2}) * x**xpow)
    e = simplify(e)
    p = Poly(e, x)
    if p.degree() != 0:
        raise ValueError(f"not x-free after weighting: {e}")
    return expand(e)


def reduced_triple():
    """(a1, b1, c1): the weight-0 reductions x^2*P, x*Q, R/x as polynomials in (v, t)."""
    a1 = to_invariants(P, 2)
    b1 = to_invariants(Q, 1)
    c1 = to_invariants(R, -1)
    return a1, b1, c1


def weighted_family_map(a1_vt, b1_vt, c1_vt):
    """Lift reduced data (a1, b1, c1) in (v, t) back to a candidate map on (x, y, z).

    Returns (P', Q', R') = (a1/x^2, b1/x, x*c1) with v = xy, t = x^2 z substituted. Components
    are returned expanded; the caller must check they are polynomials in (x, y, z).
    """
    sub = {v: x * y, t: x**2 * z}
    return (
        expand(a1_vt.subs(sub) / x**2),
        expand(b1_vt.subs(sub) / x),
        expand(x * c1_vt.subs(sub)),
    )


def is_polynomial_in_xyz(expr):
    """True iff expr is a polynomial in (x, y, z) (no negative powers survive)."""
    try:
        Poly(expand(expr), x, y, z)
        return True
    except Exception:
        return False


# ---- Constructor v2 (potential form), derived in EXP-003's failure analysis, verified in EXP-004


def seed_data(p_expr):
    """(h, Phi, p(1), p'(1)) for a seed polynomial p in w with p(0) = 0."""
    from sympy import cancel, integrate
    h = cancel(p_expr / w)
    Phi = integrate(p_expr, (w, 0, w))
    p1v = p_expr.subs(w, 1)
    dp1v = p_expr.diff(w).subs(w, 1)
    return h, Phi, p1v, dp1v


def constructor_v2(p_expr, kk, q_tail=0):
    """Build reduced data (a1, b1, c1) in (v, t) from seed p, scale k, optional q-tail.

    Requires p(0) = 0, integral_0^1 p = 0, p(1) != 0, p'(1) != 2 p(1). q_tail is a polynomial in
    v with valuation >= 2 (free higher section terms). Returns (a1, b1, c1, params dict).
    """
    from sympy import Rational, cancel, expand, integrate
    h, Phi, p1v, dp1v = seed_data(p_expr)
    assert p_expr.subs(w, 0) == 0, "seed must vanish at 0"
    assert integrate(p_expr, (w, 0, 1)) == 0, "seed must satisfy integral_0^1 p = 0"
    assert p1v != 0, "seed must have p(1) != 0"
    assert dp1v - 2 * p1v != 0, "seed must have p'(1) != 2 p(1)"
    beta = cancel(kk * (p1v - dp1v) / (dp1v - 2 * p1v))
    mm = -kk * p1v
    q = kk + beta * v + q_tail
    c1 = q - t
    warg = u_v * c1 / kk
    b1 = expand(cancel(kk**2 * p_expr.subs(w, warg) / c1) + mm)
    a1 = expand(cancel(u_v * b1 / kk) - cancel(kk**2 * Phi.subs(w, warg) / c1**2))
    return a1, b1, c1, {"k": kk, "m": mm, "beta": beta, "q": q, "h": h, "Phi": Phi,
                        "p1": p1v, "det_pred": cancel(-mm**2 / kk)}
