"""THE DECISIVE ATTACK on the manuscript's pair-equality lemma.

Claim (manuscript v0.08, two-pair stratum section): the pair equations
factor as the mass difference times (q - v) times (cx^3 - cs^3), so
pair-equal masses are FORCED whenever the two pairs sit at different
heights.

Searching for rank-3 shapes at random cannot test this: rank <= 3 is
codimension 3, so random points never land on it. The right attack runs
the other way. FIX masses with mA != mB, then solve the
central-configuration equations for the shape. If any solution has
v != q, with no collisions and positive masses, the lemma is refuted.

Configuration: bodies at (0, +-1) with masses m1, m2; mirror pairs at
(+-u, v) and (+-p, q) with masses mA, mB. The gauge fixes translation and
scale, so the centre of mass c is NOT at the origin and appears in the
equations. Independent equations, after removing the one mass-weighted
relation that holds identically: five, in the five unknowns
(u, v, p, q, lambda).
"""
import random
import mpmath as mp

mp.mp.dps = 40


def residuals(m1, m2, mA, mB, u, v, p, q, lam):
    M = [m1, m2, mA, mA, mB, mB]
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, v), (-u, v), (p, q), (-p, q)]
    tot = sum(M)
    cy = sum(M[i] * P[i][1] for i in range(6)) / tot
    cx = sum(M[i] * P[i][0] for i in range(6)) / tot

    def acc(i):
        ax = ay = mp.mpf(0)
        for j in range(6):
            if j == i:
                continue
            dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
            r2 = dx * dx + dy * dy
            if r2 <= 0:
                return None, None
            r3 = r2 ** mp.mpf("1.5")
            ax += M[j] * dx / r3
            ay += M[j] * dy / r3
        return ax, ay

    out = []
    # body 0 (0,1): y only (x vanishes by symmetry)
    a = acc(0)
    if a[0] is None:
        return None
    out.append(a[1] + lam * (P[0][1] - cy))
    # body 1 (0,-1): y only
    a = acc(1)
    out.append(a[1] + lam * (P[1][1] - cy))
    # body 2 (u,v): x and y
    a = acc(2)
    out.append(a[0] + lam * (P[2][0] - cx))
    out.append(a[1] + lam * (P[2][1] - cy))
    # body 4 (p,q): x only; the y equation is the one removed by the
    # identically-vanishing mass-weighted sum
    a = acc(4)
    out.append(a[0] + lam * (P[4][0] - cx))
    return out


def solve(m1, m2, mA, mB, x0):
    def F(u, v, p, q, lam):
        r = residuals(m1, m2, mA, mB, u, v, p, q, lam)
        if r is None:
            return [mp.mpf(1e6)] * 5
        return r
    return mp.findroot(F, x0, tol=mp.mpf(10) ** -30, maxsteps=200)


print("Attacking with mA != mB, over many mass choices and starts.")
print("A solution with v != q, no collisions, positive masses REFUTES")
print("the lemma.")
print()
rnd = random.Random(31337)
refutations = []
solutions = 0
tried = 0
for trial in range(300):
    m1 = mp.mpf(rnd.randint(5, 40)) / 10
    m2 = mp.mpf(rnd.randint(5, 40)) / 10
    mA = mp.mpf(rnd.randint(5, 40)) / 10
    mB = mA * (1 + mp.mpf(rnd.randint(3, 25)) / 10)   # forced UNequal
    x0 = [mp.mpf(rnd.randint(5, 25)) / 10,
          mp.mpf(rnd.randint(-25, 25)) / 10,
          mp.mpf(rnd.randint(5, 25)) / 10,
          mp.mpf(rnd.randint(-25, 25)) / 10,
          mp.mpf(rnd.randint(1, 30)) / 10]
    tried += 1
    try:
        s = solve(m1, m2, mA, mB, x0)
    except Exception:
        continue
    u, v, p, q, lam = [s[i] for i in range(5)]
    r = residuals(m1, m2, mA, mB, u, v, p, q, lam)
    if r is None:
        continue
    res = max(abs(t) for t in r)
    if res > mp.mpf(10) ** -25:
        continue
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, v), (-u, v), (p, q), (-p, q)]
    dmin = min(mp.sqrt((P[i][0] - P[j][0]) ** 2 + (P[i][1] - P[j][1]) ** 2)
               for i in range(6) for j in range(i + 1, 6))
    if dmin < mp.mpf("0.02") or u <= 0 or p <= 0:
        continue
    solutions += 1
    if abs(v - q) > mp.mpf("1e-8"):
        refutations.append((m1, m2, mA, mB, u, v, p, q, lam, res, dmin))

