"""EXP-052 untouched p=11 semantic holdout."""

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
EXP051 = EXPERIMENTS / "EXP-051-minimal-unreduced-lifts"
TRAINING = HERE / "artifacts" / "training-p8-p10.json"
TRAINING_CHECK = HERE / "artifacts" / "training-candidate-check.json"
CANDIDATE = HERE / "candidate.py"
CANDIDATE_RECORD = HERE / "candidate.md"
OUTPUT = HERE / "artifacts" / "holdout-p11.json"
INCLUSIONS = ((58, 59), (58, 62))
FROZEN = {
    CANDIDATE: "6a16d8cf2c112a800558d634f6cd058ea00be43986c7b92f7f9406a6d282ca0c",
    CANDIDATE_RECORD: "6cc76e4342e99eede841df638c4aae21bd6dae917fbe0daf5b3e0fd15077b0db",
    TRAINING: "259ff476b7bb09c12566e4bd771da5c88af17f541cc5732db4dc7f2067e2ec70",
    TRAINING_CHECK: "8b69d8bb37535211c21569249b9dc1f8f9632121fa2c9da3e4e80120169892e7",
    EXP051 / "artifacts" / "results.json": (
        "f1acaa6b769ec04b7d87a1ac416c184ffac2f5007d18a04efb397c8013ec8b1f"
    ),
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


def multiply_cycle(
    columns: list[list[list[int]]], cycle_columns: list[int], row_count: int
) -> list[int]:
    result = [0] * row_count
    for column in cycle_columns:
        for row, value in columns[column]:
            result[int(row)] += int(value)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    parser.add_argument("--memory-gib", type=float, default=8.0)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in FROZEN}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash
        for path, expected_hash in FROZEN.items()
    }
    if actual != expected:
        raise AssertionError({"frozen_candidate_mismatch": {"actual": actual, "expected": expected}})
    training = json.loads(TRAINING.read_text(encoding="utf-8"))
    training_check = json.loads(TRAINING_CHECK.read_text(encoding="utf-8"))
    if training["holdout_semantics_accessed"] or training_check["status"] != "PASS":
        raise AssertionError("training/candidate gate failed")

    exp036 = load_module("exp036_for_exp052_holdout", EXP036 / "run.py")
    exp037 = load_module("exp037_for_exp052_holdout", EXP037 / "run.py")
    exp042 = load_module("exp042_for_exp052_holdout", EXP042 / "run.py")
    exp047 = load_module("exp047_for_exp052_holdout", EXP047 / "run.py")
    exp048 = load_module("exp048_for_exp052_holdout", EXP048 / "run.py")
    candidate = load_module("exp052_frozen_candidate_holdout", CANDIDATE)
    exp051 = json.loads((EXP051 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    records = {
        (int(row["p"]), int(inclusion["source_mask"]), int(inclusion["target_mask"])): inclusion
        for row in exp051["rows"]
        for inclusion in row["inclusions"]
    }
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-052",
        "phase": "UNTOUCHED_HOLDOUT",
        "status": "RUNNING",
        "parameters": {"p": 11, "budget_seconds": args.budget_seconds},
        "frozen_hashes": actual,
        "inclusions": [],
    }
    write_json_atomic(args.output, result)
    print("p=11 reconstruct untouched labelled holdout component", flush=True)
    component = exp048.reconstruct_labelled_component(
        exp036=exp036, exp037=exp037, exp042=exp042, p=11, budget=budget
    )
    row_atoms = component["row_atoms"]
    for source, target in INCLUSIONS:
        relative_path = EXP047 / "artifacts" / f"relative-p11-m{source}-m{target}.json"
        relative = json.loads(relative_path.read_text(encoding="utf-8"))
        source_rows = set(exp047.rows_for_mask(row_atoms, source))
        added_rows = [
            row for row in exp047.rows_for_mask(row_atoms, target) if row not in source_rows
        ]
        if digest(added_rows) != relative["added_rows_hash"]:
            raise AssertionError({"inclusion": [source, target], "added_rows_hash": False})
        selected = [
            record
            for record in records[11, source, target]["primary"]["selected"]
            if int(record["cycle_support_size"]) == 2
        ]
        if len(selected) != 1:
            raise AssertionError({"inclusion": [source, target], "two_column_records": len(selected)})
        witness = selected[0]
        columns = relative["matrix_columns"]
        doubled = multiply_cycle(columns, list(map(int, witness["cycle_columns"])), len(added_rows))
        even = all(not (value & 1) for value in doubled)
        boundary = [value // 2 for value in doubled]
        stored_boundary = {int(row): int(value) for row, value in witness["boundary"]}
        exact_identity = even and all(
            boundary[row] == stored_boundary.get(row, 0) for row in range(len(boundary))
        )
        column_parities = [
            sum(1 << int(row) for row, value in column if int(value) & 1)
            for column in columns
        ]
        image_basis = canonical_basis(column_parities)
        parity = sum(1 << row for row, value in enumerate(boundary) if value & 1)
        quotient = reduce_mod_basis(parity, image_basis)
        observed = []
        semantic_rows = []
        for projected_row, coefficient in sorted(stored_boundary.items()):
            label = component["row_labels"][added_rows[projected_row]]
            semantic = exp048.normalize_added_row(label, 11)
            observed.append([coefficient, semantic])
            semantic_rows.append(
                {
                    "coefficient": coefficient,
                    "projected_row": projected_row,
                    "exact_label": label,
                    "token": semantic,
                }
            )
        observed.sort(key=lambda value: json.dumps(value, sort_keys=True, separators=(",", ":")))
        predicted = candidate.candidate(11, source, target)
        formula_match = observed == predicted
        result["inclusions"].append(
            {
                "source_mask": source,
                "target_mask": target,
                "relative_sha256": sha256(relative_path),
                "cycle_columns": witness["cycle_columns"],
                "cycle_hash": witness["cycle_hash"],
                "exact_identity": exact_identity,
                "nonzero_quotient_class": bool(quotient),
                "quotient_class_hash": digest(quotient),
                "formula_match": formula_match,
                "observed_size": len(observed),
                "predicted_size": len(predicted),
                "observed_hash": digest(observed),
                "predicted_hash": digest(predicted),
                "semantic_rows": semantic_rows,
            }
        )
        result["status"] = "CHECKPOINT"
        result["elapsed_seconds"] = budget.elapsed
        write_json_atomic(args.output, result)
        budget.check(f"p=11 {source}->{target} holdout")

    result["p1_status"] = training["p1_status"]
    result["p2_status"] = training_check["p2_status"]
    result["p3_status"] = (
        "PASS_FINITE_HOLDOUT"
        if all(
            record["formula_match"]
            and record["exact_identity"]
            and record["nonzero_quotient_class"]
            for record in result["inclusions"]
        )
        else "REFUTED"
    )
    result["status"] = "COMPLETE"
    result["elapsed_seconds"] = budget.elapsed
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "p1_status": result["p1_status"],
                "p2_status": result["p2_status"],
                "p3_status": result["p3_status"],
                "holdout": [
                    {
                        "inclusion": [record["source_mask"], record["target_mask"]],
                        "formula_match": record["formula_match"],
                        "size": record["observed_size"],
                    }
                    for record in result["inclusions"]
                ],
                "elapsed_seconds": result["elapsed_seconds"],
                "artifact_hash": result["artifact_hash"],
            },
            indent=2,
        )
    )
    return 0 if result["p3_status"] == "PASS_FINITE_HOLDOUT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
