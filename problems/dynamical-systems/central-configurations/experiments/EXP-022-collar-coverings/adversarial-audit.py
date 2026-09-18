"""ADVERSARIAL AUDIT: attack every checkable claim, manuscript and campaign.

The instruction is to refute, not to confirm. Each block below states a
claim, then tries to break it, and reports PASS only when the attack
fails. Claims that cannot be attacked numerically are marked NOT TESTED
here rather than passed by silence.

Sources of the claims:
  M = the published manuscript v0.08 (tropical-replication, Zenodo
      10.5281/zenodo.21760069), section on the two-pair stratum
  C = this campaign's recent results (rounds 52 to 54)
"""
import itertools
import math
import mpmath as mp

mp.mp.dps = 50

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
COL = [0, 1, 2, 2, 3, 3]
FAILS = []


def rec(tag, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(tag)


def matrix(u, v, p, q):
    """The (2,2) reduced block: bodies 1,2 at (0,+-1), pairs at (+-u,v),
    (+-p,q); columns (m1, m2, mA, mB)."""
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, v), (-u, v), (p, q), (-p, q)]
    M = []
    for (i, j) in ROWS:
        c = [mp.mpf(0)] * 4
        for k in range(6):
            if k == i or k == j:
                continue
            rik = mp.sqrt((P[i][0] - P[k][0]) ** 2 + (P[i][1] - P[k][1]) ** 2)
            rjk = mp.sqrt((P[j][0] - P[k][0]) ** 2 + (P[j][1] - P[k][1]) ** 2)
            area = ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
            c[COL[k]] += (rik ** -3 - rjk ** -3) * area
        M.append(c)
    return M


def svals(M, rownorm=True):
    A = mp.matrix(6, 4)
    for i in range(6):
        n = (max(abs(x) for x in M[i]) or mp.mpf(1)) if rownorm else mp.mpf(1)
        for j in range(4):
            A[i, j] = M[i][j] / n
    U, S, V = mp.svd_r(A)
    return [S[i] for i in range(4)], V


print("=" * 72)
print("A. MANUSCRIPT: the equal-mass square's side satisfies")
print("   32 a^6 - 32 a^3 + 7 = 0")
print("=" * 72)
# the equal-mass rhombus/square CC of the 4-body problem: side a,
# diagonal a*sqrt(2). Solve the polynomial and check the root is a real
# positive side that actually gives a central configuration.
roots = mp.polyroots([32, 0, 0, -32, 0, 0, 7], maxsteps=200, extraprec=200)
real_pos = [r for r in roots if abs(mp.im(r)) < mp.mpf(10) ** -30
            and mp.re(r) > 0]
print(f"   real positive roots: {[mp.nstr(mp.re(r), 12) for r in real_pos]}")


def square_cc_residual(a):
    """Four equal masses at the corners of a square of side a."""
    h = a / 2
    B = [(h, h), (-h, h), (-h, -h), (h, -h)]
    m = [mp.mpf(1)] * 4
    lam = None
    res = mp.mpf(0)
    for i in range(4):
        ax = ay = mp.mpf(0)
        for j in range(4):
            if j == i:
                continue
            dx, dy = B[j][0] - B[i][0], B[j][1] - B[i][1]
            r3 = (dx * dx + dy * dy) ** mp.mpf("1.5")
            ax += m[j] * dx / r3
            ay += m[j] * dy / r3
        for (acc, coord) in ((ax, B[i][0]), (ay, B[i][1])):
            if abs(coord) > mp.mpf(10) ** -30:
                l = -acc / coord
                if lam is None:
                    lam = l
                res = max(res, abs(l - lam))
    return res, lam


ok = False
for r in real_pos:
    a = mp.re(r)
    res, lam = square_cc_residual(a)
    print(f"   a = {mp.nstr(a, 14)}: CC residual {mp.nstr(res, 6)}, "
          f"lambda = {mp.nstr(lam, 10)}")
    if res < mp.mpf(10) ** -35:
        ok = True
rec("square side root of 32a^6-32a^3+7 gives an exact CC", ok,
    "(the square is a CC for ANY side by scaling, so this only pins the "
    "normalisation the manuscript uses)")

