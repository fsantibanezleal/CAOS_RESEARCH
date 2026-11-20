"""EXP-007: the family of pure pairs through <x^e, y^e> (tangent space of the rank locus D_e, explicit pure pairs over the
rationals, the linear family L_e, the plane section at e = 4, the common-factor locus).

Run from the repository root, with the repository virtual environment:
    python <this file> gates [--workers=N]     G1 (known answers), G2 (the tangent routine on known cases), G4 (pytest); exit 1 and the
                                               failing cases on a failure (a failed gate stops the run)
    python <this file> cases [--only=T1,T2,..] [--workers=N] [--budget-seconds=7200]   statements T1 to T6, resumable
    python <this file> second [--workers=N]    G3: Singular (Plural, through WSL) on W_0 (e = 4, 5), P1 to P5, C1 and C2
    python <this file> table                   gates, statements and predictions P1 to P6 into results.json, then results-summary.md

The hypothesis is hypothesis.md (frozen).  First instrument: exp007_routine.py over `uhlib` and exact linear algebra
(python-flint, exact).  Second instrument: Singular 4.3.2 (Plural), exp007_singular.py (the generator of EXP-005).  No machine
path is written to any artifact.  At most 8 worker processes, at most 7200 s of wall time per `cases` command, at most 1200 s per
case (a case loop that reaches the limit returns what it computed marked unfinished).
"""
import itertools
import json
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))

import exp007_routine as R  # noqa: E402
import exp007_singular as Sg  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
LOG = ART / "run.log"
T0 = time.time()
MAX_WORKERS = 8
CASE_LIMIT = 1200.0
BIG_P = "GF(32003)"
T2_FIELDS = {4: ("GF(13)", "GF(17)", BIG_P), 5: ("GF(13)", "GF(17)", BIG_P), 6: ("GF(13)", "GF(17)", BIG_P),
             7: ("GF(17)", BIG_P)}
T2_EXPECTED = {(4, "GF(13)"): 12, (4, "GF(17)"): 12, (4, BIG_P): 12, (5, "GF(13)"): 16, (5, "GF(17)"): 16, (5, BIG_P): 16,
               (6, "GF(13)"): 22, (6, "GF(17)"): 20, (6, BIG_P): 20, (7, "GF(17)"): 26, (7, BIG_P): 24}
T3_NAMES = ("W0_e4", "W0_e5", "P1", "P2", "P3", "P4", "P5", "C1", "C2")
G3_NAMES = T3_NAMES
T4_RANDOM = 200
T4_CHUNK = 50
T6_SPACES = 20
T6_CASES = {4: 1, 5: 2, 6: 4}  # e -> degree d of the common factor
HILBERT_FAR = 24


def log(msg):
    line = "[%8.1fs] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-007", "hypothesis": "hypothesis.md (frozen)", "cases": {}, "gates": {}, "runs": []}


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


# ------------------------------------------------------------------ gates G1, G2, G4
def gate_g1():
    """W_0 is pure over the rationals for e = 4, 5, 6, 7 (Betti table computed through uhlib) and rank mu_3e is r."""
    F = R.make_field("QQ")
    rows, bad = [], []
    for e in (4, 5, 6, 7):
        C = R.power_pair_basis(F, e)
        r3 = R.rank_mu(F, C, e, 3 * e)
        t, _ = R.betti_table(F, C, e)
        row = {"e": e, "field": "QQ", "rank_mu_3e": r3, "r": R.target_rank(e), "betti": R.table_rows(t),
               "pure": t == R.pure_table(e), "ok": t == R.pure_table(e) and r3 == R.target_rank(e)}
        rows.append(row)
        if not row["ok"]:
            bad.append(row)
    return {"passed": not bad, "cases": rows, "failing_cases": bad}


def gate_g2():
    """The tangent routine with B the identity of the space of matrices: 10 for 3 x 4 matrices of rank <= 2 at a random matrix of
    rank 2, and 3 for 2 x 2 matrices of rank <= 1 at a matrix of rank 1 (over the rationals and over GF(32003))."""
    rows, bad = [], []
    for fname in ("QQ", BIG_P):
        F = R.make_field(fname)
        for nr, nc, rk, expect, seed in ((3, 4, 2, 10, R.SEED_BASE), (2, 2, 1, 3, R.SEED_BASE + 1)):
            m = R.random_rank_matrix(F, nr, nc, rk, seed)
            d = R.tangent_all_matrices(F, m, nc)
            ok = d["rank_A"] == rk and d["tangent_dim"] == expect
            row = {"field": fname, "shape": [nr, nc], "rank": rk, "matrix": m, "seed": seed, "expected_dimension": expect,
                   "rank_A": d["rank_A"], "dim_K": d["dim_K"], "coker_dim": d["coker_dim"], "rank_T": d["rank_T"],
                   "tangent_dim": d["tangent_dim"], "ok": ok}
            rows.append(row)
            if not ok:
                bad.append(row)
    return {"passed": not bad, "cases": rows, "failing_cases": bad}


