"""Independent exact potential and original-source annihilation audit, CPU only."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import math
import time
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
CAMPAIGN = [*range(8, 21), 25, 32, 50, 64, 100]
HYPOTHESIS_SHA256 = "cd0e5715326570487cec4e79da27bbc79a14e9b3dbc1aa0787f86eebb42daf56"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_bitsets():
    path = EXPERIMENTS / "EXP-059-potential-connecting-map/audit.py"
    assert file_hash(path) == "abce39b985651b9097d5571be157702cd5a4737506dbe52cea0ee9118865c4ed"
    spec = importlib.util.spec_from_file_location("bitset059_for060audit", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def key(label):
    return label[0], tuple(label[1]), *label[2:]


def records(vector):
    return [{"coefficient": value, "exact_label": [index[0], list(index[1]), *index[2:]]}
            for index, value in sorted(vector.items()) if value]


def sparse(source):
    result = {}
    for term in source:
        index = key(term["exact_label"])
        assert index not in result and term["coefficient"] != 0
        result[index] = term["coefficient"]
    return result


def combine(*weighted_vectors):
    result = Counter()
    for vector, weight in weighted_vectors:
        for index, value in vector.items():
            result[index] += weight * value
    return {index: value for index, value in result.items() if value}


def interval_fields(p, j):
    k = p - 2 - j
    fields = {u: [0] * p for u in (0, j, k)}
    for r in range(p):
        fields[0][r] = int(j + 1 <= r <= k)
        fields[j][r] = -int(j + 1 <= r <= p - 2)
        fields[k][r] = -int(k + 1 <= r <= p - 2)
    return fields


def potential_operator(p, fields, check=lambda: None):
    """Dense potential rows and external-star anchors, with exact original labels."""
    low = {*range(1, p + 1), *range(3 * p, 4 * p - 1)}
    empty = [0] * p
    result = {}
    for u, values in sorted(fields.items()):
        assert len(values) == p and all(values[r] == 0 for r in range(u + 1))
        for r in range(p):
            for s in range(r + 1, p):
                value = values[s] - values[r]
                coefficient = p + u - r - s
                if value and 1 <= coefficient <= p:
                    exterior = tuple(sorted((low - {p - r, p - s, 3 * p + u}) | {6 * p, 8 * p - 2}))
                    result[("S", exterior, coefficient)] = (-1) ** (p + r + s + u) * value
            check()
    for u in range(p - 1):
        for v in range(u + 1, p - 1):
            if u not in fields and v not in fields:
                continue
            difference = [a - b for a, b in zip(fields.get(u, empty), fields.get(v, empty), strict=True)]
            total = u + v
            anchor = total + 1 if total <= p - 2 else 0
            for r in range(max(0, total - p + 2), min(p - 1, total) + 1):
                value = difference[r] - difference[anchor]
                if value:
                    exterior = tuple(sorted((low - {p - r, 3 * p + u, 3 * p + v}) | {6 * p, 8 * p - 2}))
                    index = ("S", exterior, 3 * p + total - r)
                    assert index not in result
                    result[index] = (-1) ** (p + r + u + v) * value
            check()
    return result


def e(p, r, u, v, weight=1):
    low = {*range(1, p + 1), *range(3 * p, 4 * p - 1)}
    exterior = tuple(sorted((low - {p - r, 3 * p + u, 3 * p + v}) | {6 * p}))
    return {("K", exterior, 11 * p - 2 + u + v - r): weight * (-1) ** (p + r + u + v)}


def q(p, a):
    low = {*range(1, p + 1), *range(3 * p, 4 * p - 1)}
    return {("K", tuple(sorted((low - {p - a, 3 * p}) | {6 * p})), 8 * p - 2 - a): 1}


def target(p):
    """Physical four-row 2 eta from EXP-057, without normalized-coordinate imports."""
    low = {*range(1, p + 1), *range(3 * p, 4 * p - 1)}
    return {("K", tuple(sorted((low - {a, 3 * p, 3 * p + j}) | {6 * p})), 10 * p + c):
            coefficient * (-1) ** p for a, j, c, coefficient in (
                (p - 3, 2, p - 3, 4), (p - 2, 2, p - 2, -2),
                (p - 2, 1, p - 3, 4), (p - 3, 1, p - 4, -4))}


def full_boundary(p, source, bitsets, independent, check=lambda: None):
    s_source = records({index: value for index, value in source.items() if index[0] == "S"})
    k_source = records({index: value for index, value in source.items() if index[0] == "K"})
    s_boundary = bitsets.bitset_boundary(p, s_source, independent, check)
    k_boundary = independent.independent_boundary(p, k_source) if k_source else {}
    check()
    return combine((s_boundary, 1), (k_boundary, 1))


def high_face_formula(p, source):
    result = {}
    for (kind, exterior, coefficient), weight in source.items():
        assert kind == "S"
        if coefficient in (1, 3 * p):
            face = tuple(value for value in exterior if value != 8 * p - 2)
            index = ("K", face, 8 * p - 2 + coefficient)
            assert index not in result
            result[index] = -weight
    return result


def archived_sources(path, result):
    manifest = result["full_source_archive"]
    filename = manifest["filename"]
    assert Path(filename).name == filename and filename.endswith(".json.gz")
    archive_path = path.parent / filename
    compressed = archive_path.read_bytes()
    assert len(compressed) == manifest["gzip_bytes"]
    assert hashlib.sha256(compressed).hexdigest() == manifest["gzip_sha256"]
    assert compressed[:3] == b"\x1f\x8b\x08" and compressed[4:8] == b"\x00" * 4
    assert not compressed[3] & 8 and manifest["gzip_mtime"] == 0 and manifest["gzip_filename"] == ""
    assert 0 < manifest["raw_bytes"] < 128 * 1024 ** 2
    with gzip.open(archive_path, "rb") as archive:
        raw = archive.read(manifest["raw_bytes"] + 1)
    assert len(raw) == manifest["raw_bytes"] and hashlib.sha256(raw).hexdigest() == manifest["raw_sha256"]
    payload = json.loads(raw)
    assert payload["experiment"] == "EXP-060"
    assert payload["format"] == manifest["format"] == "full_original_V_source_records_v1"
    assert raw == json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    assert len(payload["sources"]) == manifest["parameters"] == len(result["campaign"])
    assert [item["p"] for item in payload["sources"]] == result["campaign"]
    sources = {}
    for item, row in zip(payload["sources"], result["rows"], strict=True):
        assert item["p"] == row["p"]
        assert item["source_hash"] == row["source_hash"] == digest(item["full_source"])
        assert item["source_support"] == row["source_support"] == len(item["full_source"])
        sources[item["p"]] = item["full_source"]
    return sources, manifest


def audit(results_path=None, budget_seconds=60):
    if not math.isfinite(budget_seconds) or not 0 < budget_seconds <= 60:
        raise ValueError("audit budget must be finite, positive, and at most 60 seconds")
    started = time.monotonic()
    bitsets = load_bitsets()
    independent = bitsets.arithmetic()
    last_memory = started - 1

    def check():
        nonlocal last_memory
        now = time.monotonic()
        if now - started > budget_seconds:
            raise RuntimeError("EXP-060 independent audit time cap")
        if now - last_memory >= 0.1:
            last_memory = now
            if bitsets.private_memory_bytes() > 1024 ** 3:
                raise RuntimeError("EXP-060 independent audit private-memory cap")

    path = results_path or HERE / "artifacts/results.json"
    result = json.loads(path.read_text(encoding="utf-8"))
    assert file_hash(HERE / "hypothesis.md") == HYPOTHESIS_SHA256
    for relative, expected in result["premises"].items():
        assert file_hash(EXPERIMENTS / relative) == expected
    assert result["artifact_hash"] == digest({k: v for k, v in result.items() if k != "artifact_hash"})
    assert result["status"] == "COMPLETE" and result["campaign"] in ([8], CAMPAIGN)
    assert result["p11_original_source_accessed"] is False and result["old_hnf_source_accessed"] is False
    assert [row["p"] for row in result["rows"]] == result["campaign"]
    full_sources, archive_manifest = archived_sources(path, result)
    verified = []
    literal_checks = 0
    for saved in result["rows"]:
        saved = dict(saved)
        p = saved["p"]
        saved["full_source"] = full_sources[p]
        fields = {"F1": interval_fields(p, 1), "F2": interval_fields(p, 2),
                  "delta03": {0: [int(r == 3) for r in range(p)]},
                  "delta02": {0: [int(r == 2) for r in range(p)]}}
        sources = {name: potential_operator(p, field, check) for name, field in fields.items()}
        boundaries = {}
        for name, source in sources.items():
            actual = full_boundary(p, source, bitsets, independent, check)
            assert actual == high_face_formula(p, source) and all(index[0] == "K" for index in actual)
            if p <= 12:
                assert independent.independent_boundary(p, records(source)) == actual
                literal_checks += 1
            boundaries[name] = actual
            summary = saved["components"][name]
            assert summary["source_support"] == len(source) and summary["source_hash"] == digest(records(source))
            assert sparse(summary["full_boundary"]) == actual
            assert summary["boundary_hash"] == digest(records(actual)) and summary["P1_full_boundary_verified"] is True
        for j in (1, 2):
            assert boundaries[f"F{j}"] == e(p, j, 0, j, 2)
        for a in (2, 3):
            name = f"Q{a}"
            sources[name] = q(p, a)
            boundaries[name] = full_boundary(p, sources[name], bitsets, independent, check)
            assert all(index[0] == "K" and 6 * p in index[1] for index in boundaries[name])
        b = combine((boundaries["delta03"], 1), (boundaries["Q3"], -1))
        d = combine((boundaries["delta02"], 1), (boundaries["Q2"], 1))
        assert b == combine((e(p, 3, 0, 1), 1), (e(p, 2, 0, 2), 1), (e(p, 3, 0, 2), 1))
        assert d == combine((e(p, 1, 0, 1), 1), (e(p, 2, 0, 1), 1))
        assert sparse(saved["B_boundary"]) == b and sparse(saved["D_boundary"]) == d
        eta_reconstruction = combine((e(p, 2, 0, 2), 1), (e(p, 1, 0, 1), 2), (b, -2), (d, -2))
        assert combine((eta_reconstruction, 2)) == target(p)
        source = combine((sources["F2"], 1), (sources["F1"], 2), (sources["delta03"], -4),
                         (sources["delta02"], -4), (sources["Q3"], 4), (sources["Q2"], -4))
        assert sparse(saved["full_source"]) == source and saved["full_source"] == records(source)
        assert saved["source_hash"] == digest(records(source)) and saved["source_support"] == len(source)
        assert saved["source_coefficient_height"] == max(abs(value) for value in source.values())
        actual = full_boundary(p, source, bitsets, independent, check)
        expected = target(p)
        assert actual == expected and len(actual) == 4 and all(index[0] == "K" for index in actual)
        if p <= 12:
            assert independent.independent_boundary(p, records(source)) == actual
            literal_checks += 1
        assert sparse(saved["full_boundary"]) == actual and saved["boundary_hash"] == digest(records(actual))
        simple_omission = combine((source, 1), (sources["delta02"], 4), (sources["Q2"], 4))
        simple_difference = combine((full_boundary(p, simple_omission, bitsets, independent, check), 1), (expected, -1))
        assert simple_difference == combine((e(p, 1, 0, 1), 4), (e(p, 2, 0, 1), 4))
        historical = combine((sources["F2"], 1), (sources["F1"], -2),
                             (sources["delta03"], -4), (sources["Q3"], 4))
        historical_difference = combine((full_boundary(p, historical, bitsets, independent, check), 1), (expected, -1))
        assert historical_difference == combine((e(p, 2, 0, 1), 4), (e(p, 1, 0, 1), -4))
        assert sparse(saved["literal_earliest_difference"]) == historical_difference
        assert saved["literal_earliest_difference_hash"] == digest(records(historical_difference))
        assert saved["literal_earliest_wrong_F1_sign_and_missing_delta02_fails"] is True
        assert sparse(saved["rejected_difference"]) == simple_difference
        assert saved["rejected_difference_hash"] == digest(records(simple_difference))
        first = next(iter(sparse(saved["full_source"]).items()))
        first_source = {first[0]: first[1]}
        single_boundary = full_boundary(p, first_source, bitsets, independent, check)
        sign_difference = {index: -2 * value for index, value in single_boundary.items()}
        coefficient_difference = full_boundary(p, {first[0]: 1}, bitsets, independent, check)
        assert sign_difference and coefficient_difference
        assert saved["sign_mutation_difference_hash"] == digest(records(sign_difference))
        assert saved["coefficient_mutation_difference_hash"] == digest(records(coefficient_difference))
        assert all(saved[name] is True for name in ("P1", "P2", "P3", "M_V_equals_twice_eta",
            "full_original_independent_agreement", "rejected_missing_delta02_formula_fails",
            "sign_mutation_rejected", "coefficient_mutation_rejected"))
        verified.append({"p": p, "full_source_support": len(source), "full_original_identity": True,
                         "P1_P2_P3_verified": True, "zero_D_and_exactly_four_K_rows": True,
                         "simple_omission_difference": records(simple_difference),
                         "literal_historical_difference": records(historical_difference),
                         "coefficient_and_sign_mutations_rejected": True})
        print(f"p={p}: independent P1/P2/P3 and M V=2 eta PASS, source {len(source)}", flush=True)
        check()
    assert result["claims"]["uniform_nonvanishing_second_class_upper_bound"] == "NOT_ESTABLISHED"
    certificate = {"experiment": "EXP-060", "status": "INDEPENDENT_AUDIT_PASS",
                   "parameters_verified": result["campaign"], "literal_full_differential_crosschecks": literal_checks,
                   "rows": verified, "p11_original_source_accessed": False, "old_hnf_source_accessed": False,
                   "scope": "exact 2-annihilation; uniform claim requires signed proof; no nonvanishing claim",
                   "result_sha256": file_hash(path), "producer_sha256": file_hash(HERE / "run.py"),
                   "full_source_archive": archive_manifest,
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
    print(json.dumps({"status": certificate["status"], "parameters": certificate["parameters_verified"],
                      "artifact_hash": certificate["artifact_hash"]}))


if __name__ == "__main__":
    main()
