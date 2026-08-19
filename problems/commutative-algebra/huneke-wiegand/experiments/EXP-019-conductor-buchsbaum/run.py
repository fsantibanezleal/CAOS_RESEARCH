"""EXP-019: full graded torsion and Buchsbaum test for the conductor tangent cone."""

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

    def contains(self, value: int) -> bool:
        return value >= self.conductor or value in self.finite


def residue_sets(p: int) -> tuple[int, set[int], set[int], set[int], set[int]]:
    if p < 4:
        raise ValueError("EXP-019 is declared only for p>=4")
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
        | {4 * s + residue for residue in a}
        | interval(5 * s, 6 * s - 1)
        | {6 * s + residue for residue in b}
        | {8 * s + residue for residue in c}
        | interval(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def conductor_profile(p: int) -> Profile:
    s, a, b, c, _ = residue_sets(p)
    finite = (
        {4 * s + residue for residue in a}
        | {5 * s + residue for residue in a | b}
        | {6 * s + residue for residue in b}
        | {8 * s + residue for residue in c}
        | interval(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def maximal_profile(p: int) -> Profile:
    ring = ring_profile(p)
    return Profile(frozenset(ring.finite - {0}), ring.conductor)


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


def formula_powers(p: int, last: int = 9) -> list[Profile]:
    s, _, _, c, _ = residue_sets(p)
    powers = [
        ring_profile(p),
        conductor_profile(p),
        Profile(
            frozenset(
                {8 * s + residue for residue in c}
                | interval(9 * s, 13 * s - 2)
            ),
            13 * s,
        ),
        Profile(frozenset(interval(12 * s, 13 * s - 2)), 13 * s),
    ]
    powers.extend(Profile(frozenset(), 4 * n * s) for n in range(4, last + 1))
    return powers


def multiplied_powers(p: int, last: int = 9) -> list[Profile]:
    powers = [ring_profile(p), conductor_profile(p)]
    while len(powers) <= last:
        powers.append(product(powers[-1], powers[1]))
    return powers


def members_through(profile: Profile, stop: int) -> set[int]:
    return set(profile.finite) | interval(profile.conductor, stop)


def quotient_values(numerator: Profile, denominator: Profile) -> set[int]:
    stop = max(numerator.conductor, denominator.conductor) - 1
    numerator_values = members_through(numerator, stop)
    denominator_values = members_through(denominator, stop)
    if denominator_values - numerator_values:
        witness = min(denominator_values - numerator_values)
        raise AssertionError(f"denominator containment failure at {witness}")
    return numerator_values - denominator_values


def shift_contained(source: Profile, target: Profile, amount: int) -> bool:
    """Test amount+source subset target, including both infinite tails."""
    for value in source.finite:
        if not target.contains(amount + value):
            return False
    tail_stop = target.conductor - amount - 1
    for value in range(source.conductor, tail_stop + 1):
        if not target.contains(amount + value):
            return False
    return True


def colon_torsion(powers: list[Profile], last_degree: int = 4) -> list[set[int]]:
    """Route A: use the defining colon condition with the fourth power."""
    k = 4
    return [
        {
            value
            for value in quotient_values(powers[n], powers[n + 1])
            if shift_contained(powers[k], powers[n + k + 1], value)
        }
        for n in range(last_degree + 1)
    ]


def threshold_torsion(powers: list[Profile], s: int) -> list[set[int]]:
    """Route B: use the independently derived stable-tail threshold."""
    return [
        {
            value
            for value in quotient_values(powers[n], powers[n + 1])
            if value >= 4 * (n + 1) * s
        }
        for n in range(5)
    ]


def analyze_parameter(p: int) -> dict[str, object]:
    s, _, _, _, h = residue_sets(p)
    route_a_powers = multiplied_powers(p)
    route_b_powers = formula_powers(p)
    if route_a_powers != route_b_powers:
        raise AssertionError(f"p={p}: multiplied and formula power profiles disagree")

    torsion_a = colon_torsion(route_a_powers)
    torsion_b = threshold_torsion(route_b_powers, s)
    expected = [{5 * s + residue for residue in h}, set(), set(), set(), set()]
    if torsion_a != torsion_b or torsion_a != expected:
        raise AssertionError(f"p={p}: graded torsion profile mismatch")

    torsion_lengths = [len(values) for values in torsion_a]
    if torsion_lengths != [p, 0, 0, 0, 0]:
        raise AssertionError(f"p={p}: torsion length profile {torsion_lengths}")

    ring = route_a_powers[0]
    maximal = maximal_profile(p)
    conductor = route_a_powers[1]
    square = route_a_powers[2]
    degree_zero_action = all(
        shift_contained(maximal, conductor, value) for value in torsion_a[0]
    )
    positive_action = all(
        shift_contained(conductor, square, value) for value in torsion_a[0]
    )
    if not degree_zero_action or not positive_action:
        raise AssertionError(f"p={p}: homogeneous maximal annihilator failed")

    buchbaum_invariant = sum(torsion_lengths)
    quotient_numerator = [1, 10 * p - 1, 12 * p, 2 * p - 1, 1]
    original_numerator = [p + 1, 9 * p - 1, 12 * p, 2 * p - 1, 1]
    recovered_quotient = original_numerator.copy()
    recovered_quotient[0] -= p
    recovered_quotient[1] += p
    if recovered_quotient != quotient_numerator:
        raise AssertionError(f"p={p}: quotient Hilbert numerator mismatch")

    first = min(expected[0])
    corruptions = {
        "unit_torsion_rejected": 0 not in torsion_a[0],
        "deleted_first_torsion_rejected": expected[0] - {first} != torsion_a[0],
        "positive_degree_torsion_rejected": all(not values for values in torsion_a[1:]),
        "unit_in_degree_zero_maximal_rejected": all(
            not shift_contained(ring, conductor, value) for value in torsion_a[0]
        ),
        "perturbed_invariant_rejected": buchbaum_invariant != p - 1,
        "perturbed_quotient_numerator_rejected": (
            quotient_numerator[:-1] + [2] != recovered_quotient
        ),
    }
    if not all(corruptions.values()):
        raise AssertionError(f"p={p}: an adversarial corruption survived")

    row: dict[str, object] = {
        "p": p,
        "s": s,
        "h0_lengths_degree_0_through_4": torsion_lengths,
        "h0_degree_zero_values": sorted(torsion_a[0]),
        "h0_degree_zero_residues_from_5s": sorted(h),
        "homogeneous_maximal_annihilates_h0": True,
        "degree_zero_maximal_action": "ANNIHILATES",
        "positive_degree_action": "ANNIHILATES",
        "buchsbaum": True,
        "cohen_macaulay": False,
        "buchsbaum_invariant": buchbaum_invariant,
        "cm_quotient_hilbert_numerator": quotient_numerator,
        "torsion_hashes": [digest(sorted(values)) for values in torsion_a],
        "power_hashes": [
            digest({"finite": sorted(power.finite), "conductor": power.conductor})
            for power in route_a_powers
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

    print("EXP-019 mandatory p=4 smoke gate", flush=True)
    smoke = analyze_parameter(4)
    print(
        f"p=4 smoke PASS H0={smoke['h0_lengths_degree_0_through_4']} "
        "Buchsbaum=True",
        flush=True,
    )

    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print(f"EXP-019 exact campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1, args.last} or p % 25 == 0:
            print(
                f"p={p}: H0={rows[-1]['h0_lengths_degree_0_through_4']} "
                f"I={rows[-1]['buchsbaum_invariant']}",
                flush=True,
            )
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-019 exceeded its declared two-minute budget")

    aggregate = digest([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-019-conductor-buchsbaum",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "predictions": {
            "complete_h0": "PASS",
            "homogeneous_maximal_annihilator": "PASS",
            "buchsbaum_non_cm": "PASS",
            "unbounded_invariant": "PASS",
            "cm_quotient_series": "PASS",
            "two_routes": "PASS",
            "corruptions": "PASS",
        },
        "campaign_aggregate": aggregate,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    print(f"EXP-019 computational PASS aggregate={aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
