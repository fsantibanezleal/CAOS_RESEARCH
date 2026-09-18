"""How many degenerate cross configurations are there?

Rank <= 2 for the 3 x 4 system is codimension 2, and the cross face is
2-dimensional, so degenerate cross configurations are ISOLATED points. One
has been found and verified. This sweeps the face for the rest: a coarse
grid on sigma_3/sigma_1, then a local minimisation from every basin, then
a check that each survivor has an admissible (all-positive) mass ray.
"""
import mpmath as mp

mp.mp.dps = 50


def system(u, p):
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


def ratio(u, p):
    if u <= mp.mpf("0.03") or p <= u + mp.mpf("0.03") or p > 20:
        return mp.mpf(1)
    M = system(u, p)
    A = mp.matrix(3, 4)
    for i in range(3):
        n = max(abs(x) for x in M[i]) or mp.mpf(1)
        for j in range(4):
            A[i, j] = M[i][j] / n
    _, S, _ = mp.svd_r(A)
    return S[2] / S[0]


print("A. coarse sweep of sigma_3/sigma_1 over the cross face")
grid = {}
NU, NP = 90, 110
for iu in range(1, NU):
    u = mp.mpf(iu) / 30
    for ip in range(1, NP):
        p = mp.mpf(ip) / 30
        if p <= u + mp.mpf("0.05"):
            continue
        grid[(iu, ip)] = ratio(u, p)
print(f"   {len(grid)} grid points; smallest ratios:")
low = sorted(grid.items(), key=lambda kv: kv[1])[:8]
for (iu, ip), v in low:
    print(f"     u={float(mp.mpf(iu) / 30):.4f} p={float(mp.mpf(ip) / 30):.4f}"
          f"   ratio={float(v):.4e}")

print("\nB. local minima: descend from every grid point that beats its "
      "neighbours")
seeds = []
for (iu, ip), v in grid.items():
    nb = [grid.get((iu + a, ip + b)) for a in (-1, 0, 1) for b in (-1, 0, 1)
          if (a, b) != (0, 0)]
    nb = [x for x in nb if x is not None]
    if nb and v < min(nb):
        seeds.append((mp.mpf(iu) / 30, mp.mpf(ip) / 30, v))
print(f"   {len(seeds)} basins")

found = []
for (u0, p0, v0) in seeds:
    u, p, cur = u0, p0, v0
    step = mp.mpf(1) / 60
    for _ in range(400):
        moved = False
        for (du, dp) in ((step, 0), (-step, 0), (0, step), (0, -step),
                         (step, step), (-step, -step), (step, -step),
                         (-step, step)):
            v = ratio(u + du, p + dp)
            if v < cur:
                cur, u, p, moved = v, u + du, p + dp, True
                break
        if not moved:
            step /= 3
            if step < mp.mpf(10) ** -18:
                break
    found.append((u, p, cur))

found.sort(key=lambda t: t[2])
print("\n   basin minima (ratio below 1e-12 means an exact rank-2 point):")
real = []
for (u, p, v) in found:
    tag = "  <== RANK 2" if v < mp.mpf(10) ** -12 else ""
    print(f"     u={float(u):.12f}  p={float(p):.12f}  ratio={float(v):.3e}"
          f"{tag}")
    if v < mp.mpf(10) ** -12:
        real.append((u, p))

print(f"\nC. {len(real)} exact rank-2 point(s); admissible mass ray?")
for (u, p) in real:
    M = system(u, p)
    A = mp.matrix(3, 4)
    for i in range(3):
        n = max(abs(x) for x in M[i])
        for j in range(4):
            A[i, j] = M[i][j] / n
    _, _, V = mp.svd_r(A, full_matrices=True)
    k1 = [V[2, j] for j in range(4)]
    k2 = [V[3, j] for j in range(4)]
    k1 = [t / max(abs(z) for z in k1) for t in k1]
    k2 = [t / max(abs(z) for z in k2) for t in k2]
    lo = hi = None
    NT = 40000
    for i in range(2 * NT + 1):
        th = mp.pi * i / NT - mp.pi
        w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
        if all(t > 0 for t in w):
            if lo is None:
                lo = th
            hi = th
    if lo is None:
        print(f"   u={float(u):.10f} p={float(p):.10f}: kernel meets no "
              "positive orthant -> NOT a central configuration")
    else:
        print(f"   u={float(u):.12f} p={float(p):.12f}: positive arc of "
              f"width {float(hi - lo):.6f} rad -> DEGENERATE CC")
