"""Independent original-incidence and local-source certificates, exact CPU only."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_arithmetic():
    path = EXPERIMENTS / "EXP-054-full-source-boundary/audit.py"
    assert file_hash(path) == "9e21b8a03694938e04dc7aba3555944fa511e4d1ac0d4dfc92727288ed7a1b63"
    spec = importlib.util.spec_from_file_location("independent_exp054_for_058", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def key(label: list) -> tuple:
    return (label[0], tuple(label[1]), *label[2:])


def label(index: tuple) -> list:
    return [index[0], list(index[1]), *index[2:]]


def coefficient_sets(p: int, arithmetic) -> tuple[list, list]:
    low = [value for value in range(1, 4 * p - 1) if arithmetic.low_kind(p, value) is not None]
    high = [value for value in range(6 * p, 18 * p) if arithmetic.high_contains(p, value)]
    return low, high


def inverse_neighbors(p: int, row: tuple, arithmetic) -> dict:
    """Enumerate coefficient first, independently of forward generator insertion."""
    low, high = coefficient_sets(p, arithmetic)
    generators = set(low + high)
    exterior = set(row[1])
    total = row[-1]
    result = {}
    if row[0] == "K":
        assert arithmetic.degree_two_contains(p, total)
        for coefficient in high:
            variable = total - coefficient
            if variable in generators and variable not in exterior:
                source = ("K", tuple(sorted(exterior | {variable})), coefficient)
                result[source] = -1 if sum(value < variable for value in exterior) % 2 else 1
        for coefficient in low:
            variable = total - coefficient
            if variable in high and variable not in exterior:
                source = ("S", tuple(sorted(exterior | {variable})), coefficient)
                result[source] = -1 if sum(value < variable for value in exterior) % 2 else 1
    else:
        assert row[0] == "D" and row[2] in ("A", "B")
        for coefficient in low:
            variable = total - coefficient
            if variable not in low or variable in exterior:
                continue
            variable_kind = arithmetic.low_kind(p, variable)
            coefficient_kind = arithmetic.low_kind(p, coefficient)
            product_kind = None
            if variable_kind == coefficient_kind == "L0" and total > p:
                product_kind = "A"
            elif variable_kind != coefficient_kind and total >= 4 * p - 1:
                product_kind = "B"
            if product_kind == row[2]:
                source = ("S", tuple(sorted(exterior | {variable})), coefficient)
                result[source] = -1 if sum(value < variable for value in exterior) % 2 else 1
    return result


def endpoint_target(p: int) -> dict:
    """Encode 2 eta directly from its four endpoint terms, no producer import."""
    low = {*range(1, p + 1), *range(3 * p, 4 * p - 1)}
    endpoints = [(p - 3, 2, p - 3, 4), (p - 2, 2, p - 2, -2),
                 (p - 2, 1, p - 3, 4), (p - 3, 1, p - 4, -4)]
    return {("K", tuple(sorted((low - {a, 3 * p, 3 * p + j}) | {6 * p})), 10 * p + coefficient):
            weight * (-1) ** p for a, j, coefficient, weight in endpoints}


def rational(value) -> Fraction:
    if isinstance(value, list):
        assert len(value) == 2 and value[1] > 0
        return Fraction(value[0], value[1])
    return Fraction(value)


def sparse(records: list) -> dict:
    result = {}
    for record in records:
        index = key(record["exact_label"])
        assert index not in result
        value = rational(record["coefficient"])
        if value:
            result[index] = value
    return result


def verify_neighborhood(p: int, neighborhood: dict, expected_frontier: set,
                        previous_columns: set, arithmetic, budget_check) -> tuple[dict, set, set]:
    frontier = {key(item) for item in neighborhood["frontier"]}
    assert frontier == expected_frontier
    expected_columns = set(previous_columns)
    incident_coefficients = {}
    for row in frontier:
        neighbors = inverse_neighbors(p, row, arithmetic)
        expected_columns.update(neighbors)
        for source, coefficient in neighbors.items():
            incident_coefficients.setdefault(source, {})[row] = coefficient
        budget_check()
    source_labels = [key(column["exact_label"]) for column in neighborhood["columns"]]
    assert len(source_labels) == len(set(source_labels)) and set(source_labels) == expected_columns
    row_labels = [key(item) for item in neighborhood["row_labels"]]
    assert len(row_labels) == len(set(row_labels))
    all_rows = set(endpoint_target(p))
    boundaries = {}
    for source, column in zip(source_labels, neighborhood["columns"], strict=True):
        original = arithmetic.independent_boundary(p, [{"coefficient": 1, "exact_label": label(source)}])
        saved = {}
        for index, coefficient in column["boundary"]:
            assert isinstance(index, int) and 0 <= index < len(row_labels)
            assert row_labels[index] not in saved and coefficient != 0
            saved[row_labels[index]] = coefficient
        assert original == saved
        assert all(saved.get(row) == coefficient
                   for row, coefficient in incident_coefficients.get(source, {}).items())
        all_rows.update(original)
        boundaries[source] = original
        budget_check()
    assert all_rows == set(row_labels)
    assert len(source_labels) <= 1200 and sum(map(len, boundaries.values())) <= 20000
    assert neighborhood["status"] == "COMPLETE"
    assert neighborhood["columns_count"] == len(source_labels)
    assert neighborhood["rows_count"] == len(row_labels)
    assert neighborhood["nnz"] == sum(map(len, boundaries.values()))
    assert neighborhood["incidence_hash"] == digest({k: v for k, v in neighborhood.items()
                                                    if k not in ("incidence_hash", "solve")})
    solution = neighborhood["solve"]
    classification = solution["classification"]
    if classification == "PENDING":
        return ({"radius": neighborhood["radius"], "classification": "PENDING",
                 "columns_verified": len(source_labels), "rows_verified": len(row_labels),
                 "full_incidence_verified": True}, expected_columns, all_rows)
    witness = sparse(solution["particular_solution"])
    assert set(witness) <= set(source_labels)
    actual = {}
    for source, coefficient in witness.items():
        for row, value in boundaries[source].items():
            actual[row] = actual.get(row, Fraction(0)) + coefficient * value
    target = endpoint_target(p)
    residual = {row: Fraction(target.get(row, 0)) - actual.get(row, Fraction(0))
                for row in set(target) | set(actual)
                if target.get(row, 0) != actual.get(row, 0)}
    assert sparse(solution["residual"]) == residual
    dual_verified = False
    dual_details = None
    mutation_checks = 0
    if classification == "QQ_INCONSISTENT":
        assert residual
        assert solution["integer_membership"] == "EXCLUDED_IN_THIS_LOCAL_SPAN_ONLY"
        dual = sparse(solution["dual"])
        assert set(dual) <= all_rows and all(value.denominator == 1 for value in dual.values())
        pairing = sum(dual.get(row, 0) * value for row, value in target.items())
        assert pairing != 0 and rational(solution["dual_target_pairing"]) == pairing
        for boundary in boundaries.values():
            assert sum(dual.get(row, 0) * value for row, value in boundary.items()) == 0
            budget_check()
        altered = dict(dual)
        changed_row = next(iter(altered))
        altered[changed_row] += 1
        assert any(sum(altered.get(row, 0) * value for row, value in boundary.items()) != 0
                   for boundary in boundaries.values())
        dual_details = {
            "support": len(dual), "maximum_absolute_coefficient": max(abs(int(value)) for value in dual.values()),
            "target_pairing": int(pairing), "coefficient_mutation_rejected": True,
            "row_kinds": {kind: sum(row[0] == kind for row in dual) for kind in sorted({row[0] for row in dual})},
            "target_contributions": [{"exact_label": label(row), "pairing": int(dual[row] * target[row])}
                                     for row in sorted(set(dual) & set(target)) if dual[row] * target[row]],
        }
        dual_verified = True
    elif classification in ("INTEGRAL_WITNESS", "RATIONAL_SECTION"):
        assert not residual
        integral = all(value.denominator == 1 for value in witness.values())
        assert integral == (classification == "INTEGRAL_WITNESS")
        if integral:
            assert solution["integer_membership"] == "CERTIFIED_IN_THIS_LOCAL_SPAN"
            retained = sparse(solution["integral_witness"])
            assert retained == witness
            support = [{"exact_label": label(source), "coefficient": int(value)}
                       for source, value in witness.items()]
            assert arithmetic.independent_boundary(p, support) == target
            # Adding one to any retained source coefficient changes the full boundary
            # precisely by its independently checked, nonzero original column.
            for source in witness:
                assert boundaries[source]
                mutation_checks += 1
            changed = [dict(term) for term in support]
            changed[0]["coefficient"] += 1
            assert arithmetic.independent_boundary(p, changed) != target
        else:
            assert solution["integer_membership"] == "INCONCLUSIVE_NOT_A_LATTICE_OBSTRUCTION"
    else:
        raise AssertionError(f"unsupported local-solve classification: {classification}")
    return ({"radius": neighborhood["radius"], "classification": classification,
             "columns_verified": len(source_labels), "rows_verified": len(row_labels),
             "nonzero_incidence_entries_verified": sum(map(len, boundaries.values())),
             "full_incidence_verified": True, "rational_residual_verified": True,
             "integer_dual_verified": dual_verified, "dual_details": dual_details,
             "witness_mutation_columns_verified": mutation_checks,
             "source_span_scope": "this complete local neighborhood only"}, expected_columns, all_rows)


def verify_size_cap(p: int, frontier: set, previous_columns: set, arithmetic,
                    column_cap: int, nnz_cap: int, budget_check) -> dict:
    """Confirm independently that the next complete neighborhood cannot fit the cap."""
    columns = set(previous_columns)
    nnz = 0
    for source in columns:
        nnz += len(arithmetic.independent_boundary(p, [{"coefficient": 1, "exact_label": label(source)}]))
        budget_check()
    for row in sorted(frontier):
        for source in sorted(inverse_neighbors(p, row, arithmetic)):
            if source in columns:
                continue
            columns.add(source)
            if len(columns) > column_cap:
                return {"verified": True, "reason": "COLUMN_CAP", "lower_bound_columns": len(columns)}
            nnz += len(arithmetic.independent_boundary(p, [{"coefficient": 1, "exact_label": label(source)}]))
            if nnz > nnz_cap:
                return {"verified": True, "reason": "NNZ_CAP", "lower_bound_nnz": nnz}
            budget_check()
    raise AssertionError("claimed incidence cap is not needed for the complete next neighborhood")


def audit(results_path: Path | None = None, budget_seconds: float = 60) -> dict:
    if not 0 < budget_seconds <= 60:
        raise ValueError("audit budget must be positive and at most 60 seconds")
    started = time.monotonic()

    def budget_check():
        if time.monotonic() - started > budget_seconds:
            raise RuntimeError("EXP-058 independent audit budget exhausted")

    path = results_path or HERE / "artifacts/results.json"
    result = json.loads(path.read_text(encoding="utf-8"))
    assert result["artifact_hash"] == digest({k: v for k, v in result.items() if k != "artifact_hash"})
    for relative, expected in result["premises"].items():
        assert file_hash(EXPERIMENTS / relative) == expected
    assert result["premises"]["EXP-058-local-endpoint-source/hypothesis.md"] == (
        "f538be10015e085851e7a355df97dc73018fc6aa1d4da89c88692ccff18ed7b4")
    assert result["p11_original_source_accessed"] is False and result["old_hnf_source_accessed"] is False
    parameters = result["parameters_requested"]
    assert parameters and parameters == sorted(set(parameters)) and set(parameters) <= {8, 9, 10}
    caps = result["caps"]
    assert 0 < caps["columns"] <= 1200 and 0 < caps["nnz"] <= 20000 and 0 < caps["seconds"] <= 60
    assert caps["private_bytes"] == 1024 ** 3
    arithmetic = load_arithmetic()
    verified = []
    for position, row in enumerate(result["rows"]):
        p = row["p"]
        assert p == parameters[position]
        target = endpoint_target(p)
        assert sparse(row["target"]) == target
        frontier = set(target)
        expanded = set()
        columns = set()
        certificates = []
        for radius, neighborhood in enumerate(row["neighborhoods"], start=1):
            assert radius <= 2 and neighborhood["radius"] == radius
            certificate, columns, all_rows = verify_neighborhood(
                p, neighborhood, frontier, columns, arithmetic, budget_check)
            certificates.append(certificate)
            expanded.update(frontier)
            frontier = all_rows - expanded
            budget_check()
        assert row["completed_radius"] == len(certificates)
        cap_certificate = None
        if row["status"] == "QQ_REFUTED":
            assert row["p1_status"] == "REFUTED" and len(certificates) == 2
            assert certificates[-1]["classification"] == "QQ_INCONSISTENT"
            if not result["continued_after_refutation"]:
                assert position == len(result["rows"]) - 1
                assert result["status"] == "STOPPED_ON_FIRST_REFUTATION"
        elif row["status"] == "INTEGRAL_WITNESS":
            assert certificates[-1]["classification"] == "INTEGRAL_WITNESS"
            assert row["p1_status"] == "PASS_FINITE"
        elif row["status"] == "RATIONAL_SECTION":
            assert row["p1_status"] == "INCONCLUSIVE" and len(certificates) == 2
            assert certificates[-1]["classification"] == "RATIONAL_SECTION"
        elif row["status"] == "INCONCLUSIVE_CAP":
            assert row["p1_status"] == "INCONCLUSIVE" and len(certificates) < 2
            cap_certificate = verify_size_cap(p, frontier, columns, arithmetic,
                                              caps["columns"], caps["nnz"], budget_check)
        elif row["status"] == "INCONCLUSIVE_RESOURCE_CAP":
            assert row["p1_status"] == "INCONCLUSIVE"
        else:
            raise AssertionError(f"unfinished or unknown row status: {row['status']}")
        verified.append({"p": p, "status": row["status"], "neighborhoods": certificates,
                         "independent_size_cap": cap_certificate})
    witness_count = sum(item["status"] == "INTEGRAL_WITNESS" for item in verified)
    certificate = {"experiment": "EXP-058", "status": "INDEPENDENT_AUDIT_PASS",
                   "p2_status": "PASS_FINITE" if witness_count else "NOT_APPLICABLE_NO_INTEGRAL_WITNESS",
                   "verified_integral_parameters": witness_count,
                   "rows": verified, "p11_original_source_accessed": False, "old_hnf_source_accessed": False,
                   "scope": "full original incidence; QQ duals exclude only declared local spans",
                   "result_sha256": file_hash(path), "producer_sha256": file_hash(HERE / "run.py"),
                   "audit_code_sha256": file_hash(Path(__file__)), "premises": result["premises"]}
    certificate["artifact_hash"] = digest(certificate)
    return certificate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/audit-results.json")
    args = parser.parse_args()
    certificate = audit(args.results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": certificate["status"], "p2_status": certificate["p2_status"],
                      "verified_parameters": [row["p"] for row in certificate["rows"]],
                      "artifact_hash": certificate["artifact_hash"]}))


if __name__ == "__main__":
    main()
