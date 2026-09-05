"""Independent potential formulas and bitset full differentials, exact CPU only."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
HYPOTHESIS_SHA256 = "c08a6104dafc057711d5ec42314ea4b762a5a9121a827bf1bf4f3ac459043ea2"


def private_memory_bytes():
    if os.name != "nt":
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024

    class Counters(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("faults", ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in (
                "peak_working", "working", "peak_paged", "paged", "peak_nonpaged",
                "nonpaged", "pagefile", "peak_pagefile", "private")]

    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    handle = ctypes.windll.kernel32.GetCurrentProcess
    handle.restype = ctypes.c_void_p
    query = ctypes.windll.psapi.GetProcessMemoryInfo
    query.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
    if not query(handle(), ctypes.byref(counters), counters.cb):
        raise OSError("cannot verify the independent audit private-memory cap")
    return counters.private


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arithmetic():
    path = EXPERIMENTS / "EXP-054-full-source-boundary/audit.py"
    assert file_hash(path) == "9e21b8a03694938e04dc7aba3555944fa511e4d1ac0d4dfc92727288ed7a1b63"
    spec = importlib.util.spec_from_file_location("independent054_for059audit", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def potential_source(p, u0, r0, check=lambda: None):
    """Literal alpha differences and beta potentials, not sparse producer branches."""
    low = {*range(1, p + 1), *range(3 * p, 4 * p - 1)}
    alpha, beta = [], []

    def add(output, missing, coefficient, weight):
        if weight:
            output.append({"coefficient": weight, "exact_label": [
                "S", sorted((low - set(missing)) | {6 * p, 8 * p - 4}), coefficient]})

    for r in range(p):
        for s in range(r + 1, p):
            if u0 + 2 <= r + s <= p + u0 + 1:
                value = int(s == r0) - int(r == r0)
                add(alpha, (p - r, p - s, 3 * p + u0), p + 2 + u0 - r - s,
                    (-1) ** (p + r + s + u0) * value)
        check()
    for u in range(p - 1):
        for v in range(u + 1, p - 1):
            if u0 not in (u, v):
                continue
            total = u + v
            orientation = int(u == u0) - int(v == u0)
            anchor = orientation * int(r0 == total + 3) if total <= p - 4 else 0
            for r in range(max(0, total - p + 4), min(p - 1, total + 2) + 1):
                value = orientation * int(r == r0) - anchor
                add(beta, (p - r, 3 * p + u, 3 * p + v), 3 * p + 2 + total - r,
                    (-1) ** (p + r + u + v) * value)
            check()
    return alpha + beta, alpha, beta


def bitset_boundary(p, support, independent, check=lambda: None):
    """All original faces, accumulated before decoding nonzero exterior labels."""
    accumulator = {}
    for term in support:
        kind, exterior, coefficient = term["exact_label"]
        assert kind == "S" and exterior == sorted(set(exterior)) and len(exterior) == 2 * p - 2
        assert sum(exterior) + coefficient == 4 * p * p + 6 * p - 1
        assert independent.low_kind(p, coefficient) is not None
        assert all(independent.low_kind(p, v) is not None or independent.high_contains(p, v) for v in exterior)
        bits = sum(1 << value for value in exterior)
        sign = -1
        for variable in reversed(exterior):
            total = variable + coefficient
            variable_kind = independent.low_kind(p, variable)
            product_kind = None
            if variable_kind is not None:
                coefficient_kind = independent.low_kind(p, coefficient)
                if variable_kind == coefficient_kind == "L0" and total > p:
                    product_kind = "A"
                elif variable_kind != coefficient_kind and total >= 4 * p - 1:
                    product_kind = "B"
                row = ("D", bits ^ (1 << variable), product_kind, total) if product_kind else None
            else:
                row = ("K", bits ^ (1 << variable), total) if independent.degree_two_contains(p, total) else None
            if row is not None:
                value = accumulator.get(row, 0) + sign * term["coefficient"]
                if value:
                    accumulator[row] = value
                else:
                    accumulator.pop(row, None)
            sign = -sign
        check()
    result = {}
    for row, coefficient in accumulator.items():
        bits = row[1]
        exterior = []
        while bits:
            smallest = bits & -bits
            exterior.append(smallest.bit_length() - 1)
            bits ^= smallest
        result[(row[0], tuple(exterior), *row[2:])] = coefficient
    return result


def expected_boundary(p, source):
    result = {}
    for term in source:
        _, exterior, coefficient = term["exact_label"]
        if coefficient not in (3, 3 * p, 3 * p + 1, 3 * p + 2):
            continue
        face = tuple(value for value in exterior if value != 8 * p - 4)
        row = ("K", face, 8 * p - 4 + coefficient)
        assert row not in result
        result[row] = -term["coefficient"]
    return result


def audit(results_path=None, budget_seconds=60):
    if not math.isfinite(budget_seconds) or not 0 < budget_seconds <= 60:
        raise ValueError("audit budget must be finite, positive, and at most 60 seconds")
    started = time.monotonic()
    operations = 0

    def check():
        nonlocal operations
        operations += 1
        if time.monotonic() - started > budget_seconds:
            raise RuntimeError("EXP-059 independent audit time cap")
        if operations == 1 or operations % 256 == 0:
            if private_memory_bytes() > 1024 ** 3:
                raise RuntimeError("EXP-059 independent audit private-memory cap")

    path = results_path or HERE / "artifacts/results.json"
    result = json.loads(path.read_text(encoding="utf-8"))
    assert file_hash(HERE / "hypothesis.md") == HYPOTHESIS_SHA256
    for relative, expected_hash in result["premises"].items():
        assert file_hash(EXPERIMENTS / relative) == expected_hash
    assert result["artifact_hash"] == digest({k: v for k, v in result.items() if k != "artifact_hash"})
    assert result["status"] == "COMPLETE" and result["p11_original_source_accessed"] is False
    independent = arithmetic()
    maximum = result["parameters_requested"][1]
    assert 8 <= maximum <= 100 and [row["p"] for row in result["rows"]] == list(range(8, maximum + 1))
    verified = []
    total = 0
    literal_checks = 0
    for row in result["rows"]:
        p = row["p"]
        pairs = ([(u, r) for u in range(p - 2) for r in range(u + 2, p)] if p <= 16 else
                 [(0, 2), (0, p - 1), (1, 3), (p - 3, p - 1)])
        assert [tuple(case["potential"]) for case in row["chains"]] == pairs
        assert row["complete_basis_checked"] == (p <= 16)
        assert row["basis_rank"] == (p - 1) * (p - 2) // 2
        maxima = {"source_support": 0, "boundary_support": 0}
        for case, (u, r) in zip(row["chains"], pairs, strict=True):
            source, alpha, beta = potential_source(p, u, r, check)
            assert digest(source) == case["source_hash"]
            assert len(source) == len({independent.key(term["exact_label"]) for term in source})
            assert all(abs(term["coefficient"]) == 1 for term in source)
            assert len(source) <= 3 * p - 5
            actual = bitset_boundary(p, source, independent, check)
            expected = expected_boundary(p, source)
            assert actual == expected and all(index[0] == "K" for index in actual)
            if p <= 16:
                assert independent.independent_boundary(p, source) == actual
                literal_checks += 1
            assert digest(independent.records(actual)) == case["boundary_hash"]
            c0 = sum(index[-1] == 8 * p - 1 for index in actual)
            c2 = sum(11 * p - 4 <= index[-1] <= 11 * p - 2 for index in actual)
            assert c0 <= 1 and c2 <= 6 and c0 + c2 == len(actual) <= 7
            assert case["source_support"] == len(source) and case["alpha_support"] == len(alpha)
            assert case["beta_support"] == len(beta) and case["boundary_support"] == len(actual)
            assert case["c0_rows"] == c0 and case["c2_rows"] == c2 and case["coefficient_height"] == 1
            low = {*range(1, p + 1), *range(3 * p, 4 * p - 1)}
            distinguished = ("S", tuple(sorted((low - {p, p - r, 3 * p + u}) | {6 * p, 8 * p - 4})),
                             p + 2 + u - r)
            coordinates = independent.sparse(source)
            assert coordinates[distinguished] * (-1) ** (p + r + u) == 1
            beta_boundary = bitset_boundary(p, beta, independent, check)
            assert any(index[0] == "D" for index in beta_boundary)
            column_boundary = bitset_boundary(p, source[:1], independent, check)
            assert any(index[0] == "D" for index in column_boundary)
            assert all(case[name] is True for name in (
                "full_D_zero", "independent_agreement", "potential_recovered",
                "wrong_beta_sign_rejected", "coefficient_mutation_rejected"))
            maxima["source_support"] = max(maxima["source_support"], len(source))
            maxima["boundary_support"] = max(maxima["boundary_support"], len(actual))
            total += 1
            check()
        verified.append({"p": p, "chains_verified": len(pairs), "complete_basis": p <= 16,
                         **maxima, "full_original_D_zero": True, "unit_coordinate_recovery": True,
                         "wrong_beta_sign_and_coefficient_mutations_rejected": True})
        print(f"p={p}: independent potential/full-boundary audit PASS, cumulative {total}", flush=True)
    assert total == result["completed_chains"]
    if maximum == 100:
        assert total == 861 and literal_checks == 525
    assert result["claims"]["uniform_eta_order_two_or_nonvanishing"] == "NOT_ESTABLISHED"
    certificate = {"experiment": "EXP-059", "status": "INDEPENDENT_AUDIT_PASS",
                   "chains_verified": total, "literal_full_differential_crosschecks": literal_checks,
                   "arithmetic": "coefficient-first potential formulas and exact bitset full differential",
                   "rows": verified, "p11_original_source_accessed": False, "old_hnf_source_accessed": False,
                   "scope": "uniform completeness uses signed reconstruction proof, not finite ranks",
                   "result_sha256": file_hash(path), "producer_sha256": file_hash(HERE / "run.py"),
                   "audit_code_sha256": file_hash(Path(__file__)), "premises": result["premises"]}
    certificate["artifact_hash"] = digest(certificate)
    return certificate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/audit-results.json")
    args = parser.parse_args()
    certificate = audit(args.results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": certificate["status"], "chains": certificate["chains_verified"],
                      "artifact_hash": certificate["artifact_hash"]}))


if __name__ == "__main__":
    main()
