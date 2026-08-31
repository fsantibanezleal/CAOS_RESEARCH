"""Independent rank-order and odd-prime audit for EXP-038 at (p,t)=(11,2)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIMARY = HERE / "artifacts" / "target-t2-p11.json"
ALTERNATE = HERE / "artifacts" / "audit-canonical-t2-p11.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_HASHES = {
    "primary": "7b72b272338acfbd26dfe8e82a7fa425174e5d3fc3729ed785948f7d868a6ca1",
    "alternate": "4f7b60229c5e782891f3369ad6075c636a1452455d5df195844e919a2f3a47f1",
}
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    actual_hashes = {"primary": sha256(PRIMARY), "alternate": sha256(ALTERNATE)}
    if actual_hashes != EXPECTED_HASHES:
        raise AssertionError({"artifact_hashes": actual_hashes})
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    alternate = json.loads(ALTERNATE.read_text(encoding="utf-8"))
    first = primary["rows"][0]
    second = alternate["rows"][0]
    basis_keys = (
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
    checks = {
        "both_runs_complete": (
            primary["status"] == alternate["status"] == "PASS_FINITE_OUT_OF_SAMPLE"
        ),
        "premise_agreement": primary["premise_hashes"] == alternate["premise_hashes"],
        "formula_agreement": primary["formula_certificate"] == alternate["formula_certificate"],
        "basis_agreement": all(first[key] == second[key] for key in basis_keys),
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
        "exact_excess_is_102": first["actual_excess"] == second["actual_excess"] == 102,
        "prediction_was_102": first["predicted_excess"] == second["predicted_excess"] == 102,
        "candidate_matches": first["candidate_matches"] and second["candidate_matches"],
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    certificate = {
        "experiment": "EXP-038",
        "status": "PASS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifact_hashes": actual_hashes,
        "checks": checks,
        "ranks": {
            "GF2": first["field_rows"]["2"],
            "GF3": first["field_rows"]["3"],
            "GF5": second["field_rows"]["5"],
        },
        "actual_excess": 102,
        "scope": (
            "audited finite agreement at (p,t)=(11,2); the proposed degree-six "
            "relation and all-parameter series remain unproved"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    OUTPUT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
