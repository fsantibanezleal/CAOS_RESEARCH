"""Why did EXP-005 part B pass at small scale and fail at full scale?

The full-scale run reported the steered amplitude pair exploding during the HOLDING
interval (a factor 726 and a sign flip), while the same code at N = 128 with a two-e-fold
growth phase reproduced the ODE to better than one percent. Two candidate explanations,
and they call for opposite responses:

  INSTRUMENT. The amplitude is read by demodulation, that is, by low-passing a window of
  radius `cutoff` around the wave's own wavevector. Neighbouring modes inside that window
  sit at DIFFERENT laboratory angles, so they have their own growth rates, and during the
  hold, when the steered wave is deliberately frozen, they keep growing. A window that is
  too wide therefore stops measuring the wave and starts measuring its neighbours. The fix
  is to read the mode itself.

  PHYSICS. The holding interval is not stable in a periodic box: the layer's own gradient
  is an unstable stratification for everything finer, so the frozen state seeds a new
  instability that eats it. That would be a real limitation of the cycle as realized here,
  and it would have to be reported as such, not tuned away.

This script separates them by dumping, through the whole schedule: the exact Fourier
coefficient of the wave, demodulated readings at several window radii, and the amplitudes
of the individual neighbour modes, vertical and horizontal, with their predicted rates.

Usage:
    python diagnose_hold.py --n 256 --out E:/_Temp/exp005-diagnosis.json
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import torch

from nslib import boussinesq as B
from nslib import corotating as CR
from nslib import steering as S


def predicted_rate_of_mode(k, A, rotation):
    """Growth rate of a wave at integer wavevector `k` on `G = -A e_2`, gravity at `alpha`.

    In the co-rotating frame the background gradient keeps its direction, so
    `J zeta . G = -A zeta_1`, while the coefficient that multiplies `Theta` carries the
    LABORATORY component `zeta . (cos alpha, -sin alpha)`. The product of the two is the
    squared rate; a negative product means that mode oscillates instead of growing.
    """
    kn = math.hypot(*k)
    z = (k[0] / kn, k[1] / kn)
    z1_lab = z[0] * math.cos(rotation) - z[1] * math.sin(rotation)
    jz_dot_g = -A * z[0]
    prod = -z1_lab * jz_dot_g
    return math.copysign(math.sqrt(abs(prod)), prod)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=256)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--A0", type=float, default=4.0)
    ap.add_argument("--lam0", type=int, default=1)
    ap.add_argument("--k1", type=int, default=4)
    ap.add_argument("--k2", type=int, default=31)
    ap.add_argument("--Lambda", type=float, default=2.5)
    ap.add_argument("--L-growth", dest="L_growth", type=float, default=5.0)
    ap.add_argument("--hold", type=float, default=3.0)
    ap.add_argument("--Theta0", type=float, default=-1e-5)
    ap.add_argument("--dt", type=float, default=2e-3)
    ap.add_argument("--samples", type=int, default=60)
    ap.add_argument("--neighbours", type=int, default=8)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    dev = torch.device(args.device)
    grid = B.Grid(N=args.n, device=dev, dtype=torch.float64)
    design = S.SteeringDesign(Lam=args.Lambda)
    mu = S.select_mu(design)
    k = (args.k1, args.k2)
    lam = math.hypot(*k)
    stage = S.FirstStage(A=args.A0, lam=lam, sin_s=args.k1 / lam, design=design, mu=mu,
                         L_growth=args.L_growth)

    x1, x2 = grid.coords()
    theta_bg = -(args.A0 / args.lam0) * torch.sin(args.lam0 * x2)
    bg_hat = torch.fft.fft2(theta_bg)
    Theta0, Omega0 = stage.eigen_seed(args.Theta0)
    th = bg_hat + torch.fft.fft2(Theta0 * torch.sin(k[0] * x1 + k[1] * x2))
    om = torch.fft.fft2(Omega0 * torch.cos(k[0] * x1 + k[1] * x2))
    solver = CR.CoRotatingBoussinesq(grid, stage.gravity, bg_hat)

    t_end = stage.t_b + args.hold / stage.Gamma
    n_steps = int(round(t_end / args.dt))
    every = max(1, n_steps // args.samples)

    ns = args.neighbours
    vert = [(k[0], k[1] + d) for d in range(-ns, ns + 1) if d != 0]
    horiz = [(k[0] + d, k[1]) for d in range(-ns, ns + 1) if d != 0]

    series = []
    t = 0.0
    for step in range(n_steps + 1):
        if step % every == 0 or step == n_steps:
            row = {
                "t": t,
                "phase": ("growth" if t <= stage.t1 else
                          "steering" if t <= stage.t_b else "hold"),
                "rotation": stage.rotation_angle(t),
                "Z": stage.Z(t),
                "mode_Theta": B.mode_amplitude(th, k, grid.N, "sin"),
                "mode_Omega": B.mode_amplitude(om, k, grid.N, "cos"),
            }
            for c in (2.0, 4.0, 8.0):
                a, b = CR.wave_amplitudes(th, om, k, grid, c)
                row[f"demod_Theta_cut{int(c)}"] = a
                row[f"demod_Omega_cut{int(c)}"] = b
            row["neighbour_vertical_max"] = max(
                abs(B.mode_amplitude(th, m, grid.N, "sin")) for m in vert)
            row["neighbour_horizontal_max"] = max(
                abs(B.mode_amplitude(th, m, grid.N, "sin")) for m in horiz)
            row["neighbour_horizontal_argmax"] = max(
                horiz, key=lambda m: abs(B.mode_amplitude(th, m, grid.N, "sin")))
            row["max_abs_theta"] = solver.max_abs(th)
            series.append(row)
        if step < n_steps:
            th, om = solver.step_at(th, om, args.dt, t)
            t += args.dt

    ts, Th, Om = stage.integrate(args.Theta0, t_end, 2e-4)
    ode = [{"t": float(ts[i]), "Theta": float(Th[i]), "Omega": float(Om[i])}
           for i in range(0, len(ts), max(1, len(ts) // args.samples))]

    rot_hold = stage.rotation_angle(stage.t_b + 1.0)
    rates = {
        "main_mode_rate_during_growth": predicted_rate_of_mode(k, args.A0, 0.0),
        "main_mode_rate_during_hold": predicted_rate_of_mode(k, args.A0, rot_hold),
        "Gamma": stage.Gamma,
        "worst_vertical_neighbour_rate_in_hold": max(
            predicted_rate_of_mode(m, args.A0, rot_hold) for m in vert),
        "worst_horizontal_neighbour_rate_in_hold": max(
            predicted_rate_of_mode(m, args.A0, rot_hold) for m in horiz),
        "worst_horizontal_neighbour": max(
            horiz, key=lambda m: predicted_rate_of_mode(m, args.A0, rot_hold)),
    }

    out = {"args": vars(args) | {"device": str(dev)}, "mu_star": mu,
           "t1": stage.t1, "t_b": stage.t_b, "t_end": t_end,
           "predicted_rates": rates, "series": series, "ode": ode}
    print(json.dumps({"predicted_rates": rates,
                      "first": series[0], "at_t1": min(series, key=lambda r: abs(r["t"] - stage.t1)),
                      "at_tb": min(series, key=lambda r: abs(r["t"] - stage.t_b)),
                      "last": series[-1]}, indent=2, default=float))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2, default=float), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
