"""Decide: exact rank-2 point vs conditioning near-miss at the cross slice.

Two independent minors' zero curves in p at fixed u (v = q = 0, chart
u > p): if their roots differ beyond error, there is NO common zero on
this slice line. Then scan a 2-parameter family (p, t) with v = q = t
(f = 0 kept: the cluster is on the equal-heights slice) at fixed u: solve
minor_i = 0, minor_j = 0 jointly; a solution means a genuine rank <= 2
point ON f = 0 (off-stratum, harmless to the theorem, but a discovery for
the record); no solution means a near-miss cluster.
"""
import sympy as sp
import mpmath as mp
from itertools import combinations

mp.mp.dps = 50
u, p, t = sp.symbols("u p t", real=True)

def J_cross(uv, pv=None, tv=None):
    """Symbolic J at v = q = t (f = 0)."""
    h1 = 1 - t
    gam = -1 - t
    dA1 = sp.sqrt(u**2 + h1**2)
    dA2 = sp.sqrt(u**2 + gam**2)
    dB1 = sp.sqrt(p**2 + h1**2)   # g1 = h1, g2 = gam at q = v = t
    dB2 = sp.sqrt(p**2 + gam**2)
    cs = u - p
    cx = u + p
    wA, wB, r12 = 2 * u, 2 * p, 2
    s = lambda a, b: 1 / a**3 - 1 / b**3
    J = sp.zeros(6, 4)
    J[0, 1] = s(r12, dA2) * (-2 * u)
    J[0, 2] = s(dA1, wA) * (-2 * u * h1)
    J[0, 3] = s(dB1, cs) * (p * h1 - u * h1) + s(dB1, cx) * (-(u * h1 + p * h1))
    J[1, 1] = s(r12, dB2) * (-2 * p)
    J[1, 2] = s(dA1, cs) * (u * h1 - p * h1) + s(dA1, cx) * (-(p * h1 + u * h1))
    J[1, 3] = s(dB1, wB) * (-2 * p * h1)
    J[2, 0] = s(r12, dA1) * (2 * u)
    J[2, 2] = s(dA2, wA) * (-2 * u * gam)
    J[2, 3] = s(dB2, cs) * (p * gam - u * gam) + s(dB2, cx) * (-(u * gam + p * gam))
    J[3, 0] = s(r12, dB1) * (2 * p)
    J[3, 2] = s(dA2, cs) * (u * gam - p * gam) + s(dA2, cx) * (-(p * gam + u * gam))
    J[3, 3] = s(dB2, wB) * (-2 * p * gam)
    J[4, 0] = s(dA1, dB1) * (p * h1 - u * h1)
    J[4, 1] = s(dA2, dB2) * (p * gam - u * gam)
    J[4, 2] = 0
    J[4, 3] = 0
    J[5, 0] = s(dA1, dB1) * (-(u * h1 + p * h1))
    J[5, 1] = s(dA2, dB2) * (-(u * gam + p * gam))
    J[5, 2] = 0
    J[5, 3] = 0
    return J

J = J_cross(u)

def minor(rr, cc):
    M = sp.Matrix(3, 3, lambda i, j: J[rr[i], cc[j]])
    return M.det()

M1 = minor((0, 1, 2), (1, 2, 3))
M2 = minor((1, 2, 3), (0, 1, 2))
M3 = minor((0, 2, 4), (0, 1, 2))

UV = sp.Rational(14507, 10000)

# 1) exact root separation on the t = 0 line
f1 = sp.lambdify(p, M1.subs({u: UV, t: 0}), "mpmath")
f2 = sp.lambdify(p, M2.subs({u: UV, t: 0}), "mpmath")
f3 = sp.lambdify(p, M3.subs({u: UV, t: 0}), "mpmath")
r1 = mp.findroot(f1, mp.mpf("0.63"))
r2 = mp.findroot(f2, mp.mpf("0.63"))
r3 = mp.findroot(f3, mp.mpf("0.63"))
print("root M1:", mp.nstr(r1, 25))
print("root M2:", mp.nstr(r2, 25))
print("root M3:", mp.nstr(r3, 25))
print("|r1-r2| =", mp.nstr(abs(r1 - r2), 5), " |r1-r3| =", mp.nstr(abs(r1 - r3), 5))

# 2) joint solve in (p, t) at fixed u: does a common zero exist off t-axis?
g1 = sp.lambdify((p, t), M1.subs(u, UV), "mpmath")
g2 = sp.lambdify((p, t), M2.subs(u, UV), "mpmath")
try:
    sol = mp.findroot(lambda P, T: (g1(P, T), g2(P, T)),
                      (mp.mpf("0.63"), mp.mpf("0.0")))
    P0, T0 = sol
    print("joint (M1,M2) solution: p =", mp.nstr(P0, 20), " t =", mp.nstr(T0, 20))
    v3 = g1(P0, T0), g2(P0, T0), sp.lambdify((p, t), M3.subs(u, UV), "mpmath")(P0, T0)
    print("residuals M1,M2 and value of M3 there:", [mp.nstr(abs(x), 5) for x in v3])
except Exception as e:
    print("joint solve failed:", e)
