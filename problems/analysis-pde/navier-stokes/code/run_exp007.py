"""EXP-007: does localization break the dissipative reduction?

Hypothesis committed first: `../experiments/EXP-007-localized-dissipation/hypothesis.md`.

Our dissipative modulation system uses one fact: `(-Laplacian)^alpha` is diagonal on a plane
wave. The construction's layers are not plane waves, they are localized with an envelope of
radius `ell_q = lambda_{q-1}^(-3)`, and a localized wave is a band. This measures what that
costs, with no time stepping: build the localized wave, apply the operator spectrally, and
compare against the plane-wave answer where the envelope actually lives.

Usage:
    python run_exp007.py --n 4096 --out ../experiments/EXP-007-localized-dissipation/result.json
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import torch

from nslib import boussinesq as B


def smooth_bump(r2: torch.Tensor, radius: float) -> torch.Tensor:
    """A C-infinity bump of the given radius, as a function of squared distance.

    `exp(1 - 1/(1 - u))` with `u = r^2/radius^2`, which is one at the centre, flat to every
    order at the boundary, and exactly zero outside. A Gaussian would be smoother in
    Fourier but never compactly supported, and compact support is the property the
    construction actually uses.
    """
    u = (r2 / (radius * radius)).clamp(max=1.0)
    inside = u < 1.0
    out = torch.zeros_like(u)
    safe = torch.where(inside, u, torch.zeros_like(u))
    out[inside] = torch.exp(1.0 - 1.0 / (1.0 - safe[inside]))
    return out


def one_case(grid: B.Grid, k: tuple[int, int], radius: float, alpha: float,
             mask_level: float) -> dict:
    """Relative error of the plane-wave damping law for one localized wave."""
    x1, x2 = grid.coords()
    # distance to the centre of the box, wrapped, so the envelope is not cut by the edge
    d1 = torch.remainder(x1 - math.pi, 2 * math.pi) - math.pi
    d2 = torch.remainder(x2 - math.pi, 2 * math.pi) - math.pi
    env = smooth_bump(d1 * d1 + d2 * d2, radius)

    phase = k[0] * x1 + k[1] * x2
    field = env * torch.sin(phase)

    k1, k2 = grid.wavenumbers()
    symbol = (k1 * k1 + k2 * k2).clamp(min=0.0) ** alpha
    exact = torch.fft.ifft2(symbol * torch.fft.fft2(field)).real

    knorm = math.hypot(*k)
    plane = (knorm ** (2.0 * alpha)) * field

    # Compare only where the envelope carries the layer. In the tails both sides are near
    # zero and their ratio is numerical noise, which is how a measurement of nothing gets
    # reported as a large error.
    core = env > mask_level * float(env.max())
    num = float((exact - plane)[core].abs().max())
    den = float(plane[core].abs().max())
    bandwidth_ratio = radius * knorm          # ell * lambda
    return {
        "k": list(k),
        "lambda": knorm,
        "ell": radius,
        "ell_times_lambda": bandwidth_ratio,
        "alpha": alpha,
        "relative_error": num / max(den, 1e-300),
        "n_core_points": int(core.sum()),
        "reach": knorm + 3.0 / radius,        # wave plus a few envelope bandwidths
    }


def fit_slope(xs: list[float], ys: list[float]) -> float:
    """Least-squares slope of log y against log x."""
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    num = sum((a - mx) * (b - my) for a, b in zip(lx, ly))
    den = sum((a - mx) ** 2 for a in lx)
    return num / den


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4096)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--alpha", type=float, default=0.5)
    ap.add_argument("--mask-level", dest="mask_level", type=float, default=0.5)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    dev = torch.device(args.device)
    grid = B.Grid(N=args.n, device=dev, dtype=torch.float64)
    kmax = args.n / 3.0

    # H1: vary the bandwidth ratio through both knobs, frequency and envelope radius.
    scan = []
    for lam in (64, 128, 256, 512):
        for radius in (0.4, 0.8, 1.6):
            k = (0, lam)
            case = one_case(grid, k, radius, args.alpha, args.mask_level)
            if case["reach"] > kmax:
                raise SystemExit(
                    f"lambda {lam} with envelope {radius} reaches |k| = {case['reach']:.0f}, "
                    f"past the dealiasing limit N/3 = {kmax:.0f}; raise --n.")
            scan.append(case)

    slope = fit_slope([c["ell_times_lambda"] for c in scan],
                      [c["relative_error"] for c in scan])

    # H2: the coefficient across the range of exponents that matters.
    by_alpha = []
    for alpha in (0.05, 0.1, 0.25, 0.5, 1.0):
        case = one_case(grid, (0, 256), 0.8, alpha, args.mask_level)
        case["coefficient"] = case["relative_error"] * case["ell_times_lambda"]
        by_alpha.append(case)

    # H3: the control, an envelope as wide as the wave.
    control = one_case(grid, (0, 4), 0.35, args.alpha, args.mask_level)
    control["ell_times_lambda"] = control["ell"] * control["lambda"]

    coefficients = [c["coefficient"] for c in by_alpha]
    out = {
        "args": vars(args) | {"device": str(dev)},
        "scan": scan,
        "H1_slope_of_log_error_against_log_bandwidth_ratio": slope,
        "H2_coefficients_by_alpha": by_alpha,
        "H2_coefficient_min": min(coefficients),
        "H2_coefficient_max": max(coefficients),
        "H3_control_wide_envelope": control,
        "gates": {
            "H1_first_order": bool(abs(slope + 1.0) < 0.1),
            "H2_coefficient_bounded": bool(max(coefficients) < 10.0
                                           and min(coefficients) > 0.01),
            "H3_control_is_order_one": bool(control["relative_error"] > 0.1),
        },
    }
    out["all_pass"] = bool(all(out["gates"].values()))
    print(json.dumps(out, indent=2, default=float))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2, default=float), encoding="utf-8")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
