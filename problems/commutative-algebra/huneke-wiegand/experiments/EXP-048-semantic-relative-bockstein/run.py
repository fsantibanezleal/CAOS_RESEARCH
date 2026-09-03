"""EXP-048 semantic coordinates for the exact relative Bockstein images.

CPU only. Exact integer reconstruction and bit-packed GF(2) linear algebra.
"""

from __future__ import annotations

import argparse
import ctypes
import gc
import hashlib
import importlib.util
import json
import os
import time
from array import array
from pathlib import Path
from types import ModuleType
from typing import Iterable


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP036 = EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy"
EXP037 = EXPERIMENTS / "EXP-037-connecting-quasipolynomial"
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP047 = EXPERIMENTS / "EXP-047-relative-kernel-smith"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
INCLUSIONS = ((58, 59), (58, 62), (56, 58))
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
    EXP036 / "run.py": "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    EXP037 / "run.py": "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP042 / "artifacts" / "results.json": (
        "3c4ae292fb17a5daf473aee0ed37e473000de686607b5da0a0f4c357a8216ee2"
    ),
    EXP047 / "artifacts" / "results.json": (
        "f78d251ae1746a88d1190756572aa251b9daf70ceb103cef9765c6d73b26f46c"
    ),
}
MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    11: "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
}
RELATIVE_SHA256 = {
    (8, 56, 58): "3e9cbd723761a2c28dc5cf7110bf4407fd80b3717bcfcd96922f505bbdb4aa20",
    (8, 58, 59): "37e5c293b6aa4b2615c5c3705af13cde4a223f8ea00db16ba4d8f3b875c1ac6d",
    (8, 58, 62): "03dc1c2cb89673cce99b3700192712394230b3686c6bc7a9b0d81c2e1c4fa5f7",
    (9, 56, 58): "e77c4786ef3d0423c183071bdc6da6431ec84f271aec35500be63e4c3f816f8b",
    (9, 58, 59): "78e9a2bc34784a41ee56b46bfdfae3f62e4978ba3945c411296f30dfbbaadd3a",
    (9, 58, 62): "58aa31d8dc6c4a958c09134d42a09c92d6e1b7f22db7dbcede7689b3d5ac373d",
    (10, 56, 58): "c69053b960cc55db51c12f964ff9fed6a09662905a090da4203d03bf171ba29b",
    (10, 58, 59): "4aad918a41768e73d3d9f86b004fd9622d53ece76a213cfaf02137a6acc37aa4",
    (10, 58, 62): "35d45ddcc1aebcae6bb4b79e09db37331a41ec3dc67a83a015fa8609cf6b1f74",
    (11, 56, 58): "af9639fc0265a9490b27b7d48ace4f0c4cd0258cba72a502c361a74856669d8b",
    (11, 58, 59): "0c803c24907a9404ffe3160a87a74e6b2c926daf7666aecb2193a8c202b89d23",
    (11, 58, 62): "5435894d965d8745a203df75ba20202f92795b8e81eb5dac2876041310e8d6d5",
}


class BudgetStop(RuntimeError):
    """Raised only between deterministic reconstruction stages."""


class Budget:
    def __init__(self, seconds: float, memory_gib: float) -> None:
        self.started = time.monotonic()
        self.seconds = seconds
        self.memory_bytes = int(memory_gib * 1024**3)

    @property
    def elapsed(self) -> float:
        return time.monotonic() - self.started

    def check(self, stage: str) -> None:
        if self.elapsed > self.seconds:
            raise BudgetStop(f"time budget exceeded after {stage}: {self.elapsed:.3f}s")
        private = private_bytes()
        if private is not None and private > self.memory_bytes:
            raise BudgetStop(f"memory budget exceeded after {stage}: {private} bytes")


