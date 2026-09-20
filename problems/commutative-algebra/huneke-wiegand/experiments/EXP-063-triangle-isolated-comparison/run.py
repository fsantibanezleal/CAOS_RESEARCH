"""Exact finite comparison of EXP-062 triangle rows with the isolated component."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path
from types import ModuleType
from typing import Iterable


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP036 = EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy"
EXP037 = EXPERIMENTS / "EXP-037-connecting-quasipolynomial"
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP043 = EXPERIMENTS / "EXP-043-hadamard-rank-certificate"
EXP045 = EXPERIMENTS / "EXP-045-row-atom-carrier-lattice"
EXP048 = EXPERIMENTS / "EXP-048-semantic-relative-bockstein"
EXP062 = EXPERIMENTS / "EXP-062-triangle-torsion-family"

DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
MASKS = (56, 58, 59, 62)
EXPECTED_RANKS = {
    56: {8: 0, 9: 0, 10: 0, 11: 1},
    58: {8: 1, 9: 2, 10: 3, 11: 5},
    59: {8: 3, 9: 4, 10: 5, 11: 7},
    62: {8: 3, 9: 4, 10: 5, 11: 7},
}
PREMISES = {
    HERE / "hypothesis.md": "d3a35db2d20ccf2ac7e54e223e929919faa9295ddf324c9d938c9cba336af0ba",
    EXP036 / "run.py": "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    EXP037 / "run.py": "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP043 / "artifacts" / "results.json":
        "612d481eff7e00f5c5128d450a5eb05f79aacccb27bcd88c106dc0d5bf7426e6",
    EXP045 / "artifacts" / "results.json":
        "569220667e9d82f0806ea96cb8f60c49e94cb6317817170c39f2e574e619bcb8",
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
    EXP062 / "run.py": "019c34a9d1180b5cce3fc0d5bfb29db7ffd91c0b66d56eab9e042da7623f0d07",
    EXP062 / "hypothesis.md": "56663e362e4e26d16d8db30f6000a1761f8e3e5b1e380fc67d9a441c6c8cbeeb",
}
MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    11: "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
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


def verify_premises(p_min: int, p_max: int) -> dict[str, str]:
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    for p in range(p_min, p_max + 1):
        path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        if sha256(path) != MATRIX_SHA256[p]:
            raise AssertionError({"matrix_hash_mismatch": {"p": p, "actual": sha256(path)}})
    return actual


def triangles(p: int) -> list[tuple[int, int, int]]:
    n = p - 2
    return [
        (i, j, n - i - j)
        for i in range(n // 3 + 1)
        for j in range(i + 1, (n - i - 1) // 2 + 1)
    ]


def triangle_label(p: int, triangle: tuple[int, int, int]) -> list[object]:
    i, j, _ = triangle
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    exterior = sorted((low - {p - i - j, 3 * p + i, 3 * p + j}) | {6 * p})
    return ["K", exterior, 11 * p - 2]


def canonical_rref(vectors: Iterable[int], *, high: bool = False) -> list[int]:
    basis: dict[int, int] = {}
    for raw in vectors:
        vector = raw
        while vector:
            pivot = vector.bit_length() - 1 if high else (vector & -vector).bit_length() - 1
            existing = basis.get(pivot)
            if existing is None:
                for other in list(basis):
                    if (basis[other] >> pivot) & 1:
                        basis[other] ^= vector
                basis[pivot] = vector
                break
            vector ^= existing
    return [basis[pivot] for pivot in sorted(basis, reverse=high)]


def dependency_space(
    relation_columns: list[int], triangle_vectors: list[int], *, high: bool
) -> tuple[int, list[int]]:
    basis: dict[int, tuple[int, int]] = {}

    def pivot(vector: int) -> int:
        return vector.bit_length() - 1 if high else (vector & -vector).bit_length() - 1

    for raw in relation_columns:
        vector = raw
        while vector:
            position = pivot(vector)
            existing = basis.get(position)
            if existing is None:
                basis[position] = (vector, 0)
                break
            vector ^= existing[0]

    independent = 0
    relations: list[int] = []
    for index, raw in enumerate(triangle_vectors):
        vector = raw
        provenance = 1 << index
        while vector:
            position = pivot(vector)
            existing = basis.get(position)
            if existing is None:
                basis[position] = (vector, provenance)
                independent += 1
                break
            vector ^= existing[0]
            provenance ^= existing[1]
        if not vector:
            if not provenance:
                raise AssertionError("zero triangle dependency provenance")
            relations.append(provenance)
    return independent, canonical_rref(relations)


def bit_indices(value: int) -> list[int]:
    result: list[int] = []
    while value:
        least = value & -value
        result.append(least.bit_length() - 1)
        value ^= least
    return result


def frozen_carrier_rank(carriers: dict[int, dict[int, int]], p: int, mask: int) -> int:
    return carriers[p][mask]


def load_carrier_ranks() -> dict[int, dict[int, int]]:
    payload = json.loads((EXP045 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    result: dict[int, dict[int, int]] = {}
    for row in payload["rows"]:
        result[int(row["p"])] = {
            int(item["mask"]): int(item["bockstein_high_forward"]["bockstein_rank"])
            for item in row["subsets"]
        }
    return result


def verify_complete_torsion() -> dict[int, int]:
    payload = json.loads((EXP043 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    result: dict[int, int] = {}
    for row in payload["rows"]:
        p = int(row["p"])
        torsion_type = row["two_primary_type"]
        if not row["complete_two_primary_torsion"] or any(int(value) != 2 for value in torsion_type):
            raise AssertionError({"p": p, "complete_two_primary_torsion": False})
        result[p] = len(torsion_type)
    return result


def projected_record(
    *, p: int, mask: int, frozen: dict[str, object], component: dict[str, object],
    triangle_rows: list[int], triangle_names: list[tuple[int, int, int]],
    carrier_ranks: dict[int, dict[int, int]],
) -> dict[str, object]:
    selected_rows = component["rows_for_mask"](
        component["row_atoms"], mask
    ) if callable(component.get("rows_for_mask")) else []
    if not selected_rows:
        raise AssertionError("row-mask helper missing")
    row_position = {row: position for position, row in enumerate(selected_rows)}
    relation_columns = []
    for entries in frozen["signed_columns"]:
        value = 0
        for row, coefficient in entries:
            row = int(row)
            if row in row_position and int(coefficient) & 1:
                value ^= 1 << row_position[row]
        relation_columns.append(value)
    if any(row not in row_position for row in triangle_rows):
        raise AssertionError({"p": p, "mask": mask, "triangle_row_projected_out": True})
    triangle_vectors = [1 << row_position[row] for row in triangle_rows]
    low_rank, low_relations = dependency_space(relation_columns, triangle_vectors, high=False)
    high_rank, high_relations = dependency_space(relation_columns, triangle_vectors, high=True)
    if low_rank != high_rank or low_relations != high_relations:
        raise AssertionError({"p": p, "mask": mask, "pivot_order_disagreement": True})
    expected = EXPECTED_RANKS[mask][p]
    carrier = frozen_carrier_rank(carrier_ranks, p, mask)
    if low_rank != expected or carrier != expected:
        raise AssertionError(
            {"p": p, "mask": mask, "triangle_rank": low_rank,
             "carrier_rank": carrier, "expected": expected}
        )
    return {
        "mask": mask,
        "rows": len(selected_rows),
        "relation_columns": len(relation_columns),
        "rank_mod_two": len(canonical_rref(relation_columns)),
        "triangle_span_rank": low_rank,
        "frozen_carrier_bockstein_rank": carrier,
        "expected_rank": expected,
        "pivot_orders_agree": True,
        "relation_dimension": len(low_relations),
        "relations": [
            {
                "bits_hex": hex(relation),
                "triangles": [list(triangle_names[index]) for index in bit_indices(relation)],
            }
            for relation in low_relations
        ],
        "relation_subspace_hash": digest(low_relations),
    }


def parameter_record(
    *, p: int, exp036: ModuleType, exp037: ModuleType, exp042: ModuleType,
    exp048: ModuleType, budget: object, carrier_ranks: dict[int, dict[int, int]],
    complete_torsion: dict[int, int],
) -> dict[str, object]:
    component = exp048.reconstruct_labelled_component(
        exp036=exp036, exp037=exp037, exp042=exp042, p=p, budget=budget
    )
    frozen = json.loads((EXP042 / "artifacts" / f"matrix-p{p}.json").read_text(encoding="utf-8"))
    frozen_atoms = [frozen["row_atom_table"][index] for index in frozen["row_atom_ids"]]
    if component["row_atoms"] != frozen_atoms:
        raise AssertionError({"p": p, "row_atom_alignment": False})
    labels = component["row_labels"]
    label_index = {
        json.dumps(label, separators=(",", ":")): index for index, label in enumerate(labels)
    }
    if len(label_index) != len(labels):
        raise AssertionError({"p": p, "duplicate_component_labels": True})

    triangle_names = triangles(p)
    triangle_labels = [triangle_label(p, triangle) for triangle in triangle_names]
    missing = [
        list(triangle) for triangle, label in zip(triangle_names, triangle_labels, strict=True)
        if json.dumps(label, separators=(",", ":")) not in label_index
    ]
    if missing:
        raise AssertionError({"p": p, "missing_triangle_rows": missing})
    triangle_rows = [
        label_index[json.dumps(label, separators=(",", ":"))] for label in triangle_labels
    ]
    r5 = exp048.ATOM_ALIASES["R5"]
    if any(component["row_atoms"][row] != r5 for row in triangle_rows):
        raise AssertionError({"p": p, "non_R5_triangle": True})
    if len(set(triangle_rows)) != len(triangle_rows):
        raise AssertionError({"p": p, "duplicate_triangle_rows": True})

    component_with_helper = dict(component)
    component_with_helper["rows_for_mask"] = exp048.rows_for_mask
    masks = [
        projected_record(
            p=p, mask=mask, frozen=frozen, component=component_with_helper,
            triangle_rows=triangle_rows, triangle_names=triangle_names,
            carrier_ranks=carrier_ranks,
        )
        for mask in MASKS
    ]
    q = len(triangle_names)
    if q != complete_torsion[p] or q != EXPECTED_RANKS[59][p]:
        raise AssertionError({"p": p, "triangle_count": q, "complete_torsion": complete_torsion[p]})
    contraction_replay = {
        "reconstruction_source_sha256": sha256(EXP048 / "run.py"),
        "support_hash": frozen["support_hash"],
        "signed_hash": frozen["signed_hash"],
        "signed_columns_hash": component["signed_columns_hash"],
        "surviving_row_labels_hash": digest(labels),
        "triangle_rows": triangle_rows,
    }
    return {
        "p": p,
        "triangle_count": q,
        "triangles": [list(value) for value in triangle_names],
        "triangle_rows": triangle_rows,
        "triangle_labels": triangle_labels,
        "all_rows_survive": True,
        "all_atoms_R5": True,
        "literal_surviving_coordinates": True,
        "component_rows": component["rows"],
        "component_columns": component["columns"],
        "contraction_replay": contraction_replay,
        "contraction_replay_hash": digest(contraction_replay),
        "masks": masks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=900.0)
    parser.add_argument("--memory-gib", type=float, default=12.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()
    if not (8 <= args.p_min <= args.p_max <= 11):
        raise ValueError("EXP-063 is frozen to 8 <= p_min <= p_max <= 11")

    started = time.monotonic()
    premise_hashes = verify_premises(args.p_min, args.p_max)
    exp036 = load_module("exp036_for_063", EXP036 / "run.py")
    exp037 = load_module("exp037_for_063", EXP037 / "run.py")
    exp042 = load_module("exp042_for_063", EXP042 / "run.py")
    exp048 = load_module("exp048_for_063", EXP048 / "run.py")
    budget = exp048.Budget(args.budget_seconds, args.memory_gib)
    carrier_ranks = load_carrier_ranks()
    complete_torsion = verify_complete_torsion()
    rows: list[dict[str, object]] = []
    for p in range(args.p_min, args.p_max + 1):
        print(f"p={p} replay labelled contraction and compare triangles", flush=True)
        rows.append(
            parameter_record(
                p=p, exp036=exp036, exp037=exp037, exp042=exp042,
                exp048=exp048, budget=budget, carrier_ranks=carrier_ranks,
                complete_torsion=complete_torsion,
            )
        )
        checkpoint = {
            "experiment": "EXP-063",
            "status": "PARTIAL",
            "p_min": args.p_min,
            "p_max": args.p_max,
            "completed": [row["p"] for row in rows],
            "rows": rows,
            "elapsed_seconds": time.monotonic() - started,
        }
        write_json_atomic(args.checkpoint, checkpoint)
        budget.check(f"p={p} checkpoint")

    p1 = all(row["all_rows_survive"] and row["all_atoms_R5"] for row in rows)
    p2 = all(
        next(item for item in row["masks"] if item["mask"] == mask)["triangle_span_rank"]
        == row["triangle_count"]
        for row in rows for mask in (59, 62)
    )
    p3 = all(
        item["triangle_span_rank"] == EXPECTED_RANKS[item["mask"]][row["p"]]
        for row in rows for item in row["masks"]
    )
    result = {
        "experiment": "EXP-063",
        "status": "COMPLETE",
        "scope": {"p_min": args.p_min, "p_max": args.p_max},
        "premise_hashes": premise_hashes,
        "resource_caps": {
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
            "processes": 1,
        },
        "claims": {"P1": p1, "P2": p2, "P3": p3},
        "rows": rows,
        "elapsed_seconds": time.monotonic() - started,
    }
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps({"status": result["status"], "claims": result["claims"],
                      "elapsed_seconds": result["elapsed_seconds"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
