"""Which subspace carries the s^3 degeneracy in m2's corner?

sigma_3 and sigma_4 both vanish like s^3 as the pairs collapse onto the
axis, while sigma_1 and sigma_2 stay O(1). So the matrix has a
2-dimensional subspace on which it is O(s^3), and rank 3 survives in the
open stratum only by that much. Certificates fail because the minors are
that small, not because the rank drops.

If the small subspace is spanned by mass COLUMNS, dividing those columns
by s^3 restores an O(1) matrix and the certificates come back, which is
exactly the rescaling discipline pieces 10 to 13 used on the other faces.
This measures the structure: the right singular vectors for the two small
values, and the per-column and per-row scaling of the entries.
"""
import mpmath as mp

mp.mp.dps = 60

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
COL = [0, 1, 2, 2, 3, 3]
NAMES = ["m1", "m2", "mA", "mB"]
RN = ["L13", "L15", "L23", "L25", "L35", "L36"]


def matrix(u, v, p, q):
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


v0, q0 = mp.mpf("2.95"), mp.mpf("2.916")
ratio = mp.mpf("1.63") / mp.mpf("1.12")

print("A. order in s of every entry (from s = 2^-10 vs 2^-12)")
Ma = matrix(mp.mpf(2) ** -10, v0, mp.mpf(2) ** -10 / ratio, q0)
Mb = matrix(mp.mpf(2) ** -12, v0, mp.mpf(2) ** -12 / ratio, q0)
print("   row      " + "  ".join(f"{n:>8}" for n in NAMES))
for i in range(6):
    cells = []
    for j in range(4):
        a, b = abs(Ma[i][j]), abs(Mb[i][j])
        if a == 0 or b == 0:
            cells.append("    zero")
            continue
        o = mp.log(a / b) / mp.log(4)
        cells.append(f"{float(o):+8.3f}")
    print(f"   {RN[i]:<7} " + "  ".join(cells))

print("")
print("B. the two SMALL right singular vectors (the mass directions on")
print("   which the matrix is O(s^3))")
for k in (10, 14, 18):
    s = mp.mpf(2) ** -k
    M = matrix(s, v0, s / ratio, q0)
    A = mp.matrix(6, 4)
    for i in range(6):
        n = max(abs(x) for x in M[i])
        for j in range(4):
            A[i, j] = M[i][j] / n
    _, S, V = mp.svd_r(A)
    for idx in (2, 3):
        w = [V[idx, j] for j in range(4)]
        nrm = max(abs(t) for t in w)
        w = [t / nrm for t in w]
        print(f"   s=2^-{k:<3} sigma_{idx + 1}={float(S[idx]):.2e}  "
              "direction " + ", ".join(f"{n}={float(t):+.6f}"
                                       for n, t in zip(NAMES, w)))
    print("")

print("C. what the directions mean")
print("   if both small directions live on (m1, m2) the axis-body columns")
print("   carry the degeneracy; if on (mA, mB) it is the collapsing pairs")
print("")
print("D. per-column magnitudes, to see the scaling directly")
for k in (6, 10, 14):
    s = mp.mpf(2) ** -k
    M = matrix(s, v0, s / ratio, q0)
    print(f"   s=2^-{k:<3} " + "  ".join(
        f"{n}: {float(max(abs(M[i][j]) for i in range(6))):.3e}"
        for j, n in enumerate(NAMES)))

print("")
print("E. per-row magnitudes")
for k in (6, 10, 14):
    s = mp.mpf(2) ** -k
    M = matrix(s, v0, s / ratio, q0)
    print(f"   s=2^-{k:<3} " + " ".join(
        f"{RN[i]}:{float(max(abs(x) for x in M[i])):.2e}" for i in range(6)))
