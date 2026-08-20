"""Independent EXP-030 idealization-profile and rational-rank audit.

This file deliberately does not import run.py. It reconstructs the predicted colon
profile from the multigraded Hilbert numerator of the square-zero idealization and
checks selected relative complexes over QQ with SymPy.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from datetime import datetime, timezone
from math import comb
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
CANONICAL = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit.json"


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


def generators(p: int) -> list[int]:
    return sorted(
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


def low_generators(p: int) -> list[int]:
    return list(range(0, p + 1)) + list(range(3 * p, 4 * p - 1))


def high_generators(p: int) -> list[int]:
    low = set(low_generators(p))
    return [value for value in generators(p) if value not in low]


def add_profile(target: dict[int, int], source: dict[int, int], factor: int = 1) -> None:
    for offset, value in source.items():
        updated = target.get(offset, 0) + factor * value
        if updated:
            target[offset] = updated
        else:
            target.pop(offset, None)


def convolution(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    answer: dict[int, int] = {}
    for a, alpha in left.items():
        for b, beta in right.items():
            answer[a + b] = answer.get(a + b, 0) + alpha * beta
    return answer


def elementary_profile(values: list[int], size: int) -> dict[int, int]:
    answer: dict[int, int] = {}
    for choice in itertools.combinations(values, size):
        total = sum(choice)
        answer[total] = answer.get(total, 0) + 1
    return answer


def idealization_hilbert_profile(p: int, degree: int) -> dict[int, int]:
    if degree == 0:
        return {0: 1}
    answer = {offset: 1 for offset in range(0, degree * p + 1)}
    for offset in range(3 * p, (degree + 3) * p - 1):
        answer[offset] = answer.get(offset, 0) + 1
    return answer


def predicted_degree_six_profile(p: int) -> dict[int, int]:
    low = low_generators(p)
    e1 = {value: 1 for value in low}
    e2 = elementary_profile(low, 2)
    e3 = elementary_profile(low, 3)
    h0 = idealization_hilbert_profile(p, 0)
    h1 = idealization_hilbert_profile(p, 1)
    h2 = idealization_hilbert_profile(p, 2)
    h3 = idealization_hilbert_profile(p, 3)

    numerator_two = dict(h2)
    add_profile(numerator_two, convolution(e1, h1), -1)
    add_profile(numerator_two, convolution(e2, h0), 1)
    beta_low_1_2 = {offset: -value for offset, value in numerator_two.items()}

    numerator_three = dict(h3)
    add_profile(numerator_three, convolution(e1, h2), -1)
    add_profile(numerator_three, convolution(e2, h1), 1)
    add_profile(numerator_three, convolution(e3, h0), -1)
    beta_low_2_3 = dict(numerator_three)

    if any(value <= 0 for value in beta_low_1_2.values()):
        raise AssertionError(f"p={p}: nonpositive low beta_(1,2) profile")
    if any(value <= 0 for value in beta_low_2_3.values()):
        raise AssertionError(f"p={p}: nonpositive low beta_(2,3) profile")
    if sum(beta_low_1_2.values()) != p * (2 * p - 3):
        raise AssertionError(f"p={p}: low beta_(1,2) total mismatch")
    if sum(beta_low_2_3.values()) != 8 * p * (p - 1) * (p - 2) // 3:
        raise AssertionError(f"p={p}: low beta_(2,3) total mismatch")

    high_profile = {value: 1 for value in high_generators(p)}
    extended = dict(beta_low_2_3)
    add_profile(extended, convolution(high_profile, beta_low_1_2), 1)
    return dict(sorted((offset + 3 * p, value) for offset, value in extended.items()))


def cumulative_offsets(p: int) -> list[set[int]]:
    full = interval(0, 24 * p - 1)
    return [
        {0},
        set(generators(p)),
        interval(0, 2 * p) | interval(3 * p, 5 * p - 2) | interval(6 * p, 24 * p - 1),
        full - {6 * p - 1},
        full,
        full,
        full,
    ]


def cells_at(p: int, size: int, offset: int) -> list[tuple[int, ...]]:
    residuals = cumulative_offsets(p)[6 - size]
    return [
        cell
        for cell in itertools.combinations(generators(p), size)
        if offset - sum(cell) in residuals
    ]


def rational_boundary_rank(
    upper: list[tuple[int, ...]], lower: list[tuple[int, ...]]
) -> int:
    lower_index = {cell: row for row, cell in enumerate(lower)}
    entries: dict[tuple[int, int], int] = {}
    for column, cell in enumerate(upper):
        for position in range(len(cell)):
            face = cell[:position] + cell[position + 1 :]
            if face in lower_index:
                entries[(lower_index[face], column)] = -1 if position % 2 else 1
    matrix = sympy.MutableSparseMatrix(len(lower), len(upper), entries)
    return int(matrix.rank())


def rational_h2(p: int, offset: int) -> dict[str, object]:
    edges = cells_at(p, 2, offset)
    triangles = cells_at(p, 3, offset)
    tetrahedra = cells_at(p, 4, offset)
    rank_d3 = rational_boundary_rank(triangles, edges)
    rank_d4 = rational_boundary_rank(tetrahedra, triangles)
    h2 = len(triangles) - rank_d3 - rank_d4
    return {
        "p": p,
        "offset": offset,
        "cell_counts_2_to_4": [len(edges), len(triangles), len(tetrahedra)],
        "rank_d3": rank_d3,
        "rank_d4": rank_d4,
        "h2": h2,
    }


def main() -> int:
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))
    if canonical["status"] != "PASS":
        raise RuntimeError("canonical artifact is not PASS")

    profile_rows = []
    for row in canonical["explicit_rows"]:
        p = int(row["p"])
        predicted = predicted_degree_six_profile(p)
        observed = {int(offset): int(value) for offset, value in row["h2_profiles"]["2"].items()}
        matches = predicted == observed
        if not matches:
            raise AssertionError(f"p={p}: idealization profile does not match relative H2")
        total = sum(predicted.values())
        formula = 8 * p * (7 * p * p - 12 * p + 2) // 3
        if total != formula:
            raise AssertionError(f"p={p}: idealization total does not match formula")
        profile_rows.append(
            {
                "p": p,
                "support_count": len(predicted),
                "support_min": min(predicted),
                "support_max": max(predicted),
                "maximum_multiplicity": max(predicted.values()),
                "total": total,
                "profile_hash": canonical_hash(list(predicted.items())),
                "matches_canonical": matches,
            }
        )

    rational_rows = [rational_h2(4, offset) for offset in (16, 21, 37)]
    canonical_p4 = {
        int(offset): int(value)
        for offset, value in canonical["explicit_rows"][0]["h2_profiles"]["2"].items()
    }
    for row in rational_rows:
        if row["h2"] != canonical_p4.get(row["offset"], 0):
            raise AssertionError(f"rational boundary mismatch at offset {row['offset']}")

    controls = {
        "missing_bb_changes_profile": sum(predicted_degree_six_profile(4).values()) != 705,
        "perturbed_formula_rejected": sum(predicted_degree_six_profile(5).values())
        != 8 * 5 * (7 * 5 * 5 - 12 * 5 + 3) // 3,
        "gap_offset_is_zero": canonical_p4.get(21, 0) == 0,
    }
    if not all(controls.values()):
        raise AssertionError(f"adversarial control failed: {controls}")

    payload: dict[str, object] = {
        "experiment": "EXP-030-colon-idealization-degree-six",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "route": "independent idealization Hilbert numerator plus selected QQ ranks",
        "canonical_sha256": file_hash(CANONICAL),
        "canonical_aggregate": canonical["campaign_aggregate"],
        "sympy_version": sympy.__version__,
        "profile_rows": profile_rows,
        "rational_rows": rational_rows,
        "controls": controls,
    }
    payload["audit_aggregate"] = canonical_hash(
        {
            "profiles": profile_rows,
            "rational": rational_rows,
            "controls": controls,
            "canonical_sha256": payload["canonical_sha256"],
        }
    )
    write_json_atomic(OUTPUT, payload)
    print(f"PASS aggregate={payload['audit_aggregate']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
