"""EXP-003: does the repaired cascade model predict the published threshold?

HYPOTHESIS, committed before the run (methodology 02).

Cordoba, Martinez-Zoroa and Zheng prove finite-time blowup for the forced fractional
Navier-Stokes equations for every |grad|^alpha exponent below

    alpha_0 = (22 - 8 sqrt 7) / 9 = 0.0926655...,

that is alpha_0 / 2 = 0.0463328... in the (-Laplacian)^alpha convention used here.

The cascade bookkeeping in `nslib/cascade.py`, with the time budget and the
hold-interval damping put back in, gives

    alpha_c(p) = 1 / (4 p)

where p is the frequency growth exponent in lambda_q ~ A_q^p. Three predictions:

H1  The batched GPU evaluation reproduces alpha_c(p) over a wide range of p, once the
    FINITE-HORIZON BIAS is accounted for. A run truncated at Q stages cannot see a
    schedule whose stall arrives after stage Q, so a bisection reports a threshold
    too high by the factor 1 + 2 log(1/nu) / (g (Q-1)); see
    `cascade.alpha_c_finite_horizon`. The measured value must match that corrected
    prediction, and must converge to the naive 1/(4p) as Q grows.

H2  The two constraints that could each have set the threshold, growth positivity
    (C2) and layer survival under hold damping (C4), give the SAME exponent. The
    repair therefore does not move the threshold, which is a substantive negative
    result about the first-pass estimate's omissions.

H3  Inverting the relation at the published threshold gives p = 11/4 + sqrt 7
    exactly. This is a consistency statement, not a derivation.

PASS for H1: measured alpha_c within 1 percent of the horizon-corrected prediction
across p in [1.5, 12], AND the measured value decreasing toward 1/(4p) as Q doubles.
PASS for H2: the stage at which C4 first binds is not earlier than the stage at which
C2 first binds, for every schedule tested.
PASS for H3: exact to floating point.

FAIL of H1 would mean the scalar reference and the batched implementation disagree,
or that the closed form is wrong. FAIL of H2 would mean hold damping is the binding
constraint after all, which would LOWER the predicted threshold and change the
calibration.

Usage:
    python run_exp003.py --device cuda --batch 200000
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import torch

from nslib import cascade as C
from nslib import sweep as S


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--stages", type=int, default=400)
    ap.add_argument("--batch", type=int, default=200_000)
    ap.add_argument("--nu", type=float, default=1e-10)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    dev = torch.device(args.device)
    dt = torch.float64
    t0 = time.time()
    out: dict = {"args": vars(args) | {"device": str(dev)}}

    # ---- H1: alpha_c(p) over a range of p -----------------------------------
    p_vals = torch.linspace(1.5, 12.0, 64, device=dev, dtype=dt)
    ac = S.critical_alpha(p_vals, nu=args.nu, g=1.0, stages=args.stages)
    closed = 1.0 / (4.0 * p_vals)
    corrected = torch.tensor(
        [C.alpha_c_finite_horizon(float(x), args.nu, 1.0, args.stages) for x in p_vals],
        device=dev, dtype=dt)
    rel = ((ac - corrected).abs() / corrected)
    # Horizon convergence: doubling Q must move the measurement toward 1/(4p).
    probe = torch.tensor([3.0, C.P_STAR, 9.5], device=dev, dtype=dt)
    conv = []
    for Q in (args.stages, 2 * args.stages, 4 * args.stages):
        m = S.critical_alpha(probe, nu=args.nu, g=1.0, stages=Q)
        gap = (m - 1.0 / (4.0 * probe)).abs().max()
        conv.append({"stages": Q, "max_gap_to_closed_form": float(gap)})
    monotone = all(conv[i + 1]["max_gap_to_closed_form"] < conv[i]["max_gap_to_closed_form"]
                   for i in range(len(conv) - 1))
    out["H1"] = {
        "p_min": float(p_vals.min()), "p_max": float(p_vals.max()),
        "max_rel_err_vs_corrected": float(rel.max()),
        "median_rel_err_vs_corrected": float(rel.median()),
        "horizon_convergence": conv,
        "gap_shrinks_with_horizon": monotone,
        "sample": [{"p": round(float(a), 4), "alpha_c_measured": float(b),
                    "alpha_c_closed_form": float(c), "alpha_c_horizon_corrected": float(d)}
                   for a, b, c, d in list(zip(p_vals.tolist(), ac.tolist(),
                                              closed.tolist(), corrected.tolist()))[::12]],
        "pass": bool(rel.max() < 0.01 and monotone),
    }

    # ---- H2: which constraint binds first -----------------------------------
    # Evaluate a grid of (p, alpha) and record, for schedules that fail, whether C2
    # or C4 is responsible. If C4 ever fails while C2 holds, hold damping binds
    # harder and the threshold would be lower than 1/(4p).
    pg = torch.linspace(1.5, 12.0, 48, device=dev, dtype=dt)
    ag = torch.linspace(0.005, 0.30, 48, device=dev, dtype=dt)
    P, A = torch.meshgrid(pg, ag, indexing="ij")
    P, A = P.reshape(-1), A.reshape(-1)
    G = torch.ones_like(P)
    NU = torch.full_like(P, args.nu)
    res = S.evaluate(G, P, A, NU, stages=args.stages)
    c2, c4 = res["c2"], res["c4"]
    c4_binds_alone = (c2 & ~c4)
    out["H2"] = {
        "n_schedules": int(P.numel()),
        "n_c2_fail": int((~c2).sum()),
        "n_c4_fail": int((~c4).sum()),
        "n_c4_binds_while_c2_holds": int(c4_binds_alone.sum()),
        "pass": bool(int(c4_binds_alone.sum()) == 0),
    }

    # ---- H3: the closed-form calibration ------------------------------------
    p_star = C.implied_p(C.ALPHA0_CMZ)
    out["H3"] = {
        "alpha0_cmz": C.ALPHA0_CMZ,
        "alpha0_ours": C.ALPHA0_CMZ / 2.0,
        "implied_p": p_star,
        "closed_form_11_4_plus_sqrt7": 11.0 / 4.0 + math.sqrt(7.0),
        "abs_diff": abs(p_star - (11.0 / 4.0 + math.sqrt(7.0))),
        "alpha_c_at_p_star": C.alpha_c(p_star),
        "pass": bool(abs(p_star - (11.0 / 4.0 + math.sqrt(7.0))) < 1e-12),
    }

    # ---- large ensemble, the actual GPU load --------------------------------
    gen = torch.Generator(device=dev).manual_seed(20260912)
    n = args.batch
    Pb = torch.rand(n, device=dev, dtype=dt, generator=gen) * 10.5 + 1.5
    Ab = torch.rand(n, device=dev, dtype=dt, generator=gen) * 0.30 + 0.002
    Gb = torch.rand(n, device=dev, dtype=dt, generator=gen) * 1.5 + 0.5
    Nb = 10.0 ** (-(torch.rand(n, device=dev, dtype=dt, generator=gen) * 10.0 + 4.0))
    t1 = time.time()
    # Chunk so the (B, Q) intermediates fit: 8 * B * Q bytes per tensor, about ten of them.
    chunk = max(1, min(n, int(4e8 / (8 * args.stages * 10))))
    closes = torch.empty(n, dtype=torch.bool, device=dev)
    for i in range(0, n, chunk):
        sl = slice(i, min(i + chunk, n))
        closes[sl] = S.evaluate(Gb[sl], Pb[sl], Ab[sl], Nb[sl], stages=args.stages)["closes"]
    if dev.type == "cuda":
        torch.cuda.synchronize()
    ens_seconds = time.time() - t1
    # Every schedule that closes must satisfy alpha p < the horizon-detectable bound,
    # which is per-schedule because nu and g vary across the ensemble.
    bound = 0.25 + torch.log(1.0 / Nb) / (2.0 * Gb * max(1, args.stages - 1))
    prod = (Ab * Pb)
    violations = closes & (prod >= bound)
    out["ensemble"] = {
        "n": n, "seconds": round(ens_seconds, 2), "chunk": chunk,
        "n_closes": int(closes.sum()),
        "max_alpha_times_p_among_closing": float(prod[closes].max()) if int(closes.sum()) else None,
        "naive_bound": 0.25,
        "horizon_bound_range": [float(bound.min()), float(bound.max())],
        "n_violating_horizon_bound": int(violations.sum()),
        "pass": bool(int(violations.sum()) == 0),
        "peak_vram_mb": (round(torch.cuda.max_memory_allocated() / 1e6, 1)
                         if dev.type == "cuda" else None),
    }

    out["wall_seconds"] = round(time.time() - t0, 1)
    out["all_pass"] = all(out[k]["pass"] for k in ("H1", "H2", "H3", "ensemble"))
    print(json.dumps(out, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
