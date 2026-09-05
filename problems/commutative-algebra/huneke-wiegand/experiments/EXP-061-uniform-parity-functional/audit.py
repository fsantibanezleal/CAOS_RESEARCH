"""Independent exhaustive original-sector parity audit; no potential or producer imports."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import time
from functools import lru_cache
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def full_label(index):
    return [index[0], list(index[1]), *index[2:]]


def label_key(label):
    return label[0], tuple(label[1]), *label[2:]


@lru_cache(maxsize=None)
def low_offsets(p):
    return [*range(1, p + 1), *range(3 * p, 4 * p - 1)]


@lru_cache(maxsize=None)
def high_offsets(p):
    intervals = [(6 * p, 8 * p - 2), (8 * p, 10 * p - 2), (10 * p, 10 * p),
                 (11 * p - 1, 12 * p - 1), (13 * p + 1, 14 * p - 2),
                 (14 * p, 15 * p - 1), (16 * p, 16 * p), (17 * p - 1, 18 * p - 1)]
    return sorted({value for first, last in intervals for value in range(first, last + 1)})


def degree_two_contains(p, value):
    return (value in (8 * p - 1, 10 * p - 1, 14 * p - 1)
            or 10 * p + 1 <= value <= 11 * p - 2 or 12 * p <= value <= 13 * p
            or 15 * p <= value <= 16 * p - 1 or 16 * p + 1 <= value <= 17 * p - 2
            or 18 * p <= value <= 24 * p - 1)


def low_product(p, left, right):
    if 1 <= left <= p and 1 <= right <= p:
        return ("A", left + right) if left + right > p else None
    if (1 <= left <= p and 3 * p <= right <= 4 * p - 2
            or 1 <= right <= p and 3 * p <= left <= 4 * p - 2):
        return ("B", left + right) if left + right >= 4 * p - 1 else None
    return None


def original_boundary(p, source):
    """Every original face modulo two; signs are units and disappear only here."""
    kind, exterior, coefficient = source
    low, high = set(low_offsets(p)), set(high_offsets(p))
    assert kind in ("S", "K") and len(exterior) == 2 * p - 2
    assert list(exterior) == sorted(set(exterior)) and set(exterior) <= low | high
    assert coefficient in (low if kind == "S" else high)
    assert sum(exterior) + coefficient == 4 * p * p + 6 * p - 1
    rows = set()
    for variable in exterior:
        face = tuple(value for value in exterior if value != variable)
        if kind == "S" and variable in low:
            product = low_product(p, variable, coefficient)
            row = ("D", face, *product) if product else None
        else:
            total = variable + coefficient
            row = ("K", face, total) if degree_two_contains(p, total) else None
        if row is not None:
            if row in rows:
                rows.remove(row)
            else:
                rows.add(row)
    return rows


def z_value(p, u, v):
    if not (0 <= u <= p - 2 and 0 <= v <= p - 2) or u == v:
        return 0
    return int(sorted((u, v, p - 2 - u - v)) == [0, 2, p - 4])


def functional_rows(p):
    """Generate C0 by the reflection formula, not the producer's six-row list."""
    low = set(low_offsets(p))
    result = set()
    for u in range(p - 1):
        for v in range(u + 1, p - 1):
            if z_value(p, u, v):
                for r in (u + v, u + v + 1):
                    exterior = tuple(sorted((low - {p - r, 3 * p + u, 3 * p + v}) | {6 * p}))
                    result.add(("K", exterior, 11 * p - 2 + u + v - r))
        for r in range(p):
            s = p + u - 1 - r
            if r < s < p and (z_value(p, u, r - u) ^ z_value(p, u, r - u - 1)):
                exterior = tuple(sorted((low - {p - r, p - s, 3 * p + u}) | {6 * p}))
                result.add(("K", exterior, 8 * p - 1))
    assert len(result) == 12
    for _, exterior, coefficient in result:
        assert len(exterior) == 2 * p - 3 and degree_two_contains(p, coefficient)
        assert sum(exterior) + coefficient == 4 * p * p + 6 * p - 1
    return result


