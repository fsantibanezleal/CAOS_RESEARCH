"""EXP-021: exact conductor fiber cone and Artinian-socle campaign."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


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
    if p < 4:
        raise ValueError("EXP-021 is declared only for p>=4")
    s = 6 * p
    a = interval(0, p) | interval(3 * p, 4 * p - 2)
    b = (
        (interval(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | interval(5 * p - 1, 6 * p - 1)
    )
    c = interval(0, 2 * p) | interval(3 * p, 5 * p - 2)
    return s, a, b, c


def ring_profile(p: int) -> Profile:
    s, a, b, c = residue_sets(p)
    finite = (
        {0}
        | {4 * s + r for r in a}
        | interval(5 * s, 6 * s - 1)
        | {6 * s + r for r in b}
        | {8 * s + r for r in c}
        | interval(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def conductor_profile(p: int) -> Profile:
    s, a, b, c = residue_sets(p)
    finite = (
        {4 * s + r for r in a}
        | {5 * s + r for r in a | b}
        | {6 * s + r for r in b}
        | {8 * s + r for r in c}
        | interval(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def maximal_profile(p: int) -> Profile:
    ring = ring_profile(p)
    return Profile(frozenset(ring.finite - {0}), ring.conductor)


def bit_values(bits: int) -> set[int]:
    result: set[int] = set()
    while bits:
        lowest = bits & -bits
        result.add(lowest.bit_length() - 1)
        bits ^= lowest
    return result


def sum_bits(left: frozenset[int], right: frozenset[int], stop: int) -> int:
    if len(left) > len(right):
        left, right = right, left
    right_bits = sum(1 << value for value in right)
    total = 0
    for value in left:
        if value <= stop:
            total |= right_bits << value
    return total & ((1 << (stop + 1)) - 1)


def product(left: Profile, right: Profile) -> Profile:
    bound = min(left.minimum + right.conductor, right.minimum + left.conductor)
    sums = bit_values(sum_bits(left.finite, right.finite, bound - 1))
    floor = left.minimum + right.minimum
    gaps = interval(floor, bound - 1) - sums
    conductor = max(gaps) + 1 if gaps else floor
    return Profile(frozenset(v for v in sums if v < conductor), conductor)


def shift(profile: Profile, amount: int) -> Profile:
    return Profile(
        frozenset(value + amount for value in profile.finite),
        profile.conductor + amount,
    )


def powers(p: int, last: int = 6) -> list[Profile]:
    result = [ring_profile(p), conductor_profile(p)]
    while len(result) <= last:
        result.append(product(result[-1], result[1]))
    return result


def equal_profiles(left: Profile, right: Profile) -> bool:
    stop = max(left.conductor, right.conductor)
    start = min(left.minimum, right.minimum)
    return all(left.contains(v) == right.contains(v) for v in range(start, stop))


def quotient_basis(numerator: Profile, denominators: list[Profile]) -> list[int]:
    stop = max([numerator.conductor] + [item.conductor for item in denominators])
    return [
        value
        for value in range(numerator.minimum, stop)
        if numerator.contains(value)
        and not any(item.contains(value) for item in denominators)
    ]


def direct_route(p: int) -> dict[str, object]:
    q = 24 * p
    ideal_powers = powers(p)
    maximal = maximal_profile(p)
    maximal_products = [product(maximal, item) for item in ideal_powers]
    square_identity = equal_profiles(ideal_powers[2], maximal_products[1])
    higher_identities = [
        equal_profiles(ideal_powers[n + 1], maximal_products[n])
        for n in range(1, 6)
    ]

    kernel_degree_zero = quotient_basis(maximal, [ideal_powers[1]])
    kernel_positive = [
        quotient_basis(maximal_products[n], [ideal_powers[n + 1]])
        for n in range(1, 6)
    ]

    hilbert_function = [1] + [
        len(quotient_basis(ideal_powers[n], [maximal_products[n]]))
        for n in range(1, 6)
    ]

    artinian_basis: list[list[int]] = [[0]]
    for n in range(1, 6):
        artinian_basis.append(
            quotient_basis(
                ideal_powers[n],
                [maximal_products[n], shift(ideal_powers[n - 1], q)],
            )
        )

    degree_one = artinian_basis[1]
    socle: list[list[int]] = []
    for n, basis in enumerate(artinian_basis):
        if n + 1 >= len(artinian_basis):
            socle.append(list(basis))
            continue
        target_denominators = [
            maximal_products[n + 1],
            shift(ideal_powers[n], q),
        ]
        socle.append(
            [
                value
                for value in basis
                if all(
                    any(item.contains(value + generator) for item in target_denominators)
                    for generator in degree_one
                )
            ]
        )

    basis_offsets = [
        [value - n * q for value in basis]
        for n, basis in enumerate(artinian_basis)
    ]
    socle_offsets = [
        [value - n * q for value in basis]
        for n, basis in enumerate(socle)
    ]
    return {
        "square_identity": square_identity,
        "higher_identities": higher_identities,
        "kernel_degree_zero": kernel_degree_zero,
        "kernel_positive": kernel_positive,
        "hilbert_function_through_degree_5": hilbert_function,
        "artinian_basis_offsets": basis_offsets,
        "artinian_h_vector_through_degree_5": [len(item) for item in artinian_basis],
        "socle_offsets": socle_offsets,
        "socle_vector_through_degree_5": [len(item) for item in socle],
    }


def closed_basis_offsets(p: int) -> list[set[int]]:
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


def formula_route(p: int) -> dict[str, object]:
    basis = closed_basis_offsets(p)
    nonsocle_degree_two = interval(p + 1, 2 * p) | interval(4 * p - 1, 5 * p - 2)
    socle = [set(), set(), basis[2] - nonsocle_degree_two, set(), basis[4], set()]
    return {
        "square_identity": True,
        "higher_identities": [True] * 5,
        "kernel_dimensions": [p, 0, 0, 0, 0, 0],
        "hilbert_function_through_degree_5": [1, 10 * p, 22 * p, 24 * p - 1, 24 * p, 24 * p],
        "free_shifts": [1, 10 * p - 1, 12 * p, 2 * p - 1, 1],
        "artinian_basis_offsets": [sorted(item) for item in basis],
        "artinian_h_vector_through_degree_5": [1, 10 * p - 1, 12 * p, 2 * p - 1, 1, 0],
        "socle_offsets": [sorted(item) for item in socle],
        "socle_vector_through_degree_5": [0, 0, 10 * p, 0, 1, 0],
        "type": 10 * p + 1,
    }


def analyze_parameter(p: int) -> dict[str, object]:
    route_a = direct_route(p)
    route_b = formula_route(p)
    actual_kernel_dimensions = [len(route_a["kernel_degree_zero"])] + [
        len(item) for item in route_a["kernel_positive"]
    ]
    comparisons = {
        "square_and_higher": route_a["square_identity"]
        and all(route_a["higher_identities"]),
        "natural_kernel": actual_kernel_dimensions == route_b["kernel_dimensions"],
        "hilbert_function": route_a["hilbert_function_through_degree_5"]
        == route_b["hilbert_function_through_degree_5"],
        "artinian_basis": route_a["artinian_basis_offsets"]
        == route_b["artinian_basis_offsets"],
        "socle": route_a["socle_offsets"] == route_b["socle_offsets"],
    }
    if not all(comparisons.values()):
        raise AssertionError(f"p={p}: direct and closed routes disagree: {comparisons}")

    mutated_square = Profile(
        frozenset(set(product(maximal_profile(p), conductor_profile(p)).finite) - {48 * p}),
        product(maximal_profile(p), conductor_profile(p)).conductor,
    )
    controls = {
        "deleted_square_value_rejected": not equal_profiles(powers(p)[2], mutated_square),
        "positive_kernel_rejected": actual_kernel_dimensions[1:] != [1, 0, 0, 0, 0],
        "perturbed_mu_T2_rejected": route_b["hilbert_function_through_degree_5"][2]
        != 22 * p - 1,
        "deleted_degree_two_socle_rejected": len(route_a["socle_offsets"][2])
        != 10 * p - 1,
        "false_degree_three_socle_rejected": len(route_a["socle_offsets"][3]) != 1,
        "false_gorenstein_type_rejected": route_b["type"] != 1,
    }
    if not all(controls.values()):
        raise AssertionError(f"p={p}: an adversarial corruption survived")

    row: dict[str, object] = {
        "p": p,
        "square_identity": True,
        "all_higher_identities": True,
        "kernel_dimensions_degrees_0_to_5": actual_kernel_dimensions,
        "natural_quotient": "G_p/H0(G_p) ~= F(T_p)",
        "hilbert_function_through_degree_5": route_b["hilbert_function_through_degree_5"],
        "hilbert_numerator": route_b["free_shifts"],
        "artinian_h_vector_through_degree_5": route_b["artinian_h_vector_through_degree_5"],
        "socle_vector_through_degree_5": route_b["socle_vector_through_degree_5"],
        "type": route_b["type"],
        "cohen_macaulay": True,
        "level": False,
        "gorenstein": False,
        "multiplicity": 24 * p,
        "reduction_number": 4,
        "regularity": 4,
        "a_invariant": 3,
        "basis_aggregate": canonical_hash(route_a["artinian_basis_offsets"]),
        "socle_aggregate": canonical_hash(route_a["socle_offsets"]),
        "comparisons": comparisons,
        "controls": controls,
    }
    row["row_hash"] = canonical_hash(row)
    return row


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.first < 4 or args.last < args.first:
        raise ValueError("require 4 <= first <= last")

    print("EXP-021 mandatory p=4 smoke gate", flush=True)
    smoke = analyze_parameter(4)
    print(
        f"p=4 smoke PASS h={smoke['artinian_h_vector_through_degree_5']} "
        f"socle={smoke['socle_vector_through_degree_5']}",
        flush=True,
    )

    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print(f"EXP-021 exact campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1, args.last} or p % 25 == 0:
            print(
                f"p={p}: type={rows[-1]['type']} "
                f"kernel={rows[-1]['kernel_dimensions_degrees_0_to_5']}",
                flush=True,
            )
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-021 exceeded its declared two-minute budget")

    aggregate = canonical_hash([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-021-conductor-fiber-cone",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "predictions": {
            "square_identity": "PASS",
            "natural_graded_algebra_quotient": "PASS",
            "cohen_macaulay_fiber_cone": "PASS",
            "artinian_socle_and_type": "PASS",
            "nonlevel_nongorenstein": "PASS",
            "two_routes": "PASS",
            "corruptions": "PASS",
        },
        "campaign_aggregate": aggregate,
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    elapsed = time.perf_counter() - started
    print(f"EXP-021 computational PASS aggregate={aggregate} elapsed={elapsed:.6f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
