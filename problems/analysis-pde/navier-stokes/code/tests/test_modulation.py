"""Tests for the amplitude system and its dissipative extension."""

from __future__ import annotations

import math

import numpy as np
import pytest

from nslib import cascade, modulation as M


def test_growth_rate_is_sqrtA_times_sin_phi_not_sqrt_of_the_product():
    """Settle the mangled-radical ambiguity in the source PDF by computation.

    `pdftotext` floats the radical onto its own line, so "sqrt(A) sin(phi)" and
    "sqrt(A sin(phi))" are indistinguishable in the extracted text. The matrix
    decides: the product of the off-diagonal entries is A sin^2(phi).
    """
    rng = np.random.default_rng(20260912)
    for _ in range(25):
        A = float(rng.uniform(0.5, 40.0))
        phi = float(rng.uniform(0.2, math.pi - 0.2))
        lam = float(rng.uniform(1.0, 500.0))
        r = float(rng.uniform(0.5, 2.0))
        zeta = r * M.rot(phi)
        got = M.growth_rate(zeta, -A * np.array([0.0, 1.0]), lam)
        assert got == pytest.approx(math.sqrt(A) * math.sin(phi), rel=1e-10)
        wrong = math.sqrt(A * math.sin(phi))
        if abs(math.sin(phi) - 1.0) > 1e-3 and abs(A - 1.0) > 1e-3:
            assert abs(got - wrong) > 1e-6


def test_growth_rate_is_independent_of_lambda():
    """Frequency buys gradient, not growth. This is the load-bearing fact."""
    A, phi, r = 9.0, 1.1, 1.0
    zeta, G = r * M.rot(phi), -A * np.array([0.0, 1.0])
    rates = [M.growth_rate(zeta, G, lam) for lam in (1.0, 10.0, 1e3, 1e5, 1e8)]
    assert max(rates) - min(rates) < 1e-8


def test_growing_eigenline_matches_the_printed_one():
    """The paper prints Omega = (lambda r / sqrt(A)) Theta on the growing line."""
    A, phi, lam, r = 4.0, 0.9, 7.0, 1.3
    zeta = r * M.rot(phi)
    v = M.growing_eigenvector(zeta, -A * np.array([0.0, 1.0]), lam)
    assert v[0] != 0.0
    assert v[1] / v[0] == pytest.approx(lam * r / math.sqrt(A), rel=1e-10)


def test_integration_reproduces_the_closed_form_rate():
    """RK4 on the full system must match the eigenvalue over a finite window."""
    A, phi, lam, r, t = 6.0, 1.0, 30.0, 1.0, 0.7
    zeta = r * M.rot(phi)
    bg = M.Background(D=np.zeros((2, 2)), G=-A * np.array([0.0, 1.0]))
    v = M.growing_eigenvector(zeta, bg.G, lam)
    y0 = np.concatenate([zeta, v])
    y1 = M.integrate(y0, bg, lam, t_end=t, steps=8000)
    measured = math.log(np.linalg.norm(y1[2:]) / np.linalg.norm(y0[2:])) / t
    assert measured == pytest.approx(math.sqrt(A) * math.sin(phi), rel=1e-6)


def test_self_advection_cancels_on_the_grid():
    """v . grad(wave) = 0 exactly: v is perpendicular to zeta, gradients parallel.

    This is the geometric identity that makes the ansatz exact rather than
    asymptotic, so it is worth checking on real fields and not only on paper.
    """
    n = 256
    x = np.arange(n) * 2.0 * np.pi / n
    X1, X2 = np.meshgrid(x, x, indexing="ij")
    lam, phi, r = 8.0, 1.0, 1.0
    zeta = r * M.rot(phi)
    s = lam * (zeta[0] * X1 + zeta[1] * X2)
    Theta, Omega = -0.3, -0.7
    vartheta = Theta * np.sin(s)
    # v = Omega / (lam |zeta|^2) * J zeta * sin s
    Jz = M.J(zeta)
    coef = Omega / (lam * float(zeta @ zeta))
    v1, v2 = coef * Jz[0] * np.sin(s), coef * Jz[1] * np.sin(s)
    # grad vartheta = Theta cos(s) * lam * zeta
    g1 = Theta * np.cos(s) * lam * zeta[0]
    g2 = Theta * np.cos(s) * lam * zeta[1]
    adv = v1 * g1 + v2 * g2
    scale = float(np.abs(v1 * g1).max() + np.abs(v2 * g2).max())
    assert float(np.abs(adv).max()) <= 1e-12 * max(scale, 1.0)


