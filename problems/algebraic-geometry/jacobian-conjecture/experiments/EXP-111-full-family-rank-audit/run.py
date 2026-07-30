"""EXP-111: audit the full-family reduced GGHV rank computation.

CPU-only, exact rational input reduced modulo two primes.
Run from the repository root:
    python problems/algebraic-geometry/jacobian-conjecture/experiments/\
EXP-111-full-family-rank-audit/run.py
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from fractions import Fraction
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
E71_PATH = HERE.parent / "EXP-071-degree3-pair-necessaries" / "run.py"
PRIMES = (2_147_483_629, 2_147_483_587)
SEED = 20_260_729

spec = importlib.util.spec_from_file_location("exp071", E71_PATH)
exp071 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp071)

failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}" + (f"  {detail}" if detail else ""), flush=True)
    if not condition:
        failures.append(name)


def mod_fraction(value: Fraction, prime: int) -> int:
    numerator = value.numerator % prime
    denominator = value.denominator % prime
    return numerator * pow(denominator, prime - 2, prime) % prime


def modular_rank(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        inverse = pow(work[pivot_row][column], prime - 2, prime)
        work[pivot_row] = [
            entry * inverse % prime for entry in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % prime
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def forced_polynomial() -> dict[tuple[int, int], Fraction]:
    terms = {
        (index, 8 + index): Fraction(
            comb(8, index) * (-1) ** (8 - index)
        )
        for index in range(9)
    }
    terms[(1, 0)] = Fraction(1)
    return terms


def row_sets(
    forced: dict[tuple[int, int], Fraction],
    directions: list[tuple[int, int]],
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    forced_rows = set(exp071.bracket_terms(forced)) | {(2, 0)}
    complete_rows = set(forced_rows)
    for direction in directions:
        complete_rows.update(
            exp071.bracket_terms({direction: Fraction(1)})
        )
    complete_rows.add((2, 0))
    return sorted(forced_rows), sorted(complete_rows)


def matrix_at(
    values: list[Fraction],
    rows: list[tuple[int, int]],
    prime: int,
    forced: dict[tuple[int, int], Fraction],
    directions: list[tuple[int, int]],
) -> tuple[list[list[int]], list[list[int]]]:
    terms = dict(forced)
    for direction, value in zip(directions, values):
        if value:
            terms[direction] = terms.get(direction, Fraction(0)) + value

    row_index = {row: index for index, row in enumerate(rows)}
    matrix = [[0 for _ in exp071.NQ] for _ in rows]
    for row, columns in exp071.bracket_terms(terms).items():
        if row not in row_index:
            continue
        for column, value in columns.items():
            matrix[row_index[row]][column] = mod_fraction(
                Fraction(value), prime
            )

    augmented = [row[:] + [0] for row in matrix]
    augmented[row_index[(2, 0)]][-1] = 1
    return matrix, augmented


def main() -> None:
    print("=" * 78)
    print("EXP-111: full-family rank audit and EXP-110 correction")
    print("=" * 78)

    forced = forced_polynomial()
    directions = sorted(exp071.LOWER)
    forced_rows, complete_rows = row_sets(forced, directions)
    constant_column = exp071.NQ.index((0, 0))

    coefficient_systems = [forced] + [
        {direction: Fraction(1)} for direction in directions
    ]
    zero_constant_column = all(
        all(
            columns.get(constant_column, Fraction(0)) == 0
            for columns in exp071.bracket_terms(terms).values()
        )
        for terms in coefficient_systems
    )
    check(
        "1: the constant Q-column is identically zero",
        zero_constant_column,
        f"constant column index {constant_column}",
    )

    omitted_rows = sorted(set(complete_rows) - set(forced_rows))
    directions_with_omissions = []
    for direction in directions:
        new_rows = sorted(
            set(exp071.bracket_terms({direction: Fraction(1)}))
            - set(forced_rows)
        )
        if new_rows:
            directions_with_omissions.append(
                {"direction": list(direction), "rows": [list(row) for row in new_rows]}
            )
    check(
        "2: the forced-only row list omits lower-family equations",
        len(omitted_rows) == 13 and len(directions_with_omissions) == 14,
        (
            f"forced rows={len(forced_rows)}, complete rows={len(complete_rows)}, "
            f"omitted={len(omitted_rows)}, affected directions="
            f"{len(directions_with_omissions)}"
        ),
    )

    random_generator = random.Random(SEED)
    points: list[tuple[str, list[Fraction]]] = [
        ("pinned", [Fraction(0) for _ in directions])
    ]
    for trial in range(3):
        values = [
            Fraction(
                random_generator.randint(-9, 9),
                random_generator.randint(1, 5),
            )
            for _ in directions
        ]
        points.append((f"random-{trial + 1}", values))

    profiles: dict[str, dict[str, dict[str, list[int]]]] = {}
    all_profiles_correct = True
    for point_name, values in points:
        profiles[point_name] = {}
        for row_name, rows in (
            ("forced-only", forced_rows),
            ("complete", complete_rows),
        ):
            profiles[point_name][row_name] = {}
            for prime in PRIMES:
                matrix, augmented = matrix_at(
                    values, rows, prime, forced, directions
                )
                rank_matrix = modular_rank(matrix, prime)
                rank_augmented = modular_rank(augmented, prime)
                profiles[point_name][row_name][str(prime)] = [
                    rank_matrix,
                    rank_augmented,
                ]
                all_profiles_correct &= (
                    rank_matrix == 124 and rank_augmented == 125
                )
                print(
                    f"  {point_name:8s} {row_name:11s} mod {prime}: "
                    f"rank M={rank_matrix}, rank [M|b]={rank_augmented}",
                    flush=True,
                )
    check(
        "3: both row systems have the 124/125 profile at all declared points",
        all_profiles_correct,
        f"{len(points)} points over {len(PRIMES)} primes",
    )

    pinned_exact_record = (
        HERE.parent
        / "EXP-059-determinantal-certificate"
        / "verdict.md"
    ).read_text(encoding="utf-8")
    exact_pinned_certificate_recorded = (
        "rank[M|r] = 125 at the base" in pinned_exact_record
        and "explicit 125-row selection" in pinned_exact_record
        and "huge nonzero determinant" in pinned_exact_record
    )
    check(
        "4: an exact nonzero pinned augmented minor is already persisted",
        exact_pinned_certificate_recorded,
        "cross-check against EXP-059 verdict",
    )

    results = {
        "q_columns": len(exp071.NQ),
        "constant_column_index": constant_column,
        "lower_directions": len(directions),
        "forced_only_rows": len(forced_rows),
        "complete_rows": len(complete_rows),
        "omitted_rows": [list(row) for row in omitted_rows],
        "directions_with_omitted_rows": directions_with_omissions,
        "primes": list(PRIMES),
        "seed": SEED,
        "profiles": profiles,
        "structural_conclusion": (
            "rank(M)<=124 identically because the constant Q-column is zero"
        ),
        "generic_conclusion": (
            "the exact pinned augmented minor proves rank([M|b])=125 "
            "on a nonempty Zariski-open subset"
        ),
        "remaining_target": (
            "the common zero locus of augmented 125-minors, using the complete "
            "302-row system on residual strata"
        ),
    }
    artifacts = HERE / "artifacts"
    artifacts.mkdir(exist_ok=True)
    (artifacts / "results.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )

    print()
    print(
        "DECISION: EXP-110's all-125-minors-of-M target is structural and "
        "vacuous; audit augmented minors on the exceptional locus instead."
    )
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")


if __name__ == "__main__":
    main()
