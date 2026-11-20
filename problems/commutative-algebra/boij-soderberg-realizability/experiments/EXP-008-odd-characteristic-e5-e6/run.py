"""EXP-008: the point (1,2,2,1) on (0, e, 3e, 4e) over U(H) at e = 5 over GF(5) and GF(7) and at e = 6 over GF(3).

Run from the repository root, with the repository virtual environment:
    python <this file> gates                   G1 (known answers, EXP-006's first 2,000 spaces of family C) and G3 (pytest); exit 1 on a failure
    python <this file> cases [--only=A,B,C] [--workers=N] [--budget-seconds=N]
                                               resumable by chunk; a family stops once 40 pure spaces are found in it
    python <this file> second [--workers=N]    G2: Singular (Plural, through WSL) on the first 20 pure spaces of every family
    python <this file> table                   totals, shares and the predictions into results.json, then results-summary.md

The hypothesis is hypothesis.md (frozen).  First instrument: exp008_routine.py over EXP-006's routine and `uhlib`.  Second
instrument: Singular 4.3.2 (Plural), exp008_singular.py (the generator of EXP-005).  No machine path is written to any
artifact.  At most 8 worker processes; `cases` stops submitting after the wall-time budget (default 5 hours in total).
"""
import json
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))

import exp008_routine as X  # noqa: E402
import exp008_singular as Sg  # noqa: E402
from exp008_routine import R  # noqa: E402
from uhlib import algebra as A  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
LOG = ART / "run.log"
EXP006 = HERE.parent / "EXP-006-odd-characteristic-below-2e" / "artifacts" / "results.json"
T0 = time.time()
MAX_WORKERS = 8
SAVE_EVERY = 60.0
G2_SAMPLE = 20
FAMILY_ORDER = ("A", "B", "C")


def log(msg):
    line = "[%8.1fs] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-008", "hypothesis": "hypothesis.md (frozen)", "chunks": {}, "gates": {}, "runs": [],
            "family_wall_seconds": {}}


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
def _pair(F, e, f, g):
    return R.coeff_array(F, [[F.from_int(f.get(m, 0)) for m in A.monos(e)], [F.from_int(g.get(m, 0)) for m in A.monos(e)]])


def _g1_chunk_counts(spec):
    """EXP-006's own chunk worker on one of its chunks (family C, e = 5, GF(3))."""
    return R.run_chunk(spec)


def gate_g1():
    rows, bad = [], []
    # (a) the first three pure spaces of EXP-006 at e = 5 over GF(3), rebuilt from their stored bases
    old = json.loads(EXP006.read_text(encoding="utf-8"))
    cs = sorted((c for c in old["chunks"].values() if c["family"] == "C"), key=lambda c: c["start"])
    stored = [sp for c in cs for sp in sorted(c["spaces"], key=lambda s: s["index"]) if sp["pure"] and "basis" in sp][:3]
    F3 = R.make_field("GF(3)")
    for sp in stored:
        C = R.basis_from_json(F3, sp["basis"], 5)
        t, _ = R.betti_table(F3, C, 5)
        rows.append({"case": "EXP-006 family C pure space, index %d (GF(3), e = 5)" % sp["index"], "betti": R.table_rows(t),
                     "expected_pure": True, "ok": t == R.pure_table(5)})
    # (b) the powers x^e, y^e
    for e, fname, expect in ((5, "GF(11)", True), (5, "GF(5)", False), (5, "GF(7)", False), (6, "GF(13)", True),
                             (6, "GF(3)", False)):
        F = R.make_field(fname)
        t, _ = R.betti_table(F, _pair(F, e, {(e, 0, 0): 1}, {(0, e, 0): 1}), e)
        rows.append({"case": "<x^%d, y^%d> over %s" % (e, e, fname), "betti": R.table_rows(t), "expected_pure": expect,
                     "ok": (t == R.pure_table(e)) is expect})
    # (c) the counts of the routine on the first 2,000 spaces of EXP-006's family C against the stored ones
    specs = [s for s in R.chunk_specs(["C"]) if s["end"] <= 2000]
    with ProcessPoolExecutor(max_workers=min(workers(), len(specs))) as pool:
        recs = list(pool.map(_g1_chunk_counts, specs))
    keys = ("n", "rank_hist", "hilbert_computed", "hilbert_other", "pure_hilbert", "pure", "nonpure_tables")
    equal = 0
    for rec in recs:
        ref = old["chunks"][rec["id"]]
        same = all(rec[k] == ref[k] for k in keys) and [s["index"] for s in rec["spaces"]] == [s["index"] for s in ref["spaces"]]
        equal += same
        if not same:
            bad.append({"chunk": rec["id"], "differs": [k for k in keys if rec[k] != ref[k]]})
    tot = {k: sum(r[k] for r in recs) for k in ("n", "pure_hilbert", "pure")}
    rows.append({"case": "EXP-006 family C, first 2,000 spaces: %d chunks recomputed, %d equal to the stored counts" % (len(recs), equal),
                 "recomputed": tot, "ok": equal == len(recs) and tot["n"] == 2000})
    bad += [r for r in rows if not r["ok"]]
    return {"passed": not bad, "cases": rows, "failing_cases": bad}