def private_bytes() -> int | None:
    if os.name != "nt":
        return None

    class ProcessMemoryCountersEx(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_ulong),
            ("PageFaultCount", ctypes.c_ulong),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
            ("PrivateUsage", ctypes.c_size_t),
        ]

    counters = ProcessMemoryCountersEx()
    counters.cb = ctypes.sizeof(counters)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    get_current_process = kernel32.GetCurrentProcess
    get_current_process.argtypes = []
    get_current_process.restype = ctypes.c_void_p
    get_process_memory_info = kernel32.K32GetProcessMemoryInfo
    get_process_memory_info.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ProcessMemoryCountersEx),
        ctypes.c_ulong,
    ]
    get_process_memory_info.restype = ctypes.c_int
    process = get_current_process()
    success = get_process_memory_info(process, ctypes.byref(counters), counters.cb)
    return int(counters.PrivateUsage) if success else None


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


def verify_premises(p_min: int, p_max: int) -> dict[str, str]:
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    for p in range(p_min, p_max + 1):
        matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        if sha256(matrix_path) != MATRIX_SHA256[p]:
            raise AssertionError({"matrix_sha256": {"p": p, "actual": sha256(matrix_path)}})
        for source, target in INCLUSIONS:
            path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target}.json"
            if sha256(path) != RELATIVE_SHA256[p, source, target]:
                raise AssertionError(
                    {"relative_sha256": {"p": p, "source": source, "target": target}}
                )
    return actual


def aliases(mask: int) -> list[str]:
    return [alias for bit, alias in enumerate(ALIASES) if mask & (1 << bit)]


def rows_for_mask(row_atoms: list[str], mask: int) -> list[int]:
    selected = {ATOM_ALIASES[alias] for alias in aliases(mask)}
    return [row for row, atom in enumerate(row_atoms) if atom in selected]


def reconstruct_labelled_component(
    *,
    exp036: ModuleType,
    exp037: ModuleType,
    exp042: ModuleType,
    p: int,
    budget: Budget,
) -> dict[str, object]:
    """Repeat EXP-042 extraction and retain exact labels omitted from its artifact."""

    basis = exp037.build_basis(exp036, p, 2)
    d_rows = exp037.d_rows_for_basis(exp036, basis, budget)
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
            return exp042.semantic_atom(
                side="row", kind="D", coefficient_tag=product_kind, exterior=exterior, p=p
            )
        exterior, coefficient = codomain[row - k_base]
        return exp042.semantic_atom(
            side="row",
            kind="K",
            coefficient_tag=exp042.interval_tag(
                coefficient, exp042.degree_two_intervals(p)
            ),
            exterior=exterior,
            p=p,
        )

    def row_label(row: int) -> list[object]:
        if row < k_base:
            exterior, product_kind, product_value = d_rows[row]
            return ["D", list(exterior), product_kind, product_value]
        exterior, coefficient = codomain[row - k_base]
        return ["K", list(exterior), coefficient]

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
            print(f"p={p} incidence {column}/{column_count}", flush=True)
            budget.check(f"p={p} incidence")

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

    frozen = json.loads(
        (EXP042 / "artifacts" / f"matrix-p{p}.json").read_text(encoding="utf-8")
    )
    target_hash = frozen["support_hash"]
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
        if support_hasher.hexdigest() != target_hash:
            continue
        if selected is not None:
            raise AssertionError({"p": p, "duplicate_component": target_hash})
        selected = {
            "row_atoms": [row_atom(row) for row in global_rows],
            "row_labels": [row_label(row) for row in global_rows],
            "signed_hash": signed_hasher.hexdigest(),
            "signed_columns_hash": digest(signed_columns),
            "rows": len(global_rows),
            "columns": len(original_columns),
        }
    if selected is None:
        raise AssertionError({"p": p, "component_not_found": target_hash})
    if selected["signed_hash"] != frozen["signed_hash"]:
        raise AssertionError({"p": p, "signed_hash_mismatch": selected["signed_hash"]})
    if selected["rows"] != frozen["rows"] or selected["columns"] != frozen["columns"]:
        raise AssertionError({"p": p, "shape_mismatch": selected})
    budget.check(f"p={p} labelled component")
    return selected


