"""Independent original-boundary audit of the EXP-065 endpoint witnesses."""

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
EXP048 = EXPERIMENTS / "EXP-048-semantic-relative-bockstein"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-results.json"
PREMISES = {
    HERE / "run.py": "2a6d297c57715e92ca0330d912317b787028de295d0557424625b7f5d59e56b2",
    RESULTS: "2536e749ac7406f88577068107fd2ac6f79ab20876b8d3293e9c78c4cd695ee1",
    EXP036 / "run.py": "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    EXP037 / "run.py": "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def key(label: list[object]) -> str:
    return json.dumps(label, separators=(",", ":"))


def source_formula(p: int, r: int) -> list[object]:
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    exterior = sorted((low - {p - r, 3 * p, 3 * p + r}) | {6 * p, 10 * p})
    return ["S", exterior, p - 2]


def target_formula(p: int, r: int) -> list[object]:
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    exterior = sorted((low - {p - r, 3 * p, 3 * p + r}) | {6 * p})
    return ["K", exterior, 11 * p - 2]


def original_boundary(
    p: int, label: list[object], exp036: ModuleType, exp037: ModuleType,
    basis: dict[str, object], component_index: dict[str, int],
) -> list[tuple[int, int]]:
    kind, exterior_raw, coefficient_raw = label
    if kind != "S":
        raise AssertionError("EXP-065 witness is not an original S column")
    exterior = tuple(int(value) for value in exterior_raw)
    coefficient = int(coefficient_raw)
    low = basis["low"]
    degree_two = basis["degree_two"]
    entries = []
    for variable, sign, face in exp037.signed_faces(exterior):
        row_label = None
        if variable in low:
            product = exp036.low_product(p, variable, coefficient)
            if product is not None:
                row_label = ["D", list(face), product[0], product[1]]
        elif variable + coefficient in degree_two:
            row_label = ["K", list(face), variable + coefficient]
        if row_label is not None and key(row_label) in component_index:
            entries.append((component_index[key(row_label)], int(sign)))
    return sorted(entries)


def audit_parameter(
    producer_row: dict[str, object], modules: dict[str, ModuleType], budget: object
) -> dict[str, object]:
    p = int(producer_row["p"])
    labelled = modules["exp048"].reconstruct_labelled_component(
        exp036=modules["exp036"],
        exp037=modules["exp037"],
        exp042=modules["exp042"],
        p=p,
        budget=budget,
    )
    basis = modules["exp037"].build_basis(modules["exp036"], p, 2)
    component_index = {
        key(label): index for index, label in enumerate(labelled["row_labels"])
    }
    selected = modules["exp048"].rows_for_mask(labelled["row_atoms"], 58)
    positions = {row: position for position, row in enumerate(selected)}
    frozen = json.loads(
        (EXP042 / "artifacts" / f"matrix-p{p}.json").read_text(encoding="utf-8")
    )
    target_records = []
    for target in reversed(producer_row["targets"]):
        r = int(target["triangle"][1])
        expected_source = source_formula(p, r)
        expected_target = target_formula(p, r)
        support = target["witness"]["support"]
        if len(support) != 1 or int(support[0]["coefficient"]) != -1:
            raise AssertionError({"p": p, "r": r, "single_negative_source": False})
        if support[0]["exact_label"] != expected_source:
            raise AssertionError({"p": p, "r": r, "source_formula": False})
        if target["label"] != expected_target:
            raise AssertionError({"p": p, "r": r, "target_formula": False})

        boundary = original_boundary(
            p, expected_source, modules["exp036"], modules["exp037"], basis,
            component_index,
        )
        frozen_column = sorted(
            (int(row), int(value))
            for row, value in frozen["signed_columns"][int(support[0]["column"])]
        )
        if boundary != frozen_column:
            raise AssertionError({"p": p, "r": r, "semantic_column_mapping": False})
        projected = sorted(
            (positions[row], value) for row, value in boundary if row in positions
        )
        target_component = component_index[key(expected_target)]
        target_position = positions[target_component]
        if projected != [(target_position, -1)]:
            raise AssertionError({"p": p, "r": r, "projected_boundary": projected})

        mutated_source = list(expected_source)
        mutated_source[2] = int(mutated_source[2]) + 1
        mutated_boundary = original_boundary(
            p, mutated_source, modules["exp036"], modules["exp037"], basis,
            component_index,
        )
        mutated_projected = sorted(
            (positions[row], value) for row, value in mutated_boundary if row in positions
        )
        if mutated_projected == [(target_position, -1)]:
            raise AssertionError({"p": p, "r": r, "source_mutation_rejected": False})
        mutated_target = [((target_position + 1) % len(selected), -1)]
        if projected == mutated_target:
            raise AssertionError({"p": p, "r": r, "target_mutation_rejected": False})
        target_records.append({
            "r": r,
            "triangle": target["triangle"],
            "source_formula": expected_source,
            "target_formula": expected_target,
            "component_column": int(support[0]["column"]),
            "complete_surviving_boundary": projected,
            "single_negative_face": True,
            "source_mutation_rejected": True,
            "target_mutation_rejected": True,
            "boundary_hash": digest(boundary),
        })
    return {
        "p": p,
        "component_rows": len(labelled["row_labels"]),
        "selected_rows": len(selected),
        "targets": sorted(target_records, key=lambda item: item["r"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget-seconds", type=float, default=900.0)
    parser.add_argument("--memory-gib", type=float, default=8.0)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    producer = json.loads(RESULTS.read_text(encoding="utf-8"))
    unsigned = dict(producer)
    stored_hash = unsigned.pop("artifact_hash")
    if digest(unsigned) != stored_hash:
        raise AssertionError("producer internal artifact hash mismatch")

    modules = {
        "exp036": load_module("exp036_for_exp065_audit", EXP036 / "run.py"),
        "exp037": load_module("exp037_for_exp065_audit", EXP037 / "run.py"),
        "exp042": load_module("exp042_for_exp065_audit", EXP042 / "run.py"),
        "exp048": load_module("exp048_for_exp065_audit", EXP048 / "run.py"),
    }
    rows = []
    for producer_row in reversed(producer["rows"]):
        p = int(producer_row["p"])
        print(f"audit p={p} rebuild original endpoint boundaries", flush=True)
        budget = modules["exp048"].Budget(args.budget_seconds, args.memory_gib)
        rows.append(audit_parameter(producer_row, modules, budget))
    rows.sort(key=lambda row: row["p"])
    targets = [target for row in rows for target in row["targets"]]
    result = {
        "experiment": "EXP-065 independent audit",
        "route": "original differential rebuilt from semantic source formulas",
        "premises": actual,
        "status": "INDEPENDENT_AUDIT_PASS",
        "parameters": [row["p"] for row in rows],
        "targets": len(targets),
        "single_column_witnesses": sum(target["single_negative_face"] for target in targets),
        "mutations_rejected": 2 * len(targets),
        "formula": (
            "S_(p,r)=[S,(L_p\\{p-r,3p,3p+r})U{6p,10p};p-2], "
            "pi_58 d(S_(p,r))=-x_(0,r,p-2-r), r=1,2"
        ),
        "rows": rows,
    }
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps({
        "status": result["status"],
        "parameters": result["parameters"],
        "targets": result["targets"],
        "mutations_rejected": result["mutations_rejected"],
        "artifact_hash": result["artifact_hash"],
    }, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
