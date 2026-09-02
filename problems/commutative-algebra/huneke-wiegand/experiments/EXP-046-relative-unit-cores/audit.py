"""Independent column-first audit of the EXP-046 relative unit cores."""

from __future__ import annotations

import hashlib
import heapq
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP042 = HERE.parent / "EXP-042-bockstein-normal-form"
EXP045 = HERE.parent / "EXP-045-row-atom-carrier-lattice"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_RUN_SHA256 = "60d003d158349ef29cfd7cec476cad83e0af8871bc09d385b1284f62a651b14a"
EXPECTED_RESULTS_SHA256 = (
    "1e78f650ef041eb1f45b4e979ea90a78709ef59ff443e57613edbc9cc6ea15b0"
)
EXPECTED_EXP045_SHA256 = (
    "569220667e9d82f0806ea96cb8f60c49e94cb6317817170c39f2e574e619bcb8"
)
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
MASKS = (56, 58, 59, 62)
EXPECTED_DEFECTS = {
    8: {56: [], 58: [1], 59: [3], 62: [3]},
    9: {56: [], 58: [2], 59: [4], 62: [4]},
    10: {56: [], 58: [3], 59: [5], 62: [5]},
    11: {56: [1], 58: [5], 59: [7], 62: [7]},
}


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
        vector = {
            int(row): int(value) % prime
            for row, value in entries
            if int(value) % prime
        }
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
    columns: list[list[list[int]]], row_count: int
) -> tuple[int, int, int]:
    column_bits = [sum(1 << int(row) for row, _ in entries) for entries in columns]
    pivots: dict[int, int] = {}
    combinations: dict[int, int] = {}
    kernel: list[int] = []
    for column in range(len(columns) - 1, -1, -1):
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
            for row, sign in columns[column]:
                boundary[int(row)] += int(sign)
        if any(value & 1 for value in boundary):
            raise AssertionError("audited kernel lift is not even")
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


def atom_values(matrix: dict[str, object], side: str) -> list[str]:
    table = matrix[f"{side}_atom_table"]
    return [table[int(index)] for index in matrix[f"{side}_atom_ids"]]


def aliases(mask: int) -> list[str]:
    return [alias for bit, alias in enumerate(ALIASES) if mask & (1 << bit)]


def project_matrix(matrix: dict[str, object], mask: int) -> dict[str, object]:
    selected = {ATOM_ALIASES[alias] for alias in aliases(mask)}
    all_row_atoms = atom_values(matrix, "row")
    kept_rows = [row for row, atom in enumerate(all_row_atoms) if atom in selected]
    row_map = {original: projected for projected, original in enumerate(kept_rows)}
    columns = [
        [[row_map[int(row)], int(sign)] for row, sign in entries if int(row) in row_map]
        for entries in matrix["signed_columns"]
    ]
    return {
        "columns": columns,
        "row_atoms": [all_row_atoms[row] for row in kept_rows],
        "column_atoms": atom_values(matrix, "column"),
    }


def component_record(
    *,
    columns: list[list[list[int]]],
    rows: list[int],
    column_ids: list[int],
    row_atoms: list[str],
    column_atoms: list[str],
) -> dict[str, object]:
    row_map = {original: local for local, original in enumerate(rows)}
    local_columns = [
        [
            [row_map[int(row)], int(sign)]
            for row, sign in columns[column]
            if int(row) in row_map
        ]
        for column in column_ids
    ]
    ranks = {
        str(prime): modular_rank_low_pivot(local_columns, prime) for prime in (2, 3, 5)
    }
    rank_two, kernel_dimension, beta = bockstein_rank_low_pivot(
        local_columns, len(rows)
    )
    local_row_atoms = [row_atoms[row] for row in rows]
    local_column_atoms = [column_atoms[column] for column in column_ids]
    aliases_by_atom = {atom: alias for alias, atom in ATOM_ALIASES.items()}
    row_aliases = sorted({aliases_by_atom[atom] for atom in local_row_atoms})
    normalized_aliases = sorted(
        {"RX" if alias in ("R0", "R2") else alias for alias in row_aliases}
    )
    semantic_support_hash = digest(
        {
            "normalized_completion_aliases": normalized_aliases,
            "column_atoms": sorted(set(local_column_atoms)),
        }
    )
    return {
        "rows": len(rows),
        "columns": len(column_ids),
        "nonzeros": sum(map(len, local_columns)),
        "ranks": ranks,
        "rank_two": rank_two,
        "kernel_dimension": kernel_dimension,
        "bockstein_rank": beta,
        "semantic_support_hash": semantic_support_hash,
        "row_aliases": row_aliases,
        "row_atom_counts": dict(sorted(Counter(local_row_atoms).items())),
        "column_atom_counts": dict(sorted(Counter(local_column_atoms).items())),
    }


