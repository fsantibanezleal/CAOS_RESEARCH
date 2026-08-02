"""Recompute every EXP-004 Route B hash and status marker independently."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--proof-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = json.loads(args.results.read_text(encoding="utf-8"))
    ordered = sorted(
        results["queries"].items(),
        key=lambda item: tuple(map(int, item[0].split(":"))),
    )
    missing: list[str] = []
    hash_mismatches: list[str] = []
    bad_logs: list[str] = []
    expected_paths: list[Path] = []
    rows: list[str] = []
    for key, entry in ordered:
        frobenius = int(entry["frobenius"])
        shift = int(entry["shift"])
        stem = f"F{frobenius:03d}-s{shift:03d}"
        root = args.proof_root / f"F{frobenius:03d}"
        specifications = (
            (root / f"{stem}.cnf", entry["cnf_sha256"]),
            (root / f"{stem}.drat", entry["proof_sha256"]),
            (root / f"{stem}.cadical.log", entry["solver_log_sha256"]),
            (root / f"{stem}.drat-trim.log", entry["checker_log_sha256"]),
        )
        for path, expected in specifications:
            expected_paths.append(path)
            if not path.exists():
                missing.append(str(path))
            elif sha256(path) != expected:
                hash_mismatches.append(str(path))
        solver_log = specifications[2][0]
        checker_log = specifications[3][0]
        if solver_log.exists() and "s UNSATISFIABLE" not in solver_log.read_text(
            encoding="utf-8"
        ).splitlines():
            bad_logs.append(str(solver_log))
        if checker_log.exists() and "s VERIFIED" not in checker_log.read_text(
            encoding="utf-8"
        ).splitlines():
            bad_logs.append(str(checker_log))
        rows.append(
            f"{key}:{entry['status']}:{entry['cnf_sha256']}:{entry['proof_sha256']}"
        )
    computed_aggregate = hashlib.sha256("\n".join(rows).encode("ascii")).hexdigest()
    aggregate_matches = computed_aggregate == results["aggregate_sha256"]
    all_unsat_verified = all(
        entry["status"] == "UNSAT_VERIFIED" for _, entry in ordered
    )
    all_checks_pass = (
        len(ordered) == results["query_count"] == 1156
        and not missing
        and not hash_mismatches
        and not bad_logs
        and aggregate_matches
        and all_unsat_verified
    )
    existing_paths = [path for path in expected_paths if path.exists()]
    audit = {
        "verdict": "PASS" if all_checks_pass else "FAIL",
        "results_sha256": sha256(args.results),
        "manifest_entries": len(ordered),
        "files_expected": len(expected_paths),
        "files_hashed": len(existing_paths),
        "external_bytes": sum(path.stat().st_size for path in existing_paths),
        "missing": missing,
        "hash_mismatches": hash_mismatches,
        "bad_solver_or_checker_logs": bad_logs,
        "all_unsat_verified": all_unsat_verified,
        "stored_aggregate_sha256": results["aggregate_sha256"],
        "computed_aggregate_sha256": computed_aggregate,
        "aggregate_matches": aggregate_matches,
        "toolchain": results["toolchain"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    atomic_json(args.output, audit)
    print(json.dumps(audit, indent=2))
    return 0 if all_checks_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
