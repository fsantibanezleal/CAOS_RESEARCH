"""Is band's residue a central configuration?

Its 44 failures, and the 6 that survive a further 44 halvings, all sit at
v = q = 0 with u = 0.63092 and p = 1.45090. That is the doubly symmetric
CROSS: two bodies on the vertical axis at (0, +-1) and four on the
horizontal axis at (+-u, 0) and (+-p, 0). A rank-2 point there with a
positive kernel would be a genuine central configuration of the stratum.

Three questions, in order:
  1. what is sigma_3 at the cluster, and does it descend to zero?
  2. if it plateaus, is the near-kernel sign-definite?
  3. is v = q even inside the stratum, or is it an excluded face?
"""
import random
import mpmath as mp

mp.mp.dps = 50

# bodies: 1, 2 on the axis at (0, +1), (0, -1); pair A at (+-u, v);
# pair B at (+-p, q). Masses (m1, m2, mA, mB).
ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
PAIR_OF = [None, None, 2, 2, 3, 3]


def positions(u, v, p, q):
    return [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
            (u, v), (-u, v), (p, q), (-p, q)]


def M_of(u, v, p, q):
    P = positions(u, v, p, q)
    rows = []
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
        rows.append(c)
    return rows


def svals(M):
    A = mp.matrix(6, 4)
    for i in range(6):
        n = max(abs(x) for x in M[i]) or mp.mpf(1)
        for j in range(4):
            A[i, j] = M[i][j] / n
    U, S, V = mp.svd_r(A)
    return [S[i] for i in range(4)], V


u0 = mp.mpf("0.63092")
p0 = mp.mpf("1.45090")

print("A. singular values at the cluster (v = q = 0)")
sv, V = svals(M_of(u0, mp.mpf(0), p0, mp.mpf(0)))
print("   " + ", ".join(f"{float(x):.6e}" for x in sv))

print("\nB. descent on sigma_4 over (u, p) with v = q = 0")
rnd = random.Random(23)


def obj(x):
    u, p = x
    if u <= mp.mpf("0.05") or p <= mp.mpf("0.05") or abs(u - p) < mp.mpf("0.02"):
        return mp.mpf(10)
    return svals(M_of(u, mp.mpf(0), p, mp.mpf(0)))[0][3]


x = [u0, p0]
best = obj(x)
step = mp.mpf(1) / 64
for it in range(1500):
    y = [x[i] + step * (mp.mpf(rnd.random()) - mp.mpf(1) / 2) for i in range(2)]
    val = obj(y)
    if val < best:
        best, x = val, y
    if it % 300 == 299:
        step /= 4
print(f"   sigma_4 after descent = {mp.nstr(best, 8)}")
print(f"   at (u, p) = ({mp.nstr(x[0], 10)}, {mp.nstr(x[1], 10)})")

print("\nC. the kernel there")
sv, V = svals(M_of(x[0], mp.mpf(0), x[1], mp.mpf(0)))
ker = [V[3, j] for j in range(4)]
nrm = max(abs(k) for k in ker)
ker = [k / nrm for k in ker]
print("   kernel (m1, m2, mA, mB) = "
      + ", ".join(f"{float(k):+.8f}" for k in ker))
pos = all(k > 0 for k in ker) or all(k < 0 for k in ker)
print(f"   SIGN-DEFINITE (positive masses possible): {pos}")

print("\nD. is sigma_4 really bounded away from zero, or descending?")
for scale in (mp.mpf("1e-3"), mp.mpf("1e-5"), mp.mpf("1e-7")):
    vals = []
    for _ in range(40):
        du = scale * (mp.mpf(rnd.random()) - mp.mpf(1) / 2)
        dp = scale * (mp.mpf(rnd.random()) - mp.mpf(1) / 2)
        vals.append(svals(M_of(x[0] + du, mp.mpf(0), x[1] + dp, mp.mpf(0)))[0][3])
    print(f"   within {float(scale):.0e}: min sigma_4 = {float(min(vals)):.6e}")

print("\nE. does v = q lie INSIDE the stratum?")
print("   the stratum is declared with the two pairs at DISTINCT heights.")
print("   v = q puts all four pair bodies on one horizontal line, which is")
print("   a configuration with TWO reflection symmetries, so it belongs to")
print("   a different stratum and is a FACE of this one, not an interior")
print("   point. Checking the matrix just off it:")
for eps in (mp.mpf("1e-3"), mp.mpf("1e-5"), mp.mpf("1e-7")):
    s, _ = svals(M_of(x[0], eps, x[1], mp.mpf(0)))
    print(f"   v = {float(eps):.0e}, q = 0:  sigma_4 = {float(s[3]):.6e}")
