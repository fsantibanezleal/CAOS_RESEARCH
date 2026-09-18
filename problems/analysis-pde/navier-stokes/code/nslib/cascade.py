"""Exponent bookkeeping for the layer cascade, with the time budget and hold damping.

This repairs the two omissions of the first-pass estimate in
`../../context/2026-09-11-simplified-model-and-beyond.md`: that recursion had no
time axis, and it charged no dissipation during the holding intervals.

Everything is computed in LOG SPACE. The quantities here are exponentially large by
construction (A_q, lambda_q) or exponentially small (Theta_q, T_q), so a direct
floating-point evaluation overflows within a few dozen stages; the first version of
this module did exactly that. Working in logs is not an optimization, it is the only
way the model is representable.

Model. Stages q = 0, 1, 2, ... with a geometric background gradient and a power-law
frequency schedule,

    A_q = A_0 e^(g q),        lambda_q = c_lam * A_q^p,        Theta_q = A_{q+1} / lambda_q

where p is the frequency growth exponent. Theta_q is fixed by the amplification
identity grad(wave)(0) = lambda Theta zeta: the gradient handed to stage q+1 is
lambda_q Theta_q. Everything is scale free in the exponents.

Four constraints.

C1  amplitude budget:  sum_q Theta_q < infinity, so the temperature stays bounded
    while its gradient diverges. log Theta_q = g + g q (1 - p), so C1 is p > 1.
    The frequency must grow FASTER than the gradient it is producing.

C2  growth positivity: sqrt(A_q) sin(phi) > nu lambda_q^(2 alpha), which in logs is
    g q / 2 + log sin(phi) > log nu + 2 alpha p g q, so asymptotically alpha p < 1/4.

C3  time budget: sum_q T_q < infinity with T_q ~ log(gain) / sigma_q. Since
    sigma_q ~ e^(g q / 2), T_q decays geometrically and the sum converges for any
    g > 0. C3 is therefore NOT binding on alpha. That is the first substantive
    result of the repair.

C4  layer survival (the hold-damping omission): the gradient contributed by stage q
    must still be present at the blowup time. It decays by
    exp(-nu lambda_q^(2 alpha) R_q) with R_q = sum_{j>q} T_j the remaining time.
    Since R_q ~ e^(-g q / 2), boundedness needs 2 alpha p - 1/2 < 0, that is
    alpha p < 1/4 AGAIN.

C2 and C4 coincide. That is the second substantive result: charging dissipation
during the holds does NOT move the exponent, because the remaining time shrinks at
exactly the rate 1/sqrt(A_q) at which the growth rate rises. The threshold is

    alpha_c = 1 / (4 p)        in the (-Laplacian)^alpha convention

and the only way to lower it is to be forced into a larger p.

Calibration against the published result. Cordoba, Martinez-Zoroa and Zheng prove
blowup for every |grad|^alpha exponent below alpha_0 = (22 - 8 sqrt 7) / 9, which is
alpha_0 / 2 in our convention. Inverting,

    p = 1 / (4 * (alpha_0 / 2)) = 1 / (2 alpha_0) = 9 / (2 (22 - 8 sqrt 7))
      = 9 (22 + 8 sqrt 7) / 72 = (22 + 8 sqrt 7) / 8 = 11/4 + sqrt 7   EXACTLY.

What that does and does not establish. CORRECTED 2026-09-14: it establishes nothing
about where alpha_0 sits. alpha_c = 1/(4p) is the construction's dissipation
constraint saturated, and the published family saturates it at EVERY alpha, so
p = 1/(2 alpha) holds identically along it; the value at alpha_0 is just the identity
evaluated there. That 11/4 + sqrt 7 looks clean is automatic arithmetic in Q(sqrt 7).
The published threshold is set by a force-regularity constraint this model does not
contain, the outer velocity acting on the inner layer; `cmz_budget` derives
(22 - 8 sqrt 7)/9 from it exactly. The relation above remains correct as a statement
about this model's own threshold.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Cordoba, Martinez-Zoroa, Zheng, ARMA 250 (2026) article 38, Theorem 1.
ALPHA0_CMZ = (22.0 - 8.0 * math.sqrt(7.0)) / 9.0
P_STAR = 11.0 / 4.0 + math.sqrt(7.0)

_NEG_INF = float("-inf")


def _logsumexp(values: list[float]) -> float:
    finite = [v for v in values if v > _NEG_INF]
    if not finite:
        return _NEG_INF
    m = max(finite)
    return m + math.log(sum(math.exp(v - m) for v in finite))


def _log_diff_exp(a: float, b: float) -> float:
    """log(e^a - e^b) for a > b; -inf when a <= b (no positive difference)."""
    if a <= b:
        return _NEG_INF
    d = b - a
    if d < -700.0:
        return a
    return a + math.log1p(-math.exp(d))


def alpha_c(p: float) -> float:
    """Cascade dissipation threshold in the (-Laplacian)^alpha convention."""
    if p <= 0:
        raise ValueError("p must be positive")
    return 1.0 / (4.0 * p)


def detectable_alpha_p(nu: float, g: float = 1.0, stages: int = 400,
                       gamma: float = 0.5) -> float:
    """Largest product alpha*p whose stall is still visible within `stages`.

    A supercritical schedule does not stall immediately. The growth rate stays
    positive while

        g q / 2 + log sin(phi) > log nu + 2 alpha p g q,

    so the first stalled stage is near q* = log(1/nu) / (g (2 alpha p - 1/2)). Stages
    are indexed q = 0 .. Q-1, so the LAST stage a run of Q stages inspects is Q-1 and
    that is the binding one. A truncated run therefore cannot see any schedule with

        alpha p < 1/4 + log(1/nu) / (2 g (Q - 1)),

    and a bisection on such a run reports a threshold too HIGH by the factor
    1 + 2 log(1/nu) / (g (Q - 1)). The Q versus Q-1 distinction is not cosmetic: with
    Q it leaves 47 apparent violations in a million-schedule ensemble, and with Q-1 it
    leaves none, the tightest closing schedule sitting 2.7e-06 below the bound.

    This is the same trap that produced the refuted first-pass estimate: a long
    transient is not escape. Quote this bound whenever a numerically measured
    threshold is compared with the closed form.
    """
    if nu <= 0.0:
        return gamma / 2.0
    return gamma / 2.0 + math.log(1.0 / nu) / (2.0 * g * max(1, stages - 1))


def alpha_c_finite_horizon(p: float, nu: float, g: float = 1.0, stages: int = 400) -> float:
    """Threshold a finite-horizon bisection will actually report."""
    if p <= 0:
        raise ValueError("p must be positive")
    return detectable_alpha_p(nu, g, stages) / p


def implied_p(alpha0_cmz: float = ALPHA0_CMZ) -> float:
    """Frequency growth exponent implied by a |grad|^alpha threshold."""
    return 1.0 / (2.0 * alpha0_cmz)


@dataclass(frozen=True)
class Schedule:
    """One cascade schedule, evaluated entirely in log space."""

    g: float          # log growth per stage of the background gradient
    p: float          # lambda_q ~ A_q ** p
    alpha: float      # dissipation order, (-Laplacian)^alpha
    nu: float
    log_A0: float = 0.0
    log_c_lam: float = 0.0
    phi: float = math.pi / 2.0
    log_gain: float = 1.0   # log of the per-stage amplification factor
    # Growth law: the rate is A^gamma. 1/2 is the Boussinesq pendulum law this model was
    # built for; 1 is vortex stretching, the law of the hypodissipative Navier-Stokes
    # construction. Theorem 3.1 of the paper predicts alpha_c = gamma/(2p) for both.
    gamma: float = 0.5

    # --------------------------------------------------------------- log fields

    def log_A(self, q: int) -> float:
        return self.log_A0 + self.g * q

    def log_lam(self, q: int) -> float:
        return self.log_c_lam + self.p * self.log_A(q)

    def log_Theta(self, q: int) -> float:
        return self.log_A(q + 1) - self.log_lam(q)

    def log_inviscid_rate(self, q: int) -> float:
        s = math.sin(self.phi)
        if s <= 0.0:
            return _NEG_INF
        return self.gamma * self.log_A(q) + math.log(s)

    def log_damping(self, q: int) -> float:
        if self.nu <= 0.0:
            return _NEG_INF
        return math.log(self.nu) + 2.0 * self.alpha * self.log_lam(q)

    def log_sigma(self, q: int) -> float:
        """log of the net growth rate; -inf when the stage cannot grow."""
        return _log_diff_exp(self.log_inviscid_rate(q), self.log_damping(q))

    def log_stage_time(self, q: int) -> float:
        ls = self.log_sigma(q)
        return math.inf if ls == _NEG_INF else math.log(self.log_gain) - ls

    def log_remaining_time(self, q: int, stages: int) -> float:
        terms = [self.log_stage_time(j) for j in range(q + 1, stages)]
        if any(t == math.inf for t in terms):
            return math.inf
        return _logsumexp(terms)

    # ------------------------------------------------------------- constraints

    def c1_amplitude_summable(self) -> bool:
        """log Theta_q must go to -infinity, which happens exactly when p > 1."""
        return self.p > 1.0

    def c2_growth_positive(self, stages: int = 400) -> bool:
        return all(self.log_sigma(q) > _NEG_INF for q in range(stages))

    def c3_log_total_time(self, stages: int = 400) -> float:
        terms = [self.log_stage_time(q) for q in range(stages)]
        if any(t == math.inf for t in terms):
            return math.inf
        return _logsumexp(terms)

    def c4_log_survival_exponent(self, q: int, stages: int) -> float:
        """log of nu lambda_q^(2 alpha) R_q. Bounded means the layer survives."""
        lr = self.log_remaining_time(q, stages)
        if lr == math.inf:
            return math.inf
        ld = self.log_damping(q)
        if ld == _NEG_INF:
            return _NEG_INF
        return ld + lr

    def closes(self, stages: int = 200, max_survival_exponent: float = 6.9) -> bool:
        """Does this schedule produce a finite-time gradient blowup?

        All four constraints: summable amplitudes, positive growth at every stage,
        finite total time, and a survival exponent bounded so the accumulated
        gradient is not damped away (default bound e^-6.9, about one part in a
        thousand, matching the survival floor used before the log rewrite).
        """
        if not self.c1_amplitude_summable():
            return False
        if not self.c2_growth_positive(stages):
            return False
        if self.c3_log_total_time(stages) == math.inf:
            return False
        step = max(1, stages // 25)
        return all(
            self.c4_log_survival_exponent(q, stages) <= max_survival_exponent
            for q in range(0, stages, step)
        )


def critical_alpha_numeric(
    p: float, nu: float, g: float = 1.0, lo: float = 1e-8, hi: float = 1.0,
    iters: int = 60, stages: int = 200
) -> float:
    """Bisect on alpha for the largest exponent whose schedule still closes."""
    if not Schedule(g=g, p=p, alpha=lo, nu=nu).closes(stages):
        return float("nan")
    a, b = lo, hi
    for _ in range(iters):
        m = 0.5 * (a + b)
        if Schedule(g=g, p=p, alpha=m, nu=nu).closes(stages):
            a = m
        else:
            b = m
    return a


# ------------------------------------------- super-geometric schedules (NS-016)


def log_theta_growth_exponent(R: float, p: float) -> float:
    """Exponent of `log Theta_q` along a schedule with frequency ratio `R`.

    Write `u_q = log lambda_q`. A schedule with `u_{q+1} = R u_q` is super-geometric for
    `R > 1` and the geometric schedule of the rest of this module for `R = 1`. With
    `lambda_q = c A_q^p`, so `log A_q = u_q / p` up to a constant, the amplification
    identity `A_{q+1} = lambda_q Theta_q` gives

        log Theta_q = u_q (R/p - 1),

    so the amplitudes are summable exactly when `R < p`. That is C1 for a general
    schedule, and it reduces to `p > 1` at `R = 1`.

    Note `R` is not a free parameter beside `p`: rearranging the same identity gives
    `R = p (1 + log Theta_q / u_q)`, so choosing how much amplitude each stage spends IS
    choosing the schedule, and `R < p` always holds while `Theta_q < 1`.
    """
    if p <= 0.0:
        raise ValueError("p must be positive")
    return R / p - 1.0


def c1_holds_for_schedule(R: float, p: float) -> bool:
    """Summable amplitudes along a schedule of ratio `R`: exactly `R < p`."""
    return log_theta_growth_exponent(R, p) < 0.0


def alpha_c_under_admissible_ratios(alpha_ours: float) -> float | None:
    """Our cascade cap once the SCHEDULE must be one the published force budget admits.

    Our own constraints give `alpha_c = 1/(4p)` with `p > R`, so a schedule of ratio `R`
    caps the dissipation exponent at `1/(4R)`. The published force budget admits a ratio
    only inside an interval that closes at its threshold (`cmz_budget.feasible_R_interval`,
    in the `|grad|^alpha` convention, hence the factor two here). Combining the two:

        alpha < 1 / (4 R_-(2 alpha)),      and no admissible R at all above the threshold.

    Returns that cap, or None when no ratio is admissible. The consequence is the point of
    this function: **our model's own cap of 1/4 is never reached.** For every exponent
    above the published threshold there is no admissible schedule at all, so the cascade
    cannot close for reasons that have nothing to do with the dissipation constraint that
    produced 1/4.
    """
    from . import cmz_budget

    interval = cmz_budget.feasible_R_interval(2.0 * alpha_ours)
    if interval is None:
        return None
    return 1.0 / (4.0 * interval[0])
