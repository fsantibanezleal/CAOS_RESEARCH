"""Tests for the class ceilings, the constant-free bound of the published paper (v0.04, Thm 3.1)."""

from __future__ import annotations

import pytest

from nslib import ab_ceiling, cascade
from nslib import class_ceiling as K


def test_the_budget_factor_is_the_growth_law():
    assert K.PENDULUM.budget_factor == pytest.approx(4.0)     # rate sqrt(A)
    assert K.STRETCHING.budget_factor == pytest.approx(2.0)   # rate A


def test_the_class_ceilings_in_both_conventions():
    assert K.PENDULUM.class_ceiling == pytest.approx(0.25)
    assert K.STRETCHING.class_ceiling == pytest.approx(0.5)
    assert K.in_their_convention(K.PENDULUM.class_ceiling) == pytest.approx(0.5)
    assert K.in_their_convention(K.STRETCHING.class_ceiling) == pytest.approx(1.0)


def test_neither_class_reaches_classical_viscosity():
    for m in K.CLASSES:
        assert not K.reaches_classical(m)
    assert K.PENDULUM.shortfall_from_classical == pytest.approx(4.0)
    assert K.STRETCHING.shortfall_from_classical == pytest.approx(2.0)


def test_the_bound_at_a_given_frequency_exponent_is_gamma_over_2p():
    assert K.PENDULUM.alpha_max(2.0) == pytest.approx(1.0 / 8.0)
    assert K.STRETCHING.alpha_max(2.0) == pytest.approx(1.0 / 4.0)
    with pytest.raises(ValueError):
        K.PENDULUM.alpha_max(1.0)             # no cascade without growing frequencies


def test_classical_viscosity_would_need_frequencies_that_do_not_grow():
    """alpha = 1 requires p = 1/(c alpha) <= 1/2 < 1 for both classes."""
    for m in K.CLASSES:
        assert K.frequency_exponent_needed_for(1.0, m) < 1.0


def test_the_design_bound_is_the_class_bound_in_other_variables():
    """Q = p delta, so alpha <= gamma/(2p) is alpha <= gamma delta/(2Q) = delta/(4Q) for gamma=1/2."""
    delta, Q = 0.2583, 120.0
    p = Q / delta
    assert K.PENDULUM.alpha_max(p) == pytest.approx(delta / (4.0 * Q))


def test_the_published_constructions_sit_below_their_own_ceilings():
    rows = {r["mechanism"]: r for r in K.summary()}
    pend, stretch = rows["Boussinesq pendulum"], rows["vortex stretching"]
    assert pend["best_published"] == pytest.approx(ab_ceiling.ceiling()[1])
    assert stretch["best_published"] == pytest.approx(cascade.ALPHA0_CMZ / 2.0)
    assert pend["published_below_own_ceiling"] == pytest.approx(464.5, rel=1e-2)
    assert stretch["published_below_own_ceiling"] == pytest.approx(10.8, rel=1e-2)