def test_gradient_identity_small_amplitude_large_gradient():
    """grad(wave)(0) = lambda Theta zeta: the amplification identity."""
    zeta = M.rot(0.8)
    for lam in (10.0, 100.0, 1000.0):
        g = M.gradient_at_origin(1e-3, zeta, lam)
        assert np.linalg.norm(g) == pytest.approx(lam * 1e-3, rel=1e-12)


# ------------------------------------------------------------- dissipative part


@pytest.mark.parametrize("alpha", [0.05, 0.1, 0.25, 0.5, 1.0])
def test_dissipative_eigenvalue_closed_form(alpha):
    A, phi, lam, r, nu = 9.0, 1.1, 7.0, 1.0, 1e-3
    zeta = r * M.rot(phi)
    got = M.growth_rate(zeta, -A * np.array([0.0, 1.0]), lam, nu=nu, alpha=alpha)
    want = math.sqrt(A) * math.sin(phi) - nu * (lam * r) ** (2 * alpha)
    assert got == pytest.approx(want, abs=1e-12)


def test_frequency_cap_is_the_zero_of_the_growth_rate():
    A, phi, nu, alpha, r = 9.0, 1.2, 1e-2, 0.3, 1.0
    cap = M.frequency_cap(A, phi, nu, alpha, r)
    assert M.frozen_growth_rate(A, phi, cap, r, nu, alpha) == pytest.approx(0.0, abs=1e-9)
    assert M.frozen_growth_rate(A, phi, cap * 0.99, r, nu, alpha) > 0.0
    assert M.frozen_growth_rate(A, phi, cap * 1.01, r, nu, alpha) < 0.0


def test_frequency_cap_infinite_without_dissipation():
    assert M.frequency_cap(1.0, 1.0, 0.0, 1.0) == math.inf


def test_convention_conversion_roundtrip():
    for a in (0.01, 0.0463, 0.25, 1.0):
        assert M.alpha_cmz_to_ours(M.alpha_ours_to_cmz(a)) == pytest.approx(a)
    # classical viscosity is alpha = 1 for us and alpha = 2 for Cordoba-Martinez-Zoroa-Zheng
    assert M.alpha_ours_to_cmz(1.0) == pytest.approx(2.0)


# --------------------------------------------------------------- the calibration


def test_published_threshold_corresponds_to_a_clean_frequency_exponent():
    """alpha_c = 1/(4p) sends the published threshold to p = 11/4 + sqrt(7) exactly.

    Cordoba, Martinez-Zoroa and Zheng prove blowup for every |grad|^alpha exponent
    below alpha_0 = (22 - 8 sqrt 7)/9. Inverting the cascade relation:

        p = 1 / (2 alpha_0) = 9 / (2 (22 - 8 sqrt 7))
          = 9 (22 + 8 sqrt 7) / (2 * 36) = (22 + 8 sqrt 7) / 8 = 11/4 + sqrt 7.

    A consistency statement, not a derivation: any threshold corresponds to some p.
    What is not generic is that this p is a clean algebraic number.
    """
    p = cascade.implied_p(cascade.ALPHA0_CMZ)
    assert p == pytest.approx(11.0 / 4.0 + math.sqrt(7.0), rel=1e-13)
    # and the relation inverts
    assert cascade.alpha_c(p) == pytest.approx(M.ALPHA0_OURS, rel=1e-13)
    # the rationalization used in the docstring is exact
    assert 9.0 * (22.0 + 8.0 * math.sqrt(7.0)) / (2.0 * 36.0) == pytest.approx(p, rel=1e-13)


def test_alpha0_constants_agree_across_modules():
    assert cascade.ALPHA0_CMZ == pytest.approx(M.ALPHA0_CMZ, rel=1e-15)
    assert M.ALPHA0_OURS == pytest.approx(M.ALPHA0_CMZ / 2.0, rel=1e-15)
    assert cascade.P_STAR == pytest.approx(cascade.implied_p(), rel=1e-13)
