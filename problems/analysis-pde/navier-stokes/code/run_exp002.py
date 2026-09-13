"""EXP-002: does the reduced modulation model predict the Boussinesq PDE?

HYPOTHESIS, committed before the run (methodology 02).

Take the Alpoge-Buckmaster stratification with the cutoff dropped, which is an EXACT
steady state of the unforced inviscid system:

    theta_bg(x) = -(A0 / lam0) sin(lam0 x2),   omega = 0,   u = 0

(indeed d_1 theta_bg = 0, so the vorticity equation has zero right-hand side). Its
background temperature gradient is G(x) = (0, -A0 cos(lam0 x2)), so the LOCAL
gradient magnitude varies with height. Add one small wave at wavevector
k0 = lam * zeta, zeta = (sin phi, cos phi), started on the growing eigenline.

Three predictions are tested, each with its own pass criterion.

P1  RATE.  In the unstable bands the local growth rate is
        sigma(x2) = sqrt(A0 cos(lam0 x2)) * sin(phi) - nu |k0|^(2 alpha).
    Checked where the background is flattest, cos(lam0 x2) >= 0.9, because the
    prediction is local and the reduction cannot be blamed for band edges where the
    background gradient varies as fast as the wave grows.
    PASS: relative error <= 2 percent.

P2  BAND STRUCTURE.  Where cos(lam0 x2) < 0 the product of the off-diagonal
    coefficients changes sign, the eigenvalues become imaginary, and the wave must
    OSCILLATE rather than grow. A log-slope fit is meaningless there because the
    amplitude passes through zero, so the criterion is a bound on the amplitude
    ratio instead.
    PASS: the stable-band envelope never exceeds its initial value by more than a
    factor of 2 while the unstable band grows by orders of magnitude.

P3  FREQUENCY INDEPENDENCE.  The inviscid rate carries no lambda. This is the fact
    the whole dissipative analysis rests on, so it is tested in the PDE and not only
    in the ODE: sweeping lam must leave the measured peak rate unchanged.
    PASS: spread across lam <= 2 percent.

NEGATIVE CONTROLS.  Three corrupted models must FAIL P1: dropping the zeta_1 factor,
dropping the inverse-norm scaling, and flipping the sign. A control that passes would
mean the test cannot tell a right model from a wrong one.

FAIL of P1 or P2 means the reduction does not describe the equation it claims to
reduce, every statement built on it is void, and the plan is rewritten around the
PDE instead.

Usage:
    python run_exp002.py --n 1024 --mode all
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import torch

from nslib import boussinesq as B


def evolve(solver, grid, theta_hat, omega_hat, k0, dt, n_steps, sample_every, cutoff):
    """Return (times, envelope profiles in x2) sampled along the run."""
    times, profiles = [], []
    t = 0.0
    for step in range(n_steps + 1):
        if step % sample_every == 0:
            env = B.demodulate(theta_hat, k0, grid, cutoff)
            profiles.append(env.abs().mean(dim=0).clone())
            times.append(t)
        if step < n_steps:
            theta_hat, omega_hat = solver.step(theta_hat, omega_hat, dt)
            t += dt
    return torch.tensor(times, dtype=grid.dtype, device=grid.device), torch.stack(profiles)


def fit_rates(times, profiles):
    y = torch.log(profiles.clamp_min(1e-300))
    t = times - times.mean()
    return (t[:, None] * (y - y.mean(dim=0, keepdim=True))).sum(dim=0) / (t * t).sum()


def run_case(args, lam, nu, alpha, corrupt="none"):
    dev = torch.device(args.device)
    grid = B.Grid(N=args.n, device=dev, dtype=torch.float64)
    solver = B.Boussinesq2D(grid, nu=nu, alpha=alpha)
    z1, _z2, knorm = B.realized_zeta(lam, args.phi)
    k0 = B.realized_wavevector(lam, args.phi)
    Omega0 = knorm * args.Theta0 / math.sqrt(args.A0)
    th, om = B.layered_initial_data(grid, args.A0, args.lam0, lam, args.phi, args.Theta0, Omega0)

    n_steps = int(round(args.t_end / args.dt))
    times, profiles = evolve(solver, grid, th, om, k0, args.dt, n_steps,
                             max(1, n_steps // 40), cutoff=max(2.0 * args.lam0, 3.0))
    measured = fit_rates(times, profiles)

    _, x2 = grid.coords()
    cosb = torch.cos(args.lam0 * x2[0, :])
    damp = nu * (knorm ** (2.0 * alpha))
    coef = args.A0 * cosb * (z1 ** 2)
    if corrupt == "drop-zeta1":
        coef = args.A0 * cosb
    elif corrupt == "drop-invnorm":
        coef = args.A0 * cosb * (z1 ** 2) * knorm
    elif corrupt == "swap-sign":
        coef = -args.A0 * cosb * (z1 ** 2)
    predicted = torch.sqrt(coef.clamp_min(0.0)) - damp

    flat = cosb >= 0.9            # P1 region: background locally flat
    stable = cosb < -0.25         # P2 region
    ratio = profiles[-1] / profiles[0].clamp_min(1e-300)
    rel = ((measured[flat] - predicted[flat]).abs() / predicted[flat].abs().clamp_min(1e-12))
    return {
        "lam": lam, "nu": nu, "alpha": alpha, "corrupt": corrupt,
        "knorm": knorm, "damp": damp,
        "peak_measured": float(measured[flat].max()),
        "peak_predicted": float(predicted[flat].max()),
        "p1_max_rel_err": float(rel.max()),
        "p1_median_rel_err": float(rel.median()),
        "p2_unstable_growth_factor": float(ratio[flat].max()),
        "p2_stable_growth_factor": float(ratio[stable].max()),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1024)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--A0", type=float, default=4.0)
    ap.add_argument("--lam0", type=int, default=1)
    ap.add_argument("--lam", type=int, default=40)
    ap.add_argument("--phi", type=float, default=math.pi / 2)
    ap.add_argument("--Theta0", type=float, default=1e-6)
    ap.add_argument("--t-end", type=float, default=0.6)
    ap.add_argument("--dt", type=float, default=5e-4)
    ap.add_argument("--mode", default="all", choices=["all", "rate", "lambda", "viscous", "controls"])
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    t0 = time.time()
    out = {"args": vars(args), "cases": {}}

    if args.mode in ("all", "rate"):
        out["cases"]["P1_inviscid"] = run_case(args, args.lam, 0.0, 1.0)

    if args.mode in ("all", "lambda"):
        sweep = [run_case(args, L, 0.0, 1.0) for L in (20, 40, 80, 160)]
        peaks = [c["peak_measured"] for c in sweep]
        out["cases"]["P3_lambda_sweep"] = {
            "per_lambda": sweep,
            "peak_spread_abs": max(peaks) - min(peaks),
            "peak_spread_rel": (max(peaks) - min(peaks)) / max(abs(p) for p in peaks),
        }

    if args.mode in ("all", "viscous"):
        visc = []
        for alpha in (0.25, 0.5, 1.0):
            for nu in (1e-5, 1e-4):
                visc.append(run_case(args, args.lam, nu, alpha))
        out["cases"]["P1_viscous"] = visc

    if args.mode in ("all", "controls"):
        out["cases"]["negative_controls"] = [
            run_case(args, args.lam, 0.0, 1.0, corrupt=c)
            for c in ("drop-zeta1", "drop-invnorm", "swap-sign")
        ]

    out["wall_seconds"] = round(time.time() - t0, 1)
    print(json.dumps(out, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
