"""Decide: exact rank-2 point vs conditioning near-miss (pure mpmath).

Numeric matrix at v = q = t (equal heights, f = 0), chart u > p > 0.
"""
import mpmath as mp

mp.mp.dps = 50

def J_at(u, p, t):
    h1 = 1 - t
    gam = -1 - t
    dA1 = mp.sqrt(u**2 + h1**2)
    dA2 = mp.sqrt(u**2 + gam**2)
    dB1 = mp.sqrt(p**2 + h1**2)
    dB2 = mp.sqrt(p**2 + gam**2)
    cs = u - p
    cx = u + p
    wA, wB, r12 = 2 * u, 2 * p, mp.mpf(2)
    s = lambda a, b: a**-3 - b**-3
    J = [[mp.mpf(0)] * 4 for _ in range(6)]
    J[0][1] = s(r12, dA2) * (-2 * u)
    J[0][2] = s(dA1, wA) * (-2 * u * h1)
    J[0][3] = s(dB1, cs) * (p * h1 - u * h1) + s(dB1, cx) * (-(u * h1 + p * h1))
    J[1][1] = s(r12, dB2) * (-2 * p)
    J[1][2] = s(dA1, cs) * (u * h1 - p * h1) + s(dA1, cx) * (-(p * h1 + u * h1))
    J[1][3] = s(dB1, wB) * (-2 * p * h1)
    J[2][0] = s(r12, dA1) * (2 * u)
    J[2][2] = s(dA2, wA) * (-2 * u * gam)
    J[2][3] = s(dB2, cs) * (p * gam - u * gam) + s(dB2, cx) * (-(u * gam + p * gam))
    J[3][0] = s(r12, dB1) * (2 * p)
    J[3][2] = s(dA2, cs) * (u * gam - p * gam) + s(dA2, cx) * (-(p * gam + u * gam))
    J[3][3] = s(dB2, wB) * (-2 * p * gam)
    J[4][0] = s(dA1, dB1) * (p * h1 - u * h1)
    J[4][1] = s(dA2, dB2) * (p * gam - u * gam)
    J[5][0] = s(dA1, dB1) * (-(u * h1 + p * h1))
    J[5][1] = s(dA2, dB2) * (-(u * gam + p * gam))
    return J

def det3(J, rr, cc):
    a, b, c = rr
    x, y, z = cc
    return (J[a][x] * (J[b][y] * J[c][z] - J[b][z] * J[c][y])
            - J[a][y] * (J[b][x] * J[c][z] - J[b][z] * J[c][x])
            + J[a][z] * (J[b][x] * J[c][y] - J[b][y] * J[c][x]))

U = mp.mpf("1.4507")
M1 = lambda p, t: det3(J_at(U, p, t), (0, 1, 2), (1, 2, 3))
M2 = lambda p, t: det3(J_at(U, p, t), (1, 2, 3), (0, 1, 2))
M3 = lambda p, t: det3(J_at(U, p, t), (0, 2, 4), (0, 1, 2))

r1 = mp.findroot(lambda p: M1(p, mp.mpf(0)), mp.mpf("0.63"))
r2 = mp.findroot(lambda p: M2(p, mp.mpf(0)), mp.mpf("0.63"))
r3 = mp.findroot(lambda p: M3(p, mp.mpf(0)), mp.mpf("0.63"))
print("root M1:", mp.nstr(r1, 25))
print("root M2:", mp.nstr(r2, 25))
print("root M3:", mp.nstr(r3, 25))
print("|r1-r2| =", mp.nstr(abs(r1 - r2), 5), " |r1-r3| =", mp.nstr(abs(r1 - r3), 5))

try:
    P0, T0 = mp.findroot(lambda P, T: (M1(P, T), M2(P, T)),
                         (mp.mpf("0.63"), mp.mpf("0.001")))
    print("joint (M1,M2): p =", mp.nstr(P0, 20), " t =", mp.nstr(T0, 20))
    print("M3 there:", mp.nstr(abs(M3(P0, T0)), 5))
    # singular values of the full matrix at the joint point
    A = mp.matrix(6, 4)
    Jj = J_at(U, P0, T0)
    for i in range(6):
        for j in range(4):
            A[i, j] = Jj[i][j]
    sv = mp.svd_r(A, compute_uv=False)
    print("singular values:", [mp.nstr(s, 8) for s in sv])
except Exception as e:
    print("joint solve failed:", type(e).__name__, e)
