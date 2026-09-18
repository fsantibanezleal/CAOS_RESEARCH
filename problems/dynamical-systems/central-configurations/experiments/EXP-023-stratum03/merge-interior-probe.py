"""Is the mergeBC interior failure cluster a rank-2 point, and a CC?

Unlike every earlier cluster in this campaign, these failures are NOT on a
chart boundary: wu ~ 0.9707 and wv ~ 0.9940 sit inside [1/16, 1] and
[-1, 1], and tau ~ 0.9922 is interior too. In this stratum the rank <= 2
locus is exactly where central configurations live, so a genuine rank-2
point here with a POSITIVE kernel would be a central configuration of the
three-pair stratum.

Works in the original coordinates: pair A at (+-1, 0) and pairs B, C near
(+-wu, wv) separated by rho in the direction (alpha, beta).
"""
import math
import random
import mpmath as mp

mp.mp.dps = 50

PAIR_OF = [0, 0, 1, 1, 2, 2]
ROWS = [(0, 2), (0, 3), (0, 4), (0, 5), (2, 4), (2, 5)]


def positions(u1, v1, u2, v2, u3, v3):
    return [(u1, v1), (-u1, v1), (u2, v2), (-u2, v2), (u3, v3), (-u3, v3)]


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


def M_of(u2, v2, u3, v3):
    P = positions(mp.mpf(1), mp.mpf(0), u2, v2, u3, v3)
    return [L_coeffs(P, i, j) for (i, j) in ROWS]


def svals(M):
    A = [[float(x) for x in row] for row in M]
    for i in range(6):
        n = max(abs(x) for x in A[i]) or 1.0
        A[i] = [x / n for x in A[i]]
    G = [[sum(A[k][i] * A[k][j] for k in range(6)) for j in range(3)]
         for i in range(3)]
    for _ in range(80):
        off = sum(G[i][j] ** 2 for i in range(3) for j in range(i + 1, 3))
        if off < 1e-30:
            break
        for p in range(3):
            for q in range(p + 1, 3):
                if abs(G[p][q]) < 1e-300:
                    continue
                th = (G[q][q] - G[p][p]) / (2 * G[p][q])
                t = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(3):
                    x, y = G[k][p], G[k][q]
                    G[k][p], G[k][q] = c * x - s * y, s * x + c * y
                for k in range(3):
                    x, y = G[p][k], G[q][k]
                    G[p][k], G[q][k] = c * x - s * y, s * x + c * y
    return sorted((max(G[i][i], 0.0) ** 0.5 for i in range(3)), reverse=True)


def geom(rho, tau, wu, wv):
    o = 1 + tau * tau
    al, be = (1 - tau * tau) / o, 2 * tau / o
    return (wu + rho * al / 2, wv + rho * be / 2,
            wu - rho * al / 2, wv - rho * be / 2)


rho0 = mp.mpf("0.000008")
tau0 = mp.mpf("0.992235")
wu0 = mp.mpf("0.970750")
wv0 = mp.mpf("0.993965")

print("A. singular values at the cluster, and as rho varies")
for r in (rho0, mp.mpf("1e-4"), mp.mpf("1e-2"), mp.mpf("0.05")):
    sv = svals(M_of(*geom(r, tau0, wu0, wv0)))
    print(f"   rho={float(r):.2e}  sv = " + ", ".join(f"{x:.6e}" for x in sv))

print("\nB. descent on sigma_3 over (tau, wu, wv) with rho held at 0.02")
rnd = random.Random(17)


def obj(p, r):
    tau, wu, wv = p
    if wu <= 0:
        return mp.mpf(10)
    u2, v2, u3, v3 = geom(r, tau, wu, wv)
    if u2 <= 0 or u3 <= 0:
        return mp.mpf(10)
    return mp.mpf(svals(M_of(u2, v2, u3, v3))[2])


r_fixed = mp.mpf("0.02")
x = [tau0, wu0, wv0]
best = obj(x, r_fixed)
step = mp.mpf(1) / 64
for it in range(2000):
    y = [x[i] + step * (mp.mpf(rnd.random()) - mp.mpf(1) / 2) for i in range(3)]
    v = obj(y, r_fixed)
    if v < best:
        best, x = v, y
    if it % 400 == 399:
        step /= 4
print(f"   after descent: sigma_3 = {mp.nstr(best, 8)}")
print("   at (tau, wu, wv) =", [mp.nstr(t, 10) for t in x])

u2, v2, u3, v3 = geom(r_fixed, *x)
print(f"   pair separation |B-C| = {mp.nstr(mp.sqrt((u2-u3)**2 + (v2-v3)**2), 8)}")
M = M_of(u2, v2, u3, v3)
A = mp.matrix(6, 3)
for i in range(6):
    for j in range(3):
        A[i, j] = M[i][j]
U, S, V = mp.svd_r(A)
ker = [V[2, j] for j in range(3)]
nrm = max(abs(k) for k in ker)
ker = [k / nrm for k in ker]
print("   kernel (mA, mB, mC) =", [mp.nstr(k, 10) for k in ker])
same = all(k > 0 for k in ker) or all(k < 0 for k in ker)
print("   SIGN-DEFINITE (positive masses possible):", same)
