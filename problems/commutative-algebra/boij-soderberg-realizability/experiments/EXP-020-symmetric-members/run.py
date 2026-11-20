"""EXP-020: the members x^e + alpha y^t, y^e + beta x^t with beta = c alpha^omega (fixed by the exchange of x and y), enumerated completely
through the filter (F0) to (F3) of EXP-019, at three controls (family K) and at the open pairs (14, 11), (15, 11), (15, 13), (15, 17),
(16, 17), (16, 19) (family X).

Run from the repository root, with the repository virtual environment:
    python <this file> gates                       G3 (pytest's exit code); exit 1 on a failure
    python <this file> cases --family K|X [--only e,p] [--only e,p ...] [--workers N] [--budget-seconds N]
                                                   resumable (progress is stored every 30 s and per case); K is followed by G1; X needs G1
    python <this file> second [--workers N] [--out-dir D]
                                                   G2: Singular 4.3.2 (Plural, through WSL) on the first three pure members of each case
    python <this file> table                       predictions P1 to P4 into results.json, then results-summary.md; prints the table

The hypothesis is hypothesis.md (frozen).  The routine of EXP-010 (staged Hilbert test, Betti table), the filter of EXP-019 and the Singular
generator of EXP-009 are imported, not edited.  At most 12 worker processes for the filter and 6 for the staged test and the Betti tables, one
hour of wall time.  No machine path is written to any artifact.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
EXPS = HERE.parent
sys.path.insert(0, str(HERE))
for _p in (EXPS / "EXP-010-weight-class-strata", EXPS / "EXP-009-linear-family-below-2e"):
    if str(_p) not in sys.path:
        sys.path.append(str(_p))

import exp020_routine as R  # noqa: E402  (imports the filter of EXP-019 and the routine of EXP-010)

X = R.X

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
MAX_WORKERS = 12  # the filter
MAX_HEAVY_WORKERS = 6  # the staged test and the Betti tables (memory at e = 15 and 16)
BUDGET_SECONDS = 3600
SAVE_EVERY = 30.0
BLOCK_RANKS = 8192
G2_PER_CASE = 3
G2_TIMEOUT = 1200  # seconds: a member that Singular does not finish in twenty minutes is checked by one instrument only
FAMILIES = ("K", "X")
# (e, p, t): the exponent of each control is fixed by the table of the hypothesis ((9, 13) uses t = 3, where the rule of EXP-019 gives 5)
PLAN = {"K": [(9, 13, 3), (11, 17, 7), (13, 11, 5)],
        "X": [(14, 11, 4), (15, 11, 5), (15, 13, 5), (15, 17, 7), (16, 17, 8), (16, 19, 8)]}
# the counts of the probe of the coordinating session (hypothesis.md table; the stage vectors are from its logs)
PROBE = {(9, 13): {"members": 57_120, "differ": 0, "passing": 116, "c1": 74, "stages": [23530, 33388, 0, 86, 116]},
         (11, 17): {"members": 9_824, "differ": 0, "passing": 286, "c1": 286, "stages": [4780, 4684, 0, 74, 286]},
         (13, 11): {"members": 322_100, "differ": 0, "passing": 94, "c1": 94, "stages": [192044, 129846, 0, 116, 94]}}


def _load_exp010_run():
    spec = importlib.util.spec_from_file_location("exp010_run", EXPS / "EXP-010-weight-class-strata" / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp010_run"] = mod
    spec.loader.exec_module(mod)
    return mod


R10 = _load_exp010_run()
log = R10.log
opt = R10.opt


def workers():
    return max(1, min(MAX_WORKERS, int(opt("workers", MAX_WORKERS))))


def only_pairs():
    """The pairs of every --only e,p (repeatable; 'e,p+e,p' also works), or None."""
    out = set()
    for k, a in enumerate(sys.argv[2:], start=2):
        if a == "--only" and k + 1 < len(sys.argv):
            val = sys.argv[k + 1]
        elif a.startswith("--only="):
            val = a.split("=", 1)[1]
        else:
            continue
        out |= {tuple(int(v) for v in item.split(",")) for item in val.replace(";", "+").split("+")}
    return out or None


# ------------------------------------------------------------------ the plan
def plan(family, only=None):
    """The cases of a family in the order of its table."""
    out = []
    for e, p, t in PLAN[family]:
        d = (e - t) // 2
        ranks = p ** (d + 1) - 1
        out.append({"key": "%s|%d|%d" % (family, e, p), "family": family, "e": e, "p": p, "t": t, "d": d, "stratum": list(R.stratum(e, t)),
                    "nu": R.least_nonresidue(p), "members": R.n_members(p, d), "block_ranks": BLOCK_RANKS, "blocks": -(-ranks // BLOCK_RANKS)})
    return [c for c in out if (c["e"], c["p"]) in only] if only else out


def order():
    """Every case in the order of the run of the hypothesis: the gates, family K, family X in the order of its table."""
    return [c for fam in FAMILIES for c in plan(fam)]


# ------------------------------------------------------------------ the store
def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-020", "hypothesis": "hypothesis.md (frozen)", "cases": {}, "partial": {}, "gates": {}, "runs": [],
            "budget": {"used_seconds": 0.0, "limit_seconds": BUDGET_SECONDS}}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
    tmp.replace(RESULTS)


# ------------------------------------------------------------------ gates
def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp020.py", "-q", "-o", "addopts="], cwd=str(ROOT), capture_output=True, text=True)
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


def g1_family_part(res):
    """G1: the numbers of members, of members with (F0) where (F1) and (F2) differ, of passing members and of passing members with (C1) equal
    those of the table of the probe; each control holds a pure member (the stage vector of the probe log is compared too, as a check)."""
    rows = []
    for c in plan("K"):
        s = res["cases"].get(c["key"])
        want = PROBE[(c["e"], c["p"])]
        if s is None:
            rows.append({"pair": [c["e"], c["p"]], "t": c["t"], "ok": False, "missing": True})
            continue
        got = {"members": s["counts"]["examined"], "differ": s["counts"]["differ"], "passing": s["counts"]["f3"], "c1": s["counts"]["c1"]}
        same = all(got[k] == want[k] for k in got)
        rows.append({"pair": [c["e"], c["p"]], "t": c["t"], "got": got, "want": {k: want[k] for k in got}, "stages_got": s["stage_counts"],
                     "stages_probe": want["stages"], "stages_equal": s["stage_counts"] == want["stages"], "pure": s["pure"],
                     "pure_hilbert": s["counts"]["pure_hilbert"], "tables": s["tables"], "counts_equal": same,
                     "ok": bool(same and s["pure"] > 0 and s["status"] == "complete")})
    return {"passed": all(r["ok"] for r in rows), "rows": rows}


# ------------------------------------------------------------------ cases
def new_state(spec):
    return {"key": spec["key"], "next": 0, "filter_done": False,
            "counts": {"examined": 0, "f0": 0, "f1": 0, "f2": 0, "f3": 0, "differ": 0, "c1": 0, "pure_hilbert": 0},
            "stage_counts": [0] * 5, "passing": [], "tables": 0, "pure": 0, "nonpure_tables": {}, "worker_seconds": 0.0,
            "filter_seconds": 0.0, "staged_seconds": 0.0, "table_seconds": 0.0, "wall_seconds": 0.0, "stopped_early": False,
            "tables_cap_reached": False, "staged_done": False, "tables_done": False}


def _block_spec(spec, block):
    ranks = spec["members"] // 2
    r0 = block * spec["block_ranks"]
    return {"e": spec["e"], "p": spec["p"], "t": spec["t"], "r0": r0, "r1": min(ranks, r0 + spec["block_ranks"])}


def run_filter(res, spec, pool, deadline, save_fn, st):
    """The complete enumeration of a case on the pool.  Blocks are aggregated in the order of their index, so the stored state is the state
    after a prefix of the ranks and a resumed case continues exactly.  Returns True when every block is done."""
    key = spec["key"]
    t_start, wall0 = time.time(), st["wall_seconds"]
    nblocks = spec["blocks"]
    submit = st["next"]
    pending, done = {}, {}
    last_save = time.time()
    nw = workers()
    while True:
        cut = time.time() > deadline
        while not cut and submit < nblocks and len(pending) < nw + 2:
            pending[pool.submit(R.block_job, _block_spec(spec, submit))] = submit
            submit += 1
        if not pending:
            break
        finished, _ = wait(set(pending), timeout=5, return_when=FIRST_COMPLETED)
        for fut in finished:
            done[pending.pop(fut)] = fut.result()
        while st["next"] in done:
            out = done.pop(st["next"])
            for k, v in out["counts"].items():
                st["counts"][k] += v
            st["stage_counts"] = [a + b for a, b in zip(st["stage_counts"], out["stage_counts"])]
            st["passing"] += out["passing"]
            st["worker_seconds"] += out["seconds"]
            st["filter_seconds"] += out["seconds"]
            st["next"] += 1
        if time.time() - last_save > SAVE_EVERY:
            st["wall_seconds"] = round(wall0 + time.time() - t_start, 1)
            res["partial"][key] = st
            save_fn(res)
            last_save = time.time()
            log("%s: %d of %d members, passing %d" % (key, st["counts"]["examined"], spec["members"], st["counts"]["f3"]))
    st["wall_seconds"] = round(wall0 + time.time() - t_start, 1)
    st["filter_done"] = st["next"] >= nblocks
    res["partial"][key] = st
    return st["filter_done"]


def run_heavy(spec, st, pool):
    """The staged test on every passing member (in the order of the index), then the Betti tables on the passing members in the order of
    their index until 5 are pure or 40 are computed.  Results are consumed in the order of the index, so they do not depend on the number
    of workers."""
    e, p, t, key = spec["e"], spec["p"], spec["t"], spec["key"]
    t0 = time.time()
    jobs = [pool.submit(R.staged_job, {"e": e, "p": p, "t": t, "index": m["index"], "f": m["f"], "g": m["g"]}) for m in st["passing"]]
    for m, job in zip(st["passing"], jobs):
        out = job.result()
        m["pure_hilbert"] = out["pure_hilbert"]
        st["staged_seconds"] += out["seconds"]
        st["worker_seconds"] += out["seconds"]
    st["counts"]["pure_hilbert"] = sum(1 for m in st["passing"] if m["pure_hilbert"])
    st["staged_done"] = True
    log("%s: staged test on %d passing members: %d with the pure Hilbert function (%.0f s)" % (
        key, len(st["passing"]), st["counts"]["pure_hilbert"], time.time() - t0))
    t1 = time.time()
    window = []  # futures of the next members in the order of the index
    queue = list(st["passing"])
    nxt = 0
    st["tables"], st["pure"], st["nonpure_tables"] = 0, 0, {}
    while st["pure"] < R.EARLY_STOP_PURE and st["tables"] < R.MAX_TABLES and (window or nxt < len(queue)):
        while nxt < len(queue) and len(window) < MAX_HEAVY_WORKERS and st["tables"] + len(window) < R.MAX_TABLES:
            m = queue[nxt]
            window.append((m, pool.submit(R.betti_job, {"key": key, "index": m["index"], "e": e, "p": p, "f": m["f"], "g": m["g"]})))
            nxt += 1
        if not window:
            break
        m, job = window.pop(0)
        out = job.result()
        m["betti"], m["pure"], m["length"] = out["betti"], out["pure"], out["length"]
        st["tables"] += 1
        st["pure"] += 1 if out["pure"] else 0
        st["worker_seconds"] += out["seconds"]
        st["table_seconds"] += out["seconds"]
        if not out["pure"]:
            k = "%s, length %s" % (out["betti"], out["length"])
            st["nonpure_tables"][k] = st["nonpure_tables"].get(k, 0) + 1
        log("%s: table %d (member %d, length %s): %s, pure so far %d" % (key, st["tables"], m["index"], out["length"],
            "pure" if out["pure"] else "NOT pure", st["pure"]))
    for _, job in window:  # tables started beyond the stop are dropped (not counted)
        job.cancel()
    st["stopped_early"] = st["pure"] >= R.EARLY_STOP_PURE
    st["tables_cap_reached"] = st["tables"] >= R.MAX_TABLES and not st["stopped_early"]
    st["tables_done"] = True
    st["wall_seconds"] = round(st["wall_seconds"] + time.time() - t0, 1)
    log("%s: %d tables, %d pure (%.0f s)" % (key, st["tables"], st["pure"], time.time() - t1))


def case_record(spec, st):
    e, p = spec["e"], spec["p"]
    members = []
    for m in st["passing"]:
        members.append({"index": m["index"], "alpha": m["alpha"], "scalar": m["scalar"], "beta": m["beta"], "form_c": m["form_c"],
                        "form_cp": m["form_cp"], "c1": m["c1"], "pure_hilbert": m.get("pure_hilbert"), "betti": m.get("betti"),
                        "length": m.get("length"), "pure": m.get("pure"), "f": m["f"], "g": m["g"], "f_text": X.poly_text(e, p, m["f"]),
                        "g_text": X.poly_text(e, p, m["g"])})
    complete = st["counts"]["examined"] >= spec["members"] and st["staged_done"] and st["tables_done"]
    return {"family": spec["family"], "e": e, "p": p, "t": spec["t"], "d": spec["d"], "stratum": spec["stratum"], "nu": spec["nu"],
            "members": spec["members"], "block_ranks": spec["block_ranks"], "status": "complete" if complete else "not finished",
            "examined": st["counts"]["examined"], "blocks": [spec["blocks"], st["next"]], "counts": st["counts"],
            "stage_counts": st["stage_counts"], "tables": st["tables"], "pure": st["pure"], "stopped_early": st["stopped_early"],
            "tables_cap_reached": st["tables_cap_reached"], "nonpure_tables": st["nonpure_tables"], "passing_stored": len(members),
            "passing": members, "worker_seconds": round(st["worker_seconds"], 1), "filter_seconds": round(st["filter_seconds"], 1),
            "staged_seconds": round(st["staged_seconds"], 1), "table_seconds": round(st["table_seconds"], 1), "wall_seconds": st["wall_seconds"],
            "filter_members_per_second_per_worker": int(st["counts"]["examined"] / max(st["filter_seconds"], 1e-9))}


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
    specs = plan(fam, only_pairs())
    used = res["budget"]["used_seconds"]
    left = float(opt("budget-seconds", BUDGET_SECONDS - used))
    t0 = time.time()
    log("family %s: %d cases planned; budget left %.0f s (used %.0f s of %d s); %d workers (%d for the staged test and the tables)" % (
        fam, len(specs), left, used, BUDGET_SECONDS, workers(), MAX_HEAVY_WORKERS))
    rc = 0
    heavy = None
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        for spec in specs:
            if spec["key"] in res["cases"]:
                continue
            if time.time() > t0 + left:
                break
            st = res["partial"].get(spec["key"]) or new_state(spec)
            if not st["filter_done"] and not run_filter(res, spec, pool, t0 + left, save, st):
                save(res)
                log("%s: cut by the time budget, %d members done" % (spec["key"], st["counts"]["examined"]))
                break
            log("%s: filter done: %d members, stages %s, differ %d, passing %d, with (C1) %d (%.0f s of workers)" % (
                spec["key"], st["counts"]["examined"], st["stage_counts"], st["counts"]["differ"], st["counts"]["f3"], st["counts"]["c1"],
                st["filter_seconds"]))
            save(res)
            if heavy is None:
                heavy = ProcessPoolExecutor(max_workers=MAX_HEAVY_WORKERS)
            run_heavy(spec, st, heavy)
            res["cases"][spec["key"]] = case_record(spec, st)
            res["partial"].pop(spec["key"], None)
            save(res)
            c = res["cases"][spec["key"]]
            log("%s: examined %d, F0 %d, F1 %d, F2 %d, F3 %d, (F1) and (F2) differ %d, C1 %d, pure Hilbert %d, tables %d, pure %d (%s), %.0f s" % (
                spec["key"], c["examined"], c["counts"]["f0"], c["counts"]["f1"], c["counts"]["f2"], c["counts"]["f3"], c["counts"]["differ"],
                c["counts"]["c1"], c["counts"]["pure_hilbert"], c["tables"], c["pure"], c["status"], c["wall_seconds"]))
    if heavy is not None:
        heavy.shutdown(wait=True)
    dt = time.time() - t0
    res["budget"]["used_seconds"] = round(used + dt, 1)
    res["runs"].append({"command": "cases", "family": fam, "only": sorted(only_pairs()) if only_pairs() else None, "workers": workers(),
                        "seconds": round(dt, 1)})
    if fam == "K" and all(c["key"] in res["cases"] for c in plan("K")):
        res["gates"]["G1"] = g1_family_part(res)
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
            out += [(spec["key"], m) for m in [m for m in s["passing"] if m.get("pure")][:G2_PER_CASE]]
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
    out_dir = Path(opt("out-dir", "D:/_Temp/bs-exp020-run-2026-11-20/singular_out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    SING.mkdir(parents=True, exist_ok=True)
    sample = g2_sample(res)
    log("G2: %d pure members in the sample (%s)" % (len(sample), version))

    def one(item):
        key, mem = item
        s = res["cases"][key]
        e, p = s["e"], s["p"]
        name = "e%d_p%d_t%d_idx%d" % (e, p, s["t"], mem["index"])
        field = {"name": "GF(%d)" % p, "uhlib_name": "GF(%d)" % p, "char": p, "degree": 1, "modulus": None}
        return name, Sg.run_member(name, field, X.basis_json(e, p, mem["f"], mem["g"]), out_dir, timeout=G2_TIMEOUT)

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
            row["pure_I2"] = t == X.pure_table(e)
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
    spec = importlib.util.spec_from_file_location("exp020_make_summary", HERE / "make_summary.py")
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    res = load()
    res["plan"] = [{k: c[k] for k in ("key", "family", "e", "p", "t", "d", "stratum", "nu", "members", "block_ranks")} for c in order()]
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
