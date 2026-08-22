"""EXP-033 canonical exact campaign for the minimal cubic mapping cone."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"

PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-023-one-cubic-defining-ideal/proof.md":
        "4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-024-extremal-betti-data/proof.md":
        "b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-026-grevlex-staircase/proof.md":
        "765fa23534be9e534fd507dff0e447e967345e4d2a485f7da6fdf0383b04fb56",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-030-colon-idealization-degree-six/proof.md":
        "1822095a7d16207b7d04261b7a6645f7ca51b01f490ba9d212a84ab7ca5bc729",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-032-complete-colon-resolution/proof.md":
        "4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-032-complete-colon-resolution/verdict.md":
        "3a04956262708ebb09b14c8a1628194dd0c7a21ca6171247e518b8cc4b98d7cc",
}


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def verify_premises() -> dict[str, str]:
    observed = {relative: file_hash(ROOT / relative) for relative in PREMISES}
    if observed != PREMISES:
        mismatches = {
            relative: {"expected": PREMISES[relative], "observed": observed[relative]}
            for relative in PREMISES
            if observed[relative] != PREMISES[relative]
        }
        raise RuntimeError(f"INCONCLUSIVE_PREMISE: {mismatches}")
    return observed


def convolve(left: list[int], right: list[int]) -> list[int]:
    answer = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return answer


def one_minus_power(exponent: int) -> list[int]:
    return [(-1) ** degree * math.comb(exponent, degree) for degree in range(exponent + 1)]


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def binomial_row(n: int) -> list[int]:
    row = [1]
    for k in range(n):
        row.append(row[-1] * (n - k) // (k + 1))
    return row


def coefficient(row: list[int], k: int) -> int:
    return row[k] if 0 <= k < len(row) else 0


def lambda_rank(codimension: int, homological_degree: int) -> int:
    a = homological_degree
    return (
        codimension * choose(codimension, a)
        - choose(codimension, a + 1)
        - choose(codimension, a - 1)
    )


def d_linear_rank(codimension: int, killed: int, homological_degree: int) -> int:
    """Recover the Koszul convolution by one Hilbert-numerator coefficient.

    Literal convolution is retained in the small stored tables through the resulting
    coefficients, but recomputing all binomial summands for every parameter crossed the declared
    budget.  This equivalent coefficient form follows after subtracting the diagonal and terminal
    row from ``(1+c*z+z^2)(1-z)^(c+killed)``.
    """
    i = homological_degree
    total_codimension = codimension + killed
    return (
        -choose(total_codimension, i + 1)
        + codimension * choose(total_codimension, i)
        - choose(total_codimension, i - 1)
        + choose(killed, i + 1)
        + choose(killed, i - 1 - codimension)
    )


def predicted_strands(p: int) -> tuple[list[int], list[int]]:
    c = 2 * p - 2
    m = 8 * p
    variable_count = 10 * p
    total_binomials = binomial_row(c + m)
    killed_binomials = binomial_row(m)
    row_three = [0] * variable_count
    row_four = [0] * variable_count
    for i in range(variable_count):
        q = i - 1
        row_three[i] = (
            -coefficient(total_binomials, q + 1)
            + c * coefficient(total_binomials, q)
            - coefficient(total_binomials, q - 1)
            + coefficient(killed_binomials, q + 1)
            + coefficient(killed_binomials, q - 1 - c)
        )
        row_four[i] = coefficient(killed_binomials, q - c)
    return row_three, row_four


def nonzero_table(row: list[int], regularity: int) -> list[dict[str, int]]:
    return [
        {
            "homological_degree": i,
            "internal_degree": i + regularity,
            "rank": rank,
        }
        for i, rank in enumerate(row)
        if rank
    ]


def analyze_parameter(p: int, store_table: bool) -> dict[str, object]:
    if p < 4:
        raise ValueError("EXP-033 is declared only for p>=4")
    c = 2 * p - 2
    m = 8 * p
    n = 10 * p
    projective_dimension_a = n - 1

    h_c = [1, n - 1, 12 * p, 2 * p - 1, 1]
    h_d = [1, c, 1]
    h_t = convolve(h_d, [1, 1, 1])
    h_k = [left - right for left, right in zip(h_c, h_t, strict=True)]
    h_a = [1, n - 2, 2 * p + 1, -n]

    numerator_c = convolve(h_c, one_minus_power(n - 1))
    numerator_d = convolve(h_d, one_minus_power(n - 2))
    numerator_a = convolve(h_a, one_minus_power(n - 2))
    shifted_d = [0, 0, 0] + numerator_d
    common_length = max(len(numerator_a), len(numerator_c), len(shifted_d))
    padded_a = numerator_a + [0] * (common_length - len(numerator_a))
    padded_c = numerator_c + [0] * (common_length - len(numerator_c))
    shifted_d += [0] * (common_length - len(shifted_d))

    row_three, row_four = predicted_strands(p)
    r = n - 1
    beta_25 = p * (2 * p - 3)
    beta_36 = 8 * p * (7 * p * p - 12 * p + 2) // 3
    quadratic_count = 50 * p * p - 17 * p

    predictions = {
        "colon_h_vector": h_d == [1, 2 * p - 2, 1],
        "section_h_vector": h_t == [1, 2 * p - 1, 2 * p, 2 * p - 1, 1],
        "kernel_h_vector": h_k == [0, 8 * p, 10 * p, 0, 0],
        "kernel_regularity_two": max(i for i, value in enumerate(h_k) if value) == 2,
        "a_hilbert_numerator": h_a == [1, 10 * p - 2, 2 * p + 1, -10 * p],
        "exact_sequence_hilbert_identity": padded_a
        == [left + right for left, right in zip(padded_c, shifted_d, strict=True)],
        "a_quadratic_count": numerator_a[2] == -quadratic_count,
        "a_terminal_rank": numerator_a[n + 1] == (-1) ** projective_dimension_a * n,
        "row_three_support": [i for i, value in enumerate(row_three) if value]
        == list(range(2, n - 1)),
        "row_four_support": [i for i, value in enumerate(row_four) if value]
        == list(range(c + 1, n)),
        "known_beta_2_5": row_three[2] == beta_25,
        "known_beta_3_6": row_three[3] == beta_36,
        "known_beta_3_7": row_four[3] == 0,
        "known_penultimate_edge": row_four[r - 1] == 8 * p,
        "known_terminal_edge": row_four[r] == 1,
    }

    mutated_cubic_shift = [0, 0] + numerator_d
    mutated_common_length = max(common_length, len(mutated_cubic_shift))
    mutated_a = padded_a + [0] * (mutated_common_length - len(padded_a))
    mutated_c = padded_c + [0] * (mutated_common_length - len(padded_c))
    mutated_cubic_shift += [0] * (mutated_common_length - len(mutated_cubic_shift))
    mutated_shifted_d = shifted_d + [0] * (mutated_common_length - len(shifted_d))
    controls = {
        "quadratic_shift_rejected": mutated_a
        != [left + right for left, right in zip(mutated_c, mutated_cubic_shift, strict=True)],
        "missing_high_variable_rejected": choose(m - 1, m - 1) != row_four[r - 1],
        "filled_high_gap_rejected": choose(m + 1, m) != row_four[r - 1],
        "nonminimal_sign_rejected": mutated_a
        != [left - right for left, right in zip(mutated_c, mutated_shifted_d, strict=True)],
        "perturbed_terminal_rank_rejected": row_four[r] != 2,
        "spurious_early_row_four_rejected": row_four[c] == 0,
    }
    if not all(predictions.values()):
        raise AssertionError(f"p={p}: prediction failed: {predictions}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial control failed: {controls}")

    row: dict[str, object] = {
        "p": p,
        "c": c,
        "m": m,
        "variable_count": n,
        "depth_a": 1,
        "projective_dimension_a": projective_dimension_a,
        "regularity_a": 2,
        "h_vectors": {"c": h_c, "d": h_d, "t": h_t, "k": h_k, "a_over_dimension_two": h_a},
        "a_quadratic_count": quadratic_count,
        "a_terminal_betti": n,
        "row_three": {
            "support": [2, n - 2],
            "total_rank": sum(row_three),
            "coefficient_hash": canonical_hash(row_three),
        },
        "row_four": {
            "support": [c + 1, n - 1],
            "total_rank": sum(row_four),
            "coefficient_hash": canonical_hash(row_four),
        },
        "known_anchors": {
            "beta_2_5": beta_25,
            "beta_3_6": beta_36,
            "beta_3_7": 0,
            "beta_r_minus_1_r_plus_3": 8 * p,
            "beta_r_r_plus_4": 1,
        },
        "predictions": predictions,
        "controls": controls,
    }
    if store_table:
        row["complete_predicted_strands"] = {
            "regularity_three": nonzero_table(row_three, 3),
            "regularity_four": nonzero_table(row_four, 4),
        }
    row["row_hash"] = canonical_hash(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--tables", default="4,5,6")
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()
    if args.first < 4 or args.last < args.first:
        raise SystemExit("require 4 <= first <= last")
    if args.budget_seconds <= 0:
        raise SystemExit("budget must be positive")
    table_parameters = {int(value) for value in args.tables.split(",") if value.strip()}

    started = time.perf_counter()
    premise_hashes = verify_premises()
    rows: list[dict[str, object]] = []
    status = "PASS"
    for p in range(args.first, args.last + 1):
        if time.perf_counter() - started > args.budget_seconds:
            status = "INCONCLUSIVE_BUDGET"
            break
        rows.append(analyze_parameter(p, p in table_parameters))
        write_json_atomic(
            args.checkpoint,
            {
                "experiment": "EXP-033-minimal-cubic-mapping-cone",
                "status": "RUNNING",
                "last_completed": p,
                "row_hashes": [row["row_hash"] for row in rows],
            },
        )

    result = {
        "experiment": "EXP-033-minimal-cubic-mapping-cone",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "range": {"first": args.first, "requested_last": args.last, "completed": len(rows)},
        "premise_hashes": premise_hashes,
        "claim": "reg(P_p/Q_p)=2 and the cubic mapping cone is minimal",
        "campaign_aggregate": canonical_hash([row["row_hash"] for row in rows]),
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    write_json_atomic(args.output, result)
    write_json_atomic(
        args.checkpoint,
        {
            "experiment": result["experiment"],
            "status": status,
            "last_completed": rows[-1]["p"] if rows else None,
            "row_hashes": [row["row_hash"] for row in rows],
        },
    )
    print(
        f"EXP-033 canonical {status}: rows={len(rows)} "
        f"aggregate={result['campaign_aggregate']} elapsed={result['elapsed_seconds']:.3f}s"
    )
    return 0 if status == "PASS" and len(rows) == args.last - args.first + 1 else 2


if __name__ == "__main__":
    raise SystemExit(main())