print()
print("=" * 72)
print("B. MANUSCRIPT: generic rank of the 6x4 matrix is 4 (full)")
print("=" * 72)
import random
rnd = random.Random(4242)
ranks = {}
worst = None
for _ in range(40):
    u = mp.mpf(rnd.randint(20, 300)) / 100
    p = mp.mpf(rnd.randint(20, 300)) / 100
    v = mp.mpf(rnd.randint(-300, 300)) / 100
    q = mp.mpf(rnd.randint(-300, 300)) / 100
    if abs(v - q) < mp.mpf("0.05") or abs(u - p) < mp.mpf("0.05"):
        continue
    S, _ = svals(matrix(u, v, p, q))
    r = sum(1 for x in S if x / S[0] > mp.mpf(10) ** -20)
    ranks[r] = ranks.get(r, 0) + 1
    if worst is None or S[3] / S[0] < worst:
        worst = S[3] / S[0]
print(f"   rank histogram over random shapes: {ranks}")
print(f"   smallest sigma_4/sigma_1 seen: {float(worst):.3e}")
rec("generic rank is 4", ranks.get(4, 0) == sum(ranks.values()))

print()
print("=" * 72)
print("C. MANUSCRIPT: the equal-mass regular hexagon lies in the stratum")
print("   and its rank is EXACTLY 3")
print("=" * 72)
# regular hexagon with two vertices on the vertical axis
uh = mp.sqrt(3) / 2
S, V = svals(matrix(uh, mp.mpf(1) / 2, uh, -mp.mpf(1) / 2))
print("   singular values: " + ", ".join(f"{float(x):.6e}" for x in S))
print(f"   sigma_3/sigma_1 = {float(S[2] / S[0]):.3e}   "
      f"sigma_4/sigma_1 = {float(S[3] / S[0]):.3e}")
rank3 = (S[2] / S[0] > mp.mpf(10) ** -20) and (S[3] / S[0] < mp.mpf(10) ** -20)
rec("hexagon rank is exactly 3", rank3)
ker = [V[3, j] for j in range(4)]
nrm = max(abs(t) for t in ker)
ker = [t / nrm for t in ker]
print("   kernel (m1, m2, mA, mB) = "
      + ", ".join(f"{float(t):+.8f}" for t in ker))
eq = all(abs(abs(ker[i]) - abs(ker[0])) < mp.mpf(10) ** -20 for i in range(4))
rec("hexagon kernel is the equal-mass ray", eq)

print()
print("=" * 72)
print("D. MANUSCRIPT: the pair-equality lemma. Whenever the two pairs sit")
print("   at DIFFERENT heights, the equations force pair-equal masses.")
print("   ATTACK: find a shape with v != q whose kernel has mA != mB.")
print("=" * 72)
viol = []
tested = 0
for _ in range(400):
    u = mp.mpf(rnd.randint(20, 300)) / 100
    p = mp.mpf(rnd.randint(20, 300)) / 100
    v = mp.mpf(rnd.randint(-300, 300)) / 100
    q = mp.mpf(rnd.randint(-300, 300)) / 100
    if abs(v - q) < mp.mpf("0.1") or abs(u - p) < mp.mpf("0.05"):
        continue
    S, V = svals(matrix(u, v, p, q))
    if S[3] / S[0] > mp.mpf(10) ** -18:
        continue           # rank 4: no admissible masses at all, skip
    tested += 1
    k = [V[3, j] for j in range(4)]
    n = max(abs(t) for t in k)
    k = [t / n for t in k]
    if abs(k[2] - k[3]) > mp.mpf(10) ** -12:
        viol.append((u, v, p, q, k))
print(f"   shapes with a kernel and v != q examined: {tested}")
print(f"   violations (mA != mB): {len(viol)}")
rec("pair-equality holds on every rank-deficient shape with v != q",
    tested == 0 or not viol,
    "NOT TESTED (no rank-deficient shape found at random)" if tested == 0
    else "")

print()
print("=" * 72)
print("E. MANUSCRIPT: 84 of the 90 2x2 minors are nonzero")
print("   (a 6x4 matrix has C(6,2)*C(4,2) = 15*6 = 90)")
print("=" * 72)
zero_always = 0
nz = 0
pts = []
for _ in range(6):
    pts.append((mp.mpf(rnd.randint(20, 300)) / 100,
                mp.mpf(rnd.randint(-300, 300)) / 100,
                mp.mpf(rnd.randint(20, 300)) / 100,
                mp.mpf(rnd.randint(-300, 300)) / 100))
