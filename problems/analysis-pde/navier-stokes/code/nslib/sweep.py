"""Batched GPU evaluation of the cascade constraints over a parameter ensemble.

`cascade.Schedule` is the readable scalar reference; this module is the same four
constraints written as tensor operations so that 1e5 to 1e7 schedules can be decided
at once. Both are kept and cross-checked against each other by the tests, because a
fast path that quietly disagrees with the reference is worse than no fast path.

Everything is in log space, for the same reason as in `cascade`: A_q and lambda_q
overflow double precision within a few dozen stages.

Shapes. A batch of B schedules is evaluated over Q stages; intermediate tensors are
(B, Q), so memory is 8 B Q bytes per tensor in float64. Chunk the batch if that
exceeds the card.
"""

from __future__ import annotations

import math

import torch

NEG_INF = float("-inf")


def _log_diff_exp(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """log(e^a - e^b) elementwise, -inf where a <= b."""
    out = torch.full_like(a, NEG_INF)
    m = a > b
    if m.any():
        d = (b[m] - a[m]).clamp(max=-1e-12)
        out[m] = a[m] + torch.log1p(-torch.exp(d))
    return out


def _reverse_logcumsumexp(x: torch.Tensor) -> torch.Tensor:
    """R[:, q] = logsumexp(x[:, q+1:]), with -inf for the empty tail."""
    flipped = torch.flip(x, dims=[1])
    cum = torch.logcumsumexp(flipped, dim=1)
    cum = torch.flip(cum, dims=[1])
    out = torch.full_like(x, NEG_INF)
    out[:, :-1] = cum[:, 1:]
    return out


def evaluate(
    g: torch.Tensor,
    p: torch.Tensor,
    alpha: torch.Tensor,
    nu: torch.Tensor,
    stages: int = 200,
    phi: float = math.pi / 2.0,
    log_gain: float = 1.0,
    max_survival_exponent: float = 6.9,
) -> dict[str, torch.Tensor]:
    """Decide a batch of schedules. All inputs are 1-D tensors of equal length.

    Returns a dict of per-schedule diagnostics and the boolean `closes`.
    """
    dev, dt = g.device, g.dtype
    q = torch.arange(stages, device=dev, dtype=dt).unsqueeze(0)      # (1, Q)
    g_, p_, a_, nu_ = (t.unsqueeze(1) for t in (g, p, alpha, nu))    # (B, 1)

    log_A = g_ * q
    log_lam = p_ * log_A
    log_theta = g_ * (q + 1.0) - log_lam

    sin_phi = math.sin(phi)
    log_rate = 0.5 * log_A + math.log(sin_phi) if sin_phi > 0 else torch.full_like(log_A, NEG_INF)
    log_damp = torch.where(
        nu_ > 0, torch.log(nu_.clamp_min(1e-300)) + 2.0 * a_ * log_lam,
        torch.full_like(log_A, NEG_INF))

    log_sigma = _log_diff_exp(log_rate, log_damp)
    alive = torch.isfinite(log_sigma)

    log_T = math.log(log_gain) - log_sigma          # +inf where sigma is -inf
    log_T = torch.where(alive, log_T, torch.full_like(log_T, float("inf")))

    finite_T = torch.isfinite(log_T)
    safe_T = torch.where(finite_T, log_T, torch.full_like(log_T, NEG_INF))
    log_total_time = torch.logsumexp(safe_T, dim=1)
    log_R = _reverse_logcumsumexp(safe_T)

    surv = torch.where(torch.isfinite(log_damp) & torch.isfinite(log_R),
                       log_damp + log_R, torch.full_like(log_damp, NEG_INF))

    c1 = p > 1.0
    c2 = alive.all(dim=1)
    c3 = finite_T.all(dim=1)
    c4 = (surv <= max_survival_exponent).all(dim=1)

    return {
        "closes": c1 & c2 & c3 & c4,
        "c1": c1, "c2": c2, "c3": c3, "c4": c4,
        "log_total_time": log_total_time,
        "max_survival_exponent": surv.max(dim=1).values,
        "first_stall_stage": torch.where(
            c2, torch.full_like(g, -1.0),
            (~alive).float().argmax(dim=1).to(dt)),
        "log_theta_last": log_theta[:, -1],
    }


def critical_alpha(
    p_values: torch.Tensor,
    nu: float,
    g: float = 1.0,
    stages: int = 200,
    lo: float = 1e-8,
    hi: float = 1.0,
    iters: int = 48,
    **kw,
) -> torch.Tensor:
    """Vectorized bisection for alpha_c(p): the largest alpha whose schedule closes."""
    dev, dt = p_values.device, p_values.dtype
    a = torch.full_like(p_values, lo)
    b = torch.full_like(p_values, hi)
    gt = torch.full_like(p_values, g)
    nut = torch.full_like(p_values, nu)
    for _ in range(iters):
        m = 0.5 * (a + b)
        ok = evaluate(gt, p_values, m, nut, stages=stages, **kw)["closes"]
        a = torch.where(ok, m, a)
        b = torch.where(ok, b, m)
    _ = dev, dt
    return a
