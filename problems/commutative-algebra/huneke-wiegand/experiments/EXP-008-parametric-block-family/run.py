"""EXP-008: exact finite evaluation of the declared interval family."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT.parents[1] / "code"
sys.path.insert(0, str(CODE_ROOT))

from hwcert import (  # noqa: E402
    analyze_rigidity,
    minimal_generators,
    validate_symmetric_mask,
)
from hwcert.semigroup import multiplicity  # noqa: E402


def closed_interval(left: int, right: int) -> set[int]:
    return set(range(left, right + 1)) if left <= right else set()


def residue_sets(q: int) -> tuple[int, set[int], set[int], set[int]]:
    if q < 1:
        raise ValueError("q must be positive")
    shift = 4 * q + 2
    a_set = closed_interval(0, q - 2) | closed_interval(2 * q + 1, 2 * q + 4)
    b_set = (
        closed_interval(q - 1, q + 1)
        | closed_interval(q + 3, 2 * q)
        | {3 * q - 1}
        | closed_interval(3 * q + 3, 4 * q + 1)
    )
    reflected_a = {shift - 1 - value for value in a_set}
    c_set = set(range(shift)) - reflected_a
    return shift, a_set, b_set, c_set


def formula_mask(q: int) -> tuple[int, int, tuple[int, ...]]:
    shift, a_set, b_set, c_set = residue_sets(q)
    frobenius = 13 * shift - 1
    values = {
        0,
        *(4 * shift + residue for residue in a_set),
        *range(5 * shift, 6 * shift),
        *(6 * shift + residue for residue in b_set),
        *(8 * shift + residue for residue in c_set),
        *range(9 * shift, 13 * shift - 1),
    }
    mask = sum(1 << value for value in values)
    lower_generators = tuple(
        sorted(
            {
                *(4 * shift + residue for residue in a_set),
                *range(5 * shift, 6 * shift),
                *(6 * shift + residue for residue in b_set),
            }
        )
    )
    return mask, frobenius, lower_generators


def generated_mask(generators: tuple[int, ...], frobenius: int) -> int:
    present = bytearray(frobenius + 1)
    present[0] = 1
    for value in range(1, frobenius + 1):
        present[value] = any(
            value >= generator and present[value - generator]
            for generator in generators
        )
    return sum(1 << value for value, flag in enumerate(present) if flag)


def first_difference(left: int, right: int, limit: int) -> int | None:
    difference = (left ^ right) & ((1 << (limit + 1)) - 1)
    return (difference & -difference).bit_length() - 1 if difference else None


def analyze_q(q: int) -> dict[str, object]:
    shift, a_set, b_set, c_set = residue_sets(q)
    mask, frobenius, lower_generators = formula_mask(q)
    failures = list(validate_symmetric_mask(mask, frobenius))
    generated = generated_mask(lower_generators, frobenius)
    difference = first_difference(mask, generated, frobenius)
    if difference is not None:
        failures.append(f"lower-block generation first differs at {difference}")
    actual_multiplicity = multiplicity(mask, frobenius)
    if actual_multiplicity != 4 * shift:
        failures.append(
            f"multiplicity is {actual_multiplicity}, expected {4 * shift}"
        )
    overlap = sorted(a_set & b_set)
    if overlap:
        failures.append(f"A/B overlap begins at residue {overlap[0]}")
    reflected_b_failure = next(
        (
            residue
            for residue in range(shift)
            if (residue in b_set) == (shift - 1 - residue in b_set)
        ),
        None,
    )
    if reflected_b_failure is not None:
        failures.append(f"B reflection fails at residue {reflected_b_failure}")
    rigidity = analyze_rigidity(mask, frobenius, shift)
    if not rigidity["rigid"]:
        failures.append(f"rigidity fails first at D={rigidity['first_missing_D']}")
    vector = format(mask, f"0{frobenius + 1}b")[::-1]
    actual_generators = minimal_generators(mask, frobenius) if not failures else ()
    return {
        "q": q,
        "shift": shift,
        "frobenius": frobenius,
        "accepted": not failures,
        "failures": failures,
        "first_failure": failures[0] if failures else None,
        "membership_sha256": hashlib.sha256(vector.encode("ascii")).hexdigest(),
        "A": sorted(a_set),
        "B": sorted(b_set),
        "C": sorted(c_set),
        "A_B_overlap": overlap,
        "lower_generators": list(lower_generators),
        "actual_minimal_generators": list(actual_generators),
        "lower_generation_first_difference": difference,
        "rigidity": rigidity,
    }


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-q", type=int, default=5)
    parser.add_argument("--max-q", type=int, default=100)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.min_q != 5 or args.max_q < 9:
        raise ValueError("the declared run starts at q=5 and must reach at least q=9")
    results: list[dict[str, object]] = []
    for q in range(args.min_q, args.max_q + 1):
        result = analyze_q(q)
        results.append(result)
        print(
            f"q={q} s={result['shift']} accepted={result['accepted']} "
            f"first_failure={result['first_failure']}",
            flush=True,
        )
        if q == 5:
            if result["accepted"] or not result["A_B_overlap"]:
                raise AssertionError("declared q=5 overlap control did not reject")
            continue
        if not result["accepted"]:
            break
    accepted = [int(result["q"]) for result in results if result["accepted"]]
    first_failed = next(
        (int(result["q"]) for result in results if result["q"] >= 6 and not result["accepted"]),
        None,
    )
    summary = {
        "status": "REFUTED" if first_failed is not None else "FINITE_SWEEP_PASS",
        "requested_range": [args.min_q, args.max_q],
        "executed_q": [int(result["q"]) for result in results],
        "accepted_q": accepted,
        "first_failed_q_at_or_above_6": first_failed,
        "generalized_arithmetic_exclusion": {
            "status": "PROVED_FOR_PROPOSED_PARAMETERS",
            "argument": (
                "m and m+1 force h=1,d=1; the later member m+2q+1 would then "
                "force the declared gap m+q-1"
            ),
        },
        "results": results,
    }
    summary["aggregate_sha256"] = hashlib.sha256(
        "\n".join(
            f"{result['q']}:{result['accepted']}:{result['membership_sha256']}:"
            f"{result['first_failure']}"
            for result in results
        ).encode("ascii")
    ).hexdigest()
    atomic_json(args.artifact_dir / "results.json", summary)
    print(json.dumps(summary, indent=2), flush=True)
    return 0 if summary["status"] == "FINITE_SWEEP_PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
