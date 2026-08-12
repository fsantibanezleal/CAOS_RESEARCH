"""EXP-018: exact tangent-cone and Valabrega--Valla computation."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "artifacts" / "results.json"


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@dataclass(frozen=True)
class Profile:
    finite: frozenset[int]
    conductor: int

    @property
    def minimum(self) -> int:
        return min(self.finite) if self.finite else self.conductor


def residue_sets(p: int) -> tuple[int, set[int], set[int], set[int], set[int]]:
    if p < 4:
        raise ValueError("EXP-018 is declared only for p>=4")
    s = 6 * p
    a = interval(0, p) | interval(3 * p, 4 * p - 2)
    b = (
        (interval(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | interval(5 * p - 1, 6 * p - 1)
    )
    c = interval(0, 2 * p) | interval(3 * p, 5 * p - 2)
    h = {2 * p - 1, 4 * p - 1} | interval(4 * p + 1, 5 * p - 2)
    return s, a, b, c, h


def ring_profile(p: int) -> Profile:
    s, a, b, c, _ = residue_sets(p)
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
    s, a, b, c, _ = residue_sets(p)
    finite = (
        {4 * s + r for r in a}
        | {5 * s + r for r in a | b}
        | {6 * s + r for r in b}
        | {8 * s + r for r in c}
        | interval(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def shifted(profile: Profile, amount: int) -> Profile:
    return Profile(
        frozenset(value + amount for value in profile.finite),
        profile.conductor + amount,
    )


def sum_bits(left: frozenset[int], right: frozenset[int], stop: int) -> int:
    if len(left) > len(right):
        left, right = right, left
    right_bits = sum(1 << value for value in right)
    result = 0
    for value in left:
        if value <= stop:
            result |= right_bits << value
    return result & ((1 << (stop + 1)) - 1)


def bit_values(bits: int) -> set[int]:
    values: set[int] = set()
    while bits:
        lowest = bits & -bits
        values.add(lowest.bit_length() - 1)
        bits ^= lowest
    return values


def product(left: Profile, right: Profile) -> Profile:
    finite_bound = min(
        left.minimum + right.conductor,
        right.minimum + left.conductor,
    )
    sums = bit_values(sum_bits(left.finite, right.finite, finite_bound - 1))
    minimum_sum = left.minimum + right.minimum
    gaps = interval(minimum_sum, finite_bound - 1) - sums
    conductor = max(gaps) + 1 if gaps else minimum_sum
    return Profile(frozenset(value for value in sums if value < conductor), conductor)


def members_through(profile: Profile, stop: int) -> set[int]:
    return set(profile.finite) | interval(profile.conductor, stop)


def quotient_values(numerator: Profile, denominator: Profile) -> set[int]:
    stop = max(numerator.conductor, denominator.conductor) - 1
    numerator_values = members_through(numerator, stop)
    denominator_values = members_through(denominator, stop)
    if denominator_values - numerator_values:
        witness = min(denominator_values - numerator_values)
        raise AssertionError(f"denominator is not contained in numerator at {witness}")
    return numerator_values - denominator_values


def intersection_quotient(left: Profile, right: Profile, denominator: Profile) -> set[int]:
    stop = max(left.conductor, right.conductor, denominator.conductor) - 1
    intersection = members_through(left, stop) & members_through(right, stop)
    denominator_values = members_through(denominator, stop)
    if denominator_values - intersection:
        witness = min(denominator_values - intersection)
        raise AssertionError(f"intersection denominator failure at {witness}")
    return intersection - denominator_values


def formula_powers(p: int) -> list[Profile]:
    """Second route: reconstruct the proved closed profiles, without multiplication."""
    s, _, _, c, _ = residue_sets(p)
    ring = ring_profile(p)
    t1 = conductor_profile(p)
    t2 = Profile(
        frozenset({8 * s + r for r in c} | interval(9 * s, 13 * s - 2)),
        13 * s,
    )
    t3 = Profile(frozenset(interval(12 * s, 13 * s - 2)), 13 * s)
    t4 = Profile(frozenset(), 16 * s)
    t5 = Profile(frozenset(), 20 * s)
    return [ring, t1, t2, t3, t4, t5]


def route_defects(powers: list[Profile], x: int) -> list[set[int]]:
    reduction = shifted(powers[0], x)
    return [
        intersection_quotient(reduction, powers[n + 1], shifted(powers[n], x))
        for n in range(5)
    ]


def expected_defects(p: int) -> list[set[int]]:
    s, _, _, _, h = residue_sets(p)
    return [set(), {9 * s + residue for residue in h}, set(), set(), set()]


def analyze_parameter(p: int) -> dict[str, object]:
    s, _, _, _, h = residue_sets(p)
    x = 4 * s

    route_a = [ring_profile(p), conductor_profile(p)]
    for _ in range(4):
        route_a.append(product(route_a[-1], route_a[1]))
    route_b = formula_powers(p)
    if route_a != route_b:
        raise AssertionError(f"p={p}: multiplied and formula power profiles disagree")

    defects_a = route_defects(route_a, x)
    defects_b = route_defects(route_b, x)
    predicted = expected_defects(p)
    if defects_a != defects_b or defects_a != predicted:
        raise AssertionError(f"p={p}: Valabrega--Valla profile mismatch")
    defect_lengths = [len(values) for values in defects_a]
    if defect_lengths != [0, p, 0, 0, 0]:
        raise AssertionError(f"p={p}: defect length profile {defect_lengths}")

    sally_lengths = [
        len(quotient_values(route_a[n + 1], shifted(route_a[n], x)))
        for n in range(5)
    ]
    if sally_lengths != [23 * p - 1, 14 * p, 2 * p, 1, 0]:
        raise AssertionError(f"p={p}: Sally profile mismatch {sally_lengths}")
    e0 = len(quotient_values(route_a[0], shifted(route_a[0], x)))
    hilbert_function = [e0 - value for value in sally_lengths]
    hilbert_numerator = [
        hilbert_function[0],
        *(
            hilbert_function[index] - hilbert_function[index - 1]
            for index in range(1, len(hilbert_function))
        ),
    ]
    expected_hilbert = [p + 1, 10 * p, 22 * p, 24 * p - 1, 24 * p]
    expected_numerator = [p + 1, 9 * p - 1, 12 * p, 2 * p - 1, 1]
    if hilbert_function != expected_hilbert or hilbert_numerator != expected_numerator:
        raise AssertionError(f"p={p}: Hilbert data mismatch")

    witness = 9 * s + 2 * p - 1
    corruptions = {
        "deleted_first_witness_rejected": predicted[1] - {witness} != defects_a[1],
        "false_degree_two_defect_rejected": predicted[2] | {13 * s - 1} != defects_a[2],
        "perturbed_defect_length_rejected": defect_lengths[1] != p - 1,
        "false_cm_verdict_rejected": bool(defects_a[1]),
        "perturbed_numerator_rejected": expected_numerator[:-1] + [2] != hilbert_numerator,
    }
    if not all(corruptions.values()):
        raise AssertionError(f"p={p}: a corruption survived")

    row: dict[str, object] = {
        "p": p,
        "s": s,
        "vv_defect_lengths_n0_through_n4": defect_lengths,
        "nonzero_defect_residues": sorted(h),
        "depth": 0,
        "cohen_macaulay": False,
        "sally_quotient_lengths": sally_lengths,
        "hilbert_function_h0_through_h4": hilbert_function,
        "hilbert_numerator": hilbert_numerator,
        "defect_hashes": [digest(sorted(values)) for values in defects_a],
        "route_power_hashes": [
            digest({"finite": sorted(power.finite), "conductor": power.conductor})
            for power in route_a
        ],
        "corruptions": corruptions,
    }
    row["row_hash"] = digest(row)
    return row


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--output", type=Path, default=RESULTS)
    args = parser.parse_args()
    if args.first < 4 or args.last < args.first:
        raise ValueError("require 4 <= first <= last")

    print("EXP-018 mandatory p=4 smoke gate", flush=True)
    smoke = analyze_parameter(4)
    print(
        f"p=4 smoke PASS defect={smoke['vv_defect_lengths_n0_through_n4']}",
        flush=True,
    )

    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print(f"EXP-018 exact campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1, args.last} or p % 25 == 0:
            print(
                f"p={p}: vv={rows[-1]['vv_defect_lengths_n0_through_n4']} depth=0",
                flush=True,
            )
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-018 exceeded its declared two-minute budget")
    aggregate = digest([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-018-conductor-tangent-cone",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "predictions": {
            "exact_vv_module": "PASS",
            "depth_zero_non_cm": "PASS",
            "hilbert_series": "PASS",
            "two_routes": "PASS",
            "corruptions": "PASS",
        },
        "campaign_aggregate": aggregate,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    print(f"EXP-018 computational PASS aggregate={aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
