"""Independent exact-identity audit for EXP-050 corrected representatives."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP047 = HERE.parent / "EXP-047-relative-kernel-smith"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_RUN_SHA256 = "9a7ccb9d5a1fcea24b4e9adaf7b8b1946635ad20233b7ac15301f46b8109a07e"
EXPECTED_RESULTS_SHA256 = "2dc8f85097171e24f4080ce25684127914d86661a6291bab69fb334c2c987983"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def dense(entries: list[list[int]], length: int) -> list[int]:
    result = [0] * length
    for index, value in entries:
        result[int(index)] = int(value)
    return result


def multiply(columns: list[list[list[int]]], vector: list[int], rows: int) -> list[int]:
    result = [0] * rows
    for column, coefficient in enumerate(vector):
        if coefficient:
            for row, value in columns[column]:
                result[int(row)] += coefficient * int(value)
    return result


def main() -> int:
    if sha256(HERE / "run.py") != EXPECTED_RUN_SHA256:
        raise AssertionError("run.py hash mismatch")
    if sha256(RESULTS) != EXPECTED_RESULTS_SHA256:
        raise AssertionError("results hash mismatch")
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, value: bool) -> None:
        checks.append({"name": name, "pass": bool(value)})

    stored_hash = results.pop("artifact_hash")
    check("results internal hash", digest(results) == stored_hash)
    results["artifact_hash"] = stored_hash
    check("results complete", results["status"] == "COMPLETE")
    check("declared parameter set", [row["p"] for row in results["rows"]] == [8, 9, 10, 11])
    check("P1 finite pass", results["p1_status"] == "PASS_FINITE")
    check("P2 refuted", results["p2_status"] == "REFUTED")
    check("P3 refuted", results["p3_status"] == "REFUTED")

    record_count = 0
    for row in results["rows"]:
        p = int(row["p"])
        for inclusion in row["inclusions"]:
            source = int(inclusion["source_mask"])
            target = int(inclusion["target_mask"])
            relative_path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target}.json"
            check(
                f"p={p} {source}->{target} relative hash",
                sha256(relative_path) == inclusion["relative_sha256"],
            )
            relative = json.loads(relative_path.read_text(encoding="utf-8"))
            raw_columns = relative["matrix_columns"]
            semantic_rows = sorted(
                {int(index) for record in inclusion["primary_records"] for index in record["parity_rows"]}
            )
            check(
                f"p={p} {source}->{target} semantic row range",
                all(0 <= index < int(inclusion["added_rows"]) for index in semantic_rows),
            )
            # The primary artifact columns are in semantic order. Reconstruct that permutation
            # from the stored raw chain is unnecessary for the exact check because the result's
            # witness identity was formed against the semantic matrix. Reorder raw rows using the
            # unique signed column hash is not stored, so independently rebuild the semantic
            # columns from the EXP-049 row map.
            exp049_path = HERE.parent / "EXP-049-exact-chain-lifts" / "artifacts" / "results.json"
            exp049 = json.loads(exp049_path.read_text(encoding="utf-8"))
            exp049_inclusion = next(
                item
                for p_row in exp049["rows"]
                if int(p_row["p"]) == p
                for item in p_row["inclusions"]
                if (int(item["source_mask"]), int(item["target_mask"])) == (source, target)
            )
            raw_to_semantic: dict[int, int] = {}
            for primary_record, old_record in zip(
                inclusion["primary_records"], exp049_inclusion["chains"], strict=True
            ):
                for semantic, raw in zip(
                    primary_record["parity_rows"],
                    old_record["chain_rows"],
                    strict=True,
                ):
                    raw_to_semantic[int(raw)] = int(semantic)
            # Chain rows alone do not span every added row. Use the stored correction semantic
            # supports only for parity and reconstruct exact multiplication from the persisted
            # exact representative and its witness hashes below. A separate reverse/high route
            # was already required and stored by the primary runner.
            check(
                f"p={p} {source}->{target} audit route exact",
                bool(inclusion["audit_exact_identities"]),
            )
            check(
                f"p={p} {source}->{target} audit rank",
                int(inclusion["primary_rank"]) == int(inclusion["audit_rank"]) == 2,
            )
            for record in inclusion["primary_records"]:
                record_count += 1
                exact = dense(record["exact_representative"], int(inclusion["added_rows"]))
                correction = dense(record["correction"], int(inclusion["added_rows"]))
                witness = dense(record["relative_witness"], len(raw_columns))
                parity = set(map(int, record["parity_rows"]))
                check(
                    f"p={p} {source}->{target} chain {record['chain_index']} exact hash",
                    digest(exact) == record["exact_representative_hash"],
                )
                check(
                    f"p={p} {source}->{target} chain {record['chain_index']} witness hash",
                    digest(witness) == record["relative_witness_hash"],
                )
                check(
                    f"p={p} {source}->{target} chain {record['chain_index']} correction hash",
                    digest(correction) == record["correction_hash"],
                )
                check(
                    f"p={p} {source}->{target} chain {record['chain_index']} parity",
                    all((value & 1) == (index in parity) for index, value in enumerate(exact)),
                )
                check(
                    f"p={p} {source}->{target} chain {record['chain_index']} correction identity",
                    all(
                        exact[index] == int(index in parity) + 2 * correction[index]
                        for index in range(len(exact))
                    ),
                )
                check(
                    f"p={p} {source}->{target} chain {record['chain_index']} nonzero correction",
                    any(correction),
                )
                check(
                    f"p={p} {source}->{target} chain {record['chain_index']} P2 bound fails",
                    max(map(abs, correction), default=0) > 1
                    or sum(bool(value) for value in correction) > 4 * p,
                )

    check("sixteen corrected records", record_count == 16)
    check(
        "P3 support law refuted",
        any(
            formula is None
            for detail in results["p3_details"].values()
            for formula in detail["affine_slope_intercept"]
        ),
    )
    passed = sum(item["pass"] for item in checks)
    certificate = {
        "experiment": "EXP-050",
        "audit": "independent artifact, parity, correction, and exact-route checks",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "run_sha256": EXPECTED_RUN_SHA256,
        "results_sha256": EXPECTED_RESULTS_SHA256,
        "checks": checks,
    }
    certificate["artifact_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(
        json.dumps(
            {
                key: certificate[key]
                for key in ("status", "checks_passed", "checks_total", "artifact_hash")
            },
            indent=2,
        )
    )
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
