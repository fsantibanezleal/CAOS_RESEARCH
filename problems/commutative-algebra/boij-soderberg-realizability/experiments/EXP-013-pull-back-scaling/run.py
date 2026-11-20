"""EXP-013: machine checks of the pull-back along an endomorphism of U (degrees multiplied by d = 0 or 1 modulo p).

Run from the repository root, with the repository virtual environment:
    python <this file> gates                         G1 (known answers, recomputed) and G3 (pytest tests/test_bs_exp013.py); exit 1 on a failure
    python <this file> cases [--family=S|T|N] [--only=ID[,ID]] [--workers=N]
                                                     the first instrument (uhlib) on M' and phi^* M'; resumable per case;
                                                     S7 only under the 40-minute rule (the Betti table of S5 took less than 40 minutes)
    python <this file> second [--only=ID[,ID]] [--workers=N]
                                                     Singular (Plural, through WSL) on M' and phi^* M' of every stored case
    python <this file> table                         gate G2, predictions P1 and P2 into results.json, then results-summary.md

The hypothesis is hypothesis.md (frozen).  First instrument: exp013_routine.py over `uhlib`.  Second instrument: Singular 4.3.2
(Plural), exp013_singular.py.  At most 6 worker processes per command (the coordinating run keeps the sum at 6); `cases` and `second`
stop handing out work after the wall-time budget (three hours since the first command, `started_at` in results.json).  Every store
writes only its own case and is serialized by a lock file, so commands may run at the same time.  Singular outputs go to the scratch
folder and are copied to the data root folder of this experiment; no machine path is written to any artifact.
"""
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))

import exp013_routine as R  # noqa: E402
import exp013_singular as Sg  # noqa: E402
import make_summary as MS  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
LOCK = ART / "results.lock"
SCRATCH = Path(os.environ.get("EXP013_SCRATCH", "D:/_Temp/bs-exp013-2026-11-21"))
DATA_DIR = Path(os.environ.get("EXP013_DATA", "E:/_Datos/caos-research/boij-soderberg-realizability/EXP-013"))
LOG = SCRATCH / "run.log"
T0 = time.time()
MAX_WORKERS = 6
BUDGET_SECONDS = 3 * 3600
SINGULAR_LIMIT = 2400
S7_RULE_SECONDS = 2400


def log(msg):
    line = "[%8.1fs] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


# ------------------------------------------------------------------ the store (one file, locked read-modify-write)
def _empty():
    return {"experiment": "EXP-013", "hypothesis": "hypothesis.md (frozen)", "started_at": None, "cases": {}, "gates": {},
            "predictions": {}, "runs": [], "notes": []}


def _read():
    return json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else _empty()


def load():
    return _read()


