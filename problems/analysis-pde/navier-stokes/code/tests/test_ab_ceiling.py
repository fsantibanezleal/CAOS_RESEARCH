"""Tests for the ceiling of the Alpoge-Buckmaster mechanism under dissipation.

The claim under test is ours and is about a DESIGN, not about their theorem, which is
inviscid: given their correction hierarchy, their seed rule and their ratio rule, plus the
dissipative growth condition derived in this problem, how large can the dissipation
exponent be?
"""

from __future__ import annotations

import pytest

from nslib import ab_ceiling as C
from nslib import cascade


def test_the_transcribed_design_constants():
    d = C.Design(k=1)
    assert d.levels == 10                      # their J = 2k + 8
    assert d.ratio == 120.0                    # their 120 k <= Q, at the minimum
    assert C.SEED_SLACK == 6                   # their Theta_seed = lambda^(-k-6)
    assert C.PI_OVER_Q == 5                    # their (7.4): Pi <= lambda^(5/Q)
    assert C.Design(k=3).levels == 14 and C.Design(k=3).ratio == 360.0


def test_the_margin_is_capped_and_saturates_at_one_half():
    assert C.Design(1).margin_max == pytest.approx(0.2583, abs=5e-4)
    assert C.Design(2).margin_max == pytest.approx(0.3125, abs=5e-4)
    margins = [C.Design(k).margin_max for k in (1, 2, 5, 50, 1000)]
    assert margins == sorted(margins)                      # more levels, more margin
    assert all(m < C.margin_limit() for m in margins)      # but never one half
    assert C.Design(100000).margin_max == pytest.approx(0.5, abs=1e-3)


def test_the_ceiling_is_at_one_derivative():
    best, alpha = C.ceiling()
    assert best.k == 1
    assert best.ratio == 120.0
    assert alpha == pytest.approx(5.382e-4, rel=5e-3)
    assert C.in_their_convention(alpha) == pytest.approx(1.076e-3, rel=5e-3)


def test_more_regularity_always_costs_more_than_it_gains():
    """The trade-off: margin saturates, ratio grows, so the exponent falls monotonically."""
    alphas = [C.Design(k).alpha_max for k in range(1, 40)]
    assert alphas == sorted(alphas, reverse=True)
    assert alphas[0] / alphas[-1] > 20.0


def test_the_shortfall_against_what_is_already_proved():
    _, alpha = C.ceiling()
    proved = cascade.ALPHA0_CMZ / 2.0                      # 0.0463 in our convention
    assert proved / alpha == pytest.approx(86.1, rel=2e-2)
    assert C.shortfall_against_proved(alpha) == pytest.approx(86.1, rel=2e-2)
    # and the shortfall only worsens with more regularity
    assert C.shortfall_against_proved(C.Design(10).alpha_max) > 500


def test_the_table_the_paper_quotes():
    rows = {r["k"]: r for r in C.table()}
    assert rows[1]["alpha_max_ours"] == pytest.approx(5.382e-4, rel=5e-3)
    assert rows[1]["margin_max"] == pytest.approx(0.2583, abs=5e-4)
    assert rows[1000]["alpha_max_ours"] < 2e-6
    assert rows[1000]["margin_max"] == pytest.approx(0.499, abs=2e-3)


def test_the_gap_is_structural_not_a_matter_of_constants():
    """At the proved threshold the ratio rule cannot buy even one derivative."""
    assert C.equivalent_smoothness_at_the_proved_threshold() < 1.0
    assert C.equivalent_smoothness_at_the_proved_threshold() == pytest.approx(0.0225, rel=5e-2)


def test_a_design_with_no_derivatives_controlled_is_rejected():
    with pytest.raises(ValueError):
        C.Design(k=0)
