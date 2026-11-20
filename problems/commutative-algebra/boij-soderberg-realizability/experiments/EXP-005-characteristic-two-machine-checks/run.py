"""EXP-005: the machine checks of the characteristic 2 theorem and of the family U/U(x^e, y^e) at e = 6, 7.

Run from the repository root, with the repository virtual environment:
    python <this file> gates [--workers=N]            G1, G2, G4 (pytest) and G3 (Singular); exit 1 and the failing cases on a failure
    python <this file> cases [--only=C1a,C2b,C3,C4] [--workers=N] [--limit-seconds=1200] [--budget-seconds=14400]
    python <this file> table                          totals per family and prediction into results.json, then make_summary.py

The hypothesis is hypothesis.md (frozen).  First instrument: exp005_routine.py over `uhlib`.  Second instrument: Singular
(Plural) through WSL, exp005_singular.py (no shared arithmetic code).  Environment: EXP005_SCRATCH (scratch folder, default
none needed), no machine path is written to any artifact.  Resumable: finished cases stay in artifacts/results.json.
At most 8 worker processes, at most 20 minutes per case, at most 4 hours per `cases` command.
"""
import json
import random
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))

import exp005_routine as R  # noqa: E402
import exp005_singular as Sg  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import tor  # noqa: E402
from uhlib.fastmod import quotient_module_np  # noqa: E402
from uhlib.module import quotient_module  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
LOG = ART / "run.log"
EXP003 = HERE.parent / "EXP-003-heisenberg-characteristic-two" / "artifacts" / "results.json"
T0 = time.time()
MAX_WORKERS = 8
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
C4_FIELDS = ["QQ"] + ["GF(%d)" % p for p in PRIMES]
G2_SHAPES = ((1, 2, 3), (1, 2, 4), (2, 3, 2), (1, 3, 2))
G2_FIELDS = ("GF(2)", "GF(2^2)", "GF(2^4)", "GF(32003)")
# G3 sample, as the hypothesis fixes it: (family, field, first n cases)
G3_SAMPLE = [("C2a", "GF(2)", 10), ("C2a", "GF(2^2)", 10), ("C2e", "GF(2)", 10), ("C2b", "GF(2^4)", 5), ("C3", "GF(2^4)", 40)]


def log(msg):
    line = "[%8.1fs] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-005", "hypothesis": "hypothesis.md (frozen)", "cases": {}, "c4": {}, "gates": {}, "runs": []}


def save(res):
    ART.mkdir(exist_ok=True)
    RESULTS.write_text(json.dumps(res, indent=1), encoding="utf-8")


def opt(name, default):
    for a in sys.argv[2:]:
        if a.startswith("--%s=" % name):
            return a.split("=", 1)[1]
    return default


def workers():
    return min(MAX_WORKERS, int(opt("workers", MAX_WORKERS)))


def spec_by_id():
    return {s["id"]: s for s in R.case_specs()}


def chunks(specs, size=20):
    for i in range(0, len(specs), size):
        yield specs[i:i + size]


# ------------------------------------------------------------------ cases
def compute_cases(res, specs, limit, budget_end, stop_on_finite=True, label=""):
    """Run the specs not yet stored through a pool; store each finished chunk.  Returns the stopping record or None."""
    todo = [s for s in specs if s["id"] not in res["cases"]]
    log("%s: %d cases to compute, %d already stored" % (label, len(todo), len(specs) - len(todo)))
    if not todo:
        return None
    # the heaviest degree bounds first
    todo.sort(key=lambda s: (-s["D"], s["id"]))
    batches = list(chunks(todo, 10))
    stop = None
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        pending, it = set(), iter(batches)

        def submit_next():
            if time.time() > budget_end:
                return False
            b = next(it, None)
            if b is None:
                return False
            pending.add(pool.submit(R.run_chunk, b, limit))
            return True

        for _ in range(workers() * 2):
            submit_next()
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for fut in done:
                pending.discard(fut)
                for rec in fut.result():
                    res["cases"][rec["id"]] = rec
                    if stop_on_finite and rec["status"] == "done" and rec["cls"] == R.FINITE and rec["family"] != "C3":
                        stop = stop or rec
                save(res)
                if stop is None:
                    submit_next()
            if stop is not None:
                for f in pending:
                    f.cancel()
        # cancelled futures are dropped; running ones finish and are stored by the loop above
    left = len([s for s in specs if s["id"] not in res["cases"]])
    log("%s: %d cases stored in total, %d not reached" % (label, len(specs) - left, left))
    return stop


