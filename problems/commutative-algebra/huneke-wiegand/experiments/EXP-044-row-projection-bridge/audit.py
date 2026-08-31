"""Independent low-pivot audit of EXP-044 row projections."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP042 = HERE.parent / "EXP-042-bockstein-normal-form"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_RUN_SHA256 = "39ed1d3538917d96282b22b35ac9cb1b0dc6083af879a6910f2098eb6f764517"
EXPECTED_RESULTS_SHA256 = "6766b6ca249f1b02ba9a83a6fb8434eea4e511172c982840fc3c6db6a192e886"
EXPECTED_MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    11: "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
}
DB_ATOM = '["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]'
KC0_ATOM = '["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]'
EXPECTED_SOURCE_BETA = {8: 3, 9: 4, 10: 5, 11: 7}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def bit_indices(value: int):
    while value:
        least = value & -value
        yield least.bit_length() - 1
        value ^= least


def modular_rank_low_pivot(columns: list[list[list[int]]], prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for entries in reversed(columns):
        vector = {int(row): int(value) % prime for row, value in entries if int(value) % prime}
        while vector:
            pivot = min(vector)
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


def reduce_columns_low(
    columns: list[int], column_count: int
) -> tuple[dict[int, int], list[int]]:
    pivots: dict[int, int] = {}
    combinations: dict[int, int] = {}
    kernel: list[int] = []
    for column in range(column_count - 1, -1, -1):
        vector = columns[column]
        combination = 1 << column
        while vector:
            least = vector & -vector
            pivot = least.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = vector
                combinations[pivot] = combination
                break
            vector ^= pivots[pivot]
            combination ^= combinations[pivot]
        if not vector:
            kernel.append(combination)
    return pivots, kernel


def quotient_reduce_low(vector: int, pivots: dict[int, int]) -> int:
    for pivot in sorted(pivots):
        if (vector >> pivot) & 1:
            vector ^= pivots[pivot]
    return vector


def bockstein_rank_low_pivot(
    signed_columns: list[list[list[int]]], row_count: int
) -> tuple[int, int]:
    column_bits = [sum(1 << int(row) for row, _ in entries) for entries in signed_columns]
    pivots, kernel = reduce_columns_low(column_bits, len(signed_columns))
    beta_pivots: dict[int, int] = {}
    for combination in kernel:
        boundary = [0] * row_count
        for column in bit_indices(combination):
            for row, sign in signed_columns[column]:
                boundary[int(row)] += int(sign)
        if any(value & 1 for value in boundary):
            raise AssertionError("projected kernel lift is not even")
        divided = sum(1 << row for row, value in enumerate(boundary) if (value // 2) & 1)
        vector = quotient_reduce_low(divided, pivots)
        while vector:
            least = vector & -vector
            pivot = least.bit_length() - 1
            if pivot not in beta_pivots:
                beta_pivots[pivot] = vector
                break
            vector ^= beta_pivots[pivot]
    return len(pivots), len(beta_pivots)


def atom_values(matrix: dict[str, object]) -> list[str]:
    table = matrix["row_atom_table"]
    return [table[int(index)] for index in matrix["row_atom_ids"]]


def independently_project(
    matrix: dict[str, object], name: str
) -> tuple[list[int], list[str], list[list[list[int]]]]:
    atoms = atom_values(matrix)

    def keep(atom: str) -> bool:
        if name == "drop_db":
            return atom != DB_ATOM
        if name == "drop_kc0":
            return atom != KC0_ATOM
        if name == "drop_both":
            return atom not in (DB_ATOM, KC0_ATOM)
        if name == "only_union":
            return atom in (DB_ATOM, KC0_ATOM)
        raise ValueError(name)

    kept_rows = [row for row, atom in enumerate(atoms) if keep(atom)]
    row_map = {original: projected for projected, original in enumerate(kept_rows)}
    signed_columns = [
        [[row_map[int(row)], int(sign)] for row, sign in entries if int(row) in row_map]
        for entries in matrix["signed_columns"]
    ]
    return kept_rows, [atoms[row] for row in kept_rows], signed_columns


def main() -> int:
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    without_hash = dict(results)
    internal_hash = without_hash.pop("artifact_hash")
    rows = {int(row["p"]): row for row in results["rows"]}
    checks: dict[str, bool] = {
        "run_hash": sha256(HERE / "run.py") == EXPECTED_RUN_SHA256,
        "results_external_hash": sha256(RESULTS) == EXPECTED_RESULTS_SHA256,
        "results_internal_hash": digest(without_hash) == internal_hash,
        "parameter_coverage": set(rows) == set(EXPECTED_MATRIX_SHA256),
        "primary_complete": results["status"] == "COMPLETE",
        "primary_verdict": (
            results["p1_status"] == "PASS_FINITE"
            and results["p2_status"] == "REFUTED"
            and results["p3_status"] == "PASS_FINITE"
        ),
    }
    audit_rows: list[dict[str, object]] = []
    for p in sorted(EXPECTED_MATRIX_SHA256):
        matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        stored_row = rows[p]
        source_beta = int(matrix["bockstein"]["forward"]["bockstein_rank"])
        checks[f"p{p}_matrix_hash"] = sha256(matrix_path) == EXPECTED_MATRIX_SHA256[p]
        checks[f"p{p}_source_beta"] = source_beta == EXPECTED_SOURCE_BETA[p]
        audit_projections: dict[str, object] = {}
        for name in ("drop_db", "drop_kc0", "drop_both", "only_union"):
            kept_rows, atoms, signed_columns = independently_project(matrix, name)
            stored = stored_row["projections"][name]
            ranks = {
                str(prime): modular_rank_low_pivot(signed_columns, prime)
                for prime in (2, 3, 5)
            }
            rank_two, beta_rank = bockstein_rank_low_pivot(signed_columns, len(kept_rows))
            projection_hash = digest(
                {
                    "kept_rows": kept_rows,
                    "signed_columns": signed_columns,
                    "row_atoms": atoms,
                }
            )
            prefix = f"p{p}_{name}"
            checks.update(
                {
                    f"{prefix}_dimensions": (
                        int(stored["rows"]) == len(kept_rows)
                        and int(stored["columns"]) == len(signed_columns)
                    ),
                    f"{prefix}_nonzeros": int(stored["nonzeros"])
                    == sum(map(len, signed_columns)),
                    f"{prefix}_atom_counts": stored["kept_row_atom_counts"]
                    == dict(sorted(Counter(atoms).items())),
                    f"{prefix}_projection_hash": stored["projection_hash"] == projection_hash,
                    f"{prefix}_opposite_ranks": stored["ranks"] == ranks,
                    f"{prefix}_rank_two_consistency": rank_two == ranks["2"],
                    f"{prefix}_opposite_bockstein": beta_rank
                    == int(stored["bockstein"]["forward"]["bockstein_rank"]),
                    f"{prefix}_zero_gap": ranks["2"] == ranks["3"] == ranks["5"],
                    f"{prefix}_zero_bockstein": beta_rank == 0,
                }
            )
            audit_projections[name] = {
                "rows": len(kept_rows),
                "nonzeros": sum(map(len, signed_columns)),
                "ranks": ranks,
                "bockstein_rank": beta_rank,
                "projection_hash": projection_hash,
            }
        audit_rows.append(
            {
                "p": p,
                "source_bockstein_rank": source_beta,
                "target_atom_row_counts": stored_row["target_atom_row_counts"],
                "projections": audit_projections,
            }
        )
        print(f"audit p={p} complete", flush=True)

    certificate: dict[str, object] = {
        "experiment": "EXP-044",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "artifact_hashes": {
            "run": EXPECTED_RUN_SHA256,
            "results": EXPECTED_RESULTS_SHA256,
            "matrices": {str(p): value for p, value in EXPECTED_MATRIX_SHA256.items()},
        },
        "checks": checks,
        "rows": audit_rows,
        "result": {
            "p1_status": results["p1_status"],
            "p2_status": results["p2_status"],
            "p3_status": results["p3_status"],
            "interpretation": (
                "each marked atom is necessary, their union is insufficient, and the finite "
                "Bockstein therefore belongs to a larger signed circuit"
            ),
        },
        "scope": (
            "exact finite row-projection diagnostic for p=8,...,11; no integral equivalence, "
            "recurrence, or all-parameter theorem is claimed"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(json.dumps({"status": certificate["status"], "checks": len(checks)}, indent=2))
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
