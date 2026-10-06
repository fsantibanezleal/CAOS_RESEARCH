"""RH-034 stress test for Q >= 2N + 3O - 4S (floating point, exploratory).

Wider than rh034_linear_inequality_search.py: three window shapes eta, up to four real clusters of
multiplicity 1..4, up to three conjugate off-line pairs of multiplicity 1..2, many random starts,
and positions both spread and clustered. Reports the minimum slack per shape; a clearly negative
value (beyond 1e-7) is a counterexample and closes the candidate.
"""

from __future__ import annotations

import sys
import time

import numpy as np
from scipy.optimize import minimize

UG, WG = np.polynomial.legendre.leggauss(160)


def make_kernel(shape: str):
    u = UG
    if shape == "cos2":
        e2 = np.cos(np.pi * u / 2) ** 2
    elif shape == "mt":
        e2 = np.cos(u / np.sqrt(2))  # Montgomery-Taylor window cos(sqrt2 v) on (-1/2, 1/2), rescaled to (-1, 1)
    elif shape == "tent2":
        e2 = (1 - np.abs(u)) ** 2
    else:
        e2 = np.exp(-4 * u**2) * (1 - u**2) ** 2
    e2 = e2 / (WG @ e2)

    def k(xi):
        return (np.exp(-2j * np.pi * np.multiply.outer(xi, u)) * e2) @ WG

    return k


def slack(params, real_mult, off_mult, k, beta=3.0, gamma=4.0):
    nr, no = len(real_mult), len(off_mult)
    pts, mult = list(params[:nr].astype(complex)), list(real_mult)
    off = params[nr:].reshape(no, 2) if no else np.zeros((0, 2))
    for (x, y), m in zip(off, off_mult):
        y = abs(y) + 1e-12
        pts += [complex(x, y), complex(x, -y)]
        mult += [m, m]
    pts, mult = np.array(pts), np.array(mult, dtype=float)
    d = pts[:, None] - pts[None, :]
    kk = k(d.ravel()).reshape(d.shape)
    q = float(np.real(np.sum(mult[:, None] * mult[None, :] * kk * kk)))
    n = float(mult.sum())
    s = float(sum(1 for m in real_mult if m == 1))
    o = float(sum(1 for m in real_mult if m % 2 == 1))
    return q - (2 * n + beta * o - gamma * s)


def run(budget: float = 1500.0, seed: int = 7, shapes: tuple[str, ...] = ("cos2", "tent2", "gauss")) -> None:
    rng = np.random.default_rng(seed)
    start = time.time()
    worst = {}
    trials = 0
    while time.time() - start < budget:
        shape = shapes[trials % len(shapes)]
        k = make_kernel(shape)
        nr = int(rng.integers(0, 5))
        no = int(rng.integers(0, 4))
        if nr + no == 0:
            continue
        real_mult = tuple(int(m) for m in rng.integers(1, 5, size=nr))
        off_mult = tuple(int(m) for m in rng.integers(1, 3, size=no))
        scale = float(rng.choice([0.2, 0.6, 1.5]))
        x0 = rng.normal(scale=scale, size=nr + 2 * no)
        res = minimize(slack, x0, args=(real_mult, off_mult, k), method="Nelder-Mead", options={"maxiter": 4000, "xatol": 1e-9, "fatol": 1e-11})
        trials += 1
        if shape not in worst or res.fun < worst[shape][0]:
            worst[shape] = (res.fun, real_mult, off_mult, np.round(res.x, 4))
        if trials % 200 == 0:
            print(f"[{time.time() - start:7.1f}s] trials={trials} " + " ".join(f"{s}:{w[0]:.2e}" for s, w in worst.items()), flush=True)
    for shape, w in worst.items():
        print(f"{shape}: min slack {w[0]:.3e} real={w[1]} off={w[2]} x={w[3]}")
    print(f"trials={trials}")


if __name__ == "__main__":
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 1500.0
    shapes = tuple(sys.argv[2].split(",")) if len(sys.argv) > 2 else ("cos2", "tent2", "gauss")
    run(budget, shapes=shapes)