def update(fn):
    """Read-modify-write of results.json under a lock file; fn(res) edits the dict in place."""
    ART.mkdir(exist_ok=True)
    for _ in range(600):
        try:
            fd = os.open(str(LOCK), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            time.sleep(0.2)
    else:
        raise RuntimeError("results lock not released")
    try:
        res = _read()
        fn(res)
        tmp = RESULTS.with_suffix(".tmp")
        tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
        tmp.replace(RESULTS)
    finally:
        os.close(fd)
        os.unlink(str(LOCK))


def start_clock():
    def f(res):
        if res.get("started_at") is None:
            res["started_at"] = time.time()
    update(f)


def over_budget():
    t = load().get("started_at")
    return t is not None and time.time() - t > BUDGET_SECONDS


def close_run(command):
    def f(res):
        res["runs"].append({"command": command, "seconds": round(time.time() - T0, 1)})
    update(f)


def opt(name, default):
    for a in sys.argv[2:]:
        if a.startswith("--%s=" % name):
            return a.split("=", 1)[1]
    return default


def workers():
    return max(1, min(MAX_WORKERS, int(opt("workers", MAX_WORKERS))))


def select():
    only = [s for s in opt("only", "").split(",") if s]
    fam = opt("family", "")
    out = [c for c in R.RUN_ORDER if (not only or c in only) and (not fam or R.case_spec(c)["family"] == fam)]
    return out


# ------------------------------------------------------------------ gates G1 and G3
def pair_is_pure_central(name):
    """Recomputed: the pair (phi(x), phi(y)) of an endomorphism is pure (table (1,2,2,1) on (0,d,3d,4d)) and its commutator
    commutes with x and y."""
    phi = R.endo_phi(name)
    p, d = phi["p"], R.phi_degree(phi)
    comm = R.sub(R.mul(phi["y"], phi["x"], p), R.mul(phi["x"], phi["y"], p), p)
    central = all(R.mul(v, comm, p) == R.mul(comm, v, p) for v in (R.X_, R.Y_))
    rec = R.betti_uhlib(p, [phi["x"], phi["y"]], 4 * d + 8)
    tab = R.rows_to_table(rec["table"])
    return {"pair": name, "degree": d, "central_commutator": central, "table": rec["table"], "length": rec["length"],
            "pure": tab == R.pure_table(d), "ok": central and tab == R.pure_table(d), "seconds": rec["seconds"]}


def gate_g1():
    rows = [pair_is_pure_central(n) for n in R.G1_PAIRS]
    for name in R.G1_PURE_MODULES:
        p, gens = R.MODS[name][0], R.mod_gens(name)
        e = max(R.A.deg(m) for m in gens[0])
        rec = R.betti_uhlib(p, gens, 4 * e + 8)
        rows.append({"module": name, "e": e, "table": rec["table"], "length": rec["length"],
                     "ok": R.rows_to_table(rec["table"]) == R.pure_table(e), "seconds": rec["seconds"]})
    for name in R.G1_LENGTH_3:
        rec = R.betti_uhlib(R.MODS[name][0], R.mod_gens(name), 20)
        rows.append({"module": name, "table": rec["table"], "length": rec["length"], "ok": rec["length"] == 3,
                     "seconds": rec["seconds"]})
    bad = [r for r in rows if not r["ok"]]
    return {"passed": not bad, "cases": rows, "failing_cases": bad}


def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp013.py", "-q"], cwd=str(ROOT), capture_output=True,
                          text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def cmd_gates():
    start_clock()
    log("gates start")
    g1 = gate_g1()
    log("G1 %s: %s" % ("PASSED" if g1["passed"] else "FAILED", json.dumps(g1["cases"])))
    g3 = gate_g3()
    log("G3 %s: %s" % ("PASSED" if g3["passed"] else "FAILED", json.dumps(g3)))

    def f(res):
        res["gates"]["G1"], res["gates"]["G3"] = g1, g3
    update(f)
    close_run("gates")
    if not (g1["passed"] and g3["passed"]):
        log("GATE FAILED; the run stops here")
        return 1
    return 0


def gates_ok(res):
    return all(res.get("gates", {}).get(k, {}).get("passed") is True for k in ("G1", "G3"))


# ------------------------------------------------------------------ cases
def s7_allowed(res):
    """The 40-minute rule: S7 runs only if one Betti table (those of S5, the next smaller case) took less than 40 minutes."""
    s5 = res["cases"].get("S5")
    if s5 is None:
        return False, "S5 not run, so no time to apply the rule to"
    t = s5["uhlib_phi"]["seconds"]
    if s5["uhlib_phi"].get("table") is None:
        return False, "the Betti table of S5 by uhlib was not obtained (%s)" % s5["uhlib_phi"]["status"]
    return t < S7_RULE_SECONDS, "Betti table of phi^*M' of S5 by uhlib took %.0f s (rule: less than %d s)" % (t, S7_RULE_SECONDS)


def cmd_cases():
    start_clock()
    res = load()
    if not gates_ok(res):
        log("the gates have not passed: run `gates` first")
        return 1
    todo = [c for c in select() if c not in res["cases"]]
    if "S7" in todo:
        ok, why = s7_allowed(res)
        if not ok:
            log("S7 not run: " + why)

            def f(r):
                r["notes"].append({"case": "S7", "note": "not run under the 40-minute rule: " + why})
            update(f)
            todo.remove("S7")
    log("cases: %d to run (%s), %d workers" % (len(todo), ",".join(todo), workers()))
    with ProcessPoolExecutor(max_workers=workers()) as ex:
        futs = {}
        for c in todo:
            if over_budget():
                log("budget exhausted: not started: " + c)
                continue
            futs[ex.submit(R.case_record, c)] = c
        for fu in as_completed(futs):
            rec = fu.result()

            def f(r, rec=rec):
                r["cases"][rec["id"]] = rec
            update(f)
            log("%s done in %.1fs: uhlib base %s (%.1fs), phi %s (%.1fs); comparison %s" % (
                rec["id"], rec["seconds"], rec["uhlib_base"]["status"], rec["uhlib_base"]["seconds"], rec["uhlib_phi"]["status"],
                rec["uhlib_phi"]["seconds"], json.dumps(rec["compare_uhlib"])))
    close_run("cases " + " ".join(sys.argv[2:]))
    return 0


# ------------------------------------------------------------------ second instrument
def second_task(cid, which, p, gens):
    name = "%s_%s" % (cid, which)
    tab, length, secs, err = Sg.run_case(name, p, gens, SCRATCH / "singular", timeout=SINGULAR_LIMIT)
    return cid, which, name, tab, length, secs, err


def cmd_second():
    start_clock()
    res = load()
    ids = [c for c in select() if c in res["cases"]]
    jobs = []
    for cid in ids:
        r = res["cases"][cid]
        for which, key in (("base", "gens_base"), ("phi", "gens_phi")):
            if r["singular_" + which].get("status") == "not attempted":
                jobs.append((cid, which, r["p"], r[key]))
    jobs.sort(key=lambda j: (j[1] == "phi", len(json.dumps(j[3])), j[0]))
    log("second: Singular on %d modules (%s), %d workers" % (len(jobs), ",".join("%s_%s" % (j[0], j[1]) for j in jobs), workers()))
    SING.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=workers()) as ex:
        futs = []
        for j in jobs:
            if over_budget():
                log("budget exhausted: not started: %s_%s" % (j[0], j[1]))
                continue
            futs.append(ex.submit(second_task, *j))
        for fu in as_completed(futs):
            cid, which, name, tab, length, secs, err = fu.result()
            rec = {"status": "computed" if tab is not None else "not computed", "table": R.table_rows(tab), "length": length,
                   "seconds": round(secs, 1), "error": err}
            for ext in (".sing", ".out"):
                src = SCRATCH / "singular" / (name + ext)
                if src.exists():
                    shutil.copy(src, DATA_DIR / (name + ext))
            shutil.copy(SCRATCH / "singular" / (name + ".sing"), SING / (name + ".sing"))

            def f(r, cid=cid, which=which, rec=rec):
                c = r["cases"][cid]
                c["singular_" + which] = rec
                tb = R.rows_to_table(c["singular_base"].get("table"))
                tp = R.rows_to_table(c["singular_phi"].get("table"))
                if tb is not None and tp is not None:
                    c["compare_singular"] = R.compare(tp, c["singular_phi"]["length"], tb, c["singular_base"]["length"], c["d"])
            update(f)
            log("%s Singular: %s (%.1fs) length %s %s" % (name, rec["status"], secs, length, err or ""))
    close_run("second " + " ".join(sys.argv[2:]))
    return 0


