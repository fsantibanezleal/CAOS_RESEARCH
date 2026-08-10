"""EXP-007: proof-carrying projected enumeration at fixed Frobenius number."""

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
    minimal_generators,
    projected_blocking_clause,
    shift_from_model,
    validate_symmetric_mask,
)


CADICAL = "/usr/bin/cadical"
DRAT_TRIM = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim"
DRAT_REPO = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim"


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
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


def toolchain_identity() -> dict[str, str]:
    return {
        "cadical_version": wsl_output(CADICAL, "--version"),
        "cadical_package": wsl_output("dpkg-query", "-W", "cadical"),
        "cadical_sha256": wsl_output("sha256sum", CADICAL).split()[0],
        "drat_trim_commit": wsl_output("git", "-C", DRAT_REPO, "rev-parse", "HEAD"),
        "drat_trim_sha256": wsl_output("sha256sum", DRAT_TRIM).split()[0],
    }


def parse_model(output: str) -> set[int]:
    literals: list[int] = []
    for line in output.splitlines():
        if line.startswith("v "):
            literals.extend(int(value) for value in line[2:].split() if value != "0")
    if not literals:
        raise ValueError("SAT output contains no model")
    return {literal for literal in literals if literal > 0}


def membership(mask: int, frobenius: int) -> str:
    return format(mask, f"0{frobenius + 1}b")[::-1]


def mask_from_membership(value: str, frobenius: int) -> int:
    if len(value) != frobenius + 1 or set(value) - {"0", "1"}:
        raise ValueError("invalid persisted membership vector")
    return int(value[::-1], 2)


