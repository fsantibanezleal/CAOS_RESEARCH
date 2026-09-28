"""RH-034 window control (floating point, exploratory).

Local analysis: for a real triple at 0 and a conjugate pair x0 +- iy near a real zero x0 of K,
Q - 13 = y^2 * 4 pi^2 (8 mu2 - 12 |int u eta^2 e^(-2 pi i x0 u)|^2) + O(y^3), mu2 = int u^2 eta^2.
So the linear candidate Q >= 2N + 3O - 4S fails for small y exactly when the ratio
|int u eta^2 e^(-2 pi i x0 u)|^2 / mu2 exceeds 2/3 at some zero x0. This script evaluates the ratio and
the exact slack for three windows: the Montgomery-Taylor window used by Lamzouri
(eta^2 proportional to cos(sqrt2 u) on (-1/2, 1/2)), a cos^2 window, and an edge-concentrated
window (eta^2 proportional to u^8 on (-1, 1)), the last as a negative control.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

UG, WG = np.polynomial.legendre.leggauss(600)
WINDOWS = {
    "Montgomery-Taylor": (0.5, lambda u: np.cos(np.sqrt(2) * u)),
    "cos^2": (1.0, lambda u: np.cos(np.pi * u / 2) ** 2),
    "edge u^8 (control)": (1.0, lambda u: u**8),
}


def main() -> None:
    for name, (lam, shape) in WINDOWS.items():
        u, w = lam * UG, lam * WG
        e2 = shape(u)
        e2 = e2 / (w @ e2)

        def k(xi, u=u, w=w, e2=e2):
            return (np.exp(-2j * np.pi * np.multiply.outer(np.atleast_1d(xi), u)) * e2) @ w

        mu2 = w @ (u * u * e2)
        xs = np.linspace(0.01, 8, 8000)
        kv = k(xs).real
        zeros = [brentq(lambda t, k=k: k(t).real[0], xs[i], xs[i + 1]) for i in range(len(xs) - 1) if kv[i] * kv[i + 1] < 0][:3]
        print(name)
        for x0 in zeros:
            ratio = abs(w @ (u * e2 * np.exp(-2j * np.pi * x0 * u))) ** 2 / mu2
            best = np.inf
            for y in (5e-2, 2e-2, 1e-2, 5e-3):
                for dx in np.linspace(-0.02, 0.02, 21):
                    pts = np.array([0, x0 + dx + 1j * y, x0 + dx - 1j * y])
                    m = np.array([3.0, 1.0, 1.0])
                    d = pts[:, None] - pts[None, :]
                    kk = k(d.ravel()).reshape(3, 3)
                    best = min(best, float(np.real(np.sum(m[:, None] * m[None, :] * kk * kk))) - 13)
            print(f"  zero {x0:.4f}: ratio {ratio:.4f} (fails if > 2/3), min(Q-13) = {best:+.3e}")


if __name__ == "__main__":
    main()