def inverse_incidence(p, row):
    """Coefficient-first inversion includes every possible source at a K row."""
    assert row[0] == "K"
    low, high = set(low_offsets(p)), set(high_offsets(p))
    present = set(row[1])
    result = set()
    for coefficient in sorted(high):
        variable = row[-1] - coefficient
        if variable in low | high and variable not in present:
            result.add(("K", tuple(sorted(present | {variable})), coefficient))
    for coefficient in sorted(low):
        variable = row[-1] - coefficient
        if variable in high and variable not in present:
            result.add(("S", tuple(sorted(present | {variable})), coefficient))
    return result


def all_sector_sources(p, h, check):
    """Exhaust low missing triples using only original cardinality and total offset."""
    low = low_offsets(p)
    low_set = set(low)
    result = []
    for missing in combinations(low, 3):
        coefficient = sum(missing) + 4 * p - 2 - h
        if coefficient in low_set:
            exterior = tuple(sorted((low_set - set(missing)) | {6 * p, h}))
            result.append(("S", exterior, coefficient))
        check()
    assert len(result) == len(set(result))
    return sorted(result)


def bits_set(value):
    while value:
        smallest = value & -value
        yield smallest.bit_length() - 1
        value ^= smallest


def row_span_certificate(row_vectors, target, source_count, check):
    """Exact F2 row elimination with original-D-row provenance and a complete kernel."""
    basis = {}
    for row_index, original in enumerate(row_vectors):
        vector = original
        provenance = 1 << row_index
        while vector:
            pivot = (vector & -vector).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (vector, provenance)
                break
            other, source = basis[pivot]
            vector ^= other
            provenance ^= source
        check()
    residual, provenance = target, 0
    while residual:
        pivot = (residual & -residual).bit_length() - 1
        if pivot not in basis:
            break
        vector, rows = basis[pivot]
        residual ^= vector
        provenance ^= rows
        check()
    kernel = []
    for free in range(source_count):
        if free in basis:
            continue
        vector = 1 << free
        for pivot in sorted(basis, reverse=True):
            if (basis[pivot][0] & vector).bit_count() & 1:
                vector ^= 1 << pivot
        assert all((row & vector).bit_count() % 2 == 0 for row in row_vectors)
        kernel.append(vector)
        check()
    if residual:
        counterexample = next(vector for vector in kernel if (target & vector).bit_count() & 1)
        return {"rank": len(basis), "kernel": kernel, "dual_rows": None,
                "counterexample_source": counterexample}
    reproduced = 0
    for row in bits_set(provenance):
        reproduced ^= row_vectors[row]
    assert reproduced == target
    assert all((target & vector).bit_count() % 2 == 0 for vector in kernel)
    return {"rank": len(basis), "kernel": kernel, "dual_rows": provenance,
            "counterexample_source": None}


