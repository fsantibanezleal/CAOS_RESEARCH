"""EXP-005: the steered growth, steering and hold cycle, in the ODE and in the PDE.

Hypothesis committed before the run:
`../experiments/EXP-005-steered-cycle/hypothesis.md`.

Four parts:

A  transcription. Every assertion of Alpoge-Buckmaster Lemma 3.7 checked numerically on
   the paper-admissible design, and the root reported for the wider design the PDE run
   needs.
B  the inviscid steered cycle in the full nonlinear PDE, in the co-rotating frame, with
   the endpoint map and two negative controls.
C  the dissipative cycle, testing the factorization `(Theta, Omega) = e^(-d t) (inviscid)`
   derived in `nslib.steering`.
D  the dynamical two-layer handoff: layer 1 grown and STEERED to rest, then layer 2 grown
   on the gradient it deposited. This is the run EXP-004 Part A could not do.

Usage:
    python run_exp005.py --part A
    python run_exp005.py --part B --n 512
    python run_exp005.py --part C --n 512
    python run_exp005.py --part D --n 1024
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import torch

from nslib import boussinesq as B
from nslib import corotating as CR
from nslib import steering as S
from run_exp004 import low_pass_gradient, stats


# ------------------------------------------------------------------- utilities


def lab_z1(zeta: tuple[float, float], rotation: float) -> float:
    """Laboratory component `zeta_1` of a co-rotating direction.

    The laboratory frame is reached by rotating by `alpha`, so the laboratory `e_1` is
    `(cos alpha, -sin alpha)` in co-rotating coordinates. Reading `zeta[0]` instead
    would silently measure the wrong angle once the frame has turned, which is the whole
    point of the steering.
    """
    return zeta[0] * math.cos(rotation) - zeta[1] * math.sin(rotation)


def predicted_rate_rotated(g1, g2, zeta, rotation: float):
    """`sigma(x) = sqrt(max(0, -zeta_1^lab (J zeta . G)))`, gradients in co-rotating axes.

    `J zeta . G` is rotation invariant, so it is evaluated in the frame the fields live
    in; only the laboratory component of `zeta` feels the rotation.
    """
    z1, z2 = zeta
    jz_dot_g = -z2 * g1 + z1 * g2
    return torch.sqrt(torch.clamp(-lab_z1(zeta, rotation) * jz_dot_g, min=0.0))


def background(args, x2):
    """The prescribed stratification, and the gradient magnitude it has AT THE ORIGIN.

    `sine` is the Alpoge-Buckmaster stratification with the cutoff dropped, as used by
    EXP-002 and EXP-004: `theta = -(A/lam0) sin(lam0 x2)`, whose gradient is `-A` at the
    origin but falls off like `cos(lam0 x2)`.

    `flattened` subtracts an eighth of the second harmonic,
    `theta = -(A/lam0) (sin(lam0 x2) - (1/8) sin(2 lam0 x2))`, which cancels the
    quadratic term of the gradient and leaves it constant to fourth order, at three
    quarters of `A`. Both are functions of `x2` alone, so both are exact steady states of
    the unforced system with vertical gravity.

    This matters because the modulation reduction assumes the layer sits on an AFFINE
    background, which the construction arranges by localizing each layer on a scale where
    that is true. On a torus the background must curve somewhere, and the curvature it has
    over the layer's support is the leading error of the whole comparison. Running both
    profiles measures that error instead of asserting it.
    """
    if args.background == "sine":
        return -(args.A0 / args.lam0) * torch.sin(args.lam0 * x2), args.A0
    if args.background == "flattened":
        field = -(args.A0 / args.lam0) * (torch.sin(args.lam0 * x2)
                                          - 0.125 * torch.sin(2.0 * args.lam0 * x2))
        return field, 0.75 * args.A0
    raise SystemExit(f"unknown background {args.background}")


def parasite_level(theta_hat, k, grid, base_max: float) -> dict:
    """How much of the field is NOT the layer and NOT the prescribed background.

    The background this construction grows on is Rayleigh-Taylor unstable at rate
    `sqrt(A)`, while the steered layer only grows at `sqrt(A) sin s`. Every mode at a
    more favourable angle therefore outruns the layer by a factor `1/sin s` in the
    exponent, starting from round-off. On a torus with no localization and no force
    other than the one holding the base, those parasites eventually dominate, and a run
    that does not watch for them reports their growth as the layer's. Two readings:

      `horizontal_max`  the largest amplitude among the modes (k_1 + d, k_2), which is
                        where the fast angles live and where the layer puts nothing;
      `field_excess`    max |theta| divided by the background's own maximum, which is 1
                        while the run is still about the layer.
    """
    n = grid.N
    hor = max(abs(B.mode_amplitude(theta_hat, (k[0] + d, k[1]), n, "sin"))
              for d in range(-8, 9) if d != 0)
    return {"horizontal_max": hor,
            "field_excess": float(torch.fft.ifft2(theta_hat).real.abs().max()) / base_max}


def march(solver, th, om, dt, n_steps, t0=0.0):
    t = t0
    for _ in range(n_steps):
        th, om = solver.step_at(th, om, dt, t)
        t += dt
    return th, om, t


def run_cycle(args, stage, mu, grid, dev, nu=0.0, alpha=1.0, dt=None, samples=400,
              t_end=None):
    """March the PDE through growth, steering and hold, sampling the amplitude pair.

    Returns the sampled series plus the ODE reference integrated with the same schedule.
    """
    dt = dt or args.dt
    stage = S.FirstStage(A=stage.A, lam=stage.lam, sin_s=stage.sin_s, design=stage.design,
                         mu=mu, L_growth=stage.L_growth, nu=nu, alpha=alpha)
    t_end = t_end if t_end is not None else stage.t_b + args.hold / stage.Gamma
    n_steps = int(round(t_end / dt))

    x1, x2 = grid.coords()
    k = (args.k1, args.k2)
    theta_bg, _ = background(args, x2)
    theta_bg_hat = torch.fft.fft2(theta_bg)
    Theta0, Omega0 = stage.eigen_seed(args.Theta0)
    th = theta_bg_hat + torch.fft.fft2(Theta0 * torch.sin(k[0] * x1 + k[1] * x2))
    om = torch.fft.fft2(Omega0 * torch.cos(k[0] * x1 + k[1] * x2))

    solver = CR.CoRotatingBoussinesq(grid, stage.gravity, theta_bg_hat, nu=nu, alpha=alpha)

    # Guard: the force must actually hold the background. With the wave absent nothing
    # may move at all, however far gravity has turned. The VORTICITY is the load-bearing
    # half of this check: a tilted gravity torques the stratification, and the shear it
    # would spin up leaves the temperature field untouched (the shear is horizontal, the
    # stratification vertical), so a temperature-only guard cannot see the failure it is
    # there to catch.
    thp, omp = theta_bg_hat.clone(), torch.zeros_like(theta_bg_hat)
    thp, omp, _ = march(solver, thp, omp, dt, 200, t0=stage.t1)
    bg_drift = float(torch.fft.ifft2(thp - theta_bg_hat).real.abs().max())
    bg_vorticity = float(torch.fft.ifft2(omp).real.abs().max())

    every = max(1, n_steps // samples)
    # The comparison is made at t_1 and t_b, so those two instants are sampled exactly,
    # whatever the sampling stride is. Reading the nearest grid sample instead charges the
    # reduction for the sampler: at a growth rate near 1, one stride is already percents.
    pinned = {int(round(stage.t1 / dt)), int(round(stage.t_b / dt))}
    ts, Th, Om, par = [], [], [], []
    base_max = float(torch.fft.ifft2(theta_bg_hat).real.abs().max())
    t = 0.0
    for step in range(n_steps + 1):
        if step % every == 0 or step == n_steps or step in pinned:
            a, b = CR.wave_amplitudes(th, om, k, grid, args.cutoff)
            ts.append(t)
            Th.append(a)
            Om.append(b)
            par.append(parasite_level(th, k, grid, base_max))
        if step < n_steps:
            th, om = solver.step_at(th, om, dt, t)
            t += dt
    return {"stage": stage, "t": ts, "Theta": Th, "Omega": Om, "parasite": par,
            "bg_drift": bg_drift, "bg_vorticity": bg_vorticity,
            "theta_hat": th, "omega_hat": om, "t_end": t}


def cycle_metrics(run, args, nu=0.0, alpha=1.0):
    """Landing, gain and hold diagnostics, PDE against the ODE with the same schedule."""
    stage = run["stage"]
    ts = run["t"]
    Th = run["Theta"]
    Om = run["Omega"]
    i_b = min(range(len(ts)), key=lambda i: abs(ts[i] - stage.t_b))
    i_1 = min(range(len(ts)), key=lambda i: abs(ts[i] - stage.t1))
    peak = max(abs(v) for v in Om)
    landing = abs(Om[i_b]) / peak

    ode_t, ode_Th, ode_Om = stage.integrate(args.Theta0, ts[-1], args.dt_ode)
    # Index the ODE at the times the PDE was actually SAMPLED at, not at the nominal
    # t_1 and t_b. The sampler lands on a grid of spacing t_end/samples, and at a growth
    # rate near 1 a single sample of offset is already a percent of amplitude: comparing
    # a sampled PDE value against an ODE value at a different instant charges the
    # reduction for the sampling grid. This showed up as a spurious dt-refinement shift,
    # since halving dt also changed which instants were sampled.
    j_b = min(int(round(ts[i_b] / args.dt_ode)), len(ode_Th) - 1)
    j_1 = min(int(round(ts[i_1] / args.dt_ode)), len(ode_Th) - 1)
    ode_peak = float(abs(ode_Om).max())
    ode_landing = abs(float(ode_Om[j_b])) / ode_peak

    gain_pde = Th[i_b] / Th[i_1]
    gain_ode = float(ode_Th[j_b] / ode_Th[j_1])

    # hold: from t_b to the end
    hold = [i for i in range(len(ts)) if ts[i] >= stage.t_b]
    hold_theta_drift = (max(abs(Th[i]) for i in hold) / min(abs(Th[i]) for i in hold)) - 1.0
    hold_omega_max = max(abs(Om[i]) for i in hold) / peak
    if any(Th[i] * Th[0] <= 0.0 for i in hold):
        hold_decay_rate = float("nan")            # the amplitude changed sign: not a decay
    elif stage.damping > 0.0:
        # expected decay over the hold, e^(-d T)
        dT = ts[hold[-1]] - ts[hold[0]]
        measured = math.log(abs(Th[hold[0]]) / abs(Th[hold[-1]]))
        hold_decay_rate = measured / dT
    else:
        hold_decay_rate = -math.log(abs(Th[hold[-1]]) / abs(Th[hold[0]])) / (
            ts[hold[-1]] - ts[hold[0]])

    return {
        "t_b": stage.t_b,
        "Gamma": stage.Gamma,
        "damping": stage.damping,
        "background_drift_under_rotating_gravity": run["bg_drift"],
        "background_vorticity_under_rotating_gravity": run["bg_vorticity"],
        "landing_pde": landing,
        "landing_ode": ode_landing,
        "gain_across_steering_pde": gain_pde,
        "gain_across_steering_ode": gain_ode,
        "gain_relative_error": abs(gain_pde - gain_ode) / abs(gain_ode),
        "Theta_at_t1_pde": Th[i_1],
        "Theta_at_tb_pde": Th[i_b],
        "Theta_at_tb_ode": float(ode_Th[j_b]),
        "Theta_absolute_ratio_pde_over_ode": Th[i_b] / float(ode_Th[j_b]),
        "hold_theta_relative_drift": hold_theta_drift,
        "hold_omega_over_peak": hold_omega_max,
        "hold_decay_rate": hold_decay_rate,
        "parasite_horizontal_at_tb": run["parasite"][i_b]["horizontal_max"],
        "parasite_over_wave_at_tb": (run["parasite"][i_b]["horizontal_max"]
                                     / max(abs(Th[i_b]), 1e-300)),
        "field_excess_at_tb": run["parasite"][i_b]["field_excess"],
        "field_excess_at_end": run["parasite"][-1]["field_excess"],
        "ratio_v_pde": (Om[i_b] / Th[i_b]) * stage.sigma / stage.lam,
        "ratio_v_ode": float(ode_Om[j_b] / ode_Th[j_b]) * stage.sigma / stage.lam,
    }


def build_stage(args, mu):
    knorm = math.hypot(args.k1, args.k2)
    design = S.SteeringDesign(Lam=args.Lambda, cp=args.cp, profile=args.profile)
    _, A_origin = background(args, torch.zeros(1))
    return S.FirstStage(A=A_origin, lam=knorm, sin_s=args.k1 / knorm, design=design,
                        mu=mu, L_growth=args.L_growth)


# ----------------------------------------------------------------------- parts


def part_a(args) -> dict:
    """Gate A: the transcription of Lemma 3.7."""
    paper = S.SteeringDesign(Lam=12.0, cp=args.cp, profile="sin2")
    used = S.SteeringDesign(Lam=args.Lambda, cp=args.cp, profile=args.profile)
    rep_paper = S.lemma_37_report(paper, n_mu=args.n_mu)
    rep_used = S.lemma_37_report(used, n_mu=args.n_mu)
    keys = ["P_positive_all_trials", "integral_in_log2_to_1",
            "endpoint_map_strictly_decreasing", "mu_star_in_proof_interval",
            "log_gain_in_log2_to_1_plus_inv_Lambda"]
    ok = (rep_paper["satisfies_lemma_37_condition"]
          and all(bool(rep_paper[k]) for k in keys)
          and rep_paper["v_bounds_on_first_part"]["holds"]
          and abs(rep_paper["v_endpoint_at_mu_star"]) < 1e-10)
    return {"part": "A", "paper_admissible_design": rep_paper, "design_used_in_pde": rep_used,
            "gates": {"A_transcription": bool(ok)}}


def part_b(args, grid, dev) -> dict:
    """Gate B: the inviscid steered cycle in the PDE, with the endpoint map."""
    t0 = time.time()
    design = S.SteeringDesign(Lam=args.Lambda, cp=args.cp, profile=args.profile)
    mu_star = S.select_mu(design)
    stage = build_stage(args, mu_star)

    main = run_cycle(args, stage, mu_star, grid, dev)
    m_main = cycle_metrics(main, args)

    endpoint = {}
    for name, mu in (("mu_0", 0.0), ("mu_star", mu_star), ("mu_2star", 2.0 * mu_star)):
        if name == "mu_star":
            endpoint[name] = {"mu": mu, "landing_pde": m_main["landing_pde"],
                              "landing_ode": m_main["landing_ode"]}
            continue
        r = run_cycle(args, stage, mu, grid, dev, samples=200)
        m = cycle_metrics(r, args)
        endpoint[name] = {"mu": mu, "landing_pde": m["landing_pde"],
                          "landing_ode": m["landing_ode"]}
    endpoint_max_gap = max(abs(v["landing_pde"] - v["landing_ode"]) for v in endpoint.values())

    # numerical control: halve dt
    half = run_cycle(args, stage, mu_star, grid, dev, dt=args.dt / 2.0, samples=200)
    m_half = cycle_metrics(half, args)
    dt_shift = abs(m_half["gain_across_steering_pde"] - m_main["gain_across_steering_pde"]) / abs(
        m_main["gain_across_steering_pde"])

    # negative control: no steering at all, gravity frozen at the growth direction
    t_end_main = stage.t_b + args.hold / stage.Gamma
    frozen = S.FirstStage(A=stage.A, lam=stage.lam, sin_s=stage.sin_s, design=design,
                          mu=mu_star, L_growth=stage.L_growth * 1e3)  # Z stays sin s
    nc = run_cycle(args, frozen, mu_star, grid, dev, samples=200, t_end=t_end_main)
    nc_landing = abs(nc["Omega"][-1]) / max(abs(v) for v in nc["Omega"])

    return {
        "part": "B",
        "wall_seconds": round(time.time() - t0, 1),
        "mu_star": mu_star,
        "design": {"Lambda": args.Lambda, "cp": args.cp, "profile": args.profile,
                   "satisfies_lemma_37_condition": design.satisfies_lemma_37_condition},
        "wave": {"k": [args.k1, args.k2], "lambda": stage.lam, "sin_s": stage.sin_s,
                 "Gamma": stage.Gamma, "a": stage.a},
        "main": m_main,
        "endpoint_map": endpoint,
        "endpoint_max_gap": endpoint_max_gap,
        "dt_half_relative_shift_of_gain": dt_shift,
        "negative_control_no_steering_landing": nc_landing,
        "gates": {
            "B1_landing": bool(m_main["landing_pde"] < 2e-2),
            "B1_gain": bool(m_main["gain_relative_error"] < 2e-2),
            "B2_endpoint_map": bool(endpoint_max_gap < 2e-2),
            "B3_hold": bool(m_main["hold_theta_relative_drift"] < 1e-2
                            and m_main["hold_omega_over_peak"] < 3e-2),
            "B4_dt": bool(dt_shift < 1e-3),
            "B5_no_parasite_takeover": bool(m_main["parasite_over_wave_at_tb"] < 1e-2
                                            and m_main["field_excess_at_end"] < 1.05),
            "controls_fail_as_required": bool(endpoint["mu_0"]["landing_pde"] > 0.2
                                              and nc_landing > 0.2),
        },
    }


def part_c(args, grid, dev) -> dict:
    """Gate C: the dissipative cycle and the damping factorization."""
    t0 = time.time()
    design = S.SteeringDesign(Lam=args.Lambda, cp=args.cp, profile=args.profile)
    mu_star = S.select_mu(design)
    stage = build_stage(args, mu_star)
    d_target = args.damping_fraction * stage.Gamma
    nu = d_target / stage.lam ** (2.0 * args.alpha)

    inviscid = run_cycle(args, stage, mu_star, grid, dev)
    viscous = run_cycle(args, stage, mu_star, grid, dev, nu=nu, alpha=args.alpha)
    m_v = cycle_metrics(viscous, args, nu=nu, alpha=args.alpha)

    d = nu * stage.lam ** (2.0 * args.alpha)
    # factorization: e^(d t) * viscous should reproduce the inviscid run
    worst = 0.0
    for t, a_inv, a_vis in zip(inviscid["t"], inviscid["Theta"], viscous["Theta"]):
        if abs(a_inv) < 1e-300:
            continue
        rel = abs(a_vis * math.exp(d * t) - a_inv) / abs(a_inv)
        worst = max(worst, rel)

    return {
        "part": "C",
        "wall_seconds": round(time.time() - t0, 1),
        "nu": nu,
        "alpha": args.alpha,
        "damping_d": d,
        "damping_over_Gamma": d / stage.Gamma,
        "viscous": m_v,
        "hold_decay_rate_measured": m_v["hold_decay_rate"],
        "hold_decay_rate_relative_error": abs(m_v["hold_decay_rate"] - d) / d,
        "factorization_worst_relative_error": worst,
        "gates": {
            "C1_landing_with_inviscid_mu": bool(m_v["landing_pde"] < 2e-2),
            "C2_hold_decay": bool(abs(m_v["hold_decay_rate"] - d) / d < 2e-2),
            "C3_factorization": bool(worst < 2e-2),
        },
    }


def part_d(args, grid, dev) -> dict:
    """Gate D: the dynamical handoff, layer 1 STEERED to rest before layer 2 grows."""
    t0 = time.time()
    design = S.SteeringDesign(Lam=args.Lambda, cp=args.cp, profile=args.profile)
    mu_star = S.select_mu(design)
    stage = build_stage(args, mu_star)

    # Stage 1, seeded so the deposit at the hold is comparable with the base gradient.
    args_big = argparse.Namespace(**vars(args))
    args_big.Theta0 = args.Theta0_D
    run1 = run_cycle(args_big, stage, mu_star, grid, dev)
    m1 = cycle_metrics(run1, args_big)
    Theta1 = run1["Theta"][min(range(len(run1["t"])),
                               key=lambda i: abs(run1["t"][i] - stage.t_b))]
    deposit = abs(Theta1) * stage.lam

    th, om = run1["theta_hat"], run1["omega_hat"]
    t_now = run1["t_end"]
    rotation = stage.rotation_angle(t_now)          # frozen at s during the hold
    solver = CR.CoRotatingBoussinesq(
        grid, stage.gravity, torch.fft.fft2(background(args, grid.coords()[1])[0]),
        nu=0.0, alpha=1.0)

    # Layer 2, injected into the holding interval at a laboratory angle phi2.
    x1, x2 = grid.coords()
    phi_rot = args.phi2 + rotation                  # co-rotating angle of layer 2
    k2 = (int(round(args.lam2 * math.sin(phi_rot))), int(round(args.lam2 * math.cos(phi_rot))))
    kn2 = math.hypot(*k2)
    zeta2 = (k2[0] / kn2, k2[1] / kn2)
    A_local = stage.A + deposit
    Omega2 = kn2 * args.Theta2 / math.sqrt(max(A_local, 1e-12))
    th = th + torch.fft.fft2(args.Theta2 * torch.sin(k2[0] * x1 + k2[1] * x2))
    om = om + torch.fft.fft2(Omega2 * torch.cos(k2[0] * x1 + k2[1] * x2))

    cutoff = math.sqrt(stage.lam * kn2)
    g1, g2 = low_pass_gradient(th, grid, cutoff)
    pred_full = predicted_rate_rotated(g1, g2, zeta2, rotation)
    base_hat = torch.fft.fft2(background(args, x2)[0])
    b1, b2 = low_pass_gradient(base_hat, grid, cutoff)
    pred_base = predicted_rate_rotated(b1, b2, zeta2, rotation)

    # local rate field of layer 2, after a settling interval
    n_meas = int(round(args.measure2 / args.dt))
    n_settle = int(round(args.settle2 / args.dt))
    th, om, t_now = march(solver, th, om, args.dt, n_settle, t0=t_now)
    times, profs = [], []
    every = max(1, n_meas // 30)
    for step in range(n_meas + 1):
        if step % every == 0:
            times.append(t_now)
            profs.append(B.demodulate(th, k2, grid, 1.5 * stage.lam).abs().clone())
        if step < n_meas:
            th, om, t_now = march(solver, th, om, args.dt, 1, t0=t_now)
    T = torch.tensor(times, dtype=grid.dtype, device=grid.device)
    Y = torch.log(torch.stack(profs).clamp_min(1e-300))
    Tc = T - T.mean()
    measured = (Tc[:, None, None] * (Y - Y.mean(dim=0, keepdim=True))).sum(dim=0) / (Tc * Tc).sum()

    frac = args.mask_frac
    mask = (pred_full > frac * float(pred_full.max())) & (pred_base > frac * float(pred_base.max()))
    full = stats(measured, pred_full, mask)
    base = stats(measured, pred_base, mask)

    return {
        "part": "D",
        "wall_seconds": round(time.time() - t0, 1),
        "stage1": m1 | {"Theta_at_hold": Theta1, "deposit_lambda_Theta": deposit,
                        "deposit_over_A0": deposit / args.A0},
        "layer2": {"k": list(k2), "lambda": kn2, "phi2_lab": args.phi2,
                   "rotation_at_hold": rotation, "cutoff": cutoff,
                   "n_masked_points": int(mask.sum())},
        "H1_total_gradient": full,
        "H2_control_base_only": base,
        "gates": {
            "D0_stage1_landing": bool(m1["landing_pde"] < 5e-2),
            "D1_pattern": bool(full["corr"] > 0.9),
            "D2_control_discriminates": bool(base["corr"] < full["corr"] - 0.3
                                             and base["rmse"] > full["rmse"]),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="B", choices=["A", "B", "C", "D"])
    ap.add_argument("--n", type=int, default=512)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--A0", type=float, default=4.0)
    ap.add_argument("--lam0", type=int, default=1)
    ap.add_argument("--k1", type=int, default=4, help="wavevector of layer 1, component 1")
    ap.add_argument("--k2", type=int, default=31, help="wavevector of layer 1, component 2")
    ap.add_argument("--Lambda", type=float, default=2.5, help="pulse compression")
    ap.add_argument("--cp", type=float, default=3.0)
    ap.add_argument("--profile", default="sin2", choices=["sin2", "cinf"])
    ap.add_argument("--L-growth", dest="L_growth", type=float, default=5.0)
    ap.add_argument("--hold", type=float, default=3.0, help="hold length in units of 1/Gamma")
    ap.add_argument("--Theta0", type=float, default=-1e-5)
    ap.add_argument("--Theta0-D", dest="Theta0_D", type=float, default=-2.5e-4,
                    help="seed for part D, sized so the deposit is comparable with A0")
    ap.add_argument("--background", default="sine", choices=["sine", "flattened"],
                    help="stratification profile; flattened is affine to fourth order at the origin")
    ap.add_argument("--cutoff", type=float, default=8.0, help="demodulation radius")
    ap.add_argument("--dt", type=float, default=2e-3)
    ap.add_argument("--dt-ode", dest="dt_ode", type=float, default=2e-4)
    ap.add_argument("--n-mu", dest="n_mu", type=int, default=200)
    ap.add_argument("--alpha", type=float, default=0.5, help="dissipation order for part C")
    ap.add_argument("--damping-fraction", dest="damping_fraction", type=float, default=0.2)
    ap.add_argument("--lam2", type=int, default=256, help="layer 2 frequency, part D")
    ap.add_argument("--phi2", type=float, default=math.pi / 6, help="layer 2 laboratory angle")
    ap.add_argument("--Theta2", type=float, default=1e-9)
    ap.add_argument("--measure2", type=float, default=0.6)
    ap.add_argument("--settle2", type=float, default=0.6)
    ap.add_argument("--mask-frac", dest="mask_frac", type=float, default=0.35)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    dev = torch.device(args.device)
    grid = B.Grid(N=args.n, device=dev, dtype=torch.float64)

    # GUARD, same family as EXP-004's: a wave above the 2/3 limit is annihilated every
    # step and every rate fitted from it is noise.
    kmax = args.n / 3.0
    knorm = math.hypot(args.k1, args.k2)
    for name, lam in (("layer 1", knorm), ("layer 2", float(args.lam2) if args.part == "D" else 0.0)):
        if lam > kmax:
            raise SystemExit(f"{name} frequency {lam:.1f} exceeds the dealiasing limit "
                             f"N/3 = {kmax:.0f}; raise --n.")
    if args.part == "D" and args.lam2 < 4 * knorm:
        raise SystemExit(f"lam2 = {args.lam2} needs at least 4x the layer-1 frequency "
                         f"{knorm:.1f} for the scale separation the reduction assumes.")

    if args.part == "A":
        out = part_a(args)
    elif args.part == "B":
        out = part_b(args, grid, dev)
    elif args.part == "C":
        out = part_c(args, grid, dev)
    else:
        out = part_d(args, grid, dev)

    out = {"args": vars(args) | {"device": str(dev)}} | out
    out["all_pass"] = bool(out["gates"] and all(out["gates"].values()))
    print(json.dumps(out, indent=2, default=float))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2, default=float), encoding="utf-8")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
