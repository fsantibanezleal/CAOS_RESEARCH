"""Tests for the transcribed steering control and the co-rotating frame.

The normalized-model tests are the transcription check of EXP-005 gate A in unit form:
if any of them breaks, the control implemented here is not the one in the paper.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from nslib import steering as S

PAPER = S.SteeringDesign(Lam=12.0, cp=3.0, profile="sin2")
WIDE = S.SteeringDesign(Lam=2.5, cp=3.0, profile="sin2")


# ----------------------------------------------------------------- the profiles


def test_smooth_step_is_flat_at_both_ends():
    assert S.smooth_step(-1.0) == 0.0
    assert S.smooth_step(0.0) == 0.0
    assert S.smooth_step(1.0) == 1.0
    assert S.smooth_step(2.0) == 1.0
    assert 0.0 < S.smooth_step(0.5) < 1.0
    # the join must be flat to many orders, which is why it is this function
    assert S.smooth_step(1e-3) < 1e-300
    assert 1.0 - S.smooth_step(1.0 - 1e-3) < 1e-300


@pytest.mark.parametrize("profile", ["sin2", "cinf"])
def test_pulse_profiles_have_unit_mass_and_compact_support(profile):
    h = S._PROFILES[profile]
    ys = (np.arange(200000) + 0.5) / 200000.0
    mass = float(np.mean([h(float(y)) for y in ys[::100]]))
    assert mass == pytest.approx(1.0, abs=2e-3)
    assert h(-0.1) == 0.0 and h(1.1) == 0.0


def test_design_condition_matches_the_paper_inequality():
    assert PAPER.satisfies_lemma_37_condition          # 12 >= 2 * 3 * 2
    assert not WIDE.satisfies_lemma_37_condition       # 2.5 < 12, used anyway, flagged
    assert PAPER.tau_b == pytest.approx(1.0 + 1.0 / 12.0)


def test_z_is_one_before_steering_and_zero_after():
    assert PAPER.z(-1.0, 0.7) == 1.0
    assert PAPER.z(0.0, 0.7) == 1.0
    assert PAPER.z(PAPER.tau_b + 0.1, 0.7) == 0.0
    # the negative pulse is where the sign flip lives
    assert PAPER.z(1.0 + 0.5 / PAPER.Lam, 0.7) < 0.0


# ------------------------------------------------------------ the Lemma 3.7 set


def test_lemma_37_assertions_hold_on_the_admissible_design():
    rep = S.lemma_37_report(PAPER, n_mu=40)
    assert rep["P_positive_all_trials"]
    assert rep["v_bounds_on_first_part"]["holds"]
    assert rep["integral_in_log2_to_1"]
    assert rep["endpoint_map_strictly_decreasing"]
    assert rep["endpoint_positive_at_0"] > 0.0
    assert rep["endpoint_negative_at_cp"] < 0.0
    assert rep["mu_star_in_proof_interval"]
    assert rep["log_gain_in_log2_to_1_plus_inv_Lambda"]
    assert abs(rep["v_endpoint_at_mu_star"]) < 1e-10


def test_selected_pulse_zeroes_the_ratio_and_nothing_else_does():
    mu = S.select_mu(PAPER)
    assert abs(S.endpoint_v(PAPER, mu)) < 1e-9
    assert S.endpoint_v(PAPER, 0.5 * mu) > 1e-3
    assert S.endpoint_v(PAPER, 1.5 * mu) < -1e-3


def test_gain_is_retained_across_steering():
    """The point of the control: the vorticity is returned, the temperature is not."""
    mu = S.select_mu(PAPER)
    _, P, _ = S.integrate_model(PAPER, mu)
    assert P[-1] > 2.0                      # at least the log 2 of their (3.29)
    assert math.log(P[-1]) <= 1.0 + 1.0 / PAPER.Lam + 1e-9


def test_model_is_resolution_independent():
    mu = S.select_mu(PAPER)
    coarse = S.endpoint_v(PAPER, mu, n1=500, n2=500)
    fine = S.endpoint_v(PAPER, mu, n1=8000, n2=8000)
    assert abs(coarse - fine) < 1e-6


# --------------------------------------------------------- the physical staging


def _stage(mu=None, nu=0.0, alpha=1.0):
    k1, k2 = 4, 31
    lam = math.hypot(k1, k2)
    mu = S.select_mu(WIDE) if mu is None else mu
    return S.FirstStage(A=4.0, lam=lam, sin_s=k1 / lam, design=WIDE, mu=mu,
                        L_growth=5.0, nu=nu, alpha=alpha)


def test_growth_phase_reproduces_the_frozen_rate():
    """Before steering the schedule must be the EXP-002 configuration exactly."""
    st = _stage()
    assert st.Gamma == pytest.approx(math.sqrt(st.A) * st.sin_s)
    assert st.a * st.b(0.0) == pytest.approx(st.Gamma ** 2)
    assert st.rotation_angle(0.0) == pytest.approx(0.0, abs=1e-12)
    assert st.gravity(0.0) == pytest.approx((0.0, 1.0), abs=1e-12)


def test_steering_ends_with_both_phase_component_and_vorticity_at_zero():
    st = _stage()
    ts, Th, Om = st.integrate(-1e-5, st.t_b + 3.0 / st.Gamma, 2e-4)
    j = int(round(st.t_b / 2e-4))
    peak = float(np.abs(Om).max())
    assert abs(st.Z(st.t_b)) < 1e-12
    assert abs(Om[j]) / peak < 1e-3
    # and it stays there: the holding interval is stationary
    assert abs(Om[-1]) / peak < 1e-3
    assert Th[-1] == pytest.approx(Th[j], rel=1e-9)
    # the temperature gain survives the steering
    assert abs(Th[j]) > 2.0 * abs(Th[int(round(st.t1 / 2e-4))])


def test_theta_stays_negative_and_the_pulse_is_what_turns_omega():
    st = _stage()
    _, Th, Om = st.integrate(-1e-5, st.t_b, 2e-4)
    assert np.all(Th < 0.0)
    assert float(Om.min()) < 0.0            # it went negative during growth
    assert Om[-1] > Om.min()                # and was brought back up by the pulse


def test_dissipation_factorizes_out_of_the_whole_cycle():
    """The derived statement: equal damping is an exact exponential factor."""
    inv = _stage()
    vis = _stage(nu=1e-3, alpha=0.5)
    d = vis.damping
    assert d > 0.0
    t_end = inv.t_b + 2.0 / inv.Gamma
    _, Th_i, Om_i = inv.integrate(-1e-5, t_end, 2e-4)
    ts, Th_v, Om_v = vis.integrate(-1e-5, t_end, 2e-4)
    scale = np.exp(d * ts)
    assert np.allclose(Th_v * scale, Th_i, rtol=1e-8)
    assert np.allclose(Om_v * scale, Om_i, rtol=1e-8)


def test_the_selected_pulse_does_not_depend_on_viscosity():
    """Corollary of the factorization, and the reason part C reuses the inviscid root."""
    mu = S.select_mu(WIDE)
    for nu in (0.0, 1e-4, 1e-2):
        st = _stage(mu=mu, nu=nu, alpha=0.5)
        _, _, Om = st.integrate(-1e-5, st.t_b, 2e-4)
        assert abs(Om[-1]) / float(np.abs(Om).max()) < 2e-3


# ------------------------------------------------------------ the PDE machinery


def test_lab_component_of_a_rotated_direction():
    """A common rotation must move zeta_1 without moving |zeta| or J zeta . G."""
    import run_exp005 as R

    zeta = (math.sin(0.3), math.cos(0.3))
    assert R.lab_z1(zeta, 0.0) == pytest.approx(math.sin(0.3))
    assert R.lab_z1(zeta, 0.3) == pytest.approx(0.0, abs=1e-12)
    assert R.lab_z1(zeta, 0.6) == pytest.approx(-math.sin(0.3))


def _torch_or_skip():
    torch = pytest.importorskip("torch")
    return torch


def test_co_rotating_solver_reduces_to_the_base_solver_when_gravity_is_vertical():
    torch = _torch_or_skip()
    from nslib import boussinesq as B

    from nslib import corotating as CR

    grid = B.Grid(N=32, device=torch.device("cpu"), dtype=torch.float64)
    th, om = B.layered_initial_data(grid, 4.0, 1, 8, math.pi / 4, 1e-3, 1e-2)
    base = B.Boussinesq2D(grid, nu=0.0, alpha=1.0)
    rot = CR.CoRotatingBoussinesq(grid, lambda t: (0.0, 1.0), None, nu=0.0, alpha=1.0)
    t1, o1 = base.step(th, om, 1e-3)
    t2, o2 = rot.step_at(th, om, 1e-3, 0.0)
    assert torch.allclose(t1, t2, atol=1e-14)
    assert torch.allclose(o1, o2, atol=1e-14)


def test_the_background_force_holds_the_stratification_under_tilted_gravity():
    """Without the force, a tilted gravity torques the base and the test is invalid."""
    torch = _torch_or_skip()
    from nslib import boussinesq as B

    from nslib import corotating as CR

    grid = B.Grid(N=64, device=torch.device("cpu"), dtype=torch.float64)
    _, x2 = grid.coords()
    bg = torch.fft.fft2(-4.0 * torch.sin(x2))
    zero = torch.zeros_like(bg)
    tilted = CR.CoRotatingBoussinesq(grid, lambda t: (0.5, math.sqrt(0.75)), bg)
    unforced = CR.CoRotatingBoussinesq(grid, lambda t: (0.5, math.sqrt(0.75)), None)

    held_t, held_o = bg.clone(), zero.clone()
    free_t, free_o = bg.clone(), zero.clone()
    for i in range(100):
        held_t, held_o = tilted.step_at(held_t, held_o, 2e-3, i * 2e-3)
        free_t, free_o = unforced.step_at(free_t, free_o, 2e-3, i * 2e-3)
    assert float(torch.fft.ifft2(held_t - bg).real.abs().max()) < 1e-14
    assert float(torch.fft.ifft2(held_o).real.abs().max()) < 1e-14
    # The unforced background does not move in TEMPERATURE at all: the shear it spins
    # up is horizontal and the stratification is vertical, so u . grad theta vanishes
    # identically. It is the VORTICITY that runs away, and a background carrying a
    # shear is exactly what the reduction may not be handed. Asserting on theta alone
    # would be a guard that cannot see its own subject.
    assert float(torch.fft.ifft2(free_t - bg).real.abs().max()) < 1e-14
    assert float(torch.fft.ifft2(free_o).real.abs().max()) > 0.1


def test_amplitudes_are_read_back_exactly_from_a_planted_wave():
    torch = _torch_or_skip()
    from nslib import boussinesq as B

    from nslib import corotating as CR

    grid = B.Grid(N=64, device=torch.device("cpu"), dtype=torch.float64)
    x1, x2 = grid.coords()
    k = (3, 20)
    th = torch.fft.fft2(-2e-3 * torch.sin(k[0] * x1 + k[1] * x2))
    om = torch.fft.fft2(5e-2 * torch.cos(k[0] * x1 + k[1] * x2))
    Theta, Omega = CR.wave_amplitudes(th, om, k, grid, 4.0)
    assert Theta == pytest.approx(-2e-3, rel=1e-12)
    assert Omega == pytest.approx(5e-2, rel=1e-12)
