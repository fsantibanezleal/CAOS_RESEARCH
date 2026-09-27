"""Exploratory, uncertified floating-point computation from the 2026-09-27 sweep (see ../README.md)."""

import numpy as np
from scipy.optimize import brentq


def minQ(lam, n=1500):
    # g on [-lam/2,lam/2], Q = (||g||^2 + int int |x-y| g g)/(int g)^2 ; midpoint rule
    h = lam / n
    x = (np.arange(n) + 0.5) * h - lam / 2
    A = np.eye(n) * h + np.abs(x[:, None] - x[None, :]) * h * h
    w = np.ones(n) * h
    return 1.0 / (w @ np.linalg.solve(A, w))


def fejer(lam):
    return 1 / lam + lam / 3


for lam in [1.0, 0.8, 0.6, 0.55, 0.534, 0.5]:
    q = minQ(lam)
    print(
        f"lam={lam}: MT-type sum m <= {q:.5f}, simple>= {2 - q:.5f}, distinct>=({(3 - q) / 2:.5f}); Fejer sum m<= {fejer(lam):.5f}"
    )
t = brentq(lambda l: minQ(l) - 2, 0.3, 1.0)
print("MT-type threshold simple>0:", t)
print("Fejer threshold 3-sqrt6 =", 3 - 6**0.5)
