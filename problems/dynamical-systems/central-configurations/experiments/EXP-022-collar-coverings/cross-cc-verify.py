"""The cross-face rank-2 point: verify it as a central configuration.

sigma_3 falls in exact proportion to the search bracket over thirteen
orders of magnitude, so its infimum is zero and the point is exactly rank
2. Rank 2 in a 6x4 matrix leaves a TWO-dimensional kernel, so if that
kernel meets the positive orthant the SAME configuration is central for a
one-parameter family of mass vectors. That is the signature of a
degenerate central configuration, and the (2,2) stratum was believed to
have exactly one, the centred pentagon.

This verifies the whole claim against the actual central-configuration
equations rather than the reduced ones.
"""
import mpmath as mp

mp.mp.dps = 160

U = mp.mpf("0.6309181371067367971679885968642467138842")
Pp = mp.mpf("1.450907465908073057191660806806502905941")

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
PAIR_OF = [None, None, 2, 2, 3, 3]


def positions(u, p):
    return [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
            (u, mp.mpf(0)), (-u, mp.mpf(0)),
            (p, mp.mpf(0)), (-p, mp.mpf(0))]


def rows_at(u, p):
    P = positions(u, p)
    out = []
    for (i, j) in ROWS:
        c = [mp.mpf(0)] * 4
        for k in range(6):
            if k == i or k == j:
                continue
            rik = mp.sqrt((P[i][0] - P[k][0]) ** 2 + (P[i][1] - P[k][1]) ** 2)
            rjk = mp.sqrt((P[j][0] - P[k][0]) ** 2 + (P[j][1] - P[k][1]) ** 2)
            area = ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
            col = k if k < 2 else PAIR_OF[k]
            c[col] += (rik ** -3 - rjk ** -3) * area
        out.append(c)
    return out


def lam_spread(u, p, w):
    m = [w[0], w[1], w[2], w[2], w[3], w[3]]
    P = positions(u, p)
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
        for (a, c0, d) in ((ax, cx, P[i][0]), (ay, cy, P[i][1])):
            if abs(d - c0) > mp.mpf(10) ** -80:
                lam.append(-a / (d - c0))
    return max(lam) - min(lam), lam[0], len(lam)


M = rows_at(U, Pp)
A = mp.matrix(6, 4)
for i in range(6):
    n = max(abs(x) for x in M[i])
    for j in range(4):
        A[i, j] = M[i][j] / n
_, S, V = mp.svd_r(A)
print("singular values at the point")
print("  " + ", ".join(mp.nstr(S[i], 10) for i in range(4)))
print(f"  sigma_3/sigma_1 = {mp.nstr(S[2] / S[0], 8)}")

k1 = [V[2, j] for j in range(4)]
k2 = [V[3, j] for j in range(4)]
k1 = [t / max(abs(z) for z in k1) for t in k1]
k2 = [t / max(abs(z) for z in k2) for t in k2]
print("\nkernel basis")
print("  v1 = " + ", ".join(mp.nstr(t, 16) for t in k1))
print("  v2 = " + ", ".join(mp.nstr(t, 16) for t in k2))

print("\nthe positive cone of the kernel")
lo = hi = None
NT = 400000
for i in range(NT + 1):
    th = mp.pi * i / NT
    w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
    if all(t > 0 for t in w) or all(t < 0 for t in w):
        if lo is None:
            lo = th
        hi = th
if lo is None:
    print("  EMPTY -> not a central configuration for any positive masses")
else:
    print(f"  theta in [{mp.nstr(lo, 10)}, {mp.nstr(hi, 10)}], width "
          f"{mp.nstr(hi - lo, 10)} rad -> a ONE-PARAMETER family of masses")
    print("\nchecking the ACTUAL central-configuration equations along it")
    print("   frac    m1        m2        mA           mB          "
          "lambda spread")
    for frac in (mp.mpf(1) / 8, mp.mpf(1) / 4, mp.mpf(1) / 2,
                 mp.mpf(3) / 4, mp.mpf(7) / 8):
        th = lo + (hi - lo) * frac
        w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
        if w[0] < 0:
            w = [-t for t in w]
        nn = max(w)
        w = [t / nn for t in w]
        sp, l0, nl = lam_spread(U, Pp, w)
        print(f"   {float(frac):.3f}  {float(w[0]):.6f}  {float(w[1]):.6f}  "
              f"{float(w[2]):.8f}  {float(w[3]):.8f}  {mp.nstr(sp, 6)}")
    print(f"\n   (for scale, sigma_3 at this point is "
          f"{mp.nstr(S[2], 6)}; a spread at that level means the")
    print("    equations hold to the accuracy the point is known to)")
    th = (lo + hi) / 2
    w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
    if w[0] < 0:
        w = [-t for t in w]
    nn = max(w)
    w = [t / nn for t in w]
    sp, l0, nl = lam_spread(U, Pp, w)
    print(f"\n   at the middle of the cone: lambda = {mp.nstr(l0, 20)}")
    print(f"   masses = " + ", ".join(mp.nstr(t, 18) for t in w))
