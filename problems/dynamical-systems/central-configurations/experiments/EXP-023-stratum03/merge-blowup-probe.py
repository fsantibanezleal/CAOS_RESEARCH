"""Does a COLUMN blow-up make the merge face analytic and rank 3?

At rho = 0 pairs B and C coincide, so their mass columns coincide too and
the 6x3 matrix drops rank for a trivial reason: it has a repeated column.
That is not a central configuration, it is a bad chart. The classical cure
for a merging pair is to change basis in mass space to the TOTAL mass of
the merged couple and the DIPOLE, i.e.

    S = c_B + c_C           (finite, the divergences cancel)
    D = rho * (c_B - c_C)   (the difference diverges like 1/rho)

The map (c_B, c_C) -> (S, D) has determinant 2*rho, so it is invertible for
every rho > 0 and PRESERVES THE RANK there. If the transformed matrix has a
finite limit at rho = 0 of rank 3, then by continuity it is rank 3 on a
whole neighbourhood, hence the original is rank 3 on the punctured
neighbourhood, and the merge collar closes by a finite argument instead of
infinitely many shells.
"""
import math
import random
import mpmath as mp

mp.mp.dps = 60

PAIR_OF = [0, 0, 1, 1, 2, 2]
ROWS = [(0, 2), (0, 3), (0, 4), (0, 5), (2, 4), (2, 5)]


def positions(uv):
    P = []
    for (u, v) in uv:
        P.append((u, v))
        P.append((-u, v))
    return P


def L_coeffs(P, i, j):
    c = [mp.mpf(0)] * 3
    for k in range(6):
        if k == i or k == j:
            continue
        rik = mp.sqrt((P[i][0] - P[k][0]) ** 2 + (P[i][1] - P[k][1]) ** 2)
        rjk = mp.sqrt((P[j][0] - P[k][0]) ** 2 + (P[j][1] - P[k][1]) ** 2)
        area = ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
        c[PAIR_OF[k]] += (rik ** -3 - rjk ** -3) * area
    return c


def blown_up(rho, tau, wu, wv, mi=1, mj=2):
    """Matrix in the merge chart, rows cleared and mass columns blown up."""
    o = 1 + tau * tau
    al, be = (1 - tau * tau) / o, 2 * tau / o
    uv = [None] * 3
    uv[3 - mi - mj] = (mp.mpf(1), mp.mpf(0))
    uv[mi] = (wu + rho * al / 2, wv + rho * be / 2)
    uv[mj] = (wu - rho * al / 2, wv - rho * be / 2)
    P = positions(uv)
    merging = (frozenset((2 * mi, 2 * mj)), frozenset((2 * mi + 1, 2 * mj + 1)))
    M = []
    for (i, j) in ROWS:
        c = L_coeffs(P, i, j)
        # the merging row vanishes to second order in rho: clear it
        if frozenset((i, j)) in merging:
            c = [x / (rho * rho) for x in c]
        # column blow-up on the two merging pairs
        S = c[mi] + c[mj]
        D = rho * (c[mi] - c[mj])
        row = [None] * 3
        row[3 - mi - mj] = c[3 - mi - mj]
        row[mi], row[mj] = S, D
        M.append(row)
    return M


def sigmas(M):
    A = mp.matrix(6, 3)
    for i in range(6):
        n = max(abs(x) for x in M[i]) or mp.mpf(1)
        for j in range(3):
            A[i, j] = M[i][j] / n
    _, S, _ = mp.svd_r(A)
    return [S[i] for i in range(3)]


tau0 = mp.mpf("0.992235")
wu0 = mp.mpf("0.970750")
wv0 = mp.mpf("0.993965")

print("A. the RESIDUE point: does the blown-up matrix converge as rho -> 0?")
print("   (raw = no column blow-up, blown = with it)")
for k in range(2, 14, 2):
    r = mp.mpf(2) ** (-k)
    o = 1 + tau0 * tau0
    al, be = (1 - tau0 * tau0) / o, 2 * tau0 / o
    uv = [(mp.mpf(1), mp.mpf(0)),
          (wu0 + r * al / 2, wv0 + r * be / 2),
          (wu0 - r * al / 2, wv0 - r * be / 2)]
    P = positions(uv)
    raw = [L_coeffs(P, i, j) for (i, j) in ROWS]
    sr = sigmas(raw)
    sb = sigmas(blown_up(r, tau0, wu0, wv0))
    print(f"   rho=2^-{k:<2}  raw s3={float(sr[2]):.4e}   "
          f"blown s1={float(sb[0]):.4f} s2={float(sb[1]):.4f} "
          f"s3={float(sb[2]):.4e}")

print("\nB. random face points: is rank 3 GENERIC on the merge face?")
rnd = random.Random(31)
hist = {}
worst = None
for _ in range(60):
    tv = mp.mpf(rnd.randint(-60, 60)) / 64
    wuv = mp.mpf(rnd.randint(8, 62)) / 64
    wvv = mp.mpf(rnd.randint(-60, 60)) / 64
    if abs(wvv) < mp.mpf(1) / 16 and abs(wuv - 1) < mp.mpf(1) / 16:
        continue
    s = sigmas(blown_up(mp.mpf(2) ** -20, tv, wuv, wvv))
    b = int(math.floor(math.log10(max(float(s[2]), 1e-99))))
    hist[b] = hist.get(b, 0) + 1
    if worst is None or s[2] < worst[0]:
        worst = (s[2], tv, wuv, wvv)
print("   log10(sigma_3) histogram on the face:",
      dict(sorted(hist.items())))
print(f"   smallest sigma_3 = {float(worst[0]):.4e} at "
      f"tau={float(worst[1]):.4f} wu={float(worst[2]):.4f} "
      f"wv={float(worst[3]):.4f}")
