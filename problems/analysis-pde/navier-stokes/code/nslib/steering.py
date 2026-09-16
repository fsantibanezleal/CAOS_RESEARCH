"""The first-stage steering control, and its realization in the co-rotating frame.

Transcribed from L. Alpoge and T. Buckmaster, "Blowup for the Boussinesq equations
with smooth forcing" (2026-09-07), Subsections 3.2, 3.3 and 3.6.2. The control, like
the whole layer mechanism, belongs to that program and to Cordoba and Martinez-Zoroa
before it; nothing here is our construction. What is ours is the numerical realization
and the tests.

WHY THE CYCLE NEEDS STEERING. A grown layer leaves behind not only the temperature
gradient the next layer needs (`grad vartheta(0) = lambda Theta zeta`) but also a shear
`Dv(0) = Omega J e(phi) tensor e(phi)`, and that shear would keep deforming the next
layer instead of letting it grow on a frozen background. The construction removes it:
after growth it applies a COMMON rotation to the background gradient `G` and the phase
direction `zeta`. A common rotation preserves `J zeta . G` and `|zeta|`, so the
coefficient in `Theta_dot` is untouched, but it moves the LABORATORY component `zeta_1`
that multiplies `Theta` in `Omega_dot`. Taking `zeta_1` briefly negative drives the
(negative) vorticity amplitude back to zero while the temperature amplitude keeps
growing. When `Omega = 0` and `zeta_1 = 0` both derivatives vanish: the layer is frozen
and the next one can grow on the gradient it deposited.

THE NORMALIZED MODEL (their (3.25)). With `tau = Gamma (t - t_1)`, a trial pulse
amplitude `mu`, a smooth step `eta` and a unit-mass profile `h` supported in (0, 1),

    P_tautau = z(tau) P,     P(0) = P_tau(0) = 1,      tau_b = 1 + 1/Lambda
    z(tau) = 1 - eta(tau)                      on [0, 1]
    z(tau) = -mu Lambda h(Lambda (tau - 1))    on [1, tau_b]

The first piece rotates the phase component smoothly to zero; the second is the short
negative pulse. `mu` is selected so that `v = P_tau / P` vanishes at `tau_b`, which is
exactly `Omega(t_b) = 0`. Lemma 3.7 proves the endpoint map is strictly decreasing with
a unique root in `[1/2 - 1/(4 Lambda), 1]` and that `log P(tau_b)` is between `log 2`
and `1 + 1/Lambda`: the steering keeps a definite temperature gain. `lemma_37_report`
checks every one of those assertions numerically.

THE PHYSICAL STAGE (their Lemma 3.8). With `sigma^2 = |G|`, `s` the insertion angle,

    Gamma = sigma sin s,   a = sigma^2 sin(s) / lambda,   b = lambda Z,
    Z = sin(s) z(tau),     alpha = s - arcsin Z,          Omega(t_1) = (lambda/sigma) Theta(t_1)

and `Theta < 0`. `alpha` is the common rotation angle, which is what the PDE has to
implement.

THE PDE REALIZATION. A rigid rotation of the background does not fit on a torus. In two
dimensions it does not have to: in the frame co-rotating with `alpha(t)`, the Coriolis
and centrifugal accelerations are gradients (for divergence-free `u` in 2D,
`J u = -grad psi` up to sign) and are absorbed by the pressure, and the Euler
acceleration `alpha_ddot J x` only shifts the spatially uniform mean vorticity, which
induces no velocity on the torus. What survives is the Boussinesq system with a
ROTATING GRAVITY DIRECTION `g(t) = e(alpha(t))`, in which the stratification and every
wavevector stay fixed grid modes. The buoyancy torque `g_2 d_1 theta - g_1 d_2 theta`
then gives a wave at unit `zeta` exactly

    b = lambda (zeta . (cos alpha, -sin alpha)) = lambda sin(s - alpha) = lambda Z,

the transcribed coefficient. Once gravity tilts, the base stratification is no longer
steady, and `CoRotatingBoussinesq` cancels its torque with a low-frequency force. That
is not a cheat: the theorem being modelled is a FORCED blowup statement, and holding
the prescribed background is precisely what its force does.

DISSIPATION FACTORIZES. With equal dissipation on both fields the damping
`d = nu lambda^(2 alpha)` enters both amplitude equations on the diagonal, so
`(Theta, Omega) = e^(-d t) (Theta~, Omega~)` with the tilde pair inviscid. The selected
pulse amplitude is therefore INDEPENDENT of the viscosity, the zero of `Omega` lands at
the same time, and a holding interval decays at exactly `d`. EXP-005 Part C tests that
against the PDE rather than assuming it.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache

import numpy as np

from . import boussinesq as B


# --------------------------------------------------------------------- profiles


def smooth_step(x: float) -> float:
    """C-infinity nondecreasing step: 0 on (-inf, 0], 1 on [1, inf)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    a = math.exp(-1.0 / x)
    b = math.exp(-1.0 / (1.0 - x))
    return a / (a + b)


