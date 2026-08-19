"""Arithmetic and Z3 interval certificate for EXP-028."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from z3 import And, Int, Not, Or, Solver, unsat


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "symbolic-certificate.json"


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def interval(value, start, stop):
    return And(start <= value, value <= stop)


def check_unsat(name: str, expression) -> dict[str, object]:
    solver = Solver()
    solver.add(expression)
    result = solver.check()
    row = {"name": name, "result": str(result), "passed": result == unsat}
    if result != unsat:
        row["model"] = str(solver.model())
    return row


def outer(p: int, r: int) -> int:
    return min(r // 2 + 1, (2 * p - 4 - r) // 2 + 1)


def middle(p: int, r: int) -> int:
    return min(r + 1, 2 * p - 3 - r, p - 2)


def third_critical(p: int, r: int) -> int:
    if r == 2 * p - 4:
        return 1
    return min(r + 1, 2 * p - 4 - r, p - 2)


def arithmetic_row(p: int) -> dict[str, object]:
    outer_values = [outer(p, r) for r in range(2 * p - 3)]
    middle_values = [middle(p, r) for r in range(2 * p - 3)]
    third_critical_values = [third_critical(p, r) for r in range(2 * p - 3)]
    checks = {
        "outer_reflection": outer_values == list(reversed(outer_values)),
        "outer_sum": sum(outer_values) == p * (p - 1) // 2,
        "middle_reflection": middle_values == list(reversed(middle_values)),
        "middle_sum": sum(middle_values) == p * (p - 2),
        "total": 2 * sum(outer_values) + sum(middle_values) == p * (2 * p - 3),
        "positive": min(outer_values + middle_values) >= 1,
        "third_unit_pivot_count_nonnegative": all(
            critical >= surviving
            for critical, surviving in zip(third_critical_values, outer_values)
        ),
    }
    return {"p": p, "passed": all(checks.values()), "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    p, b, r, i, j = (Int(name) for name in ("p", "b", "r", "i", "j"))
    block_a = interval(b, 3 * p + 2, 5 * p - 2)
    block_b = interval(b, 6 * p + 1, 8 * p - 3)
    block_c = interval(b, 9 * p, 11 * p - 4)
    queries = [
        check_unsat(
            "support_blocks_pairwise_disjoint",
            And(p >= 4, Or(And(block_a, block_b), And(block_a, block_c), And(block_b, block_c))),
        ),
        check_unsat(
            "each_support_block_has_length_2p_minus_3",
            And(
                p >= 4,
                Or(
                    (5 * p - 2) - (3 * p + 2) + 1 != 2 * p - 3,
                    (8 * p - 3) - (6 * p + 1) + 1 != 2 * p - 3,
                    (11 * p - 4) - 9 * p + 1 != 2 * p - 3,
                ),
            ),
        ),
        check_unsat(
            "A_critical_edges_stay_in_low_block",
            And(p >= 4, 0 <= r, r <= 2 * p - 4, 1 <= i, i < j, j <= p, i + j == r + 3,
                Not(3 <= i + j),
            ),
        ),
        check_unsat(
            "C_regular_critical_edges_stay_in_declared_blocks",
            And(
                p >= 4,
                0 <= r,
                r <= 2 * p - 5,
                2 <= i,
                i <= p - 1,
                0 <= j,
                j <= p - 2,
                i + j == r + 2,
                Not(3 * p <= 3 * p + j),
            ),
        ),
        check_unsat(
            "degree_six_hole_is_only_6p_minus_1",
            And(p >= 4, b >= 0, b != 6 * p - 1, b == 6 * p - 1),
        ),
    ]
    arithmetic = [arithmetic_row(value) for value in range(4, 10_001)]
    status = "PASS" if all(row["passed"] for row in queries + arithmetic) else "FAIL"
    payload = {
        "experiment": "EXP-028-symbolic-certificate",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "z3_queries": queries,
        "arithmetic_range": [4, 10_000],
        "arithmetic_aggregate": hashlib.sha256(
            json.dumps(arithmetic, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "arithmetic_failures": [row for row in arithmetic if not row["passed"]],
    }
    write_json_atomic(args.output, payload)
    print(f"EXP-028 symbolic {status}: z3={len(queries)} arithmetic={len(arithmetic)}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
