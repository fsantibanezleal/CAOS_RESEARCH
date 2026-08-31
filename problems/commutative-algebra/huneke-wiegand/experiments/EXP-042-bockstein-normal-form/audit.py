"""Independent audit of EXP-042 signed matrices and Bockstein certificates."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTIFACTS = HERE / "artifacts"
RESULTS = ARTIFACTS / "results.json"
OUTPUT = ARTIFACTS / "audit-certificate.json"
EXPECTED_RESULTS_SHA256 = "3c4ae292fb17a5daf473aee0ed37e473000de686607b5da0a0f4c357a8216ee2"
EXPECTED_MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    11: "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
}
EXPECTED = {
    8: {
        "rows": 2675,
        "columns": 1094,
        "nonzeros": 6747,
        "ranks": {"2": 999, "3": 1002, "5": 1002},
        "support_hash": "226fe0db14b3ace29537ba3c7a3d4ceccf78b19d3591badc69ed5e5c6eb02f5b",
        "signed_hash": "7b1b2c8c93fd9919c5415d42688ccbf6ea852c3bd1514a891a9122b76950757f",
        "bockstein_rank": 3,
    },
    9: {
        "rows": 4757,
        "columns": 1729,
        "nonzeros": 11849,
        "ranks": {"2": 1603, "3": 1607, "5": 1607},
        "support_hash": "f0ae2b05186daf7db912364f2de843a5bd94552243e1a9da5c52345f86f8ef96",
        "signed_hash": "33fd10f22cc55fbfc851f983fe5eaa8c60270e5a8f2b25fda9cd56172c46b763",
        "bockstein_rank": 4,
    },
    10: {
        "rows": 7973,
        "columns": 2607,
        "nonzeros": 19654,
        "ranks": {"2": 2445, "3": 2450, "5": 2450},
        "support_hash": "bcdb558d4afb10b03e7f37af29d5b3a5ca8422a4f92be9bdf954bf1db3899be9",
        "signed_hash": "427c4565a8446119ed68595213f4ee1848c969024430e10b6764d0ce25878185",
        "bockstein_rank": 5,
    },
    11: {
        "rows": 12711,
        "columns": 3785,
        "nonzeros": 31073,
        "ranks": {"2": 3579, "3": 3586, "5": 3586},
        "support_hash": "227a94ea264a15ff38ff0837f4dbcfeea370015cc5dd328080eb4d94ef5a4e2c",
        "signed_hash": "d532dcd7e9eb7d364feae9a9f25439d53347d205bcfef9bfc11b14b64e91c856",
        "bockstein_rank": 7,
    },
}
EXPECTED_SKELETON_HASH = "d0c296e39c7c4f10ffd886b23b3b3d4d9cea0a291dd1aed6fcc079998c57676d"
EXPECTED_HIGH_IMAGE_ATOM = '["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]'
EXPECTED_LOW_IMAGE_ATOM = '["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def int_digest(value: int, bits: int) -> str:
    width = max(1, (bits + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "little")).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def bit_indices(value: int):
    while value:
        least = value & -value
        yield least.bit_length() - 1
        value ^= least


def atom_histogram(indices: list[int], atom_ids: list[int], table: list[str]) -> dict[str, int]:
    counts = Counter(table[atom_ids[index]] for index in indices)
    return dict(sorted(counts.items()))


def pivot_row(vector: int, low_pivot: bool) -> int:
    if low_pivot:
        return (vector & -vector).bit_length() - 1
    return vector.bit_length() - 1


def binary_reduction(
    column_bits: list[int], row_count: int, order: list[int], low_pivot: bool
) -> tuple[list[int], list[int], list[int]]:
    pivots = [0] * row_count
    combinations = [0] * row_count
    kernel: list[int] = []
    for column in order:
        vector = column_bits[column]
        combination = 1 << column
        while vector:
            pivot = pivot_row(vector, low_pivot)
            if not pivots[pivot]:
                pivots[pivot] = vector
                combinations[pivot] = combination
                break
            vector ^= pivots[pivot]
            combination ^= combinations[pivot]
        if not vector:
            kernel.append(combination)
    pivot_rows = [row for row, vector in enumerate(pivots) if vector]
    return pivots, pivot_rows, kernel


def quotient_reduce(
    vector: int, pivots: list[int], pivot_rows: list[int], low_pivot: bool
) -> int:
    rows = pivot_rows if low_pivot else reversed(pivot_rows)
    for pivot in rows:
        if (vector >> pivot) & 1:
            vector ^= pivots[pivot]
    return vector


def bockstein(
    matrix: dict[str, object], *, reverse: bool, low_pivot: bool
) -> dict[str, object]:
    columns = [
        [(int(row), int(sign)) for row, sign in entries]
        for entries in matrix["signed_columns"]
    ]
    row_count = int(matrix["rows"])
    column_count = len(columns)
    column_bits = [sum(1 << row for row, _ in entries) for entries in columns]
    order = list(range(column_count - 1, -1, -1)) if reverse else list(range(column_count))
    pivots, pivot_rows, kernel = binary_reduction(
        column_bits, row_count, order, low_pivot
    )

    records: list[dict[str, object]] = []
    quotient_classes: list[int] = []
    for combination in kernel:
        selected = list(bit_indices(combination))
        boundary: dict[int, int] = {}
        for column in selected:
            for row, sign in columns[column]:
                boundary[row] = boundary.get(row, 0) + sign
        if any(value & 1 for value in boundary.values()):
            raise AssertionError("stored matrix produced a non-even kernel lift")
        divided = sum(1 << row for row, value in boundary.items() if (value // 2) & 1)
        quotient = quotient_reduce(divided, pivots, pivot_rows, low_pivot)
        quotient_classes.append(quotient)
        records.append(
            {
                "cycle_hash": int_digest(combination, column_count),
                "cycle_weight": len(selected),
                "cycle_column_atoms": atom_histogram(
                    selected, matrix["column_atom_ids"], matrix["column_atom_table"]
                ),
                "divided_boundary_hash": int_digest(divided, row_count),
                "quotient_class_hash": int_digest(quotient, row_count),
                "quotient_weight": quotient.bit_count(),
            }
        )

    beta_pivots: dict[int, int] = {}
    independent: list[int] = []
    for index, quotient in enumerate(quotient_classes):
        vector = quotient
        while vector:
            pivot = pivot_row(vector, low_pivot)
            if pivot not in beta_pivots:
                beta_pivots[pivot] = vector
                independent.append(index)
                break
            vector ^= beta_pivots[pivot]

    independent_records: list[dict[str, object]] = []
    for index in independent:
        record = dict(records[index])
        rows = list(bit_indices(quotient_classes[index]))
        record["quotient_row_atoms"] = atom_histogram(
            rows, matrix["row_atom_ids"], matrix["row_atom_table"]
        )
        independent_records.append(record)
    return {
        "order": "reverse" if reverse else "forward",
        "rank_mod_two": len(pivot_rows),
        "kernel_dimension": len(kernel),
        "kernel_basis_hash": digest(sorted(record["cycle_hash"] for record in records)),
        "bockstein_rank": len(beta_pivots),
        "bockstein_class_hash": digest(
            sorted(record["quotient_class_hash"] for record in independent_records)
        ),
        "independent_witnesses": independent_records,
    }


def modular_rank(columns: list[list[list[int]]], prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for entries in columns:
        vector = {int(row): int(value) % prime for row, value in entries if int(value) % prime}
        while vector:
            pivot = max(vector)
            coefficient = vector[pivot]
            if pivot not in pivots:
                inverse = pow(coefficient, -1, prime)
                pivots[pivot] = {
                    row: value * inverse % prime for row, value in vector.items()
                }
                break
            basis = pivots[pivot]
            for row, value in basis.items():
                replacement = (vector.get(row, 0) - coefficient * value) % prime
                if replacement:
                    vector[row] = replacement
                else:
                    vector.pop(row, None)
    return len(pivots)


def matrix_hash_checks(matrix: dict[str, object]) -> dict[str, object]:
    support_hasher = hashlib.sha256()
    signed_hasher = hashlib.sha256()
    for entries in matrix["signed_columns"]:
        support_hasher.update(json.dumps([int(row) for row, _ in entries]).encode())
        signed_hasher.update(json.dumps(entries).encode())
    without_hash = dict(matrix)
    internal_hash = without_hash.pop("artifact_hash")
    return {
        "support_hash": support_hasher.hexdigest(),
        "signed_hash": signed_hasher.hexdigest(),
        "internal_hash_matches": digest(without_hash) == internal_hash,
        "skeleton_hash": digest(
            sorted(set(matrix["row_atom_table"] + matrix["column_atom_table"]))
        ),
    }


def witness_image_atoms(profile: dict[str, object]) -> set[str]:
    return {
        atom
        for witness in profile["independent_witnesses"]
        for atom in witness["quotient_row_atoms"]
    }


def main() -> int:
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = {int(row["p"]): row for row in results["rows"]}
    checks: dict[str, bool] = {
        "results_hash": sha256(RESULTS) == EXPECTED_RESULTS_SHA256,
        "parameter_coverage": set(rows) == set(EXPECTED),
        "primary_status_complete": results["status"] == "COMPLETE",
        "primary_predictions_pass": all(
            results[key] == "PASS_FINITE" for key in ("p1_status", "p2_status", "p3_status")
        ),
    }
    audit_rows: list[dict[str, object]] = []
    for p, expected in EXPECTED.items():
        path = ARTIFACTS / f"matrix-p{p}.json"
        matrix = json.loads(path.read_text(encoding="utf-8"))
        hashes = matrix_hash_checks(matrix)
        stored_forward = matrix["bockstein"]["forward"]
        stored_reverse = matrix["bockstein"]["reverse"]
        reproduced_forward = bockstein(matrix, reverse=False, low_pivot=False)
        reproduced_reverse = bockstein(matrix, reverse=True, low_pivot=False)
        alternate_forward = bockstein(matrix, reverse=False, low_pivot=True)
        alternate_reverse = bockstein(matrix, reverse=True, low_pivot=True)
        ranks = {
            "2": alternate_forward["rank_mod_two"],
            "3": modular_rank(matrix["signed_columns"], 3),
            "5": modular_rank(matrix["signed_columns"], 5),
        }
        checks.update(
            {
                f"p{p}_external_hash": sha256(path) == EXPECTED_MATRIX_SHA256[p],
                f"p{p}_result_pointer": rows[p]["matrix_artifact_sha256"] == sha256(path),
                f"p{p}_internal_hash": bool(hashes["internal_hash_matches"]),
                f"p{p}_dimensions": (
                    int(matrix["rows"]) == expected["rows"]
                    and int(matrix["columns"]) == expected["columns"]
                    and int(matrix["nonzeros"]) == expected["nonzeros"]
                ),
                f"p{p}_support_hash": hashes["support_hash"] == expected["support_hash"],
                f"p{p}_signed_hash": hashes["signed_hash"] == expected["signed_hash"],
                f"p{p}_skeleton_hash": hashes["skeleton_hash"] == EXPECTED_SKELETON_HASH,
                f"p{p}_independent_ranks": ranks == expected["ranks"],
                f"p{p}_forward_certificate": reproduced_forward == stored_forward,
                f"p{p}_reverse_certificate": reproduced_reverse == stored_reverse,
                f"p{p}_alternate_order_rank": (
                    alternate_forward["bockstein_rank"] == expected["bockstein_rank"]
                    and alternate_reverse["bockstein_rank"] == expected["bockstein_rank"]
                ),
                f"p{p}_high_pivot_image_atom": all(
                    witness_image_atoms(profile) == {EXPECTED_HIGH_IMAGE_ATOM}
                    for profile in (stored_forward, stored_reverse)
                ),
                f"p{p}_low_pivot_image_atom": all(
                    witness_image_atoms(profile) == {EXPECTED_LOW_IMAGE_ATOM}
                    for profile in (alternate_forward, alternate_reverse)
                ),
                f"p{p}_representative_is_pivot_dependent": (
                    witness_image_atoms(stored_forward)
                    != witness_image_atoms(alternate_forward)
                ),
            }
        )
        audit_rows.append(
            {
                "p": p,
                "ranks": ranks,
                "kernel_dimension": alternate_forward["kernel_dimension"],
                "bockstein_rank": alternate_forward["bockstein_rank"],
                "high_pivot_image_atom": EXPECTED_HIGH_IMAGE_ATOM,
                "low_pivot_image_atom": EXPECTED_LOW_IMAGE_ATOM,
                "alternate_forward_class_hash": alternate_forward["bockstein_class_hash"],
                "alternate_reverse_class_hash": alternate_reverse["bockstein_class_hash"],
            }
        )

    certificate: dict[str, object] = {
        "experiment": "EXP-042",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "artifact_hashes": {
            "results": EXPECTED_RESULTS_SHA256,
            "matrices": {str(p): value for p, value in EXPECTED_MATRIX_SHA256.items()},
        },
        "checks": checks,
        "rows": audit_rows,
        "result": {
            "p1_status": results["p1_status"],
            "p2_status": results["p2_status"],
            "p3_status": results["p3_status"],
            "bockstein_ranks": {
                str(row["p"]): row["bockstein_rank"] for row in audit_rows
            },
            "high_pivot_image_atom": EXPECTED_HIGH_IMAGE_ATOM,
            "low_pivot_image_atom": EXPECTED_LOW_IMAGE_ATOM,
            "image_representative_is_pivot_dependent": True,
        },
        "scope": (
            "exact finite first-Bockstein ranks and pivot-dependent representative comparison "
            "through p=11; no rational rank upper bound, full Smith form, recurrence, or "
            "all-parameter theorem is claimed"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(json.dumps(certificate, indent=2))
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