# ------------------------------------------------------------------ C4
def c4_i1(e, fname):
    """First instrument for U/U(x^e, y^e): module by uhlib and Betti table through Tor (as EXP-003, claim C3)."""
    F = R.make_field(fname)
    gens = [{(0, (e, 0, 0)): F.one}, {(0, (0, e, 0)): F.one}]
    maxdeg = 4 * e + 8
    t0 = time.time()
    M = (quotient_module if fname == "QQ" else quotient_module_np)(F, [0], gens, maxdeg=maxdeg)
    expected = {(0, 0): 1, (1, e): 2, (2, 3 * e): 2, (3, 4 * e): 1}
    dims = list(M.dims) + [0] * (maxdeg + 1 - len(M.dims))
    pure_hf = [A.dim_U(n) - 2 * A.dim_U(n - e) + 2 * A.dim_U(n - 3 * e) - A.dim_U(n - 4 * e) for n in range(maxdeg + 1)]
    b1 = tor.betti(M) if M.finished else None
    return {"id": "C4|%s|e%d" % (fname, e), "family": "C4", "field": fname, "e": e, "degree_bound": maxdeg,
            "relations": [R.rel_to_json(F, g) for g in gens], "finite_length": bool(M.finished), "hilbert": dims,
            "hilbert_equals_pure_prediction": dims == pure_hf,
            "betti_I1": [[i, j, r] for (i, j), r in sorted(b1.items())] if b1 is not None else None,
            "pure_table_I1": bool(b1 == expected), "seconds_I1": round(time.time() - t0, 1)}


def c4_i2(rec):
    """Second instrument: Singular's table from the stored relations; recorded next to I1."""
    F = R.make_field(rec["field"])
    rels_json = [[[k, list(m), c] for k, m, c in r] for r in rec["relations"]]
    fr = R.field_record(F)
    b2, dt, err = Sg.run_case("C4_%s_e%d" % (rec["field"], rec["e"]), fr, 1, rels_json, SING)
    rec["seconds_I2"] = round(dt, 1)
    expected = {(0, 0): 1, (1, rec["e"]): 2, (2, 3 * rec["e"]): 2, (3, 4 * rec["e"]): 1}
    if err or b2 is None:
        rec["I2_error"] = err
        rec["betti_I2"] = None
        rec["pure_table_I2"] = None
        rec["hilbert_consistent_I2"] = None
        return rec
    rec["betti_I2"] = [[i, j, r] for (i, j), r in sorted(b2.items())]
    rec["pure_table_I2"] = b2 == expected
    rec["hilbert_consistent_I2"] = Sg.hilbert_from_table(b2, rec["degree_bound"]) == rec["hilbert"]
    if rec["betti_I1"] is not None:
        rec["tables_agree"] = [tuple(t) for t in rec["betti_I1"]] == [tuple(t) for t in rec["betti_I2"]]
    else:
        rec["tables_agree"] = None  # I1 has no table for an infinite length module; compared through the Hilbert function
    return rec


def compute_c4(res):
    todo = [(e, f) for e in (6, 7) for f in C4_FIELDS if "C4|%s|e%d" % (f, e) not in res["c4"]]
    log("C4: %d modules to compute" % len(todo))
    if not todo:
        return
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        futs = [pool.submit(c4_i1, e, f) for e, f in todo]
        recs = [f.result() for f in futs]
    with ThreadPoolExecutor(max_workers=workers()) as tp:
        recs = list(tp.map(c4_i2, recs))
    for r in recs:
        res["c4"][r["id"]] = r
    save(res)
    log("C4: %d modules stored" % len(res["c4"]))


