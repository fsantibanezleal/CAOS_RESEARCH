"""Tests for the batched cascade evaluation.

The scalar `cascade.Schedule` is the readable reference and `sweep.evaluate` is the
fast path. A fast path that quietly disagrees with its reference is worse than no
fast path, so the central test here is that they agree schedule by schedule.
"""

from __future__ import annotations

import math

import pytest
import torch

from nslib import cascade as C
from nslib import sweep as S

DEV = torch.device("cpu")
DT = torch.float64


def _t(x):
    return torch.tensor(x, device=DEV, dtype=DT)


def test_batched_agrees_with_the_scalar_reference():
    """Same verdict as cascade.Schedule.closes on a spread of parameters."""
    cases = [(g, p, a, nu)
             for g in (0.5, 1.0, 1.7)
             for p in (1.2, 3.0, C.P_STAR, 9.0)
             for a in (0.005, 0.02, 0.08, 0.2)
             for nu in (1e-6, 1e-10)]
    g, p, a, nu = (_t([c[i] for c in cases]) for i in range(4))
    batched = S.evaluate(g, p, a, nu, stages=120)["closes"].tolist()
    scalar = [C.Schedule(g=c[0], p=c[1], alpha=c[2], nu=c[3]).closes(stages=120) for c in cases]
    assert batched == scalar


def test_batched_constraint_flags_agree_with_the_reference():
    cases = [(1.0, p, a, 1e-8) for p in (0.8, 2.0, 6.0) for a in (0.01, 0.05, 0.2)]
    g, p, a, nu = (_t([c[i] for c in cases]) for i in range(4))
    r = S.evaluate(g, p, a, nu, stages=120)
    for i, c in enumerate(cases):
        sched = C.Schedule(g=c[0], p=c[1], alpha=c[2], nu=c[3])
        assert bool(r["c1"][i]) == sched.c1_amplitude_summable()
        assert bool(r["c2"][i]) == sched.c2_growth_positive(stages=120)


def test_reverse_logcumsumexp_matches_a_direct_sum():
    x = torch.log(torch.rand(5, 30, dtype=DT) + 1e-3)
    got = S._reverse_logcumsumexp(x)
    for i in range(x.shape[0]):
        for q in range(x.shape[1] - 1):
            want = torch.logsumexp(x[i, q + 1:], dim=0)
            assert float(got[i, q]) == pytest.approx(float(want), rel=1e-12)
        assert got[i, -1] == float("-inf")


def test_log_diff_exp_matches_direct_evaluation():
    a = _t([1.0, 2.0, -3.0, 10.0])
    b = _t([0.0, 1.9, -4.0, 10.0])
    got = S._log_diff_exp(a, b)
    for i in range(3):
        want = math.log(math.exp(float(a[i])) - math.exp(float(b[i])))
        assert float(got[i]) == pytest.approx(want, rel=1e-10)
    assert got[3] == float("-inf")       # a == b gives no positive difference


def test_closing_schedules_respect_the_horizon_bound():
    """Every schedule that closes must satisfy alpha p below the DETECTABLE bound.

    Not below 1/4: a finite horizon cannot see a stall that arrives after the last
    stage, so the honest bound is 1/4 + log(1/nu) / (2 g (Q-1)). Using Q instead of
    Q-1 here leaves apparent violations; the binding stage is the last one inspected.
    """
    stages = 200
    gen = torch.Generator().manual_seed(7)
    n = 20000
    p = torch.rand(n, generator=gen, dtype=DT) * 10.5 + 1.5
    a = torch.rand(n, generator=gen, dtype=DT) * 0.30 + 0.002
    g = torch.rand(n, generator=gen, dtype=DT) * 1.5 + 0.5
    nu = 10.0 ** (-(torch.rand(n, generator=gen, dtype=DT) * 10.0 + 4.0))
    closes = S.evaluate(g, p, a, nu, stages=stages)["closes"]
    bound = 0.25 + torch.log(1.0 / nu) / (2.0 * g * (stages - 1))
    assert int((closes & (a * p >= bound)).sum()) == 0
    assert int(closes.sum()) > 0, "the ensemble must contain some closing schedules"


def test_critical_alpha_matches_the_horizon_corrected_closed_form():
    p = _t([2.0, 3.0, C.P_STAR, 9.5])
    for stages in (200, 400):
        got = S.critical_alpha(p, nu=1e-10, g=1.0, stages=stages)
        want = _t([C.alpha_c_finite_horizon(float(x), 1e-10, 1.0, stages) for x in p])
        assert torch.allclose(got, want, rtol=1e-4)


def test_measured_threshold_converges_to_one_over_four_p():
    """Doubling the horizon must halve the gap to the asymptotic closed form."""
    p = _t([3.0])
    gaps = []
    for stages in (200, 400, 800, 1600):
        got = float(S.critical_alpha(p, nu=1e-10, g=1.0, stages=stages)[0])
        gaps.append(abs(got - C.alpha_c(3.0)))
    for i in range(len(gaps) - 1):
        assert gaps[i + 1] < gaps[i]
        assert gaps[i] / gaps[i + 1] == pytest.approx(2.0, rel=0.05)


def test_hold_damping_never_binds_alone():
    """C4 must not fail while C2 holds, or the threshold would be lower than 1/(4p)."""
    pg = torch.linspace(1.5, 12.0, 24, dtype=DT)
    ag = torch.linspace(0.005, 0.30, 24, dtype=DT)
    P, A = torch.meshgrid(pg, ag, indexing="ij")
    P, A = P.reshape(-1), A.reshape(-1)
    r = S.evaluate(torch.ones_like(P), P, A, torch.full_like(P, 1e-10), stages=300)
    assert int((r["c2"] & ~r["c4"]).sum()) == 0


def test_zero_viscosity_never_stalls():
    n = 16
    p = torch.linspace(1.5, 12.0, n, dtype=DT)
    r = S.evaluate(torch.ones(n, dtype=DT), p, torch.full((n,), 0.2, dtype=DT),
                   torch.zeros(n, dtype=DT), stages=150)
    assert bool(r["c2"].all())
    assert bool(r["closes"].all())
