"""Tests for the exponent content of the Alpoge-Buckmaster force estimates (their Sections 5-8).

The claim under test is about what the DESIGN's estimates can certify under dissipation, not
about their theorem, which is inviscid.
"""

from __future__ import annotations

import pytest

from nslib import ab_force_budget as F


def test_their_own_design_passes_their_own_constraints():
    """Transcription check: margin 1/8 at their ratio rule must close, at every order."""
    assert all(F.published_design_is_feasible(d) for d in range(0, 60))


def test_their_displayed_intermediate_inequalities_are_reproduced():
    """(7.25): delta <= lambda^(-3/4) needs 25/Q <= 1/8; Pi^(2d+3) <= lambda^(1/4) needs Q >= 40d+60."""
    for d in range(0, 30):
        Q = F.PUBLISHED.ratio_floor(d)
        assert 25.0 / Q <= 1.0 / 8.0
        assert F.PI_COEFF * (2 * d + 3) / Q <= 0.25
        # the leading-means bound at their margin is exactly that inequality
        b = F.PUBLISHED.margin_bounds(d, Q)
        assert b["leading_means"] >= F.PUBLISHED_MARGIN


def test_the_ratio_floor_is_the_derivative_range():
    """r_* = 9d + 41 <= Q - 1, from (7.15) and the range of Theorem 5.5."""
    assert F.RELAXED.ratio_floor(0) == 42
    assert F.RELAXED.ratio_floor(1) == 51
    assert F.PUBLISHED.ratio_floor(1) == 201
    assert F.PUBLISHED.ratio_floor(3) == 360


def test_the_remainder_constraint_saturates_the_margin_at_one_half():
    """Two levels per derivative, each gaining (1 - m): the margin falls to 1/2 as d grows.

    Without the Pi costs the bound is (d + 9)/(2d + 10), which decreases to 1/2 from above.
    """
    ms = [F.RELAXED.margin_bounds(d, 10 ** 9)["remainder"] for d in (0, 5, 50, 500, 5000)]
    assert ms == sorted(ms, reverse=True)
    assert ms[0] == pytest.approx(0.9, abs=1e-6)
    assert ms[-1] == pytest.approx(0.5, abs=1e-3)


def test_the_published_reading():
    s = {r["reading"]: r for r in F.summary()}["published"]
    assert s["best"]["d"] == 0 and s["best"]["Q"] == 201
    assert s["best"]["binding"] == "leading_means"
    assert s["best"]["alpha"] == pytest.approx(2.645e-4, rel=2e-3)
    assert s["best_alpha_theirs"] == pytest.approx(5.29e-4, rel=2e-3)
    assert s["best_times_below_proved"] == pytest.approx(175.1, rel=5e-3)
    assert s["one_derivative"]["alpha"] == pytest.approx(2.336e-4, rel=2e-3)


def test_the_relaxed_reading():
    s = {r["reading"]: r for r in F.summary()}["relaxed"]
    assert s["best"]["d"] == 0 and s["best"]["Q"] == 45
    assert s["best"]["alpha"] == pytest.approx(2.222e-3, rel=2e-3)
    assert s["best_times_below_proved"] == pytest.approx(20.8, rel=5e-3)
    assert s["one_derivative"]["Q"] == 57
    assert s["one_derivative"]["alpha"] == pytest.approx(1.827e-3, rel=2e-3)


def test_every_reading_stays_at_least_ten_times_below_the_proved_threshold():
    for s in F.summary():
        assert s["best_times_below_proved"] > 10.0
        assert s["one_derivative_times_below_proved"] > 12.0
    opt = {r["reading"]: r for r in F.summary()}["optimistic"]
    assert opt["best"]["alpha"] == pytest.approx(4.478e-3, rel=2e-3)


def test_more_regularity_never_helps():
    for arch in (F.PUBLISHED, F.RELAXED, F.OPTIMISTIC):
        rows = arch.ceiling(d_max=20)["rows"]
        alphas = [r["alpha"] for r in rows]
        assert alphas[0] == max(alphas)
        assert alphas[-1] < alphas[0] / 3


def test_the_dissipation_constraint_is_the_class_bound():
    """alpha <= m/(4Q) is Theorem 3.1 with p = Q/m and gamma = 1/2."""
    from nslib import class_ceiling as K

    m, Q = 0.4, 45
    assert F.RELAXED.alpha_max(0, Q) == pytest.approx(K.PENDULUM.alpha_max(Q / m))