def semantic_record(mask: int, frobenius: int, shift: int) -> dict[str, object]:
    failures = validate_symmetric_mask(mask, frobenius)
    rigidity = analyze_rigidity(mask, frobenius, shift)
    if failures or not rigidity["rigid"]:
        raise AssertionError(
            f"SAT model failed exact semantics: failures={failures}, rigidity={rigidity}"
        )
    generators = minimal_generators(mask, frobenius)
    return {
        "shift": shift,
        "membership": membership(mask, frobenius),
        "membership_sha256": hashlib.sha256(
            membership(mask, frobenius).encode("ascii")
        ).hexdigest(),
        "multiplicity": generators[0],
        "embedding_dimension": len(generators),
        "minimal_generators": list(generators),
        "rigidity": rigidity,
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


def check_proof(
    cnf_path: Path,
    proof_path: Path,
    checker_log_path: Path,
    timeout_seconds: int,
) -> dict[str, object]:
    if not proof_path.exists() or proof_path.stat().st_size == 0:
        raise AssertionError("UNSAT result emitted no proof")
    started = time.perf_counter()
    checker = subprocess.run(
        ["wsl.exe", "-e", DRAT_TRIM, wsl_path(cnf_path), wsl_path(proof_path)],
        capture_output=True,
        text=True,
        timeout=timeout_seconds + 30,
        check=False,
    )
    elapsed = time.perf_counter() - started
    output = checker.stdout + checker.stderr
    checker_log_path.write_text(output, encoding="utf-8")
    if checker.returncode != 0 or "s VERIFIED" not in output:
        raise AssertionError(f"DRAT-trim rejected proof with code {checker.returncode}")
    return {
        "proof_bytes": proof_path.stat().st_size,
        "proof_sha256": sha256(proof_path),
        "checker_seconds": elapsed,
        "checker_returncode": checker.returncode,
        "checker_log_sha256": sha256(checker_log_path),
    }


def validate_checkpoint(
    checkpoint: dict[str, object], frobenius: int, tools: dict[str, str]
) -> None:
    if checkpoint.get("frobenius") != frobenius:
        raise AssertionError("checkpoint Frobenius mismatch")
    if checkpoint.get("toolchain") != tools:
        raise AssertionError("toolchain changed since checkpoint")
    seen: set[tuple[int, str]] = set()
    for model in checkpoint.get("models", []):
        shift = int(model["shift"])
        vector = str(model["membership"])
        mask = mask_from_membership(vector, frobenius)
        semantic_record(mask, frobenius, shift)
        key = (shift, vector)
        if key in seen:
            raise AssertionError("checkpoint contains a duplicate projected model")
        seen.add(key)


def checkpoint_solver_seconds(checkpoint: dict[str, object]) -> float:
    seconds = sum(
        float(model["discovery"]["seconds"]) for model in checkpoint.get("models", [])
    )
    for key in ("terminal", "unknown"):
        record = checkpoint.get(key)
        if isinstance(record, dict):
            seconds += float(record.get("seconds", 0.0))
    return seconds


def solve_iteration(
    cnf: object,
    stem: str,
    query_root: Path,
    timeout_seconds: int,
    comments: list[str],
) -> tuple[str, set[int] | None, dict[str, object]]:
    cnf_path = query_root / f"{stem}.cnf"
    proof_path = query_root / f"{stem}.drat"
    solver_log_path = query_root / f"{stem}.cadical.log"
    checker_log_path = query_root / f"{stem}.drat-trim.log"
    cnf.write(cnf_path, comments=comments)
    completed, seconds, output = run_solver(
        cnf_path, proof_path, solver_log_path, timeout_seconds
    )
    record: dict[str, object] = {
        "stem": stem,
        "seconds": seconds,
        "variables": len(cnf.names),
        "clauses": len(cnf.clauses),
        "solver_returncode": completed.returncode,
        "cnf_bytes": cnf_path.stat().st_size,
        "cnf_sha256": sha256(cnf_path),
        "solver_log_sha256": sha256(solver_log_path),
    }
    if completed.returncode == 10 and "s SATISFIABLE" in output:
        proof_path.unlink(missing_ok=True)
        return "SAT", parse_model(output), record
    if completed.returncode == 20 and "s UNSATISFIABLE" in output:
        record.update(check_proof(cnf_path, proof_path, checker_log_path, timeout_seconds))
        return "UNSAT_VERIFIED", None, record
    proof_path.unlink(missing_ok=True)
    return "UNKNOWN", None, record


def run_support(args: argparse.Namespace, tools: dict[str, str]) -> dict[str, object]:
    phase_root = args.proof_root / f"F{args.frobenius:03d}" / "support"
    phase_root.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.artifact_dir / "support-checkpoint.json"
    checkpoint: dict[str, object] = {
        "frobenius": args.frobenius,
        "toolchain": tools,
        "models": [],
        "terminal": None,
    }
    if checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        validate_checkpoint(checkpoint, args.frobenius, tools)
    if checkpoint.get("terminal") is not None:
        return checkpoint

    started = time.perf_counter()
    prior_seconds = checkpoint_solver_seconds(checkpoint)
    while len(checkpoint["models"]) < args.max_models:
        if prior_seconds + time.perf_counter() - started > args.total_seconds:
            checkpoint["stop_reason"] = "TOTAL_TIME_CAP"
            atomic_json(checkpoint_path, checkpoint)
            return checkpoint
        cnf, h, q = build_selector_rigidity_cnf(args.frobenius)
        blocked_shifts = [int(model["shift"]) for model in checkpoint["models"]]
        if len(set(blocked_shifts)) != len(blocked_shifts):
            raise AssertionError("support checkpoint repeats a blocked shift")
        for shift in blocked_shifts:
            cnf.add(-q[shift - 1])
        iteration = len(blocked_shifts)
        stem = f"support-{iteration:03d}"
        status, true_variables, solve = solve_iteration(
            cnf,
            stem,
            phase_root,
            args.timeout_seconds,
            [
                "EXP-007 projected shift-support classification",
                f"F={args.frobenius}",
                "blocked shifts: " + " ".join(map(str, blocked_shifts)),
            ],
        )
        if status == "SAT":
            assert true_variables is not None
            shift = shift_from_model(q, true_variables)
            if shift in blocked_shifts:
                raise AssertionError("solver returned a blocked shift")
            mask = mask_from_model(h, true_variables)
            model = semantic_record(mask, args.frobenius, shift)
            model["discovery"] = solve
            checkpoint["models"].append(model)
            atomic_json(checkpoint_path, checkpoint)
            continue
        if status == "UNSAT_VERIFIED":
            checkpoint["terminal"] = solve
            checkpoint["status"] = "COMPLETE"
            checkpoint["feasible_shifts"] = sorted(blocked_shifts)
            checkpoint["aggregate_sha256"] = digest_rows(
                [f"{model['shift']}:{model['membership_sha256']}" for model in checkpoint["models"]]
                + [f"terminal:{solve['cnf_sha256']}:{solve['proof_sha256']}"]
            )
            atomic_json(checkpoint_path, checkpoint)
            atomic_json(args.artifact_dir / "support-results.json", checkpoint)
            return checkpoint
        checkpoint["stop_reason"] = "SOLVER_UNKNOWN"
        checkpoint["unknown"] = solve
        atomic_json(checkpoint_path, checkpoint)
        return checkpoint
    checkpoint["stop_reason"] = "MODEL_CAP"
    atomic_json(checkpoint_path, checkpoint)
    return checkpoint


def support_result(args: argparse.Namespace) -> dict[str, object]:
    path = args.artifact_dir / "support-results.json"
    if not path.exists():
        raise FileNotFoundError("complete support-results.json is required for classification")
    result = json.loads(path.read_text(encoding="utf-8"))
    if result.get("status") != "COMPLETE" or result.get("terminal") is None:
        raise AssertionError("shift support is not proof-complete")
    return result


def run_fixed_shift(
    args: argparse.Namespace,
    tools: dict[str, str],
    shift: int,
    total_budget_seconds: float,
) -> dict[str, object]:
    phase_root = args.proof_root / f"F{args.frobenius:03d}" / f"s{shift:03d}"
    phase_root.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.artifact_dir / f"s{shift:03d}-checkpoint.json"
    checkpoint: dict[str, object] = {
        "frobenius": args.frobenius,
        "shift": shift,
        "toolchain": tools,
        "models": [],
        "terminal": None,
    }
    if checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        validate_checkpoint(checkpoint, args.frobenius, tools)
        if checkpoint.get("shift") != shift:
            raise AssertionError("fixed-shift checkpoint mismatch")
        if any(int(model["shift"]) != shift for model in checkpoint["models"]):
            raise AssertionError("fixed-shift checkpoint contains another shift")
    if checkpoint.get("terminal") is not None:
        return checkpoint

    started = time.perf_counter()
    prior_seconds = checkpoint_solver_seconds(checkpoint)
    while len(checkpoint["models"]) < args.max_models:
        if prior_seconds + time.perf_counter() - started > total_budget_seconds:
            checkpoint["stop_reason"] = "TOTAL_TIME_CAP"
            atomic_json(checkpoint_path, checkpoint)
            return checkpoint
        cnf, h = build_rigidity_cnf(args.frobenius, shift)
        vectors = [str(model["membership"]) for model in checkpoint["models"]]
        for vector in vectors:
            mask = mask_from_membership(vector, args.frobenius)
            projected_true = {
                variable for value, variable in enumerate(h) if mask & (1 << value)
            }
            cnf.add(*projected_blocking_clause(h, projected_true))
        iteration = len(vectors)
        stem = f"s{shift:03d}-{iteration:05d}"
        status, true_variables, solve = solve_iteration(
            cnf,
            stem,
            phase_root,
            args.timeout_seconds,
            [
                "EXP-007 fixed-shift projected membership classification",
                f"F={args.frobenius} s={shift}",
                f"blocked membership vectors: {len(vectors)}",
            ],
        )
        if status == "SAT":
            assert true_variables is not None
            mask = mask_from_model(h, true_variables)
            model = semantic_record(mask, args.frobenius, shift)
            if model["membership"] in vectors:
                raise AssertionError("solver returned a blocked membership vector")
            model["discovery"] = solve
            checkpoint["models"].append(model)
            atomic_json(checkpoint_path, checkpoint)
            continue
        if status == "UNSAT_VERIFIED":
            checkpoint["terminal"] = solve
            checkpoint["status"] = "COMPLETE"
            checkpoint["model_count"] = len(checkpoint["models"])
            checkpoint["aggregate_sha256"] = digest_rows(
                [str(model["membership_sha256"]) for model in checkpoint["models"]]
                + [f"terminal:{solve['cnf_sha256']}:{solve['proof_sha256']}"]
            )
            atomic_json(checkpoint_path, checkpoint)
            atomic_json(args.artifact_dir / f"s{shift:03d}-results.json", checkpoint)
            return checkpoint
        checkpoint["stop_reason"] = "SOLVER_UNKNOWN"
        checkpoint["unknown"] = solve
        atomic_json(checkpoint_path, checkpoint)
        return checkpoint
    checkpoint["stop_reason"] = "MODEL_CAP"
    atomic_json(checkpoint_path, checkpoint)
    return checkpoint


def run_classification(args: argparse.Namespace, tools: dict[str, str]) -> dict[str, object]:
    support = support_result(args)
    validate_checkpoint(support, args.frobenius, tools)
    shifts = [int(value) for value in support["feasible_shifts"]]
    classes: dict[str, object] = {}
    for shift in shifts:
        previous_seconds = sum(
            checkpoint_solver_seconds(result) for result in classes.values()
        )
        remaining_seconds = args.total_seconds - previous_seconds
        if remaining_seconds <= 0:
            break
        result = run_fixed_shift(args, tools, shift, remaining_seconds)
        classes[str(shift)] = result
        if result.get("status") != "COMPLETE":
            break
    complete = len(classes) == len(shifts) and all(
        result.get("status") == "COMPLETE" for result in classes.values()
    )
    summary: dict[str, object] = {
        "frobenius": args.frobenius,
        "status": "COMPLETE" if complete else "INCONCLUSIVE",
        "toolchain": tools,
        "support_aggregate_sha256": support["aggregate_sha256"],
        "feasible_shifts": shifts,
        "classes": classes,
    }
    if complete:
        union_shifts = sorted(
            int(shift) for shift, result in classes.items() if result["model_count"] > 0
        )
        if union_shifts != shifts:
            raise AssertionError("support and fixed-shift nonempty classes disagree")
        all_models = [
            model
            for result in classes.values()
            for model in result["models"]
        ]
        summary["normalized_pair_count"] = len(all_models)
        summary["distinct_semigroup_count"] = len(
            {str(model["membership"]) for model in all_models}
        )
        summary["unique_public_pair_prediction"] = len(all_models) == 1 and shifts == [14]
        summary["aggregate_sha256"] = digest_rows(
            [str(support["aggregate_sha256"])]
            + [f"{shift}:{classes[str(shift)]['aggregate_sha256']}" for shift in shifts]
        )
    atomic_json(args.artifact_dir / "classification-results.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("support", "classify"), required=True)
    parser.add_argument("--frobenius", type=int, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--proof-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--total-seconds", type=int, default=14400)
    parser.add_argument("--max-models", type=int, default=10000)
    args = parser.parse_args()
    if args.frobenius <= 0 or args.frobenius % 2 == 0:
        raise ValueError("F must be positive and odd")
    if min(args.timeout_seconds, args.total_seconds, args.max_models) <= 0:
        raise ValueError("all budgets must be positive")
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    args.proof_root.mkdir(parents=True, exist_ok=True)
    tools = toolchain_identity()
    if args.phase == "support":
        result = run_support(args, tools)
    else:
        result = run_classification(args, tools)
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") == "COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
