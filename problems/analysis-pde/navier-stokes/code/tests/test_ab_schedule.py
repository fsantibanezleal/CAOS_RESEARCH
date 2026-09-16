"""Tests for the Alpoge-Buckmaster schedule and the dissipation it could carry.

These check the transcription of their (3.7), (3.8) and (3.10) and the arithmetic of the
trade-off derived from it. They do NOT check a claim about their theorem, which is
inviscid; the claim under test is what our dissipative extension would require of their
schedule, and it is stated that way in the module and in the dossier.
"""

from __future__ import annotations

import pytest

from nslib import ab_schedule as A
from nslib import cascade as C


def test_the_published_constants_are_the_ones_transcribed():
    s = A.ABSchedule()
    assert s.Q_star == 200 and s.delta == 0.125
    assert s.Q(1) == 201 and s.Q(2) == 202 and s.Q(50) == 250
    # their rule 120 k_q <= Q_q, so Q* = 200 buys one derivative, and more needs more Q
    assert s.derivatives_controlled(1) == 1
    assert A.ABSchedule(Q_star=1000).derivatives_controlled(1) == 8


def test_the_amplitude_identity_they_state_exactly():
    """|Theta_seed| e^(L_q) = lambda_q^(-7/8): the margin delta is 1/8."""
    k, beta = 7, A.BETA                      # any k works; the k cancels
    seed_exponent = -k - 6
    gain_exponent = k + 5 + beta
    assert seed_exponent + gain_exponent == pytest.approx(-0.875)
    assert 1.0 + (seed_exponent + gain_exponent) == pytest.approx(A.DELTA_PUBLISHED)


def test_our_cascade_exponent_for_their_schedule():
    s = A.ABSchedule()
    assert s.p(1) == pytest.approx(201 / 0.125)            # p = Q/delta = 8 Q
    # and our own threshold relation applied to it
    assert C.alpha_c(s.p(1)) == pytest.approx(s.alpha_max(1))
    assert s.alpha_max(1) == pytest.approx(0.125 / (4 * 201))
    assert s.alpha_max(1) < 1.6e-4


def test_their_own_insertion_angle_costs_another_factor_of_the_ratio():
    s = A.ABSchedule()
    assert s.alpha_max(5, favourable_angle=False) == pytest.approx(
        s.alpha_max(5) / s.Q(4))
    assert s.alpha_max(5, favourable_angle=False) < 8e-7


def test_no_positive_dissipation_survives_every_stage():
    s = A.ABSchedule()
    for epsilon in (1e-6, 1e-9, 1e-12):
        assert A.smooth_forcing_is_incompatible_with_dissipation(s, epsilon)
    # the admissible exponent goes to zero as the ratio grows
    assert s.alpha_max(10_000) < s.alpha_max(100) < s.alpha_max(1)
    assert s.alpha_max(10**7) < 1e-8


@pytest.mark.parametrize("alpha", [1.0, 1e-3, 1.6e-4])
def test_exponents_above_the_first_stage_bound_stop_it_immediately(alpha):
    """The first stage already fails above delta / (4 (Q* + 1)) = 1.55e-04."""
    assert A.ABSchedule().alpha_max(1) < 1.6e-4
    assert A.ABSchedule().stall_stage(alpha) == 1


def test_just_below_that_bound_the_cascade_runs_and_then_stalls():
    """1e-04 clears the first stage, runs 112 of them, and stops at 113."""
    s = A.ABSchedule()
    assert s.alpha_max(1) > 1e-4
    q = s.stall_stage(1e-4)
    assert q == 113
    assert s.Q(q) == pytest.approx(0.125 / (4 * 1e-4), abs=1)


def test_a_small_exponent_survives_finitely_many_stages_and_then_stalls():
    s = A.ABSchedule()
    q = s.stall_stage(1e-5)
    assert q is not None and q > 1
    assert s.alpha_max(q - 1) > 1e-5 >= s.alpha_max(q)
    # delta/(4 alpha) - Q_star stages, which is 3125 - 200 here
    assert q == pytest.approx(0.125 / (4 * 1e-5) - s.Q_star, abs=2)


def test_the_trade_off_reduces_to_our_own_cap_in_the_limit():
    assert A.alpha_max_general(1.0, 1.0) == pytest.approx(0.25)
    assert A.alpha_max_general(A.DELTA_PUBLISHED, 200) == pytest.approx(0.125 / 800)
    assert A.alpha_max_general(0.5, 2.0) == pytest.approx(0.0625)


def test_how_many_derivatives_a_target_exponent_can_afford():
    published_cmz_ours = C.ALPHA0_CMZ / 2.0
    assert A.derivatives_affordable(published_cmz_ours) < 1.0   # not even one
    assert A.derivatives_affordable(1e-4) == pytest.approx(0.125 / (4e-4 * 120), rel=1e-9)
    assert A.derivatives_affordable(1e-4) > 2.0
    # and the ratio a target exponent allows
    assert A.ratio_needed_for(1e-4) == pytest.approx(312.5)


def test_the_closed_form_stall_stage_agrees_with_a_direct_search():
    """The closed form replaced a bounded loop; check it against the loop where both run."""
    s = A.ABSchedule()
    for alpha in (1e-3, 3e-4, 1e-4, 3e-5, 1e-5):
        closed = s.stall_stage(alpha)
        direct = next(q for q in range(1, 20_000) if alpha >= s.alpha_max(q))
        assert closed == direct
    for alpha in (1e-5, 1e-6):
        closed = s.stall_stage(alpha, favourable_angle=False)
        direct = next(q for q in range(1, 20_000)
                      if alpha >= s.alpha_max(q, favourable_angle=False))
        assert closed == direct


def test_one_derivative_of_force_regularity_caps_the_exponent_far_below_the_published_one():
    """The sharpened form: the correction rate, not the constants, is what blocks it."""
    assert A.alpha_max_for_derivatives(1) == pytest.approx(1.0 / 480.0)
    assert A.alpha_max_for_derivatives(1) == pytest.approx(0.002083, rel=1e-3)
    assert A.alpha_max_for_derivatives(1, delta=0.125) == pytest.approx(0.125 / 480.0)
    assert A.alpha_max_for_derivatives(2) == pytest.approx(1.0 / 960.0)
    with pytest.raises(ValueError):
        A.alpha_max_for_derivatives(0)
    with pytest.raises(ValueError):
        A.alpha_max_for_derivatives(1, delta=1.5)


def test_the_gap_to_the_published_threshold_is_more_than_twentyfold():
    gap = A.gap_to_published_threshold(k=1, delta=1.0)
    assert gap > 20.0
    assert gap == pytest.approx(22.2, rel=5e-2)
    # and at their own margin it is worse by exactly 1/delta, since the bound is linear
    # in delta (the first draft of this test asserted a strict inequality where the
    # relation is an identity, and failed by one part in ten thousand)
    assert A.gap_to_published_threshold(k=1, delta=A.DELTA_PUBLISHED) == pytest.approx(
        gap / A.DELTA_PUBLISHED)
    assert A.gap_to_published_threshold(k=1, delta=A.DELTA_PUBLISHED) == pytest.approx(
        177.9, rel=5e-3)