def gate_g4():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp007.py", "-q", "-p", "no:cacheprovider"],
                          cwd=str(ROOT), capture_output=True, text=True)
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
            break
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    if failed:
        log("GATE FAILED: %s; the run stops here; failing cases: %s" % (failed, json.dumps(res["gates"][failed].get("failing_cases"))[:1500]))
        return 1
    log("G1, G2, G4 passed (G3 is run by `second` after the cases)")
    return 0


# ------------------------------------------------------------------ the cases (each a top-level function, run in a worker)
def _space_record(F, C, e, ev, name=None):
    rec = {"field": R.fname(F), "e": e, "basis": R.basis_json(F, C, e), "coefficients": R.coef_lists(F, C), "monomials": [list(m) for m in R.A.monos(e)]}
    rec["text"] = [R.poly_text(F, p) for p in rec["basis"]]
    rec.update(ev)
    if name:
        rec["name"] = name
    return rec


def case_t1(spec):
    F = R.make_field(spec["field"])
    d = R.tangent_at_power_pair(F, spec["e"])
    e = spec["e"]
    d.update({"statement": "T1", "field": spec["field"], "e": e})
    d["holds"] = bool(d["rank_A"] == R.target_rank(e) and d["dim_K"] == 2 and d["coker_dim"] == R.h_e(e, 3 * e)
                      and d["tangent_dim"] == 4 * e - 4 and d["orbit_directions_in_tangent_space"] and d["orbit_directions_rank"] == 2)
    return d


def case_t2(spec):
    F = R.make_field(spec["field"])
    e = spec["e"]
    d = R.tangent_at_power_pair(F, e)
    d.update({"statement": "T2", "field": spec["field"], "e": e, "expected_tangent_dim": T2_EXPECTED[(e, spec["field"])]})
    d["holds"] = d["tangent_dim"] == d["expected_tangent_dim"]
    return d


def case_t3(spec):
    name = spec["name"]
    e, polys = R.named_spaces()[name]
    F = R.make_field("QQ")
    C = R.space_of(F, e, polys)
    far = HILBERT_FAR if name == "C2" else None
    ev = R.evaluate_space(F, C, e, hilbert_to=far)
    rec = _space_record(F, C, e, ev, name)
    rec["statement"] = "T3"
    pure_names = ("W0_e4", "W0_e5", "P1", "P2", "P3", "P4", "P5")
    if name in pure_names:
        want_outside = not name.startswith("W0")
        rec["expected"] = "rank mu_3e = r, pure table, %s the orbit" % ("outside" if want_outside else "inside")
        rec["holds_first_instrument"] = bool(ev["rank_mu_3e"] == R.target_rank(e) and ev["pure"]
                                             and ev["orbit"]["outside_orbit"] == want_outside
                                             and (want_outside or ev["orbit"]["dim_S_plus_W"] == e + 1))
    elif name == "C1":
        rec["expected"] = "rank mu_12 = 49 and not pure"
        rec["holds_first_instrument"] = bool(ev["rank_mu_3e"] == 49 and not ev["pure"])
    else:
        rec["expected"] = "rank mu_12 = 46 and infinite length (nonzero in every degree up to 24)"
        rec["nonzero_in_every_degree_to_24"] = all(h > 0 for h in ev["hilbert"][: HILBERT_FAR + 1])
        rec["holds_first_instrument"] = bool(ev["rank_mu_3e"] == 46 and rec["nonzero_in_every_degree_to_24"])
    return rec


def case_t4_qq(spec, deadline):
    e = spec["e"]
    F = R.make_field("QQ")
    r = R.target_rank(e)
    hist, over, done = {}, [], 0
    for a, b, c, d in itertools.product(range(-2, 3), repeat=4):
        if time.time() > deadline:
            break
        C = R.space_of(F, e, R.family_L(e, a, b, c, d))
        r3 = R.rank_mu(F, C, e, 3 * e)
        hist[str(r3)] = hist.get(str(r3), 0) + 1
        done += 1
        if r3 > r:
            over.append({"abcd": [a, b, c, d], "rank_mu_3e": r3, "basis": R.basis_json(F, C, e)})
    return {"statement": "T4", "field": "QQ", "e": e, "members_planned": 625, "members_done": done, "target_rank_r": r,
            "rank_hist": {k: hist[k] for k in sorted(hist, key=int)}, "rank_le_r": sum(v for k, v in hist.items() if int(k) <= r),
            "members_above_r": over, "unfinished": done < 625,
            "holds": done == 625 and not over}


