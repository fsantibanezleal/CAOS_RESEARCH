"""Independent EXP-028 audit using SymPy rational ranks and Smith forms."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from datetime import datetime, timezone
from pathlib import Path

from sympy import SparseMatrix, ZZ
from sympy.matrices.normalforms import smith_normal_form


HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE / "artifacts" / "results.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit.json"


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def generators(p: int) -> list[int]:
    return sorted(
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


def bases(p: int) -> list[set[int]]:
    q = 24 * p
    full = interval(0, q - 1)
    return [
        {0},
        set(generators(p)),
        interval(0, 2 * p) | interval(3 * p, 5 * p - 2) | interval(6 * p, q - 1),
        full - {6 * p - 1},
        full,
        full,
    ]


def cells(p: int, total_degree: int, offset: int) -> dict[int, list[tuple[int, ...]]]:
    values = generators(p)
    cumulative = bases(p)
    return {
        size: [
            cell
            for cell in itertools.combinations(values, size)
            if offset - sum(cell) in cumulative[total_degree - size]
        ]
        for size in (1, 2, 3)
    }


def signed_boundary(
    upper: list[tuple[int, ...]], lower: list[tuple[int, ...]]
) -> SparseMatrix:
    lower_index = {cell: index for index, cell in enumerate(lower)}
    entries = {}
    for column, cell in enumerate(upper):
        for position in range(len(cell)):
            face = cell[:position] + cell[position + 1 :]
            if face in lower_index:
                entries[(lower_index[face], column)] = -1 if position % 2 else 1
    return SparseMatrix(len(lower), len(upper), entries)


def smith_chord_audit(p: int, offset: int) -> dict[str, object]:
    block = cells(p, 5, offset)
    vertex_index = {cell[0]: index for index, cell in enumerate(block[1])}
    parent = list(range(len(block[1])))

    def find(value: int) -> int:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    tree = set()
    for edge in block[2]:
        if edge[0] not in vertex_index or edge[1] not in vertex_index:
            continue
        left, right = find(vertex_index[edge[0]]), find(vertex_index[edge[1]])
        if left != right:
            parent[left] = right
            tree.add(edge)
    chords = [edge for edge in block[2] if edge not in tree]
    chord_index = {edge: index for index, edge in enumerate(chords)}
    entries = {}
    for column, triangle in enumerate(block[3]):
        for position in range(3):
            face = triangle[:position] + triangle[position + 1 :]
            if face in chord_index:
                entries[(chord_index[face], column)] = -1 if position % 2 else 1
    presentation = SparseMatrix(len(chords), len(block[3]), entries)
    smith = smith_normal_form(presentation, domain=ZZ)
    invariants = [
        abs(int(smith[index, index]))
        for index in range(min(smith.shape))
        if smith[index, index]
    ]
    free_rank = len(chords) - len(invariants)
    return {
        "p": p,
        "offset": offset,
        "presentation_shape": list(presentation.shape),
        "nonzero_smith_factors": invariants,
        "all_nonzero_factors_are_units": all(value == 1 for value in invariants),
        "free_rank": free_rank,
    }


def rational_rank_audit(p: int, total_degree: int, offset: int) -> dict[str, object]:
    block = cells(p, total_degree, offset)
    d2 = signed_boundary(block[2], block[1])
    d3 = signed_boundary(block[3], block[2])
    rank_d2 = d2.rank()
    rank_d3 = d3.rank()
    return {
        "p": p,
        "total_degree": total_degree,
        "offset": offset,
        "chain_sizes": [len(block[size]) for size in (1, 2, 3)],
        "rational_ranks": [rank_d2, rank_d3],
        "h1": len(block[2]) - rank_d2 - rank_d3,
    }


def expected_outer(p: int, r: int) -> int:
    return min(r // 2 + 1, (2 * p - 4 - r) // 2 + 1)


def expected_middle(p: int, r: int) -> int:
    return min(r + 1, 2 * p - 3 - r, p - 2)


def formula_audit(source: dict[str, object], p: int) -> dict[str, object]:
    source_row = next(row for row in source["rows"] if row["p"] == p)
    outer = sum(expected_outer(p, r) for r in range(2 * p - 3))
    middle = sum(expected_middle(p, r) for r in range(2 * p - 3))
    expected_beta = 2 * outer + middle
    checks = {
        "outer_sum": outer == p * (p - 1) // 2,
        "middle_sum": middle == p * (p - 2),
        "beta_2_5": source_row["beta_2_5"] == expected_beta == p * (2 * p - 3),
        "beta_2_6": source_row["beta_2_6"] == 0,
        "support_count": source_row["support_count"] == 6 * p - 9,
    }
    if not all(checks.values()):
        raise AssertionError(f"p={p}: independent formula audit failed {checks}")
    return {"p": p, "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    source_bytes = args.source.read_bytes()
    source = json.loads(source_bytes)
    if source["status"] != "PASS":
        raise RuntimeError("canonical source is not PASS")
    formula_rows = [formula_audit(source, p) for p in (4, 5, 17, 73, 151, 300)]
    smith_rows = [smith_chord_audit(4, offset) for offset in (14, 27, 37, 38)]
    rational_rows = [
        rational_rank_audit(4, 5, offset) for offset in (14, 16, 25, 27, 36, 37, 38, 40)
    ] + [rational_rank_audit(4, 6, offset) for offset in (23, 30, 200)]
    expected_h1 = {14: 1, 16: 2, 25: 1, 27: 2, 36: 1, 37: 1, 38: 2, 40: 1}
    chain_checks = {
        "degree_five_rational_ranks": all(
            row["h1"] == expected_h1[row["offset"]]
            for row in rational_rows
            if row["total_degree"] == 5
        ),
        "degree_six_rational_vanishing": all(
            row["h1"] == 0 for row in rational_rows if row["total_degree"] == 6
        ),
        "smith_quotients_torsion_free": all(
            row["all_nonzero_factors_are_units"] for row in smith_rows
        ),
        "smith_free_ranks": [row["free_rank"] for row in smith_rows] == [1, 2, 1, 2],
    }
    controls = {
        "beta_minus_one_rejected": source["rows"][0]["beta_2_5"] != 4 * (2 * 4 - 3) - 1,
        "degree_six_one_rejected": source["rows"][0]["beta_2_6"] != 1,
        "nonunit_smith_factor_rejected": all(
            2 not in row["nonzero_smith_factors"] for row in smith_rows
        ),
    }
    status = "PASS" if all(chain_checks.values()) and all(controls.values()) else "FAIL"
    payload = {
        "experiment": "EXP-028-independent-audit",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "formula_rows": formula_rows,
        "smith_rows": smith_rows,
        "rational_rows": rational_rows,
        "checks": chain_checks,
        "controls": controls,
    }
    write_json_atomic(args.output, payload)
    print(f"EXP-028 audit {status}: source={payload['source_sha256']}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

