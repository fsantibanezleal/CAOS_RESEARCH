"""Nested high-precision minimisation: does sigma_3 reach zero?

Outer golden section over u, inner golden section over p. If the minimum
falls like the bracket width, sigma_3 has a genuine zero and the point is
exactly rank 2. If it plateaus, it is a near-miss like the three the
campaign has already rejected, and the distinction is the whole question.
"""
import mpmath as mp

mp.mp.dps = 80

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
PAIR_OF = [None, None, 2, 2, 3, 3]


def svd_at(u, p):
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, mp.mpf(0)), (-u, mp.mpf(0)), (p, mp.mpf(0)), (-p, mp.mpf(0))]
    A = mp.matrix(6, 4)
    for r, (i, j) in enumerate(ROWS):
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
        n = max(abs(x) for x in c) or mp.mpf(1)
        for j2 in range(4):
            A[r, j2] = c[j2] / n
    return mp.svd_r(A)


def s3(u, p):
    if u <= mp.mpf("0.02") or p <= u + mp.mpf("0.02"):
        return mp.mpf(10)
    _, S, _ = svd_at(u, p)
    return S[2]


GR = (mp.sqrt(5) - 1) / 2


def gmin(f, lo, hi, iters):
    a, b = mp.mpf(lo), mp.mpf(hi)
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


def inner(u, plo, phi, iters=90):
    return gmin(lambda p: s3(u, p), plo, phi, iters)


print("nested minimisation, tightening the u bracket each round")
ulo, uhi = mp.mpf("0.6308"), mp.mpf("0.6310")
plo, phi = mp.mpf("1.4505"), mp.mpf("1.4513")
for rnd in range(7):
    def outer(u):
        return inner(u, plo, phi)[1]
    u, val = gmin(outer, ulo, uhi, 60)
    p, val2 = inner(u, plo, phi, 120)
    w = (uhi - ulo)
    print(f"  round {rnd}: bracket {float(w):.2e}   u={mp.nstr(u, 20)}")
    print(f"            p={mp.nstr(p, 20)}   sigma_3={mp.nstr(val2, 8)}")
    ulo, uhi = u - w / 20, u + w / 20
    plo, phi = p - (phi - plo) / 20, p + (phi - plo) / 20

print("\nfinal singular values")
_, S, V = svd_at(u, p)
print("  " + ", ".join(mp.nstr(S[i], 8) for i in range(4)))
print(f"\n  sigma_3/sigma_1 = {mp.nstr(S[2] / S[0], 8)}")
if S[2] / S[0] < mp.mpf(10) ** -25:
    print("  -> EXACT RANK 2: this is a degenerate central configuration")
else:
    print("  -> sigma_3 PLATEAUS: rank is 3, not 2; a near-miss, and the")
    print("     kernel is one-dimensional so it is an ordinary point of")
    print("     the cross family rather than a degenerate one")
