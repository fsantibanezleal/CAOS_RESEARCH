"""EXP-012: machine checks of the central-commutator criterion (e = 0 or 1 modulo p), among them the open pairs (6, 5) and (7, 3).

Run from the repository root, with the repository virtual environment:
    python <this file> gates                         G1 (known answers) and G3 (pytest); exit 1 on a failure
    python <this file> cases --family X|R|N [--only=ID or e,p[+...]] [--workers=N] [--budget-seconds=N]
                                                     resumable per case (family X: one record per case; family R: one record per
                                                     pair (e, p); family N: one record per case)
    python <this file> second [--workers=N]          G2: Singular (Plural, through WSL) on every case of family X
    python <this file> table                         gates, predictions and totals into results.json, then results-summary.md

The hypothesis is hypothesis.md (frozen).  First instrument: exp012_routine.py over `uhlib`, python-flint and sympy.  Second
instrument: Singular 4.3.2 (Plural), exp012_singular.py (EXP-009's generator).  No machine path is written to any artifact.  At most
6 worker processes; the wall-time budget is three hours in total (`cases` and `second` stop handing out work when it is spent).
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

import exp012_routine as R  # noqa: E402
import exp012_singular as Sg  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
LOG = ART / "run.log"
SCRATCH = Path("D:/_Temp/bs-exp012-2026-11-20")
T0 = time.time()
MAX_WORKERS = 6
BUDGET = 10800.0
SEED_BASE = 20261120
N_PAIRS = 200
BETTI_PAIRS = 10

# Family X: the explicit pairs of the corollary, as in the hypothesis (name, e, p, f, g)
FAMILY_X = [
    ("B1", 4, 3, "x^4 + z^2", "y^4 + z^2"),
    ("B2", 6, 5, "x^6 + z^3", "y^6 + z^3"),
    ("B3", 8, 7, "x^8 + z^4", "y^8 + z^4"),
    ("B4", 10, 3, "x^10 + z^5", "y^10 + z^5"),
    ("B5", 12, 11, "x^12 + z^6", "y^12 + z^6"),
    ("C1", 6, 3, "x^6 + z^3 + y^4 z", "y^6 + x^4 z"),
    ("C2", 10, 5, "x^10 + z^5 + y^6 z^2", "y^10 + x^6 z^2"),
    ("C3", 12, 3, "x^12 + z^6 + y^4 z^4", "y^12 + x^4 z^4"),
    ("D1", 7, 3, "x^7 + y z^3 + x^3 z^2", "y^7 + x z^3"),
    ("D2", 11, 5, "x^11 + y z^5 + x^5 z^3", "y^11 + x z^5"),
    ("D3", 13, 3, "x^13 + y z^6 + x^3 z^5", "y^13 + x z^6"),
]
# Family R: the pairs (e, p) in the order of the hypothesis; the seed of an (e, p) is 20261120 + its 0-based index in this list
FAMILY_R = [(4, 3), (6, 3), (6, 5), (7, 3), (7, 7), (8, 7), (9, 3), (10, 3)]
# Family N: pairs of the class for which the criterion should fail
FAMILY_N = [
    ("N1", 7, 3, "x^7 + y z^3", "y^7 + x z^3"),
    ("N2", 6, 5, "x^6", "y^6 + z^3"),
    ("N3", 6, 3, "x^6 + y^4 z", "y^6 + x^4 z"),
]


def log(msg):
    line = "[%8.1fs] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-012", "hypothesis": "hypothesis.md (frozen)", "gates": {}, "X": {}, "R": {}, "N": {}, "runs": []}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
    tmp.replace(RESULTS)


def opt(name, default):
    for a in sys.argv[2:]:
        if a.startswith("--%s=" % name):
            return a.split("=", 1)[1]
        if a == "--%s" % name:
            i = sys.argv.index(a)
            if i + 1 < len(sys.argv):
                return sys.argv[i + 1]
    return default


def workers():
    return max(1, min(MAX_WORKERS, int(opt("workers", MAX_WORKERS))))


def spent(res):
    return sum(r.get("seconds", 0) for r in res["runs"])


def rows(table):
    return None if table is None else [[i, j, r] for (i, j), r in sorted(table.items())]


def from_rows(lst):
    return None if lst is None else {(i, j): r for i, j, r in lst}


# ------------------------------------------------------------------ gates
def gate_g1_direct():
    """The three pairs of the hypothesis (Hilbert function and Betti table by this routine) and the two ideals."""
    out = []
    for name, e, p, ft, gt, expect_pure in (
            ("<x^4 + z^2, y^4 + z^2> over GF(3)", 4, 3, "x^4 + z^2", "y^4 + z^2", True),
            ("<x^5 + y z^2, y^5 + x z^2> over GF(5)", 5, 5, "x^5 + y z^2", "y^5 + x z^2", True),
            ("<x^4, y^4> over GF(5)", 4, 5, "x^4", "y^4", False)):
        f, g = R.parse_pbw(ft), R.parse_pbw(gt)
        hf_ok, dims = R.pure_hilbert(f, g, e, p)
        t, mdims = R.betti_uhlib(f, g, e, p)
        pure = t == R.pure_table(e)
        out.append({"case": name, "hilbert_is_h_e": hf_ok, "hilbert": dims, "betti": rows(t), "pure": pure,
                    "expected_pure": expect_pure, "ok": pure is expect_pure})
    ideals = []
    for name, polys, p, expect in (
            ("(z^3, X^2 + z^3, Y^2 + z^3) in GF(3)[X, Y, z]", [{(0, 0, 3): 1}, {(2, 0, 0): 1, (0, 0, 3): 1},
                                                              {(0, 2, 0): 1, (0, 0, 3): 1}], 3, True),
            ("(z X Y, X^2, Y^2 + z^3) in GF(3)[X, Y, z]", [{(1, 1, 1): 1}, {(2, 0, 0): 1}, {(0, 2, 0): 1, (0, 0, 3): 1}], 3, False)):
        d = R.criterion_detail(polys, p)
        ideals.append({"ideal": name, "criterion": d["holds"], "expected": expect, "pure_powers": d["pure_powers"],
                       "ok": d["holds"] is expect})
    bad = [c for c in out + ideals if not c["ok"]]
    return {"passed": not bad, "pairs": out, "ideals": ideals, "failing_cases": bad}


def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp012.py", "-q"], cwd=str(ROOT), capture_output=True,
                          text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def gates_ok(res):
    return res["gates"].get("G1", {}).get("passed") is True and res["gates"].get("G3", {}).get("passed") is True


def cmd_gates():
    ART.mkdir(exist_ok=True)
    res = load()
    t0 = time.time()
    log("gates start")
    res["gates"]["G1"] = gate_g1_direct()
    save(res)
    log("G1 %s" % ("PASSED" if res["gates"]["G1"]["passed"] else "FAILED: " + json.dumps(res["gates"]["G1"]["failing_cases"])[:1500]))
    res["gates"]["G3"] = gate_g3()
    save(res)
    log("G3 %s: %s" % ("PASSED" if res["gates"]["G3"]["passed"] else "FAILED", json.dumps(res["gates"]["G3"])))
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    return 0 if gates_ok(res) else 1


# ------------------------------------------------------------------ workers (module level: picklable)
def work_x(spec):
    """Family X case: the data, D, n(f), n(g), the identities, the criterion, the Hilbert function, the length, the uhlib table."""
    name, e, p, ft, gt = spec
    t0 = time.perf_counter()
    f, g = R.parse_pbw(ft), R.parse_pbw(gt)
    case = R.case_from_pbw(name, e, p, f, g)
    Ad, b1, b2 = case["data_f"]
    Bd, d1, d2 = case["data_g"]
    rec = {"name": name, "e": e, "p": p, "f_text": ft, "g_text": gt, "f": R.pj(f), "g": R.pj(g),
           "vec_f": R.data_to_vec(e, p, Ad, b1, b2), "vec_g": R.data_to_vec(e, p, Bd, d1, d2),
           "data_f": {"A": R.pj(Ad), "beta1": R.pj(b1), "beta2": R.pj(b2)},
           "data_g": {"B": R.pj(Bd), "delta1": R.pj(d1), "delta2": R.pj(d2)},
           "D": R.pj(case["D"]), "nf": R.pj(case["nf"]), "ng": R.pj(case["ng"])}
    t = time.perf_counter()
    rec["identities"] = R.identities(case, p)
    rec["seconds_identities"] = round(time.perf_counter() - t, 2)
    t = time.perf_counter()
    rec["criterion"] = R.criterion(case, p)
    rec["seconds_criterion"] = round(time.perf_counter() - t, 2)
    t = time.perf_counter()
    dims = R.hilbert_dims(f, g, e, p, 4 * e + 3)
    rec["hilbert"] = dims
    rec["h_e"] = R.expected_hilbert(e)
    rec["hilbert_is_h_e"] = dims == rec["h_e"]
    rec["length"] = sum(dims)
    rec["length_is_e_cubed"] = sum(dims) == e ** 3
    rec["seconds_hilbert"] = round(time.perf_counter() - t, 2)
    t = time.perf_counter()
    tab, mdims = R.betti_uhlib(f, g, e, p)
    rec["betti_uhlib"] = rows(tab)
    rec["betti_uhlib_pure"] = tab == R.pure_table(e)
    rec["uhlib_dims_equal_ranks"] = (mdims + [0] * len(dims))[:len(dims)] == dims
    rec["seconds_betti_uhlib"] = round(time.perf_counter() - t, 2)
    rec["seconds"] = round(time.perf_counter() - t0, 2)
    rec["complete"] = True
    return ("X", name, rec)


def work_r(key):
    """Family R, one pair (e, p): the 200 pairs, the identity, the criterion, the pure Hilbert function."""
    e, p = key
    idx = FAMILY_R.index((e, p))
    seed = SEED_BASE + idx
    t0 = time.perf_counter()
    pairs = R.draw_pairs(e, p, seed, N_PAIRS)
    recs = []
    for k, (fv, gv) in enumerate(pairs):
        f, g = R.pair_from_vectors(e, p, fv, gv)
        case = R.case_from_pbw("R", e, p, f, g)
        ident = R.identities(case, p)["commutator"]
        crit = R.criterion(case, p)
        ph, dims = R.pure_hilbert(f, g, e, p)
        rec = {"i": k, "f": fv, "g": gv, "identity": ident, "criterion": crit["holds"], "pure_hilbert": ph}
        if crit["holds"] != ph:
            rec["intermediate"] = {"f": R.pj(f), "g": R.pj(g), "D": R.pj(case["D"]), "nf": R.pj(case["nf"]),
                                   "ng": R.pj(case["ng"]), "criterion": crit, "hilbert_prefix": dims}
        recs.append(rec)
    return ("R", "%d,%d" % key, {"e": e, "p": p, "seed": seed, "n_pairs": N_PAIRS, "pairs": recs, "betti": {},
                                 "seconds": round(time.perf_counter() - t0, 2), "complete": True})


def work_rb(args):
    """Family R: the Betti table by uhlib of one pair with the pure Hilbert function."""
    e, p, k, fv, gv = args
    t0 = time.perf_counter()
    f, g = R.pair_from_vectors(e, p, fv, gv)
    tab, _ = R.betti_uhlib(f, g, e, p)
    return ("RB", "%d,%d" % (e, p), {"i": k, "betti": rows(tab), "pure": tab == R.pure_table(e),
                                     "seconds": round(time.perf_counter() - t0, 2)})


def work_n(spec):
    """Family N case: the criterion and the Hilbert function to degree 5e."""
    name, e, p, ft, gt = spec
    t0 = time.perf_counter()
    f, g = R.parse_pbw(ft), R.parse_pbw(gt)
    case = R.case_from_pbw(name, e, p, f, g)
    Ad, b1, b2 = case["data_f"]
    Bd, d1, d2 = case["data_g"]
    dims = R.hilbert_dims(f, g, e, p, 5 * e)
    finite = dims[-1] == 0
    rec = {"name": name, "e": e, "p": p, "f_text": ft, "g_text": gt, "f": R.pj(f), "g": R.pj(g),
           "vec_f": R.data_to_vec(e, p, Ad, b1, b2), "vec_g": R.data_to_vec(e, p, Bd, d1, d2),
           "data_f": {"A": R.pj(Ad), "beta1": R.pj(b1), "beta2": R.pj(b2)},
           "data_g": {"B": R.pj(Bd), "delta1": R.pj(d1), "delta2": R.pj(d2)},
           "D": R.pj(case["D"]), "nf": R.pj(case["nf"]), "ng": R.pj(case["ng"]),
           "identities": R.identities(case, p), "criterion": R.criterion(case, p),
           "hilbert_to_5e": dims, "finite_length_within_5e": finite, "length": sum(dims) if finite else None,
           "hilbert_is_h_e": dims[:4 * e + 4] == R.expected_hilbert(e) and finite,
           "seconds": round(time.perf_counter() - t0, 2), "complete": True}
    return ("N", name, rec)


# ------------------------------------------------------------------ the pool driver
def drive(tasks, res, on_result, deadline):
    """Run (function, argument) tasks on at most `workers()` processes; on_result(kind, key, rec) updates res; saves after each."""
    n = workers()
    pending = list(tasks)
    running = {}
    with ProcessPoolExecutor(max_workers=n) as ex:
        while pending or running:
            while pending and len(running) < n and time.time() < deadline:
                fn, arg = pending.pop(0)
                label = (fn.__name__, arg[:3] if fn is work_rb else arg)
                running[ex.submit(fn, arg)] = label
                log("start %s %s" % label)
            if not running:
                if pending:
                    log("budget spent: %d tasks not started" % len(pending))
                break
            done, _ = wait(list(running), return_when=FIRST_COMPLETED, timeout=60)
            for fut in done:
                nm, arg = running.pop(fut)
                try:
                    kind, key, rec = fut.result()
                except Exception as exc:  # recorded, never hidden
                    log("ERROR in %s %s: %r" % (nm, arg, exc))
                    continue
                more = on_result(kind, key, rec, res)
                save(res)
                log("done %s %s (%.1f s)" % (kind, key, rec.get("seconds", 0)))
                if more:
                    pending = list(more) + pending
    return not pending


def wanted(items, key_of):
    only = opt("only", None)
    if not only:
        return items
    keys = {s.strip() for s in only.split("+")}
    return [it for it in items if key_of(it) in keys]


def cmd_cases():
    fam = opt("family", None)
    if fam not in ("X", "R", "N"):
        print("cases needs --family X|R|N")
        return 2
    ART.mkdir(exist_ok=True)
    res = load()
    if not gates_ok(res):
        log("gates G1 and G3 have not passed: run `gates` first (a failed gate stops the run)")
        return 1
    t0 = time.time()
    left = BUDGET - spent(res)
    tasks = []
    if fam == "X":
        specs = sorted(FAMILY_X, key=lambda s: (s[1] > 8, s[1], s[0]))        # e <= 8 first
        tasks = [(work_x, s) for s in wanted(specs, lambda s: s[0]) if not res["X"].get(s[0], {}).get("complete")]
    elif fam == "N":
        tasks = [(work_n, s) for s in wanted(FAMILY_N, lambda s: s[0]) if not res["N"].get(s[0], {}).get("complete")]
    else:
        keys = wanted(FAMILY_R, lambda k: "%d,%d" % k)
        tasks = [(work_r, k) for k in keys if not res["R"].get("%d,%d" % k, {}).get("complete")]
        for k in keys:                                  # Betti tables still missing on a stored pair record
            rec = res["R"].get("%d,%d" % k)
            if rec and rec.get("complete"):
                tasks += betti_tasks(rec)

    def on_result(kind, key, rec, res):
        if kind in ("X", "N"):
            res[kind][key] = rec
        elif kind == "R":
            res["R"][key] = rec
            return betti_tasks(rec)
        elif kind == "RB":
            res["R"][key]["betti"][str(rec["i"])] = rec
        return None

    log("cases family %s: %d tasks, %d workers, %.0f s of budget left" % (fam, len(tasks), workers(), left))
    ok = drive(tasks, res, on_result, time.time() + left)
    res["runs"].append({"command": "cases --family %s" % fam, "seconds": round(time.time() - t0, 1), "all_started": ok})
    save(res)
    return 0


def betti_tasks(rec):
    """The first BETTI_PAIRS pairs of a family R record with the pure Hilbert function whose table is not stored yet."""
    pure = [pr for pr in rec["pairs"] if pr["pure_hilbert"]][:BETTI_PAIRS]
    return [(work_rb, (rec["e"], rec["p"], pr["i"], pr["f"], pr["g"])) for pr in pure if str(pr["i"]) not in rec["betti"]]


# ------------------------------------------------------------------ second instrument
def one_singular(res_x, name):
    rec = res_x[name]
    tab, secs, err = Sg.run_case(name, rec["p"], rec["f"], rec["g"], SING, SCRATCH / "singular-out")
    return name, {"betti": rows(tab), "seconds": round(secs, 1), "error": err,
                  "same_as_uhlib": (rows(tab) == rec["betti_uhlib"]) if tab is not None else None}


def cmd_second():
    res = load()
    if not gates_ok(res):
        log("gates G1 and G3 have not passed: run `gates` first")
        return 1
    t0 = time.time()
    names = [n for n in wanted([s[0] for s in FAMILY_X], lambda n: n) if n in res["X"] and "singular" not in res["X"][n]]
    names.sort(key=lambda n: res["X"][n]["e"])
    log("second: %d cases, %d workers" % (len(names), workers()))
    ART.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=workers()) as ex:
        futs = [ex.submit(one_singular, res["X"], n) for n in names]
        for fu in futs:
            name, s = fu.result()
            res["X"][name]["singular"] = s
            save(res)
            log("Singular %s: table %s, same as uhlib %s, %.1f s, error %s" % (name, s["betti"], s["same_as_uhlib"], s["seconds"],
                                                                              s["error"]))
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    save(res)
    return 0


def cmd_table():
    import make_summary as M
    res = load()
    M.build(res)
    save(res)
    (HERE / "results-summary.md").write_text(M.render(res), encoding="utf-8", newline="\n")
    print(M.render_table(res))
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"gates": cmd_gates, "cases": cmd_cases, "second": cmd_second, "table": cmd_table}.get(cmd)
    if not fn:
        print(__doc__)
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
