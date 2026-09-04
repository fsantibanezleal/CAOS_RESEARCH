"""Independent labelled-component audit for the EXP-052 holdout."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP036 = EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy"
EXP037 = EXPERIMENTS / "EXP-037-connecting-quasipolynomial"
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP047 = EXPERIMENTS / "EXP-047-relative-kernel-smith"
EXP048 = EXPERIMENTS / "EXP-048-semantic-relative-bockstein"
RESULTS = HERE / "artifacts" / "holdout-p11.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED = {
    HERE / "run_holdout.py": "2bd9d28fcfaf44b303a58ec674b972b095fd4fe5b91b015c773bf788d4759c7b",
    HERE / "candidate.py": "6a16d8cf2c112a800558d634f6cd058ea00be43986c7b92f7f9406a6d282ca0c",
    RESULTS: "0bb32fd050a8e9739ea866ffb6e75b612189899c84c350a1214b60ed78eebc8b",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def canonical_basis(vectors: list[int]) -> list[int]:
    basis: dict[int, int] = {}
    for raw in vectors:
        vector = raw
        for pivot in sorted(basis):
            if vector & (1 << pivot):
                vector ^= basis[pivot]
        if not vector:
            continue
        pivot = (vector & -vector).bit_length() - 1
        for other in list(basis):
            if basis[other] & (1 << pivot):
                basis[other] ^= vector
        basis[pivot] = vector
    return [basis[pivot] for pivot in sorted(basis)]


def reduce_mod_basis(vector: int, basis: list[int]) -> int:
    for basis_vector in basis:
        pivot = (basis_vector & -basis_vector).bit_length() - 1
        if vector & (1 << pivot):
            vector ^= basis_vector
    return vector


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    parser.add_argument("--memory-gib", type=float, default=8.0)
    args = parser.parse_args()
    for path, expected in EXPECTED.items():
        if sha256(path) != expected:
            raise AssertionError(f"frozen hash mismatch: {path}")
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, value: bool) -> None:
        checks.append({"name": name, "pass": bool(value)})

    stored_hash = results.pop("artifact_hash")
    check("holdout internal hash", digest(results) == stored_hash)
    results["artifact_hash"] = stored_hash
    check("holdout complete", results["status"] == "COMPLETE")
    check("P1 finite pass", results["p1_status"] == "PASS_FINITE")
    check("P2 training pass", results["p2_status"] == "PASS_TRAINING")
    check("P3 finite holdout pass", results["p3_status"] == "PASS_FINITE_HOLDOUT")

    exp036 = load_module("exp036_for_exp052_audit", EXP036 / "run.py")
    exp037 = load_module("exp037_for_exp052_audit", EXP037 / "run.py")
    exp042 = load_module("exp042_for_exp052_audit", EXP042 / "run.py")
    exp047 = load_module("exp047_for_exp052_audit", EXP047 / "run.py")
    exp048 = load_module("exp048_for_exp052_audit", EXP048 / "run.py")
    candidate = load_module("exp052_frozen_candidate_audit", HERE / "candidate.py")
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    print("p=11 independently reconstruct labelled holdout component", flush=True)
    component = exp048.reconstruct_labelled_component(
        exp036=exp036, exp037=exp037, exp042=exp042, p=11, budget=budget
    )
    row_atoms = component["row_atoms"]
    for result_record in results["inclusions"]:
        source = int(result_record["source_mask"])
        target = int(result_record["target_mask"])
        prefix = f"p=11 {source}->{target}"
        relative_path = EXP047 / "artifacts" / f"relative-p11-m{source}-m{target}.json"
        relative = json.loads(relative_path.read_text(encoding="utf-8"))
        check(f"{prefix} relative hash", sha256(relative_path) == result_record["relative_sha256"])
        source_rows = set(exp047.rows_for_mask(row_atoms, source))
        added_rows = [
            row for row in exp047.rows_for_mask(row_atoms, target) if row not in source_rows
        ]
        check(f"{prefix} added-row hash", digest(added_rows) == relative["added_rows_hash"])
        cycle_columns = list(map(int, result_record["cycle_columns"]))
        doubled = [0] * len(added_rows)
        for column in cycle_columns:
            for row, value in relative["matrix_columns"][column]:
                doubled[int(row)] += int(value)
        check(f"{prefix} even boundary", all(not (value & 1) for value in doubled))
        boundary = [value // 2 for value in doubled]
        observed = []
        semantic_rows = []
        for projected_row, coefficient in enumerate(boundary):
            if not coefficient:
                continue
            label = component["row_labels"][added_rows[projected_row]]
            token = exp048.normalize_added_row(label, 11)
            observed.append([coefficient, token])
            semantic_rows.append(
                {
                    "coefficient": coefficient,
                    "projected_row": projected_row,
                    "exact_label": label,
                    "token": token,
                }
            )
        observed.sort(key=lambda value: json.dumps(value, sort_keys=True, separators=(",", ":")))
        predicted = candidate.candidate(11, source, target)
        check(f"{prefix} frozen formula", observed == predicted)
        check(f"{prefix} observed size", len(observed) == int(result_record["observed_size"]))
        check(f"{prefix} predicted size", len(predicted) == int(result_record["predicted_size"]))
        check(f"{prefix} observed hash", digest(observed) == result_record["observed_hash"])
        check(f"{prefix} predicted hash", digest(predicted) == result_record["predicted_hash"])
        check(f"{prefix} exact labelled rows", semantic_rows == result_record["semantic_rows"])
        column_parities = [
            sum(1 << int(row) for row, value in column if int(value) & 1)
            for column in relative["matrix_columns"]
        ]
        image_basis = canonical_basis(column_parities)
        parity = sum(1 << row for row, value in enumerate(boundary) if value & 1)
        quotient = reduce_mod_basis(parity, image_basis)
        check(f"{prefix} nonzero quotient", quotient != 0)
        check(f"{prefix} quotient hash", digest(quotient) == result_record["quotient_class_hash"])
        check(f"{prefix} exact result flag", bool(result_record["exact_identity"]))
        check(f"{prefix} formula result flag", bool(result_record["formula_match"]))
        budget.check(f"{prefix} audit")

    passed = sum(record["pass"] for record in checks)
    certificate = {
        "experiment": "EXP-052",
        "audit": "independent p=11 labelled reconstruction and exact formula comparison",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "frozen_hashes": {str(path.relative_to(EXPERIMENTS)): value for path, value in EXPECTED.items()},
        "elapsed_seconds": budget.elapsed,
        "checks": checks,
    }
    certificate["artifact_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(
        json.dumps(
            {
                key: certificate[key]
                for key in ("status", "checks_passed", "checks_total", "elapsed_seconds", "artifact_hash")
            },
            indent=2,
        )
    )
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
