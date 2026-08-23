"""The rank-2 point of the cross face, and whether it is a central
configuration.

On the face v = q = 0 the rank is 3 almost everywhere (sigma_4 vanishes
identically). band's residue sits where sigma_3 collapses too, to 1.19e-4
against neighbours of 0.16 to 1.5, so it is a RANK-2 point of the face.
Rank 2 gives a two-dimensional kernel, i.e. a whole line of admissible
mass rays, which is what the dimension count has to bound.

The centred pentagon is the (2,2) stratum's known sharp degenerate point,
exact rank 2 with a positive kernel. If this cross point is also rank 2
with a positive kernel it is a SECOND one, and the theorem statement has
to name it.
"""
import random
import mpmath as mp

mp.mp.dps = 60

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
PAIR_OF = [None, None, 2, 2, 3, 3]


def M_of(u, v, p, q):
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, v), (-u, v), (p, q), (-p, q)]
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


def norm_svd(u, p):
    A = mp.matrix(6, 4)
    M = M_of(u, mp.mpf(0), p, mp.mpf(0))
    for i in range(6):
        n = max(abs(x) for x in M[i]) or mp.mpf(1)
        for j in range(4):
            A[i, j] = M[i][j] / n
    return mp.svd_r(A)


def s3(u, p):
    if u <= mp.mpf("0.02") or p <= u + mp.mpf("0.02"):
        return mp.mpf(10)
    _, S, _ = norm_svd(u, p)
    return S[2]


print("A. descent on sigma_3 over the face, from band's residue")
rnd = random.Random(9)
x = [mp.mpf("0.63092"), mp.mpf("1.45090")]
best = s3(*x)
step = mp.mpf(1) / 256
for it in range(4000):
    y = [x[i] + step * (mp.mpf(rnd.random()) - mp.mpf(1) / 2) for i in range(2)]
    v = s3(*y)
    if v < best:
        best, x = v, y
    if it % 500 == 499:
        step /= 3
print(f"   sigma_3 = {mp.nstr(best, 10)}")
print(f"   at u = {mp.nstr(x[0], 14)}, p = {mp.nstr(x[1], 14)}")

print("\nB. all four singular values there")
U, S, V = norm_svd(*x)
print("   " + ", ".join(f"{float(S[i]):.8e}" for i in range(4)))

print("\nC. the two-dimensional kernel, and whether it contains a positive ray")
k1 = [V[2, j] for j in range(4)]
k2 = [V[3, j] for j in range(4)]
n1 = max(abs(t) for t in k1)
n2 = max(abs(t) for t in k2)
k1 = [t / n1 for t in k1]
k2 = [t / n2 for t in k2]
print("   kernel basis 1: " + ", ".join(f"{float(t):+.8f}" for t in k1))
print("   kernel basis 2: " + ", ".join(f"{float(t):+.8f}" for t in k2))
pos = None
NT = 4000
for i in range(NT + 1):
    th = mp.pi * i / NT
    w = [mp.cos(th) * k1[j] + mp.sin(th) * k2[j] for j in range(4)]
    if all(t > 0 for t in w) or all(t < 0 for t in w):
        pos = (th, [t if w[0] > 0 else -t for t in w])
        break
if pos:
    th, w = pos
    nn = max(abs(t) for t in w)
    w = [t / nn for t in w]
    print(f"   POSITIVE RAY FOUND at theta = {float(th):.6f}")
    print("   masses (m1, m2, mA, mB) = "
          + ", ".join(f"{float(t):+.8f}" for t in w))
else:
    print("   NO positive ray in the kernel: not a central configuration")

print("\nD. direct check against the ACTUAL central-configuration equations")
if pos:
    _, w = pos
    nn = max(abs(t) for t in w)
    w = [t / nn for t in w]
    m = [w[0], w[1], w[2], w[2], w[3], w[3]]
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (x[0], mp.mpf(0)), (-x[0], mp.mpf(0)),
         (x[1], mp.mpf(0)), (-x[1], mp.mpf(0))]
    tot = sum(m)
    cx = sum(m[i] * P[i][0] for i in range(6)) / tot
    cy = sum(m[i] * P[i][1] for i in range(6)) / tot
    print(f"   centre of mass = ({float(cx):.3e}, {float(cy):.3e})")
    acc = []
    for i in range(6):
        ax = ay = mp.mpf(0)
        for j in range(6):
            if j == i:
                continue
            dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
            r3 = (dx * dx + dy * dy) ** mp.mpf("1.5")
            ax += m[j] * dx / r3
            ay += m[j] * dy / r3
        acc.append((ax, ay))
    lam = []
    for i in range(6):
        for d in range(2):
            den = (P[i][d] - (cx if d == 0 else cy))
            if abs(den) > mp.mpf("1e-12"):
                lam.append(-acc[i][d] / den)
    lam0 = lam[0]
    resid = max(abs(l - lam0) for l in lam)
    print(f"   lambda from every coordinate: spread = {float(resid):.3e}")
    print(f"   lambda = {mp.nstr(lam0, 12)}")
    print(f"   IS A CENTRAL CONFIGURATION: {float(resid) < 1e-25}")
