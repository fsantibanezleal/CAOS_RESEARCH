"""EXP-036 exact-sum torsion screen and integral residual localization.

CPU only. All decisive ranks are exact over explicit prime fields. The target
constructor enumerates only fixed-cardinality subsets at permitted sums.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import sympy
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ


HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
EXP035 = HERE.parent / "EXP-035-zero-row-survival-family"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
PRIMES = (2, 3, 1_000_003)
PREMISES = {
    "EXP-032 proof": (
        HERE.parent / "EXP-032-complete-colon-resolution" / "proof.md",
        "4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c",
    ),
    "EXP-033 proof": (
        HERE.parent / "EXP-033-minimal-cubic-mapping-cone" / "proof.md",
        "e27cd386ad47da7ad5282e88a095d82f2b1156f76546e934b287e911da2c7b1c",
    ),
    "EXP-034 proof": (
        HERE.parent / "EXP-034-two-layer-kernel-syzygy" / "proof.md",
        "0d0a87b0a5fd4e3bbb5570e3e664eb59fcf8d07222abd62c48bdae9d20d61b4a",
    ),
    "EXP-034 verdict": (
        HERE.parent / "EXP-034-two-layer-kernel-syzygy" / "verdict.md",
        "ebbf52a0b2d85b0bb5c71ca6fb48846d17b1d91644e48e69dbc3a5e8a5f81304",
    ),
}
P4_EXPECTED = {
    "kernel_codomain_rows": 79,
    "kernel_domain_columns": 119,
    "d_source_columns": 710,
    "kernel_codomain_hash": "07f914ec36c6f04b755998cf951567912e58f2e0d75af32d6844d9d791738152",
    "kernel_domain_hash": "ccab1ef2304fbb10c06c4379c20af6f6753d10156039ca56077191dcf757af22",
    "d_source_hash": "82c747b01bece3055f8ae21cc138110163b2bb9c76e479078a083e4f4fdcb367",
    "field_rows": {
        "2": (74, 513, 588, 5, 1, 4),
        "3": (75, 513, 589, 4, 1, 3),
        "1000003": (75, 513, 589, 4, 1, 3),
    },
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


def verify_premises() -> dict[str, str]:
    actual = {name: file_hash(path) for name, (path, _) in PREMISES.items()}
    expected = {name: expected_hash for name, (_, expected_hash) in PREMISES.items()}
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


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


def predicted_family(p: int, t: int) -> tuple[int, set[int], int, int]:
    target = 10 * p + t
    exterior = interval(3 * p, 4 * p - 2) | {t} | interval(t + 2, p)
    degree = 2 * p - t - 1
    total_offset = 4 * p * p + 6 * p - t * (t - 1) // 2
    return target, exterior, degree, total_offset


def low_product(p: int, left: int, right: int) -> tuple[str, int] | None:
    left_second = left >= 3 * p
    right_second = right >= 3 * p
    if left_second and right_second:
        return None
    total = left + right
    if not left_second and not right_second:
        return ("A", total) if total > p else None
    return ("B", total) if total >= 4 * p - 1 else None


def exact_sum_combinations(
    values: tuple[int, ...], size: int, target: int
) -> Iterable[tuple[int, ...]]:
    """Yield increasing fixed-size subsets with one exact sum.

    A memoized feasibility predicate prevents traversal of branches that cannot
    reach the requested sum. This replaces literal traversal of all n-choose-k
    subsets while retaining the canonical lexicographic order.
    """

    count = len(values)
    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)

    @lru_cache(maxsize=None)
    def feasible(start: int, need: int, remaining: int) -> bool:
        if need == 0:
            return remaining == 0
        if count - start < need:
            return False
        minimum = prefix[start + need] - prefix[start]
        maximum = prefix[count] - prefix[count - need]
        if remaining < minimum or remaining > maximum:
            return False
        last_start = count - need
        for index in range(start, last_start + 1):
            value = values[index]
            if value > remaining:
                break
            if feasible(index + 1, need - 1, remaining - value):
                return True
        return False

    if not feasible(0, size, target):
        return

    prefix_values: list[int] = []

    def visit(start: int, need: int, remaining: int) -> Iterable[tuple[int, ...]]:
        if need == 0:
            if remaining == 0:
                yield tuple(prefix_values)
            return
        last_start = count - need
        for index in range(start, last_start + 1):
            value = values[index]
            if value > remaining:
                break
            if not feasible(index + 1, need - 1, remaining - value):
                continue
            prefix_values.append(value)
            yield from visit(index + 1, need - 1, remaining - value)
            prefix_values.pop()

    yield from visit(0, size, target)


def labelled_subsets(
    generators: tuple[int, ...], size: int, total_offset: int, coefficients: set[int]
) -> list[tuple[tuple[int, ...], int]]:
    labels: list[tuple[tuple[int, ...], int]] = []
    for coefficient in sorted(coefficients):
        target_sum = total_offset - coefficient
        if target_sum <= 0:
            continue
        labels.extend(
            (exterior, coefficient)
            for exterior in exact_sum_combinations(generators, size, target_sum)
        )
    labels.sort(key=lambda item: item[0])
    if len(labels) != len({exterior for exterior, _ in labels}):
        raise AssertionError("one exterior subset received multiple coefficients")
    return labels


def rank_mod_prime(columns: list[dict[object, int]], prime: int) -> int:
    pivots: dict[object, dict[object, int]] = {}
    for raw in columns:
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


def dense_matrix(
    rows: list[object], columns: list[dict[object, int]]
) -> list[list[int]]:
    row_index = {row: index for index, row in enumerate(rows)}
    matrix = [[0 for _ in columns] for _ in rows]
    for column_index, column in enumerate(columns):
        for row, value in column.items():
            matrix[row_index[row]][column_index] = value
    return matrix


def smith_profile(matrix: list[list[int]]) -> dict[str, object]:
    normal = smith_normal_form(sympy.Matrix(matrix), domain=ZZ)
    diagonal = [
        abs(int(normal[index, index]))
        for index in range(min(normal.rows, normal.cols))
        if normal[index, index]
    ]
    torsion: dict[str, int] = {}
    for value in diagonal:
        if value > 1:
            key = str(value)
            torsion[key] = torsion.get(key, 0) + 1
    return {
        "integer_rank": len(diagonal),
        "free_cokernel_rank": normal.rows - len(diagonal),
        "torsion_invariant_factors": torsion,
        "diagonal_hash": digest(diagonal),
    }


def unit_residual(matrix: list[list[int]]) -> dict[str, object]:
    """Cancel unit pivots by exact unimodular row and column operations."""

    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_count = 0
    while pivot_count < min(row_count, column_count):
        best: tuple[int, int, int] | None = None
        row_degrees = [
            sum(value != 0 for value in work[row][pivot_count:])
            for row in range(pivot_count, row_count)
        ]
        column_degrees = [
            sum(work[row][column] != 0 for row in range(pivot_count, row_count))
            for column in range(pivot_count, column_count)
        ]
        for row in range(pivot_count, row_count):
            for column in range(pivot_count, column_count):
                if abs(work[row][column]) != 1:
                    continue
                cost = row_degrees[row - pivot_count] * column_degrees[column - pivot_count]
                candidate = (cost, row, column)
                if best is None or candidate < best:
                    best = candidate
        if best is None:
            break
        _, pivot_row, pivot_column = best
        work[pivot_count], work[pivot_row] = work[pivot_row], work[pivot_count]
        for row in work:
            row[pivot_count], row[pivot_column] = row[pivot_column], row[pivot_count]
        if work[pivot_count][pivot_count] == -1:
            work[pivot_count] = [-value for value in work[pivot_count]]

        for column in range(pivot_count + 1, column_count):
            factor = work[pivot_count][column]
            if not factor:
                continue
            for row in range(pivot_count, row_count):
                work[row][column] -= factor * work[row][pivot_count]
        for row in range(pivot_count + 1, row_count):
            factor = work[row][pivot_count]
            if not factor:
                continue
            for column in range(pivot_count, column_count):
                work[row][column] -= factor * work[pivot_count][column]
        pivot_count += 1

    residual = [row[pivot_count:] for row in work[pivot_count:]]
    nonzero = [abs(value) for row in residual for value in row if value]
    residual_profile = smith_profile(residual) if residual and residual[0] else {
        "integer_rank": 0,
        "free_cokernel_rank": len(residual),
        "torsion_invariant_factors": {},
        "diagonal_hash": digest([]),
    }
    return {
        "unit_pivots": pivot_count,
        "residual_rows": len(residual),
        "residual_columns": len(residual[0]) if residual else 0,
        "residual_nonzeros": len(nonzero),
        "residual_entry_gcd": int(sympy.gcd(nonzero)) if nonzero else 0,
        "residual_max_abs": max(nonzero, default=0),
        "residual_matrix_hash": digest(residual),
        "residual_smith_profile": residual_profile,
        "residual_matrix": residual,
    }


def build_target(p: int, t: int, localize: bool) -> dict[str, object]:
    target, selected_exterior, degree, total_offset = predicted_family(p, t)
    generators = tuple(sorted(degree_one_offsets(p) - {0}))
    low = low_offsets(p)
    high = high_offsets(p)
    degree_two = degree_two_offsets(p)

    codomain_rows = labelled_subsets(generators, degree, total_offset, degree_two)
    codomain_set = set(codomain_rows)
    selected_row = (tuple(sorted(selected_exterior)), target)
    if selected_row not in codomain_set:
        raise AssertionError("declared selected row is absent from the complete codomain")
    print(f"(p,t)=({p},{t}) K rows={len(codomain_rows)}", flush=True)

    kernel_domain_labels = labelled_subsets(generators, degree + 1, total_offset, high)
    kernel_boundary_columns: list[dict[object, int]] = []
    for exterior, coefficient in kernel_domain_labels:
        column: dict[object, int] = {}
        for position, variable in enumerate(exterior):
            product = coefficient + variable
            row = (exterior[:position] + exterior[position + 1 :], product)
            if product in degree_two:
                if row not in codomain_set:
                    raise AssertionError("kernel boundary left the selected multidegree")
                column[row] = -1 if position % 2 else 1
        kernel_boundary_columns.append(column)
    print(f"(p,t)=({p},{t}) K columns={len(kernel_boundary_columns)}", flush=True)

    d_source_labels = labelled_subsets(generators, degree + 1, total_offset, low)
    d_boundary_columns: list[dict[object, int]] = []
    connecting_columns: list[dict[object, int]] = []
    for exterior, coefficient in d_source_labels:
        d_column: dict[object, int] = {}
        connecting_column: dict[object, int] = {}
        for position, variable in enumerate(exterior):
            face = exterior[:position] + exterior[position + 1 :]
            sign = -1 if position % 2 else 1
            if variable in low:
                product = low_product(p, variable, coefficient)
                if product is not None:
                    d_column[(face, product[0], product[1])] = sign
            else:
                product_offset = variable + coefficient
                row = (face, product_offset)
                if product_offset in degree_two:
                    if row not in codomain_set:
                        raise AssertionError("connecting map left the selected multidegree")
                    connecting_column[row] = sign
        d_boundary_columns.append(d_column)
        connecting_columns.append(connecting_column)
    print(f"(p,t)=({p},{t}) D columns={len(d_boundary_columns)}", flush=True)

    selected_connecting_sources = [
        index for index, column in enumerate(connecting_columns) if selected_row in column
    ]
    if not selected_connecting_sources:
        raise AssertionError("no connecting source reaches the declared coordinate")

    combined_columns = []
    for d_column, connecting_column in zip(
        d_boundary_columns, connecting_columns, strict=True
    ):
        combined = {("D", row): value for row, value in d_column.items()}
        combined.update({("K", row): value for row, value in connecting_column.items()})
        combined_columns.append(combined)
    combined_columns.extend(
        {("K", row): value for row, value in column.items()}
        for column in kernel_boundary_columns
    )

    field_rows = {}
    for prime in PRIMES:
        rank_kernel = rank_mod_prime(kernel_boundary_columns, prime)
        rank_d = rank_mod_prime(d_boundary_columns, prime)
        rank_combined = rank_mod_prime(combined_columns, prime)
        kernel_dimension = len(codomain_rows) - rank_kernel
        connecting_dimension = rank_combined - rank_d - rank_kernel
        surviving_dimension = len(codomain_rows) + rank_d - rank_combined
        field_rows[str(prime)] = {
            "rank_kernel_boundary": rank_kernel,
            "kernel_cokernel_dimension": kernel_dimension,
            "rank_d_boundary": rank_d,
            "rank_combined": rank_combined,
            "connecting_image_dimension_in_kernel_cokernel": connecting_dimension,
            "surviving_a_dimension": surviving_dimension,
        }
        print(
            f"(p,t)=({p},{t}) GF({prime}): K={kernel_dimension}, "
            f"image={connecting_dimension}, A={surviving_dimension}",
            flush=True,
        )

    odd_rank = field_rows["1000003"]["rank_kernel_boundary"]
    even_rank = field_rows["2"]["rank_kernel_boundary"]
    even_rank_defect = odd_rank - even_rank
    row: dict[str, object] = {
        "p": p,
        "t": t,
        "target_offset": target,
        "homological_degree": degree,
        "standard_internal_degree": degree + 2,
        "total_offset": total_offset,
        "selected_row": [list(selected_row[0]), selected_row[1]],
        "kernel_codomain_rows": len(codomain_rows),
        "kernel_domain_columns": len(kernel_boundary_columns),
        "d_source_columns": len(d_boundary_columns),
        "selected_connecting_source_count": len(selected_connecting_sources),
        "kernel_codomain_hash": digest(
            [[list(exterior), coefficient] for exterior, coefficient in codomain_rows]
        ),
        "kernel_domain_hash": digest(
            [[list(exterior), coefficient] for exterior, coefficient in kernel_domain_labels]
        ),
        "d_source_hash": digest(
            [[list(exterior), coefficient] for exterior, coefficient in d_source_labels]
        ),
        "field_rows": field_rows,
        "even_rank_defect": even_rank_defect,
        "kernel_characteristic_dependent": even_rank_defect > 0,
        "a_characteristic_dependent": len(
            {item["surviving_a_dimension"] for item in field_rows.values()}
        )
        > 1,
    }
    if localize:
        matrix = dense_matrix(codomain_rows, kernel_boundary_columns)
        row["kernel_boundary_smith_profile"] = smith_profile(matrix)
        row["unit_residual"] = unit_residual(matrix)
    row["row_hash"] = digest(row)
    return row


def assert_p4_regression(row: dict[str, object]) -> None:
    for key in (
        "kernel_codomain_rows",
        "kernel_domain_columns",
        "d_source_columns",
        "kernel_codomain_hash",
        "kernel_domain_hash",
        "d_source_hash",
    ):
        if row[key] != P4_EXPECTED[key]:
            raise AssertionError({"p4_regression": key, "actual": row[key], "expected": P4_EXPECTED[key]})
    for prime, expected in P4_EXPECTED["field_rows"].items():
        actual_row = row["field_rows"][prime]
        actual = (
            actual_row["rank_kernel_boundary"],
            actual_row["rank_d_boundary"],
            actual_row["rank_combined"],
            actual_row["kernel_cokernel_dimension"],
            actual_row["connecting_image_dimension_in_kernel_cokernel"],
            actual_row["surviving_a_dimension"],
        )
        if actual != expected:
            raise AssertionError({"p4_field_regression": prime, "actual": actual, "expected": expected})
    smith = row["kernel_boundary_smith_profile"]
    if smith["free_cokernel_rank"] != 4 or smith["torsion_invariant_factors"] != {"2": 1}:
        raise AssertionError({"p4_smith_regression": smith})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-max", type=int, default=5)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=420.0)
    args = parser.parse_args()
    if args.p_max < 4:
        raise ValueError("require p-max>=4")

    started = time.perf_counter()
    result: dict[str, object] = {
        "experiment": "EXP-036",
        "route": "exact-sum finite torsion screen and unit residual",
        "status": "RUNNING",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "p_min": 4,
            "p_max": args.p_max,
            "fields": list(PRIMES),
            "budget_seconds": args.budget_seconds,
        },
        "premise_hashes": verify_premises(),
        "rows": [],
    }
    write_json_atomic(args.output, result)

    completed_p5 = True
    for p in range(4, args.p_max + 1):
        for t in range(2, p - 1):
            elapsed = time.perf_counter() - started
            if elapsed > args.budget_seconds:
                result["status"] = "INCONCLUSIVE_BUDGET"
                result["elapsed_seconds"] = round(elapsed, 6)
                result["artifact_sha256"] = digest(result)
                write_json_atomic(args.output, result)
                print("INCONCLUSIVE_BUDGET", flush=True)
                return 2
            row = build_target(p, t, localize=(p == 4 and t == 2))
            if p == 4 and t == 2:
                assert_p4_regression(row)
                print("EXP-035 (4,2) regression: PASS", flush=True)
            result["rows"].append(row)
            result["elapsed_seconds"] = round(time.perf_counter() - started, 6)
            write_json_atomic(args.output, result)
        if p == 5 and len([row for row in result["rows"] if row["p"] == 5]) != 2:
            completed_p5 = False

    p5_rows = [row for row in result["rows"] if row["p"] == 5]
    if completed_p5 and len(p5_rows) == 2:
        p1_pass = any(row["even_rank_defect"] > 0 for row in p5_rows)
        result["p1_finite_propagation"] = "CONFIRMED" if p1_pass else "REFUTED"
    else:
        result["p1_finite_propagation"] = "NOT_REACHED"
    result["positive_cells"] = [
        [row["p"], row["t"]]
        for row in result["rows"]
        if row["even_rank_defect"] > 0
    ]
    result["status"] = "PASS_FINITE_SCREEN"
    result["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    result["artifact_sha256"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
