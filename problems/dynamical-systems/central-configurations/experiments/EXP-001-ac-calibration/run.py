"""EXP-001: exact Albouy-Chenciner system builder, calibrated on n = 3, assembled for n = 4.

Deterministic, CPU-only, exact arithmetic (sympy over QQ; algebraic numbers where needed).
No randomness. Exits nonzero on any prediction failure (P1, P2, P3, P5, P6, P7 asserts;
P4 descriptive). Run from the repo root with the repo .venv:

    .venv/Scripts/python.exe problems/dynamical-systems/central-configurations/experiments/EXP-001-ac-calibration/run.py

Equations per the method dossier (HJ11 eq. (3), PDF read 2026-07-23):
    S_ij = r_ij^{-3} - 1   (Lambda = -1 scale normalization; S_ii = 0 by convention)
    f_ij = sum_{k=1..n} m_k [ S_ik (r_jk^2 - r_ik^2 - r_ij^2) + S_jk (r_ik^2 - r_jk^2 - r_ij^2) ]
cleared of denominators to polynomials in QQ[m][r].
"""

import json
import sys
import time
from itertools import combinations
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)

LOG_LINES = []


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG_LINES.append(line)


FAILURES = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    log(f"CHECK {name}: {status} {detail}")
    if not ok:
        FAILURES.append(name)


# ---------------------------------------------------------------- builders

def rvar(i: int, j: int):
    i, j = min(i, j), max(i, j)
    return sp.Symbol(f"r{i}{j}", positive=True)


def ac_symmetric(n: int, masses):
    """Cleared symmetric Albouy-Chenciner polynomials f_ij, i < j (list of sympy Polys' exprs)."""
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


def cayley_menger_planar4(subs=None):
    """Bordered 5x5 Cayley-Menger determinant for 4 points; zero iff coplanar (in R^2)."""
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
    d = M.det(method="berkowitz")
    return sp.expand(d if subs is None else d.subs(subs))


def support_profile(expr, gens):
    p = sp.Poly(expr, *gens)
    monoms = p.monoms()
    vecs = [sp.Matrix(m) for m in monoms]
    if len(vecs) <= 1:
        adim = 0
    else:
        M = sp.Matrix.hstack(*[v - vecs[0] for v in vecs[1:]])
        adim = M.rank()
    return {
        "n_monomials": len(monoms),
        "total_degree": int(sp.Poly(expr, *gens).total_degree()),
        "support_affine_dim": int(adim),
    }


def is_zero_dimensional(polys, gens):
    """0-dim criterion: grevlex GB has, for each gen, a leading monomial that is a pure power."""
    G = sp.groebner(polys, *gens, order="grevlex")
    lead = [sp.Poly(g, *gens).LM(order="grevlex") for g in G.exprs]
    pure = set()
    for lm in lead:
        exps = lm.exponents if hasattr(lm, "exponents") else None
        mon = sp.Poly(lm.as_expr() if hasattr(lm, "as_expr") else lm, *gens).monoms()[0]
        nz = [t for t in range(len(gens)) if mon[t] > 0]
        if len(nz) == 1:
            pure.add(nz[0])
    return all(t in pure for t in range(len(gens))), [str(m) for m in lead]


def positive_real_roots_univ(poly, var):
    """Exact count + isolating data of positive real roots of a univariate polynomial."""
    p = sp.Poly(sp.factor(poly), var)
    roots = []
    for r_, mult in p.real_roots(multiple=False):
        if r_.is_positive:
            roots.append((r_, mult))
    return roots


# ---------------------------------------------------------------- stages

