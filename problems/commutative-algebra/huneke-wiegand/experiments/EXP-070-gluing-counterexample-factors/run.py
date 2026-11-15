"""EXP-070: the EXP-068 gluing law on factors that are counterexamples.

Run from the repository root:
  .venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-070-gluing-counterexample-factors/run.py
CPU only, headless, exact integer arithmetic, no random choice (no seed). At most 10 worker processes (the jobs
are subprocesses of this driver, each killed by its recorded PID at its limit). Exit 0: every completed case
passes P1 to P4, the controls pass and B1 to B3 (36 cases) completed; exit 1: a prediction or control failed;
exit 2: nothing failed but a required case did not complete; exit 3: a premise input is missing; exit 4: a factor
status differs from its premise (the run stops). Internal mode: --job SPEC.json --out RESULT.json.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ARTIFACTS = HERE / "artifacts"
TEMP = Path(os.environ.get("HW_EXP070_TEMP", "D:/_Temp/hw-exp069-exp070-2026-11-14/exp070"))
MAX_WORKERS = 10
TOTAL_LIMIT_SECONDS = 3 * 3600
B4_START_LIMIT_SECONDS = 2 * 3600
LOG: list[str] = []


def log(message: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {message}"
    LOG.append(line)
    print(line, flush=True)


# ---------------------------------------------------------------------------------------------- job side
def job_main(spec_path: Path, out_path: Path) -> int:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    kind = spec["kind"]
    if kind == "audit":
        import auditor
        result = auditor.audit_case(spec["case"])
    else:
        import gluing_cases as gc
        if kind == "factor":
            result = gc.factor_job(tuple(spec["gens"]), tuple(spec["ideal"]), spec["y"])
        elif kind == "case":
            result = gc.case_job(spec["case"])
        elif kind == "c1":
            result = gc.control_c1(spec["base"])
        elif kind == "c2":
            result = gc.control_c2()
        else:
            raise ValueError(kind)
    out_path.write_text(json.dumps(result), encoding="utf-8")
    return 0


# ------------------------------------------------------------------------------------------ driver side
class Pool:
    """At most MAX_WORKERS subprocess jobs; each job is killed through its own Popen handle at its limit."""

    def __init__(self, deadline: float) -> None:
        self.deadline = deadline
        self.counter = 0

    def run(self, jobs: list[tuple[str, dict, float]]) -> dict[str, dict]:
        pending = list(jobs)
        running: dict[str, tuple[subprocess.Popen, float, float, Path, Path]] = {}
        results: dict[str, dict] = {}
        TEMP.mkdir(parents=True, exist_ok=True)
        while pending or running:
            while pending and len(running) < MAX_WORKERS and time.time() < self.deadline:
                job_id, spec, limit = pending.pop(0)
                self.counter += 1
                spec_path, out_path = TEMP / f"job{self.counter}.spec.json", TEMP / f"job{self.counter}.out.json"
                spec_path.write_text(json.dumps(spec), encoding="utf-8")
                out_path.unlink(missing_ok=True)
                process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--job", str(spec_path),
                                            "--out", str(out_path)], stdout=subprocess.DEVNULL,
                                           stderr=subprocess.PIPE, text=True)
                running[job_id] = (process, time.time(), limit, out_path, spec_path)
            if time.time() >= self.deadline and pending:
                for job_id, _spec, _limit in pending:
                    results[job_id] = {"status": "not completed", "reason": "total wall-time limit reached"}
                pending = []
            for job_id in list(running):
                process, started, limit, out_path, spec_path = running[job_id]
                code = process.poll()
                age = time.time() - started
                if code is None and (age > limit or time.time() > self.deadline):
                    process.kill()
                    process.wait()
                    results[job_id] = {"status": "not completed", "reason": f"killed after {age:.0f}s (limit {limit:.0f}s)"}
                elif code is not None:
                    if code == 0 and out_path.exists():
                        record = json.loads(out_path.read_text(encoding="utf-8"))
                        record["status"] = "completed"
                        record["wall_seconds"] = round(age, 1)
                        results[job_id] = record
                    else:
                        results[job_id] = {"status": "error", "reason": (process.stderr.read() or "")[-2000:]}
                else:
                    continue
                del running[job_id]
                out_path.unlink(missing_ok=True)
                spec_path.unlink(missing_ok=True)
            time.sleep(0.5)
        return results


def factor_key(gens, ideal, y) -> str:
    return f"{min(gens)}-{len(gens)}-{max(gens)}|{tuple(ideal)}|{y}"


def run_group(pool: Pool, gc, bases: list[str], started: float) -> tuple[list[dict], dict, bool]:
    """Factor jobs, then producer and auditor jobs of every case of the given bases."""
    plan = []
    for base in bases:
        gens_b, ideal_b = tuple(gc.BASES[base]["gens"]), tuple(gc.BASES[base]["ideal"])
        for partner, gens_s in gc.PARTNERS.items():
            a1, a2 = gc.gluing_parameters(gens_b, gens_s)
            for ideal_s in gc.PARTNER_IDEALS:
                plan.append((base, partner, ideal_s, a1, a2))
    factor_jobs: dict[str, tuple[str, dict, float]] = {}
    for base, partner, ideal_s, a1, a2 in plan:
        gens_b, ideal_b = tuple(gc.BASES[base]["gens"]), tuple(gc.BASES[base]["ideal"])
        gens_s = gc.PARTNERS[partner]
        for gens, ideal, y in ((gens_b, ideal_b, a2), (gens_s, ideal_s, a1)):
            key = factor_key(gens, ideal, y)
            factor_jobs.setdefault(key, (key, {"kind": "factor", "gens": list(gens), "ideal": list(ideal), "y": y},
                                         gc.PRODUCER_LIMIT_SECONDS))
    # the largest windows first, so the pool is busy with the long jobs from the start
    ordered = sorted(factor_jobs.values(), key=lambda job: -max(job[1]["gens"]))
    log(f"factor jobs for {bases}: {len(ordered)}")
    factors = pool.run(ordered)
    done_all = True
    case_jobs: list[tuple[str, dict, float]] = []
    specs = {}
    for base, partner, ideal_s, a1, a2 in plan:
        gens_b, ideal_b = tuple(gc.BASES[base]["gens"]), tuple(gc.BASES[base]["ideal"])
        gens_s = gc.PARTNERS[partner]
        fb, fs = factors[factor_key(gens_b, ideal_b, a2)], factors[factor_key(gens_s, ideal_s, a1)]
        if fb["status"] != "completed" or fs["status"] != "completed":
            done_all = False
            continue
        spec = gc.build_spec(base, partner, ideal_s, {"b": fb, "s": fs})
        specs[spec["label"]] = spec
        case_jobs.append((f"case|{spec['label']}", {"kind": "case", "case": spec}, gc.PRODUCER_LIMIT_SECONDS))
        case_jobs.append((f"audit|{spec['label']}", {"kind": "audit", "case": spec}, gc.AUDITOR_LIMIT_SECONDS))
    log(f"case jobs for {bases}: {len(case_jobs) // 2} cases, producer and auditor")
    results = pool.run(case_jobs)
    cases = []
    for label, spec in specs.items():
        produced, audited = results[f"case|{label}"], results[f"audit|{label}"]
        record = {"label": label, "spec_factors": {"b": spec["factor_b"], "s": spec["factor_s"]},
                  "producer_status": produced["status"], "audit_status": audited["status"]}
        if produced["status"] == "completed":
            record["producer"] = produced
        else:
            done_all = False
            record["producer_reason"] = produced.get("reason")
        if audited["status"] == "completed":
            record["audit"] = audited
        else:
            record["audit_reason"] = audited.get("reason")
        if produced["status"] == "completed" and audited["status"] == "completed":
            record["audit_agrees"] = (audited["torsion"] == produced["torsion_direct"]
                                      and audited["hw"] == produced["hw"]
                                      and audited["mu"] == produced["mu"][2]
                                      and audited["frobenius"] == produced["frobenius_measured"])
        else:
            record["audit_agrees"] = None
        cases.append(record)
        if produced["status"] == "completed":
            p = produced
            log(f"{label}: law={p['torsion_law']} direct={p['torsion_direct']} audit="
                f"{audited.get('torsion', 'not completed')} hw={p['hw']} mu={p['mu']} hilbert={p['hilbert_identity']} "
                f"pairs={p['pairs_scanned']} window={p['window']} t={p['seconds']}s")
        else:
            log(f"{label}: producer {produced['status']} ({produced.get('reason')})")
    return cases, factors, done_all


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.job:
        return job_main(Path(args.job), Path(args.out))

    started = time.time()
    ARTIFACTS.mkdir(exist_ok=True)
    try:
        import gluing_cases as gc
        import auditor
        auditor.load_audit()
    except FileNotFoundError as error:
        print(f"MISSING INPUT: {error}", file=sys.stderr)
        return 3
    pool = Pool(deadline=started + TOTAL_LIMIT_SECONDS)

    # premise check and controls first (cheap), jobs in the pool
    control_results = pool.run([("c1|B1", {"kind": "c1", "base": "B1"}, gc.PRODUCER_LIMIT_SECONDS),
                                ("c1|B2", {"kind": "c1", "base": "B2"}, gc.PRODUCER_LIMIT_SECONDS),
                                ("c2", {"kind": "c2"}, gc.PRODUCER_LIMIT_SECONDS)])
    log(f"controls: {control_results}")

    cases, factors, complete = run_group(pool, gc, ["B1", "B2", "B3"], started)
    premise = {}
    for case in cases:
        if "producer" not in case:
            continue
        base = case["label"].split(" ")[0]
        fb = case["spec_factors"]["b"]
        premise[base] = {"hw": fb["hw"], "length": fb["length"], "frobenius": fb["frobenius"],
                         "multiplicity": fb["multiplicity"]}
    bad = [b for b, v in premise.items()
           if (gc.BASES[b]["role"] == "counterexample" and (v["hw"] is not False or v["length"] != 0))
           or (gc.BASES[b]["role"] != "counterexample" and (v["hw"] is not True or v["length"] == 0))
           or v["frobenius"] != gc.FROBENIUS_DECLARED[b] or v["multiplicity"] != gc.MULTIPLICITY_DECLARED[b]]
    if bad:
        log(f"PREMISE DIFFERS for {bad}: {premise}")
        (ARTIFACTS / "run-log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
        return 4
    log(f"premises recomputed: {premise}")

    b4_run, b4_reason = False, None
    elapsed = time.time() - started
    if complete and elapsed < B4_START_LIMIT_SECONDS:
        b4_cases, b4_factors, b4_complete = run_group(pool, gc, ["B4"], started)
        cases += b4_cases
        factors.update(b4_factors)
        b4_run = True
        if not b4_complete:
            b4_reason = "some B4 jobs did not complete"
    else:
        b4_reason = f"B1 to B3 not complete after {elapsed:.0f} s (limit {B4_START_LIMIT_SECONDS} s)"
        log(f"B4 skipped: {b4_reason}")

    done = [c for c in cases if "producer" in c]
    required = [c for c in cases if c["label"].split(" ")[0] in ("B1", "B2", "B3")]
    required_done = [c for c in required if "producer" in c]
    p1 = all(c["producer"]["p1"] for c in done)
    p2 = all(c["producer"]["p2"] and c["producer"]["p2_special_rule"] is not False for c in done)
    audited_cases = [c for c in done if c["audit_agrees"] is not None]
    p3 = all(c["audit_agrees"] for c in audited_cases)
    p4 = all(c["producer"]["p4"] for c in done)
    frobenius_ok = all(c["producer"]["frobenius_matches"] for c in done)
    c1 = [control_results["c1|B1"], control_results["c1|B2"]]
    c1_ok = all(r.get("status") == "completed" and r.get("broken") is True for r in c1)
    c2 = control_results["c2"]
    c2_ok = (c2.get("status") == "completed" and c2["true_ideal_is_extension"] is True
             and c2["perturbed_is_extension"] is False)
    ce_cases = [c for c in done if c["producer"]["factor_hw"][0] is False]
    ce_principal = [c for c in ce_cases if c["producer"]["factor_hw"][1] is None]
    summary = {
        "P1_torsion_length_law": p1, "P2_characterization": p2, "P3_independent_route_agrees": p3,
        "P4_hilbert_identity": p4, "frobenius_formula_confirmed": frobenius_ok,
        "C1_not_a_gluing_breaks": c1_ok, "C2_not_an_extension": c2_ok,
        "cases_completed_by_producer": len(done), "cases_required": len(required),
        "required_cases_completed": len(required_done),
        "cases_audited": len(audited_cases),
        "cases_audit_not_completed": [c["label"] for c in done if c["audit_agrees"] is None],
        "cases_not_completed": [c["label"] for c in cases if "producer" not in c],
        "cases_with_counterexample_factor": len(ce_cases),
        "counterexample_factor_with_principal_partner_ideal": len(ce_principal),
        "extension_is_itself_counterexample": sum(1 for c in ce_principal if c["producer"]["hw"] is False),
        "cases_with_nonzero_torsion": sum(1 for c in done if c["producer"]["torsion_direct"] > 0),
        "b4_run": b4_run, "b4_reason": b4_reason, "premises": premise,
        "max_workers": MAX_WORKERS, "wall_seconds": round(time.time() - started, 1),
    }
    (ARTIFACTS / "results.json").write_text(json.dumps({"summary": summary, "cases": cases, "controls":
                                                         {"c1": c1, "c2": c2}, "factors": factors}, indent=1) + "\n",
                                            encoding="utf-8", newline="\n")
    log(f"done: {json.dumps({k: v for k, v in summary.items() if k != 'premises'})}")
    (ARTIFACTS / "run-log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8", newline="\n")
    if not (p1 and p2 and p3 and p4 and frobenius_ok and c1_ok and c2_ok):
        return 1
    if len(required_done) != len(required):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