def peel_column_first(projected: dict[str, object]) -> dict[str, object]:
    """Peel maximum-index column leaves first, independently of the runner."""
    columns = projected["columns"]
    row_count = len(projected["row_atoms"])
    column_rows = [[int(row) for row, _ in entries] for entries in columns]
    row_columns: list[list[int]] = [[] for _ in range(row_count)]
    for column, rows in enumerate(column_rows):
        for row in rows:
            row_columns[row].append(column)
    row_degrees = list(map(len, row_columns))
    column_degrees = list(map(len, column_rows))
    active_rows = bytearray([1]) * row_count
    active_columns = bytearray([1]) * len(columns)
    row_heap = [-row for row, degree in enumerate(row_degrees) if degree == 1]
    column_heap = [
        -column for column, degree in enumerate(column_degrees) if degree == 1
    ]
    heapq.heapify(row_heap)
    heapq.heapify(column_heap)
    cancellations = 0

    def pop_leaf(heap: list[int], degrees: list[int], active: bytearray) -> int | None:
        while heap:
            vertex = -heapq.heappop(heap)
            if active[vertex] and degrees[vertex] == 1:
                return vertex
        return None

    def cancel(row: int, column: int) -> None:
        nonlocal cancellations
        cancellations += 1
        active_rows[row] = 0
        active_columns[column] = 0
        for adjacent_column in row_columns[row]:
            if active_columns[adjacent_column]:
                column_degrees[adjacent_column] -= 1
                if column_degrees[adjacent_column] == 1:
                    heapq.heappush(column_heap, -adjacent_column)
        for adjacent_row in column_rows[column]:
            if active_rows[adjacent_row]:
                row_degrees[adjacent_row] -= 1
                if row_degrees[adjacent_row] == 1:
                    heapq.heappush(row_heap, -adjacent_row)
        row_degrees[row] = 0
        column_degrees[column] = 0

    while row_heap or column_heap:
        column = pop_leaf(column_heap, column_degrees, active_columns)
        if column is not None:
            neighbors = [row for row in column_rows[column] if active_rows[row]]
            if len(neighbors) != 1:
                raise AssertionError("audit column leaf degree mismatch")
            cancel(neighbors[0], column)
            continue
        row = pop_leaf(row_heap, row_degrees, active_rows)
        if row is None:
            break
        neighbors = [column for column in row_columns[row] if active_columns[column]]
        if len(neighbors) != 1:
            raise AssertionError("audit row leaf degree mismatch")
        cancel(row, neighbors[0])

    core_rows = {
        row for row in range(row_count) if active_rows[row] and row_degrees[row] > 0
    }
    core_columns = {
        column
        for column in range(len(columns))
        if active_columns[column] and column_degrees[column] > 0
    }
    unseen_rows = set(core_rows)
    components: list[dict[str, object]] = []
    while unseen_rows:
        rows_here: set[int] = set()
        columns_here: set[int] = set()
        stack = [max(unseen_rows)]
        while stack:
            row = stack.pop()
            if row in rows_here:
                continue
            rows_here.add(row)
            unseen_rows.discard(row)
            for column in row_columns[row]:
                if column not in core_columns or column in columns_here:
                    continue
                columns_here.add(column)
                stack.extend(
                    adjacent_row
                    for adjacent_row in column_rows[column]
                    if adjacent_row in core_rows and adjacent_row not in rows_here
                )
        components.append(
            component_record(
                columns=columns,
                rows=sorted(rows_here),
                column_ids=sorted(columns_here),
                row_atoms=projected["row_atoms"],
                column_atoms=projected["column_atoms"],
            )
        )
    summary = sorted(
        [
            [
                component["rows"],
                component["columns"],
                component["nonzeros"],
                component["ranks"]["2"],
                component["ranks"]["3"],
                component["ranks"]["5"],
                component["bockstein_rank"],
            ]
            for component in components
        ]
    )
    return {
        "cancellations": cancellations,
        "free_rows": sum(
            bool(active_rows[row]) and row_degrees[row] == 0 for row in range(row_count)
        ),
        "zero_columns": sum(
            bool(active_columns[column]) and column_degrees[column] == 0
            for column in range(len(columns))
        ),
        "core_rows": len(core_rows),
        "core_columns": len(core_columns),
        "components": components,
        "component_summary": summary,
        "positive_defects": sorted(
            int(component["bockstein_rank"])
            for component in components
            if int(component["bockstein_rank"]) > 0
        ),
    }


