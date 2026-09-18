"""EXP-008: does the cascade's critical exponent follow gamma/(2p) for BOTH growth laws?

The prediction is Theorem 3.1 of the navier-stokes paper, published as v0.04
(10.5281/zenodo.22821790) before this run: a layer cascade with frequencies
`lambda = A^p` and layers growing at rate `A^gamma` can carry dissipation only up to
`alpha_c = gamma/(2p)`. The pendulum case `gamma = 1/2` was measured by EXP-003; the
stretching case `gamma = 1`, the law of the hypodissipative Navier-Stokes construction, had
not been.

The measured threshold is compared with the horizon-corrected prediction
`detectable_alpha_p(nu, g, stages, gamma) / p`, since a finite-horizon bisection reports a
threshold slightly above the asymptotic one (see `cascade.detectable_alpha_p`).

Usage:
    python run_exp008.py --out ../experiments/EXP-008-growth-law-ceiling/result.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nslib import cascade as C


def critical_alpha(p: float, gamma: float, nu: float, g: float, stages: int,
                   iters: int = 60) -> float:
    """Bisect on alpha for the largest exponent whose schedule still closes."""
    def closes(alpha: float) -> bool:
        return C.Schedule(g=g, p=p, alpha=alpha, nu=nu, gamma=gamma).closes(stages)

    lo, hi = 1e-8, 2.0
    if not closes(lo):
        return float("nan")
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if closes(mid) else (lo, mid)
    return lo


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nu", type=float, default=1e-10)
    ap.add_argument("--g", type=float, default=1.0)
    ap.add_argument("--stages", type=int, default=200)
    ap.add_argument("--tolerance", type=float, default=1e-5,
                    help="largest acceptable relative error against the prediction")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    rows = []
    for gamma in (0.5, 1.0):
        for p in (1.5, 2.0, 3.0, 5.0):
            measured = critical_alpha(p, gamma, args.nu, args.g, args.stages)
            predicted = C.detectable_alpha_p(args.nu, args.g, args.stages, gamma) / p
            asymptotic = gamma / (2.0 * p)
            rows.append({
                "gamma": gamma, "p": p,
                "measured_alpha_c": measured,
                "predicted_horizon_corrected": predicted,
                "asymptotic_gamma_over_2p": asymptotic,
                "relative_error": abs(measured - predicted) / predicted,
            })

    by_gamma = {g: [r for r in rows if r["gamma"] == g] for g in (0.5, 1.0)}
    # the ratio between the two laws at the same p should be exactly 2 asymptotically
    ratios = [
        next(r for r in by_gamma[1.0] if r["p"] == p)["asymptotic_gamma_over_2p"]
        / next(r for r in by_gamma[0.5] if r["p"] == p)["asymptotic_gamma_over_2p"]
        for p in (1.5, 2.0, 3.0, 5.0)
    ]
    worst = max(r["relative_error"] for r in rows)
    out = {
        "args": vars(args),
        "prediction": "alpha_c = gamma/(2p), Theorem 3.1, published v0.04 before this run",
        "rows": rows,
        "worst_relative_error": worst,
        "stretching_over_pendulum_ratio": ratios,
        "gates": {
            "pendulum_law_matches": bool(max(r["relative_error"] for r in by_gamma[0.5])
                                         < args.tolerance),
            "stretching_law_matches": bool(max(r["relative_error"] for r in by_gamma[1.0])
                                           < args.tolerance),
            "factor_two_between_laws": bool(all(abs(x - 2.0) < 1e-12 for x in ratios)),
        },
    }
    out["all_pass"] = bool(all(out["gates"].values()))
    print(json.dumps(out, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
