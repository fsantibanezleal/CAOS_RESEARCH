"""Independent triangle torsion audit using complete original sector incidence."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
CAMPAIGN = [*range(8, 15), 16, 20, 25, 32, 50, 64, 100]
HYPOTHESIS_SHA256 = "56663e362e4e26d16d8db30f6000a1761f8e3e5b1e380fc67d9a441c6c8cbeeb"
PRODUCER_SHA256 = "019c34a9d1180b5cce3fc0d5bfb29db7ffd91c0b66d56eab9e042da7623f0d07"
RESULTS_SHA256 = "09aef05e577e58b11c4ccc363ed47ccf1ed1598deb1b156a33bb3b6e49ae638d"
FROZEN_MACHINERY = {
    "EXP-061-uniform-parity-functional/audit.py": "2808798097a4c257c640e864ad73ffc23981197d4f422ee3e8472c14f7ab3ab5",
    "EXP-060-uniform-endpoint-annihilator/audit.py": "daa4b8bf019b09374f5be0d69b43ae235065c905f37ce3316d9d937c7c9b58be",
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def machinery():
    modules = []
    for relative, expected in FROZEN_MACHINERY.items():
        path = EXPERIMENTS / relative
        assert file_hash(path) == expected
        spec = importlib.util.spec_from_file_location(f"independent062_{len(modules)}", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules.append(module)
    return tuple(modules)


def triangles(p):
    return [(i, j, p - 2 - i - j) for i in range(p - 1) for j in range(i + 1, p - 1)
            if j < p - 2 - i - j]


def selected_triangles(p):
    available = triangles(p)
    if p <= 14:
        return available
    return [available[index] for index in sorted({0, (len(available) - 1) // 2, len(available) - 1})]


def triangle_z(p, triangle, u, v):
    if not 0 <= u <= p - 2 or not 0 <= v <= p - 2 or u == v:
        return 0
    return int(tuple(sorted((u, v, p - 2 - u - v))) == tuple(triangle))


def triangle_functional(p, triangle, parity):
    """Reflection construction, including cancellation of adjacent endpoints."""
    assert tuple(triangle) in triangles(p)
    low = set(parity.low_offsets(p))
    rows = set()
    for u in range(p - 1):
        for v in range(u + 1, p - 1):
            if triangle_z(p, triangle, u, v):
                for r in (u + v, u + v + 1):
                    exterior = tuple(sorted((low - {p - r, 3 * p + u, 3 * p + v}) | {6 * p}))
                    rows.add(("K", exterior, 11 * p - 2 + u + v - r))
        for r in range(p):
            s = p + u - 1 - r
            value = triangle_z(p, triangle, u, r - u) ^ triangle_z(p, triangle, u, r - u - 1)
            if value and r < s < p:
                exterior = tuple(sorted((low - {p - r, p - s, 3 * p + u}) | {6 * p}))
                rows.add(("K", exterior, 8 * p - 1))
    for _, exterior, coefficient in rows:
        assert len(exterior) == 2 * p - 3 and parity.degree_two_contains(p, coefficient)
        assert sum(exterior) + coefficient == 4 * p * p + 6 * p - 1
    return rows


def triangle_fields(p, triangle):
    """Construct the three oriented closed intervals, independently of the producer."""
    assert tuple(triangle) in triangles(p)
    i, j, k = triangle
    fields = {u: [0] * p for u in triangle}
    for u, a, b, sign in ((i, j, k, 1), (j, i, k, -1), (k, i, j, -1)):
        for r in range(p):
            fields[u][r] = sign if u + a < r <= u + b else 0
    return fields


def target_x(p, triangle, signed):
    i, j, _ = triangle
    return signed.e(p, i + j, i, j)


def incident_certificate(p, functional, parity, check):
    incident = set()
    for row in sorted(functional):
        for source in parity.inverse_incidence(p, row):
            assert row in parity.original_boundary(p, source)
            incident.add(source)
        check()
    low = set(parity.low_offsets(p))
    k_sources = sorted(source for source in incident if source[0] == "K")
    s_sources = sorted(source for source in incident if source[0] == "S")
    for source in k_sources:
        assert len(parity.original_boundary(p, source) & functional) % 2 == 0
        check()
    highs = set()
    for source in s_sources:
        high_set = set(source[1]) - low
        assert len(high_set) == 2 and 6 * p in high_set
        highs.update(high_set - {6 * p})
    declared_possible = {*range(7 * p - 1, 8 * p - 1), 10 * p - 3, 10 * p - 2, 10 * p}
    assert highs <= declared_possible
    return {
        "K_source_count": len(k_sources), "S_source_count": len(s_sources),
        "K_sources": [parity.full_label(source) for source in k_sources],
        "S_sources": [parity.full_label(source) for source in s_sources],
        "inverse_incidence_hash": digest([parity.full_label(source) for source in sorted(incident)]),
        "all_original_K_pairings_zero": True,
        "actual_reachable_sectors": sorted(highs), "declared_possible_sectors": sorted(declared_possible),
    }


def functional_pairing_matrix(p, functionals, target_triangles, signed):
    return [[sum(value for row, value in target_x(p, triangle, signed).items() if row in functional) % 2
             for triangle in target_triangles] for functional in functionals]


def binary_rank(matrix):
    basis = {}
    for row in matrix:
        vector = sum((value % 2) << index for index, value in enumerate(row))
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = vector
                break
            vector ^= basis[pivot]
    return len(basis)


def parity_parameter(p, parity, signed, check):
    available = triangles(p)
    functionals = [triangle_functional(p, triangle, parity) for triangle in available]
    pairing = functional_pairing_matrix(p, functionals, available, signed)
    assert pairing == [[int(i == j) for j in range(len(available))] for i in range(len(available))]
    rows = []
    for triangle, functional in zip(available, functionals, strict=True):
        incidence = incident_certificate(p, functional, parity, check)
        row = {"triangle": list(triangle), "functional_support": [parity.full_label(index) for index in sorted(functional)],
               "incidence": incidence, "sectors": []}
        for h in incidence["actual_reachable_sectors"]:
            certificate = parity.sector_certificate(p, h, functional, check)
            if certificate["status"] != "ROW_SPAN_CERTIFIED":
                row["sectors"].append(certificate)
                row["status"] = "REFUTED"
                rows.append(row)
                return {"p": p, "status": "REFUTED", "triangles": rows, "pairing_matrix": pairing}
            row["sectors"].append(certificate)
        removed = next(iter(target_x(p, triangle, signed)))
        assert removed in functional
        mutated = functional - {removed}
        assert functional_pairing_matrix(p, [mutated], [triangle], signed) == [[0]]
        row["removed_endpoint_control"] = {"removed": parity.full_label(removed), "mutated_diagonal": 0}
        row["status"] = "COMPLETE"
        rows.append(row)
    duplicated = [available[0], *available[:-1]]
    singular = functional_pairing_matrix(p, functionals, duplicated, signed)
    assert binary_rank(singular) == len(available) - 1
    # Mirroring an edge does not select a different original K label.
    i, j, _ = available[0]
    assert tuple(sorted((j, i))) == (i, j)
    mirrored_target = {index: -value for index, value in target_x(p, available[0], signed).items()}
    mirrored_column = [sum(value for index, value in mirrored_target.items() if index in functional) % 2
                       for functional in functionals]
    assert mirrored_column == [row[0] for row in pairing]
    return {"p": p, "status": "COMPLETE", "triangles": rows, "pairing_matrix": pairing,
            "duplicate_mirrored_edge_control": {"selected_triangles": [list(item) for item in duplicated],
                                                "matrix": singular, "rank": binary_rank(singular),
                                                "expected_nonsingular_rank": len(available),
                                                "mirrored_first_edge": [j, i],
                                                "mirrored_column": mirrored_column}}


def signed_source_check(p, triangle, signed, bitsets, literal, check):
    source = signed.potential_operator(p, triangle_fields(p, triangle), check)
    expected = {index: 2 * value for index, value in target_x(p, triangle, signed).items()}
    boundary = signed.full_boundary(p, source, bitsets, literal, check)
    assert boundary == expected and all(index[0] == "K" for index in boundary)
    if p <= 12:
        assert literal.independent_boundary(p, signed.records(source)) == boundary
    first = min(source)
    unit_boundary = signed.full_boundary(p, {first: 1}, bitsets, literal, check)
    assert unit_boundary
    sign_difference = {index: -2 * source[first] * value for index, value in unit_boundary.items()}
    assert sign_difference
    return source, {
        "triangle": list(triangle), "source_support": len(source), "source_hash": digest(signed.records(source)),
        "full_boundary": signed.records(boundary), "boundary_hash": digest(signed.records(boundary)),
        "full_integer_boundary_equals_twice_x": True, "zero_D_and_exactly_one_K_row": True,
        "literal_054_crosscheck": p <= 12,
        "coefficient_mutation": {"source": [first[0], list(first[1]), first[2]],
                                 "difference_hash": digest(signed.records(unit_boundary)), "rejected": True},
        "sign_mutation": {"difference_hash": digest(signed.records(sign_difference)), "rejected": True},
    }


def eta_transfer_check(p, signed, bitsets, literal, check):
    first_triangle = (0, 1, p - 3)
    first = signed.potential_operator(p, triangle_fields(p, first_triangle), check)
    d2 = signed.potential_operator(p, {0: [int(r == 2) for r in range(p)]}, check)
    d3 = signed.potential_operator(p, {0: [int(r == 3) for r in range(p)]}, check)
    source = signed.combine((first, 1), (d2, -2), (d3, -2), (signed.q(p, 2), -2), (signed.q(p, 3), 2))
    twice_eta = signed.target(p)
    assert all(value % 2 == 0 for value in twice_eta.values())
    eta = {index: value // 2 for index, value in twice_eta.items()}
    expected = signed.combine((eta, 1), (target_x(p, (0, 2, p - 4), signed), -1))
    boundary = signed.full_boundary(p, source, bitsets, literal, check)
    assert boundary == expected
    assert literal.independent_boundary(p, signed.records(source)) == expected
    return source, {"source_support": len(source), "source_hash": digest(signed.records(source)),
                    "full_boundary": signed.records(boundary), "boundary_hash": digest(signed.records(boundary)),
                    "M_source_equals_eta_minus_x02": True}


def read_archive(path, producer):
    manifest = producer["full_source_archive"]
    filename = manifest["filename"]
    assert filename == Path(filename).name and filename.endswith(".json.gz")
    compressed = (path.parent / filename).read_bytes()
    assert len(compressed) == manifest["gzip_bytes"]
    assert hashlib.sha256(compressed).hexdigest() == manifest["gzip_sha256"]
    assert compressed[:3] == b"\x1f\x8b\x08" and compressed[4:8] == b"\x00" * 4
    assert not compressed[3] & 8 and manifest["gzip_mtime"] == 0 and manifest["gzip_filename"] == ""
    assert 0 < manifest["raw_bytes"] < 128 * 1024 ** 2
    with gzip.open(path.parent / filename, "rb") as archive:
        raw = archive.read(manifest["raw_bytes"] + 1)
    assert len(raw) == manifest["raw_bytes"]
    assert hashlib.sha256(raw).hexdigest() == manifest["raw_sha256"]
    payload = json.loads(raw)
    assert payload["experiment"] == "EXP-062" and payload["format"] == manifest["format"]
    assert raw == json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    sources, transfers = {}, {}
    for item in payload["sources"]:
        index = item["p"], tuple(item["triangle"])
        assert index not in sources
        assert item["source_hash"] == digest(item["full_source"])
        assert item["source_support"] == len(item["full_source"])
        sources[index] = item["full_source"]
    for item in payload["transfers"]:
        assert item["p"] not in transfers and item["source_hash"] == digest(item["full_source"])
        transfers[item["p"]] = item["full_source"]
    assert set(sources) == {(p, triangle) for p in CAMPAIGN for triangle in selected_triangles(p)}
    assert set(transfers) == set(range(8, 13))
    return sources, transfers, manifest


def save_checkpoint(path, result):
    result.pop("artifact_hash", None)
    result["artifact_hash"] = digest(result)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")


def audit(results=None, output=None, seconds=120, memory_mib=1024):
    results = results or HERE / "artifacts/results.json"
    output = output or HERE / "artifacts/audit-results.json"
    parity, signed = machinery()
    budget = parity.Budget(seconds=seconds, memory_mib=memory_mib)
    bitsets = signed.load_bitsets()
    literal = bitsets.arithmetic()
    assert file_hash(HERE / "hypothesis.md") == HYPOTHESIS_SHA256
    assert file_hash(HERE / "run.py") == PRODUCER_SHA256
    assert file_hash(results) == RESULTS_SHA256
    producer = json.loads(results.read_text(encoding="utf-8"))
    assert producer["artifact_hash"] == digest({key: value for key, value in producer.items() if key != "artifact_hash"})
    assert producer["status"] == "COMPLETE" and producer["campaign"] == CAMPAIGN
    assert producer["producer_sha256"] == file_hash(HERE / "run.py")
    assert producer["old_p11_hnf_source_accessed"] is False
    for relative, expected in producer["premises"].items():
        assert file_hash(EXPERIMENTS / relative) == expected, relative
    producer_rows = {row["p"]: row for row in producer["rows"]}
    assert list(producer_rows) == CAMPAIGN
    archive, transfers, manifest = read_archive(results, producer)
    assert manifest["sources"] == len(archive) and manifest["transfers"] == len(transfers)
    budget.check()
    result = {
        "experiment": "EXP-062", "audit": "independent_complete_original_triangle_family",
        "status": "RUNNING", "campaign": CAMPAIGN, "rows": [],
        "hypothesis_sha256": HYPOTHESIS_SHA256, "auditor_sha256": file_hash(Path(__file__)),
        "producer_sha256": file_hash(HERE / "run.py"), "producer_result_sha256": file_hash(results),
        "producer_artifact_hash": producer["artifact_hash"], "frozen_independent_machinery": FROZEN_MACHINERY,
        "full_source_archive": manifest, "producer_math_imported": False, "old_HNF_source_accessed": False,
        "resource_caps": {"seconds": seconds, "private_memory_mib": memory_mib, "processes": 1,
                          "global_dense_matrix": False},
        "incidence_completeness": [
            "Every K-row inverse source is obtained by c+v=b with c in H and v in L union H, or c in L and v in H.",
            "All actual reachable exterior-high sectors are obtained from those complete inverse source labels.",
            "Every original S source in each such sector is enumerated by all missing low triples and the forced low coefficient.",
            "All complete original D faces are retained; saved D-row duals reproduce lambda_T B on every sector source.",
            "Other sectors have zero supported incidence, so no omitted sector can affect the functional.",
        ],
    }
    save_checkpoint(output, result)
    try:
        counts = []
        for p in range(8, 101):
            count = len(triangles(p))
            assert count == ((p - 2) ** 2 + 3) // 12
            counts.append([p, count])
            budget.check()
        result["exact_count_checks"] = counts
        for p in CAMPAIGN:
            reference = producer_rows[p]
            available = triangles(p)
            chosen = selected_triangles(p)
            assert reference["all_triangle_count"] == len(available)
            assert reference["tested_triangles"] == [list(triangle) for triangle in chosen]
            row = {"p": p, "all_triangle_count": len(available), "triangles": []}
            result["rows"].append(row)
            if p <= 12:
                row["complete_original_parity_audit"] = parity_parameter(p, parity, signed, budget.check)
                if row["complete_original_parity_audit"]["status"] != "COMPLETE":
                    result["status"] = "REFUTED"
                    save_checkpoint(output, result)
                    return result
            reference_triangles = {tuple(item["triangle"]): item for item in reference["triangles"]}
            assert list(reference_triangles) == chosen
            functionals = []
            for triangle in chosen:
                source, certificate = signed_source_check(p, triangle, signed, bitsets, literal, budget.check)
                saved = reference_triangles[triangle]
                assert signed.records(source) == archive[(p, triangle)]
                assert saved["source_hash"] == certificate["source_hash"]
                assert saved["source_support"] == certificate["source_support"]
                assert saved["source_coefficient_height"] == max(map(abs, source.values()))
                assert saved["full_boundary"] == certificate["full_boundary"]
                assert saved["boundary_hash"] == certificate["boundary_hash"]
                assert saved["integer_boundary_equals_twice_class"] is True
                functional = triangle_functional(p, triangle, parity)
                assert {parity.label_key(item["exact_label"]) for item in saved["functional_support"]} == functional
                assert all(item["coefficient"] == 1 for item in saved["functional_support"])
                assert saved["functional_rows"] == len(functional)
                assert saved["functional_hash"] == digest(saved["functional_support"])
                functionals.append(functional)
                certificate["functional_support_hash"] = digest([parity.full_label(index) for index in sorted(functional)])
                certificate["functional_rows"] = len(functional)
                row["triangles"].append(certificate)
                budget.check()
            pairing = functional_pairing_matrix(p, functionals, chosen, signed)
            assert pairing == [[int(i == j) for j in range(len(chosen))] for i in range(len(chosen))]
            assert reference["pairing_matrix"] == pairing and reference["pairing_identity"] is True
            row["pairing_matrix"] = pairing
            if p <= 12:
                transfer, certificate = eta_transfer_check(p, signed, bitsets, literal, budget.check)
                assert signed.records(transfer) == transfers[p]
                assert reference["eta_transfer"]["source_hash"] == certificate["source_hash"]
                row["eta_transfer"] = certificate
            row["status"] = "COMPLETE"
            save_checkpoint(output, result)
            print(f"p={p}: {len(chosen)} independent full signed W identities; complete parity audit={p <= 12}", flush=True)
        parity_rows = [row["complete_original_parity_audit"] for row in result["rows"] if "complete_original_parity_audit" in row]
        sectors = [sector for row in parity_rows for triangle in row["triangles"] for sector in triangle["sectors"]]
        unique_sectors = {}
        for row in parity_rows:
            for triangle in row["triangles"]:
                for sector in triangle["sectors"]:
                    index = row["p"], sector["h"]
                    if index in unique_sectors:
                        assert unique_sectors[index]["D_incidence_hash"] == sector["D_incidence_hash"]
                        assert unique_sectors[index]["source_labels_hash"] == sector["source_labels_hash"]
                    unique_sectors[index] = sector
        result["totals"] = {
            "signed_parameter_campaign": len(CAMPAIGN), "full_signed_W_sources": sum(len(row["triangles"]) for row in result["rows"]),
            "complete_parity_parameters": len(parity_rows), "complete_parity_triangles": sum(len(row["triangles"]) for row in parity_rows),
            "complete_original_sectors": len(sectors), "original_S_sources": sum(sector["source_count"] for sector in sectors),
            "D_rows": sum(sector["D_row_count"] for sector in sectors), "D_nnz": sum(sector["D_nnz"] for sector in sectors),
            "D_dual_terms": sum(len(sector["D_row_dual"]) for sector in sectors),
            "distinct_parameter_high_sectors": len(unique_sectors),
            "distinct_original_S_sources": sum(sector["source_count"] for sector in unique_sectors.values()),
            "counting_convention": "Unqualified incidence totals count triangle-sector instances; distinct totals deduplicate by (p,h).",
            "eta_transfer_identities": 5, "count_formula_checks": len(counts),
        }
        result["status"] = "COMPLETE"
        result["scope"] = "Finite full original-incidence and signed-source audit; the uniform elementary proof supplies the all-p lower bound, not an upper bound."
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
    parser.add_argument("--results", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/audit-results.json")
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--memory-mib", type=int, default=1024)
    args = parser.parse_args()
    result = audit(args.results, args.output, args.seconds, args.memory_mib)
    print(json.dumps({"status": result["status"], "totals": result.get("totals"),
                      "artifact_hash": result["artifact_hash"]}, sort_keys=True))
    return 0 if result["status"] == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