def bump_sin2(y: float) -> float:
    """C^1 unit-mass profile on (0, 1); sup norm H = 2."""
    if y <= 0.0 or y >= 1.0:
        return 0.0
    return 2.0 * math.sin(math.pi * y) ** 2


_CINF_MASS: float | None = None


def _cinf_mass() -> float:
    global _CINF_MASS
    if _CINF_MASS is None:
        n = 20000
        ys = (np.arange(n) + 0.5) / n
        vals = np.exp(-1.0 / (ys * (1.0 - ys)))
        _CINF_MASS = float(vals.mean())
    return _CINF_MASS


def bump_cinf(y: float) -> float:
    """C-infinity unit-mass profile on (0, 1); sup norm about 2.605."""
    if y <= 0.0 or y >= 1.0:
        return 0.0
    return math.exp(-1.0 / (y * (1.0 - y))) / _cinf_mass()


_PROFILES: dict[str, Callable[[float], float]] = {"sin2": bump_sin2, "cinf": bump_cinf}


# ------------------------------------------------------------ normalized model


@dataclass(frozen=True)
class SteeringDesign:
    """Design data of the first-stage steering model, their (3.24) and (3.25).

    `Lam` is the pulse compression, `cp` the pulse multiplier bounding the trial range.
    The proof's sufficient condition is `Lam >= 2 cp H`; a design violating it is
    allowed here and flagged by `satisfies_lemma_37_condition`, because the PDE run
    needs a wider pulse than the proof's constants give and the difference has to be
    visible rather than silent.
    """

    Lam: float
    cp: float = 3.0
    profile: str = "sin2"

    @property
    def h(self) -> Callable[[float], float]:
        return _PROFILES[self.profile]

    @property
    def H(self) -> float:
        ys = (np.arange(4000) + 0.5) / 4000.0
        return float(max(self.h(float(y)) for y in ys))

    @property
    def tau_b(self) -> float:
        return 1.0 + 1.0 / self.Lam

    @property
    def satisfies_lemma_37_condition(self) -> bool:
        return self.cp > 1.0 and self.Lam >= 2.0 * self.cp * self.H

    def z(self, tau: float, mu: float) -> float:
        """The coefficient of the normalized model; also `zeta_1 / sin s`."""
        if tau <= 0.0:
            return 1.0
        if tau <= 1.0:
            return 1.0 - smooth_step(tau)
        if tau <= self.tau_b:
            return -mu * self.Lam * self.h(self.Lam * (tau - 1.0))
        return 0.0


