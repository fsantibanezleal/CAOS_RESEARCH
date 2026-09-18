"""Identify the band's degeneracy locus exactly.

The 44 stubborn boxes cluster at v = q = 0 (the cross configurations:
bodies 1,2 at (0,+-1), pair A at (+-u, 0), pair B at (+-p, 0)) around
(u, p) ~ (1.45, 0.63) and the swap image. On the v = q = 0 slice compute
J(u, 0, p, 0) symbolically, extract all 3x3 minors, and find the curve in
(u, p) where rank <= 2.

At v = q = 0: h1 = g1 = 1, gam = g2 = -1, f = 0, d1A = d2A = sqrt(u^2+1),
d1B = d2B = sqrt(p^2+1), cs = |u - p|, cx = u + p (u, p > 0). Rows L35 and
L36 both become proportional to earlier structure; the matrix simplifies
enough for exact minor analysis.
"""
import sympy as sp
from itertools import combinations

u, p = sp.symbols("u p", positive=True)

dA = sp.sqrt(u**2 + 1)
dB = sp.sqrt(p**2 + 1)
cs = u - p          # SIGNED: valid chart u > p (the cluster has u > p);
                    # the u < p branch is the swap image (piece 9d)
cx = u + p
wA = 2 * u
wB = 2 * p
r12 = 2
s = lambda a, b: 1 / a**3 - 1 / b**3

# entries at v = q = 0 from the verified table:
J = sp.zeros(6, 4)
J[0, 1] = s(r12, dA) * (-2 * u)
J[0, 2] = s(dA, wA) * (-2 * u)
J[0, 3] = s(dB, cs) * (p - u) + s(dB, cx) * (-(u + p))
J[1, 1] = s(r12, dB) * (-2 * p)
J[1, 2] = s(dA, cs) * (u - p) + s(dA, cx) * (-(p + u))
J[1, 3] = s(dB, wB) * (-2 * p)
J[2, 0] = s(r12, dA) * (2 * u)
J[2, 2] = s(dA, wA) * (2 * u)          # gam = -1: (-2*u*gam) = 2u
J[2, 3] = s(dB, cs) * (-p + u) + s(dB, cx) * ((u + p))   # pgam - ug2 = -p + u; -(ug2+pgam) = u + p
J[3, 0] = s(r12, dB) * (2 * p)
J[3, 2] = s(dA, cs) * (-u + p) + s(dA, cx) * ((p + u))
J[3, 3] = s(dB, wB) * (2 * p)
J[4, 0] = s(dA, dB) * (p - u)
J[4, 1] = s(dA, dB) * (-p + u)         # pgam - ug2 = u - p ... times s(d2A,d2B)=s(dA,dB)
J[4, 2] = 0
J[4, 3] = 0
J[5, 0] = s(dA, dB) * (-(u + p))
J[5, 1] = s(dA, dB) * (-(-u - p))      # -(ug2+pgam) = u+p
J[5, 2] = 0
J[5, 3] = 0

# sanity: numeric rank at the cluster point (1.4507, 0.6299)
Jn = sp.Matrix(6, 4, lambda i, j: J[i, j].subs({u: sp.Rational(14507, 10000), p: sp.Rational(6299, 10000)}))
print("rank at cluster point:", Jn.rank())
# and at a generic cross point
Jg = sp.Matrix(6, 4, lambda i, j: J[i, j].subs({u: sp.Rational(2), p: sp.Rational(1, 2)}))
print("rank at generic cross point (2, 1/2):", Jg.rank())

# all 3x3 minors: find the common vanishing curve near the cluster.
# strategy: the minors are radical expressions; sample the candidate curve
# by solving minor = 0 numerically in p for fixed u, for TWO independent
# minors, and check the roots agree (=> a genuine rank<=2 curve), then
# characterize: try simple laws (u*p = c? dA/dB law? s-relations?).
rows = list(range(6))
cols = list(range(4))
minors = []
for rr in combinations(rows, 3):
    for cc in combinations(cols, 3):
        m = J[rr[0], cc[0]] * (J[rr[1], cc[1]] * J[rr[2], cc[2]] - J[rr[1], cc[2]] * J[rr[2], cc[1]]) \
            - J[rr[0], cc[1]] * (J[rr[1], cc[0]] * J[rr[2], cc[2]] - J[rr[1], cc[2]] * J[rr[2], cc[0]]) \
            + J[rr[0], cc[2]] * (J[rr[1], cc[0]] * J[rr[2], cc[1]] - J[rr[1], cc[1]] * J[rr[2], cc[0]])
        minors.append(((rr, cc), m))

import mpmath as mp
mp.mp.dps = 40
UVAL = mp.mpf("1.4507")
roots = []
for (rc, m) in minors:
    fm = sp.lambdify(p, m.subs(u, sp.Rational(14507, 10000)), "mpmath")
    try:
        r = mp.findroot(fm, mp.mpf("0.63"))
        if 0.55 < r < 0.72:
            roots.append((rc, r))
    except Exception:
        pass
vals = sorted(set(round(float(r), 8) for _, r in roots))
print(f"{len(roots)} minors vanish near p~0.63 at u=1.4507; distinct roots: {vals[:6]}")
if roots:
    r0 = roots[0][1]
    print("candidate p at u=1.4507:", mp.nstr(r0, 20))
    print("  u*p =", mp.nstr(UVAL * r0, 15))
    print("  (u^2+1)(p^2+1) =", mp.nstr((UVAL**2 + 1) * (r0**2 + 1), 15))
    print("  u - p =", mp.nstr(UVAL - r0, 15), "  u + p =", mp.nstr(UVAL + r0, 15))
    print("  dA =", mp.nstr(mp.sqrt(UVAL**2 + 1), 15), " dB =", mp.nstr(mp.sqrt(r0**2 + 1), 15))
    print("  dA*dB =", mp.nstr(mp.sqrt(UVAL**2 + 1) * mp.sqrt(r0**2 + 1), 15))
    print("  dA/dB =", mp.nstr(mp.sqrt(UVAL**2 + 1) / mp.sqrt(r0**2 + 1), 15))
