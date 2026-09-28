"""RH-034 follow-up: how low can (Q - 2N)/O go with S = 0 (floating point, exploratory).

The linear candidate Q >= 2N + 3O - 4S is false for the Montgomery-Taylor window: six triples at
about +-0.949, +-1.993, +-3.033 around one conjugate pair at +-0.2456 i give Q = 57.94178 < 58 = 2N + 3O
(verified at 40 digits with the closed-form kernel). This script searches configurations with S = 0
(triples plus conjugate pairs, multiplicity-one pairs) for the infimum beta* of (Q - 2N)/O. A value of
beta* above 2 would still give a linear inequality stronger than the EXP-006 product near the onset;
beta* = 2 would mean the product is asymptotically sharp there.
"""

from __future__ import annotations

import sys
import time

import numpy as np
from scipy.optimize import minimize

A_HALF = 0.5
B = np.sqrt(2.0)
NORM = 2 * np.sin(B * A_HALF) / B


def kernel(xi: np.ndarray) -> np.ndarray:
    c = 2 * np.pi * xi
    d1, d2 = B - c, B + c
    t1 = np.where(np.abs(d1) < 1e-12, A_HALF, np.sin(d1 * A_HALF) / np.where(np.abs(d1) < 1e-12, 1, d1))
    t2 = np.where(np.abs(d2) < 1e-12, A_HALF, np.sin(d2 * A_HALF) / np.where(np.abs(d2) < 1e-12, 1, d2))
    return (t1 + t2) / NORM


def ratio(params: np.ndarray, n_t: int, n_p: int) -> float:
    xt = params[:n_t]
    pp = params[n_t:].reshape(n_p, 2)
    pts = list(xt.astype(complex))
    mult = [3.0] * n_t
    for x, y in pp:
        y = abs(y) + 1e-9
        pts += [complex(x, y), complex(x, -y)]
        mult += [1.0, 1.0]
    pts = np.array(pts)
    m = np.array(mult)
    d = pts[:, None] - pts[None, :]
    kk = kernel(d)
    q = float(np.real(np.sum(m[:, None] * m[None, :] * kk * kk)))
    n = m.sum()
    return (q - 2 * n) / n_t


def main(budget: float = 900.0, seed: int = 3) -> None:
    rng = np.random.default_rng(seed)
    best = (np.inf, None)
    start = time.time()
    trials = 0
    while time.time() - start < budget:
        n_t = int(rng.integers(1, 11))
        n_p = int(rng.integers(1, 6))
        span = float(rng.choice([2.0, 4.0, 8.0]))
        xt = rng.uniform(-span, span, size=n_t)
        pp = np.column_stack([rng.uniform(-span, span, size=n_p), rng.uniform(0.05, 0.6, size=n_p)]).ravel()
        res = minimize(ratio, np.r_[xt, pp], args=(n_t, n_p), method="Nelder-Mead", options={"maxiter": 8000, "xatol": 1e-9, "fatol": 1e-11})
        trials += 1
        if res.fun < best[0]:
            best = (res.fun, (n_t, n_p, np.round(res.x, 4)))
            print(f"[{time.time() - start:6.1f}s] trial {trials}: (Q-2N)/O = {res.fun:.5f} with {n_t} triples, {n_p} pairs", flush=True)
    print(f"best (Q-2N)/O = {best[0]:.6f}; config {best[1]}; trials={trials}")


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 900.0)