def sector_certificate(p, h, functional, check):
    sources = all_sector_sources(p, h, check)
    columns = []
    pairing = 0
    all_d_rows = set()
    for index, source in enumerate(sources):
        boundary = original_boundary(p, source)
        d_boundary = {row for row in boundary if row[0] == "D"}
        columns.append(d_boundary)
        all_d_rows.update(d_boundary)
        if len(boundary & functional) % 2:
            pairing |= 1 << index
        check()
    d_rows = sorted(all_d_rows)
    row_index = {row: index for index, row in enumerate(d_rows)}
    row_vectors = [0] * len(d_rows)
    packed_columns = []
    for index, column in enumerate(columns):
        positions = sorted(row_index[row] for row in column)
        packed_columns.append(positions)
        for row in positions:
            row_vectors[row] |= 1 << index
        check()
    algebra = row_span_certificate(row_vectors, pairing, len(sources), check)
    certificate = {
        "h": h, "source_count": len(sources), "D_row_count": len(d_rows),
        "D_nnz": sum(map(len, columns)), "D_rank_F2": algebra["rank"],
        "full_D_kernel_dimension": len(sources) - algebra["rank"],
        "source_labels_hash": digest([full_label(source) for source in sources]),
        "D_row_labels_hash": digest([full_label(row) for row in d_rows]),
        "D_incidence_hash": digest(packed_columns), "K_functional_source_bits": hex(pairing),
        "kernel_basis_hash": digest([hex(vector) for vector in algebra["kernel"]]),
    }
    if algebra["counterexample_source"] is not None:
        certificate["status"] = "REFUTED"
        certificate["counterexample_source"] = [full_label(sources[index])
                                                for index in bits_set(algebra["counterexample_source"])]
    else:
        certificate["status"] = "ROW_SPAN_CERTIFIED"
        certificate["D_row_dual"] = [full_label(d_rows[index]) for index in bits_set(algebra["dual_rows"])]
        if p <= 9:
            certificate["complete_kernel_basis_hex"] = [hex(vector) for vector in algebra["kernel"]]
    return certificate


