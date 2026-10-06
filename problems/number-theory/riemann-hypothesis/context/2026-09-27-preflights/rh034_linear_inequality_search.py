"""RH-034 invariant-first search (floating point, exploratory).

Lamzouri's Proposition 2.1 and the EXP-006 product constrain, for a conjugation-invariant finite
multiset Z, the quantities N (copies), S (simple real points), O (distinct odd-multiplicity real
points) and Q = sum_{z,s} K(z-s)^2 with K = (eta^2)^, supp eta in (-lam, lam), K(0) = 1.

For separated real clusters with S = 0 the minimum of Q/N at odd fraction k = O/N is 2 + 3k
(doubles and triples), strictly above the EXP-006 curve 2/(1-k) for 0 < k < 1/3. This script
searches for multisets violating the linear candidate

    Q >= 2N + beta*O - gamma*S          (beta = 3, gamma = 4 fits single points of order 1, 2, 3),

including off-line conjugate pairs and near-collisions, by minimizing Q - (2N + beta O - gamma S)
over continuous positions for many combinatorial types. A negative minimum is a counterexample.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.optimize import minimize

LAM = 1.0
UG, WG = np.polynomial.legendre.leggauss(200)
U = LAM * UG
WU = LAM * WG
ETA2 = np.cos(np.pi * U / (2 * LAM)) ** 2
ETA2 = ETA2 / (WU @ ETA2)


def kernel(xi: np.ndarray) -> np.ndarray:
    return (np.exp(-2j * np.pi * np.multiply.outer(xi, U)) * ETA2) @ WU


def q_value(points: np.ndarray, mult: np.ndarray) -> float:
    d = points[:, None] - points[None, :]
    k = kernel(d.ravel()).reshape(d.shape)
    return float(np.real(np.sum(mult[:, None] * mult[None, :] * k * k)))


def build(real_pos, real_mult, off_pos) -> tuple[np.ndarray, np.ndarray]:
    pts = list(real_pos)
    mult = list(real_mult)
    for x, y in off_pos:
        pts += [complex(x, y), complex(x, -y)]
        mult += [1, 1]
    return np.array(pts, dtype=complex), np.array(mult, dtype=float)


def slack(config_type, params, beta, gamma):
    real_mult, n_off = config_type
    nr = len(real_mult)
    real_pos = params[:nr]
    off = params[nr:].reshape(n_off, 2) if n_off else np.zeros((0, 2))
    off = [(x, abs(y) + 1e-9) for x, y in off]
    pts, mult = build(real_pos, real_mult, off)
    n = float(np.sum(mult))
    s = float(sum(1 for m in real_mult if m == 1))
    # distinct real support points (merge coincident ones is not modelled; positions are continuous)
    o = float(sum(1 for m in real_mult if m % 2 == 1))
    return q_value(pts, mult) - (2 * n + beta * o - gamma * s)


def search(beta: float = 3.0, gamma: float = 4.0, starts: int = 12, seed: int = 1):
    rng = np.random.default_rng(seed)
    worst = (math.inf, None, None)
    types = []
    for nr in range(0, 4):
        for real_mult in itertools.product((1, 2, 3), repeat=nr):
            for n_off in range(0, 3):
                if nr + n_off == 0:
                    continue
                types.append((tuple(real_mult), n_off))
    for config_type in types:
        nr, n_off = len(config_type[0]), config_type[1]
        dim = nr + 2 * n_off
        for _ in range(starts):
            x0 = rng.normal(scale=0.6, size=dim)
            res = minimize(lambda p: slack(config_type, p, beta, gamma), x0, method="Nelder-Mead", options={"maxiter": 3000, "xatol": 1e-8, "fatol": 1e-10})
            if res.fun < worst[0]:
                worst = (res.fun, config_type, res.x)
    return worst


if __name__ == "__main__":
    for beta, gamma in ((3.0, 4.0), (2.5, 3.5), (2.0 + 1e-9, 3.0)):
        val, ctype, x = search(beta, gamma)
        print(f"beta={beta} gamma={gamma}: min slack {val:.6f} at type {ctype} params {np.round(x, 4)}")
