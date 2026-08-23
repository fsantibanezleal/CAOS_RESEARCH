"""LEMMA PIECE 13 (0,3): the merge face rank floor in closed form.

On the merge face two of the three pairs coincide. The chart's row clearing
(non-merging rows times rho^2, the merging row divided by rho^2) sends the
whole mass column of the FIXED pair to zero in five of the six rows, so
every rank-3 minor has to use the single surviving entry: row (2,4),
column 0. That entry is the rank floor of the face.

Write the merging couple as w +- (rho/2) n with n = (alpha, beta) a unit
vector, and let g_k = w - P_k for the two bodies of the fixed pair. Then

    area(2,4,k)          = rho * cross(n, g_k)
    r_{2k}^-3 - r_{4k}^-3 = -3 rho (n . g_k) / |g_k|^5 + O(rho^3)

so the cleared entry has the limit

    E = -3 sum_k (n . g_k) cross(n, g_k) / |g_k|^5
      = -(3/2) sum_k sin(2 phi_k) / |g_k|^3

with phi_k the angle from n to g_k. This file checks that formula against
the chart and locates the covering residue with respect to E = 0.
"""
import math
import random
import mpmath as mp

mp.mp.dps = 50

PAIR_OF = [0, 0, 1, 1, 2, 2]
ROWS = [(0, 2), (0, 3), (0, 4), (0, 5), (2, 4), (2, 5)]


def cleared_row24_col0(rho, tau, wu, wv):
    """The chart's entry, computed directly and divided by rho^2."""
    o = 1 + tau * tau
    al, be = (1 - tau * tau) / o, 2 * tau / o
    uv = [(mp.mpf(1), mp.mpf(0)),
          (wu + rho * al / 2, wv + rho * be / 2),
          (wu - rho * al / 2, wv - rho * be / 2)]
    P = []
    for (u, v) in uv:
        P.append((u, v))
        P.append((-u, v))
    i, j = 2, 4
    tot = mp.mpf(0)
    for k in (0, 1):
        rik = mp.sqrt((P[i][0] - P[k][0]) ** 2 + (P[i][1] - P[k][1]) ** 2)
        rjk = mp.sqrt((P[j][0] - P[k][0]) ** 2 + (P[j][1] - P[k][1]) ** 2)
        area = ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
        tot += (rik ** -3 - rjk ** -3) * area
    return tot / (rho * rho)


def E_closed(tau, wu, wv):
    """The closed form."""
    o = 1 + tau * tau
    n = ((1 - tau * tau) / o, 2 * tau / o)
    tot = mp.mpf(0)
    for Pk in ((mp.mpf(1), mp.mpf(0)), (mp.mpf(-1), mp.mpf(0))):
        g = (wu - Pk[0], wv - Pk[1])
        dot = n[0] * g[0] + n[1] * g[1]
        crs = n[0] * g[1] - n[1] * g[0]
        gn = mp.sqrt(g[0] ** 2 + g[1] ** 2)
        tot += dot * crs / gn ** 5
    return -3 * tot


print("A. closed form vs the chart entry, as rho -> 0")
rnd = random.Random(77)
for _ in range(5):
    tv = mp.mpf(rnd.randint(-60, 60)) / 64
    wuv = mp.mpf(rnd.randint(10, 60)) / 64
    wvv = mp.mpf(rnd.randint(-60, 60)) / 64
    a = cleared_row24_col0(mp.mpf(2) ** -18, tv, wuv, wvv)
    b = E_closed(tv, wuv, wvv)
    rel = abs(a - b) / (abs(b) or mp.mpf(1))
    print(f"   tau={float(tv):+.4f} wu={float(wuv):.4f} wv={float(wvv):+.4f}"
          f"   chart={float(a):+.8e}  closed={float(b):+.8e}"
          f"   rel err {float(rel):.2e}")

print("\nB. the covering residue: where is it relative to E = 0?")
tau0, wu0, wv0 = mp.mpf("0.992235"), mp.mpf("0.970750"), mp.mpf("0.993965")
print(f"   E at the residue point = {float(E_closed(tau0, wu0, wv0)):+.6e}")
print("   for scale, the row's other entries are ~3.2e-3")

print("\nC. does E vanish anywhere on the face? scan over tau at fixed w")
for (wuv, wvv) in ((mp.mpf("0.97"), mp.mpf("0.99")),
                   (mp.mpf("0.5"), mp.mpf("0.25")),
                   (mp.mpf("0.2"), mp.mpf("-0.7"))):
    vals = []
    prev = None
    roots = 0
    for t in range(-200, 201):
        tv = mp.mpf(t) / 100
        e = E_closed(tv, wuv, wvv)
        if prev is not None and prev * e < 0:
            roots += 1
        prev = e
        vals.append(abs(e))
    print(f"   w=({float(wuv):.2f},{float(wvv):+.2f})  sign changes in tau: "
          f"{roots}   min|E| = {float(min(vals)):.3e}   "
          f"max|E| = {float(max(vals)):.3e}")

print("\nD. THE STRUCTURE OF E: n is a unit vector, so with phi_k the angle")
print("   from n to g_k,  E = -(3/2) [ sin(2 phi_0)/|g_0|^3 "
      "+ sin(2 phi_1)/|g_1|^3 ].")
print("   E vanishes exactly when those two terms cancel, which is ONE")
print("   equation on the 3-dimensional face, hence a surface, NOT empty.")