# ------------------------------------------------------------------ gates
def gate_g1(res):
    specs = [s for s in R.case_specs() if s["family"] == "C1a"]
    compute_cases(res, specs, 1200, time.time() + 3600, stop_on_finite=False, label="G1 (C1a)")
    old = json.loads(EXP003.read_text(encoding="utf-8"))["tasks"]["A1:GF(2):0"]["records"]
    bad, same_basis = [], 0
    for rec in old:
        mine = res["cases"][R.case_id("C1a", "GF(2)", rec["index"])]
        theirs = rec["hilbert_0_to_20"]
        k = min(len(mine["hilbert"]), len(theirs))
        basis_old = sorted([sorted((tuple(m), int(c)) for m, c in poly) for poly in rec["basis"]])
        basis_new = sorted([sorted((tuple(m), int(c)) for _, m, c in rel) for rel in mine["relations"]])
        same_basis += basis_old == basis_new
        if mine["hilbert"][:k] != theirs[:k] or k != 19:
            bad.append(rec["index"])
    return {"passed": not bad and same_basis == 35 and len(old) == 35, "compared": len(old), "degrees_compared": 19,
            "same_subspace_as_EXP003": same_basis, "failing_cases": bad}


def _g2_one(args):
    fname, shape, idx = args
    F = R.make_field(fname)
    a, b, e = shape
    rels = R.random_relations(F, a, b, e, R.SEED_BASE + idx)
    mine = R.hilbert_function(F, a, rels, 12)
    M = quotient_module(F, [0] * a, rels, maxdeg=12)
    theirs = list(M.dims) + [0] * (13 - len(M.dims))
    ok_np = None
    if fname != "QQ":
        Mn = quotient_module_np(F, [0] * a, rels, maxdeg=12, with_action=False)
        ok_np = (list(Mn.dims) + [0] * (13 - len(Mn.dims))) == mine
    return {"field": fname, "shape": list(shape), "index": idx, "equal_uhlib_python": mine == theirs,
            "equal_uhlib_numpy": ok_np, "hilbert": mine}


def gate_g2(res):
    jobs = [(f, s, i) for f in G2_FIELDS for s in G2_SHAPES for i in range(10)]
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        out = list(pool.map(_g2_one, jobs, chunksize=4))
    bad = [(o["field"], o["shape"], o["index"]) for o in out if not o["equal_uhlib_python"] or o["equal_uhlib_numpy"] is False]
    return {"passed": not bad and len(out) == 160, "compared": len(out), "degrees": "0..12",
            "per_field": {f: sum(o["equal_uhlib_python"] for o in out if o["field"] == f) for f in G2_FIELDS},
            "failing_cases": bad}


def gate_g4():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp005.py", "-q"], cwd=str(ROOT),
                          capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def singular_available():
    try:
        p = subprocess.run(["wsl", "-e", "bash", "-c", "which Singular && Singular -v < /dev/null | head -1"],
                           capture_output=True, text=True, timeout=120)
    except Exception as exc:
        return False, repr(exc)[:200]
    return p.returncode == 0, p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[:200]


def _g3_case(rec):
    fr = rec["field_record"]
    rels = [[[k, list(m), c] for k, m, c in r] for r in rec["relations"]]
    try:
        b2, dt, err = Sg.run_case(rec["id"], fr, rec["a"], rels, SING)
    except ValueError as exc:  # all relations zero: the module is free, nothing to resolve
        return rec["id"], None, 0.0, str(exc)
    return rec["id"], b2, dt, err


