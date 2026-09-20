"""EXP-066 producer: holdout and uniform endpoint face classification."""

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
EXP048 = EXPERIMENTS / "EXP-048-semantic-relative-bockstein"
EXP053 = EXPERIMENTS / "EXP-053-labelled-source-pullback"
EXP063 = EXPERIMENTS / "EXP-063-triangle-isolated-comparison"
OUTPUT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
PREMISES = {
    EXP036 / "run.py": "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    EXP037 / "run.py": "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
    EXP053 / "extract_training.py": "cd1ff29b95944224a4d05265ce175926fcf60c08b34c4d4bff8b5884b729fc90",
    EXP063 / "run.py": "97a9e7511ff9d004b091f244df653f02182e1d9304c9042fefe47ce241a89461",
    EXP042 / "artifacts" / "matrix-p11.json": "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
}
MASK58 = {"R1", "R3", "R4", "R5"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


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


def source_label(p: int, r: int) -> list[object]:
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    exterior = sorted((low - {p - r, 3 * p, 3 * p + r}) | {6 * p, 10 * p})
    return ["S", exterior, p - 2]


def target_label(p: int, r: int) -> list[object]:
    exterior = list(source_label(p, r)[1])
    exterior.remove(10 * p)
    return ["K", exterior, 11 * p - 2]


def classify_source(p: int, r: int, modules: dict[str, ModuleType], label=None) -> dict[str, object]:
    label = source_label(p, r) if label is None else label
    exterior = tuple(int(value) for value in label[1])
    coefficient = int(label[2])
    low = modules["exp036"].low_offsets(p)
    degree_two = modules["exp036"].degree_two_offsets(p)
    reverse_alias = {atom: alias for alias, atom in modules["exp048"].ATOM_ALIASES.items()}
    boundary = []
    for variable, sign, face in modules["exp037"].signed_faces(exterior):
        atom = None
        row = None
        if variable in low:
            product = modules["exp036"].low_product(p, variable, coefficient)
            if product is not None:
                atom = modules["exp042"].semantic_atom(
                    side="row", kind="D", coefficient_tag=product[0], exterior=face, p=p
                )
                row = ["D", list(face), product[0], product[1]]
        elif variable + coefficient in degree_two:
            tag = modules["exp042"].interval_tag(
                variable + coefficient, modules["exp042"].degree_two_intervals(p)
            )
            atom = modules["exp042"].semantic_atom(
                side="row", kind="K", coefficient_tag=tag, exterior=face, p=p
            )
            row = ["K", list(face), variable + coefficient]
        if row is not None:
            boundary.append({
                "deleted": variable,
                "sign": int(sign),
                "row": row,
                "alias": reverse_alias.get(atom, "OTHER"),
                "atom": atom,
            })
    projected = [item for item in boundary if item["alias"] in MASK58]
    return {"source": label, "boundary": boundary, "projected": projected}


def check_formula(p: int, r: int, modules: dict[str, ModuleType]) -> dict[str, object]:
    record = classify_source(p, r, modules)
    expected = target_label(p, r)
    if [(item["row"], item["sign"]) for item in record["projected"]] != [(expected, -1)]:
        raise AssertionError({"p": p, "r": r, "projection": record["projected"]})
    counts = Counter(item["alias"] for item in record["boundary"])
    expected_counts = Counter({"R0": p - 3, "R2": p - 3, "R5": 1})
    if counts != expected_counts:
        raise AssertionError({"p": p, "r": r, "counts": counts, "expected": expected_counts})
    if len(record["source"][1]) != 2 * p - 2:
        raise AssertionError({"p": p, "r": r, "source_size": len(record["source"][1])})
    if modules["exp063"].triangle_label(p, (0, r, p - 2 - r)) != expected:
        raise AssertionError({"p": p, "r": r, "triangle_label": False})
    return {
        "r": r,
        "source_hash": digest(record["source"]),
        "boundary_hash": digest(record["boundary"]),
        "counts": dict(sorted(counts.items())),
        "projected": record["projected"],
    }


def check_mutations(p: int, r: int, modules: dict[str, ModuleType]) -> int:
    expected = [(target_label(p, r), -1)]
    source = source_label(p, r)
    exterior = set(int(value) for value in source[1])
    mutations = []
    for removed, replacement in ((p - r, p - r - 1), (3 * p + r, 3 * p + r + 1)):
        changed = set(exterior)
        changed.add(removed)
        changed.discard(replacement)
        mutations.append(["S", sorted(changed), p - 2])
    changed = set(exterior)
    changed.remove(10 * p)
    changed.add(10 * p - 1)
    mutations.append(["S", sorted(changed), p - 2])
    rejected = 0
    for label in mutations:
        actual = classify_source(p, r, modules, label)
        if [(item["row"], item["sign"]) for item in actual["projected"]] == expected:
            raise AssertionError({"p": p, "r": r, "mutation_not_rejected": label})
        rejected += 1
    original = classify_source(p, r, modules)
    expanded = [item for item in original["boundary"] if item["alias"] in MASK58 | {"R0"}]
    if [(item["row"], item["sign"]) for item in expanded] == expected:
        raise AssertionError("R0 retention mutation not rejected")
    rejected += 1
    expanded = [item for item in original["boundary"] if item["alias"] in MASK58 | {"R2"}]
    if [(item["row"], item["sign"]) for item in expanded] == expected:
        raise AssertionError("R2 retention mutation not rejected")
    return rejected + 1


def holdout(modules: dict[str, ModuleType], seconds: float, memory_gib: float) -> dict[str, object]:
    p = 11
    budget = modules["exp048"].Budget(seconds, memory_gib)
    model = modules["exp053"].make_component_model(
        exp036=modules["exp036"], exp037=modules["exp037"], exp042=modules["exp042"],
        exp048=modules["exp048"], p=p, budget=budget,
    )
    if not model["unique_mapping"]:
        raise AssertionError({"p": p, "unique_mapping": False})
    labels = model["model"]["column_labels"]
    row_labels = model["labelled"]["row_labels"]
    row_atoms = model["labelled"]["row_atoms"]
    selected = set(modules["exp048"].rows_for_mask(row_atoms, 58))
    frozen_columns = model["frozen"]["signed_columns"]
    records = []
    for r in (1, 2):
        source = source_label(p, r)
        matches = [index for index, label in enumerate(labels) if label == source]
        if len(matches) != 1:
            raise AssertionError({"p": p, "r": r, "source_matches": matches})
        column = matches[0]
        projected = [(int(row), int(value)) for row, value in frozen_columns[column] if int(row) in selected]
        expected_row_matches = [index for index, label in enumerate(row_labels) if label == target_label(p, r)]
        if len(expected_row_matches) != 1 or projected != [(expected_row_matches[0], -1)]:
            raise AssertionError({"p": p, "r": r, "contracted_projection": projected})
        direct = check_formula(p, r, modules)
        records.append({
            "r": r, "component_column": column, "component_row": expected_row_matches[0],
            "contracted_projection": projected, "direct_boundary_hash": direct["boundary_hash"],
        })
    return {"p": p, "status": "HOLDOUT_PASS", "records": records}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-max", type=int, default=300)
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    parser.add_argument("--memory-gib", type=float, default=2.0)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=CHECKPOINT)
    args = parser.parse_args()
    if not 11 <= args.p_max <= 300:
        raise ValueError("frozen sweep requires 11 <= p-max <= 300")
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PREMISES}
    expected = {str(path.relative_to(EXPERIMENTS)): value for path, value in PREMISES.items()}
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    modules = {
        "exp036": load_module("exp036_for_exp066", EXP036 / "run.py"),
        "exp037": load_module("exp037_for_exp066", EXP037 / "run.py"),
        "exp042": load_module("exp042_for_exp066", EXP042 / "run.py"),
        "exp048": load_module("exp048_for_exp066", EXP048 / "run.py"),
        "exp053": load_module("exp053_for_exp066", EXP053 / "extract_training.py"),
        "exp063": load_module("exp063_for_exp066", EXP063 / "run.py"),
    }
    result = {"experiment": "EXP-066", "premises": actual, "holdout": None, "sweep": []}
    print("p=11 locked holdout: reconstruct labelled component", flush=True)
    result["holdout"] = holdout(modules, args.budget_seconds, args.memory_gib)
    write_json_atomic(args.checkpoint, result)
    mutation_count = 0
    for p in range(8, args.p_max + 1):
        row = {"p": p, "endpoints": [check_formula(p, r, modules) for r in (1, 2)]}
        mutation_count += sum(check_mutations(p, r, modules) for r in (1, 2))
        result["sweep"].append(row)
        if p == 8 or p % 25 == 0 or p == args.p_max:
            print(f"symbolic-regression p={p} PASS", flush=True)
            write_json_atomic(args.checkpoint, result)
    result.update({
        "status": "PASS", "parameters": [8, args.p_max],
        "endpoint_checks": 2 * (args.p_max - 7), "mutations_rejected": mutation_count,
        "symbolic_case_counts": {"R0": "p-3", "R2": "p-3", "R5": "1"},
        "uniform_identity": "Pi_58 d(s_(p,r)) = -x_(0,r,p-2-r), p>=8, r=1,2",
    })
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps({key: result[key] for key in ("status", "endpoint_checks", "mutations_rejected", "artifact_hash")}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
