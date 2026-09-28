"""RH-034 follow-up: infinite periodic lattices of real triples and near-real pairs (exploratory).

Per-cell excess (Q - 2N)/O for a lattice of period s with one triple and p conjugate pairs per cell,
using lattice sums over |n| <= 600 (K decays like 1/|x| for the truncated Montgomery-Taylor window, so
K^2 is summable). This is the thermodynamic limit of rh034_lattice.py without boundary effects.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.optimize import minimize

from rh034_beta_search import kernel

NS = np.arange(-600, 601)


def per_cell(params: np.ndarray, p: int) -> float:
    s = abs(params[0]) + 0.2
    ys = np.abs(params[1 : 1 + p]) + 1e-6
    offs = params[1 + p : 1 + 2 * p]
    cell = np.array([0j] + [o * s + 1j * y for y, o in zip(ys, offs)] + [o * s - 1j * y for y, o in zip(ys, offs)])
    m = np.array([3.0] + [1.0] * (2 * p))
    diff = cell[:, None] - cell[None, :]
    kk = kernel(diff[:, :, None] + NS[None, None, :] * s)
    q = np.real(np.sum(m[:, None, None] * m[None, :, None] * kk * kk))
    return float(q - 2 * m.sum())


def main(p_max: int = 3) -> None:
    for p in range(1, p_max + 1):
        best = None
        for s0 in (p + 1.0, p + 1.5):
            for y0 in (0.27, 0.3):
                x0 = np.r_[s0 - 0.2, [y0] * p, (np.arange(p) + 0.5) / p]
                r = minimize(per_cell, x0, args=(p,), method="Nelder-Mead", options={"maxiter": 3000 * p, "xatol": 1e-8, "fatol": 1e-10})
                if best is None or r.fun < best.fun:
                    best = r
        print(f"p={p}: (Q-2N)/O={best.fun:.5f} s={abs(best.x[0]) + 0.2:.5f} y={np.round(np.abs(best.x[1 : 1 + p]), 5)} offsets={np.round(best.x[1 + p :], 5)}", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