def main() -> int:
    t0 = time.time()
    profile = {"experiment": "EXP-001", "date": "2026-07-23"}
    m1, m2, m3 = sp.symbols("m1 m2 m3", positive=True)
    R12, R13, R23 = rvar(1, 2), rvar(1, 3), rvar(2, 3)
    gens3 = [R12, R13, R23]

    # ---- P2: Lagrange point, symbolic masses -------------------------------
    log("P2: equilateral r = 1 with symbolic masses")
    F_sym = ac_symmetric(3, [m1, m2, m3])
    ok = all(sp.expand(f.subs({R12: 1, R13: 1, R23: 1})) == 0 for f in F_sym.values())
    check("P2-lagrange-symbolic", ok)

    # sanity: non-CC rational point must NOT satisfy the system (non-vacuity)
    bad = {R12: sp.Rational(1), R13: sp.Rational(2), R23: sp.Rational(5, 2)}
    vals = [sp.expand(f.subs(bad).subs({m1: 1, m2: 2, m3: 3})) for f in F_sym.values()]
    check("sanity-nonvacuous", any(v != 0 for v in vals), f"values {vals}")

    samples = [(1, 1, 1), (1, 2, 3), (2, 3, 5), (1, 1, 2)]

    # ---- P1: zero-dimensionality per sample mass vector --------------------
    for mv in samples:
        F = ac_symmetric(3, [sp.Integer(v) for v in mv])
        t = sp.Symbol("t", positive=True)
        polys = list(F.values()) + [t * R12 * R13 * R23 - 1]
        zd, lead = is_zero_dimensional(polys, gens3 + [t])
        check(f"P1-zerodim-{mv}", zd, f"leading monomials {lead}")

    # ---- P3: Euler-Moulton, one positive collinear solution per ordering ---
    # orderings: (middle body b): 1-2-3 means r13 = r12 + r23, etc.
    orderings = {
        "2-middle": (R13, R12 + R23),
        "3-middle": (R12, R13 + R23),
        "1-middle": (R23, R12 + R13),
    }
    p3_data = {}
    for mv in samples:
        F = ac_symmetric(3, [sp.Integer(v) for v in mv])
        for oname, (lhs, rhs) in orderings.items():
            sub = {lhs: rhs}
            eqs = [sp.expand(f.subs(sub)) for f in F.values()]
            eqs = [e for e in eqs if e != 0]
            vars2 = sorted({s for e in eqs for s in e.free_symbols}, key=str)
            sols = sp.solve_poly_system([sp.Poly(e, *vars2) for e in eqs], *vars2)
            pos = []
            for sol in sols:
                if all(s.is_real is not False and sp.im(s) == 0 for s in sol):
                    solr = [sp.nsimplify(s) if s.is_Rational else s for s in sol]
                    if all(sp.simplify(s) > 0 for s in sol):
                        pos.append(tuple(sp.simplify(s) for s in sol))
            p3_data[f"{mv}-{oname}"] = [tuple(str(x) for x in s) for s in pos]
            check(f"P3-euler-{mv}-{oname}", len(pos) == 1,
                  f"positive solutions {p3_data[f'{mv}-{oname}']}")
            if mv == (1, 1, 1) and oname == "2-middle" and len(pos) == 1:
                r12v, r23v = (pos[0][vars2.index(R12)], pos[0][vars2.index(R23)])
                check("P3-equal-masses-symmetric", sp.simplify(r12v - r23v) == 0,
                      f"r12 = {r12v}, r23 = {r23v}")

    # ---- P4: the Euler eliminant, symbolic masses (descriptive) ------------
    log("P4: symbolic-mass eliminant on the 2-middle chart")
    Fsym = ac_symmetric(3, [m1, m2, m3])
    eqs = [sp.expand(f.subs({R13: R12 + R23})) for f in Fsym.values()]
    eqs = [e for e in eqs if e != 0]
    res = sp.resultant(sp.Poly(eqs[0], R12), sp.Poly(eqs[1], R12), R12)
    res = sp.factor(res)
    elim_deg = sp.Poly(res, R23).degree() if res != 0 else -1
    profile["P4_eliminant_degree_in_r23"] = int(elim_deg)
    (ART / "p4-euler-eliminant.txt").write_text(sp.srepr(res)[:200000] + "\n\nfactored:\n" + str(res), encoding="utf-8")
    check("P4-eliminant-nonzero", res != 0, f"degree in r23: {elim_deg}")

    # ---- P5: labeled census, equal masses ----------------------------------
    log("P5: full labeled census for equal masses (1,1,1)")
    F = ac_symmetric(3, [1, 1, 1])
    sols = sp.solve_poly_system([sp.Poly(f, *gens3) for f in F.values()], *gens3)
    real_pos, realizable = [], []
    for sol in sols:
        if all(sp.im(s) == 0 for s in sol):
            if all(sp.simplify(s) > 0 for s in sol):
                real_pos.append(sol)
                a, b, c = sol  # r12, r13, r23
                tri = (sp.simplify(a + c - b) >= 0) and (sp.simplify(a + b - c) >= 0) and (sp.simplify(b + c - a) >= 0)
                if tri:
                    realizable.append(sol)
    profile["P5_real_positive"] = [tuple(str(x) for x in s) for s in real_pos]
    profile["P5_realizable"] = [tuple(str(x) for x in s) for s in realizable]
    check("P5-census-equal-masses", len(realizable) == 4,
          f"realizable {len(realizable)} of {len(real_pos)} real-positive; {profile['P5_realizable']}")

    # ---- P6: n = 4 assembly, equal masses ----------------------------------
    log("P6: assemble the planar 4-body HM system (equal masses)")
    F4 = ac_symmetric(4, [1, 1, 1, 1])
    cm = cayley_menger_planar4()
    gens6 = [rvar(i, j) for i, j in combinations(range(1, 5), 2)]
    system4 = {f"f{i}{j}": F4[(i, j)] for i, j in F4}
    system4["e_CM"] = cm
    prof6 = {}
    ok_nonzero = True
    for name, e in system4.items():
        if sp.expand(e) == 0:
            ok_nonzero = False
            prof6[name] = None
        else:
            prof6[name] = support_profile(e, gens6)
    profile["P6_structure"] = prof6
    (ART / "p6-n4-system.txt").write_text(
        "\n\n".join(f"### {k}\n{sp.expand(v)}" for k, v in system4.items()), encoding="utf-8")
    check("P6-assembly", ok_nonzero and len(system4) == 7,
          f"7 polynomials, profiles {json.dumps(prof6)}")

    # ---- P7: the square, exactly -------------------------------------------
    log("P7: equal-mass rhombus ansatz (a sides, b diagonals)")
    a, b = sp.symbols("a b", positive=True)
    subsq = {rvar(1, 2): a, rvar(2, 3): a, rvar(3, 4): a, rvar(1, 4): a,
             rvar(1, 3): b, rvar(2, 4): b}
    red = sorted({sp.expand(e.subs(subsq)) for e in F4.values()})
    red = [e for e in red if e != 0]
    log(f"P7: reduced to {len(red)} distinct nonzero equations")
    sols = sp.solve_poly_system([sp.Poly(e, a, b) for e in red], a, b)
    pos = [s for s in sols if all(sp.im(x) == 0 for x in s) and all(sp.simplify(x) > 0 for x in s)]
    profile["P7_positive_solutions"] = [tuple(str(x) for x in s) for s in pos]
    ok_unique = len(pos) == 1
    ok_square = False
    ok_cm = False
    a_min_poly = None
    if ok_unique:
        av, bv = pos[0]
        ok_square = sp.simplify(bv ** 2 - 2 * av ** 2) == 0
        cmval = cayley_menger_planar4(subs=None).subs(
            {rvar(1, 2): av, rvar(2, 3): av, rvar(3, 4): av, rvar(1, 4): av,
             rvar(1, 3): bv, rvar(2, 4): bv})
        ok_cm = sp.simplify(cmval) == 0
        a_min_poly = str(sp.minimal_polynomial(av, sp.Symbol("x")))
        profile["P7_a_minimal_polynomial"] = a_min_poly
        profile["P7_a_cubed"] = str(sp.simplify(av ** 3))
    check("P7-unique-positive", ok_unique, f"positive {profile['P7_positive_solutions']}")
    check("P7-square-shape", ok_square, f"a minpoly {a_min_poly}")
    check("P7-cayley-menger", ok_cm)
    log(f"P7: expected-by-hand a^3 = (4+sqrt2)/2 vs machine a^3 = {profile.get('P7_a_cubed')}"
        " (expectation informational, not an assert)")

    # ---- wrap-up -------------------------------------------------------------
    profile["failures"] = FAILURES
    profile["elapsed_s"] = round(time.time() - t0, 2)
    profile["sympy_version"] = sp.__version__
    profile["python_version"] = sys.version
    (ART / "profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")
    (ART / "run-log.txt").write_text("\n".join(LOG_LINES), encoding="utf-8")
    log(f"done in {profile['elapsed_s']} s; failures: {FAILURES or 'none'}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
