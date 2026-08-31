"""EXP-039 exact connected-component anatomy of the combined parity core.

CPU only.  The frozen EXP-037 constructor supplies complete signed columns.  This
script independently repeats unit peeling, decomposes the residual bipartite
support, and ranks every connected component over the requested prime fields.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
from array import array
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Callable


HERE = Path(__file__).resolve().parent
EXP037 = HERE.parent / "EXP-037-connecting-quasipolynomial"
EXP038 = HERE.parent / "EXP-038-degree-six-relation"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
PREMISES = {
    "EXP-038 proof": (
        EXP038 / "proof.md",
        "829eaa8645258d065f2d0b8bb7e6ee9dbad9ee439d4b659faf31e621e8e40213",
    ),
    "EXP-038 verdict": (
        EXP038 / "verdict.md",
        "90ccf41cd338378bed687292d593aeab6897be919827f9fd5851506d94a40b7b",
    ),
    "EXP-038 audit": (
        EXP038 / "artifacts" / "audit-certificate.json",
        "3b5d2871d893b29871b8e58d9e66d00ee65e86c5545fe90909b322ecb5623b39",
    ),
    "EXP-037 rank engine": (
        EXP037 / "run.py",
        "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    ),
}
EXPECTED_COMBINED_RANKS = {
    4: {2: 588, 3: 589},
    5: {2: 2935, 3: 2939},
    6: {2: 11548, 3: 11557},
    7: {2: 38611, 3: 38629},
    8: {2: 113694, 3: 113725},
    9: {2: 302169, 3: 302218},
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


def verify_premises() -> dict[str, str]:
    actual = {name: sha256(path) for name, (path, _) in PREMISES.items()}
    expected = {name: expected_hash for name, (_, expected_hash) in PREMISES.items()}
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalized_integer(value: int, p: int) -> tuple[int, int]:
    return divmod(value, p)


def normalized_label(value: object, p: int) -> object:
    if isinstance(value, int):
        return normalized_integer(value, p)
    if isinstance(value, str):
        return value
    if isinstance(value, tuple):
        return tuple(normalized_label(item, p) for item in value)
    raise TypeError(f"unsupported semantic label {value!r}")


EntryFunction = Callable[[int], list[tuple[int, int]]]


def analyze_combined_core(
    *,
    exp037: ModuleType,
    basis: dict[str, object],
    d_rows: list[object],
    fields: tuple[int, ...],
    budget: object,
) -> dict[str, object]:
    p = int(basis["p"])
    low = basis["low"]
    degree_two = basis["degree_two"]
    codomain = basis["codomain"]
    kernel_domain = basis["kernel_domain"]
    source = basis["source"]
    k_index = {row: index for index, row in enumerate(codomain)}
    d_index = {row: index for index, row in enumerate(d_rows)}
    k_base = len(d_rows)
    row_count = len(d_rows) + len(codomain)
    column_count = len(source) + len(kernel_domain)

    def kernel_entries(column: int) -> list[tuple[int, int]]:
        exterior, coefficient = kernel_domain[column]
        entries: list[tuple[int, int]] = []
        for variable, sign, face in exp037.signed_faces(exterior):
            product_offset = coefficient + variable
            if product_offset in degree_two:
                entries.append((k_base + k_index[(face, product_offset)], sign))
        return entries

    def source_entries(column: int) -> list[tuple[int, int]]:
        exterior, coefficient = source[column]
        entries: list[tuple[int, int]] = []
        for variable, sign, face in exp037.signed_faces(exterior):
            if variable in low:
                product = exp037_exp036.low_product(p, variable, coefficient)
                if product is not None:
                    entries.append((d_index[(face, product[0], product[1])], sign))
            else:
                product_offset = variable + coefficient
                if product_offset in degree_two:
                    entries.append((k_base + k_index[(face, product_offset)], sign))
        return entries

    def combined_entries(column: int) -> list[tuple[int, int]]:
        if column < len(source):
            return source_entries(column)
        return kernel_entries(column - len(source))

    def row_label(row: int) -> object:
        if row < k_base:
            return ("D", normalized_label(d_rows[row], p))
        return ("K", normalized_label(codomain[row - k_base], p))

    def column_label(column: int) -> object:
        if column < len(source):
            return ("S", normalized_label(source[column], p))
        return ("K", normalized_label(kernel_domain[column - len(source)], p))

    counts = array("I", [0]) * row_count
    incident_xor = array("I", [0]) * row_count
    column_sizes = array("I", [0]) * column_count
    initial_nonzeros = 0
    for column in range(column_count):
        entries = combined_entries(column)
        column_sizes[column] = len(entries)
        initial_nonzeros += len(entries)
        for row, value in entries:
            if value:
                counts[row] += 1
                incident_xor[row] ^= column
        if column and column % 50_000 == 0:
            budget.check(f"p={p} incidence scan")
            print(f"p={p} incidence {column}/{column_count}", flush=True)

    active = bytearray(1 if size else 0 for size in column_sizes)
    del column_sizes
    leaf_rows = array("I", (row for row, count in enumerate(counts) if count == 1))
    initial_leaf_rows = len(leaf_rows)
    row_leaf_pivots = 0
    while leaf_rows:
        row = leaf_rows.pop()
        if counts[row] != 1:
            continue
        column = incident_xor[row]
        if not active[column]:
            raise AssertionError("stale unique-column sketch")
        active[column] = 0
        row_leaf_pivots += 1
        for adjacent_row, value in combined_entries(column):
            if value:
                counts[adjacent_row] -= 1
                incident_xor[adjacent_row] ^= column
                if counts[adjacent_row] == 1:
                    leaf_rows.append(adjacent_row)
    del incident_xor, leaf_rows

    row_only_rows = sum(count > 0 for count in counts)
    row_only_columns = sum(active)
    row_only_nonzeros = sum(counts)
    first_row_map = array("i", [-1]) * row_count
    core_global_rows = array("I")
    for row, count in enumerate(counts):
        if count:
            first_row_map[row] = len(core_global_rows)
            core_global_rows.append(row)

    core_original_columns = array("I")
    column_offsets = array("Q", [0])
    edge_rows = array("I")
    column_degrees = array("I")
    for original_column, is_active in enumerate(active):
        if not is_active:
            continue
        mapped = [
            first_row_map[row]
            for row, value in combined_entries(original_column)
            if value and first_row_map[row] >= 0
        ]
        if mapped:
            core_original_columns.append(original_column)
            edge_rows.extend(mapped)
            column_degrees.append(len(mapped))
            column_offsets.append(len(edge_rows))
    del active, first_row_map, counts
    gc.collect()
    if len(edge_rows) != row_only_nonzeros:
        raise AssertionError("CSR nonzero mismatch")

    row_degrees = array("I", [0]) * row_only_rows
    for row in edge_rows:
        row_degrees[row] += 1
    row_offsets = array("Q", [0])
    for degree in row_degrees:
        row_offsets.append(row_offsets[-1] + degree)
    row_edges = array("I", [0]) * len(edge_rows)
    row_positions = array("Q", row_offsets[:-1])
    for column in range(len(core_original_columns)):
        for edge in range(column_offsets[column], column_offsets[column + 1]):
            row = edge_rows[edge]
            row_edges[row_positions[row]] = column
            row_positions[row] += 1
    del row_positions

    active_rows = bytearray([1]) * row_only_rows
    active_columns = bytearray([1]) * len(core_original_columns)
    row_queue = array("I", (row for row, degree in enumerate(row_degrees) if degree == 1))
    column_queue = array(
        "I", (column for column, degree in enumerate(column_degrees) if degree == 1)
    )
    initial_leaf_columns = len(column_queue)
    two_sided_pivots = 0

    def cancel_pair(row: int, column: int) -> None:
        nonlocal two_sided_pivots
        active_rows[row] = 0
        active_columns[column] = 0
        two_sided_pivots += 1
        for edge in range(column_offsets[column], column_offsets[column + 1]):
            adjacent_row = edge_rows[edge]
            if active_rows[adjacent_row]:
                row_degrees[adjacent_row] -= 1
                if row_degrees[adjacent_row] == 1:
                    row_queue.append(adjacent_row)
        for edge in range(row_offsets[row], row_offsets[row + 1]):
            adjacent_column = row_edges[edge]
            if active_columns[adjacent_column]:
                column_degrees[adjacent_column] -= 1
                if column_degrees[adjacent_column] == 1:
                    column_queue.append(adjacent_column)
        row_degrees[row] = 0
        column_degrees[column] = 0

    while row_queue or column_queue:
        if row_queue:
            row = row_queue.pop()
            if not active_rows[row] or row_degrees[row] != 1:
                continue
            neighbors = [
                row_edges[edge]
                for edge in range(row_offsets[row], row_offsets[row + 1])
                if active_columns[row_edges[edge]]
            ]
            if len(neighbors) != 1:
                raise AssertionError("row leaf degree mismatch")
            cancel_pair(row, neighbors[0])
        else:
            column = column_queue.pop()
            if not active_columns[column] or column_degrees[column] != 1:
                continue
            neighbors = [
                edge_rows[edge]
                for edge in range(column_offsets[column], column_offsets[column + 1])
                if active_rows[edge_rows[edge]]
            ]
            if len(neighbors) != 1:
                raise AssertionError("column leaf degree mismatch")
            cancel_pair(neighbors[0], column)

    component_rows: list[array[int]] = []
    component_columns: list[array[int]] = []
    row_components = array("i", [-1]) * row_only_rows
    column_components = array("i", [-1]) * len(core_original_columns)
    for seed in range(len(core_original_columns)):
        if not active_columns[seed] or column_components[seed] >= 0:
            continue
        component = len(component_columns)
        rows_here = array("I")
        columns_here = array("I")
        column_components[seed] = component
        column_stack = [seed]
        row_stack: list[int] = []
        while column_stack or row_stack:
            while column_stack:
                column = column_stack.pop()
                columns_here.append(column)
                for edge in range(column_offsets[column], column_offsets[column + 1]):
                    row = edge_rows[edge]
                    if active_rows[row] and row_components[row] < 0:
                        row_components[row] = component
                        row_stack.append(row)
            while row_stack:
                row = row_stack.pop()
                rows_here.append(row)
                for edge in range(row_offsets[row], row_offsets[row + 1]):
                    column = row_edges[edge]
                    if active_columns[column] and column_components[column] < 0:
                        column_components[column] = component
                        column_stack.append(column)
        component_rows.append(rows_here)
        component_columns.append(columns_here)

    if sum(map(len, component_rows)) != sum(active_rows):
        raise AssertionError("active row component coverage mismatch")
    if sum(map(len, component_columns)) != sum(active_columns):
        raise AssertionError("active column component coverage mismatch")

    records: list[dict[str, object]] = []
    core_rank_sums = {prime: 0 for prime in fields}
    for component, (local_rows, local_columns) in enumerate(
        zip(component_rows, component_columns, strict=True)
    ):
        global_rows = sorted(core_global_rows[row] for row in local_rows)
        row_map = {row: index for index, row in enumerate(global_rows)}
        original_columns = sorted(core_original_columns[column] for column in local_columns)
        accumulators = {
            prime: exp037.rank_accumulator(prime, sparse_gf2=len(global_rows) > 50_000)
            for prime in fields
        }
        support_hasher = hashlib.sha256()
        signed_hasher = hashlib.sha256()
        normalized_hasher = hashlib.sha256()
        degree_histogram: Counter[int] = Counter()
        nonzeros = 0
        cached_entries: list[list[tuple[int, int]]] = []
        for original_column in original_columns:
            entries = [
                (row_map[row], value)
                for row, value in combined_entries(original_column)
                if row in row_map and value
            ]
            entries.sort()
            cached_entries.append(entries)
            nonzeros += len(entries)
            degree_histogram[len(entries)] += 1
            support_hasher.update(json.dumps([row for row, _ in entries]).encode())
            signed_hasher.update(json.dumps(entries).encode())
            semantic = [
                column_label(original_column),
                sorted((row_label(global_rows[row]), value) for row, value in entries),
            ]
            normalized_hasher.update(
                json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()
            )
            for accumulator in accumulators.values():
                accumulator.add(entries)
        ranks = {prime: accumulator.rank for prime, accumulator in accumulators.items()}
        for prime, rank in ranks.items():
            core_rank_sums[prime] += rank
        defect = ranks.get(3, 0) - ranks.get(2, 0) if 2 in ranks and 3 in ranks else None

        controls: dict[str, object] = {}
        if defect and 3 in fields:
            erased = exp037.rank_accumulator(3, sparse_gf2=False)
            perturbed = exp037.rank_accumulator(3, sparse_gf2=False)
            first_entry_flipped = False
            for entries in cached_entries:
                erased.add((row, 1) for row, _ in entries)
                changed: list[tuple[int, int]] = []
                for row, value in entries:
                    if not first_entry_flipped:
                        value = -value
                        first_entry_flipped = True
                    changed.append((row, value))
                perturbed.add(changed)
            controls = {
                "sign_erased_gf3_rank": erased.rank,
                "one_sign_flipped_gf3_rank": perturbed.rank,
                "original_gf3_rank": ranks[3],
            }

        records.append(
            {
                "component": component,
                "rows": len(global_rows),
                "columns": len(original_columns),
                "vertices": len(global_rows) + len(original_columns),
                "nonzeros": nonzeros,
                "column_degree_histogram": dict(sorted(degree_histogram.items())),
                "ranks": {str(prime): rank for prime, rank in ranks.items()},
                "odd_minus_two_rank_defect": defect,
                "support_hash": support_hasher.hexdigest(),
                "signed_hash": signed_hasher.hexdigest(),
                "normalized_signed_hash": normalized_hasher.hexdigest(),
                "controls": controls,
            }
        )
        budget.check(f"p={p} component {component}")

    peeled_rank = row_leaf_pivots + two_sided_pivots
    complete_ranks = {prime: peeled_rank + rank for prime, rank in core_rank_sums.items()}
    expected = {prime: EXPECTED_COMBINED_RANKS[p][prime] for prime in fields}
    if complete_ranks != expected:
        raise AssertionError({"p": p, "complete_ranks": complete_ranks, "expected": expected})
    defect_records = [record for record in records if record["odd_minus_two_rank_defect"]]
    total_defect = complete_ranks.get(3, 0) - complete_ranks.get(2, 0)
    p1_pass = p < 5 or (
        sum(int(record["odd_minus_two_rank_defect"]) for record in defect_records) == total_defect
        and all(
            record["odd_minus_two_rank_defect"] == 1 and int(record["vertices"]) <= 5_000
            for record in defect_records
        )
    )
    print(
        f"p={p}: components={len(records)}, defective={len(defect_records)}, "
        f"largest={max((int(record['vertices']) for record in records), default=0)}, "
        f"defect={total_defect}, P1={'PASS' if p1_pass else 'FAIL'}",
        flush=True,
    )
    return {
        "p": p,
        "t": 2,
        "basis_hashes": basis["hashes"],
        "matrix": {
            "rows": row_count,
            "columns": column_count,
            "initial_nonzeros": initial_nonzeros,
            "initial_leaf_rows": initial_leaf_rows,
            "initial_leaf_columns_after_row_peel": initial_leaf_columns,
            "row_leaf_pivots": row_leaf_pivots,
            "two_sided_leaf_pivots": two_sided_pivots,
            "peeled_rank": peeled_rank,
            "row_only_residual_rows": row_only_rows,
            "row_only_residual_columns": row_only_columns,
            "row_only_residual_nonzeros": row_only_nonzeros,
            "residual_rows": sum(active_rows),
            "residual_columns": sum(active_columns),
            "residual_nonzeros": sum(int(record["nonzeros"]) for record in records),
            "component_count": len(records),
            "complete_ranks": {str(prime): rank for prime, rank in complete_ranks.items()},
        },
        "components": records,
        "defective_component_count": len(defect_records),
        "total_odd_minus_two_rank_defect": total_defect,
        "p1_bounded_defect_one_components": p1_pass,
        "row_hash": digest(records),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=4)
    parser.add_argument("--p-max", type=int, default=9)
    parser.add_argument("--fields", default="2,3")
    parser.add_argument("--budget-seconds", type=float, default=1800.0)
    parser.add_argument("--memory-gib", type=float, default=20.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    fields = tuple(int(value) for value in args.fields.split(","))
    if not set(fields).issubset({2, 3}) or not fields:
        raise ValueError("EXP-039 primary fields must be a nonempty subset of 2,3")
    if args.p_min < 4 or args.p_max > 9 or args.p_min > args.p_max:
        raise ValueError("declared primary range is 4<=p_min<=p_max<=9")

    premise_hashes = verify_premises()
    exp037 = load_module("exp037_frozen_for_exp039", EXP037 / "run.py")
    global exp037_exp036
    exp037_exp036 = exp037.load_exp036()
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-039",
        "route": "exact connected components of the signed combined residual core",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "t": 2,
            "fields": fields,
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
        },
        "premise_hashes": premise_hashes,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            print(f"building complete basis for p={p}", flush=True)
            basis = exp037.build_basis(exp037_exp036, p, 2)
            d_rows = exp037.d_rows_for_basis(exp037_exp036, basis, budget)
            row = analyze_combined_core(
                exp037=exp037,
                basis=basis,
                d_rows=d_rows,
                fields=fields,
                budget=budget,
            )
            result["rows"].append(row)
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
            del basis, d_rows
            gc.collect()
    except exp037.BudgetStop as error:
        result["status"] = "RESOURCE_STOP"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        print(json.dumps(result, indent=2), flush=True)
        return 2

    rows = result["rows"]
    all_p1 = all(row["p1_bounded_defect_one_components"] for row in rows if row["p"] >= 5)
    normalized_types: dict[str, list[dict[str, int]]] = {}
    for row in rows:
        for component in row["components"]:
            if component["odd_minus_two_rank_defect"]:
                normalized_types.setdefault(component["normalized_signed_hash"], []).append(
                    {"p": row["p"], "component": component["component"]}
                )
    recurring = {key: value for key, value in normalized_types.items() if len(value) > 1}
    result["p1_status"] = "PASS_FINITE" if all_p1 else "REFUTED"
    result["p2_normalized_type_count"] = len(normalized_types)
    result["p2_recurring_normalized_types"] = recurring
    result["p2_status"] = "SUPPORTED_FINITE" if recurring and all_p1 else "REFUTED"
    result["status"] = "COMPLETE"
    result["elapsed_seconds"] = budget.elapsed
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
