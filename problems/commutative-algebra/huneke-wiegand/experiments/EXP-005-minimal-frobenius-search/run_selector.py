"""EXP-005: proof-carrying one-selector-CNF minimal Frobenius search."""

from __future__ import annotations

import argparse
import hashlib
import json
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
    build_selector_rigidity_cnf,
    mask_from_model,
    shift_from_model,
    validate_symmetric_mask,
)


CADICAL = "/usr/bin/cadical"
DRAT_TRIM = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim"
DRAT_REPO = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim"


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


def run_solver(
    cnf_path: Path,
    proof_path: Path,
    log_path: Path,
    timeout_seconds: int,
) -> tuple[subprocess.CompletedProcess[str], float, str]:
    proof_path.unlink(missing_ok=True)
    started = time.perf_counter()
    completed = subprocess.run(
        [
            "wsl.exe",
            "-e",
            CADICAL,
            "-t",
            str(timeout_seconds),
            wsl_path(cnf_path),
            wsl_path(proof_path),
        ],
        capture_output=True,
        text=True,
        timeout=timeout_seconds + 30,
        check=False,
    )
    elapsed = time.perf_counter() - started
    output = completed.stdout + completed.stderr
    log_path.write_text(output, encoding="utf-8")
    return completed, elapsed, output


def fixed_pair_adversary(
    frobenius: int,
    shift: int,
    query_root: Path,
    timeout_seconds: int,
) -> dict[str, object]:
    cnf, h = build_rigidity_cnf(frobenius, shift)
    cnf_path = query_root / f"F{frobenius:03d}-s{shift:03d}-fixed.cnf"
    proof_path = query_root / f"F{frobenius:03d}-s{shift:03d}-fixed.drat"
    log_path = query_root / f"F{frobenius:03d}-s{shift:03d}-fixed.cadical.log"
    cnf.write(cnf_path, comments=["EXP-005 fixed-pair adversarial cross-check"])
    completed, elapsed, output = run_solver(
        cnf_path, proof_path, log_path, timeout_seconds
    )
    if completed.returncode != 10 or "s SATISFIABLE" not in output:
        raise AssertionError(
            f"fixed-pair adversary expected SAT, code={completed.returncode}"
        )
    true_variables = parse_model(output)
    mask = mask_from_model(h, true_variables)
    failures = validate_symmetric_mask(mask, frobenius)
    rigidity = analyze_rigidity(mask, frobenius, shift)
    if failures or not rigidity["rigid"]:
        raise AssertionError("fixed-pair SAT model failed independent semantics")
    proof_path.unlink(missing_ok=True)
    return {
        "status": "SAT_VALIDATED",
        "seconds": elapsed,
        "variables": len(cnf.names),
        "clauses": len(cnf.clauses),
        "cnf_bytes": cnf_path.stat().st_size,
        "cnf_sha256": sha256(cnf_path),
        "solver_log_sha256": sha256(log_path),
        "membership": format(mask, f"0{frobenius + 1}b")[::-1],
        "rigidity": rigidity,
    }


def run_frobenius(
    frobenius: int,
    query_root: Path,
    timeout_seconds: int,
) -> dict[str, object]:
    query_root.mkdir(parents=True, exist_ok=True)
    stem = f"F{frobenius:03d}-selector"
    cnf_path = query_root / f"{stem}.cnf"
    proof_path = query_root / f"{stem}.drat"
    solver_log_path = query_root / f"{stem}.cadical.log"
    checker_log_path = query_root / f"{stem}.drat-trim.log"
    cnf, h, q = build_selector_rigidity_cnf(frobenius)
    cnf.write(
        cnf_path,
        comments=[
            "EXP-005 one-hot shift selector rigidity formula",
            f"F={frobenius}",
            "h variables: "
            + " ".join(f"{value}:{variable}" for value, variable in enumerate(h)),
            "q variables: "
            + " ".join(
                f"{shift}:{variable}" for shift, variable in enumerate(q, start=1)
            ),
        ],
    )
    completed, elapsed, solver_output = run_solver(
        cnf_path, proof_path, solver_log_path, timeout_seconds
    )
    result: dict[str, object] = {
        "frobenius": frobenius,
        "seconds": elapsed,
        "variables": len(cnf.names),
        "clauses": len(cnf.clauses),
        "solver_returncode": completed.returncode,
        "cnf_bytes": cnf_path.stat().st_size,
        "cnf_sha256": sha256(cnf_path),
        "solver_log_sha256": sha256(solver_log_path),
    }
    if completed.returncode == 10 and "s SATISFIABLE" in solver_output:
        true_variables = parse_model(solver_output)
        shift = shift_from_model(q, true_variables)
        mask = mask_from_model(h, true_variables)
        failures = validate_symmetric_mask(mask, frobenius)
        rigidity = analyze_rigidity(mask, frobenius, shift)
        if failures or not rigidity["rigid"]:
            raise AssertionError("selector SAT model failed independent semantics")
        result.update(
            {
                "status": "SAT_VALIDATED",
                "shift": shift,
                "membership": format(mask, f"0{frobenius + 1}b")[::-1],
                "semantic_failures": failures,
                "rigidity": rigidity,
                "fixed_pair_adversary": fixed_pair_adversary(
                    frobenius, shift, query_root, timeout_seconds
                ),
            }
        )
        proof_path.unlink(missing_ok=True)
        return result
    if completed.returncode != 20 or "s UNSATISFIABLE" not in solver_output:
        result["status"] = "UNKNOWN"
        return result
    if not proof_path.exists() or proof_path.stat().st_size == 0:
        raise AssertionError("UNSAT query emitted no proof")
    checker = subprocess.run(
        ["wsl.exe", "-e", DRAT_TRIM, wsl_path(cnf_path), wsl_path(proof_path)],
        capture_output=True,
        text=True,
        timeout=timeout_seconds + 30,
        check=False,
    )
    checker_output = checker.stdout + checker.stderr
    checker_log_path.write_text(checker_output, encoding="utf-8")
    if checker.returncode != 0 or "s VERIFIED" not in checker_output:
        raise AssertionError(f"DRAT-trim rejected proof with code {checker.returncode}")
    result.update(
        {
            "status": "UNSAT_VERIFIED",
            "proof_bytes": proof_path.stat().st_size,
            "proof_sha256": sha256(proof_path),
            "checker_returncode": checker.returncode,
            "checker_log_sha256": sha256(checker_log_path),
        }
    )
    return result


