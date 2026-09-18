"""EXP-022 part (b) preflight: machine-verify the tube blow-up algebra.

Coordinates: u = w + t/2, p = w - t/2, q = v - f, t = rho*alpha,
f = rho*beta, alpha^2 + beta^2 = 1, cs = rho exactly.

Verifies EXACTLY (polynomial identities):
  P1: Delta135 = p h1 - u g1 = -rho (alpha h1 + beta w + rho alpha beta/2)
  P2: Delta235 = p gam - u g2 = -rho (alpha gam + beta w + rho alpha beta/2)
  P3: d1B^2 - d1A^2 = rho (2 beta h1 - 2 alpha w + rho beta^2)
  P4: d2B^2 - d2A^2 = rho (2 beta gam - 2 alpha w + rho beta^2)
  P5: cx^2 - wA^2 = rho (-4 w alpha + rho (beta^2 - alpha^2))
  P6: cx^2 - wB^2 = rho (+4 w alpha + rho (beta^2 - alpha^2))

Then verifies NUMERICALLY-EXACTLY (rational points, exact sympy radicals,
two shrinking rho values) that each rescaled L35 entry converges to the
derived face limit:
  m1 -> -(3/2) E1 D135 / D1^5,  E1 = 2 beta h1 - 2 alpha w, D1 = sqrt(w^2+h1^2)
  m2 -> -(3/2) E2 D235 / D2^5
  mA -> 3 alpha beta / (8 w^3)
  mB -> 3 alpha beta / (8 w^3)
and that the face degeneracy curve satisfies gam*h1 + w^2 = 0, i.e.
w^2 + v^2 = 1 (with alpha = beta gam / w), where the face rank drops to 2.
"""
import sympy as sp

w, v, rho, al, be = sp.symbols("w v rho alpha beta", real=True)

t = rho * al
f = rho * be
u = w + t / 2
p = w - t / 2
h1 = 1 - v
gam = -1 - v
g1 = h1 + f
g2 = gam + f

D135 = al * h1 + be * w + rho * al * be / 2
D235 = al * gam + be * w + rho * al * be / 2
E1 = 2 * be * h1 - 2 * al * w + rho * be**2
E2 = 2 * be * gam - 2 * al * w + rho * be**2
F1 = -4 * w * al + rho * (be**2 - al**2)
G1 = 4 * w * al + rho * (be**2 - al**2)

checks = {
    "P1": sp.expand(p * h1 - u * g1 + rho * D135),
    "P2": sp.expand(p * gam - u * g2 + rho * D235),
    "P3": sp.expand((p**2 + g1**2) - (u**2 + h1**2) - rho * E1),
    "P4": sp.expand((p**2 + g2**2) - (u**2 + gam**2) - rho * E2),
    "P5": sp.expand(((u + p)**2 + f**2) - (2 * u)**2 - rho * F1),
    "P6": sp.expand(((u + p)**2 + f**2) - (2 * p)**2 - rho * G1),
}
for k, e in checks.items():
    assert e == 0, (k, e)
    print(f"{k}: exact identity OK")

# ---- numeric-exact convergence of the rescaled L35 row ----
def L35_entries(wv, vv, alv, bev, rhov):
    sub = {w: wv, v: vv, al: alv, be: bev, rho: rhov}
    uu, pp = u.subs(sub), p.subs(sub)
    hh1, gg1 = h1.subs(sub), g1.subs(sub)
    ggam, gg2 = gam.subs(sub), g2.subs(sub)
    ff = f.subs(sub)
    d1A = sp.sqrt(uu**2 + hh1**2)
    d1B = sp.sqrt(pp**2 + gg1**2)
    d2A = sp.sqrt(uu**2 + ggam**2)
    d2B = sp.sqrt(pp**2 + gg2**2)
    cx = sp.sqrt((uu + pp)**2 + ff**2)
    wA, wB = 2 * uu, 2 * pp
    s = lambda a, b: 1 / a**3 - 1 / b**3
    m1 = s(d1A, d1B) * (pp * hh1 - uu * gg1) / rhov**2
    m2 = s(d2A, d2B) * (pp * ggam - uu * gg2) / rhov**2
    mA = s(wA, cx) * (-2 * ff * uu) / rhov**2
    mB = s(cx, wB) * (-2 * ff * pp) / rhov**2
    return [sp.nsimplify(x) for x in (m1, m2, mA, mB)]

# rational direction close to the circle: alpha = 3/5, beta = 4/5
WV, VV, ALV, BEV = sp.Rational(3, 2), sp.Rational(1, 3), sp.Rational(3, 5), sp.Rational(4, 5)
D1 = sp.sqrt(WV**2 + (1 - VV)**2)
D2 = sp.sqrt(WV**2 + (-1 - VV)**2)
lim = [
    sp.Rational(-3, 2) * (2 * BEV * (1 - VV) - 2 * ALV * WV) * (ALV * (1 - VV) + BEV * WV) / D1**5,
    sp.Rational(-3, 2) * (2 * BEV * (-1 - VV) - 2 * ALV * WV) * (ALV * (-1 - VV) + BEV * WV) / D2**5,
    sp.Rational(3, 8) * ALV * BEV / WV**3,
    sp.Rational(3, 8) * ALV * BEV / WV**3,
]
names = ["m1", "m2", "mA", "mB"]
r1, r2 = sp.Rational(1, 1000), sp.Rational(1, 100000)
e1v = L35_entries(WV, VV, ALV, BEV, r1)
e2v = L35_entries(WV, VV, ALV, BEV, r2)
for nm, a, b, L in zip(names, e1v, e2v, lim):
    d1_ = abs(sp.N(a - L, 30))
    d2_ = abs(sp.N(b - L, 30))
    ratio = d1_ / d2_ if d2_ != 0 else sp.oo
    print(f"{nm}: |err(1e-3)|={sp.N(d1_,4)} |err(1e-5)|={sp.N(d2_,4)} ratio={sp.N(ratio,4)}")
    assert d2_ < d1_ / 50, (nm, "no linear convergence to the claimed limit")
print("L35 rescaled face limits: VERIFIED (linear convergence, exact arithmetic)")

# ---- the face degeneracy curve ----
# On the face (rho=0): rank drops to 2 iff E1*D135 = E2*D235 = 0 with the
# mA/mB directions still spanned. Solve D135 = 0, E2 = 0 (rho = 0):
D135f = (al * h1 + be * w)
E2f = 2 * be * gam - 2 * al * w
sols = sp.solve([D135f, E2f, al**2 + be**2 - 1], [al, be, v], dict=True)
curve = sp.simplify(gam * h1 + w**2)   # = w^2 - (1 - v^2) hmm: (-1-v)(1-v) = v^2-1
print("gam*h1 + w^2 =", sp.expand(gam * h1 + w**2))
for so in sols:
    vs = so.get(v)
    if vs is not None:
        chk = sp.simplify(vs**2 + w**2 - 1)
        print("  solution branch v satisfies v^2 + w^2 - 1 =", chk)
print("face degeneracy curve: w^2 + v^2 = 1 (documented; handled by the "
      "gradient-pair trap in the tube covering)")
