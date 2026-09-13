"""GPU pseudo-spectral solver for the 2D Boussinesq system, with fractional dissipation.

Solves on the periodic box [0, 2 pi)^2

    d_t theta + u . grad theta = -nu (-Laplacian)^alpha theta
    d_t omega + u . grad omega = d_1 theta - nu (-Laplacian)^alpha omega
    u = grad^perp psi,   Laplacian psi = omega

with grad^perp = J grad and J(x1, x2) = (-x2, x1), so that
omega = d_1 u_2 - d_2 u_1 is consistent with Laplacian psi = omega.

Conventions match `modulation.py`: dissipation is (-Laplacian)^alpha, which is
|k|^(2 alpha) in Fourier, so classical viscosity is alpha = 1.

Time stepping is integrating-factor RK4: the linear dissipative part is solved
exactly in Fourier space and RK4 is applied to the nonlinearity only, so the scheme
stays stable when nu |k|^(2 alpha) is large at the grid scale. Dealiasing is the
2/3 rule.

This module exists to be the positive control for the reduced modulation model of
EXP-002: a reduced model that is never checked against the equation it reduces is a
picture, not an instrument.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class Grid:
    """Spectral grid on [0, 2 pi)^2 with N points per side."""

    N: int
    device: torch.device
    dtype: torch.dtype = torch.float64

    @property
    def cdtype(self) -> torch.dtype:
        return torch.complex128 if self.dtype == torch.float64 else torch.complex64

    def coords(self) -> tuple[torch.Tensor, torch.Tensor]:
        n = torch.arange(self.N, device=self.device, dtype=self.dtype)
        x = 2.0 * torch.pi * n / self.N
        return torch.meshgrid(x, x, indexing="ij")

    def wavenumbers(self) -> tuple[torch.Tensor, torch.Tensor]:
        """Integer wavenumbers (k1, k2) laid out for `torch.fft.fft2`."""
        k = torch.fft.fftfreq(self.N, d=1.0 / self.N).to(self.device, self.dtype)
        return torch.meshgrid(k, k, indexing="ij")

    def dealias_mask(self) -> torch.Tensor:
        """2/3-rule mask."""
        k1, k2 = self.wavenumbers()
        kmax = self.N / 3.0
        return (k1.abs() <= kmax) & (k2.abs() <= kmax)


class Boussinesq2D:
    """State holder and stepper for the 2D Boussinesq system."""

    def __init__(self, grid: Grid, nu: float = 0.0, alpha: float = 1.0) -> None:
        self.g = grid
        self.nu = float(nu)
        self.alpha = float(alpha)
        k1, k2 = grid.wavenumbers()
        self.k1, self.k2 = k1, k2
        self.k2sum = k1 * k1 + k2 * k2
        # Inverse Laplacian with the mean mode annihilated.
        inv = torch.zeros_like(self.k2sum)
        nz = self.k2sum > 0
        inv[nz] = -1.0 / self.k2sum[nz]
        self.inv_lap = inv                      # psi_hat = inv_lap * omega_hat
        self.mask = grid.dealias_mask()
        # Dissipation symbol for (-Laplacian)^alpha.
        self.diss = self.nu * self.k2sum.clamp(min=0.0) ** self.alpha

    # ---------------------------------------------------------------- helpers

    def velocity_hat(self, omega_hat: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Biot-Savart: u = grad^perp psi with Laplacian psi = omega."""
        psi_hat = self.inv_lap * omega_hat
        u1_hat = -1j * self.k2 * psi_hat
        u2_hat = 1j * self.k1 * psi_hat
        return u1_hat, u2_hat

    def _advect_hat(self, f_hat: torch.Tensor, u1: torch.Tensor, u2: torch.Tensor) -> torch.Tensor:
        """Spectral u . grad f, dealiased."""
        f1 = torch.fft.ifft2(1j * self.k1 * f_hat).real
        f2 = torch.fft.ifft2(1j * self.k2 * f_hat).real
        return torch.fft.fft2(u1 * f1 + u2 * f2) * self.mask

    def nonlinear(
        self, theta_hat: torch.Tensor, omega_hat: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Everything except the dissipative linear part."""
        u1_hat, u2_hat = self.velocity_hat(omega_hat)
        u1 = torch.fft.ifft2(u1_hat).real
        u2 = torch.fft.ifft2(u2_hat).real
        dtheta = -self._advect_hat(theta_hat, u1, u2)
        domega = -self._advect_hat(omega_hat, u1, u2) + 1j * self.k1 * theta_hat
        return dtheta, domega

    # ------------------------------------------------------------- time step

    def step(
        self, theta_hat: torch.Tensor, omega_hat: torch.Tensor, dt: float
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """One integrating-factor RK4 step.

        Writes y' = L y + N(y) with L = -diss, substitutes w = exp(-L t) y and takes
        RK4 on w, which is equivalent to the standard IFRK4 combination below.
        """
        E1 = torch.exp(-self.diss * (dt / 2.0))
        E2 = E1 * E1

        a1, b1 = self.nonlinear(theta_hat, omega_hat)
        a2, b2 = self.nonlinear(E1 * (theta_hat + 0.5 * dt * a1),
                                E1 * (omega_hat + 0.5 * dt * b1))
        a3, b3 = self.nonlinear(E1 * theta_hat + 0.5 * dt * a2,
                                E1 * omega_hat + 0.5 * dt * b2)
        a4, b4 = self.nonlinear(E2 * theta_hat + dt * E1 * a3,
                                E2 * omega_hat + dt * E1 * b3)

        theta_new = E2 * theta_hat + (dt / 6.0) * (E2 * a1 + 2.0 * E1 * (a2 + a3) + a4)
        omega_new = E2 * omega_hat + (dt / 6.0) * (E2 * b1 + 2.0 * E1 * (b2 + b3) + b4)
        return theta_new * self.mask, omega_new * self.mask

    # ------------------------------------------------------------ diagnostics

    def energy(self, omega_hat: torch.Tensor) -> float:
        u1_hat, u2_hat = self.velocity_hat(omega_hat)
        e = (u1_hat.abs() ** 2 + u2_hat.abs() ** 2).sum() / (self.g.N ** 2)
        return float(e.real if torch.is_complex(e) else e)

    def max_abs(self, f_hat: torch.Tensor) -> float:
        return float(torch.fft.ifft2(f_hat).real.abs().max())


# ------------------------------------------------------------------ field setup


def mode_amplitude(f_hat: torch.Tensor, k: tuple[int, int], N: int, kind: str) -> float:
    """Signed amplitude of a single Fourier mode of a real field.

    For f = Theta sin(k . x) the coefficient at +k is -i Theta / 2, so
    Theta = -2 Im(f_hat_k). For f = Omega cos(k . x) it is Omega / 2, so
    Omega = 2 Re(f_hat_k). `f_hat` is the unnormalized `torch.fft.fft2` output.
    """
    c = f_hat[k[0] % N, k[1] % N] / (N * N)
    if kind == "sin":
        return float(-2.0 * c.imag)
    if kind == "cos":
        return float(2.0 * c.real)
    raise ValueError("kind must be 'sin' or 'cos'")


def demodulate(f_hat: torch.Tensor, k: tuple[int, int], grid: Grid, cutoff: float) -> torch.Tensor:
    """Complex envelope of the component of `f` carried near wavevector `k`.

    Shifts the spectrum so that `k` lands at the origin and low-passes with radius
    `cutoff`. The magnitude of the result is the slowly varying local amplitude,
    which is what makes a LOCAL growth rate measurable on a background whose
    gradient varies in space.
    """
    k1, k2 = grid.wavenumbers()
    shifted = torch.roll(f_hat, shifts=(-k[0], -k[1]), dims=(0, 1))
    low = (k1 * k1 + k2 * k2) <= cutoff * cutoff
    return torch.fft.ifft2(shifted * low)


def layered_initial_data(
    grid: Grid,
    A0: float,
    lam0: int,
    lam: int,
    phi: float,
    Theta0: float,
    Omega0: float,
) -> tuple[torch.Tensor, torch.Tensor]:
    """The Alpoge-Buckmaster stratification plus one wave, as Fourier coefficients.

    theta = -(A0 / lam0) sin(lam0 x2) + Theta0 sin(lam zeta . x)
    omega =                             Omega0 cos(lam zeta . x)

    The first term is the smooth Rayleigh-Taylor-unstable stratification of their
    equation (1.4) with the cutoff dropped, which is legitimate on the torus. It has
    d_2 theta(x) = -A0 cos(lam0 x2), so the LOCAL background gradient magnitude is
    A0 |cos(lam0 x2)|: one run gives a whole curve of growth-rate predictions
    indexed by height, not a single number.

    `zeta = (sin phi, cos phi)` is rounded to the nearest integer wavevector so the
    wave is an exact mode of the grid; the realized angle is returned by
    `realized_zeta`.
    """
    import math

    x1, x2 = grid.coords()
    k1w, k2w = realized_wavevector(lam, phi)
    theta = -(A0 / lam0) * torch.sin(lam0 * x2) + Theta0 * torch.sin(k1w * x1 + k2w * x2)
    omega = Omega0 * torch.cos(k1w * x1 + k2w * x2)
    _ = math  # keep the import meaningful for readers of the docstring
    return torch.fft.fft2(theta), torch.fft.fft2(omega)


def realized_wavevector(lam: int, phi: float) -> tuple[int, int]:
    """Nearest integer wavevector to lam * (sin phi, cos phi)."""
    import math

    return (int(round(lam * math.sin(phi))), int(round(lam * math.cos(phi))))


def realized_zeta(lam: int, phi: float) -> tuple[float, float, float]:
    """Return (zeta1, zeta2, |k|) for the integer wavevector actually used.

    The modulation prediction must be evaluated at the wavevector the grid can
    represent, not at the requested one, or the comparison silently tests the wrong
    angle.
    """
    import math

    k1w, k2w = realized_wavevector(lam, phi)
    norm = math.hypot(k1w, k2w)
    return (k1w / norm, k2w / norm, norm)