def gate_g3(res, limit, budget_end):
    ok, version = singular_available()
    if not ok:
        return {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version}
    sample = []
    by_id = spec_by_id()
    for fam, fname, n in G3_SAMPLE:
        ids = [R.case_id(fam, fname, i) for i in range(n)]
        sample += [by_id[i] for i in ids]
    compute_cases(res, sample, limit, budget_end, stop_on_finite=False, label="G3 sample (first instrument)")
    recs = [res["cases"][s["id"]] for s in sample]
    unfinished = [r["id"] for r in recs if r["status"] != "done"]
    with ThreadPoolExecutor(max_workers=workers()) as tp:
        outs = list(tp.map(_g3_case, [r for r in recs if r["status"] == "done"]))
    compare = {}
    bad, errors = [], []
    for cid, b2, dt, err in outs:
        rec = res["cases"][cid]
        if err or b2 is None:
            errors.append([cid, err])
            continue
        h2 = Sg.hilbert_from_table(b2, rec["D"])
        same = h2 == rec["hilbert"]
        rec["betti_I2"] = [[i, j, r] for (i, j), r in sorted(b2.items())]
        rec["hilbert_equals_I2"] = same
        compare[cid] = same
        if not same:
            bad.append(cid)
    save(res)
    compute_c4(res)
    c4 = res["c4"]
    c4_bad = [k for k, r in c4.items() if r.get("betti_I2") is None or not r.get("hilbert_consistent_I2")
              or r.get("tables_agree") is False or (r["pure_table_I1"] != (r.get("pure_table_I2") is True))]
    per_sample = {"%s|%s|first %d" % (fam, f, n): sum(1 for i in range(n) if compare.get(R.case_id(fam, f, i)) is True)
                  for fam, f, n in G3_SAMPLE}
    passed = not bad and not errors and not unfinished and not c4_bad and len(c4) == 24
    return {"passed": passed, "singular": version, "sample_cases": len(sample), "agree": sum(compare.values()),
            "per_sample": per_sample, "failing_cases": bad, "singular_errors": errors, "unfinished": unfinished,
            "c4_modules": len(c4), "c4_failing": c4_bad,
            "c4_i1_i2_tables_agree": sum(1 for r in c4.values() if r.get("tables_agree") is True),
            "c4_i2_hilbert_consistent": sum(1 for r in c4.values() if r.get("hilbert_consistent_I2") is True)}


def cmd_gates():
    ART.mkdir(exist_ok=True)
    SING.mkdir(exist_ok=True)
    res = load()
    t0 = time.time()
    log("gates start")
    res["gates"] = {}
    failed = []
    for name, fn in (("G1", lambda: gate_g1(res)), ("G2", lambda: gate_g2(res)), ("G4", gate_g4),
                     ("G3", lambda: gate_g3(res, 1200, time.time() + 7200))):
        g = fn()
        res["gates"][name] = g
        save(res)
        log("%s %s: %s" % (name, "PASSED" if g["passed"] else "FAILED", json.dumps({k: v for k, v in g.items() if k != "passed"})[:600]))
        if not g["passed"]:
            failed.append(name)
            break  # a failed gate stops the run
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    if failed:
        log("GATE FAILED: %s; the run stops here; failing cases: %s" % (failed[0], json.dumps(res["gates"][failed[0]].get("failing_cases"))[:800]))
        return 1
    log("all gates passed")
    return 0


def cmd_cases():
    res = load()
    if not all(res.get("gates", {}).get(g, {}).get("passed") for g in ("G1", "G2", "G3", "G4")):
        log("the gates have not all passed; run `gates` first (no verdict before the gates)")
        return 1
    t0 = time.time()
    only = opt("only", "")
    only = only.split(",") if only else []
    limit = float(opt("limit-seconds", 1200))
    budget_end = t0 + float(opt("budget-seconds", 14400))
    specs = [s for s in R.case_specs() if not only or s["family"] in only]
    stop = compute_cases(res, specs, limit, budget_end, label="cases")
    if not only or "C4" in only:
        compute_c4(res)
    res["runs"].append({"command": "cases", "seconds": round(time.time() - t0, 1)})
    save(res)
    if stop is not None:
        log("P1 STOP: finite length case %s (%s); the run stops here for examination" % (stop["id"], stop["field"]))
        return 1
    return 0


def cmd_table():
    import make_summary
    res = load()
    res["totals"] = make_summary.compute_totals(res)
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
    save(res)
    print(make_summary.totals_text(res["totals"]))
    make_summary.write_summary(res, HERE / "results-summary.md")
    log("table written")
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    ART.mkdir(exist_ok=True)
    random.seed(0)
    if cmd == "gates":
        return cmd_gates()
    if cmd == "cases":
        return cmd_cases()
    if cmd == "table":
        return cmd_table()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
