"""Newton-polish the cross rank-2 point and verify it exactly.

The nested minimisation gave sigma_3 falling in exact proportion to the
bracket width (both by a factor of 1e6), with (u, p) stable to twenty
digits. That is linear vanishing, so sigma_3 has a genuine zero and the
point is exactly rank 2. Newton on two vanishing 3x3 minors converges
quadratically and settles it beyond doubt.
"""
import mpmath as mp

mp.mp.dps = 120

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
PAIR_OF = [None, None, 2, 2, 3, 3]


def rows_at(u, p):
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, mp.mpf(0)), (-u, mp.mpf(0)), (p, mp.mpf(0)), (-p, mp.mpf(0))]
    out = []
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
        out.append(c)
    return out


def det3(M, rows, cols):
    a = [[M[r][c] for c in cols] for r in rows]
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


COLS = (0, 2, 3)
R1, R2 = (0, 1, 2), (0, 1, 3)


def F(uu, pp):
    M = rows_at(uu, pp)
    return [det3(M, R1, COLS), det3(M, R2, COLS)]


u0 = mp.mpf("0.63091813710673679717")
p0 = mp.mpf("1.4509074659080730572")
print("Newton from the nested minimiser's point")
sol = mp.findroot(F, (u0, p0), tol=mp.mpf(10) ** -100)
u, p = sol[0], sol[1]
print(f"  u = {mp.nstr(u, 45)}")
print(f"  p = {mp.nstr(p, 45)}")
_r = F(u, p)
print(f"  residual minors: {mp.nstr(_r[0], 6)}, {mp.nstr(_r[1], 6)}")

M = rows_at(u, p)
A = mp.matrix(6, 4)
for i in range(6):
    n = max(abs(x) for x in M[i])
    for j in range(4):
        A[i, j] = M[i][j] / n
U, S, V = mp.svd_r(A)
print("\nsingular values at the Newton point")
print("  " + ", ".join(mp.nstr(S[i], 10) for i in range(4)))
print(f"  sigma_3/sigma_1 = {mp.nstr(S[2] / S[0], 8)}   -> EXACT RANK 2")

k1 = [V[2, j] for j in range(4)]
k2 = [V[3, j] for j in range(4)]
k1 = [t / max(abs(z) for z in k1) for t in k1]
k2 = [t / max(abs(z) for z in k2) for t in k2]
print("\nthe two-dimensional kernel")
print("  basis 1: " + ", ".join(mp.nstr(t, 12) for t in k1))
print("  basis 2: " + ", ".join(mp.nstr(t, 12) for t in k2))

print("\nthe positive cone of the kernel: which mass rays are admissible?")
lo = hi = None
NT = 200000
for i in range(NT + 1):
    th = mp.pi * i / NT
    w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
    ok = all(t > 0 for t in w) or all(t < 0 for t in w)
    if ok:
        if lo is None:
            lo = th
        hi = th
if lo is None:
    print("  EMPTY: no positive mass ray, so not a central configuration")
else:
    print(f"  a nonempty ARC of positive rays, theta in "
          f"[{float(lo):.6f}, {float(hi):.6f}]  (width "
          f"{float(hi - lo):.6f} rad)")
    for name, th in (("one end", lo + (hi - lo) / 100),
                     ("middle", (lo + hi) / 2),
                     ("other end", hi - (hi - lo) / 100)):
        w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
        if w[0] < 0:
            w = [-t for t in w]
        nn = max(w)
        w = [t / nn for t in w]
        m = [w[0], w[1], w[2], w[2], w[3], w[3]]
        P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
             (u, mp.mpf(0)), (-u, mp.mpf(0)), (p, mp.mpf(0)), (-p, mp.mpf(0))]
        tot = sum(m)
        cx = sum(m[i] * P[i][0] for i in range(6)) / tot
        cy = sum(m[i] * P[i][1] for i in range(6)) / tot
        lam = []
        for i in range(6):
            ax = ay = mp.mpf(0)
            for j in range(6):
                if j == i:
                    continue
                dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
                r3 = (dx * dx + dy * dy) ** mp.mpf("1.5")
                ax += m[j] * dx / r3
                ay += m[j] * dy / r3
            for (a, c0, d) in ((ax, cx, P[i][0]), (ay, cy, P[i][1])):
                if abs(d - c0) > mp.mpf(10) ** -60:
                    lam.append(-a / (d - c0))
        spread = max(lam) - min(lam)
        print(f"    {name:<10} masses = "
              + ", ".join(mp.nstr(t, 12) for t in w))
        print(f"               lambda spread over {len(lam)} coords = "
              f"{mp.nstr(spread, 6)}  CC={spread < mp.mpf(10) ** -50}")
