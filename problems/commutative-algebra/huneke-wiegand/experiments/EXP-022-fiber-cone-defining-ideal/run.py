"""EXP-022: exact minimal defining-equation counts for the conductor fiber cone."""

from __future__ import annotations

import argparse
import gc
import hashlib
import itertools
import json
import math
import time
from array import array
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "smoke-p4-results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "smoke-p4-checkpoint.json"


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def artinian_blocks(p: int) -> list[set[int]]:
    """Closed EXP-021 bases D_0,...,D_5 after killing the parameter."""
    if p < 4:
        raise ValueError("EXP-022 is declared only for p>=4")
    degree_one = (
        interval(1, p)
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
    degree_two = (
        interval(p + 1, 2 * p)
        | interval(4 * p - 1, 5 * p - 2)
        | {8 * p - 1, 10 * p - 1}
        | interval(10 * p + 1, 11 * p - 2)
        | interval(12 * p, 13 * p)
        | {14 * p - 1}
        | interval(15 * p, 16 * p - 1)
        | interval(16 * p + 1, 17 * p - 2)
        | interval(18 * p, 24 * p - 1)
    )
    degree_three = interval(2 * p + 1, 3 * p - 1) | interval(5 * p - 1, 6 * p - 2)
    return [{0}, degree_one, degree_two, degree_three, {6 * p - 1}, set()]


def fiber_basis_offsets(p: int, degree: int) -> set[int]:
    """Offsets of a monomial basis of C_p in the requested degree."""
    blocks = artinian_blocks(p)
    return set().union(*blocks[: min(degree, 4) + 1])


def generator_offsets(p: int) -> list[int]:
    result = sorted(fiber_basis_offsets(p, 1))
    if len(result) != 10 * p or result[0] != 0:
        raise AssertionError("closed degree-one basis does not have the predicted size")
    return result


class DisjointSet:
    """Compact union-find with one extra vertex reserved for the zero class."""

    def __init__(self, size: int) -> None:
        self.parent = array("I", range(size))
        self.rank = bytearray(size)

    def find(self, item: int) -> int:
        parent = self.parent
        root = item
        while parent[root] != root:
            root = parent[root]
        while parent[item] != item:
            next_item = parent[item]
            parent[item] = root
            item = next_item
        return root

    def union(self, left: int, right: int) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return
        rank = self.rank
        if rank[root_left] < rank[root_right]:
            root_left, root_right = root_right, root_left
        self.parent[root_right] = root_left
        if rank[root_left] == rank[root_right]:
            rank[root_left] += 1


def symmetric_monomials(variable_count: int, degree: int) -> Iterable[tuple[int, ...]]:
    return itertools.combinations_with_replacement(range(variable_count), degree)


def canonical_monomials(
    monomials: list[tuple[int, ...]],
    sums: array,
    valid_offsets: set[int],
) -> dict[int, tuple[int, ...]]:
    result: dict[int, tuple[int, ...]] = {}
    for monomial, value_sum in zip(monomials, sums, strict=True):
        if value_sum in valid_offsets and value_sum not in result:
            result[value_sum] = monomial
    missing = valid_offsets - set(result)
    if missing:
        raise AssertionError(f"basis offsets without monomial representatives: {sorted(missing)}")
    return result


def witness_for_components(
    components: dict[int, tuple[int, tuple[int, ...]]],
    valid_offsets: set[int],
) -> dict[str, object] | None:
    by_sum: dict[int, list[tuple[int, tuple[int, ...]]]] = {}
    for root, (value_sum, monomial) in components.items():
        if value_sum not in valid_offsets:
            return {
                "kind": "zero_monomial_not_generated_below",
                "value_sum": value_sum,
                "component_root": root,
                "monomial": list(monomial),
            }
        by_sum.setdefault(value_sum, []).append((root, monomial))
    for value_sum in sorted(by_sum):
        items = by_sum[value_sum]
        if len(items) > 1:
            return {
                "kind": "equal_sum_components_not_connected_below",
                "value_sum": value_sum,
                "left_root": items[0][0],
                "left_monomial": list(items[0][1]),
                "right_root": items[1][0],
                "right_monomial": list(items[1][1]),
            }
    return None


def analyze_degree(
    p: int,
    degree: int,
    offsets: list[int],
    previous_valid: set[int],
    previous_canonical: dict[int, tuple[int, ...]],
) -> tuple[dict[str, object], dict[int, tuple[int, ...]]]:
    started = time.perf_counter()
    variable_count = len(offsets)
    expected_monomials = math.comb(variable_count + degree - 1, degree)
    monomials = list(symmetric_monomials(variable_count, degree))
    if len(monomials) != expected_monomials:
        raise AssertionError("symmetric-monomial enumeration count mismatch")
    index = {monomial: position for position, monomial in enumerate(monomials)}
    sums = array("I", (sum(offsets[item] for item in monomial) for monomial in monomials))
    zero = len(monomials)
    classes = DisjointSet(zero + 1)

    for position, monomial in enumerate(monomials):
        total = sums[position]
        previous_variable = -1
        for slot, variable in enumerate(monomial):
            if variable == previous_variable:
                continue
            previous_variable = variable
            rest_sum = total - offsets[variable]
            if rest_sum not in previous_valid:
                classes.union(position, zero)
                continue
            rest_canonical = previous_canonical[rest_sum]
            target = tuple(sorted((variable, *rest_canonical)))
            classes.union(position, index[target])

    zero_root = classes.find(zero)
    components: dict[int, tuple[int, tuple[int, ...]]] = {}
    for position, monomial in enumerate(monomials):
        root = classes.find(position)
        if root == zero_root:
            continue
        value_sum = sums[position]
        prior = components.get(root)
        if prior is None:
            components[root] = (value_sum, monomial)
        elif prior[0] != value_sum:
            raise AssertionError("a lower-degree relation changed the value sum")

    valid = fiber_basis_offsets(p, degree)
    actual_dimension = len(valid)
    lower_relation_quotient_dimension = len(components)
    minimal_generators = lower_relation_quotient_dimension - actual_dimension
    if minimal_generators < 0:
        raise AssertionError("lower relations produced a quotient smaller than the fiber")
    witness = witness_for_components(components, valid)
    if (minimal_generators == 0) != (witness is None):
        raise AssertionError("component witness and dimension defect disagree")

    canonical = canonical_monomials(monomials, sums, valid)
    summary: dict[str, object] = {
        "degree": degree,
        "monomial_count": len(monomials),
        "lower_relation_quotient_dimension": lower_relation_quotient_dimension,
        "actual_fiber_dimension": actual_dimension,
        "minimal_defining_equations": minimal_generators,
        "first_obstruction": witness,
        "canonical_representative_hash": canonical_hash(
            {str(key): list(value) for key, value in sorted(canonical.items())}
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }

    del index
    del sums
    del monomials
    del classes
    gc.collect()
    return summary, canonical


def analyze_parameter(
    p: int,
    max_degree: int,
    checkpoint: Path,
    budget_seconds: float,
) -> dict[str, object]:
    if not 2 <= max_degree <= 5:
        raise ValueError("max_degree must lie between 2 and 5")
    started = time.perf_counter()
    offsets = generator_offsets(p)
    expected_dimensions = [1, 10 * p, 22 * p, 24 * p - 1, 24 * p, 24 * p]
    actual_dimensions = [len(fiber_basis_offsets(p, degree)) for degree in range(6)]
    if actual_dimensions != expected_dimensions:
        raise AssertionError(
            f"closed fiber dimensions disagree: {actual_dimensions} != {expected_dimensions}"
        )

    previous_valid = fiber_basis_offsets(p, 1)
    previous_canonical = {offset: (index,) for index, offset in enumerate(offsets)}
    degrees: list[dict[str, object]] = []
    for degree in range(2, max_degree + 1):
        print(
            f"EXP-022 p={p} degree={degree}: "
            f"enumerating {math.comb(len(offsets) + degree - 1, degree):,} monomials",
            flush=True,
        )
        summary, canonical = analyze_degree(
            p,
            degree,
            offsets,
            previous_valid,
            previous_canonical,
        )
        degrees.append(summary)
        elapsed = time.perf_counter() - started
        checkpoint_payload = {
            "experiment": "EXP-022-fiber-cone-defining-ideal",
            "status": "RUNNING" if degree < max_degree else "COMPUTATIONAL_PASS",
            "p": p,
            "completed_through_degree": degree,
            "degrees": degrees,
            "elapsed_seconds": elapsed,
        }
        write_json_atomic(checkpoint, checkpoint_payload)
        print(
            f"degree={degree}: beta_1,{degree}={summary['minimal_defining_equations']} "
            f"quotient={summary['lower_relation_quotient_dimension']} "
            f"actual={summary['actual_fiber_dimension']} elapsed={elapsed:.3f}s",
            flush=True,
        )
        if elapsed > budget_seconds:
            checkpoint_payload["status"] = "INCONCLUSIVE_BUDGET"
            write_json_atomic(checkpoint, checkpoint_payload)
            raise TimeoutError(
                f"EXP-022 exceeded its declared {budget_seconds:g}-second budget after degree {degree}"
            )
        previous_valid = fiber_basis_offsets(p, degree)
        previous_canonical = canonical

    betti = {str(item["degree"]): item["minimal_defining_equations"] for item in degrees}
    predicted_quadrics = 50 * p * p - 17 * p
    quadratic_generation = (
        betti.get("2") == predicted_quadrics
        and max_degree == 5
        and all(betti.get(str(degree)) == 0 for degree in range(3, 6))
    )
    result: dict[str, object] = {
        "experiment": "EXP-022-fiber-cone-defining-ideal",
        "status": "COMPUTATIONAL_PASS",
        "p": p,
        "variable_count": len(offsets),
        "parameter_offset": 0,
        "fiber_dimensions_degrees_0_to_5": actual_dimensions,
        "first_betti_row_degrees_2_to_5": betti,
        "predicted_quadrics": predicted_quadrics,
        "quadratic_generation_through_degree_5": quadratic_generation,
        "source_degree_bound": 5,
        "degrees": degrees,
        "elapsed_seconds": time.perf_counter() - started,
    }
    result["result_hash"] = canonical_hash(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=4)
    parser.add_argument("--max-degree", type=int, default=5)
    parser.add_argument("--budget-seconds", type=float, default=300.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()
    if args.p < 4:
        raise ValueError("require p>=4")
    if args.budget_seconds <= 0:
        raise ValueError("budget_seconds must be positive")

    print(f"EXP-022 mandatory p={args.p} defining-ideal gate", flush=True)
    result = analyze_parameter(
        args.p,
        args.max_degree,
        args.checkpoint,
        args.budget_seconds,
    )
    write_json_atomic(args.output, result)
    print(
        f"EXP-022 p={args.p} computational PASS "
        f"betti={result['first_betti_row_degrees_2_to_5']} "
        f"quadratic={result['quadratic_generation_through_degree_5']} "
        f"hash={result['result_hash']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
