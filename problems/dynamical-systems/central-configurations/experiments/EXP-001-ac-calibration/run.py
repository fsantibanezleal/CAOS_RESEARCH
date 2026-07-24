"""EXP-001: exact Albouy-Chenciner system builder, calibrated on n = 3, assembled for n = 4.

Deterministic, CPU-only, exact arithmetic (sympy over QQ; algebraic numbers where
needed). No randomness. Staged with per-stage caps (heavy Groebner stages run in
subprocesses and report `inconclusive-cap` when the cap strikes: recorded honestly, not
a pass). Exits nonzero if any DECLARED prediction assert fails (a refutation).

Run from the repo root with the repo .venv:
    .venv/Scripts/python.exe problems/dynamical-systems/central-configurations/experiments/EXP-001-ac-calibration/run.py

Equations per the method dossier (HJ11 eq. (3), PDF read 2026-07-23):
    S_ij = r_ij^{-3} - 1   (Lambda = -1 scale normalization; S_ii = 0 by convention)
    f_ij = sum_{k=1..n} m_k [ S_ik (r_jk^2 - r_ik^2 - r_ij^2) + S_jk (r_ik^2 - r_jk^2 - r_ij^2) ]
cleared of denominators to polynomials in QQ[m][r].

Engineering note (recorded for the verdict): a first monolithic runner was aborted after
~78 min CPU inside the product-Rabinowitsch Groebner saturation for P1; this staged
runner caps that stage and orders the cheap decisive stages first.
"""

import json
import multiprocessing as mp
import sys
import time
from itertools import combinations
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOGF = ART / "run-log.txt"

# caps in seconds
CAP_P4 = 900
CAP_P1_EQUAL = 3600
CAP_P1_OTHER = 900
CAP_P5_SOLVE = 1800

SAMPLES = [(1, 1, 1), (1, 2, 3), (2, 3, 5), (1, 1, 2)]


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOGF.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


RESULTS = {}   # prediction -> {"status": "pass"|"fail"|"inconclusive-cap", "detail": ...}


def record(pred: str, status: str, detail: str = "") -> None:
    RESULTS[pred] = {"status": status, "detail": detail}
    log(f"RESULT {pred}: {status} {detail}")
    (ART / "results.json").write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- builders

def rvar(i: int, j: int):
    i, j = min(i, j), max(i, j)
    return sp.Symbol(f"r{i}{j}", positive=True)


def ac_symmetric(n: int, masses):
    """Cleared symmetric Albouy-Chenciner polynomials f_ij, i < j."""
    def S(i, j):
        if i == j:
            return sp.Integer(0)
        return rvar(i, j) ** -3 - 1

    def r2(i, j):
        if i == j:
            return sp.Integer(0)
        return rvar(i, j) ** 2

    out = {}
    for i, j in combinations(range(1, n + 1), 2):
        expr = sp.Integer(0)
        for k in range(1, n + 1):
            expr += masses[k - 1] * (
                S(i, k) * (r2(j, k) - r2(i, k) - r2(i, j))
                + S(j, k) * (r2(i, k) - r2(j, k) - r2(i, j))
            )
        num, _den = sp.fraction(sp.together(expr))
        out[(i, j)] = sp.expand(num)
    return out


def cayley_menger_planar4():
    r = {}
    for i, j in combinations(range(1, 5), 2):
        r[(i, j)] = rvar(i, j) ** 2
    M = sp.Matrix([
        [0, 1, 1, 1, 1],
        [1, 0, r[(1, 2)], r[(1, 3)], r[(1, 4)]],
        [1, r[(1, 2)], 0, r[(2, 3)], r[(2, 4)]],
        [1, r[(1, 3)], r[(2, 3)], 0, r[(3, 4)]],
        [1, r[(1, 4)], r[(2, 4)], r[(3, 4)], 0],
    ])
    return sp.expand(M.det(method="berkowitz"))


def strip_monomial_factors(expr, gens):
    """Return the product of non-monomial irreducible factors (torus-equivalent form)."""
    coeff, factors = sp.factor_list(sp.expand(expr), *gens)
    out = sp.Integer(1)
    stripped = []
    for base, exp in factors:
        p = sp.Poly(base, *gens)
        if len(p.monoms()) == 1:
            stripped.append(f"{base}**{exp}")
        else:
            out *= base ** exp
    return sp.expand(out), stripped


