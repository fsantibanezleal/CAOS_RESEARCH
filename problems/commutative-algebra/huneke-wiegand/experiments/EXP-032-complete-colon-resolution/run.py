"""Canonical exact campaign for the complete EXP-032 colon resolution.

Finite exact checks validate the formulas and implementation.  The every-field
claim depends on the separately written Gorenstein-duality proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-030-colon-idealization-degree-six/proof.md":
        "1822095a7d16207b7d04261b7a6645f7ca51b01f490ba9d212a84ab7ca5bc729",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-030-colon-idealization-degree-six/verdict.md":
        "7f8d2fe3c61a0fc1f864452ca98d05d04e154496a2d45d2c8d8a7b32644de4d9",
}


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def choose(n: int, k: int) -> int:
    return comb(n, k) if 0 <= k <= n else 0


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def verify_premises() -> dict[str, str]:
    observed = {relative: file_hash(ROOT / relative) for relative in PREMISES}
    if observed != PREMISES:
        mismatch = {
            relative: {"expected": PREMISES[relative], "observed": observed[relative]}
            for relative in PREMISES
            if observed[relative] != PREMISES[relative]
        }
        raise RuntimeError(f"INCONCLUSIVE_PREMISE: {mismatch}")
    return observed


def hilbert_numerator(exponent: int, h_linear: int) -> list[int]:
    """Coefficients of (1+h_linear*z+z^2)(1-z)^exponent."""
    h = (1, h_linear, 1)
    return [
        sum(
            h[k] * (-1) ** (degree - k) * choose(exponent, degree - k)
            for k in range(3)
        )
        for degree in range(exponent + 3)
    ]


def linear_rank(codimension: int, homological_degree: int) -> int:
    a = homological_degree
    return (
        codimension * choose(codimension, a)
        - choose(codimension, a + 1)
        - choose(codimension, a - 1)
    )


def reconstruct_numerator(
    codimension: int,
    diagonal: list[int],
    linear: list[int],
    quadratic: list[int],
) -> list[int]:
    result = [0] * (codimension + 3)
    for i, value in enumerate(diagonal):
        result[i] += (-1) ** i * value
    for i, value in enumerate(linear):
        if i + 1 < len(result):
            result[i + 1] += (-1) ** i * value
    for i, value in enumerate(quadratic):
        if i + 2 < len(result):
            result[i + 2] += (-1) ** i * value
    return result


def convolution(left: list[int], right: list[int]) -> list[int]:
    output = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            output[i + j] += x * y
    return output


def parameter_row(parameter: int) -> tuple[dict[str, object], dict[str, object]]:
    if parameter < 4:
        raise ValueError("EXP-032 is declared only for p>=4")
    c = 2 * parameter - 2
    m = 8 * parameter
    total_codimension = c + m

    low_linear = [0] + [linear_rank(c, a) for a in range(1, c)] + [0]
    low_diagonal = [1] + [0] * c
    low_quadratic = [0] * c + [1]
    low_target = hilbert_numerator(c, c)
    low_reconstructed = reconstruct_numerator(c, low_diagonal, low_linear, low_quadratic)

    koszul = [choose(m, t) for t in range(m + 1)]
    full_diagonal = koszul
    full_linear = convolution(low_linear, koszul)
    full_quadratic = convolution(low_quadratic, koszul)
    full_target = hilbert_numerator(total_codimension, c)
    full_reconstructed = reconstruct_numerator(
        total_codimension, full_diagonal, full_linear, full_quadratic
    )

    omitted_top = [0] * (c + 1)
    wrong_sign = low_linear.copy()
    wrong_sign[1] *= -1
    spurious_quadratic = low_quadratic.copy()
    spurious_quadratic[c - 1] = 1
    controls = {
        "wrong_codimension_rejected": low_reconstructed != hilbert_numerator(c + 1, c + 1),
        "omitted_top_rejected": (
            reconstruct_numerator(c, low_diagonal, low_linear, omitted_top) != low_target
        ),
        "wrong_linear_sign_rejected": (
            reconstruct_numerator(c, low_diagonal, wrong_sign, low_quadratic) != low_target
        ),
        "spurious_quadratic_rejected": (
            reconstruct_numerator(c, low_diagonal, low_linear, spurious_quadratic) != low_target
        ),
    }
    checks = {
        "positive_linear_strand": all(value > 0 for value in low_linear[1:c]),
        "linear_strand_symmetric": all(
            low_linear[a] == low_linear[c - a] for a in range(1, c)
        ),
        "known_first_rank": low_linear[1] == parameter * (2 * parameter - 3),
        "known_second_rank": (
            low_linear[2] == 8 * parameter * (parameter - 1) * (parameter - 2) // 3
        ),
        "low_hilbert_reconstruction": low_reconstructed == low_target,
        "full_hilbert_reconstruction": full_reconstructed == full_target,
        "full_gorenstein_symmetry": all(
            full_diagonal[i] == full_quadratic[total_codimension - i]
            for i in range(len(full_diagonal))
        ) and all(
            full_linear[i] == full_linear[total_codimension - i]
            for i in range(1, total_codimension)
        ),
        "projective_dimension": len(full_quadratic) - 1 == 10 * parameter - 2,
        "regularity_two": full_quadratic[-1] == 1,
        "low_total_rank": (
            sum(low_diagonal) + sum(low_linear) + sum(low_quadratic)
            == (c - 2) * 2**c + 4
        ),
        "koszul_total_factor": (
            sum(full_diagonal) + sum(full_linear) + sum(full_quadratic)
            == ((c - 2) * 2**c + 4) * 2**m
        ),
    }
    if not all(checks.values()):
        raise AssertionError(f"p={parameter}: check failed: {checks}")
    if not all(controls.values()):
        raise AssertionError(f"p={parameter}: adversarial control failed: {controls}")

    row: dict[str, object] = {
        "p": parameter,
        "low_codimension": c,
        "killed_variables": m,
        "projective_dimension": total_codimension,
        "regularity": 2,
        "linear_rank_sum": sum(low_linear),
        "low_total_betti_rank": (c - 2) * 2**c + 4,
        "full_total_betti_rank": str(((c - 2) * 2**c + 4) * 2**m),
        "low_linear_hash": canonical_hash(low_linear),
        "full_diagonal_hash": canonical_hash(full_diagonal),
        "full_linear_hash": canonical_hash(full_linear),
        "full_quadratic_hash": canonical_hash(full_quadratic),
        "hilbert_numerator_hash": canonical_hash(full_target),
        "checks": checks,
        "controls": controls,
    }
    row["row_hash"] = canonical_hash(row)
    table: dict[str, object] = {
        "p": parameter,
        "low": {
            "diagonal": low_diagonal,
            "linear": low_linear,
            "quadratic": low_quadratic,
        },
        "over_P": {
            "diagonal": full_diagonal,
            "linear": full_linear,
            "quadratic": full_quadratic,
        },
    }
    return row, table


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-max", type=int, default=300)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    p_max = 4 if args.smoke else args.p_max
    output = args.output or HERE / "artifacts" / (
        "smoke-results.json" if args.smoke else "results.json"
    )
    started = time.perf_counter()
    premises = verify_premises()
    rows = []
    small_tables: dict[str, object] = {}
    for parameter in range(4, p_max + 1):
        row, table = parameter_row(parameter)
        rows.append(row)
        if parameter <= 6:
            small_tables[str(parameter)] = table
        if parameter in (4, 5, 6, 10, 25, 50, 100, 200, p_max):
            print(f"canonical p={parameter}: pd={row['projective_dimension']}", flush=True)
        if time.perf_counter() - started > args.budget_seconds:
            payload = {
                "experiment": "EXP-032-complete-colon-resolution",
                "route": "canonical",
                "status": "INCONCLUSIVE_BUDGET",
                "completed": [item["p"] for item in rows],
                "elapsed_seconds": time.perf_counter() - started,
            }
            write_json_atomic(output, payload)
            return 2
    payload: dict[str, object] = {
        "experiment": "EXP-032-complete-colon-resolution",
        "route": "canonical",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "range": [4, p_max],
        "premise_hashes": premises,
        "rows": rows,
        "small_tables": small_tables,
        "claim_boundary": (
            "Exact finite checks support the formula; the all-field theorem uses the "
            "separate Gorenstein-duality proof and does not determine the resolution of C_p."
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }
    payload["canonical_aggregate"] = canonical_hash([row["row_hash"] for row in rows])
    write_json_atomic(output, payload)
    print(f"PASS aggregate={payload['canonical_aggregate']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
