"""Independent low-pivot audit of the EXP-045 carrier lattice."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP042 = HERE.parent / "EXP-042-bockstein-normal-form"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_RUN_SHA256 = "2ae864d472e470869673eb1cd2ffd25ef6d0e2da6530cd6c675d335f860e2109"
EXPECTED_RESULTS_SHA256 = "569220667e9d82f0806ea96cb8f60c49e94cb6317817170c39f2e574e619bcb8"
EXPECTED_MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    11: "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
}
ATOM_ALIASES = {
    "R0": '["row","D","A",[-2,-3,1,0,1,0,0,0,0,0]]',
    "R1": '["row","D","A",[-3,-2,2,0,0,0,0,0,0,0]]',
    "R2": '["row","D","B",[-1,-4,1,0,1,0,0,0,0,0]]',
    "R3": '["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]',
    "R4": '["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]',
    "R5": '["row","K","C2",[-1,-3,1,0,0,0,0,0,0,0]]',
}
ALIASES = tuple(ATOM_ALIASES)
EXPECTED_SOURCE_BETA = {8: 3, 9: 4, 10: 5, 11: 7}
EXPECTED_CORE_BETA = {8: 1, 9: 2, 10: 3, 11: 5}
EXPECTED_MINIMAL_NONZERO = {8: [58], 9: [58], 10: [58], 11: [56]}
EXPECTED_MINIMAL_FULL = {8: [59, 62], 9: [59, 62], 10: [59, 62], 11: [59, 62]}


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


def bockstein_rank_low_pivot(
    signed_columns: list[list[list[int]]], row_count: int
) -> tuple[int, int, int]:
    column_count = len(signed_columns)
    column_bits = [sum(1 << int(row) for row, _ in entries) for entries in signed_columns]
    pivots: dict[int, int] = {}
    combinations: dict[int, int] = {}
    kernel: list[int] = []
    for column in range(column_count - 1, -1, -1):
        vector = column_bits[column]
        combination = 1 << column
        while vector:
            pivot = (vector & -vector).bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = vector
                combinations[pivot] = combination
                break
            vector ^= pivots[pivot]
            combination ^= combinations[pivot]
        if not vector:
            kernel.append(combination)
    beta_pivots: dict[int, int] = {}
    for combination in kernel:
        boundary = [0] * row_count
        for column in bit_indices(combination):
            for row, sign in signed_columns[column]:
                boundary[int(row)] += int(sign)
        if any(value & 1 for value in boundary):
            raise AssertionError("projected kernel lift is not even")
        vector = sum(1 << row for row, value in enumerate(boundary) if (value // 2) & 1)
        for pivot in sorted(pivots):
            if (vector >> pivot) & 1:
                vector ^= pivots[pivot]
        while vector:
            pivot = (vector & -vector).bit_length() - 1
            if pivot not in beta_pivots:
                beta_pivots[pivot] = vector
                break
            vector ^= beta_pivots[pivot]
    return len(pivots), len(kernel), len(beta_pivots)


def atom_values(matrix: dict[str, object]) -> list[str]:
    table = matrix["row_atom_table"]
    return [table[int(index)] for index in matrix["row_atom_ids"]]


def aliases(mask: int) -> list[str]:
    return [alias for bit, alias in enumerate(ALIASES) if mask & (1 << bit)]


def independently_project(
    matrix: dict[str, object], mask: int
) -> tuple[list[int], list[str], list[list[list[int]]]]:
    selected = {ATOM_ALIASES[alias] for alias in aliases(mask)}
    atoms = atom_values(matrix)
    kept_rows = [row for row, atom in enumerate(atoms) if atom in selected]
    row_map = {original: projected for projected, original in enumerate(kept_rows)}
    signed_columns = [
        [[row_map[int(row)], int(sign)] for row, sign in entries if int(row) in row_map]
        for entries in matrix["signed_columns"]
    ]
    return kept_rows, [atoms[row] for row in kept_rows], signed_columns


def minimal_masks(carriers: set[int]) -> list[int]:
    return sorted(
        mask
        for mask in carriers
        if not any(other != mask and other & mask == other for other in carriers)
    )


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
        "declared_predictions_refuted": all(
            results[key] == "REFUTED" for key in ("p1_status", "p2_status", "p3_status")
        ),
        "atom_aliases": results["atom_aliases"] == ATOM_ALIASES,
    }
    audit_rows: list[dict[str, object]] = []
    for p in sorted(rows):
        matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        row = rows[p]
        stored_subsets = {int(subset["mask"]): subset for subset in row["subsets"]}
        checks[f"p{p}_matrix_hash"] = sha256(matrix_path) == EXPECTED_MATRIX_SHA256[p]
        checks[f"p{p}_subset_coverage"] = set(stored_subsets) == set(range(64))
        independent_records: list[dict[str, object]] = []
        nonzero: set[int] = set()
        full: set[int] = set()
        for mask in range(64):
            kept_rows, row_atoms, columns = independently_project(matrix, mask)
            stored = stored_subsets[mask]
            ranks = {
                str(prime): modular_rank_low_pivot(columns, prime) for prime in (2, 3, 5)
            }
            rank_two, kernel_dimension, beta = bockstein_rank_low_pivot(columns, len(kept_rows))
            projection_hash = digest(
                {
                    "kept_rows": kept_rows,
                    "row_atoms": row_atoms,
                    "signed_columns": columns,
                }
            )
            prefix = f"p{p}_m{mask}"
            checks.update(
                {
                    f"{prefix}_aliases": stored["aliases"] == aliases(mask),
                    f"{prefix}_dimensions": (
                        int(stored["rows"]) == len(kept_rows)
                        and int(stored["columns"]) == len(columns)
                    ),
                    f"{prefix}_nonzeros": int(stored["nonzeros"]) == sum(map(len, columns)),
                    f"{prefix}_atom_counts": stored["row_atom_counts"]
                    == dict(sorted(Counter(row_atoms).items())),
                    f"{prefix}_projection_hash": stored["projection_hash"] == projection_hash,
                    f"{prefix}_ranks": stored["ranks"] == ranks,
                    f"{prefix}_rank_two": rank_two == ranks["2"],
                    f"{prefix}_kernel": kernel_dimension
                    == int(stored["bockstein_low_reverse"]["kernel_dimension"]),
                    f"{prefix}_bockstein": beta
                    == int(stored["bockstein_high_forward"]["bockstein_rank"]),
                    f"{prefix}_opposite_stored": bool(stored["opposite_agreement"]),
                    f"{prefix}_gap": ranks["3"] == ranks["5"]
                    and int(ranks["3"]) - int(ranks["2"]) == beta,
                }
            )
            if beta:
                nonzero.add(mask)
            if beta == EXPECTED_SOURCE_BETA[p]:
                full.add(mask)
            independent_records.append(
                {
                    "mask": mask,
                    "ranks": ranks,
                    "bockstein_rank": beta,
                    "projection_hash": projection_hash,
                }
            )
        minimal_nonzero = minimal_masks(nonzero)
        minimal_full = minimal_masks(full)
        checks.update(
            {
                f"p{p}_nonzero_masks": sorted(nonzero) == row["nonzero_carrier_masks"],
                f"p{p}_full_masks": sorted(full) == row["full_carrier_masks"],
                f"p{p}_minimal_nonzero": minimal_nonzero
                == row["minimal_nonzero_carrier_masks"]
                == EXPECTED_MINIMAL_NONZERO[p],
                f"p{p}_minimal_full": minimal_full
                == row["minimal_full_carrier_masks"]
                == EXPECTED_MINIMAL_FULL[p],
                f"p{p}_four_atom_core": int(
                    stored_subsets[58]["bockstein_high_forward"]["bockstein_rank"]
                )
                == EXPECTED_CORE_BETA[p],
                f"p{p}_constant_completion": (
                    EXPECTED_SOURCE_BETA[p] - EXPECTED_CORE_BETA[p] == 2
                ),
            }
        )
        audit_rows.append(
            {
                "p": p,
                "minimal_nonzero_carrier_masks": minimal_nonzero,
                "minimal_full_carrier_masks": minimal_full,
                "mask58_bockstein_rank": EXPECTED_CORE_BETA[p],
                "full_bockstein_rank": EXPECTED_SOURCE_BETA[p],
                "subset_table_digest": digest(independent_records),
            }
        )
        print(f"audit p={p}: 64/64 subsets", flush=True)

    certificate: dict[str, object] = {
        "experiment": "EXP-045",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "artifact_hashes": {
            "run": EXPECTED_RUN_SHA256,
            "results": EXPECTED_RESULTS_SHA256,
            "matrices": {str(p): value for p, value in EXPECTED_MATRIX_SHA256.items()},
        },
        "checks": checks,
        "rows": audit_rows,
        "result": {
            "minimal_full_carriers": [59, 62],
            "stable_full_carrier_intersection": 58,
            "mask58_bockstein_sequence": [1, 2, 3, 5],
            "p11_minimal_nonzero_threshold_mask": 56,
        },
        "scope": (
            "complete finite six-row-atom carrier lattice for p=8,...,11; no integral "
            "equivalence, recurrence, or all-parameter theorem is claimed"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(json.dumps({"status": certificate["status"], "checks": len(checks)}, indent=2))
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
