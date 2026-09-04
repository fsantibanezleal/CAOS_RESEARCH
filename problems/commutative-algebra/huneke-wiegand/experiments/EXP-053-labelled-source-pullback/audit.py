"""Integrity and cross-completion audit for the partial EXP-053 artifact."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "extract_training.py"
ARTIFACT = HERE / "artifacts" / "training-p8-p10.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
SOURCE_SHA256 = "5ee95eece90e3278b769a277ce124e8d21a9bce74f879ad696260994070bfbab"
ARTIFACT_SHA256 = "c415521c477b715ecea71cb1e983279b26f44baed78e54995674fa430167dc31"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_source():
    spec = importlib.util.spec_from_file_location("exp053_source_for_audit", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load extractor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if sha256(SOURCE) != SOURCE_SHA256 or sha256(ARTIFACT) != ARTIFACT_SHA256:
        raise AssertionError("source or artifact hash mismatch")
    source = load_source()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    stored_hash = artifact.pop("artifact_hash")
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool) -> None:
        checks.append({"name": name, "passed": bool(passed)})
        if not passed:
            raise AssertionError(name)

    check("internal artifact hash", source.digest(artifact) == stored_hash)
    check("resource status", artifact["status"] == "RESOURCE_STOP_WITH_P2_REFUTATION")
    check("holdout locked", artifact["p11_source_labels_accessed"] is False)
    check("completed parameters", artifact["completed_parameters"] == [8, 9])
    check("stopped parameter", int(artifact["stopped_parameter"]) == 10)
    check("P1 resource verdict", artifact["p1_status"] == "INCONCLUSIVE_RESOURCE")
    check("P2 refuted", artifact["p2_status"] == "REFUTED")
    check("P3 unevaluated", artifact["p3_status"] == "NOT_EVALUATED_HOLDOUT_LOCKED")
    for row in artifact["rows"]:
        p = int(row["p"])
        check(f"p{p} unique mapping", row["column_mapping_unique"] is True)
        check(f"p{p} no mapping ambiguity", not row["mapping_ambiguities"])
        check(f"p{p} two completions", len(row["inclusions"]) == 2)
        left, right = row["inclusions"]
        check(f"p{p} common cycle coordinates", left["cycle_columns"] == right["cycle_columns"])
        check(f"p{p} common labelled source multiset", left["source_multiset_hash"] == right["source_multiset_hash"])
        for item in row["inclusions"]:
            label = f"p{p} {item['source_mask']}->{item['target_mask']}"
            support = item["source_support"]
            check(f"{label} support count", len(support) == int(item["source_support_size"]))
            check(f"{label} coefficient maximum", max(abs(int(record["coefficient"])) for record in support) == int(item["source_max_abs_coefficient"]))
            check(f"{label} source kernel identity", item["source_zero_on_mask"] is True)
            check(f"{label} relative identity", item["source_to_relative_identity"] is True)
            check(f"{label} labels normalize", all(source.normalize_column(record["exact_label"], p) == record["token"] for record in support))
            check(f"{label} support hash", digest([[record["coefficient"], record["token"]] for record in support]) == item["source_multiset_hash"])
    check("declared supports", [item["source_support_size"] for row in artifact["rows"] for item in row["inclusions"]] == [125, 125, 178, 178])
    check("bounded coefficients", all(int(item["source_max_abs_coefficient"]) == 4 for row in artifact["rows"] for item in row["inclusions"]))
    check("skeleton obstruction", {key: len(value) for key, value in artifact["skeleton_vocabularies"].items()} == {"58->59": 75, "58->62": 75})
    certificate: dict[str, object] = {
        "experiment": "EXP-053", "audit_scope": "artifact integrity and cross-completion identities",
        "source_sha256": SOURCE_SHA256, "artifact_sha256": ARTIFACT_SHA256,
        "checks": checks, "passed": sum(bool(item["passed"]) for item in checks),
        "total": len(checks), "status": "PASS",
    }
    certificate["artifact_hash"] = digest(certificate)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "checks": len(checks), "artifact_hash": certificate["artifact_hash"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
