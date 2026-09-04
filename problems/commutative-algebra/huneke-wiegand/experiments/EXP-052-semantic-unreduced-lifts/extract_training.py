"""EXP-052 training-only semantic extraction for p=8,9,10."""

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
OUTPUT = HERE / "artifacts" / "training-p8-p10.json"
INCLUSIONS = ((58, 59), (58, 62))
PREMISES = {
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP047 / "artifacts" / "results.json": (
        "f78d251ae1746a88d1190756572aa251b9daf70ceb103cef9765c6d73b26f46c"
    ),
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
    EXP048 / "artifacts" / "results.json": (
        "ba44eae4c9193bc941411b059dc7a7d7a4c69dff3d818e05d3395338e125a400"
    ),
    EXP051 / "run.py": "4e0debc35c7aa286cfcc73dcbe6c6d4e1d15cfcc5e7d184db7e81e45f5e8b98a",
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


def verify_premises() -> dict[str, str]:
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def multiply_cycle(
    columns: list[list[list[int]]], cycle_columns: list[int], row_count: int
) -> list[int]:
    result = [0] * row_count
    for column in cycle_columns:
        for row, value in columns[column]:
            result[int(row)] += int(value)
    return result


def numeric_skeleton(value: object) -> object:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return "#"
    if isinstance(value, list):
        return [numeric_skeleton(item) for item in value]
    if isinstance(value, dict):
        return {key: numeric_skeleton(value[key]) for key in sorted(value)}
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget-seconds", type=float, default=300.0)
    parser.add_argument("--memory-gib", type=float, default=8.0)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    premises = verify_premises()
    exp036 = load_module("exp036_for_exp052_training", EXP036 / "run.py")
    exp037 = load_module("exp037_for_exp052_training", EXP037 / "run.py")
    exp042 = load_module("exp042_for_exp052_training", EXP042 / "run.py")
    exp047 = load_module("exp047_for_exp052_training", EXP047 / "run.py")
    exp048 = load_module("exp048_for_exp052_training", EXP048 / "run.py")
    exp051 = json.loads((EXP051 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    records = {
        (int(row["p"]), int(inclusion["source_mask"]), int(inclusion["target_mask"])): inclusion
        for row in exp051["rows"]
        for inclusion in row["inclusions"]
    }
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-052",
        "phase": "TRAINING_ONLY",
        "holdout_semantics_accessed": False,
        "parameters": {"p": [8, 9, 10], "budget_seconds": args.budget_seconds},
        "premise_hashes": premises,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    for p in (8, 9, 10):
        print(f"p={p} reconstruct labelled training component", flush=True)
        component = exp048.reconstruct_labelled_component(
            exp036=exp036, exp037=exp037, exp042=exp042, p=p, budget=budget
        )
        row_atoms = component["row_atoms"]
        p_record: dict[str, object] = {"p": p, "inclusions": []}
        for source, target in INCLUSIONS:
            relative_path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target}.json"
            relative = json.loads(relative_path.read_text(encoding="utf-8"))
            source_rows = set(exp047.rows_for_mask(row_atoms, source))
            added_rows = [
                row for row in exp047.rows_for_mask(row_atoms, target) if row not in source_rows
            ]
            if digest(added_rows) != relative["added_rows_hash"]:
                raise AssertionError({"p": p, "inclusion": [source, target], "added_rows_hash": False})
            selected = [
                record
                for record in records[p, source, target]["primary"]["selected"]
                if int(record["cycle_support_size"]) == 2
            ]
            if len(selected) != 1:
                raise AssertionError(
                    {"p": p, "inclusion": [source, target], "two_column_records": len(selected)}
                )
            witness = selected[0]
            doubled = multiply_cycle(
                relative["matrix_columns"],
                list(map(int, witness["cycle_columns"])),
                len(added_rows),
            )
            if any(value & 1 for value in doubled):
                raise AssertionError("stored binary cycle has an odd boundary")
            boundary = [value // 2 for value in doubled]
            stored_boundary = {int(row): int(value) for row, value in witness["boundary"]}
            if any(boundary[row] != stored_boundary.get(row, 0) for row in range(len(boundary))):
                raise AssertionError("EXP-051 exact boundary mismatch")
            semantic_rows = []
            for projected_row, coefficient in sorted(stored_boundary.items()):
                label = component["row_labels"][added_rows[projected_row]]
                token = exp048.normalize_added_row(label, p)
                semantic_rows.append(
                    {
                        "coefficient": coefficient,
                        "projected_row": projected_row,
                        "exact_label": label,
                        "token": token,
                        "coefficient_sensitive_skeleton": [
                            coefficient,
                            numeric_skeleton(token),
                        ],
                    }
                )
            semantic_multiset = sorted(
                [[record["coefficient"], record["token"]] for record in semantic_rows],
                key=lambda value: json.dumps(value, sort_keys=True, separators=(",", ":")),
            )
            p_record["inclusions"].append(
                {
                    "source_mask": source,
                    "target_mask": target,
                    "relative_sha256": sha256(relative_path),
                    "cycle_columns": witness["cycle_columns"],
                    "cycle_hash": witness["cycle_hash"],
                    "exact_identity": True,
                    "semantic_multiset_hash": digest(semantic_multiset),
                    "semantic_rows": semantic_rows,
                }
            )
        result["rows"].append(p_record)
        result["status"] = "CHECKPOINT"
        result["elapsed_seconds"] = budget.elapsed
        write_json_atomic(args.output, result)
        budget.check(f"p={p} training extraction")

    skeleton_vocabularies: dict[str, list[object]] = {}
    for source, target in INCLUSIONS:
        values = {
            json.dumps(record["coefficient_sensitive_skeleton"], sort_keys=True, separators=(",", ":"))
            for row in result["rows"]
            for inclusion in row["inclusions"]
            if (int(inclusion["source_mask"]), int(inclusion["target_mask"])) == (source, target)
            for record in inclusion["semantic_rows"]
        }
        skeleton_vocabularies[f"{source}->{target}"] = [json.loads(value) for value in sorted(values)]
    result["skeleton_vocabularies"] = skeleton_vocabularies
    result["p1_status"] = (
        "PASS_FINITE"
        if all(len(values) <= 12 for values in skeleton_vocabularies.values())
        else "REFUTED"
    )
    result["p2_status"] = "AWAITING_FROZEN_CANDIDATE"
    result["p3_status"] = "NOT_EVALUATED_HOLDOUT_LOCKED"
    result["status"] = "TRAINING_COMPLETE"
    result["elapsed_seconds"] = budget.elapsed
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "p1_status": result["p1_status"],
                "vocabulary_sizes": {
                    key: len(value) for key, value in skeleton_vocabularies.items()
                },
                "elapsed_seconds": result["elapsed_seconds"],
                "artifact_hash": result["artifact_hash"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
