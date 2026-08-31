"""Deterministic audit for EXP-040 component partitions."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIMARY_P10 = HERE / "artifacts" / "target-t2-p10.json"
COMBINED = HERE / "artifacts" / "target-t2-p10-p11.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_HASHES = {
    "primary_p10": "8107af8e2810414144e5ee94f4caeaa634ca81e14af92b26050b3f50d48648b6",
    "combined": "ad1fec04199ff94b803f95f98650c8c8ab386386240d584f447afbb9fe27668b",
}
EXPECTED_RANKS = {
    10: {"2": 738459, "3": 738531, "5": 738531},
    11: {"2": 1683307, "3": 1683409, "5": 1683409},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def partition(row: dict[str, object]) -> list[int]:
    return sorted(
        (
            int(component["odd_minus_two_rank_defect"])
            for component in row["components"]
            if component["odd_minus_two_rank_defect"]
        ),
        reverse=True,
    )


def main() -> int:
    actual_hashes = {
        "primary_p10": sha256(PRIMARY_P10),
        "combined": sha256(COMBINED),
    }
    if actual_hashes != EXPECTED_HASHES:
        raise AssertionError({"artifact_hashes": actual_hashes})
    primary = json.loads(PRIMARY_P10.read_text(encoding="utf-8"))
    combined = json.loads(COMBINED.read_text(encoding="utf-8"))
    rows = {row["p"]: row for row in combined["rows"]}
    checks: dict[str, bool] = {
        "combined_run_refutes_p2": combined["status"] == "REFUTED",
        "p1_passes": combined["p1_status"] == "PASS_FINITE",
        "p2_refuted": combined["p2_status"] == "REFUTED",
        "p3_not_attempted": combined["p3_status"] == "NOT_ATTEMPTED",
        "p10_reproduced": primary["rows"][0]["row_hash"] == rows[10]["row_hash"],
        "p10_partition_67_5": partition(rows[10]) == [67, 5],
        "p11_partition_95_7": partition(rows[11]) == [95, 7],
        "declared_p11_partition_refuted": partition(rows[11]) != [96, 6],
    }
    for p, row in rows.items():
        checks[f"p{p}_aggregate_ranks"] = row["matrix"]["complete_ranks"] == EXPECTED_RANKS[p]
        checks[f"p{p}_componentwise_odd_agreement"] = all(
            component["ranks"]["3"] == component["ranks"]["5"]
            for component in row["components"]
        )
        defective = [
            component
            for component in row["components"]
            if component["odd_minus_two_rank_defect"]
        ]
        checks[f"p{p}_orientation_controls"] = all(
            component["controls"]["sign_erased_gf3_rank"]
            > component["controls"]["original_gf3_rank"]
            and component["controls"]["one_sign_flipped_gf3_rank"]
            == component["controls"]["original_gf3_rank"] + 1
            for component in defective
        )
    if not all(checks.values()):
        raise AssertionError(checks)
    certificate = {
        "experiment": "EXP-040",
        "status": "PASS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifact_hashes": actual_hashes,
        "checks": checks,
        "observed_partitions": {"10": [67, 5], "11": [95, 7]},
        "scope": (
            "P1 is exact finite evidence; P2 is refuted and P3 was not attempted; no "
            "all-parameter sector or degree-six relation theorem is claimed"
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