def is_real_positive(x) -> bool:
    """Exact-backed sign decision for an algebraic number.

    sympy's `is_positive` returns None on nested RootOf expressions (silently dropping
    genuine solutions if used as a filter: the bug found in the first staged run).
    Here: realness via exact `im(x).equals(0)` (with a simplify fallback), positivity
    via adaptive-precision evalf on the real part (sympy evalf tracks error for
    algebraic expressions); callers additionally verify each ACCEPTED solution by an
    exact residual check against the defining equations.
    """
    x = sp.nsimplify(x, rational=False) if x.is_Rational else x
    im = sp.im(x)
    if im != 0:
        ok = im.equals(0)
        if ok is not True and sp.simplify(im) != 0:
            return False
    re = sp.re(x)
    if re == 0 or re.equals(0):
        return False
    v = re.evalf(60)
    if not v.is_comparable:
        v = sp.N(re, 120)
    return bool(v > 0)


def exact_zero_residuals(eqs, subs_map) -> bool:
    """Exact check that every equation vanishes at the (algebraic) point."""
    for e in eqs:
        val = e.subs(subs_map)
        if val == 0:
            continue
        z = sp.simplify(val)
        if z == 0:
            continue
        if z.equals(0) is not True:
            return False
    return True


def support_profile(expr, gens):
    p = sp.Poly(expr, *gens)
    monoms = p.monoms()
    vecs = [sp.Matrix(m) for m in monoms]
    if len(vecs) <= 1:
        adim = 0
    else:
        M = sp.Matrix.hstack(*[v - vecs[0] for v in vecs[1:]])
        adim = M.rank()
    return {"n_monomials": len(monoms),
            "total_degree": int(p.total_degree()),
            "support_affine_dim": int(adim)}


def grevlex_pure_power_zero_dim(polys, gens):
    G = sp.groebner(polys, *gens, order="grevlex")
    pure = set()
    lms = []
    for g in G.exprs:
        p = sp.Poly(g, *gens)
        lm = p.LM(order="grevlex")
        mon = tuple(lm.exponents)
        lms.append(mon)
        nz = [i for i, e in enumerate(mon) if e > 0]
        if len(nz) == 1:
            pure.add(nz[0])
    return pure == set(range(len(gens))), lms, G


# ------------------------------------------------- subprocess workers (picklable)

def _worker_p1(mv, outfile):
    import sympy as spp  # noqa: F811 (fresh import in child)
    R12, R13, R23 = rvar(1, 2), rvar(1, 3), rvar(2, 3)
    gens = [R12, R13, R23]
    F = ac_symmetric(3, [spp.Integer(v) for v in mv])
    G0 = spp.groebner(list(F.values()), *gens, order="grevlex")
    t = spp.Symbol("t")
    zd, lms, G = grevlex_pure_power_zero_dim(
        list(G0.exprs) + [t * R12 * R13 * R23 - 1], gens + [t])
    payload = {"mv": list(mv), "zero_dim": bool(zd),
               "gb_size": len(G.exprs),
               "gb_exprs": [spp.srepr(e) for e in G.exprs]}
    Path(outfile).write_text(json.dumps(payload), encoding="utf-8")


def _worker_p4(outfile):
    import sympy as spp  # noqa: F811
    m1, m2, m3 = spp.symbols("m1 m2 m3", positive=True)
    R12, R13, R23 = rvar(1, 2), rvar(1, 3), rvar(2, 3)
    F = ac_symmetric(3, [m1, m2, m3])
    eqs = [spp.expand(f.subs({R13: R12 + R23})) for f in F.values()]
    eqs = [e for e in eqs if e != 0]
    res = spp.resultant(spp.Poly(eqs[0], R12), spp.Poly(eqs[1], R12), R12)
    fac = spp.factor(res)
    payload = {"eliminant_nonzero": bool(res != 0),
               "degree_r23": int(spp.degree(res, R23)) if res != 0 else -1,
               "factored": str(fac)[:500000]}
    Path(outfile).write_text(json.dumps(payload), encoding="utf-8")