def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp008.py", "-q"], cwd=str(ROOT),
                          capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def gates_ok(res, names):
    return all(res.get("gates", {}).get(g, {}).get("passed") for g in names)


def cmd_gates():
    ART.mkdir(exist_ok=True)
    res = load()
    t0 = time.time()
    log("gates start")
    failed = None
    for name, fn in (("G1", gate_g1), ("G3", gate_g3)):
        res["gates"].pop(name, None)
        g = fn()
        res["gates"][name] = g
        save(res)
        log("%s %s: %s" % (name, "PASSED" if g["passed"] else "FAILED",
                           json.dumps({k: v for k, v in g.items() if k not in ("passed", "cases")})[:500]))
        if not g["passed"]:
            failed = name
            break
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    if failed:
        log("GATE FAILED: %s; the run stops here; failing cases: %s" % (failed, json.dumps(res["gates"][failed].get("failing_cases"))[:1500]))
        return 1
    log("G1 and G3 passed (G2 is run by `second` after the cases)")
    return 0


# ------------------------------------------------------------------ cases
def family_pure(res, fam):
    return sum(c["pure"] for c in res["chunks"].values() if c["family"] == fam)


def cmd_cases():
    res = load()
    if not gates_ok(res, ("G1", "G3")):
        log("G1 and G3 have not both passed; run `gates` first")
        return 1
    only = [s for s in opt("only", "").split(",") if s]
    budget_end = T0 + float(opt("budget-seconds", 5 * 3600 - 600))
    for fam in FAMILY_ORDER:
        if only and fam not in only:
            continue
        specs = X.chunk_specs([fam])
        es = X.EarlyStop()
        es.add(family_pure(res, fam))
        todo = iter([s for s in specs if s["id"] not in res["chunks"]])
        t0 = time.time()
        log("family %s: %d chunks stored, %d pure so far, early stop %s" % (
            fam, sum(1 for s in specs if s["id"] in res["chunks"]), es.pure, "reached" if es.stopped else "not reached"))
        done_n, last_save = 0, time.time()
        with ProcessPoolExecutor(max_workers=workers()) as pool:
            pending = set()

            def submit_next():
                if es.stopped or time.time() > budget_end:
                    return False
                s = next(todo, None)
                if s is None:
                    return False
                pending.add(pool.submit(X.run_chunk, s))
                return True

            for _ in range(workers() * 2):
                submit_next()
            while pending:
                done, _ = wait(pending, timeout=120, return_when=FIRST_COMPLETED)
                for fut in done:
                    pending.discard(fut)
                    rec = fut.result()
                    res["chunks"][rec["id"]] = rec
                    es.add(rec["pure"])
                    done_n += 1
                    submit_next()
                    if time.time() - last_save > SAVE_EVERY:
                        save(res)
                        last_save = time.time()
                        log("family %s: %d chunks done in this run, %d pure, last %s (%.1f s)" % (fam, done_n, es.pure, rec["id"], rec["seconds"]))
        dt = time.time() - t0
        res["family_wall_seconds"][fam] = round(res["family_wall_seconds"].get(fam, 0) + dt, 1)
        left = sum(1 for s in specs if s["id"] not in res["chunks"])
        res["runs"].append({"command": "cases", "family": fam, "seconds": round(dt, 1), "chunks_done": done_n, "chunks_left": left,
                            "stopped_early": es.stopped})
        save(res)
        log("family %s: %d chunks done now, %d not reached, %d pure, early stop %s, %.1f s" % (
            fam, done_n, left, es.pure, "yes" if es.stopped else "no", dt))
    return 0


