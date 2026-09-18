"""EXTERNAL CALIBRATION: reproduce Dias-Pan's published witness.

Their Proposition 5.2 gives an explicit cross central configuration with
m1 = m2 = m3 = m4 = 1 on the symmetry line and m5 = m6 about 4.7648 off
it, the four collinear bodies plus a square, normalised by r14 = 2. The
campaign dossier (read in full, 2026-08-01) records that value and
proposes re-deriving it with our own instruments as a calibration anchor.
This does that, and it is the strongest available external check on the
3 x 4 cross system used for the degeneracy work.

Their configuration, rotated so the symmetry line is the x axis and
rescaled so the off-line pair sits at (0, +-1):

    on the line:  (+-1, 0) and (+-p, 0)      with p = 1/s
    off the line: (0, +-1)

where s is the square's half-diagonal in their normalisation. In our
gauge the four line bodies carry masses mA, mA, mB, mB and the off-line
pair carries m1 = m2. Their witness has ALL FOUR line masses equal, so it
is the point of our family where the kernel satisfies mA = mB. That is one
condition on p, which pins it, and then m1/mA is a PREDICTION we can
compare against their 4.7648.
"""
import mpmath as mp

mp.mp.dps = 50


def system(u, p):
    """Rows E1, E2, E3; columns (m1, mA, mB, lambda). Built from scratch."""
    B = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, mp.mpf(0)), (-u, mp.mpf(0)), (p, mp.mpf(0)), (-p, mp.mpf(0))]
    grp = [0, 0, 1, 1, 2, 2]

    def row(i, comp):
        c = [mp.mpf(0)] * 4
        for j in range(6):
            if j == i:
                continue
            dx = B[j][0] - B[i][0]
            dy = B[j][1] - B[i][1]
            r3 = (dx * dx + dy * dy) ** mp.mpf("1.5")
            c[grp[j]] += (dx if comp == 0 else dy) / r3
        c[3] = B[i][0] if comp == 0 else B[i][1]
        return c
    return [row(2, 0), row(4, 0), row(0, 1)]


def kernel(u, p):
    M = system(u, p)
    A = mp.matrix(3, 4)
    for i in range(3):
        n = max(abs(x) for x in M[i])
        for j in range(4):
            A[i, j] = M[i][j] / n
    U, S, V = mp.svd_r(A, full_matrices=True)
    k = [V[3, j] for j in range(4)]
    n = max(abs(t) for t in k)
    k = [t / n for t in k]
    if k[0] < 0:
        k = [-t for t in k]
    return k, [S[i] for i in range(3)]


def gap(p):
    """mA - mB along the kernel, at u = 1."""
    k, _ = kernel(mp.mpf(1), p)
    return k[1] - k[2]


print("A. locate p where the kernel has mA = mB (their equal-mass line)")
lo, hi = mp.mpf("1.05"), mp.mpf("8")
flo = gap(lo)
brack = None
prev_p, prev_f = lo, flo
n = 400
for i in range(1, n + 1):
    pp = lo + (hi - lo) * i / n
    f = gap(pp)
    if prev_f * f < 0:
        brack = (prev_p, pp)
        break
    prev_p, prev_f = pp, f
if brack is None:
    print("   no sign change found in p in [1.05, 8]")
else:
    a, b = brack
    for _ in range(200):
        m = (a + b) / 2
        if gap(a) * gap(m) <= 0:
            b = m
        else:
            a = m
    p = (a + b) / 2
    print(f"   p = {mp.nstr(p, 20)}")
    k, S = kernel(mp.mpf(1), p)
    print(f"   kernel (m1, mA, mB, lambda) = "
          + ", ".join(mp.nstr(t, 14) for t in k))
    print(f"   |mA - mB| = {mp.nstr(abs(k[1] - k[2]), 6)}")
    print(f"   sigma_3/sigma_1 of the system = {mp.nstr(S[2] / S[0], 6)}")
    print()
    print("B. the PREDICTION: the off-line mass relative to the line mass")
    ratio = k[0] / ((k[1] + k[2]) / 2)
    print(f"   m1 / mA = {mp.nstr(ratio, 16)}")
    print(f"   Dias-Pan's published value (per the dossier): 4.7648")
    err = abs(ratio - mp.mpf("4.7648"))
    print(f"   |difference| = {mp.nstr(err, 6)}")
    print(f"   AGREES to the 5 digits the dossier records: "
          f"{err < mp.mpf('0.0001')}")
    print()
    print("C. the geometry, in their normalisation (rescale so the two")
    print("   outer line bodies sit at +-1, i.e. divide by p)")
    s = 1 / p
    print(f"   line bodies at +-1 and +-{mp.nstr(s, 14)}")
    print(f"   off-line pair at (0, +-{mp.nstr(s, 14)})")
    print(f"   square check: the off-line pair and the INNER line pair are")
    print(f"   both at distance {mp.nstr(s, 14)} from the centre, so they")
    print(f"   form a square. Their Prop 5.2 imposes exactly this.")
    print(f"   r14 (outer separation) = 2, as they normalise.")
    print()
    print("D. verify it directly against the central-configuration equations")
    m = [k[0], k[0], k[1], k[1], k[2], k[2]]
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (mp.mpf(1), mp.mpf(0)), (-mp.mpf(1), mp.mpf(0)),
         (p, mp.mpf(0)), (-p, mp.mpf(0))]
    tot = sum(m)
    cx = sum(m[i] * P[i][0] for i in range(6)) / tot
    cy = sum(m[i] * P[i][1] for i in range(6)) / tot
    lam = []
    for i in range(6):
        ax = ay = mp.mpf(0)
        for j in range(6):
            if j == i:
                continue
            dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
            r3 = (dx * dx + dy * dy) ** mp.mpf("1.5")
            ax += m[j] * dx / r3
            ay += m[j] * dy / r3
        for (a2, c0, d) in ((ax, cx, P[i][0]), (ay, cy, P[i][1])):
            if abs(d - c0) > mp.mpf(10) ** -30:
                lam.append(-a2 / (d - c0))
    spread = max(lam) - min(lam)
    print(f"   centre of mass = ({float(cx):.2e}, {float(cy):.2e})")
    print(f"   lambda over {len(lam)} coordinates, spread = "
          f"{mp.nstr(spread, 6)}")
    print(f"   IS A CENTRAL CONFIGURATION: {spread < mp.mpf(10) ** -30}")
