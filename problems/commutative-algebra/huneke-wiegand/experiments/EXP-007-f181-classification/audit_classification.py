"""Independent reconstruction audit for EXP-007 compact and external artifacts."""

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


DRAT_TRIM = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim"


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


def parse_model(output: str) -> set[int]:
    literals: list[int] = []
    for line in output.splitlines():
        if line.startswith("v "):
            literals.extend(int(value) for value in line[2:].split() if value != "0")
    if not literals:
        raise AssertionError("persisted SAT log contains no model")
    return {literal for literal in literals if literal > 0}


def serialized_sha256(cnf: object, comments: list[str]) -> str:
    lines = [f"c {comment}" for comment in comments]
    lines.append(f"p cnf {len(cnf.names)} {len(cnf.clauses)}")
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in cnf.clauses)
    payload = (os.linesep.join(lines) + os.linesep).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def mask_from_membership(value: str, frobenius: int) -> int:
    if len(value) != frobenius + 1 or set(value) - {"0", "1"}:
        raise AssertionError("invalid membership vector")
    return int(value[::-1], 2)


def assert_semantics(model: dict[str, object], frobenius: int, shift: int) -> None:
    vector = str(model["membership"])
    mask = mask_from_membership(vector, frobenius)
    failures = validate_symmetric_mask(mask, frobenius)
    rigidity = analyze_rigidity(mask, frobenius, shift)
    generators = minimal_generators(mask, frobenius)
    expected_hash = hashlib.sha256(vector.encode("ascii")).hexdigest()
    if failures or not rigidity["rigid"]:
        raise AssertionError(f"semantic failure: {failures}, {rigidity}")
    if model["membership_sha256"] != expected_hash:
        raise AssertionError("membership hash mismatch")
    if model["minimal_generators"] != list(generators):
        raise AssertionError("minimal-generator mismatch")
    if model["multiplicity"] != generators[0]:
        raise AssertionError("multiplicity mismatch")
    if model["embedding_dimension"] != len(generators):
        raise AssertionError("embedding-dimension mismatch")
    if model["rigidity"] != rigidity:
        raise AssertionError("persisted rigidity record mismatch")


def require_file(
    path: Path,
    expected_sha256: object,
    expected_files: set[Path],
) -> None:
    if not path.is_file():
        raise AssertionError(f"missing external artifact: {path}")
    expected_files.add(path.resolve())
    if sha256(path) != expected_sha256:
        raise AssertionError(f"external artifact hash mismatch: {path}")


def audit_solve_record(
    record: dict[str, object],
    phase_root: Path,
    expected_files: set[Path],
    expected_status: str,
    recheck_proofs: bool,
    proof_timeout_seconds: int,
) -> float:
    stem = str(record["stem"])
    cnf_path = phase_root / f"{stem}.cnf"
    solver_log_path = phase_root / f"{stem}.cadical.log"
    require_file(cnf_path, record["cnf_sha256"], expected_files)
    require_file(solver_log_path, record["solver_log_sha256"], expected_files)
    solver_log = solver_log_path.read_text(encoding="utf-8")
    marker = "s SATISFIABLE" if expected_status == "SAT" else "s UNSATISFIABLE"
    if marker not in solver_log:
        raise AssertionError(f"solver status marker absent from {solver_log_path}")
    recheck_seconds = 0.0
    if expected_status == "UNSAT":
        proof_path = phase_root / f"{stem}.drat"
        checker_log_path = phase_root / f"{stem}.drat-trim.log"
        require_file(proof_path, record["proof_sha256"], expected_files)
        require_file(checker_log_path, record["checker_log_sha256"], expected_files)
        if "s VERIFIED" not in checker_log_path.read_text(encoding="utf-8"):
            raise AssertionError(f"checker marker absent from {checker_log_path}")
        if recheck_proofs:
            started = time.perf_counter()
            completed = subprocess.run(
                ["wsl.exe", "-e", DRAT_TRIM, wsl_path(cnf_path), wsl_path(proof_path)],
                capture_output=True,
                text=True,
                timeout=proof_timeout_seconds + 30,
                check=False,
            )
            recheck_seconds = time.perf_counter() - started
            output = completed.stdout + completed.stderr
            if completed.returncode != 0 or "s VERIFIED" not in output:
                raise AssertionError(f"fresh proof recheck failed for {stem}")
    return recheck_seconds


