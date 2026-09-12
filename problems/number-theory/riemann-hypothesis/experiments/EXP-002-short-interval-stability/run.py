"""Deterministic CPU certificate runner; hypothesis committed before execution."""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

from flint import ctx

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "code"))
from riemann_certificates import (  # noqa: E402
    bracket, c_value, certify_triangle, improved_bound, verify_triangle,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--radius", default="6")
    parser.add_argument("--threshold", default="1/100000")
    parser.add_argument("--budget", type=float, default=600)
    parser.add_argument("--max-nodes", type=int, default=2_000_000)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ctx.prec = 160
    theta, radius, delta = Fraction(3, 4), Fraction(args.radius), Fraction(args.threshold)
    cert = certify_triangle(theta, radius, delta, budget=args.budget,
        max_nodes=args.max_nodes, checkpoint=args.output_dir / "checkpoint.json", resume=args.resume)
    (args.output_dir / "triangle-certificate.json").write_text(json.dumps(cert, indent=2) + "\n",
                                                            encoding="utf-8", newline="\n")
    ctx.prec = 256
    audit = verify_triangle(cert)
    result = improved_bound(theta, radius, delta)
    gain = result - c_value(theta)
    if not gain > 0:
        raise AssertionError("No certified gain")
    summary = {"theta": str(theta), "radius": str(radius), "delta": str(delta),
        "baseline": bracket(c_value(theta)), "improved": bracket(result),
        "gain": bracket(gain), "audit": audit,
        "scope": "Finite certificate plus EXP-002 written proof; not a global zero-proportion record"}
    (args.output_dir / "result.json").write_text(json.dumps(summary, indent=2) + "\n",
                                              encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
