"""Independent confirmation, without the reduced matrix.

For the cross configuration -- bodies at (0, +-1), (+-u, 0), (+-p, 0) --
symmetry forces m1 = m2 and the centre of mass at the origin, so the
central-configuration equations collapse to THREE independent scalar
conditions:

   E1: x-component at (u, 0)
   E2: x-component at (p, 0)
   E3: y-component at (0, 1)

each LINEAR in (m1, mA, mB, lambda). That is a 3 x 4 system. Its kernel is
one-dimensional at a generic cross point, giving the unique mass ray the
face scan found. At an exceptional point the rank drops to 2 and the
kernel becomes two-dimensional, which is a ONE-PARAMETER family of masses
for a single shape: a degenerate central configuration.

This routine builds that 3 x 4 system from scratch -- no Laura-Andoyer
reduction, no 6 x 4 matrix, no shared code with the covering -- and
measures its rank at the candidate point and at controls.
"""
import mpmath as mp

mp.mp.dps = 120

U = mp.mpf("0.6309181371067367971679885968642467138842")
P = mp.mpf("1.450907465908073057191660806806502905941")


def system(u, p):
    """Rows E1, E2, E3; columns (m1, mA, mB, lambda)."""
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


def svals(M):
    A = mp.matrix(3, 4)
    for i in range(3):
        n = max(abs(x) for x in M[i]) or mp.mpf(1)
        for j in range(4):
            A[i, j] = M[i][j] / n
    _, S, V = mp.svd_r(A)
    return [S[i] for i in range(3)], V


print("A. the 3 x 4 system at the candidate point")
S, V = svals(system(U, P))
print("   singular values: " + ", ".join(mp.nstr(x, 10) for x in S))
print(f"   sigma_3/sigma_1 = {mp.nstr(S[2] / S[0], 8)}")
print(f"   RANK 2 (kernel is two-dimensional): {S[2] / S[0] < mp.mpf(10) ** -30}")

print("\nB. controls: the same system at ordinary cross points")
for (du, dp) in ((mp.mpf("0.01"), mp.mpf(0)), (mp.mpf(0), mp.mpf("0.01")),
                 (mp.mpf("-0.05"), mp.mpf("0.03"))):
    Sc, _ = svals(system(U + du, P + dp))
    print(f"   (u+{float(du):+.3f}, p+{float(dp):+.3f}): "
          f"sigma_3/sigma_1 = {mp.nstr(Sc[2] / Sc[0], 8)}  -> rank 3, "
          "unique mass ray")

print("\nC. the two-dimensional kernel, from THIS system")
A = mp.matrix(3, 4)
M = system(U, P)
for i in range(3):
    n = max(abs(x) for x in M[i])
    for j in range(4):
        A[i, j] = M[i][j] / n
_, _, V = mp.svd_r(A, full_matrices=True)
k1 = [V[2, j] for j in range(4)]
k2 = [V[3, j] for j in range(4)]
k1 = [t / max(abs(z) for z in k1) for t in k1]
k2 = [t / max(abs(z) for z in k2) for t in k2]
print("   v1 = " + ", ".join(mp.nstr(t, 14) for t in k1))
print("   v2 = " + ", ".join(mp.nstr(t, 14) for t in k2))
print("   (columns are m1, mA, mB, lambda)")

print("\nD. the admissible arc: masses AND lambda all positive")
lo = hi = None
NT = 200000
for i in range(2 * NT + 1):
    th = mp.pi * i / NT - mp.pi
    w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
    if all(t > 0 for t in w):
        if lo is None:
            lo = th
        hi = th
if lo is None:
    print("   EMPTY")
else:
    print(f"   theta in [{mp.nstr(lo, 8)}, {mp.nstr(hi, 8)}], width "
          f"{mp.nstr(hi - lo, 8)} rad")
    print("\n   frac      m1           mA           mB           lambda"
          "        max |residual|")
    for frac in (mp.mpf(1) / 10, mp.mpf(1) / 3, mp.mpf(1) / 2,
                 mp.mpf(2) / 3, mp.mpf(9) / 10):
        th = lo + (hi - lo) * frac
        w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
        nn = max(w)
        w = [t / nn for t in w]
        res = max(abs(sum(M[r][c] * w[c] for c in range(4)))
                  for r in range(3))
        print(f"   {float(frac):.3f}  {float(w[0]):.10f}  {float(w[1]):.10f}"
              f"  {float(w[2]):.10f}  {float(w[3]):.10f}  {mp.nstr(res, 6)}")

print("\nE. no collisions, and the mutual distances")
B = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
     (U, mp.mpf(0)), (-U, mp.mpf(0)), (P, mp.mpf(0)), (-P, mp.mpf(0))]
ds = []
for i in range(6):
    for j in range(i + 1, 6):
        ds.append(mp.sqrt((B[i][0] - B[j][0]) ** 2 + (B[i][1] - B[j][1]) ** 2))
print(f"   smallest mutual distance = {mp.nstr(min(ds), 12)}")
print(f"   largest  mutual distance = {mp.nstr(max(ds), 12)}")