def endpoint_token(
    value: int, intervals: Iterable[tuple[str, int, int]]
) -> list[object]:
    matches = [(tag, first, last) for tag, first, last in intervals if first <= value <= last]
    if len(matches) != 1:
        raise AssertionError({"value": value, "interval_matches": matches})
    tag, first, last = matches[0]
    left = value - first
    right = last - value
    return [tag, "L", left] if left <= right else [tag, "R", right]


def affine_token(value: int, p: int) -> list[int]:
    slope = min(range(25), key=lambda candidate: (abs(value - candidate * p), candidate))
    return [slope, value - slope * p]


def normalize_added_row(label: list[object], p: int) -> dict[str, object]:
    if label[0] != "D":
        raise AssertionError({"non_d_added_row": label})
    exterior = {int(value) for value in label[1]}
    l0 = set(range(1, p + 1))
    l1 = set(range(3 * p, 4 * p - 1))
    generator_intervals = [
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
    high = sorted(exterior - l0 - l1)
    return {
        "kind": str(label[2]),
        "product": affine_token(int(label[3]), p),
        "l0_missing": [endpoint_token(value, [("L0", 1, p)]) for value in sorted(l0 - exterior)],
        "l1_missing": [
            endpoint_token(value, [("L1", 3 * p, 4 * p - 2)])
            for value in sorted(l1 - exterior)
        ],
        "high_selected": [endpoint_token(value, generator_intervals) for value in high],
    }


def canonical_rref(vectors: Iterable[int]) -> list[int]:
    basis: dict[int, int] = {}
    for raw in vectors:
        vector = raw
        for pivot in sorted(basis):
            if (vector >> pivot) & 1:
                vector ^= basis[pivot]
        if not vector:
            continue
        pivot = (vector & -vector).bit_length() - 1
        for other in list(basis):
            if (basis[other] >> pivot) & 1:
                basis[other] ^= vector
        basis[pivot] = vector
    return [basis[pivot] for pivot in sorted(basis)]


def reduce_quotient(vector: int, image_basis: list[int]) -> int:
    for basis_vector in image_basis:
        pivot = (basis_vector & -basis_vector).bit_length() - 1
        if (vector >> pivot) & 1:
            vector ^= basis_vector
    return vector


def kernel_combinations(column_bits: list[int], order: list[int]) -> list[int]:
    pivots: dict[int, tuple[int, int]] = {}
    kernel: list[int] = []
    for column in order:
        vector = column_bits[column]
        combination = 1 << column
        while vector:
            pivot = (vector & -vector).bit_length() - 1
            existing = pivots.get(pivot)
            if existing is None:
                pivots[pivot] = (vector, combination)
                break
            vector ^= existing[0]
            combination ^= existing[1]
        if not vector:
            kernel.append(combination)
    return kernel


def bit_indices(value: int):
    while value:
        least = value & -value
        yield least.bit_length() - 1
        value ^= least


def bockstein_basis(
    columns: list[list[list[int]]], row_count: int, reverse: bool
) -> list[int]:
    column_bits = [
        sum(1 << int(row) for row, value in entries if int(value) & 1)
        for entries in columns
    ]
    image_basis = canonical_rref(column_bits)
    order = list(range(len(columns)))
    if reverse:
        order.reverse()
    quotient_classes: list[int] = []
    for combination in kernel_combinations(column_bits, order):
        boundary: dict[int, int] = {}
        for column in bit_indices(combination):
            for row, value in columns[column]:
                row = int(row)
                boundary[row] = boundary.get(row, 0) + int(value)
        if any(value & 1 for value in boundary.values()):
            raise AssertionError("mod-two cycle has a non-even integral boundary")
        half = sum(1 << row for row, value in boundary.items() if (value // 2) & 1)
        reduced = reduce_quotient(half, image_basis)
        if reduced:
            quotient_classes.append(reduced)
    return canonical_rref(quotient_classes)


def relative_record(
    *, p: int, source: int, target: int, component: dict[str, object]
) -> dict[str, object]:
    row_atoms = component["row_atoms"]
    source_rows = rows_for_mask(row_atoms, source)
    source_set = set(source_rows)
    added_rows = [row for row in rows_for_mask(row_atoms, target) if row not in source_set]
    artifact_path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target}.json"
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    if digest(added_rows) != artifact["added_rows_hash"]:
        raise AssertionError({"p": p, "inclusion": [source, target], "added_rows_hash": False})
    if len(added_rows) != artifact["matrix_shape"][0]:
        raise AssertionError({"p": p, "inclusion": [source, target], "row_count": False})

    tokens = [normalize_added_row(component["row_labels"][row], p) for row in added_rows]
    token_strings = [json.dumps(token, sort_keys=True, separators=(",", ":")) for token in tokens]
    if len(token_strings) != len(set(token_strings)):
        raise AssertionError({"p": p, "inclusion": [source, target], "duplicate_tokens": True})
    semantic_order = sorted(range(len(tokens)), key=lambda row: token_strings[row])
    semantic_position = {old: new for new, old in enumerate(semantic_order)}
    ordered_tokens = [tokens[old] for old in semantic_order]
    columns = [
        sorted([[semantic_position[int(row)], int(value)] for row, value in entries])
        for entries in artifact["matrix_columns"]
    ]
    forward = bockstein_basis(columns, len(tokens), reverse=False)
    reverse = bockstein_basis(columns, len(tokens), reverse=True)
    if forward != reverse:
        raise AssertionError({"p": p, "inclusion": [source, target], "audit": "disagrees"})
    representatives = [
        [ordered_tokens[row] for row in bit_indices(vector)] for vector in forward
    ]
    representative_hashes = [digest(representative) for representative in representatives]
    return {
        "source_mask": source,
        "target_mask": target,
        "added_rows": len(tokens),
        "semantic_row_hash": digest(ordered_tokens),
        "bockstein_rank": len(forward),
        "bockstein_subspace_hash": digest(forward),
        "reverse_agrees": True,
        "support_sizes": [len(representative) for representative in representatives],
        "representative_template_hashes": representative_hashes,
        "representatives": representatives,
    }


def numeric_skeleton(value: object) -> object:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return "#"
    if isinstance(value, list):
        return [numeric_skeleton(item) for item in value]
    if isinstance(value, dict):
        return {key: numeric_skeleton(item) for key, item in sorted(value.items())}
    return value


def numeric_coordinates(value: object) -> list[int]:
    result: list[int] = []
    if isinstance(value, bool):
        return result
    if isinstance(value, int):
        result.append(value)
    elif isinstance(value, list):
        for item in value:
            result.extend(numeric_coordinates(item))
    elif isinstance(value, dict):
        for key in sorted(value):
            result.extend(numeric_coordinates(value[key]))
    return result


def classify_predictions(rows: list[dict[str, object]]) -> dict[str, object]:
    by_key = {
        (int(row["p"]), int(record["source_mask"]), int(record["target_mask"])): record
        for row in rows
        for record in row["inclusions"]
    }
    full = {int(row["p"]) for row in rows} == {8, 9, 10, 11}
    if not full:
        return {
            "p1_status": "NOT_EVALUATED",
            "p2_status": "NOT_EVALUATED",
            "p3_status": "NOT_EVALUATED",
        }
    p1 = all(
        int(by_key[p, source, target]["bockstein_rank"])
        == (2 if (source, target) != (56, 58) else p - 7)
        for p in range(8, 12)
        for source, target in INCLUSIONS
    )
    completion_details: dict[str, object] = {}
    p2 = True
    for source, target in ((58, 59), (58, 62)):
        hashes = [
            sorted(by_key[p, source, target]["representative_template_hashes"])
            for p in range(8, 12)
        ]
        sizes = [by_key[p, source, target]["support_sizes"] for p in range(8, 12)]
        passes = len({json.dumps(value) for value in hashes}) == 1 and max(
            size for group in sizes for size in group
        ) <= 64
        p2 &= passes
        completion_details[f"{source}->{target}"] = {
            "passes": passes,
            "template_hashes_by_p": dict(zip(map(str, range(8, 12)), hashes, strict=True)),
            "support_sizes_by_p": dict(zip(map(str, range(8, 12)), sizes, strict=True)),
        }

    threshold_points: list[tuple[int, int, list[int]]] = []
    skeletons: list[str] = []
    counts_ok = True
    for p in range(8, 12):
        representatives = sorted(
            by_key[p, 56, 58]["representatives"],
            key=lambda value: json.dumps(value, sort_keys=True),
        )
        counts_ok &= len(representatives) == p - 7
        for k, representative in enumerate(representatives, start=1):
            skeletons.append(json.dumps(numeric_skeleton(representative), sort_keys=True))
            threshold_points.append((p, k, numeric_coordinates(representative)))
    skeleton_ok = len(set(skeletons)) == 1
    coordinate_lengths = {len(point[2]) for point in threshold_points}
    affine_formulas: list[list[int]] = []
    affine_ok = skeleton_ok and len(coordinate_lengths) == 1
    if affine_ok:
        coordinate_count = next(iter(coordinate_lengths))
        for coordinate in range(coordinate_count):
            formula: list[int] | None = None
            p0, k0, values0 = threshold_points[0]
            for a in range(-4, 5):
                for b in range(-4, 5):
                    c = values0[coordinate] - a * p0 - b * k0
                    if all(
                        values[coordinate] == a * p + b * k + c
                        for p, k, values in threshold_points
                    ):
                        formula = [a, b, c]
                        break
                if formula is not None:
                    break
            if formula is None:
                affine_ok = False
                break
            affine_formulas.append(formula)
    p3 = counts_ok and skeleton_ok and affine_ok
    return {
        "p1_status": "PASS_FINITE" if p1 else "REFUTED",
        "p2_status": "PASS_FINITE" if p2 else "REFUTED",
        "p3_status": "PASS_FINITE" if p3 else "REFUTED",
        "p2_details": completion_details,
        "p3_details": {
            "counts_ok": counts_ok,
            "single_nonnumeric_skeleton": skeleton_ok,
            "integer_affine_coordinates": affine_ok,
            "affine_formulas_a_p_b_k_c": affine_formulas if affine_ok else [],
            "skeleton_hashes": sorted({digest(value) for value in skeletons}),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=900.0)
    parser.add_argument("--memory-gib", type=float, default=12.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")

    premises = verify_premises(args.p_min, args.p_max)
    exp036 = load_module("exp036_for_exp048", EXP036 / "run.py")
    exp037 = load_module("exp037_for_exp048", EXP037 / "run.py")
    exp042 = load_module("exp042_for_exp048", EXP042 / "run.py")
    budget = Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-048",
        "route": "canonical relative Bockstein image in normalized added-row coordinates",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
        },
        "premise_hashes": premises,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            print(f"p={p} reconstruct labelled isolated component", flush=True)
            component = reconstruct_labelled_component(
                exp036=exp036, exp037=exp037, exp042=exp042, p=p, budget=budget
            )
            print(f"p={p} compute three canonical relative Bocksteins", flush=True)
            inclusions = [
                relative_record(p=p, source=source, target=target, component=component)
                for source, target in INCLUSIONS
            ]
            result["rows"].append(
                {
                    "p": p,
                    "component_rows": component["rows"],
                    "component_columns": component["columns"],
                    "component_signed_hash": component["signed_hash"],
                    "inclusions": inclusions,
                }
            )
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
            print(f"p={p} checkpoint elapsed={budget.elapsed:.3f}s", flush=True)
            budget.check(f"p={p} checkpoint")
            del component
            gc.collect()
    except BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        return 2

    result.update(classify_predictions(result["rows"]))
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
                "ranks": {
                    f"p{row['p']}_{record['source_mask']}_{record['target_mask']}": record[
                        "bockstein_rank"
                    ]
                    for row in result["rows"]
                    for record in row["inclusions"]
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
