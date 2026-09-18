"""Tests for the exponent content of the Alpoge-Buckmaster Euler force estimates (Sections 3, 6, 12)."""

from __future__ import annotations

import pytest

from nslib import ab_euler_budget as E


def test_their_own_constants_pass_their_own_targets():
    """Transcription check: (12.1)-(12.2) must satisfy (12.15) and every side condition."""
    c = E.published_check()
    assert c["passes"]
    assert c["activation"] < -6 and c["terminal"] < -6 and c["means"] < -1.5
    assert c["h_star"] > 13 / 16                       # their stated h* > 13/16


def test_the_published_design_carries_almost_no_dissipation():
    c = E.published_check()
    assert c["Q"] == 2 ** 20 + 1
    assert c["alpha_first_stage"] == pytest.approx(2.98e-8, rel=1e-2)


def test_the_quotient_table_needs_only_d_at_least_two_when_pi_is_small():
    """The (12.13) rows with no N factor are Pi^(2-d): d >= 2 is the structural minimum."""
    assert E.min_level_power(0.5, 0.01) == pytest.approx(2.0)
    assert E.quotient_rows_hold(0.125, 1e-5, 16)        # theirs


def test_the_relaxed_reading():
    r = E.RELAXED.ceiling(k_max=1)
    best = r["best"]
    assert best["k"] == 0 and best["Q"] == 51
    assert best["margin"] == pytest.approx(0.742, abs=2e-3)
    assert best["alpha"] == pytest.approx(3.64e-3, rel=5e-3)
    one = next(x for x in r["rows"] if x["k"] == 1)
    assert one["Q"] == 60 and one["alpha"] == pytest.approx(3.12e-3, rel=5e-3)


def test_the_binding_constraint_in_the_relaxed_reading_is_the_center_row():
    """Just above the maximal margin, 2 h* > beta/2 of (12.7) is the first condition to fail."""
    ok, info = E.RELAXED.margin_ok(0.741, 0, 51)
    assert ok
    ok2, info2 = E.RELAXED.margin_ok(0.745, 0, 51)
    assert not ok2
    assert 2 * info2["h_star"] - 0.745 / 2 <= 0
    assert info2["terminal"] < 0 and info2["means"] < 0


def test_every_reading_stays_more_than_ten_times_below_the_proved_threshold():
    from nslib import cascade

    proved = cascade.ALPHA0_CMZ / 2.0
    for reading in (E.RELAXED, E.OPTIMISTIC):
        best = reading.ceiling(k_max=1)["best"]
        assert proved / best["alpha"] > 12.0
    assert E.OPTIMISTIC.ceiling(k_max=0)["best"]["alpha"] == pytest.approx(3.77e-3, rel=5e-3)


def test_the_class_is_the_pendulum_class():
    """alpha <= beta/(4Q) is Theorem 3.1 with gamma = 1/2 and p = Q/beta."""
    from nslib import class_ceiling as K

    beta, Q = 0.742, 51
    assert beta / (4 * Q) == pytest.approx(K.PENDULUM.alpha_max(Q / beta))
    assert K.PENDULUM.class_ceiling == pytest.approx(0.25)
