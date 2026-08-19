"""EXP-027 exact campaign for the first interior Betti strand."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"

PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-021-conductor-fiber-cone/proof.md":
        "463e609b256fc2e39a7f0056a5aa92d17e20d16c1f6861692a1ce7a18f88fe38",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-023-one-cubic-defining-ideal/proof.md":
        "4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-024-extremal-betti-data/proof.md":
        "b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-025-curvilinear-primary-structure/proof.md":
        "70c7838ce843252aba335d80ade105d1d1942c490530ea7770483be0dff9a61f",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-025-curvilinear-primary-structure/run.py":
        "42411e5f8a166bd4a4663b49dfa3c19808b283735d2d633517c632e876f0377d",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-026-grevlex-staircase/proof.md":
        "765fa23534be9e534fd507dff0e447e967345e4d2a485f7da6fdf0383b04fb56",
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
    return [
        {0},
        degree_one_offsets(p),
        interval(0, 2 * p) | interval(3 * p, 5 * p - 2) | interval(6 * p, q - 1),
        interval(0, q - 1) - {6 * p - 1},
        interval(0, q - 1),
    ]


def expected_support(p: int) -> set[int]:
    return (
        interval(9 * p, 11 * p - 2)
        | interval(11 * p, 13 * p - 2)
        | {13 * p}
        | interval(14 * p - 1, 15 * p - 1)
        | interval(16 * p + 1, 17 * p - 2)
        | interval(17 * p, 18 * p - 1)
        | {19 * p}
        | interval(20 * p - 1, 21 * p - 1)
    )


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


def center_offsets(p: int, generators: set[int]) -> set[int]:
    return {value for value in generators if value - p in generators and value + p in generators}


def validate_quadratic_path(path: list[tuple[int, ...]], generators: set[int]) -> bool:
    if any(any(value not in generators for value in state) for state in path):
        return False
    for left, right in itertools.pairwise(path):
        if len(left) != 4 or len(right) != 4 or sum(left) != sum(right):
            return False
        common = list(left)
        for value in right:
            if value in common:
                common.remove(value)
        if len(common) != 2:
            return False
    return True


def colon_path(p: int, a: int, generators: set[int]) -> tuple[str, list[tuple[int, ...]]]:
    start = tuple(sorted((0, 0, 3 * p, a)))
    target = tuple(sorted((p, p, p, a)))
    if a + p in generators and a + 2 * p in generators:
        path = [
            start,
            tuple(sorted((0, 0, p, a + 2 * p))),
            tuple(sorted((0, p, p, a + p))),
            target,
        ]
        kind = "forward_three_move"
    elif a == 7 * p - 1:
        path = [
            start,
            tuple(sorted((0, 1, 3 * p, 7 * p - 2))),
            tuple(sorted((0, 1, p, 9 * p - 2))),
            tuple(sorted((1, p, p, 8 * p - 2))),
            target,
        ]
        kind = "exceptional_bridge"
    else:
        centers = center_offsets(p, generators)
        witness = next(
            ((u, a - u) for u in sorted(generators) if a - u in centers),
            None,
        )
        if witness is None:
            raise AssertionError(f"p={p}, a={a}: no high-offset colon path")
        u, v = witness
        path = [
            start,
            tuple(sorted((0, 3 * p, u, v))),
            tuple(sorted((p, 3 * p, u, v - p))),
            tuple(sorted((p, p, u, v + p))),
            target,
        ]
        kind = "center_four_move"
    path = [state for index, state in enumerate(path) if index == 0 or state != path[index - 1]]
    if not validate_quadratic_path(path, generators):
        raise AssertionError(f"p={p}, a={a}: invalid {kind} path {path}")
    return kind, path


def hilbert_numerator_coefficient(p: int, degree: int) -> int:
    c = 10 * p - 1
    h = [1, 10 * p - 1, 12 * p, 2 * p - 1, 1]
    answer = 0
    for j in range(min(degree, len(h) - 1) + 1):
        k = degree - j
        if k <= c:
            answer += (-1) ** k * __import__("math").comb(c, k) * h[j]
    return answer


def formula_row(p: int) -> dict[str, object]:
    if p < 4:
        raise ValueError("EXP-027 is declared only for p>=4")
    generators = degree_one_offsets(p)
    high = {a for a in generators if a >= 6 * p}
    low = generators - high
    shifted_high = {3 * p + a for a in high}
    support = expected_support(p)
    path_kinds: dict[str, int] = defaultdict(int)
    witness_hashes = []
    for a in sorted(high):
        kind, path = colon_path(p, a, generators)
        path_kinds[kind] += 1
        witness_hashes.append(canonical_hash(path))

    low_obstructions = {
        a: {
            "total": 3 * p + a,
            "below_7p": 3 * p + a <= 7 * p - 2,
            "start_mid_parity": (1 if a <= p else 0),
            "target_mid_parity": (0 if a <= p else 1),
        }
        for a in sorted(low)
    }
    if not all(
        row["below_7p"] and row["start_mid_parity"] != row["target_mid_parity"]
        for row in low_obstructions.values()
    ):
        raise AssertionError(f"p={p}: low-offset parity obstruction failed")

    beta_24 = 8 * p
    beta_34 = p * (5 * p - 1) * (500 * p * p - 440 * p + 47) // 2
    q4 = hilbert_numerator_coefficient(p, 4)
    predictions = {
        "generator_count": len(generators) == 10 * p,
        "high_count": len(high) == beta_24,
        "support_is_shifted_high": support == shifted_high,
        "support_count": len(support) == beta_24,
        "colon_paths_cover_high": sum(path_kinds.values()) == beta_24,
        "low_parity_obstructions_cover_low": len(low_obstructions) == 2 * p,
        "hilbert_identity": q4 == beta_24 - beta_34,
        "beta_34_integral": (
            p * (5 * p - 1) * (500 * p * p - 440 * p + 47)
        ) % 2 == 0,
    }
    mutated_support = support - {min(support)}
    controls = {
        "deleted_support_endpoint_rejected": mutated_support != shifted_high,
        "shifted_support_rejected": {value + 1 for value in support} != shifted_high,
        "low_colon_candidate_rejected": bool(low_obstructions),
        "hilbert_sign_mutation_rejected": q4 != beta_24 + beta_34,
        "false_support_multiplicity_rejected": len(support) != beta_24 - 1,
    }
    if not all(predictions.values()):
        raise AssertionError(f"p={p}: formula prediction failed: {predictions}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial mutation survived: {controls}")

    row: dict[str, object] = {
        "p": p,
        "q": 24 * p,
        "generator_count": len(generators),
        "low_generator_count": len(low),
        "high_generator_count": len(high),
        "support_count": len(support),
        "support_min": min(support),
        "support_max": max(support),
        "support_hash": canonical_hash(sorted(support)),
        "colon_path_kind_counts": dict(sorted(path_kinds.items())),
        "colon_path_hash": canonical_hash(witness_hashes),
        "low_parity_obstruction_hash": canonical_hash(low_obstructions),
        "beta_2_4": beta_24,
        "hilbert_numerator_coefficient_4": q4,
        "beta_3_4": beta_34,
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
    upper: list[tuple[int, ...]],
    lower_index: dict[tuple[int, ...], int],
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


def cells_at_offset(
    b: int,
    combinations_by_size: dict[int, list[tuple[int, ...]]],
    bases: list[set[int]],
) -> dict[int, list[tuple[int, ...]]]:
    return {
        size: [
            cell
            for cell in combinations_by_size[size]
            if b - sum(cell) in bases[4 - size]
        ]
        for size in (1, 2, 3)
    }


def morse_critical_cells(
    cells: dict[int, list[tuple[int, ...]]], generators: list[int]
) -> dict[int, list[tuple[int, ...]]]:
    unmatched = {
        frozenset(cell)
        for size in (1, 2, 3)
        for cell in cells[size]
    }
    for vertex in generators:
        ordered = sorted(unmatched, key=lambda face: (len(face), tuple(sorted(face))))
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


def explicit_relative_profile(p: int, primes: tuple[int, ...]) -> dict[str, object]:
    started = time.perf_counter()
    generators = sorted(degree_one_offsets(p))
    bases = cumulative_offsets(p)
    combinations_by_size = {
        size: list(itertools.combinations(generators, size)) for size in (1, 2, 3)
    }
    maximum_b = max(
        max(generators) + max(bases[3]),
        2 * max(generators) + max(bases[2]),
        4 * max(generators),
    )
    support = expected_support(p)
    transient = interval(6 * p, 7 * p - 3)
    prime_profiles: dict[str, dict[int, int]] = {str(prime): {} for prime in primes}
    morse_critical_edges: dict[int, list[tuple[int, ...]]] = {}
    block_hashes = []

    for b in range(maximum_b + 1):
        cells = cells_at_offset(b, combinations_by_size, bases)
        vertex_index = {cell: index for index, cell in enumerate(cells[1])}
        edge_index = {cell: index for index, cell in enumerate(cells[2])}
        d2 = boundary_columns(cells[2], vertex_index)
        d3 = boundary_columns(cells[3], edge_index)
        for prime in primes:
            rank = rank_mod2 if prime == 2 else lambda columns, q=prime: rank_mod_prime(columns, q)
            h1 = len(cells[2]) - rank(d2) - rank(d3)
            if h1:
                prime_profiles[str(prime)][b] = h1

        critical = morse_critical_cells(cells, generators)
        if critical[1]:
            morse_critical_edges[b] = critical[1]
        if b in support:
            a = b - 3 * p
            if critical[0] != [(0,)] or critical[1] != [(p, a)]:
                raise AssertionError(
                    f"p={p}, b={b}: support Morse profile "
                    f"vertices={critical[0]} edges={critical[1]}"
                )
        elif b in transient:
            a = b - 3 * p
            expected_vertices = [(0,), (b - 6 * p + 2,)]
            if critical[0] != expected_vertices or critical[1] != [(p, a)]:
                raise AssertionError(
                    f"p={p}, b={b}: transient Morse profile "
                    f"vertices={critical[0]} edges={critical[1]}"
                )
        elif critical[1]:
            raise AssertionError(f"p={p}, b={b}: unexpected critical edge {critical[1]}")
        block_hashes.append(
            canonical_hash(
                {
                    "b": b,
                    "chain_sizes_1_to_3": [len(cells[size]) for size in (1, 2, 3)],
                    "h1": {prime: prime_profiles[prime].get(b, 0) for prime in prime_profiles},
                    "critical_0_to_2": critical,
                }
            )
        )

    expected_profile = {b: 1 for b in sorted(support)}
    if any(profile != expected_profile for profile in prime_profiles.values()):
        raise AssertionError(f"p={p}: relative H1 profile mismatch {prime_profiles}")
    if set(morse_critical_edges) != support | transient:
        raise AssertionError(f"p={p}: Morse critical support mismatch")
    return {
        "p": p,
        "primes": list(primes),
        "maximum_offset_checked": maximum_b,
        "combination_counts_1_to_3": [len(combinations_by_size[size]) for size in (1, 2, 3)],
        "h1_profiles": {
            prime: {str(b): value for b, value in sorted(profile.items())}
            for prime, profile in prime_profiles.items()
        },
        "h1_total": sum(expected_profile.values()),
        "morse_critical_edge_offsets": sorted(morse_critical_edges),
        "morse_transient_offsets": sorted(transient),
        "block_aggregate": canonical_hash(block_hashes),
        "elapsed_seconds": time.perf_counter() - started,
    }


def parse_explicit(value: str) -> list[int]:
    if not value.strip():
        return []
    return [int(item) for item in value.split(",")]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--explicit", default="4,5,6")
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()

    if args.first < 4 or args.last < args.first:
        raise SystemExit("require 4 <= first <= last")
    explicit_parameters = parse_explicit(args.explicit)
    if any(p < 4 for p in explicit_parameters):
        raise SystemExit("explicit parameters must be at least four")

    started = time.perf_counter()
    premise_hashes = verify_premises()
    rows = []
    status = "PASS"
    for p in range(args.first, args.last + 1):
        if time.perf_counter() - started > args.budget_seconds:
            status = "INCONCLUSIVE_BUDGET"
            break
        row = formula_row(p)
        rows.append(row)
        write_json_atomic(
            args.checkpoint,
            {
                "experiment": "EXP-027",
                "status": "RUNNING",
                "first": args.first,
                "requested_last": args.last,
                "last_completed": p,
                "row_hashes": [item["row_hash"] for item in rows],
            },
        )

    explicit = []
    if status == "PASS":
        for p in explicit_parameters:
            if time.perf_counter() - started > args.budget_seconds:
                status = "INCONCLUSIVE_BUDGET"
                break
            primes = (2, 1_000_003) if p == min(explicit_parameters) else (2,)
            explicit.append(explicit_relative_profile(p, primes))

    expected_rows = args.last - args.first + 1
    if len(rows) != expected_rows and status == "PASS":
        status = "INCONCLUSIVE"
    result = {
        "experiment": "EXP-027-relative-betti-strand",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "range": {"first": args.first, "requested_last": args.last},
        "completed_rows": len(rows),
        "premise_hashes": premise_hashes,
        "campaign_aggregate": canonical_hash([row["row_hash"] for row in rows]),
        "explicit_profiles": explicit,
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    write_json_atomic(args.output, result)
    write_json_atomic(
        args.checkpoint,
        {
            "experiment": "EXP-027",
            "status": status,
            "first": args.first,
            "requested_last": args.last,
            "last_completed": rows[-1]["p"] if rows else None,
            "row_hashes": [item["row_hash"] for item in rows],
            "explicit_parameters": [row["p"] for row in explicit],
        },
    )
    print(
        f"EXP-027 {status}: rows={len(rows)} explicit={len(explicit)} "
        f"aggregate={result['campaign_aggregate']} elapsed={result['elapsed_seconds']:.3f}s"
    )
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
