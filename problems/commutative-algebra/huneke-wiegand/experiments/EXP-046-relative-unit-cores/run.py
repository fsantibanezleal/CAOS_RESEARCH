"""EXP-046 exact unit-leaf cores of the stable row carriers."""

from __future__ import annotations

import argparse
import hashlib
import heapq
import importlib.util
import json
from collections import Counter
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXP042 = HERE.parent / "EXP-042-bockstein-normal-form"
EXP045 = HERE.parent / "EXP-045-row-atom-carrier-lattice"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
MASKS = (56, 58, 59, 62)
ATOM_ALIASES = {
    "R0": '["row","D","A",[-2,-3,1,0,1,0,0,0,0,0]]',
    "R1": '["row","D","A",[-3,-2,2,0,0,0,0,0,0,0]]',
    "R2": '["row","D","B",[-1,-4,1,0,1,0,0,0,0,0]]',
    "R3": '["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]',
    "R4": '["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]',
    "R5": '["row","K","C2",[-1,-3,1,0,0,0,0,0,0,0]]',
}
ALIASES = tuple(ATOM_ALIASES)
PREMISES = {
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP042 / "artifacts" / "matrix-p8.json": (
        "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff"
    ),
    EXP042 / "artifacts" / "matrix-p9.json": (
        "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c"
    ),
    EXP042 / "artifacts" / "matrix-p10.json": (
        "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d"
    ),
    EXP042 / "artifacts" / "matrix-p11.json": (
        "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9"
    ),
    EXP045 / "artifacts" / "results.json": (
        "569220667e9d82f0806ea96cb8f60c49e94cb6317817170c39f2e574e619bcb8"
    ),
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


def verify_premises() -> dict[str, str]:
    actual = {str(path.relative_to(HERE.parent)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(HERE.parent)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def bit_indices(value: int):
    while value:
        least = value & -value
        yield least.bit_length() - 1
        value ^= least


def bockstein_rank(signed_columns: list[list[list[int]]], row_count: int) -> dict[str, int]:
    column_bits = [sum(1 << int(row) for row, _ in entries) for entries in signed_columns]
    pivots: dict[int, int] = {}
    combinations: dict[int, int] = {}
    kernel: list[int] = []
    for column, original in enumerate(column_bits):
        vector = original
        combination = 1 << column
        while vector:
            pivot = vector.bit_length() - 1
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
            raise AssertionError("unit-core kernel lift is not even")
        vector = sum(1 << row for row, value in enumerate(boundary) if (value // 2) & 1)
        for pivot in sorted(pivots, reverse=True):
            if (vector >> pivot) & 1:
                vector ^= pivots[pivot]
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in beta_pivots:
                beta_pivots[pivot] = vector
                break
            vector ^= beta_pivots[pivot]
    return {
        "rank_mod_two": len(pivots),
        "kernel_dimension": len(kernel),
        "bockstein_rank": len(beta_pivots),
    }


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
    signed_columns = [
        [[row_map[int(row)], int(sign)] for row, sign in entries if int(row) in row_map]
        for entries in matrix["signed_columns"]
    ]
    return {
        "signed_columns": signed_columns,
        "row_atoms": [all_row_atoms[row] for row in kept_rows],
        "column_atoms": atom_values(matrix, "column"),
        "kept_rows": kept_rows,
    }


def pop_leaf(
    heap: list[int], degrees: list[int], active: bytearray, reverse: bool
) -> int | None:
    while heap:
        encoded = heapq.heappop(heap)
        vertex = -encoded if reverse else encoded
        if active[vertex] and degrees[vertex] == 1:
            return vertex
    return None


def component_record(
    *,
    original_columns: list[list[list[int]]],
    rows: list[int],
    columns: list[int],
    row_atoms: list[str],
    column_atoms: list[str],
    exp042: ModuleType,
    exp037: ModuleType,
) -> dict[str, object]:
    row_map = {original: local for local, original in enumerate(rows)}
    local_columns = [
        [[row_map[int(row)], int(sign)] for row, sign in original_columns[column]]
        for column in columns
    ]
    local_row_atoms = [row_atoms[row] for row in rows]
    local_column_atoms = [column_atoms[column] for column in columns]
    ranks = exp042.rank_fields(exp037, local_columns)
    beta = bockstein_rank(local_columns, len(rows))
    defect = int(ranks["3"]) - int(ranks["2"])
    alias_by_atom = {value: alias for alias, value in ATOM_ALIASES.items()}
    row_aliases = sorted({alias_by_atom[atom] for atom in local_row_atoms})
    normalized_aliases = ["RX" if alias in ("R0", "R2") else alias for alias in row_aliases]
    atom_set_signature = {
        "row_aliases": row_aliases,
        "normalized_completion_aliases": sorted(set(normalized_aliases)),
        "column_atoms": sorted(set(local_column_atoms)),
    }
    return {
        "rows": len(rows),
        "columns": len(columns),
        "nonzeros": sum(map(len, local_columns)),
        "ranks": ranks,
        "odd_minus_two_rank": defect,
        "bockstein": beta,
        "rank_gap_matches_bockstein": defect == beta["bockstein_rank"],
        "row_atom_counts": dict(sorted(Counter(local_row_atoms).items())),
        "column_atom_counts": dict(sorted(Counter(local_column_atoms).items())),
        "atom_set_signature": atom_set_signature,
        "normalized_signature_hash": digest(
            {
                "normalized_completion_aliases": atom_set_signature[
                    "normalized_completion_aliases"
                ],
                "column_atoms": atom_set_signature["column_atoms"],
                "defect": defect,
            }
        ),
        "support_hash": digest(
            [[int(row) for row, _ in entries] for entries in local_columns]
        ),
        "signed_hash": digest(local_columns),
    }


def peel_unit_core(
    *,
    projected: dict[str, object],
    reverse: bool,
    exp042: ModuleType,
    exp037: ModuleType,
) -> dict[str, object]:
    signed_columns = projected["signed_columns"]
    row_atoms = projected["row_atoms"]
    column_atoms = projected["column_atoms"]
    row_count = len(row_atoms)
    column_count = len(signed_columns)
    column_rows = [[int(row) for row, _ in entries] for entries in signed_columns]
    row_columns: list[list[int]] = [[] for _ in range(row_count)]
    for column, rows in enumerate(column_rows):
        for row in rows:
            row_columns[row].append(column)
    row_degrees = list(map(len, row_columns))
    column_degrees = list(map(len, column_rows))
    active_rows = bytearray([1]) * row_count
    active_columns = bytearray([1]) * column_count
    encode = (lambda value: -value) if reverse else (lambda value: value)
    row_heap = [encode(row) for row, degree in enumerate(row_degrees) if degree == 1]
    column_heap = [
        encode(column) for column, degree in enumerate(column_degrees) if degree == 1
    ]
    heapq.heapify(row_heap)
    heapq.heapify(column_heap)
    cancelled_pairs: list[list[int]] = []

    def cancel(row: int, column: int) -> None:
        active_rows[row] = 0
        active_columns[column] = 0
        cancelled_pairs.append([row, column])
        for adjacent_column in row_columns[row]:
            if active_columns[adjacent_column]:
                column_degrees[adjacent_column] -= 1
                if column_degrees[adjacent_column] == 1:
                    heapq.heappush(column_heap, encode(adjacent_column))
        for adjacent_row in column_rows[column]:
            if active_rows[adjacent_row]:
                row_degrees[adjacent_row] -= 1
                if row_degrees[adjacent_row] == 1:
                    heapq.heappush(row_heap, encode(adjacent_row))
        row_degrees[row] = 0
        column_degrees[column] = 0

    while row_heap or column_heap:
        if reverse:
            column = pop_leaf(column_heap, column_degrees, active_columns, reverse)
            if column is not None:
                neighbors = [row for row in column_rows[column] if active_rows[row]]
                if len(neighbors) != 1:
                    raise AssertionError("column leaf degree mismatch")
                cancel(neighbors[0], column)
                continue
            row = pop_leaf(row_heap, row_degrees, active_rows, reverse)
            if row is None:
                break
            neighbors = [column for column in row_columns[row] if active_columns[column]]
            if len(neighbors) != 1:
                raise AssertionError("row leaf degree mismatch")
            cancel(row, neighbors[0])
        else:
            row = pop_leaf(row_heap, row_degrees, active_rows, reverse)
            if row is not None:
                neighbors = [column for column in row_columns[row] if active_columns[column]]
                if len(neighbors) != 1:
                    raise AssertionError("row leaf degree mismatch")
                cancel(row, neighbors[0])
                continue
            column = pop_leaf(column_heap, column_degrees, active_columns, reverse)
            if column is None:
                break
            neighbors = [row for row in column_rows[column] if active_rows[row]]
            if len(neighbors) != 1:
                raise AssertionError("column leaf degree mismatch")
            cancel(neighbors[0], column)

    core_rows = {
        row for row in range(row_count) if active_rows[row] and row_degrees[row] > 0
    }
    core_columns = {
        column
        for column in range(column_count)
        if active_columns[column] and column_degrees[column] > 0
    }
    components: list[dict[str, object]] = []
    unseen_rows = set(core_rows)
    while unseen_rows:
        seed = max(unseen_rows) if reverse else min(unseen_rows)
        rows_here: set[int] = set()
        columns_here: set[int] = set()
        row_stack = [seed]
        while row_stack:
            row = row_stack.pop()
            if row in rows_here:
                continue
            rows_here.add(row)
            unseen_rows.discard(row)
            for column in row_columns[row]:
                if column not in core_columns or column in columns_here:
                    continue
                columns_here.add(column)
                for adjacent_row in column_rows[column]:
                    if adjacent_row in core_rows and adjacent_row not in rows_here:
                        row_stack.append(adjacent_row)
        components.append(
            component_record(
                original_columns=signed_columns,
                rows=sorted(rows_here),
                columns=sorted(columns_here),
                row_atoms=row_atoms,
                column_atoms=column_atoms,
                exp042=exp042,
                exp037=exp037,
            )
        )
    components.sort(
        key=lambda item: (
            -int(item["odd_minus_two_rank"]),
            -int(item["rows"]),
            -int(item["columns"]),
            str(item["signed_hash"]),
        )
    )
    component_summary = sorted(
        [
            [
                component["rows"],
                component["columns"],
                component["nonzeros"],
                component["ranks"]["2"],
                component["ranks"]["3"],
                component["ranks"]["5"],
                component["bockstein"]["bockstein_rank"],
            ]
            for component in components
        ]
    )
    return {
        "order": "reverse-column-first" if reverse else "forward-row-first",
        "cancellations": len(cancelled_pairs),
        "cancelled_pairs_hash": digest(cancelled_pairs),
        "free_rows": sum(
            bool(active_rows[row]) and row_degrees[row] == 0 for row in range(row_count)
        ),
        "zero_columns": sum(
            bool(active_columns[column]) and column_degrees[column] == 0
            for column in range(column_count)
        ),
        "core_rows": len(core_rows),
        "core_columns": len(core_columns),
        "components": components,
        "component_summary": component_summary,
        "component_summary_hash": digest(component_summary),
    }


def exact_recomposition(
    peel: dict[str, object], stored: dict[str, object]
) -> dict[str, bool]:
    cancellations = int(peel["cancellations"])
    return {
        f"rank_{prime}": cancellations
        + sum(int(component["ranks"][prime]) for component in peel["components"])
        == int(stored["ranks"][prime])
        for prime in ("2", "3", "5")
    } | {
        "bockstein": sum(
            int(component["bockstein"]["bockstein_rank"])
            for component in peel["components"]
        )
        == int(stored["bockstein_high_forward"]["bockstein_rank"]),
        "free_rank_three": int(peel["free_rows"])
        + sum(
            int(component["rows"]) - int(component["ranks"]["3"])
            for component in peel["components"]
        )
        == int(stored["rows"]) - int(stored["ranks"]["3"]),
    }


def positive_defects(peel: dict[str, object]) -> list[int]:
    return sorted(
        int(component["bockstein"]["bockstein_rank"])
        for component in peel["components"]
        if int(component["bockstein"]["bockstein_rank"]) > 0
    )


def completion_signatures(record: dict[str, object], alias: str) -> list[str]:
    atom = ATOM_ALIASES[alias]
    return sorted(
        str(component["normalized_signature_hash"])
        for component in record["forward"]["components"]
        if atom in component["row_atom_counts"]
        and int(component["bockstein"]["bockstein_rank"]) > 0
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=1200.0)
    parser.add_argument("--memory-gib", type=float, default=16.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")

    premise_hashes = verify_premises()
    exp042 = load_module("exp042_frozen_for_exp046", EXP042 / "run.py")
    exp037 = exp042.load_module("exp037_frozen_for_exp046", exp042.EXP037 / "run.py")
    exp045 = json.loads((EXP045 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    stored_rows = {int(row["p"]): row for row in exp045["rows"]}
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-046",
        "route": "exact integral unit-leaf cores of stable row carriers",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "masks": list(MASKS),
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
        },
        "atom_aliases": ATOM_ALIASES,
        "premise_hashes": premise_hashes,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            stored_subsets = {
                int(subset["mask"]): subset for subset in stored_rows[p]["subsets"]
            }
            row: dict[str, object] = {
                "p": p,
                "source_matrix_sha256": sha256(matrix_path),
                "masks": {},
            }
            for mask in MASKS:
                print(f"p={p} mask={mask} forward", flush=True)
                projected = project_matrix(matrix, mask)
                forward = peel_unit_core(
                    projected=projected,
                    reverse=False,
                    exp042=exp042,
                    exp037=exp037,
                )
                budget.check(f"p={p} mask={mask} forward")
                print(f"p={p} mask={mask} reverse", flush=True)
                reverse = peel_unit_core(
                    projected=projected,
                    reverse=True,
                    exp042=exp042,
                    exp037=exp037,
                )
                budget.check(f"p={p} mask={mask} reverse")
                stored = stored_subsets[mask]
                row["masks"][str(mask)] = {
                    "aliases": aliases(mask),
                    "source": {
                        "rows": stored["rows"],
                        "columns": stored["columns"],
                        "nonzeros": stored["nonzeros"],
                        "ranks": stored["ranks"],
                        "bockstein_rank": stored["bockstein_high_forward"][
                            "bockstein_rank"
                        ],
                    },
                    "forward": forward,
                    "reverse": reverse,
                    "forward_recomposition": exact_recomposition(forward, stored),
                    "reverse_recomposition": exact_recomposition(reverse, stored),
                    "order_component_agreement": (
                        forward["component_summary"] == reverse["component_summary"]
                    ),
                    "positive_defects": positive_defects(forward),
                }
            result["rows"].append(row)
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
    except exp037.BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        return 2

    full_range = {int(row["p"]) for row in result["rows"]} == {8, 9, 10, 11}
    p1 = all(
        int(record["forward"]["cancellations"]) > 0
        and all(record["forward_recomposition"].values())
        and all(record["reverse_recomposition"].values())
        and bool(record["order_component_agreement"])
        for row in result["rows"]
        for record in row["masks"].values()
    )
    p2 = all(
        row["masks"]["59"]["positive_defects"]
        == sorted(row["masks"]["58"]["positive_defects"] + [1, 1])
        and row["masks"]["62"]["positive_defects"]
        == sorted(row["masks"]["58"]["positive_defects"] + [1, 1])
        and len(completion_signatures(row["masks"]["59"], "R0")) == 2
        and completion_signatures(row["masks"]["59"], "R0")
        == completion_signatures(row["masks"]["62"], "R2")
        for row in result["rows"]
    )
    p3_defects = {
        int(row["p"]): row["masks"]["56"]["positive_defects"] for row in result["rows"]
    }
    earlier_signatures = {
        component["normalized_signature_hash"]
        for row in result["rows"]
        if int(row["p"]) < 11
        for component in row["masks"]["56"]["forward"]["components"]
    }
    p11_positive_signatures = {
        component["normalized_signature_hash"]
        for row in result["rows"]
        if int(row["p"]) == 11
        for component in row["masks"]["56"]["forward"]["components"]
        if int(component["bockstein"]["bockstein_rank"]) > 0
    }
    p3 = (
        p3_defects == {8: [], 9: [], 10: [], 11: [1]}
        and bool(p11_positive_signatures)
        and p11_positive_signatures <= earlier_signatures
    )
    result["p1_status"] = (
        "PASS_FINITE" if full_range and p1 else "REFUTED" if full_range else "NOT_EVALUATED"
    )
    result["p2_status"] = (
        "PASS_FINITE" if full_range and p2 else "REFUTED" if full_range else "NOT_EVALUATED"
    )
    result["p3_status"] = (
        "PASS_FINITE" if full_range and p3 else "REFUTED" if full_range else "NOT_EVALUATED"
    )
    result["status"] = "COMPLETE"
    result["elapsed_seconds"] = budget.elapsed
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(
        json.dumps(
            {
                "experiment": result["experiment"],
                "status": result["status"],
                "p1_status": result["p1_status"],
                "p2_status": result["p2_status"],
                "p3_status": result["p3_status"],
                "positive_defects": {
                    str(row["p"]): {
                        mask: row["masks"][mask]["positive_defects"]
                        for mask in map(str, MASKS)
                    }
                    for row in result["rows"]
                },
                "elapsed_seconds": result["elapsed_seconds"],
                "artifact_hash": result["artifact_hash"],
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
