"""EXP-029 exact campaign for the colon-Koszul degree-five diagonal."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from datetime import datetime, timezone
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"

PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-023-one-cubic-defining-ideal/proof.md":
        "4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-024-extremal-betti-data/proof.md":
        "b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-025-curvilinear-primary-structure/proof.md":
        "70c7838ce843252aba335d80ade105d1d1942c490530ea7770483be0dff9a61f",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-026-grevlex-staircase/proof.md":
        "765fa23534be9e534fd507dff0e447e967345e4d2a485f7da6fdf0383b04fb56",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-027-relative-betti-strand/proof.md":
        "355ff5c7e4bbc74fc8a1e346aac041d77b3fbc758051dbc729836db6a259e0bc",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-028-complete-second-betti-row/proof.md":
        "7c382237b8ab87d6c8ff6e0ff8b37ccfd586fcc0f8ea4e7c9c9acb3ab0297ace",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-028-complete-second-betti-row/verdict.md":
        "2bdbd96cb37d6891ca4f3fc0d5796a7c016e398f7ddfc5cbc00d0b26d0cac1ff",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-028-complete-second-betti-row/artifacts/results.json":
        "d7ecf4078907d427e6641eeec359dd007bc0411ee1e77018e5b3a19306bfe96d",
}


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def degree_one_offsets(p: int) -> set[int]:
    return (
        {0}
        | interval(1, p)
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


def high_offsets(p: int) -> list[int]:
    return sorted(value for value in degree_one_offsets(p) if value >= 6 * p)


def cumulative_offsets(p: int) -> list[set[int]]:
    q = 24 * p
    full = interval(0, q - 1)
    return [
        {0},
        degree_one_offsets(p),
        interval(0, 2 * p) | interval(3 * p, 5 * p - 2) | interval(6 * p, q - 1),
        full - {6 * p - 1},
        full,
        full,
    ]


def verify_premises() -> dict[str, str]:
    observed = {relative: file_hash(ROOT / relative) for relative in PREMISES}
    if observed != PREMISES:
        mismatch = {
            relative: {"expected": PREMISES[relative], "observed": observed[relative]}
            for relative in PREMISES
            if observed[relative] != PREMISES[relative]
        }
        raise RuntimeError(f"frozen premise mismatch: {mismatch}")
    return observed


def pair_profile(p: int) -> dict[int, int]:
    profile: dict[int, int] = {}
    for left, right in itertools.combinations(high_offsets(p), 2):
        offset = 3 * p + left + right
        profile[offset] = profile.get(offset, 0) + 1
    return dict(sorted(profile.items()))


def expected_support(p: int) -> set[int]:
    return interval(15 * p + 1, 39 * p - 3) - {33 * p - 1}


def hilbert_coefficient_five(p: int) -> int:
    codimension = 10 * p - 1
    h = [1, 10 * p - 1, 12 * p, 2 * p - 1, 1]
    return sum(
        h[degree] * (-1) ** (5 - degree) * comb(codimension, 5 - degree)
        for degree in range(5)
    )


def beta_4_5(p: int) -> int:
    numerator = 2 * p * (5 * p - 1) * (10 * p - 3) * (100 * p * p - 110 * p + 13)
    if numerator % 3:
        raise AssertionError(f"p={p}: beta_(4,5) numerator is not divisible by three")
    return numerator // 3


def formula_row(p: int) -> dict[str, object]:
    if p < 4:
        raise ValueError("EXP-029 is declared only for p>=4")
    high = high_offsets(p)
    profile = pair_profile(p)
    support = set(profile)
    beta25 = p * (2 * p - 3)
    beta35 = sum(profile.values())
    beta45 = beta_4_5(p)
    coefficient = hilbert_coefficient_five(p)
    predictions = {
        "generator_count": len(degree_one_offsets(p)) == 10 * p,
        "high_colon_count": len(high) == 8 * p,
        "support": support == expected_support(p),
        "support_count": len(support) == 24 * p - 4,
        "unique_hole": 33 * p - 1 not in support,
        "beta_3_5": beta35 == comb(8 * p, 2) == 4 * p * (8 * p - 1),
        "degree_five_coefficient": coefficient == beta25 - beta35 + beta45,
    }
    controls = {
        "repeated_pairs_rejected": sum(profile.values()) != comb(8 * p + 1, 2),
        "ordered_pairs_rejected": sum(profile.values()) * 2 != sum(profile.values()),
        "hole_insertion_rejected": support | {33 * p - 1} != expected_support(p),
        "all_generators_rejected": comb(10 * p, 2) != beta35,
        "endpoint_shift_rejected": min(support) != 15 * p,
    }
    if not all(predictions.values()):
        raise AssertionError(f"p={p}: prediction failed: {predictions}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial control failed: {controls}")
    row: dict[str, object] = {
        "p": p,
        "high_colon_count": len(high),
        "beta_2_5": beta25,
        "beta_3_5": beta35,
        "beta_4_5": beta45,
        "hilbert_coefficient_5": coefficient,
        "support_count": len(support),
        "support_min": min(support),
        "support_max": max(support),
        "support_hole": 33 * p - 1,
        "profile_hash": canonical_hash(list(profile.items())),
        "predictions": predictions,
        "controls": controls,
    }
    row["row_hash"] = canonical_hash(row)
    return row


def rank_mod2(columns: list[list[tuple[int, int]]]) -> int:
    pivots: dict[int, int] = {}
    for column in columns:
        vector = 0
        for row, coefficient in column:
            if coefficient & 1:
                vector ^= 1 << row
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                vector ^= pivots[pivot]
            else:
                pivots[pivot] = vector
                break
    return len(pivots)


def rank_mod_prime(columns: list[list[tuple[int, int]]], prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for column in columns:
        vector = {row: coefficient % prime for row, coefficient in column if coefficient % prime}
        while vector:
            pivot = max(vector)
            if pivot not in pivots:
                inverse = pow(vector[pivot], prime - 2, prime)
                vector = {
                    row: (coefficient * inverse) % prime
                    for row, coefficient in vector.items()
                    if (coefficient * inverse) % prime
                }
                pivots[pivot] = vector
                break
            factor = vector[pivot]
            for row, coefficient in pivots[pivot].items():
                updated = (vector.get(row, 0) - factor * coefficient) % prime
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
    return len(pivots)


def boundary_columns(
    upper: list[tuple[int, ...]], lower_index: dict[tuple[int, ...], int]
) -> list[list[tuple[int, int]]]:
    columns = []
    for cell in upper:
        column = []
        for position in range(len(cell)):
            face = cell[:position] + cell[position + 1 :]
            if face in lower_index:
                column.append((lower_index[face], -1 if position % 2 else 1))
        columns.append(column)
    return columns


def grouped_combinations(generators: list[int], size: int) -> dict[int, list[tuple[int, ...]]]:
    answer: dict[int, list[tuple[int, ...]]] = {}
    for cell in itertools.combinations(generators, size):
        answer.setdefault(sum(cell), []).append(cell)
    return answer


def collect_cells(
    grouped: dict[int, list[tuple[int, ...]]], residuals: set[int], offset: int
) -> list[tuple[int, ...]]:
    answer: list[tuple[int, ...]] = []
    for residual in residuals:
        answer.extend(grouped.get(offset - residual, ()))
    answer.sort()
    return answer


def greedy_critical(
    cells: dict[int, list[tuple[int, ...]]], generators: list[int]
) -> dict[int, list[tuple[int, ...]]]:
    unmatched = {frozenset(cell) for size in cells for cell in cells[size]}
    ordered = sorted(unmatched, key=lambda face: (len(face), tuple(sorted(face))))
    for vertex in generators:
        for face in ordered:
            if face not in unmatched or vertex in face:
                continue
            coface = face | {vertex}
            if coface in unmatched:
                unmatched.remove(face)
                unmatched.remove(coface)
    answer = {dimension: [] for dimension in range(4)}
    for face in unmatched:
        answer[len(face) - 1].append(tuple(sorted(face)))
    for dimension in answer:
        answer[dimension].sort()
    return answer


def explicit_profile(p: int, primes: tuple[int, ...]) -> dict[str, object]:
    started = time.perf_counter()
    total_degree = 5
    generators = sorted(degree_one_offsets(p))
    cumulative = cumulative_offsets(p)
    grouped = {size: grouped_combinations(generators, size) for size in (2, 3, 4)}
    maximum = max(max(grouped[size]) + max(cumulative[total_degree - size]) for size in grouped)
    expected = pair_profile(p)
    profiles: dict[str, dict[int, int]] = {str(prime): {} for prime in primes}
    maximum_cells = {2: 0, 3: 0, 4: 0}

    for offset in range(maximum + 1):
        cells = {
            size: collect_cells(grouped[size], cumulative[total_degree - size], offset)
            for size in grouped
        }
        for size in cells:
            maximum_cells[size] = max(maximum_cells[size], len(cells[size]))
        edge_index = {cell: index for index, cell in enumerate(cells[2])}
        triangle_index = {cell: index for index, cell in enumerate(cells[3])}
        d3 = boundary_columns(cells[3], edge_index)
        d4 = boundary_columns(cells[4], triangle_index)
        for prime in primes:
            rank = rank_mod2 if prime == 2 else lambda columns, q=prime: rank_mod_prime(columns, q)
            h2 = len(cells[3]) - rank(d3) - rank(d4)
            if h2:
                profiles[str(prime)][offset] = h2
        if offset % 100 == 0:
            print(f"explicit p={p}: offset {offset}/{maximum}", flush=True)

    expected_profile = dict(sorted(expected.items()))
    if any(profile != expected_profile for profile in profiles.values()):
        raise AssertionError(f"p={p}: relative H2 profile mismatch")

    snapshots = []
    if p == 4:
        grouped_one = grouped_combinations(generators, 1)
        all_grouped = {1: grouped_one, **grouped}
        for offset in (15 * p + 1, 20 * p, 33 * p - 1, 39 * p - 3):
            cells = {
                size: collect_cells(
                    all_grouped[size], cumulative[total_degree - size], offset
                )
                for size in all_grouped
            }
            critical = greedy_critical(cells, generators)
            core = sorted(
                (p, left, right)
                for left, right in itertools.combinations(high_offsets(p), 2)
                if 3 * p + left + right == offset
            )
            if not set(core) <= set(critical[2]):
                raise AssertionError(f"p={p}, offset={offset}: missing critical pair triangle")
            snapshots.append(
                {
                    "offset": offset,
                    "cell_counts_1_to_4": [len(cells[size]) for size in range(1, 5)],
                    "critical_counts_0_to_3": [len(critical[size]) for size in range(4)],
                    "pair_triangle_count": len(core),
                    "transient_triangle_count": len(critical[2]) - len(core),
                }
            )

    result: dict[str, object] = {
        "p": p,
        "total_degree": total_degree,
        "primes": list(primes),
        "maximum_offset_checked": maximum,
        "combination_counts_2_to_4": [sum(len(v) for v in grouped[size].values()) for size in (2, 3, 4)],
        "maximum_cell_counts_2_to_4": [maximum_cells[size] for size in (2, 3, 4)],
        "h2_profiles": {
            prime: {str(offset): value for offset, value in sorted(profile.items())}
            for prime, profile in profiles.items()
        },
        "h2_total": sum(expected_profile.values()),
        "profile_hash": canonical_hash(list(expected_profile.items())),
        "critical_snapshots": snapshots,
        "elapsed_seconds": time.perf_counter() - started,
    }
    result["row_hash"] = canonical_hash(result)
    return result


def parse_ints(value: str) -> list[int]:
    return [int(item) for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=4)
    parser.add_argument("--p-max", type=int, default=300)
    parser.add_argument("--explicit", default="4,5,6")
    parser.add_argument("--large-prime-p", default="4")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--budget-seconds", type=float, default=300.0)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        args.p_min = 4
        args.p_max = 4
        args.explicit = "4"
        args.large_prime_p = "4"
    if args.p_min < 4 or args.p_max < args.p_min:
        raise ValueError("invalid parameter range")

    started = time.perf_counter()
    premise_hashes = verify_premises()
    formula_rows = []
    explicit_rows = []

    for p in range(args.p_min, args.p_max + 1):
        formula_rows.append(formula_row(p))
        if p == args.p_min or p == args.p_max or p % 25 == 0:
            print(f"formula p={p}/{args.p_max}", flush=True)
        write_json_atomic(
            args.checkpoint,
            {"stage": "formula", "completed_p": p, "elapsed_seconds": time.perf_counter() - started},
        )
        if time.perf_counter() - started > args.budget_seconds:
            write_json_atomic(
                args.output,
                {
                    "experiment": "EXP-029-colon-koszul-diagonal",
                    "status": "INCONCLUSIVE_BUDGET",
                    "completed_formula_rows": len(formula_rows),
                    "elapsed_seconds": time.perf_counter() - started,
                },
            )
            return 2

    explicit_parameters = parse_ints(args.explicit)
    large_prime_parameters = set(parse_ints(args.large_prime_p))
    for p in explicit_parameters:
        primes = (2, 1000003) if p in large_prime_parameters else (2,)
        explicit_rows.append(explicit_profile(p, primes))
        print(f"explicit p={p}: PASS", flush=True)
        write_json_atomic(
            args.checkpoint,
            {"stage": "explicit", "completed_p": p, "elapsed_seconds": time.perf_counter() - started},
        )
        if time.perf_counter() - started > 2 * args.budget_seconds:
            write_json_atomic(
                args.output,
                {
                    "experiment": "EXP-029-colon-koszul-diagonal",
                    "status": "INCONCLUSIVE_BUDGET",
                    "completed_formula_rows": len(formula_rows),
                    "completed_explicit": [row["p"] for row in explicit_rows],
                    "elapsed_seconds": time.perf_counter() - started,
                },
            )
            return 2

    payload: dict[str, object] = {
        "experiment": "EXP-029-colon-koszul-diagonal",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "mode": "smoke" if args.smoke else "canonical",
        "range": [args.p_min, args.p_max],
        "completed_formula_rows": len(formula_rows),
        "premise_hashes": premise_hashes,
        "formula_rows": formula_rows,
        "explicit_rows": explicit_rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    payload["campaign_aggregate"] = canonical_hash(
        {
            "formula": [row["row_hash"] for row in formula_rows],
            "explicit": [row["row_hash"] for row in explicit_rows],
            "premises": premise_hashes,
        }
    )
    write_json_atomic(args.output, payload)
    write_json_atomic(
        args.checkpoint,
        {"stage": "complete", "status": "PASS", "elapsed_seconds": payload["elapsed_seconds"]},
    )
    print(f"PASS aggregate={payload['campaign_aggregate']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

