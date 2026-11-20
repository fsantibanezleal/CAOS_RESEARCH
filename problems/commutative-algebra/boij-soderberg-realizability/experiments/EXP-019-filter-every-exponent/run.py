"""EXP-019: the pairs (x^e + alpha(xy, z) y^t, y^e + beta(xy, z) x^t) searched through the filter (F0) to (F3) written for every exponent t,
at the open pairs (13, 7), (13, 11), (14, 5), (14, 11) and nine open pairs with e = 15, 16, with controls on four settled pairs.

Run from the repository root, with the repository virtual environment:
    python <this file> gates                       G3 (pytest's exit code) and G1 (a) on the stored members; exit 1 on a failure
    python <this file> cases --family K|X|Y [--only e,p] [--only e,p ...] [--workers N] [--budget-seconds N]
                                                   resumable (progress is stored every 30 s and per case); the early stop is at 5 pure
                                                   members; K is followed by the family part of G1 (b); X and Y need it
    python <this file> second [--workers N] [--out-dir D]
                                                   G2: Singular 4.3.2 (Plural, through WSL) on the first three pure members of each case
    python <this file> table                       predictions P1 to P5 into results.json, then results-summary.md; prints the table

The hypothesis is hypothesis.md (frozen).  The routine of EXP-010 (rank, staged Hilbert test, Betti table) and the Singular generator of
EXP-009 are imported, not edited.  At most 12 worker processes and five hours of wall time in total.  No machine path is written to any
artifact.  The order of the run of the hypothesis is `order()`; `plan(family)` lists the cases of a family in the order of its table.
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

import exp019_routine as R  # noqa: E402  (imports the routine of EXP-010 and sets the cache of tensors to 4 entries)

X = R.X

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
MAX_WORKERS = 12
BUDGET_SECONDS = 5 * 3600
SAVE_EVERY = 30.0
G2_PER_CASE = 3
G2_TIMEOUT = 1200  # seconds: a member that Singular does not finish in twenty minutes is checked by one instrument only
FAMILIES = ("K", "X", "Y")
# (e, p, t, budget) in the order of the tables of hypothesis.md; the seed index is the position in K, X, Y order (K 0-3, X 4-7, Y 8-16)
PLAN = {"K": [(9, 11, 5, 100_000), (9, 13, 3, 2_000_000), (11, 17, 7, 100_000), (13, 17, 7, 5_000_000)],
        "X": [(13, 11, 5, 300_000_000), (13, 7, 3, 1_000_000_000), (14, 5, 2, 1_500_000_000), (14, 11, 4, 3_000_000_000)],
        "Y": [(15, 29, 13, 200_000), (16, 29, 14, 200_000), (16, 31, 14, 200_000), (15, 23, 11, 1_000_000), (15, 19, 9, 50_000_000),
              (16, 23, 10, 50_000_000), (15, 17, 7, 1_500_000_000), (16, 17, 8, 1_500_000_000), (16, 19, 8, 2_000_000_000)]}
# the order of the run of the hypothesis: K; the six cases of Y with d <= 3; X in the order (13, 11), (13, 7), (14, 5); the three cases
# of Y with d = 4; (14, 11) last
ORDER = [("K", 9, 11), ("K", 9, 13), ("K", 11, 17), ("K", 13, 17), ("Y", 15, 29), ("Y", 16, 29), ("Y", 16, 31), ("Y", 15, 23),
         ("Y", 15, 19), ("Y", 16, 23), ("X", 13, 11), ("X", 13, 7), ("X", 14, 5), ("Y", 15, 17), ("Y", 16, 17), ("Y", 16, 19),
         ("X", 14, 11)]


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
def block_size(d):
    """Members per block: small blocks where a large share of the members passes (d = 1), so that a case stops soon after its fifth pure
    member; larger blocks where the filter is the whole cost."""
    return 256 if d == 1 else (1 << 14 if d == 2 else (1 << 16 if d == 3 else 1 << 18))


def plan(family, only=None):
    """The cases of a family in the order of its table.  The seed index of a case is its position in K, X, Y order (seed = 20261120 + index)."""
    base = {"K": 0, "X": len(PLAN["K"]), "Y": len(PLAN["K"]) + len(PLAN["X"])}[family]
    out = []
    for k, (e, p, t, budget) in enumerate(PLAN[family]):
        d = (e - t) // 2
        bs = block_size(d)
        out.append({"key": "%s|%d|%d" % (family, e, p), "family": family, "e": e, "p": p, "t": t, "d": d, "stratum": list(R.stratum(e, t)),
                    "budget": budget, "seed_index": base + k, "seed": R.case_seed(base + k), "block_size": bs, "blocks": -(-budget // bs)})
    return [c for c in out if (c["e"], c["p"]) in only] if only else out


def order():
    """Every case in the order of the run of the hypothesis."""
    by = {c["key"]: c for fam in FAMILIES for c in plan(fam)}
    return [by["%s|%d|%d" % o] for o in ORDER]


def case_by_key(key):
    return next(c for c in order() if c["key"] == key)


# ------------------------------------------------------------------ the store
def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-019", "hypothesis": "hypothesis.md (frozen)", "cases": {}, "partial": {}, "gates": {}, "runs": [],
            "budget": {"used_seconds": 0.0, "limit_seconds": BUDGET_SECONDS}}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
    tmp.replace(RESULTS)


# ------------------------------------------------------------------ gates
def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp019.py", "-q"], cwd=str(ROOT), capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def gates_ok(res):
    g = res.get("gates", {})
    return g.get("G1", {}).get("stored", {}).get("ok") is True and g.get("G3", {}).get("passed") is True


def cmd_gates():
    res = load()
    t0 = time.time()
    rec = R.stored_members_record()
    res["gates"].setdefault("G1", {})["stored"] = rec
    log("G1 (a), stored members: %d pure (by stage %s), %d other (by stage %s), %d not of the form; probe counts %s; %s" % (
        rec["pure"], rec["pure_by_stage"], rec["other"], rec["other_by_stage"], rec["not_of_the_form"], rec["probe_counts"],
        "PASSED" if rec["ok"] else "FAILED"))
    g3 = gate_g3()
    res["gates"]["G3"] = g3
    log("G3 %s: %s" % ("PASSED" if g3["passed"] else "FAILED", g3["last_line"]))
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    return 0 if rec["ok"] and g3["passed"] else 1


def g1_family_part(res):
    """G1 (b) after family K: every control holds a pure member."""
    rows = []
    for c in plan("K"):
        s = res["cases"].get(c["key"])
        rows.append({"pair": [c["e"], c["p"]], "t": c["t"], "examined": None if s is None else s["examined"],
                     "pass_filter": None if s is None else s["counts"]["f3"], "pure": None if s is None else s["pure"],
                     "ok": bool(s and s["pure"] > 0)})
    return {"passed": all(r["ok"] for r in rows), "rows": rows}


# ------------------------------------------------------------------ cases
def new_state(spec):
    return {"key": spec["key"], "next": 0, "counts": {"examined": 0, "f0": 0, "f1": 0, "f2": 0, "f3": 0, "pure_hilbert": 0},
            "members": [], "tables": 0, "pure": 0, "nonpure_tables": {}, "worker_seconds": 0.0, "filter_seconds": 0.0, "staged_seconds": 0.0,
            "table_seconds": 0.0, "wall_seconds": 0.0, "stopped_early": False}


def _block_spec(spec, block):
    count = min(spec["block_size"], spec["budget"] - block * spec["block_size"])
    return {"e": spec["e"], "p": spec["p"], "t": spec["t"], "seed_index": spec["seed_index"], "block": block, "count": count,
            "block_size": spec["block_size"]}


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
    nw = workers()

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
        for mem in st["members"]:  # Betti tables first, in the order found
            if len(pending) >= nw + 2 or not may_table():
                break
            if mem.get("betti") is None and id(mem) not in tables:
                job = pool.submit(R.betti_job, {"key": key, "index": mem["index"], "e": spec["e"], "p": spec["p"], "f": mem["f"], "g": mem["g"]})
                tables[id(mem)] = (job, mem)
                pending[job] = ("t", mem)
        while not closing and not stop and submit < nblocks and len(pending) < nw + 2:
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
                st["table_seconds"] += out["seconds"]
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
            st["filter_seconds"] += out["filter_seconds"]
            st["staged_seconds"] += out["staged_seconds"]
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
            log("%s: %d of %d members, F3 %d, pure Hilbert %d, tables %d, pure %d" % (
                key, st["counts"]["examined"], spec["budget"], st["counts"]["f3"], st["counts"]["pure_hilbert"], st["tables"], st["pure"]))
    # blocks completed out of order beyond the prefix at the cut are dropped (not counted); the prefix is what is stored
    snapshot()
    finished_case = st["stopped_early"] or st["next"] >= nblocks
    cands_left = any(m["betti"] is None for m in st["members"]) and not st["stopped_early"] and st["tables"] < R.MAX_TABLES
    if finished_case and not cands_left:
        res["cases"][key] = case_record(spec, st)
        res["partial"].pop(key, None)
        return True
    return False


def case_record(spec, st):
    e, p = spec["e"], spec["p"]
    members = []
    for m in st["members"]:
        members.append({"index": m["index"], "alpha": m["alpha"], "beta": m["beta"], "c": m["c"], "cp": m["cp"], "f": m["f"], "g": m["g"],
                        "f_text": X.poly_text(e, p, m["f"]), "g_text": X.poly_text(e, p, m["g"]), "betti": m["betti"], "pure": m["pure"]})
    complete = st["counts"]["examined"] >= spec["budget"]
    return {"family": spec["family"], "e": e, "p": p, "t": spec["t"], "d": spec["d"], "stratum": spec["stratum"], "budget": spec["budget"],
            "seed": spec["seed"], "seed_index": spec["seed_index"], "block_size": spec["block_size"],
            "status": "early stop" if st["stopped_early"] else ("complete" if complete else "not finished"),
            "examined": st["counts"]["examined"], "blocks": [spec["blocks"], st["next"]], "counts": st["counts"], "tables": st["tables"],
            "pure": st["pure"], "tables_cap_reached": st["tables"] >= R.MAX_TABLES and not st["stopped_early"],
            "nonpure_tables": st["nonpure_tables"], "members_stored": len(members), "members": members,
            "worker_seconds": round(st["worker_seconds"], 1), "filter_seconds": round(st["filter_seconds"], 1),
            "staged_seconds": round(st["staged_seconds"], 1), "table_seconds": round(st["table_seconds"], 1), "wall_seconds": st["wall_seconds"],
            "filter_members_per_second_per_worker": int(st["counts"]["examined"] / max(st["filter_seconds"], 1e-9))}


def cmd_cases():
    res = load()
    if not gates_ok(res):
        log("G1 (a) and G3 have not both passed; run `gates` first")
        return 1
    fam = opt("family", "")
    if fam not in FAMILIES:
        log("--family K|X|Y is required")
        return 2
    if fam != "K" and not res["gates"].get("G1", {}).get("family", {}).get("passed"):
        log("family K has not passed G1 (b); run `cases --family K` first")
        return 1
    specs = plan(fam, only_pairs())
    if fam != "K":
        specs = sorted(specs, key=lambda c: ORDER.index((c["family"], c["e"], c["p"])))
    used = res["budget"]["used_seconds"]
    left = float(opt("budget-seconds", BUDGET_SECONDS - used))
    t0 = time.time()
    log("family %s: %d cases planned; budget left %.0f s (used %.0f s of %d s); %d workers" % (fam, len(specs), left, used, BUDGET_SECONDS,
                                                                                                  workers()))
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
                log("%s: examined %d, F0 %d, F1 %d, F2 %d, F3 %d, pure Hilbert %d, tables %d, pure %d (%s), %.0f s" % (
                    spec["key"], c["examined"], c["counts"]["f0"], c["counts"]["f1"], c["counts"]["f2"], c["counts"]["f3"],
                    c["counts"]["pure_hilbert"], c["tables"], c["pure"], c["status"], c["wall_seconds"]))
            else:
                log("%s: cut by the time budget, %d members done" % (spec["key"], res["partial"][spec["key"]]["counts"]["examined"]))
                break
    dt = time.time() - t0
    res["budget"]["used_seconds"] = round(used + dt, 1)
    res["runs"].append({"command": "cases", "family": fam, "only": sorted(only_pairs()) if only_pairs() else None, "workers": workers(),
                        "seconds": round(dt, 1)})
    if fam == "K" and all(c["key"] in res["cases"] for c in plan("K")):
        res["gates"].setdefault("G1", {})["family"] = g1_family_part(res)
        ok = res["gates"]["G1"]["family"]["passed"]
        log("G1 (b) %s" % ("PASSED" if ok else "FAILED: " + json.dumps([r for r in res["gates"]["G1"]["family"]["rows"] if not r["ok"]])))
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
            out += [(spec["key"], m) for m in [m for m in s["members"] if m["pure"]][:G2_PER_CASE]]
    return out


def cmd_second():
    import exp009_singular as Sg
    res = load()
    t0 = time.time()
    if not gates_ok(res):
        log("G1 (a) and G3 have not both passed; run `gates` first")
        return 1
    ok, version = R10.singular_available()
    if not ok:
        res["gates"]["G2"] = {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version,
                              "note": "single-instrument results"}
        save(res)
        log("G2 BLOCKED: " + version)
        return 1
    out_dir = Path(opt("out-dir", "D:/_Temp/bs-exp019-2026-11-20/singular_out"))
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
    res["gates"]["G2"] = {"passed": not bad and not errors, "singular": version, "timeout_seconds": G2_TIMEOUT, "sample_members": len(sample),
                          "agree_and_pure_in_I2": agree, "failing_cases": bad, "singular_errors": errors, "rows": rows}
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    save(res)
    log("G2 %s: %d of %d agree and are pure in both instruments; failing %s; errors %s" % (
        "PASSED" if res["gates"]["G2"]["passed"] else "FAILED", agree, len(sample), bad[:5], errors[:5]))
    return 0 if res["gates"]["G2"]["passed"] else 1


# ------------------------------------------------------------------ table
def cmd_table():
    spec = importlib.util.spec_from_file_location("exp019_make_summary", HERE / "make_summary.py")
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    res = load()
    res["plan"] = [{k: c[k] for k in ("key", "family", "e", "p", "t", "d", "stratum", "budget", "seed", "seed_index", "block_size")}
                   for c in order()]
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
