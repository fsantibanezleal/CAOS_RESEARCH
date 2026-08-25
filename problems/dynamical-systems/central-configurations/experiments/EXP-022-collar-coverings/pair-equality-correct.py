"""THE CORRECT test of the pair-equality lemma, after a misreading.

A first attack fixed mA != mB, solved for the shape, and reported 213
refutations. That was a MISREADING and is withdrawn. The manuscript says:

  the PAIR equations factor as the mass difference times (q - v) times
  (cx^3 - cs^3), forcing PAIR-EQUAL masses whenever the two pairs sit at
  different heights

The pair equations are L34 and L56, the ones BETWEEN the two bodies of a
single mirror pair, which the six-row reduction drops precisely because
they are the ones this lemma consumes. And pair-equal means the two bodies
OF a pair carry equal mass. The lemma justifies the equal-mass-within-a-
pair ansatz; it says nothing about mA versus mB. The first attack varied
mA against mB, which the lemma never claimed, so its 213 solutions are
ordinary central configurations of the stratum and refute nothing.

The correct attack drops the ansatz. Let the four pair bodies carry
independent masses m3, m4 (pair A) and m5, m6 (pair B) on a mirror
SYMMETRIC geometry, and solve the full central-configuration system. If
any collision-free solution has m3 != m4 or m5 != m6 with v != q, the
lemma is refuted.
"""
import random
import mpmath as mp

mp.mp.dps = 40


def full_residuals(M, u, v, p, q, lam):
    """All 12 scalar central-configuration equations, no symmetry assumed
    on the masses. M = [m1, m2, m3, m4, m5, m6] for bodies
    (0,1), (0,-1), (u,v), (-u,v), (p,q), (-p,q)."""
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, v), (-u, v), (p, q), (-p, q)]
    tot = sum(M)
    cx = sum(M[i] * P[i][0] for i in range(6)) / tot
    cy = sum(M[i] * P[i][1] for i in range(6)) / tot
    out = []
    for i in range(6):
        ax = ay = mp.mpf(0)
        for j in range(6):
            if j == i:
                continue
            dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
            r2 = dx * dx + dy * dy
            if r2 <= 0:
                return None
            r3 = r2 ** mp.mpf("1.5")
            ax += M[j] * dx / r3
            ay += M[j] * dy / r3
        out.append(ax + lam * (P[i][0] - cx))
        out.append(ay + lam * (P[i][1] - cy))
    return out


print("STEP 1. Are the first attack solutions genuine central")
print("configurations? Checking one against ALL TWELVE equations.")
M = [mp.mpf("3.7"), mp.mpf("1.5"), mp.mpf("2.4"), mp.mpf("2.4"),
     mp.mpf("7.68"), mp.mpf("7.68")]
u = mp.mpf("0.697575")
v = mp.mpf("-1.023165")
p = mp.mpf("1.977645")
q = mp.mpf("-1.160525")


def refine(M, x0):
    def F(u_, v_, p_, q_, l_):
        r = full_residuals(M, u_, v_, p_, q_, l_)
        if r is None:
            return [mp.mpf(1e6)] * 5
        return [r[1], r[3], r[4], r[5], r[8]]
    return mp.findroot(F, x0, tol=mp.mpf(10) ** -30, maxsteps=200)


s = refine(M, [u, v, p, q, mp.mpf("0.5")])
u, v, p, q, lam = [s[i] for i in range(5)]
r = full_residuals(M, u, v, p, q, lam)
print(f"   refined shape u={float(u):.9f} v={float(v):.9f} "
      f"p={float(p):.9f} q={float(q):.9f}")
print(f"   max residual over ALL 12 equations: "
      f"{mp.nstr(max(abs(t) for t in r), 6)}")
print(f"   v - q = {mp.nstr(v - q, 8)}")
print("   So yes: an ordinary central configuration of the stratum with")
print("   mA different from mB. The lemma never forbade that.")

print()
print("STEP 2. THE CORRECT ATTACK. Drop the equal-mass-within-a-pair")
print("ansatz: let m3, m4 and m5, m6 be independent on a mirror symmetric")
print("geometry, and solve. Unknowns: the four pair masses up to scale,")
print("plus lambda, against the twelve equations.")
print()

rnd = random.Random(9091)
found = []
tried = 0
for trial in range(220):
    uu = mp.mpf(rnd.randint(6, 26)) / 10
    vv = mp.mpf(rnd.randint(-26, 26)) / 10
    pp = mp.mpf(rnd.randint(6, 26)) / 10
    qq = mp.mpf(rnd.randint(-26, 26)) / 10
    if abs(vv - qq) < mp.mpf("0.2"):
        continue
    if (uu - pp) ** 2 + (vv - qq) ** 2 < mp.mpf("0.25"):
        continue
    tried += 1
    # unknowns: m2, m3, m4, m5, m6, lambda  (m1 fixed to 1 by scale)
    def G(m2, m3, m4, m5, m6, l_):
        MM = [mp.mpf(1), m2, m3, m4, m5, m6]
        r = full_residuals(MM, uu, vv, pp, qq, l_)
        if r is None:
            return [mp.mpf(1e6)] * 6
        # six independent equations: y at bodies 0,1,2,4 and x at 2,4
        return [r[1], r[3], r[5], r[9], r[4], r[8]]
    x0 = [mp.mpf(rnd.randint(5, 25)) / 10 for _ in range(5)] + \
         [mp.mpf(rnd.randint(1, 20)) / 10]
    try:
        s = mp.findroot(G, x0, tol=mp.mpf(10) ** -28, maxsteps=200)
    except Exception:
        continue
    m2, m3, m4, m5, m6, lam = [s[i] for i in range(6)]
    MM = [mp.mpf(1), m2, m3, m4, m5, m6]
    if min(MM) <= 0:
        continue
    r = full_residuals(MM, uu, vv, pp, qq, lam)
    if r is None or max(abs(t) for t in r) > mp.mpf(10) ** -25:
        continue
    d34 = abs(m3 - m4)
    d56 = abs(m5 - m6)
    found.append((uu, vv, pp, qq, MM, lam, d34, d56,
                  max(abs(t) for t in r)))

print(f"   geometries tried: {tried}")
print(f"   positive-mass solutions of the FULL system: {len(found)}")
viol = [f for f in found if f[6] > mp.mpf(10) ** -12
        or f[7] > mp.mpf(10) ** -12]
print(f"   of those, with m3 != m4 or m5 != m6: {len(viol)}")
print()
for (uu, vv, pp, qq, MM, lam, d34, d56, res) in found[:8]:
    print(f"     v-q={float(vv - qq):+7.3f}  m=("
          + ", ".join(f"{float(t):.6f}" for t in MM)
          + f")  |m3-m4|={float(d34):.2e} |m5-m6|={float(d56):.2e} "
          f"res={float(res):.1e}")
print()
if not found:
    print("   INCONCLUSIVE: the solver found no positive-mass solution.")
elif viol:
    print(f"   *** REFUTED *** {len(viol)} solutions have unequal masses")
    print("   within a mirror pair while the two pairs sit at different")
    print("   heights.")
else:
    print("   SURVIVES: every positive-mass solution of the full system on")
    print("   a mirror symmetric geometry with v != q has m3 = m4 and")
    print("   m5 = m6, to 1e-12 or better. The lemma holds where tested,")
    print("   and it is doing real work: the equal-mass-within-a-pair")
    print("   ansatz is a consequence, not an assumption.")
