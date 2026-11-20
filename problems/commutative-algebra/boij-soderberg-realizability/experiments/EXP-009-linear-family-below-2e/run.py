"""EXP-009: the linear family L_e(a, b, c, d) in odd characteristic below 2e, e = 4 to 7.

Run from the repository root, with the repository virtual environment:
    python <this file> gates                   G1 (known answers) and G3 (pytest); exit 1 on a failure
    python <this file> cases [--only=e,p[+e,p]] [--fam=X|Y] [--workers=N] [--budget-seconds=N]
                                               resumable; family X (all p^4 members) for the five control pairs, then the fifteen pairs
                                               with p < 2e, then family Y (GF(p^2) sample) where X found no pure member
    python <this file> second [--workers=N]    G2: Singular (Plural, through WSL) on the first five pure members of every pair
    python <this file> table                   totals, gates and predictions into results.json, then results-summary.md

The hypothesis is hypothesis.md (frozen).  First instrument: exp009_routine.py over EXP-006's routine and `uhlib`.  Second instrument:
Singular 4.3.2 (Plural), exp009_singular.py (the generator of EXP-005).  No machine path is written to any artifact.  At most 8
worker processes; `cases` stops handing out work after the wall-time budget (default five hours in total).
"""
import importlib.util
import json
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))

import exp009_routine as X  # noqa: E402
import exp009_singular as Sg  # noqa: E402
from exp009_routine import R  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
LOG = ART / "run.log"
T0 = time.time()
MAX_WORKERS = 8
SAVE_EVERY = 60.0
G2_SAMPLE = 5
RANK_CHUNK = {"X": X.RANK_CHUNK, "Y": 500}


def log(msg):
    line = "[%8.1fs] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-009", "hypothesis": "hypothesis.md (frozen)", "rank_chunks": {}, "pairs": {}, "gates": {},
            "runs": []}


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


# ------------------------------------------------------------------ gates G1 and G3
def gate_g1_direct():
    rows = []
    for name, params, expect in (("GF(11)", (0, 0, 0, 0), True), ("GF(13)", (0, 0, 0, 0), True), ("GF(3)", (0, 0, 0, 0), False),
                                 ("GF(5)", (0, 0, 0, 0), False), ("GF(7)", (0, 0, 0, 0), False), ("GF(13)", (1, 0, 0, 0), True)):
        F = R.make_field(name)
        t, _ = R.betti_table(F, X.family_coeff_array(F, 4, params), 4)
        rows.append({"case": "L_4%s over %s" % (params, name), "betti": R.table_rows(t), "expected_pure": expect,
                     "ok": (t == R.pure_table(4)) is expect})
    bad = [r for r in rows if not r["ok"]]
    return {"passed": not bad, "cases": rows, "failing_cases": bad}


def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp009.py", "-q"], cwd=str(ROOT),
                          capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def g1_direct_ok(res):
    return res.get("gates", {}).get("G1", {}).get("direct", {}).get("passed") is True


def gate_g3_ok(res):
    return res.get("gates", {}).get("G3", {}).get("passed") is True


def cmd_gates():
    ART.mkdir(exist_ok=True)
    res = load()
    t0 = time.time()
    log("gates start")
    g1 = res["gates"].get("G1", {})
    g1["direct"] = gate_g1_direct()
    g1["passed"] = g1["direct"]["passed"] and g1.get("controls", {}).get("passed", True)
    res["gates"]["G1"] = g1
    save(res)
    log("G1 (direct part) %s: %d cases" % ("PASSED" if g1["direct"]["passed"] else "FAILED", len(g1["direct"]["cases"])))
    failed = None if g1["direct"]["passed"] else "G1"
    if not failed:
        g3 = gate_g3()
        res["gates"]["G3"] = g3
        save(res)
        log("G3 %s: %s" % ("PASSED" if g3["passed"] else "FAILED", json.dumps(g3)))
        if not g3["passed"]:
            failed = "G3"
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    if failed:
        log("GATE FAILED: %s; the run stops here; failing cases: %s" % (failed, json.dumps(res["gates"][failed].get(
            "direct", res["gates"][failed]).get("failing_cases"))[:1500]))
        return 1
    log("G1 (direct part) and G3 passed; the control-pair part of G1 is checked by `cases` after the five control pairs; G2 by `second`")
    return 0


