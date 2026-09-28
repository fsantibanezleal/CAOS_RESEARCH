"""RH-034 follow-up: periodic lattices of real triples and near-real conjugate pairs (exploratory).

Triples at n*s (|n| <= M), p conjugate pairs per period at n*s + o_j*s +- i y_j. Minimizes the
per-triple excess (Q - 2N)/O for the Montgomery-Taylor window; values near 2 would mean that no
linear refinement Q >= 2N + beta O (S = 0) with beta > 2 exists, i.e. the EXP-006 product is
asymptotically sharp near the onset.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.optimize import minimize

from rh034_beta_search import kernel


def per_triple(params: np.ndarray, m_half: int, p: int) -> float:
    s = abs(params[0]) + 0.2
    ys = np.abs(params[1 : 1 + p]) + 1e-6
    offs = params[1 + p : 1 + 2 * p]
    n = np.arange(-m_half, m_half + 1)
    pts = list((n * s).astype(complex))
    m = [3.0] * len(n)
    for y, o in zip(ys, offs):
        pts += list(n * s + o * s + 1j * y) + list(n * s + o * s - 1j * y)
        m += [1.0] * (2 * len(n))
    pts = np.array(pts)
    m = np.array(m)
    kk = kernel(pts[:, None] - pts[None, :])
    q = np.real(np.sum(m[:, None] * m[None, :] * kk * kk))
    return float((q - 2 * m.sum()) / len(n))


def main(p_max: int = 6) -> None:
    for p in range(1, p_max + 1):
        best = None
        for s0 in (p * 1.0, p * 1.5 + 0.5):
            for y0 in (0.2, 0.35):
                x0 = np.r_[s0 - 0.2, [y0] * p, (np.arange(p) + 0.5) / p]
                r = minimize(per_triple, x0, args=(12, p), method="Nelder-Mead", options={"maxiter": 4000 * p, "xatol": 1e-7, "fatol": 1e-9})
                if best is None or r.fun < best.fun:
                    best = r
        check = per_triple(best.x, 30, p)
        print(f"pairs per triple={p}: (Q-2N)/O={best.fun:.5f} (M=30 check {check:.5f}) s={abs(best.x[0]) + 0.2:.4f} y={np.round(np.abs(best.x[1 : 1 + p]), 3)}", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
