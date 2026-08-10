"""EXP-006 Route K: proof-carrying constrained block-family search.

CPU only.  CaDiCaL produces SAT models or DRAT proofs under WSL; DRAT-trim
independently checks every UNSAT result.  SAT models are rechecked by the
standard-library exact semigroup implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT.parents[1] / "code"
sys.path.insert(0, str(CODE_ROOT))

from hwcert import (  # noqa: E402
    analyze_rigidity,
    build_rigidity_cnf,
    mask_from_model,
    minimal_generators,
    validate_symmetric_mask,
)


CADICAL = "/usr/bin/cadical"
DRAT_TRIM = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim"
DRAT_REPO = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim"
SEED_GENERATORS = (
    56, 57, 58, 63, 64, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
    82, 83, 87, 89, 90, 93, 95, 96, 97,
)


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def digest_rows(rows: list[str]) -> str:
    return hashlib.sha256("\n".join(rows).encode("ascii")).hexdigest()


def wsl_path(path: Path) -> str:
    completed = subprocess.run(
        ["wsl.exe", "-e", "wslpath", "-a", str(path.resolve())],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    return completed.stdout.strip()


def wsl_output(*command: str, timeout: int = 30) -> str:
    completed = subprocess.run(
        ["wsl.exe", "-e", *command],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return completed.stdout.strip()


def parse_model(output: str) -> set[int]:
    literals: list[int] = []
    for line in output.splitlines():
        if line.startswith("v "):
            literals.extend(int(value) for value in line[2:].split() if value != "0")
    if not literals:
        raise ValueError("SAT output contains no model")
    return {literal for literal in literals if literal > 0}


def toolchain_identity() -> dict[str, str]:
    return {
        "cadical_version": wsl_output(CADICAL, "--version"),
        "cadical_package": wsl_output("dpkg-query", "-W", "cadical"),
        "cadical_sha256": wsl_output("sha256sum", CADICAL).split()[0],
        "drat_trim_commit": wsl_output("git", "-C", DRAT_REPO, "rev-parse", "HEAD"),
        "drat_trim_sha256": wsl_output("sha256sum", DRAT_TRIM).split()[0],
    }


def build_route_k_cnf(shift: int):
    """Return the broad Route K formula and membership projection."""
    if shift < 2 or shift % 2:
        raise ValueError("Route K requires an even shift")
    frobenius = 13 * shift - 1
    cnf, membership = build_rigidity_cnf(frobenius, shift)
    for value in range(1, 4 * shift):
        cnf.add(-membership[value])
    cnf.add(membership[4 * shift])
    for value in range(5 * shift, 6 * shift):
        cnf.add(membership[value])
    return cnf, membership


def generated_mask(generators: tuple[int, ...], frobenius: int) -> int:
    present = bytearray(frobenius + 1)
    present[0] = 1
    for value in range(1, frobenius + 1):
        present[value] = any(
            value >= generator and present[value - generator] for generator in generators
        )
    return sum(1 << value for value, flag in enumerate(present) if flag)


def generalized_arithmetic_presentation(
    mask: int, frobenius: int
) -> dict[str, int] | None:
    """Find an exact generalized-arithmetic presentation, if one exists."""
    generators = minimal_generators(mask, frobenius)
    if not generators:
        return None
    a = generators[0]
    other = generators[1:]
    if not other:
        return {"a": a, "h": 1, "d": 1, "k": 0}
    maximum = max(other)
    for h in range(1, maximum // a + 1):
        base = a * h
        for d in range(1, maximum - base + 1):
            if math.gcd(a, d) != 1:
                continue
            offsets = [value - base for value in other]
            if any(offset <= 0 or offset % d for offset in offsets):
                continue
            k = max(offset // d for offset in offsets)
            displayed = (a,) + tuple(base + index * d for index in range(1, k + 1))
            if generated_mask(displayed, frobenius) == mask:
                return {"a": a, "h": h, "d": d, "k": k}
    return None


def validate_route_k_mask(mask: int, shift: int) -> dict[str, object]:
    frobenius = 13 * shift - 1
    failures = list(validate_symmetric_mask(mask, frobenius))

    def present(value: int) -> bool:
        return bool(mask & (1 << value))

    actual_multiplicity = next(
        (value for value in range(1, frobenius + 1) if present(value)),
        frobenius + 1,
    )
    if actual_multiplicity != 4 * shift:
        failures.append(
            f"multiplicity is {actual_multiplicity}, expected {4 * shift}"
        )
    missing_level5 = [value for value in range(5 * shift, 6 * shift) if not present(value)]
    if missing_level5:
        failures.append(f"level-5 block misses {missing_level5[0]}")
    if present(shift):
        failures.append("selected shift is not a gap")

    set_a = tuple(residue for residue in range(shift) if present(4 * shift + residue))
    set_b = tuple(residue for residue in range(shift) if present(6 * shift + residue))
    reflected_b_failures = tuple(
        residue
        for residue in range(shift)
        if (residue in set_b) == (shift - 1 - residue in set_b)
    )
    if reflected_b_failures:
        failures.append(f"level-6 reflection fails at {reflected_b_failures[0]}")
    if len(set_b) != shift // 2:
        failures.append(f"level-6 size is {len(set_b)}, expected {shift // 2}")
    overlap = tuple(sorted(set(set_a).intersection(set_b)))
    if overlap:
        failures.append(f"level-4/6 overlap begins at residue {overlap[0]}")

    forced_high_failure = next(
        (value for value in range(9 * shift, 13 * shift - 1) if not present(value)),
        None,
    )
    if forced_high_failure is not None:
        failures.append(f"forced high member absent at {forced_high_failure}")
    if present(9 * shift - 1):
        failures.append("forced gap 9s-1 is present")
    forced_level7_failure = next(
        (value for value in range(7 * shift, 8 * shift) if present(value)),
        None,
    )
    if forced_level7_failure is not None:
        failures.append(f"forced level-7 gap present at {forced_level7_failure}")

    rigidity = None
    if not present(shift):
        rigidity = analyze_rigidity(mask, frobenius, shift)
        if not rigidity["rigid"]:
            failures.append(f"rigidity fails at D={rigidity['first_missing_D']}")

    generators = minimal_generators(mask, frobenius) if not failures else ()
    presentation = (
        generalized_arithmetic_presentation(mask, frobenius) if not failures else None
    )
    return {
        "accepted": not failures,
        "failures": tuple(failures),
        "multiplicity": actual_multiplicity,
        "level4_residues": set_a,
        "level4_count": len(set_a),
        "level6_residues": set_b,
        "level6_count": len(set_b),
        "level4_level6_overlap": overlap,
        "rigidity": rigidity,
        "minimal_generators": generators,
        "generalized_arithmetic_presentation": presentation,
    }


def run_solver(
    cnf_path: Path, proof_path: Path, log_path: Path, timeout_seconds: int
) -> tuple[subprocess.CompletedProcess[str], float, str]:
    proof_path.unlink(missing_ok=True)
    started = time.perf_counter()
    completed = subprocess.run(
        [
            "wsl.exe", "-e", CADICAL, "-t", str(timeout_seconds),
            wsl_path(cnf_path), wsl_path(proof_path),
        ],
        capture_output=True,
        text=True,
        timeout=timeout_seconds + 30,
        check=False,
    )
    seconds = time.perf_counter() - started
    output = completed.stdout + completed.stderr
    log_path.write_text(output, encoding="utf-8")
    return completed, seconds, output


def check_proof(
    cnf_path: Path, proof_path: Path, log_path: Path, timeout_seconds: int
) -> dict[str, object]:
    if not proof_path.exists() or proof_path.stat().st_size == 0:
        raise AssertionError("UNSAT result emitted no proof")
    completed = subprocess.run(
        ["wsl.exe", "-e", DRAT_TRIM, wsl_path(cnf_path), wsl_path(proof_path)],
        capture_output=True,
        text=True,
        timeout=timeout_seconds + 30,
        check=False,
    )
    output = completed.stdout + completed.stderr
    log_path.write_text(output, encoding="utf-8")
    if completed.returncode != 0 or "s VERIFIED" not in output:
        raise AssertionError(f"DRAT-trim rejected proof with code {completed.returncode}")
    return {
        "proof_bytes": proof_path.stat().st_size,
        "proof_sha256": sha256(proof_path),
        "checker_returncode": completed.returncode,
        "checker_log_sha256": sha256(log_path),
    }


def run_shift(shift: int, query_root: Path, timeout_seconds: int) -> dict[str, object]:
    query_root.mkdir(parents=True, exist_ok=True)
    frobenius = 13 * shift - 1
    stem = f"s{shift:03d}-F{frobenius:03d}-route-k"
    cnf_path = query_root / f"{stem}.cnf"
    proof_path = query_root / f"{stem}.drat"
    solver_log_path = query_root / f"{stem}.cadical.log"
    checker_log_path = query_root / f"{stem}.drat-trim.log"
    cnf, membership = build_route_k_cnf(shift)
    cnf.write(
        cnf_path,
        comments=[
            "EXP-006 Route K broad block-family formula",
            f"s={shift} F={frobenius} m={4 * shift}",
            f"full level-5 block={5 * shift}..{6 * shift - 1}",
        ],
    )
    completed, seconds, output = run_solver(
        cnf_path, proof_path, solver_log_path, timeout_seconds
    )
    result: dict[str, object] = {
        "shift": shift,
        "frobenius": frobenius,
        "seconds": seconds,
        "variables": len(cnf.names),
        "clauses": len(cnf.clauses),
        "solver_returncode": completed.returncode,
        "cnf_bytes": cnf_path.stat().st_size,
        "cnf_sha256": sha256(cnf_path),
        "solver_log_sha256": sha256(solver_log_path),
    }
    if completed.returncode == 10 and "s SATISFIABLE" in output:
        true_variables = parse_model(output)
        mask = mask_from_model(membership, true_variables)
        validation = validate_route_k_mask(mask, shift)
        if not validation["accepted"]:
            raise AssertionError(f"SAT model failed exact checks: {validation['failures']}")
        corrupted = mask & ~(1 << (5 * shift))
        corruption = validate_route_k_mask(corrupted, shift)
        if corruption["accepted"] or not any(
            "level-5 block misses" in item for item in corruption["failures"]
        ):
            raise AssertionError("forced-block corruption was not rejected")
        result.update(
            {
                "status": "SAT_VALIDATED",
                "membership": format(mask, f"0{frobenius + 1}b")[::-1],
                "membership_sha256": hashlib.sha256(
                    format(mask, f"0{frobenius + 1}b")[::-1].encode("ascii")
                ).hexdigest(),
                "validation": validation,
                "corruption_rejected": True,
                "corruption_first_failure": corruption["failures"][0],
            }
        )
        proof_path.unlink(missing_ok=True)
        return result
    if completed.returncode == 20 and "s UNSATISFIABLE" in output:
        result["status"] = "UNSAT_VERIFIED"
        result.update(check_proof(cnf_path, proof_path, checker_log_path, timeout_seconds))
        return result
    proof_path.unlink(missing_ok=True)
    result["status"] = "UNKNOWN"
    return result


def validate_resume_entry(entry: dict[str, object], query_root: Path) -> None:
    shift = int(entry["shift"])
    frobenius = 13 * shift - 1
    stem = f"s{shift:03d}-F{frobenius:03d}-route-k"
    cnf_path = query_root / f"{stem}.cnf"
    if not cnf_path.exists() or sha256(cnf_path) != entry["cnf_sha256"]:
        raise AssertionError(f"resume CNF hash mismatch for s={shift}")
    if entry["status"] == "UNSAT_VERIFIED":
        proof_path = query_root / f"{stem}.drat"
        if not proof_path.exists() or sha256(proof_path) != entry["proof_sha256"]:
            raise AssertionError(f"resume proof hash mismatch for s={shift}")
    if entry["status"] == "SAT_VALIDATED":
        mask = int(str(entry["membership"])[::-1], 2)
        if not validate_route_k_mask(mask, shift)["accepted"]:
            raise AssertionError(f"resume model failed exact validation for s={shift}")


def requested_shifts(args: argparse.Namespace) -> list[int]:
    if args.mode == "calibrate":
        return [14]
    if (
        args.min_shift is None or args.max_shift is None
        or args.min_shift < 16 or args.min_shift % 2
        or args.max_shift < args.min_shift or args.max_shift % 2
    ):
        raise ValueError("search requires even 16<=--min-shift<=--max-shift")
    return list(range(args.min_shift, args.max_shift + 1, 2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("calibrate", "search"), required=True)
    parser.add_argument("--min-shift", type=int)
    parser.add_argument("--max-shift", type=int)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--proof-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    args = parser.parse_args()
    shifts = requested_shifts(args)
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    args.proof_root.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.artifact_dir / "route-k-checkpoint.json"
    results_path = args.artifact_dir / "route-k-results.json"
    log_path = args.artifact_dir / "route-k.log"
    toolchain = toolchain_identity()
    checkpoint: dict[str, object] = {"toolchain": toolchain, "queries": {}}
    if checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        if checkpoint["toolchain"] != toolchain:
            raise AssertionError("toolchain changed since checkpoint")
    queries = checkpoint["queries"]

    def log(message: str) -> None:
        line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {message}"
        print(line, flush=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    started = time.perf_counter()
    for index, shift in enumerate(shifts, start=1):
        key = str(shift)
        query_root = args.proof_root / f"s{shift:03d}"
        if key in queries:
            validate_resume_entry(queries[key], query_root)
            result = queries[key]
            log(f"resume {index}/{len(shifts)} s={shift} {result['status']}")
        else:
            log(f"start {index}/{len(shifts)} s={shift} F={13 * shift - 1}")
            result = run_shift(shift, query_root, args.timeout_seconds)
            queries[key] = result
            atomic_json(checkpoint_path, {"toolchain": toolchain, "queries": queries})
            log(
                f"query {index}/{len(shifts)} s={shift} status={result['status']} "
                f"seconds={result['seconds']:.6f}"
            )
        if result["status"] == "UNKNOWN":
            break
        if args.mode == "calibrate":
            if result["status"] != "SAT_VALIDATED":
                raise AssertionError("s=14 calibration expected SAT")
            if tuple(result["validation"]["minimal_generators"]) != SEED_GENERATORS:
                raise AssertionError("s=14 calibration did not recover the public seed")

    completed = [shift for shift in shifts if str(shift) in queries]
    rows = [
        f"{shift}:{queries[str(shift)]['status']}:{queries[str(shift)]['cnf_sha256']}:"
        f"{queries[str(shift)].get('proof_sha256', queries[str(shift)].get('membership_sha256', '-'))}"
        for shift in completed
    ]
    summary = {
        "mode": args.mode,
        "requested_shifts": shifts,
        "completed_shifts": completed,
        "sat_shifts": [shift for shift in completed if queries[str(shift)]["status"] == "SAT_VALIDATED"],
        "unsat_shifts": [shift for shift in completed if queries[str(shift)]["status"] == "UNSAT_VERIFIED"],
        "unknown_shifts": [shift for shift in completed if queries[str(shift)]["status"] == "UNKNOWN"],
        "aggregate_sha256": digest_rows(rows),
        "seconds": time.perf_counter() - started,
        "toolchain": toolchain,
        "queries": {str(shift): queries[str(shift)] for shift in completed},
    }
    atomic_json(results_path, summary)
    log(
        f"COMPLETE mode={args.mode} completed={len(completed)} "
        f"sat={summary['sat_shifts']} unknown={summary['unknown_shifts']} "
        f"seconds={summary['seconds']:.6f}"
    )
    return 0 if not summary["unknown_shifts"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
