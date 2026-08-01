"""EXP-130 deterministic verifier for the accepted base-locus certificate.

CPU only. This verifier rechecks the persisted characteristic-zero artifacts
and reruns the final quotient-algebra certificate. The full reconstruction
sequence is recorded in verdict.md.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
FINAL_CERTIFIER = HERE / "final_certify.py"
FINAL_CERTIFICATE = HERE / "artifacts" / "final-certificate.json"
ARTIFACT = HERE / "artifacts" / "results.json"
EXPECTED_SOURCES = {
    "EXP-123": (
        HERE.parent
        / "EXP-123-direction-29-symbolic-lift"
        / "artifacts"
        / "results.json",
        "43C24C42F37F952AB09EAA834EC042DBA7B7E3E02C1AF1E52E13691C7E9D30EF",
    ),
    "EXP-124": (
        HERE.parent
        / "EXP-124-rational-graph-alternative-chart"
        / "artifacts"
        / "results.json",
        "3AE5A2DA83FA99EDFDAF06486B0AB65150D506D1378B2372710915713066D113",
    ),
    "EXP-129": (
        HERE.parent
        / "EXP-129-f7-crt-minor-atlas"
        / "artifacts"
        / "results.json",
        "AFA272D686DCA1E08D5969F2E1C825EE4D62B9CEC4627301FEFC2A64D258B0B2",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def persist(payload: dict[str, object]) -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    source_hashes = {}
    for name, (path, expected) in EXPECTED_SOURCES.items():
        actual = sha256(path)
        require(actual == expected, f"{name} source hash matches")
        source_hashes[name] = actual
    completed = subprocess.run(
        [sys.executable, str(FINAL_CERTIFIER)],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    print(completed.stdout, end="", flush=True)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="", flush=True)
    require(completed.returncode == 0, "final characteristic-zero certifier completed")
    certificate = json.loads(FINAL_CERTIFICATE.read_text(encoding="utf-8"))
    require(
        certificate["principal_open_base_locus"]["covered"],
        "complete principal-open base locus is covered",
    )
    require(
        certificate["principal_open_base_locus"]["dimension"] == 90,
        "principal-open base-locus algebra has dimension 90",
    )
    payload = {
        "experiment": "EXP-130",
        "source_hashes": source_hashes,
        "final_certificate_sha256": sha256(FINAL_CERTIFICATE),
        "principal_open_base_locus": certificate["principal_open_base_locus"],
        "coordinate_boundary": certificate["coordinate_boundary"],
        "decision": "complete_principal_open_base_locus_closed",
        "scope": certificate["scope"],
    }
    persist(payload)
    print(f"[PASS] results SHA256 {sha256(ARTIFACT)}", flush=True)
    print("RESULT: COMPLETE PRINCIPAL-OPEN BASE LOCUS CLOSED", flush=True)


if __name__ == "__main__":
    main()
