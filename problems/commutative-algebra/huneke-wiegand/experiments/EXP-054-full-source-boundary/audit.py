"""Independent integer differential audit for EXP-054; CPU only, no HNF."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
SOURCE = EXPERIMENTS / "EXP-053-labelled-source-pullback/artifacts/training-p8-p10.json"
TARGET = EXPERIMENTS / "EXP-052-semantic-unreduced-lifts/artifacts/training-p8-p10.json"
RESULTS = HERE / "artifacts/results.json"
PINNED = {
    SOURCE: "0d6bb8b885d965ed91a94d06a072d8baacca56df65903e10e1c91382f649edfe",
    TARGET: "259ff476b7bb09c12566e4bd771da5c88af17f541cc5732db4dc7f2067e2ec70",
    HERE / "run.py": "bb6c35f36da17d4e4045670348416a18d9cbb28bf5f5774fcf1deabf28ed951f",
    RESULTS: "2e8fad6fea215517a4007f9628e1f14e6c39918ed2920e9a4e7d62a6f229f36a",
}


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def degree_two_contains(p: int, value: int) -> bool:
    """Explicit gap intervals, independent of the producer's set subtraction."""
    return (
        value in (8 * p - 1, 10 * p - 1, 14 * p - 1)
        or 10 * p + 1 <= value <= 11 * p - 2
        or 12 * p <= value <= 13 * p
        or 15 * p <= value <= 16 * p - 1
        or 16 * p + 1 <= value <= 17 * p - 2
        or 18 * p <= value <= 24 * p - 1
    )


def low_kind(p: int, value: int) -> str | None:
    if 1 <= value <= p:
        return "L0"
    if 3 * p <= value <= 4 * p - 2:
        return "L1"
    return None


def high_contains(p: int, value: int) -> bool:
    return any(first <= value <= last for first, last in (
        (6 * p, 8 * p - 2), (8 * p, 10 * p - 2), (10 * p, 10 * p),
        (11 * p - 1, 12 * p - 1), (13 * p + 1, 14 * p - 2),
        (14 * p, 15 * p - 1), (16 * p, 16 * p), (17 * p - 1, 18 * p - 1),
    ))


def key(label: list) -> tuple:
    return label[0], tuple(label[1]), *label[2:]


def sparse(records: list) -> dict:
    result = {}
    for record in records:
        index = key(record["exact_label"])
        assert index not in result and record["coefficient"] != 0
        result[index] = record["coefficient"]
    return result


def records(vector: dict) -> list:
    return [{"coefficient": coefficient, "exact_label": [index[0], list(index[1]), *index[2:]]}
            for index, coefficient in sorted(vector.items()) if coefficient]


def independent_boundary(p: int, support: list) -> dict:
    """Right-to-left exterior differential with directly encoded product cases."""
    output = Counter()
    labels = set()
    for term in support:
        kind, exterior, coefficient = term["exact_label"]
        assert kind in ("S", "K")
        assert key(term["exact_label"]) not in labels
        labels.add(key(term["exact_label"]))
        assert exterior == sorted(set(exterior)) and len(exterior) == 2 * p - 2
        assert sum(exterior) + coefficient == 4 * p * p + 6 * p - 1
        assert all(low_kind(p, value) is not None or high_contains(p, value) for value in exterior)
        assert low_kind(p, coefficient) is not None if kind == "S" else high_contains(p, coefficient)
        sign = -1 if (len(exterior) - 1) % 2 else 1
        for position in range(len(exterior) - 1, -1, -1):
            variable = exterior[position]
            face = tuple(value for index, value in enumerate(exterior) if index != position)
            total = variable + coefficient
            variable_low = low_kind(p, variable)
            row = None
            if kind == "S" and variable_low is not None:
                coefficient_low = low_kind(p, coefficient)
                if variable_low == coefficient_low == "L0" and total > p:
                    row = ("D", face, "A", total)
                elif variable_low != coefficient_low and total >= 4 * p - 1:
                    row = ("D", face, "B", total)
            elif degree_two_contains(p, total):
                row = ("K", face, total)
            if row is not None:
                output[row] += sign * term["coefficient"]
            sign = -sign
    return {index: coefficient for index, coefficient in output.items() if coefficient}


