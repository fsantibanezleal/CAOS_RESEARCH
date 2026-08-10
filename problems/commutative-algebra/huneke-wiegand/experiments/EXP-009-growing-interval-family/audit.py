"""Independent compact-artifact and exact-checkpoint audit for EXP-009."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT.parents[1] / "code"
sys.path.insert(0, str(CODE_ROOT))

from hwcert import analyze_rigidity, minimal_generators, validate_symmetric_mask  # noqa: E402


def block_mask(parameter: int) -> tuple[int, int, int]:
    shift = 6 * parameter
    frobenius = 13 * shift - 1
    set_a = set(range(parameter + 1)) | set(range(3 * parameter, 4 * parameter - 1))
    set_b = (
        (set(range(parameter + 1, 3 * parameter)) - {2 * parameter - 1})
        | {4 * parameter}
        | set(range(5 * parameter - 1, 6 * parameter))
    )
    set_c = set(range(shift)) - {shift - 1 - value for value in set_a}
    values = {
        0,
        *(4 * shift + value for value in set_a),
        *range(5 * shift, 6 * shift),
        *(6 * shift + value for value in set_b),
        *(8 * shift + value for value in set_c),
        *range(9 * shift, frobenius),
    }
    return sum(1 << value for value in values), frobenius, shift


def digest(mask: int, frobenius: int) -> str:
    vector = format(mask, f"0{frobenius + 1}b")[::-1]
    return hashlib.sha256(vector.encode("ascii")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.results.read_text(encoding="utf-8"))
    if source["status"] != "FINITE_SWEEP_PASS":
        raise AssertionError("source campaign is not complete")
    records = {int(item["p"]): item for item in source["results"]}
    rows: list[str] = []
    mismatches: list[int] = []
    for parameter in range(2, 301):
        mask, frobenius, _ = block_mask(parameter)
        current = digest(mask, frobenius)
        record = records[parameter]
        if current != record["membership_sha256"]:
            mismatches.append(parameter)
        rows.append(
            f"{parameter}:{record['accepted']}:{current}:{record['first_failure']}"
        )
    aggregate = hashlib.sha256("\n".join(rows).encode("ascii")).hexdigest()
    if aggregate != source["aggregate_sha256"] or mismatches:
        raise AssertionError(f"compact reconstruction failed: {mismatches}")

    checkpoints: dict[str, object] = {}
    for parameter in (2, 3, 4, 5, 10, 25, 50, 75):
        mask, frobenius, shift = block_mask(parameter)
        failures = validate_symmetric_mask(mask, frobenius)
        rigidity = analyze_rigidity(mask, frobenius, shift)
        generators = minimal_generators(mask, frobenius) if not failures else ()
        expected = parameter >= 4
        accepted = not failures and rigidity["rigid"]
        if accepted != expected:
            raise AssertionError(f"checkpoint disagreement at p={parameter}")
        if accepted and len(generators) != 11 * parameter:
            raise AssertionError(f"embedding dimension mismatch at p={parameter}")
        checkpoints[str(parameter)] = {
            "accepted": accepted,
            "semigroup_failures": failures,
            "rigidity": rigidity,
            "embedding_dimension": len(generators),
            "membership_sha256": digest(mask, frobenius),
        }
    output = {
        "status": "PASS",
        "reconstructed_parameters": 299,
        "membership_hash_mismatches": mismatches,
        "aggregate_sha256": aggregate,
        "fresh_standard_checkpoints": checkpoints,
    }
    args.artifact.parent.mkdir(parents=True, exist_ok=True)
    args.artifact.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
