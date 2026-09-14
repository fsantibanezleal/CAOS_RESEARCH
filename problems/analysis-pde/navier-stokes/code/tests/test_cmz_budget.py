"""Tests for the exponent-budget reconstruction of the published threshold."""

from __future__ import annotations

import math

import pytest

from nslib import cmz_budget as B

ALPHAS = [0.005, 0.02, 0.05, 0.08, 0.09]


def test_published_threshold_is_the_root_of_the_outer_budget():
    assert B.s_max_outer(B.ALPHA0) == pytest.approx(0.0, abs=1e-14)
    assert B.s_max_outer(0.9 * B.ALPHA0) > 0.0
    assert B.s_max_outer(1.1 * B.ALPHA0) < 0.0


def test_heuristic_threshold_is_the_root_of_the_localization_budget():
    assert B.s_max_localization(B.ALPHA_HEURISTIC) == pytest.approx(0.0, abs=1e-14)
    assert B.ALPHA_HEURISTIC > B.ALPHA0, "the heuristic must overshoot the proved threshold"


@pytest.mark.parametrize("alpha", ALPHAS)
def test_papers_R_is_the_optimum_of_the_outer_budget(alpha):
    """R = sqrt(2/(7 alpha)) is chosen in the paper; it must maximise constraint O."""
    Rs = B.optimal_R_outer(alpha)
    assert Rs == pytest.approx(math.sqrt(2.0 / (7.0 * alpha)), rel=1e-14)
    best = B.s_bound_outer(alpha, Rs)
    for f in (0.8, 0.95, 1.05, 1.25):
        assert B.s_bound_outer(alpha, f * Rs) < best
    assert best == pytest.approx(B.s_max_outer(alpha), rel=1e-12)


@pytest.mark.parametrize("alpha", ALPHAS)
def test_heuristic_R_is_the_optimum_of_the_localization_budget(alpha):
    Rh = B.optimal_R_localization(alpha)
    best = B.s_bound_localization(alpha, Rh)
    for f in (0.8, 1.25):
        assert B.s_bound_localization(alpha, f * Rh) < best
    assert best == pytest.approx(B.s_max_localization(alpha), rel=1e-12)


@pytest.mark.parametrize("alpha", ALPHAS)
def test_at_the_published_point_D_S_O_bind_and_L_is_slack(alpha):
    """The whole finding in one assertion: O sets the threshold, not L."""
    status = B.Point.published(alpha).binding(tol=1e-10)
    assert status["D"] == "binds"
    assert status["S"] == "binds"
    assert status["O"] == "binds"
    assert status["L"] == "holds"
    assert status["dissipation_summable"] == "holds"


@pytest.mark.parametrize("alpha", ALPHAS)
def test_localization_slack_closed_form(alpha):
    want = (math.sqrt(2.0 * alpha / 7.0) - alpha) / 2.0
    assert B.localization_slack_at_published(alpha) == pytest.approx(want, rel=1e-10)
    assert B.localization_slack_at_published(alpha) > 0.0


def test_localization_slack_is_positive_all_the_way_to_alpha0():
    assert B.localization_slack_at_published(B.ALPHA0) == pytest.approx(0.0350242673558888, rel=1e-9)


@pytest.mark.parametrize("alpha", ALPHAS + [B.ALPHA0])
def test_implied_p_identity_holds_at_every_alpha_so_it_selects_nothing(alpha):
    """The round-1 calibration is tautological along the published family."""
    assert B.implied_p_is_tautological(alpha) == pytest.approx(0.0, abs=1e-12)


def test_heuristic_and_proof_differ_exactly_by_the_binding_swap():
    """Same D and S; replacing O by L moves the threshold from alpha_0 to 5 - 2 sqrt 6."""
    assert B.ALPHA0 == pytest.approx(0.0926655012759195, rel=1e-13)
    assert B.ALPHA_HEURISTIC == pytest.approx(0.101020514433644, rel=1e-13)
