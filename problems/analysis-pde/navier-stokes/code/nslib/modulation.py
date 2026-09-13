"""The Alpoge-Buckmaster amplitude (modulation) system, and its dissipative extension.

Reference for the inviscid system: L. Alpoge and T. Buckmaster, "Blowup for the
Boussinesq equations with smooth forcing", 2026-09-07, Subsection 1.2 and Lemma 3.1.
The construction and its intellectual credit belong to Diego Cordoba and Luis
Martinez-Zoroa; nothing in this module is our mechanism.

The dissipative extension is derived in
`../../context/2026-09-11-simplified-model-and-beyond.md` Subsection 2.1 and is
checked against a direct PDE simulation by EXP-002.

Setting. The 2D inviscid Boussinesq system on R^2,

    d_t theta + u . grad theta = f_theta
    d_t u     + u . grad u + grad p = theta e_2 + f_u,   div u = 0

with vorticity form  d_t omega + u . grad omega = d_1 theta + curl f_u.

Take a background that is affine near the origin,

    u_old(x, t) = D(t) x   (trace-free),      theta_old(x, t) = G(t) . x

and add a temperature wave and a vorticity wave sharing one phase,

    s = lambda zeta(t) . x,   vartheta = Theta(t) F(s),   varpi = Omega(t) F'(s)

with streamfunction psi = Omega P(s) / (lambda^2 |zeta|^2), P' = F. The wave velocity
v = grad^perp psi is perpendicular to zeta while both wave gradients are parallel to
zeta, so the wave does not advect itself and the ansatz is EXACT (no nonlinear
correction) wherever the envelope is one and F(s) = s.

Matching coefficients gives the closed system implemented here:

    zeta_dot  = -D^T zeta
    Theta_dot = -(J zeta . G) / (lambda |zeta|^2) * Omega
    Omega_dot = lambda * zeta_1 * Theta

with J(x1, x2) = (-x2, x1).

Adding dissipation of order alpha to both equations, that is -nu (-Laplacian)^alpha,
is diagonal on the phase because (-Laplacian)^alpha F(lambda zeta . x) picks up
(lambda |zeta|)^(2 alpha). The geometric cancellations are untouched, so the only
change is one damping term per amplitude. NOTE the convention: this module uses
(-Laplacian)^alpha, so classical viscosity is alpha = 1. Cordoba, Martinez-Zoroa and
Zheng write |grad|^alpha = (-Laplacian)^(alpha/2), so their alpha is twice ours; see
`alpha_cmz_to_ours`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# Cordoba, Martinez-Zoroa, Zheng, ARMA 250 (2026) article 38, Theorem 1:
# blowup for the forced fractional Navier-Stokes equations for every |grad|^alpha
# exponent below this value.
ALPHA0_CMZ = (22.0 - 8.0 * math.sqrt(7.0)) / 9.0


def alpha_cmz_to_ours(alpha_cmz: float) -> float:
    """Convert a |grad|^alpha exponent to the (-Laplacian)^alpha convention."""
    return alpha_cmz / 2.0


def alpha_ours_to_cmz(alpha_ours: float) -> float:
    """Convert a (-Laplacian)^alpha exponent to the |grad|^alpha convention."""
    return 2.0 * alpha_ours


ALPHA0_OURS = alpha_cmz_to_ours(ALPHA0_CMZ)


def rot(phi: float) -> np.ndarray:
    """The direction e(phi) = (sin phi, cos phi) used throughout the source paper.

    phi measures the angle from the positive x2 direction toward positive x1.
    """
    return np.array([math.sin(phi), math.cos(phi)])


def J(v: np.ndarray) -> np.ndarray:
    """The rotation J(x1, x2) = (-x2, x1)."""
    return np.array([-v[1], v[0]])


@dataclass(frozen=True)
class Background:
    """The affine background seen by a layer: u_old = D x, theta_old = G . x."""

    D: np.ndarray  # 2x2, trace free
    G: np.ndarray  # 2-vector

    def __post_init__(self) -> None:
        if abs(float(np.trace(self.D))) > 1e-12:
            raise ValueError("the background velocity gradient D must be trace free")


def amplitude_matrix(
    zeta: np.ndarray,
    G: np.ndarray,
    lam: float,
    nu: float = 0.0,
    alpha: float = 1.0,
) -> np.ndarray:
    """Return the 2x2 generator of (Theta, Omega) at a frozen (zeta, G).

    The inviscid entries are exactly the coefficients of the source system; the
    diagonal carries the dissipative damping -nu (lambda |zeta|)^(2 alpha).
    """
    z2 = float(zeta @ zeta)
    damping = nu * (lam * math.sqrt(z2)) ** (2.0 * alpha)
    c_theta = -float(J(zeta) @ G) / (lam * z2)  # multiplies Omega
    c_omega = lam * float(zeta[0])              # multiplies Theta
    return np.array([[-damping, c_theta], [c_omega, -damping]])


def growth_rate(
    zeta: np.ndarray,
    G: np.ndarray,
    lam: float,
    nu: float = 0.0,
    alpha: float = 1.0,
) -> float:
    """Top eigenvalue of the amplitude generator, that is the exponential rate."""
    return float(np.max(np.real(np.linalg.eigvals(amplitude_matrix(zeta, G, lam, nu, alpha)))))


def frozen_growth_rate(
    A: float, phi: float, lam: float, r: float = 1.0, nu: float = 0.0, alpha: float = 1.0
) -> float:
    """Closed form for the frozen configuration D = 0, G = -A e_2, zeta = r e(phi).

    The inviscid rate is sqrt(A) * sin(phi), INDEPENDENT of the frequency lambda:
    the lambda in the Omega equation cancels the 1/lambda in the Theta equation.
    Frequency buys gradient, not growth. Dissipation then charges for frequency at
    order 2 alpha, which is the whole obstruction to pushing this cascade viscous.
    """
    return math.sqrt(A) * math.sin(phi) - nu * (lam * r) ** (2.0 * alpha)


def frequency_cap(A: float, phi: float, nu: float, alpha: float, r: float = 1.0) -> float:
    """Largest lambda whose wave still grows on a background of gradient A.

    Solves sqrt(A) sin(phi) = nu (lambda r)^(2 alpha). Returns +inf when nu = 0.
    """
    if nu <= 0.0:
        return math.inf
    rhs = math.sqrt(A) * math.sin(phi) / nu
    if rhs <= 0.0:
        return 0.0
    return rhs ** (1.0 / (2.0 * alpha)) / r


def rhs(
    state: np.ndarray,
    bg: Background,
    lam: float,
    nu: float = 0.0,
    alpha: float = 1.0,
) -> np.ndarray:
    """Right-hand side of the full system for state = (zeta_1, zeta_2, Theta, Omega)."""
    zeta = state[:2]
    Theta, Omega = float(state[2]), float(state[3])
    dzeta = -bg.D.T @ zeta
    M = amplitude_matrix(zeta, bg.G, lam, nu, alpha)
    dTheta, dOmega = M @ np.array([Theta, Omega])
    return np.concatenate([dzeta, [dTheta, dOmega]])


def integrate(
    state0: np.ndarray,
    bg: Background,
    lam: float,
    t_end: float,
    nu: float = 0.0,
    alpha: float = 1.0,
    steps: int = 4000,
) -> np.ndarray:
    """Classical RK4 on the full system. Returns the final state."""
    y = np.asarray(state0, dtype=float).copy()
    h = t_end / steps
    for _ in range(steps):
        k1 = rhs(y, bg, lam, nu, alpha)
        k2 = rhs(y + 0.5 * h * k1, bg, lam, nu, alpha)
        k3 = rhs(y + 0.5 * h * k2, bg, lam, nu, alpha)
        k4 = rhs(y + h * k3, bg, lam, nu, alpha)
        y = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return y


def growing_eigenvector(
    zeta: np.ndarray, G: np.ndarray, lam: float, nu: float = 0.0, alpha: float = 1.0
) -> np.ndarray:
    """Unit (Theta, Omega) on the growing eigenline.

    For the frozen case the source paper prints the eigenline Omega = (lambda r /
    sqrt(A)) Theta, which is what this returns up to normalization and is the check
    that settles the mangled-radical ambiguity in the PDF.
    """
    M = amplitude_matrix(zeta, G, lam, nu, alpha)
    vals, vecs = np.linalg.eig(M)
    v = np.real(vecs[:, int(np.argmax(np.real(vals)))])
    n = float(np.linalg.norm(v))
    return v / n if n > 0 else v


def gradient_at_origin(Theta: float, zeta: np.ndarray, lam: float) -> np.ndarray:
    """grad vartheta(0, t) = lambda Theta zeta.

    This identity is why the program works: a short wave carries a SMALL amplitude
    and a LARGE gradient, so each layer can hand the next one a bigger background
    gradient while the temperature itself stays bounded.
    """
    return lam * Theta * np.asarray(zeta, dtype=float)
