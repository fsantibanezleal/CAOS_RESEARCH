"""EXP-042 exact Bockstein of the persistent isolated parity component.

CPU only. The script independently reconstructs the signed combined core,
extracts the frozen isolated component, and computes the first matrix
Bockstein from its bit-packed mod-two kernel to its mod-two cokernel.
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


HERE = Path(__file__).resolve().parent
EXP037 = HERE.parent / "EXP-037-connecting-quasipolynomial"
EXP039 = HERE.parent / "EXP-039-core-component-stabilization"
EXP040 = HERE.parent / "EXP-040-merged-sector-relation"
EXP041 = HERE.parent / "EXP-041-semantic-sector-tags"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
PREMISES = {
    "EXP-037 rank engine": (
        EXP037 / "run.py",
        "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    ),
    "EXP-039 component engine": (
        EXP039 / "run.py",
        "8ab5678829094a2b314a23889201b06f555aafc5af176500ef62a5eb30e4a352",
    ),
    "EXP-039 p8-p9 components": (
        EXP039 / "artifacts" / "results-p9.json",
        "831a4300cac10bf44753050a686a7993fabef09bf28b4332c6bb1fb9881c9e2c",
    ),
    "EXP-040 p10-p11 components": (
        EXP040 / "artifacts" / "target-t2-p10-p11.json",
        "ad1fec04199ff94b803f95f98650c8c8ab386386240d584f447afbb9fe27668b",
    ),
    "EXP-041 semantic profiles": (
        EXP041 / "artifacts" / "results.json",
        "069e587b779bd1571d72e1a47bf74f4d1640dae5fbbf09907d2bf798c4941534",
    ),
}
EXPECTED_DEFECTS = {8: 3, 9: 4, 10: 5, 11: 7}
EXPECTED_SKELETON_HASH = "d0c296e39c7c4f10ffd886b23b3b3d4d9cea0a291dd1aed6fcc079998c57676d"
GENERATOR_TAGS = ("L0", "L1", "H0", "H1", "H2", "H3", "H4", "H5", "H6", "H7")


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
    actual = {name: sha256(path) for name, (path, _) in PREMISES.items()}
    expected = {name: expected_hash for name, (_, expected_hash) in PREMISES.items()}
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def load_frozen() -> dict[int, dict[str, object]]:
    exp039 = json.loads((EXP039 / "artifacts" / "results-p9.json").read_text(encoding="utf-8"))
    exp040 = json.loads(
        (EXP040 / "artifacts" / "target-t2-p10-p11.json").read_text(encoding="utf-8")
    )
    exp041 = json.loads((EXP041 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    source_rows = {int(row["p"]): row for row in exp039["rows"] if int(row["p"]) in (8, 9)}
    source_rows.update({int(row["p"]): row for row in exp040["rows"]})
    isolated_hashes = {int(p): value for p, value in exp041["isolated_hashes"].items()}
    frozen: dict[int, dict[str, object]] = {}
    for p, support_hash in isolated_hashes.items():
        matches = [
            component
            for component in source_rows[p]["components"]
            if component["support_hash"] == support_hash
        ]
        if len(matches) != 1:
            raise AssertionError({"p": p, "isolated_frozen_matches": len(matches)})
        frozen[p] = matches[0]
    if set(frozen) != {8, 9, 10, 11}:
        raise AssertionError({"frozen_parameters": sorted(frozen)})
    return frozen


def generator_intervals(p: int) -> list[tuple[str, int, int]]:
    return [
        ("L0", 1, p),
        ("L1", 3 * p, 4 * p - 2),
        ("H0", 6 * p, 8 * p - 2),
        ("H1", 8 * p, 10 * p - 2),
        ("H2", 10 * p, 10 * p),
        ("H3", 11 * p - 1, 12 * p - 1),
        ("H4", 13 * p + 1, 14 * p - 2),
        ("H5", 14 * p, 15 * p - 1),
        ("H6", 16 * p, 16 * p),
        ("H7", 17 * p - 1, 18 * p - 1),
    ]


def degree_two_intervals(p: int) -> list[tuple[str, int, int]]:
    return [
        ("C0", 8 * p - 1, 8 * p - 1),
        ("C1", 10 * p - 1, 10 * p - 1),
        ("C2", 10 * p + 1, 11 * p - 2),
        ("C3", 12 * p, 13 * p),
        ("C4", 14 * p - 1, 14 * p - 1),
        ("C5", 15 * p, 16 * p - 1),
        ("C6", 16 * p + 1, 17 * p - 2),
        ("C7", 18 * p, 24 * p - 1),
    ]


def interval_tag(value: int, intervals: list[tuple[str, int, int]]) -> str:
    matches = [tag for tag, first, last in intervals if first <= value <= last]
    if len(matches) != 1:
        raise AssertionError({"value": value, "interval_matches": matches})
    return matches[0]


def normalized_exterior_counts(exterior: tuple[int, ...], p: int) -> tuple[int, ...]:
    counts = Counter(interval_tag(variable, generator_intervals(p)) for variable in exterior)
    result = [counts[tag] for tag in GENERATOR_TAGS]
    result[0] -= p
    result[1] -= p
    return tuple(result)


def semantic_atom(
    *, side: str, kind: str, coefficient_tag: str, exterior: tuple[int, ...], p: int
) -> str:
    return json.dumps(
        [side, kind, coefficient_tag, list(normalized_exterior_counts(exterior, p))],
        separators=(",", ":"),
    )


def table_encode(values: list[str]) -> tuple[list[str], list[int]]:
    table = sorted(set(values))
    positions = {value: index for index, value in enumerate(table)}
    return table, [positions[value] for value in values]


def int_digest(value: int, bits: int) -> str:
    width = max(1, (bits + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "little")).hexdigest()


def reduce_mod_two_columns(
    column_bits: list[int], row_count: int, order: list[int]
) -> tuple[list[int], list[int], list[int]]:
    pivot_vectors = [0] * row_count
    pivot_combinations = [0] * row_count
    kernel: list[int] = []
    for column in order:
        vector = column_bits[column]
        combination = 1 << column
        while vector:
            pivot = vector.bit_length() - 1
            if not pivot_vectors[pivot]:
                pivot_vectors[pivot] = vector
                pivot_combinations[pivot] = combination
                break
            vector ^= pivot_vectors[pivot]
            combination ^= pivot_combinations[pivot]
        if not vector:
            kernel.append(combination)
    pivot_rows = [row for row, vector in enumerate(pivot_vectors) if vector]
    return pivot_vectors, pivot_rows, kernel


def reduce_mod_image(vector: int, pivot_vectors: list[int], pivot_rows: list[int]) -> int:
    for pivot in reversed(pivot_rows):
        if (vector >> pivot) & 1:
            vector ^= pivot_vectors[pivot]
    return vector


def bit_indices(value: int):
    while value:
        least = value & -value
        yield least.bit_length() - 1
        value ^= least


def atom_histogram(indices: list[int], atom_ids: list[int], table: list[str]) -> dict[str, int]:
    counts = Counter(table[atom_ids[index]] for index in indices)
    return dict(sorted(counts.items()))


def bockstein_profile(
    *,
    signed_columns: list[list[tuple[int, int]]],
    row_count: int,
    row_atom_table: list[str],
    row_atom_ids: list[int],
    column_atom_table: list[str],
    column_atom_ids: list[int],
    reverse: bool,
) -> dict[str, object]:
    column_count = len(signed_columns)
    column_bits = [sum(1 << row for row, _ in entries) for entries in signed_columns]
    order = list(range(column_count - 1, -1, -1)) if reverse else list(range(column_count))
    pivot_vectors, pivot_rows, kernel = reduce_mod_two_columns(column_bits, row_count, order)
    if len(pivot_rows) + len(kernel) != column_count:
        raise AssertionError("rank-nullity failure")

    quotient_classes: list[int] = []
    kernel_records: list[dict[str, object]] = []
    for combination in kernel:
        boundary = [0] * row_count
        selected_columns = list(bit_indices(combination))
        for column in selected_columns:
            for row, sign in signed_columns[column]:
                boundary[row] += sign
        odd_rows = [row for row, value in enumerate(boundary) if value & 1]
        if odd_rows:
            raise AssertionError({"kernel_lift_not_even": odd_rows[:10]})
        divided_bits = 0
        for row, value in enumerate(boundary):
            if (value // 2) & 1:
                divided_bits |= 1 << row
        quotient = reduce_mod_image(divided_bits, pivot_vectors, pivot_rows)
        quotient_classes.append(quotient)
        kernel_records.append(
            {
                "cycle_hash": int_digest(combination, column_count),
                "cycle_weight": len(selected_columns),
                "cycle_column_atoms": atom_histogram(
                    selected_columns, column_atom_ids, column_atom_table
                ),
                "divided_boundary_hash": int_digest(divided_bits, row_count),
                "quotient_class_hash": int_digest(quotient, row_count),
                "quotient_weight": quotient.bit_count(),
            }
        )

    beta_pivots: dict[int, int] = {}
    independent_indices: list[int] = []
    for index, original in enumerate(quotient_classes):
        vector = original
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in beta_pivots:
                beta_pivots[pivot] = vector
                independent_indices.append(index)
                break
            vector ^= beta_pivots[pivot]

    independent_records: list[dict[str, object]] = []
    for index in independent_indices:
        quotient = quotient_classes[index]
        rows = list(bit_indices(quotient))
        record = dict(kernel_records[index])
        record["quotient_row_atoms"] = atom_histogram(rows, row_atom_ids, row_atom_table)
        independent_records.append(record)
    return {
        "order": "reverse" if reverse else "forward",
        "rank_mod_two": len(pivot_rows),
        "kernel_dimension": len(kernel),
        "kernel_basis_hash": digest(sorted(record["cycle_hash"] for record in kernel_records)),
        "bockstein_rank": len(beta_pivots),
        "bockstein_class_hash": digest(
            sorted(record["quotient_class_hash"] for record in independent_records)
        ),
        "independent_witnesses": independent_records,
    }


def extract_isolated_component(
    *,
    exp037: ModuleType,
    exp036: ModuleType,
    basis: dict[str, object],
    d_rows: list[object],
    frozen: dict[str, object],
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
                product = exp036.low_product(p, variable, coefficient)
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

    def row_atom(row: int) -> str:
        if row < k_base:
            exterior, product_kind, _ = d_rows[row]
            return semantic_atom(
                side="row", kind="D", coefficient_tag=product_kind, exterior=exterior, p=p
            )
        exterior, coefficient = codomain[row - k_base]
        return semantic_atom(
            side="row",
            kind="K",
            coefficient_tag=interval_tag(coefficient, degree_two_intervals(p)),
            exterior=exterior,
            p=p,
        )

    def column_atom(column: int) -> str:
        if column < len(source):
            exterior, coefficient = source[column]
            kind = "S"
        else:
            exterior, coefficient = kernel_domain[column - len(source)]
            kind = "K"
        return semantic_atom(
            side="column",
            kind=kind,
            coefficient_tag=interval_tag(coefficient, generator_intervals(p)),
            exterior=exterior,
            p=p,
        )

    counts = array("I", [0]) * row_count
    incident_xor = array("I", [0]) * row_count
    column_sizes = array("I", [0]) * column_count
    for column in range(column_count):
        entries = combined_entries(column)
        column_sizes[column] = len(entries)
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
    while leaf_rows:
        row = leaf_rows.pop()
        if counts[row] != 1:
            continue
        column = incident_xor[row]
        if not active[column]:
            raise AssertionError("stale unique-column sketch")
        active[column] = 0
        for adjacent_row, value in combined_entries(column):
            if value:
                counts[adjacent_row] -= 1
                incident_xor[adjacent_row] ^= column
                if counts[adjacent_row] == 1:
                    leaf_rows.append(adjacent_row)
    del incident_xor, leaf_rows

    row_only_rows = sum(count > 0 for count in counts)
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

    def cancel_pair(row: int, column: int) -> None:
        active_rows[row] = 0
        active_columns[column] = 0
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
        if not active_columns[seed] or column_degrees[seed] == 0 or column_components[seed] >= 0:
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

    target_hash = str(frozen["support_hash"])
    selected: dict[str, object] | None = None
    for local_rows, local_columns in zip(component_rows, component_columns, strict=True):
        global_rows = sorted(core_global_rows[row] for row in local_rows)
        row_map = {row: index for index, row in enumerate(global_rows)}
        original_columns = sorted(core_original_columns[column] for column in local_columns)
        support_hasher = hashlib.sha256()
        signed_hasher = hashlib.sha256()
        signed_columns: list[list[tuple[int, int]]] = []
        for original_column in original_columns:
            entries = [
                (row_map[row], value)
                for row, value in combined_entries(original_column)
                if row in row_map and value
            ]
            entries.sort()
            signed_columns.append(entries)
            support_hasher.update(json.dumps([row for row, _ in entries]).encode())
            signed_hasher.update(json.dumps(entries).encode())
        support_hash = support_hasher.hexdigest()
        if support_hash != target_hash:
            continue
        if selected is not None:
            raise AssertionError({"p": p, "duplicate_isolated_support_hash": target_hash})
        row_atoms = [row_atom(row) for row in global_rows]
        column_atoms = [column_atom(column) for column in original_columns]
        row_atom_table, row_atom_ids = table_encode(row_atoms)
        column_atom_table, column_atom_ids = table_encode(column_atoms)
        skeleton_hash = digest(sorted(set(row_atoms + column_atoms)))
        selected = {
            "experiment": "EXP-042",
            "p": p,
            "rows": len(global_rows),
            "columns": len(original_columns),
            "nonzeros": sum(map(len, signed_columns)),
            "support_hash": support_hash,
            "signed_hash": signed_hasher.hexdigest(),
            "normalized_atom_skeleton_hash": skeleton_hash,
            "row_atom_table": row_atom_table,
            "row_atom_ids": row_atom_ids,
            "column_atom_table": column_atom_table,
            "column_atom_ids": column_atom_ids,
            "signed_columns": signed_columns,
        }
    if selected is None:
        raise AssertionError({"p": p, "isolated_component_not_found": target_hash})
    return selected


def rank_fields(exp037: ModuleType, signed_columns: list[list[tuple[int, int]]]) -> dict[str, int]:
    accumulators = {
        prime: exp037.rank_accumulator(prime, sparse_gf2=False) for prime in (2, 3, 5)
    }
    for entries in signed_columns:
        for accumulator in accumulators.values():
            accumulator.add(entries)
    return {str(prime): accumulator.rank for prime, accumulator in accumulators.items()}


def verify_frozen_matrix(matrix: dict[str, object], frozen: dict[str, object]) -> dict[str, bool]:
    p = int(matrix["p"])
    expected_ranks = {str(prime): int(rank) for prime, rank in frozen["ranks"].items()}
    actual_ranks = matrix["ranks"]
    checks = {
        "rows": int(matrix["rows"]) == int(frozen["rows"]),
        "columns": int(matrix["columns"]) == int(frozen["columns"]),
        "nonzeros": int(matrix["nonzeros"]) == int(frozen["nonzeros"]),
        "support_hash": matrix["support_hash"] == frozen["support_hash"],
        "signed_hash": matrix["signed_hash"] == frozen["signed_hash"],
        "rank_two": int(actual_ranks["2"]) == expected_ranks["2"],
        "rank_three": int(actual_ranks["3"]) == expected_ranks["3"],
        "rank_five": (
            int(actual_ranks["5"]) == expected_ranks["5"]
            if "5" in expected_ranks
            else int(actual_ranks["5"]) == int(actual_ranks["3"])
        ),
        "skeleton": matrix["normalized_atom_skeleton_hash"] == EXPECTED_SKELETON_HASH,
        "defect": int(actual_ranks["3"]) - int(actual_ranks["2"]) == EXPECTED_DEFECTS[p],
    }
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=2400.0)
    parser.add_argument("--memory-gib", type=float, default=36.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")

    premise_hashes = verify_premises()
    frozen = load_frozen()
    exp037 = load_module("exp037_frozen_for_exp042", EXP037 / "run.py")
    exp036 = exp037.load_exp036()
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-042",
        "route": "first Bockstein of the persistent isolated signed component",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "t": 2,
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
        },
        "premise_hashes": premise_hashes,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            print(f"building and extracting isolated component for p={p}", flush=True)
            basis = exp037.build_basis(exp036, p, 2)
            d_rows = exp037.d_rows_for_basis(exp036, basis, budget)
            matrix = extract_isolated_component(
                exp037=exp037,
                exp036=exp036,
                basis=basis,
                d_rows=d_rows,
                frozen=frozen[p],
                budget=budget,
            )
            matrix["ranks"] = rank_fields(exp037, matrix["signed_columns"])
            matrix["frozen_checks"] = verify_frozen_matrix(matrix, frozen[p])
            if not all(matrix["frozen_checks"].values()):
                raise AssertionError({"p": p, "frozen_checks": matrix["frozen_checks"]})
            print(f"computing forward Bockstein for p={p}", flush=True)
            forward = bockstein_profile(
                signed_columns=matrix["signed_columns"],
                row_count=int(matrix["rows"]),
                row_atom_table=matrix["row_atom_table"],
                row_atom_ids=matrix["row_atom_ids"],
                column_atom_table=matrix["column_atom_table"],
                column_atom_ids=matrix["column_atom_ids"],
                reverse=False,
            )
            print(f"computing reverse Bockstein for p={p}", flush=True)
            reverse = bockstein_profile(
                signed_columns=matrix["signed_columns"],
                row_count=int(matrix["rows"]),
                row_atom_table=matrix["row_atom_table"],
                row_atom_ids=matrix["row_atom_ids"],
                column_atom_table=matrix["column_atom_table"],
                column_atom_ids=matrix["column_atom_ids"],
                reverse=True,
            )
            matrix["bockstein"] = {"forward": forward, "reverse": reverse}
            matrix["order_agreement"] = {
                "rank_mod_two": forward["rank_mod_two"] == reverse["rank_mod_two"],
                "kernel_dimension": forward["kernel_dimension"] == reverse["kernel_dimension"],
                "bockstein_rank": forward["bockstein_rank"] == reverse["bockstein_rank"],
            }
            matrix["prediction_matches"] = (
                int(forward["bockstein_rank"]) == EXPECTED_DEFECTS[p]
                and int(reverse["bockstein_rank"]) == EXPECTED_DEFECTS[p]
            )
            matrix["artifact_hash"] = digest(matrix)
            matrix_path = HERE / "artifacts" / f"matrix-p{p}.json"
            write_json_atomic(matrix_path, matrix)
            result["rows"].append(
                {
                    "p": p,
                    "rows": matrix["rows"],
                    "columns": matrix["columns"],
                    "nonzeros": matrix["nonzeros"],
                    "support_hash": matrix["support_hash"],
                    "signed_hash": matrix["signed_hash"],
                    "ranks": matrix["ranks"],
                    "frozen_checks": matrix["frozen_checks"],
                    "bockstein": matrix["bockstein"],
                    "order_agreement": matrix["order_agreement"],
                    "prediction_matches": matrix["prediction_matches"],
                    "matrix_artifact": matrix_path.name,
                    "matrix_artifact_sha256": sha256(matrix_path),
                    "matrix_internal_hash": matrix["artifact_hash"],
                }
            )
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
            del matrix, basis, d_rows
            gc.collect()
    except exp037.BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        print(json.dumps({"status": result["status"], "error": str(error)}, indent=2), flush=True)
        return 2

    full_range = {int(row["p"]) for row in result["rows"]} == {8, 9, 10, 11}
    result["p1_status"] = (
        "PASS_FINITE"
        if full_range
        and all(all(row["frozen_checks"].values()) for row in result["rows"])
        else "NOT_EVALUATED"
    )
    result["p2_status"] = (
        "PASS_FINITE"
        if full_range and all(row["prediction_matches"] for row in result["rows"])
        else "REFUTED" if full_range else "NOT_EVALUATED"
    )
    result["p3_status"] = (
        "PASS_FINITE"
        if full_range
        and all(all(row["order_agreement"].values()) for row in result["rows"])
        else "REFUTED" if full_range else "NOT_EVALUATED"
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
                "completed_parameters": [row["p"] for row in result["rows"]],
                "bockstein_ranks": {
                    str(row["p"]): row["bockstein"]["forward"]["bockstein_rank"]
                    for row in result["rows"]
                },
                "p1_status": result["p1_status"],
                "p2_status": result["p2_status"],
                "p3_status": result["p3_status"],
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