# ------------------------------------------------------------------ G2: the second instrument
def ordered_pure(res, fam):
    recs = sorted((c for c in res["chunks"].values() if c["family"] == fam), key=lambda c: c["start"])
    return [sp for c in recs for sp in sorted(c["spaces"], key=lambda s: s["index"]) if sp["pure"]]


def singular_available():
    try:
        p = subprocess.run(["wsl", "-e", "bash", "-c", "Singular -v < /dev/null | head -1"], capture_output=True, text=True, timeout=120)
    except Exception as exc:
        return False, repr(exc)[:200]
    lines = [ln for ln in p.stdout.splitlines() if "Singular" in ln]
    return p.returncode == 0 and bool(lines), lines[0].strip() if lines else p.stderr[:200]


def _g2_one(item):
    fam, sp = item
    F = R.make_field(X.FAMILIES[fam][1])
    name = "%s_%d" % (fam, sp["index"])
    t, dt, err = Sg.run_space(name, R.field_record(F), sp["basis"], SING)
    return name, t, dt, err


def cmd_second():
    res = load()
    t0 = time.time()
    if not gates_ok(res, ("G1", "G3")):
        log("G1 and G3 have not both passed; run `gates` first")
        return 1
    ok, version = singular_available()
    if not ok:
        res["gates"]["G2"] = {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version,
                              "note": "single-instrument results"}
        save(res)
        log("G2 BLOCKED: " + version)
        return 1
    SING.mkdir(parents=True, exist_ok=True)
    sample = [(fam, sp) for fam in FAMILY_ORDER for sp in ordered_pure(res, fam)[:G2_SAMPLE]]
    log("G2: %d pure spaces in the sample (%s)" % (len(sample), version))
    with ThreadPoolExecutor(max_workers=workers()) as tp:
        outs = list(tp.map(_g2_one, sample))
    rows, bad, errors = [], [], []
    for (fam, sp), (name, t, dt, err) in zip(sample, outs):
        e = X.FAMILIES[fam][0]
        row = {"family": fam, "field": X.FAMILIES[fam][1], "index": sp["index"], "script": name + ".sing", "seconds": round(dt, 1)}
        if err or t is None:
            row["error"] = err
            errors.append(name)
        else:
            row["betti_I1"] = sp["betti"]
            row["betti_I2"] = [[i, j, r] for (i, j), r in sorted(t.items())]
            row["agree"] = [tuple(x) for x in sp["betti"]] == [tuple(x) for x in row["betti_I2"]]
            row["pure_I2"] = t == R.pure_table(e)
            if not row["agree"] or not row["pure_I2"]:
                bad.append(name)
        rows.append(row)
    per = {}
    for r in rows:
        per[r["family"]] = per.get(r["family"], 0) + (1 if r.get("agree") and r.get("pure_I2") else 0)
    res["gates"]["G2"] = {"passed": not bad and not errors, "singular": version, "sample_spaces": len(sample),
                          "agree_and_pure_in_I2": sum(per.values()), "per_family": per, "failing_cases": bad,
                          "singular_errors": errors, "rows": rows}
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    save(res)
    g = res["gates"]["G2"]
    log("G2 %s: %d of %d agree; failing %s; errors %s" % ("PASSED" if g["passed"] else "FAILED", g["agree_and_pure_in_I2"], len(sample), bad[:5], errors[:5]))
    return 0 if g["passed"] else 1


# ------------------------------------------------------------------ table
def cmd_table():
    import importlib.util  # EXP-006 has a make_summary.py too and its folder is on sys.path: load ours by path
    spec = importlib.util.spec_from_file_location("exp008_make_summary", HERE / "make_summary.py")
    make_summary = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(make_summary)
    res = load()
    res["totals"] = make_summary.compute_totals(res)
    res["predictions"] = make_summary.predictions(res["totals"])
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
    save(res)
    print(make_summary.totals_text(res["totals"]))
    make_summary.write_summary(res, HERE / "results-summary.md")
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
