"""Why does m2's corner resist every certificate?

The residue maps to six bodies nearly on the symmetry axis: (0, +-1), and
two mirror pairs at (+-u, v), (+-p, q) with u and p around 1e-4 and the
heights near 2.95. That is the COLLINEAR limit, and the (0,3) stratum
already taught this lesson: every Laura-Andoyer coefficient carries a
triangle area, six collinear bodies span none, so the matrix goes to zero
identically. A matrix going to zero has no nonzero minor, so no rank-3
certificate and no trap can fire, no matter how deep the bisection goes.

The (2,2) stratum was said to be free of this (finding 22) because
collinearity there forces u = p = 0, which is a collision. That is right
about the INTERIOR and says nothing about the approach, which is what m2
covers.

This measures the approach: singular values as u, p go to zero at fixed
heights, and the rank after the degeneracy is scaled out.
"""
import mpmath as mp

mp.mp.dps = 60

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
COL = [0, 1, 2, 2, 3, 3]


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


def svals(M, rownorm=True):
    A = mp.matrix(6, 4)
    for i in range(6):
        n = (max(abs(x) for x in M[i]) or mp.mpf(1)) if rownorm else mp.mpf(1)
        for j in range(4):
            A[i, j] = M[i][j] / n
    _, S, _ = mp.svd_r(A)
    return [S[i] for i in range(4)]


v0 = mp.mpf("2.95")
q0 = mp.mpf("2.916")
ratio = mp.mpf("1.63") / mp.mpf("1.12")

print("A. RAW magnitudes as the pairs collapse onto the axis")
print("   (u = s, p = s/1.455, heights fixed)")
print("   s          largest |entry|     sigma_1(raw)")
for k in range(2, 16, 2):
    s = mp.mpf(2) ** -k
    M = matrix(s, v0, s / ratio, q0)
    big = max(abs(x) for r in M for x in r)
    sv = svals(M, rownorm=False)
    print(f"   2^-{k:<3}  {mp.nstr(big, 8):>16}  {mp.nstr(sv[0], 8)}")

print("")
print("B. after row normalisation, is the RANK still 3?")
print("   s          sigma_1   sigma_2   sigma_3   sigma_4   s3/s1")
for k in range(2, 22, 2):
    s = mp.mpf(2) ** -k
    sv = svals(matrix(s, v0, s / ratio, q0))
    print(f"   2^-{k:<3}  " + "  ".join(f"{float(x):.2e}" for x in sv)
          + f"   {float(sv[2] / sv[0]):.3e}")

print("")
print("C. the same at the residue's ACTUAL heights and ratio")
uv = mp.mpf("1.63e-4")
pv = mp.mpf("1.12e-4")
sv = svals(matrix(uv, v0, pv, q0))
print("   sigma = " + ", ".join(f"{float(x):.4e}" for x in sv))
print(f"   sigma_3/sigma_1 = {float(sv[2] / sv[0]):.4e}")
print(f"   sigma_4/sigma_1 = {float(sv[3] / sv[0]):.4e}")

print("")
print("D. control: the SAME heights but pairs NOT collapsed")
for uu in ("0.5", "1.0", "2.0"):
    u1 = mp.mpf(uu)
    sv = svals(matrix(u1, v0, u1 / ratio, q0))
    print(f"   u={uu:<4} sigma_3/sigma_1 = {float(sv[2] / sv[0]):.4e}"
          f"   sigma_4/sigma_1 = {float(sv[3] / sv[0]):.4e}")

print("")
print("E. is the limit matrix (after scaling) rank-deficient?")
print("   dividing every entry by its leading power of s and re-measuring")
for k in (8, 12, 16, 20):
    s = mp.mpf(2) ** -k
    M = matrix(s, v0, s / ratio, q0)
    sv = svals(M)
    print(f"   s=2^-{k:<3} row-normalised sigma_3/sigma_1 = "
          f"{float(sv[2] / sv[0]):.4e}, sigma_4/sigma_1 = "
          f"{float(sv[3] / sv[0]):.4e}")
