"""Bounded, headless EXP-003 arithmetic. The hypothesis precedes machine work."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sympy as sp
from flint import ctx

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
ROOT = HERE.parents[4]
sys.path.insert(0, str(PROBLEM / "code"))
from riemann_certificates import ball, bracket, c_value, kernel  # noqa: E402
from riemann_pressure import (  # noqa: E402
    certify_pressure_triangle, digest, exact, frame_coefficients, gain_comparison,
    parameters, pressure_frame_bound, source_identity, verify_pressure_triangle, write_json,
)

DECLARATION = "8ed806d64e5df2b83ab1ad75cb9f17a5633208bc"
THETA, OLD_D, OLD_R = Fraction(3, 4), Fraction(1, 7000), Fraction(21, 4)
OLD = PROBLEM / "experiments/EXP-002-short-interval-stability/artifacts"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def committed_input(path: Path) -> dict:
    relative = path.relative_to(ROOT).as_posix()
    recorded = subprocess.run(["git", "show", f"{DECLARATION}:{relative}"], cwd=ROOT,
                              check=True, capture_output=True).stdout
    if recorded != path.read_bytes():
        raise ValueError(f"Committed input differs: {relative}")
    return {"path": relative, "sha256": sha(path), "source_commit": DECLARATION}


def provenance() -> dict:
    return {"hypothesis": committed_input(HERE / "hypothesis.md"),
            "certificate_code": source_identity(), "runner_sha256": sha(Path(__file__))}


def symbolic_and_index_checks() -> dict:
    k, d, c, r = sp.symbols("k d c r", positive=True)
    difference = k * d / (2 * k + 1 - k * d) - d / (3 - d)
    assert sp.cancel(difference - d * (k - 1) / ((2 * k + 1 - k * d) * (3 - d))) == 0
    assert sp.cancel((c - (2 * k * d / r) / (2 * k + 1)) /
                     (1 - k * d / (2 * k + 1)) -
                     (c + k * d * (c - 2 / r) / (2 * k + 1 - k * d))) == 0
    cases = 0
    for kk in range(1, 9):
        size = 2 * kk + 1
        triples = [range(start, start + 3) for start in range(0, size - 2, 2)]
        pairs = Counter(pair for triple in triples for pair in itertools.combinations(triple, 2))
        assert len(pairs) == 3 * kk and set(pairs.values()) == {1}
        coefficients = Counter(gap for triple in triples for gap in range(triple[0], triple[-1]))
        assert coefficients == Counter(range(size - 1))
        for count in range(41):
            starts = [start for offset in range(size) for start in range(offset, count - size + 1, size)]
            assert sorted(starts) == list(range(max(0, count - size + 1)))
            pressure_counts = Counter(gap for start in starts for gap in range(start, start + size - 1))
            assert max(pressure_counts.values(), default=0) <= size - 1
            cases += 1
    alpha, beta = frame_coefficients(OLD_D, OLD_D / OLD_R, 7000)
    assert alpha == Fraction(1, 14001) and beta == 2 * alpha / OLD_R
    assert alpha / (1 - alpha) == OLD_D / 2
    return {"symbolic_identities": 2, "frame_sizes": [2 * n + 1 for n in range(1, 9)],
            "sequence_lengths": [0, 40], "index_cases": cases,
            "pairs_disjoint": True, "spans_telescope": True,
            "offset_coverage_and_boundary": True, "alpha": str(alpha), "beta": str(beta)}


def stage_a(output: Path) -> dict:
    start = time.monotonic()
    record = provenance()
    record["reused_certificate"] = committed_input(OLD / "triangle-certificate.json")
    checks = symbolic_and_index_checks()
    child = """import json,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from flint import ctx
