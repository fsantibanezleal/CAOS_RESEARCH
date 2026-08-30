"""Independent EXP-036 semigroup-basis and reverse-pivot audit.

This route reconstructs both Artinian layers from numerical-semigroup ideal
powers. Its exact-sum enumeration is iterative dynamic programming, not the
canonical feasibility DFS, and its sparse elimination reverses both columns
and pivot order.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_CANONICAL = HERE / "artifacts" / "results-p6.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit-p6.json"
PRIMES = (2, 3, 5)


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def integers(first: int, last: int) -> set[int]:
    return set(range(first, last + 1)) if first <= last else set()


@dataclass(frozen=True)
class Profile:
    finite: frozenset[int]
    conductor: int

    @property
    def minimum(self) -> int:
        return min(self.finite) if self.finite else self.conductor

    def contains(self, value: int) -> bool:
        return value >= self.conductor or value in self.finite


def residue_sets(p: int) -> tuple[int, set[int], set[int], set[int]]:
    s = 6 * p
    first = integers(0, p) | integers(3 * p, 4 * p - 2)
    second = (
        (integers(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | integers(5 * p - 1, 6 * p - 1)
    )
    third = integers(0, 2 * p) | integers(3 * p, 5 * p - 2)
    return s, first, second, third


def ring_profile(p: int) -> Profile:
    s, first, second, third = residue_sets(p)
    finite = (
        {0}
        | {4 * s + value for value in first}
        | integers(5 * s, 6 * s - 1)
        | {6 * s + value for value in second}
        | {8 * s + value for value in third}
        | integers(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def conductor_profile(p: int) -> Profile:
    s, first, second, third = residue_sets(p)
    finite = (
        {4 * s + value for value in first}
        | {5 * s + value for value in first | second}
        | {6 * s + value for value in second}
        | {8 * s + value for value in third}
        | integers(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def maximal_profile(p: int) -> Profile:
    ring = ring_profile(p)
    return Profile(frozenset(ring.finite - {0}), ring.conductor)


def product(left: Profile, right: Profile) -> Profile:
    bound = min(left.minimum + right.conductor, right.minimum + left.conductor)
    sums = {
        a + b
        for a in left.finite
        for b in right.finite
        if a + b < bound
    }
    floor = left.minimum + right.minimum
    gaps = integers(floor, bound - 1) - sums
    conductor = max(gaps) + 1 if gaps else floor
    return Profile(frozenset(value for value in sums if value < conductor), conductor)


def shift(profile: Profile, amount: int) -> Profile:
    return Profile(
        frozenset(value + amount for value in profile.finite),
        profile.conductor + amount,
    )


def quotient_basis(numerator: Profile, denominators: list[Profile]) -> list[int]:
    stop = max([numerator.conductor] + [item.conductor for item in denominators])
    return [
        value
        for value in range(numerator.minimum, stop)
        if numerator.contains(value)
        and not any(item.contains(value) for item in denominators)
    ]


def direct_artinian_bases(p: int) -> tuple[set[int], set[int]]:
    section = 24 * p
    ideal = conductor_profile(p)
    maximal = maximal_profile(p)
    square = product(ideal, ideal)
    degree_one = quotient_basis(
        ideal, [product(maximal, ideal), shift(ring_profile(p), section)]
    )
    degree_two = quotient_basis(
        square, [product(maximal, square), shift(ideal, section)]
    )
    return (
        {value - section for value in degree_one},
        {value - 2 * section for value in degree_two},
    )


def low_product(p: int, left: int, right: int) -> tuple[str, int] | None:
    left_second = left >= 3 * p
    right_second = right >= 3 * p
    if left_second and right_second:
        return None
    total = left + right
    if not left_second and not right_second:
        return ("ring", total) if total > p else None
    return ("canonical", total) if total >= 4 * p - 1 else None


def dynamic_labels(
    generators: list[int], size: int, total_offset: int, coefficients: set[int]
) -> list[tuple[tuple[int, ...], int]]:
    """Iteratively build fixed-size subsets up to the largest permitted sum."""

    target_to_coefficient = {
        total_offset - coefficient: coefficient
        for coefficient in coefficients
        if total_offset - coefficient > 0
    }
    maximum = max(target_to_coefficient, default=-1)
    layers: list[dict[int, list[tuple[int, ...]]]] = [dict() for _ in range(size + 1)]
    layers[0][0] = [()]
    for generator in generators:
        for count in range(size, 0, -1):
            previous = layers[count - 1]
            current = layers[count]
            for subtotal, subsets in list(previous.items()):
                new_sum = subtotal + generator
                if new_sum > maximum:
                    continue
                current.setdefault(new_sum, []).extend(
                    subset + (generator,) for subset in subsets
                )
    labels = [
        (subset, target_to_coefficient[subtotal])
        for subtotal, subsets in layers[size].items()
        if subtotal in target_to_coefficient
        for subset in subsets
    ]
    labels.sort(key=lambda item: item[0])
    if len(labels) != len({subset for subset, _ in labels}):
        raise AssertionError("independent labels are not unique")
    return labels


def reverse_rank(columns: list[dict[object, int]], prime: int) -> int:
    pivots: dict[object, dict[object, int]] = {}
    for raw in reversed(columns):
        vector = {row: value % prime for row, value in raw.items() if value % prime}
        while vector:
            pivot = max(vector, key=repr)
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


def audit_cell(p: int, t: int) -> dict[str, object]:
    degree_one, degree_two = direct_artinian_bases(p)
    low = integers(1, p) | integers(3 * p, 4 * p - 2)
    high = degree_one - low
    low_products = {
        product_value[1]
        for left, right in itertools.combinations_with_replacement(sorted(low), 2)
        if (product_value := low_product(p, left, right)) is not None
    }
    kernel_degree_two = degree_two - low_products
    generators = sorted(degree_one)

    target = 10 * p + t
    selected = integers(3 * p, 4 * p - 2) | {t} | integers(t + 2, p)
    degree = 2 * p - t - 1
    total_offset = 4 * p * p + 6 * p - t * (t - 1) // 2

    codomain = dynamic_labels(generators, degree, total_offset, kernel_degree_two)
    codomain_set = set(codomain)
    kernel_labels = dynamic_labels(generators, degree + 1, total_offset, high)
    source_labels = dynamic_labels(generators, degree + 1, total_offset, low)

    kernel_columns = []
    for exterior, coefficient in kernel_labels:
        column = {}
        for position, variable in enumerate(exterior):
            product_offset = coefficient + variable
            row = (exterior[:position] + exterior[position + 1 :], product_offset)
            if product_offset in kernel_degree_two:
                if row not in codomain_set:
                    raise AssertionError("independent kernel boundary left the target")
                column[row] = -1 if position % 2 else 1
        kernel_columns.append(column)

    d_columns = []
    connecting_columns = []
    for exterior, coefficient in source_labels:
        d_column = {}
        connecting_column = {}
        for position, variable in enumerate(exterior):
            face = exterior[:position] + exterior[position + 1 :]
            sign = -1 if position % 2 else 1
            if variable in low:
                product_value = low_product(p, variable, coefficient)
                if product_value is not None:
                    d_column[(face, *product_value)] = sign
            else:
                product_offset = variable + coefficient
                row = (face, product_offset)
                if product_offset in kernel_degree_two:
                    connecting_column[row] = sign
        d_columns.append(d_column)
        connecting_columns.append(connecting_column)

    combined_columns = []
    for d_column, connecting_column in zip(d_columns, connecting_columns, strict=True):
        column = {("source", row): value for row, value in d_column.items()}
        column.update({("target", row): value for row, value in connecting_column.items()})
        combined_columns.append(column)
    combined_columns.extend(
        {("target", row): value for row, value in column.items()}
        for column in kernel_columns
    )

    field_rows = {}
    for prime in PRIMES:
        rank_kernel = reverse_rank(kernel_columns, prime)
        rank_d = reverse_rank(d_columns, prime)
        rank_combined = reverse_rank(combined_columns, prime)
        field_rows[str(prime)] = {
            "rank_kernel_boundary": rank_kernel,
            "kernel_cokernel_dimension": len(codomain) - rank_kernel,
            "rank_d_boundary": rank_d,
            "rank_combined": rank_combined,
            "connecting_image_dimension_in_kernel_cokernel": (
                rank_combined - rank_d - rank_kernel
            ),
            "surviving_a_dimension": len(codomain) + rank_d - rank_combined,
        }

    checks = {
        "degree_one_count": len(degree_one) == 10 * p - 1,
        "degree_two_count": len(degree_two) == 12 * p,
        "high_count": len(high) == 8 * p,
        "kernel_degree_two_count": len(kernel_degree_two) == 10 * p,
        "selected_representation_set": {
            variable for variable in degree_one if target - variable in high
        }
        == selected,
        "selected_row_present": (tuple(sorted(selected)), target) in codomain_set,
        "odd_fields_agree": field_rows["3"] == field_rows["5"],
    }
    if not all(checks.values()):
        raise AssertionError({"independent_cell_failure": (p, t), "checks": checks})

    row: dict[str, object] = {
        "p": p,
        "t": t,
        "checks": checks,
        "kernel_codomain_rows": len(codomain),
        "kernel_domain_columns": len(kernel_columns),
        "d_source_columns": len(d_columns),
        "kernel_codomain_hash": digest(
            [[list(exterior), coefficient] for exterior, coefficient in codomain]
        ),
        "kernel_domain_hash": digest(
            [[list(exterior), coefficient] for exterior, coefficient in kernel_labels]
        ),
        "d_source_hash": digest(
            [[list(exterior), coefficient] for exterior, coefficient in source_labels]
        ),
        "field_rows": field_rows,
    }
    row["row_hash"] = digest(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--budget-seconds", type=float, default=300.0)
    args = parser.parse_args()
    started = time.perf_counter()
    canonical = json.loads(args.canonical.read_text(encoding="utf-8"))
    canonical_rows = {
        (row["p"], row["t"]): row
        for row in canonical["rows"]
    }
    if not canonical_rows:
        raise RuntimeError("canonical artifact contains no cells")
    for p, t in canonical_rows:
        if p < 4 or not 2 <= t <= p - 2:
            raise RuntimeError(f"canonical artifact contains invalid family cell {(p, t)}")

    rows = []
    comparisons = {}
    for cell in sorted(canonical_rows):
        row = audit_cell(*cell)
        canonical_row = canonical_rows[cell]
        comparison = {
            "basis_counts": (
                row["kernel_codomain_rows"] == canonical_row["kernel_codomain_rows"]
                and row["kernel_domain_columns"] == canonical_row["kernel_domain_columns"]
                and row["d_source_columns"] == canonical_row["d_source_columns"]
            ),
            "basis_hashes": (
                row["kernel_codomain_hash"] == canonical_row["kernel_codomain_hash"]
                and row["kernel_domain_hash"] == canonical_row["kernel_domain_hash"]
                and row["d_source_hash"] == canonical_row["d_source_hash"]
            ),
            "gf2_ranks": row["field_rows"]["2"] == canonical_row["field_rows"]["2"],
            "gf3_ranks": row["field_rows"]["3"] == canonical_row["field_rows"]["3"],
        }
        if not all(comparison.values()):
            raise AssertionError({"canonical_comparison_failure": cell, "comparison": comparison})
        comparisons[f"{cell[0]}:{cell[1]}"] = comparison
        rows.append(row)
        elapsed = time.perf_counter() - started
        print(f"independent {cell}: PASS at {elapsed:.3f}s", flush=True)
        if elapsed > args.budget_seconds:
            raise TimeoutError("INCONCLUSIVE_BUDGET")

    result = {
        "experiment": "EXP-036",
        "route": "semigroup reconstruction, dynamic exact sums, reverse pivots",
        "status": "PASS_INDEPENDENT",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_artifact_sha256": canonical["artifact_sha256"],
        "comparisons": comparisons,
        "rows": rows,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    result["artifact_sha256"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
