"""Deterministic certificate for the EXP-039 component partition."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
RESULT = HERE / "artifacts" / "results-p9.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
RESULT_SHA256 = "831a4300cac10bf44753050a686a7993fabef09bf28b4332c6bb1fb9881c9e2c"
EXPECTED = {
    4: {
        "components": 27,
        "partition": [1],
        "ranks": {"2": 588, "3": 589},
        "row_hash": "51464de7688baf7d8e14d7355b7b6abc38ee76547cf2235ec3dde6acc854fae0",
    },
    5: {
        "components": 56,
        "partition": [1, 1, 1, 1],
        "ranks": {"2": 2935, "3": 2939},
        "row_hash": "99d41e413e33646b2fb9959e8a7aff4846cfdec0fbf5c8ea37bcb5822e44087b",
    },
    6: {
        "components": 100,
        "partition": [4, 2, 2, 1],
        "ranks": {"2": 11548, "3": 11557},
        "row_hash": "6d7b73e4b40c3e04aa0bc88b188cb46fb86685e6d229a2b6b8b7db9149fba8ec",
    },
    7: {
        "components": 173,
        "partition": [10, 3, 3, 2],
        "ranks": {"2": 38611, "3": 38629},
        "row_hash": "78b1ed4c32c98a84f346048a367c731ee70d9000efbe1d5ad52a73f4c2858b68",
    },
    8: {
        "components": 289,
        "partition": [20, 4, 4, 3],
        "ranks": {"2": 113694, "3": 113725},
        "row_hash": "9e59baf4571a38b26c57cb649c7bcb5c5acd28dc5c8c90741c3a6ae8cef745f3",
    },
    9: {
        "components": 447,
        "partition": [45, 4],
        "ranks": {"2": 302169, "3": 302218},
        "row_hash": "5b21f9822f5275951f6c71acd58b9227f6948ee8fda9552925fabac4552f4eef",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def free_sector_partition(p: int) -> list[int]:
    return [comb(p - 2, 3), p - 4, p - 4, p - 5]


def main() -> int:
    if sha256(RESULT) != RESULT_SHA256:
        raise AssertionError("EXP-039 result hash mismatch")
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    rows = {row["p"]: row for row in result["rows"]}
    checks: dict[str, bool] = {
        "complete_declared_range": set(rows) == set(EXPECTED),
        "experiment_complete": result["status"] == "COMPLETE",
        "p1_refuted": result["p1_status"] == "REFUTED",
        "p2_refuted": result["p2_status"] == "REFUTED",
    }
    observed: dict[str, object] = {}
    for p, expected in EXPECTED.items():
        row = rows[p]
        defective = [
            component
            for component in row["components"]
            if component["odd_minus_two_rank_defect"]
        ]
        partition = sorted(
            (component["odd_minus_two_rank_defect"] for component in defective),
            reverse=True,
        )
        checks[f"p{p}_component_count"] = row["matrix"]["component_count"] == expected["components"]
        checks[f"p{p}_partition"] = partition == expected["partition"]
        checks[f"p{p}_complete_ranks"] = row["matrix"]["complete_ranks"] == expected["ranks"]
        checks[f"p{p}_row_hash"] = row["row_hash"] == expected["row_hash"]
        checks[f"p{p}_rank_sum"] = sum(partition) == (
            expected["ranks"]["3"] - expected["ranks"]["2"]
        )
        checks[f"p{p}_orientation_controls"] = all(
            component["controls"]["sign_erased_gf3_rank"]
            > component["controls"]["original_gf3_rank"]
            and component["controls"]["one_sign_flipped_gf3_rank"]
            == component["controls"]["original_gf3_rank"] + 1
            for component in defective
        )
        observed[str(p)] = {
            "partition": partition,
            "defective_components": len(defective),
            "total_defect": sum(partition),
        }

    for p in range(6, 9):
        checks[f"p{p}_free_sector_partition"] = (
            observed[str(p)]["partition"] == free_sector_partition(p)
        )
    latent_p9 = free_sector_partition(9)
    checks["p9_support_merge_preserves_latent_partition"] = (
        observed["9"]["partition"] == [sum(latent_p9[:3]), latent_p9[3]]
    )
    checks["free_sector_total_matches_p6_p9"] = all(
        sum(free_sector_partition(p)) == observed[str(p)]["total_defect"]
        for p in range(6, 10)
    )
    free_p10 = sum(free_sector_partition(10))
    checks["free_sector_extension_predicts_old_p10_value"] = free_p10 == 73
    checks["exp037_first_relation_deficit"] = free_p10 - 72 == 1
    if not all(checks.values()):
        raise AssertionError(checks)

    certificate = {
        "experiment": "EXP-039",
        "status": "PASS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "result_sha256": RESULT_SHA256,
        "checks": checks,
        "observed": observed,
        "latent_free_sector_law_p6_p10": (
            "C(p-2,3)+(p-4)+(p-4)+(p-5)"
        ),
        "latent_p9_partition": latent_p9,
        "free_p10_prediction": free_p10,
        "exact_p10_value": 72,
        "scope": (
            "exact finite component partitions and orientation controls; the latent sector "
            "identification and degree-six relation require a new experiment"
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
