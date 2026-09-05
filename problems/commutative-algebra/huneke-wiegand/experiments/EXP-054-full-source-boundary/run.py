"""Exact original differential audit, CPU only; no basis enumeration or HNF."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
SOURCE = EXPERIMENTS / "EXP-053-labelled-source-pullback/artifacts/training-p8-p10.json"
TARGET = EXPERIMENTS / "EXP-052-semantic-unreduced-lifts/artifacts/training-p8-p10.json"
PREMISES = {
    SOURCE: "0d6bb8b885d965ed91a94d06a072d8baacca56df65903e10e1c91382f649edfe",
    TARGET: "259ff476b7bb09c12566e4bd771da5c88af17f541cc5732db4dc7f2067e2ec70",
    EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy/run.py":
        "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    EXPERIMENTS / "EXP-052-semantic-unreduced-lifts/candidate.py":
        "6a16d8cf2c112a800558d634f6cd058ea00be43986c7b92f7f9406a6d282ca0c",
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def row_key(label: list) -> tuple:
    return (label[0], tuple(label[1]), *label[2:])


def records(vector: dict) -> list:
    return [
        {"coefficient": value, "exact_label": [key[0], list(key[1]), *key[2:]]}
        for key, value in sorted(vector.items()) if value
    ]


def multiply(p: int, support: list, algebra) -> Counter:
    result = Counter()
    low = algebra.low_offsets(p)
    high = algebra.high_offsets(p)
    degree_two = algebra.degree_two_offsets(p)
    generators = low | high
    for term in support:
        kind, exterior, coefficient = term["exact_label"]
        assert exterior == sorted(set(exterior))
        assert set(exterior) <= generators
        assert len(exterior) == 2 * p - 2
        assert sum(exterior) + coefficient == 4 * p * p + 6 * p - 1
        assert coefficient in (low if kind == "S" else high)
        for position, variable in enumerate(exterior):
            face = tuple(exterior[:position] + exterior[position + 1:])
            value = term["coefficient"] * (-1 if position % 2 else 1)
            if kind == "S" and variable in low:
                product = algebra.low_product(p, variable, coefficient)
                if product is not None:
                    result[("D", face, *product)] += value
            elif variable + coefficient in degree_two:
                result[("K", face, variable + coefficient)] += value
    return Counter({key: value for key, value in result.items() if value})


def expected_boundary(training: dict) -> Counter:
    result = Counter()
    for inclusion in training["inclusions"]:
        for row in inclusion["semantic_rows"]:
            result[row_key(row["exact_label"])] += 2 * row["coefficient"]
    return result


def projected_check(source_row: dict, target_row: dict) -> dict:
    p = source_row["p"]
    path = EXPERIMENTS / f"EXP-042-bockstein-normal-form/artifacts/matrix-p{p}.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source_row["matrix_sha256"]
    matrix = json.loads(path.read_text())
    actual = [0] * matrix["rows"]
    for term in source_row["inclusions"][0]["source_support"]:
        for row, value in matrix["signed_columns"][term["matrix_column"]]:
            actual[row] += term["coefficient"] * value
    expected = [0] * matrix["rows"]
    atoms = [matrix["row_atom_table"][index] for index in matrix["row_atom_ids"]]
    for inclusion in target_row["inclusions"]:
        tag = "A" if inclusion["target_mask"] == 59 else "B"
        pattern = [-2, -3, 1, 0, 1, 0, 0, 0, 0, 0] if tag == "A" else [-1, -4, 1, 0, 1, 0, 0, 0, 0, 0]
        wanted = json.dumps(["row", "D", tag, pattern], separators=(",", ":"))
        added = [index for index, atom in enumerate(atoms) if atom == wanted]
        for term in inclusion["semantic_rows"]:
            expected[added[term["projected_row"]]] += 2 * term["coefficient"]
    assert actual == expected
    return {"all_component_rows_checked": len(actual), "identity": True,
            "boundary_hash": digest(actual), "matrix_sha256": source_row["matrix_sha256"]}


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def run(output: Path, budget_seconds: float = 60) -> dict:
    started = time.monotonic()
    for path, expected in PREMISES.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path
    algebra = load_module("exp036_for_054", EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy/run.py")
    candidate = load_module("candidate_054", EXPERIMENTS / "EXP-052-semantic-unreduced-lifts/candidate.py")
    source = json.loads(SOURCE.read_text())
    target = json.loads(TARGET.read_text())
    result = {"experiment": "EXP-054", "status": "CHECKPOINT", "p11_source_accessed": False,
              "premises": {path.relative_to(EXPERIMENTS).as_posix(): value for path, value in PREMISES.items()},
              "rows": []}
    for source_row, target_row in zip(source["rows"], target["rows"], strict=True):
        p = source_row["p"]
        assert p == target_row["p"] and p in (8, 9, 10)
        first, second = source_row["inclusions"]
        assert first["source_support"] == second["source_support"]
        for inclusion in target_row["inclusions"]:
            frozen = candidate.canonical([[term["coefficient"], term["token"]]
                                          for term in inclusion["semantic_rows"]])
            assert frozen == candidate.candidate(p, 58, inclusion["target_mask"])
        actual = multiply(p, first["source_support"], algebra)
        expected = expected_boundary(target_row)
        residual = actual.copy()
        residual.subtract(expected)
        residual = Counter({key: value for key, value in residual.items() if value})
        row = {"p": p, "source_support": len(first["source_support"]),
               "same_source": True, "projected_regression": projected_check(source_row, target_row),
               "full_identity": not residual, "boundary_support": len(actual),
               "expected_support": len(expected), "residual_support": len(residual),
               "residual_odd_coefficients": sum(value % 2 != 0 for value in residual.values()),
               "residual_kinds": dict(Counter(key[0] for key in residual)),
               "boundary": records(actual), "expected_boundary": records(expected),
               "residual": records(residual)}
        row["row_hash"] = digest(row)
        result["rows"].append(row)
        write_json(output, result)
        print(f"p={p}: component identity PASS; full residual {len(residual)} rows", flush=True)
        if time.monotonic() - started > budget_seconds:
            raise RuntimeError("EXP-054 budget exhausted; checkpoint retained")
    assert [row["p"] for row in result["rows"]] == [8, 9, 10]
    result["p1_status"] = "PASS_FINITE" if all(row["full_identity"] for row in result["rows"]) else "REFUTED"
    result["p2_status"] = "PASS_FINITE"
    result["status"] = "COMPLETE"
    result["artifact_hash"] = digest(result)
    write_json(output, result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--budget-seconds", type=float, default=60)
    args = parser.parse_args()
    run(args.output, args.budget_seconds)
