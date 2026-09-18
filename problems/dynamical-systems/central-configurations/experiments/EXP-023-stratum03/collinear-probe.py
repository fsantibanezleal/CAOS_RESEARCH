"""Are the collapse1 failures the COLLINEAR central configurations?

The cluster sits at v1 = v2 = v3 = 0 (all three pairs at the same height),
i.e. six bodies on a horizontal line at +-a, +-b, +-c. Those are Moulton
collinear central configurations, which exist for every ordering and every
positive mass vector, so they ARE central configurations of this stratum
and must lie on its rank <= 2 locus. The covering is therefore right to
refuse a rank-3 certificate there.

Two things to establish:
  1. the rank on the collinear locus is really <= 2, and
  2. its dimension: v2 = v3 = 0 is two conditions in the 4-dimensional
     shape space, so the locus is 2-dimensional, which would mean the
     bound dim R_2 <= 2 is ATTAINED here, exactly as the centred pentagon
     attains it in the (2,2) stratum.
"""
import math
import random
import mpmath as mp

mp.mp.dps = 40

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


def M_of(u1, v1, u2, v2, u3, v3):
    P = positions(u1, v1, u2, v2, u3, v3)
    return [L_coeffs(P, i, j) for (i, j) in ROWS]


def rank_num(M, tol=mp.mpf(10) ** -25):
    A = [row[:] for row in M]
    r = 0
    for c in range(3):
        piv, best = None, tol
        for i in range(r, 6):
            if abs(A[i][c]) > best:
                piv, best = i, abs(A[i][c])
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(6):
            if i != r and abs(A[i][c]) > 0:
                f = A[i][c] / A[r][c]
                for cc in range(3):
                    A[i][cc] -= f * A[r][cc]
        r += 1
    return r


print("A. rank ON the collinear locus (all heights zero), random widths")
rnd = random.Random(5)
ranks = {}
for _ in range(20):
    a = mp.mpf(rnd.randint(20, 120)) / 128
    b = mp.mpf(rnd.randint(20, 120)) / 128
    c = mp.mpf(1)
    if len({float(a), float(b), float(c)}) < 3:
        continue
    r = rank_num(M_of(c, mp.mpf(0), a, mp.mpf(0), b, mp.mpf(0)))
    ranks[r] = ranks.get(r, 0) + 1
print(f"   rank histogram on the collinear locus: {ranks}")

print("\nB. rank just OFF it (one height perturbed)")
for eps in (mp.mpf("1e-2"), mp.mpf("1e-4"), mp.mpf("1e-6")):
    ranks = {}
    for _ in range(20):
        a = mp.mpf(rnd.randint(20, 120)) / 128
        b = mp.mpf(rnd.randint(20, 120)) / 128
        r = rank_num(M_of(mp.mpf(1), mp.mpf(0), a, eps, b, mp.mpf(0)))
        ranks[r] = ranks.get(r, 0) + 1
    print(f"   eps={float(eps):.0e}: {ranks}")

print("\nC. the kernel on the collinear locus (is it a positive-mass CC?)")
for trial in range(4):
    a = mp.mpf(rnd.randint(20, 120)) / 128
    b = mp.mpf(rnd.randint(20, 120)) / 128
    M = M_of(mp.mpf(1), mp.mpf(0), a, mp.mpf(0), b, mp.mpf(0))
    A = mp.matrix(6, 3)
    for i in range(6):
        for j in range(3):
            A[i, j] = M[i][j]
    try:
        U, S, V = mp.svd_r(A)
        sv = [S[i] for i in range(3)]
        ker = [V[2, j] for j in range(3)]
        nrm = max(abs(k) for k in ker) or mp.mpf(1)
        ker = [k / nrm for k in ker]
        pos = all(k > 0 for k in ker) or all(k < 0 for k in ker)
        print(f"   widths (1, {float(a):.4f}, {float(b):.4f})  "
              f"sv3={float(sv[2]):.3e}  kernel="
              + ", ".join(f"{float(k):+.4f}" for k in ker)
              + f"  sign-definite={pos}")
    except Exception as e:
        print("   svd failed:", e)
