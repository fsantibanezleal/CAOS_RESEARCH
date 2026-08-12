"""EXP-015: exact square and stability-defect formulas.

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


def family_blocks(p: int) -> tuple[int, set[int], set[int], set[int], set[int]]:
    if p < 4:
        raise ValueError("EXP-015 is declared only for p>=4")
    s = 6 * p
    a = interval(0, p) | interval(3 * p, 4 * p - 2)
    b = (
        (interval(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | interval(5 * p - 1, 6 * p - 1)
    )
    c = interval(0, 2 * p) | interval(3 * p, 5 * p - 2)
    return s, a, b, c, a | b


def sumset(left: set[int], right: set[int]) -> set[int]:
    return {x + y for x in left for y in right}


def low_high(left: set[int], right: set[int], s: int) -> tuple[set[int], set[int]]:
    sums = sumset(left, right)
    return {value for value in sums if value < s}, {
        value - s for value in sums if value >= s
    }


def verify_identities(p: int) -> dict[str, str]:
    s, a, b, c, u = family_blocks(p)
    full = interval(0, s - 1)
    aa = low_high(a, a, s)
    au = low_high(a, u, s)
    ab = low_high(a, b, s)
    uu = low_high(u, u, s)
    ub = low_high(u, b, s)
    bb = low_high(b, b, s)
    ac = low_high(a, c, s)
    checks = {
        "level_8": aa[0] == c,
        "level_9": aa[1] | au[0] == full,
        "level_10": au[1] | ab[0] | uu[0] == full,
        "level_11": ab[1] | uu[1] | ub[0] == full,
        "level_12": ub[1] | bb[0] | ac[0] == interval(0, s - 2),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(f"p={p}: residue identities failed: {failed}")
    return {name: "PASS" for name in checks}


def ideal_values(p: int, stop: int) -> set[int]:
    s, a, b, c, u = family_blocks(p)
    values = (
        {4 * s + residue for residue in a}
        | {5 * s + residue for residue in u}
        | {6 * s + residue for residue in b}
        | {8 * s + residue for residue in c}
        | interval(9 * s, 13 * s - 2)
    )
    return values | interval(13 * s, stop)


def residue_sum_bits(left: set[int], right: set[int]) -> int:
    if len(left) > len(right):
        left, right = right, left
    right_bits = sum(1 << value for value in right)
    result = 0
    for value in left:
        result |= right_bits << value
    return result


def exact_square(p: int, stop: int) -> set[int]:
    s, a, b, c, u = family_blocks(p)
    layers = {
        4: a,
        5: u,
        6: b,
        8: c,
        9: interval(0, s - 1),
        10: interval(0, s - 1),
        11: interval(0, s - 1),
        12: interval(0, s - 2),
    }
    bits = 0
    ordered = sorted(layers)
    for index, left_level in enumerate(ordered):
        for right_level in ordered[index:]:
            base = (left_level + right_level) * s
            if base <= stop:
                bits |= residue_sum_bits(layers[left_level], layers[right_level]) << base
    mask = (1 << (stop + 1)) - 1
    bits &= mask
    result: set[int] = set()
    while bits:
        lowest = bits & -bits
        result.add(lowest.bit_length() - 1)
        bits ^= lowest
    return result


def predicted_square(p: int, stop: int) -> set[int]:
    s, _, _, c, _ = family_blocks(p)
    return {8 * s + residue for residue in c} | interval(9 * s, stop)


def predicted_defect(p: int) -> set[int]:
    s, _, _, _, _ = family_blocks(p)
    return (
        {8 * s + residue for residue in interval(p + 1, 2 * p) | interval(4 * p - 1, 5 * p - 2)}
        | {
            9 * s + residue
            for residue in {2 * p - 1, 4 * p - 1} | interval(4 * p + 1, 5 * p - 2)
        }
        | {
            10 * s + residue
            for residue in (
                interval(0, p)
                | {2 * p - 1}
                | interval(3 * p, 4 * p - 1)
                | interval(4 * p + 1, 5 * p - 2)
            )
        }
        | {11 * s + residue for residue in interval(0, s - 1)}
        | {
            12 * s + residue
            for residue in interval(2 * p + 1, 3 * p - 1) | interval(5 * p - 1, s - 2)
        }
        | {17 * s - 1}
    )


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def analyze_parameter(p: int) -> dict[str, object]:
    s, _, _, c, _ = family_blocks(p)
    stop = 17 * s - 1
    identities = verify_identities(p)
    actual_square = exact_square(p, stop)
    expected_square = predicted_square(p, stop)
    if actual_square != expected_square:
        witness = min(actual_square ^ expected_square)
        raise AssertionError(f"p={p}: square formula mismatch at {witness}")

    t_values = ideal_values(p, stop)
    x_t = {4 * s + value for value in t_values if 4 * s + value <= stop}
    actual_defect = actual_square - x_t
    expected_defect = predicted_defect(p)
    if actual_defect != expected_defect:
        witness = min(actual_defect ^ expected_defect)
        raise AssertionError(f"p={p}: defect formula mismatch at {witness}")
    if len(actual_defect) != 14 * p:
        raise AssertionError(f"p={p}: defect length is not 14p")

    deleted_endpoint = expected_square - {17 * s - 1}
    injected_xt = x_t | {17 * s - 1}
    altered_c = c | {2 * p + 1}
    altered_square = {8 * s + residue for residue in altered_c} | interval(9 * s, stop)
    controls = {
        "deleted_endpoint_rejected": deleted_endpoint != actual_square,
        "injected_xt_rejected": injected_xt != x_t,
        "altered_c_rejected": altered_square != actual_square,
    }
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial control failed")

    counts = {
        str(level): sum(value // s == level for value in actual_defect)
        for level in (8, 9, 10, 11, 12, 16)
    }
    row: dict[str, object] = {
        "p": p,
        "s": s,
        "square_formula": "(8s+C) union [9s,infinity)",
        "defect_length": len(actual_defect),
        "level_counts": counts,
        "identity_checks": identities,
        "square_hash_through_17s_minus_1": digest(sorted(actual_square)),
        "defect_hash": digest(sorted(actual_defect)),
        "controls": controls,
    }
    row["row_hash"] = digest(row)
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
    print(f"EXP-015 exact campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1, args.last} or p % 25 == 0:
            print(f"p={p}: PASS defect=14p={14 * p}", flush=True)
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-015 exceeded its declared two-minute budget")
    aggregate = digest([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-015-exact-stability-defect",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "predictions": {
            "five_residue_identities": "PASS",
            "exact_square_formula": "PASS",
            "exact_defect_formula": "PASS",
            "defect_length_14p": "PASS",
            "adversarial_controls": "PASS",
            "all_parameter_theorem": "PENDING_SYMBOLIC_PROOF",
        },
        "campaign_aggregate": aggregate,
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    print(f"EXP-015 computational PASS aggregate={aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