def gate_g1_controls(res):
    """The control pairs: every member has rank at most r; among the members of rank r whose Betti table is computed at least half
    are pure; at least one pure member per pair (the proposition applies there)."""
    rows, bad = [], []
    for e, p in X.CONTROL_PAIRS:
        pr = res["pairs"].get(X.pair_key(e, p, "X"))
        if not pr or "s2" not in pr:
            return None
        s2 = pr["s2"]
        above = sum(len(res["rank_chunks"][c]["above"]) for c in pr["rank_chunk_ids"])
        computed = s2["betti_computed"]
        ok = above == 0 and computed > 0 and 2 * s2["pure"] >= computed
        row = {"pair": [e, p], "members_above_r": above, "tables_computed": computed, "pure": s2["pure"], "ok": ok}
        rows.append(row)
        if not ok:
            bad.append(row)
    return {"passed": not bad, "pairs": rows, "failing_cases": bad}


# ------------------------------------------------------------------ cases
def pair_list():
    only = opt("only", "")
    if not only:
        return list(X.PAIRS)
    out = []
    for item in only.replace(";", "+").split("+"):
        e, p = (int(t) for t in item.split(","))
        out.append((e, p))
    return out


def pair_record(res, e, p, fam):
    return res["pairs"].setdefault(X.pair_key(e, p, fam), {"e": e, "p": p, "family": fam,
                                                           "field": X.field_name(p, fam), "n_members": X.n_members(p, fam)})


def rank_specs(e, p, fam):
    n, c = X.n_members(p, fam), RANK_CHUNK[fam]
    return [{"id": "R|%d|%d|%s|%07d-%07d" % (e, p, fam, s, min(s + c, n)), "e": e, "p": p, "fam": fam, "start": s,
             "end": min(s + c, n)} for s in range(0, n, c)]


def _rank_job(spec):
    return X.rank_chunk(spec["e"], spec["p"], spec["fam"], spec["start"], spec["end"])


def stage1(res, e, p, fam, budget_end):
    """The rank of mu_3e for every member (family X: all p^4; family Y: 20,000); resumable by chunk."""
    pr = pair_record(res, e, p, fam)
    specs = rank_specs(e, p, fam)
    pr["rank_chunk_ids"] = [s["id"] for s in specs]
    todo = [s for s in specs if s["id"] not in res["rank_chunks"]]
    t0 = time.time()
    if todo:
        log("%s: stage 1, %d of %d chunks to do" % (X.pair_key(e, p, fam), len(todo), len(specs)))
        it = iter(todo)
        last_save = time.time()
        with ProcessPoolExecutor(max_workers=workers()) as pool:
            pending = set()

            def submit_next():
                if time.time() > budget_end:
                    return
                s = next(it, None)
                if s is not None:
                    pending.add(pool.submit(_rank_job, s))

            for _ in range(workers() * 2):
                submit_next()
            while pending:
                done, _ = wait(pending, timeout=120, return_when=FIRST_COMPLETED)
                for fut in done:
                    pending.discard(fut)
                    rec = fut.result()
                    res["rank_chunks"]["R|%d|%d|%s|%07d-%07d" % (e, p, fam, rec["start"], rec["end"])] = rec
                    submit_next()
                if time.time() - last_save > SAVE_EVERY:
                    save(res)
                    last_save = time.time()
    done_n = sum(res["rank_chunks"][c]["n"] for c in pr["rank_chunk_ids"] if c in res["rank_chunks"])
    pr["rank_seconds"] = round(pr.get("rank_seconds", 0) + time.time() - t0, 1)
    pr["rank_complete"] = done_n == pr["n_members"]
    save(res)
    log("%s: stage 1 %d of %d members" % (X.pair_key(e, p, fam), done_n, pr["n_members"]))
    return pr["rank_complete"]


def rank_r_list(res, pr):
    return sorted(i for c in pr["rank_chunk_ids"] for i in res["rank_chunks"][c]["rank_r"])


def _s2_job(args):
    return X.s2_task(*args)


