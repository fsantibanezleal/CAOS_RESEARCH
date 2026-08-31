"""Independent rank-order and odd-prime audit for EXP-038 finite gates."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
CELLS = (
    {
        "p": 11,
        "expected_excess": 102,
        "primary": HERE / "artifacts" / "target-t2-p11.json",
        "alternate": HERE / "artifacts" / "audit-canonical-t2-p11.json",
        "primary_sha256": "7b72b272338acfbd26dfe8e82a7fa425174e5d3fc3729ed785948f7d868a6ca1",
        "alternate_sha256": "4f7b60229c5e782891f3369ad6075c636a1452455d5df195844e919a2f3a47f1",
    },
    {
        "p": 12,
        "expected_excess": 138,
        "primary": HERE / "artifacts" / "target-t2-p12.json",
        "alternate": HERE / "artifacts" / "audit-canonical-t2-p12.json",
        "primary_sha256": "960585dff4288a19242d0388f0c229a13701c2112dfa2f9cae415f5a2ff3d14e",
        "alternate_sha256": "dbf5f7b34bead8dba6fda769b9561ee311455f62215df8b07370b051f8359097",
    },
)
STRUCTURAL_KEYS = (
    "rows",
    "columns",
    "initial_nonzeros",
    "row_leaf_pivots",
    "two_sided_leaf_pivots",
    "peeled_rank",
    "residual_rows",
    "residual_columns",
    "residual_nonzeros",
)
RANK_KEYS = (
    "rank_kernel_boundary",
    "kernel_cokernel_dimension",
    "rank_d_boundary",
    "rank_combined",
    "connecting_image_dimension_in_kernel_cokernel",
    "surviving_a_dimension",
)
BASIS_KEYS = (
    "p",
    "t",
    "target_offset",
    "homological_degree",
    "total_offset",
    "kernel_codomain_rows",
    "kernel_domain_columns",
    "d_source_columns",
    "d_codomain_rows",
    "kernel_codomain_hash",
    "kernel_domain_hash",
    "d_source_hash",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def audit_cell(spec: dict[str, object]) -> dict[str, object]:
    primary_path = spec["primary"]
    alternate_path = spec["alternate"]
    if not isinstance(primary_path, Path) or not isinstance(alternate_path, Path):
        raise TypeError("cell paths must be pathlib.Path instances")
    actual_hashes = {
        "primary": sha256(primary_path),
        "alternate": sha256(alternate_path),
    }
    expected_hashes = {
        "primary": spec["primary_sha256"],
        "alternate": spec["alternate_sha256"],
    }
    if actual_hashes != expected_hashes:
        raise AssertionError({"p": spec["p"], "artifact_hashes": actual_hashes})

    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    alternate = json.loads(alternate_path.read_text(encoding="utf-8"))
    first = primary["rows"][0]
    second = alternate["rows"][0]
    expected_excess = spec["expected_excess"]
    checks = {
        "both_runs_complete": (
            primary["status"] == alternate["status"] == "PASS_FINITE_OUT_OF_SAMPLE"
        ),
        "premise_agreement": primary["premise_hashes"] == alternate["premise_hashes"],
        "formula_agreement": primary["formula_certificate"] == alternate["formula_certificate"],
        "basis_agreement": all(first[key] == second[key] for key in BASIS_KEYS),
        "structural_agreement": all(
            first["structural_profiles"][matrix][key]
            == second["structural_profiles"][matrix][key]
            for matrix in ("kernel", "d_boundary", "combined")
            for key in STRUCTURAL_KEYS
        ),
        "gf2_rank_agreement_across_orders": all(
            first["field_rows"]["2"][key] == second["field_rows"]["2"][key]
            for key in RANK_KEYS
        ),
        "gf3_gf5_odd_rank_agreement": all(
            first["field_rows"]["3"][key] == second["field_rows"]["5"][key]
            for key in RANK_KEYS
        ),
        "exact_excess_matches": (
            first["actual_excess"] == second["actual_excess"] == expected_excess
        ),
        "prediction_matches": (
            first["predicted_excess"] == second["predicted_excess"] == expected_excess
        ),
        "candidate_matches": first["candidate_matches"] and second["candidate_matches"],
    }
    if not all(checks.values()):
        raise AssertionError({"p": spec["p"], "checks": checks})
    return {
        "p": spec["p"],
        "t": 2,
        "artifact_hashes": actual_hashes,
        "checks": checks,
        "ranks": {
            "GF2": first["field_rows"]["2"],
            "GF3": first["field_rows"]["3"],
            "GF5": second["field_rows"]["5"],
        },
        "actual_excess": expected_excess,
    }


def main() -> int:
    cells = [audit_cell(spec) for spec in CELLS]
    certificate = {
        "experiment": "EXP-038",
        "status": "PASS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cells": cells,
        "finite_sequence_p4_p12": [1, 4, 9, 18, 31, 49, 72, 102, 138],
        "scope": (
            "audited finite agreement at (p,t)=(11,2) and (12,2); the proposed "
            "degree-six relation, order-seven recurrence, and all-parameter series remain unproved"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    OUTPUT.write_text(
        json.dumps(certificate, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
