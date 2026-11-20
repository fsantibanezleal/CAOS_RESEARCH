"""EXP-006: the point (1,2,2,1) on (0, e, 3e, 4e) over U(H) in odd characteristic below 2e (e = 3, 4, 5).

Run from the repository root, with the repository virtual environment:
    python <this file> gates [--workers=N]      G1 (known pairs), G2 (the formula), G4 (pytest); exit 1 and the failing cases on a failure
    python <this file> cases [--only=A1,A2,B1,B2,B3,C] [--workers=N] [--budget-seconds=14400]   resumable, chunks of 250 spaces
    python <this file> second [--workers=N]     G3: Singular (Plural, through WSL) on the first pure spaces of every family
    python <this file> table                    totals per family and field and the four predictions into results.json,
                                                then make_summary.py writes results-summary.md

The hypothesis is hypothesis.md (frozen).  First instrument: exp006_routine.py over `uhlib`.  Second instrument:
Singular 4.3.2 (Plural), exp006_singular.py (the generator of EXP-005, no arithmetic shared with the first
instrument).  No machine path is written to any artifact.  Resumable: finished chunks stay in artifacts/results.json.
At most 8 worker processes, at most 4 hours per `cases` command.
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

import exp006_routine as R  # noqa: E402
import exp006_singular as Sg  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib.module import quotient_module  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
LOG = ART / "run.log"
T0 = time.time()
MAX_WORKERS = 8
SAVE_EVERY = 60.0
G3_SAMPLE = {"A1": 50}  # first n pure spaces per (family, field); every other family: 20 per field
G3_DEFAULT = 20
KEEP_BASES = 2000


def log(msg):
    line = "[%8.1fs] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-006", "hypothesis": "hypothesis.md (frozen)", "chunks": {}, "gates": {}, "runs": []}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    tmp.replace(RESULTS)


def opt(name, default):
    for a in sys.argv[2:]:
        if a.startswith("--%s=" % name):
            return a.split("=", 1)[1]
    return default


def workers():
    return max(1, min(MAX_WORKERS, int(opt("workers", MAX_WORKERS))))


# ------------------------------------------------------------------ gates G1, G2, G4
def _pair(F, e, f, g):
    """Coefficient array of the pair of forms f, g given as {(i, j, k): integer}."""
    return R.coeff_array(F, [[F.from_int(f.get(m, 0)) for m in A.monos(e)], [F.from_int(g.get(m, 0)) for m in A.monos(e)]])


def gate_g1():
    """The known answers.  The pair (x^3, y^3) over GF(5) appears in the hypothesis both among the pure tables and among
    the non-pure ones; Theorem A (pure iff p >= 2e) puts it among the non-pure ones, which is what is checked and reported."""
    rows = []
    cases = [(4, "GF(11)", True), (4, "GF(13)", True), (3, "GF(7)", True), (4, "GF(3)", False), (4, "GF(5)", False),
             (4, "GF(7)", False), (3, "GF(3)", False), (3, "GF(5)", False)]
    for e, fname, expect in cases:
        F = R.make_field(fname)
        C = _pair(F, e, {(e, 0, 0): 1}, {(0, e, 0): 1})
        t, _ = R.betti_table(F, C, e)
        rows.append({"pair": "(x^%d, y^%d)" % (e, e), "e": e, "field": fname, "expected_pure": expect,
                     "betti": R.table_rows(t), "pure": t == R.pure_table(e), "ok": (t == R.pure_table(e)) is expect})
    F = R.make_field("GF(3)")
    f = {(2, 0, 0): 1, (0, 2, 0): 1, (1, 1, 0): 1, (0, 0, 1): -1}  # x^2 + y^2 + yx, yx = xy - z
    g = {(2, 0, 0): 1, (1, 1, 0): 1, (0, 0, 1): -2}  # x^2 + yx - z = x^2 + xy - 2z
    t, _ = R.betti_table(F, _pair(F, 2, f, g), 2)
    rows.append({"pair": "(x^2 + y^2 + yx, x^2 + yx - z), PBW form x^2 + y^2 + xy - z, x^2 + xy - 2z", "e": 2,
                 "field": "GF(3)", "expected_pure": True, "betti": R.table_rows(t), "pure": t == R.pure_table(2),
                 "ok": t == R.pure_table(2)})
    bad = [r for r in rows if not r["ok"]]
    return {"passed": not bad, "cases": rows, "failing_cases": bad,
            "note": "(x^3, y^3) over GF(5) is listed as pure and as not pure in the hypothesis; checked as not pure (Theorem A: 5 < 2e = 6)"}


def gate_g2():
    """h_e equals the Hilbert function of U/U(x^e, y^e) over GF(32003) (own rank routine and uhlib's module), e = 3, 4, 5."""
    F = R.make_field("GF(32003)")
    ctx = R.ctx_of(F)
    out, bad = [], []
    for e in (3, 4, 5):
        D = R.hilbert_bound(e)
        C = _pair(F, e, {(e, 0, 0): 1}, {(0, e, 0): 1})
        mine = R.hilbert_pair(ctx, C, e, D)
        formula = [R.h_e(e, n) for n in range(D + 1)]
        M = quotient_module(F, [0], R.polys_as_relations(F, C, e), maxdeg=D)
        theirs = list(M.dims) + [0] * (D + 1 - len(M.dims))
        ok = mine == formula and theirs == formula
        out.append({"e": e, "degrees": "0..%d" % D, "formula": formula, "routine": mine, "uhlib_module": theirs, "ok": ok})
        if not ok:
            bad.append(e)
    return {"passed": not bad, "cases": out, "failing_cases": bad}


def gate_g4():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp006.py"], cwd=str(ROOT),
                          capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def cmd_gates():
    ART.mkdir(exist_ok=True)
    SING.mkdir(exist_ok=True)
    res = load()
    t0 = time.time()
    log("gates start")
    for k in ("G1", "G2", "G4"):
        res["gates"].pop(k, None)
    failed = None
    for name, fn in (("G1", gate_g1), ("G2", gate_g2), ("G4", gate_g4)):
        g = fn()
        res["gates"][name] = g
        save(res)
        log("%s %s: %s" % (name, "PASSED" if g["passed"] else "FAILED",
                           json.dumps({k: v for k, v in g.items() if k not in ("passed", "cases")})[:500]))
        if not g["passed"]:
            failed = name
            break  # a failed gate stops the run
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    if failed:
        log("GATE FAILED: %s; the run stops here; failing cases: %s" % (failed, json.dumps(res["gates"][failed].get("failing_cases"))[:1500]))
        return 1
    log("G1, G2, G4 passed (G3 is run by `second` after the cases)")
    return 0


# ------------------------------------------------------------------ cases
def cmd_cases():
    res = load()
    if not all(res.get("gates", {}).get(g, {}).get("passed") for g in ("G1", "G2", "G4")):
        log("G1, G2, G4 have not all passed; run `gates` first")
        return 1
    t0 = time.time()
    budget_end = t0 + float(opt("budget-seconds", 14400))
    only = [s for s in opt("only", "").split(",") if s]
    specs = R.chunk_specs(only or None)
    todo = [s for s in specs if s["id"] not in res["chunks"]]
    # the slowest first: extension fields of G(27), G(25), then the others
    todo.sort(key=lambda s: (-R.make_field(s["field"]).degree * 10 - (s["family"] == "A2") * 5, s["id"]))
    log("cases: %d chunks to compute, %d already stored" % (len(todo), len(specs) - len(todo)))
    last_save, done_n = time.time(), 0
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        pending, it = set(), iter(todo)

        def submit_next():
            if time.time() > budget_end:
                return False
            s = next(it, None)
            if s is None:
                return False
            pending.add(pool.submit(R.run_chunk, s))
            return True

        for _ in range(workers() * 2):
            submit_next()
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for fut in done:
                pending.discard(fut)
                rec = fut.result()
                res["chunks"][rec["id"]] = rec
                done_n += 1
                submit_next()
                if time.time() - last_save > SAVE_EVERY:
                    save(res)
                    last_save = time.time()
                    log("cases: %d chunks done in this run, last %s (%.1f s)" % (done_n, rec["id"], rec["seconds"]))
    left = len([s for s in specs if s["id"] not in res["chunks"]])
    res["runs"].append({"command": "cases", "seconds": round(time.time() - t0, 1), "only": only, "chunks_done": done_n,
                        "chunks_left": left})
    save(res)
    log("cases: %d chunks stored in total, %d not reached" % (len(specs) - left, left))
    return 0


# ------------------------------------------------------------------ G3: the second instrument
def ordered_spaces(res, family, field):
    """Stored spaces of a (family, field) in index order, with the chunk records they came from."""
    recs = sorted((c for c in res["chunks"].values() if c["family"] == family and c["field"] == field),
                  key=lambda c: c["start"])
    return [sp for c in recs for sp in sorted(c["spaces"], key=lambda s: s["index"])]


def g3_sample(res):
    """(family, field, space) of the first pure spaces: 50 in A1, 20 per field in every other family."""
    out = []
    for fam, (e, fields, kind, n, mode, orbit) in R.FAMILIES.items():
        for fname in fields:
            pure = [sp for sp in ordered_spaces(res, fam, fname) if sp["pure"]][: G3_SAMPLE.get(fam, G3_DEFAULT)]
            out += [(fam, fname, sp) for sp in pure]
    return out


def singular_available():
    try:
        p = subprocess.run(["wsl", "-e", "bash", "-c", "Singular -v < /dev/null | head -1"],
                           capture_output=True, text=True, timeout=120)
    except Exception as exc:
        return False, repr(exc)[:200]
    lines = [ln for ln in p.stdout.splitlines() if "Singular" in ln]
    return p.returncode == 0 and bool(lines), lines[0].strip() if lines else p.stderr[:200]


def _g3_one(item):
    fam, fname, sp = item
    F = R.make_field(fname)
    name = "%s_%s_%d" % (fam, fname, sp["index"])
    t, dt, err = Sg.run_space(name, R.field_record(F), sp["basis"], SING)
    return name, t, dt, err


def cmd_second():
    res = load()
    t0 = time.time()
    if not all(res.get("gates", {}).get(g, {}).get("passed") for g in ("G1", "G2", "G4")):
        log("G1, G2, G4 have not all passed; run `gates` first")
        return 1
    ok, version = singular_available()
    if not ok:
        res["gates"]["G3"] = {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version}
        save(res)
        log("G3 BLOCKED: " + version)
        return 1
    SING.mkdir(parents=True, exist_ok=True)
    sample = g3_sample(res)
    log("G3: %d pure spaces in the sample (%s)" % (len(sample), version))
    with ThreadPoolExecutor(max_workers=workers()) as tp:
        outs = list(tp.map(_g3_one, sample))
    rows, bad, errors = [], [], []
    for (fam, fname, sp), (name, t, dt, err) in zip(sample, outs):
        e = R.FAMILIES[fam][0]
        row = {"family": fam, "field": fname, "index": sp["index"], "script": name + ".sing", "seconds": round(dt, 1)}
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
        k = "%s|%s" % (r["family"], r["field"])
        per[k] = per.get(k, 0) + (1 if r.get("agree") and r.get("pure_I2") else 0)
    res["gates"]["G3"] = {"passed": not bad and not errors, "singular": version, "sample_spaces": len(sample),
                          "agree_and_pure_in_I2": sum(per.values()), "per_family_field": per, "failing_cases": bad,
                          "singular_errors": errors, "rows": rows}
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    save(res)
    g = res["gates"]["G3"]
    log("G3 %s: %d of %d agree; failing %s; errors %s" % ("PASSED" if g["passed"] else "FAILED", g["agree_and_pure_in_I2"],
                                                          len(sample), bad[:5], errors[:5]))
    return 0 if g["passed"] else 1


# ------------------------------------------------------------------ table
def cmd_table():
    import make_summary
    res = load()
    res["totals"] = make_summary.compute_totals(res)
    res["predictions"] = make_summary.predictions(res["totals"])
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
    make_summary.prune_bases(res, KEEP_BASES)
    save(res)
    print(make_summary.totals_text(res["totals"]))
    make_summary.write_summary(res, HERE / "results-summary.md")
    log("table written")
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    ART.mkdir(exist_ok=True)
    if cmd == "gates":
        return cmd_gates()
    if cmd == "cases":
        return cmd_cases()
    if cmd == "second":
        return cmd_second()
    if cmd == "table":
        return cmd_table()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
