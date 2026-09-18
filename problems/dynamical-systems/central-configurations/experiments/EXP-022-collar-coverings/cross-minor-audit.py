"""Which minors actually vanish, and is sigma_3 really reaching zero?

Newton killed two chosen 3x3 minors to 1e-122 but left sigma_3 at 8e-21,
while the nested minimiser's nearby point had sigma_3 = 8.6e-24. Those two
facts cannot both describe a rank-2 point, so this audits ALL 3x3 minors
at both points and then pushes the minimisation far enough to decide
whether the infimum of sigma_3 is zero or a small positive plateau.
"""
import itertools
import mpmath as mp

mp.mp.dps = 200

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


def audit(name, u, p):
    M = rows_at(u, p)
    scale = max(abs(M[i][j]) for i in range(6) for j in range(4))
    vals = []
    for rows in itertools.combinations(range(6), 3):
        for cols in itertools.combinations(range(4), 3):
            vals.append(abs(det3(M, rows, cols)) / scale ** 3)
    A = mp.matrix(6, 4)
    for i in range(6):
        n = max(abs(x) for x in M[i])
        for j in range(4):
            A[i, j] = M[i][j] / n
    _, S, _ = mp.svd_r(A)
    print(f"  {name}")
    print(f"    sigma = " + ", ".join(mp.nstr(S[i], 8) for i in range(4)))
    print(f"    3x3 minors (80 of them): max {mp.nstr(max(vals), 6)}   "
          f"median {mp.nstr(sorted(vals)[len(vals) // 2], 6)}")
    return S[2]


print("A. the two candidate points")
uN = mp.mpf("0.630918137106736797174733661069437694669385034")
pN = mp.mpf("1.45090746590807305720015347712719492140257986")
uM = mp.mpf("0.63091813710673679717")
pM = mp.mpf("1.4509074659080730572")
audit("Newton point (two minors forced to zero)", uN, pN)
audit("nested-minimiser point", uM, pM)

print("\nB. push the minimisation much further and watch sigma_3")


def s3(u, p):
    M = rows_at(u, p)
    A = mp.matrix(6, 4)
    for i in range(6):
        n = max(abs(x) for x in M[i])
        for j in range(4):
            A[i, j] = M[i][j] / n
    _, S, _ = mp.svd_r(A)
    return S[2]


GR = (mp.sqrt(5) - 1) / 2


def gmin(f, a, b, iters):
    a, b = mp.mpf(a), mp.mpf(b)
    c, d = b - GR * (b - a), a + GR * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(iters):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - GR * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + GR * (b - a)
            fd = f(d)
    m = (a + b) / 2
    return m, f(m)


ulo, uhi = uM - mp.mpf(10) ** -12, uM + mp.mpf(10) ** -12
plo, phi = pM - mp.mpf(10) ** -12, pM + mp.mpf(10) ** -12
for rnd in range(6):
    u, _ = gmin(lambda uu: gmin(lambda pp: s3(uu, pp), plo, phi, 70)[1],
                ulo, uhi, 70)
    p, val = gmin(lambda pp: s3(u, pp), plo, phi, 140)
    w = uhi - ulo
    print(f"   bracket {mp.nstr(w, 4)}  sigma_3 = {mp.nstr(val, 8)}")
    ulo, uhi = u - w / 30, u + w / 30
    plo, phi = p - (phi - plo) / 30, p + (phi - plo) / 30
print(f"\n   u = {mp.nstr(u, 40)}")
print(f"   p = {mp.nstr(p, 40)}")
