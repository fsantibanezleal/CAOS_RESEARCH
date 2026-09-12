"""One bounded deterministic floating design pass; samples certify nothing."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
THETA = 0.75
A = THETA / np.sqrt(2)


def kernel(x):
    phase = np.pi * THETA * x
    return (np.sinc((phase - A) / np.pi) + np.sinc((phase + A) / np.pi)) / (2 * np.sinc(A / np.pi))


def objective(u, v, pressure):
    return 2 * (kernel(u) ** 2 + kernel(v) ** 2 + kernel(u + v) ** 2) + pressure * (u + v)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise ValueError("A fresh exploration directory is required")
    args.output_dir.mkdir(parents=True)
    start = time.monotonic()
    deadline = start + 60
    prior_path = HERE.parent / "EXP-002-short-interval-stability/artifacts/exploration.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    seeds = [(row["u"], row["v"]) for row in prior["rows"]]
    axis = np.linspace(0, 12, 601)
    uu, vv = np.meshgrid(axis, axis, indexing="ij")
    inside = uu + vv <= 12
    u, v = uu[inside], vv[inside]
    energy = objective(u, v, 0)
    baseline = 2 - THETA / 2 - 1 / (np.sqrt(2) * np.tan(A))
    stage_a_gain = (baseline - 8 / 21) / 14000
    trials = []
    pressures = [Fraction(n, 1_000_000) for n in (2, 4, 8, 16, 24, 32, 48, 64, 80, 96, 128, 192, 256, 384, 512, 768)]
    for rational_p in pressures:
        if time.monotonic() >= deadline:
            break
        pressure = float(rational_p)
        values = energy + pressure * (u + v)
        indices = np.argpartition(values, 12)[:12]
        initial = [(float(u[i]), float(v[i])) for i in indices] + seeds
        best_index = int(np.argmin(values))
        best = (float(values[best_index]), float(u[best_index]), float(v[best_index]))
        for left, right in initial:
            if time.monotonic() >= deadline:
                break
            for width in (0.03, 0.003, 0.0003, 0.00003, 0.000003):
                x = np.linspace(max(0, left - width), min(12, left + width), 17)
                y = np.linspace(max(0, right - width), min(12, right + width), 17)
                xx, yy = np.meshgrid(x, y, indexing="ij")
                current = np.where(xx + yy <= 12, objective(xx, yy, pressure), np.inf)
                position = np.unravel_index(np.argmin(current), current.shape)
                left, right = float(xx[position]), float(yy[position])
                candidate = (float(current[position]), left, right)
                if candidate[0] < best[0]:
                    best = candidate
        # A generous 5% reserve makes certification useful before chasing precision.
        epsilon = Fraction(int(np.floor(best[0] * 0.95 * 1_000_000_000)), 1_000_000_000)
        cutoff = epsilon / rational_p
        count = int(Fraction(1) // epsilon) if epsilon > 0 else 0
        gain = count * (float(epsilon) * baseline - 2 * pressure) / (2 * count + 1 - count * float(epsilon)) if count else 0
        eligible = bool(0 < epsilon <= Fraction(1, 2) and cutoff <= 12 and count >= 2 and gain > 1.25 * stage_a_gain)
        trials.append({"pressure": str(rational_p), "epsilon": str(epsilon), "cutoff": str(cutoff),
            "sample_minimum": best[0], "sample_witness": [str(Fraction(str(q)).limit_denominator(10**9)) for q in best[1:]],
            "sample_conditional_gain": gain, "sample_gain_ratio_to_stage_a": gain / stage_a_gain,
            "eligible_by_floating_preflight": eligible, "k": count})
    candidates = sorted([row for row in trials if row["eligible_by_floating_preflight"]],
                        key=lambda row: (-row["sample_conditional_gain"], Fraction(row["pressure"])))[:3]
    result = {"schema": "riemann-pressure-candidates-v1", "declaration_commit": "8ed806d64e5df2b83ab1ad75cb9f17a5633208bc",
        "status": "exploration only; all lower bounds remain unproved", "theta": "3/4",
        "method": "deterministic 600-interval triangular grid plus local 17x17 refinements; no random numbers",
        "reserve_fraction": "1/20", "maximum_candidates": 3,
        "prior_exploration_sha256": hashlib.sha256(prior_path.read_bytes()).hexdigest(),
        "exploration_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "trials": trials, "candidates": candidates}
    (args.output_dir / "candidates.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    elapsed = time.monotonic() - start
    (args.output_dir / "operational.json").write_text(json.dumps({"elapsed_seconds": elapsed, "budget_seconds": 60,
        "budget_extended": False}, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"elapsed_seconds": elapsed, "trials": len(trials), "candidates": candidates}, indent=2), flush=True)
    if not candidates or elapsed > 60:
        raise RuntimeError("No eligible frozen candidates within the declared exploration budget")


if __name__ == "__main__":
    main()
