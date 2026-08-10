"""EXP-006 Route K: proof-carrying constrained block search."""

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
    add_exact_cardinality,
    analyze_rigidity,
    build_rigidity_cnf,
    mask_from_model,
    minimal_generators,
    validate_symmetric_mask,
)
from hwcert.semigroup import member, multiplicity  # noqa: E402


CADICAL = "/usr/bin/cadical"
DRAT_TRIM = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim"
DRAT_REPO = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim"
PUBLIC_MEMBERSHIP_SHA256 = "8bf4cd6f17f12068a5755533a6852f2c36fbe9cb704c17a778a94789745fd80b"


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


def membership_vector(mask: int, frobenius: int) -> str:
    return format(mask, f"0{frobenius + 1}b")[::-1]


def build_route_k_cnf(shift: int, level4_count: int | None = None):
    if shift < 14 or shift % 2:
        raise ValueError("Route K requires even s>=14")
    frobenius = 13 * shift - 1
    cnf, h = build_rigidity_cnf(frobenius, shift)
    for value in range(1, 4 * shift):
        cnf.add(-h[value])
    cnf.add(h[4 * shift])
    for value in range(5 * shift, 6 * shift):
        cnf.add(h[value])
    if level4_count is not None:
        add_exact_cardinality(
            cnf,
            tuple(h[4 * shift : 5 * shift]),
            level4_count,
            f"route-k:s{shift}:level4",
        )
    return cnf, h


def generated_mask(generators: tuple[int, ...], frobenius: int) -> int:
    present = bytearray(frobenius + 1)
    present[0] = 1
    for value in range(1, frobenius + 1):
        present[value] = any(
            value >= generator and present[value - generator]
            for generator in generators
        )
    return sum(1 << value for value, flag in enumerate(present) if flag)


