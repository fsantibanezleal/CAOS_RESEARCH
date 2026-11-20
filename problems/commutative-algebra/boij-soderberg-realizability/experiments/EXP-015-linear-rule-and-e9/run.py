"""EXP-015: the rule of the linear family S(e - 1; 0, 1) for e = 10 to 13 (family L), the strata of e = 9 at the pairs (9, 5), (9, 11), (9, 13)
(family R) and the four controls (family K).

Run from the repository root, with the repository virtual environment:
    python <this file> gates                       the fixed member of G1 and G3 (pytest's exit code); exit 1 on a failure
    python <this file> cases --family K|L|R [--only e,p[+e,p]] [--workers N] [--budget-seconds N] [--chunk N]
                                                   resumable (results are stored per case); the early stop is at 5 pure members; K is
                                                   followed by the family part of G1; L and R need it
    python <this file> second [--workers N] [--out-dir D]
                                                   G2: Singular 4.3.2 (Plural, through WSL) on the first three pure members of each case
    python <this file> table                       predictions P1 and P2 into results.json, then results-summary.md; prints the table

The hypothesis is hypothesis.md (frozen).  The routine, the worker pool, the early stop and the second instrument are those of EXP-010
(imported, not edited).  At most 16 worker processes and four hours of wall time in total.  No machine path is written to any artifact.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
EXP10 = HERE.parent / "EXP-010-weight-class-strata"
for _p in (EXP10, HERE.parent / "EXP-009-linear-family-below-2e"):
    if str(_p) not in sys.path:
        sys.path.append(str(_p))

import exp010_routine as X  # noqa: E402



def _struct_tensor_mod_p(p, e, n):
    """The tensor of exp010_routine.struct_tensor with every coefficient reduced modulo p before it is accumulated.  The routine adds the
    exact integer coefficients (k! C(b, k) C(a, k)) into an int64 array, which overflows at e = 13, n = 49; reducing first gives the same
    tensor modulo p and never overflows.  Applied at import, so that the worker processes (which import this file as their main module)
    use it too; the routine of EXP-010 is not edited."""
    me, ma, mn = X.A.monos(e), X.A.monos(n - e), X.A.monos(n)
    col = {mm: k for k, mm in enumerate(mn)}
    T = X.np.zeros((len(me), len(ma), len(mn)), dtype=X.np.int64)
    for im, mono in enumerate(me):
        for ia, a in enumerate(ma):
            for mm, c in X.A.mono_mul(a, mono):
                T[im, ia, col[mm]] += c % p
    return T % p


struct_tensor_original = X.struct_tensor
X.struct_tensor = X.lru_cache(maxsize=64)(_struct_tensor_mod_p)

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
MAX_WORKERS = 16
BUDGET_SECONDS = 4 * 3600
G2_PER_CASE = 3
FAMILIES = ("K", "L", "R")
BUDGET_CASE = 100000
K_CASES = [(9, 17), (9, 13), (8, 13), (8, 11)]
L_PAIRS = [(10, 17), (10, 19), (10, 13), (10, 11), (11, 19), (11, 17), (11, 13), (12, 23), (12, 19), (12, 17), (13, 23), (13, 19)]
L_PURE = {(10, 17), (10, 19), (11, 19), (12, 23), (13, 23)}
R_PAIRS = [(9, 5), (9, 11), (9, 13)]
R_STRATA = [((7, 0, 2), 500000), ((6, 0, 3), 200000), ((6, 1, 4), 200000), ((6, 2, 5), 200000), ((4, 0, 1), 200000)] + [
    ((3, i, j), 100000) for i, j in ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2))] + [((2, 0, 1), 300000)]
FIXED = {"e": 9, "p": 17, "f": [((9, 0, 0), 1), ((1, 8, 0), 1)], "g": [((0, 9, 0), 1), ((7, 0, 1), 1)]}


def _load_exp010_run():
    spec = importlib.util.spec_from_file_location("exp010_run", EXP10 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp010_run"] = mod
    spec.loader.exec_module(mod)
    return mod


R = _load_exp010_run()
log = R.log


def l_stratum(e):
    return (e - 1, 0, 1)


def _spec(family, e, p, stratum, budget):
    return X.make_spec(family, e, p, *stratum, budget, True)


def plan(family, only=None):
    """The ordered cases of a family (specs of EXP-010), in the order of the hypothesis."""
    if family == "K":
        specs = [_spec("K", e, p, l_stratum(e), BUDGET_CASE) for e, p in K_CASES]
    elif family == "L":
        specs = [_spec("L", e, p, l_stratum(e), BUDGET_CASE) for e, p in L_PAIRS]
    elif family == "R":
        specs = [_spec("R", e, p, st, b) for e, p in R_PAIRS for st, b in R_STRATA]
    else:
        raise ValueError(family)
    return [s for s in specs if (s["e"], s["p"]) in only] if only else specs


def in_stratum(e, m, i, j, f, g):
    return R._in_stratum(e, m, i, j, f, g)


# ------------------------------------------------------------------ store
def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-015", "hypothesis": "hypothesis.md (frozen)", "strata": {}, "gates": {}, "runs": [],
            "budget": {"used_seconds": 0.0, "limit_seconds": BUDGET_SECONDS}}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
    tmp.replace(RESULTS)


def opt(name, default):
    return R.opt(name, default)


def workers():
    return max(1, min(MAX_WORKERS, int(opt("workers", MAX_WORKERS))))


# ------------------------------------------------------------------ gates
def fixed_member():
    e, p = FIXED["e"], FIXED["p"]
    f, g = R._pair_vectors(e, [FIXED["f"], FIXED["g"]])
    t = X.betti_table(e, p, f, g)
    hf = bool(X.pure_hilbert_full(e, p, f, g))
    return {"case": "f = x^9 + x y^8, g = y^9 + x^7 z over GF(17)", "pure_hilbert": hf, "betti": X.table_rows(t),
            "ok": bool(t == X.pure_table(e) and hf)}


def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp015.py", "-q"], cwd=str(ROOT), capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def gates_ok(res):
    g = res.get("gates", {})
    return g.get("G1", {}).get("fixed", {}).get("ok") is True and g.get("G3", {}).get("passed") is True


def cmd_gates():
    res = load()
    t0 = time.time()
    fm = fixed_member()
    res["gates"].setdefault("G1", {})["fixed"] = fm
    log("G1 fixed member: %s" % ("PASSED" if fm["ok"] else "FAILED"))
    ok = fm["ok"]
    if ok:
        g3 = gate_g3()
        res["gates"]["G3"] = g3
        ok = g3["passed"]
        log("G3 %s: %s" % ("PASSED" if ok else "FAILED", g3["last_line"]))
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    return 0 if ok else 1


def k_key(e, p):
    return "K|%d|%d|%d|%d|%d" % ((e, p) + l_stratum(e))


def g1_family_part(res):
    """Gate G1 after family K: pure members at (9, 17) and (8, 13); no member with the pure Hilbert function at (9, 13) and (8, 11), the
    two enumerated in full."""
    rows = []
    for e, p in K_CASES:
        s = res["strata"].get(k_key(e, p))
        if (e, p) in ((9, 17), (8, 13)):
            rows.append({"pair": [e, p], "expect": "pure members", "pure": None if s is None else s["pure"], "ok": bool(s and s["pure"] > 0)})
        else:
            rows.append({"pair": [e, p], "expect": "no member with the pure Hilbert function, all members examined",
                         "pure_hilbert": None if s is None else s["pure_hilbert"], "examined": None if s is None else s["examined"],
                         "all_members": bool(s and s["all_members"] and s["complete"]),
                         "ok": bool(s and s["pure_hilbert"] == 0 and s["examined"] > 0 and s["all_members"] and s["complete"])})
    return {"passed": all(r["ok"] for r in rows), "rows": rows}


# ------------------------------------------------------------------ cases
def cmd_cases():
    res = load()
    if not gates_ok(res):
        log("the fixed member of G1 and G3 have not both passed; run `gates` first")
        return 1
    fam = opt("family", "")
    if fam not in FAMILIES:
        log("--family K|L|R is required")
        return 2
    if fam != "K" and not res["gates"].get("G1", {}).get("family", {}).get("passed"):
        log("family K has not passed the family part of G1; run `cases --family K` first")
        return 1
    only = R.pair_list()
    specs = plan(fam, only)
    remaining = [s for s in specs if s["key"] not in res["strata"]]
    used = res["budget"]["used_seconds"]
    left = float(opt("budget-seconds", BUDGET_SECONDS - used))
    t0 = time.time()
    log("family %s: %d cases planned, %d to do; budget left %.0f s (used %.0f s of %d s)" % (fam, len(specs), len(remaining), left, used,
                                                                                          BUDGET_SECONDS))
    rc = R.run_specs(res, remaining, workers(), chunk=int(opt("chunk", 0)) or None, deadline=t0 + left, save_fn=save)
    dt = time.time() - t0
    res["budget"]["used_seconds"] = round(used + dt, 1)
    res["runs"].append({"command": "cases", "family": fam, "only": opt("only", None), "workers": workers(), "seconds": round(dt, 1)})
    if fam == "K" and all(s["key"] in res["strata"] for s in plan("K")):
        res["gates"]["G1"]["family"] = g1_family_part(res)
        ok = res["gates"]["G1"]["family"]["passed"]
        log("G1 (family part) %s" % ("PASSED" if ok else "FAILED: " + json.dumps([r for r in res["gates"]["G1"]["family"]["rows"] if not r["ok"]])))
        rc = 0 if ok else 1
    save(res)
    log("family %s: %d of %d cases stored; %.0f s this run" % (fam, sum(1 for s in specs if s["key"] in res["strata"]), len(specs), dt))
    return rc


# ------------------------------------------------------------------ G2
def g2_sample(res):
    """The first three pure members of every case that has one."""
    out = []
    for key, s in sorted(res["strata"].items(), key=lambda kv: (kv[1]["family"], kv[1]["e"], kv[1]["p"], kv[1]["m"], kv[0])):
        out += [(key, m) for m in [m for m in s["members"] if m["pure"]][:G2_PER_CASE]]
    return out


def cmd_second():
    import exp009_singular as Sg
    res = load()
    t0 = time.time()
    if not gates_ok(res):
        log("the fixed member of G1 and G3 have not both passed; run `gates` first")
        return 1
    ok, version = R.singular_available()
    if not ok:
        res["gates"]["G2"] = {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version,
                              "note": "single-instrument results"}
        save(res)
        log("G2 BLOCKED: " + version)
        return 1
    out_dir = Path(opt("out-dir", "E:/_Datos/caos-research/boij-soderberg-realizability/EXP-015"))
    out_dir.mkdir(parents=True, exist_ok=True)
    SING.mkdir(parents=True, exist_ok=True)
    sample = g2_sample(res)
    log("G2: %d pure members in the sample (%s)" % (len(sample), version))

    def one(item):
        key, mem = item
        s = res["strata"][key]
        e, p = s["e"], s["p"]
        name = "e%d_p%d_m%d_%d_%d_idx%d" % (e, p, s["m"], s["i"], s["j"], mem["index"])
        field = {"name": "GF(%d)" % p, "uhlib_name": "GF(%d)" % p, "char": p, "degree": 1, "modulus": None}
        return name, Sg.run_member(name, field, X.basis_json(e, p, mem["f"], mem["g"]), out_dir)

    with ThreadPoolExecutor(max_workers=min(8, workers())) as tp:
        outs = list(tp.map(one, sample))
    rows, bad, errors = [], [], []
    for (key, mem), (name, (t, dt, err)) in zip(sample, outs):
        e = res["strata"][key]["e"]
        row = {"stratum": key, "index": mem["index"], "script": name + ".sing", "seconds": round(dt, 1), "betti_I1": mem["betti"]}
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
    spec = importlib.util.spec_from_file_location("exp015_make_summary", HERE / "make_summary.py")
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    res = load()
    res["totals"] = ms.compute_totals(res)
    res["predictions"] = ms.predictions(res, res["totals"])
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
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