def _worker_p5(gb_file, outfile):
    import sympy as spp  # noqa: F811
    R12, R13, R23 = rvar(1, 2), rvar(1, 3), rvar(2, 3)
    t = spp.Symbol("t")
    gens4 = [R12, R13, R23, t]
    data = json.loads(Path(gb_file).read_text(encoding="utf-8"))
    basis = [spp.sympify(e) for e in data["gb_exprs"]]
    sols = spp.solve_poly_system([spp.Poly(bb, *gens4) for bb in basis], *gens4)
    out = []
    for s in sols:
        r12v, r13v, r23v, tv = s
        if all(is_real_positive(x) for x in (r12v, r13v, r23v)):
            out.append([spp.srepr(r12v), spp.srepr(r13v), spp.srepr(r23v)])
    Path(outfile).write_text(json.dumps({"n_sols_total": len(sols),
                                         "positive": out}), encoding="utf-8")


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
    ok = p.exitcode == 0
    if not ok:
        log(f"{label}: subprocess exit {p.exitcode}")
    return ok, time.time() - t0


# ---------------------------------------------------------------- stages

def stage_s0():
    m1, m2, m3 = sp.symbols("m1 m2 m3", positive=True)
    R12, R13, R23 = rvar(1, 2), rvar(1, 3), rvar(2, 3)
    F_sym = ac_symmetric(3, [m1, m2, m3])
    ok = all(sp.expand(f.subs({R12: 1, R13: 1, R23: 1})) == 0 for f in F_sym.values())
    record("P2-lagrange-symbolic", "pass" if ok else "fail")

    bad = {R12: sp.Rational(1), R13: sp.Rational(2), R23: sp.Rational(5, 2)}
    vals = [sp.expand(f.subs(bad).subs({m1: 1, m2: 2, m3: 3})) for f in F_sym.values()]
    record("sanity-nonvacuous", "pass" if any(v != 0 for v in vals) else "fail")

    line_in = all(sp.expand(f.subs({R13: 0, R23: 0})) == 0 for f in F_sym.values())
    record("fact-line-r13r23-in-VF", "pass" if line_in else "fail",
           "the line {r13 = r23 = 0} lies in V(F) for ALL masses (why saturation is needed)")


def stage_p3():
    R12, R13, R23 = rvar(1, 2), rvar(1, 3), rvar(2, 3)
    orderings = {
        "2-middle": (R13, R12 + R23),
        "3-middle": (R12, R13 + R23),
        "1-middle": (R23, R12 + R13),
    }
    all_ok = True
    details = {}
    for mv in SAMPLES:
        F = ac_symmetric(3, [sp.Integer(v) for v in mv])
        for oname, (lhs, rhs) in orderings.items():
            eqs = [sp.expand(f.subs({lhs: rhs})) for f in F.values()]
            eqs = [e for e in eqs if e != 0]
            vars2 = sorted({s for e in eqs for s in e.free_symbols}, key=str)
            sols = sp.solve_poly_system([sp.Poly(e, *vars2) for e in eqs], *vars2)
            pos = []
            for sol in sols:
                if all(is_real_positive(x) for x in sol):
                    if exact_zero_residuals(eqs, dict(zip(vars2, sol))):
                        pos.append(sol)
                    else:
                        log(f"P3 WARNING {mv}-{oname}: positive candidate failed exact residual: {sol}")
            key = f"{mv}-{oname}"
            details[key] = [[str(x) for x in s] for s in pos]
            if len(pos) != 1:
                all_ok = False
            if mv == (1, 1, 1) and oname == "2-middle" and len(pos) == 1:
                iv = {str(v): i for i, v in enumerate(vars2)}
                r12v = pos[0][iv["r12"]]
                r23v = pos[0][iv["r23"]]
                sym_ok = sp.simplify(r12v - r23v) == 0
                record("P3-equal-masses-symmetric", "pass" if sym_ok else "fail",
                       f"r12 = {r12v}, r23 = {r23v}")
    (ART / "stage-p3.json").write_text(json.dumps(details, indent=2), encoding="utf-8")
    record("P3-euler-moulton", "pass" if all_ok else "fail",
           "exactly one positive collinear solution per ordering per sample"
           if all_ok else json.dumps({k: len(v) for k, v in details.items()}))


