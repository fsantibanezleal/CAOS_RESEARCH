"""EXP-004 Route A: complete Blanco-Rosales tree and exact rigidity checks."""

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

from hwcert import (  # noqa: E402
    analyze_rigidity,
    enumerate_symmetric_masks,
    gap_values,
    minimal_generators,
    validate_symmetric_mask,
)
from hwcert.semigroup import root_mask  # noqa: E402


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def digest_rows(rows: list[str]) -> str:
    return hashlib.sha256("\n".join(rows).encode("ascii")).hexdigest()


def analyze_f(frobenius: int) -> dict[str, object]:
    masks = enumerate_symmetric_masks(frobenius)
    semigroup_rows: list[str] = []
    witness_rows: list[str] = []
    rigid_cases: list[dict[str, object]] = []
    gap_case_count = 0
    for mask in masks:
        bitstring = format(mask, f"0{frobenius + 1}b")[::-1]
        generators = minimal_generators(mask, frobenius)
        semigroup_rows.append(f"{bitstring}:{','.join(map(str, generators))}")
        for shift in gap_values(mask, frobenius):
            gap_case_count += 1
            result = analyze_rigidity(mask, frobenius, shift)
            if result["first_reverse_failure"] is not None:
                raise AssertionError("automatic inclusion E+E subset D failed")
            if result["rigid"]:
                rigid_cases.append(
                    {"membership": bitstring, "generators": generators, "shift": shift}
                )
            else:
                witness_rows.append(f"{bitstring}:{shift}:{result['first_missing_D']}")
    return {
        "frobenius": frobenius,
        "semigroup_count": len(masks),
        "gap_case_count": gap_case_count,
        "rigid_count": len(rigid_cases),
        "rigid_cases": rigid_cases,
        "semigroup_sha256": digest_rows(semigroup_rows),
        "witness_sha256": digest_rows(witness_rows),
        "first_semigroups": semigroup_rows[:6],
        "first_witnesses": witness_rows[:12],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-f", type=int, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--expect-smoke", action="store_true")
    args = parser.parse_args()
    if args.max_f <= 0 or args.max_f % 2 == 0:
        raise ValueError("--max-f must be positive and odd")
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.artifact_dir / "route-a-checkpoint.json"
    log_path = args.artifact_dir / "route-a.log"

    checkpoint: dict[str, object] = {"route": "A", "completed": [], "results": {}}
    if checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    completed = set(checkpoint["completed"])
    results = checkpoint["results"]

    def log(message: str) -> None:
        line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {message}"
        print(line, flush=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    invalid = (root_mask(11) & ~(1 << 10)) | (1 << 1)
    mutation_failures = validate_symmetric_mask(invalid, 11)
    if not mutation_failures:
        raise AssertionError("P3 invalid tree mutation was accepted")
    log(f"P3 mutation rejected: {mutation_failures[0]}")

    started = time.perf_counter()
    for frobenius in range(1, args.max_f + 1, 2):
        key = str(frobenius)
        if frobenius in completed:
            log(f"resume F={frobenius} already complete")
            continue
        item_started = time.perf_counter()
        result = analyze_f(frobenius)
        results[key] = result
        completed.add(frobenius)
        checkpoint = {
            "route": "A",
            "max_f": args.max_f,
            "completed": sorted(completed),
            "results": results,
        }
        atomic_json(checkpoint_path, checkpoint)
        log(
            f"F={frobenius} semigroups={result['semigroup_count']} "
            f"gap_cases={result['gap_case_count']} rigid={result['rigid_count']} "
            f"seconds={time.perf_counter() - item_started:.6f}"
        )
        if result["rigid_count"]:
            raise AssertionError(f"counterexample found below frontier at F={frobenius}")

    if args.expect_smoke:
        f11 = results.get("11")
        if f11 is None or f11["semigroup_count"] != 6:
            raise AssertionError("P1 expected exactly six semigroups at F=11")
    aggregate_rows = [
        f"{key}:{results[key]['semigroup_sha256']}:{results[key]['witness_sha256']}"
        for key in sorted(results, key=int)
        if int(key) <= args.max_f
    ]
    summary = {
        "verdict": "NO_COUNTEREXAMPLE",
        "max_f": args.max_f,
        "odd_f_count": (args.max_f + 1) // 2,
        "semigroup_count": sum(
            results[str(value)]["semigroup_count"] for value in range(1, args.max_f + 1, 2)
        ),
        "gap_case_count": sum(
            results[str(value)]["gap_case_count"] for value in range(1, args.max_f + 1, 2)
        ),
        "aggregate_sha256": digest_rows(aggregate_rows),
        "seconds": time.perf_counter() - started,
        "results": {str(value): results[str(value)] for value in range(1, args.max_f + 1, 2)},
    }
    atomic_json(args.artifact_dir / "route-a-results.json", summary)
    log(
        f"COMPLETE max_f={args.max_f} semigroups={summary['semigroup_count']} "
        f"gap_cases={summary['gap_case_count']} seconds={summary['seconds']:.6f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
