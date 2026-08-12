"""EXP-017: exact conductor reduction sequence and Hilbert data."""

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


def residue_sets(p: int) -> tuple[int, set[int], set[int], set[int]]:
    if p < 4:
        raise ValueError("EXP-017 is declared only for p>=4")
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
    stop = denominator.conductor - 1
    numerator_values = members_through(numerator, stop)
    denominator_values = members_through(denominator, stop)
    if denominator_values - numerator_values:
        witness = min(denominator_values - numerator_values)
        raise AssertionError(f"denominator is not contained in numerator at {witness}")
    return numerator_values - denominator_values


def expected_defects(p: int) -> list[set[int]]:
    s, a, b, c = residue_sets(p)
    d0 = (
        {4 * s + r for r in a - {0}}
        | {5 * s + r for r in a | b}
        | {6 * s + r for r in b}
        | {8 * s + r for r in c - a}
        | {10 * s + r for r in interval(0, s - 1) - b}
        | interval(11 * s, 12 * s - 1)
        | {12 * s + r for r in interval(0, s - 2) - c}
        | {17 * s - 1}
    )
    d1 = (
        {
            8 * s + r
            for r in interval(p + 1, 2 * p) | interval(4 * p - 1, 5 * p - 2)
        }
        | {
            9 * s + r
            for r in {2 * p - 1, 4 * p - 1} | interval(4 * p + 1, 5 * p - 2)
        }
        | {
            10 * s + r
            for r in (
                interval(0, p)
                | {2 * p - 1}
                | interval(3 * p, 4 * p - 1)
                | interval(4 * p + 1, 5 * p - 2)
            )
        }
        | interval(11 * s, 12 * s - 1)
        | {
            12 * s + r
            for r in interval(2 * p + 1, 3 * p - 1)
            | interval(5 * p - 1, s - 2)
        }
        | {17 * s - 1}
    )
    d2 = (
        {
            12 * s + r
            for r in interval(2 * p + 1, 3 * p - 1)
            | interval(5 * p - 1, s - 2)
        }
        | {17 * s - 1}
    )
    d3 = {17 * s - 1}
    return [d0, d1, d2, d3, set()]


def analyze_parameter(p: int) -> dict[str, object]:
    s, _, _, _ = residue_sets(p)
    ring = ring_profile(p)
    t_power = conductor_profile(p)
    powers = [t_power]
    for _ in range(4):
        powers.append(product(powers[-1], powers[0]))

    actual: list[set[int]] = []
    for index, power in enumerate(powers):
        denominator = ring if index == 0 else powers[index - 1]
        actual.append(quotient_values(power, shifted(denominator, 4 * s)))
    predicted = expected_defects(p)
    for index, (found, wanted) in enumerate(zip(actual, predicted, strict=True)):
        if found != wanted:
            witness = min(found ^ wanted)
            raise AssertionError(f"p={p}: quotient {index} mismatch at {witness}")

    lengths = [len(values) for values in actual]
    if lengths != [23 * p - 1, 14 * p, 2 * p, 1, 0]:
        raise AssertionError(f"p={p}: length profile mismatch {lengths}")
    if powers[4] != shifted(powers[3], 4 * s):
        raise AssertionError(f"p={p}: false terminal reduction equality")

    e0 = len(quotient_values(ring, shifted(ring, 4 * s)))
    e1 = sum(lengths[:-1])
    if e0 != 24 * p or e1 != 39 * p:
        raise AssertionError(f"p={p}: Hilbert coefficients {(e0, e1)}")
    for n in (4, 5):
        power = powers[n - 1]
        hilbert_value = len(quotient_values(ring, power))
        if hilbert_value != e0 * n - e1:
            raise AssertionError(f"p={p}: Hilbert polynomial mismatch at n={n}")

    corruptions = {
        "deleted_terminal_rejected": predicted[2] - {17 * s - 1} != actual[2],
        "false_power_three_stability_rejected": bool(actual[2]),
        "false_power_four_stability_rejected": bool(actual[3]),
        "altered_cubic_interval_rejected": predicted[2] | {12 * s + 2 * p} != actual[2],
        "perturbed_length_rejected": lengths[2] != 2 * p + 1,
    }
    if not all(corruptions.values()):
        raise AssertionError(f"p={p}: a corruption survived")

    row: dict[str, object] = {
        "p": p,
        "s": s,
        "quotient_lengths": lengths,
        "reduction_number": 4,
        "e0": e0,
        "e1": e1,
        "conductors_T1_through_T5": [power.conductor for power in powers],
        "defect_hashes": [digest(sorted(values)) for values in actual],
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
    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print(f"EXP-017 exact campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1, args.last} or p % 25 == 0:
            print(f"p={p}: lengths={rows[-1]['quotient_lengths']} r=4", flush=True)
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-017 exceeded its declared two-minute budget")
    aggregate = digest([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-017-conductor-reduction-number",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "predictions": {
            "exact_quotient_sets": "PASS",
            "reduction_number_four": "PASS",
            "hilbert_coefficients": "PASS",
            "corruptions": "PASS",
        },
        "campaign_aggregate": aggregate,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    print(f"EXP-017 computational PASS aggregate={aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
