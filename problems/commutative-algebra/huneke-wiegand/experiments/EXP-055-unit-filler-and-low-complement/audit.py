"""Independent EXP-055 filler, source repair, and complement-sign audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
RESULTS = HERE / "artifacts/results.json"
SOURCE = EXPERIMENTS / "EXP-053-labelled-source-pullback/artifacts/training-p8-p10.json"
TARGET = EXPERIMENTS / "EXP-052-semantic-unreduced-lifts/artifacts/training-p8-p10.json"
PREVIOUS_AUDIT = EXPERIMENTS / "EXP-054-full-source-boundary/audit.py"
PINNED = {
    SOURCE: "0d6bb8b885d965ed91a94d06a072d8baacca56df65903e10e1c91382f649edfe",
    TARGET: "259ff476b7bb09c12566e4bd771da5c88af17f541cc5732db4dc7f2067e2ec70",
    PREVIOUS_AUDIT: "9e21b8a03694938e04dc7aba3555944fa511e4d1ac0d4dfc92727288ed7a1b63",
    HERE / "run.py": "95e23a3e9136e1e46b1272a337796901cededb51d0c3345f1f08cc0ba4103fef",
    RESULTS: "c54419a4b0de90ffc5caccaa6bc71ac7b3758bc88cd7bbc5ba9671831cad6bc7",
}


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_previous():
    spec = importlib.util.spec_from_file_location("independent_exp054_for_exp055", PREVIOUS_AUDIT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def complement_sign(selected: list, universe: list) -> int:
    """Parity from selected positions, independent of pairwise inversion counting."""
    assert universe == sorted(set(universe)) and selected == sorted(set(selected))
    assert set(selected) <= set(universe)
    positions = {value: index for index, value in enumerate(universe)}
    exponent = sum(positions[value] for value in selected) - len(selected) * (len(selected) - 1) // 2
    return -1 if exponent % 2 else 1


def verify_complements() -> dict:
    checks = 0
    mutation_rejections = 0
    for size in range(1, 9):
        universe = list(range(size))
        for bits in range(1, 1 << size):
            selected = [value for value in universe if bits & (1 << value)]
            missing = [value for value in universe if not bits & (1 << value)]
            orientation = complement_sign(selected, universe)
            for value in selected:
                face = [other for other in selected if other != value]
                differential_sign = -1 if selected.index(value) % 2 else 1
                transformed = differential_sign * complement_sign(face, universe)
                insertion_index = sum(other < value for other in missing)
                expected = orientation * (-1) ** (len(selected) - 1 + insertion_index)
                assert transformed == expected
                assert transformed != -expected
                checks += 1
                mutation_rejections += 1
    return {"universe_sizes": [1, 8], "signed_insertion_checks": checks,
            "reversed_sign_mutations_rejected": mutation_rejections, "passed": True}


def independent_filler(p: int) -> tuple[dict, tuple]:
    exterior = [value for value in range(1, 4 * p - 1)
                if (value <= p or value >= 3 * p) and value not in (2, 3 * p)]
    return ({"coefficient": 1, "exact_label": ["K", exterior + [7 * p], 6 * p]},
            ("K", tuple(exterior), 13 * p))


def audit() -> dict:
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        assert condition, message
        checks += 1

    for path, expected in PINNED.items():
        check(file_hash(path) == expected, f"premise hash {path.name}")
    arithmetic = load_previous()
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    target = json.loads(TARGET.read_text(encoding="utf-8"))
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    check(results["artifact_hash"] == digest({k: v for k, v in results.items() if k != "artifact_hash"}),
          "artifact internal hash")
    check(results["status"] == "COMPLETE" and results["p11_source_accessed"] is False, "run status")
    check(results["p1_status"] == "UNIFORM_FILLER_PROVED_FINITE_SOURCES_REPAIRED"
          and results["p2_status"] == "PASS_FINITE", "honest theorem scope")
    check([row["p"] for row in results["uniform_filler_regressions"]] == list(range(4, 101)),
          "all 97 declared filler parameters")
    for saved in results["uniform_filler_regressions"]:
        p = saved["p"]
        column, row = independent_filler(p)
        boundary = arithmetic.independent_boundary(p, [column])
        check(boundary == {row: -1}, f"p={p} unit filler identity")
        check(arithmetic.sparse(saved["boundary"]) == boundary, f"p={p} saved filler")
        check(all(arithmetic.high_contains(p, 6 * p + value) for value in row[1]),
              f"p={p} every low face vanishes")
        corrupted = {**column, "coefficient": -1}
        check(arithmetic.independent_boundary(p, [corrupted]) == {row: 1}, f"p={p} sign control")
    check([row["p"] for row in results["training"]] == [8, 9, 10], "training parameters")
    certificates = []
    for source_row, target_row, saved in zip(source["rows"], target["rows"], results["training"], strict=True):
        p = source_row["p"]
        check(p == target_row["p"] == saved["p"], f"p={p} alignment")
        check(saved["row_hash"] == digest({k: v for k, v in saved.items() if k != "row_hash"}),
              f"p={p} row hash")
        support = source_row["inclusions"][0]["source_support"]
        correction, residual_row = independent_filler(p)
        correction["coefficient"] = 2 * (-1) ** p
        expected = Counter()
        for inclusion in target_row["inclusions"]:
            for term in inclusion["semantic_rows"]:
                expected[arithmetic.key(term["exact_label"])] += 2 * term["coefficient"]
        expected = {index: value for index, value in expected.items() if value}
        actual = arithmetic.independent_boundary(p, support + [correction])
        check(actual == expected, f"p={p} repaired full source")
        check(saved["even_correction"] == correction and saved["corrected_full_identity"] is True,
              f"p={p} correction record")
        check(saved["source_support_before"] == len(support)
              and saved["source_support_after"] == len(support) + 1, f"p={p} full support sizes")
        wrong_correction = {**correction, "coefficient": -correction["coefficient"]}
        corrupted = arithmetic.independent_boundary(p, support + [wrong_correction])
        difference = {index: corrupted.get(index, 0) - expected.get(index, 0)
                      for index in corrupted.keys() | expected.keys()
                      if corrupted.get(index, 0) != expected.get(index, 0)}
        check(difference == {residual_row: 4 * (-1) ** p}, f"p={p} correction sign mutation")
        low = [*range(1, p + 1), *range(3 * p, 4 * p - 1)]
        low_set = set(low)
        selected = [term for term in support if term["exact_label"][0] == "S"
                    and [value for value in term["exact_label"][1] if value not in low_set] == [6 * p, 10 * p]]
        check(selected == saved["fixed_high_source"] and len(selected) == saved["fixed_high_source_support"],
              f"p={p} fixed-high slice")
        check(len(selected) == p - 1, f"p={p} observed slice size")
        sliced_boundary = arithmetic.independent_boundary(p, selected)
        d_boundary = {index: value for index, value in sliced_boundary.items() if index[0] == "D"}
        k_boundary = {index: value for index, value in sliced_boundary.items() if index[0] == "K"}
        check(d_boundary == expected and saved["d_identity"] is True, f"p={p} slice D boundary")
        check(k_boundary == arithmetic.sparse(saved["k_boundary"])
              and len(k_boundary) == saved["k_boundary_support"], f"p={p} complete slice K boundary")
        missing_records = []
        for term in selected:
            _, exterior, coefficient = term["exact_label"]
            missing = [value for value in low if value not in exterior]
            check(len(missing) == 3 and sum(missing) - coefficient == 6 * p + 2,
                  f"p={p} complement grading")
            missing_records.append({"coefficient": term["coefficient"], "missing_low": missing,
                                    "source_coefficient": coefficient,
                                    "complement_sign": complement_sign(
                                        [value for value in exterior if value in low_set], low)})
        check(missing_records == saved["missing_set_source"], f"p={p} signed complement labels")
        certificates.append({"p": p, "corrected_full_identity": True,
                             "corrected_boundary_hash": digest(arithmetic.records(actual)),
                             "fixed_high_source_support": len(selected), "k_boundary_support": len(k_boundary),
                             "correction_sign_mutation_detected": True})
    complement = verify_complements()
    check(results["complement_certificate"] == {
        k: v for k, v in complement.items() if k != "reversed_sign_mutations_rejected"
    }, "complete complement-sign certificate")
    certificate = {"experiment": "EXP-055", "status": "INDEPENDENT_AUDIT_PASS", "p3_status": "PASS",
                   "checks": checks, "filler_parameters_verified": [4, 100], "filler_count": 97,
                   "p11_source_accessed": False, "training": certificates, "complement": complement,
                   "scope": "uniform filler checked against direct interval proof; other source claims finite",
                   "premise_sha256": {path.relative_to(EXPERIMENTS).as_posix(): value
                                      for path, value in PINNED.items()},
                   "audit_code_sha256": file_hash(Path(__file__))}
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
                      "complement_checks": certificate["complement"]["signed_insertion_checks"],
                      "artifact_hash": certificate["artifact_hash"]}))


if __name__ == "__main__":
    main()
