"""Exploratory, uncertified floating-point computation from the 2026-09-27 sweep (see ../README.md)."""

import numpy as np
from scipy.optimize import linprog


def ce(lam, A_mult=2.5, m=50, X=40, nx=4000):
    h = lam / m
    K = int(round(A_mult * lam / h))
    a = (
        np.arange(0, K + 1) * h
    )  # nodes, even r-hat, hats centered at a_k (k=0 half-hat counted fully as even)
    # r(x)=sum c_k * FT(hat_k)(x); hat centered a_k (even-symmetrized): FT = 2cos(2pi a_k x) h sinc^2(hx) for k>0, h sinc^2(hx) for k=0
    x = np.linspace(0, X / lam, nx)
    s = np.sinc(h * x) ** 2 * h
    M = np.array([(s if k == 0 else 2 * np.cos(2 * np.pi * a[k] * x) * s) for k in range(K + 1)]).T
    # objective: rhat(0)=c0 ; int_{|a|<=lam} |a| rhat = 2 * int_0^lam a*rhat(a)
    obj = np.zeros(K + 1)
    obj[0] += 1
    # exact integral of a*hat_k over [0,lam] (hat_k within [0,lam] for k<=m-1; k=m straddles)
    from numpy.polynomial import legendre

    g, wg = legendre.leggauss(40)
    for k in range(K + 1):
        lo, hi = max(0, a[k] - h), min(lam, a[k] + h)
        if hi <= lo:
            continue
        t = (g + 1) / 2 * (hi - lo) + lo
        hat = np.clip(1 - np.abs(t - a[k]) / h, 0, None)
        obj[k] += 2 * np.sum(wg * (hi - lo) / 2 * t * hat)
    # constraints: r(x)>=0 -> -M c <=0 ; r(0)=1 ; c_k<=0 for a_k>=lam (outside), c_k free inside
    bounds = [(None, None) if a[k] < lam else (None, 0) for k in range(K + 1)]
    r0 = M[0]
    res = linprog(obj, A_ub=-M, b_ub=np.zeros(nx), A_eq=r0[None, :], b_eq=[1], bounds=bounds, method="highs")
    return res.fun, res


for lam in [1.0, 0.6, 0.55, 0.534]:
    v, res = ce(lam)
    print(lam, "CE-relaxed sum m <=", round(v, 5), " simple>=", round(2 - v, 5))
    v2, _ = ce(lam, A_mult=1.0)
    print("   bandlimited LP (same discretization):", round(v2, 5))
