"""EXP-004 Route B: DIMACS, CaDiCaL DRAT proofs, and DRAT-trim checks."""

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
    mask_from_model,
    validate_symmetric_mask,
)


CADICAL = "/usr/bin/cadical"
DRAT_TRIM = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim"


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


def run_query(
    frobenius: int,
    shift: int,
    query_root: Path,
    timeout_seconds: int,
) -> dict[str, object]:
    query_root.mkdir(parents=True, exist_ok=True)
    stem = f"F{frobenius:03d}-s{shift:03d}"
    cnf_path = query_root / f"{stem}.cnf"
    proof_path = query_root / f"{stem}.drat"
    solver_log_path = query_root / f"{stem}.cadical.log"
    checker_log_path = query_root / f"{stem}.drat-trim.log"
    cnf, h_variables = build_rigidity_cnf(frobenius, shift)
    cnf.write(
        cnf_path,
        comments=[
            "EXP-004 fixed Frobenius and shift rigidity formula",
            f"F={frobenius} s={shift}",
            "h variables: " + " ".join(f"{value}:{variable}" for value, variable in enumerate(h_variables)),
        ],
    )
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
    solver_output = completed.stdout + completed.stderr
    solver_log_path.write_text(solver_output, encoding="utf-8")
    result: dict[str, object] = {
        "frobenius": frobenius,
        "shift": shift,
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
        mask = mask_from_model(h_variables, true_variables)
        semantic_failures = validate_symmetric_mask(mask, frobenius)
        rigidity = analyze_rigidity(mask, frobenius, shift)
        result.update(
            {
                "status": "SAT",
                "membership": format(mask, f"0{frobenius + 1}b")[::-1],
                "semantic_failures": semantic_failures,
                "rigidity": rigidity,
            }
        )
        if semantic_failures or not rigidity["rigid"]:
            raise AssertionError("CaDiCaL SAT model failed independent semantics")
        proof_path.unlink(missing_ok=True)
        return result
    if completed.returncode != 20 or "s UNSATISFIABLE" not in solver_output:
        result["status"] = "UNKNOWN"
        return result
    if not proof_path.exists() or proof_path.stat().st_size == 0:
        raise AssertionError("UNSAT query emitted no proof")
    checker = subprocess.run(
        [
            "wsl.exe",
            "-e",
            DRAT_TRIM,
            wsl_path(cnf_path),
            wsl_path(proof_path),
        ],
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
    stem = f"F{entry['frobenius']:03d}-s{entry['shift']:03d}"
    cnf_path = query_root / f"{stem}.cnf"
    if not cnf_path.exists() or sha256(cnf_path) != entry["cnf_sha256"]:
        raise AssertionError(f"resume CNF hash mismatch for {stem}")
    if entry["status"] == "UNSAT_VERIFIED":
        proof_path = query_root / f"{stem}.drat"
        if not proof_path.exists() or sha256(proof_path) != entry["proof_sha256"]:
            raise AssertionError(f"resume proof hash mismatch for {stem}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("frontier", "candidate"), required=True)
    parser.add_argument("--max-f", type=int)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--proof-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    args.proof_root.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.artifact_dir / "route-b-checkpoint.json"
    log_path = args.artifact_dir / "route-b.log"

    toolchain = {
        "cadical_version": wsl_output(CADICAL, "--version"),
        "cadical_package": wsl_output("dpkg-query", "-W", "cadical"),
        "cadical_sha256": wsl_output("sha256sum", CADICAL).split()[0],
        "drat_trim_commit": wsl_output(
            "git",
            "-C",
            "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim",
            "rev-parse",
            "HEAD",
        ),
        "drat_trim_sha256": wsl_output("sha256sum", DRAT_TRIM).split()[0],
    }
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

    if args.mode == "candidate":
        pairs = [(181, 14)]
    else:
        if args.max_f is None or args.max_f <= 0 or args.max_f % 2 == 0:
            raise ValueError("frontier mode requires positive odd --max-f")
        pairs = [
            (frobenius, shift)
            for frobenius in range(1, args.max_f + 1, 2)
            for shift in range(1, frobenius + 1)
        ]

    started = time.perf_counter()
    for index, (frobenius, shift) in enumerate(pairs, start=1):
        key = f"{frobenius}:{shift}"
        query_root = args.proof_root / f"F{frobenius:03d}"
        if key in queries:
            validate_resume_entry(queries[key], query_root)
            log(f"resume {index}/{len(pairs)} F={frobenius} s={shift} {queries[key]['status']}")
            continue
        result = run_query(frobenius, shift, query_root, args.timeout_seconds)
        queries[key] = result
        atomic_json(checkpoint_path, {"toolchain": toolchain, "queries": queries})
        log(
            f"query {index}/{len(pairs)} F={frobenius} s={shift} "
            f"status={result['status']} seconds={result['seconds']:.6f}"
        )
        expected = "SAT" if args.mode == "candidate" else "UNSAT_VERIFIED"
        if result["status"] != expected:
            raise AssertionError(f"expected {expected}, got {result['status']} at {key}")

    manifest_rows = [
        f"{key}:{queries[key]['status']}:{queries[key]['cnf_sha256']}:"
        f"{queries[key].get('proof_sha256', '-')}"
        for key in sorted(queries, key=lambda item: tuple(map(int, item.split(":"))))
        if tuple(map(int, key.split(":"))) in pairs
    ]
    summary = {
        "verdict": "CALIBRATED" if args.mode == "candidate" else "NO_COUNTEREXAMPLE",
        "mode": args.mode,
        "max_f": args.max_f,
        "query_count": len(pairs),
        "status_counts": {
            status: sum(queries[f"{f}:{s}"]["status"] == status for f, s in pairs)
            for status in ("SAT", "UNSAT_VERIFIED", "UNKNOWN")
        },
        "aggregate_sha256": hashlib.sha256("\n".join(manifest_rows).encode("ascii")).hexdigest(),
        "seconds": time.perf_counter() - started,
        "toolchain": toolchain,
        "queries": {f"{f}:{s}": queries[f"{f}:{s}"] for f, s in pairs},
    }
    atomic_json(args.artifact_dir / "route-b-results.json", summary)
    log(
        f"COMPLETE mode={args.mode} queries={len(pairs)} "
        f"seconds={summary['seconds']:.6f} aggregate={summary['aggregate_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
