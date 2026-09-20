"""Independent audit for EXP-066; does not import the producer."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP036 = EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy"
EXP037 = EXPERIMENTS / "EXP-037-connecting-quasipolynomial"
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP048 = EXPERIMENTS / "EXP-048-semantic-relative-bockstein"
EXP053 = EXPERIMENTS / "EXP-053-labelled-source-pullback"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-results.json"
RUN_SHA256 = "9780eaa178f5360f77b10cc16acfaa45c2e56c098dfc275d4b59a21dc84175bf"
ALIASES = {
    ("D", "A", (-2, -3, 1, 0, 1, 0, 0, 0, 0, 0)): "R0",
    ("D", "A", (-3, -2, 2, 0, 0, 0, 0, 0, 0, 0)): "R1",
    ("D", "B", (-1, -4, 1, 0, 1, 0, 0, 0, 0, 0)): "R2",
    ("D", "B", (-2, -3, 2, 0, 0, 0, 0, 0, 0, 0)): "R3",
    ("K", "C0", (-2, -2, 1, 0, 0, 0, 0, 0, 0, 0)): "R4",
    ("K", "C2", (-1, -3, 1, 0, 0, 0, 0, 0, 0, 0)): "R5",
}
KEEP = {"R1", "R3", "R4", "R5"}


def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generator_tag(p: int, value: int) -> str:
    intervals = (
        ("L0", 1, p), ("L1", 3 * p, 4 * p - 2), ("H0", 6 * p, 8 * p - 2),
        ("H1", 8 * p, 10 * p - 2), ("H2", 10 * p, 10 * p),
        ("H3", 11 * p - 1, 12 * p - 1), ("H4", 13 * p + 1, 14 * p - 2),
        ("H5", 14 * p, 15 * p - 1), ("H6", 16 * p, 16 * p),
        ("H7", 17 * p - 1, 18 * p - 1),
    )
    matches = [tag for tag, first, last in intervals if first <= value <= last]
    if len(matches) != 1:
        raise AssertionError({"generator": value, "matches": matches})
    return matches[0]


def degree_two_tag(p: int, value: int) -> str | None:
    intervals = (
        ("C0", 8 * p - 1, 8 * p - 1), ("C1", 10 * p - 1, 10 * p - 1),
        ("C2", 10 * p + 1, 11 * p - 2), ("C3", 12 * p, 13 * p),
        ("C4", 14 * p - 1, 14 * p - 1), ("C5", 15 * p, 16 * p - 1),
        ("C6", 16 * p + 1, 17 * p - 2), ("C7", 18 * p, 24 * p - 1),
    )
    matches = [tag for tag, first, last in intervals if first <= value <= last]
    if len(matches) > 1:
        raise AssertionError({"degree_two": value, "matches": matches})
    return matches[0] if matches else None


def counts(p: int, exterior: tuple[int, ...]) -> tuple[int, ...]:
    order = ("L0", "L1", "H0", "H1", "H2", "H3", "H4", "H5", "H6", "H7")
    counted = Counter(generator_tag(p, value) for value in exterior)
    result = [counted[tag] for tag in order]
    result[0] -= p
    result[1] -= p
    return tuple(result)


def source(p: int, r: int) -> tuple[int, ...]:
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    return tuple(sorted((low - {p - r, 3 * p, 3 * p + r}) | {6 * p, 10 * p}))


def target(p: int, r: int) -> list[object]:
    exterior = list(source(p, r))
    exterior.remove(10 * p)
    return ["K", exterior, 11 * p - 2]


def boundary(p: int, exterior: tuple[int, ...]) -> list[dict[str, object]]:
    coefficient = p - 2
    result = []
    for position, variable in enumerate(exterior):
        face = exterior[:position] + exterior[position + 1:]
        sign = -1 if position % 2 else 1
        kind = None
        coefficient_tag = None
        row = None
        if 1 <= variable <= p or 3 * p <= variable <= 4 * p - 2:
            second = variable >= 3 * p
            total = variable + coefficient
            if (not second and total > p) or (second and total >= 4 * p - 1):
                kind, coefficient_tag = "D", "B" if second else "A"
                row = ["D", list(face), coefficient_tag, total]
        else:
            coefficient_tag = degree_two_tag(p, variable + coefficient)
            if coefficient_tag is not None:
                kind = "K"
                row = ["K", list(face), variable + coefficient]
        if row is not None:
            atom_key = (kind, coefficient_tag, counts(p, face))
            result.append({
                "deleted": variable, "sign": sign, "row": row,
                "alias": ALIASES.get(atom_key, "OTHER"), "atom_key": atom_key,
            })
    return result


def audit_formula(p: int, r: int) -> dict[str, object]:
    exterior = source(p, r)
    rows = boundary(p, exterior)
    projected = [(item["row"], item["sign"]) for item in rows if item["alias"] in KEEP]
    expected = [(target(p, r), -1)]
    if projected != expected:
        raise AssertionError({"p": p, "r": r, "projected": projected})
    aliases = Counter(item["alias"] for item in rows)
    if aliases != Counter({"R0": p - 3, "R2": p - 3, "R5": 1}):
        raise AssertionError({"p": p, "r": r, "aliases": aliases})
    if exterior[-1] != 10 * p or len(exterior) != 2 * p - 2:
        raise AssertionError({"p": p, "r": r, "exterior_parity": False})
    return {"r": r, "boundary_hash": digest(rows), "aliases": dict(sorted(aliases.items()))}


def component_holdout(modules: dict[str, object], seconds: float, memory_gib: float):
    p = 11
    model = modules["exp053"].make_component_model(
        exp036=modules["exp036"], exp037=modules["exp037"], exp042=modules["exp042"],
        exp048=modules["exp048"], p=p, budget=modules["exp048"].Budget(seconds, memory_gib),
    )
    if not model["unique_mapping"]:
        raise AssertionError("nonunique p=11 source map")
    selected = set(modules["exp048"].rows_for_mask(model["labelled"]["row_atoms"], 58))
    records = []
    for r in (2, 1):
        exact_source = ["S", list(source(p, r)), p - 2]
        columns = [index for index, label in enumerate(model["model"]["column_labels"]) if label == exact_source]
        rows = [index for index, label in enumerate(model["labelled"]["row_labels"]) if label == target(p, r)]
        if len(columns) != 1 or len(rows) != 1:
            raise AssertionError({"r": r, "columns": columns, "rows": rows})
        projected = [(int(row), int(value)) for row, value in model["frozen"]["signed_columns"][columns[0]] if int(row) in selected]
        if projected != [(rows[0], -1)]:
            raise AssertionError({"r": r, "projected": projected})
        records.append({"r": r, "column": columns[0], "row": rows[0], "projected": projected})
    return sorted(records, key=lambda item: item["r"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    parser.add_argument("--memory-gib", type=float, default=2.0)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if hashlib.sha256((HERE / "run.py").read_bytes()).hexdigest() != RUN_SHA256:
        raise AssertionError("producer source hash changed")
    producer = json.loads(RESULTS.read_text(encoding="utf-8"))
    unsigned = dict(producer)
    stored = unsigned.pop("artifact_hash")
    if digest(unsigned) != stored or producer["status"] != "PASS":
        raise AssertionError("producer artifact invalid")
    modules = {
        "exp036": load("audit_exp036", EXP036 / "run.py"),
        "exp037": load("audit_exp037", EXP037 / "run.py"),
        "exp042": load("audit_exp042", EXP042 / "run.py"),
        "exp048": load("audit_exp048", EXP048 / "run.py"),
        "exp053": load("audit_exp053", EXP053 / "extract_training.py"),
    }
    holdout = component_holdout(modules, args.budget_seconds, args.memory_gib)
    checks = []
    for p in range(300, 7, -1):
        checks.extend({"p": p, **audit_formula(p, r)} for r in (2, 1))
    if len(checks) != producer["endpoint_checks"]:
        raise AssertionError("producer/auditor check count mismatch")
    result = {
        "experiment": "EXP-066 independent audit", "status": "INDEPENDENT_AUDIT_PASS",
        "producer_artifact_hash": stored, "holdout": holdout, "endpoint_checks": len(checks),
        "reverse_parameter_order": True, "formula_checks_hash": digest(checks),
    }
    result["artifact_hash"] = digest(result)
    write_json(args.output, result)
    print(json.dumps(result, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
