"""EXP-037 exact connecting-parity falsifier and quasipolynomial certificate.

CPU only. Canonical bases use the frozen EXP-036 exact-sum constructor. Rank
arithmetic is independently encoded here. The default engine first performs
exact degree-one row cancellation and sends only the residual 2-core to bitset
elimination over GF(2) or reverse sparse elimination over odd prime fields.
Columns are generated on demand; the complete block is never materialized.
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
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Callable, Iterable


HERE = Path(__file__).resolve().parent
EXP036 = HERE.parent / "EXP-036-factor-two-torsion-anatomy"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
PREMISES = {
    "EXP-036 proof": (
        EXP036 / "proof.md",
        "8e1dc8f69dbbd1e0587f33509fc80566bbb1e72e2a991e5db9c07ab2a7d2cc02",
    ),
    "EXP-036 verdict": (
        EXP036 / "verdict.md",
        "d6a86209cf36c8b78fca7bdefbf33ec23872b392c3cae26db7f7611646d69cbc",
    ),
    "EXP-036 run.py": (
        EXP036 / "run.py",
        "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    ),
    "EXP-036 p<=6": (
        EXP036 / "artifacts" / "results-p6.json",
        "b2452d307112b0d6010483cbafbdcde13fa83a46299f6c24b4a490f7e0cdd073",
    ),
    "EXP-036 p=7,8": (
        EXP036 / "artifacts" / "target-t2-p7-p8.json",
        "79da3d9f03ecf5dd7dfee27a8bd69382189214254e419ba7f2facd7e3fa06f31",
    ),
    "EXP-036 p=9": (
        EXP036 / "artifacts" / "target-t2-p9.json",
        "24be490dd4e9a17562d9731f9ec033906824e76b258d1d37afd12d37de732a29",
    ),
}
STORED_FILES = (
    EXP036 / "artifacts" / "results-p6.json",
    EXP036 / "artifacts" / "target-t2-p7-p8.json",
    EXP036 / "artifacts" / "target-t2-p9.json",
)
KNOWN_EXCESS = {4: 1, 5: 4, 6: 9, 7: 18, 8: 31, 9: 49}
REGRESSION_FIELDS = {
    (4, 2): {
        2: (74, 513, 588, 5, 1, 4),
        3: (75, 513, 589, 4, 1, 3),
    },
    (5, 2): {
        2: (223, 2697, 2935, 39, 15, 24),
        3: (223, 2697, 2939, 39, 19, 20),
    },
}


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def verify_premises() -> dict[str, str]:
    actual = {name: file_hash(path) for name, (path, _) in PREMISES.items()}
    expected = {name: expected for name, (_, expected) in PREMISES.items()}
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def load_exp036() -> ModuleType:
    path = EXP036 / "run.py"
    spec = importlib.util.spec_from_file_location("exp036_frozen", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def candidate_closed(p: int) -> int:
    n = p - 4
    if n < 0:
        raise ValueError("require p>=4")
    return (10 * n**3 + 63 * n**2 + 126 * n + 89) // 72


def candidate_lattice(p: int) -> int:
    n = p - 4
    weights = (1, 2, 1, 1)
    total = 0
    for residue, weight in enumerate(weights):
        remaining = n - residue
        if remaining < 0:
            continue
        for c_value in range(remaining // 3 + 1):
            after_c = remaining - 3 * c_value
            for b_value in range(after_c // 2 + 1):
                total += weight * (after_c - 2 * b_value + 1)
    return total


def stored_formula_certificate() -> dict[str, object]:
    rows: dict[int, dict[str, object]] = {}
    for path in STORED_FILES:
        artifact = json.loads(path.read_text(encoding="utf-8"))
        for row in artifact["rows"]:
            if row["t"] == 2:
                rows[row["p"]] = row
    if set(rows) != set(KNOWN_EXCESS):
        raise AssertionError({"stored_t2_parameters": sorted(rows)})

    checks = []
    for p in sorted(rows):
        field_rows = rows[p]["field_rows"]
        actual = (
            field_rows["2"]["surviving_a_dimension"]
            - field_rows["3"]["surviving_a_dimension"]
        )
        closed = candidate_closed(p)
        lattice = candidate_lattice(p)
        expected = KNOWN_EXCESS[p]
        if not actual == expected == closed == lattice:
            raise AssertionError(
                {"p": p, "actual": actual, "expected": expected, "closed": closed, "lattice": lattice}
            )
        checks.append(
            {
                "p": p,
                "stored_excess": actual,
                "closed_formula": closed,
                "lattice_coefficient": lattice,
                "row_hash": rows[p]["row_hash"],
            }
        )

    coefficients = [candidate_lattice(p) for p in range(4, 41)]
    if coefficients != [candidate_closed(p) for p in range(4, 41)]:
        raise AssertionError("closed formula and lattice coefficients disagree")
    return {
        "known_checks": checks,
        "predictions": {"10": candidate_closed(10), "11": candidate_closed(11)},
        "coefficients_p4_p40": coefficients,
        "coefficient_hash": digest(coefficients),
    }


class BudgetStop(RuntimeError):
    pass


class Budget:
    def __init__(self, seconds: float, memory_gib: float) -> None:
        self.started = time.perf_counter()
        self.seconds = seconds
        self.memory_bytes = int(memory_gib * 1024**3)

    @property
    def elapsed(self) -> float:
        return time.perf_counter() - self.started

    def check(self, stage: str) -> None:
        if self.elapsed > self.seconds:
            raise BudgetStop(f"time budget crossed during {stage}")
        private = private_bytes()
        if private is not None and private > self.memory_bytes:
            raise BudgetStop(f"memory budget crossed during {stage}: {private} bytes")


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


class GF2BitsetRank:
    def __init__(self) -> None:
        self.pivots: dict[int, int] = {}

    def add(self, entries: Iterable[tuple[int, int]]) -> None:
        vector = 0
        for row, value in entries:
            if value & 1:
                vector ^= 1 << row
        while vector:
            low_bit = vector & -vector
            pivot = low_bit.bit_length() - 1
            existing = self.pivots.get(pivot)
            if existing is None:
                self.pivots[pivot] = vector
                return
            vector ^= existing

    @property
    def rank(self) -> int:
        return len(self.pivots)


class GF2SparseRank:
    """GF(2) elimination that does not allocate one global-width bitset per pivot."""

    def __init__(self) -> None:
        self.pivots: dict[int, set[int]] = {}

    def add(self, entries: Iterable[tuple[int, int]]) -> None:
        vector = {row for row, value in entries if value & 1}
        while vector:
            pivot = min(vector)
            existing = self.pivots.get(pivot)
            if existing is None:
                self.pivots[pivot] = vector
                return
            vector.symmetric_difference_update(existing)

    @property
    def rank(self) -> int:
        return len(self.pivots)


class SparsePrimeRank:
    def __init__(self, prime: int) -> None:
        self.prime = prime
        self.pivots: dict[int, dict[int, int]] = {}

    def add(self, entries: Iterable[tuple[int, int]]) -> None:
        prime = self.prime
        vector = {row: value % prime for row, value in entries if value % prime}
        while vector:
            pivot = min(vector)
            existing = self.pivots.get(pivot)
            if existing is None:
                inverse = pow(vector[pivot], -1, prime)
                self.pivots[pivot] = {
                    row: value * inverse % prime for row, value in vector.items()
                }
                return
            factor = vector[pivot]
            for row, value in existing.items():
                updated = (vector.get(row, 0) - factor * value) % prime
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)

    @property
    def rank(self) -> int:
        return len(self.pivots)


def rank_accumulator(
    prime: int, *, sparse_gf2: bool = False
) -> GF2BitsetRank | GF2SparseRank | SparsePrimeRank:
    if prime == 2:
        return GF2SparseRank() if sparse_gf2 else GF2BitsetRank()
    return SparsePrimeRank(prime)


def signed_faces(exterior: tuple[int, ...]) -> Iterable[tuple[int, int, tuple[int, ...]]]:
    for position, variable in enumerate(exterior):
        yield variable, (-1 if position % 2 else 1), exterior[:position] + exterior[position + 1 :]


def build_basis(exp036: ModuleType, p: int, t: int) -> dict[str, object]:
    target, selected, degree, total_offset = exp036.predicted_family(p, t)
    generators = tuple(sorted(exp036.degree_one_offsets(p) - {0}))
    low = exp036.low_offsets(p)
    high = exp036.high_offsets(p)
    degree_two = exp036.degree_two_offsets(p)
    codomain = exp036.labelled_subsets(generators, degree, total_offset, degree_two)
    kernel_domain = exp036.labelled_subsets(generators, degree + 1, total_offset, high)
    source = exp036.labelled_subsets(generators, degree + 1, total_offset, low)
    selected_row = (tuple(sorted(selected)), target)
    if selected_row not in set(codomain):
        raise AssertionError("selected row absent")
    return {
        "p": p,
        "t": t,
        "target": target,
        "degree": degree,
        "total_offset": total_offset,
        "generators": generators,
        "low": low,
        "degree_two": degree_two,
        "codomain": codomain,
        "kernel_domain": kernel_domain,
        "source": source,
        "selected_row": selected_row,
        "hashes": {
            "kernel_codomain_hash": digest([[list(e), c] for e, c in codomain]),
            "kernel_domain_hash": digest([[list(e), c] for e, c in kernel_domain]),
            "d_source_hash": digest([[list(e), c] for e, c in source]),
        },
    }


def d_rows_for_basis(exp036: ModuleType, basis: dict[str, object], budget: Budget) -> list[object]:
    p = int(basis["p"])
    low = basis["low"]
    rows: set[object] = set()
    source = basis["source"]
    for index, (exterior, coefficient) in enumerate(source):
        for variable, _, face in signed_faces(exterior):
            if variable in low:
                product = exp036.low_product(p, variable, coefficient)
                if product is not None:
                    rows.add((face, product[0], product[1]))
        if index and index % 50_000 == 0:
            budget.check("D-row enumeration")
            print(f"D rows scan {index}/{len(source)}: {len(rows)} rows", flush=True)
    return sorted(rows, key=repr)


def field_rank(
    exp036: ModuleType,
    basis: dict[str, object],
    d_rows: list[object],
    prime: int,
    budget: Budget,
) -> dict[str, int]:
    p = int(basis["p"])
    low = basis["low"]
    degree_two = basis["degree_two"]
    codomain = basis["codomain"]
    kernel_domain = basis["kernel_domain"]
    source = basis["source"]
    k_index = {row: index for index, row in enumerate(codomain)}
    d_index = {row: index for index, row in enumerate(d_rows)}
    k_base = len(d_rows)
    kernel_rank = rank_accumulator(prime)
    d_rank = rank_accumulator(prime)
    combined_rank = rank_accumulator(prime)

    for count, (exterior, coefficient) in enumerate(reversed(kernel_domain), start=1):
        entries: list[tuple[int, int]] = []
        for variable, sign, face in signed_faces(exterior):
            product_offset = coefficient + variable
            if product_offset in degree_two:
                entries.append((k_index[(face, product_offset)], sign))
        kernel_rank.add(entries)
        combined_rank.add((k_base + row, value) for row, value in entries)
        if count % 50_000 == 0:
            budget.check(f"GF({prime}) kernel rank")
            print(
                f"GF({prime}) K {count}/{len(kernel_domain)} rank={kernel_rank.rank}",
                flush=True,
            )

    for count, (exterior, coefficient) in enumerate(reversed(source), start=1):
        d_entries: list[tuple[int, int]] = []
        combined_entries: list[tuple[int, int]] = []
        for variable, sign, face in signed_faces(exterior):
            if variable in low:
                product = exp036.low_product(p, variable, coefficient)
                if product is not None:
                    row = d_index[(face, product[0], product[1])]
                    d_entries.append((row, sign))
                    combined_entries.append((row, sign))
            else:
                product_offset = variable + coefficient
                if product_offset in degree_two:
                    row = k_index[(face, product_offset)]
                    combined_entries.append((k_base + row, sign))
        d_rank.add(d_entries)
        combined_rank.add(combined_entries)
        if count % 25_000 == 0:
            budget.check(f"GF({prime}) connecting rank")
            print(
                f"GF({prime}) D/J {count}/{len(source)} "
                f"d={d_rank.rank} combined={combined_rank.rank}",
                flush=True,
            )

    rank_kernel = kernel_rank.rank
    rank_d = d_rank.rank
    rank_combined = combined_rank.rank
    kernel_dimension = len(codomain) - rank_kernel
    connecting_dimension = rank_combined - rank_d - rank_kernel
    surviving_dimension = len(codomain) + rank_d - rank_combined
    return {
        "rank_kernel_boundary": rank_kernel,
        "kernel_cokernel_dimension": kernel_dimension,
        "rank_d_boundary": rank_d,
        "rank_combined": rank_combined,
        "connecting_image_dimension_in_kernel_cokernel": connecting_dimension,
        "surviving_a_dimension": surviving_dimension,
    }


EntryFunction = Callable[[int], list[tuple[int, int]]]


def rank_matrix_after_leaf_peeling(
    *,
    label: str,
    row_count: int,
    column_count: int,
    entries_for_column: EntryFunction,
    primes: tuple[int, ...],
    core_order: str,
    budget: Budget,
) -> tuple[dict[int, int], dict[str, object]]:
    """Rank a sparse matrix after exact two-sided leaf cancellation.

    If a row occurs in exactly one active column, that column is independent
    over every field because all entries are signs.  Pivoting there introduces
    no fill.  The transpose statement handles degree-one columns identically.
    Count/XOR sketches recover the unique incident column without storing the
    enormous initial row adjacency.  A compact CSR representation of the
    row-peeled core then supports two-sided cancellation.  Only its final
    bipartite 2-core is sent to field-specific elimination, with static
    low-degree row and column order to control fill.
    """

    counts = array("I", [0]) * row_count
    incident_xor = array("I", [0]) * row_count
    column_sizes = array("I", [0]) * column_count
    initial_nonzeros = 0
    for column in range(column_count):
        entries = entries_for_column(column)
        nonzero_count = 0
        for row, value in entries:
            if not value:
                continue
            nonzero_count += 1
            counts[row] += 1
            incident_xor[row] ^= column
        column_sizes[column] = nonzero_count
        initial_nonzeros += nonzero_count
        if column and column % 50_000 == 0:
            budget.check(f"{label} incidence scan")
            print(
                f"{label} incidence {column}/{column_count}: "
                f"nonzeros={initial_nonzeros}",
                flush=True,
            )

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
            raise AssertionError(f"{label}: stale unique-column sketch")
        active[column] = 0
        row_leaf_pivots += 1
        for adjacent_row, value in entries_for_column(column):
            if not value:
                continue
            if counts[adjacent_row] == 0:
                raise AssertionError(f"{label}: incidence underflow")
            counts[adjacent_row] -= 1
            incident_xor[adjacent_row] ^= column
            if counts[adjacent_row] == 1:
                leaf_rows.append(adjacent_row)
        if row_leaf_pivots % 50_000 == 0:
            budget.check(f"{label} leaf peeling")
            print(
                f"{label} row-peeled {row_leaf_pivots}/{column_count} columns",
                flush=True,
            )

    del incident_xor, leaf_rows
    gc.collect()
    row_only_columns = sum(active)
    row_only_rows = sum(count > 0 for count in counts)
    row_only_nonzeros = sum(counts)
    first_row_map = array("i", [-1]) * row_count
    core_global_rows = array("I")
    local_row = 0
    for row, count in enumerate(counts):
        if count:
            first_row_map[row] = local_row
            core_global_rows.append(row)
            local_row += 1
    if local_row != row_only_rows:
        raise AssertionError(f"{label}: residual row-map mismatch")
    print(
        f"{label} row peel: rank={row_leaf_pivots}, "
        f"core={row_only_rows}x{row_only_columns}, nnz={row_only_nonzeros}",
        flush=True,
    )

    core_original_columns = array("I")
    column_offsets = array("Q", [0])
    edge_rows = array("I")
    column_degrees = array("I")
    for original_column, is_active in enumerate(active):
        if not is_active:
            continue
        mapped_rows = [
            first_row_map[row]
            for row, value in entries_for_column(original_column)
            if value and first_row_map[row] >= 0
        ]
        if not mapped_rows:
            continue
        core_original_columns.append(original_column)
        edge_rows.extend(mapped_rows)
        column_degrees.append(len(mapped_rows))
        column_offsets.append(len(edge_rows))
    del active, first_row_map
    gc.collect()
    if len(edge_rows) != row_only_nonzeros:
        raise AssertionError(f"{label}: CSR nonzero mismatch")

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
    del row_positions, counts
    gc.collect()

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
                raise AssertionError(f"{label}: row leaf degree mismatch")
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
                raise AssertionError(f"{label}: column leaf degree mismatch")
            cancel_pair(neighbors[0], column)
        if two_sided_pivots and two_sided_pivots % 50_000 == 0:
            budget.check(f"{label} two-sided peeling")
            print(
                f"{label} two-sided peeled {two_sided_pivots} more pivots",
                flush=True,
            )

    final_local_rows = [
        row
        for row, is_active in enumerate(active_rows)
        if is_active and row_degrees[row] > 0
    ]
    final_local_columns = [
        column
        for column, is_active in enumerate(active_columns)
        if is_active and column_degrees[column] > 0
    ]
    if core_order == "low-degree":
        final_local_rows.sort(key=row_degrees.__getitem__)
        final_local_columns.sort(key=column_degrees.__getitem__)
    elif core_order == "reverse-low-degree":
        final_local_rows.sort(key=row_degrees.__getitem__, reverse=True)
        final_local_columns.sort(key=column_degrees.__getitem__, reverse=True)
    elif core_order != "canonical":
        raise ValueError(f"unknown core order: {core_order}")
    final_row_map = array("i", [-1]) * row_count
    for new_row, old_row in enumerate(final_local_rows):
        final_row_map[core_global_rows[old_row]] = new_row
    final_original_columns = [
        core_original_columns[column] for column in final_local_columns
    ]
    residual_rows = len(final_local_rows)
    residual_columns = len(final_original_columns)
    residual_nonzeros = sum(row_degrees[row] for row in final_local_rows)
    peeled_rank = row_leaf_pivots + two_sided_pivots
    del (
        core_global_rows,
        core_original_columns,
        final_local_rows,
        final_local_columns,
    )
    gc.collect()
    budget.check(f"{label} residual start")
    print(
        f"{label} two-sided peel complete: rank={peeled_rank}, "
        f"2-core={residual_rows}x{residual_columns}, nnz={residual_nonzeros}",
        flush=True,
    )

    ranks: dict[int, int] = {}
    core_ranks: dict[str, int] = {}
    for prime in primes:
        accumulator = rank_accumulator(prime, sparse_gf2=residual_rows > 50_000)
        processed = 0
        for column in final_original_columns:
            entries = [
                (final_row_map[row], value)
                for row, value in entries_for_column(column)
                if final_row_map[row] >= 0 and value
            ]
            accumulator.add(entries)
            processed += 1
            if processed % 10_000 == 0:
                budget.check(f"{label} GF({prime}) residual rank")
                print(
                    f"{label} GF({prime}) core {processed}/{residual_columns}: "
                    f"rank={accumulator.rank}",
                    flush=True,
                )
        core_rank = accumulator.rank
        ranks[prime] = peeled_rank + core_rank
        core_ranks[str(prime)] = core_rank
        del accumulator
        gc.collect()
        budget.check(f"{label} GF({prime}) residual complete")

    profile = {
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
        "residual_rows": residual_rows,
        "residual_columns": residual_columns,
        "residual_nonzeros": residual_nonzeros,
        "core_order": core_order,
        "core_ranks": core_ranks,
    }
    return ranks, profile


def peeling_field_ranks(
    exp036: ModuleType,
    basis: dict[str, object],
    d_rows: list[object],
    primes: tuple[int, ...],
    core_order: str,
    budget: Budget,
) -> tuple[dict[int, dict[str, int]], dict[str, dict[str, object]]]:
    """Compute K, D, and combined ranks with a shared structural strategy."""

    p = int(basis["p"])
    low = basis["low"]
    degree_two = basis["degree_two"]
    codomain = basis["codomain"]
    kernel_domain = basis["kernel_domain"]
    source = basis["source"]
    k_index = {row: index for index, row in enumerate(codomain)}
    d_index = {row: index for index, row in enumerate(d_rows)}
    k_base = len(d_rows)

    def kernel_entries(column: int) -> list[tuple[int, int]]:
        exterior, coefficient = kernel_domain[column]
        entries: list[tuple[int, int]] = []
        for variable, sign, face in signed_faces(exterior):
            product_offset = coefficient + variable
            if product_offset in degree_two:
                entries.append((k_index[(face, product_offset)], sign))
        return entries

    def source_entries(column: int, include_connecting: bool) -> list[tuple[int, int]]:
        exterior, coefficient = source[column]
        entries: list[tuple[int, int]] = []
        for variable, sign, face in signed_faces(exterior):
            if variable in low:
                product = exp036.low_product(p, variable, coefficient)
                if product is not None:
                    entries.append((d_index[(face, product[0], product[1])], sign))
            elif include_connecting:
                product_offset = variable + coefficient
                if product_offset in degree_two:
                    entries.append((k_base + k_index[(face, product_offset)], sign))
        return entries

    def d_entries(column: int) -> list[tuple[int, int]]:
        return source_entries(column, False)

    def combined_entries(column: int) -> list[tuple[int, int]]:
        if column < len(source):
            return source_entries(column, True)
        return [
            (k_base + row, value)
            for row, value in kernel_entries(column - len(source))
        ]

    kernel_ranks, kernel_profile = rank_matrix_after_leaf_peeling(
        label="K",
        row_count=len(codomain),
        column_count=len(kernel_domain),
        entries_for_column=kernel_entries,
        primes=primes,
        core_order=core_order,
        budget=budget,
    )
    d_ranks, d_profile = rank_matrix_after_leaf_peeling(
        label="D",
        row_count=len(d_rows),
        column_count=len(source),
        entries_for_column=d_entries,
        primes=primes,
        core_order=core_order,
        budget=budget,
    )
    combined_ranks, combined_profile = rank_matrix_after_leaf_peeling(
        label="M",
        row_count=len(d_rows) + len(codomain),
        column_count=len(source) + len(kernel_domain),
        entries_for_column=combined_entries,
        primes=primes,
        core_order=core_order,
        budget=budget,
    )
    field_rows: dict[int, dict[str, int]] = {}
    for prime in primes:
        rank_kernel = kernel_ranks[prime]
        rank_d = d_ranks[prime]
        rank_combined = combined_ranks[prime]
        field_rows[prime] = {
            "rank_kernel_boundary": rank_kernel,
            "kernel_cokernel_dimension": len(codomain) - rank_kernel,
            "rank_d_boundary": rank_d,
            "rank_combined": rank_combined,
            "connecting_image_dimension_in_kernel_cokernel": (
                rank_combined - rank_d - rank_kernel
            ),
            "surviving_a_dimension": len(codomain) + rank_d - rank_combined,
        }
    return field_rows, {
        "kernel": kernel_profile,
        "d_boundary": d_profile,
        "combined": combined_profile,
    }


def assert_regression(p: int, t: int, prime: int, row: dict[str, int]) -> None:
    expected = REGRESSION_FIELDS.get((p, t), {}).get(prime)
    if expected is None:
        return
    actual = (
        row["rank_kernel_boundary"],
        row["rank_d_boundary"],
        row["rank_combined"],
        row["kernel_cokernel_dimension"],
        row["connecting_image_dimension_in_kernel_cokernel"],
        row["surviving_a_dimension"],
    )
    if actual != expected:
        raise AssertionError({"regression": [p, t, prime], "actual": actual, "expected": expected})


def compact_basis_record(basis: dict[str, object], d_rows: list[object]) -> dict[str, object]:
    return {
        "p": basis["p"],
        "t": basis["t"],
        "target_offset": basis["target"],
        "homological_degree": basis["degree"],
        "total_offset": basis["total_offset"],
        "kernel_codomain_rows": len(basis["codomain"]),
        "kernel_domain_columns": len(basis["kernel_domain"]),
        "d_source_columns": len(basis["source"]),
        "d_codomain_rows": len(d_rows),
        **basis["hashes"],
        "field_rows": {},
        "predicted_excess": candidate_closed(int(basis["p"])),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cell", action="append", default=[], help="complete target p:t")
    parser.add_argument("--fields", default="2,3")
    parser.add_argument("--formula-only", action="store_true")
    parser.add_argument(
        "--engine",
        choices=("peel", "streaming"),
        default="peel",
        help="exact rank engine; streaming is retained as a small-cell audit",
    )
    parser.add_argument(
        "--core-order",
        choices=("low-degree", "canonical", "reverse-low-degree"),
        default="low-degree",
        help="residual row/column order; alternate orders provide rank audits",
    )
    parser.add_argument("--budget-seconds", type=float, default=1800.0)
    parser.add_argument("--memory-gib", type=float, default=24.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    fields = tuple(int(value) for value in args.fields.split(",") if value)
    if any(value < 2 for value in fields):
        raise ValueError("fields must be prime integers")

    cells: list[tuple[int, int]] = []
    for raw in args.cell:
        p_text, t_text = raw.split(":", maxsplit=1)
        p, t = int(p_text), int(t_text)
        if p < 4 or not 2 <= t <= p - 2:
            raise ValueError(f"invalid cell {(p, t)}")
        cells.append((p, t))

    budget = Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-037",
        "route": "quasipolynomial falsifier with exact leaf-peeling field ranks",
        "status": "RUNNING",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "cells": [list(cell) for cell in cells],
            "fields": list(fields),
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
            "engine": args.engine,
            "core_order": args.core_order,
        },
        "premise_hashes": verify_premises(),
        "formula_certificate": stored_formula_certificate(),
        "rows": [],
    }
    write_json_atomic(args.output, result)
    print(
        "formula regression: PASS; predictions e_10=73, e_11=104",
        flush=True,
    )
    if args.formula_only or not cells:
        result["status"] = "PASS_FORMULA_REGRESSION_ONLY"
        result["elapsed_seconds"] = round(budget.elapsed, 6)
        result["artifact_sha256"] = digest(result)
        write_json_atomic(args.output, result)
        return 0

    exp036 = load_exp036()
    try:
        for p, t in cells:
            budget.check("basis start")
            print(f"building complete basis for ({p},{t})", flush=True)
            basis = build_basis(exp036, p, t)
            print(
                f"basis ({p},{t}): K rows={len(basis['codomain'])}, "
                f"K cols={len(basis['kernel_domain'])}, D cols={len(basis['source'])}",
                flush=True,
            )
            d_rows = d_rows_for_basis(exp036, basis, budget)
            row = compact_basis_record(basis, d_rows)
            result["rows"].append(row)
            result["elapsed_seconds"] = round(budget.elapsed, 6)
            write_json_atomic(args.output, result)
            print(f"basis checkpoint: D rows={len(d_rows)}", flush=True)

            if args.engine == "peel":
                print("starting exact leaf-peeling ranks", flush=True)
                all_field_rows, profiles = peeling_field_ranks(
                    exp036, basis, d_rows, fields, args.core_order, budget
                )
                row["structural_profiles"] = profiles
                for prime, field_row in all_field_rows.items():
                    assert_regression(p, t, prime, field_row)
                    row["field_rows"][str(prime)] = field_row
                    print(
                        f"GF({prime}) complete: "
                        f"K={field_row['kernel_cokernel_dimension']}, "
                        f"image={field_row['connecting_image_dimension_in_kernel_cokernel']}, "
                        f"A={field_row['surviving_a_dimension']}",
                        flush=True,
                    )
                result["elapsed_seconds"] = round(budget.elapsed, 6)
                write_json_atomic(args.output, result)
            else:
                for prime in fields:
                    budget.check(f"GF({prime}) start")
                    print(f"starting GF({prime}) reverse streaming ranks", flush=True)
                    field_row = field_rank(exp036, basis, d_rows, prime, budget)
                    assert_regression(p, t, prime, field_row)
                    row["field_rows"][str(prime)] = field_row
                    result["elapsed_seconds"] = round(budget.elapsed, 6)
                    write_json_atomic(args.output, result)
                    print(
                        f"GF({prime}) complete: "
                        f"K={field_row['kernel_cokernel_dimension']}, "
                        f"image={field_row['connecting_image_dimension_in_kernel_cokernel']}, "
                        f"A={field_row['surviving_a_dimension']}",
                        flush=True,
                    )

            if 2 in fields and 3 in fields:
                actual = (
                    row["field_rows"]["2"]["surviving_a_dimension"]
                    - row["field_rows"]["3"]["surviving_a_dimension"]
                )
                row["actual_excess"] = actual
                row["candidate_matches"] = actual == row["predicted_excess"]
                if not row["candidate_matches"]:
                    result["status"] = "REFUTED_QUASIPOLYNOMIAL"
                    result["elapsed_seconds"] = round(budget.elapsed, 6)
                    result["artifact_sha256"] = digest(result)
                    write_json_atomic(args.output, result)
                    print(
                        f"candidate REFUTED at p={p}: actual {actual}, "
                        f"predicted {row['predicted_excess']}",
                        flush=True,
                    )
                    return 1
            row["row_hash"] = digest(row)
            write_json_atomic(args.output, result)
    except BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["stop_reason"] = str(error)
        result["elapsed_seconds"] = round(budget.elapsed, 6)
        result["private_bytes_at_stop"] = private_bytes()
        result["artifact_sha256"] = digest(result)
        write_json_atomic(args.output, result)
        print(f"INCONCLUSIVE_RESOURCE_BUDGET: {error}", flush=True)
        return 2

    result["status"] = "PASS_FINITE_OUT_OF_SAMPLE"
    result["elapsed_seconds"] = round(budget.elapsed, 6)
    result["artifact_sha256"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