def integrate_model(
    design: SteeringDesign, mu: float, n1: int = 4000, n2: int = 4000
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """RK4 on `P_tautau = z P`, returning (tau, P, P_tau) over [0, tau_b].

    The two pieces are integrated with their own step counts because the pulse lives on
    an interval `Lam` times shorter and has to be resolved on its own scale.
    """

    taus = np.concatenate([
        np.linspace(0.0, 1.0, n1 + 1),
        np.linspace(1.0, design.tau_b, n2 + 1)[1:],
    ])
    ys = np.empty((taus.size, 2))
    # Scalar RK4 on (P, P_tau). Written with floats rather than length-2 arrays
    # because this loop runs tens of millions of times inside the root selection.
    y1, y2 = 1.0, 1.0
    ys[0] = (y1, y2)
    z = design.z
    for i in range(taus.size - 1):
        t = float(taus[i])
        hs = float(taus[i + 1]) - t
        za, zb, zc = z(t, mu), z(t + hs / 2.0, mu), z(t + hs, mu)
        k1a, k1b = y2, za * y1
        k2a, k2b = y2 + hs / 2.0 * k1b, zb * (y1 + hs / 2.0 * k1a)
        k3a, k3b = y2 + hs / 2.0 * k2b, zb * (y1 + hs / 2.0 * k2a)
        k4a, k4b = y2 + hs * k3b, zc * (y1 + hs * k3a)
        y1 += (hs / 6.0) * (k1a + 2.0 * k2a + 2.0 * k3a + k4a)
        y2 += (hs / 6.0) * (k1b + 2.0 * k2b + 2.0 * k3b + k4b)
        ys[i + 1] = (y1, y2)
    return taus, ys[:, 0], ys[:, 1]


def endpoint_v(design: SteeringDesign, mu: float, **kw) -> float:
    """`v(tau_b; mu) = P_tau / P` at the end of steering; its zero selects `mu`."""
    _, P, Pt = integrate_model(design, mu, **kw)
    return float(Pt[-1] / P[-1])


@lru_cache(maxsize=64)
def select_mu(design: SteeringDesign, iters: int = 48, n1: int = 2000, n2: int = 2000) -> float:
    """The selected pulse amplitude: the unique root of the endpoint map.

    Their Theorem 3.2 selects the SMALLEST root; Lemma 3.7 proves there is exactly one
    and that it lies in `[1/2 - 1/(4 Lam), 1]` under the design condition.
    """
    kw = {"n1": n1, "n2": n2}
    lo, hi = 0.0, design.cp
    if endpoint_v(design, lo, **kw) <= 0.0:
        raise ValueError("endpoint map is not positive at mu = 0")
    if endpoint_v(design, hi, **kw) >= 0.0:
        raise ValueError("endpoint map is not negative at mu = cp; raise cp")
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if endpoint_v(design, mid, **kw) > 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def lemma_37_report(design: SteeringDesign, n_mu: int = 200) -> dict:
    """Check every assertion of their Lemma 3.7 numerically. See EXP-005 gate A."""
    mu_star = select_mu(design)
    taus, P, Pt = integrate_model(design, mu_star)
    v = Pt / P
    first = taus <= 1.0
    v_first = v[first]
    tau_first = taus[first]
    int_v_first = float(np.trapezoid(v_first, tau_first))
    mus = np.linspace(0.0, design.cp, n_mu + 1)
    endpoint = np.array([endpoint_v(design, float(m), n1=800, n2=800) for m in mus])
    # every trial, not just the selected one, must keep P positive
    p_min_over_trials = min(
        float(integrate_model(design, float(m), n1=800, n2=800)[1].min()) for m in mus
    )
    return {
        "Lambda": design.Lam,
        "cp": design.cp,
        "profile": design.profile,
        "H": design.H,
        "satisfies_lemma_37_condition": design.satisfies_lemma_37_condition,
        "mu_star": mu_star,
        "P_positive_all_trials": bool(p_min_over_trials > 0.0),
        "P_min_over_trials": p_min_over_trials,
        "v_bounds_on_first_part": {
            "min_v_minus_1_over_1_plus_tau": float(np.min(v_first - 1.0 / (1.0 + tau_first))),
            "max_v": float(np.max(v_first)),
            "holds": bool(np.all(v_first >= 1.0 / (1.0 + tau_first) - 1e-9)
                          and np.all(v_first <= 1.0 + 1e-9)),
        },
        "integral_v_first_part": int_v_first,
        "integral_in_log2_to_1": bool(math.log(2.0) - 1e-9 <= int_v_first <= 1.0 + 1e-9),
        "endpoint_map_strictly_decreasing": bool(np.all(np.diff(endpoint) < 0.0)),
        "endpoint_positive_at_0": float(endpoint[0]),
        "endpoint_negative_at_cp": float(endpoint[-1]),
        "mu_star_in_proof_interval": bool(0.5 - 1.0 / (4.0 * design.Lam) <= mu_star <= 1.0),
        "log_gain": float(np.log(P[-1])),
        "log_gain_in_log2_to_1_plus_inv_Lambda": bool(
            math.log(2.0) - 1e-9 <= float(np.log(P[-1])) <= 1.0 + 1.0 / design.Lam + 1e-9
        ),
        "v_endpoint_at_mu_star": float(v[-1]),
    }


# --------------------------------------------------------------- physical stage


@dataclass(frozen=True)
class FirstStage:
    """The physical first-stage schedule of their Lemma 3.8, with dissipation.

    `A` is the background temperature-gradient magnitude at the measurement point,
    `lam = |k|` the wave frequency, `sin_s` the laboratory phase component during
    growth. Times are measured from the start of growth; growth plus their transition
    occupies `L_growth / Gamma`, steering the following `tau_b / Gamma`.
    """

    A: float
    lam: float
    sin_s: float
    design: SteeringDesign
    mu: float
    L_growth: float = 7.0
    nu: float = 0.0
    alpha: float = 1.0

    @property
    def sigma(self) -> float:
        return math.sqrt(self.A)

    @property
    def Gamma(self) -> float:
        return self.sigma * self.sin_s

    @property
    def a(self) -> float:
        return self.A * self.sin_s / self.lam

    @property
    def damping(self) -> float:
        return self.nu * self.lam ** (2.0 * self.alpha)

    @property
    def s(self) -> float:
        return math.asin(self.sin_s)

    @property
    def t1(self) -> float:
        return self.L_growth / self.Gamma

    @property
    def t_b(self) -> float:
        return self.t1 + self.design.tau_b / self.Gamma

    def Z(self, t: float) -> float:
        """Laboratory phase component `zeta_1(t)` for a unit `zeta`."""
        if t <= self.t1:
            return self.sin_s
        return self.sin_s * self.design.z(self.Gamma * (t - self.t1), self.mu)

    def rotation_angle(self, t: float) -> float:
        """Common rotation angle `alpha = s - arcsin Z`, zero during growth."""
        z = max(-1.0, min(1.0, self.Z(t) / 1.0))
        return self.s - math.asin(z)

    def gravity(self, t: float) -> tuple[float, float]:
        """Laboratory gravity direction expressed in co-rotating coordinates."""
        ang = self.rotation_angle(t)
        return (math.sin(ang), math.cos(ang))

    def b(self, t: float) -> float:
        return self.lam * self.Z(t)

    def eigen_seed(self, Theta0: float) -> tuple[float, float]:
        """Data on the growing eigenline, `Omega = (lambda / sigma) Theta`."""
        return (Theta0, self.lam * Theta0 / self.sigma)

    def integrate(
        self, Theta0: float, t_end: float, dt: float
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """RK4 on the amplitude pair through the whole cycle."""
        d = self.damping
        a = self.a
        b = self.b
        n = int(round(t_end / dt))
        ts = np.linspace(0.0, n * dt, n + 1)
        ys = np.empty((n + 1, 2))
        y1, y2 = self.eigen_seed(Theta0)
        ys[0] = (y1, y2)
        half = dt / 2.0
        for i in range(n):
            t = float(ts[i])
            ba, bb, bc = b(t), b(t + half), b(t + dt)
            k1a, k1b = a * y2 - d * y1, ba * y1 - d * y2
            k2a, k2b = (a * (y2 + half * k1b) - d * (y1 + half * k1a),
                        bb * (y1 + half * k1a) - d * (y2 + half * k1b))
            k3a, k3b = (a * (y2 + half * k2b) - d * (y1 + half * k2a),
                        bb * (y1 + half * k2a) - d * (y2 + half * k2b))
            k4a, k4b = (a * (y2 + dt * k3b) - d * (y1 + dt * k3a),
                        bc * (y1 + dt * k3a) - d * (y2 + dt * k3b))
            y1 += (dt / 6.0) * (k1a + 2.0 * k2a + 2.0 * k3a + k4a)
            y2 += (dt / 6.0) * (k1b + 2.0 * k2b + 2.0 * k3b + k4b)
            ys[i + 1] = (y1, y2)
        return ts, ys[:, 0], ys[:, 1]


# ------------------------------------------------------------------ PDE solver


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
        import torch

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
        import torch

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
