"""Independent finite audit for EXP-063."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP036 = EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy"
EXP037 = EXPERIMENTS / "EXP-037-connecting-quasipolynomial"
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP048 = EXPERIMENTS / "EXP-048-semantic-relative-bockstein"
EXP062 = EXPERIMENTS / "EXP-062-triangle-torsion-family"
RESULTS = HERE / "artifacts" / "results.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit-results.json"
MASKS = (56, 58, 59, 62)
PINS = {
    HERE / "hypothesis.md": "d3a35db2d20ccf2ac7e54e223e929919faa9295ddf324c9d938c9cba336af0ba",
    HERE / "run.py": "97a9e7511ff9d004b091f244df653f02182e1d9304c9042fefe47ce241a89461",
    RESULTS: "c219ce4c4549d970063a787227793bb5f7141e8f4d6e14c614f62085ecc8059a",
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
    EXP062 / "artifacts" / "results.json":
        "09aef05e577e58b11c4ccc363ed47ccf1ed1598deb1b156a33bb3b6e49ae638d",
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


def all_triangles(p: int) -> list[tuple[int, int, int]]:
    values: list[tuple[int, int, int]] = []
    for a in range(p - 1):
        for b in range(a + 1, p - 1):
            c = p - 2 - a - b
            if b < c:
                values.append((a, b, c))
    return values


def exact_x_label(p: int, value: tuple[int, int, int]) -> list[object]:
    a, b, _ = value
    exterior = set(range(1, p + 1))
    exterior.update(range(3 * p, 4 * p - 1))
    exterior.remove(p - a - b)
    exterior.remove(3 * p + a)
    exterior.remove(3 * p + b)
    exterior.add(6 * p)
    return ["K", sorted(exterior), 11 * p - 2]


def high_basis(vectors: list[int]) -> dict[int, int]:
    basis: dict[int, int] = {}
    for raw in reversed(vectors):
        value = raw
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return basis


def in_span(value: int, basis: dict[int, int]) -> bool:
    while value:
        pivot = value.bit_length() - 1
        if pivot not in basis:
            return False
        value ^= basis[pivot]
    return True


def low_canonical(vectors: list[int]) -> list[int]:
    basis: dict[int, int] = {}
    for raw in vectors:
        value = raw
        while value:
            pivot = (value & -value).bit_length() - 1
            if pivot not in basis:
                for other in list(basis):
                    if (basis[other] >> pivot) & 1:
                        basis[other] ^= value
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return [basis[pivot] for pivot in sorted(basis)]


def signed_hash(columns: list[list[list[int]]]) -> str:
    hasher = hashlib.sha256()
    for entries in columns:
        hasher.update(json.dumps([(int(row), int(value)) for row, value in entries]).encode())
    return hasher.hexdigest()


def projected_vectors(
    frozen: dict[str, object], selected_rows: list[int], triangle_rows: list[int]
) -> tuple[list[int], list[int]]:
    positions = {row: index for index, row in enumerate(selected_rows)}
    columns: list[int] = []
    for entries in frozen["signed_columns"]:
        vector = 0
        for row, coefficient in entries:
            row = int(row)
            if row in positions and int(coefficient) % 2:
                vector ^= 1 << positions[row]
        columns.append(vector)
    return columns, [1 << positions[row] for row in triangle_rows]


def brute_relation_space(columns: list[int], triangle_vectors: list[int]) -> tuple[int, list[int]]:
    image = high_basis(columns)
    relations: list[int] = []
    for subset in range(1, 1 << len(triangle_vectors)):
        value = 0
        for index, vector in enumerate(triangle_vectors):
            if (subset >> index) & 1:
                value ^= vector
        if in_span(value, image):
            relations.append(subset)
    kernel_basis = low_canonical(relations)
    return len(triangle_vectors) - len(kernel_basis), kernel_basis


def producer_integrity(results: dict[str, object]) -> None:
    stored = results["artifact_hash"]
    unsigned = dict(results)
    del unsigned["artifact_hash"]
    if digest(unsigned) != stored:
        raise AssertionError("producer artifact self-hash mismatch")


def source_boundary_labels() -> dict[int, set[str]]:
    payload = json.loads(
        (EXP062 / "artifacts" / "results.json").read_text(encoding="utf-8")
    )
    result: dict[int, set[str]] = {}
    for row in payload["rows"]:
        p = int(row["p"])
        if p > 11:
            continue
        labels: set[str] = set()
        for item in row["triangles"]:
            boundary = item["full_boundary"]
            if len(boundary) != 1 or abs(int(boundary[0]["coefficient"])) != 2:
                raise AssertionError({"p": p, "EXP062_boundary": False})
            labels.add(json.dumps(boundary[0]["exact_label"], separators=(",", ":")))
        result[p] = labels
    return result


def audit_parameter(
    *, producer_row: dict[str, object], exp036: ModuleType, exp037: ModuleType,
    exp042: ModuleType, exp048: ModuleType, budget: object,
    source_labels: dict[int, set[str]],
) -> dict[str, object]:
    p = int(producer_row["p"])
    component = exp048.reconstruct_labelled_component(
        exp036=exp036, exp037=exp037, exp042=exp042, p=p, budget=budget
    )
    frozen_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    if signed_hash(frozen["signed_columns"]) != frozen["signed_hash"]:
        raise AssertionError({"p": p, "independent_signed_hash": False})

    names = all_triangles(p)
    labels = [exact_x_label(p, triangle) for triangle in names]
    component_keys = {
        json.dumps(label, separators=(",", ":")): index
        for index, label in enumerate(component["row_labels"])
    }
    label_keys = [json.dumps(label, separators=(",", ":")) for label in labels]
    if set(label_keys) != source_labels[p]:
        raise AssertionError({"p": p, "EXP062_label_set": False})
    triangle_rows = [component_keys[key] for key in label_keys]
    if triangle_rows != producer_row["triangle_rows"]:
        raise AssertionError({"p": p, "producer_triangle_rows": False})

    mask_records: list[dict[str, object]] = []
    for producer_mask in producer_row["masks"]:
        mask = int(producer_mask["mask"])
        selected = exp048.rows_for_mask(component["row_atoms"], mask)
        columns, triangle_vectors = projected_vectors(frozen, selected, triangle_rows)
        rank, relations = brute_relation_space(columns, triangle_vectors)
        producer_relations = [int(item["bits_hex"], 16) for item in producer_mask["relations"]]
        if rank != producer_mask["triangle_span_rank"] or relations != producer_relations:
            raise AssertionError({"p": p, "mask": mask, "independent_relation_space": False})
        mask_records.append(
            {
                "mask": mask,
                "triangle_span_rank": rank,
                "relation_dimension": len(relations),
                "relation_subspace_hash": digest(relations),
                "agrees": True,
            }
        )

    full_selected = exp048.rows_for_mask(component["row_atoms"], 59)
    full_columns, full_triangles = projected_vectors(frozen, full_selected, triangle_rows)
    duplicate = list(full_triangles)
    duplicate[-1] = duplicate[0]
    duplicate_rank, _ = brute_relation_space(full_columns, duplicate)
    if duplicate_rank != len(full_triangles) - 1:
        raise AssertionError({"p": p, "duplicate_control": False})

    r5 = exp048.ATOM_ALIASES["R5"]
    nontriangle_rows = [
        row for row, atom in enumerate(component["row_atoms"])
        if atom == r5 and row not in set(triangle_rows)
    ]
    if not nontriangle_rows:
        raise AssertionError({"p": p, "nontriangle_control_available": False})
    nontriangle_key = json.dumps(component["row_labels"][nontriangle_rows[0]], separators=(",", ":"))
    if nontriangle_key in set(label_keys):
        raise AssertionError({"p": p, "nontriangle_control": False})

    mutated = [[list(entry) for entry in column] for column in frozen["signed_columns"]]
    first = next(column for column in mutated if column)
    first[0][1] = -int(first[0][1])
    if signed_hash(mutated) == frozen["signed_hash"]:
        raise AssertionError({"p": p, "sign_mutation_control": False})
    return {
        "p": p,
        "triangles": len(names),
        "source_boundary_labels_agree": True,
        "labelled_reconstruction_agrees": True,
        "masks": mask_records,
        "controls": {
            "duplicate_triangle_rejected": True,
            "duplicate_rank": duplicate_rank,
            "nontriangle_R5_rejected": True,
            "nontriangle_row": nontriangle_rows[0],
            "signed_entry_mutation_rejected": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget-seconds", type=float, default=900.0)
    parser.add_argument("--memory-gib", type=float, default=12.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PINS}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash for path, expected_hash in PINS.items()
    }
    if actual != expected:
        raise AssertionError({"pin_mismatch": {"actual": actual, "expected": expected}})

    producer = json.loads(RESULTS.read_text(encoding="utf-8"))
    producer_integrity(producer)
    exp036 = load_module("exp036_for_063_audit", EXP036 / "run.py")
    exp037 = load_module("exp037_for_063_audit", EXP037 / "run.py")
    exp042 = load_module("exp042_for_063_audit", EXP042 / "run.py")
    exp048 = load_module("exp048_for_063_audit", EXP048 / "run.py")
    budget = exp048.Budget(args.budget_seconds, args.memory_gib)
    sources = source_boundary_labels()
    started = time.monotonic()
    rows = []
    for producer_row in producer["rows"]:
        print(f"audit p={producer_row['p']} independent relation enumeration", flush=True)
        rows.append(
            audit_parameter(
                producer_row=producer_row, exp036=exp036, exp037=exp037,
                exp042=exp042, exp048=exp048, budget=budget, source_labels=sources,
            )
        )
        budget.check(f"p={producer_row['p']} audit")

    result = {
        "experiment": "EXP-063-audit",
        "status": "COMPLETE",
        "pins": actual,
        "producer_artifact_hash": producer["artifact_hash"],
        "checks": {
            "parameters": len(rows),
            "triangle_labels": sum(row["triangles"] for row in rows),
            "mask_relation_spaces": sum(len(row["masks"]) for row in rows),
            "mutation_controls": 3 * len(rows),
        },
        "rows": rows,
        "elapsed_seconds": time.monotonic() - started,
    }
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps({"status": result["status"], "checks": result["checks"],
                      "elapsed_seconds": result["elapsed_seconds"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
