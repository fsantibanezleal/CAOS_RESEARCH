"""Replay completed distinct-zero evidence; never run a mathematical search."""
from __future__ import annotations

import hashlib
import json

from . import riemann_publication

PROBLEM = "problems/number-theory/riemann-hypothesis"
E20 = "EXP-020-quadratic-local-certificate"
E25 = "EXP-025-vector-pressure-distinct-lift"
PAPER = "manuscripts/riemann-hypothesis/distinct-zero-gram"
INPUTS = {
    "distinct_cover": (E20, f"{PROBLEM}/experiments/{E20}/artifacts/independent-cover-audit.json"),
    "distinct_transfer": (E20, f"{PROBLEM}/experiments/{E20}/artifacts/exact-transfer-audit.json"),
    "distinct_native": (E20, f"{PROBLEM}/experiments/{E20}/artifacts/native-kernel-taylor-full.json"),
    "distinct_controls": (E20, f"{PROBLEM}/experiments/{E20}/artifacts/actual-cover-corruption-controls.json"),
    "distinct_archive": (E20, f"{PROBLEM}/experiments/{E20}/artifacts/runtime-archive-receipt.json"),
    "distinct_vector": (E25, f"{PROBLEM}/experiments/{E25}/artifacts/independent-rational-audit.json"),
    "distinct_vector_preflight": (E25, f"{PROBLEM}/experiments/{E25}/artifacts/preflight.json"),
    "distinct_attestation": (E25, f"{PROBLEM}/experiments/{E25}/artifacts/input/attestation.json"),
    "distinct_external_source": (E25, f"{PROBLEM}/experiments/{E25}/artifacts/input/Solution.lean"),
    "distinct_license": (E25, f"{PROBLEM}/experiments/{E25}/artifacts/input/LICENSE-2.0.txt"),
    "distinct_vector_proof": (E25, f"{PROBLEM}/experiments/{E25}/proof.md"),
    "distinct_vector_review": (E25, f"{PROBLEM}/experiments/{E25}/final-review.md"),
    "distinct_vector_verdict": (E25, f"{PROBLEM}/experiments/{E25}/verdict.md"),
    "distinct_local_proof": (E20, f"{PROBLEM}/experiments/{E20}/proof.md"),
    "distinct_local_verdict": (E20, f"{PROBLEM}/experiments/{E20}/verdict.md"),
    "distinct_publication": ("distinct-zero-companion", f"{PAPER}/publication-receipt.json"),
    "distinct_paper": ("distinct-zero-companion", f"{PAPER}/main.pdf"),
    "distinct_current_publication": ("distinct-zero-publication-correction", f"{PAPER}/current-publication.json"),
    "distinct_companion": ("distinct-zero-publication-correction", f"{PAPER}/evidence-companion.json"),
}


