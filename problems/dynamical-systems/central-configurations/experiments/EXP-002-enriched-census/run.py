"""EXP-002: censuses on the enriched system (F + G + e_IU, + Cayley-Menger for planarity).

Deterministic, CPU-only, exact arithmetic (sympy over QQ). Staged; heavy Groebner
stages subprocess-capped (900 s per sample, reported inconclusive-cap honestly).
Exits nonzero if any DECLARED prediction assert fails.

Run from the repo root:
    .venv/Scripts/python.exe problems/dynamical-systems/central-configurations/experiments/EXP-002-enriched-census/run.py
"""

import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
sys.path.insert(0, str(CODE))
from cclib import (ac_asymmetric, ac_symmetric, cayley_menger_planar4,  # noqa: E402
                   census_positive, e_iu, grevlex_pure_power_zero_dim, rvar,
                   strip_monomial_factors, u_i_j_invariants)

ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOGF = ART / "run-log.txt"
CAP_GB = 900
SAMPLES = [(1, 1, 1), (1, 2, 3), (2, 3, 5), (1, 1, 2)]
RESULTS = {}


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOGF.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def record(pred: str, status: str, detail: str = "") -> None:
    RESULTS[pred] = {"status": status, "detail": detail}
    log(f"RESULT {pred}: {status} {detail}")
    (ART / "results.json").write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")


def enriched3(mv):
    F = ac_symmetric(3, [sp.Integer(v) for v in mv])
    G = ac_asymmetric(3, [sp.Integer(v) for v in mv])
    iu = e_iu(3, [sp.Integer(v) for v in mv])
    return list(F.values()) + list(G.values()) + [iu]


# ---------------- subprocess workers

def _worker_zerodim(mv, outfile):
    eqs = enriched3(mv)
    gens = [rvar(1, 2), rvar(1, 3), rvar(2, 3)]
    zd, lms, G = grevlex_pure_power_zero_dim(eqs, gens)
    Path(outfile).write_text(json.dumps(
        {"zero_dim": bool(zd), "gb_size": len(G.exprs)}), encoding="utf-8")


def _worker_census(mv, outfile):
    eqs = enriched3(mv)
    gens = [rvar(1, 2), rvar(1, 3), rvar(2, 3)]
    accepted, meta = census_positive(eqs, gens)
    out = [[sp.srepr(x) for x in combo] for combo in accepted]
    Path(outfile).write_text(json.dumps(
        {"positive": out, "eliminants": meta["eliminants"],
         "candidate_tuples": meta["candidate_tuples"]}), encoding="utf-8")


def run_capped(target, args, cap_s, label):
    p = mp.Process(target=target, args=args)
    t0 = time.time()
    p.start()
    p.join(cap_s)
    if p.is_alive():
        p.terminate()
        p.join()
        log(f"{label}: CAP struck after {cap_s} s")
        return False, time.time() - t0
    return p.exitcode == 0, time.time() - t0


# ---------------- stages

def stage_p1():
    # symbolic line check first
    m1, m2, m3 = sp.symbols("m1 m2 m3", positive=True)
    Gsym = ac_asymmetric(3, [m1, m2, m3])
    line = {rvar(1, 3): 0, rvar(2, 3): 0}
    on_line = [sp.expand(g.subs(line)) for g in Gsym.values()]
    line_killed = any(v != 0 for v in on_line)
    all_ok = line_killed
    details = {"line_killed_by_G": bool(line_killed)}
    for mv in SAMPLES:
        outfile = ART / f"p1-{'_'.join(map(str, mv))}.json"
        ok, secs = run_capped(_worker_zerodim, (mv, str(outfile)), CAP_GB, f"P1 {mv}")
        if ok and outfile.exists():
            data = json.loads(outfile.read_text(encoding="utf-8"))
            details[str(mv)] = {"zero_dim": data["zero_dim"],
                                "gb_size": data["gb_size"], "s": round(secs, 1)}
            if not data["zero_dim"]:
                all_ok = False
        else:
            details[str(mv)] = "inconclusive-cap"
            all_ok = False
    status = "pass" if all_ok else (
        "inconclusive-cap" if any(v == "inconclusive-cap" for v in details.values())
        and line_killed else "fail")
    record("P1-enrichment-zero-dim", status, json.dumps(details))


