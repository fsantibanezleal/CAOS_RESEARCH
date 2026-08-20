"""EXP-031 exact degree-seven relative-homology and unit-filler campaign.

CPU only. Finite-field ranks validate the implementation. The every-field theorem
requires the separately written integral matching proof.
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
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-024-extremal-betti-data/proof.md":
        "b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-027-relative-betti-strand/proof.md":
        "355ff5c7e4bbc74fc8a1e346aac041d77b3fbc758051dbc729836db6a259e0bc",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-030-colon-idealization-degree-six/proof.md":
        "1822095a7d16207b7d04261b7a6645f7ca51b01f490ba9d212a84ab7ca5bc729",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-030-colon-idealization-degree-six/verdict.md":
        "7f8d2fe3c61a0fc1f864452ca98d05d04e154496a2d45d2c8d8a7b32644de4d9",
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


def formula_row(p: int) -> dict[str, object]:
    if p < 4:
        raise ValueError("EXP-031 is declared only for p>=4")
    full = interval(0, 24 * p - 1)
    cumulative = cumulative_offsets(p)
    positive_low = interval(1, p) | interval(3 * p, 4 * p - 2)
    first_four = {1, 2, 3, 4}
    hole = 6 * p - 1
    checks = {
        "generator_count": len(degree_one_offsets(p)) == 10 * p,
        "degree_five_full": cumulative[5] == full,
        "degree_four_full": cumulative[4] == full,
        "degree_three_one_hole": cumulative[3] == full - {hole},
        "positive_low_count": len(positive_low) == 2 * p - 1,
        "four_universal_fillers": first_four <= positive_low,
        "three_vertices_cannot_exhaust_fillers": len(first_four) > 3,
        "filler_residual_interval": hole - 4 >= 0 and hole - 1 < 24 * p,
        "filler_residual_avoids_hole": all(hole - x != hole for x in first_four),
    }
    controls = {
        "zero_filler_rejected": hole not in cumulative[3],
        "wrong_zero_hole_rejected": all(-x not in cumulative[3] for x in first_four),
        "three_fillers_rejected": not any(x not in (1, 2, 3) for x in (1, 2, 3)),
        "wrong_full_degree_three_rejected": cumulative[3] != full,
    }
    if not all(checks.values()):
        raise AssertionError(f"p={p}: formula check failed: {checks}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial control failed: {controls}")
    row: dict[str, object] = {
        "p": p,
        "hole": hole,
        "generator_count": 10 * p,
        "positive_low_count": 2 * p - 1,
        "universal_filler_pool": sorted(first_four),
        "predicted_beta_3_7": 0,
        "checks": checks,
        "controls": controls,
    }
    row["row_hash"] = canonical_hash(row)
    return row


def filler_certificate(p: int) -> dict[str, object]:
    generators = sorted(degree_one_offsets(p) - {0})
    hole = 6 * p - 1
    filler_pool = (1, 2, 3, 4)
    used: dict[tuple[int, ...], tuple[int, ...]] = {}
    signs = {"1": 0, "-1": 0}
    offset_counts: dict[int, int] = {}
    for triangle in itertools.combinations(generators, 3):
        total_offset = sum(triangle) + hole
        filler = next(x for x in filler_pool if x not in triangle)
        tetrahedron = tuple(sorted((*triangle, filler)))
        residual = total_offset - sum(tetrahedron)
        if residual != hole - filler or residual not in cumulative_offsets(p)[3]:
            raise AssertionError(f"p={p}: invalid filler residual for {triangle}")
        critical_faces = []
        coefficient = None
        for position in range(4):
            face = tetrahedron[:position] + tetrahedron[position + 1 :]
            if total_offset - sum(face) == hole:
                critical_faces.append(face)
                coefficient = -1 if position % 2 else 1
        if critical_faces != [triangle] or coefficient not in (-1, 1):
            raise AssertionError(
                f"p={p}: filler does not have one unit critical face: {triangle}, {critical_faces}"
            )
        previous = used.setdefault(tetrahedron, triangle)
        if previous != triangle:
            raise AssertionError(f"p={p}: filler collision: {previous}, {triangle}")
        signs[str(coefficient)] += 1
        offset_counts[total_offset] = offset_counts.get(total_offset, 0) + 1

    expected = comb(10 * p - 1, 3)
    if len(used) != expected:
        raise AssertionError(f"p={p}: expected {expected} fillers, got {len(used)}")
    result: dict[str, object] = {
        "p": p,
        "critical_triangle_count": expected,
        "distinct_filler_count": len(used),
        "supported_offset_count": len(offset_counts),
        "minimum_offset": min(offset_counts),
        "maximum_offset": max(offset_counts),
        "unit_sign_counts": signs,
        "all_critical_rows_have_distinct_unit_fillers": True,
    }
    result["row_hash"] = canonical_hash(result)
    return result


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
                pivots[pivot] = {
                    row: (coefficient * inverse) % prime
                    for row, coefficient in vector.items()
                    if (coefficient * inverse) % prime
                }
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
    result: dict[int, list[tuple[int, ...]]] = {}
    for cell in itertools.combinations(generators, size):
        result.setdefault(sum(cell), []).append(cell)
    return result


def collect_cells(
    grouped: dict[int, list[tuple[int, ...]]], residuals: set[int], offset: int
) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    for residual in residuals:
        result.extend(grouped.get(offset - residual, ()))
    result.sort()
    return result


def explicit_profile(
    p: int,
    primes: tuple[int, ...],
    checkpoint: Path,
    started: float,
    budget_seconds: float,
) -> dict[str, object]:
    total_degree = 7
    profile_started = time.perf_counter()
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
            rank = rank_mod2 if prime == 2 else lambda cols, q=prime: rank_mod_prime(cols, q)
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
        "h2_totals": {prime: sum(profile.values()) for prime, profile in profiles.items()},
        "profiles_agree": len({canonical_hash(list(p.items())) for p in profiles.values()}) == 1,
        "prediction_matches": all(not profile for profile in profiles.values()),
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
    parser.add_argument("--fillers", default="4,5,6,7,8,9,10,11,12")
    parser.add_argument("--explicit", default="4,5")
    parser.add_argument("--large-prime-p", default="4")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--budget-seconds", type=float, default=900.0)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        args.p_min = args.p_max = 4
        args.fillers = "4"
        args.explicit = "4"
        args.large_prime_p = "4"
        args.budget_seconds = min(args.budget_seconds, 180.0)
    if args.p_min < 4 or args.p_max < args.p_min:
        raise ValueError("invalid parameter range")
    output = args.output or HERE / "artifacts" / (
        "smoke-results.json" if args.smoke else "results.json"
    )
    checkpoint = args.checkpoint or HERE / "artifacts" / (
        "smoke-checkpoint.json" if args.smoke else "checkpoint.json"
    )
    started = time.perf_counter()
    premise_hashes = verify_premises()
    formula_rows = []
    filler_rows = []
    explicit_rows = []
    try:
        for p in range(args.p_min, args.p_max + 1):
            formula_rows.append(formula_row(p))
        for p in parse_ints(args.fillers):
            filler_rows.append(filler_certificate(p))
            print(f"fillers p={p}: {filler_rows[-1]['critical_triangle_count']}", flush=True)
            if time.perf_counter() - started > args.budget_seconds:
                raise TimeoutError("filler route exceeded budget")
        large_prime = set(parse_ints(args.large_prime_p))
        for p in parse_ints(args.explicit):
            primes = (2, 1000003) if p in large_prime else (2,)
            row = explicit_profile(p, primes, checkpoint, started, args.budget_seconds)
            explicit_rows.append(row)
            print(f"explicit p={p}: totals={row['h2_totals']}", flush=True)
        status = "PASS" if all(
            row["profiles_agree"] and row["prediction_matches"] for row in explicit_rows
        ) else "REFUTED"
    except TimeoutError as error:
        payload = {
            "experiment": "EXP-031-final-third-row-vanishing",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "INCONCLUSIVE_BUDGET",
            "mode": "smoke" if args.smoke else "canonical",
            "completed_formula_rows": len(formula_rows),
            "completed_fillers": [row["p"] for row in filler_rows],
            "completed_explicit": [row["p"] for row in explicit_rows],
            "reason": str(error),
            "elapsed_seconds": time.perf_counter() - started,
        }
        write_json_atomic(output, payload)
        print(f"INCONCLUSIVE_BUDGET: {error}", flush=True)
        return 2
    payload: dict[str, object] = {
        "experiment": "EXP-031-final-third-row-vanishing",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "mode": "smoke" if args.smoke else "canonical",
        "range": [args.p_min, args.p_max],
        "premise_hashes": premise_hashes,
        "formula_rows": formula_rows,
        "filler_rows": filler_rows,
        "explicit_rows": explicit_rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    payload["campaign_aggregate"] = canonical_hash(
        {
            "premises": premise_hashes,
            "formula": [row["row_hash"] for row in formula_rows],
            "fillers": [row["row_hash"] for row in filler_rows],
            "explicit": [row["row_hash"] for row in explicit_rows],
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
