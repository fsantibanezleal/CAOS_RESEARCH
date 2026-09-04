"""Verify the frozen semantic candidate against training data only."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
TRAINING = HERE / "artifacts" / "training-p8-p10.json"
OUTPUT = HERE / "artifacts" / "training-candidate-check.json"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def main() -> int:
    training = json.loads(TRAINING.read_text(encoding="utf-8"))
    if training["phase"] != "TRAINING_ONLY" or training["holdout_semantics_accessed"]:
        raise AssertionError("training leakage barrier failed")
    candidate = load_module("exp052_frozen_candidate_training", HERE / "candidate.py")
    checks = []
    for row in training["rows"]:
        p = int(row["p"])
        for inclusion in row["inclusions"]:
            source = int(inclusion["source_mask"])
            target = int(inclusion["target_mask"])
            observed = sorted(
                [[record["coefficient"], record["token"]] for record in inclusion["semantic_rows"]],
                key=lambda value: json.dumps(value, sort_keys=True, separators=(",", ":")),
            )
            predicted = candidate.candidate(p, source, target)
            checks.append(
                {
                    "p": p,
                    "source_mask": source,
                    "target_mask": target,
                    "pass": observed == predicted,
                    "observed_hash": digest(observed),
                    "predicted_hash": digest(predicted),
                    "observed_size": len(observed),
                    "predicted_size": len(predicted),
                }
            )
    passed = sum(record["pass"] for record in checks)
    result = {
        "experiment": "EXP-052",
        "phase": "TRAINING_CANDIDATE_CHECK",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "p2_status": "PASS_TRAINING" if passed == len(checks) else "REFUTED",
        "checks": checks,
    }
    result["artifact_hash"] = digest(result)
    write_json_atomic(OUTPUT, result)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