def stage2(res, e, p, fam, budget_end):
    """Hilbert function for the members of rank r in index order, the Betti table when it is h_e; early stop at 40 pure members (X) or
    10 pure members and 40 tables (Y); tasks are handed out in order, running tasks finish and are counted."""
    pr = pair_record(res, e, p, fam)
    L = rank_r_list(res, pr)
    es = X.EarlyStop(X.EARLY_STOP_X) if fam == "X" else X.EarlyStop(X.EARLY_STOP_Y, X.MAX_BETTI_Y)
    size = X.S2_CHUNK_X if fam == "X" else 1
    tasks = [L[i:i + size] for i in range(0, len(L), size)]
    t0 = time.time()
    log("%s: stage 2, %d members of rank r in %d tasks" % (X.pair_key(e, p, fam), len(L), len(tasks)))
    records, next_i, last_save, timeout = [], 0, time.time(), False
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        pending = {}

        def submit_next():
            nonlocal next_i, timeout
            if next_i >= len(tasks) or not es.may_submit():
                return False
            if time.time() > budget_end:
                timeout = True
                return False
            pending[pool.submit(_s2_job, (e, p, fam, tasks[next_i]))] = next_i
            es.inflight += 1
            next_i += 1
            return True

        for _ in range(workers() * 2):
            if not submit_next():
                break
        while pending:
            done, _ = wait(set(pending), timeout=120, return_when=FIRST_COMPLETED)
            for fut in done:
                pending.pop(fut)
                es.inflight -= 1
                out = fut.result()
                records += out["records"]
                es.add(out["records"])
                while len(pending) < workers() * 2 and submit_next():
                    pass
            if time.time() - last_save > SAVE_EVERY:
                last_save = time.time()
                log("%s: stage 2, %d members examined, %d pure, %d tables" % (X.pair_key(e, p, fam), len(records), es.pure, es.betti))
    records.sort(key=lambda r: r["index"])
    htab, hid = [], {}
    other, pure_h, nonpure = [], [], {}
    for r in records:
        if r["pure_hilbert"]:
            item = {"index": r["index"], "params": r["params"], "betti": r["betti"], "pure": r["pure"]}
            if r["pure"]:
                item["basis"] = r["basis"]
            else:
                nonpure[str(r["betti"])] = nonpure.get(str(r["betti"]), 0) + 1
            pure_h.append(item)
        else:
            key = ",".join(str(v) for v in r["hilbert"])
            if key not in hid:
                hid[key] = len(htab)
                htab.append(r["hilbert"])
            other.append([r["index"], r["params"], hid[key]])
    complete = len(records) == len(L)
    pr["s2"] = {"rank_r_total": len(L), "examined": len(records), "examined_prefix_end": records[-1]["index"] if records else None,
                "complete": complete, "stopped_early": es.stopped, "stopped_by_budget": timeout,
                "tables_cap_reached": es.max_betti is not None and es.betti >= es.max_betti,
                "betti_computed": es.betti, "pure_hilbert": len(pure_h), "pure": es.pure, "hilbert_table": htab,
                "members_other_hilbert": other, "members_pure_hilbert": pure_h, "nonpure_tables": nonpure,
                "seconds": round(time.time() - t0, 1)}
    save(res)
    log("%s: stage 2 done: %d of %d examined, pure Hilbert %d, tables %d, pure %d, early stop %s, %.1f s" % (
        X.pair_key(e, p, fam), len(records), len(L), len(pure_h), es.betti, es.pure, es.stopped, time.time() - t0))
    return pr["s2"]


def cmd_cases():
    res = load()
    if not (g1_direct_ok(res) and gate_g3_ok(res)):
        log("G1 (direct part) and G3 have not both passed; run `gates` first")
        return 1
    budget_end = T0 + float(opt("budget-seconds", 5 * 3600 - 600))
    fam_sel = opt("fam", "")
    pairs = pair_list()
    t0 = time.time()
    res["runs"].append({"command": "cases", "seconds": 0.0})
    run_rec = res["runs"][-1]
    if fam_sel in ("", "X"):
        for e, p in pairs:
            if (e, p) in X.MAIN_PAIRS and not res["gates"].get("G1", {}).get("controls", {}).get("passed"):
                log("the control pairs have not passed the control part of G1; run them first (`cases --only=...`)")
                run_rec["seconds"] = round(time.time() - t0, 1)
                save(res)
                return 1
            key = X.pair_key(e, p, "X")
            if "s2" in res["pairs"].get(key, {}):
                log("%s: stored, skipped" % key)
            elif stage1(res, e, p, "X", budget_end):
                stage2(res, e, p, "X", budget_end)
            if (e, p) in X.CONTROL_PAIRS and not _check_controls(res):
                run_rec["seconds"] = round(time.time() - t0, 1)
                save(res)
                return 1
    if fam_sel in ("", "Y"):
        for e, p in pairs:
            if (e, p) not in X.MAIN_PAIRS:
                continue
            xs = res["pairs"].get(X.pair_key(e, p, "X"), {}).get("s2")
            if not xs or not xs["complete"] or xs["pure"] > 0:
                continue
            key = X.pair_key(e, p, "Y")
            if "s2" in res["pairs"].get(key, {}):
                log("%s: stored, skipped" % key)
            elif stage1(res, e, p, "Y", budget_end):
                stage2(res, e, p, "Y", budget_end)
    run_rec["seconds"] = round(time.time() - t0, 1)
    save(res)
    return 0


