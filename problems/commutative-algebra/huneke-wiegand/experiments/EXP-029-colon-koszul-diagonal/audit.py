"""Independent exact audit for EXP-029."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path

from sympy import SparseMatrix


HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE / "artifacts" / "results.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit.json"


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def integers(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def generators(p: int) -> list[int]:
    values = (
        {0}
        | integers(1, p)
        | integers(3 * p, 4 * p - 2)
        | integers(6 * p, 8 * p - 2)
        | integers(8 * p, 10 * p - 2)
        | {10 * p}
        | integers(11 * p - 1, 12 * p - 1)
        | integers(13 * p + 1, 14 * p - 2)
        | integers(14 * p, 15 * p - 1)
        | {16 * p}
        | integers(17 * p - 1, 18 * p - 1)
    )
    return sorted(values)


def bases(p: int) -> list[set[int]]:
    full = integers(0, 24 * p - 1)
    return [
        {0},
        set(generators(p)),
        integers(0, 2 * p) | integers(3 * p, 5 * p - 2) | integers(6 * p, 24 * p - 1),
        full - {6 * p - 1},
        full,
        full,
    ]


def pair_profile(p: int) -> dict[int, int]:
    high = [value for value in generators(p) if value >= 6 * p]
    profile: dict[int, int] = {}
    for left_index in range(len(high)):
        for right_index in range(left_index + 1, len(high)):
            offset = 3 * p + high[left_index] + high[right_index]
            profile[offset] = profile.get(offset, 0) + 1
    return dict(sorted(profile.items()))


def cells(p: int, offset: int) -> dict[int, list[tuple[int, ...]]]:
    degree = 5
    cumulative = bases(p)
    values = generators(p)
    return {
        size: [
            cell
            for cell in itertools.combinations(values, size)
            if offset - sum(cell) in cumulative[degree - size]
        ]
        for size in (2, 3, 4)
    }


def boundary_matrix(
    upper: list[tuple[int, ...]], lower: list[tuple[int, ...]]
) -> SparseMatrix:
    lower_index = {cell: index for index, cell in enumerate(lower)}
    entries: dict[tuple[int, int], int] = {}
    for column, cell in enumerate(upper):
        for position in range(len(cell)):
            face = cell[:position] + cell[position + 1 :]
            if face in lower_index:
                entries[(lower_index[face], column)] = -1 if position % 2 else 1
    return SparseMatrix(len(lower), len(upper), entries)


def rational_h2(p: int, offset: int) -> dict[str, object]:
    block = cells(p, offset)
    d3 = boundary_matrix(block[3], block[2])
    d4 = boundary_matrix(block[4], block[3])
    rank3 = d3.rank()
    rank4 = d4.rank()
    return {
        "p": p,
        "offset": offset,
        "cell_counts_2_to_4": [len(block[size]) for size in (2, 3, 4)],
        "rank_d3": rank3,
        "rank_d4": rank4,
        "h2": len(block[3]) - rank3 - rank4,
    }


def coefficient_five(p: int) -> int:
    c = 10 * p - 1
    h = [1, c, 12 * p, 2 * p - 1, 1]
    return sum(h[r] * (-1) ** (5 - r) * comb(c, 5 - r) for r in range(5))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    source = json.loads(args.source.read_text(encoding="utf-8"))
    if source.get("status") != "PASS":
        raise RuntimeError("source campaign is not PASS")

    samples = []
    source_rows = {row["p"]: row for row in source["formula_rows"]}
    for p in (4, 5, 17, 73, 151, 300):
        profile = pair_profile(p)
        beta35 = sum(profile.values())
        beta25 = p * (2 * p - 3)
        beta45 = coefficient_five(p) - beta25 + beta35
        expected45 = 2 * p * (5 * p - 1) * (10 * p - 3) * (100 * p * p - 110 * p + 13) // 3
        row = {
            "p": p,
            "high_count": len([value for value in generators(p) if value >= 6 * p]),
            "beta_3_5": beta35,
            "beta_4_5": beta45,
            "support_count": len(profile),
            "profile_hash": canonical_hash(list(profile.items())),
        }
        if p in source_rows:
            expected = source_rows[p]
            if row["beta_3_5"] != expected["beta_3_5"]:
                raise AssertionError(f"p={p}: source beta mismatch")
            if row["profile_hash"] != expected["profile_hash"]:
                raise AssertionError(f"p={p}: source profile mismatch")
        if beta35 != comb(8 * p, 2) or beta45 != expected45:
            raise AssertionError(f"p={p}: independent formula mismatch")
        samples.append(row)

    rational = [rational_h2(4, offset) for offset in (60, 61)]
    expected = pair_profile(4)
    if any(row["h2"] != expected.get(row["offset"], 0) for row in rational):
        raise AssertionError("independent rational ranks disagree")

    payload: dict[str, object] = {
        "experiment": "EXP-029-colon-koszul-diagonal",
        "status": "PASS",
        "source_aggregate": source["campaign_aggregate"],
        "samples": samples,
        "rational_rows": rational,
    }
    payload["audit_aggregate"] = canonical_hash(payload)
    write_json_atomic(args.output, payload)
    print(f"PASS audit_aggregate={payload['audit_aggregate']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

