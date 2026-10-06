"""RH-028 exploratory main-term check for a two-piece mollifier (floating point, uncertified).

Evaluates the Bui-Conrey-Young (arXiv:1002.4127v1, Theorems 3-5) main term
c = c1 + 2 c12 + c2 for psi = psi1 + psi2, with psi2 the chi(s)-type second piece built from the
coefficients of 1/zeta^2 and P2 vanishing to third order. Mixed derivatives at x=y=0 are taken by
central finite differences; integrals by tensor Gauss-Legendre quadrature.

Invariant: the published parameters (theta1=4/7, theta2=1/2, R=1.28) must give kappa >= 0.4105.
Then, at short-window lengths theta1 = nu, theta2 = nu - 1e-9, the optimal P2 (c is quadratic in the
coefficients of P2) is added to the RH-031 one-piece optimum, and the relative gain in kappa is
reported. This is main-term arithmetic only; it assumes nothing about localizing psi2.
"""

from __future__ import annotations

import math

import numpy as np
from numpy.polynomial import polynomial as Pn


def ev(poly, x):
    """Evaluate a coefficient array (numpy polynomial order) or a callable."""
    return poly(x) if callable(poly) else Pn.polyval(x, poly)


def gl(n: int, a: float = 0.0, b: float = 1.0):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * w


def c1(p1, q, r, th1, n=200):
    u, wu = gl(n)
    v, wv = gl(n)
    hstep = 1e-6
    qv = ev(q, v)
    dqv = (ev(q, v + hstep) - ev(q, v - hstep)) / (2 * hstep)
    pu = ev(p1, u)
    dpu = (ev(p1, u + hstep) - ev(p1, u - hstep)) / (2 * hstep)
    integrand = np.exp(2 * r * v)[None, :] * (
        qv[None, :] * dpu[:, None] + th1 * dqv[None, :] * pu[:, None] + th1 * r * qv[None, :] * pu[:, None]
    ) ** 2
    return 1.0 + (wu @ integrand @ wv) / th1


def c12_linear(p1, q, r, th1, th2, p2_basis, h=1e-3, n=40):
    """Return vector g_j with c12 = sum_j b_j g_j for P2 = sum_j b_j x^j (j in p2_basis)."""
    a1, wa = gl(n)
    s1, ws = gl(n)
    u, wu = gl(n)
    # simplex a+b<=1 via a = s*(1-t)... use a in [0,1], b in [0, 1-a]
    A = a1[:, None, None]
    B = (1 - a1)[:, None, None] * s1[None, :, None]
    jac = (1 - a1)[:, None, None]
    U = u[None, None, :]
    wts = wa[:, None, None] * ws[None, :, None] * wu[None, None, :] * jac

    def inner(x, y, j):
        d2 = j * (j - 1) * ((1 - A - B) * U) ** (j - 2)
        arg = x + y + 1 - (1 - U) * th2 / th1
        val = (
            U**2
            * (1 - U)
            * np.exp(r * (th1 * (y - x) + U * th2 * (A - B)))
            * ev(q, -x * th1 + A * U * th2)
            * ev(q, 1 + y * th1 - B * U * th2)
            * ev(p1, arg)
            * d2
        )
        return float(np.sum(val * wts))

    out = []
    for j in p2_basis:
        mixed = (inner(h, h, j) - inner(h, -h, j) - inner(-h, h, j) + inner(-h, -h, j)) / (4 * h * h)
        out.append(4 * (th2 / th1) ** 2 * math.exp(r) * mixed)
    return np.array(out)


def c2_quadratic(q, r, th2, p2_basis, h=2e-2, n=18, n_t=None):
    """Return matrix M with c2 = b^T M b."""
    t, wt = gl(n_t or n)
    rr, wr = gl(n)
    u, wu = gl(n)
    v, wv = gl(n)
    T, R_, U, Vv = np.meshgrid(t, rr, u, v, indexing="ij")
    W = wt[:, None, None, None] * wr[None, :, None, None] * wu[None, None, :, None] * wv[None, None, None, :]

    def inner(x, y, j, k):
        s = x + y - Vv * (y + R_) - U * (x + R_)
        tt = T * (1 + th2 * s)
        base = (
            (1 - R_) ** 4
            * (1 / th2 + s)
            * np.exp(-th2 * r * s)
            * ev(q, th2 * (-y + U * (x + R_)) + tt)
            * np.exp(2 * r * tt)
            * ev(q, th2 * (-x + Vv * (y + R_)) + tt)
            * (x + R_)
            * (y + R_)
        )
        f1 = j * (j - 1) * ((1 - U) * (x + R_)) ** (j - 2)
        f2 = k * (k - 1) * ((1 - Vv) * (y + R_)) ** (k - 2)
        return float(np.sum(base * f1 * f2 * W))

    # d^4/dx^2 dy^2 by the tensor product of 3-point second differences
    stencil = [(-h, 1.0), (0.0, -2.0), (h, 1.0)]
    m = np.zeros((len(p2_basis), len(p2_basis)))
    for a, j in enumerate(p2_basis):
        for b, k in enumerate(p2_basis):
            if b < a:
                continue
            acc = 0.0
            for dx, cx in stencil:
                for dy, cy in stencil:
                    acc += cx * cy * inner(dx, dy, j, k)
            m[a, b] = m[b, a] = (2.0 / 3.0) * acc / h**4
    return m


