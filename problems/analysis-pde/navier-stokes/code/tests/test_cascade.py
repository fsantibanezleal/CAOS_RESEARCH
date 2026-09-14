"""Tests for the cascade exponent bookkeeping."""

from __future__ import annotations

import math

import pytest

from nslib import cascade as C


def test_alpha_c_is_one_over_four_p():
    for p in (1.0, 2.0, 5.0, C.P_STAR):
        assert C.alpha_c(p) == pytest.approx(1.0 / (4.0 * p), rel=1e-15)


def test_alpha_c_rejects_nonpositive_p():
    with pytest.raises(ValueError):
        C.alpha_c(0.0)


def test_published_threshold_gives_p_star_exactly():
    """p = 1/(2 alpha_0) = (22 + 8 sqrt 7)/8 = 11/4 + sqrt 7.

    Arithmetic regression only. Corrected 2026-09-14: the identity holds at every alpha
    along the published family and does not locate alpha_0; see nslib.cmz_budget.
    """
    p = C.implied_p(C.ALPHA0_CMZ)
    assert p == pytest.approx(11.0 / 4.0 + math.sqrt(7.0), rel=1e-13)
    assert p == pytest.approx((22.0 + 8.0 * math.sqrt(7.0)) / 8.0, rel=1e-13)


def test_p_star_is_above_one_so_c1_is_satisfiable():
    """C1 (summable amplitudes) needs p > 1. The calibrated p must respect it."""
    assert C.P_STAR > 1.0


def test_c1_requires_frequency_to_outgrow_gradient():
    """p <= 1 makes the wave amplitudes non-summable, so the temperature is unbounded."""
    assert not C.Schedule(g=1.0, p=0.9, alpha=0.01, nu=1e-6).c1_amplitude_summable()
    assert C.Schedule(g=1.0, p=2.0, alpha=0.01, nu=1e-6).c1_amplitude_summable()
    # and log Theta_q really does fall away when p > 1
    s = C.Schedule(g=1.0, p=2.0, alpha=0.01, nu=1e-6)
    assert s.log_Theta(200) < s.log_Theta(0) - 100.0


def test_c3_time_budget_is_finite_for_any_positive_growth():
    """The repair's first substantive result: the time budget is not the binding constraint."""
    s = C.Schedule(g=1.0, p=2.0, alpha=0.01, nu=1e-9)
    assert math.isfinite(s.c3_log_total_time(stages=200))


def test_c2_and_c4_agree_on_the_exponent():
    """Charging dissipation during the holds does NOT move the threshold.

    The remaining time shrinks like 1/sqrt(A_q), exactly the rate at which the
    growth rate rises, so the survival constraint reproduces the growth constraint.
    Both read alpha p < 1/4, which is what this checks at the level of which
    schedules close.
    """
    p, nu = 3.0, 1e-8
    below = C.Schedule(g=1.0, p=p, alpha=0.9 * C.alpha_c(p), nu=nu)
    above = C.Schedule(g=1.0, p=p, alpha=1.6 * C.alpha_c(p), nu=nu)
    assert below.c2_growth_positive(stages=400)
    # The horizon must reach the asymptotic regime. A supercritical schedule with a
    # tiny viscosity still grows for many stages: the stall sets in only near
    # q ~ log(1/nu) / (g (2 alpha p - 1/2)), which is about 61 stages here. A short
    # horizon would report "grows" and hide the constraint entirely.
    assert above.c2_growth_positive(stages=50)
    assert not above.c2_growth_positive(stages=400)


def test_supercritical_stall_onset_scales_like_log_one_over_nu():
    """Smaller viscosity delays the stall but never prevents it.

    This is the same trap as the refuted first-pass threshold: a long transient rise
    is not escape. Recorded as a test so nobody reads an early stage count as a pass.
    """
    p, alpha = 3.0, 1.6 * C.alpha_c(3.0)
    onsets = []
    for nu in (1e-4, 1e-8, 1e-12):
        s = C.Schedule(g=1.0, p=p, alpha=alpha, nu=nu)
        q = next(q for q in range(4000) if s.log_sigma(q) == float("-inf"))
        onsets.append(q)
    assert onsets[0] < onsets[1] < onsets[2]
    # the predicted onset is log(1/nu) / (g (2 alpha p - 1/2))
    predicted = math.log(1e8) / (2 * alpha * p - 0.5)
    assert abs(onsets[1] - predicted) <= 2.0


def test_growth_rate_turns_negative_beyond_the_cap():
    s = C.Schedule(g=1.0, p=2.0, alpha=0.5, nu=1e-3)
    alive = [s.log_sigma(q) > float("-inf") for q in range(40)]
    assert alive[0]
    assert not all(alive), "a supercritical alpha must eventually stall the cascade"


def test_stage_time_is_infinite_when_the_stage_cannot_grow():
    s = C.Schedule(g=1.0, p=2.0, alpha=1.0, nu=1e3)
    assert s.log_stage_time(0) == math.inf


def test_survival_exponent_is_finite_for_a_subcritical_schedule():
    s = C.Schedule(g=1.0, p=2.0, alpha=0.05, nu=1e-6)
    for q in (0, 5, 20):
        e = s.c4_log_survival_exponent(q, stages=120)
        assert e < math.inf


def test_subcritical_schedule_closes_and_supercritical_does_not():
    p, nu = 4.0, 1e-10
    assert C.Schedule(g=1.0, p=p, alpha=0.5 * C.alpha_c(p), nu=nu).closes(stages=120)
    assert not C.Schedule(g=1.0, p=p, alpha=4.0 * C.alpha_c(p), nu=nu).closes(stages=120)


def test_numeric_threshold_tracks_the_closed_form():
    """Bisection on the simulated schedule must land near 1/(4p).

    A loose tolerance is correct here: the numeric search uses a finite stage
    horizon and a survival floor, both of which bite slightly below the asymptotic
    threshold. The point is that the closed form is not off by a factor.
    """
    for p in (2.0, 4.0, C.P_STAR):
        got = C.critical_alpha_numeric(p, nu=1e-10, g=1.0)
        assert math.isfinite(got)
        assert got == pytest.approx(C.alpha_c(p), rel=0.5)


def test_classical_viscosity_is_far_above_every_plausible_threshold():
    """alpha = 1 is the classical case. No p > 1 admits it."""
    for p in (1.0, 2.0, C.P_STAR, 20.0):
        assert C.alpha_c(p) < 1.0
