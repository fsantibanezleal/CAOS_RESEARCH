"""EXP-049 exact lifts and dual parity certificates for completion chains.

CPU only. Exact integer HNF and bit-packed GF(2) arithmetic.
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
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Iterable

import flint
from flint import fmpz_mat


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP047 = EXPERIMENTS / "EXP-047-relative-kernel-smith"
EXP048 = EXPERIMENTS / "EXP-048-semantic-relative-bockstein"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
INCLUSIONS = ((58, 59), (58, 62))
PREMISES = {
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP047 / "run.py": "1350159ebc2c718208f62e08231f54ae2cc6178aa653bb5b67c100b56cd2a82b",
    EXP047 / "artifacts" / "results.json": (
        "f78d251ae1746a88d1190756572aa251b9daf70ceb103cef9765c6d73b26f46c"
    ),
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
    EXP048 / "artifacts" / "results.json": (
        "ba44eae4c9193bc941411b059dc7a7d7a4c69dff3d818e05d3395338e125a400"
    ),
}


class BudgetStop(RuntimeError):
    """Raised only between deterministic exact stages."""


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
    process = kernel32.GetCurrentProcess()
    success = kernel32.K32GetProcessMemoryInfo(
        process, ctypes.byref(counters), counters.cb
    )
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
    exp047 = json.loads((EXP047 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    relative_hashes = {
        (int(row["p"]), int(record["source_mask"]), int(record["target_mask"])): str(
            record["relative_artifact_sha256"]
        )
        for row in exp047["rows"]
        for record in row["inclusions"]
    }
    for p in range(p_min, p_max + 1):
        for source, target in INCLUSIONS:
            path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target}.json"
            if sha256(path) != relative_hashes[p, source, target]:
                raise AssertionError({"relative_sha256": str(path)})
    return actual


def bit_indices(value: int) -> Iterable[int]:
    while value:
        least = value & -value
        yield least.bit_length() - 1
        value ^= least


def sparse_vector(values: list[int]) -> list[list[int]]:
    return [[index, value] for index, value in enumerate(values) if value]


def dense_vector(entries: list[list[int]], length: int) -> list[int]:
    result = [0] * length
    for index, value in entries:
        result[int(index)] = int(value)
    return result


def atom_values(matrix: dict[str, object], side: str) -> list[str]:
    table = matrix[f"{side}_atom_table"]
    return [table[int(index)] for index in matrix[f"{side}_atom_ids"]]


def semantic_rows(
    *, exp047: ModuleType, exp048: ModuleType, component: dict[str, object], p: int,
    source: int, target: int
) -> tuple[list[int], list[list[object]], list[int]]:
    row_atoms = component["row_atoms"]
    source_rows = exp047.rows_for_mask(row_atoms, source)
    source_set = set(source_rows)
    added_rows = [
        row for row in exp047.rows_for_mask(row_atoms, target) if row not in source_set
    ]
    tokens = [exp048.normalize_added_row(component["row_labels"][row], p) for row in added_rows]
    token_strings = [json.dumps(token, sort_keys=True, separators=(",", ":")) for token in tokens]
    semantic_order = sorted(range(len(tokens)), key=lambda row: token_strings[row])
    return added_rows, tokens, semantic_order


def find_added_row(
    labels: list[list[object]], *, exterior: set[int], kind: str, product: int
) -> int:
    matches = [
        index
        for index, label in enumerate(labels)
        if str(label[0]) == "D"
        and set(map(int, label[1])) == exterior
        and str(label[2]) == kind
        and int(label[3]) == product
    ]
    if len(matches) != 1:
        raise AssertionError(
            {"formula_row_match_count": len(matches), "kind": kind, "product": product}
        )
    return matches[0]


def formula_chains(
    *, p: int, source: int, target: int, added_labels: list[list[object]]
) -> list[list[int]]:
    l0 = set(range(1, p + 1))
    l1 = set(range(3 * p, 4 * p - 1))
    chains: list[list[int]] = []
    if (source, target) == (58, 59):
        for j in (1, 2):
            rows = []
            for w in range(4, p + 1):
                if w == p - 1 - j:
                    continue
                exterior = (
                    (l0 - {p - 1 - j, w})
                    | (l1 - {3 * p, 3 * p + j})
                    | {6 * p, 10 * p}
                )
                rows.append(
                    find_added_row(
                        added_labels,
                        exterior=exterior,
                        kind="A",
                        product=p + w - 3,
                    )
                )
            chains.append(sorted(rows))
    elif (source, target) == (58, 62):
        rows = []
        for r in (1, 2):
            for v in range(3, p - 1):
                exterior = (
                    (l0 - {p - 2})
                    | (l1 - {3 * p, 3 * p + r, 3 * p + v})
                    | {6 * p, 10 * p}
                )
                rows.append(
                    find_added_row(
                        added_labels,
                        exterior=exterior,
                        kind="B",
                        product=4 * p + v + r - 4,
                    )
                )
        chains.append(sorted(set(rows)))
        rows = []
        for v in range(3, p - 1):
            exterior = (
                (l0 - {p - 3})
                | (l1 - {3 * p, 3 * p + 2, 3 * p + v})
                | {6 * p, 10 * p}
            )
            rows.append(
                find_added_row(
                    added_labels,
                    exterior=exterior,
                    kind="B",
                    product=4 * p + v - 3,
                )
            )
        chains.append(sorted(set(rows)))
    else:
        raise AssertionError((source, target))
    return chains


def verify_exp048_representatives(
    *, p: int, source: int, target: int, chains: list[list[int]],
    tokens: list[dict[str, object]], semantic_order: list[int], stored: dict[str, object]
) -> list[list[int]]:
    semantic_position = {old: new for new, old in enumerate(semantic_order)}
    reconstructed = []
    for chain in chains:
        ordered = sorted((tokens[row] for row in chain), key=lambda value: json.dumps(value, sort_keys=True))
        reconstructed.append(ordered)
    expected = sorted(
        (json.dumps(value, sort_keys=True, separators=(",", ":")) for value in stored["representatives"])
    )
    actual = sorted(
        json.dumps(value, sort_keys=True, separators=(",", ":")) for value in reconstructed
    )
    if actual != expected:
        raise AssertionError({"p": p, "inclusion": [source, target], "formula_mismatch": True})
    return [sorted(semantic_position[row] for row in chain) for chain in chains]


def sparse_columns_to_transpose(
    columns: list[list[list[int]]], row_count: int
) -> fmpz_mat:
    matrix = fmpz_mat(len(columns), row_count)
    for column, entries in enumerate(columns):
        for row, value in entries:
            matrix[column, int(row)] = int(value)
    return matrix


def hnf_lattice_solver(
    columns: list[list[list[int]]], row_count: int
) -> tuple[fmpz_mat, fmpz_mat, list[int]]:
    hnf, transform = sparse_columns_to_transpose(columns, row_count).hnf(transform=True)
    pivots: list[int] = []
    for row in range(hnf.nrows()):
        pivot = next((column for column in range(hnf.ncols()) if hnf[row, column]), None)
        if pivot is None:
            break
        pivots.append(pivot)
    return hnf, transform, pivots


def solve_row_lattice(
    hnf: fmpz_mat, transform: fmpz_mat, pivots: list[int], target: list[int]
) -> list[int] | None:
    residual = list(target)
    coordinates = [0] * hnf.nrows()
    for row, pivot in enumerate(pivots):
        divisor = int(hnf[row, pivot])
        quotient, remainder = divmod(residual[pivot], divisor)
        if remainder:
            return None
        coordinates[row] = quotient
        if quotient:
            for column in range(hnf.ncols()):
                residual[column] -= quotient * int(hnf[row, column])
    if any(residual):
        return None
    return [
        sum(coordinates[row] * int(transform[row, column]) for row in range(len(pivots)))
        for column in range(transform.ncols())
    ]


def multiply_sparse_columns(
    columns: list[list[list[int]]], vector: list[int], row_count: int
) -> list[int]:
    result = [0] * row_count
    for column, coefficient in enumerate(vector):
        if coefficient:
            for row, value in columns[column]:
                result[int(row)] += coefficient * int(value)
    return result


def projected_product(
    columns: list[list[list[int]]], vector: list[int], selected_rows: list[int]
) -> list[int]:
    row_map = {row: index for index, row in enumerate(selected_rows)}
    result = [0] * len(selected_rows)
    for column, coefficient in enumerate(vector):
        if not coefficient:
            continue
        for row, value in columns[column]:
            projected = row_map.get(int(row))
            if projected is not None:
                result[projected] += coefficient * int(value)
    return result


def left_dual(
    columns: list[list[list[int]]], chains: list[list[int]], row_count: int, high: bool
) -> list[int]:
    equations: list[tuple[int, int]] = [
        (sum(1 << int(row) for row, value in entries if int(value) & 1), 0)
        for entries in columns
    ]
    chain_bits = [sum(1 << row for row in chain) for chain in chains]
    duals: list[int] = []
    for wanted in range(2):
        system = list(equations)
        system.extend((chain_bits[index], int(index == wanted)) for index in range(2))
        basis: dict[int, tuple[int, int]] = {}
        for raw_bits, raw_rhs in system:
            bits, rhs = raw_bits, raw_rhs
            while bits:
                pivot = bits.bit_length() - 1 if high else (bits & -bits).bit_length() - 1
                existing = basis.get(pivot)
                if existing is None:
                    for other, (other_bits, other_rhs) in list(basis.items()):
                        if (other_bits >> pivot) & 1:
                            basis[other] = (other_bits ^ bits, other_rhs ^ rhs)
                    basis[pivot] = (bits, rhs)
                    break
                bits ^= existing[0]
                rhs ^= existing[1]
            if not bits and rhs:
                raise AssertionError({"dual_system_inconsistent": wanted, "high": high})
        solution = 0
        pivot_order = sorted(basis) if high else sorted(basis, reverse=True)
        for pivot in pivot_order:
            bits, rhs = basis[pivot]
            known = (bits & solution).bit_count() & 1
            if known != rhs:
                solution |= 1 << pivot
        if solution >> row_count:
            raise AssertionError("dual index outside row range")
        duals.append(solution)
    return duals


def parity(value: int, rows: Iterable[int]) -> int:
    return sum((value >> row) & 1 for row in rows) & 1


def verify_duals(
    columns: list[list[list[int]]], chains: list[list[int]], duals: list[int]
) -> dict[str, object]:
    annihilation = [
        all(parity(dual, (int(row) for row, value in entries if int(value) & 1)) == 0 for entries in columns)
        for dual in duals
    ]
    pairings = [[parity(dual, chain) for chain in chains] for dual in duals]
    return {
        "annihilation": annihilation,
        "pairings": pairings,
        "support_sizes": [dual.bit_count() for dual in duals],
        "supports": [list(bit_indices(dual)) for dual in duals],
    }


def add_semantic_dual_supports(
    record: dict[str, object], tokens: list[dict[str, object]]
) -> dict[str, object]:
    return record | {
        "semantic_supports": [
            [tokens[row] for row in support] for support in record["supports"]
        ]
    }


def chain_record(
    *, index: int, chain: list[int], relative_columns: list[list[list[int]]],
    y: list[int] | None, kernel_rows: list[list[int]] | None,
    full_columns: list[list[list[int]]], source_rows: list[int], added_rows: list[int],
    column_atoms: list[str]
) -> dict[str, object]:
    target = [2 if row in set(chain) else 0 for row in range(len(added_rows))]
    if y is None:
        return {
            "chain_index": index,
            "chain_rows": chain,
            "chain_hash": digest(chain),
            "support_size": len(chain),
            "exact_membership": False,
        }
    if kernel_rows is None:
        raise AssertionError("source kernel required for an exact relative witness")
    if multiply_sparse_columns(relative_columns, y, len(target)) != target:
        raise AssertionError({"relative_multiplication": index})
    x = [
        sum(y[row] * kernel_rows[row][column] for row in range(len(kernel_rows)))
        for column in range(len(full_columns))
    ]
    source_boundary = projected_product(full_columns, x, source_rows)
    added_boundary = projected_product(full_columns, x, added_rows)
    if any(source_boundary) or added_boundary != target:
        raise AssertionError({"source_lift_verification": index})
    histogram = Counter(column_atoms[column] for column, value in enumerate(x) if value)
    return {
        "chain_index": index,
        "chain_rows": chain,
        "chain_hash": digest(chain),
        "support_size": len(chain),
        "exact_membership": True,
        "relative_witness": sparse_vector(y),
        "relative_witness_hash": digest(y),
        "relative_support_size": sum(bool(value) for value in y),
        "relative_max_abs": max(map(abs, y), default=0),
        "source_cycle": sparse_vector(x),
        "source_cycle_hash": digest(x),
        "source_support_size": sum(bool(value) for value in x),
        "source_max_abs": max(map(abs, x), default=0),
        "source_atom_histogram": dict(sorted(histogram.items())),
        "source_only_atoms": all(json.loads(atom)[1] == "S" for atom in histogram),
        "source_annihilation": True,
        "added_boundary_twice_chain": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=2400.0)
    parser.add_argument("--memory-gib", type=float, default=24.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")
    if flint.__version__ != "0.9.0":
        raise RuntimeError(f"python-flint 0.9.0 required, found {flint.__version__}")

    premises = verify_premises(args.p_min, args.p_max)
    exp036 = load_module("exp036_for_exp049", EXP048.parent / "EXP-036-factor-two-torsion-anatomy" / "run.py")
    exp037 = load_module("exp037_for_exp049", EXP048.parent / "EXP-037-connecting-quasipolynomial" / "run.py")
    exp042 = load_module("exp042_for_exp049", EXP042 / "run.py")
    exp047 = load_module("exp047_for_exp049", EXP047 / "run.py")
    exp048 = load_module("exp048_for_exp049", EXP048 / "run.py")
    stored048 = json.loads((EXP048 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    stored_records = {
        (int(row["p"]), int(record["source_mask"]), int(record["target_mask"])): record
        for row in stored048["rows"]
        for record in row["inclusions"]
    }
    budget = Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-049",
        "route": "exact lattice lifts and dual parity certificates for EXP-048 chains",
        "status": "RUNNING",
        "engine": {"python_flint": flint.__version__},
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
            print(f"p={p} reconstruct semantic component", flush=True)
            component = exp048.reconstruct_labelled_component(
                exp036=exp036, exp037=exp037, exp042=exp042, p=p, budget=budget
            )
            matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            full_columns = matrix["signed_columns"]
            row_atoms = atom_values(matrix, "row")
            column_atoms = atom_values(matrix, "column")
            if component["signed_columns_hash"] != digest(full_columns):
                raise AssertionError({"p": p, "signed_column_reconstruction": False})
            source_rows = exp047.rows_for_mask(row_atoms, 58)
            kernel_rows: list[list[int]] | None = None
            source_kernel: dict[str, object] = {
                "status": "NOT_COMPUTED_UNLESS_EXACT_MEMBERSHIP_PASSES"
            }
            p_record: dict[str, object] = {
                "p": p,
                "source_matrix_sha256": sha256(matrix_path),
                "source_kernel": source_kernel,
                "inclusions": [],
            }
            for source, target_mask in INCLUSIONS:
                print(f"p={p} {source}->{target_mask} exact chain lifts", flush=True)
                relative_path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target_mask}.json"
                relative = json.loads(relative_path.read_text(encoding="utf-8"))
                relative_columns = relative["matrix_columns"]
                added_rows, tokens, semantic_order = semantic_rows(
                    exp047=exp047,
                    exp048=exp048,
                    component=component,
                    p=p,
                    source=source,
                    target=target_mask,
                )
                added_labels = [component["row_labels"][row] for row in added_rows]
                chains = formula_chains(
                    p=p, source=source, target=target_mask, added_labels=added_labels
                )
                semantic_chains = verify_exp048_representatives(
                    p=p,
                    source=source,
                    target=target_mask,
                    chains=chains,
                    tokens=tokens,
                    semantic_order=semantic_order,
                    stored=stored_records[p, source, target_mask],
                )
                hnf, transform, pivots = hnf_lattice_solver(
                    relative_columns, len(added_rows)
                )
                targets = [
                    [2 if row in set(chain) else 0 for row in range(len(added_rows))]
                    for chain in chains
                ]
                solutions = [
                    solve_row_lattice(hnf, transform, pivots, target_vector)
                    for target_vector in targets
                ]
                if any(solution is not None for solution in solutions) and kernel_rows is None:
                    print(f"p={p} compute saturated mask-58 source kernel", flush=True)
                    kernel_rows, source_kernel = exp047.saturated_kernel(
                        full_columns, source_rows
                    )
                    budget.check(f"p={p} source kernel")
                    if relative["kernel_basis_hash"] != source_kernel["kernel_basis_hash"]:
                        raise AssertionError({"p": p, "kernel_hash": False})
                chain_records = [
                    chain_record(
                        index=index + 1,
                        chain=chain,
                        relative_columns=relative_columns,
                        y=solutions[index],
                        kernel_rows=kernel_rows,
                        full_columns=full_columns,
                        source_rows=source_rows,
                        added_rows=added_rows,
                        column_atoms=column_atoms,
                    )
                    for index, chain in enumerate(chains)
                ]
                low = add_semantic_dual_supports(
                    verify_duals(
                        relative_columns,
                        chains,
                        left_dual(relative_columns, chains, len(added_rows), high=False),
                    ),
                    tokens,
                )
                high = add_semantic_dual_supports(
                    verify_duals(
                        relative_columns,
                        chains,
                        left_dual(relative_columns, chains, len(added_rows), high=True),
                    ),
                    tokens,
                )
                expected_pairings = [[1, 0], [0, 1]]
                if (
                    low["annihilation"] != [True, True]
                    or high["annihilation"] != [True, True]
                    or low["pairings"] != expected_pairings
                    or high["pairings"] != expected_pairings
                ):
                    raise AssertionError(
                        {
                            "p": p,
                            "inclusion": [source, target_mask],
                            "duals": False,
                            "low": low,
                            "high": high,
                        }
                    )
                p_record["inclusions"].append(
                    {
                        "source_mask": source,
                        "target_mask": target_mask,
                        "relative_sha256": sha256(relative_path),
                        "added_rows": len(added_rows),
                        "formula_semantic_chain_rows": semantic_chains,
                        "hnf_rank": len(pivots),
                        "hnf_diagonal": [abs(int(hnf[row, pivot])) for row, pivot in enumerate(pivots)],
                        "chains": chain_records,
                        "dual_low": low,
                        "dual_high": high,
                    }
                )
                result["status"] = "CHECKPOINT"
                result["elapsed_seconds"] = budget.elapsed
                write_json_atomic(args.output, result | {"rows": result["rows"] + [p_record]})
                budget.check(f"p={p} {source}->{target_mask}")
            p_record["source_kernel"] = source_kernel
            result["rows"].append(p_record)
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
            del component, matrix, full_columns, kernel_rows
            gc.collect()
    except BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        return 2

    all_chains = [
        chain
        for row in result["rows"]
        for inclusion in row["inclusions"]
        for chain in inclusion["chains"]
    ]
    p1 = all(chain["exact_membership"] for chain in all_chains)
    p2 = p1 and all(chain["source_only_atoms"] for chain in all_chains)
    p3 = all(
        inclusion["dual_low"]["annihilation"] == [True, True]
        and inclusion["dual_low"]["pairings"] == [[1, 0], [0, 1]]
        and inclusion["dual_high"]["annihilation"] == [True, True]
        and inclusion["dual_high"]["pairings"] == [[1, 0], [0, 1]]
        for row in result["rows"]
        for inclusion in row["inclusions"]
    )
    result["p1_status"] = "PASS_FINITE" if p1 else "REFUTED"
    result["p2_status"] = "PASS_FINITE" if p2 else "REFUTED"
    result["p3_status"] = "PASS_FINITE" if p3 else "REFUTED"
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
                "memberships": [chain["exact_membership"] for chain in all_chains],
                "source_supports": [chain.get("source_support_size") for chain in all_chains],
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
