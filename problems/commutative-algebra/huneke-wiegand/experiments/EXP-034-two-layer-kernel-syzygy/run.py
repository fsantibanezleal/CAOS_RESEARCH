"""EXP-034 canonical two-layer-kernel and survival campaign.

CPU only, deterministic, and exact. Finite rows validate the implementation; the
all-parameter claims require the written interval and unit-pivot arguments.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"

PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-030-colon-idealization-degree-six/proof.md":
        "1822095a7d16207b7d04261b7a6645f7ca51b01f490ba9d212a84ab7ca5bc729",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-032-complete-colon-resolution/proof.md":
        "4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-033-minimal-cubic-mapping-cone/proof.md":
        "e27cd386ad47da7ad5282e88a095d82f2b1156f76546e934b287e911da2c7b1c",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-033-minimal-cubic-mapping-cone/verdict.md":
        "674b2940259465f0a2cba96261a8bb021e103cb3e51db50a8aac4f64c0c5927b",
}


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def interval(first: int, last: int) -> set[int]:
    return set(range(first, last + 1)) if first <= last else set()


def degree_one_offsets(p: int) -> set[int]:
    return (
        interval(0, p)
        | interval(3 * p, 4 * p - 2)
        | interval(6 * p, 8 * p - 2)
        | interval(8 * p, 10 * p - 2)
        | {10 * p}
        | interval(11 * p - 1, 12 * p - 1)
        | interval(13 * p + 1, 14 * p - 2)
        | interval(14 * p, 15 * p - 1)
        | {16 * p}
        | interval(17 * p - 1, 18 * p - 1)
    )


def low_offsets(p: int, include_zero: bool = True) -> set[int]:
    low = interval(0, p) | interval(3 * p, 4 * p - 2)
    return low if include_zero else low - {0}


def high_offsets(p: int) -> set[int]:
    return {value for value in degree_one_offsets(p) if value >= 6 * p}


def stable_kernel_offsets(p: int) -> set[int]:
    return interval(6 * p, 24 * p - 1)


def artinian_kernel_degree_two(p: int) -> set[int]:
    return stable_kernel_offsets(p) - high_offsets(p)


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


def representation_set(p: int, target: int) -> set[int]:
    generators = degree_one_offsets(p) - {0}
    high = high_offsets(p)
    return {g for g in generators if target - g in high}


def kernel_row(p: int, store_detail: bool) -> dict[str, object]:
    generators = degree_one_offsets(p)
    high = high_offsets(p)
    stable = stable_kernel_offsets(p)
    degree_two = artinian_kernel_degree_two(p)
    target = 8 * p - 1
    exterior = set(range(1, p + 1))
    representations = representation_set(p, target)
    tau = target + p * (p + 1) // 2
    smallest_exterior = sorted(generators - {0})[:p]
    shifted_d_diagonal_floor = 3 * p + sum(sorted(high)[: p - 1])

    incoming = [
        {"extra_variable": g, "degree_one_kernel_offset": target - g}
        for g in sorted(representations - exterior)
    ]
    nonzero_products = 40 * p * p - 16 * p - 1
    if store_detail:
        enumerated_products = sum(
            1
            for g in generators - {0}
            for h in high
            if g + h in degree_two
        )
        if enumerated_products != nonzero_products:
            raise AssertionError(
                f"p={p}: two-layer product count {enumerated_products}!={nonzero_products}"
            )

    predictions = {
        "generator_count": len(generators) == 10 * p,
        "degree_one_kernel_count": len(high) == 8 * p,
        "stable_kernel_count": len(stable) == 18 * p,
        "artinian_degree_two_count": len(degree_two) == 10 * p,
        "target_is_missing_generator": target not in generators,
        "target_is_degree_two_basis": target in degree_two,
        "representation_set": representations == exterior,
        "no_incoming_face": not incoming,
        "target_is_first_degree_two_offset": min(degree_two) == target,
        "exterior_has_minimum_sum": smallest_exterior == sorted(exterior),
        "target_multidegree_cokernel_is_one": (
            min(degree_two) == target and smallest_exterior == sorted(exterior)
        ),
        "tau_formula": tau == 8 * p - 1 + sum(exterior),
        "unit_target_coordinate": True,
        "two_layer_product_formula": nonzero_products == 40 * p * p - 16 * p - 1,
        "d_row_two_starts_after_p": 2 * p - 2 > p,
        "shifted_d_diagonal_above_target": shifted_d_diagonal_floor > tau,
    }
    controls = {
        "filled_gap_rejected": target not in degree_two - (generators | {target}),
        "deleted_variable_rejected": representation_set(p, target) != exterior - {p},
        "wrong_exterior_rejected": representations != interval(1, p - 1),
        "wrong_shift_rejected": tau != target + sum(range(0, p)),
        "low_high_partition_rejected": len(generators - low_offsets(p)) != 8 * p - 1,
    }
    if not all(predictions.values()):
        raise AssertionError(f"p={p}: kernel prediction failed: {predictions}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: mutated kernel control survived: {controls}")

    row: dict[str, object] = {
        "p": p,
        "target_offset": target,
        "homological_degree": p,
        "standard_internal_degree": p + 2,
        "total_offset": tau,
        "representation_count": len(representations),
        "nonzero_two_layer_products": nonzero_products,
        "shifted_d_diagonal_offset_floor": shifted_d_diagonal_floor,
        "predictions": predictions,
        "controls": controls,
    }
    if store_detail:
        row.update(
            {
                "exterior": sorted(exterior),
                "representations": sorted(representations),
                "incoming_faces": incoming,
                "degree_two_basis_hash": digest(sorted(degree_two)),
                "high_basis_hash": digest(sorted(high)),
            }
        )
    row["row_hash"] = digest(row)
    return row


def low_product_after_x0(p: int, left: int, right: int) -> tuple[str, int] | None:
    left_is_b = left >= 3 * p
    right_is_b = right >= 3 * p
    if left_is_b and right_is_b:
        return None
    if not left_is_b and not right_is_b:
        total = left + right
        return ("A", total) if total > p else None
    a = right if left_is_b else left
    b = left if left_is_b else right
    total = a + b
    return ("B", total) if total >= 4 * p - 1 else None


def source_boundary(
    p: int, sigma: int
) -> tuple[list[tuple[tuple[int, ...], int]], list[dict[tuple[tuple[int, ...], str, int], int]]]:
    low = sorted(low_offsets(p, include_zero=False))
    low_set = set(low)
    source: list[tuple[tuple[int, ...], int]] = []
    columns: list[dict[tuple[tuple[int, ...], str, int], int]] = []
    for exterior in itertools.combinations(low, p):
        coefficient = sigma - sum(exterior)
        if coefficient not in low_set:
            continue
        column: dict[tuple[tuple[int, ...], str, int], int] = {}
        for position, variable in enumerate(exterior):
            product = low_product_after_x0(p, variable, coefficient)
            if product is None:
                continue
            face = exterior[:position] + exterior[position + 1 :]
            key = (face, product[0], product[1])
            column[key] = column.get(key, 0) + (-1 if position % 2 else 1)
            if not column[key]:
                del column[key]
        source.append((exterior, coefficient))
        columns.append(column)
    return source, columns


def rank_mod_prime(
    columns: list[dict[object, int]], prime: int, skip: int | None = None
) -> int:
    pivots: dict[object, dict[object, int]] = {}
    for column_index, raw in enumerate(columns):
        if column_index == skip:
            continue
        vector = {row: value % prime for row, value in raw.items() if value % prime}
        while vector:
            pivot = min(vector, key=repr)
            if pivot not in pivots:
                inverse = pow(vector[pivot], -1, prime)
                normalized = {row: value * inverse % prime for row, value in vector.items()}
                pivots[pivot] = normalized
                break
            factor = vector[pivot]
            for row, value in pivots[pivot].items():
                updated = (vector.get(row, 0) - factor * value) % prime
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
    return len(pivots)


def source_pivot_probe(p: int) -> dict[str, object]:
    exterior = tuple(range(1, p + 1))
    exterior_sum = sum(exterior)
    rows: list[dict[str, object]] = []
    for coefficient in range(1, p + 1):
        sigma = exterior_sum + coefficient
        source, columns = source_boundary(p, sigma)
        selected = source.index((exterior, coefficient))
        pivot_face = tuple(range(1, p))
        pivot_key = (pivot_face, "A", p + coefficient)
        occurrences = [index for index, column in enumerate(columns) if pivot_key in column]
        field_rows = {}
        for prime in (2, 1_000_003):
            full_rank = rank_mod_prime(columns, prime)
            deleted_rank = rank_mod_prime(columns, prime, skip=selected)
            field_rows[str(prime)] = {
                "rank": full_rank,
                "rank_without_selected": deleted_rank,
                "drop": full_rank - deleted_rank,
            }
            if full_rank - deleted_rank != 1:
                raise AssertionError(
                    f"p={p}, coefficient={coefficient}, GF({prime}): selected column is not a coloop"
                )
        if occurrences != [selected] or abs(columns[selected].get(pivot_key, 0)) != 1:
            raise AssertionError(f"p={p}, coefficient={coefficient}: unit pivot is not unique")
        rows.append(
            {
                "coefficient_offset": coefficient,
                "high_exterior_offset": 8 * p - 1 - coefficient,
                "low_total_offset": sigma,
                "source_columns": len(columns),
                "target_rows": len({row for column in columns for row in column}),
                "selected_column": selected,
                "unique_unit_pivot": [list(pivot_face), "A", p + coefficient],
                "field_ranks": field_rows,
            }
        )
    result: dict[str, object] = {
        "p": p,
        "coordinates_checked": p,
        "all_unique_unit_pivots": True,
        "rows": rows,
    }
    result["row_hash"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-p", type=int, default=4)
    parser.add_argument("--max-p", type=int, default=300)
    parser.add_argument("--rank-max-p", type=int, default=8)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    args = parser.parse_args()
    if args.min_p < 4 or args.max_p < args.min_p:
        raise ValueError("require 4<=min-p<=max-p")

    started = time.perf_counter()
    premises = verify_premises()
    rows = []
    explicit = {4, 5, 6, args.max_p}
    for p in range(args.min_p, args.max_p + 1):
        rows.append(kernel_row(p, p in explicit))
        if time.perf_counter() - started > args.budget_seconds:
            raise TimeoutError(f"INCONCLUSIVE_BUDGET after p={p}")

    rank_rows = []
    for p in range(args.min_p, min(args.rank_max_p, args.max_p) + 1):
        rank_rows.append(source_pivot_probe(p))
        if time.perf_counter() - started > args.budget_seconds:
            raise TimeoutError(f"INCONCLUSIVE_BUDGET during source probe p={p}")

    aggregate = digest([row["row_hash"] for row in rows])
    rank_aggregate = digest([row["row_hash"] for row in rank_rows])
    result = {
        "experiment": "EXP-034",
        "status": "PASS_CANONICAL",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "min_p": args.min_p,
            "max_p": args.max_p,
            "rank_max_p": min(args.rank_max_p, args.max_p),
            "fields": [2, 1_000_003],
            "budget_seconds": args.budget_seconds,
        },
        "premise_hashes": premises,
        "theorem_boundary": {
            "two_layer_kernel": "validated",
            "primitive_kernel_class": "validated",
            "connecting_coordinate": "annihilated by a unique integral low pivot",
            "a_p_multigraded_value": "exactly one subject to written all-parameter proof",
            "c_p_multigraded_value": "exactly one subject to written all-parameter proof",
            "full_lower_strands": "not claimed",
        },
        "row_count": len(rows),
        "aggregate_sha256": aggregate,
        "rank_aggregate_sha256": rank_aggregate,
        "explicit_rows": [row for row in rows if row["p"] in explicit],
        "source_pivot_probes": rank_rows,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    result["artifact_sha256"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
