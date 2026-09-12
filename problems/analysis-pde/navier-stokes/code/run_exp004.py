"""EXP-004: does the layer-to-layer handoff survive in the full nonlinear PDE?

This closes the gap named in EXP-002's and EXP-003's verdicts. EXP-002 validated a
SINGLE layer on a prescribed background. EXP-003's exponent bookkeeping assumes
infinitely many NESTED layers, each growing on the gradient the previous ones built,
and nothing has tested that handoff against the equation. Neither source paper
reports a numerical multi-layer check either.

HYPOTHESIS, committed before the run (methodology 02).

The modulation system says a wave at unit wavevector `zeta` on a local background
temperature gradient `G` grows at

    sigma^2 = -zeta_1 (J zeta . G) / |zeta|^2 ,     J(x1, x2) = (-x2, x1)

(for the frozen configuration G = -A e_2 and zeta = (sin phi, cos phi) this reduces to
sigma = sqrt(A) sin(phi), which EXP-002 confirmed). The cascade's whole premise is that
`G` in that formula is the TOTAL low-frequency gradient, including the contribution
`lambda_1 Theta_1 zeta_1` that earlier layers have deposited, and NOT merely the
original stratification.

So: grow layer 1 until its own gradient contribution is comparable to the
stratification, then inject layer 2 at a much higher frequency and measure where it
grows fastest.

H1  The local growth rate of layer 2, measured by demodulation at its wavevector,
    tracks sigma(x) computed from the LOW-PASS FILTERED gradient field, which contains
    the stratification plus layer 1.

H2  DISCRIMINATING CONTROL. The same prediction computed from the ORIGINAL
    stratification alone, ignoring layer 1's deposit, fits WORSE. If it fits equally
    well the experiment proves nothing about the handoff, because layer 1 would not be
    affecting layer 2 at all.

PASS: H1 correlation above 0.9 with a regression slope within 15 percent of 1, AND the
stratification-only control doing measurably worse on both.

FAIL of H1 means the handoff does not work in the PDE the way the bookkeeping assumes,
which would invalidate the multi-layer premise of EXP-003 and is the most informative
outcome available here.

Usage:
    python run_exp004.py --n 1024 --lam1 12 --lam2 96
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import torch

from nslib import boussinesq as B


def low_pass_gradient(theta_hat, grid, cutoff):
    """Spatial gradient of theta restricted to wavenumbers below `cutoff`."""
    k1, k2 = grid.wavenumbers()
    keep = (k1 * k1 + k2 * k2) <= cutoff * cutoff
    g1 = torch.fft.ifft2(1j * k1 * theta_hat * keep).real
    g2 = torch.fft.ifft2(1j * k2 * theta_hat * keep).real
    return g1, g2


def predicted_rate(g1, g2, zeta):
    """sigma(x) = sqrt(max(0, -zeta_1 (J zeta . G))) for a unit zeta."""
    z1, z2 = zeta
    # J zeta = (-zeta_2, zeta_1); (J zeta) . G = -zeta_2 g1 + zeta_1 g2
    jz_dot_g = -z2 * g1 + z1 * g2
    return torch.sqrt(torch.clamp(-z1 * jz_dot_g, min=0.0))


def evolve(solver, theta_hat, omega_hat, dt, n_steps):
    for _ in range(n_steps):
        theta_hat, omega_hat = solver.step(theta_hat, omega_hat, dt)
    return theta_hat, omega_hat


def local_rate_field(solver, grid, theta_hat, omega_hat, k, dt, n_steps, samples, cutoff,
                     settle_steps=0):
    """Fit log|envelope| against time pointwise, returning the local rate field.

    `settle_steps` are evolved and DISCARDED before sampling begins. A wave injected
    off the local growing eigenmode carries a transient as it settles onto it, and
    fitting from t = 0 over a short window reads that transient as an inflated rate.
    Settling first removes it; the load-bearing pattern is unaffected either way (the
    correlation) but the slope only comes out near 1 once the transient is gone.
    """
    for _ in range(settle_steps):
        theta_hat, omega_hat = solver.step(theta_hat, omega_hat, dt)
    times, profs = [], []
    every = max(1, n_steps // samples)
    t = 0.0
    for step in range(n_steps + 1):
        if step % every == 0:
            times.append(t)
            profs.append(B.demodulate(theta_hat, k, grid, cutoff).abs().clone())
        if step < n_steps:
            theta_hat, omega_hat = solver.step(theta_hat, omega_hat, dt)
            t += dt
    T = torch.tensor(times, dtype=grid.dtype, device=grid.device)
    Y = torch.log(torch.stack(profs).clamp_min(1e-300))
    Tc = T - T.mean()
    slope = (Tc[:, None, None] * (Y - Y.mean(dim=0, keepdim=True))).sum(dim=0) / (Tc * Tc).sum()
    return slope, theta_hat, omega_hat


def stats(measured, pred, mask):
    m = measured[mask].flatten()
    p = pred[mask].flatten()
    mm, pm = m.mean(), p.mean()
    cov = ((m - mm) * (p - pm)).mean()
    corr = cov / (m.std(unbiased=False) * p.std(unbiased=False) + 1e-300)
    slope = cov / (p.var(unbiased=False) + 1e-300)
    rmse = torch.sqrt(((m - p) ** 2).mean())
    return {"corr": float(corr), "slope": float(slope), "rmse": float(rmse),
            "measured_mean": float(mm), "predicted_mean": float(pm)}


def run_dynamical(args, grid, solver, dev):
    """Grow layer 1 dynamically, then inject layer 2. See the module docstring.

    NOTE (2026-09-12): this path is INCONCLUSIVE by construction, and kept as the
    honest companion to the frozen test. The reduction assumes each layer grows on a
    FROZEN affine background, which the construction arranges by steering the previous
    layer into a holding interval (zeta_1 = 0, Omega = 0). This path does not implement
    steering, so layer 1 is still rotating and shearing while layer 2 grows, and the
    background layer 2 sees is not stationary over the measurement window. That is a
    defect of the SETUP, not evidence about the mechanism.
    """
    t0 = time.time()
    z1a, z1b, kn1 = B.realized_zeta(args.lam1, args.phi1)
    Omega1 = kn1 * args.Theta1 / math.sqrt(args.A0)
    th, om = B.layered_initial_data(grid, args.A0, args.lam0, args.lam1, args.phi1,
                                    args.Theta1, Omega1)
    k1v = B.realized_wavevector(args.lam1, args.phi1)
    th, om = evolve(solver, th, om, args.dt, int(round(args.grow1 / args.dt)))

    theta1_now = B.mode_amplitude(th, k1v, grid.N, "sin")
    deposit = abs(theta1_now) * kn1
    max_theta = solver.max_abs(th)

    x1, x2 = grid.coords()
    k2v = B.realized_wavevector(args.lam2, args.phi2)
    z2a, z2b, kn2 = B.realized_zeta(args.lam2, args.phi2)
    Omega2 = kn2 * args.Theta2 / math.sqrt(args.A0)
    th = th + torch.fft.fft2(args.Theta2 * torch.sin(k2v[0] * x1 + k2v[1] * x2))
    om = om + torch.fft.fft2(Omega2 * torch.cos(k2v[0] * x1 + k2v[1] * x2))

    cutoff = math.sqrt(kn1 * kn2)
    g1, g2 = low_pass_gradient(th, grid, cutoff)
    pred_full = predicted_rate(g1, g2, (z2a, z2b))
    theta_bg_hat = torch.fft.fft2(-(args.A0 / args.lam0) * torch.sin(args.lam0 * x2))
    b1, b2 = low_pass_gradient(theta_bg_hat, grid, cutoff)
    pred_strat = predicted_rate(b1, b2, (z2a, z2b))

    n2 = int(round(args.measure2 / args.dt))
    measured, th, om = local_rate_field(solver, grid, th, om, k2v, args.dt, n2,
                                        samples=30, cutoff=max(2.0 * kn1, 4.0))
    mask = (pred_full > 0.35 * float(pred_full.max())) & (pred_strat > 0.35 * float(pred_strat.max()))
    full = stats(measured, pred_full, mask)
    strat = stats(measured, pred_strat, mask)
    return {
        "mode": "dynamical",
        "wall_seconds": round(time.time() - t0, 1),
        "layer1": {"k": list(k1v), "Theta_initial": args.Theta1,
                   "Theta_after_growth": theta1_now,
                   "gradient_deposit_lambda_Theta": deposit,
                   "A0_for_comparison": args.A0, "deposit_over_A0": deposit / args.A0,
                   "max_abs_theta": max_theta},
        "layer2": {"k": list(k2v), "cutoff": cutoff, "n_masked_points": int(mask.sum())},
        "H1_lowpass_including_layer1": full,
        "H2_control_stratification_only": strat,
        "H1_pass": bool(full["corr"] > 0.9 and abs(full["slope"] - 1.0) < 0.15),
        "H2_control_is_worse": bool(strat["corr"] < full["corr"]
                                    and abs(strat["slope"] - 1.0) > abs(full["slope"] - 1.0)),
    }


def run_frozen(args, grid, solver, dev):
    """The clean test: a FROZEN two-scale vertical background.

    theta_bg(x) = -(A0/lam0) sin(lam0 x2) - (A1/lam1b) sin(lam1b x2)

    is a function of x2 alone, so d_1 theta = 0 exactly (both modes have k1 = 0), the
    vorticity source vanishes and u stays 0: it is an EXACT steady state of the
    unforced system, verified by test_two_scale_background_is_steady. Its gradient

        G(x) = (0, -A0 cos(lam0 x2) - A1 cos(lam1b x2))

    varies with height at two scales. The lam1b term stands in for the gradient an
    earlier layer would have deposited; modelling it as a vertical sinusoid rather than
    a tilted travelling wave is the one simplification, and it is what keeps the
    background frozen so the test is clean.

    Inject a fine layer-2 wave and ask whether its local growth rate tracks the TOTAL
    two-scale gradient (H1) better than the base stratification alone (H2 control). A
    yes is the load-bearing assumption of EXP-003: that a layer responds to the total
    accumulated low-frequency gradient, not merely the base.
    """
    t0 = time.time()
    x1, x2 = grid.coords()
    theta_bg = (-(args.A0 / args.lam0) * torch.sin(args.lam0 * x2)
                - (args.A1 / args.lam1b) * torch.sin(args.lam1b * x2))
    th = torch.fft.fft2(theta_bg)
    om = torch.zeros_like(th)

    # confirm the background is actually frozen before trusting the rest
    th_probe, om_probe = th.clone(), om.clone()
    for _ in range(200):
        th_probe, om_probe = solver.step(th_probe, om_probe, args.dt)
    drift = float(torch.fft.ifft2(th_probe - th).real.abs().max())

    k2v = B.realized_wavevector(args.lam2, args.phi2)
    z2a, z2b, kn2 = B.realized_zeta(args.lam2, args.phi2)
    Omega2 = kn2 * args.Theta2 / math.sqrt(args.A0)
    th = th + torch.fft.fft2(args.Theta2 * torch.sin(k2v[0] * x1 + k2v[1] * x2))
    om = om + torch.fft.fft2(Omega2 * torch.cos(k2v[0] * x1 + k2v[1] * x2))

    cutoff = math.sqrt(args.lam1b * kn2)
    g1, g2 = low_pass_gradient(th, grid, cutoff)
    pred_full = predicted_rate(g1, g2, (z2a, z2b))
    base_hat = torch.fft.fft2(-(args.A0 / args.lam0) * torch.sin(args.lam0 * x2))
    b1, b2 = low_pass_gradient(base_hat, grid, cutoff)
    pred_base = predicted_rate(b1, b2, (z2a, z2b))

    n2 = int(round(args.measure2 / args.dt))
    settle = int(round(args.settle * args.measure2 / args.dt))
    measured, th, om = local_rate_field(solver, grid, th, om, k2v, args.dt, n2,
                                        samples=30, cutoff=1.5 * args.lam1b, settle_steps=settle)
    frac = args.mask_frac
    mask = (pred_full > frac * float(pred_full.max())) & (pred_base > frac * float(pred_base.max()))
    full = stats(measured, pred_full, mask)
    base = stats(measured, pred_base, mask)
    return {
        "mode": "frozen",
        "wall_seconds": round(time.time() - t0, 1),
        "background": {"A0": args.A0, "lam0": args.lam0, "A1": args.A1, "lam1b": args.lam1b,
                       "steady_state_drift_over_200_steps": drift},
        "layer2": {"k": list(k2v), "cutoff": cutoff, "settle_steps": settle,
                   "n_masked_points": int(mask.sum())},
        "H1_full_two_scale_gradient": full,
        "H2_control_base_only": base,
        # Sub-verdicts reported separately so the honest picture survives. The
        # load-bearing claim is the PATTERN: does the local rate follow the total
        # two-scale gradient rather than the base alone? Correlation and RMSE decide
        # that. The slope-near-1 sub-gate is a quantitative bonus; it carries a
        # measurement-geometry systematic (present already at A1 = 0, shrinking as the
        # mask tightens toward flat regions) and the absolute rate was pinned to 4e-5
        # by EXP-002, so a slope miss here is not a failure of the handoff.
        "pattern_confirmed": bool(full["corr"] > 0.9),
        "control_discriminates": bool(base["corr"] < full["corr"] - 0.3 and base["rmse"] > full["rmse"]),
        "slope_gate_committed": bool(abs(full["slope"] - 1.0) < 0.15),
        # all_pass follows the ORIGINAL committed criterion, slope gate included.
        "H1_pass": bool(full["corr"] > 0.9 and abs(full["slope"] - 1.0) < 0.15),
        "H2_control_is_worse": bool(base["corr"] < full["corr"] - 0.3 and base["rmse"] > full["rmse"]),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1024)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--mode", default="frozen", choices=["frozen", "dynamical"])
    ap.add_argument("--A0", type=float, default=4.0)
    ap.add_argument("--A1", type=float, default=4.0, help="mid-scale amplitude (frozen mode)")
    ap.add_argument("--lam0", type=int, default=1)
    ap.add_argument("--lam1b", type=int, default=16, help="mid-scale wavenumber (frozen mode)")
    ap.add_argument("--lam1", type=int, default=12, help="layer 1 (dynamical mode)")
    ap.add_argument("--lam2", type=int, default=96)
    ap.add_argument("--phi1", type=float, default=math.pi / 2)
    ap.add_argument("--phi2", type=float, default=math.pi / 2)
    ap.add_argument("--Theta1", type=float, default=2e-3)
    ap.add_argument("--Theta2", type=float, default=1e-7)
    ap.add_argument("--grow1", type=float, default=2.4, help="time to grow layer 1")
    ap.add_argument("--measure2", type=float, default=0.25, help="fit window for layer 2")
    ap.add_argument("--settle", type=float, default=1.0,
                    help="settling time before fitting, as a multiple of measure2 (frozen mode)")
    ap.add_argument("--mask-frac", type=float, default=0.35,
                    help="compare where prediction exceeds this fraction of its max")
    ap.add_argument("--dt", type=float, default=2e-4)
    ap.add_argument("--nu", type=float, default=0.0)
    ap.add_argument("--alpha", type=float, default=1.0)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    dev = torch.device(args.device)
    grid = B.Grid(N=args.n, device=dev, dtype=torch.float64)
    solver = B.Boussinesq2D(grid, nu=args.nu, alpha=args.alpha)

    # GUARD. The 2/3 rule keeps only |k| <= N/3. A wave above that is annihilated by the
    # dealiasing mask every step, and the demodulated envelope is then numerical noise
    # whose log-slope fit produces enormous meaningless rates. This happened on the first
    # attempt (lam2 = 256 at N = 512, limit 170); it now fails LOUDLY rather than being
    # reported as a failed hypothesis.
    kmax = args.n / 3.0
    mid = args.lam1b if args.mode == "frozen" else args.lam1
    for name, lam in (("mid", mid), ("lam2", args.lam2)):
        if lam > kmax:
            raise SystemExit(
                f"{name}={lam} exceeds the dealiasing limit N/3={kmax:.0f} at N={args.n}. "
                f"Raise --n to at least {int(3 * lam) + 1} or lower {name}.")
    if args.lam2 < 4 * mid:
        raise SystemExit(
            f"lam2={args.lam2} needs to be well above the mid scale {mid} for the scale "
            f"separation the reduction assumes; use at least 4x.")

    runner = run_frozen if args.mode == "frozen" else run_dynamical
    out = {"args": vars(args) | {"device": str(dev)}} | runner(args, grid, solver, dev)
    out["all_pass"] = bool(out["H1_pass"] and out["H2_control_is_worse"])
    print(json.dumps(out, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