def case_t4_gf(spec, deadline):
    e = spec["e"]
    F = R.make_field(BIG_P)
    r = R.target_rank(e)
    members, done = [], 0
    for idx in range(spec["start"], spec["end"]):
        if time.time() > deadline:
            break
        a, b, c, d = R.draw_L_params(F.p, idx)
        C = R.space_of(F, e, R.family_L(e, a, b, c, d))
        ev = R.evaluate_space(F, C, e) if R.rank_mu(F, C, e, 3 * e) <= r else {"rank_mu_3e": R.rank_mu(F, C, e, 3 * e),
                                                                           "pure": False, "orbit": R.orbit_test(F, C, e)}
        done += 1
        keep = {"index": idx, "seed": R.SEED_BASE + idx, "abcd": [a, b, c, d], "rank_mu_3e": ev["rank_mu_3e"], "pure": ev["pure"],
                "outside_orbit": ev["orbit"]["outside_orbit"], "dim_S_plus_W": ev["orbit"]["dim_S_plus_W"],
                "betti": ev.get("betti"), "pure_hilbert": ev.get("pure_hilbert")}
        if ev["rank_mu_3e"] > r or not (ev["pure"] and ev["orbit"]["outside_orbit"]):
            keep["basis"] = R.basis_json(F, C, e)
            keep["text"] = [R.poly_text(F, p) for p in keep["basis"]]
        members.append(keep)
    return {"statement": "T4", "field": BIG_P, "e": e, "start": spec["start"], "end": spec["end"], "members_done": done,
            "target_rank_r": r, "members": members, "unfinished": done < spec["end"] - spec["start"]}


def case_t5_grid(spec, deadline):
    F = R.make_field("QQ")
    rows, done = [], 0
    for al, be, ga in itertools.product(range(-4, 5), repeat=3):
        if time.time() > deadline:
            break
        C = R.space_of(F, 4, R.family_plane(al, be, ga))
        r3 = R.rank_mu(F, C, 4, 12)
        rows.append([al, be, ga, r3])
        done += 1
    on_plane = [x for x in rows if 8 * x[0] + 31 * x[1] + 118 * x[2] == 0]
    low = [x for x in rows if x[3] <= 48]
    mism = [x for x in rows if (x[3] <= 48) != (8 * x[0] + 31 * x[1] + 118 * x[2] == 0)]
    hist = {}
    for x in rows:
        hist[str(x[3])] = hist.get(str(x[3]), 0) + 1
    return {"statement": "T5", "part": "grid", "field": "QQ", "e": 4, "spaces_planned": 729, "spaces_done": done,
            "plane_points": len(on_plane), "rank_le_48": len(low), "rank_hist": {k: hist[k] for k in sorted(hist, key=int)},
            "points_on_plane": [x[:3] for x in on_plane], "mismatches": mism, "unfinished": done < 729,
            "holds": done == 729 and not mism}


def case_t5_pure(spec):
    F = R.make_field("QQ")
    out = []
    for dirn in ((31, -8, 0), (59, 0, -4)):
        for t in (1, 2, 3):
            al, be, ga = (t * dirn[0], t * dirn[1], t * dirn[2])
            C = R.space_of(F, 4, R.family_plane(al, be, ga))
            ev = R.evaluate_space(F, C, 4)
            rec = _space_record(F, C, 4, ev, "plane(%d,%d,%d)" % (al, be, ga))
            rec.update({"alpha_beta_gamma": [al, be, ga], "direction": list(dirn), "t": t,
                        "equation_value": 8 * al + 31 * be + 118 * ga})
            out.append(rec)
    return {"statement": "T5", "part": "pure", "field": "QQ", "e": 4, "spaces": out,
            "holds": all(s["pure"] and s["rank_mu_3e"] <= 48 for s in out)}


