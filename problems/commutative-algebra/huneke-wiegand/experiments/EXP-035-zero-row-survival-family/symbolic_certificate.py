"""EXP-035 symbolic zero-row, interval-family, and publication-boundary checks."""

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
DEFAULT_TARGET = HERE / "artifacts" / "target-quotient-p4-t2.json"
DEFAULT_AUDIT = HERE / "artifacts" / "audit.json"
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=240.0)
    args = parser.parse_args()
    started = time.perf_counter()

    p, t, g = z3.Ints("p t g")
    base = [p >= 4, t >= 2, t <= p - 2]
    obligations = [
        prove_unsat(
            "first-low values below t miss every high block",
            base + [g >= 1, g <= t - 1],
            z3.Or(10 * p + t - g <= 10 * p, 10 * p + t - g >= 11 * p - 1),
        ),
        prove_unsat(
            "the value t lands at the high singleton",
            base + [g == t],
            10 * p + t - g != 10 * p,
        ),
        prove_unsat(
            "the value t+1 lands at the missing offset",
            base + [g == t + 1],
            10 * p + t - g != 10 * p - 1,
        ),
        prove_unsat(
            "remaining first-low values land in the second high interval",
            base + [g >= t + 2, g <= p],
            z3.Or(10 * p + t - g < 8 * p, 10 * p + t - g > 10 * p - 2),
        ),
        prove_unsat(
            "every second-low value lands in the first high interval",
            base + [g >= 3 * p, g <= 4 * p - 2],
            z3.Or(10 * p + t - g < 6 * p, 10 * p + t - g > 8 * p - 2),
        ),
        prove_unsat(
            "no high variable represents the target",
            base + [g >= 6 * p],
            10 * p + t - g >= 6 * p,
        ),
        prove_unsat(
            "candidate homological degree is below the D row-two threshold",
            base,
            2 * p - t - 1 >= 2 * p - 2,
        ),
        prove_unsat(
            "candidate degrees fail to reach the lower endpoint",
            [p >= 4],
            2 * p - (p - 2) - 1 != p + 1,
        ),
        prove_unsat(
            "candidate degrees fail to reach the upper endpoint",
            [p >= 4],
            2 * p - 2 - 1 != 2 * p - 3,
        ),
    ]

    ps, ts = sympy.symbols("p t", integer=True, positive=True)
    first_sum = ps * (ps + 1) / 2 - (ts + 1) * (ts + 2) / 2 + ts
    second_sum = (ps - 1) * (7 * ps - 2) / 2
    total_offset = sympy.factor(10 * ps + ts + first_sum + second_sum)
    expected_offset = 4 * ps**2 + 6 * ps - ts * (ts - 1) / 2
    if sympy.simplify(total_offset - expected_offset) != 0:
        raise AssertionError("candidate total-offset identity failed")

    target = json.loads(args.target.read_text(encoding="utf-8"))
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    target_row = target["row"]
    checks = {
        "target_status": target["status"] == "PASS_CHARACTERISTIC_DEPENDENCE",
        "audit_status": audit["status"] == "PASS_INDEPENDENT",
        "audit_matches_target": audit["comparisons"] == {
            "basis_counts": True,
            "basis_hashes": True,
            "field_ranks": True,
        },
        "kernel_smith_profile": target_row["kernel_boundary_smith_profile"] == {
            "row_count": 79,
            "column_count": 119,
            "integer_rank": 75,
            "free_cokernel_rank": 4,
            "torsion_invariant_factors": {"2": 1},
            "diagonal_hash": "b57ebfd6175567e070f15e581c04e4fd920134736d11b92b90249cb9f36d2036",
        },
        "characteristic_two_a_dimension": (
            target_row["field_rows"]["2"]["surviving_a_dimension"] == 4
        ),
        "characteristic_three_a_dimension": (
            target_row["field_rows"]["3"]["surviving_a_dimension"] == 3
        ),
        "connecting_rank_is_one": all(
            item["connecting_image_dimension_in_kernel_cokernel"] == 1
            for item in target_row["field_rows"].values()
        ),
        "cubic_shifted_diagonal_absent": 24 + 25 + 26 + 27 > 87 - 12,
    }
    if not all(checks.values()):
        raise AssertionError(f"artifact boundary check failed: {checks}")

    result = {
        "experiment": "EXP-035",
        "route": "symbolic interval and characteristic-boundary certificate",
        "status": "PASS_SYMBOLIC",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "zero_row_criterion": (
            "the row [b,F] has an incoming coefficient iff R_b minus F is nonempty"
        ),
        "z3_obligations": obligations,
        "candidate_cardinality": "2*p-t-1",
        "candidate_total_offset": str(total_offset),
        "artifact_checks": checks,
        "target_artifact_sha256": target["artifact_sha256"],
        "audit_artifact_sha256": audit["artifact_sha256"],
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