from riemann_certificates import verify_triangle
ctx.prec=256
print(json.dumps(verify_triangle(json.loads(Path(sys.argv[2]).read_text(encoding='utf-8')))))
"""
    print(json.dumps({"event": "stage-a-replay-start", "budget_seconds": 60}), flush=True)
    replay = subprocess.run([sys.executable, "-c", child, str(PROBLEM / "code"),
                             str(OLD / "triangle-certificate.json")], capture_output=True,
                            text=True, check=True, timeout=max(0.001, 60 - (time.monotonic() - start)))
    audit = json.loads(replay.stdout)
    ctx.prec = 256
    baseline = c_value(THETA)
    improved = pressure_frame_bound(THETA, OLD_D / OLD_R, OLD_D, 7000)
    gain = ball(OLD_D / 2) * (baseline - ball(2 / OLD_R))
    assert gain > 0
    result = {"stage": "A", "arithmetic_status": "verified", "theta": str(THETA),
        "radius": str(OLD_R), "delta": str(OLD_D), "k": 7000, "frame_size": 14001,
        "baseline": bracket(baseline), "improved": bracket(improved), "gain": bracket(gain),
        "distinct": bracket((1 + improved) / 2),
        "gain_ratio_to_exp002": str((3 - OLD_D) / 2), "invariants": checks,
        "replay": audit, "provenance": record,
        "scope": "Arithmetic and incidence evidence; complete proof and source review remain separate gates"}
    if time.monotonic() - start >= 60:
        raise TimeoutError("Stage A combined arithmetic budget exhausted")
    write_json(output / "stage-a-result.json", result)
    write_json(output / "operational.json", {"elapsed_seconds": time.monotonic() - start})
    return result


def smoke(output: Path) -> dict:
    ctx.prec = 160
    spec = (THETA, Fraction(1, 20), Fraction(1, 10))
    checkpoint = output / "construction-checkpoint.json"
    stopped = False
    try:
        certify_pressure_triangle(*spec, checkpoint=checkpoint, max_nodes=10, progress_every=1)
    except TimeoutError:
        stopped = True
    assert stopped
    saved = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert saved["counts"]["nodes"] == 10 and saved["pending"]
    resumed = certify_pressure_triangle(*spec, checkpoint=checkpoint, resume=True)
    fresh = certify_pressure_triangle(*spec)
    assert resumed == fresh
    rejected = False
    try:
        certify_pressure_triangle(THETA, "1/30", "1/10", checkpoint=checkpoint, resume=True)
    except ValueError:
        rejected = True
    assert rejected
    ctx.prec = 256
    replay_checkpoint = output / "replay-checkpoint.json"
    try:
        verify_pressure_triangle(resumed, checkpoint=replay_checkpoint, budget=0)
    except TimeoutError:
        pass
    audit = verify_pressure_triangle(resumed, checkpoint=replay_checkpoint, resume=True)
    result = {"verified": True, "forced_stop_nodes": 10, "resumed_equals_fresh": True,
        "mismatched_parameters_rejected": True, "replay": audit,
        "source_identity": source_identity(),
        "replay_restart_policy": "Checkpoint identity is validated; prior arithmetic is rechecked, never trusted"}
    write_json(output / "smoke-result.json", result)
    return result


def stage_b(output: Path, candidates_path: Path, smoke_path: Path) -> dict:
    smoke_record = json.loads(smoke_path.read_text(encoding="utf-8"))
    if not (smoke_record.get("verified") and smoke_record.get("forced_stop_nodes") == 10
            and smoke_record.get("resumed_equals_fresh")
            and smoke_record.get("mismatched_parameters_rejected")
            and smoke_record.get("source_identity") == source_identity()
            and smoke_record.get("replay", {}).get("verified")):
        raise ValueError("Successful smoke receipt required")
    candidates = json.loads(candidates_path.read_text(encoding="utf-8"))
    proposals = candidates["candidates"]
    if not 1 <= len(proposals) <= 3:
        raise ValueError("Frozen candidate count must be one to three")
    record = provenance()
    record["candidate_list_sha256"] = sha(candidates_path)
    outcomes = []
    success = False
    for index, proposal in enumerate(proposals, 1):
        if success:
            outcomes.append({"candidate": index, "status": "not_run_after_higher_ranked_success"})
            continue
        target = output / f"candidate-{index}"
        target.mkdir()
        p, epsilon = exact(proposal["pressure"]), exact(proposal["epsilon"])
        spec = parameters(THETA, p, epsilon)
        k = int(Fraction(1) // epsilon)
        ctx.prec = 256
        gate = gain_comparison(THETA, p, epsilon, k)
        if not gate > 0:
            outcomes.append({"candidate": index, "status": "rejected_gain_gate", **spec})
            continue
        witness = proposal.get("sample_witness")
        if witness:
            if not isinstance(witness, list) or len(witness) != 2:
                raise ValueError("Witness must contain two exact nonnegative gaps")
            u, v = map(exact, witness)
            if u < 0 or v < 0:
                raise ValueError("Witness gaps must be nonnegative")
            upper = 2 * sum((kernel(THETA, x) ** 2 for x in (u, v, u + v)), ball(0)) + ball(p * (u + v))
            if upper < ball(epsilon):
                outcomes.append({"candidate": index, "status": "refuted_by_exact_witness", **spec,
                                 "witness": witness, "upper": bracket(upper)})
                continue
        start = time.monotonic()
        print(json.dumps({"event": "candidate-start", "candidate": index, **spec}), flush=True)
        try:
            ctx.prec = 160
            certificate = certify_pressure_triangle(THETA, p, epsilon, budget=600,
                checkpoint=target / "construction-checkpoint.json")
            write_json(target / "pressure-certificate.json", certificate)
            remaining = max(0, 600 - (time.monotonic() - start))
            ctx.prec = 256
            audit = verify_pressure_triangle(certificate, budget=remaining,
                checkpoint=target / "replay-checkpoint.json")
            final_gate = gain_comparison(THETA, p, epsilon, k)
            if not final_gate > 0:
                raise AssertionError("Terminal strict gain gate failed")
            improved = pressure_frame_bound(THETA, p, epsilon, k)
            result = {"candidate": index, "status": "arithmetic_verified", **spec,
                "k": k, "frame_size": 2 * k + 1, "baseline": bracket(c_value(THETA)),
                "improved": bracket(improved), "gain": bracket(improved - c_value(THETA)),
                "distinct": bracket((1 + improved) / 2), "strict_gain_gate": bracket(final_gate),
                "audit": audit, "certificate_sha256": digest(certificate), "provenance": record}
            if time.monotonic() - start >= 600:
                raise TimeoutError("Combined construction-and-replay budget exhausted")
            write_json(target / "result.json", result)
            outcomes.append(result)
            success = True
        except (TimeoutError, ValueError, AssertionError) as error:
            result = {"candidate": index, "status": "inconclusive", **spec,
                      "reason": str(error), "provenance": record}
            write_json(target / "result.json", result)
            outcomes.append(result)
        write_json(target / "operational.json", {"elapsed_seconds": time.monotonic() - start,
            "combined_budget_seconds": 600, "budget_extended": False,
            "replay_checkpoint_policy": "Validated restart; all prefix rechecking counts inside remaining budget"})
    result = {"stage": "B", "arithmetic_status": "verified" if success else "not_confirmed",
              "candidate_list_sha256": sha(candidates_path), "outcomes": outcomes,
              "scope": "Finite pressure arithmetic; theorem and novelty verdict require separate proof review"}
    write_json(output / "stage-b-result.json", result)
    if not success:
        raise RuntimeError("Declared Stage B target not confirmed")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["A", "B", "smoke"], required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--candidates", type=Path)
    parser.add_argument("--smoke-receipt", type=Path)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists():
        raise ValueError("A fresh output directory is required")
    if output.is_relative_to(PROBLEM.resolve()) or output.is_relative_to((ROOT / "manuscripts").resolve()):
        raise ValueError("Run outputs must not overwrite canonical research or manuscript inputs")
    output.mkdir(parents=True)
    try:
        if args.stage == "A":
            result = stage_a(output)
        elif args.stage == "smoke":
            result = smoke(output)
        else:
            if args.candidates is None or args.smoke_receipt is None:
                raise ValueError("Stage B requires frozen candidates and a smoke receipt")
            result = stage_b(output, args.candidates, args.smoke_receipt)
        print(json.dumps(result, indent=2), flush=True)
    except Exception as error:
        write_json(output / "failure.json", {"stage": args.stage, "status": "inconclusive",
                                             "reason": str(error)})
        raise


if __name__ == "__main__":
    main()