def case_t6(spec, deadline):
    e, d = spec["e"], spec["d"]
    F = R.make_field(BIG_P)
    r = R.target_rank(e)
    spaces, done = [], 0
    for idx in range(T6_SPACES):
        if time.time() > deadline:
            break
        rows, (q, a, b) = R.draw_common_factor_space(F, e, d, idx)
        C = rows
        r3 = R.rank_mu(F, C, e, 3 * e)
        hl = R.hilbert_list(F, C, e, HILBERT_FAR)
        done += 1
        rec = {"index": idx, "seed": R.SEED_BASE + idx, "q": q, "a": a, "b": b, "rank_mu_3e": r3, "rank_le_r": r3 <= r,
               "hilbert_to_24": hl, "nonzero_in_every_degree_to_24": all(h > 0 for h in hl)}
        if not (r3 <= r) or (e == 4 and not rec["nonzero_in_every_degree_to_24"]):
            rec["basis"] = R.basis_json(F, C, e)
            rec["text"] = [R.poly_text(F, p) for p in rec["basis"]]
        spaces.append(rec)
    out = {"statement": "T6", "field": BIG_P, "e": e, "common_factor_degree": d, "target_rank_r": r, "spaces_done": done,
           "spaces_planned": T6_SPACES, "spaces": spaces, "rank_le_r": sum(1 for s in spaces if s["rank_le_r"]),
           "unfinished": done < T6_SPACES}
    out["infinite_length_count"] = sum(1 for s in spaces if s["nonzero_in_every_degree_to_24"])
    out["holds"] = done == T6_SPACES and out["rank_le_r"] == T6_SPACES and (e != 4 or out["infinite_length_count"] == T6_SPACES)
    return out


def run_task(spec):
    """Worker entry point: one case; returns (id, record, seconds)."""
    t0 = time.time()
    deadline = t0 + CASE_LIMIT
    kind = spec["kind"]
    if kind == "T1":
        rec = case_t1(spec)
    elif kind == "T2":
        rec = case_t2(spec)
    elif kind == "T3":
        rec = case_t3(spec)
    elif kind == "T4qq":
        rec = case_t4_qq(spec, deadline)
    elif kind == "T4gf":
        rec = case_t4_gf(spec, deadline)
    elif kind == "T5grid":
        rec = case_t5_grid(spec, deadline)
    elif kind == "T5pure":
        rec = case_t5_pure(spec)
    elif kind == "T6":
        rec = case_t6(spec, deadline)
    else:
        raise ValueError(kind)
    rec["seconds"] = round(time.time() - t0, 2)
    return spec["id"], rec


def task_specs():
    out = []
    for e in (4, 5, 6, 7):
        out.append({"id": "T1|QQ|e%d" % e, "stmt": "T1", "kind": "T1", "field": "QQ", "e": e})
    for e, fields in T2_FIELDS.items():
        for f in fields:
            out.append({"id": "T2|%s|e%d" % (f, e), "stmt": "T2", "kind": "T2", "field": f, "e": e})
    for n in T3_NAMES:
        out.append({"id": "T3|%s" % n, "stmt": "T3", "kind": "T3", "name": n})
    for e in (4, 5):
        out.append({"id": "T4|QQ|e%d" % e, "stmt": "T4", "kind": "T4qq", "e": e})
        for s in range(0, T4_RANDOM, T4_CHUNK):
            out.append({"id": "T4|%s|e%d|%03d-%03d" % (BIG_P, e, s, s + T4_CHUNK), "stmt": "T4", "kind": "T4gf", "e": e, "start": s,
                        "end": s + T4_CHUNK})
    out.append({"id": "T5|grid", "stmt": "T5", "kind": "T5grid"})
    out.append({"id": "T5|pure", "stmt": "T5", "kind": "T5pure"})
    for e, d in T6_CASES.items():
        out.append({"id": "T6|e%d|d%d" % (e, d), "stmt": "T6", "kind": "T6", "e": e, "d": d})
    return out


