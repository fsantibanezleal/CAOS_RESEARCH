"""EXP-130: orchestrate the exact finite base-locus algebra gate.

CPU only. The worker is killed after the declared five-minute stage gate.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
E123_ARTIFACT = (
    HERE.parent
    / "EXP-123-direction-29-symbolic-lift"
    / "artifacts"
    / "results.json"
)
E129_ARTIFACT = (
    HERE.parent
    / "EXP-129-f7-crt-minor-atlas"
    / "artifacts"
    / "results.json"
)
E124_ARTIFACT = (
    HERE.parent
    / "EXP-124-rational-graph-alternative-chart"
    / "artifacts"
    / "results.json"
)
WORKER = HERE / "algebra_worker.py"
WORKER_ARTIFACT = HERE / "artifacts" / "algebra-worker.json"
CRT_WORKER = HERE / "crt_worker.py"
CRT_WORKER_ARTIFACT = HERE / "artifacts" / "crt-worker.json"
ALGEBRA_CHECKPOINT = HERE / "artifacts" / "algebra-checkpoint.json"
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
EXPECTED_E123_SHA256 = "43C24C42F37F952AB09EAA834EC042DBA7B7E3E02C1AF1E52E13691C7E9D30EF"
EXPECTED_E124_SHA256 = "3AE5A2DA83FA99EDFDAF06486B0AB65150D506D1378B2372710915713066D113"
EXPECTED_E129_SHA256 = "AFA272D686DCA1E08D5969F2E1C825EE4D62B9CEC4627301FEFC2A64D258B0B2"
EXPECTED_ALGEBRA_CHECKPOINT_SHA256 = "9C3E1212CE6D7FC8296DD732E7488F74731BD333446A10817F9BFAF1C41A6179"
WORKER_TIMEOUT_SECONDS = 300


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def persist(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    started = time.time()
    e123_hash = digest(E123_ARTIFACT)
    e124_hash = digest(E124_ARTIFACT)
    e129_hash = digest(E129_ARTIFACT)
    require(e123_hash == EXPECTED_E123_SHA256, "EXP-123 source hash matches")
    require(e124_hash == EXPECTED_E124_SHA256, "EXP-124 source hash matches")
    require(e129_hash == EXPECTED_E129_SHA256, "EXP-129 source hash matches")
    payload: dict[str, object] = {
        "experiment": "EXP-130",
        "source_hashes": {
            "EXP-123": e123_hash,
            "EXP-124": e124_hash,
            "EXP-129": e129_hash,
        },
        "worker_timeout_seconds": WORKER_TIMEOUT_SECONDS,
    }
    persist(payload, CHECKPOINT)
    algebra_checkpoint_hash = digest(ALGEBRA_CHECKPOINT)
    require(
        algebra_checkpoint_hash == EXPECTED_ALGEBRA_CHECKPOINT_SHA256,
        "timeout-retained exact resultant checkpoint matches",
    )
    print("[INFO] launching factorwise subresultant and CRT worker", flush=True)
    try:
        completed = subprocess.run(
            [sys.executable, str(CRT_WORKER)],
            cwd=HERE,
            capture_output=True,
            text=True,
            timeout=WORKER_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        payload.update(
            {
                "decision": "stopped_at_crt_worker_timeout",
                "worker_stdout": error.stdout or "",
                "worker_stderr": error.stderr or "",
                "elapsed_seconds": time.time() - started,
            }
        )
        persist(payload, ARTIFACT)
        print("[STOP] exact CRT worker reached the five-minute gate", flush=True)
        print("RESULT: INCONCLUSIVE AT DECLARED GATE", flush=True)
        return
    print(completed.stdout, end="", flush=True)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="", flush=True)
    require(completed.returncode == 0, "exact CRT worker completed")
    record = json.loads(CRT_WORKER_ARTIFACT.read_text(encoding="utf-8"))
    require(record["experiment"] == "EXP-130", "CRT artifact identifies EXP-130")
    require(record["principal_open_algebra"]["dimension"] == 90, "principal-open algebra has dimension 90")
    payload.update(
        {
            "retained_resultant_checkpoint_sha256": algebra_checkpoint_hash,
            "crt_worker": record,
            "crt_worker_sha256": digest(CRT_WORKER_ARTIFACT),
            "decision": record["decision"],
            "elapsed_seconds": time.time() - started,
            "scope": (
                "Exact finite base-locus algebra gate on V(R,S) intersect D(X). "
                "No A=0, full core, (72,108), degree-floor, or JC(2) conclusion."
            ),
        }
    )
    persist(payload, ARTIFACT)
    print(f"[PASS] wrote results SHA256 {digest(ARTIFACT)}", flush=True)
    if record["principal_open_algebra"]["all_blocks_covered"]:
        print("RESULT: EXISTING EXACT ATLAS CLOSES THE PRINCIPAL-OPEN BASE LOCUS", flush=True)
    else:
        print(
            "RESULT: NEW ROW SELECTION REQUIRED ON DEGREES "
            + ",".join(
                str(value)
                for value in record["principal_open_algebra"]["uncovered_degrees"]
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
