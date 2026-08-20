"""Classify the ulow trapped structure: exact rank-2 or near-miss?

Singular values at a trapped midpoint (u, v, p, q) = (63/512, 1023/1024,
6667/4096, 171/1024) (the A-near-body-1 collar), then random descent on
sigma_3^2 + sigma_4^2 to see whether the bottom pair reaches zero.
"""
import random
import mpmath as mp

mp.mp.dps = 40

def J_at(u, v, p, q):
    h1 = 1 - v; gam = -1 - v; g1 = 1 - q; g2 = -1 - q; f = v - q
    d1A = mp.sqrt(u**2 + h1**2); d2A = mp.sqrt(u**2 + gam**2)
    d1B = mp.sqrt(p**2 + g1**2); d2B = mp.sqrt(p**2 + g2**2)
    cs = mp.sqrt((u - p)**2 + f**2); cx = mp.sqrt((u + p)**2 + f**2)
    wA = 2 * u; wB = 2 * p; r12 = mp.mpf(2)
    s = lambda a, b: a**-3 - b**-3
    J = [[mp.mpf(0)] * 4 for _ in range(6)]
    J[0][1] = s(r12, d2A) * (-2 * u)
    J[0][2] = s(d1A, wA) * (-2 * u * h1)
    J[0][3] = s(d1B, cs) * (p * h1 - u * g1) + s(d1B, cx) * (-(u * g1 + p * h1))
    J[1][1] = s(r12, d2B) * (-2 * p)
    J[1][2] = s(d1A, cs) * (u * g1 - p * h1) + s(d1A, cx) * (-(p * h1 + u * g1))
    J[1][3] = s(d1B, wB) * (-2 * p * g1)
    J[2][0] = s(r12, d1A) * (2 * u)
    J[2][2] = s(d2A, wA) * (-2 * u * gam)
    J[2][3] = s(d2B, cs) * (p * gam - u * g2) + s(d2B, cx) * (-(u * g2 + p * gam))
    J[3][0] = s(r12, d1B) * (2 * p)
    J[3][2] = s(d2A, cs) * (u * g2 - p * gam) + s(d2A, cx) * (-(p * gam + u * g2))
    J[3][3] = s(d2B, wB) * (-2 * p * g2)
    J[4][0] = s(d1A, d1B) * (p * h1 - u * g1)
    J[4][1] = s(d2A, d2B) * (p * gam - u * g2)
    J[4][2] = s(wA, cx) * (-2 * f * u)
    J[4][3] = s(cx, wB) * (-2 * f * p)
    J[5][0] = s(d1A, d1B) * (-(u * g1 + p * h1))
    J[5][1] = s(d2A, d2B) * (-(u * g2 + p * gam))
    J[5][2] = s(wA, cs) * (-2 * f * u)
    J[5][3] = s(cs, wB) * (2 * f * p)
    return J

def svals(u, v, p, q):
    A = mp.matrix(6, 4)
    Jj = J_at(u, v, p, q)
    for i in range(6):
        for j in range(4):
            A[i, j] = Jj[i][j]
    return mp.svd_r(A, compute_uv=False)

pt = (mp.mpf(63) / 512, mp.mpf(1023) / 1024, mp.mpf(6667) / 4096, mp.mpf(171) / 1024)
sv = svals(*pt)
print("sv at trapped midpoint:", [mp.nstr(x, 8) for x in sv])

def s34(x):
    s = svals(*x)
    return s[2] * s[2] + s[3] * s[3]

x = list(pt)
best = s34(x)
step = mp.mpf(1) / 64
random.seed(5)
for it in range(400):
    y = [xi + step * (random.random() - mp.mpf(1) / 2) for xi in x]
    if y[0] <= mp.mpf(1) / 32 or y[2] <= mp.mpf(1) / 4:
        continue
    v2 = s34(y)
    if v2 < best:
        best, x = v2, y
    if it % 100 == 99:
        step /= 4
sv = svals(*x)
print("after descent:", [mp.nstr(t, 8) for t in sv])
print("at point:", [mp.nstr(t, 10) for t in x])
