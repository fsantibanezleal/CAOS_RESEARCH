"""EXP-033 independent coefficient and high-kernel structural audit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_CANONICAL = HERE / "artifacts" / "results.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit.json"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def closed_interval(first: int, last: int) -> set[int]:
    return set(range(first, last + 1)) if first <= last else set()


def generators(p: int) -> set[int]:
    return (
        {0}
        | closed_interval(1, p)
        | closed_interval(3 * p, 4 * p - 2)
        | closed_interval(6 * p, 8 * p - 2)
        | closed_interval(8 * p, 10 * p - 2)
        | {10 * p}
        | closed_interval(11 * p - 1, 12 * p - 1)
        | closed_interval(13 * p + 1, 14 * p - 2)
        | closed_interval(14 * p, 15 * p - 1)
        | {16 * p}
        | closed_interval(17 * p - 1, 18 * p - 1)
    )


def c_offset_basis(p: int, degree: int) -> set[int]:
    q = 24 * p
    if degree == 0:
        return {0}
    if degree == 1:
        return generators(p)
    if degree == 2:
        return (
            closed_interval(0, 2 * p)
            | closed_interval(3 * p, 5 * p - 2)
            | closed_interval(6 * p, q - 1)
        )
    if degree == 3:
        return closed_interval(0, q - 1) - {6 * p - 1}
    return closed_interval(0, q - 1)


def coefficient_one_minus(exponent: int, degree: int) -> int:
    if not 0 <= degree <= exponent:
        return 0
    return (-1) ** degree * math.comb(exponent, degree)


def independent_strands(p: int) -> tuple[list[int], list[int]]:
    c = 2 * p - 2
    m = 8 * p
    n = 10 * p
    total_codimension = n - 2
    numerator = [
        coefficient_one_minus(total_codimension, degree)
        + c * coefficient_one_minus(total_codimension, degree - 1)
        + coefficient_one_minus(total_codimension, degree - 2)
        for degree in range(n + 1)
    ]
    d_linear = []
    for q in range(n - 1):
        internal_degree = q + 1
        diagonal = math.comb(m, internal_degree) if internal_degree <= m else 0
        terminal = math.comb(m, q - 1 - c) if 0 <= q - 1 - c <= m else 0
        d_linear.append((-1) ** q * numerator[internal_degree] + diagonal + terminal)
    row_three = []
    row_four = []
    for i in range(n):
        q = i - 1
        row_three.append(d_linear[q] if q >= 0 else 0)
        row_four.append(math.comb(m, q - c) if 0 <= q - c <= m else 0)
    return row_three, row_four


def structural_row(p: int) -> dict[str, object]:
    q = 24 * p
    g = generators(p)
    high_variables = {value for value in g if value >= 6 * p}
    stable_kernel = closed_interval(6 * p, q - 1)

    c_dimensions = [len(c_offset_basis(p, degree)) for degree in range(6)]
    expected_c_dimensions = [1, 10 * p, 22 * p, 24 * p - 1, 24 * p, 24 * p]
    t_h_vector = [1, 2 * p - 1, 2 * p, 2 * p - 1, 1]
    t_dimensions = list(itertools.accumulate(t_h_vector)) + [sum(t_h_vector)]
    kernel_dimensions = [
        c_dimension - t_dimension
        for c_dimension, t_dimension in zip(c_dimensions, t_dimensions, strict=True)
    ]

    degree_one_kernel = high_variables
    degree_two_kernel = c_offset_basis(p, 2) - (
        closed_interval(0, 2 * p) | closed_interval(3 * p, 5 * p - 2)
    )
    degree_three_kernel = c_offset_basis(p, 3) - closed_interval(0, 6 * p - 2)
    degree_four_kernel = c_offset_basis(p, 4) - closed_interval(0, 6 * p - 1)

    predictions = {
        "generator_count": len(g) == 10 * p,
        "high_variable_count": len(high_variables) == 8 * p,
        "c_dimensions": c_dimensions == expected_c_dimensions,
        "section_dimensions": t_dimensions == [1, 2 * p, 4 * p, 6 * p - 1, 6 * p, 6 * p],
        "kernel_dimensions": kernel_dimensions == [0, 8 * p, 18 * p, 18 * p, 18 * p, 18 * p],
        "degree_two_kernel": degree_two_kernel == stable_kernel,
        "degree_three_kernel": degree_three_kernel == stable_kernel,
        "degree_four_kernel": degree_four_kernel == stable_kernel,
        "x0_injective_degree_one": degree_one_kernel <= degree_two_kernel,
        "x0_stable_after_degree_two": degree_two_kernel == degree_three_kernel == degree_four_kernel,
        "forbidden_variable_gap": 8 * p - 1 not in high_variables,
        "stable_kernel_fills_gap": 8 * p - 1 in stable_kernel,
    }
    controls = {
        "deleted_stable_endpoint_rejected": len(stable_kernel - {q - 1}) != 18 * p,
        "raised_kernel_floor_rejected": len(closed_interval(6 * p + 1, q - 1)) != 18 * p,
        "filled_variable_gap_rejected": len(high_variables | {8 * p - 1}) != 8 * p,
        "wrong_section_middle_rejected": t_h_vector != [1, 2 * p - 1, 2 * p + 1, 2 * p - 1, 1],
        "kernel_degree_three_drop_rejected": len(degree_three_kernel) != 18 * p - 1,
    }
    if not all(predictions.values()):
        raise AssertionError(f"p={p}: structural prediction failed: {predictions}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: structural mutation survived: {controls}")

    row: dict[str, object] = {
        "p": p,
        "generator_count": len(g),
        "high_variable_count": len(high_variables),
        "high_variable_hash": digest(sorted(high_variables)),
        "stable_kernel_interval": [6 * p, q - 1],
        "stable_kernel_count": len(stable_kernel),
        "c_dimensions_0_to_5": c_dimensions,
        "section_dimensions_0_to_5": t_dimensions,
        "kernel_dimensions_0_to_5": kernel_dimensions,
        "predictions": predictions,
        "controls": controls,
    }
    row["row_hash"] = digest(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    args = parser.parse_args()
    started = time.perf_counter()

    canonical = json.loads(args.canonical.read_text(encoding="utf-8"))
    if canonical.get("status") != "PASS":
        raise RuntimeError("canonical EXP-033 artifact is not PASS")
    canonical_rows = {int(row["p"]): row for row in canonical["rows"]}
    if sorted(canonical_rows) != list(range(4, 301)):
        raise RuntimeError("canonical EXP-033 range is not p=4,...,300")

    coefficient_rows = []
    for p, canonical_row in canonical_rows.items():
        if time.perf_counter() - started > args.budget_seconds:
            raise TimeoutError(f"INCONCLUSIVE_BUDGET while reconstructing p={p}")
        row_three, row_four = independent_strands(p)
        comparisons = {
            "row_three_hash": digest(row_three) == canonical_row["row_three"]["coefficient_hash"],
            "row_four_hash": digest(row_four) == canonical_row["row_four"]["coefficient_hash"],
            "row_three_total": sum(row_three) == canonical_row["row_three"]["total_rank"],
            "row_four_total": sum(row_four) == canonical_row["row_four"]["total_rank"],
            "a_terminal_rank": canonical_row["a_terminal_betti"] == 10 * p,
        }
        if not all(comparisons.values()):
            raise AssertionError(f"p={p}: independent coefficient mismatch: {comparisons}")
        coefficient_rows.append({"p": p, "comparisons": comparisons, "row_hash": digest(comparisons)})

    structural_parameters = list(range(4, 26)) + [50, 100, 300]
    structural_rows = [structural_row(p) for p in structural_parameters]
    result = {
        "experiment": "EXP-033-minimal-cubic-mapping-cone",
        "route": "independent-coefficients-and-structural-kernel",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "INDEPENDENT_AUDIT_PASS",
        "canonical_sha256": hashlib.sha256(args.canonical.read_bytes()).hexdigest(),
        "coefficient_range": {"first": 4, "last": 300, "count": len(coefficient_rows)},
        "coefficient_aggregate": digest(coefficient_rows),
        "structural_parameters": structural_parameters,
        "structural_aggregate": digest([row["row_hash"] for row in structural_rows]),
        "elapsed_seconds": time.perf_counter() - started,
        "coefficient_rows": coefficient_rows,
        "structural_rows": structural_rows,
    }
    result["audit_aggregate"] = digest(
        {
            "canonical_sha256": result["canonical_sha256"],
            "coefficient_aggregate": result["coefficient_aggregate"],
            "structural_aggregate": result["structural_aggregate"],
        }
    )
    write_json_atomic(args.output, result)
    print(
        "EXP-033 independent PASS: "
        f"coefficients={len(coefficient_rows)} structural={len(structural_rows)} "
        f"aggregate={result['audit_aggregate']} elapsed={result['elapsed_seconds']:.3f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
