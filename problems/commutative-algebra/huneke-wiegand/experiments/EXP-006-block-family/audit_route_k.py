"""Independent reconstruction and proof audit for EXP-006 Route K."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT.parents[1] / "code"
sys.path.insert(0, str(CODE_ROOT))

from hwcert import (  # noqa: E402
    add_exact_cardinality,
    analyze_rigidity,
    build_rigidity_cnf,
    mask_from_model,
    validate_symmetric_mask,
)
from hwcert.semigroup import member, multiplicity  # noqa: E402


DRAT_TRIM = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def digest_rows(rows: list[str]) -> str:
    return hashlib.sha256("\n".join(rows).encode("ascii")).hexdigest()


def wsl_path(path: Path) -> str:
    completed = subprocess.run(
        ["wsl.exe", "-e", "wslpath", "-a", str(path.resolve())],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    return completed.stdout.strip()


def parse_model(output: str) -> set[int]:
    literals: list[int] = []
    for line in output.splitlines():
        if line.startswith("v "):
            literals.extend(int(value) for value in line[2:].split() if value != "0")
    if not literals:
        raise ValueError("SAT log contains no model")
    return {literal for literal in literals if literal > 0}


def build_formula(shift: int, level4_count: int | None = None):
    frobenius = 13 * shift - 1
    cnf, h = build_rigidity_cnf(frobenius, shift)
    for value in range(1, 4 * shift):
        cnf.add(-h[value])
    cnf.add(h[4 * shift])
    for value in range(5 * shift, 6 * shift):
        cnf.add(h[value])
    if level4_count is not None:
        add_exact_cardinality(
            cnf,
            tuple(h[4 * shift : 5 * shift]),
            level4_count,
            f"route-k:s{shift}:level4",
        )
    return cnf, h


def serialized_sha256(cnf: object, comments: list[str]) -> str:
    digest = hashlib.sha256()
    for comment in comments:
        digest.update(f"c {comment}\r\n".encode("ascii"))
    digest.update(
        f"p cnf {len(cnf.names)} {len(cnf.clauses)}\r\n".encode("ascii")
    )
    for clause in cnf.clauses:
        digest.update((" ".join(map(str, clause)) + " 0\r\n").encode("ascii"))
    return digest.hexdigest()


def semantic_audit(mask: int, shift: int, expected_sha256: str) -> dict[str, object]:
    frobenius = 13 * shift - 1
    vector = format(mask, f"0{frobenius + 1}b")[::-1]
    if hashlib.sha256(vector.encode("ascii")).hexdigest() != expected_sha256:
        raise AssertionError(f"membership hash mismatch at s={shift}")
    failures = validate_symmetric_mask(mask, frobenius)
    if failures:
        raise AssertionError(f"semantic failures at s={shift}: {failures}")
    if multiplicity(mask, frobenius) != 4 * shift:
        raise AssertionError(f"multiplicity mismatch at s={shift}")
    if any(
        not member(mask, frobenius, value)
        for value in range(5 * shift, 6 * shift)
    ):
        raise AssertionError(f"level-5 block mismatch at s={shift}")
    rigidity = analyze_rigidity(mask, frobenius, shift)
    if not rigidity["rigid"]:
        raise AssertionError(f"rigidity failure at s={shift}: {rigidity}")
    level4 = sum(
        member(mask, frobenius, value)
        for value in range(4 * shift, 5 * shift)
    )
    level6 = sum(
        member(mask, frobenius, value)
        for value in range(6 * shift, 7 * shift)
    )
    if level6 != shift // 2:
        raise AssertionError(f"level-6 cardinality mismatch at s={shift}")
    return {
        "shift": shift,
        "membership_sha256": expected_sha256,
        "level4_count": level4,
        "level6_count": level6,
        "rigidity_window_end": rigidity["window_end"],
        "rigidity_tail_start": rigidity["tail_start"],
    }


def verify_proof(cnf_path: Path, proof_path: Path) -> dict[str, object]:
    completed = subprocess.run(
        ["wsl.exe", "-e", DRAT_TRIM, wsl_path(cnf_path), wsl_path(proof_path)],
        capture_output=True,
        text=True,
        timeout=1230,
        check=False,
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0 or "s VERIFIED" not in output:
        raise AssertionError(f"fresh DRAT check failed for {proof_path.name}")
    return {
        "returncode": completed.returncode,
        "output_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
    }


def audit_query(
    shift: int,
    level4_count: int | None,
    status: str,
    solve: dict[str, object],
    model_sha256: str | None,
    proof_root: Path,
) -> dict[str, object]:
    cnf, h = build_formula(shift, level4_count)
    if level4_count is None:
        comments = [
            "EXP-006 Route K unconstrained-count existence",
            f"s={shift} F={13 * shift - 1} m={4 * shift}",
        ]
    else:
        comments = [
            "EXP-006 Route K level-4 density ranking",
            f"s={shift} level4_count={level4_count}",
        ]
    rebuilt_hash = serialized_sha256(cnf, comments)
    if rebuilt_hash != solve["cnf_sha256"]:
        raise AssertionError(f"rebuilt CNF mismatch for {solve['stem']}")
    query_root = proof_root / f"s{shift:03d}"
    log_path = query_root / f"{solve['stem']}.cadical.log"
    if sha256(log_path) != solve["solver_log_sha256"]:
        raise AssertionError(f"solver log mismatch for {solve['stem']}")
    record: dict[str, object] = {
        "stem": solve["stem"],
        "status": status,
        "rebuilt_cnf_sha256": rebuilt_hash,
    }
    if status == "SAT":
        true_variables = parse_model(log_path.read_text(encoding="utf-8"))
        if model_sha256 is None:
            raise AssertionError("SAT audit requires a model hash")
        record["semantic"] = semantic_audit(
            mask_from_model(h, true_variables), shift, model_sha256
        )
    elif status == "UNSAT_VERIFIED":
        cnf_path = query_root / f"{solve['stem']}.cnf"
        proof_path = query_root / f"{solve['stem']}.drat"
        if sha256(cnf_path) != solve["cnf_sha256"]:
            raise AssertionError(f"persisted CNF mismatch for {solve['stem']}")
        if sha256(proof_path) != solve["proof_sha256"]:
            raise AssertionError(f"proof mismatch for {solve['stem']}")
        record["fresh_proof_check"] = verify_proof(cnf_path, proof_path)
    else:
        raise AssertionError(f"unexpected query status {status}")
    del cnf
    gc.collect()
    return record


def verify_manifest(manifest: dict[str, object], proof_root: Path) -> dict[str, object]:
    rows: list[str] = []
    listed: set[str] = set()
    total = 0
    for item in manifest["files"]:
        relative = str(item["path"])
        path = proof_root / Path(relative)
        if relative in listed or not path.is_file():
            raise AssertionError(f"invalid external manifest entry {relative}")
        listed.add(relative)
        size = path.stat().st_size
        digest = sha256(path)
        if size != item["bytes"] or digest != item["sha256"]:
            raise AssertionError(f"external manifest mismatch for {relative}")
        total += size
        rows.append(f"{relative}:{size}:{digest}")
    actual = {
        path.relative_to(proof_root).as_posix()
        for path in proof_root.rglob("*")
        if path.is_file()
    }
    if actual != listed:
        raise AssertionError("external manifest file set is not exact")
    aggregate = digest_rows(rows)
    if aggregate != manifest["aggregate_sha256"]:
        raise AssertionError("external manifest aggregate mismatch")
    return {"file_count": len(rows), "total_bytes": total, "aggregate_sha256": aggregate}


def count_order(shift: int) -> list[int]:
    return sorted(
        range(1, shift + 1),
        key=lambda count: (abs(14 * count - 5 * shift), count),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--proof-root", type=Path, required=True)
    args = parser.parse_args()
    results = json.loads(
        (args.artifact_dir / "route-k-results.json").read_text(encoding="utf-8")
    )
    checkpoint = json.loads(
        (args.artifact_dir / "route-k-checkpoint.json").read_text(encoding="utf-8")
    )
    manifest = json.loads(
        (args.artifact_dir / "external-manifest.json").read_text(encoding="utf-8")
    )
    if results["status"] != "COMPLETE" or results["cases"] != checkpoint["cases"]:
        raise AssertionError("results/checkpoint case mismatch")

    query_audits: list[dict[str, object]] = []
    calibration = checkpoint["calibration"]
    calibration_cnf, calibration_h = build_formula(14)
    calibration_comments = [
        "EXP-006 Route K public-seed calibration",
        "s=14 F=181 m=56",
    ]
    if serialized_sha256(calibration_cnf, calibration_comments) != calibration["solve"][
        "cnf_sha256"
    ]:
        raise AssertionError("calibration CNF reconstruction failed")
    calibration_log = args.proof_root / "s014" / "s014-calibration.cadical.log"
    calibration_true = parse_model(calibration_log.read_text(encoding="utf-8"))
    calibration_semantic = semantic_audit(
        mask_from_model(calibration_h, calibration_true),
        14,
        calibration["model"]["membership_sha256"],
    )
    del calibration_cnf
    gc.collect()

    for shift in range(16, 41, 2):
        case = results["cases"][str(shift)]
        existence_status = (
            "SAT" if case["status"] == "SAT_OPTIMAL" else "UNSAT_VERIFIED"
        )
        selected = case.get("selected_model")
        unconstrained = case.get("unconstrained_model")
        query_audits.append(
            audit_query(
                shift,
                None,
                existence_status,
                case["existence"],
                None if unconstrained is None else unconstrained["membership_sha256"],
                args.proof_root,
            )
        )
        for attempt in case["optimization_attempts"]:
            attempt_model_sha = (
                selected["membership_sha256"] if attempt["status"] == "SAT" else None
            )
            query_audits.append(
                audit_query(
                    shift,
                    int(attempt["level4_count"]),
                    attempt["status"],
                    attempt["solve"],
                    attempt_model_sha,
                    args.proof_root,
                )
            )
        if selected is not None:
            prior_counts = [
                int(attempt["level4_count"])
                for attempt in case["optimization_attempts"]
            ]
            order = count_order(shift)
            selected_count = int(selected["level4_count"])
            if prior_counts != order[: len(prior_counts)]:
                raise AssertionError(f"density ranking order mismatch at s={shift}")
            if case["selected_count_source"] == "ranked exact-cardinality query":
                if (
                    not case["optimization_attempts"]
                    or case["optimization_attempts"][-1]["status"] != "SAT"
                    or prior_counts[-1] != selected_count
                ):
                    raise AssertionError(f"ranked selection mismatch at s={shift}")
            elif order[len(prior_counts)] != selected_count:
                raise AssertionError(f"density optimality gap at s={shift}")

    manifest_audit = verify_manifest(manifest, args.proof_root)
    sat_shifts = [20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
    if results["sat_shifts"] != sat_shifts or results["unsat_shifts"] != [16, 18]:
        raise AssertionError("declared Route K classification mismatch")
    audit: dict[str, object] = {
        "status": "PASS",
        "calibration": calibration_semantic,
        "classification": {
            "unsat_shifts": [16, 18],
            "sat_shifts": sat_shifts,
            "route_a_gate_open": True,
        },
        "query_count": len(query_audits),
        "fresh_unsat_proof_checks": sum(
            query["status"] == "UNSAT_VERIFIED" for query in query_audits
        ),
        "sat_model_checks": sum(query["status"] == "SAT" for query in query_audits),
        "external_manifest": manifest_audit,
        "queries": query_audits,
    }
    audit["aggregate_sha256"] = digest_rows(
        [
            f"{query['stem']}:{query['status']}:{query['rebuilt_cnf_sha256']}"
            for query in query_audits
        ]
        + [f"external:{manifest_audit['aggregate_sha256']}"]
    )
    output = args.artifact_dir / "route-k-audit.json"
    output.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