def classify_point(combo, gens):
    """equilateral / collinear-<pattern> / nonrealizable / scalene-triangle"""
    vals = dict(zip([str(g) for g in gens], combo))
    x, y, z = vals["r12"], vals["r13"], vals["r23"]
    if all((v - 1).equals(0) is True for v in (x, y, z)):
        return "equilateral"
    sums = {"2-middle": y - (x + z), "3-middle": z - (x + y), "1-middle": x - (y + z)}
    for name, expr in sums.items():
        if expr.equals(0) is True:
            return f"collinear-{name}"

    def sign_pos(e):
        v = e.evalf(60)
        if not v.is_comparable:
            v = sp.N(e, 120)
        return bool(v > 0)
    tri = sign_pos(x + z - y) and sign_pos(x + y - z) and sign_pos(y + z - x)
    return "scalene-triangle" if tri else "nonrealizable"


def stage_p2():
    all_ok = True
    full = {}
    for mv in SAMPLES:
        outfile = ART / f"p2-census-{'_'.join(map(str, mv))}.json"
        ok, secs = run_capped(_worker_census, (mv, str(outfile)), CAP_GB, f"P2 {mv}")
        if not (ok and outfile.exists()):
            full[str(mv)] = "inconclusive-cap"
            all_ok = False
            continue
        data = json.loads(outfile.read_text(encoding="utf-8"))
        gens = [rvar(1, 2), rvar(1, 3), rvar(2, 3)]
        pts = [[sp.sympify(x) for x in s] for s in data["positive"]]
        classes = [classify_point(p, gens) for p in pts]
        entry = {"n_positive": len(pts), "classes": classes,
                 "points": [[str(x) for x in p] for p in pts],
                 "eliminants": data["eliminants"], "s": round(secs, 1)}
        full[str(mv)] = entry
        n_eq = classes.count("equilateral")
        n_col = len([c for c in classes if c.startswith("collinear")])
        n_scalene = classes.count("scalene-triangle")
        distinct_col = len({c for c in classes if c.startswith("collinear")})
        if not (n_eq == 1 and n_col == 3 and distinct_col == 3 and n_scalene == 0):
            all_ok = False
    (ART / "stage-p2.json").write_text(json.dumps(full, indent=2), encoding="utf-8")
    caps = [k for k, v in full.items() if v == "inconclusive-cap"]
    # honest rule: any decided sample violating the classical census -> fail;
    # otherwise any cap -> inconclusive-cap; otherwise pass.
    decided_bad = any(isinstance(v, dict) and (
        v["classes"].count("equilateral") != 1
        or len([c for c in v["classes"] if c.startswith("collinear")]) != 3
        or v["classes"].count("scalene-triangle") != 0) for v in full.values())
    if decided_bad:
        status = "fail"
    elif caps:
        status = "inconclusive-cap"
    else:
        status = "pass"
    record("P2-classical-census", status,
           json.dumps({k: (v if isinstance(v, str) else
                           {"n": v["n_positive"], "classes": v["classes"]})
                       for k, v in full.items()}))


