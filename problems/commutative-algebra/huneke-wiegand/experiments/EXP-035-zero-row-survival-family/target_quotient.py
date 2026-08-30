"""EXP-035 complete selected-multidegree quotient after the connecting image.

For one declared ``(p,t)`` cell, this script builds the full kernel cokernel,
the full degree-one source complex of ``D_p``, and the connecting chain map.
It computes the surviving ``A_p`` dimension without choosing a cycle basis.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import sympy
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "target-quotient.json"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


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


def predicted_family(p: int, t: int) -> tuple[int, set[int], int, int]:
    target = 10 * p + t
    exterior = interval(3 * p, 4 * p - 2) | {t} | interval(t + 2, p)
    homological_degree = 2 * p - t - 1
    total_offset = 4 * p * p + 6 * p - t * (t - 1) // 2
    return target, exterior, homological_degree, total_offset


def low_product(p: int, left: int, right: int) -> tuple[str, int] | None:
    left_second = left >= 3 * p
    right_second = right >= 3 * p
    if left_second and right_second:
        return None
    total = left + right
    if not left_second and not right_second:
        return ("A", total) if total > p else None
    return ("B", total) if total >= 4 * p - 1 else None


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


def smith_profile(
    rows: list[object], columns: list[dict[object, int]]
) -> dict[str, object]:
    row_index = {row: index for index, row in enumerate(rows)}
    matrix = sympy.zeros(len(rows), len(columns))
    for column_index, column in enumerate(columns):
        for row, value in column.items():
            matrix[row_index[row], column_index] = value
    normal = smith_normal_form(matrix, domain=ZZ)
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
        "row_count": len(rows),
        "column_count": len(columns),
        "integer_rank": len(diagonal),
        "free_cokernel_rank": len(rows) - len(diagonal),
        "torsion_invariant_factors": torsion,
        "diagonal_hash": digest(diagonal),
    }


def build_target(p: int, t: int) -> dict[str, object]:
    target, selected_exterior, degree, total_offset = predicted_family(p, t)
    generators = sorted(degree_one_offsets(p) - {0})
    low = low_offsets(p)
    high = high_offsets(p)
    degree_two = degree_two_offsets(p)

    codomain_rows = []
    for exterior in itertools.combinations(generators, degree):
        coefficient = total_offset - sum(exterior)
        if coefficient in degree_two:
            codomain_rows.append((exterior, coefficient))
    codomain_set = set(codomain_rows)
    selected_row = (tuple(sorted(selected_exterior)), target)
    if selected_row not in codomain_set:
        raise AssertionError("declared selected row is absent from the complete codomain")
    print(f"K codomain rows: {len(codomain_rows)}", flush=True)

    kernel_boundary_columns: list[dict[object, int]] = []
    kernel_domain_labels = []
    for exterior in itertools.combinations(generators, degree + 1):
        coefficient = total_offset - sum(exterior)
        if coefficient not in high:
            continue
        column: dict[object, int] = {}
        for position, variable in enumerate(exterior):
            product = coefficient + variable
            row = (exterior[:position] + exterior[position + 1 :], product)
            if product in degree_two:
                if row not in codomain_set:
                    raise AssertionError("kernel boundary left the selected multidegree")
                column[row] = -1 if position % 2 else 1
        kernel_domain_labels.append((exterior, coefficient))
        kernel_boundary_columns.append(column)
    print(f"K boundary columns: {len(kernel_boundary_columns)}", flush=True)

    d_boundary_columns: list[dict[object, int]] = []
    connecting_columns: list[dict[object, int]] = []
    d_source_labels = []
    for exterior in itertools.combinations(generators, degree + 1):
        coefficient = total_offset - sum(exterior)
        if coefficient not in low:
            continue
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
        d_source_labels.append((exterior, coefficient))
        d_boundary_columns.append(d_column)
        connecting_columns.append(connecting_column)
    print(f"D source columns: {len(d_boundary_columns)}", flush=True)

    selected_connecting_sources = [
        index
        for index, column in enumerate(connecting_columns)
        if selected_row in column
    ]
    if not selected_connecting_sources:
        raise AssertionError("no connecting source reaches the declared coordinate")

    field_rows = {}
    for prime in (2, 3, 5, 1_000_003):
        rank_kernel_boundary = rank_mod_prime(kernel_boundary_columns, prime)
        rank_d_boundary = rank_mod_prime(d_boundary_columns, prime)
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
        rank_combined = rank_mod_prime(combined_columns, prime)
        kernel_cokernel_dimension = len(codomain_rows) - rank_kernel_boundary
        killed_dimension = rank_combined - rank_d_boundary - rank_kernel_boundary
        surviving_dimension = len(codomain_rows) + rank_d_boundary - rank_combined
        if killed_dimension < 0 or surviving_dimension < 0:
            raise AssertionError("rank formula produced a negative dimension")
        field_rows[str(prime)] = {
            "rank_kernel_boundary": rank_kernel_boundary,
            "kernel_cokernel_dimension": kernel_cokernel_dimension,
            "rank_d_boundary": rank_d_boundary,
            "rank_combined": rank_combined,
            "connecting_image_dimension_in_kernel_cokernel": killed_dimension,
            "surviving_a_dimension": surviving_dimension,
        }
        print(
            f"GF({prime}): K={kernel_cokernel_dimension}, "
            f"killed={killed_dimension}, A={surviving_dimension}",
            flush=True,
        )

    smith = smith_profile(codomain_rows, kernel_boundary_columns)
    if smith["free_cokernel_rank"] != field_rows["1000003"]["kernel_cokernel_dimension"]:
        raise AssertionError("Smith free rank disagrees with the large-prime cokernel")
    characteristic_dependent = len(
        {item["surviving_a_dimension"] for item in field_rows.values()}
    ) > 1

    result: dict[str, object] = {
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
        "selected_connecting_sources": [
            {
                "source_index": index,
                "exterior": list(d_source_labels[index][0]),
                "coefficient": d_source_labels[index][1],
                "sign": connecting_columns[index][selected_row],
            }
            for index in selected_connecting_sources
        ],
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
        "kernel_boundary_smith_profile": smith,
        "characteristic_dependent": characteristic_dependent,
    }
    result["row_hash"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=4)
    parser.add_argument("--t", type=int, default=2)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=300.0)
    args = parser.parse_args()
    if args.p < 4 or not 2 <= args.t <= args.p - 2:
        raise ValueError("require p>=4 and 2<=t<=p-2")

    started = time.perf_counter()
    row = build_target(args.p, args.t)
    elapsed = time.perf_counter() - started
    if elapsed > args.budget_seconds:
        raise TimeoutError("INCONCLUSIVE_BUDGET")
    result = {
        "experiment": "EXP-035",
        "route": "complete selected-multidegree quotient",
        "status": "PASS_CHARACTERISTIC_DEPENDENCE" if row["characteristic_dependent"] else "PASS_EXACT_FINITE_TARGET",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "p": args.p,
            "t": args.t,
            "fields": [2, 3, 5, 1_000_003],
            "budget_seconds": args.budget_seconds,
        },
        "rank_identity": (
            "dim A = dim C_K + rank(d_D) - rank([[d_D,0],[J,delta_K]])"
        ),
        "row": row,
        "elapsed_seconds": round(elapsed, 6),
    }
    result["artifact_sha256"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