def audit() -> dict:
    checks = 0

    def check(condition: bool, name: str) -> None:
        nonlocal checks
        if not condition:
            raise AssertionError(name)
        checks += 1

    for path, expected in PINNED.items():
        check(file_hash(path) == expected, f"premise hash {path.name}")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    target = json.loads(TARGET.read_text(encoding="utf-8"))
    result = json.loads(RESULTS.read_text(encoding="utf-8"))
    check(result["artifact_hash"] == digest({k: v for k, v in result.items() if k != "artifact_hash"}),
          "result internal hash")
    check(result["status"] == "COMPLETE" and result["p1_status"] == "REFUTED"
          and result["p2_status"] == "PASS_FINITE", "result verdicts")
    check(source["p11_source_labels_accessed"] is False and result["p11_source_accessed"] is False,
          "holdout remains locked")
    check([[row["p"] for row in item["rows"]] for item in (source, target, result)]
          == [[8, 9, 10]] * 3, "parameter alignment")
    rows = []
    for source_row, target_row, saved in zip(source["rows"], target["rows"], result["rows"], strict=True):
        p = source_row["p"]
        support = source_row["inclusions"][0]["source_support"]
        check(support == source_row["inclusions"][1]["source_support"], f"p={p} common source")
        check(saved["row_hash"] == digest({k: v for k, v in saved.items() if k != "row_hash"}),
              f"p={p} row hash")
        actual = independent_boundary(p, support)
        expected = Counter()
        for inclusion in target_row["inclusions"]:
            for term in inclusion["semantic_rows"]:
                row_label = term["exact_label"]
                check(len(row_label[1]) == 2 * p - 3
                      and sum(row_label[1]) + row_label[-1] == 4 * p * p + 6 * p - 1,
                      f"p={p} target grading")
                expected[key(row_label)] += 2 * term["coefficient"]
        expected = {index: coefficient for index, coefficient in expected.items() if coefficient}
        residual = {index: actual.get(index, 0) - expected.get(index, 0)
                    for index in actual.keys() | expected.keys()
                    if actual.get(index, 0) != expected.get(index, 0)}
        for field, vector in (("boundary", actual), ("expected_boundary", expected), ("residual", residual)):
            check(sparse(saved[field]) == vector, f"p={p} exact {field}")
        check(saved["boundary_support"] == len(actual) and saved["expected_support"] == len(expected)
              and saved["residual_support"] == len(residual) == 1, f"p={p} supports")
        residual_exterior = tuple(value for value in (*range(1, p + 1), *range(3 * p, 4 * p - 1))
                                  if value not in (2, 3 * p))
        check(residual == {("K", residual_exterior, 13 * p): 2 * (-1) ** p},
              f"p={p} observed residual description")
        check(all(value % 2 == 0 for value in actual.values()) and saved["residual_odd_coefficients"] == 0,
              f"p={p} full mod-two cycle")
        check(saved["full_identity"] is False and saved["residual_kinds"] == {"K": 1},
              f"p={p} honest identity failure")

        matrix_path = EXPERIMENTS / f"EXP-042-bockstein-normal-form/artifacts/matrix-p{p}.json"
        check(file_hash(matrix_path) == source_row["matrix_sha256"], f"p={p} matrix hash")
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        projected = [0] * matrix["rows"]
        for term in support:
            for row_index, coefficient in matrix["signed_columns"][term["matrix_column"]]:
                projected[row_index] += term["coefficient"] * coefficient
        target_projected = [0] * matrix["rows"]
        for inclusion in target_row["inclusions"]:
            tag = "A" if inclusion["target_mask"] == 59 else "B"
            pattern = [-2, -3, 1, 0, 1, 0, 0, 0, 0, 0] if tag == "A" else [-1, -4, 1, 0, 1, 0, 0, 0, 0, 0]
            matching = [index for index, atom_id in enumerate(matrix["row_atom_ids"])
                        if json.loads(matrix["row_atom_table"][atom_id]) == ["row", "D", tag, pattern]]
            for term in inclusion["semantic_rows"]:
                target_projected[matching[term["projected_row"]]] += 2 * term["coefficient"]
        check(projected == target_projected, f"p={p} every projected row")
        check(saved["projected_regression"] == {
            "all_component_rows_checked": matrix["rows"], "identity": True,
            "boundary_hash": digest(projected), "matrix_sha256": file_hash(matrix_path),
        }, f"p={p} projected certificate")
        mutation = deepcopy(support)
        mutation[0]["coefficient"] *= -1
        corrupted = independent_boundary(p, mutation)
        check(corrupted != actual, f"p={p} sign mutation detected")
        mutation_difference = {index: corrupted.get(index, 0) - actual.get(index, 0)
                               for index in corrupted.keys() | actual.keys()
                               if corrupted.get(index, 0) != actual.get(index, 0)}
        rows.append({"p": p, "source_support_checked": len(support),
                     "full_boundary_support_checked": len(actual),
                     "component_rows_checked": matrix["rows"],
                     "residual": records(residual), "sign_mutation_detected": True,
                     "mutation_difference_support": len(mutation_difference),
                     "independent_boundary_hash": digest(records(actual))})
    certificate = {
        "experiment": "EXP-054", "status": "INDEPENDENT_AUDIT_PASS", "p3_status": "PASS_FINITE",
        "checks": checks, "independence": "direct gap intervals and reverse-order exterior differential",
        "scope": "p=8,9,10 only; projected regression plus full semantic differential; no uniform claim",
        "p11_source_accessed": False,
        "premise_sha256": {path.relative_to(EXPERIMENTS).as_posix(): value for path, value in PINNED.items()},
        "audit_code_sha256": file_hash(Path(__file__)), "rows": rows,
    }
    certificate["artifact_hash"] = digest(certificate)
    return certificate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/audit-certificate.json")
    args = parser.parse_args()
    certificate = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": certificate["status"], "checks": certificate["checks"],
                      "artifact_hash": certificate["artifact_hash"]}))


if __name__ == "__main__":
    main()