def validate(raw: dict[str, bytes]) -> dict:
    """Validate recorded receipts, retaining the external arithmetic trust boundary."""
    if set(INPUTS) - set(raw):
        raise ValueError("Distinct-zero evidence rejected: missing source")
    def record(role, schema):
        data = json.loads(raw[role])
        if data.get("schema") != schema:
            raise ValueError(f"Distinct-zero receipt schema mismatch: {role}")
        return data

    def require(condition, message):
        if not condition:
            raise ValueError(f"Distinct-zero evidence rejected: {message}")

    cover = record("distinct_cover", "exp020-independent-cover-audit-v1")
    transfer = record("distinct_transfer", "exp020-exact-transfer-audit-v1")
    native = record("distinct_native", "exp020-native-kernel-taylor-audit-v1")
    controls = record("distinct_controls", "exp020-actual-cover-corruption-controls-v1")
    archive = record("distinct_archive", "exp020-runtime-archive-receipt-v1")
    vector = record("distinct_vector", "exp025-independent-rational-audit-v1")
    preflight = record("distinct_vector_preflight", "exp025-vector-pressure-preflight-v1")
    publication = record("distinct_publication", "distinct-zero-zenodo-publication-v1")
    for name, value in [("cover", cover), ("transfer", transfer), ("controls", controls),
                        ("archive", archive), ("vector", vector), ("publication", publication)]:
        require(value.get("passed") is True, f"{name} did not pass")
    reports = transfer["reports_sha256"]
    require(set(reports) == {f"shard-{i:03}.json" for i in range(96)}, "incomplete local cover")
    require(cover.get("reports_sha256") == reports
            and controls.get("actual_cover_reports_sha256") == reports, "report bindings")
    totals = transfer["totals"]
    require(cover["totals"] == totals and totals == {
        "nodes": 107752902, "pruned": 53876579, "splits": 53876323,
        "initial_boxes": 256, "pressure_pruned": 95807,
        "interval_pruned": 30730268, "tangent_pruned": 23050504}, "tree accounting")
    require(native.get("all_cells_passed") is True and native.get("budget_expired") is False
            and native["completed_closed_cells"] == native["table_cells"] == 61029
            and native.get("unresolved_cell") is None, "native closed-cell audit")
    require(native["packet_sha256"] == transfer["packet_sha256"] == cover["binding"]["packet_sha256"],
            "packet bindings")
    require(native["tables_sha256"] == cover["binding"]["tables"], "table bindings")
    require(len(controls["cases"]) == 12 and all(x.get("rejected") is True for x in controls["cases"]),
            "actual corruption controls")
    require(transfer["liminf_fraction"] == archive["liminf_fraction"]
            == "3997934614153/4775507750000", "local transfer fraction")
    require(archive["members"] == 233 and archive["extracted_stdlib_cover_audit"] is True
            and archive["extracted_exact_transfer_audit"] is True
            and archive["native_full_table_audit_included_and_bound"] is True, "archive reproduction")
    require(transfer["m"] == 958 and transfer["r"] == 8 and transfer["pressure"] == "1/2500"
            and transfer["delta"] == "3051/500000", "local parameters")
    source_hash = hashlib.sha256(raw["distinct_external_source"]).hexdigest()
    require(source_hash == vector["source_sha256"] == preflight["source_sha256"]
            == "65564079527487fde93b43bb83dd840a768acf9fb8db1f1f015d38c4faf3b7d4", "external source bytes")
    attestation = json.loads(raw["distinct_attestation"])
    require(attestation.get("result") == "kernel-verified" and attestation.get("submissionId") == "attempt-013"
            and set(attestation["kernels"]) == {"lean", "nanoda"}, "external attestation")
    require(b"Apache License" in raw["distinct_license"], "source license")
    require(vector["liminf_fraction"] == preflight["conditional_transfer"]["liminf_fraction"]
            == "30945470743359/36955122080000", "vector transfer fraction")
    require(vector["pressure_total"] == preflight["conditional_transfer"]["pressure_sum"]
            == "199193/50000000", "vector pressure total")
    params = preflight["conditional_transfer"]
    require(all(params[k] == v for k, v in {
        "r": 6, "m": 742, "tau": "12043/5000", "c": "17043/5000",
        "delta": "39369/5000000"}.items()), "vector parameters")
    require(preflight["gap_pressures"] == ["10367/25000000", "8793/12500000",
            "87381/100000000", "87381/100000000", "8793/12500000", "10367/25000000"],
            "individual pressure vector")
    require(vector["external_local_formalization_rebuilt_here"] is False, "external trust boundary")
    require(all(value is True for value in vector["negative_controls"].values())
            and len(vector["negative_controls"]) == 3
            and vector["counting_controls"]["exact_list_block_cases"] == 288
            and vector["counting_controls"]["block_pair_checks"] == 183
            and vector["counting_controls"]["unequal_pressure_vector_used"] is True,
            "independent rational controls")
    require(vector["span_capacities"] == preflight["span_capacities"]
            and vector["residuals"] == params["residuals"], "vector residual bindings")
    require(vector["window"]["H_cert"] == preflight["window"]["H_cert"] == "33608554629/50000000000",
            "vector scalar binding")
    require(b"confirmed" in raw["distinct_vector_verdict"].lower()
            and b"confirmed" in raw["distinct_local_verdict"].lower()
            and b"pass internal review" in raw["distinct_vector_review"], "completed proof reviews")
    require(publication["id"] == 23128663 and publication["concept_doi"] == "10.5281/zenodo.23128662",
            "publication record")
    # Preserve the original deposit receipt; admit current packaging separately.
    files = publication["files"]
    require(len(files) == 3 and all(f.get("live_download_exact_match") is True for f in files),
            "published byte checks")
    pdf = next(f for f in files if f["filename"].endswith(".pdf"))
    require(pdf["sha256"] == hashlib.sha256(raw["distinct_paper"]).hexdigest(), "published PDF bytes")
    zipped = next(f for f in files if f["filename"] == archive["archive_filename"])
    require(zipped["sha256"] == archive["archive_sha256"], "published runtime archive")
    current, companion = riemann_publication.admit(publication, raw["distinct_current_publication"],
                                                  raw["distinct_companion"], raw["distinct_paper"])
    return {
        "schema": "riemann-distinct-zero-v1", "accepted": True,
        "counted_objects": "distinct zero points in the whole critical strip",
        "denominator": "all nontrivial zeros counted with multiplicity up to height T",
        "local": {"fraction": transfer["liminf_fraction"], "decimal": "0.8371747724947154",
                  "m": transfer["m"], "r": transfer["r"], "tau": transfer["tau"], "c": transfer["c"],
                  "delta": transfer["delta"], "pressure": transfer["pressure"],
                  "completed_shards": 96, "nodes": totals["nodes"], "closed_cells": 61029,
                  "corruption_controls": 12, "accepted": True},
        "vector": {"fraction": vector["liminf_fraction"], "decimal": "0.8373797460706156",
                   "parameters": preflight["conditional_transfer"], "gap_pressures": preflight["gap_pressures"],
                   "H_lower": vector["window"]["H_cert"], "accepted": True,
                   "source_sha256": source_hash, "external_local_formalization_rebuilt_here": False,
                   "source_author": "Samuel Lavery; window by typh; weighted refinement by Ainta"},
        "publication": current, "evidence_companion": companion, "archive": archive,
        "incomplete_experiments": ["019", "023"],
        "excluded_claims": transfer["excluded_claims"],
        "trust_boundary": "Recorded source-dependent proofs; EXP-020 native checks share FLINT/Arb; EXP-025 external Lean/nanoda verification was archived, not rebuilt locally.",
    }
