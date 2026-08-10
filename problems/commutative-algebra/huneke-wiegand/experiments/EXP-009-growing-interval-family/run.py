"""EXP-009: exact evaluation of the growing interval family."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT.parents[1] / "code"
sys.path.insert(0, str(CODE_ROOT))

from hwcert import analyze_rigidity  # noqa: E402
from hwcert.semigroup import member, multiplicity  # noqa: E402


ROUTE_K_HASHES = {
    4: "5692f234e4398fd967e3dc94a9c203067a3c0634dfbedb9c19143003100bd017",
    5: "5ec44ddea51b09125614e0b9518463483ff1fb218d0ad6d704a3c916d1a3887e",
}


def interval(left: int, right: int) -> set[int]:
    return set(range(left, right + 1)) if left <= right else set()


def residue_sets(p: int) -> tuple[int, set[int], set[int], set[int]]:
    if p < 1:
        raise ValueError("p must be positive")
    shift = 6 * p
    a_set = interval(0, p) | interval(3 * p, 4 * p - 2)
    b_set = (
        (interval(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | interval(5 * p - 1, 6 * p - 1)
    )
    c_set = set(range(shift)) - {shift - 1 - value for value in a_set}
    return shift, a_set, b_set, c_set


def formula_mask(p: int) -> tuple[int, int, tuple[int, ...]]:
    shift, a_set, b_set, c_set = residue_sets(p)
    frobenius = 13 * shift - 1
    values = {
        0,
        *(4 * shift + residue for residue in a_set),
        *range(5 * shift, 6 * shift),
        *(6 * shift + residue for residue in b_set),
        *(8 * shift + residue for residue in c_set),
        *range(9 * shift, 13 * shift - 1),
    }
    lower_generators = tuple(
        sorted(
            {
                *(4 * shift + residue for residue in a_set),
                *range(5 * shift, 6 * shift),
                *(6 * shift + residue for residue in b_set),
            }
        )
    )
    return sum(1 << value for value in values), frobenius, lower_generators


def set_bits(values: set[int]) -> int:
    return sum(1 << value for value in values)


def sumset(left: set[int], right: set[int]) -> set[int]:
    right_bits = set_bits(right)
    sums = 0
    for value in left:
        sums |= right_bits << value
    return {index for index in range(sums.bit_length()) if sums & (1 << index)}


def low_and_carry(left: set[int], right: set[int], shift: int) -> tuple[set[int], set[int]]:
    sums = sumset(left, right)
    return (
        {value for value in sums if value < shift},
        {value - shift for value in sums if shift <= value < 2 * shift},
    )


def expected_sumsets(p: int) -> dict[str, set[int]]:
    shift = 6 * p
    return {
        "low_AA": interval(0, 2 * p) | interval(3 * p, 5 * p - 2),
        "carry_AA": interval(0, 2 * p - 4),
        "low_AB": interval(p + 1, 6 * p - 1),
        "carry_AB": interval(0, 4 * p - 3),
        "low_BB": interval(2 * p + 2, 6 * p - 2),
        "carry_BB": interval(0, 6 * p - 2),
        "low_AC": interval(0, shift - 2),
    }


def sumset_record(p: int, a_set: set[int], b_set: set[int], c_set: set[int]) -> dict[str, object]:
    shift = 6 * p
    low_aa, carry_aa = low_and_carry(a_set, a_set, shift)
    low_ab, carry_ab = low_and_carry(a_set, b_set, shift)
    low_bb, carry_bb = low_and_carry(b_set, b_set, shift)
    low_ac, _ = low_and_carry(a_set, c_set, shift)
    actual = {
        "low_AA": low_aa,
        "carry_AA": carry_aa,
        "low_AB": low_ab,
        "carry_AB": carry_ab,
        "low_BB": low_bb,
        "carry_BB": carry_bb,
        "low_AC": low_ac,
    }
    expected = expected_sumsets(p)
    failures = [name for name in expected if actual[name] != expected[name]]
    return {
        "passed": not failures,
        "failures": failures,
        "hashes": {
            name: hashlib.sha256(
                ",".join(map(str, sorted(values))).encode("ascii")
            ).hexdigest()
            for name, values in actual.items()
        },
    }


def generated_mask(generators: tuple[int, ...], frobenius: int) -> int:
    window = (1 << (frobenius + 1)) - 1
    generator_bits = sum(1 << value for value in generators if value <= frobenius)
    pair_bits = 0
    for generator in generators:
        pair_bits |= generator_bits << generator
    pair_bits &= window
    triple_bits = 0
    for generator in generators:
        triple_bits |= pair_bits << generator
    return (1 | generator_bits | pair_bits | triple_bits) & window


def first_bit(bits: int) -> int | None:
    return (bits & -bits).bit_length() - 1 if bits else None


def symmetry_failure(mask: int, frobenius: int) -> int | None:
    return next(
        (
            value
            for value in range(frobenius + 1)
            if member(mask, frobenius, value)
            == member(mask, frobenius, frobenius - value)
        ),
        None,
    )


def closure_failure(mask: int, frobenius: int) -> tuple[int, int] | None:
    window = (1 << (frobenius + 1)) - 1
    missing = (~mask) & window
    members = mask
    while members:
        low = members & -members
        left = low.bit_length() - 1
        failure_bits = ((mask << left) & window) & missing
        if failure_bits:
            total = first_bit(failure_bits)
            assert total is not None
            return left, total - left
        members ^= low
    return None


def analyze_p(p: int, full_window: bool = True) -> dict[str, object]:
    shift, a_set, b_set, c_set = residue_sets(p)
    mask, frobenius, lower_generators = formula_mask(p)
    failures: list[str] = []
    expected_c = interval(0, 2 * p) | interval(3 * p, 5 * p - 2)
    if c_set != expected_c:
        failures.append("C interval formula mismatch")
    if len(a_set) != 2 * p or len(b_set) != 3 * p:
        failures.append("A/B cardinality mismatch")
    if a_set & b_set:
        failures.append(f"A/B overlap begins at {min(a_set & b_set)}")
    reflected_b_failure = next(
        (
            residue
            for residue in range(shift)
            if (residue in b_set) == (shift - 1 - residue in b_set)
        ),
        None,
    )
    if reflected_b_failure is not None:
        failures.append(f"B reflection fails at {reflected_b_failure}")
    sumsets = sumset_record(p, a_set, b_set, c_set)
    if not sumsets["passed"]:
        failures.append(f"sumset identities fail: {sumsets['failures']}")
    generated = generated_mask(lower_generators, frobenius)
    generation_difference = first_bit(mask ^ generated)
    if generation_difference is not None:
        failures.append(f"lower generation differs at {generation_difference}")
    reflected = symmetry_failure(mask, frobenius)
    if reflected is not None:
        failures.append(f"symmetry fails at {reflected}")
    closure = closure_failure(mask, frobenius)
    if closure is not None:
        failures.append(f"closure fails at {closure}")
    if multiplicity(mask, frobenius) != 4 * shift:
        failures.append("multiplicity mismatch")
    rigidity = analyze_rigidity(mask, frobenius, shift) if full_window else None
    if rigidity is not None and not rigidity["rigid"]:
        failures.append(f"rigidity fails at D={rigidity['first_missing_D']}")
    vector = format(mask, f"0{frobenius + 1}b")[::-1]
    digest = hashlib.sha256(vector.encode("ascii")).hexdigest()
    if p in ROUTE_K_HASHES and digest != ROUTE_K_HASHES[p]:
        failures.append("Route K source-model hash mismatch")
    # Every displayed generator is below 7s, while the sum of two positive members is at least
    # 8s. Hence all displayed values are minimal. Exact equality of the generated mask with the
    # formula then proves that there are no additional minimal generators.
    embedding_dimension = len(lower_generators) if generation_difference is None else 0
    return {
        "p": p,
        "shift": shift,
        "frobenius": frobenius,
        "accepted": not failures,
        "failures": failures,
        "first_failure": failures[0] if failures else None,
        "membership_sha256": digest,
        "A_count": len(a_set),
        "B_count": len(b_set),
        "C_count": len(c_set),
        "embedding_dimension": embedding_dimension,
        "expected_embedding_dimension": 11 * p,
        "sumsets": sumsets,
        "generation_first_difference": generation_difference,
        "symmetry_failure": reflected,
        "closure_failure": closure,
        "rigidity": rigidity,
    }


def affine_record(p: int) -> dict[str, object]:
    """Check the all-parameter affine obligations without the slower generic census."""
    shift, a_set, b_set, c_set = residue_sets(p)
    mask, frobenius, lower_generators = formula_mask(p)
    expected_c = interval(0, 2 * p) | interval(3 * p, 5 * p - 2)
    sumsets = sumset_record(p, a_set, b_set, c_set)
    reflected_b_failure = next(
        (
            residue
            for residue in range(shift)
            if (residue in b_set) == (shift - 1 - residue in b_set)
        ),
        None,
    )
    vector = format(mask, f"0{frobenius + 1}b")[::-1]
    digest = hashlib.sha256(vector.encode("ascii")).hexdigest()
    failures: list[str] = []
    if c_set != expected_c:
        failures.append("C interval formula mismatch")
    if len(a_set) != 2 * p or len(b_set) != 3 * p:
        failures.append("A/B cardinality mismatch")
    if a_set & b_set:
        failures.append(f"A/B overlap begins at {min(a_set & b_set)}")
    if reflected_b_failure is not None:
        failures.append(f"B reflection fails at {reflected_b_failure}")
    if not sumsets["passed"]:
        failures.append(f"sumset identities fail: {sumsets['failures']}")
    if p < 4:
        failures.append("level-9 endpoint inequality 2p-4>=p fails")
    if p in ROUTE_K_HASHES and digest != ROUTE_K_HASHES[p]:
        failures.append("Route K source-model hash mismatch")
    return {
        "p": p,
        "shift": shift,
        "frobenius": frobenius,
        "accepted": not failures,
        "failures": failures,
        "first_failure": failures[0] if failures else None,
        "membership_sha256": digest,
        "A_count": len(a_set),
        "B_count": len(b_set),
        "C_count": len(c_set),
        "embedding_dimension": len(lower_generators),
        "expected_embedding_dimension": 11 * p,
        "sumsets": sumsets,
        "generation_first_difference": None,
        "symmetry_failure": reflected_b_failure,
        "closure_failure": None,
        "rigidity": None,
        "proof_mode": "affine interval obligations",
    }


def corruption_record(p: int) -> dict[str, object]:
    shift, _, _, _ = residue_sets(p)
    mask, frobenius, _ = formula_mask(p)
    endpoint_corruption = mask & ~(1 << (4 * shift + p))
    endpoint_failure = symmetry_failure(endpoint_corruption, frobenius)
    omitted_selector_corruption = mask | (1 << (6 * shift + 2 * p - 1))
    selector_failure = symmetry_failure(omitted_selector_corruption, frobenius)
    if endpoint_failure is None or selector_failure is None:
        raise AssertionError("an adversarial corruption was not rejected")
    return {
        "p": p,
        "cleared_A_endpoint": 4 * shift + p,
        "endpoint_symmetry_failure": endpoint_failure,
        "added_omitted_B_residue": 2 * p - 1,
        "selector_symmetry_failure": selector_failure,
    }


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-p", type=int, default=2)
    parser.add_argument("--max-p", type=int, default=300)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.min_p != 2 or args.max_p < 5:
        raise ValueError("the declared sweep starts at p=2 and must include p=5")
    started = time.perf_counter()
    results: list[dict[str, object]] = []
    full_checkpoints = set(range(args.min_p, args.max_p + 1))
    for p in range(args.min_p, args.max_p + 1):
        result = analyze_p(p)
        results.append(result)
        print(
            f"p={p}/{args.max_p} s={result['shift']} accepted={result['accepted']} "
            f"first_failure={result['first_failure']}",
            flush=True,
        )
        if p in (2, 3):
            if result["accepted"]:
                raise AssertionError(f"negative boundary p={p} unexpectedly passed")
            continue
        if not result["accepted"]:
            break
    tested_positive = [result for result in results if int(result["p"]) >= 4]
    complete = (
        len(results) == args.max_p - args.min_p + 1
        and all(bool(result["accepted"]) for result in tested_positive)
    )
    corruptions = [corruption_record(4), corruption_record(5)]
    summary = {
        "status": "FINITE_SWEEP_PASS" if complete else "REFUTED_OR_INCOMPLETE",
        "declared_range": [args.min_p, args.max_p],
        "executed_p": [int(result["p"]) for result in results],
        "accepted_positive_count": sum(
            bool(result["accepted"]) for result in tested_positive
        ),
        "boundary_failures": {
            str(result["p"]): result["first_failure"]
            for result in results
            if int(result["p"]) in (2, 3)
        },
        "route_k_reproductions": ROUTE_K_HASHES,
        "full_standard_checkpoints": sorted(full_checkpoints),
        "corruptions": corruptions,
        "seconds": time.perf_counter() - started,
        "results": results,
    }
    summary["aggregate_sha256"] = hashlib.sha256(
        "\n".join(
            f"{result['p']}:{result['accepted']}:{result['membership_sha256']}:"
            f"{result['first_failure']}"
            for result in results
        ).encode("ascii")
    ).hexdigest()
    atomic_json(args.artifact_dir / "results.json", summary)
    print(json.dumps(summary, indent=2), flush=True)
    return 0 if complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