def audit_support(
    result: dict[str, object],
    frobenius: int,
    proof_root: Path,
    expected_files: set[Path],
    recheck_proofs: bool,
    proof_timeout_seconds: int,
) -> tuple[tuple[int, ...], float]:
    if result.get("status") != "COMPLETE" or result.get("terminal") is None:
        raise AssertionError("support result is not complete")
    cnf, h, q = build_selector_rigidity_cnf(frobenius)
    models = result["models"]
    recheck_seconds = 0.0
    for index, model in enumerate(models):
        assert_semantics(model, frobenius, int(model["shift"]))
        record = model["discovery"]
        expected_stem = f"support-{index:03d}"
        if record["stem"] != expected_stem:
            raise AssertionError("support discovery order mismatch")
        comments = [
            "EXP-007 projected shift-support classification",
            f"F={frobenius}",
            "blocked shifts: " + " ".join(str(item["shift"]) for item in models[:index]),
        ]
        if serialized_sha256(cnf, comments) != record["cnf_sha256"]:
            raise AssertionError("reconstructed support SAT CNF hash mismatch")
        phase_root = proof_root / f"F{frobenius:03d}" / "support"
        audit_solve_record(
            record,
            phase_root,
            expected_files,
            "SAT",
            False,
            proof_timeout_seconds,
        )
        true_variables = parse_model(
            (phase_root / f"{expected_stem}.cadical.log").read_text(encoding="utf-8")
        )
        decoded_shift = shift_from_model(q, true_variables)
        decoded_mask = mask_from_model(h, true_variables)
        if decoded_shift != model["shift"]:
            raise AssertionError("support SAT log shift does not match compact result")
        if format(decoded_mask, f"0{frobenius + 1}b")[::-1] != model["membership"]:
            raise AssertionError("support SAT log membership does not match compact result")
        cnf.add(-q[decoded_shift - 1])

    terminal = result["terminal"]
    comments = [
        "EXP-007 projected shift-support classification",
        f"F={frobenius}",
        "blocked shifts: " + " ".join(str(model["shift"]) for model in models),
    ]
    if serialized_sha256(cnf, comments) != terminal["cnf_sha256"]:
        raise AssertionError("reconstructed support terminal CNF hash mismatch")
    recheck_seconds += audit_solve_record(
        terminal,
        proof_root / f"F{frobenius:03d}" / "support",
        expected_files,
        "UNSAT",
        recheck_proofs,
        proof_timeout_seconds,
    )
    shifts = tuple(sorted(int(model["shift"]) for model in models))
    if result["feasible_shifts"] != list(shifts):
        raise AssertionError("support shift list mismatch")
    aggregate = digest_rows(
        [f"{model['shift']}:{model['membership_sha256']}" for model in models]
        + [f"terminal:{terminal['cnf_sha256']}:{terminal['proof_sha256']}"]
    )
    if aggregate != result["aggregate_sha256"]:
        raise AssertionError("support aggregate mismatch")
    return shifts, recheck_seconds