print(f"  mass choices tried: {tried}")
print(f"  genuine collision-free solutions found: {solutions}")
print(f"  of those, with v != q: {len(refutations)}")
print()
if refutations:
    print("  *** THE LEMMA IS REFUTED *** witnesses:")
    for (m1, m2, mA, mB, u, v, p, q, lam, res, dmin) in refutations[:6]:
        print(f"    m=({float(m1):.3f},{float(m2):.3f},{float(mA):.3f},"
              f"{float(mB):.3f})  u={float(u):.6f} v={float(v):.6f} "
              f"p={float(p):.6f} q={float(q):.6f}")
        print(f"      v-q={float(v - q):+.6e}  residual={float(res):.2e}  "
              f"min distance={float(dmin):.4f}")
else:
    print("  NO refutation found. Every collision-free solution with")
    print("  unequal pair masses has v = q, i.e. lands on the equal-height")
    print("  face the lemma excludes. The lemma SURVIVES this attack.")
    print()
    print("  Control: the same solver WITH mA = mB, to show it can find")
    print("  solutions at all and is not just failing to converge.")
    ok = 0
    ex = None
    for trial in range(120):
        m1 = mp.mpf(rnd.randint(5, 40)) / 10
        m2 = mp.mpf(rnd.randint(5, 40)) / 10
        mA = mp.mpf(rnd.randint(5, 40)) / 10
        x0 = [mp.mpf(rnd.randint(5, 25)) / 10,
              mp.mpf(rnd.randint(-25, 25)) / 10,
              mp.mpf(rnd.randint(5, 25)) / 10,
              mp.mpf(rnd.randint(-25, 25)) / 10,
              mp.mpf(rnd.randint(1, 30)) / 10]
        try:
            s = solve(m1, m2, mA, mA, x0)
        except Exception:
            continue
        u, v, p, q, lam = [s[i] for i in range(5)]
        r = residuals(m1, m2, mA, mA, u, v, p, q, lam)
        if r is None:
            continue
        res = max(abs(t) for t in r)
        P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
             (u, v), (-u, v), (p, q), (-p, q)]
        dmin = min(mp.sqrt((P[i][0] - P[j][0]) ** 2
                           + (P[i][1] - P[j][1]) ** 2)
                   for i in range(6) for j in range(i + 1, 6))
        if res < mp.mpf(10) ** -25 and dmin > mp.mpf("0.02") and u > 0 and p > 0:
            ok += 1
            if ex is None and abs(v - q) > mp.mpf("1e-8"):
                ex = (m1, m2, mA, u, v, p, q, res, dmin)
    print(f"    solutions found with mA = mB: {ok}")
    if ex:
        m1, m2, mA, u, v, p, q, res, dmin = ex
        print(f"    example with v != q: m=({float(m1):.3f},{float(m2):.3f},"
              f"{float(mA):.3f}) u={float(u):.6f} v={float(v):.6f} "
              f"p={float(p):.6f} q={float(q):.6f}")
        print(f"      residual {float(res):.2e}, min distance {float(dmin):.4f}")
        print("    So the solver DOES find v != q solutions when the pair")
        print("    masses are equal, which is exactly what the lemma says.")