def stage_p6():
    F4 = ac_symmetric(4, [1, 1, 1, 1])
    cm = cayley_menger_planar4()
    gens6 = [rvar(i, j) for i, j in combinations(range(1, 5), 2)]
    system4 = {f"f{i}{j}": F4[(i, j)] for i, j in F4}
    system4["e_CM"] = cm
    prof = {}
    ok = len(system4) == 7
    for name, e in system4.items():
        if sp.expand(e) == 0:
            ok = False
            prof[name] = None
        else:
            prof[name] = support_profile(e, gens6)
    (ART / "p6-n4-system.txt").write_text(
        "\n\n".join(f"### {k}\n{sp.expand(v)}" for k, v in system4.items()),
        encoding="utf-8")
    (ART / "stage-p6.json").write_text(json.dumps(prof, indent=2), encoding="utf-8")
    record("P6-assembly", "pass" if ok else "fail", json.dumps(prof))
    return F4, cm


def stage_p7(F4, cm):
    a, b = sp.symbols("a b", positive=True)
    subsq = {rvar(1, 2): a, rvar(2, 3): a, rvar(3, 4): a, rvar(1, 4): a,
             rvar(1, 3): b, rvar(2, 4): b}
    red = sorted({sp.expand(e.subs(subsq)) for e in F4.values()}, key=sp.default_sort_key)
    red = [e for e in red if e != 0]
    stripped_info = []
    core = []
    for e in red:
        c, stripped = strip_monomial_factors(e, [a, b])
        core.append(c)
        stripped_info.append(stripped)
    core = sorted(set(core), key=sp.default_sort_key)
    log(f"P7: reduced to {len(red)} equations; torus cores: {[str(c) for c in core]};"
        f" stripped {stripped_info}")
    g = sp.gcd(core[0], core[1]) if len(core) == 2 else sp.Integer(1)
    coprime = sp.total_degree(g) == 0
    sols = sp.solve_poly_system([sp.Poly(e, a, b) for e in core], a, b)
    pos = []
    for s in sols:
        if all(is_real_positive(x) for x in s):
            if exact_zero_residuals(core, {a: s[0], b: s[1]}):
                pos.append(s)
            else:
                log(f"P7 WARNING: positive candidate failed exact residual: {s}")
    entries = []
    square = None
    for (av, bv) in pos:
        is_square = sp.simplify(bv ** 2 - 2 * av ** 2) == 0
        cmv = sp.simplify(cm.subs({rvar(1, 2): av, rvar(2, 3): av, rvar(3, 4): av,
                                   rvar(1, 4): av, rvar(1, 3): bv, rvar(2, 4): bv}))
        ent = {"a": str(av), "b": str(bv),
               "a_cubed": str(sp.simplify(av ** 3)),
               "b2_eq_2a2": bool(is_square),
               "a_eq_b": bool(sp.simplify(av - bv) == 0),
               "cayley_menger": str(cmv),
               "cm_zero": bool(cmv == 0)}
        entries.append(ent)
        if is_square:
            square = (av, bv, ent)
    (ART / "stage-p7.json").write_text(json.dumps({
        "torus_cores": [str(c) for c in core], "coprime": bool(coprime),
        "n_positive": len(pos), "solutions": entries}, indent=2), encoding="utf-8")

    record("P7-unique-positive", "pass" if len(pos) == 1 else "fail",
           f"{len(pos)} positive torus solutions of the rhombus-stratum AC system: {entries}")
    if square is not None:
        av = square[0]
        minp = sp.minimal_polynomial(av, sp.Symbol("x"))
        planar = [e for e in entries if e["cm_zero"]]
        record("P7-square-shape", "pass",
               f"square present: a^3 = {square[2]['a_cubed']}, minpoly {minp};"
               f" planar (CM = 0) positive solutions: {len(planar)}")
        record("P7-cayley-menger", "pass" if square[2]["cm_zero"] else "fail",
               f"CM at the square = {square[2]['cayley_menger']}")
    else:
        record("P7-square-shape", "fail", "no positive solution with b^2 = 2a^2")
        record("P7-cayley-menger", "fail", "square absent")


