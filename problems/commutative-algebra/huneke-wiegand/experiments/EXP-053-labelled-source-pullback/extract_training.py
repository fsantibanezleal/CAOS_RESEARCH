"""Pull the EXP-052 cycle back to exact source labels on training parameters."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
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
    EXP036 / "run.py": "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    EXP037 / "run.py": "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP047 / "run.py": "1350159ebc2c718208f62e08231f54ae2cc6178aa653bb5b67c100b56cd2a82b",
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
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


def make_component_model(
    *, exp036: ModuleType, exp037: ModuleType, exp042: ModuleType,
    exp048: ModuleType, p: int, budget: object,
) -> dict[str, object]:
    labelled = exp048.reconstruct_labelled_component(
        exp036=exp036, exp037=exp037, exp042=exp042, p=p, budget=budget
    )
    basis = exp037.build_basis(exp036, p, 2)
    d_rows = exp037.d_rows_for_basis(exp036, basis, budget)
    low = basis["low"]
    degree_two = basis["degree_two"]
    codomain = basis["codomain"]
    kernel_domain = basis["kernel_domain"]
    source = basis["source"]
    d_index = {row: index for index, row in enumerate(d_rows)}
    k_index = {row: index for index, row in enumerate(codomain)}
    k_base = len(d_rows)

    def row_label(row: int) -> list[object]:
        if row < k_base:
            exterior, product_kind, product_value = d_rows[row]
            return ["D", list(exterior), product_kind, product_value]
        exterior, coefficient = codomain[row - k_base]
        return ["K", list(exterior), coefficient]

    label_to_global = {
        json.dumps(row_label(row), separators=(",", ":")): row
        for row in range(len(d_rows) + len(codomain))
    }
    if len(label_to_global) != len(d_rows) + len(codomain):
        raise AssertionError("global row labels are not unique")
    component_globals = [
        label_to_global[json.dumps(label, separators=(",", ":"))]
        for label in labelled["row_labels"]
    ]
    global_to_component = {row: index for index, row in enumerate(component_globals)}

    def kernel_entries(column: int) -> list[tuple[int, int]]:
        exterior, coefficient = kernel_domain[column]
        entries: list[tuple[int, int]] = []
        for variable, sign, face in exp037.signed_faces(exterior):
            product_offset = coefficient + variable
            if product_offset in degree_two:
                entries.append((k_base + k_index[(face, product_offset)], sign))
        return entries

    def source_entries(column: int) -> list[tuple[int, int]]:
        exterior, coefficient = source[column]
        entries: list[tuple[int, int]] = []
        for variable, sign, face in exp037.signed_faces(exterior):
            if variable in low:
                product = exp036.low_product(p, variable, coefficient)
                if product is not None:
                    entries.append((d_index[(face, product[0], product[1])], sign))
            else:
                product_offset = variable + coefficient
                if product_offset in degree_two:
                    entries.append((k_base + k_index[(face, product_offset)], sign))
        return entries

    def combined_entries(column: int) -> list[tuple[int, int]]:
        if column < len(source):
            return source_entries(column)
        return kernel_entries(column - len(source))

    def column_label(column: int) -> list[object]:
        if column < len(source):
            exterior, coefficient = source[column]
            return ["S", list(exterior), coefficient]
        exterior, coefficient = kernel_domain[column - len(source)]
        return ["K", list(exterior), coefficient]

    def column_atom(column: int) -> str:
        if column < len(source):
            exterior, coefficient = source[column]
            kind = "S"
        else:
            exterior, coefficient = kernel_domain[column - len(source)]
            kind = "K"
        return exp042.semantic_atom(
            side="column",
            kind=kind,
            coefficient_tag=exp042.interval_tag(
                coefficient, exp042.generator_intervals(p)
            ),
            exterior=exterior,
            p=p,
        )

    frozen_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    frozen_atoms = [
        frozen["column_atom_table"][int(index)] for index in frozen["column_atom_ids"]
    ]
    frozen_keys = [
        (atom, json.dumps(entries, separators=(",", ":")))
        for atom, entries in zip(frozen_atoms, frozen["signed_columns"], strict=True)
    ]
    needed = Counter(frozen_keys)
    candidates: dict[tuple[str, str], list[int]] = {key: [] for key in needed}
    for column in range(len(source) + len(kernel_domain)):
        entries = sorted(
            (global_to_component[row], int(value))
            for row, value in combined_entries(column)
            if row in global_to_component and value
        )
        if not entries:
            continue
        key = (column_atom(column), json.dumps(entries, separators=(",", ":")))
        if key in needed:
            candidates[key].append(column)
    ambiguous = {
        digest(key): {"needed": needed[key], "candidates": len(candidates[key])}
        for key in needed
        if len(candidates[key]) != needed[key]
    }
    unique_mapping = not ambiguous
    original_columns: list[int] = []
    offsets: Counter[tuple[str, str]] = Counter()
    if unique_mapping:
        for key in frozen_keys:
            original_columns.append(candidates[key][offsets[key]])
            offsets[key] += 1
        if original_columns != sorted(original_columns):
            raise AssertionError("reconstructed component columns are not in original order")
    return {
        "labelled": labelled,
        "frozen": frozen,
        "frozen_path": frozen_path,
        "original_columns": original_columns,
        "column_labels": [column_label(column) for column in original_columns],
        "unique_mapping": unique_mapping,
        "ambiguous": ambiguous,
    }


def endpoint(value: int, tag: str, first: int, last: int) -> list[object]:
    left = value - first
    right = last - value
    return [tag, "L", left] if left <= right else [tag, "R", right]


def normalize_column(label: list[object], p: int) -> dict[str, object]:
    kind = str(label[0])
    exterior = {int(value) for value in label[1]}
    coefficient = int(label[2])
    intervals = [
        ("L0", 1, p), ("L1", 3 * p, 4 * p - 2), ("H0", 6 * p, 8 * p - 2),
        ("H1", 8 * p, 10 * p - 2), ("H2", 10 * p, 10 * p),
        ("H3", 11 * p - 1, 12 * p - 1), ("H4", 13 * p + 1, 14 * p - 2),
        ("H5", 14 * p, 15 * p - 1), ("H6", 16 * p, 16 * p),
        ("H7", 17 * p - 1, 18 * p - 1),
    ]
    interval = next((entry for entry in intervals if entry[1] <= coefficient <= entry[2]), None)
    if interval is None:
        raise AssertionError({"coefficient_outside_intervals": coefficient})
    low0 = set(range(1, p + 1))
    low1 = set(range(3 * p, 4 * p - 1))
    high = sorted(exterior - low0 - low1)
    return {
        "kind": kind,
        "coefficient": endpoint(coefficient, *interval),
        "l0_missing": [endpoint(value, "L0", 1, p) for value in sorted(low0 - exterior)],
        "l1_missing": [
            endpoint(value, "L1", 3 * p, 4 * p - 2) for value in sorted(low1 - exterior)
        ],
        "high_selected": [
            endpoint(value, tag, first, last)
            for value in high
            for tag, first, last in intervals
            if first <= value <= last
        ],
    }


def multiply(
    columns: list[list[list[int]]], vector: list[int], row_count: int
) -> list[int]:
    result = [0] * row_count
    for column, coefficient in enumerate(vector):
        if coefficient:
            for row, value in columns[column]:
                result[int(row)] += coefficient * int(value)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget-seconds", type=float, default=600.0)
    parser.add_argument("--memory-gib", type=float, default=10.0)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--finalize-partial", action="store_true")
    args = parser.parse_args()
    if args.finalize_partial:
        result = json.loads(args.output.read_text(encoding="utf-8"))
        inclusions = [item for row in result["rows"] for item in row["inclusions"]]
        skeleton_vocabularies: dict[str, list[object]] = {}
        for source_mask, target_mask in INCLUSIONS:
            values = {
                json.dumps(
                    record["coefficient_sensitive_skeleton"],
                    sort_keys=True,
                    separators=(",", ":"),
                )
                for row in result["rows"]
                for item in row["inclusions"]
                if (int(item["source_mask"]), int(item["target_mask"]))
                == (source_mask, target_mask)
                for record in item["source_support"]
            }
            skeleton_vocabularies[f"{source_mask}->{target_mask}"] = [
                json.loads(value) for value in sorted(values)
            ]
        result["completed_parameters"] = [int(row["p"]) for row in result["rows"]]
        result["stopped_parameter"] = 10
        result["resource_stop"] = (
            "p=10 transformed HNF did not return within the declared safe-stage budget; "
            "the process was interrupted after preserving p=8,9 checkpoints"
        )
        result["skeleton_vocabularies"] = skeleton_vocabularies
        result["p1_status"] = "INCONCLUSIVE_RESOURCE"
        result["p2_status"] = (
            "PASS_PARTIAL" if inclusions and all(
                int(item["source_max_abs_coefficient"]) <= 4 for item in inclusions
            ) and all(len(values) <= 12 for values in skeleton_vocabularies.values())
            else "REFUTED"
        )
        result["p3_status"] = "NOT_EVALUATED_HOLDOUT_LOCKED"
        result["status"] = "RESOURCE_STOP_WITH_P2_REFUTATION"
        result.pop("artifact_hash", None)
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        print(json.dumps({
            "status": result["status"], "p1": result["p1_status"],
            "p2": result["p2_status"],
            "completed_parameters": result["completed_parameters"],
            "supports": [item["source_support_size"] for item in inclusions],
            "max_abs": [item["source_max_abs_coefficient"] for item in inclusions],
            "skeleton_sizes": {
                key: len(value) for key, value in skeleton_vocabularies.items()
            }, "artifact_hash": result["artifact_hash"],
        }, indent=2))
        return 0
    premises = verify_premises()
    exp036 = load_module("exp036_for_exp053", EXP036 / "run.py")
    exp037 = load_module("exp037_for_exp053", EXP037 / "run.py")
    exp042 = load_module("exp042_for_exp053", EXP042 / "run.py")
    exp047 = load_module("exp047_for_exp053", EXP047 / "run.py")
    exp048 = load_module("exp048_for_exp053", EXP048 / "run.py")
    exp051 = json.loads((EXP051 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    witness_records = {
        (int(row["p"]), int(item["source_mask"]), int(item["target_mask"])): item
        for row in exp051["rows"] for item in row["inclusions"]
    }
    budget = exp048.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-053", "phase": "TRAINING_ONLY",
        "parameters": {"p": [8, 9, 10], "budget_seconds": args.budget_seconds},
        "p11_source_labels_accessed": False, "premise_hashes": premises, "rows": [],
    }
    write_json_atomic(args.output, result)
    for p in (8, 9, 10):
        print(f"p={p} reconstruct exact component column labels", flush=True)
        model = make_component_model(
            exp036=exp036, exp037=exp037, exp042=exp042, exp048=exp048,
            p=p, budget=budget,
        )
        frozen = model["frozen"]
        row_atoms = [
            frozen["row_atom_table"][int(index)] for index in frozen["row_atom_ids"]
        ]
        p_record: dict[str, object] = {
            "p": p, "matrix_sha256": sha256(model["frozen_path"]),
            "column_mapping_unique": model["unique_mapping"],
            "mapping_ambiguities": model["ambiguous"], "inclusions": [],
        }
        if not model["unique_mapping"]:
            result["rows"].append(p_record)
            result["status"] = "CHECKPOINT_MAPPING_AMBIGUOUS"
            write_json_atomic(args.output, result)
            continue
        for source_mask, target_mask in INCLUSIONS:
            source_rows = exp047.rows_for_mask(row_atoms, source_mask)
            kernel_rows, kernel_record = exp047.saturated_kernel(
                frozen["signed_columns"], source_rows
            )
            relative_path = EXP047 / "artifacts" / f"relative-p{p}-m{source_mask}-m{target_mask}.json"
            relative = json.loads(relative_path.read_text(encoding="utf-8"))
            if kernel_record["kernel_basis_hash"] != relative["kernel_basis_hash"]:
                raise AssertionError({"p": p, "inclusion": [source_mask, target_mask], "kernel_hash": False})
            selected = [
                item for item in witness_records[p, source_mask, target_mask]["primary"]["selected"]
                if int(item["cycle_support_size"]) == 2
            ]
            if len(selected) != 1:
                raise AssertionError({"two_column_witnesses": len(selected)})
            cycle_columns = list(map(int, selected[0]["cycle_columns"]))
            source_vector = [
                sum(kernel_rows[index][column] for index in cycle_columns)
                for column in range(len(frozen["signed_columns"]))
            ]
            full_boundary = multiply(frozen["signed_columns"], source_vector, int(frozen["rows"]))
            source_zero = all(full_boundary[row] == 0 for row in source_rows)
            source_set = set(source_rows)
            target_rows = exp047.rows_for_mask(row_atoms, target_mask)
            added_rows = [row for row in target_rows if row not in source_set]
            added_boundary = [full_boundary[row] for row in added_rows]
            relative_boundary = multiply(
                relative["matrix_columns"],
                [int(index in cycle_columns) for index in range(len(kernel_rows))],
                len(added_rows),
            )
            exact_identity = source_zero and added_boundary == relative_boundary
            support_records = []
            for column, coefficient in enumerate(source_vector):
                if not coefficient:
                    continue
                label = model["column_labels"][column]
                token = normalize_column(label, p)
                support_records.append({
                    "coefficient": coefficient, "matrix_column": column,
                    "original_column": model["original_columns"][column],
                    "exact_label": label, "token": token,
                    "coefficient_sensitive_skeleton": [coefficient, numeric_skeleton(token)],
                })
            p_record["inclusions"].append({
                "source_mask": source_mask, "target_mask": target_mask,
                "cycle_columns": cycle_columns,
                "kernel_basis_hash": kernel_record["kernel_basis_hash"],
                "source_support_size": len(support_records),
                "source_max_abs_coefficient": max((abs(item["coefficient"]) for item in support_records), default=0),
                "source_zero_on_mask": source_zero,
                "source_to_relative_identity": exact_identity,
                "source_multiset_hash": digest([
                    [item["coefficient"], item["token"]] for item in support_records
                ]),
                "source_support": support_records,
            })
        result["rows"].append(p_record)
        result["status"] = "CHECKPOINT"
        result["elapsed_seconds"] = budget.elapsed
        write_json_atomic(args.output, result)
        budget.check(f"p={p} source pullback")

    inclusions = [item for row in result["rows"] for item in row["inclusions"]]
    skeleton_vocabularies: dict[str, list[object]] = {}
    for source_mask, target_mask in INCLUSIONS:
        values = {
            json.dumps(record["coefficient_sensitive_skeleton"], sort_keys=True, separators=(",", ":"))
            for row in result["rows"] for item in row["inclusions"]
            if (int(item["source_mask"]), int(item["target_mask"])) == (source_mask, target_mask)
            for record in item["source_support"]
        }
        skeleton_vocabularies[f"{source_mask}->{target_mask}"] = [
            json.loads(value) for value in sorted(values)
        ]
    result["skeleton_vocabularies"] = skeleton_vocabularies
    result["p1_status"] = (
        "PASS_FINITE" if len(inclusions) == 6 and all(
            row["column_mapping_unique"] for row in result["rows"]
        ) and all(item["source_to_relative_identity"] for item in inclusions) else "REFUTED"
    )
    result["p2_status"] = (
        "PASS_FINITE" if inclusions and all(
            int(item["source_max_abs_coefficient"]) <= 4 for item in inclusions
        ) and all(len(values) <= 12 for values in skeleton_vocabularies.values()) else "REFUTED"
    )
    result["p3_status"] = "NOT_EVALUATED_HOLDOUT_LOCKED"
    result["status"] = "TRAINING_COMPLETE"
    result["elapsed_seconds"] = budget.elapsed
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps({
        "status": result["status"], "p1": result["p1_status"], "p2": result["p2_status"],
        "supports": [item["source_support_size"] for item in inclusions],
        "max_abs": [item["source_max_abs_coefficient"] for item in inclusions],
        "skeleton_sizes": {key: len(value) for key, value in skeleton_vocabularies.items()},
        "elapsed_seconds": result["elapsed_seconds"], "artifact_hash": result["artifact_hash"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