def audit_fixed_class(
    result: dict[str, object],
    frobenius: int,
    shift: int,
    proof_root: Path,
    expected_files: set[Path],
    recheck_proofs: bool,
    proof_timeout_seconds: int,
) -> float:
    if result.get("status") != "COMPLETE" or result.get("terminal") is None:
        raise AssertionError(f"fixed class s={shift} is not complete")
    cnf, h = build_rigidity_cnf(frobenius, shift)
    models = result["models"]
    phase_root = proof_root / f"F{frobenius:03d}" / f"s{shift:03d}"
    for index, model in enumerate(models):
        if model["shift"] != shift:
            raise AssertionError("model occurs in the wrong fixed class")
        assert_semantics(model, frobenius, shift)
        record = model["discovery"]
        expected_stem = f"s{shift:03d}-{index:05d}"
        comments = [
            "EXP-007 fixed-shift projected membership classification",
            f"F={frobenius} s={shift}",
            f"blocked membership vectors: {index}",
        ]
        if record["stem"] != expected_stem:
            raise AssertionError("fixed-class discovery order mismatch")
        if serialized_sha256(cnf, comments) != record["cnf_sha256"]:
            raise AssertionError("reconstructed fixed SAT CNF hash mismatch")
        audit_solve_record(
            record,
            phase_root,
            expected_files,
            "SAT",
            False,
            proof_timeout_seconds,
        )
        true_variables = parse_model(
            (phase_root / f"{expected_stem}.cadical.log").read_text(encoding="utf-8")
        )
        decoded_mask = mask_from_model(h, true_variables)
        if format(decoded_mask, f"0{frobenius + 1}b")[::-1] != model["membership"]:
            raise AssertionError("fixed SAT log membership does not match compact result")
        projected_true = {
            variable for value, variable in enumerate(h) if decoded_mask & (1 << value)
        }
        cnf.add(*projected_blocking_clause(h, projected_true))

    terminal = result["terminal"]
    comments = [
        "EXP-007 fixed-shift projected membership classification",
        f"F={frobenius} s={shift}",
        f"blocked membership vectors: {len(models)}",
    ]
    if serialized_sha256(cnf, comments) != terminal["cnf_sha256"]:
        raise AssertionError("reconstructed fixed terminal CNF hash mismatch")
    recheck_seconds = audit_solve_record(
        terminal,
        phase_root,
        expected_files,
        "UNSAT",
        recheck_proofs,
        proof_timeout_seconds,
    )
    if result["model_count"] != len(models):
        raise AssertionError("fixed model count mismatch")
    aggregate = digest_rows(
        [str(model["membership_sha256"]) for model in models]
        + [f"terminal:{terminal['cnf_sha256']}:{terminal['proof_sha256']}"]
    )
    if aggregate != result["aggregate_sha256"]:
        raise AssertionError("fixed aggregate mismatch")
    return recheck_seconds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--proof-root", type=Path, required=True)
    parser.add_argument("--frobenius", type=int, default=181)
    parser.add_argument("--recheck-proofs", action="store_true")
    parser.add_argument("--proof-timeout-seconds", type=int, default=1800)
    args = parser.parse_args()
    support = json.loads((args.artifact_dir / "support-results.json").read_text(encoding="utf-8"))
    classification = json.loads(
        (args.artifact_dir / "classification-results.json").read_text(encoding="utf-8")
    )
    if classification.get("status") != "COMPLETE":
        raise AssertionError("classification result is not complete")
    if classification["toolchain"] != support["toolchain"]:
        raise AssertionError("compact results use different toolchains")
    if classification["support_aggregate_sha256"] != support["aggregate_sha256"]:
        raise AssertionError("classification references another support result")

    expected_files: set[Path] = set()
    shifts, recheck_seconds = audit_support(
        support,
        args.frobenius,
        args.proof_root,
        expected_files,
        args.recheck_proofs,
        args.proof_timeout_seconds,
    )
    classes = classification["classes"]
    if sorted(map(int, classes)) != list(shifts):
        raise AssertionError("fixed classes do not equal support shifts")
    all_models: list[dict[str, object]] = []
    for shift in shifts:
        result = classes[str(shift)]
        recheck_seconds += audit_fixed_class(
            result,
            args.frobenius,
            shift,
            args.proof_root,
            expected_files,
            args.recheck_proofs,
            args.proof_timeout_seconds,
        )
        all_models.extend(result["models"])

    if classification["normalized_pair_count"] != len(all_models):
        raise AssertionError("normalized-pair count mismatch")
    distinct_count = len({str(model["membership"]) for model in all_models})
    if classification["distinct_semigroup_count"] != distinct_count:
        raise AssertionError("distinct-semigroup count mismatch")
    unique_prediction = len(all_models) == 1 and list(shifts) == [14]
    if classification["unique_public_pair_prediction"] != unique_prediction:
        raise AssertionError("uniqueness prediction evaluation mismatch")
    aggregate = digest_rows(
        [str(support["aggregate_sha256"])]
        + [f"{shift}:{classes[str(shift)]['aggregate_sha256']}" for shift in shifts]
    )
    if aggregate != classification["aggregate_sha256"]:
        raise AssertionError("classification aggregate mismatch")

    actual_files = {
        path.resolve() for path in args.proof_root.rglob("*") if path.is_file()
    }
    extra_files = sorted(str(path) for path in actual_files - expected_files)
    missing_references = sorted(str(path) for path in expected_files - actual_files)
    if extra_files or missing_references:
        raise AssertionError(
            f"external manifest mismatch: extra={extra_files}, missing={missing_references}"
        )
    manifest_rows = [
        f"{path.relative_to(args.proof_root.resolve()).as_posix()}:{path.stat().st_size}:{sha256(path)}"
        for path in sorted(expected_files)
    ]
    output = {
        "status": "PASS",
        "frobenius": args.frobenius,
        "feasible_shifts": list(shifts),
        "normalized_pair_count": len(all_models),
        "distinct_semigroup_count": distinct_count,
        "unique_public_pair": unique_prediction,
        "proofs_freshly_rechecked": args.recheck_proofs,
        "fresh_proof_recheck_seconds": recheck_seconds,
        "external_file_count": len(expected_files),
        "external_total_bytes": sum(path.stat().st_size for path in expected_files),
        "external_manifest_sha256": digest_rows(manifest_rows),
        "classification_aggregate_sha256": classification["aggregate_sha256"],
        "failures": [],
    }
    output_path = args.artifact_dir / "classification-audit.json"
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
