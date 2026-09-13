"""Tests for the pseudo-spectral Boussinesq solver.

These run on CPU at small N so they stay fast; the GPU path is the same code.
"""

from __future__ import annotations

import math

import pytest
import torch

from nslib import boussinesq as B


@pytest.fixture
def grid():
    return B.Grid(N=64, device=torch.device("cpu"), dtype=torch.float64)


def test_biot_savart_inverts_the_curl(grid):
    """Starting from a known streamfunction, recover u and then omega = curl u."""
    x1, x2 = grid.coords()
    psi = torch.sin(2 * x1) * torch.cos(3 * x2)
    omega = -(4 + 9) * psi                      # Laplacian psi
    solver = B.Boussinesq2D(grid)
    u1_hat, u2_hat = solver.velocity_hat(torch.fft.fft2(omega))
    u1, u2 = torch.fft.ifft2(u1_hat).real, torch.fft.ifft2(u2_hat).real
    # u = grad^perp psi = (-d_2 psi, d_1 psi)
    want1 = 3 * torch.sin(2 * x1) * torch.sin(3 * x2)
    want2 = 2 * torch.cos(2 * x1) * torch.cos(3 * x2)
    assert torch.allclose(u1, want1, atol=1e-10)
    assert torch.allclose(u2, want2, atol=1e-10)


def test_velocity_is_divergence_free(grid):
    solver = B.Boussinesq2D(grid)
    omega = torch.fft.fft2(torch.randn(grid.N, grid.N, dtype=grid.dtype))
    u1_hat, u2_hat = solver.velocity_hat(omega)
    div = 1j * solver.k1 * u1_hat + 1j * solver.k2 * u2_hat
    assert float(div.abs().max()) < 1e-9


def test_stratification_is_an_exact_steady_state(grid):
    """theta_bg = -(A0/lam0) sin(lam0 x2), omega = 0 must not move.

    d_1 theta_bg = 0, so the vorticity equation has zero right-hand side, and with
    u = 0 the temperature is not advected. This is what makes it a clean control.
    """
    solver = B.Boussinesq2D(grid, nu=0.0, alpha=1.0)
    th, om = B.layered_initial_data(grid, A0=4.0, lam0=1, lam=8, phi=math.pi / 2,
                                    Theta0=0.0, Omega0=0.0)
    th0 = th.clone()
    for _ in range(50):
        th, om = solver.step(th, om, 1e-3)
    assert float((th - th0).abs().max()) < 1e-10
    assert float(om.abs().max()) < 1e-10


def test_two_scale_vertical_background_is_steady(grid):
    """theta = -(A0/lam0) sin(lam0 x2) - (A1/lam1) sin(lam1 x2), omega = 0 is steady.

    Any function of x2 alone has d_1 theta = 0 (every mode has k1 = 0), so the vorticity
    source vanishes and, with u = 0, nothing is advected. This is what makes the
    frozen multi-scale background of EXP-004 a legitimate control: the mid-scale term
    stands in for an earlier layer's deposited gradient while the whole field stays put.
    """
    solver = B.Boussinesq2D(grid, nu=0.0, alpha=1.0)
    x1, x2 = grid.coords()
    theta = -(4.0 / 1) * torch.sin(1 * x2) - (4.0 / 8) * torch.sin(8 * x2)
    th = torch.fft.fft2(theta)
    om = torch.zeros_like(th)
    th0 = th.clone()
    for _ in range(100):
        th, om = solver.step(th, om, 1e-3)
    assert float((th - th0).abs().max()) < 1e-9
    assert float(om.abs().max()) < 1e-9
    # a term with k1 != 0 would NOT be steady, confirming the test is not vacuous
    tilted = torch.fft.fft2(theta + 0.1 * torch.sin(8 * x1))
    om2 = torch.zeros_like(tilted)
    for _ in range(20):
        tilted, om2 = solver.step(tilted, om2, 1e-3)
    assert float(om2.abs().max()) > 1e-6


def test_mode_amplitude_roundtrip(grid):
    x1, x2 = grid.coords()
    k = (5, 3)
    Theta, Omega = -0.37, 0.84
    th = torch.fft.fft2(Theta * torch.sin(k[0] * x1 + k[1] * x2))
    om = torch.fft.fft2(Omega * torch.cos(k[0] * x1 + k[1] * x2))
    assert B.mode_amplitude(th, k, grid.N, "sin") == pytest.approx(Theta, rel=1e-10)
    assert B.mode_amplitude(om, k, grid.N, "cos") == pytest.approx(Omega, rel=1e-10)


def test_mode_amplitude_rejects_unknown_kind(grid):
    with pytest.raises(ValueError):
        B.mode_amplitude(torch.zeros(grid.N, grid.N, dtype=grid.cdtype), (1, 1), grid.N, "tan")


def test_demodulate_recovers_a_constant_envelope(grid):
    """A pure mode has a flat envelope equal to half its amplitude."""
    x1, x2 = grid.coords()
    k = (7, 2)
    Theta = 0.25
    th = torch.fft.fft2(Theta * torch.sin(k[0] * x1 + k[1] * x2))
    env = B.demodulate(th, k, grid, cutoff=3.0)
    assert float(env.abs().std()) < 1e-12
    assert float(env.abs().mean()) == pytest.approx(Theta / 2.0, rel=1e-10)


def test_dissipation_decays_a_single_mode_at_the_predicted_rate(grid):
    """Pure dissipation on one mode: amplitude must fall like exp(-nu |k|^(2 alpha) t)."""
    nu, alpha = 0.05, 0.75
    solver = B.Boussinesq2D(grid, nu=nu, alpha=alpha)
    x1, x2 = grid.coords()
    k = (4, 3)
    th = torch.fft.fft2(0.1 * torch.sin(k[0] * x1 + k[1] * x2))
    om = torch.zeros_like(th)
    # Suppress the buoyancy source so only dissipation acts on theta.
    solver_no_src = B.Boussinesq2D(grid, nu=nu, alpha=alpha)
    solver_no_src.nonlinear = lambda t_hat, o_hat: (torch.zeros_like(t_hat), torch.zeros_like(o_hat))
    a0 = B.mode_amplitude(th, k, grid.N, "sin")
    t_end, dt = 0.5, 1e-3
    for _ in range(int(t_end / dt)):
        th, om = solver_no_src.step(th, om, dt)
    a1 = B.mode_amplitude(th, k, grid.N, "sin")
    rate = -math.log(a1 / a0) / t_end
    assert rate == pytest.approx(nu * (k[0] ** 2 + k[1] ** 2) ** alpha, rel=1e-8)
    _ = solver


def test_realized_wavevector_is_the_nearest_integer_mode():
    k = B.realized_wavevector(40, math.pi / 2)
    assert k == (40, 0)
    z1, z2, norm = B.realized_zeta(40, math.pi / 2)
    assert z1 == pytest.approx(1.0)
    assert z2 == pytest.approx(0.0)
    assert norm == pytest.approx(40.0)


def test_realized_zeta_is_a_unit_vector():
    for lam in (10, 40, 97):
        for phi in (0.4, 1.0, 2.2):
            z1, z2, norm = B.realized_zeta(lam, phi)
            assert math.hypot(z1, z2) == pytest.approx(1.0, rel=1e-12)
            assert norm > 0


def test_dealias_mask_removes_the_top_third(grid):
    mask = grid.dealias_mask()
    frac = float(mask.to(torch.float64).mean())
    assert 0.4 < frac < 0.5        # (2/3)^2 of the modes survive, about 0.44
