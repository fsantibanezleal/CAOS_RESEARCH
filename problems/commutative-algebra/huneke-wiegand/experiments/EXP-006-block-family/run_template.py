"""EXP-006 Route G: falsify or validate the fixed-offset block template."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT.parents[1] / "code"
sys.path.insert(0, str(CODE_ROOT))

from hwcert import analyze_rigidity, minimal_generators, validate_symmetric_mask  # noqa: E402


SEED_GENERATORS = (
    56,
    57,
    58,
    63,
    64,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    87,
    89,
    90,
    93,
    95,
    96,
    97,
)
LEVEL4_OFFSETS = (0, 1, 2, 7, 8)
LEVEL6_OFFSETS = (3, 5, 6, 9, 11, 12, 13)


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def digest_rows(rows: list[str]) -> str:
    return hashlib.sha256("\n".join(rows).encode("ascii")).hexdigest()


def template_generators(shift: int) -> tuple[int, ...]:
    if shift < 14 or shift % 2:
        raise ValueError("the declared template requires even s>=14")
    values = {
        *(4 * shift + offset for offset in LEVEL4_OFFSETS),
        *(5 * shift + offset for offset in range(shift)),
        *(6 * shift + offset for offset in LEVEL6_OFFSETS),
    }
    return tuple(sorted(values))


def generated_mask(generators: tuple[int, ...]) -> tuple[int, int]:
    if not generators or math.gcd(*generators) != 1:
        raise ValueError("generators must have gcd one")
    multiplicity = min(generators)
    limit = max(generators) + 4 * multiplicity * multiplicity
    present = bytearray(limit + 1)
    present[0] = 1
    consecutive = 0
    conductor: int | None = None
    for value in range(1, limit + 1):
        present[value] = any(
            value >= generator and present[value - generator] for generator in generators
        )
        consecutive = consecutive + 1 if present[value] else 0
        if consecutive == multiplicity:
            conductor = value - multiplicity + 1
            break
    if conductor is None:
        raise AssertionError(f"conductor not found below deterministic limit {limit}")
    frobenius = conductor - 1
    mask = sum(1 << value for value in range(frobenius + 1) if present[value])
    return mask, frobenius


def analyze_shift(shift: int) -> dict[str, object]:
    generators = template_generators(shift)
    mask, frobenius = generated_mask(generators)
    expected_frobenius = 13 * shift - 1
    failures: list[str] = []
    if frobenius != expected_frobenius:
        failures.append(f"F={frobenius}, expected {expected_frobenius}")
    if frobenius % 2 == 0:
        semantic_failures = ("F is even, hence cannot be symmetric",)
    else:
        semantic_failures = validate_symmetric_mask(mask, frobenius)
    failures.extend(semantic_failures)
    actual_minimal = minimal_generators(mask, frobenius) if frobenius % 2 else ()
    if actual_minimal != generators:
        failures.append("displayed template is not the exact minimal generating set")
    if mask & (1 << shift):
        failures.append("selected shift belongs to the semigroup")
        rigidity: dict[str, object] | None = None
    elif semantic_failures:
        rigidity = None
    else:
        rigidity = analyze_rigidity(mask, frobenius, shift)
        if not rigidity["rigid"]:
            failures.append(
                f"not rigid; first missing D={rigidity['first_missing_D']}"
            )
    bitstring = format(mask, f"0{frobenius + 1}b")[::-1]
    return {
        "shift": shift,
        "generators": generators,
        "frobenius": frobenius,
        "expected_frobenius": expected_frobenius,
        "membership_sha256": hashlib.sha256(bitstring.encode("ascii")).hexdigest(),
        "minimal_generators": actual_minimal,
        "semantic_failures": semantic_failures,
        "rigidity": rigidity,
        "accepted": not failures,
        "first_failure": None if not failures else failures[0],
        "all_failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-shift", type=int, default=14)
    parser.add_argument("--max-shift", type=int, default=100)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    args = parser.parse_args()
    if (
        args.min_shift < 14
        or args.min_shift % 2
        or args.max_shift < args.min_shift
        or args.max_shift % 2
    ):
        raise ValueError("shift range must have even endpoints with 14<=min<=max")
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.artifact_dir / "template-checkpoint.json"
    log_path = args.artifact_dir / "template.log"
    checkpoint: dict[str, object] = {"results": {}}
    if checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    results = checkpoint["results"]

    def log(message: str) -> None:
        line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {message}"
        print(line, flush=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    started = time.perf_counter()
    values = list(range(args.min_shift, args.max_shift + 1, 2))
    for index, shift in enumerate(values, start=1):
        key = str(shift)
        if key in results:
            log(f"resume {index}/{len(values)} s={shift} accepted={results[key]['accepted']}")
            continue
        result = analyze_shift(shift)
        if shift == 14:
            if tuple(result["minimal_generators"]) != SEED_GENERATORS:
                raise AssertionError("P1 seed generator reconstruction failed")
            if not result["accepted"]:
                raise AssertionError(f"P1 seed validation failed: {result['all_failures']}")
        results[key] = result
        atomic_json(checkpoint_path, {"results": results})
        log(
            f"query {index}/{len(values)} s={shift} F={result['frobenius']} "
            f"accepted={result['accepted']} first_failure={result['first_failure']}"
        )

    rows = [
        f"{shift}:{results[str(shift)]['membership_sha256']}:"
        f"{results[str(shift)]['accepted']}:{results[str(shift)]['first_failure']}"
        for shift in values
    ]
    summary = {
        "verdict": "FIXED_TEMPLATE_ASSESSED",
        "min_shift": args.min_shift,
        "max_shift": args.max_shift,
        "accepted_shifts": [shift for shift in values if results[str(shift)]["accepted"]],
        "first_failed_shift": next(
            (shift for shift in values if not results[str(shift)]["accepted"]), None
        ),
        "aggregate_sha256": digest_rows(rows),
        "seconds": time.perf_counter() - started,
        "results": {str(shift): results[str(shift)] for shift in values},
    }
    atomic_json(args.artifact_dir / "template-results.json", summary)
    log(
        f"COMPLETE accepted={summary['accepted_shifts']} "
        f"first_failed={summary['first_failed_shift']} seconds={summary['seconds']:.6f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
