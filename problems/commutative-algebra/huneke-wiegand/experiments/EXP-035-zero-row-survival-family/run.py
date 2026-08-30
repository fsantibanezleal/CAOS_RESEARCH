"""EXP-035 canonical zero-row classification and connecting-source probes.

CPU only, deterministic, and exact. Finite ranks validate the implementation.
The all-parameter conclusions require the written set-containment and pivot proofs.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"

PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-032-complete-colon-resolution/proof.md":
        "4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-033-minimal-cubic-mapping-cone/proof.md":
        "e27cd386ad47da7ad5282e88a095d82f2b1156f76546e934b287e911da2c7b1c",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-034-two-layer-kernel-syzygy/proof.md":
        "0d0a87b0a5fd4e3bbb5570e3e664eb59fcf8d07222abd62c48bdae9d20d61b4a",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-034-two-layer-kernel-syzygy/verdict.md":
        "ebbf52a0b2d85b0bb5c71ca6fb48846d17b1d91644e48e69dbc3a5e8a5f81304",
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


def low_offsets(p: int) -> set[int]:
    return interval(1, p) | interval(3 * p, 4 * p - 2)


def high_offsets(p: int) -> set[int]:
    return {value for value in degree_one_offsets(p) if value >= 6 * p}


def degree_two_offsets(p: int) -> set[int]:
    return interval(6 * p, 24 * p - 1) - high_offsets(p)


def representation_set(p: int, target: int) -> set[int]:
    high = high_offsets(p)
    return {g for g in degree_one_offsets(p) - {0} if target - g in high}


def generator_blocks(p: int) -> list[tuple[int, int]]:
    return [
        (1, p),
        (3 * p, 4 * p - 2),
        (6 * p, 8 * p - 2),
        (8 * p, 10 * p - 2),
        (10 * p, 10 * p),
        (11 * p - 1, 12 * p - 1),
        (13 * p + 1, 14 * p - 2),
        (14 * p, 15 * p - 1),
        (16 * p, 16 * p),
        (17 * p - 1, 18 * p - 1),
    ]


def high_blocks(p: int) -> list[tuple[int, int]]:
    return generator_blocks(p)[2:]


def representation_count(p: int, target: int) -> int:
    count = 0
    for generator_first, generator_last in generator_blocks(p):
        for high_first, high_last in high_blocks(p):
            first = max(generator_first, target - high_last)
            last = min(generator_last, target - high_first)
            count += max(0, last - first + 1)
    return count


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


def predicted_family(p: int, t: int) -> tuple[int, set[int], int, int]:
    target = 10 * p + t
    exterior = interval(3 * p, 4 * p - 2) | {t} | interval(t + 2, p)
    homological_degree = 2 * p - t - 1
    total_offset = 4 * p * p + 6 * p - t * (t - 1) // 2
    return target, exterior, homological_degree, total_offset


def zero_rank(
    p: int, homological_degree: int, representation_histogram: dict[int, int]
) -> int:
    variable_count = 10 * p - 1
    return sum(
        count * math.comb(variable_count - size, homological_degree - size)
        for size, count in representation_histogram.items()
        if size <= homological_degree
    )


def classification_row(p: int, store_detail: bool) -> dict[str, object]:
    degree_two = degree_two_offsets(p)
    representation_counts = {
        target: representation_count(p, target) for target in degree_two
    }
    histogram: dict[int, int] = {}
    for key in representation_counts.values():
        histogram[key] = histogram.get(key, 0) + 1

    candidates = []
    for t in range(2, p - 1):
        target, exterior, degree, total_offset = predicted_family(p, t)
        observed = representation_set(p, target)
        checks = {
            "representation_formula": observed == exterior,
            "interval_count_matches_literal": representation_counts[target] == len(observed),
            "cardinality_formula": len(observed) == degree,
            "below_d_row_two": degree < 2 * p - 2,
            "offset_formula": target + sum(exterior) == total_offset,
            "zero_row": not observed - exterior,
            "deleted_member_creates_incoming": bool(observed - (exterior - {min(exterior)})),
        }
        if not all(checks.values()):
            raise AssertionError(f"p={p}, t={t}: candidate classification failed: {checks}")
        candidates.append(
            {
                "t": t,
                "target_offset": target,
                "homological_degree": degree,
                "total_offset": total_offset,
                "representation_count": len(observed),
                "zero_rank_lower_bound_at_degree": zero_rank(p, degree, histogram),
                "checks": checks,
                **({"representations": sorted(observed)} if store_detail else {}),
            }
        )

    first_target = 8 * p - 1
    first_representations = representation_set(p, first_target)
    checks = {
        "generator_count": len(degree_one_offsets(p)) == 10 * p,
        "high_count": len(high_offsets(p)) == 8 * p,
        "degree_two_count": len(degree_two) == 10 * p,
        "all_rows_classified": len(representation_counts) == 10 * p,
        "histogram_count": sum(histogram.values()) == 10 * p,
        "exp034_recovered": first_representations == interval(1, p),
        "candidate_count": len(candidates) == p - 3,
        "candidate_degrees_consecutive": (
            sorted(item["homological_degree"] for item in candidates)
            == list(range(p + 1, 2 * p - 2))
        ),
    }
    if store_detail:
        checks["literal_counts_match"] = all(
            count == len(representation_set(p, target))
            for target, count in representation_counts.items()
        )
    if not all(checks.values()):
        raise AssertionError(f"p={p}: classification failed: {checks}")

    row: dict[str, object] = {
        "p": p,
        "representation_size_histogram": dict(sorted(histogram.items())),
        "minimum_representation_size": min(representation_counts.values()),
        "minimum_cells": [
            target
            for target, count in sorted(representation_counts.items())
            if count == min(representation_counts.values())
        ],
        "candidate_count": len(candidates),
        "candidates": candidates,
        "checks": checks,
        "representation_size_profile_hash": digest(
            [[target, representation_counts[target]] for target in sorted(representation_counts)]
        ),
    }
    row["row_hash"] = digest(row)
    return row


def low_product(p: int, left: int, right: int) -> tuple[str, int] | None:
    left_second = left >= 3 * p
    right_second = right >= 3 * p
    if left_second and right_second:
        return None
    total = left + right
    if not left_second and not right_second:
        return ("A", total) if total > p else None
    return ("B", total) if total >= 4 * p - 1 else None


def source_boundary(
    p: int, exterior_size: int, total_offset: int
) -> tuple[list[tuple[tuple[int, ...], int]], list[dict[tuple[tuple[int, ...], str, int], int]]]:
    low = sorted(low_offsets(p))
    low_set = set(low)
    sources: list[tuple[tuple[int, ...], int]] = []
    columns: list[dict[tuple[tuple[int, ...], str, int], int]] = []
    for exterior in itertools.combinations(low, exterior_size):
        coefficient = total_offset - sum(exterior)
        if coefficient not in low_set:
            continue
        column: dict[tuple[tuple[int, ...], str, int], int] = {}
        for position, variable in enumerate(exterior):
            product = low_product(p, variable, coefficient)
            if product is None:
                continue
            face = exterior[:position] + exterior[position + 1 :]
            key = (face, product[0], product[1])
            column[key] = column.get(key, 0) + (-1 if position % 2 else 1)
            if not column[key]:
                del column[key]
        sources.append((exterior, coefficient))
        columns.append(column)
    return sources, columns


def rank_mod_prime(columns: list[dict[object, int]], prime: int, skip: int | None = None) -> int:
    pivots: dict[object, dict[object, int]] = {}
    for column_index, raw in enumerate(columns):
        if column_index == skip:
            continue
        vector = {row: value % prime for row, value in raw.items() if value % prime}
        while vector:
            pivot = min(vector, key=repr)
            if pivot not in pivots:
                inverse = pow(vector[pivot], -1, prime)
                pivots[pivot] = {row: value * inverse % prime for row, value in vector.items()}
                break
            factor = vector[pivot]
            for row, value in pivots[pivot].items():
                updated = (vector.get(row, 0) - factor * value) % prime
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
    return len(pivots)


def integral_dependency(
    columns: list[dict[object, int]], selected: int
) -> list[dict[str, object]] | None:
    rows = sorted({row for column in columns for row in column}, key=repr)
    other_indices = [index for index in range(len(columns)) if index != selected]
    matrix = sympy.Matrix(
        [[columns[index].get(row, 0) for index in other_indices] for row in rows]
    )
    target = sympy.Matrix([columns[selected].get(row, 0) for row in rows])
    try:
        solution, parameters = matrix.gauss_jordan_solve(target)
    except ValueError:
        return None
    substitutions = {parameter: 0 for parameter in parameters}
    solution = solution.subs(substitutions)
    if matrix * solution != target:
        raise AssertionError("rational dependency reconstruction failed")
    denominators = [sympy.denom(value) for value in solution]
    scale = int(sympy.ilcm(*[int(value) for value in denominators])) if denominators else 1
    coefficients = {selected: scale}
    for index, value in zip(other_indices, solution, strict=True):
        coefficient = -int(value * scale)
        if coefficient:
            coefficients[index] = coefficient
    common = abs(math.gcd(*coefficients.values()))
    coefficients = {index: value // common for index, value in coefficients.items()}
    for row in rows:
        if sum(value * columns[index].get(row, 0) for index, value in coefficients.items()):
            raise AssertionError("integral cycle verification failed")
    return [
        {
            "source_index": index,
            "coefficient": coefficients[index],
        }
        for index in sorted(coefficients)
    ]


def connecting_probe(p: int, t: int) -> dict[str, object]:
    target, exterior_set, degree, total_offset = predicted_family(p, t)
    exterior = tuple(sorted(exterior_set))
    rows = []
    all_coloops = True
    first_cycle = None
    for coefficient in exterior:
        low_total = sum(exterior) + coefficient
        sources, columns = source_boundary(p, degree, low_total)
        selected = sources.index((exterior, coefficient))
        field_rows = {}
        for prime in (2, 1_000_003):
            full_rank = rank_mod_prime(columns, prime)
            deleted_rank = rank_mod_prime(columns, prime, skip=selected)
            field_rows[str(prime)] = {
                "rank": full_rank,
                "rank_without_selected": deleted_rank,
                "drop": full_rank - deleted_rank,
            }
        is_coloop = all(item["drop"] == 1 for item in field_rows.values())
        if not is_coloop and first_cycle is None:
            dependency = integral_dependency(columns, selected)
            first_cycle = {
                "coefficient_offset": coefficient,
                "sources": [
                    {"exterior": list(source[0]), "coefficient": source[1]}
                    for source in sources
                ],
                "integral_cycle": dependency,
            }
        all_coloops = all_coloops and is_coloop
        rows.append(
            {
                "coefficient_offset": coefficient,
                "low_total_offset": low_total,
                "source_columns": len(columns),
                "target_rows": len({row for column in columns for row in column}),
                "selected_column": selected,
                "selected_is_coloop": is_coloop,
                "field_ranks": field_rows,
            }
        )
    result: dict[str, object] = {
        "p": p,
        "t": t,
        "target_offset": target,
        "homological_degree": degree,
        "total_offset": total_offset,
        "coordinates_checked": len(exterior),
        "all_selected_columns_are_coloops": all_coloops,
        "first_integral_cycle": first_cycle,
        "rows": rows,
    }
    result["row_hash"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-p", type=int, default=4)
    parser.add_argument("--max-p", type=int, default=300)
    parser.add_argument("--connecting-max-p", type=int, default=8)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    args = parser.parse_args()
    if args.min_p < 4 or args.max_p < args.min_p:
        raise ValueError("require 4<=min-p<=max-p")

    started = time.perf_counter()
    premises = verify_premises()
    print("premise gate: PASS", flush=True)
    rows = []
    explicit = {4, 5, 6, args.max_p}
    literal_detail = {4, 5, 6}
    for p in range(args.min_p, args.max_p + 1):
        rows.append(classification_row(p, p in literal_detail))
        if p in explicit:
            print(f"classification p={p}: PASS", flush=True)
        if time.perf_counter() - started > args.budget_seconds:
            raise TimeoutError(f"INCONCLUSIVE_BUDGET during classification p={p}")

    connecting_rows = []
    connecting_limit = min(args.connecting_max_p, args.max_p)
    for p in range(args.min_p, connecting_limit + 1):
        for t in range(2, p - 1):
            probe = connecting_probe(p, t)
            connecting_rows.append(probe)
            status = "COLOOP" if probe["all_selected_columns_are_coloops"] else "CYCLE"
            print(f"connecting p={p}, t={t}: {status}", flush=True)
            if time.perf_counter() - started > args.budget_seconds:
                raise TimeoutError(f"INCONCLUSIVE_BUDGET during connecting p={p}, t={t}")

    p3_passed = all(row["all_selected_columns_are_coloops"] for row in connecting_rows)
    result = {
        "experiment": "EXP-035",
        "status": "PASS_SMOKE" if p3_passed else "P3_REFUTED_SMOKE",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "min_p": args.min_p,
            "max_p": args.max_p,
            "connecting_max_p": connecting_limit,
            "fields": [2, 1_000_003],
            "budget_seconds": args.budget_seconds,
        },
        "premise_hashes": premises,
        "theorem_boundary": {
            "zero_row_classification": "finite implementation validation",
            "primitive_coordinate_formula": "finite implementation validation",
            "consecutive_connecting_survival": (
                "finite probes pass" if p3_passed else "refuted by persisted integral cycle"
            ),
            "all_parameter_claim": "requires written symbolic proof",
            "complete_lower_strands": "not claimed",
        },
        "classification_row_count": len(rows),
        "classification_aggregate_sha256": digest([row["row_hash"] for row in rows]),
        "explicit_classification_rows": [row for row in rows if row["p"] in explicit],
        "connecting_probe_count": len(connecting_rows),
        "connecting_aggregate_sha256": digest(
            [row["row_hash"] for row in connecting_rows]
        ),
        "connecting_probes": connecting_rows,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    result["artifact_sha256"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
