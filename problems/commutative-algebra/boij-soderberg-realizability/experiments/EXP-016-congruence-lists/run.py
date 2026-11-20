"""EXP-016: the lists L(e, q) of forms G with (C) and (b), every listed form checked in U by two instruments.

Run from the repository root, with the repository virtual environment:
    python <this file> gates                      G3 (pytest's exit code) and the Singular version line; exit 1 on a failure
    python <this file> throughput                 forms per second of one process on (12, 13)
    python <this file> cases --family A|N|B|X|O [--only e,p[+e,p]] [--workers N] [--budget-seconds N] [--verify]
                                                  resumable; A: G1, N: G5, B: prime fields, X: GF(p^2), O: the two optional cases;
                                                  --verify runs `verify` on each case as it finishes
    python <this file> verify [--family F] [--only e,p[+e,p]] [--timeout S]
                                                  the Betti tables (first instrument, uhlib) of the forms named by the hypothesis; G4
    python <this file> second [--workers N] [--timeout S]
                                                  G2: Singular 4.3.2 (Plural, through WSL) on every verified form
    python <this file> table                      predictions P1 to P5 into results.json, then results-summary.md; prints the table

The hypothesis is hypothesis.md (frozen).  At most 8 worker processes and three hours of wall time in total.  No machine path is written
to any artifact; Singular outputs go to the scratch folder (--scratch) and are moved to the data root by hand when the run ends.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from collections import deque
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
for _p in (HERE, HERE.parent / "EXP-009-linear-family-below-2e"):
    if str(_p) not in sys.path:
        sys.path.append(str(_p))

import exp016_routine as R  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
MAX_WORKERS = 8
BUDGET_SECONDS = 3 * 3600
CHUNK = 1 << 22
BETTI_TIMEOUT = 2400
VERIFY_FIRST = {"A": 1, "B": 3, "X": 3, "O": 3}
FAMILIES = ("A", "N", "B", "X", "O")
A_CASES = [(4, 7), (4, 11), (4, 13), (4, 17), (6, 5), (6, 7), (6, 11), (6, 13), (6, 17), (8, 3), (8, 5), (8, 7), (8, 11), (8, 13), (10, 5)]
B_CASES = [(10, p) for p in (3, 7, 11, 13, 17, 19)] + [(12, p) for p in (5, 7, 11, 13, 17, 19, 23)] + [
    (14, p) for p in (3, 5, 11, 13, 17, 19, 23)] + [(16, p) for p in (3, 5, 7, 11, 13)]
O_CASES = [(16, 17), (16, 19)]
X_CASES = [(8, 3), (6, 13), (14, 3)]
N_CASES = [(6, 7), (8, 5), (8, 13)]
G1_SIZES = {(4, 7): 1, (4, 11): 2, (4, 13): 16, (4, 17): 13, (6, 5): 2, (6, 7): 2, (6, 11): 4, (6, 13): 0, (6, 17): 2, (8, 3): 0, (8, 5): 1,
            (8, 7): 4, (8, 11): 1, (8, 13): 1, (10, 5): 0}
G1_LISTS = {(6, 7): [[3, 0, 0], [3, 3, 4]], (8, 5): [[2, 0, 1, 3]], (8, 13): [[6, 11, 3, 11]]}
DATA_HINT = "E:/_Datos/caos-research/boij-soderberg-realizability/EXP-016"


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def opt(name, default=None):
    flag = "--" + name
    if flag in sys.argv:
        i = sys.argv.index(flag)
        return sys.argv[i + 1] if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--") else True
    return default


def workers():
    return max(1, min(MAX_WORKERS, int(opt("workers", MAX_WORKERS))))


def scratch():
    d = Path(opt("scratch", "D:/_Temp/bs-exp016-2026-11-20"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def only_list():
    v = opt("only")
    return {tuple(int(x) for x in s.split(",")) for s in v.split("+")} if isinstance(v, str) else None


# ------------------------------------------------------------------ store
def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-016", "hypothesis": "hypothesis.md (frozen)", "cases": {}, "negatives": {}, "gates": {}, "runs": [],
            "throughput": None, "budget": {"used_seconds": 0.0, "limit_seconds": BUDGET_SECONDS}}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
    tmp.replace(RESULTS)


def key_of(family, e, p, k):
    return "%s|%d|%d|%d" % (family, e, p, k)


def plan(family):
    table = {"A": [(e, p, 1) for e, p in A_CASES], "B": [(e, p, 1) for e, p in B_CASES], "O": [(e, p, 1) for e, p in O_CASES],
             "X": [(e, p, 2) for e, p in X_CASES], "N": [(e, p, 1) for e, p in N_CASES]}[family]
    only = only_list()
    return [{"key": key_of(family, e, p, k), "family": family, "e": e, "p": p, "k": k} for e, p, k in table if not only or (e, p) in only]


# ------------------------------------------------------------------ gates
def singular_version():
    try:
        proc = subprocess.run(["wsl", "-e", "bash", "-c", "Singular -v < /dev/null | head -1"], capture_output=True, text=True, timeout=120)
    except Exception as exc:
        return False, repr(exc)[:200]
    lines = [ln for ln in proc.stdout.splitlines() if "Singular" in ln]
    return proc.returncode == 0 and bool(lines), lines[0].strip() if lines else proc.stderr[:200]


def cmd_gates():
    res = load()
    t0 = time.time()
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp016.py", "-q"], cwd=str(ROOT), capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    res["gates"]["G3"] = {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}
    ok, version = singular_version()
    res["gates"]["singular"] = {"available": ok, "version": version}
    log("G3 %s: %s" % ("PASSED" if proc.returncode == 0 else "FAILED", res["gates"]["G3"]["last_line"]))
    log("Singular through WSL: %s (%s)" % ("available" if ok else "NOT available", version))
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    return 0 if proc.returncode == 0 else 1


def gate_ok(res, name):
    return res["gates"].get(name, {}).get("passed") is True


def eval_g1(res):
    rows = []
    for (e, p), size in G1_SIZES.items():
        c = res["cases"].get(key_of("A", e, p, 1))
        got = None if c is None or not c["complete"] else len(c["list"])
        row = {"pair": [e, p], "expected": size, "size": got, "ok": got == size}
        if (e, p) in G1_LISTS and c is not None and c["complete"]:
            row["expected_list"] = G1_LISTS[(e, p)]
            row["list_ok"] = sorted(f["coeffs"] for f in c["list"]) == sorted(G1_LISTS[(e, p)])
            row["ok"] = row["ok"] and row["list_ok"]
        rows.append(row)
    return {"passed": all(r["ok"] for r in rows), "rows": rows}


# ------------------------------------------------------------------ throughput
def cmd_throughput():
    res = load()
    out = R.throughput(12, 13, 1 << 21)
    res["throughput"] = out
    res["runs"].append({"command": "throughput", "seconds": out["fast_test_seconds"] + out["with_exact_seconds"]})
    save(res)
    log("throughput on (12, 13), one process: %s" % json.dumps(out))
    return 0


# ------------------------------------------------------------------ cases
def new_case(spec):
    F = R.Field(spec["p"], spec["k"])
    return {"family": spec["family"], "e": spec["e"], "p": spec["p"], "degree": spec["k"], "field": F.name, "n_forms": F.q ** (spec["e"] // 2),
            "complete": False, "done_upto": 0, "n_fast": 0, "n_b": 0, "n_b_noC": 0, "n_fast_not_exact": 0, "list": [], "seconds": 0.0,
            "worker_seconds": 0.0, "verified": []}


def run_scan(res, spec, pool, deadline):
    case = res["cases"].setdefault(spec["key"], new_case(spec))
    if case["complete"]:
        return case
    total, t0, last_save = case["n_forms"], time.time(), time.time()
    starts = iter(range(case["done_upto"], total, CHUNK))
    inflight, stop = deque(), False
    e, p, k = spec["e"], spec["p"], spec["k"]
    while True:
        while not stop and len(inflight) < 2 * workers():
            s = next(starts, None)
            if s is None:
                stop = True
                break
            if time.time() > deadline:
                stop = True
                break
            inflight.append(pool.submit(R.scan_task, (e, p, k, s, min(total, s + CHUNK))))
        if not inflight:
            break
        s, t, r, dt = inflight.popleft().result()
        for name in ("n_fast", "n_b", "n_b_noC", "n_fast_not_exact"):
            case[name] += r[name]
        case["list"] += r["list"]
        case["done_upto"] = t
        case["worker_seconds"] = round(case["worker_seconds"] + dt, 1)
        if time.time() - last_save > 60:
            case["seconds"] = round(case["seconds"] + time.time() - t0, 1)
            t0 = time.time()
            save(res)
            last_save = time.time()
            log("%s: %d of %d forms, %d in the list" % (spec["key"], t, total, len(case["list"])))
    case["seconds"] = round(case["seconds"] + time.time() - t0, 1)
    case["complete"] = case["done_upto"] >= total
    case["index_range_done"] = [0, case["done_upto"]]
    save(res)
    log("%s: %s, %d forms scanned, %d passing the fast test, %d with (b), %d with (b) and without (C), list size %d, %.1f s" % (
        spec["key"], "complete" if case["complete"] else "PARTIAL up to index %d" % case["done_upto"], case["done_upto"], case["n_fast"],
        case["n_b"], case["n_b_noC"], len(case["list"]), case["seconds"]))
    return case


def run_negatives(res, spec, pool):
    if spec["key"] in res["negatives"]:
        return
    e, p, k = spec["e"], spec["p"], spec["k"]
    F = R.Field(p, k)
    t0 = time.time()
    forms = pool.submit(R.negatives_task, (e, p, k, 5)).result()
    for f in forms:
        g = {tuple(m): (c if k == 1 else tuple(c)) for m, c in f["g"]}
        out = R.run_isolated("length", e, F, g, BETTI_TIMEOUT)
        f["length"] = out.get("length")
        f["different_from_e_cubed"] = out.get("length") != e ** 3 and "error" not in out and "timeout" not in out
        f["length_note"] = "module not finite within degree %d" % (4 * e + 3) if "length" in out and out["length"] is None else out.get(
            "error") or out.get("note")
    res["negatives"][spec["key"]] = {"e": e, "p": p, "degree": k, "e_cubed": e ** 3, "forms": forms, "seconds": round(time.time() - t0, 1)}
    save(res)
    log("%s: %d forms with (C) and without (b); lengths %s (e^3 = %d)" % (spec["key"], len(forms), [f["length"] for f in forms], e ** 3))


def eval_g5(res):
    rows = []
    for e, p in N_CASES:
        n = res["negatives"].get(key_of("N", e, p, 1))
        rows.append({"pair": [e, p], "forms": 0 if n is None else len(n["forms"]),
                     "ok": bool(n and len(n["forms"]) == 5 and all(f["different_from_e_cubed"] for f in n["forms"]))})
    return {"passed": all(r["ok"] for r in rows), "rows": rows}


def verify_case(res, key, timeout):
    """The first instrument on the first forms of the list; returns the keys of forms that are not pure (G4)."""
    case = res["cases"][key]
    e, p, k = case["e"], case["p"], case["degree"]
    F = R.Field(p, k)
    want = case["list"][:VERIFY_FIRST[case["family"]]]
    have = {v["index"] for v in case["verified"]}
    todo = [f for f in want if f["index"] not in have]

    def one(f):
        cs = [c if k == 1 else tuple(c) for c in f["coeffs"]]
        g = R.pbw_g(e, F, cs)
        return f, g, R.run_isolated("betti", e, F, g, timeout)

    with ThreadPoolExecutor(max_workers=workers()) as tp:
        outs = list(tp.map(one, todo))
    for f, g, out in outs:
        cs = [c if k == 1 else tuple(c) for c in f["coeffs"]]
        case["verified"].append({"index": f["index"], "coeffs": f["coeffs"], "poly": R.poly_text(F, cs), "lam": f["lam"],
                                 "g": [[list(mo), c if isinstance(c, int) else list(c)] for mo, c in sorted(g.items())], "first": out})
    case["verified"].sort(key=lambda v: v["index"])
    save(res)
    return [(key, v["index"]) for v in case["verified"] if not v["first"].get("pure")]


def eval_g4(res):
    rows, bad = [], []
    for key, c in sorted(res["cases"].items()):
        if not c["verified"]:
            continue
        nonpure = [v["index"] for v in c["verified"] if not v["first"].get("pure")]
        rows.append({"case": key, "verified": len(c["verified"]), "pure": len(c["verified"]) - len(nonpure), "not_pure": nonpure})
        bad += [(key, i) for i in nonpure]
    return {"passed": not bad, "rows": rows}


def families_ready(res, family):
    if not gate_ok(res, "G3"):
        log("G3 has not passed; run `gates` first")
        return False
    if family in ("B", "X", "O"):
        if not gate_ok(res, "G1") or not gate_ok(res, "G5"):
            log("G1 (family A) and G5 (family N) have not both passed; run families A and N first")
            return False
    return True


def cmd_cases():
    res = load()
    fam = opt("family", "")
    if fam not in FAMILIES:
        log("--family A|N|B|X|O is required")
        return 2
    if not families_ready(res, fam):
        return 1
    specs = plan(fam)
    used = res["budget"]["used_seconds"]
    left = float(opt("budget-seconds", res["budget"]["limit_seconds"] - used))
    t0 = time.time()
    deadline = t0 + left
    log("family %s: %d cases planned; budget left %.0f s (used %.0f of %d s)" % (fam, len(specs), left, used, res["budget"]["limit_seconds"]))
    rc = 0
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        for spec in specs:
            if time.time() > deadline:
                log("time limit reached before %s" % spec["key"])
                break
            if fam == "N":
                run_negatives(res, spec, pool)
                continue
            case = run_scan(res, spec, pool, deadline)
            if opt("verify") and case["complete"] and case["list"]:
                bad = verify_case(res, spec["key"], int(opt("timeout", BETTI_TIMEOUT)))
                res["gates"]["G4"] = eval_g4(res)
                log("%s verified: %s" % (spec["key"], [(v["index"], v["first"].get("pure"), v["first"].get("length"), v["first"].get("seconds"))
                                                       for v in res["cases"][spec["key"]]["verified"]]))
                if bad:
                    log("G4 FAILED: forms not pure in the first instrument: %s; the run stops" % bad)
                    rc = 1
                    break
    dt = time.time() - t0
    if fam == "A" and all(s["key"] in res["cases"] and res["cases"][s["key"]]["complete"] for s in plan("A")):
        res["gates"]["G1"] = eval_g1(res)
        log("G1 %s" % ("PASSED" if res["gates"]["G1"]["passed"] else "FAILED: " + json.dumps([r for r in res["gates"]["G1"]["rows"] if not r["ok"]])))
        rc = rc or (0 if res["gates"]["G1"]["passed"] else 1)
    if fam == "N" and all(s["key"] in res["negatives"] for s in plan("N")):
        res["gates"]["G5"] = eval_g5(res)
        log("G5 %s" % ("PASSED" if res["gates"]["G5"]["passed"] else "FAILED: " + json.dumps(res["gates"]["G5"]["rows"])))
        rc = rc or (0 if res["gates"]["G5"]["passed"] else 1)
    res["budget"]["used_seconds"] = round(used + dt, 1)
    res["runs"].append({"command": "cases", "family": fam, "only": opt("only"), "workers": workers(), "seconds": round(dt, 1)})
    save(res)
    log("family %s done in %.0f s" % (fam, dt))
    return rc


def cmd_verify():
    res = load()
    if not gate_ok(res, "G3"):
        log("G3 has not passed; run `gates` first")
        return 1
    fam, only = opt("family"), only_list()
    t0 = time.time()
    rc = 0
    for key, c in sorted(res["cases"].items(), key=lambda kv: (kv[1]["family"], kv[1]["e"], kv[1]["p"])):
        if (fam and c["family"] != fam) or (only and (c["e"], c["p"]) not in only) or not c["complete"] or not c["list"]:
            continue
        bad = verify_case(res, key, int(opt("timeout", BETTI_TIMEOUT)))
        log("%s verified: %s" % (key, [(v["index"], v["first"].get("pure"), v["first"].get("length"), v["first"].get("seconds"))
                                       for v in res["cases"][key]["verified"]]))
        if bad:
            log("G4 FAILED: %s" % bad)
            rc = 1
            break
    res["gates"]["G4"] = eval_g4(res)
    res["runs"].append({"command": "verify", "seconds": round(time.time() - t0, 1)})
    res["budget"]["used_seconds"] = round(res["budget"]["used_seconds"] + time.time() - t0, 1)
    save(res)
    return rc


# ------------------------------------------------------------------ G2
def cmd_second():
    import exp009_singular as Sg
    res = load()
    t0 = time.time()
    ok, version = singular_version()
    if not ok:
        res["gates"]["G2"] = {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version,
                              "note": "single-instrument results"}
        save(res)
        log("G2 BLOCKED: " + version)
        return 1
    out_dir = scratch() / "singular"
    out_dir.mkdir(parents=True, exist_ok=True)
    SING.mkdir(parents=True, exist_ok=True)
    timeout = int(opt("timeout", BETTI_TIMEOUT))
    items = [(key, v) for key, c in sorted(res["cases"].items(), key=lambda kv: (kv[1]["family"], kv[1]["e"], kv[1]["p"]))
             for v in c["verified"] if "second" not in v or "error" in v["second"]]

    def one(item):
        key, v = item
        c = res["cases"][key]
        name = "e%d_p%d_k%d_idx%d" % (c["e"], c["p"], c["degree"], v["index"])
        F = R.Field(c["p"], c["degree"])
        g = {tuple(m): (cf if c["degree"] == 1 else tuple(cf)) for m, cf in v["g"]}
        return name, Sg.run_member(name, F.record(), R.basis_json(c["e"], g), out_dir, timeout=timeout)

    log("G2: %d verified forms to run (%s)" % (len(items), version))
    with ThreadPoolExecutor(max_workers=workers()) as tp:
        outs = list(tp.map(one, items))
    for (key, v), (name, (t, dt, err)) in zip(items, outs):
        e = res["cases"][key]["e"]
        row = {"script": name + ".sing", "seconds": round(dt, 1)}
        if err or t is None:
            row["error"] = str(err)[:300] if err else "no table"
        else:
            row["betti"] = [[i, j, r] for (i, j), r in sorted(t.items())]
            row["pure"] = t == R.PURE_BETTI(e)
        v["second"] = row
        src = out_dir / (name + ".sing")
        if src.exists():
            shutil.copyfile(src, SING / (name + ".sing"))
    res["gates"]["G2"] = eval_g2(res, version)
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    res["budget"]["used_seconds"] = round(res["budget"]["used_seconds"] + time.time() - t0, 1)
    save(res)
    g2 = res["gates"]["G2"]
    log("G2 %s: %d of %d verified forms agree; failing %s" % ("PASSED" if g2["passed"] else "FAILED", g2["agree"], g2["forms"], g2["failing"][:5]))
    return 0 if g2["passed"] else 1


def eval_g2(res, version):
    forms, agree, failing = 0, 0, []
    for key, c in res["cases"].items():
        for v in c["verified"]:
            forms += 1
            s = v.get("second")
            if s and "betti" in s and v["first"].get("betti") is not None and [list(x) for x in v["first"]["betti"]] == s["betti"]:
                agree += 1
            else:
                failing.append("%s idx %d" % (key, v["index"]))
    return {"passed": forms > 0 and agree == forms, "singular": version, "forms": forms, "agree": agree, "failing": failing}


# ------------------------------------------------------------------ table
def cmd_table():
    spec = importlib.util.spec_from_file_location("exp016_make_summary", HERE / "make_summary.py")
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    res = load()
    res["totals"] = ms.compute_totals(res)
    res["predictions"] = ms.predictions(res)
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
    save(res)
    print(ms.table_text(res))
    ms.write_summary(res, HERE / "results-summary.md")
    log("table written")
    return 0


def main():
    fn = {"gates": cmd_gates, "throughput": cmd_throughput, "cases": cmd_cases, "verify": cmd_verify, "second": cmd_second,
          "table": cmd_table}.get(sys.argv[1] if len(sys.argv) > 1 else "")
    if fn is None:
        print(__doc__)
        return 2
    ART.mkdir(exist_ok=True)
    return fn()


if __name__ == "__main__":
    sys.exit(main())
