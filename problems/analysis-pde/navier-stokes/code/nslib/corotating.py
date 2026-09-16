"""The co-rotating-frame Boussinesq solver used to realize the steering control.

Separated from `nslib.steering` so that the control law itself (which carries the
transcribed content) has no torch dependency and can be guarded by repository CI, while
this module, which only runs on a GPU anyway, holds the torch-backed part.

The frame argument is in `nslib.steering`: in two dimensions the construction's common
rotation of the background is equivalent, on the torus, to turning the gravity direction
and holding the prescribed stratification with a low-frequency force.
"""

from __future__ import annotations

from collections.abc import Callable

import torch

from . import boussinesq as B


class CoRotatingBoussinesq(B.Boussinesq2D):
    """Boussinesq in the co-rotating frame: gravity turns, the grid does not.

    `gravity(t)` returns the laboratory gravity direction in co-rotating coordinates.
    `theta_bg_hat`, when given, is exempted from buoyancy, which is the low-frequency
    force that holds the prescribed background steady while gravity tilts. Without it
    the base stratification would itself start rolling as soon as `alpha != 0` and the
    layer would be measured against a background that is not the one the reduction
    assumes.
    """

    def __init__(
        self,
        grid: B.Grid,
        gravity: Callable[[float], tuple[float, float]],
        theta_bg_hat=None,
        nu: float = 0.0,
        alpha: float = 1.0,
    ) -> None:
        super().__init__(grid, nu=nu, alpha=alpha)
        self.gravity = gravity
        self.theta_bg_hat = theta_bg_hat

    def buoyancy(self, theta_hat, t: float):
        g1, g2 = self.gravity(t)
        src = theta_hat if self.theta_bg_hat is None else theta_hat - self.theta_bg_hat
        return 1j * (g2 * self.k1 - g1 * self.k2) * src

    def nonlinear_at(self, theta_hat, omega_hat, t: float):
        u1_hat, u2_hat = self.velocity_hat(omega_hat)
        u1 = torch.fft.ifft2(u1_hat).real
        u2 = torch.fft.ifft2(u2_hat).real
        dtheta = -self._advect_hat(theta_hat, u1, u2)
        domega = -self._advect_hat(omega_hat, u1, u2) + self.buoyancy(theta_hat, t)
        if self.theta_bg_hat is not None and self.nu > 0.0:
            # The same force also pays the background's dissipation bill. Without this
            # the prescribed stratification would decay on its own and the amplitude
            # comparison would be made against a background the reduction never saw.
            dtheta = dtheta + self.diss * self.theta_bg_hat
        return dtheta, domega

    def step_at(self, theta_hat, omega_hat, dt: float, t: float):
        """One integrating-factor RK4 step with time-dependent gravity."""
        E1 = torch.exp(-self.diss * (dt / 2.0))
        E2 = E1 * E1
        a1, b1 = self.nonlinear_at(theta_hat, omega_hat, t)
        a2, b2 = self.nonlinear_at(E1 * (theta_hat + 0.5 * dt * a1),
                                   E1 * (omega_hat + 0.5 * dt * b1), t + dt / 2.0)
        a3, b3 = self.nonlinear_at(E1 * theta_hat + 0.5 * dt * a2,
                                   E1 * omega_hat + 0.5 * dt * b2, t + dt / 2.0)
        a4, b4 = self.nonlinear_at(E2 * theta_hat + dt * E1 * a3,
                                   E2 * omega_hat + dt * E1 * b3, t + dt)
        theta_new = E2 * theta_hat + (dt / 6.0) * (E2 * a1 + 2.0 * E1 * (a2 + a3) + a4)
        omega_new = E2 * omega_hat + (dt / 6.0) * (E2 * b1 + 2.0 * E1 * (b2 + b3) + b4)
        return theta_new * self.mask, omega_new * self.mask


def wave_amplitudes(theta_hat, omega_hat, k, grid, cutoff: float) -> tuple[float, float]:
    """`(Theta, Omega)` of the wave at wavevector `k`, read AT THE ORIGIN.

    The background gradient varies in space, so the amplitude pair is only defined
    locally; demodulation at `k` followed by evaluation at `x = 0` is the local reading,
    and `x = 0` is where the stratification gradient equals `-A e_2` exactly.
    """
    ct = B.demodulate(theta_hat, k, grid, cutoff)[0, 0]
    co = B.demodulate(omega_hat, k, grid, cutoff)[0, 0]
    return (float(-2.0 * ct.imag), float(2.0 * co.real))