def kappa(c, r):
    return 1 - math.log(c) / r


def anchor() -> float:
    z = np.array([1.0, -2.0])
    q = Pn.polyadd(np.array([0.492]), 0.604 * z)
    for coef, power in ((-0.08, 3), (-0.06, 5), (0.046, 7)):
        q = Pn.polyadd(q, coef * Pn.polypow(z, power))
    p1 = np.array([0, 0.842706, 0.00845721, 0.093117, 0.118788, -0.0630687])
    basis = [3, 4, 5]
    b = np.array([0.0245412, -0.00635566, 0.00603128])
    r, th1, th2 = 1.28, 4 / 7, 1 / 2
    cc1 = c1(p1, q, r, th1)
    g = c12_linear(p1, q, r, th1, th2, basis)
    m = c2_quadratic(q, r, th2, basis)
    c = cc1 + 2 * g @ b + b @ m @ b
    print(f"anchor: c1={cc1:.6f} kappa1={kappa(cc1, r):.5f} c={c:.6f} kappa={kappa(c, r):.5f} (published >= 0.4105)")
    b_opt = -np.linalg.solve(m, g)
    c_opt = cc1 - g @ np.linalg.solve(m, g)
    print(f"        optimal P2 for these P1,Q,R: kappa={kappa(c_opt, r):.5f} b={np.round(b_opt, 6)}")
    return kappa(c, r)


def short_window(nu: float, basis=(3, 4, 5, 6, 7), n_t: int = 100) -> dict[str, float]:
    import rh031_value_of_information as v

    k_terms = min(150, max(8, int(math.ceil(3.0 / nu))))
    kap, r = v.kappa_opt(nu, k_terms)
    c_one, lam, x = v.optimize_q(r, nu, k_terms)
    coeffs = [0.0] * (2 * k_terms + 2)

    def q_fn(y):
        z = 1.0 - 2.0 * np.asarray(y)
        out = 1.0 - np.asarray(y)
        for j, xj in enumerate(x, start=1):
            c = np.zeros(2 * j + 2)
            c[2 * j + 1] = 1.0
            out = out + xj * (np.polynomial.chebyshev.chebval(z, c) - z)
        return out

    def p_fn(u):
        u = np.asarray(u)
        return np.sinh(lam * u) / math.sinh(lam) if lam > 1e-6 else u

    del coeffs
    th1, th2 = nu, nu - 1e-9
    cc1 = c1(p_fn, q_fn, r, th1)
    g = c12_linear(p_fn, q_fn, r, th1, th2, list(basis))
    m = c2_quadratic(q_fn, r, th2, list(basis), n=16, n_t=n_t)
    gain = g @ np.linalg.solve(m, g)
    k1 = kappa(cc1, r)
    k_bcy = kappa(cc1 - gain, r)
    k_x2 = kappa(cc1 - 2 * gain, r)
    return {"nu": nu, "R": r, "kappa_one_piece": k1, "kappa_rh031": kap, "kappa_two_piece": k_bcy, "kappa_two_piece_x2": k_x2}


if __name__ == "__main__":
    anchor()
    for nu in (0.15, 0.068):
        res = short_window(nu)
        rel = (res["kappa_two_piece"] / res["kappa_one_piece"] - 1) * 100
        rel2 = (res["kappa_two_piece_x2"] / res["kappa_one_piece"] - 1) * 100
        print(
            f"nu={nu}: R={res['R']:.3f} kappa1={res['kappa_one_piece']:.6f} (RH-031 {res['kappa_rh031']:.6f}) "
            f"two-piece={res['kappa_two_piece']:.6f} ({rel:+.3f}%), with published normalization "
            f"{res['kappa_two_piece_x2']:.6f} ({rel2:+.3f}%)"
        )