def cmd_cases():
    res = load()
    if not all(res.get("gates", {}).get(g, {}).get("passed") for g in ("G1", "G2", "G4")):
        log("G1, G2, G4 have not all passed; run `gates` first")
        return 1
    t0 = time.time()
    budget_end = t0 + float(opt("budget-seconds", 7200))
    only = [s for s in opt("only", "").split(",") if s]
    specs = [s for s in task_specs() if not only or s["stmt"] in only]
    todo = [s for s in specs if s["id"] not in res["cases"]]
    todo.sort(key=lambda s: {"T4gf": 0, "T6": 1, "T3": 2, "T4qq": 3, "T5grid": 4}.get(s["kind"], 5))
    log("cases: %d to compute, %d already stored" % (len(todo), len(specs) - len(todo)))
    done_n = 0
    with ProcessPoolExecutor(max_workers=workers()) as pool:
        pending, it = set(), iter(todo)

        def submit_next():
            if time.time() > budget_end:
                return False
            s = next(it, None)
            if s is None:
                return False
            pending.add(pool.submit(run_task, s))
            return True

        for _ in range(workers()):
            submit_next()
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for fut in done:
                pending.discard(fut)
                cid, rec = fut.result()
                res["cases"][cid] = rec
                done_n += 1
                submit_next()
                save(res)
                log("case %s done in %.1f s%s" % (cid, rec["seconds"], " (UNFINISHED)" if rec.get("unfinished") else ""))
    left = [s["id"] for s in specs if s["id"] not in res["cases"]]
    res["runs"].append({"command": "cases", "seconds": round(time.time() - t0, 1), "only": only, "cases_done": done_n, "cases_left": len(left)})
    save(res)
    log("cases: %d stored in total, %d not reached %s" % (len(specs) - len(left), len(left), left[:5]))
    return 0


# ------------------------------------------------------------------ G3: the second instrument
def singular_available():
    try:
        p = subprocess.run(["wsl", "-e", "bash", "-c", "Singular -v < /dev/null | head -1"], capture_output=True, text=True, timeout=120)
    except Exception as exc:
        return False, repr(exc)[:200]
    lines = [ln for ln in p.stdout.splitlines() if "Singular" in ln]
    return p.returncode == 0 and bool(lines), lines[0].strip() if lines else p.stderr[:200]


def _g3_one(item):
    name, rec = item
    t, dt, err = Sg.run_space("G3_" + name, rec["basis"], SING)
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
    missing = [n for n in G3_NAMES if "T3|%s" % n not in res["cases"]]
    if missing:
        log("T3 cases missing for G3: %s; run `cases` first" % missing)
        return 1
    SING.mkdir(parents=True, exist_ok=True)
    items = [(n, res["cases"]["T3|%s" % n]) for n in G3_NAMES]
    log("G3: %d spaces (%s)" % (len(items), version))
    with ThreadPoolExecutor(max_workers=workers()) as tp:
        outs = list(tp.map(_g3_one, items))
    rows, bad, errors = [], [], []
    for (name, rec), (_, t, dt, err) in zip(items, outs):
        e = rec["e"]
        row = {"name": name, "e": e, "script": "G3_%s.sing" % name, "output": "G3_%s.out" % name, "seconds": round(dt, 1)}
        if err or t is None:
            row["error"] = err
            errors.append(name)
        elif name == "C2":
            hs = Sg.hilbert_from_table(t, HILBERT_FAR)
            row["betti_I2"] = [[i, j, r] for (i, j), r in sorted(t.items())]
            row["hilbert_I2_to_24"] = hs
            row["hilbert_I1_to_24"] = rec["hilbert"][: HILBERT_FAR + 1]
            row["agree"] = hs == row["hilbert_I1_to_24"]
            row["compared"] = "Hilbert function up to degree 24 (module of infinite length: the first instrument has no finite Betti table)"
            if not row["agree"]:
                bad.append(name)
        else:
            row["betti_I1"] = rec["betti"]
            row["betti_I2"] = [[i, j, r] for (i, j), r in sorted(t.items())]
            row["agree"] = [tuple(x) for x in rec["betti"]] == [tuple(x) for x in row["betti_I2"]]
            row["pure_I2"] = t == R.pure_table(e)
            hs = Sg.hilbert_from_table(t, R.hilbert_bound(e))
            row["hilbert_I2_equals_I1"] = hs == rec["hilbert"][: R.hilbert_bound(e) + 1]
            row["compared"] = "Betti table"
            if not row["agree"] or not row["hilbert_I2_equals_I1"]:
                bad.append(name)
        rows.append(row)
    res["gates"]["G3"] = {"passed": not bad and not errors, "singular": version, "spaces": len(items), "agree": sum(1 for r in rows if r.get("agree")),
                          "failing_cases": bad, "singular_errors": errors, "rows": rows}
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    save(res)
    g = res["gates"]["G3"]
    log("G3 %s: %d of %d agree; failing %s; errors %s" % ("PASSED" if g["passed"] else "FAILED", g["agree"], len(items), bad, errors))
    return 0 if g["passed"] else 1


# ------------------------------------------------------------------ table
def cmd_table():
    import make_summary
    res = load()
    res["statements"] = make_summary.statements(res)
    res["predictions"] = make_summary.predictions(res)
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
    save(res)
    print(make_summary.table_text(res))
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