def generalized_arithmetic_presentation(
    mask: int, frobenius: int, generators: tuple[int, ...]
) -> dict[str, int] | None:
    """Find an exact generalized-arithmetic presentation, if one exists."""
    a = generators[0]
    other = generators[1:]
    if not other:
        return {"a": a, "h": 1, "d": 1, "k": 0}
    maximum = max(other)
    for h in range(1, maximum // a + 1):
        base = a * h
        for step in range(1, maximum - base + 1):
            if math.gcd(a, step) != 1:
                continue
            offsets = [value - base for value in other]
            if any(offset <= 0 or offset % step for offset in offsets):
                continue
            k = max(offset // step for offset in offsets)
            displayed = (a,) + tuple(
                base + index * step for index in range(1, k + 1)
            )
            if generated_mask(displayed, frobenius) == mask:
                return {"a": a, "h": h, "d": step, "k": k}
    return None


def route_k_failures(mask: int, shift: int) -> tuple[str, ...]:
    frobenius = 13 * shift - 1
    failures = list(validate_symmetric_mask(mask, frobenius))
    actual_multiplicity = multiplicity(mask, frobenius)
    if actual_multiplicity != 4 * shift:
        failures.append(f"multiplicity is {actual_multiplicity}, expected {4 * shift}")
    missing_middle = next(
        (value for value in range(5 * shift, 6 * shift) if not member(mask, frobenius, value)),
        None,
    )
    if missing_middle is not None:
        failures.append(f"full level-5 block fails at {missing_middle}")
    if member(mask, frobenius, shift):
        failures.append("selected shift is a member")
    return tuple(failures)


def semantic_record(mask: int, shift: int) -> dict[str, object]:
    frobenius = 13 * shift - 1
    failures = route_k_failures(mask, shift)
    rigidity = analyze_rigidity(mask, frobenius, shift)
    if failures or not rigidity["rigid"]:
        raise AssertionError(f"SAT model failed exact semantics: failures={failures}, rigidity={rigidity}")
    generators = minimal_generators(mask, frobenius)
    level4 = [value - 4 * shift for value in range(4 * shift, 5 * shift) if member(mask, frobenius, value)]
    level6 = [value - 6 * shift for value in range(6 * shift, 7 * shift) if member(mask, frobenius, value)]
    if len(level6) != shift // 2:
        raise AssertionError("symmetry-forced level-6 cardinality failed")
    if set(level4) & set(level6):
        raise AssertionError("rigidity-forced level-4/level-6 disjointness failed")
    reflected_level6 = all(
        (residue in level6) != (shift - 1 - residue in level6)
        for residue in range(shift)
    )
    forced_high = all(
        member(mask, frobenius, value)
        for value in range(9 * shift, 13 * shift - 1)
    )
    forced_level7_gaps = all(
        not member(mask, frobenius, value)
        for value in range(7 * shift, 8 * shift)
    )
    if not reflected_level6:
        raise AssertionError("level-6 reflection invariant failed")
    if not forced_high or member(mask, frobenius, 9 * shift - 1):
        raise AssertionError("multiplicity/symmetry high-block invariant failed")
    if not forced_level7_gaps:
        raise AssertionError("level-5/symmetry gap-block invariant failed")
    vector = membership_vector(mask, frobenius)
    corrupted = mask & ~(1 << (4 * shift))
    corruption_failures = route_k_failures(corrupted, shift)
    if not any("multiplicity" in failure for failure in corruption_failures):
        raise AssertionError("corrupted multiplicity bit was not rejected")
    return {
        "shift": shift,
        "frobenius": frobenius,
        "membership": vector,
        "membership_sha256": hashlib.sha256(vector.encode("ascii")).hexdigest(),
        "multiplicity": multiplicity(mask, frobenius),
        "embedding_dimension": len(generators),
        "minimal_generators": list(generators),
        "level4_offsets": level4,
        "level4_count": len(level4),
        "level4_density_score": abs(14 * len(level4) - 5 * shift),
        "level6_offsets": level6,
        "level6_count": len(level6),
        "invariant_checks": {
            "even_shift": True,
            "forced_high_block": forced_high,
            "forced_gap_9s_minus_1": True,
            "forced_level7_gaps": forced_level7_gaps,
            "level6_reflection": reflected_level6,
            "level6_half_density": True,
            "level4_level6_disjoint": True,
        },
        "rigidity": rigidity,
        "corruption": {
            "cleared_value": 4 * shift,
            "rejected": True,
            "failures": list(corruption_failures),
        },
        "generalized_arithmetic_presentation": generalized_arithmetic_presentation(
            mask, frobenius, generators
        ),
    }


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


def solve_query(
    cnf: object,
    stem: str,
    query_root: Path,
    timeout_seconds: int,
    comments: list[str],
) -> tuple[str, set[int] | None, dict[str, object]]:
    query_root.mkdir(parents=True, exist_ok=True)
    cnf_path = query_root / f"{stem}.cnf"
    proof_path = query_root / f"{stem}.drat"
    solver_log_path = query_root / f"{stem}.cadical.log"
    checker_log_path = query_root / f"{stem}.drat-trim.log"
    cnf.write(cnf_path, comments=comments)
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
    seconds = time.perf_counter() - started
    output = completed.stdout + completed.stderr
    solver_log_path.write_text(output, encoding="utf-8")
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


def count_order(shift: int) -> list[int]:
    return sorted(range(1, shift + 1), key=lambda count: (abs(14 * count - 5 * shift), count))


def result_solver_seconds(result: dict[str, object]) -> float:
    seconds = 0.0
    existence = result.get("existence")
    if isinstance(existence, dict):
        seconds += float(existence.get("seconds", 0.0))
    for attempt in result.get("optimization_attempts", []):
        seconds += float(attempt["solve"].get("seconds", 0.0))
    return seconds


def run_shift(
    shift: int,
    proof_root: Path,
    timeout_seconds: int,
    checkpoint: dict[str, object],
    checkpoint_path: Path,
) -> dict[str, object]:
    print(f"Route K s={shift}: build unconstrained existence CNF", flush=True)
    cnf, h = build_route_k_cnf(shift)
    status, true_variables, solve = solve_query(
        cnf,
        f"s{shift:03d}-existence",
        proof_root / f"s{shift:03d}",
        timeout_seconds,
        [
            "EXP-006 Route K unconstrained-count existence",
            f"s={shift} F={13 * shift - 1} m={4 * shift}",
        ],
    )
    result: dict[str, object] = {
        "shift": shift,
        "status": status,
        "existence": solve,
        "optimization_attempts": [],
    }
    checkpoint["cases"][str(shift)] = result
    atomic_json(checkpoint_path, checkpoint)
    print(f"Route K s={shift}: existence {status} in {solve['seconds']:.3f}s", flush=True)
    if status != "SAT":
        return result

    assert true_variables is not None
    unconstrained_model = semantic_record(mask_from_model(h, true_variables), shift)
    unconstrained_model["solve"] = solve
    result["unconstrained_model"] = unconstrained_model
    incumbent_count = int(unconstrained_model["level4_count"])
    for count in count_order(shift):
        if count == incumbent_count:
            result["selected_model"] = unconstrained_model
            result["selected_count_source"] = "unconstrained existence model"
            result["status"] = "SAT_OPTIMAL"
            atomic_json(checkpoint_path, checkpoint)
            return result
        print(f"Route K s={shift}: density query level4_count={count}", flush=True)
        ranked_cnf, ranked_h = build_route_k_cnf(shift, count)
        ranked_status, ranked_true, ranked_solve = solve_query(
            ranked_cnf,
            f"s{shift:03d}-level4-{count:03d}",
            proof_root / f"s{shift:03d}",
            timeout_seconds,
            [
                "EXP-006 Route K level-4 density ranking",
                f"s={shift} level4_count={count}",
            ],
        )
        attempt: dict[str, object] = {
            "level4_count": count,
            "status": ranked_status,
            "solve": ranked_solve,
        }
        result["optimization_attempts"].append(attempt)
        atomic_json(checkpoint_path, checkpoint)
        print(
            f"Route K s={shift}: count={count} {ranked_status} in {ranked_solve['seconds']:.3f}s",
            flush=True,
        )
        if ranked_status == "UNKNOWN":
            result["status"] = "SAT_DENSITY_UNKNOWN"
            atomic_json(checkpoint_path, checkpoint)
            return result
        if ranked_status == "SAT":
            assert ranked_true is not None
            model = semantic_record(mask_from_model(ranked_h, ranked_true), shift)
            if int(model["level4_count"]) != count:
                raise AssertionError("cardinality-constrained model has the wrong count")
            model["solve"] = ranked_solve
            attempt["model_membership_sha256"] = model["membership_sha256"]
            result["selected_model"] = model
            result["selected_count_source"] = "ranked exact-cardinality query"
            result["status"] = "SAT_OPTIMAL"
            atomic_json(checkpoint_path, checkpoint)
            return result
    raise AssertionError("unconstrained SAT count was absent from the deterministic count order")


def external_manifest(root: Path) -> dict[str, object]:
    files: list[dict[str, object]] = []
    for path in sorted(value for value in root.rglob("*") if value.is_file()):
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return {
        "root_label": "EXP-006-block-family/route-k-v1",
        "file_count": len(files),
        "total_bytes": sum(int(item["bytes"]) for item in files),
        "aggregate_sha256": digest_rows(
            [f"{item['path']}:{item['bytes']}:{item['sha256']}" for item in files]
        ),
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-shift", type=int, default=16)
    parser.add_argument("--max-shift", type=int, default=40)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--proof-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--total-seconds", type=int, default=14400)
    args = parser.parse_args()
    if args.min_shift < 16 or args.min_shift % 2 or args.max_shift < args.min_shift or args.max_shift % 2:
        raise ValueError("campaign range must have even endpoints with 16<=min<=max")
    if min(args.timeout_seconds, args.total_seconds) <= 0:
        raise ValueError("budgets must be positive")
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    args.proof_root.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.artifact_dir / "route-k-checkpoint.json"
    tools = toolchain_identity()
    checkpoint: dict[str, object] = {
        "schema": 1,
        "toolchain": tools,
        "declared_range": [args.min_shift, args.max_shift],
        "calibration": None,
        "cases": {},
    }
    if checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        if checkpoint.get("toolchain") != tools:
            raise AssertionError("toolchain changed since checkpoint")
        if checkpoint.get("declared_range") != [args.min_shift, args.max_shift]:
            raise AssertionError("campaign range changed since checkpoint")

    if checkpoint.get("calibration") is None:
        print("Route K calibration s=14: start", flush=True)
        calibration_cnf, calibration_h = build_route_k_cnf(14)
        status, true_variables, solve = solve_query(
            calibration_cnf,
            "s014-calibration",
            args.proof_root / "s014",
            args.timeout_seconds,
            ["EXP-006 Route K public-seed calibration", "s=14 F=181 m=56"],
        )
        if status != "SAT" or true_variables is None:
            raise AssertionError(f"public calibration was not SAT: {status}")
        model = semantic_record(mask_from_model(calibration_h, true_variables), 14)
        if model["membership_sha256"] != PUBLIC_MEMBERSHIP_SHA256:
            raise AssertionError("s=14 calibration did not decode to the unique public semigroup")
        checkpoint["calibration"] = {"status": "PASS", "solve": solve, "model": model}
        atomic_json(checkpoint_path, checkpoint)
        print(f"Route K calibration s=14: PASS in {solve['seconds']:.3f}s", flush=True)

    values = list(range(args.min_shift, args.max_shift + 1, 2))
    for shift in values:
        prior = checkpoint["cases"].get(str(shift))
        if prior and prior.get("status") in {"UNSAT_VERIFIED", "SAT_OPTIMAL"}:
            print(f"Route K s={shift}: resume completed {prior['status']}", flush=True)
            continue
        spent = sum(result_solver_seconds(result) for result in checkpoint["cases"].values())
        if spent >= args.total_seconds:
            print(f"Route K total cap reached after {spent:.3f}s", flush=True)
            break
        result = run_shift(
            shift,
            args.proof_root,
            min(args.timeout_seconds, max(1, int(args.total_seconds - spent))),
            checkpoint,
            checkpoint_path,
        )
        if result["status"] not in {"UNSAT_VERIFIED", "SAT_OPTIMAL"}:
            break

    complete = all(
        checkpoint["cases"].get(str(shift), {}).get("status") in {"UNSAT_VERIFIED", "SAT_OPTIMAL"}
        for shift in values
    )
    sat_shifts = [
        shift for shift in values if checkpoint["cases"].get(str(shift), {}).get("status") == "SAT_OPTIMAL"
    ]
    unsat_shifts = [
        shift for shift in values if checkpoint["cases"].get(str(shift), {}).get("status") == "UNSAT_VERIFIED"
    ]
    manifest = external_manifest(args.proof_root)
    atomic_json(args.artifact_dir / "external-manifest.json", manifest)
    summary: dict[str, object] = {
        "status": "COMPLETE" if complete else "INCONCLUSIVE",
        "declared_range": [args.min_shift, args.max_shift],
        "tested_shifts": sorted(int(value) for value in checkpoint["cases"]),
        "sat_shifts": sat_shifts,
        "unsat_shifts": unsat_shifts,
        "nonseed_model_count": len(sat_shifts),
        "route_a_gate_open": len(sat_shifts) >= 3,
        "solver_seconds": sum(result_solver_seconds(result) for result in checkpoint["cases"].values()),
        "calibration_membership_sha256": checkpoint["calibration"]["model"]["membership_sha256"],
        "external_manifest_aggregate_sha256": manifest["aggregate_sha256"],
        "cases": checkpoint["cases"],
    }
    summary["aggregate_sha256"] = digest_rows(
        [
            f"{shift}:{summary['cases'][str(shift)]['status']}:"
            f"{summary['cases'][str(shift)].get('selected_model', {}).get('membership_sha256', '')}:"
            f"{summary['cases'][str(shift)]['existence']['cnf_sha256']}"
            for shift in sorted(int(value) for value in checkpoint["cases"])
        ]
        + [f"external:{manifest['aggregate_sha256']}"]
    )
    atomic_json(args.artifact_dir / "route-k-results.json", summary)
    print(json.dumps(summary, indent=2), flush=True)
    return 0 if complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
