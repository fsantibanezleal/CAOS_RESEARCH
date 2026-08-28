"""EXP-034 symbolic interval and uniqueness certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import sympy
import z3


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "symbolic-certificate.json"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def prove_unsat(name: str, assumptions: list[z3.BoolRef], negation: z3.BoolRef) -> dict[str, str]:
    solver = z3.Solver()
    solver.add(*assumptions, negation)
    status = solver.check()
    if status != z3.unsat:
        raise AssertionError(f"{name}: expected UNSAT, observed {status}")
    return {"obligation": name, "status": "UNSAT"}


def finite_row(p: int) -> dict[str, object]:
    target = 8 * p - 1
    exterior = set(range(1, p + 1))
    high_first = set(range(6 * p, 8 * p - 1))
    low_second = set(range(3 * p, 4 * p - 1))
    all_high_floor = 6 * p
    representation_from_first = {
        g for g in exterior if target - g in high_first
    }
    excluded_second = {
        g for g in low_second if target - g >= all_high_floor
    }
    source_floor_with_b_exterior = (
        3 * p + p * (p - 1) // 2 + 1
    )
    source_floor_with_b_coefficient = p * (p + 1) // 2 + 3 * p
    target_ceiling = p * (p + 1) // 2 + p
    checks = {
        "first_block_representations": representation_from_first == exterior,
        "second_low_block_excluded": not excluded_second,
        "high_variables_excluded": target - all_high_floor < all_high_floor,
        "b_exterior_source_excluded": source_floor_with_b_exterior > target_ceiling,
        "b_coefficient_source_excluded": source_floor_with_b_coefficient > target_ceiling,
        "unit_pivot_interval": p + 1 <= p + 1 <= 2 * p and p + p == 2 * p,
        "d_row_two_absent": p < 2 * p - 2,
    }
    if not all(checks.values()):
        raise AssertionError(f"p={p}: symbolic finite row failed: {checks}")
    row: dict[str, object] = {"p": p, "checks": checks}
    row["row_hash"] = digest(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    args = parser.parse_args()
    started = time.perf_counter()

    p, g, ell = z3.Ints("p g ell")
    base = [p >= 4]
    obligations = [
        prove_unsat(
            "first-low-block maps into first high block",
            base + [g >= 1, g <= p],
            z3.Or(8 * p - 1 - g < 6 * p, 8 * p - 1 - g > 8 * p - 2),
        ),
        prove_unsat(
            "second-low-block cannot represent target",
            base + [g >= 3 * p, g <= 4 * p - 2],
            8 * p - 1 - g >= 6 * p,
        ),
        prove_unsat(
            "high variable cannot represent target",
            base + [g >= 6 * p],
            8 * p - 1 - g >= 6 * p,
        ),
        prove_unsat(
            "connecting high label lies in first high block",
            base + [ell >= 1, ell <= p],
            z3.Or(8 * p - 1 - ell < 6 * p, 8 * p - 1 - ell > 8 * p - 2),
        ),
        prove_unsat(
            "a B exterior variable exceeds source multidegree",
            base + [ell >= 1, ell <= p],
            3 * p + p * (p - 1) / 2 + 1 <= p * (p + 1) / 2 + ell,
        ),
        prove_unsat(
            "a B coefficient exceeds source multidegree",
            base + [ell >= 1, ell <= p],
            p * (p + 1) / 2 + 3 * p <= p * (p + 1) / 2 + ell,
        ),
        prove_unsat(
            "unit pivot product leaves Dbar ring interval",
            base + [ell >= 1, ell <= p],
            z3.Or(p + ell < p + 1, p + ell > 2 * p),
        ),
        prove_unsat(
            "D row two can occur at homological degree p",
            base,
            2 * p - 2 <= p,
        ),
    ]

    ps = sympy.symbols("p", integer=True, positive=True)
    target_tau = 8 * ps - 1 + ps * (ps + 1) / 2
    shifted_diagonal_floor = (
        3 * ps + (ps - 1) * 6 * ps + (ps - 1) * (ps - 2) / 2
    )
    diagonal_gap = sympy.factor(shifted_diagonal_floor - target_tau)
    if diagonal_gap != (ps - 2) * (6 * ps - 1):
        raise AssertionError(f"unexpected shifted-diagonal gap: {diagonal_gap}")

    rows = [finite_row(value) for value in list(range(4, 301)) + [500, 1000]]
    result = {
        "experiment": "EXP-034",
        "route": "symbolic interval and source-uniqueness certificate",
        "status": "PASS_SYMBOLIC",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "z3_obligations": obligations,
        "shifted_d_diagonal_gap": str(diagonal_gap),
        "finite_rows": len(rows),
        "aggregate_sha256": digest([row["row_hash"] for row in rows]),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    if result["elapsed_seconds"] > args.budget_seconds:
        raise TimeoutError("INCONCLUSIVE_BUDGET")
    result["artifact_sha256"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