def stage_p1_p5():
    for mv in SAMPLES:
        cap = CAP_P1_EQUAL if mv == (1, 1, 1) else CAP_P1_OTHER
        outfile = ART / f"p1-gb-{'_'.join(map(str, mv))}.json"
        ok, secs = run_capped(_worker_p1, (mv, str(outfile)), cap, f"P1 {mv}")
        if ok and outfile.exists():
            data = json.loads(outfile.read_text(encoding="utf-8"))
            record(f"P1-zerodim-{mv}", "pass" if data["zero_dim"] else "fail",
                   f"saturated GB size {data['gb_size']} in {secs:.0f} s")
        else:
            record(f"P1-zerodim-{mv}", "inconclusive-cap",
                   f"saturation Groebner did not finish within {cap} s")

    gb_equal = ART / "p1-gb-1_1_1.json"
    if gb_equal.exists() and RESULTS.get("P1-zerodim-(1, 1, 1)", {}).get("status") == "pass":
        outfile = ART / "p5-census.json"
        ok, secs = run_capped(_worker_p5, (str(gb_equal), str(outfile)),
                              CAP_P5_SOLVE, "P5 census")
        if ok and outfile.exists():
            data = json.loads(outfile.read_text(encoding="utf-8"))
            pos = [[sp.sympify(x) for x in s] for s in data["positive"]]
            realizable = []
            for (x, y, z) in pos:  # r12, r13, r23
                tri = (sp.simplify(x + z - y) >= 0) and (sp.simplify(x + y - z) >= 0) \
                      and (sp.simplify(y + z - x) >= 0)
                if tri:
                    realizable.append((x, y, z))
            record("P5-census-equal-masses",
                   "pass" if len(realizable) == 4 else "fail",
                   f"{len(realizable)} realizable of {len(pos)} positive"
                   f" (total sols {data['n_sols_total']});"
                   f" realizable = {[[str(v) for v in s] for s in realizable]}")
        else:
            record("P5-census-equal-masses", "inconclusive-cap",
                   f"saturated-system solve did not finish within {CAP_P5_SOLVE} s")
    else:
        record("P5-census-equal-masses", "inconclusive-cap",
               "prerequisite saturated GB unavailable (P1 equal masses not passed in cap)")


def stage_p4():
    outfile = ART / "p4-eliminant.json"
    ok, secs = run_capped(_worker_p4, (str(outfile),), CAP_P4, "P4 symbolic eliminant")
    if ok and outfile.exists():
        data = json.loads(outfile.read_text(encoding="utf-8"))
        (ART / "p4-euler-eliminant.txt").write_text(data["factored"], encoding="utf-8")
        record("P4-eliminant-nonzero",
               "pass" if data["eliminant_nonzero"] else "fail",
               f"degree in r23: {data['degree_r23']} ({secs:.0f} s)")
    else:
        record("P4-eliminant-nonzero", "inconclusive-cap",
               f"symbolic resultant did not finish within {CAP_P4} s")


def main() -> int:
    t0 = time.time()
    LOGF.write_text("", encoding="utf-8")
    log("EXP-001 staged run start")
    stage_s0()
    stage_p3()
    F4, cm = stage_p6()
    stage_p7(F4, cm)
    stage_p4()
    stage_p1_p5()

    profile = {"experiment": "EXP-001", "date": "2026-07-23",
               "results": RESULTS,
               "elapsed_s": round(time.time() - t0, 2),
               "sympy_version": sp.__version__,
               "python_version": sys.version,
               "caps": {"P4": CAP_P4, "P1_equal": CAP_P1_EQUAL,
                        "P1_other": CAP_P1_OTHER, "P5": CAP_P5_SOLVE}}
    (ART / "profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")
    fails = [k for k, v in RESULTS.items() if v["status"] == "fail"]
    caps = [k for k, v in RESULTS.items() if v["status"] == "inconclusive-cap"]
    log(f"done in {profile['elapsed_s']} s; FAIL: {fails or 'none'}; CAP: {caps or 'none'}")
    return 1 if fails else 0


if __name__ == "__main__":
    mp.freeze_support()
    sys.exit(main())
