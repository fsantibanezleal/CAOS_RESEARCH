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
EXP063 = EXPERIMENTS / "EXP-063-triangle-isolated-comparison"
OUTPUT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
PREMISES = {
    EXP036 / "run.py": "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    EXP037 / "run.py": "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
    EXP063 / "run.py": "97a9e7511ff9d004b091f244df653f02182e1d9304c9042fefe47ce241a89461",
    EXP063 / "artifacts" / "results.json": "c219ce4c4549d970063a787227793bb5f7141e8f4d6e14c614f62085ecc8059a",
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
    intervals = modules["exp042"].generator_intervals(p)
    tags = modules["exp042"].GENERATOR_TAGS
    exterior_tags = {value: modules["exp042"].interval_tag(value, intervals) for value in exterior}
    source_counts = Counter(exterior_tags.values())

    def face_atom(kind: str, coefficient_tag: str, deleted: int) -> str:
        face_counts = source_counts.copy()
        face_counts[exterior_tags[deleted]] -= 1
        normalized = [face_counts[tag] for tag in tags]
        normalized[0] -= p
        normalized[1] -= p
        return json.dumps(["row", kind, coefficient_tag, normalized], separators=(",", ":"))

    boundary = []
    for position, variable in enumerate(exterior):
        sign = -1 if position % 2 else 1
        atom = None
        row_kind = None
        coefficient_tag = None
        product_value = None
        if variable in low:
            product = modules["exp036"].low_product(p, variable, coefficient)
            if product is not None:
                row_kind, coefficient_tag, product_value = "D", product[0], product[1]
                atom = face_atom(row_kind, coefficient_tag, variable)
        elif variable + coefficient in degree_two:
            coefficient_tag = modules["exp042"].interval_tag(
                variable + coefficient, modules["exp042"].degree_two_intervals(p)
            )
            row_kind, product_value = "K", variable + coefficient
            atom = face_atom(row_kind, coefficient_tag, variable)
        if row_kind is not None:
            alias = reverse_alias.get(atom, "OTHER")
            row = None
            if alias in MASK58:
                face = exterior[:position] + exterior[position + 1:]
                row = (["D", list(face), coefficient_tag, product_value] if row_kind == "D"
                       else ["K", list(face), product_value])
            boundary.append({
                "deleted": variable,
                "sign": int(sign),
                "row": row,
                "kind": row_kind,
                "coefficient_tag": coefficient_tag,
                "product": product_value,
                "alias": alias,
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
    # 10p-1 is a degree-two singleton, not a degree-one generator.  Use the
    # nearest admissible degree-one neighbour specified by the control's
    # "where admissible" qualifier.
    changed.add(10 * p - 2)
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


def holdout(modules: dict[str, ModuleType]) -> dict[str, object]:
    p = 11
    frozen = json.loads((EXP042 / "artifacts" / "matrix-p11.json").read_text(encoding="utf-8"))
    comparison = json.loads((EXP063 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    p11 = next(row for row in comparison["rows"] if int(row["p"]) == p)
    column_atom = '["column","S","L0",[-1,-3,1,0,1,0,0,0,0,0]]'
    column_atom_id = frozen["column_atom_table"].index(column_atom)
    row_aliases = {
        row: next(alias for alias, atom in modules["exp048"].ATOM_ALIASES.items() if atom == frozen["row_atom_table"][atom_id])
        for row, atom_id in enumerate(frozen["row_atom_ids"])
    }
    records = []
    for r in (1, 2):
        triangle = [0, r, p - 2 - r]
        position = p11["triangles"].index(triangle)
        target_row = int(p11["triangle_rows"][position])
        if p11["triangle_labels"][position] != target_label(p, r):
            raise AssertionError({"p": p, "r": r, "target_label": False})
        candidates = []
        for column, (atom_id, entries) in enumerate(zip(frozen["column_atom_ids"], frozen["signed_columns"], strict=True)):
            if atom_id != column_atom_id:
                continue
            aliases = Counter(row_aliases[int(row)] for row, _ in entries)
            r5_entries = [(int(row), int(value)) for row, value in entries if row_aliases[int(row)] == "R5"]
            if aliases == Counter({"R0": p - 3, "R2": p - 3, "R5": 1}) and r5_entries == [(target_row, -1)]:
                candidates.append(column)
        if len(candidates) != 1:
            raise AssertionError({"p": p, "r": r, "semantic_candidates": candidates})
        column = candidates[0]
        projected = [(int(row), int(value)) for row, value in frozen["signed_columns"][column] if row_aliases[int(row)] in MASK58]
        if projected != [(target_row, -1)]:
            raise AssertionError({"p": p, "r": r, "contracted_projection": projected})
        direct = check_formula(p, r, modules)
        records.append({
            "r": r, "component_column": column, "component_row": target_row,
            "contracted_projection": projected, "direct_boundary_hash": direct["boundary_hash"],
            "source_recovered_from_target_face": source_label(p, r),
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
        "exp063": load_module("exp063_for_exp066", EXP063 / "run.py"),
    }
    result = {"experiment": "EXP-066", "premises": actual, "holdout": None, "sweep": []}
    print("p=11 locked holdout: reconstruct labelled component", flush=True)
    result["holdout"] = holdout(modules)
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
