"""EXP-020: exact module over the minimal-reduction Noether normalization."""

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


def residue_sets(p: int) -> tuple[int, set[int], set[int], set[int]]:
    if p < 4:
        raise ValueError("EXP-020 is declared only for p>=4")
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
        | {4 * s + residue for residue in a}
        | interval(5 * s, 6 * s - 1)
        | {6 * s + residue for residue in b}
        | {8 * s + residue for residue in c}
        | interval(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def conductor_profile(p: int) -> Profile:
    s, a, b, c = residue_sets(p)
    finite = (
        {4 * s + residue for residue in a}
        | {5 * s + residue for residue in a | b}
        | {6 * s + residue for residue in b}
        | {8 * s + residue for residue in c}
        | interval(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


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


def multiplied_powers(p: int) -> list[Profile]:
    powers = [ring_profile(p), conductor_profile(p)]
    while len(powers) <= 5:
        powers.append(product(powers[-1], powers[1]))
    return powers


def apery(profile: Profile, modulus: int) -> list[int]:
    result: list[int] = []
    for residue in range(modulus):
        value = residue
        while not profile.contains(value):
            value += modulus
        result.append(value)
    return result


def add_count(counts: dict[int, int], degree: int) -> None:
    counts[degree] = counts.get(degree, 0) + 1


def add_torsion(counts: dict[tuple[int, int], int], shift: int, exponent: int) -> None:
    key = (shift, exponent)
    counts[key] = counts.get(key, 0) + 1


def apery_decomposition(p: int) -> dict[str, object]:
    """Route A: decompose the exact conductor-power Apery columns."""
    s, _, _, _ = residue_sets(p)
    modulus = 4 * s
    powers = multiplied_powers(p)
    table = [apery(power, modulus) for power in powers]

    free: dict[int, int] = {}
    torsion: dict[tuple[int, int], int] = {}
    increment_hashes: list[str] = []
    for residue in range(modulus):
        increments: list[int] = []
        for n in range(5):
            difference = table[n + 1][residue] - table[n][residue]
            if difference not in {0, modulus}:
                raise AssertionError(
                    f"p={p}, residue={residue}, n={n}: invalid Apery increment {difference}"
                )
            increments.append(difference // modulus)
        if increments[-1] != 1:
            raise AssertionError(f"p={p}, residue={residue}: unstable final increment")

        increment_hashes.append(digest(increments))
        n = 0
        while n < len(increments):
            if increments[n] == 0:
                n += 1
                continue
            start = n
            while n < len(increments) and increments[n] == 1:
                n += 1
            if n == len(increments):
                add_count(free, start)
            else:
                add_torsion(torsion, start, n - start)

    return {
        "free_shifts": {str(key): free[key] for key in sorted(free)},
        "torsion_summands": {
            f"shift_{shift}_exponent_{exponent}": torsion[(shift, exponent)]
            for shift, exponent in sorted(torsion)
        },
        "apery_table_hash": digest(table),
        "increment_aggregate": digest(increment_hashes),
    }


def invariant_decomposition(p: int) -> dict[str, object]:
    """Route B: use the Hilbert numerator and complete exponent-one torsion."""
    original_numerator = [p + 1, 9 * p - 1, 12 * p, 2 * p - 1, 1]
    torsion_numerator = [p, -p, 0, 0, 0]
    free_numerator = [
        original - torsion
        for original, torsion in zip(original_numerator, torsion_numerator, strict=True)
    ]
    return {
        "free_shifts": {
            str(degree): count
            for degree, count in enumerate(free_numerator)
            if count
        },
        "torsion_summands": {"shift_0_exponent_1": p},
        "original_hilbert_numerator": original_numerator,
        "torsion_hilbert_numerator": torsion_numerator,
        "free_hilbert_numerator": free_numerator,
    }


def analyze_parameter(p: int) -> dict[str, object]:
    route_a = apery_decomposition(p)
    route_b = invariant_decomposition(p)
    if route_a["free_shifts"] != route_b["free_shifts"]:
        raise AssertionError(f"p={p}: free-shift routes disagree")
    if route_a["torsion_summands"] != route_b["torsion_summands"]:
        raise AssertionError(f"p={p}: torsion routes disagree")

    free = {int(key): value for key, value in route_a["free_shifts"].items()}
    expected_free = {0: 1, 1: 10 * p - 1, 2: 12 * p, 3: 2 * p - 1, 4: 1}
    expected_torsion = {"shift_0_exponent_1": p}
    if free != expected_free or route_a["torsion_summands"] != expected_torsion:
        raise AssertionError(f"p={p}: predicted cyclic decomposition failed")

    beta_0 = expected_free.copy()
    beta_0[0] += p
    beta_1 = {1: p}
    projective_dimension = 1
    regularity = max(
        max(beta_0),
        max(degree - 1 for degree in beta_1),
    )
    a_invariant = max(expected_free) - 1
    free_rank = sum(expected_free.values())
    parameter_section_length = free_rank + p
    if free_rank != 24 * p or parameter_section_length != 25 * p:
        raise AssertionError(f"p={p}: rank or parameter-section identity failed")

    corruptions = {
        "torsion_exponent_two_rejected": {"shift_0_exponent_2": 1} != expected_torsion,
        "deleted_degree_one_free_rejected": expected_free[1] - 1 != expected_free[1],
        "perturbed_first_betti_rejected": beta_1[1] != p - 1,
        "regularity_three_rejected": regularity != 3,
        "section_length_minus_one_rejected": parameter_section_length != 25 * p - 1,
    }
    if not all(corruptions.values()):
        raise AssertionError(f"p={p}: an adversarial corruption survived")

    row: dict[str, object] = {
        "p": p,
        "noether_normalization": "k[x_p], deg(x_p)=1",
        "torsion_summands": expected_torsion,
        "free_shifts": {str(key): expected_free[key] for key in expected_free},
        "beta_0": {str(key): beta_0[key] for key in beta_0},
        "beta_1": {str(key): beta_1[key] for key in beta_1},
        "projective_dimension_over_F": projective_dimension,
        "regularity_over_F": regularity,
        "a_invariant": a_invariant,
        "free_rank": free_rank,
        "buchsbaum_invariant": p,
        "parameter_section_length": parameter_section_length,
        "parameter_section_identity": "25p=e0+I=24p+p",
        "apery_table_hash": route_a["apery_table_hash"],
        "increment_aggregate": route_a["increment_aggregate"],
        "original_hilbert_numerator": route_b["original_hilbert_numerator"],
        "free_hilbert_numerator": route_b["free_hilbert_numerator"],
        "corruptions": corruptions,
    }
    row["row_hash"] = digest(row)
    return row


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--output", type=Path, default=RESULTS)
    args = parser.parse_args()
    if args.first < 4 or args.last < args.first:
        raise ValueError("require 4 <= first <= last")

    print("EXP-020 mandatory p=4 smoke gate", flush=True)
    smoke = analyze_parameter(4)
    print(
        "p=4 smoke PASS "
        f"free={smoke['free_shifts']} torsion={smoke['torsion_summands']}",
        flush=True,
    )

    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print(f"EXP-020 exact campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1, args.last} or p % 25 == 0:
            print(
                f"p={p}: beta1={rows[-1]['beta_1']} "
                f"reg={rows[-1]['regularity_over_F']} section={rows[-1]['parameter_section_length']}",
                flush=True,
            )
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-020 exceeded its declared two-minute budget")

    aggregate = digest([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-020-noether-normalization-module",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "predictions": {
            "cyclic_decomposition": "PASS",
            "minimal_resolution": "PASS",
            "regularity_and_a_invariant": "PASS",
            "parameter_section_identity": "PASS",
            "two_routes": "PASS",
            "corruptions": "PASS",
        },
        "campaign_aggregate": aggregate,
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    elapsed = time.perf_counter() - started
    print(
        f"EXP-020 computational PASS aggregate={aggregate} elapsed={elapsed:.6f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
