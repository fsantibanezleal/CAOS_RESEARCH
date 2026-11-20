"""EXP-017: the pairs (x^e + alpha(xy, z) y, y^e + beta(xy, z) x) for odd e, searched through the filter (F0) to (F3), at (9, 11), (9, 13),
(11, 7) and (13, 5), with controls at (5, 7), (7, 5), (7, 11) and (9, 7).

Run from the repository root, with the repository virtual environment:
    python <this file> gates                       the fixed member of G1 and G3 (pytest's exit code); exit 1 on a failure
    python <this file> throughput [--e 9 --p 11]   members per second per worker of the block test and of the whole case job
    python <this file> cases --family K|Q|X [--only e,p[+e,p]] [--workers N] [--budget-seconds N]
                                                   resumable (progress is stored every 30 s and per case); the early stop is at 5 pure
                                                   members; K is followed by the family part of G1; Q and X need it
    python <this file> second [--workers N] [--out-dir D]
                                                   G2: Singular 4.3.2 (Plural, through WSL) on the first three pure members of each case
    python <this file> table                       predictions P1 to P4 into results.json, then results-summary.md; prints the table

The hypothesis is hypothesis.md (frozen).  The routine of EXP-010 (rank, staged Hilbert test, Betti table) and the Singular generator of
EXP-009 are imported, not edited.  At most 12 worker processes and three hours of wall time in total.  No machine path is written to any
artifact.
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

import exp010_routine as X  # noqa: E402
import exp017_routine as R  # noqa: E402
import numpy as np  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
MAX_WORKERS = 12
BUDGET_SECONDS = 3 * 3600
SAVE_EVERY = 30.0
G2_PER_CASE = 3
FAMILIES = ("K", "Q", "X")
PLAN = {"K": [(5, 7, 200_000), (7, 5, 2_000_000), (7, 11, 20_000_000), (9, 7, 60_000_000)],
        "Q": [(9, 11, 200_000_000), (9, 13, 400_000_000)],
        "X": [(11, 7, 300_000_000), (13, 5, 200_000_000)]}
FIXED = {"e": 9, "p": 7,
         "f": {(9, 0, 0): 4, (4, 5, 0): 5, (3, 4, 1): 6, (2, 3, 2): 3, (1, 2, 3): 5, (0, 1, 4): 3},
         "g": {(5, 4, 0): 1, (4, 3, 1): 3, (3, 2, 2): 2, (2, 1, 3): 2, (1, 0, 4): 6, (0, 9, 0): 4}}
FIXED_TEXT = ("f = 4 x^9 + 5 x^4 y^5 + 6 x^3 y^4 z + 3 x^2 y^3 z^2 + 5 x y^2 z^3 + 3 y z^4, "
              "g = x^5 y^4 + 3 x^4 y^3 z + 2 x^3 y^2 z^2 + 2 x^2 y z^3 + 6 x z^4 + 4 y^9 over GF(7)")


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


# ------------------------------------------------------------------ the plan
def plan(family, only=None):
    """The ordered cases of a family.  The seed index of a case is its position in K, Q, X order (seed = 20261120 + index)."""
    base = {"K": 0, "Q": len(PLAN["K"]), "X": len(PLAN["K"]) + len(PLAN["Q"])}[family]
    out = []
    for k, (e, p, budget) in enumerate(PLAN[family]):
        out.append({"key": "%s|%d|%d" % (family, e, p), "family": family, "e": e, "p": p, "budget": budget, "seed_index": base + k,
                    "seed": R.case_seed(base + k), "blocks": -(-budget // R.BLOCK)})
    return [c for c in out if (c["e"], c["p"]) in only] if only else out


# ------------------------------------------------------------------ the store
def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-017", "hypothesis": "hypothesis.md (frozen)", "cases": {}, "partial": {}, "gates": {}, "runs": [],
            "throughput": {}, "budget": {"used_seconds": 0.0, "limit_seconds": BUDGET_SECONDS}}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
    tmp.replace(RESULTS)


# ------------------------------------------------------------------ gates
def fixed_member(with_betti=False):
    """G1, the fixed member: the pure pair of EXP-014 at (9, 7), rescaled to the form of the stratum, passes the filter."""
    e, p = FIXED["e"], FIXED["p"]
    mons = list(R.A.monos(e))
    f = [FIXED["f"].get(m, 0) for m in mons]
    g = [FIXED["g"].get(m, 0) for m in mons]
    ab = R.alpha_beta_of_pair(e, p, f, g)
    stage, c, cp = R.filter_member(e, p, *ab) if ab else (None, None, None)
    out = {"case": FIXED_TEXT, "alpha": None if ab is None else ab[0], "beta": None if ab is None else ab[1], "filter_stage": stage,
           "c": c, "cp": cp, "pure_hilbert": R.hilbert_pure(e, p, f, g) if ab else None}
    ok = stage == 4 and out["pure_hilbert"] is True
    if with_betti:
        t = X.betti_table(e, p, np.array(f), np.array(g))
        out["betti"] = X.table_rows(t)
        ok = ok and t == X.pure_table(e)
    out["ok"] = bool(ok)
    return out


def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp017.py", "-q"], cwd=str(ROOT), capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def gates_ok(res):
    g = res.get("gates", {})
    return g.get("G1", {}).get("fixed", {}).get("ok") is True and g.get("G3", {}).get("passed") is True


def cmd_gates():
    res = load()
    t0 = time.time()
    fm = fixed_member(with_betti=True)
    res["gates"].setdefault("G1", {})["fixed"] = fm
    log("G1 fixed member: %s (filter stage %s, pure Hilbert %s, Betti %s)" % ("PASSED" if fm["ok"] else "FAILED", fm["filter_stage"],
                                                                              fm["pure_hilbert"], fm.get("betti")))
    ok = fm["ok"]
    if ok:
        g3 = gate_g3()
        res["gates"]["G3"] = g3
        ok = g3["passed"]
        log("G3 %s: %s" % ("PASSED" if ok else "FAILED", g3["last_line"]))
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    return 0 if ok else 1


def k_cases():
    return plan("K")


def g1_family_part(res):
    """G1 after family K: every control finds members that pass the filter and, among them, at least one pure member."""
    rows = []
    for c in k_cases():
        s = res["cases"].get(c["key"])
        rows.append({"pair": [c["e"], c["p"]], "examined": None if s is None else s["counts"]["examined"],
                     "pass_filter": None if s is None else s["counts"]["f3"], "pure": None if s is None else s["pure"],
                     "ok": bool(s and s["counts"]["f3"] > 0 and s["pure"] > 0)})
    return {"passed": all(r["ok"] for r in rows), "rows": rows}


# ------------------------------------------------------------------ throughput
def cmd_throughput():
    e, p = int(opt("e", 9)), int(opt("p", 11))
    idx = {(c["e"], c["p"]): c["seed_index"] for f in FAMILIES for c in plan(f)}.get((e, p), 0)
    res = load()
    blocks = 3
    t0 = time.time()
    outs = [R.block_job({"e": e, "p": p, "seed_index": idx, "block": b, "count": R.BLOCK}) for b in range(blocks)]
    dt = time.time() - t0
    n = sum(o["counts"]["examined"] for o in outs)
    rec = {"e": e, "p": p, "members": n, "seconds": round(dt, 2), "members_per_second_per_worker": int(n / dt),
           "sample_seconds": round(sum(o["sample_seconds"] for o in outs), 2), "block_f1_seconds": round(sum(o["block_seconds"] for o in outs), 2),
           "exact_and_hilbert_seconds": round(dt - sum(o["sample_seconds"] + o["block_seconds"] for o in outs), 2),
           "block_f1_accepted": sum(o["counts"]["block_f1"] for o in outs), "pass_all_four": sum(o["counts"]["f3"] for o in outs),
           "workers_planned": workers(), "members_per_second_planned": int(n / dt * workers())}
    res["throughput"]["%d,%d" % (e, p)] = rec
    save(res)
    log("throughput (%d, %d): %s" % (e, p, json.dumps(rec)))
    return 0


# ------------------------------------------------------------------ cases
def new_state(spec):
    return {"key": spec["key"], "next": 0, "counts": {"examined": 0, "block_f1": 0, "f0": 0, "f1": 0, "f2": 0, "f3": 0, "pure_hilbert": 0,
                                                      "inconsistent": 0},
            "members": [], "tables": 0, "pure": 0, "nonpure_tables": {}, "worker_seconds": 0.0, "wall_seconds": 0.0, "stopped_early": False}


def _block_spec(spec, block):
    count = min(R.BLOCK, spec["budget"] - block * R.BLOCK)
    return {"e": spec["e"], "p": spec["p"], "seed_index": spec["seed_index"], "block": block, "count": count}


def run_case(res, spec, pool, deadline, save_fn):
    """One case on the pool: blocks are aggregated in the order of their index (so the stored state is the state after a prefix of the
    members and a resumed case continues exactly), the staged test is inside each block job, the Betti tables of the members with the pure
    Hilbert function run in the order found until 5 are pure or MAX_TABLES are done.  Returns True when the case finished (all members
    examined, or the early stop), False when the deadline cut it (its state stays in res['partial'])."""
    key = spec["key"]
    st = res["partial"].get(key) or new_state(spec)
    t_start, wall0 = time.time(), st["wall_seconds"]
    nblocks = spec["blocks"]
    submit = st["next"]
    pending, done = {}, {}
    tables = {}
    last_save = time.time()
    closing = False

    def stopped():
        return st["pure"] >= R.EARLY_STOP_PURE

    def may_table():
        return not stopped() and st["tables"] + len(tables) < R.MAX_TABLES

    def snapshot():
        st["wall_seconds"] = round(wall0 + time.time() - t_start, 1)
        res["partial"][key] = st

    while True:
        if not closing and time.time() > deadline:
            closing = True
            log("%s: time budget reached after %d members" % (key, st["counts"]["examined"]))
        stop = stopped()
        # Betti tables first, in the order found
        for mem in st["members"]:
            if len(pending) >= workers() + 2 or not may_table():
                break
            if mem.get("betti") is None and id(mem) not in tables:
                job = pool.submit(R.betti_job, {"key": key, "index": mem["index"], "e": spec["e"], "p": spec["p"], "f": mem["f"], "g": mem["g"]})
                tables[id(mem)] = (job, mem)
                pending[job] = ("t", mem)
        while not closing and not stop and submit < nblocks and len(pending) < workers() + 2:
            job = pool.submit(R.block_job, _block_spec(spec, submit))
            pending[job] = ("b", submit)
            submit += 1
        if not pending:
            break
        finished, _ = wait(set(pending), timeout=5, return_when=FIRST_COMPLETED)
        for fut in finished:
            kind, ref = pending.pop(fut)
            out = fut.result()
            if kind == "t":
                tables.pop(id(ref))
                ref["betti"], ref["pure"] = out["betti"], out["pure"]
                st["tables"] += 1
                st["pure"] += 1 if out["pure"] else 0
                st["worker_seconds"] += out["seconds"]
                if not out["pure"]:
                    k = str(out["betti"])
                    st["nonpure_tables"][k] = st["nonpure_tables"].get(k, 0) + 1
            else:
                done[ref] = out
        while st["next"] in done and not stopped():
            out = done.pop(st["next"])
            for k, v in out["counts"].items():
                st["counts"][k] += v
            st["worker_seconds"] += out["seconds"]
            for mem in out["found"]:
                if len(st["members"]) < R.MAX_STORED:
                    mem.update({"betti": None, "pure": None})
                    st["members"].append(mem)
            st["next"] += 1
        if stopped():
            st["stopped_early"] = True
            closing = True
            done.clear()
        if time.time() - last_save > SAVE_EVERY:
            snapshot()
            save_fn(res)
            last_save = time.time()
            log("%s: %d of %d members, filter F3 %d, pure Hilbert %d, tables %d, pure %d" % (
                key, st["counts"]["examined"], spec["budget"], st["counts"]["f3"], st["counts"]["pure_hilbert"], st["tables"], st["pure"]))
    # blocks completed out of order beyond the prefix at the cut are dropped (not counted); the prefix is what is stored
    snapshot()
    finished_case = st["stopped_early"] or st["next"] >= nblocks
    cands_left = any(m["betti"] is None for m in st["members"]) and may_table_after(st)
    if finished_case and not cands_left:
        res["cases"][key] = case_record(spec, st)
        res["partial"].pop(key, None)
        return True
    return False


def may_table_after(st):
    return not st["stopped_early"] and st["tables"] < R.MAX_TABLES


def case_record(spec, st):
    e, p = spec["e"], spec["p"]
    members = []
    for m in st["members"]:
        members.append({"index": m["index"], "alpha": m["alpha"], "beta": m["beta"], "c": m["c"], "cp": m["cp"], "f": m["f"], "g": m["g"],
                        "f_text": X.poly_text(e, p, m["f"]), "g_text": X.poly_text(e, p, m["g"]), "betti": m["betti"], "pure": m["pure"]})
    return {"family": spec["family"], "e": e, "p": p, "budget": spec["budget"], "seed": spec["seed"], "seed_index": spec["seed_index"],
            "examined": st["counts"]["examined"], "complete": st["counts"]["examined"] >= spec["budget"], "stopped_early": st["stopped_early"],
            "blocks": [spec["blocks"], st["next"]], "counts": st["counts"], "tables": st["tables"], "pure": st["pure"],
            "tables_cap_reached": st["tables"] >= R.MAX_TABLES and not st["stopped_early"], "nonpure_tables": st["nonpure_tables"],
            "members_stored": len(members), "members": members, "worker_seconds": round(st["worker_seconds"], 1),
            "wall_seconds": st["wall_seconds"],
            "members_per_second_per_worker": int(st["counts"]["examined"] / max(st["worker_seconds"], 1e-9))}


def cmd_cases():
    res = load()
    if not gates_ok(res):
        log("the fixed member of G1 and G3 have not both passed; run `gates` first")
        return 1
    fam = opt("family", "")
    if fam not in FAMILIES:
        log("--family K|Q|X is required")
        return 2
    if fam != "K" and not res["gates"].get("G1", {}).get("family", {}).get("passed"):
        log("family K has not passed the family part of G1; run `cases --family K` first")
        return 1
    only = R10.pair_list()
    specs = plan(fam, only)
    used = res["budget"]["used_seconds"]
    left = float(opt("budget-seconds", BUDGET_SECONDS - used))
    t0 = time.time()
    log("family %s: %d cases planned; budget left %.0f s (used %.0f s of %d s)" % (fam, len(specs), left, used, BUDGET_SECONDS))
    rc = 0
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        for spec in specs:
            if spec["key"] in res["cases"]:
                continue
            if time.time() > t0 + left:
                break
            ok = run_case(res, spec, pool, t0 + left, save)
            save(res)
            if ok:
                c = res["cases"][spec["key"]]
                log("%s: examined %d, F0 %d, F1 %d, F2 %d, F3 %d, pure Hilbert %d, tables %d, pure %d%s, %.0f s" % (
                    spec["key"], c["examined"], c["counts"]["f0"], c["counts"]["f1"], c["counts"]["f2"], c["counts"]["f3"],
                    c["counts"]["pure_hilbert"], c["tables"], c["pure"], " (early stop)" if c["stopped_early"] else "", c["wall_seconds"]))
            else:
                log("%s: cut by the time budget, %d members done" % (spec["key"], res["partial"][spec["key"]]["counts"]["examined"]))
                break
    dt = time.time() - t0
    res["budget"]["used_seconds"] = round(used + dt, 1)
    res["runs"].append({"command": "cases", "family": fam, "only": opt("only", None), "workers": workers(), "seconds": round(dt, 1)})
    if fam == "K" and all(c["key"] in res["cases"] for c in k_cases()):
        res["gates"].setdefault("G1", {})["family"] = g1_family_part(res)
        ok = res["gates"]["G1"]["family"]["passed"]
        log("G1 (family part) %s" % ("PASSED" if ok else "FAILED: " + json.dumps([r for r in res["gates"]["G1"]["family"]["rows"] if not r["ok"]])))
        rc = 0 if ok else 1
    save(res)
    log("family %s: %d of %d cases stored; %.0f s this run" % (fam, sum(1 for c in specs if c["key"] in res["cases"]), len(specs), dt))
    return rc


# ------------------------------------------------------------------ G2
def g2_sample(res):
    """The first three pure members of every case that has one."""
    out = []
    for key, s in sorted(res["cases"].items(), key=lambda kv: ("KQX".index(kv[1]["family"]), kv[1]["e"], kv[1]["p"])):
        out += [(key, m) for m in [m for m in s["members"] if m["pure"]][:G2_PER_CASE]]
    return out


def cmd_second():
    import exp009_singular as Sg
    res = load()
    t0 = time.time()
    if not gates_ok(res):
        log("the fixed member of G1 and G3 have not both passed; run `gates` first")
        return 1
    ok, version = R10.singular_available()
    if not ok:
        res["gates"]["G2"] = {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version,
                              "note": "single-instrument results"}
        save(res)
        log("G2 BLOCKED: " + version)
        return 1
    out_dir = Path(opt("out-dir", "D:/_Temp/bs-exp017-2026-11-20/singular_out"))
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
        return name, Sg.run_member(name, field, X.basis_json(e, p, mem["f"], mem["g"]), out_dir)

    with ThreadPoolExecutor(max_workers=min(8, workers())) as tp:
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
    res["gates"]["G2"] = {"passed": not bad and not errors, "singular": version, "sample_members": len(sample), "agree_and_pure_in_I2": agree,
                          "failing_cases": bad, "singular_errors": errors, "rows": rows}
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    save(res)
    log("G2 %s: %d of %d agree and are pure in both instruments; failing %s; errors %s" % (
        "PASSED" if res["gates"]["G2"]["passed"] else "FAILED", agree, len(sample), bad[:5], errors[:5]))
    return 0 if res["gates"]["G2"]["passed"] else 1


# ------------------------------------------------------------------ table
def cmd_table():
    spec = importlib.util.spec_from_file_location("exp017_make_summary", HERE / "make_summary.py")
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    res = load()
    res["totals"] = ms.compute_totals(res)
    res["predictions"] = ms.predictions(res)
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
    save(res)
    print(ms.totals_text(res["totals"]))
    ms.write_summary(res, HERE / "results-summary.md")
    log("table written")
    return 0


def main():
    fn = {"gates": cmd_gates, "throughput": cmd_throughput, "cases": cmd_cases, "second": cmd_second, "table": cmd_table}.get(
        sys.argv[1] if len(sys.argv) > 1 else "")
    if fn is None:
        print(__doc__)
        return 2
    ART.mkdir(exist_ok=True)
    return fn()


if __name__ == "__main__":
    sys.exit(main())
