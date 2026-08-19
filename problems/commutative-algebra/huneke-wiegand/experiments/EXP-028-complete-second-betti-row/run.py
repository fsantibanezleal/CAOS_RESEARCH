"""EXP-028 exact campaign for the complete second Betti row."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"

PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-024-extremal-betti-data/proof.md":
        "b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-025-curvilinear-primary-structure/proof.md":
        "70c7838ce843252aba335d80ade105d1d1942c490530ea7770483be0dff9a61f",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-026-grevlex-staircase/proof.md":
        "765fa23534be9e534fd507dff0e447e967345e4d2a485f7da6fdf0383b04fb56",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-027-relative-betti-strand/proof.md":
        "355ff5c7e4bbc74fc8a1e346aac041d77b3fbc758051dbc729836db6a259e0bc",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-027-relative-betti-strand/verdict.md":
        "fa0553e067fceb3ad538136e769ec19c2498dcf123af0df22f281dd3643e9f80",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-027-relative-betti-strand/artifacts/results.json":
        "06c630fc74d3e630f4dfbf47736313e6e40ff4e65a30acabe1e1a505b40a123f",
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


def outer_multiplicity(p: int, r: int) -> int:
    return min(r // 2 + 1, (2 * p - 4 - r) // 2 + 1)


def middle_multiplicity(p: int, r: int) -> int:
    return min(r + 1, 2 * p - 3 - r, p - 2)


def third_critical_multiplicity(p: int, r: int) -> int:
    if r == 2 * p - 4:
        return 1
    return min(r + 1, 2 * p - 4 - r, p - 2)


def degree_five_profile(p: int) -> dict[int, int]:
    profile: dict[int, int] = {}
    for r in range(2 * p - 3):
        profile[3 * p + 2 + r] = outer_multiplicity(p, r)
        profile[6 * p + 1 + r] = middle_multiplicity(p, r)
        profile[9 * p + r] = outer_multiplicity(p, 2 * p - 4 - r)
    return profile


def critical_edges(p: int, block: str, r: int) -> list[tuple[int, int]]:
    if block == "A":
        edges = [
            (i, j)
            for i in range(1, p + 1)
            for j in range(i + 1, p + 1)
            if i + j == r + 3
        ]
    elif block == "B":
        edges = [
            (i, j)
            for i in range(1, p + 1)
            for j in range(i + 1, p + 1)
            if i + j == r + 4
        ] + [
            (i, j)
            for i in range(2, p + 1)
            for j in range(i + 1, p + 1)
            if i + j == r + 3
        ]
    elif block == "C":
        edges = [
            (i, 3 * p + j)
            for i in range(2, p)
            for j in range(0, p - 1)
            if i + j == r + 2
        ]
        if r == 2 * p - 4:
            edges.append((p, 4 * p - 2))
    else:
        raise ValueError(f"unknown block {block}")
    return sorted(edges)


def formula_row(p: int) -> dict[str, object]:
    if p < 4:
        raise ValueError("EXP-028 is declared only for p>=4")
    profile = degree_five_profile(p)
    support = set(profile)
    a = interval(3 * p + 2, 5 * p - 2)
    b = interval(6 * p + 1, 8 * p - 3)
    c = interval(9 * p, 11 * p - 4)
    outer_sum = sum(outer_multiplicity(p, r) for r in range(2 * p - 3))
    middle_sum = sum(middle_multiplicity(p, r) for r in range(2 * p - 3))
    critical_counts = {
        "A": [outer_multiplicity(p, r) for r in range(2 * p - 3)],
        "B": [middle_multiplicity(p, r) for r in range(2 * p - 3)],
        "C": [third_critical_multiplicity(p, r) for r in range(2 * p - 3)],
    }
    enumerated_critical_counts = None
    if p in {4, 5, 17, 73, 151, 300}:
        enumerated_critical_counts = {
            block: [len(critical_edges(p, block, r)) for r in range(2 * p - 3)]
            for block in ("A", "B", "C")
        }
    predictions = {
        "generator_count": len(degree_one_offsets(p)) == 10 * p,
        "blocks_pairwise_disjoint": not (a & b or a & c or b & c),
        "support_is_three_blocks": support == a | b | c,
        "support_count": len(support) == 6 * p - 9,
        "outer_sum": outer_sum == p * (p - 1) // 2,
        "middle_sum": middle_sum == p * (p - 2),
        "beta_2_5": sum(profile.values()) == p * (2 * p - 3),
        "outer_reflection": all(
            profile[3 * p + 2 + r] == profile[11 * p - 4 - r]
            for r in range(2 * p - 3)
        ),
        "critical_A_count": critical_counts["A"]
        == [outer_multiplicity(p, r) for r in range(2 * p - 3)],
        "critical_B_count": critical_counts["B"]
        == [middle_multiplicity(p, r) for r in range(2 * p - 3)],
        "critical_C_count": critical_counts["C"]
        == [third_critical_multiplicity(p, r) for r in range(2 * p - 3)],
        "enumerated_critical_counts": (
            enumerated_critical_counts is None or enumerated_critical_counts == critical_counts
        ),
    }
    controls = {
        "deleted_support_endpoint_rejected": support - {min(a)} != a | b | c,
        "merged_blocks_rejected": interval(min(a), max(c)) != support,
        "outer_endpoint_mutation_rejected": sum(
            min(r // 2 + 1, (2 * p - 5 - r) // 2 + 1)
            for r in range(2 * p - 3)
        ) != outer_sum,
        "middle_plateau_mutation_rejected": sum(
            min(r + 1, 2 * p - 3 - r, p - 1) for r in range(2 * p - 3)
        ) != middle_sum,
        "third_critical_not_homology": any(
            third_critical_multiplicity(p, r) != outer_multiplicity(p, r)
            for r in range(2 * p - 3)
        ),
    }
    if not all(predictions.values()):
        raise AssertionError(f"p={p}: formula prediction failed: {predictions}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial mutation survived: {controls}")
    row: dict[str, object] = {
        "p": p,
        "beta_2_3": 2 * p * (500 * p * p - 330 * p + 31) // 3,
        "beta_2_4": 8 * p,
        "beta_2_5": sum(profile.values()),
        "beta_2_6": 0,
        "support_count": len(support),
        "support_hash": canonical_hash(sorted(profile.items())),
        "outer_block_total": outer_sum,
        "middle_block_total": middle_sum,
        "critical_count_hash": canonical_hash(critical_counts),
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


def fast_morse_critical(
    cells: dict[int, list[tuple[int, ...]]], generators: list[int]
) -> dict[int, list[tuple[int, ...]]]:
    unmatched = {frozenset(cell) for size in (1, 2, 3) for cell in cells[size]}
    ordered = sorted(unmatched, key=lambda face: (len(face), tuple(sorted(face))))
    for vertex in generators:
        for face in ordered:
            if face not in unmatched or vertex in face:
                continue
            coface = face | {vertex}
            if coface in unmatched:
                unmatched.remove(face)
                unmatched.remove(coface)
    answer: dict[int, list[tuple[int, ...]]] = {0: [], 1: [], 2: []}
    for face in unmatched:
        answer[len(face) - 1].append(tuple(sorted(face)))
    for dimension in answer:
        answer[dimension].sort()
    return answer


def explicit_profile(p: int, total_degree: int, primes: tuple[int, ...]) -> dict[str, object]:
    started = time.perf_counter()
    generators = sorted(degree_one_offsets(p))
    bases = cumulative_offsets(p)
    combinations = {
        size: [(sum(cell), cell) for cell in itertools.combinations(generators, size)]
        for size in (1, 2, 3)
    }
    maximum = max(
        max(value for value, _ in combinations[size]) + max(bases[total_degree - size])
        for size in (1, 2, 3)
    )
    expected = degree_five_profile(p) if total_degree == 5 else {}
    profiles: dict[str, dict[int, int]] = {str(prime): {} for prime in primes}
    critical_hashes = []
    degree_six_critical_edges = []

    for offset in range(maximum + 1):
        cells = {
            size: [
                cell
                for cell_sum, cell in combinations[size]
                if offset - cell_sum in bases[total_degree - size]
            ]
            for size in (1, 2, 3)
        }
        vertex_index = {cell: index for index, cell in enumerate(cells[1])}
        edge_index = {cell: index for index, cell in enumerate(cells[2])}
        d2 = boundary_columns(cells[2], vertex_index)
        d3 = boundary_columns(cells[3], edge_index)
        for prime in primes:
            rank = rank_mod2 if prime == 2 else lambda columns, q=prime: rank_mod_prime(columns, q)
            h1 = len(cells[2]) - rank(d2) - rank(d3)
            if h1:
                profiles[str(prime)][offset] = h1

        if total_degree == 5 and offset in expected:
            if 3 * p + 2 <= offset <= 5 * p - 2:
                block, r = "A", offset - (3 * p + 2)
            elif 6 * p + 1 <= offset <= 8 * p - 3:
                block, r = "B", offset - (6 * p + 1)
            else:
                block, r = "C", offset - 9 * p
            critical = fast_morse_critical(cells, generators)
            predicted_edges = critical_edges(p, block, r)
            if critical[1] != predicted_edges:
                raise AssertionError(
                    f"p={p}, degree={total_degree}, offset={offset}: "
                    f"critical edge mismatch {critical[1]} != {predicted_edges}"
                )
            critical_hashes.append(canonical_hash({"offset": offset, "critical": critical}))
        elif total_degree == 6:
            critical = fast_morse_critical(cells, generators)
            if critical[1]:
                degree_six_critical_edges.append({"offset": offset, "edges": critical[1]})

    expected_profile = {offset: value for offset, value in sorted(expected.items())}
    if any(profile != expected_profile for profile in profiles.values()):
        raise AssertionError(
            f"p={p}, degree={total_degree}: relative H1 profile mismatch {profiles}"
        )
    if degree_six_critical_edges:
        raise AssertionError(f"p={p}, degree=6: unmatched critical edges")
    return {
        "p": p,
        "total_degree": total_degree,
        "primes": list(primes),
        "maximum_offset_checked": maximum,
        "combination_counts_1_to_3": [len(combinations[size]) for size in (1, 2, 3)],
        "h1_profiles": {
            prime: {str(offset): value for offset, value in sorted(profile.items())}
            for prime, profile in profiles.items()
        },
        "h1_total": sum(expected_profile.values()),
        "critical_aggregate": canonical_hash(critical_hashes),
        "degree_six_no_critical_edges": (
            not degree_six_critical_edges if total_degree == 6 else None
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }


def parse_explicit(value: str) -> list[int]:
    return [int(item) for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--explicit-five", default="4,5,6")
    parser.add_argument("--explicit-six", default="4")
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()

    if args.first < 4 or args.last < args.first:
        raise SystemExit("require 4 <= first <= last")
    explicit_five = parse_explicit(args.explicit_five)
    explicit_six = parse_explicit(args.explicit_six)
    started = time.perf_counter()
    premises = verify_premises()
    rows = []
    status = "PASS"
    for p in range(args.first, args.last + 1):
        if time.perf_counter() - started > args.budget_seconds:
            status = "INCONCLUSIVE_BUDGET"
            break
        rows.append(formula_row(p))
        write_json_atomic(
            args.checkpoint,
            {
                "experiment": "EXP-028",
                "status": "RUNNING",
                "last_completed": p,
                "row_hashes": [row["row_hash"] for row in rows],
            },
        )

    explicit = []
    if status == "PASS":
        for p in explicit_five:
            if time.perf_counter() - started > args.budget_seconds:
                status = "INCONCLUSIVE_BUDGET"
                break
            primes = (2, 1_000_003) if p == min(explicit_five) else (2,)
            explicit.append(explicit_profile(p, 5, primes))
    if status == "PASS":
        for p in explicit_six:
            if time.perf_counter() - started > args.budget_seconds:
                status = "INCONCLUSIVE_BUDGET"
                break
            explicit.append(explicit_profile(p, 6, (2, 1_000_003)))

    result = {
        "experiment": "EXP-028-complete-second-betti-row",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "range": {"first": args.first, "requested_last": args.last},
        "completed_rows": len(rows),
        "premise_hashes": premises,
        "campaign_aggregate": canonical_hash([row["row_hash"] for row in rows]),
        "explicit_profiles": explicit,
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    write_json_atomic(args.output, result)
    write_json_atomic(
        args.checkpoint,
        {
            "experiment": "EXP-028",
            "status": status,
            "last_completed": rows[-1]["p"] if rows else None,
            "row_hashes": [row["row_hash"] for row in rows],
            "explicit": [[row["p"], row["total_degree"]] for row in explicit],
        },
    )
    print(
        f"EXP-028 {status}: rows={len(rows)} explicit={len(explicit)} "
        f"aggregate={result['campaign_aggregate']} elapsed={result['elapsed_seconds']:.3f}s"
    )
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
