"""Independent exact-matrix audit for EXP-051 unreduced lifts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP047 = HERE.parent / "EXP-047-relative-kernel-smith"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_RUN_SHA256 = "4e0debc35c7aa286cfcc73dcbe6c6d4e1d15cfcc5e7d184db7e81e45f5e8b98a"
EXPECTED_RESULTS_SHA256 = "f1acaa6b769ec04b7d87a1ac416c184ffac2f5007d18a04efb397c8013ec8b1f"


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


def dense(entries: list[list[int]], length: int) -> list[int]:
    result = [0] * length
    for index, value in entries:
        result[int(index)] = int(value)
    return result


def multiply_cycle(
    columns: list[list[list[int]]], cycle_columns: list[int], row_count: int
) -> list[int]:
    result = [0] * row_count
    for column in cycle_columns:
        for row, value in columns[int(column)]:
            result[int(row)] += int(value)
    return result


def canonical_binary_basis(vectors: list[int]) -> list[int]:
    """Low-pivot reduced basis, implemented independently of the runner."""
    basis: dict[int, int] = {}
    for raw in vectors:
        vector = raw
        for pivot in sorted(basis):
            if vector & (1 << pivot):
                vector ^= basis[pivot]
        if not vector:
            continue
        pivot = (vector & -vector).bit_length() - 1
        for other in list(basis):
            if basis[other] & (1 << pivot):
                basis[other] ^= vector
        basis[pivot] = vector
    return [basis[pivot] for pivot in sorted(basis)]


def reduce_mod_basis(vector: int, basis: list[int]) -> int:
    for basis_vector in basis:
        pivot = (basis_vector & -basis_vector).bit_length() - 1
        if vector & (1 << pivot):
            vector ^= basis_vector
    return vector


def affine(values: list[int]) -> list[int] | None:
    slope = values[1] - values[0]
    if any(right - left != slope for left, right in zip(values, values[1:])):
        return None
    return [slope, values[0] - 8 * slope]


def main() -> int:
    if sha256(HERE / "run.py") != EXPECTED_RUN_SHA256:
        raise AssertionError("run.py hash mismatch")
    if sha256(RESULTS) != EXPECTED_RESULTS_SHA256:
        raise AssertionError("results hash mismatch")
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, value: bool) -> None:
        checks.append({"name": name, "pass": bool(value)})

    stored_hash = results.pop("artifact_hash")
    check("results internal hash", digest(results) == stored_hash)
    results["artifact_hash"] = stored_hash
    check("results complete", results["status"] == "COMPLETE")
    check("declared parameter set", [row["p"] for row in results["rows"]] == [8, 9, 10, 11])
    check("P1 finite pass", results["p1_status"] == "PASS_FINITE")
    check("P2 finite pass", results["p2_status"] == "PASS_FINITE")
    check("P3 refuted", results["p3_status"] == "REFUTED")

    route_records = 0
    for row in results["rows"]:
        p = int(row["p"])
        for inclusion in row["inclusions"]:
            source = int(inclusion["source_mask"])
            target = int(inclusion["target_mask"])
            relative_path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target}.json"
            check(
                f"p={p} {source}->{target} relative hash",
                sha256(relative_path) == inclusion["relative_sha256"],
            )
            relative = json.loads(relative_path.read_text(encoding="utf-8"))
            columns = relative["matrix_columns"]
            row_count = int(relative["matrix_shape"][0])
            column_parities = [
                sum(1 << int(index) for index, value in column if int(value) & 1)
                for column in columns
            ]
            image_basis = canonical_binary_basis(column_parities)
            route_subspaces = []
            for route_name in ("primary", "audit"):
                route = inclusion[route_name]
                quotient_classes = []
                for index, record in enumerate(route["selected"]):
                    route_records += 1
                    prefix = f"p={p} {source}->{target} {route_name} lift={index}"
                    cycle_columns = list(map(int, record["cycle_columns"]))
                    doubled = multiply_cycle(columns, cycle_columns, row_count)
                    check(f"{prefix} even boundary", all(not (value & 1) for value in doubled))
                    exact = [value // 2 for value in doubled]
                    stored = dense(record["boundary"], row_count)
                    check(f"{prefix} exact identity", exact == stored)
                    check(f"{prefix} boundary hash", digest(exact) == record["boundary_hash"])
                    cycle = sum(1 << column for column in cycle_columns)
                    check(f"{prefix} cycle hash", digest(cycle) == record["cycle_hash"])
                    check(
                        f"{prefix} cycle support",
                        len(cycle_columns) == int(record["cycle_support_size"]),
                    )
                    check(
                        f"{prefix} boundary support",
                        sum(bool(value) for value in exact) == int(record["boundary_support_size"]),
                    )
                    check(
                        f"{prefix} boundary height",
                        max(map(abs, exact), default=0) == int(record["boundary_max_abs"]),
                    )
                    parity = sum(1 << index for index, value in enumerate(exact) if value & 1)
                    quotient = reduce_mod_basis(parity, image_basis)
                    stored_quotient = sum(
                        1 << int(index) for index in record["quotient_class_rows"]
                    )
                    check(f"{prefix} quotient class", quotient == stored_quotient != 0)
                    check(
                        f"{prefix} quotient hash",
                        digest(quotient) == record["quotient_class_hash"],
                    )
                    check(
                        f"{prefix} P1 bounds",
                        int(record["boundary_support_size"]) <= 8 * p
                        and int(record["boundary_max_abs"]) <= 2,
                    )
                    check(
                        f"{prefix} P2 bound",
                        int(record["cycle_support_size"]) <= 4 * p,
                    )
                    quotient_classes.append(quotient)
                subspace = canonical_binary_basis(quotient_classes)
                route_subspaces.append(subspace)
                check(f"p={p} {source}->{target} {route_name} quotient rank", len(subspace) == 2)
                check(
                    f"p={p} {source}->{target} {route_name} subspace hash",
                    digest(subspace) == route["selected_subspace_hash"],
                )
            check(
                f"p={p} {source}->{target} route subspace agreement",
                route_subspaces[0] == route_subspaces[1],
            )

    check("thirty-two exact route records", route_records == 32)
    p3_recomputed: dict[str, object] = {}
    for source, target in ((58, 59), (58, 62)):
        groups = [
            sorted(
                next(
                    inclusion
                    for inclusion in row["inclusions"]
                    if (int(inclusion["source_mask"]), int(inclusion["target_mask"]))
                    == (source, target)
                )["primary"]["selected"],
                key=lambda record: (
                    int(record["boundary_support_size"]),
                    int(record["cycle_support_size"]),
                ),
            )
            for row in results["rows"]
        ]
        boundary_series = [
            [int(group[index]["boundary_support_size"]) for group in groups]
            for index in range(2)
        ]
        cycle_series = [
            [int(group[index]["cycle_support_size"]) for group in groups]
            for index in range(2)
        ]
        boundary_affine = [affine(series) for series in boundary_series]
        cycle_affine = [affine(series) for series in cycle_series]
        p3_recomputed[f"{source}->{target}"] = {
            "boundary_support_series": boundary_series,
            "boundary_affine_slope_intercept": boundary_affine,
            "cycle_support_series": cycle_series,
            "cycle_affine_slope_intercept": cycle_affine,
            "passes": all(value is not None for value in boundary_affine + cycle_affine),
        }
    check("P3 details independently reproduced", p3_recomputed == results["p3_details"])
    check("P3 has a non-affine series", any(not detail["passes"] for detail in p3_recomputed.values()))

    passed = sum(item["pass"] for item in checks)
    certificate = {
        "experiment": "EXP-051",
        "audit": "independent raw-matrix, quotient-rank, exact-identity, and bound checks",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "run_sha256": EXPECTED_RUN_SHA256,
        "results_sha256": EXPECTED_RESULTS_SHA256,
        "checks": checks,
    }
    certificate["artifact_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(
        json.dumps(
            {
                key: certificate[key]
                for key in ("status", "checks_passed", "checks_total", "artifact_hash")
            },
            indent=2,
        )
    )
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