def main() -> int:
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    without_hash = dict(results)
    internal_hash = without_hash.pop("artifact_hash")
    stored_rows = {int(row["p"]): row for row in results["rows"]}
    exp045 = json.loads(
        (EXP045 / "artifacts" / "results.json").read_text(encoding="utf-8")
    )
    source_rows = {int(row["p"]): row for row in exp045["rows"]}
    checks: dict[str, bool] = {
        "run_hash": sha256(HERE / "run.py") == EXPECTED_RUN_SHA256,
        "results_external_hash": sha256(RESULTS) == EXPECTED_RESULTS_SHA256,
        "results_internal_hash": digest(without_hash) == internal_hash,
        "exp045_hash": sha256(EXP045 / "artifacts" / "results.json")
        == EXPECTED_EXP045_SHA256,
        "parameter_coverage": set(stored_rows) == set(EXPECTED_MATRIX_SHA256),
        "primary_complete": results["status"] == "COMPLETE",
        "declared_statuses": (
            results["p1_status"] == "REFUTED"
            and results["p2_status"] == "REFUTED"
            and results["p3_status"] == "PASS_FINITE"
        ),
        "atom_aliases": results["atom_aliases"] == ATOM_ALIASES,
    }
    audit_rows: list[dict[str, object]] = []
    mask56_supports: dict[int, list[str]] = {}
    for p in sorted(stored_rows):
        matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        stored = stored_rows[p]
        source = {
            int(subset["mask"]): subset for subset in source_rows[p]["subsets"]
        }
        checks[f"p{p}_matrix_hash"] = sha256(matrix_path) == EXPECTED_MATRIX_SHA256[p]
        audit_masks: dict[str, object] = {}
        for mask in MASKS:
            projected = project_matrix(matrix, mask)
            peeled = peel_column_first(projected)
            stored_record = stored["masks"][str(mask)]
            stored_reverse = stored_record["reverse"]
            source_record = source[mask]
            prefix = f"p{p}_m{mask}"
            semantic_supports = sorted(
                str(component["semantic_support_hash"])
                for component in peeled["components"]
            )
            stored_supports = sorted(
                str(component["semantic_support_hash"])
                for component in stored_reverse["components"]
            )
            recomposed_ranks = {
                prime: int(peeled["cancellations"])
                + sum(
                    int(component["ranks"][prime])
                    for component in peeled["components"]
                )
                for prime in ("2", "3", "5")
            }
            recomposed_beta = sum(
                int(component["bockstein_rank"])
                for component in peeled["components"]
            )
            checks.update(
                {
                    f"{prefix}_dimensions": (
                        len(projected["row_atoms"]) == int(source_record["rows"])
                        and len(projected["columns"])
                        == int(source_record["columns"])
                    ),
                    f"{prefix}_nonzeros": sum(map(len, projected["columns"]))
                    == int(source_record["nonzeros"]),
                    f"{prefix}_cancellations": int(peeled["cancellations"])
                    == int(stored_reverse["cancellations"]),
                    f"{prefix}_core_dimensions": (
                        int(peeled["core_rows"]) == int(stored_reverse["core_rows"])
                        and int(peeled["core_columns"])
                        == int(stored_reverse["core_columns"])
                    ),
                    f"{prefix}_free_zero": (
                        int(peeled["free_rows"]) == int(stored_reverse["free_rows"])
                        and int(peeled["zero_columns"])
                        == int(stored_reverse["zero_columns"])
                    ),
                    f"{prefix}_component_summary": peeled["component_summary"]
                    == stored_reverse["component_summary"],
                    f"{prefix}_semantic_supports": semantic_supports
                    == stored_supports,
                    f"{prefix}_defects": peeled["positive_defects"]
                    == stored_record["positive_defects"]
                    == EXPECTED_DEFECTS[p][mask],
                    f"{prefix}_recompose_ranks": recomposed_ranks
                    == source_record["ranks"],
                    f"{prefix}_recompose_beta": recomposed_beta
                    == int(source_record["bockstein_high_forward"]["bockstein_rank"]),
                    f"{prefix}_single_core": len(peeled["components"]) == 1,
                    f"{prefix}_component_rank_checks": all(
                        int(component["rank_two"])
                        == int(component["ranks"]["2"])
                        and int(component["ranks"]["3"])
                        == int(component["ranks"]["5"])
                        and int(component["ranks"]["3"])
                        - int(component["ranks"]["2"])
                        == int(component["bockstein_rank"])
                        for component in peeled["components"]
                    ),
                }
            )
            if mask in (59, 62):
                checks[f"{prefix}_no_leaf_cancellation"] = (
                    int(peeled["cancellations"]) == 0
                )
            if mask == 56:
                mask56_supports[p] = semantic_supports
            audit_masks[str(mask)] = {
                "cancellations": peeled["cancellations"],
                "core_rows": peeled["core_rows"],
                "core_columns": peeled["core_columns"],
                "component_count": len(peeled["components"]),
                "positive_defects": peeled["positive_defects"],
                "semantic_support_hashes": semantic_supports,
            }
            print(f"audit p={p} mask={mask}", flush=True)
        audit_rows.append({"p": p, "masks": audit_masks})

    checks["mask56_persistent_semantic_support"] = (
        len({tuple(values) for values in mask56_supports.values()}) == 1
    )
    checks["constant_two_completion_defect"] = all(
        EXPECTED_DEFECTS[p][59][0] - EXPECTED_DEFECTS[p][58][0] == 2
        and EXPECTED_DEFECTS[p][62][0] - EXPECTED_DEFECTS[p][58][0] == 2
        for p in EXPECTED_DEFECTS
    )
    certificate: dict[str, object] = {
        "experiment": "EXP-046",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "audit_route": (
            "independent low-pivot ranks and Bockstein with maximum-index "
            "column-first unit peeling"
        ),
        "artifact_hashes": {
            "run": EXPECTED_RUN_SHA256,
            "results": EXPECTED_RESULTS_SHA256,
            "exp045_results": EXPECTED_EXP045_SHA256,
            "matrices": {str(p): value for p, value in EXPECTED_MATRIX_SHA256.items()},
        },
        "checks": checks,
        "rows": audit_rows,
        "result": {
            "p1_status": "REFUTED",
            "p2_status": "REFUTED",
            "p3_status": "PASS_FINITE",
            "minimal_full_carriers_have_no_unit_leaf": [59, 62],
            "all_tested_residuals_have_one_connected_component": True,
            "mask56_threshold_occurs_in_persistent_semantic_support": True,
        },
        "scope": (
            "finite p=8,...,11 exact unit-core obstruction; no all-parameter "
            "recurrence or Huneke-Wiegand theorem is claimed"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(json.dumps({"status": certificate["status"], "checks": len(checks)}, indent=2))
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
