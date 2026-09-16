"""Repository-level guard for the smoothness-versus-dissipation trade-off (NS-017).

The claim under test is ours, not the authors': applying the dissipative extension of the
Alpoge-Buckmaster modulation system (derived in this problem, checked against the PDE by
EXP-002) to their PUBLISHED inviscid schedule. Their theorem is inviscid and nothing here
contradicts it.

Numpy-free and torch-free on purpose, so it runs in the CI lane.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "problems/analysis-pde/navier-stokes/code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from nslib import ab_schedule as A  # noqa: E402
from nslib import cascade as C  # noqa: E402


def test_the_transcribed_constants():
    """Their (3.7) and (3.8): Q_q = Q* + q with Q* >= 200, and the margin delta = 1/8."""
    s = A.ABSchedule()
    assert s.Q_star >= 200
    assert s.Q(1) == s.Q_star + 1 and s.Q(7) == s.Q_star + 7
    assert s.delta == pytest.approx(0.125)
    # |Theta_seed| e^(L_q) = lambda^(-7/8), so the deposited gradient is lambda^(1/8)
    assert 1.0 - 0.875 == pytest.approx(s.delta)


def test_the_trade_off_is_our_own_cascade_constraint_in_their_variables():
    s = A.ABSchedule()
    assert s.p(3) == pytest.approx(s.Q(3) / s.delta)
    assert C.alpha_c(s.p(3)) == pytest.approx(s.alpha_max(3))
    assert A.alpha_max_general(1.0, 1.0) == pytest.approx(0.25)  # our cap is the corner


def test_no_positive_exponent_survives_their_unbounded_ratio():
    """The load-bearing statement: Q_q grows, so the admissible alpha goes to zero."""
    s = A.ABSchedule()
    assert s.alpha_max(1) > s.alpha_max(100) > s.alpha_max(10_000)
    for epsilon in (1e-6, 1e-9, 1e-12):
        assert A.smooth_forcing_is_incompatible_with_dissipation(s, epsilon)
    assert s.stall_stage(1e-9) is not None


def test_the_published_numbers_quoted_in_the_dossier():
    s = A.ABSchedule()
    assert s.alpha_max(1) == pytest.approx(1.5547e-4, rel=1e-3)
    assert s.alpha_max(2, favourable_angle=False) == pytest.approx(7.6967e-7, rel=1e-3)
    assert s.stall_stage(1e-4) == 113
    published_cmz_ours = C.ALPHA0_CMZ / 2.0
    assert A.ratio_needed_for(published_cmz_ours) < 1.0
    assert A.derivatives_affordable(published_cmz_ours) < 0.01


def test_the_prediction_is_stated_with_a_falsification_criterion():
    """A prediction without a way to be wrong is not a prediction (methodology 02)."""
    dossier = (ROOT / "problems/analysis-pde/navier-stokes/context"
               / "2026-09-16-smoothness-versus-dissipation.md").read_text(encoding="utf-8")
    assert "**Prediction.**" in dossier
    assert "**Falsification.**" in dossier
    assert "UNVERIFIED" in dossier
