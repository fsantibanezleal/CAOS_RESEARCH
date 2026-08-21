"""EXP-023: the (k=0, p=3) stratum, three mirror pairs, no axis bodies.

Six bodies in the plane, reflection-symmetric about a vertical axis, with
NOTHING on the axis:

    pair A = (+-u1, v1)  bodies 1, 2, mass mA each
    pair B = (+-u2, v2)  bodies 3, 4, mass mB each
    pair C = (+-u3, v3)  bodies 5, 6, mass mC each

Shape space: six coordinates minus vertical translation and scale = 4,
the SAME dimension as the (2,2) stratum this campaign is closing. The
mass vector has only THREE entries, which changes the dimension count in
an interesting way and is the reason this stratum is the natural next
target (see context/2026-08-20-exploration-which-strata-next.md).

Laura-Andoyer equations: L_ij = sum over k != i,j of
m_k (R_ik - R_jk) Delta_ijk, with R_ab = 1/r_ab^3 and Delta_ijk twice the
signed area of the triangle (i, j, k). L is symmetric in (i, j), and under
the mirror sigma (1<->2, 3<->4, 5<->6) the distances are invariant while
every area flips sign, so L_{sigma i, sigma j} = -L_ij. Consequences:

    L_12 = L_34 = L_56 = 0 identically   (each is its own mirror)
    L_24 = -L_13,  L_23 = -L_14,  L_26 = -L_15,
    L_25 = -L_16,  L_46 = -L_35,  L_45 = -L_36

so exactly SIX independent equations remain, {L13, L14, L15, L16, L35,
L36}, giving a 6 x 3 mass matrix. This script builds that matrix
numerically, verifies the symmetry claims above, and measures its GENERIC
RANK, which decides the shape of the whole programme for this stratum.
"""
import itertools
import random
import mpmath as mp

mp.mp.dps = 40

def positions(u1, v1, u2, v2, u3, v3):
    return [(u1, v1), (-u1, v1), (u2, v2), (-u2, v2), (u3, v3), (-u3, v3)]

def R(pi, pj):
    d = mp.sqrt((pi[0] - pj[0]) ** 2 + (pi[1] - pj[1]) ** 2)
    return d ** -3, d

def area2(pi, pj, pk):
    """twice the signed area of (i, j, k)."""
    return ((pj[0] - pi[0]) * (pk[1] - pi[1])
            - (pj[1] - pi[1]) * (pk[0] - pi[0]))

PAIR_OF = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2}   # body -> mass index

def L_coeffs(P, i, j):
    """coefficients of (mA, mB, mC) in the equation L_ij."""
    c = [mp.mpf(0)] * 3
    for k in range(6):
        if k == i or k == j:
            continue
        Rik, _ = R(P[i], P[k])
        Rjk, _ = R(P[j], P[k])
        c[PAIR_OF[k]] += (Rik - Rjk) * area2(P[i], P[j], P[k])
    return c

def matrix(P, rows):
    return [L_coeffs(P, i, j) for (i, j) in rows]

ROWS = [(0, 2), (0, 3), (0, 4), (0, 5), (2, 4), (2, 5)]   # L13,L14,L15,L16,L35,L36
NAMES = ["L13", "L14", "L15", "L16", "L35", "L36"]

def rank_num(M, tol=mp.mpf(10) ** -25):
    """rank by Gaussian elimination with partial pivoting."""
    A = [row[:] for row in M]
    rows, cols = len(A), len(A[0])
    r = 0
    for c in range(cols):
        piv, best = None, tol
        for i in range(r, rows):
            if abs(A[i][c]) > best:
                piv, best = i, abs(A[i][c])
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(rows):
            if i != r and abs(A[i][c]) > 0:
                f = A[i][c] / A[r][c]
                for cc in range(cols):
                    A[i][cc] -= f * A[r][cc]
        r += 1
        if r == rows:
            break
    return r

rnd = random.Random(2026)
def rr(a, b):
    return mp.mpf(rnd.randint(a, b)) / 64

print("A. symmetry claims (L12 = L34 = L56 = 0; mirror pairs anti-equal)")
for _ in range(3):
    u1, v1 = rr(8, 200), rr(-200, 200)
    u2, v2 = rr(8, 200), rr(-200, 200)
    u3, v3 = rr(8, 200), rr(-200, 200)
    P = positions(u1, v1, u2, v2, u3, v3)
    z = [max(abs(x) for x in L_coeffs(P, i, j)) for (i, j) in ((0, 1), (2, 3), (4, 5))]
    a1 = [L_coeffs(P, 1, 3)[t] + L_coeffs(P, 0, 2)[t] for t in range(3)]
    a2 = [L_coeffs(P, 1, 5)[t] + L_coeffs(P, 0, 4)[t] for t in range(3)]
    print(f"   |L12|,|L34|,|L56| = {[mp.nstr(x,3) for x in z]}   "
          f"|L24+L13| = {mp.nstr(max(abs(x) for x in a1),3)}   "
          f"|L26+L15| = {mp.nstr(max(abs(x) for x in a2),3)}")

print("\nB. generic rank of the 6 x 3 reduced matrix (20 random shapes)")
ranks = {}
for _ in range(20):
    u1, v1 = rr(8, 200), rr(-200, 200)
    u2, v2 = rr(8, 200), rr(-200, 200)
    u3, v3 = rr(8, 200), rr(-200, 200)
    if len({(u1, v1), (u2, v2), (u3, v3)}) < 3:
        continue
    P = positions(u1, v1, u2, v2, u3, v3)
    M = matrix(P, ROWS)
    r = rank_num(M)
    ranks[r] = ranks.get(r, 0) + 1
print(f"   rank histogram: {ranks}")
print("   (rank 3 means the kernel is trivial: NO admissible masses at that")
print("    shape, so central configurations of this stratum live only on the")
print("    rank <= 2 locus)")

print("\nC. a known member: the regular hexagon (all six on a circle)")
h = mp.sqrt(3) / 2
P = [(mp.mpf(1), mp.mpf(0)), (-mp.mpf(1), mp.mpf(0)),
     (mp.mpf(1) / 2, h), (-mp.mpf(1) / 2, h),
     (mp.mpf(1) / 2, -h), (-mp.mpf(1) / 2, -h)]
M = matrix(P, ROWS)
print(f"   hexagon rank = {rank_num(M)}")
for nm, row in zip(NAMES, M):
    print(f"     {nm}: " + "  ".join(mp.nstr(x, 6) for x in row))
