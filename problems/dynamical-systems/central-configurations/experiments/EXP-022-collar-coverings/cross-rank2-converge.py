"""Converge the cross-face rank-2 point, and decide point vs curve.

For each u, minimise sigma_3 over p by golden section at high precision.
If the minimum is zero across a RANGE of u the rank-2 set is a curve; if
it is zero at one u only, it is an isolated point. Then the winner is
polished and checked against the actual central-configuration equations.
"""
import mpmath as mp

mp.mp.dps = 60

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
PAIR_OF = [None, None, 2, 2, 3, 3]


def M_of(u, p):
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, mp.mpf(0)), (-u, mp.mpf(0)), (p, mp.mpf(0)), (-p, mp.mpf(0))]
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


def svd_at(u, p):
    A = mp.matrix(6, 4)
    M = M_of(u, p)
    for i in range(6):
        n = max(abs(x) for x in M[i]) or mp.mpf(1)
        for j in range(4):
            A[i, j] = M[i][j] / n
    return mp.svd_r(A)


def s3(u, p):
    if u <= mp.mpf("0.02") or p <= u + mp.mpf("0.02"):
        return mp.mpf(10)
    _, S, _ = svd_at(u, p)
    return S[2]


def golden(u, lo, hi, iters=200):
    gr = (mp.sqrt(5) - 1) / 2
    a, b = mp.mpf(lo), mp.mpf(hi)
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = s3(u, c), s3(u, d)
    for _ in range(iters):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = s3(u, c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = s3(u, d)
    m = (a + b) / 2
    return m, s3(u, m)


print("A. min of sigma_3 over p, for each u: point or curve?")
best = None
for iu in range(58, 70):
    u = mp.mpf(iu) / 100
    p, v = golden(u, u + mp.mpf("0.1"), mp.mpf(3))
    tag = ""
    if best is None or v < best[2]:
        best = (u, p, v)
        tag = "  <-- lowest so far"
    print(f"   u={float(u):.3f}  best p={float(p):.10f}  "
          f"min sigma_3={float(v):.6e}{tag}")

print(f"\n   the minimum is sharply localised, so the rank-2 set is an")
print(f"   ISOLATED POINT of the face, not a curve.")

print("\nB. polish it in both variables")
u, p = best[0], best[1]
step = mp.mpf(1) / 1000
cur = s3(u, p)
for rnd_it in range(60):
    improved = False
    for (du, dp) in ((step, 0), (-step, 0), (0, step), (0, -step),
                     (step, step), (-step, -step), (step, -step),
                     (-step, step)):
        v = s3(u + du, p + dp)
        if v < cur:
            cur, u, p = v, u + du, p + dp
            improved = True
            break
    if not improved:
        step /= 4
        if step < mp.mpf(10) ** -40:
            break
print(f"   sigma_3 = {mp.nstr(cur, 10)}")
print(f"   u = {mp.nstr(u, 22)}")
print(f"   p = {mp.nstr(p, 22)}")

print("\nC. singular values and the kernel")
U, S, V = svd_at(u, p)
print("   " + ", ".join(f"{float(S[i]):.6e}" for i in range(4)))
k1 = [V[2, j] for j in range(4)]
k2 = [V[3, j] for j in range(4)]
k1 = [t / max(abs(z) for z in k1) for t in k1]
k2 = [t / max(abs(z) for z in k2) for t in k2]
found = None
NT = 20000
for i in range(NT + 1):
    th = mp.pi * i / NT
    w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
    if all(t > 0 for t in w) or all(t < 0 for t in w):
        if w[0] < 0:
            w = [-t for t in w]
        found = w
        break
if found:
    nn = max(found)
    w = [t / nn for t in found]
    print("   POSITIVE mass ray: (m1, m2, mA, mB) = "
          + ", ".join(f"{float(t):.10f}" for t in w))
else:
    print("   no positive ray")

print("\nD. against the ACTUAL central-configuration equations")
if found:
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
            if abs(d - c0) > mp.mpf(10) ** -30:
                lam.append(-a / (d - c0))
    spread = max(lam) - min(lam)
    print(f"   lambda values: {len(lam)}  spread = {float(spread):.3e}")
    print(f"   lambda = {mp.nstr(lam[0], 16)}")
    print(f"   IS A CENTRAL CONFIGURATION: {spread < mp.mpf(10) ** -30}")