def private_memory_bytes():
    if os.name != "nt":
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024

    class Counters(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong),
                    *[(name, ctypes.c_size_t) for name in (
                        "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                        "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
                        "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage",
                        "PrivateUsage")]]

    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
    if not psapi.GetProcessMemoryInfo(kernel32.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
        raise OSError(ctypes.get_last_error(), "GetProcessMemoryInfo failed")
    return counters.PrivateUsage


class Budget:
    def __init__(self, seconds=120, memory_mib=1024):
        assert 0 < seconds <= 120 and 0 < memory_mib <= 1024
        self.seconds, self.memory = seconds, memory_mib * 1024 * 1024
        self.started = time.monotonic()
        self.calls = 0

    def check(self):
        self.calls += 1
        if time.monotonic() - self.started > self.seconds:
            raise TimeoutError("Declared wall-clock cap reached")
        if self.calls % 256 == 1 and private_memory_bytes() > self.memory:
            raise MemoryError("Declared private-memory cap reached")


def incidence_and_controls(p, functional, producer, check):
    incident = set()
    for row in sorted(functional):
        inverse = inverse_incidence(p, row)
        for source in inverse:
            assert row in original_boundary(p, source)
        incident.update(inverse)
        check()
    k_sources = sorted(source for source in incident if source[0] == "K")
    s_sources = sorted(source for source in incident if source[0] == "S")
    assert k_sources and s_sources
    k_boundaries = {source: original_boundary(p, source) for source in k_sources}
    assert all(len(boundary & functional) % 2 == 0 for boundary in k_boundaries.values())
    low = set(low_offsets(p))
    highs = set()
    for source in s_sources:
        high_set = set(source[1]) - low
        assert len(high_set) == 2 and 6 * p in high_set
        highs.add(next(iter(high_set - {6 * p})))
    expected = sorted([*range(7 * p - 1, 8 * p - 1), 10 * p - 3, 10 * p - 2, 10 * p])
    assert sorted(highs) == expected
    reported = producer["incidence"]
    assert k_sources == sorted(label_key(record["exact_label"]) for record in reported["all_incident_K_sources"])
    assert s_sources == sorted(label_key(record["exact_label"]) for record in reported["all_incident_S_sources"])
    assert reported["reachable_high_sectors"] == expected
    assert reported["K_source_count"] == len(k_sources) and reported["S_source_count"] == len(s_sources)

    odd_eta = ("K", tuple(sorted((low - {p - 2, 3 * p, 3 * p + 2}) | {6 * p})), 11 * p - 2)
    assert odd_eta in functional and odd_eta not in functional - {odd_eta}
    # The other three coefficients of the frozen integral eta are even.
    c0 = ("K", tuple(sorted((low - {p - 2, 3, 3 * p}) | {6 * p})), 8 * p - 1)
    mutated_row = ("K", tuple(sorted((low - {p - 1, 2, 3 * p}) | {6 * p})), 8 * p - 1)
    assert c0 in functional and mutated_row not in functional
    mutation = (functional - {c0}) | {mutated_row}
    mutation_witness = next(source for source in k_sources
                            if len(original_boundary(p, source) & mutation) % 2)
    # A sparse fake functional that passes a proper subset is not a global certificate.
    fake = {odd_eta}
    passing = [source for source in k_sources if not len(k_boundaries[source] & fake) % 2]
    failing = [source for source in k_sources if len(k_boundaries[source] & fake) % 2]
    assert passing and failing and len(passing) < len(k_sources)
    omitted = next(source for source in s_sources if 10 * p - 3 in source[1])
    omitted_boundary = original_boundary(p, omitted)
    assert len(omitted_boundary & functional) % 2 == 1
    assert any(row[0] == "D" for row in omitted_boundary)
    return {
        "K_source_count": len(k_sources), "S_source_count": len(s_sources),
        "all_incident_K_sources": [full_label(source) for source in k_sources],
        "all_incident_S_sources": [full_label(source) for source in s_sources],
        "inverse_incidence_hash": digest([full_label(source) for source in sorted(incident)]),
        "K_full_boundary_hash": digest([[full_label(source), [full_label(row) for row in sorted(k_boundaries[source])]]
                                        for source in k_sources]),
        "all_original_K_source_pairings_zero": True,
        "reachable_high_sectors": expected, "eta_pairing": 1,
        "controls": {
            "remove_odd_eta_row": {"removed_row": full_label(odd_eta), "mutated_pairing": 0},
            "support_index_mutation": {"removed_row": full_label(c0), "added_row": full_label(mutated_row),
                                       "counterexample_source": full_label(mutation_witness), "pairing": 1},
            "omitted_reachable_sector": {"h": 10 * p - 3, "source": full_label(omitted),
                                         "K_pairing": 1, "D_boundary_nonzero": True,
                                         "interpretation": "Omitting this sector leaves actual incident sources unverified"},
            "local_passing_global_failing_functional": {
                "functional": [full_label(odd_eta)], "local_passing_K_columns": len(passing),
                "local_subset_hash": digest([full_label(source) for source in passing]),
                "added_original_source": full_label(failing[0]), "added_pairing": 1},
        },
    }


def save_checkpoint(output, result):
    result.pop("artifact_hash", None)
    result["artifact_hash"] = digest(result)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def audit(output=HERE / "artifacts" / "audit-results.json", seconds=120, memory_mib=1024):
    budget = Budget(seconds, memory_mib)
    producer_path = HERE / "artifacts" / "results.json"
    premises = {
        "hypothesis.md": "ff85801daf2facc0df6399c3d128636c17ec575e35c8fadd8166eb6532d98d97",
        "run.py": "767b34ffe8dcd880ece54743bfff400a59f3c91471483afc5a76350d8de60968",
        "artifacts/results.json": "0dbff45a4da41912b5d0857f7fea7d3b22b45cfc1ff955f14a008d47a1a1dc7c",
    }
    for name, expected in premises.items():
        assert file_hash(HERE / name) == expected, name
    producer = json.loads(producer_path.read_text(encoding="utf-8"))
    producer_hash = producer.pop("artifact_hash")
    assert digest(producer) == producer_hash and producer["status"] == "COMPLETE"
    producer_rows = {row["p"]: row for row in producer["rows"]}
    result = {
        "experiment": "EXP-061", "audit": "complete_original_F2_sector_row_space",
        "status": "RUNNING", "premises": premises, "producer_artifact_hash": producer_hash,
        "auditor_sha256": file_hash(Path(__file__)), "campaign": list(range(8, 13)), "rows": [],
        "arithmetic": "F2 using separately encoded original offset intervals and all source faces",
        "producer_math_imported": False, "potential_formula_used_for_audit": False,
        "old_p11_HNF_source_accessed": False,
        "resource_caps": {"seconds": seconds, "private_memory_mib": memory_mib,
                          "processes": 1, "global_dense_matrix": False},
        "incidence_completeness": [
            "For any supported K row (E,b), every preimage adds one missing variable v and has coefficient c=b-v.",
            "K sources require c in H and v in L union H; S sources require c in L and v in H. Both sets are exhausted.",
            "An incident S source has high exterior {6p,h}; D preserves that complete high set.",
            "All sources in a two-high sector omit exactly three of the 2p-1 low variables.",
            "Their coefficient is sum(missing)+4p-2-h, so enumerating all low triples with coefficient in L is exhaustive.",
            "All other K columns have zero supported incidence and all other S sectors have identically zero K pairing.",
            "Each saved original-D-row dual exactly reproduces lambda_K times B on every original sector source.",
        ],
    }
    save_checkpoint(output, result)
    try:
        for p in result["campaign"]:
            budget.check()
            functional = functional_rows(p)
            reference = producer_rows[p]
            assert functional == {label_key(record["exact_label"]) for record in reference["functional_support"]}
            assert reference["eta_pairing"] == 1
            row = {"p": p, "functional_support": [full_label(item) for item in sorted(functional)],
                   "incidence": incidence_and_controls(p, functional, reference, budget.check), "sectors": []}
            result["rows"].append(row)
            potential_dimensions = {sector["high"]: sector["complete_potential_basis_rank"]
                                    for sector in reference["sectors"]}
            for h in row["incidence"]["reachable_high_sectors"]:
                certificate = sector_certificate(p, h, functional, budget.check)
                row["sectors"].append(certificate)
                if certificate["status"] != "ROW_SPAN_CERTIFIED":
                    result["status"] = "REFUTED"
                    save_checkpoint(output, result)
                    return result
                if h in potential_dimensions:
                    assert certificate["full_D_kernel_dimension"] == potential_dimensions[h], (p, h)
                    certificate["producer_complete_potential_dimension_agrees"] = True
            row["status"] = "COMPLETE"
            save_checkpoint(output, result)
            print(f"p={p}: {len(row['sectors'])} complete original sector certificates", flush=True)
        result["status"] = "COMPLETE"
        result["totals"] = {
            "parameters": len(result["rows"]),
            "sector_certificates": sum(len(row["sectors"]) for row in result["rows"]),
            "original_S_sources": sum(sector["source_count"] for row in result["rows"] for sector in row["sectors"]),
            "D_rows": sum(sector["D_row_count"] for row in result["rows"] for sector in row["sectors"]),
            "D_nnz": sum(sector["D_nnz"] for row in result["rows"] for sector in row["sectors"]),
            "D_row_dual_terms": sum(len(sector["D_row_dual"]) for row in result["rows"] for sector in row["sectors"]),
            "adversarial_controls": 4 * len(result["rows"]),
        }
        result["scope"] = {
            "finite_complete_original_p1_p2_audit": "PASS",
            "uniform_proof": "Separate paper proof required; ranks are not extrapolated",
            "original_Huneke_Wiegand_conjecture": "Not resolved by this audit",
        }
    except (TimeoutError, MemoryError) as error:
        result["status"] = "BUDGET_STOP"
        result["error"] = str(error)
    except Exception as error:
        result["status"] = "AUDIT_FAILED"
        result["error"] = f"{type(error).__name__}: {error}"
        save_checkpoint(output, result)
        raise
    save_checkpoint(output, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "artifacts" / "audit-results.json")
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--memory-mib", type=int, default=1024)
    args = parser.parse_args()
    result = audit(args.output, args.seconds, args.memory_mib)
    print(json.dumps({"status": result["status"], "totals": result.get("totals"),
                      "artifact_hash": result["artifact_hash"]}, sort_keys=True))
    return 0 if result["status"] == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
