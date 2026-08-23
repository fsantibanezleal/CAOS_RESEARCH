"""Which of the four reflection-symmetric strata of n = 6 contain an
INTERIOR collinear locus, and what does Moulton contribute there?

The four strata are indexed by (a, b) with a bodies on the reflection axis
and b mirror pairs off it, a + 2b = 6: (6,0), (4,1), (2,2), (0,3).

The Laura-Andoyer equations are equivalent to the central-configuration
equations only for NON-collinear configurations: every coefficient carries
a triangle area, so on a collinear configuration the whole matrix vanishes
identically and the equations say nothing. Any stratum containing collinear
configurations in its interior therefore needs Moulton's theorem alongside
the covering, which is a split in the argument, not a gap.

A stratum has an interior collinear locus exactly when six bodies can be
collinear without any collision. The reflection axis is x = 0.
"""
import itertools
import random
import mpmath as mp

mp.mp.dps = 40


def report(name, a, b, verdict, reason):
    print(f"  {name:<8} axis={a} pairs={b}   collinear interior: "
          f"{verdict:<3}  {reason}")


print("A. can six bodies of each stratum be collinear with no collision?")
print("   two lines are available: the axis x = 0 itself, and any line")
print("   PERPENDICULAR to it, y = const (which the mirror preserves).\n")

report("(6,0)", 6, 0, "ALL",
       "every configuration of the stratum is already on the axis")
report("(4,1)", 4, 1, "no",
       "on the axis the pair needs u = 0, a collision; on a horizontal "
       "line the four axis bodies would share a height, a 4-fold collision")
report("(2,2)", 2, 2, "no",
       "same two obstructions: u = 0 for the pairs, or the two axis "
       "bodies sharing a height")
report("(0,3)", 0, 3, "YES",
       "no body is on the axis, so the three pairs can share one height "
       "v and lie on y = v with all six distinct")

print("\nB. exhibit it: a collinear, collision-free (0,3) configuration")
P = [(mp.mpf(1), mp.mpf(0)), (mp.mpf(-1), mp.mpf(0)),
     (mp.mpf("0.6"), mp.mpf(0)), (mp.mpf("-0.6"), mp.mpf(0)),
     (mp.mpf("0.25"), mp.mpf(0)), (mp.mpf("-0.25"), mp.mpf(0))]
d = [float(mp.sqrt((P[i][0] - P[j][0]) ** 2 + (P[i][1] - P[j][1]) ** 2))
     for i in range(6) for j in range(i + 1, 6)]
print(f"   six bodies at x = +-1, +-0.6, +-0.25 on y = 0")
print(f"   smallest mutual distance = {min(d):.4f} (no collision)")
print("   and it lies in the (0,3) stratum: three mirror pairs, none on "
      "the axis")

print("\nC. Moulton on that locus: is the mass ray determined, and positive?")
print("   Moulton (1910): for n bodies on a line with POSITIVE masses there")
print("   are exactly n!/2 central configurations, one per ordering up to")
print("   reflection. Read the other way, a collinear shape that is central")
print("   for some positive masses determines that mass ray uniquely.")


def collinear_cc_masses(xs):
    """Solve the collinear CC equations for the mass ray, if one exists."""
    n = len(xs)
    # centre of mass at 0 is imposed by the symmetric ansatz; the CC
    # equations for a collinear configuration on the x axis read
    #   sum_{j != i} m_j (x_j - x_i)/|x_j - x_i|^3 = -lam x_i
    A = mp.matrix(n, n + 1)
    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            A[i, j] = (xs[j] - xs[i]) / abs(xs[j] - xs[i]) ** 3
        A[i, n] = xs[i]
    U, S, V = mp.svd_r(A, full_matrices=True)
    ker = [V[n, j] for j in range(n + 1)]
    nrm = max(abs(k) for k in ker)
    ker = [k / nrm for k in ker]
    return [S[i] for i in range(min(n, len(S)))], ker


xs = [mp.mpf(t) for t in ("-1", "-0.6", "-0.25", "0.25", "0.6", "1")]
sv, ker = collinear_cc_masses(xs)
print(f"\n   smallest singular value = {float(sv[-1]):.3e} "
      f"(a kernel exists)")
ms = ker[:6]
sgn = mp.sign(ms[0]) if ms[0] != 0 else mp.mpf(1)
ms = [m * sgn for m in ms]
print("   mass ray = " + ", ".join(f"{float(m):+.5f}" for m in ms))
print(f"   lambda component = {float(ker[6] * sgn):+.5f}")
print(f"   ALL MASSES POSITIVE: {all(m > 0 for m in ms)}")
print(f"   mirror-symmetric (m1=m6, m2=m5, m3=m4): "
      f"{all(abs(ms[i] - ms[5 - i]) < mp.mpf('1e-20') for i in range(3))}")

print("\nD. dimension of the collinear locus inside the (0,3) shape space")
print("   a symmetric collinear shape is (u1, u2, u3) up to scale: 2 free")
print("   parameters. The stratum's shape space is 4-dimensional. Moulton")
print("   makes every one of those shapes central for exactly one positive")
print("   mass ray, so the collinear central configurations form a set of")
print("   dimension 2 -- which MEETS the bound dim R_2 <= 2 without")
print("   breaking it, exactly as the centred pentagon does in (2,2).")

print("\nE. sanity: does the covering's own matrix really vanish there?")
PAIR_OF = [0, 0, 1, 1, 2, 2]
ROWS = [(0, 2), (0, 3), (0, 4), (0, 5), (2, 4), (2, 5)]
rnd = random.Random(3)
worst = mp.mpf(0)
for _ in range(12):
    uu = sorted({mp.mpf(rnd.randint(10, 120)) / 128 for _ in range(3)})
    if len(uu) < 3:
        continue
    Q = []
    for u in uu:
        Q.append((u, mp.mpf(0)))
        Q.append((-u, mp.mpf(0)))
    for (i, j) in ROWS:
        for k in range(6):
            if k in (i, j):
                continue
            rik = mp.sqrt((Q[i][0] - Q[k][0]) ** 2 + (Q[i][1] - Q[k][1]) ** 2)
            rjk = mp.sqrt((Q[j][0] - Q[k][0]) ** 2 + (Q[j][1] - Q[k][1]) ** 2)
            area = ((Q[j][0] - Q[i][0]) * (Q[k][1] - Q[i][1])
                    - (Q[j][1] - Q[i][1]) * (Q[k][0] - Q[i][0]))
            worst = max(worst, abs((rik ** -3 - rjk ** -3) * area))
print(f"   largest matrix entry over 12 random collinear shapes: "
      f"{float(worst):.3e}")
