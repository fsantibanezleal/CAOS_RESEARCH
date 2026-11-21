"""EXP-021: the stratum S(5; 0, 1) at the open pair (11, 3), the 43,046,721 monic pairs x^11 + alpha x + gamma y^9, y^11 + beta y + delta x^9
over GF(3), enumerated completely with the block pattern of the syzygy classes, at three controls (family K) and at (11, 3) (family X).

Run from the repository root, with the repository virtual environment:
    python <this file> gates                       G3 (pytest's exit code); exit 1 on a failure
    python <this file> cases --family K|X [--workers N] [--budget-seconds N]
                                                   resumable (progress is stored every 60 s and per block); K is followed by G1; X needs G1
    python <this file> second [--workers N] [--out-dir D]
                                                   G2: Singular 4.3.2 (Plural, through WSL) on the first three pure members of each case
    python <this file> table                       predictions P1 to P5 into results.json, then results-summary.md; prints the table

The hypothesis is hypothesis.md (frozen).  The routine of EXP-010 (block ranks, staged test, Betti table) and the Singular generator of
EXP-009 are imported, not edited.  At most 12 worker processes.  Family K: 30 minutes of wall time; family X: 4 hours.  No machine path is
written to any artifact.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from collections import deque
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
EXPS = HERE.parent
sys.path.insert(0, str(HERE))
for _p in (EXPS / "EXP-010-weight-class-strata", EXPS / "EXP-009-linear-family-below-2e"):
    if str(_p) not in sys.path:
        sys.path.append(str(_p))  # appended: those folders have their own run.py and make_summary.py, which must not shadow this folder's

import exp021_routine as X  # noqa: E402

R = X.R
np = X.np

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
MAX_WORKERS = 12
SAVE_EVERY = 60.0
BUDGET_SECONDS = {"K": 1800, "X": 14400}
TABLES_WHILE_ENUMERATING = 2  # Betti tables in flight while blocks are still being counted
G2_PER_CASE = 3
G2_TIMEOUT = 1200  # seconds: a member that Singular does not finish in twenty minutes is checked by one instrument only
FAMILIES = ("K", "X")
NONMONIC_CHUNK = 5000


def _load_exp010_run():
    spec = importlib.util.spec_from_file_location("exp010_run", EXPS / "EXP-010-weight-class-strata" / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp010_run"] = mod
    spec.loader.exec_module(mod)
    return mod


R10 = _load_exp010_run()
log = R10.log
opt = R10.opt

# the cases (hypothesis.md): (e, p, mode, number of members); the controls K and the open pair X
PLAN = {"K": [(5, 3, "complete", None), (7, 5, "random", 400_000), (11, 7, "random", 200_000)],
        "X": [(11, 3, "complete", None)]}
# the counts of the table of the controls of the hypothesis (reference implementation `probe_canonical.py`; stage 3 below the thresholds
# and the plain count from its logs)
KNOWN = {"K|5|3": {"stages": [44175, 7526, 5684, 1664], "found": 1664, "tables": 1664, "pure": 400, "pure_delta0": 58, "pure_gamma_delta0": 0,
                   "first_pure": [866, 919], "plain": 1736, "stage3_delta0": 180, "stage3_gamma_delta0": 22},
         "K|7|5": {"stages": [316708, 64914, 18166, 212], "found": 212, "tables": 212, "pure": 64},
         "K|11|7": {"stages": [196061, 3249, 690, 0], "found": 0, "tables": 0, "pure": 0}}
NONMONIC = {"e": 5, "p": 3, "members": 132_496, "monic": 59_049, "non_monic": 73_447}
NONMONIC_KNOWN = {"stages": [60933, 3942, 8572, 0]}


def workers():
    return max(1, min(MAX_WORKERS, int(opt("workers", MAX_WORKERS))))


# ------------------------------------------------------------------ the plan
def plan(family, only=None):
    """The cases of a family in the order of the hypothesis; `only` is a set of pairs (e, p)."""
    out = []
    for e, p, mode, n in PLAN[family]:
        total = X.n_members(e, p)
        members = total if mode == "complete" else n
        out.append({"key": "%s|%d|%d" % (family, e, p), "family": family, "e": e, "p": p, "d": (e - 1) // 2, "mode": mode,
                    "members": members, "total": total, "blocks": len(X.blocks_of(members)), "block": X.BLOCK,
                    "table_rule": "early" if family == "X" else "all", "plain": (e, p) == (5, 3)})
    return [c for c in out if (c["e"], c["p"]) in only] if only else out


def order():
    """Every case in the order of the run: family K, family X."""
    return [c for fam in FAMILIES for c in plan(fam)]


# ------------------------------------------------------------------ the store
def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-021", "hypothesis": "hypothesis.md (frozen)", "cases": {}, "partial": {}, "gates": {}, "runs": [],
            "nonmonic": None, "budget": {"K": {"used_seconds": 0.0, "limit_seconds": BUDGET_SECONDS["K"]},
                                         "X": {"used_seconds": 0.0, "limit_seconds": BUDGET_SECONDS["X"]}}}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
    tmp.replace(RESULTS)


# ------------------------------------------------------------------ gates
def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp021.py", "-q", "-o", "addopts="], cwd=str(ROOT),
                          capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def gates_ok(res):
    return res.get("gates", {}).get("G3", {}).get("passed") is True


def cmd_gates():
    res = load()
    t0 = time.time()
    g3 = gate_g3()
    res["gates"]["G3"] = g3
    log("G3 %s: %s" % ("PASSED" if g3["passed"] else "FAILED", g3["last_line"]))
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    return 0 if g3["passed"] else 1


def g1(res):
    """G1: every count of the table of the controls (stages, members of stage 3, tables, pure members, and at (5, 3) the pure members with
    delta = 0 and gamma = delta = 0, the first pure indices and the 1,736 members with the pure Hilbert function by the plain staged
    test), and the non-monic members at (5, 3)."""
    rows = []
    for c in plan("K"):
        s, want = res["cases"].get(c["key"]), KNOWN[c["key"]]
        if s is None:
            rows.append({"case": c["key"], "ok": False, "missing": True})
            continue
        got = {"stages": s["stages"], "found": s["found_total"], "tables": s["tables"], "pure": s["pure"]}
        same = {k: got[k] == want[k] for k in got}
        if "pure_delta0" in want:
            got.update(pure_delta0=s["pure_delta0"], pure_gamma_delta0=s["pure_gamma_delta0"], first_pure=s["pure_indices"][:2],
                       plain=s["plain"], stage3_delta0=s["stage3_delta0"], stage3_gamma_delta0=s["stage3_gamma_delta0"])
            same.update({k: got[k] == want[k] for k in want if k not in same})
        rows.append({"case": c["key"], "got": got, "want": want, "equal": same,
                     "ok": bool(all(same.values()) and s["status"] == "complete")})
    nm = res.get("nonmonic")
    if nm is None:
        rows.append({"case": "non-monic (5, 3)", "ok": False, "missing": True})
    else:
        same = {"members": nm["non_monic"] == NONMONIC["non_monic"] and nm["monic_seen"] == NONMONIC["monic"],
                "stages": nm["stages"] == NONMONIC_KNOWN["stages"], "plain": nm["plain"] == 0}
        rows.append({"case": "non-monic (5, 3)", "got": {"members": nm["non_monic"], "stages": nm["stages"], "plain": nm["plain"]},
                     "want": {"members": NONMONIC["non_monic"], "stages": NONMONIC_KNOWN["stages"], "plain": 0}, "equal": same,
                     "ok": bool(all(same.values()))})
    return {"passed": all(r["ok"] for r in rows), "rows": rows}


# ------------------------------------------------------------------ cases
def new_state(spec):
    return {"key": spec["key"], "next": 0, "block_rows": [], "found": [], "found_total": 0, "found_kept_all": True, "plain": 0,
            "tables": 0, "pure": 0, "tables_extended": False, "nonpure_tables": {}, "worker_seconds": 0.0, "table_seconds": 0.0,
            "wall_seconds": 0.0, "enum_done": False, "tables_done": False}


def table_wanted(st, rule, inflight):
    """May another Betti table be started?  Rule 'all': on every member of stage 3.  Rule 'early': in the order of the index until 5 pure
    members or 40 tables; when 40 tables hold no pure member the tables continue on every remaining member of stage 3 (the hypothesis
    requires it before any negative statement)."""
    if rule == "all":
        return True
    if st["pure"] >= X.EARLY_STOP_PURE:
        return False
    return st["tables_extended"] or st["tables"] + inflight < X.MAX_TABLES


def run_case(res, spec, pool, deadline):
    """Count the blocks in order and table the members of stage 3 as the prefix grows; blocks are aggregated in the order of their index,
    so the stored state is the state after a prefix and a resumed case continues exactly.  Returns True when the case is complete."""
    key, e, p = spec["key"], spec["e"], spec["p"]
    st = res["partial"].get(key) or new_state(spec)
    res["partial"][key] = st
    bl = X.blocks_of(spec["members"])
    complete_list = spec["mode"] == "complete"
    nw = workers()
    t_start, wall0 = time.time(), st["wall_seconds"]
    submit = st["next"]
    pending, done, window = {}, {}, deque()
    tnext = sum(1 for m in st["found"] if "pure" in m)  # the members tabled so far are a prefix of the list, in the order of the index
    last_save = time.time()
    while True:
        cut = time.time() > deadline
        while not cut and submit < len(bl) and len(pending) < nw + 1:
            pending[pool.submit(X.job, (e, p, bl[submit][0], bl[submit][1], complete_list, spec["plain"]))] = submit
            submit += 1
        cap = TABLES_WHILE_ENUMERATING if st["next"] < len(bl) else max(2, nw // 2)
        while tnext < len(st["found"]) and len(window) < cap and table_wanted(st, spec["table_rule"], len(window)):
            m = st["found"][tnext]
            window.append((m, pool.submit(X.betti_job, {"index": m["index"], "e": e, "p": p, "f": m["f"], "g": m["g"]})))
            tnext += 1
        waiting = set(pending) | {f for _, f in window}
        if not waiting:
            break
        finished, _ = wait(waiting, timeout=5, return_when=FIRST_COMPLETED)
        for fut in finished & set(pending):
            done[pending.pop(fut)] = fut.result()
        while st["next"] in done:
            out = done.pop(st["next"])
            st["block_rows"].append(out["stages"] + out["below_delta0"] + out["below_gamma_delta0"] + [out["seconds"]])
            for m in out["found"]:
                if len(st["found"]) < X.MAX_FOUND:
                    m["f_text"], m["g_text"] = R.poly_text(e, p, m["f"]), R.poly_text(e, p, m["g"])
                    st["found"].append(m)
                else:
                    st["found_kept_all"] = False
            st["found_total"] += len(out["found"])
            st["plain"] += out["plain"] or 0
            st["worker_seconds"] += out["seconds"]
            st["next"] += 1
        while window and window[0][1].done():
            m, fut = window.popleft()
            out = fut.result()
            m["betti"], m["length"], m["pure"] = out["betti"], out["length"], out["pure"]
            st["tables"] += 1
            st["pure"] += 1 if out["pure"] else 0
            st["table_seconds"] += out["seconds"]
            st["worker_seconds"] += out["seconds"]
            if not out["pure"]:
                k = "%s, length %s" % (out["betti"], out["length"])
                st["nonpure_tables"][k] = st["nonpure_tables"].get(k, 0) + 1
            if spec["table_rule"] == "early" and st["tables"] >= X.MAX_TABLES and st["pure"] == 0 and not st["tables_extended"]:
                st["tables_extended"] = True
                log("%s: 40 tables without a pure member: the tables continue on every remaining member of stage 3" % key)
            log("%s: table %d (member %d, length %s): %s, pure so far %d" % (key, st["tables"], m["index"], out["length"],
                                                                          "PURE" if out["pure"] else "not pure", st["pure"]))
            if spec["table_rule"] == "early" and st["pure"] >= X.EARLY_STOP_PURE:
                for _, f in window:
                    f.cancel()
                window.clear()
        if time.time() - last_save > SAVE_EVERY:
            st["wall_seconds"] = round(wall0 + time.time() - t_start, 1)
            save(res)
            last_save = time.time()
            log("%s: %d of %d blocks, stage 3 so far %d, tables %d, pure %d" % (key, st["next"], len(bl), st["found_total"], st["tables"],
                                                                              st["pure"]))
    st["wall_seconds"] = round(wall0 + time.time() - t_start, 1)
    st["enum_done"] = st["next"] >= len(bl)
    st["tables_done"] = st["enum_done"] and (tnext >= len(st["found"]) or not table_wanted(st, spec["table_rule"], 0))
    return st["enum_done"] and st["tables_done"]


def case_record(spec, st):
    e, p = spec["e"], spec["p"]
    rows = st["block_rows"]
    stages = [sum(r[k] for r in rows) for k in range(4)]
    d0 = [sum(r[4 + k] for r in rows) for k in range(4)]
    gd0 = [sum(r[8 + k] for r in rows) for k in range(4)]
    done_members = sum(min(spec["members"], (k + 1) * spec["block"]) - k * spec["block"] for k in range(st["next"]))
    tabled = [m for m in st["found"] if "pure" in m]
    complete = st["enum_done"] and st["tables_done"]
    return {"family": spec["family"], "e": e, "p": p, "d": spec["d"], "mode": spec["mode"], "syzygy_classes": list(X.pattern(e)[1:3]),
            "block_order": X.pattern(e)[3], "members": spec["members"], "total_list": spec["total"], "done": done_members,
            "blocks": [spec["blocks"], st["next"]], "block_size": spec["block"],
            "status": "complete" if complete else "not finished", "stages": stages, "stages_delta0": d0, "stages_gamma_delta0": gd0,
            "found_total": st["found_total"], "found_kept": len(st["found"]), "found_kept_all": st["found_kept_all"], "plain": st["plain"],
            "tables": st["tables"], "pure": st["pure"], "tables_extended": st["tables_extended"], "table_rule": spec["table_rule"],
            "pure_indices": [m["index"] for m in tabled if m["pure"]],
            "pure_delta0": sum(1 for m in tabled if m["pure"] and m["index"] < p ** (e + 3)),
            "pure_gamma_delta0": sum(1 for m in tabled if m["pure"] and m["index"] < p ** (e + 1)),
            "stage3_delta0": d0[3], "stage3_gamma_delta0": gd0[3], "nonpure_tables": st["nonpure_tables"],
            "block_rows": rows, "members_stage3": st["found"], "worker_seconds": round(st["worker_seconds"], 1),
            "table_seconds": round(st["table_seconds"], 1), "wall_seconds": st["wall_seconds"],
            "ms_per_member_per_worker": round(1000 * sum(r[12] for r in rows) / max(done_members, 1), 3),
            "blocks_seconds_min_max": [min((r[12] for r in rows), default=None), max((r[12] for r in rows), default=None)]}


def run_nonmonic(res, pool):
    """Family K, the non-monic members at (5, 3): the 132,496 normalized members of S(2; 0, 1), those with the coefficient of x^5 in f or of
    y^5 in g zero staged and tested by the plain staged test."""
    e, p, n = NONMONIC["e"], NONMONIC["p"], NONMONIC["members"]
    assert R.n_members(e, p, 2, 0, 1) == n
    t0 = time.time()
    futs = [pool.submit(X.nonmonic_job, (e, p, s, min(n, s + NONMONIC_CHUNK))) for s in range(0, n, NONMONIC_CHUNK)]
    outs = [f.result() for f in futs]
    res["nonmonic"] = {"members": n, "stages": [sum(o["stages"][k] for o in outs) for k in range(4)], "plain": sum(o["plain"] for o in outs),
                       "monic_seen": sum(o["both_nonzero"] for o in outs), "non_monic": sum(sum(o["stages"]) for o in outs),
                       "worker_seconds": round(sum(o["seconds"] for o in outs), 1), "wall_seconds": round(time.time() - t0, 1)}
    log("non-monic members at (5, 3): %s" % json.dumps({k: v for k, v in res["nonmonic"].items()}))


def cmd_cases():
    res = load()
    if not gates_ok(res):
        log("G3 has not passed; run `gates` first")
        return 1
    fam = opt("family", "")
    if fam not in FAMILIES:
        log("--family K|X is required")
        return 2
    if fam == "X" and not res["gates"].get("G1", {}).get("passed"):
        log("family K has not passed G1; run `cases --family K` first")
        return 1
    specs = plan(fam)
    used = res["budget"][fam]["used_seconds"]
    left = float(opt("budget-seconds", BUDGET_SECONDS[fam] - used))
    t0 = time.time()
    log("family %s: %d cases planned; budget left %.0f s (used %.0f s of %d s); %d workers" % (fam, len(specs), left, used,
                                                                                            BUDGET_SECONDS[fam], workers()))
    rc = 0
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        for spec in specs:
            if spec["key"] in res["cases"]:
                continue
            if time.time() > t0 + left:
                break
            ok = run_case(res, spec, pool, t0 + left)
            st = res["partial"][spec["key"]]
            if not ok:
                save(res)
                log("%s: stopped with %d of %d blocks done, tables done %s" % (spec["key"], st["next"], spec["blocks"], st["tables_done"]))
                break
            res["cases"][spec["key"]] = case_record(spec, st)
            res["partial"].pop(spec["key"], None)
            save(res)
            c = res["cases"][spec["key"]]
            log("%s: %d members, stages %s, stage 3 %d, tables %d, pure %d, %.0f s" % (spec["key"], c["done"], c["stages"], c["found_total"],
                                                                                     c["tables"], c["pure"], c["wall_seconds"]))
        if fam == "K" and res.get("nonmonic") is None and all(c["key"] in res["cases"] for c in specs) and time.time() < t0 + left:
            run_nonmonic(res, pool)
    dt = time.time() - t0
    res["budget"][fam]["used_seconds"] = round(used + dt, 1)
    res["runs"].append({"command": "cases", "family": fam, "workers": workers(), "seconds": round(dt, 1)})
    if fam == "K" and all(c["key"] in res["cases"] for c in specs) and res.get("nonmonic") is not None:
        res["gates"]["G1"] = g1(res)
        ok = res["gates"]["G1"]["passed"]
        log("G1 %s" % ("PASSED" if ok else "FAILED: " + json.dumps([r for r in res["gates"]["G1"]["rows"] if not r["ok"]])))
        rc = 0 if ok else 1
    save(res)
    log("family %s: %d of %d cases stored; %.0f s this run" % (fam, sum(1 for c in specs if c["key"] in res["cases"]), len(specs), dt))
    return rc


# ------------------------------------------------------------------ G2
def g2_sample(res):
    """The first three pure members of every case that has one, in the order of the run."""
    out = []
    for spec in order():
        s = res["cases"].get(spec["key"])
        if s:
            out += [(spec["key"], m) for m in [m for m in s["members_stage3"] if m.get("pure")][:G2_PER_CASE]]
    return out


def cmd_second():
    import exp009_singular as Sg
    res = load()
    t0 = time.time()
    if not gates_ok(res):
        log("G3 has not passed; run `gates` first")
        return 1
    ok, version = R10.singular_available()
    if not ok:
        res["gates"]["G2"] = {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version,
                              "note": "single-instrument results"}
        save(res)
        log("G2 BLOCKED: " + version)
        return 1
    out_dir = Path(opt("out-dir", "D:/_Temp/bs-exp021-2026-11-20/singular_out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    SING.mkdir(parents=True, exist_ok=True)
    sample = g2_sample(res)
    log("G2: %d pure members in the sample (%s)" % (len(sample), version))

    def one(item):
        key, mem = item
        s = res["cases"][key]
        e, p = s["e"], s["p"]
        name = "e%d_p%d_idx%d" % (e, p, mem["index"])
        field = {"name": "GF(%d)" % p, "uhlib_name": "GF(%d)" % p, "char": p, "degree": 1, "modulus": None}
        return name, Sg.run_member(name, field, R.basis_json(e, p, mem["f"], mem["g"]), out_dir, timeout=G2_TIMEOUT)

    with ThreadPoolExecutor(max_workers=min(6, workers())) as tp:
        outs = list(tp.map(one, sample))
    rows, bad, errors = [], [], []
    for (key, mem), (name, (t, dt, err)) in zip(sample, outs):
        e = res["cases"][key]["e"]
        row = {"case": key, "index": mem["index"], "script": name + ".sing", "seconds": round(dt, 1), "betti_I1": mem["betti"]}
        if err or t is None:
            row["error"] = err
            errors.append(name)
        else:
            row["betti_I2"] = [[i, j, r] for (i, j), r in sorted(t.items())]
            row["agree"] = [tuple(x) for x in mem["betti"]] == [tuple(x) for x in row["betti_I2"]]
            row["pure_I2"] = t == R.pure_table(e)
            if not (row["agree"] and row["pure_I2"]):
                bad.append(name)
        rows.append(row)
        src = out_dir / (name + ".sing")
        if src.exists():
            shutil.copyfile(src, SING / (name + ".sing"))
    agree = sum(1 for r in rows if r.get("agree") and r.get("pure_I2"))
    res["gates"]["G2"] = {"passed": not bad and not errors, "singular": version, "timeout_seconds": G2_TIMEOUT, "sample_members": len(sample),
                          "agree_and_pure_in_I2": agree, "failing_cases": bad, "singular_errors": errors, "rows": rows}
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    save(res)
    log("G2 %s: %d of %d agree and are pure in both instruments; failing %s; errors %s" % (
        "PASSED" if res["gates"]["G2"]["passed"] else "FAILED", agree, len(sample), bad[:5], errors[:5]))
    return 0 if res["gates"]["G2"]["passed"] else 1


# ------------------------------------------------------------------ table
def cmd_table():
    spec = importlib.util.spec_from_file_location("exp021_make_summary", HERE / "make_summary.py")
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    res = load()
    res["plan"] = [{k: c[k] for k in ("key", "family", "e", "p", "d", "mode", "members", "total", "blocks", "block", "table_rule")}
                   for c in order()]
    res["cases_partial"] = {c["key"]: case_record(c, res["partial"][c["key"]]) for c in order() if c["key"] in res["partial"]}
    res["totals"] = ms.compute_totals(res)
    res["predictions"] = ms.predictions(res)
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
    res["wall_seconds_by_family"] = ms.family_seconds(res)
    save(res)
    print(ms.totals_text(res["totals"]))
    ms.write_summary(res, HERE / "results-summary.md")
    log("table written")
    return 0


def main():
    fn = {"gates": cmd_gates, "cases": cmd_cases, "second": cmd_second, "table": cmd_table}.get(sys.argv[1] if len(sys.argv) > 1 else "")
    if fn is None:
        print(__doc__)
        return 2
    ART.mkdir(exist_ok=True)
    return fn()


if __name__ == "__main__":
    sys.exit(main())
