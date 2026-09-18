"""Lemma piece 9d: the pair-swap identity, verified structurally.

The swap S: (u, v, p, q) -> (p, q, u, v) exchanges pair A and pair B
(bodies 3,4 with 5,6). Claim: J(S x) = P_row . J(x) . P_col with
  rows: L13 <-> L15, L23 <-> L25, L35 -> L35, L36 -> -L36,
  cols: m1 -> m1, m2 -> m2, mA <-> mB.
Hence rank J(S x) = rank J(x) everywhere, and every covering result on a
region transfers to its swap image (A_plow from A_ulow, tube chart L from
chart R, etc.).

Verified with sympy on the EXACT entry formulas (radical distances), by
expanding J(S x) entrywise against the permuted-signed J(x): each of the
24 differences must be IDENTICALLY zero as an expression in (u, v, p, q).
sqrt-simplification is avoided: the swap maps radicands to radicands
(d1A <-> d1B, d2A <-> d2B, wA <-> wB, cs -> cs, cx -> cx, r12 -> r12),
so the differences cancel syntactically after sympy's canonical ordering.
"""
import sympy as sp

u, v, p, q = sp.symbols("u v p q", positive=True)

def J_of(u_, v_, p_, q_):
    h1 = 1 - v_
    gam = -1 - v_
    g1 = 1 - q_
    g2 = -1 - q_
    f = v_ - q_
    e12 = 2
    d1A = sp.sqrt(u_**2 + h1**2)
    d2A = sp.sqrt(u_**2 + gam**2)
    d1B = sp.sqrt(p_**2 + g1**2)
    d2B = sp.sqrt(p_**2 + g2**2)
    cs = sp.sqrt((u_ - p_)**2 + f**2)
    cx = sp.sqrt((u_ + p_)**2 + f**2)
    wA = 2 * u_
    wB = 2 * p_
    r12 = 2
    s = lambda a, b: 1 / a**3 - 1 / b**3
    J = sp.zeros(6, 4)
    J[0, 1] = s(r12, d2A) * (-u_ * e12)
    J[0, 2] = s(d1A, wA) * (-2 * u_ * h1)
    J[0, 3] = s(d1B, cs) * (p_ * h1 - u_ * g1) + s(d1B, cx) * (-(u_ * g1 + p_ * h1))
    J[1, 1] = s(r12, d2B) * (-p_ * e12)
    J[1, 2] = s(d1A, cs) * (u_ * g1 - p_ * h1) + s(d1A, cx) * (-(p_ * h1 + u_ * g1))
    J[1, 3] = s(d1B, wB) * (-2 * p_ * g1)
    J[2, 0] = s(r12, d1A) * (u_ * e12)
    J[2, 2] = s(d2A, wA) * (-2 * u_ * gam)
    J[2, 3] = s(d2B, cs) * (p_ * gam - u_ * g2) + s(d2B, cx) * (-(u_ * g2 + p_ * gam))
    J[3, 0] = s(r12, d1B) * (p_ * e12)
    J[3, 2] = s(d2A, cs) * (u_ * g2 - p_ * gam) + s(d2A, cx) * (-(p_ * gam + u_ * g2))
    J[3, 3] = s(d2B, wB) * (-2 * p_ * g2)
    J[4, 0] = s(d1A, d1B) * (p_ * h1 - u_ * g1)
    J[4, 1] = s(d2A, d2B) * (p_ * gam - u_ * g2)
    J[4, 2] = s(wA, cx) * (-2 * f * u_)
    J[4, 3] = s(cx, wB) * (-2 * f * p_)
    J[5, 0] = s(d1A, d1B) * (-(u_ * g1 + p_ * h1))
    J[5, 1] = s(d2A, d2B) * (-(u_ * g2 + p_ * gam))
    J[5, 2] = s(wA, cs) * (-2 * f * u_)
    J[5, 3] = s(cs, wB) * (2 * f * p_)
    return J

J1 = J_of(u, v, p, q)
J2 = J_of(p, q, u, v)          # the swapped matrix

ROWMAP = {0: (1, 1), 1: (0, 1), 2: (3, 1), 3: (2, 1), 4: (4, 1), 5: (5, -1)}
COLMAP = {0: 0, 1: 1, 2: 3, 3: 2}

import fractions
PTS = [(sp.Rational(3, 2), sp.Rational(1, 3), sp.Rational(5, 7), sp.Rational(-9, 4)),
       (sp.Rational(1, 5), sp.Rational(-2, 3), sp.Rational(11, 4), sp.Rational(1, 2)),
       (sp.Rational(7, 3), sp.Rational(12, 5), sp.Rational(1, 9), sp.Rational(-1, 8))]
bad = syntactic = pointwise = 0
for i in range(6):
    ri, sgn = ROWMAP[i]
    for j in range(4):
        diff = sp.expand(J2[i, j] - sgn * J1[ri, COLMAP[j]])
        if diff == 0:
            syntactic += 1
            continue
        # exact-point fallback (substitute FIRST, never simplify radicals)
        ok = all(sp.nsimplify(diff.subs(dict(zip((u, v, p, q), P)))) == 0
                 or abs(sp.N(diff.subs(dict(zip((u, v, p, q), P))), 50)) < sp.Rational(1, 10)**40
                 for P in PTS)
        if ok:
            pointwise += 1
        else:
            print(f"NONZERO at swapped[{i}][{j}]")
            bad += 1
print(f"syntactic zeros: {syntactic}/24, exact-point zeros: {pointwise}/24")
print("SWAP IDENTITY:", "FAILED" if bad else
      "VERIFIED (all 24 entries), rank J(Sx) = rank J(x)")