def validate_resume_entry(entry: dict[str, object], query_root: Path) -> None:
    frobenius = int(entry["frobenius"])
    stem = f"F{frobenius:03d}-selector"
    cnf_path = query_root / f"{stem}.cnf"
    if not cnf_path.exists() or sha256(cnf_path) != entry["cnf_sha256"]:
        raise AssertionError(f"resume CNF hash mismatch for F={frobenius}")
    if entry["status"] == "UNSAT_VERIFIED":
        proof_path = query_root / f"{stem}.drat"
        if not proof_path.exists() or sha256(proof_path) != entry["proof_sha256"]:
            raise AssertionError(f"resume proof hash mismatch for F={frobenius}")


def requested_values(args: argparse.Namespace) -> list[int]:
    if args.mode == "calibrate":
        if args.frobenius is None or args.frobenius <= 0 or args.frobenius % 2 == 0:
            raise ValueError("calibrate mode requires positive odd --frobenius")
        return [args.frobenius]
    if (
        args.min_f is None
        or args.max_f is None
        or args.min_f <= 0
        or args.min_f % 2 == 0
        or args.max_f < args.min_f
        or args.max_f % 2 == 0
    ):
        raise ValueError("regression/search require positive odd --min-f and --max-f")
    return list(range(args.min_f, args.max_f + 1, 2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("regression", "calibrate", "search"), required=True)
    parser.add_argument("--frobenius", type=int)
    parser.add_argument("--min-f", type=int)
    parser.add_argument("--max-f", type=int)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--proof-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    args = parser.parse_args()
    values = requested_values(args)
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    args.proof_root.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.artifact_dir / "selector-checkpoint.json"
    log_path = args.artifact_dir / "selector.log"
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
    first_sat: dict[str, object] | None = None
    for index, frobenius in enumerate(values, start=1):
        key = str(frobenius)
        query_root = args.proof_root / f"F{frobenius:03d}"
        if key in queries:
            validate_resume_entry(queries[key], query_root)
            result = queries[key]
            log(f"resume {index}/{len(values)} F={frobenius} {result['status']}")
        else:
            result = run_frobenius(frobenius, query_root, args.timeout_seconds)
            queries[key] = result
            atomic_json(checkpoint_path, {"toolchain": toolchain, "queries": queries})
            log(
                f"query {index}/{len(values)} F={frobenius} status={result['status']} "
                f"seconds={result['seconds']:.6f}"
            )
        if result["status"] == "UNKNOWN":
            raise AssertionError(f"unknown result blocks frontier at F={frobenius}")
        if args.mode == "regression" and result["status"] != "UNSAT_VERIFIED":
            raise AssertionError(f"regression expected UNSAT at F={frobenius}")
        if args.mode == "calibrate" and result["status"] != "SAT_VALIDATED":
            raise AssertionError(f"calibration expected SAT at F={frobenius}")
        if result["status"] == "SAT_VALIDATED":
            first_sat = result
            if args.mode == "search":
                break

    completed_values = [value for value in values if str(value) in queries]
    rows = [
        f"{value}:{queries[str(value)]['status']}:{queries[str(value)]['cnf_sha256']}:"
        f"{queries[str(value)].get('proof_sha256', '-')}"
        for value in completed_values
    ]
    summary = {
        "mode": args.mode,
        "requested_min_f": min(values),
        "requested_max_f": max(values),
        "completed_values": completed_values,
        "first_sat_frobenius": None if first_sat is None else first_sat["frobenius"],
        "first_sat_shift": None if first_sat is None else first_sat["shift"],
        "aggregate_sha256": digest_rows(rows),
        "seconds": time.perf_counter() - started,
        "toolchain": toolchain,
        "queries": {str(value): queries[str(value)] for value in completed_values},
    }
    atomic_json(args.artifact_dir / "selector-results.json", summary)
    log(
        f"COMPLETE mode={args.mode} completed={len(completed_values)} "
        f"first_sat={summary['first_sat_frobenius']} seconds={summary['seconds']:.6f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
