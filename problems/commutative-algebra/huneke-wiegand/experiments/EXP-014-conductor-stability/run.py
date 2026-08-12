"""EXP-014: exact conductor-stability defect for the EXP-009 family.

CPU only. Exact integer and bitset arithmetic. No randomness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "artifacts" / "results.json"


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def blocks(p: int) -> tuple[int, dict[int, set[int]]]:
    if p < 4:
        raise ValueError("EXP-014 is declared only for p>=4")
    s = 6 * p
    a = interval(0, p) | interval(3 * p, 4 * p - 2)
    b = (
        (interval(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | interval(5 * p - 1, 6 * p - 1)
    )
    c = interval(0, 2 * p) | interval(3 * p, 5 * p - 2)
    return s, {
        4: a,
        5: a | b,
        6: b,
        8: c,
        9: interval(0, s - 1),
        10: interval(0, s - 1),
        11: interval(0, s - 1),
        12: interval(0, s - 2),
    }


def residue_sum_bits(left: set[int], right: set[int]) -> int:
    """Return the exact Boolean Minkowski sum as a bitset."""
    if len(left) > len(right):
        left, right = right, left
    right_bits = sum(1 << value for value in right)
    result = 0
    for value in left:
        result |= right_bits << value
    return result


def ideal_bits(p: int, stop: int) -> int:
    s, level_blocks = blocks(p)
    result = 0
    for level, residues in level_blocks.items():
        result |= sum(1 << (level * s + residue) for residue in residues)
    if stop >= 13 * s:
        result |= ((1 << (stop - 13 * s + 1)) - 1) << (13 * s)
    return result & ((1 << (stop + 1)) - 1)


def square_bits(p: int, stop: int) -> int:
    s, level_blocks = blocks(p)
    levels = sorted(level_blocks)
    result = 0
    for index, left_level in enumerate(levels):
        for right_level in levels[index:]:
            base = (left_level + right_level) * s
            if base > stop:
                continue
            sums = residue_sum_bits(level_blocks[left_level], level_blocks[right_level])
            result |= sums << base
    return result & ((1 << (stop + 1)) - 1)


def bits_to_values(bits: int) -> list[int]:
    values: list[int] = []
    while bits:
        lowest = bits & -bits
        values.append(lowest.bit_length() - 1)
        bits ^= lowest
    return values


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def analyze_parameter(p: int) -> dict[str, object]:
    s, _ = blocks(p)
    stop = 17 * s - 1
    t_bits = ideal_bits(p, stop)
    t_square = square_bits(p, stop)
    principal_reduction = (t_bits << (4 * s)) & ((1 << (stop + 1)) - 1)
    if principal_reduction & ~t_square:
        witness = bits_to_values(principal_reduction & ~t_square)[0]
        raise AssertionError(f"p={p}: xT is not contained in T^2 at {witness}")

    defect_bits = t_square & ~principal_reduction
    defect = bits_to_values(defect_bits)
    declared_witness = 8 * s + p + 1
    if declared_witness not in defect:
        raise AssertionError(f"p={p}: declared witness {declared_witness} is absent")
    if not defect:
        raise AssertionError(f"p={p}: false stability")

    level_counts: dict[str, int] = {}
    level_hashes: dict[str, str] = {}
    for level in range(8, 17):
        residues = [value - level * s for value in defect if value // s == level]
        if residues:
            level_counts[str(level)] = len(residues)
            level_hashes[str(level)] = canonical_hash(residues)

    stable_control = principal_reduction
    if stable_control & ~principal_reduction or t_square == principal_reduction:
        raise AssertionError(f"p={p}: false-stability control was not rejected")

    row: dict[str, object] = {
        "p": p,
        "s": s,
        "stable": False,
        "declared_witness": declared_witness,
        "defect_length": len(defect),
        "first_defect": defect[0],
        "last_defect": defect[-1],
        "level_counts": level_counts,
        "level_hashes": level_hashes,
        "defect_hash": canonical_hash(defect),
        "false_stability_control_rejected": True,
    }
    row["row_hash"] = canonical_hash(row)
    return row


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--output", type=Path, default=RESULTS)
    args = parser.parse_args()
    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print(f"EXP-014 exact campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1, args.last} or p % 25 == 0:
            print(f"p={p}: NONSTABLE defect={rows[-1]['defect_length']}", flush=True)
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-014 exceeded its declared two-minute budget")
    aggregate = canonical_hash([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-014-conductor-stability",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "predictions": {
            "nonstable": "PASS",
            "declared_witness": "PASS",
            "exact_finite_defect": "PASS",
            "false_stability_control": "PASS",
            "all_parameter_defect_formula": "NOT_CLAIMED",
        },
        "campaign_aggregate": aggregate,
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    print(f"EXP-014 computational PASS aggregate={aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
