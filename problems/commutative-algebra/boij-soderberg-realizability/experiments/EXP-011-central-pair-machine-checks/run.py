"""EXP-011: machine checks of the central-pair theorem in characteristic p dividing an odd e (families T, G, N).

Run from the repository root, with the repository virtual environment:
    python <this file> gates                         G1 (known answers) and G3 (pytest tests/test_bs_exp011.py); exit 1 on a failure
    python <this file> cases [--family=T|G|N] [--only=ID[,ID]] [--workers=N]
                                                     identities, Hilbert function, length (and the Betti table by uhlib: for e <= 9
                                                     in the worker, for e >= 11 as one subprocess per case with a 30-minute limit);
                                                     resumable per case; the cases with e <= 9 first within each family
    python <this file> second [--only=ID[,ID]] [--workers=N]
                                                     Singular (Plural, through WSL) on every case, from the stored polynomials
    python <this file> table                         gates G2, predictions P1 and P2 into results.json, then results-summary.md

The hypothesis is hypothesis.md (frozen).  First instrument: exp011_routine.py over `uhlib`.  Second instrument: Singular 4.3.2
(Plural), exp011_singular.py.  At most 6 worker processes in total; `cases` and `second` stop handing out work after the wall-time
budget (three hours since the first command, counted in results.json).  Singular outputs go to the scratch folder and are copied to
the data root folder of this experiment.  No machine path is written to any artifact.
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

import exp011_cases as C  # noqa: E402
import exp011_routine as R  # noqa: E402
import exp011_singular as Sg  # noqa: E402
import make_summary as MS  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
SCRATCH = Path(os.environ.get("EXP011_SCRATCH", "D:/_Temp/bs-exp011-2026-11-20"))
DATA_DIR = Path(os.environ.get("EXP011_DATA", "E:/_Datos/caos-research/boij-soderberg-realizability/EXP-011"))
LOG = SCRATCH / "run.log"
T0 = time.time()
MAX_WORKERS = 6
BUDGET_SECONDS = 3 * 3600
BETTI_BIG_LIMIT = 1800
SINGULAR_LIMIT = 2400


def log(msg):
    line = "[%8.1fs] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-011", "hypothesis": "hypothesis.md (frozen)", "cases": {}, "gates": {}, "predictions": {},
            "runs": [], "spent_seconds": 0.0}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
    tmp.replace(RESULTS)


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
    out = [s for s in C.specs() if (not only or s["id"] in only) and (not fam or s["family"] == fam)]
    return C.sort_specs(out)


def over_budget(res):
    return res.get("spent_seconds", 0.0) + (time.time() - T0) > BUDGET_SECONDS


def close_run(res, command):
    res["spent_seconds"] = round(res.get("spent_seconds", 0.0) + time.time() - T0, 1)
    res["runs"].append({"command": command, "seconds": round(time.time() - T0, 1)})
    save(res)


# ------------------------------------------------------------------ gates G1 and G3
def gate_g1():
    rows = []

    def case(label, p, e, f, g, expect_pure):
        tab, _, secs = R.betti_uhlib(p, e, f, g)
        rows.append({"case": label, "betti": R.table_rows(tab), "expected_pure": expect_pure,
                     "ok": (tab == R.pure_table(e)) is expect_pure, "seconds": round(secs, 2)})

    for p, expect in ((11, True), (5, False)):
        case("<x^5, y^5> over GF(%d)" % p, p, 5, {(5, 0, 0): 1}, {(0, 5, 0): 1}, expect)
    f, g = R.build_pair(5, 5, {(5, 0): 1}, {(0, 5): 1}, (0, 1), (1, 0))
    case("<x^5 + y z^2, y^5 + x z^2> over GF(5)", 5, 5, f, g, True)
    bad = [r for r in rows if not r["ok"]]
    return {"passed": not bad, "cases": rows, "failing_cases": bad}


def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp011.py", "-q"], cwd=str(ROOT), capture_output=True,
                          text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def cmd_gates():
    res = load()
    log("gates start")
    res["gates"]["G1"] = gate_g1()
    log("G1 %s: %s" % ("PASSED" if res["gates"]["G1"]["passed"] else "FAILED", json.dumps(res["gates"]["G1"]["cases"])))
    res["gates"]["G3"] = gate_g3()
    log("G3 %s: %s" % ("PASSED" if res["gates"]["G3"]["passed"] else "FAILED", json.dumps(res["gates"]["G3"])))
    close_run(res, "gates")
    failed = [k for k in ("G1", "G3") if not res["gates"][k]["passed"]]
    if failed:
        log("GATE FAILED: %s; the run stops here" % ",".join(failed))
        return 1
    return 0


def gates_ok(res):
    return all(res.get("gates", {}).get(k, {}).get("passed") is True for k in ("G1", "G3"))


# ------------------------------------------------------------------ cases
def cmd_betti_one():
    """Internal: the Betti table by uhlib of one case, from its stored polynomials; prints the record as JSON."""
    rec = load()["cases"][opt("id", "")]
    f, g = R.poly_from_list(rec["f"]), R.poly_from_list(rec["g"])
    print(json.dumps(C.betti_record(rec["p"], rec["e"], f, g)))
    return 0


def run_betti_big(cid):
    """The Betti table by uhlib of an e >= 11 case in a subprocess with the 30-minute limit (the child is killed on expiry)."""
    t0 = time.time()
    try:
        proc = subprocess.run([sys.executable, str(HERE / "run.py"), "betti-one", "--id=" + cid], capture_output=True, text=True,
                              timeout=BETTI_BIG_LIMIT)
        if proc.returncode == 0:
            return cid, json.loads(proc.stdout.strip().splitlines()[-1])
        return cid, {"status": "failed: " + proc.stderr.strip()[-300:], "table": None, "pure": None,
                     "seconds": round(time.time() - t0, 1)}
    except subprocess.TimeoutExpired:
        return cid, {"status": "not computed: the table took more than %d s (30-minute rule of the hypothesis)" % BETTI_BIG_LIMIT,
                     "table": None, "pure": None, "seconds": float(BETTI_BIG_LIMIT)}


def cmd_cases():
    res = load()
    if not gates_ok(res):
        log("the gates have not passed: run `gates` first")
        return 1
    todo = [s for s in select() if s["id"] not in res["cases"]]
    log("cases: %d to run (%s), %d workers" % (len(todo), ",".join(s["id"] for s in todo), workers()))
    with ProcessPoolExecutor(max_workers=workers()) as ex:
        futs = {}
        for s in todo:
            if over_budget(res):
                log("budget exhausted: not started: " + s["id"])
                continue
            futs[ex.submit(C.case_record, s)] = s["id"]
        for fu in as_completed(futs):
            rec = fu.result()
            res["cases"][rec["id"]] = rec
            save(res)
            log("%s done in %.1fs: identities %s, Hilbert = h_e %s, length %s, uhlib Betti %s" % (
                rec["id"], rec["seconds"], rec["identities"]["all"], rec["hilbert_equals_h_e"], rec["length"],
                rec["betti_uhlib"]["status"] + (" pure" if rec["betti_uhlib"].get("pure") else "")))
    big = [s["id"] for s in select() if s["e"] > C.BETTI_UHLIB_MAX_E and s["id"] in res["cases"]
           and res["cases"][s["id"]]["finite_length"] and res["cases"][s["id"]]["betti_uhlib"]["status"] == "not attempted"]
    if big:
        log("Betti by uhlib for e >= 11 (30-minute limit each): " + ",".join(big))
        with ThreadPoolExecutor(max_workers=workers()) as ex:
            for cid, brec in ex.map(run_betti_big, big):
                res["cases"][cid]["betti_uhlib"] = brec
                save(res)
                log("%s uhlib Betti: %s (%.1fs)" % (cid, brec["status"], brec["seconds"]))
    close_run(res, "cases " + " ".join(sys.argv[2:]))
    return 0


# ------------------------------------------------------------------ second instrument
def second_task(cid, p, f_list, g_list):
    tab, secs, err = Sg.run_case(cid, p, f_list, g_list, SCRATCH / "singular", timeout=SINGULAR_LIMIT)
    return cid, tab, secs, err


def cmd_second():
    res = load()
    ids = [s["id"] for s in select() if s["id"] in res["cases"]]
    todo = [i for i in ids if res["cases"][i]["betti_singular"]["status"] == "not attempted"]
    todo.sort(key=lambda i: (res["cases"][i]["e"], i))
    log("second: Singular on %d cases (%s), %d workers" % (len(todo), ",".join(todo), workers()))
    SING.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=workers()) as ex:
        futs = []
        for cid in todo:
            if over_budget(res):
                log("budget exhausted: not started: " + cid)
                continue
            r = res["cases"][cid]
            futs.append(ex.submit(second_task, cid, r["p"], r["f"], r["g"]))
        for fu in as_completed(futs):
            cid, tab, secs, err = fu.result()
            rec = res["cases"][cid]
            e = rec["e"]
            rec["betti_singular"] = {"status": "computed" if tab is not None else "not computed", "table": R.table_rows(tab),
                                     "pure": None if tab is None else tab == R.pure_table(e), "seconds": round(secs, 1),
                                     "error": err}
            shutil.copy(SCRATCH / "singular" / (cid + ".sing"), SING / (cid + ".sing"))
            for ext in (".sing", ".out"):
                if (SCRATCH / "singular" / (cid + ext)).exists():
                    shutil.copy(SCRATCH / "singular" / (cid + ext), DATA_DIR / (cid + ext))
            save(res)
            log("%s Singular: %s (%.1fs) %s" % (cid, rec["betti_singular"]["status"], secs, err or ""))
    close_run(res, "second " + " ".join(sys.argv[2:]))
    return 0


# ------------------------------------------------------------------ table: gate G2 and the predictions
def evaluate(res):
    cases = res["cases"]
    g2_rows, g2_bad = [], []
    for cid, r in cases.items():
        u_, s_ = r["betti_uhlib"], r["betti_singular"]
        if u_.get("table") is not None and s_.get("table") is not None:
            ok = u_["table"] == s_["table"]
            g2_rows.append({"case": cid, "equal": ok})
            if not ok:
                g2_bad.append({"case": cid, "uhlib": u_["table"], "singular": s_["table"]})
    missing = [cid for cid, r in cases.items() if r["betti_singular"].get("table") is None]
    res["gates"]["G2"] = {"passed": bool(g2_rows) and not g2_bad and not missing, "compared": len(g2_rows),
                          "failing_cases": g2_bad, "singular_not_computed": missing,
                          "single_instrument_cases": missing}
    tg = [r for r in cases.values() if r["family"] in ("T", "G")]
    p1_fail, p1_open = [], []
    for r in tg:
        tabs = [t for t in (r["betti_uhlib"].get("table"), r["betti_singular"].get("table")) if t is not None]
        pure_all = all(R.rows_to_table(t) == R.pure_table(r["e"]) for t in tabs)
        ok = (r["identities"]["all"] and r["hilbert_equals_h_e"] and r["length_equals_e3"] and pure_all and bool(tabs))
        if not ok:
            p1_fail.append(r["id"])
        if len(tabs) < 2:
            p1_open.append(r["id"])
    n_expected = len(C.T_CASES) + len(C.G_CASES)
    res["predictions"]["P1"] = {"holds": not p1_fail and len(tg) == n_expected, "cases_run": len(tg), "cases_expected": n_expected,
                                "failing_cases": p1_fail, "cases_with_a_single_Betti_instrument": p1_open}
    p2 = {}
    for cid in ("N1", "N2", "N5"):
        r = cases.get(cid)
        if r is None:
            p2[cid] = "not run"
            continue
        tabs = [r["betti_uhlib"].get("table"), r["betti_singular"].get("table")]
        tabs = [t for t in tabs if t is not None]
        p2[cid] = {"not_pure": any(R.rows_to_table(t) != R.pure_table(r["e"]) for t in tabs) if tabs else not r["hilbert_equals_h_e"],
                   "decided_by": "Betti table" if tabs else "Hilbert function"}
    for cid in ("N3", "N4"):
        r = cases.get(cid)
        p2[cid] = "not run" if r is None else {"hilbert_not_pure": not r["hilbert_equals_h_e"]}
    holds = all(isinstance(v, dict) and (v.get("not_pure") if "not_pure" in v else v.get("hilbert_not_pure")) for v in p2.values())
    res["predictions"]["P2"] = {"holds": holds, "per_case": p2}


def cmd_table():
    res = load()
    evaluate(res)
    save(res)
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
    fn = {"gates": cmd_gates, "cases": cmd_cases, "second": cmd_second, "table": cmd_table, "betti-one": cmd_betti_one}.get(cmd)
    if fn is None:
        print(__doc__)
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
