"""EXP-030 exact colon and total-degree-six relative-homology campaign.

CPU only. All ranks use exact finite-field arithmetic. Finite profiles validate the
implementation; they do not replace the declared integral all-parameter proof gate.
"""

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

PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-023-one-cubic-defining-ideal/proof.md":
        "4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-027-relative-betti-strand/proof.md":
        "355ff5c7e4bbc74fc8a1e346aac041d77b3fbc758051dbc729836db6a259e0bc",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-028-complete-second-betti-row/proof.md":
        "7c382237b8ab87d6c8ff6e0ff8b37ccfd586fcc0f8ea4e7c9c9acb3ab0297ace",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-029-colon-koszul-diagonal/proof.md":
        "c1bb1a599d5cb608e70f30a9dd96c9d4993ec3d9d844e669121482941e8f039e",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-029-colon-koszul-diagonal/verdict.md":
        "eac3dc7ee46d984dcfe90500a89a829ed3794b826359d0ccc07e31e3a9d0ba7c",
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


def low_offsets(p: int) -> list[int]:
    return sorted(interval(0, p) | interval(3 * p, 4 * p - 2))


def high_offsets(p: int) -> list[int]:
    return sorted(degree_one_offsets(p) - set(low_offsets(p)))


def cumulative_offsets(p: int) -> list[set[int]]:
    full = interval(0, 24 * p - 1)
    return [
        {0},
        degree_one_offsets(p),
        interval(0, 2 * p) | interval(3 * p, 5 * p - 2) | interval(6 * p, 24 * p - 1),
        full - {6 * p - 1},
        full,
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


def predicted_beta_3_6(p: int) -> int:
    numerator = 8 * p * (7 * p * p - 12 * p + 2)
    if numerator % 3:
        raise AssertionError(f"p={p}: predicted numerator is not divisible by three")
    return numerator // 3


def low_pair_class(p: int, left: int, right: int) -> tuple[str, int] | None:
    """Return the predicted nonzero idealization class of a low quadratic monomial."""
    left_is_b = left >= 3 * p
    right_is_b = right >= 3 * p
    if left_is_b and right_is_b:
        return None
    kind = "AB" if left_is_b or right_is_b else "AA"
    normalized = left + right - (3 * p if kind == "AB" else 0)
    return kind, normalized


def colon_formula_row(p: int) -> dict[str, object]:
    if p < 4:
        raise ValueError("EXP-030 is declared only for p>=4")
    low = low_offsets(p)
    high = high_offsets(p)
    pair_fibers: dict[tuple[str, int], int] = {}
    killed_pairs = 0
    killed_pair_high_witnesses = 0
    for left, right in itertools.combinations_with_replacement(low, 2):
        key = low_pair_class(p, left, right)
        if key is None:
            killed_pairs += 1
            if left + right in set(high):
                killed_pair_high_witnesses += 1
        else:
            pair_fibers[key] = pair_fibers.get(key, 0) + 1

    low_variables = 2 * p
    low_degree_two_monomials = comb(low_variables + 1, 2)
    low_degree_two_dimension = len(pair_fibers)
    beta_low_1_2 = low_degree_two_monomials - low_degree_two_dimension
    beta_low_2_3 = 8 * p * (p - 1) * (p - 2) // 3
    extended = len(high) * beta_low_1_2 + beta_low_2_3
    predicted = predicted_beta_3_6(p)
    c = 2 * p - 2

    checks = {
        "all_generator_count": len(degree_one_offsets(p)) == 10 * p,
        "low_count": len(low) == 2 * p,
        "high_count": len(high) == 8 * p,
        "aa_class_count": sum(1 for key in pair_fibers if key[0] == "AA") == 2 * p + 1,
        "ab_class_count": sum(1 for key in pair_fibers if key[0] == "AB") == 2 * p - 1,
        "low_degree_two_dimension": low_degree_two_dimension == 4 * p,
        "bb_count": killed_pairs == comb(p, 2),
        "bb_high_witness": killed_pair_high_witnesses == killed_pairs,
        "beta_low_1_2": beta_low_1_2 == p * (2 * p - 3),
        "hilbert_coefficient_2": beta_low_1_2 == c * (c + 1) // 2 - 1,
        "hilbert_coefficient_3": beta_low_2_3 == c * (c - 2) * (c + 2) // 3,
        "extended_colon_coefficient": extended == predicted,
    }
    controls = {
        "missing_bb_rejected": low_degree_two_dimension + killed_pairs != 4 * p,
        "shifted_ab_rejected": {value + 1 for kind, value in pair_fibers if kind == "AB"}
        != set(range(0, 2 * p - 1)),
        "wrong_high_count_rejected": (8 * p - 1) * beta_low_1_2 + beta_low_2_3 != predicted,
        "perturbed_numerator_rejected": 8 * p * (7 * p * p - 12 * p + 3) // 3 != predicted,
    }
    if not all(checks.values()):
        raise AssertionError(f"p={p}: colon formula check failed: {checks}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial control failed: {controls}")

    row: dict[str, object] = {
        "p": p,
        "low_variable_count": len(low),
        "high_variable_count": len(high),
        "low_degree_two_monomials": low_degree_two_monomials,
        "low_degree_two_quotient_dimension": low_degree_two_dimension,
        "low_quadratic_generator_count": beta_low_1_2,
        "low_beta_2_3": beta_low_2_3,
        "extended_colon_beta_2_3": extended,
        "predicted_beta_3_6": predicted,
        "checks": checks,
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


def explicit_profile(
    p: int,
    primes: tuple[int, ...],
    checkpoint: Path,
    started: float,
    budget_seconds: float,
) -> dict[str, object]:
    profile_started = time.perf_counter()
    total_degree = 6
    generators = sorted(degree_one_offsets(p))
    cumulative = cumulative_offsets(p)
    grouped = {size: grouped_combinations(generators, size) for size in (2, 3, 4)}
    maximum = max(
        max(grouped[size]) + max(cumulative[total_degree - size]) for size in grouped
    )
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
            if h2 < 0:
                raise AssertionError(f"p={p}, offset={offset}: negative homology rank")
            if h2:
                profiles[str(prime)][offset] = h2

        if offset % 25 == 0 or offset == maximum:
            elapsed = time.perf_counter() - started
            print(f"explicit p={p}: offset {offset}/{maximum}, elapsed={elapsed:.3f}s", flush=True)
            write_json_atomic(
                checkpoint,
                {
                    "stage": "explicit",
                    "p": p,
                    "completed_offset": offset,
                    "maximum_offset": maximum,
                    "elapsed_seconds": elapsed,
                },
            )
            if elapsed > budget_seconds:
                raise TimeoutError(f"p={p}: explicit route exceeded {budget_seconds} seconds")

    totals = {prime: sum(profile.values()) for prime, profile in profiles.items()}
    predicted = predicted_beta_3_6(p)
    profiles_agree = len({canonical_hash(list(profile.items())) for profile in profiles.values()}) == 1
    prediction_matches = all(total == predicted for total in totals.values())
    result: dict[str, object] = {
        "p": p,
        "total_degree": total_degree,
        "primes": list(primes),
        "maximum_offset_checked": maximum,
        "combination_counts_2_to_4": [
            sum(len(value) for value in grouped[size].values()) for size in (2, 3, 4)
        ],
        "maximum_cell_counts_2_to_4": [maximum_cells[size] for size in (2, 3, 4)],
        "h2_profiles": {
            prime: {str(offset): value for offset, value in sorted(profile.items())}
            for prime, profile in profiles.items()
        },
        "h2_totals": totals,
        "predicted_total": predicted,
        "profiles_agree": profiles_agree,
        "prediction_matches": prediction_matches,
        "elapsed_seconds": time.perf_counter() - profile_started,
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
    parser.add_argument("--output", type=Path)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--budget-seconds", type=float, default=900.0)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        args.p_min = 4
        args.p_max = 4
        args.explicit = "4"
        args.large_prime_p = "4"
        args.budget_seconds = min(args.budget_seconds, 120.0)
    if args.p_min < 4 or args.p_max < args.p_min:
        raise ValueError("invalid parameter range")

    output = args.output or HERE / "artifacts" / ("smoke-results.json" if args.smoke else "results.json")
    checkpoint = args.checkpoint or HERE / "artifacts" / (
        "smoke-checkpoint.json" if args.smoke else "checkpoint.json"
    )
    started = time.perf_counter()
    premise_hashes = verify_premises()
    formula_rows = []
    explicit_rows = []

    try:
        for p in range(args.p_min, args.p_max + 1):
            formula_rows.append(colon_formula_row(p))
            if p == args.p_min or p == args.p_max or p % 25 == 0:
                print(f"colon formula p={p}/{args.p_max}", flush=True)
            write_json_atomic(
                checkpoint,
                {"stage": "formula", "completed_p": p, "elapsed_seconds": time.perf_counter() - started},
            )
            if time.perf_counter() - started > args.budget_seconds:
                raise TimeoutError(f"formula route exceeded {args.budget_seconds} seconds")

        explicit_parameters = parse_ints(args.explicit)
        large_prime_parameters = set(parse_ints(args.large_prime_p))
        for p in explicit_parameters:
            primes = (2, 1000003) if p in large_prime_parameters else (2,)
            row = explicit_profile(p, primes, checkpoint, started, args.budget_seconds)
            explicit_rows.append(row)
            print(
                f"explicit p={p}: totals={row['h2_totals']} predicted={row['predicted_total']}",
                flush=True,
            )

        target_matches = all(
            row["profiles_agree"] and row["prediction_matches"] for row in explicit_rows
        )
        status = "PASS" if target_matches else "REFUTED"
    except TimeoutError as error:
        payload = {
            "experiment": "EXP-030-colon-idealization-degree-six",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "INCONCLUSIVE_BUDGET",
            "mode": "smoke" if args.smoke else "canonical",
            "completed_formula_rows": len(formula_rows),
            "completed_explicit": [row["p"] for row in explicit_rows],
            "reason": str(error),
            "elapsed_seconds": time.perf_counter() - started,
        }
        write_json_atomic(output, payload)
        print(f"INCONCLUSIVE_BUDGET: {error}", flush=True)
        return 2

    payload: dict[str, object] = {
        "experiment": "EXP-030-colon-idealization-degree-six",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
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
    write_json_atomic(output, payload)
    write_json_atomic(
        checkpoint,
        {"stage": "complete", "status": status, "elapsed_seconds": payload["elapsed_seconds"]},
    )
    print(f"{status} aggregate={payload['campaign_aggregate']}", flush=True)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
