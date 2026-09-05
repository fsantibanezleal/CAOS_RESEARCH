"""Bounded original-incidence image search over QQ, CPU only, with source provenance."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
MAX_COLUMNS = 1200
MAX_NNZ = 20000
MAX_SECONDS = 60
MAX_PRIVATE_BYTES = 1024 ** 3
PREMISES = {
    "EXP-058-local-endpoint-source/hypothesis.md":
        "f538be10015e085851e7a355df97dc73018fc6aa1d4da89c88692ccff18ed7b4",
    "EXP-057-four-row-kernel-normal-form/run.py":
        "e07ea055a55df8faa909653b763aa95cc07a42b40fde552fbc7043dc1299b05d",
    "EXP-054-full-source-boundary/run.py":
        "bb6c35f36da17d4e4045670348416a18d9cbb28bf5f5774fcf1deabf28ed951f",
    "EXP-054-full-source-boundary/audit.py":
        "9e21b8a03694938e04dc7aba3555944fa511e4d1ac0d4dfc92727288ed7a1b63",
    "EXP-036-factor-two-torsion-anatomy/run.py":
        "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def label_key(label):
    return label[0], tuple(label[1]), *label[2:]


def full_label(key):
    return [key[0], list(key[1]), *key[2:]]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENTS / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dependencies():
    for relative, expected in PREMISES.items():
        if hashlib.sha256((EXPERIMENTS / relative).read_bytes()).hexdigest() != expected:
            raise AssertionError(f"premise hash mismatch: {relative}")
    return {
        "primary": load("primary054_for_058", "EXP-054-full-source-boundary/run.py"),
        "algebra": load("algebra036_for_058", "EXP-036-factor-two-torsion-anatomy/run.py"),
        "endpoint": load("endpoint057_for_058", "EXP-057-four-row-kernel-normal-form/run.py"),
    }


def private_bytes():
    if os.name != "nt":
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024

    class Counters(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("faults", ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in (
                "peak_working", "working", "peak_paged", "paged", "peak_nonpaged",
                "nonpaged", "pagefile", "peak_pagefile", "private",
            )
        ]

    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    query = ctypes.windll.psapi.GetProcessMemoryInfo
    query.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
    query.restype = ctypes.c_int
    if not query(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
        raise OSError("cannot enforce process private-memory budget")
    return counters.private


class ResourceStop(RuntimeError):
    pass


class SizeStop(RuntimeError):
    def __init__(self, metrics):
        super().__init__("local incidence cap reached")
        self.metrics = metrics


class Budget:
    def __init__(self, seconds=MAX_SECONDS):
        if not math.isfinite(seconds) or not 0 < seconds <= MAX_SECONDS:
            raise ValueError("budget must be finite, positive, and at most 60 seconds")
        self.started = time.monotonic()
        self.seconds = seconds
        self.calls = 0

    def check(self):
        self.calls += 1
        if time.monotonic() - self.started > self.seconds:
            raise ResourceStop("TIME_CAP")
        if self.calls == 1 or self.calls % 128 == 0:
            if private_bytes() > MAX_PRIVATE_BYTES:
                raise ResourceStop("PRIVATE_MEMORY_CAP")


def inverse_sources(p, row, algebra, budget):
    """Enumerate every source at one row by its removed generator, not its coefficient."""
    kind, exterior, *tail = row
    present = set(exterior)
    low, high = algebra.low_offsets(p), algebra.high_offsets(p)
    offset = tail[-1]
    for variable in sorted(low | high):
        budget.check()
        if variable in present:
            continue
        coefficient = offset - variable
        source_kind = None
        if kind == "K":
            if coefficient in high:
                source_kind = "K"
            elif variable in high and coefficient in low:
                source_kind = "S"
        elif kind == "D":
            if variable in low and coefficient in low:
                if algebra.low_product(p, variable, coefficient) == (tail[0], offset):
                    source_kind = "S"
        else:
            raise ValueError("unknown row kind")
        if source_kind is not None:
            source = source_kind, tuple(sorted((*exterior, variable))), coefficient
            sign = (-1) ** sum(value < variable for value in exterior)
            yield source, sign


def expand(p, previous, frontier, modules, budget, max_columns, max_nnz):
    columns = dict(previous)
    nnz = sum(len(boundary) for boundary in columns.values())
    for row in sorted(frontier):
        budget.check()
        for source, sign in inverse_sources(p, row, modules["algebra"], budget):
            if source in columns:
                assert columns[source][row] == sign
                continue
            if len(columns) + 1 > max_columns:
                raise SizeStop({"reason": "COLUMN_CAP", "attempted_columns": len(columns) + 1,
                                "partial_columns": len(columns), "partial_nnz": nnz})
            support = [{"coefficient": 1, "exact_label": full_label(source)}]
            boundary = dict(modules["primary"].multiply(p, support, modules["algebra"]))
            assert boundary.get(row) == sign, "inverse neighbor does not reproduce its incident row"
            budget.check()
            if nnz + len(boundary) > max_nnz:
                raise SizeStop({"reason": "NNZ_CAP", "attempted_columns": len(columns) + 1,
                                "partial_columns": len(columns), "partial_nnz": nnz,
                                "attempted_nnz": nnz + len(boundary)})
            columns[source] = boundary
            nnz += len(boundary)
    return columns


def matrix_record(radius, columns, frontier, target, budget):
    row_set = set(target)
    for boundary in columns.values():
        budget.check()
        row_set.update(boundary)
    rows = sorted(row_set)
    row_index = {row: index for index, row in enumerate(rows)}
    packed = []
    for source, boundary in sorted(columns.items()):
        budget.check()
        packed.append({"exact_label": full_label(source),
                       "boundary": sorted([row_index[row], value] for row, value in boundary.items())})
    result = {
        "radius": radius,
        "status": "COMPLETE",
        "frontier": [full_label(row) for row in sorted(frontier)],
        "row_labels": [full_label(row) for row in rows],
        "columns": packed,
        "rows_count": len(rows),
        "columns_count": len(packed),
        "nnz": sum(len(column["boundary"]) for column in packed),
    }
    result["incidence_hash"] = digest(result)
    result["solve"] = {"classification": "PENDING"}
    return result


def axpy(destination, source, scale, budget):
    for index, value in source.items():
        budget.check()
        updated = destination.get(index, Fraction(0)) + scale * value
        if updated:
            destination[index] = updated
        else:
            destination.pop(index, None)


def rational_records(vector, labels):
    return [{"coefficient": [value.numerator, value.denominator], "exact_label": labels[index]}
            for index, value in sorted(vector.items()) if value]


def image_solution(matrix, target, budget):
    """Unit-first QQ column elimination; every basis vector retains original-source provenance."""
    rows = matrix["row_labels"]
    row_index = {label_key(label): index for index, label in enumerate(rows)}
    target_vector = {row_index[row]: Fraction(value) for row, value in target.items()}
    columns = matrix["columns"]
    ordering = sorted(range(len(columns)), key=lambda index: (
        len(columns[index]["boundary"]) != 1,
        len(columns[index]["boundary"]), label_key(columns[index]["exact_label"]),
    ))
    basis = []
    unit_pivots = 0
    for column_index in ordering:
        budget.check()
        vector = {row: Fraction(value) for row, value in columns[column_index]["boundary"]}
        provenance = {column_index: Fraction(1)}
        for pivot, reduced, source in basis:
            budget.check()
            factor = vector.get(pivot)
            if factor:
                axpy(vector, reduced, -factor, budget)
                axpy(provenance, source, -factor, budget)
        if not vector:
            continue
        units = [row for row, value in vector.items() if abs(value) == 1]
        pivot = min(units) if units else min(vector)
        divisor = vector[pivot]
        if abs(divisor) == 1:
            unit_pivots += 1
        normalized, source = {}, {}
        for row, value in vector.items():
            budget.check()
            normalized[row] = value / divisor
        for index, value in provenance.items():
            budget.check()
            source[index] = value / divisor
        basis.append((pivot, normalized, source))

    residual = dict(target_vector)
    particular = {}
    for pivot, vector, source in basis:
        budget.check()
        factor = residual.get(pivot)
        if factor:
            axpy(residual, vector, -factor, budget)
            axpy(particular, source, factor, budget)
    result = {
        "rank_qq": len(basis), "unit_pivots": unit_pivots,
        "nonunit_pivots": len(basis) - unit_pivots,
        "particular_solution": rational_records(particular, [column["exact_label"] for column in columns]),
        "residual": rational_records(residual, rows),
        "residual_semantics": "target - M*particular_solution in original row coordinates",
    }
    if residual:
        dual = {min(residual): Fraction(1)}
        for pivot, vector, _ in reversed(basis):
            budget.check()
            value = Fraction(0)
            for row, coefficient in vector.items():
                budget.check()
                if row != pivot:
                    value -= coefficient * dual.get(row, 0)
            if value:
                dual[pivot] = value
            else:
                dual.pop(pivot, None)
        denominator = math.lcm(*(value.denominator for value in dual.values()))
        integer_dual = {row: int(value * denominator) for row, value in dual.items()}
        common = math.gcd(*integer_dual.values())
        integer_dual = {row: value // common for row, value in integer_dual.items()}
        pairing = sum(integer_dual.get(row, 0) * value for row, value in target_vector.items())
        assert pairing and pairing.denominator == 1
        if pairing < 0:
            integer_dual = {row: -value for row, value in integer_dual.items()}
            pairing = -pairing
        for column in columns:
            budget.check()
            assert sum(integer_dual.get(row, 0) * value for row, value in column["boundary"]) == 0
        result.update({
            "classification": "QQ_INCONSISTENT",
            "dual": [{"coefficient": value, "exact_label": rows[row]}
                     for row, value in sorted(integer_dual.items())],
            "dual_target_pairing": int(pairing),
            "integer_membership": "EXCLUDED_IN_THIS_LOCAL_SPAN_ONLY",
        })
    elif all(value.denominator == 1 for value in particular.values()):
        result.update({
            "classification": "INTEGRAL_WITNESS",
            "integral_witness": [{"coefficient": int(value), "exact_label": columns[index]["exact_label"]}
                                 for index, value in sorted(particular.items())],
            "integer_membership": "CERTIFIED_IN_THIS_LOCAL_SPAN",
        })
    else:
        result.update({
            "classification": "RATIONAL_SECTION",
            "particular_denominator_lcm": math.lcm(*(value.denominator for value in particular.values())),
            "integer_membership": "INCONCLUSIVE_NOT_A_LATTICE_OBSTRUCTION",
        })
    return result


def solve_parameter(p, modules, budget, max_columns, max_nnz, output_row, checkpoint):
    if p not in (8, 9, 10):
        raise ValueError("only declared training parameters 8,9,10 are allowed")
    target_records = [{**term, "coefficient": 2 * term["coefficient"]}
                      for term in modules["endpoint"].eta_formula(p)]
    target = {label_key(term["exact_label"]): term["coefficient"] for term in target_records}
    output_row.update({"p": p, "status": "RUNNING", "target": target_records,
                       "neighborhoods": [], "completed_radius": 0})
    columns, frontier, expanded = {}, set(target), set()
    for radius in (1, 2):
        output_row["attempted_radius"] = radius
        checkpoint()
        try:
            next_columns = expand(p, columns, frontier, modules, budget, max_columns, max_nnz)
        except SizeStop as stop:
            output_row.update({"status": "INCONCLUSIVE_CAP", "cap": stop.metrics,
                               "p1_status": "INCONCLUSIVE"})
            checkpoint()
            print(f"p={p} radius={radius}: cap, retaining completed radius {radius-1}", flush=True)
            return
        matrix = matrix_record(radius, next_columns, frontier, target, budget)
        output_row["neighborhoods"].append(matrix)
        output_row["completed_radius"] = radius
        checkpoint()
        matrix["solve"] = image_solution(matrix, target, budget)
        checkpoint()
        classification = matrix["solve"]["classification"]
        print(f"p={p} radius={radius}: {matrix['columns_count']} columns, {matrix['rows_count']} rows, "
              f"{matrix['nnz']} nnz, {classification}", flush=True)
        if classification == "INTEGRAL_WITNESS":
            witness = matrix["solve"]["integral_witness"]
            actual = dict(modules["primary"].multiply(p, witness, modules["algebra"]))
            assert actual == target, "integral provenance does not reproduce the complete target"
            output_row.update({"status": "INTEGRAL_WITNESS", "p1_status": "PASS_FINITE",
                               "p2_status": "AWAITING_INDEPENDENT_AUDIT"})
            checkpoint()
            return
        columns = next_columns
        expanded.update(frontier)
        frontier = {row for boundary in columns.values() for row in boundary} - expanded
    output_row.update({
        "status": "QQ_REFUTED" if classification == "QQ_INCONSISTENT" else "RATIONAL_SECTION",
        "p1_status": "REFUTED" if classification == "QQ_INCONSISTENT" else "INCONCLUSIVE",
        "p2_status": "NOT_APPLICABLE_NO_INTEGRAL_WITNESS",
    })
    checkpoint()


def run(output, parameters=(8, 9, 10), budget_seconds=60, max_columns=MAX_COLUMNS,
        max_nnz=MAX_NNZ, continue_retained=False):
    parameters = tuple(parameters)
    if not parameters or parameters != tuple(sorted(set(parameters))) or any(p not in (8, 9, 10)
                                                                          for p in parameters):
        raise ValueError("parameters must be a nonempty increasing subset of 8,9,10")
    if not 0 < max_columns <= MAX_COLUMNS or not 0 < max_nnz <= MAX_NNZ:
        raise ValueError("requested incidence caps exceed the declared maxima")
    budget = Budget(budget_seconds)
    budget.check()
    modules = dependencies()
    result = {"experiment": "EXP-058", "status": "CHECKPOINT", "premises": PREMISES,
              "parameters_requested": list(parameters), "p11_original_source_accessed": False,
              "old_hnf_source_accessed": False, "continued_after_refutation": continue_retained,
              "caps": {"columns": max_columns, "nnz": max_nnz, "seconds": budget_seconds,
                       "private_bytes": MAX_PRIVATE_BYTES}, "rows": []}

    def checkpoint():
        result["artifact_hash"] = digest({key: value for key, value in result.items() if key != "artifact_hash"})
        modules["primary"].write_json(output, result)

    checkpoint()
    try:
        for p in parameters:
            budget.check()
            row = {}
            result["rows"].append(row)
            solve_parameter(p, modules, budget, max_columns, max_nnz, row, checkpoint)
            if row["status"] == "QQ_REFUTED" and not continue_retained:
                result["status"] = "STOPPED_ON_FIRST_REFUTATION"
                checkpoint()
                return result
        result["status"] = "COMPLETE"
    except ResourceStop as stop:
        result["status"] = "INCONCLUSIVE_RESOURCE_CAP"
        result["resource_stop"] = str(stop)
        if result["rows"] and result["rows"][-1].get("status") == "RUNNING":
            result["rows"][-1].update({"status": "INCONCLUSIVE_RESOURCE_CAP", "p1_status": "INCONCLUSIVE"})
        checkpoint()
        raise
    checkpoint()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--parameters", type=int, nargs="+", default=[8, 9, 10])
    parser.add_argument("--budget", type=float, default=60)
    parser.add_argument("--max-columns", type=int, default=MAX_COLUMNS)
    parser.add_argument("--max-nnz", type=int, default=MAX_NNZ)
    parser.add_argument("--continue-retained", action="store_true")
    args = parser.parse_args()
    run(args.output, args.parameters, args.budget, args.max_columns, args.max_nnz, args.continue_retained)
