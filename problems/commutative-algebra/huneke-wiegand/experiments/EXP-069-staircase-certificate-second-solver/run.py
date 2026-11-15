"""EXP-069: the 16 Presburger obligations of EXP-026 decided by a second solver (cvc5).

Run from the repository root:
  .venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-069-staircase-certificate-second-solver/run.py
CPU only, headless, one process at a time (every leaf and control in a fresh subprocess, because the fresh
variable names of the query depend on process state). Exits 0 on PASS (P1 to P4), 1 otherwise, 3 when an
input is missing or changed. Solver times are the only nondeterminism.
Internal modes (used by the driver and the tests): --leaf LABEL, --control C1..C4, --rebuild-only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import second_solver as ss  # noqa: E402
from exact_eval import Unevaluable, evaluate_assertions  # noqa: E402

ARTIFACTS = HERE / "artifacts"
LOG: list[str] = []


def log(message: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {message}"
    LOG.append(line)
    print(line, flush=True)


def stored_digests() -> dict[str, dict]:
    if not ss.STORED_PATH.exists():
        raise FileNotFoundError(f"EXP-026 artifact missing: {ss.STORED_PATH}")
    stored = json.loads(ss.STORED_PATH.read_text(encoding="utf-8"))
    return {leaf["label"]: leaf for leaf in stored["leaves"]}


def child(args: argparse.Namespace) -> int:
    """Build, export and decide one obligation or control in this fresh process."""
    control = args.control
    label = ss.CONTROLS[control][0] if control else args.leaf
    solver = ss.build_obligation(label, control)
    # EXP-026 hashes solver.sexpr() AFTER solver.check() (the check renames the let-bound subterms of the
    # printed text for some leaves), so the identity of a query is the digest after the same native check.
    sha_before_check = ss.sha256_text(solver.sexpr())
    smt2_before_check = solver.to_smt2()
    native = None
    if control is None:
        native = ss.z3_native_check(solver, args.native_timeout_ms)
    query_sha = ss.sha256_text(solver.sexpr())
    smt2 = solver.to_smt2()
    record: dict = {"label": label, "control": control, "query_sha256": query_sha,
                    "query_sha256_before_check": sha_before_check, "z3_native": native,
                    "smt2_sha256": ss.sha256_text(smt2), "smt2_bytes": len(smt2),
                    "smt2_before_check_sha256": ss.sha256_text(smt2_before_check)}
    if control is None:
        stored = stored_digests()[label]
        record["stored_sha256"] = stored["query_sha256"]
        record["digest_match"] = stored["query_sha256"] == query_sha
        record["z3_original_seconds"] = stored["elapsed_seconds"]
    if args.smt2_dir:
        directory = Path(args.smt2_dir)
        directory.mkdir(parents=True, exist_ok=True)
        name = f"{control}-{label}" if control else label
        (directory / f"{name}.smt2").write_text(smt2, encoding="utf-8", newline="\n")
        record["smt2_file"] = f"artifacts/smt2/{name}.smt2"
    if not args.rebuild_only:
        record["cvc5"] = ss.cvc5_decide(smt2, args.tlimit_ms)
        if smt2_before_check != smt2:
            record["cvc5_text_before_check"] = ss.cvc5_decide(smt2_before_check, args.tlimit_ms)
        record["z3"] = ss.z3_decide(smt2, args.tlimit_ms)
        if control:
            model = record["cvc5"].get("model")
            if model is None:
                record["evaluator"] = {"verdict": None, "note": "cvc5 returned no model"}
            else:
                started = time.perf_counter()
                try:
                    verdict = evaluate_assertions(smt2, model)
                    record["evaluator"] = {"verdict": verdict, "seconds": time.perf_counter() - started}
                    # adversarial check of the evaluator: the same model must FAIL the unperturbed obligation
                    original = ss.build_obligation(label).to_smt2()
                    record["evaluator"]["model_on_unperturbed_obligation"] = evaluate_assertions(original, model)
                except Unevaluable as error:
                    record["evaluator"] = {"verdict": None, "note": f"unevaluable: {error}"}
    print("RECORD_JSON " + json.dumps(record, sort_keys=True), flush=True)
    return 0


def run_child(extra: list[str], tlimit_ms: int) -> dict:
    command = [sys.executable, str(Path(__file__).resolve()), *extra, "--tlimit-ms", str(tlimit_ms),
               "--smt2-dir", str(ARTIFACTS / "smt2")]
    done = subprocess.run(command, capture_output=True, text=True, timeout=2 * tlimit_ms / 1000 + 300)
    if done.returncode != 0:
        raise RuntimeError(f"{extra}: child failed\n{done.stdout}\n{done.stderr}")
    line = next(x for x in done.stdout.splitlines() if x.startswith("RECORD_JSON "))
    return json.loads(line.removeprefix("RECORD_JSON "))


def driver(args: argparse.Namespace) -> int:
    ARTIFACTS.mkdir(exist_ok=True)
    started = time.perf_counter()
    try:
        stored = stored_digests()
        module = ss.load_exp026()
    except FileNotFoundError as error:
        print(f"MISSING INPUT: {error}", file=sys.stderr)
        return 3
    labels = list(module.LEAF_LABELS)
    if set(labels) != set(stored):
        print("MISSING INPUT: EXP-026 leaf labels differ from the stored artifact", file=sys.stderr)
        return 3
    import z3

    leaves = []
    for label in labels:
        record = run_child(["--leaf", label], args.tlimit_ms)
        leaves.append(record)
        log(f"{label}: native_z3={record['z3_native']['result']} digest_match={record['digest_match']} "
            f"cvc5={record['cvc5']['result']} ({record['cvc5']['seconds']:.2f}s) "
            f"z3_roundtrip={record['z3']['result']} ({record['z3']['seconds']:.2f}s)")
    controls = []
    for name in ss.CONTROLS:
        record = run_child(["--control", name], args.tlimit_ms)
        record["perturbation"] = ss.CONTROLS[name][1]
        controls.append(record)
        log(f"{name} ({record['label']}): cvc5={record['cvc5']['result']} z3={record['z3']['result']} "
            f"evaluator={record['evaluator']} model={record['cvc5'].get('model')}")

    p1 = all(r["digest_match"] for r in leaves)
    p2 = all(r["cvc5"]["result"] == "unsat" and r.get("cvc5_text_before_check", {}).get("result", "unsat") == "unsat"
             for r in leaves)
    p3 = all(r["z3"]["result"] == "unsat" for r in leaves)
    p4 = all(r["cvc5"]["result"] == "sat" and r["z3"]["result"] == "sat"
             and r["evaluator"]["verdict"] is True
             and r["evaluator"]["model_on_unperturbed_obligation"] is False for r in controls)
    summary = {
        "P1_same_obligations": p1, "P2_cvc5_unsat_on_all_16": p2, "P3_z3_roundtrip_unsat_on_all_16": p3,
        "P4_controls_sat_and_exactly_evaluated": p4,
        "leaves": len(leaves), "cvc5_unsat": sum(r["cvc5"]["result"] == "unsat" for r in leaves),
        "cvc5_unknown": [r["label"] for r in leaves if r["cvc5"]["result"] == "unknown"],
        "cvc5_sat": [r["label"] for r in leaves if r["cvc5"]["result"] == "sat"],
        "z3_unsat": sum(r["z3"]["result"] == "unsat" for r in leaves),
        "cvc5_total_seconds": sum(r["cvc5"]["seconds"] for r in leaves),
        "z3_roundtrip_total_seconds": sum(r["z3"]["seconds"] for r in leaves),
        "solvers": {"z3": z3.get_version_string(), "cvc5": ss.cvc5_version(), "cvc5_logic": "LIA",
                    "tlimit_ms_per_leaf": args.tlimit_ms},
        "wall_seconds": time.perf_counter() - started,
    }
    (ARTIFACTS / "results.json").write_text(json.dumps({"summary": summary, "leaves": leaves, "controls": controls},
                                                       indent=1) + "\n", encoding="utf-8", newline="\n")
    log(f"P1={p1} P2={p2} P3={p3} P4={p4} in {summary['wall_seconds']:.1f}s")
    (ARTIFACTS / "run-log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8", newline="\n")
    return 0 if (p1 and p2 and p3 and p4) else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--leaf", choices=None)
    parser.add_argument("--control", choices=sorted(ss.CONTROLS))
    parser.add_argument("--rebuild-only", action="store_true")
    parser.add_argument("--tlimit-ms", type=int, default=600000)
    parser.add_argument("--native-timeout-ms", type=int, default=120000)
    parser.add_argument("--smt2-dir")
    args = parser.parse_args()
    if args.leaf or args.control:
        return child(args)
    return driver(args)


if __name__ == "__main__":
    raise SystemExit(main())
