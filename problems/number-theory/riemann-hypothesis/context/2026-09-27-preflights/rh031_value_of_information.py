"""RH-031 exploratory value-of-information computation (floating point, uncertified).

Optimizes the Levinson-Conrey density kappa(P,Q,R,nu) = 1 - log(c)/R over P, Q (Chebyshev family of
EXP-010, degree 2K+1) and R, for a given mollifier exponent nu, where

    c = 1 + (1/nu) [C_P a + nu e + nu^2 B_P b],   a = L(Q^2), e = L(Q(RQ+Q')), b = L((RQ+Q')^2),

L(p) = int_0^1 e^(2Rv) p(v) dv, C_P = int P'^2, B_P = int P^2 (D_P = 1/2 folds into e). For fixed Q
the optimal P is sinh(lam x)/sinh(lam), lam = nu sqrt(b/a); for fixed P, c is quadratic in the free
Q coefficients. The two steps alternate. The onset combines kappa with Wang's pair term c(theta)
through the EXP-006 root h_L(theta), exactly as in EXP-010.

Invariant: with Q(x)=1-x, P(x)=x, the Steuding-type range nu=(3theta-1)/4 must reproduce the classical
onset near 0.591, and the best linear Q near 0.552.
"""

from __future__ import annotations

import math

import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import brentq, minimize_scalar

NODES, WEIGHTS = np.polynomial.legendre.leggauss(400)
V = 0.5 * (NODES + 1.0)
W = 0.5 * WEIGHTS


def basis(k_terms: int):
    z = 1.0 - 2.0 * V
    q0 = 1.0 - V
    dq0 = -np.ones_like(V)
    phis, dphis = [], []
    for j in range(1, k_terms + 1):
        n = 2 * j + 1
        coeff = np.zeros(n + 1)
        coeff[n] = 1.0
        t = C.chebval(z, coeff)
        dt = C.chebval(z, C.chebder(coeff)) * (-2.0)
        phis.append(t - z)
        dphis.append(dt + 2.0)
    return q0, dq0, np.array(phis), np.array(dphis)


def p_moments(lam: float) -> tuple[float, float]:
    """C_P, B_P for P = sinh(lam x)/sinh(lam) (P = x when lam -> 0)."""
    if lam < 1e-6:
        return 1.0, 1.0 / 3.0
    x = V
    s = math.sinh(lam)
    p = np.sinh(lam * x) / s
    dp = lam * np.cosh(lam * x) / s
    return float(W @ dp**2), float(W @ p**2)


def c_value(r: float, nu: float, q: np.ndarray, dq: np.ndarray, lam: float | None = None) -> tuple[float, float]:
    e2 = np.exp(2 * r * V)
    u = r * q + dq
    a, e, b = W @ (e2 * q * q), W @ (e2 * q * u), W @ (e2 * u * u)
    if lam is None:
        lam = nu * math.sqrt(max(b, 1e-300) / a)
    cp, bp = p_moments(lam)
    return 1.0 + (cp * a + nu * e + nu * nu * bp * b) / nu, lam


def optimize_q(r: float, nu: float, k_terms: int, iters: int = 8, linear_p: bool = False):
    q0, dq0, phis, dphis = basis(k_terms)
    e2 = np.exp(2 * r * V)
    lam = 0.0 if linear_p else nu
    x = np.zeros(k_terms)
    for _ in range(iters):
        cp, bp = p_moments(lam)
        # c - 1 = (cp/nu) L(Q^2) + L(Q(RQ+Q')) + nu bp L((RQ+Q')^2), quadratic in x.
        qs = np.vstack([q0, phis])
        us = r * qs + np.vstack([dq0, dphis])
        m = (cp / nu) * (qs * e2) @ (qs * W).T
        m += 0.5 * ((qs * e2) @ (us * W).T + (us * e2) @ (qs * W).T)
        m += nu * bp * (us * e2) @ (us * W).T
        m = 0.5 * (m + m.T)
        if k_terms == 0:
            break
        a_ff, a_f0 = m[1:, 1:], m[1:, 0]
        x = np.linalg.solve(a_ff + 1e-14 * np.eye(k_terms), -a_f0)
        if linear_p:
            break
        q = q0 + x @ phis
        dq = dq0 + x @ dphis
        _, lam = c_value(r, nu, q, dq)
    q = q0 + (x @ phis if k_terms else 0)
    dq = dq0 + (x @ dphis if k_terms else 0)
    c, lam = c_value(r, nu, q, dq, lam=0.0 if linear_p else None)
    return c, lam, x