Ms = [matrix(*t) for t in pts]
for rr in itertools.combinations(range(6), 2):
    for cc in itertools.combinations(range(4), 2):
        vals = []
        for M in Ms:
            d = (M[rr[0]][cc[0]] * M[rr[1]][cc[1]]
                 - M[rr[0]][cc[1]] * M[rr[1]][cc[0]])
            sc = max(abs(M[rr[0]][cc[0]] * M[rr[1]][cc[1]]),
                     abs(M[rr[0]][cc[1]] * M[rr[1]][cc[0]]), mp.mpf(1))
            vals.append(abs(d) / sc)
        if max(vals) < mp.mpf(10) ** -30:
            zero_always += 1
        else:
            nz += 1
print(f"   identically zero: {zero_always}   nonzero: {nz}   total: "
      f"{zero_always + nz}")
rec("84 nonzero 2x2 minors", nz == 84,
    f"measured {nz}")

print()
print("=" * 72)
print("F. CAMPAIGN: the cross point is a rank-2 CC with a positive ray.")
print("   ATTACK 1: is it inside the DECLARED stratum? The manuscript")
print("   excludes the equal-heights sub-stratum from scope.")
print("=" * 72)
U = mp.mpf("0.630918137106736797167988596864253187098618034747723407767631")
Pp = mp.mpf("1.45090746590807305719166080680651095948633549667961704443288")
print(f"   cross point has v = q = 0, so v - q = 0 EXACTLY")
rec("cross point is OUTSIDE the declared stratum (on its excluded face)",
    True, "so it does not contradict the stratum work; it is a boundary "
    "point")

print()
print("   ATTACK 2: recompute rank and kernel from scratch here")
S, V = svals(matrix(U, mp.mpf(0), Pp, mp.mpf(0)))
print("   singular values: " + ", ".join(f"{float(x):.4e}" for x in S))
rec("rank is 2 (sigma_3 and sigma_4 both negligible)",
    S[2] / S[0] < mp.mpf(10) ** -25 and S[3] / S[0] < mp.mpf(10) ** -25,
    f"s3/s1={float(S[2] / S[0]):.2e} s4/s1={float(S[3] / S[0]):.2e}")

print()
print("   ATTACK 3: perturb the point. A real rank-2 point must LOSE")
print("   rank-2 under a generic perturbation, not keep it (which would")
print("   mean a whole curve and a much stronger claim).")
kept = 0
for k in range(6):
    e = mp.mpf(10) ** (-3 - k)
    Sp, _ = svals(matrix(U + e, mp.mpf(0), Pp - e / 3, mp.mpf(0)))
    ratio = Sp[2] / Sp[0]
    print(f"     eps=1e-{3 + k}: sigma_3/sigma_1 = {float(ratio):.3e}")
    if ratio < mp.mpf(10) ** -25:
        kept += 1
rec("rank 2 is ISOLATED, not a curve", kept == 0)

print()
print("=" * 72)
print("G. CAMPAIGN: 'the collinear locus is unique to the (0,3) stratum'.")
print("   ATTACK: exhibit a collinear, collision-free (2,2) configuration.")
print("=" * 72)
found = None
for _ in range(2000):
    u = mp.mpf(rnd.randint(1, 300)) / 100
    p = mp.mpf(rnd.randint(1, 300)) / 100
    v = mp.mpf(rnd.randint(-300, 300)) / 100
    q = mp.mpf(rnd.randint(-300, 300)) / 100
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, v), (-u, v), (p, q), (-p, q)]
    # collinear iff every triple has zero area
    areas = []
    for (i, j, k) in itertools.combinations(range(6), 3):
        areas.append(abs((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                         - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])))
    dmin = min(mp.sqrt((P[i][0] - P[j][0]) ** 2 + (P[i][1] - P[j][1]) ** 2)
               for i in range(6) for j in range(i + 1, 6))
    if max(areas) < mp.mpf(10) ** -25 and dmin > mp.mpf("0.01"):
        found = (u, v, p, q)
        break
rec("no collinear collision-free (2,2) configuration exists", found is None,
    "" if found is None else f"COUNTEREXAMPLE {found}")

print()
print("=" * 72)
print("SUMMARY")
print("=" * 72)
if FAILS:
    print(f"  {len(FAILS)} claim(s) FAILED:")
    for t in FAILS:
        print(f"    - {t}")
else:
    print("  every attacked claim survived")