def _check_controls(res):
    g = gate_g1_controls(res)
    if g is None:
        return True
    g1 = res["gates"]["G1"]
    g1["controls"] = g
    g1["passed"] = g1["direct"]["passed"] and g["passed"]
    save(res)
    log("G1 (control pairs) %s: %s" % ("PASSED" if g["passed"] else "FAILED", json.dumps(g["pairs"])))
    if not g["passed"]:
        log("GATE FAILED: G1 (control pairs); the run stops here; failing cases: %s" % json.dumps(g["failing_cases"])[:1500])
    return g["passed"]


# ------------------------------------------------------------------ G2: the second instrument
def pure_members(res, key):
    s2 = res["pairs"][key].get("s2")
    return [m for m in s2["members_pure_hilbert"] if m["pure"]] if s2 else []


def singular_available():
    try:
        p = subprocess.run(["wsl", "-e", "bash", "-c", "Singular -v < /dev/null | head -1"], capture_output=True, text=True, timeout=120)
    except Exception as exc:
        return False, repr(exc)[:200]
    lines = [ln for ln in p.stdout.splitlines() if "Singular" in ln]
    return p.returncode == 0 and bool(lines), lines[0].strip() if lines else p.stderr[:200]


def _g2_one(item):
    key, m = item
    e, p, fam = key.split("|")
    F = R.make_field(X.field_name(int(p), fam))
    name = "e%s_p%s_%s_%d" % (e, p, fam, m["index"])
    t, dt, err = Sg.run_member(name, R.field_record(F), m["basis"], SING)
    return name, t, dt, err


def cmd_second():
    res = load()
    t0 = time.time()
    if not (g1_direct_ok(res) and gate_g3_ok(res)):
        log("G1 (direct part) and G3 have not both passed; run `gates` first")
        return 1
    ok, version = singular_available()
    if not ok:
        res["gates"]["G2"] = {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version,
                              "note": "single-instrument results"}
        save(res)
        log("G2 BLOCKED: " + version)
        return 1
    SING.mkdir(parents=True, exist_ok=True)
    sample = [(key, m) for key in sorted(res["pairs"]) for m in pure_members(res, key)[:G2_SAMPLE]]
    log("G2: %d pure members in the sample (%s)" % (len(sample), version))
    with ThreadPoolExecutor(max_workers=workers()) as tp:
        outs = list(tp.map(_g2_one, sample))
    rows, bad, errors, per = [], [], [], {}
    for (key, m), (name, t, dt, err) in zip(sample, outs):
        e = int(key.split("|")[0])
        row = {"pair": key, "index": m["index"], "script": name + ".sing", "seconds": round(dt, 1)}
        if err or t is None:
            row["error"] = err
            errors.append(name)
        else:
            row["betti_I1"] = m["betti"]
            row["betti_I2"] = [[i, j, r] for (i, j), r in sorted(t.items())]
            row["agree"] = [tuple(x) for x in m["betti"]] == [tuple(x) for x in row["betti_I2"]]
            row["pure_I2"] = t == R.pure_table(e)
            if not row["agree"] or not row["pure_I2"]:
                bad.append(name)
            else:
                per[key] = per.get(key, 0) + 1
        rows.append(row)
    res["gates"]["G2"] = {"passed": not bad and not errors, "singular": version, "sample_members": len(sample),
                          "agree_and_pure_in_I2": sum(per.values()), "per_pair": per, "failing_cases": bad,
                          "singular_errors": errors, "rows": rows}
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    save(res)
    g = res["gates"]["G2"]
    log("G2 %s: %d of %d agree; failing %s; errors %s" % ("PASSED" if g["passed"] else "FAILED", g["agree_and_pure_in_I2"], len(sample),
                                                           bad[:5], errors[:5]))
    return 0 if g["passed"] else 1


# ------------------------------------------------------------------ table
def cmd_table():
    spec = importlib.util.spec_from_file_location("exp009_make_summary", HERE / "make_summary.py")
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    res = load()
    res["totals"] = ms.compute_totals(res)
    res["predictions"] = ms.predictions(res["totals"])
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
    save(res)
    print(ms.totals_text(res["totals"]))
    ms.write_summary(res, HERE / "results-summary.md")
    log("table written")
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    ART.mkdir(exist_ok=True)
    fn = {"gates": cmd_gates, "cases": cmd_cases, "second": cmd_second, "table": cmd_table}.get(cmd)
    if fn is None:
        print(__doc__)
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