def kappa_opt(nu: float, k_terms: int, linear_p: bool = False, q_fixed: str | None = None) -> tuple[float, float]:
    def neg(r: float) -> float:
        if q_fixed == "1-x":
            q = 1.0 - V
            dq = -np.ones_like(V)
            c, _ = c_value(r, nu, q, dq, lam=0.0 if linear_p else None)
        else:
            c, _, _ = optimize_q(r, nu, k_terms, linear_p=linear_p)
        return -(1.0 - math.log(c) / r)

    res = minimize_scalar(neg, bounds=(0.05, 60.0), method="bounded", options={"xatol": 1e-7})
    return -res.fun, res.x


def wang_c(theta: float) -> float:
    return 2 - theta / 2 - (1 / math.tan(theta / math.sqrt(2))) / math.sqrt(2)


def h_l(k: float, c: float) -> float:
    disc = (1 - k) * (9 - k - 8 * c)
    return (3 + k - math.sqrt(disc)) / 4


def main() -> None:
    print("Invariant: Steuding-type range, degree-one Q")
    for label, lin in (("Q=1-x, P=x", True), ("Q=1-x, optimal P", False)):
        f = lambda th: kappa_opt((3 * th - 1) / 4, 0, linear_p=lin, q_fixed="1-x")[0]
        print(f"  {label}: onset theta = {brentq(f, 0.52, 0.70, xtol=1e-7):.5f}")
    # best linear Q is Q=1-x within the admissible class (Q(0)=1, Q(y)+Q(1-y)=1 forces 1-y).
    print("kappa*(nu) with the Chebyshev family")
    grid = [0.01, 0.02, 0.034, 0.05, 0.068, 0.10, 0.125, 0.15, 0.1875, 0.25, 0.3, 0.375]
    kap = {}
    for nu in grid:
        kt = max(8, int(math.ceil(3.0 / nu)))
        kt = min(kt, 150)
        k, r = kappa_opt(nu, kt)
        kap[nu] = k
        print(f"  nu={nu:6.4f} K={kt:3d} kappa={k:.6f} kappa/nu={k / nu:.5f} R={r:.3f}")

    def kappa_at(nu: float) -> float:
        kt = min(150, max(8, int(math.ceil(3.0 / nu))))
        return kappa_opt(nu, kt)[0]

    ranges = {
        "Young (EXP-010)": lambda th: th - 0.5,
        "Tang-type 2theta-1": lambda th: 2 * th - 1,
        "Steuding-type": lambda th: min((3 * th - 1) / 4, 3 / 8),
    }
    print("Onset of h_L > 0 and sample values")
    for name, rng in ranges.items():
        g = lambda th: kappa_at(rng(th)) - (1 - 2 / (2 - wang_c(th)))
        lo = 0.5005
        onset = None
        if g(lo) > 0:
            onset = f"< {lo} (positive for every theta > 1/2 tested)"
        else:
            onset = f"{brentq(g, lo, 0.56, xtol=1e-6):.5f}"
        print(f"  {name}: onset {onset}")
        for th in (0.505, 0.51, 0.52, 0.534, 0.55, 0.6):
            k = kappa_at(rng(th))
            print(f"     theta={th}: nu={rng(th):.4f} kappa={k:.5f} h_L={h_l(k, wang_c(th)):.6f}")


if __name__ == "__main__":
    main()
