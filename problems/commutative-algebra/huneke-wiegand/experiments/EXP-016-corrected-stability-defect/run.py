"""EXP-016: corrected exact conductor-stability defect.

CPU only. Exact integer and bitset arithmetic. No randomness.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "artifacts" / "results.json"
EXP014 = ROOT.parent / "EXP-014-conductor-stability" / "run.py"


def load_exact_engine() -> ModuleType:
    spec = importlib.util.spec_from_file_location("hw_exp014_engine", EXP014)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the EXP-014 exact engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ENGINE = load_exact_engine()


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def family_sets(p: int) -> tuple[int, set[int], set[int], set[int], set[int]]:
    s, layers = ENGINE.blocks(p)
    return s, set(layers[4]), set(layers[6]), set(layers[8]), set(layers[5])


def low_high(left: set[int], right: set[int], s: int) -> tuple[set[int], set[int]]:
    sums = {x + y for x in left for y in right}
    return {value for value in sums if value < s}, {
        value - s for value in sums if value >= s
    }


def identity_checks(p: int) -> dict[str, bool]:
    s, a, b, c, u = family_sets(p)
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
    if not all(checks.values()):
        raise AssertionError(f"p={p}: an affine residue identity failed")
    return checks


def expected_square(p: int, stop: int) -> set[int]:
    s, _, _, c, _ = family_sets(p)
    return (
        {8 * s + residue for residue in c}
        | interval(9 * s, 13 * s - 2)
        | interval(13 * s, stop)
    )


def expected_defect(p: int) -> set[int]:
    s, _, _, _, _ = family_sets(p)
    return (
        {8 * s + r for r in interval(p + 1, 2 * p) | interval(4 * p - 1, 5 * p - 2)}
        | {9 * s + r for r in {2 * p - 1, 4 * p - 1} | interval(4 * p + 1, 5 * p - 2)}
        | {
            10 * s + r
            for r in (
                interval(0, p)
                | {2 * p - 1}
                | interval(3 * p, 4 * p - 1)
                | interval(4 * p + 1, 5 * p - 2)
            )
        }
        | {11 * s + r for r in interval(0, s - 1)}
        | {12 * s + r for r in interval(2 * p + 1, 3 * p - 1) | interval(5 * p - 1, s - 2)}
        | {17 * s - 1}
    )


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def analyze_parameter(p: int) -> dict[str, object]:
    s, _, _, c, _ = family_sets(p)
    stop = 17 * s - 1
    checks = identity_checks(p)
    actual_square = set(ENGINE.bits_to_values(ENGINE.square_bits(p, stop)))
    predicted_square = expected_square(p, stop)
    if actual_square != predicted_square:
        witness = min(actual_square ^ predicted_square)
        raise AssertionError(f"p={p}: corrected square mismatch at {witness}")
    if 13 * s - 1 in actual_square:
        raise AssertionError(f"p={p}: EXP-015 false tail survived")
    if 17 * s - 1 not in actual_square:
        raise AssertionError(f"p={p}: terminal square endpoint is absent")

    t_values = set(ENGINE.bits_to_values(ENGINE.ideal_bits(p, stop)))
    shifted = {4 * s + value for value in t_values if 4 * s + value <= stop}
    actual_defect = actual_square - shifted
    predicted_defect = expected_defect(p)
    if actual_defect != predicted_defect:
        witness = min(actual_defect ^ predicted_defect)
        raise AssertionError(f"p={p}: corrected defect mismatch at {witness}")
    if len(actual_defect) != 14 * p:
        raise AssertionError(f"p={p}: defect length is not 14p")

    false_tail = predicted_square | {13 * s - 1}
    deleted_endpoint = predicted_square - {17 * s - 1}
    altered_c = c | {2 * p + 1}
    altered_level_eight = (
        {8 * s + residue for residue in altered_c}
        | interval(9 * s, 13 * s - 2)
        | interval(13 * s, stop)
    )
    controls = {
        "exp015_false_tail_rejected": false_tail != actual_square,
        "deleted_endpoint_rejected": deleted_endpoint != actual_square,
        "altered_c_rejected": altered_level_eight != actual_square,
    }
    if not all(controls.values()):
        raise AssertionError(f"p={p}: an adversarial control was not rejected")

    counts = {
        str(level): sum(value // s == level for value in actual_defect)
        for level in (8, 9, 10, 11, 12, 16)
    }
    row: dict[str, object] = {
        "p": p,
        "s": s,
        "frobenius_gap_retained": 13 * s - 1,
        "terminal_endpoint_filled": 17 * s - 1,
        "defect_length": len(actual_defect),
        "level_counts": counts,
        "identity_checks": checks,
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
    print(f"EXP-016 corrected campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1, args.last} or p % 25 == 0:
            print(f"p={p}: PASS defect=14p={14 * p}", flush=True)
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-016 exceeded its declared two-minute budget")
    aggregate = digest([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-016-corrected-stability-defect",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "predictions": {
            "corrected_square_formula": "PASS",
            "frobenius_gap_retained": "PASS",
            "exact_defect_formula": "PASS",
            "defect_length_14p": "PASS",
            "five_residue_identities": "PASS",
            "adversarial_controls": "PASS",
            "all_parameter_theorem": "PENDING_SYMBOLIC_PROOF",
        },
        "campaign_aggregate": aggregate,
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    print(f"EXP-016 computational PASS aggregate={aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
