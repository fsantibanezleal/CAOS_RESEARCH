"""Independent formula and semantic audit for EXP-009."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT.parents[1] / "code"
sys.path.insert(0, str(CODE_ROOT))

from hwcert import analyze_rigidity, validate_symmetric_mask  # noqa: E402
from hwcert.semigroup import multiplicity  # noqa: E402


SAMPLES = (4, 5, 17, 73, 151, 300)


def independent_sets(p: int) -> tuple[int, set[int], set[int], set[int]]:
    shift = 6 * p
    a_set = {
        value
        for value in range(shift)
        if 0 <= value <= p or 3 * p <= value <= 4 * p - 2
    }
    b_set = {
        value
        for value in range(shift)
        if (
            p + 1 <= value <= 3 * p - 1
            and value != 2 * p - 1
            or value == 4 * p
            or 5 * p - 1 <= value <= 6 * p - 1
        )
    }
    c_set = {
        value for value in range(shift) if shift - 1 - value not in a_set
    }
    return shift, a_set, b_set, c_set


def independent_mask(p: int) -> tuple[int, int, tuple[int, ...]]:
    shift, a_set, b_set, c_set = independent_sets(p)
    frobenius = 13 * shift - 1

    def present(value: int) -> bool:
        if value == 0:
            return True
        if 4 * shift <= value < 5 * shift:
            return value - 4 * shift in a_set
        if 5 * shift <= value < 6 * shift:
            return True
        if 6 * shift <= value < 7 * shift:
            return value - 6 * shift in b_set
        if 8 * shift <= value < 9 * shift:
            return value - 8 * shift in c_set
        return 9 * shift <= value <= 13 * shift - 2

    mask = sum(1 << value for value in range(frobenius + 1) if present(value))
    generators = tuple(
        value
        for value in range(4 * shift, 7 * shift)
        if present(value)
    )
    return mask, frobenius, generators


def closure_failure(mask: int, frobenius: int) -> tuple[int, int] | None:
    window = (1 << (frobenius + 1)) - 1
    absent = (~mask) & window
    bits = mask
    while bits:
        low = bits & -bits
        left = low.bit_length() - 1
        failed = ((mask << left) & window) & absent
        if failed:
            total_low = failed & -failed
            total = total_low.bit_length() - 1
            return left, total - left
        bits ^= low
    return None


def generation_mask(generators: tuple[int, ...], frobenius: int) -> int:
    window = (1 << (frobenius + 1)) - 1
    one = sum(1 << value for value in generators)
    two = 0
    for value in generators:
        two |= one << value
    two &= window
    three = 0
    for value in generators:
        three |= two << value
    return (1 | one | two | three) & window


def direct_sumset(left: set[int], right: set[int]) -> set[int]:
    return {x + y for x in left for y in right}


def sample_audit(p: int, expected_hash: str) -> dict[str, object]:
    shift, a_set, b_set, c_set = independent_sets(p)
    mask, frobenius, generators = independent_mask(p)
    vector = format(mask, f"0{frobenius + 1}b")[::-1]
    digest = hashlib.sha256(vector.encode("ascii")).hexdigest()
    if digest != expected_hash:
        raise AssertionError(f"independent membership mismatch at p={p}")
    if p <= 17:
        failures = validate_symmetric_mask(mask, frobenius)
        if failures:
            raise AssertionError(f"standard semantic failure at p={p}: {failures}")
    if closure_failure(mask, frobenius) is not None:
        raise AssertionError(f"independent closure failure at p={p}")
    if generation_mask(generators, frobenius) != mask:
        raise AssertionError(f"independent generation failure at p={p}")
    if multiplicity(mask, frobenius) != 4 * shift:
        raise AssertionError(f"independent multiplicity failure at p={p}")
    rigidity = analyze_rigidity(mask, frobenius, shift)
    if not rigidity["rigid"]:
        raise AssertionError(f"independent rigidity failure at p={p}")

    aa = direct_sumset(a_set, a_set)
    ab = direct_sumset(a_set, b_set)
    bb = direct_sumset(b_set, b_set)
    ac = direct_sumset(a_set, c_set)
    identities = {
        "low_AA": {value for value in aa if value < shift} == c_set,
        "carry_AA": {value - shift for value in aa if value >= shift}
        == set(range(0, 2 * p - 3)),
        "low_AB": {value for value in ab if value < shift}
        == set(range(p + 1, shift)),
        "carry_AB": {value - shift for value in ab if value >= shift}
        == set(range(0, 4 * p - 2)),
        "low_BB": {value for value in bb if value < shift}
        == set(range(2 * p + 2, shift - 1)),
        "carry_BB": {value - shift for value in bb if value >= shift}
        == set(range(0, shift - 1)),
        "low_AC": {value for value in ac if value < shift}
        == set(range(0, shift - 1)),
    }
    if not all(identities.values()):
        raise AssertionError(f"independent sumset failure at p={p}: {identities}")
    return {
        "p": p,
        "membership_sha256": digest,
        "embedding_dimension": len(generators),
        "sumset_identities": identities,
        "rigidity_window_end": rigidity["window_end"],
        "rigidity_tail_start": rigidity["tail_start"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = json.loads(args.results.read_text(encoding="utf-8"))
    if results["status"] != "FINITE_SWEEP_PASS":
        raise AssertionError("finite campaign is not complete")
    rows = {int(row["p"]): row for row in results["results"]}
    if set(rows) != set(range(2, 301)):
        raise AssertionError("finite campaign parameter set is incomplete")
    for p in (2, 3):
        if rows[p]["accepted"]:
            raise AssertionError(f"boundary p={p} unexpectedly accepted")
    for p in range(4, 301):
        if not rows[p]["accepted"]:
            raise AssertionError(f"positive parameter p={p} is not accepted")
        mask, frobenius, generators = independent_mask(p)
        vector = format(mask, f"0{frobenius + 1}b")[::-1]
        digest = hashlib.sha256(vector.encode("ascii")).hexdigest()
        if digest != rows[p]["membership_sha256"]:
            raise AssertionError(f"all-row hash mismatch at p={p}")
        if len(generators) != 11 * p:
            raise AssertionError(f"generator count mismatch at p={p}")
    aggregate = hashlib.sha256(
        "\n".join(
            f"{row['p']}:{row['accepted']}:{row['membership_sha256']}:{row['first_failure']}"
            for row in results["results"]
        ).encode("ascii")
    ).hexdigest()
    if aggregate != results["aggregate_sha256"]:
        raise AssertionError("campaign aggregate mismatch")
    samples = [sample_audit(p, rows[p]["membership_sha256"]) for p in SAMPLES]
    audit = {
        "status": "PASS",
        "all_row_membership_hashes": 297,
        "boundary_controls": [2, 3],
        "independent_semantic_samples": list(SAMPLES),
        "samples": samples,
        "campaign_aggregate_sha256": aggregate,
    }
    audit["aggregate_sha256"] = hashlib.sha256(
        "\n".join(
            f"{sample['p']}:{sample['membership_sha256']}:{sample['rigidity_window_end']}"
            for sample in samples
        ).encode("ascii")
    ).hexdigest()
    args.output.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
