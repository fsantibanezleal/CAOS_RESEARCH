"""Independent artifact-order and odd-prime audit for EXP-037 at (p,t)=(10,2)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIMARY = HERE / "artifacts" / "target-t2-p10.json"
ALTERNATE = HERE / "artifacts" / "audit-canonical-t2-p10.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_HASHES = {
    "primary": "ca97087466fdd705e22f69e79cdfecfc7dbce0684475b98bd99757cfed030d7b",
    "alternate": "a8456b4d2de3fcf53cf97a63b63671656b4968fac80f8b8f151b76f43aba1b05",
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
    basis_agreement = all(first[key] == second[key] for key in basis_keys)
    premise_agreement = primary["premise_hashes"] == alternate["premise_hashes"]
    structural_agreement = all(
        first["structural_profiles"][matrix][key]
        == second["structural_profiles"][matrix][key]
        for matrix in ("kernel", "d_boundary", "combined")
        for key in STRUCTURAL_KEYS
    )
    gf2_agreement = all(
        first["field_rows"]["2"][key] == second["field_rows"]["2"][key]
        for key in RANK_KEYS
    )
    odd_agreement = all(
        first["field_rows"]["3"][key] == second["field_rows"]["5"][key]
        for key in RANK_KEYS
    )
    actual_excess = (
        first["field_rows"]["2"]["surviving_a_dimension"]
        - first["field_rows"]["3"]["surviving_a_dimension"]
    )
    checks = {
        "primary_status_refuted": primary["status"] == "REFUTED_QUASIPOLYNOMIAL",
        "alternate_status_complete": alternate["status"] == "PASS_FINITE_OUT_OF_SAMPLE",
        "premise_agreement": premise_agreement,
        "basis_agreement": basis_agreement,
        "structural_agreement": structural_agreement,
        "gf2_rank_agreement_across_orders": gf2_agreement,
        "gf3_gf5_odd_rank_agreement": odd_agreement,
        "exact_excess_is_72": actual_excess == 72,
        "prediction_was_73": first["predicted_excess"] == 73,
        "candidate_refuted": first["candidate_matches"] is False,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    certificate = {
        "experiment": "EXP-037",
        "status": "PASS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifact_hashes": actual_hashes,
        "checks": checks,
        "ranks": {
            "GF2": first["field_rows"]["2"],
            "GF3": first["field_rows"]["3"],
            "GF5": second["field_rows"]["5"],
        },
        "actual_excess": actual_excess,
        "refuted_prediction": first["predicted_excess"],
        "scope": (
            "exact finite refutation at (p,t)=(10,2); no all-parameter formula "
            "and no resolution of the Huneke-Wiegand conjecture"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    OUTPUT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
