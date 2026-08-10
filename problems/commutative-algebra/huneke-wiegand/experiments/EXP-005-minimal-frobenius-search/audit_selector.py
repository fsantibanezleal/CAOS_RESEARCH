"""Audit EXP-005 selector proofs, models, hashes, and strict search order."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT.parents[1] / "code"
sys.path.insert(0, str(CODE_ROOT))

from hwcert import analyze_rigidity, validate_symmetric_mask  # noqa: E402


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


def mask_from_membership(membership: str) -> int:
    if any(value not in "01" for value in membership):
        raise ValueError("membership string is not binary")
    return sum(1 << value for value, bit in enumerate(membership) if bit == "1")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--proof-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--public-results", type=Path)
    args = parser.parse_args()
    results = json.loads(args.results.read_text(encoding="utf-8"))
    values = [int(value) for value in results["completed_values"]]
    ordered = [(value, results["queries"][str(value)]) for value in values]
    missing: list[str] = []
    hash_mismatches: list[str] = []
    bad_logs: list[str] = []
    semantic_failures: list[str] = []
    expected_paths: list[Path] = []
    rows: list[str] = []
    sat_values: list[int] = []

    def verify(path: Path, expected_hash: str) -> None:
        expected_paths.append(path)
        if not path.exists():
            missing.append(str(path))
        elif sha256(path) != expected_hash:
            hash_mismatches.append(str(path))

    for frobenius, entry in ordered:
        root = args.proof_root / f"F{frobenius:03d}"
        stem = f"F{frobenius:03d}-selector"
        selector_cnf = root / f"{stem}.cnf"
        selector_log = root / f"{stem}.cadical.log"
        verify(selector_cnf, entry["cnf_sha256"])
        verify(selector_log, entry["solver_log_sha256"])
        if entry["status"] == "UNSAT_VERIFIED":
            proof = root / f"{stem}.drat"
            checker_log = root / f"{stem}.drat-trim.log"
            verify(proof, entry["proof_sha256"])
            verify(checker_log, entry["checker_log_sha256"])
            if selector_log.exists() and "s UNSATISFIABLE" not in selector_log.read_text(
                encoding="utf-8"
            ).splitlines():
                bad_logs.append(str(selector_log))
            if checker_log.exists() and "s VERIFIED" not in checker_log.read_text(
                encoding="utf-8"
            ).splitlines():
                bad_logs.append(str(checker_log))
        elif entry["status"] == "SAT_VALIDATED":
            sat_values.append(frobenius)
            if selector_log.exists() and "s SATISFIABLE" not in selector_log.read_text(
                encoding="utf-8"
            ).splitlines():
                bad_logs.append(str(selector_log))
            shift = int(entry["shift"])
            mask = mask_from_membership(entry["membership"])
            failures = validate_symmetric_mask(mask, frobenius)
            rigidity = analyze_rigidity(mask, frobenius, shift)
            if failures or not rigidity["rigid"]:
                semantic_failures.append(f"selector model F={frobenius}, s={shift}")
            fixed = entry["fixed_pair_adversary"]
            fixed_stem = f"F{frobenius:03d}-s{shift:03d}-fixed"
            fixed_cnf = root / f"{fixed_stem}.cnf"
            fixed_log = root / f"{fixed_stem}.cadical.log"
            verify(fixed_cnf, fixed["cnf_sha256"])
            verify(fixed_log, fixed["solver_log_sha256"])
            fixed_mask = mask_from_membership(fixed["membership"])
            fixed_failures = validate_symmetric_mask(fixed_mask, frobenius)
            fixed_rigidity = analyze_rigidity(fixed_mask, frobenius, shift)
            if fixed_failures or not fixed_rigidity["rigid"]:
                semantic_failures.append(f"fixed model F={frobenius}, s={shift}")
            if entry["membership"] != fixed["membership"]:
                semantic_failures.append(f"selector/fixed model mismatch F={frobenius}")
            if fixed_log.exists() and "s SATISFIABLE" not in fixed_log.read_text(
                encoding="utf-8"
            ).splitlines():
                bad_logs.append(str(fixed_log))
        else:
            semantic_failures.append(f"unexpected status {entry['status']} at F={frobenius}")
        rows.append(
            f"{frobenius}:{entry['status']}:{entry['cnf_sha256']}:"
            f"{entry.get('proof_sha256', '-')}"
        )

    computed_aggregate = hashlib.sha256("\n".join(rows).encode("ascii")).hexdigest()
    aggregate_matches = computed_aggregate == results["aggregate_sha256"]
    first_sat = results["first_sat_frobenius"]
    strict_order = values == list(range(values[0], values[-1] + 1, 2))
    if results["mode"] == "search":
        mode_order_valid = (
            sat_values == [first_sat]
            and values[-1] == first_sat
            and all(
                entry["status"] == "UNSAT_VERIFIED"
                for value, entry in ordered
                if value < first_sat
            )
        )
    elif results["mode"] == "regression":
        mode_order_valid = first_sat is None and not sat_values and all(
            entry["status"] == "UNSAT_VERIFIED" for _, entry in ordered
        )
    else:
        mode_order_valid = (
            results["mode"] == "calibrate"
            and len(values) == 1
            and sat_values == values
            and first_sat == values[0]
        )
    public_model_matches: bool | None = None
    if args.public_results is not None:
        public = json.loads(args.public_results.read_text(encoding="utf-8"))
        public_membership = public["queries"][f"{first_sat}:14"]["membership"]
        public_model_matches = (
            results["queries"][str(first_sat)]["membership"] == public_membership
        )
    all_checks_pass = (
        not missing
        and not hash_mismatches
        and not bad_logs
        and not semantic_failures
        and aggregate_matches
        and strict_order
        and mode_order_valid
        and public_model_matches is not False
    )
    existing_paths = [path for path in expected_paths if path.exists()]
    audit = {
        "verdict": "PASS" if all_checks_pass else "FAIL",
        "results_sha256": sha256(args.results),
        "completed_values": values,
        "first_sat_frobenius": first_sat,
        "first_sat_shift": results["first_sat_shift"],
        "strict_odd_order": strict_order,
        "mode_order_valid": mode_order_valid,
        "public_model_matches": public_model_matches,
        "files_expected": len(expected_paths),
        "files_hashed": len(existing_paths),
        "external_bytes": sum(path.stat().st_size for path in existing_paths),
        "missing": missing,
        "hash_mismatches": hash_mismatches,
        "bad_solver_or_checker_logs": bad_logs,
        "semantic_failures": semantic_failures,
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
