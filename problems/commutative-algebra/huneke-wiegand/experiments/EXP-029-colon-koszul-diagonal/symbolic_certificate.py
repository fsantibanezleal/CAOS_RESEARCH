"""Arithmetic and Z3 certificate for the EXP-029 closed formulas."""

from __future__ import annotations

import argparse
import hashlib
import json
from math import comb
from pathlib import Path

import sympy as sp
from z3 import Int, Solver, sat


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "symbolic-certificate.json"


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def coverage_intervals(p: int) -> list[tuple[int, int, str]]:
    return [
        (12 * p + 1, 16 * p - 5, "AA"),
        (14 * p, 18 * p - 4, "AB"),
        (17 * p - 1, 20 * p - 3, "AD"),
        (19 * p - 1, 22 * p - 3, "BD"),
        (21 * p + 1, 24 * p - 4, "BE"),
        (23 * p - 1, 26 * p - 3, "AK"),
        (25 * p - 1, 28 * p - 3, "BK"),
        (28 * p - 2, 30 * p - 2, "DK"),
        (30 * p, 32 * p - 3, "EK"),
        (31 * p - 1, 33 * p - 2, "FK"),
        (33 * p - 1, 34 * p - 1, "GK"),
        (34 * p - 1, 36 * p - 3, "KK"),
    ]


def interval_union_summary(intervals: list[tuple[int, int, str]]) -> tuple[int, list[tuple[int, int]]]:
    merged: list[list[int]] = []
    for left, right, _label in sorted(intervals):
        if not merged or left > merged[-1][1] + 1:
            merged.append([left, right])
        else:
            merged[-1][1] = max(merged[-1][1], right)
    count = sum(right - left + 1 for left, right in merged)
    return count, [(left, right) for left, right in merged]


def arithmetic_checks(limit: int) -> list[dict[str, object]]:
    rows = []
    for p in range(4, limit + 1):
        support_count, components = interval_union_summary(coverage_intervals(p))
        target_components = [(12 * p + 1, 30 * p - 2), (30 * p, 36 * p - 3)]
        beta35 = comb(8 * p, 2)
        numerator45 = 2 * p * (5 * p - 1) * (10 * p - 3) * (100 * p * p - 110 * p + 13)
        if components != target_components or support_count != 24 * p - 4:
            raise AssertionError(f"p={p}: support coverage mismatch")
        if beta35 != 4 * p * (8 * p - 1) or numerator45 % 3:
            raise AssertionError(f"p={p}: closed formula mismatch")
        if p in {4, 5, 17, 73, 151, 300, limit}:
            rows.append(
                {
                    "p": p,
                    "support_count": support_count,
                    "unshifted_hole": 30 * p - 1,
                    "beta_3_5": beta35,
                    "beta_4_5": numerator45 // 3,
                }
            )
    return rows


def z3_chain_checks() -> list[dict[str, object]]:
    p = Int("p")
    intervals = coverage_intervals(p)
    obligations = []
    for index in range(len(intervals) - 1):
        left = intervals[index]
        right = intervals[index + 1]
        allowed_gap = 1 if left[2] == "DK" and right[2] == "EK" else 0
        solver = Solver()
        solver.add(p >= 4)
        solver.add(right[0] > left[1] + 1 + allowed_gap)
        result = solver.check()
        if result == sat:
            raise AssertionError(f"unexpected interval gap between {left[2]} and {right[2]}")
        obligations.append(
            {
                "left": left[2],
                "right": right[2],
                "allowed_gap": allowed_gap,
                "negated_gap": str(result).upper(),
            }
        )
    return obligations


def symbolic_identity() -> str:
    p = sp.symbols("p", integer=True, positive=True)
    c = 10 * p - 1
    h = [1, c, 12 * p, 2 * p - 1, 1]
    coefficient = sum(h[r] * (-1) ** (5 - r) * sp.binomial(c, 5 - r) for r in range(5))
    beta25 = p * (2 * p - 3)
    beta35 = 4 * p * (8 * p - 1)
    beta45 = 2 * p * (5 * p - 1) * (10 * p - 3) * (100 * p**2 - 110 * p + 13) / 3
    residual = sp.factor(sp.expand_func(coefficient - beta25 + beta35 - beta45))
    if residual != 0:
        raise AssertionError(f"degree-five coefficient residual: {residual}")
    return str(residual)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.limit < 4:
        raise ValueError("limit must be at least four")

    payload: dict[str, object] = {
        "experiment": "EXP-029-colon-koszul-diagonal",
        "status": "PASS",
        "arithmetic_limit": args.limit,
        "arithmetic_samples": arithmetic_checks(args.limit),
        "z3_obligations": z3_chain_checks(),
        "coefficient_residual": symbolic_identity(),
    }
    payload["symbolic_aggregate"] = canonical_hash(payload)
    write_json_atomic(args.output, payload)
    print(f"PASS symbolic_aggregate={payload['symbolic_aggregate']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