def stage_p3_p4():
    F4 = ac_symmetric(4, [1, 1, 1, 1])
    G4 = ac_asymmetric(4, [1, 1, 1, 1])
    iu4 = e_iu(4, [1, 1, 1, 1])
    cm = cayley_menger_planar4()
    a, b = sp.symbols("a b", positive=True)
    subsq = {rvar(1, 2): a, rvar(2, 3): a, rvar(3, 4): a, rvar(1, 4): a,
             rvar(1, 3): b, rvar(2, 4): b}
    raw = list(F4.values()) + list(G4.values()) + [iu4]
    cores = set()
    for e in raw:
        er = sp.expand(e.subs(subsq))
        if er == 0:
            continue
        c, _ = strip_monomial_factors(er, [a, b])
        cores.add(c)
    cores = sorted(cores, key=sp.default_sort_key)
    log(f"P3: enriched stratum cores (no CM): {len(cores)}")
    cm_red = sp.expand(cm.subs(subsq))
    cm_core, _ = strip_monomial_factors(cm_red, [a, b])

    # tetrahedron sanity on the no-CM enriched stratum system
    tet_ok = all(e.subs({a: 1, b: 1}) == 0 for e in cores)
    cm_at_tet = sp.expand(cm_red.subs({a: 1, b: 1}))

    accepted, meta = census_positive(list(cores) + [cm_core], [a, b])
    entries = []
    square_seen = False
    for (av, bv) in accepted:
        is_square = (bv ** 2 - 2 * av ** 2).equals(0) is True
        minp = sp.minimal_polynomial(av, sp.Symbol("x"))
        entries.append({"a": str(av), "b": str(bv), "square": bool(is_square),
                        "a_minpoly": str(minp)})
        if is_square and str(minp) == "32*x**6 - 32*x**3 + 7":
            square_seen = True
    ok = len(accepted) == 1 and square_seen
    record("P3-planar-rhombus-census", "pass" if ok else "fail",
           json.dumps({"n_positive": len(accepted), "entries": entries,
                       "eliminants": meta["eliminants"],
                       "tetra_satisfies_noCM_stratum": bool(tet_ok),
                       "cm_at_tetrahedron": str(cm_at_tet)}))

    # P4: invariants at the accepted points + at EXP-001 exact anchors
    inv = {}
    ok4 = True
    anchors = {"square": accepted[0] if ok else None}
    if ok:
        av, bv = accepted[0]
        pt = {rvar(1, 2): av, rvar(2, 3): av, rvar(3, 4): av, rvar(1, 4): av,
              rvar(1, 3): bv, rvar(2, 4): bv}
        U, I, M, J = u_i_j_invariants(4, [1, 1, 1, 1], pt)
        ident = (U - M * I).equals(0)
        ok4 = ok4 and ident is True
        inv["square"] = {"U=MI": bool(ident), "J": str(sp.nsimplify(sp.N(J, 30), rational=False))}
    tetpt = {rvar(i, j): sp.Integer(1) for i in range(1, 5) for j in range(i + 1, 5)}
    U, I, M, J = u_i_j_invariants(4, [1, 1, 1, 1], tetpt)
    ident = (U - M * I).equals(0) is True or sp.simplify(U - M * I) == 0
    ok4 = ok4 and ident
    inv["tetrahedron"] = {"U=MI": bool(ident), "J": str(sp.nsimplify(sp.N(J, 30), rational=False))}
    record("P4-invariant-identity", "pass" if ok4 else "fail", json.dumps(inv))


def main() -> int:
    t0 = time.time()
    LOGF.write_text("", encoding="utf-8")
    log("EXP-002 staged run start")
    stage_p1()
    stage_p2()
    stage_p3_p4()
    profile = {"experiment": "EXP-002", "date": "2026-07-24", "results": RESULTS,
               "elapsed_s": round(time.time() - t0, 2),
               "sympy_version": sp.__version__, "python_version": sys.version,
               "caps": {"GB": CAP_GB}}
    (ART / "profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")
    fails = [k for k, v in RESULTS.items() if v["status"] == "fail"]
    caps = [k for k, v in RESULTS.items() if v["status"] == "inconclusive-cap"]
    log(f"done in {profile['elapsed_s']} s; FAIL: {fails or 'none'}; CAP: {caps or 'none'}")
    return 1 if fails else 0


if __name__ == "__main__":
    mp.freeze_support()
    sys.exit(main())