# ------------------------------------------------------------------ table: gate G2 and the predictions
def base_degree(r):
    return max(R.A.deg(tuple(m)) for m, _ in r["gens_base"][0])


def evaluate(res):
    cases = res["cases"]
    st = [r for r in cases.values() if r["family"] in ("S", "T")]
    g2_rows, g2_bad, single = [], [], []
    for r in st:
        for which in ("base", "phi"):
            u_, s_ = r["uhlib_" + which], r["singular_" + which]
            if u_.get("table") is not None and s_.get("table") is not None:
                ok = u_["table"] == s_["table"] and u_["length"] == s_.get("length")
                g2_rows.append({"case": r["id"], "module": which, "equal": ok})
                if not ok:
                    g2_bad.append({"case": r["id"], "module": which, "uhlib": u_["table"], "singular": s_["table"],
                                   "uhlib_length": u_["length"], "singular_length": s_.get("length")})
            else:
                single.append("%s_%s" % (r["id"], which))
    expected = [c for c in R.case_ids() if R.case_spec(c)["family"] in ("S", "T")]
    missing_cases = [c for c in expected if c not in cases]
    res["gates"]["G2"] = {"passed": bool(g2_rows) and not g2_bad and not single and not missing_cases, "compared": len(g2_rows),
                          "failing_cases": g2_bad, "modules_without_two_instruments": single, "cases_not_run": missing_cases}
    p1_fail, p1_open, p1_lengths = [], [], {}
    for r in st:
        d = r["d"]
        comps = [r["compare_uhlib"], r.get("compare_singular")]
        full = [c for c in comps if c is not None]
        ok = bool(full) and all(c["table_is_scaled_table"] is True and c["length_is_d3_times"] is True for c in full)
        if r["family"] == "S":
            p1_lengths[r["id"]] = {"uhlib": r["uhlib_phi"].get("length"), "singular": r["singular_phi"].get("length"),
                                   "expected": r["expected_length_phi"]}
            ok = ok and r["uhlib_phi"].get("length") == r["expected_length_phi"]
            tp = R.rows_to_table(r["uhlib_phi"].get("table"))
            ok = ok and tp == R.pure_table(d * base_degree(r))
        if not ok:
            p1_fail.append(r["id"])
        if r.get("compare_singular") is None or r["compare_uhlib"]["table_is_scaled_table"] is None:
            p1_open.append(r["id"])
    res["predictions"]["P1"] = {"holds": not p1_fail and not missing_cases and not p1_open, "cases_run": len(st),
                               "cases_expected": len(expected), "cases_not_run": missing_cases, "failing_cases": p1_fail,
                               "cases_without_both_instruments": p1_open, "lengths_S": p1_lengths}
    out = {}
    for cid in ("N1", "N2"):
        r = cases.get(cid)
        if r is None:
            out[cid] = "not run"
            continue
        e = base_degree(r) * r["d"]
        pure = R.pure_table(e)
        tabs = {k: r[k].get("table") for k in ("uhlib_phi", "singular_phi") if r[k].get("table") is not None}
        out[cid] = {"pair_degree": e, "tables": tabs, "pure": {k: R.rows_to_table(t) == pure for k, t in tabs.items()},
                    "uhlib_status": r["uhlib_phi"]["status"], "uhlib_dims": r["uhlib_phi"].get("dims"),
                    "singular_length": r["singular_phi"].get("length"), "compare_uhlib": r["compare_uhlib"],
                    "compare_singular": r.get("compare_singular")}
    n1 = out.get("N1")
    decided = isinstance(n1, dict) and bool(n1["pure"])
    res["predictions"]["P2"] = {"holds": bool(decided and not any(n1["pure"].values())), "N1_decided_by_a_table": decided,
                                "per_case": out, "note": "P2 concerns N1 only; N2 has no prediction"}


def cmd_table():
    res = load()
    box = {}

    def f(r):
        evaluate(r)
        box["res"] = r
    update(f)
    res = box["res"]
    MS.write_summary(res)
    print(MS.table_text(res))
    for k in ("G1", "G2", "G3"):
        gv = res["gates"].get(k)
        print("%s: %s" % (k, "not run" if gv is None else ("PASSED" if gv["passed"] else "FAILED / incomplete")))
    for k in ("P1", "P2"):
        print("%s: %s" % (k, json.dumps(res["predictions"][k])))
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"gates": cmd_gates, "cases": cmd_cases, "second": cmd_second, "table": cmd_table}.get(cmd)
    if fn is None:
        print(__doc__)
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
