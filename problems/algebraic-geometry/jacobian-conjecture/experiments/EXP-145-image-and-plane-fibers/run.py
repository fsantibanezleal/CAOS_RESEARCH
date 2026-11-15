# EXP-145: the image of the announced map and its fibers over the plane C = 0. CPU only; exact
# rational arithmetic (sympy over QQ); fixed seed 20261114. See hypothesis.md (frozen).
# Run from the repo root:
#   .venv/Scripts/python.exe problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-145-image-and-plane-fibers/run.py
#
# P1  Groebner basis of the fiber over Gamma(c), c inverted, is [1] (lex).      Control C1: 5/27 instead of 4/27.
# P2  (a) F(0, y, z) = (z + 4 y^2, y, 0); (b) 40 targets with C != 0 off Gamma: fiber ideal proper, quotient
#     dimension 1..3 (staircase of a grevlex Groebner basis), a real preimage exists (Sturm count of W + reconstruction).
# P3  the plane C = 0: symbolic parametrization; 20 targets B^2 != 16A with dimension 3 and three distinct points,
#     5 targets B^2 = 16A with dimension 1; the fibers over (0, 1, 0) and (-1/4, 0, 0).
# C2  the C = 0 targets of EXP-007 item 4, read from its artifact: three complex points, exactly one rational.
# Writes artifacts/results.json and artifacts/run-log.txt; exits 0 on PASS, 1 on a failed prediction, 3 on a missing input.
import itertools
import json
import math
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
JC = HERE.parents[1]
sys.path.insert(0, str(JC / "code"))

import sympy as sp  # noqa: E402
from jclib import constructor_v2, v as jv, w as jw  # noqa: E402

SEED = 20261114
KILL_SECONDS = 600
x, y, z, c, v = sp.symbols("x y z c v")
A, B, C = sp.symbols("A B C")
w = jw
u = 1 + x * y
F1 = u**3 * z + y**2 * u * (4 + 3 * x * y)
F2 = y + 3 * x * u**2 * z + 3 * x * y**2 * (4 + 3 * x * y)
F3 = 2 * x - 3 * x**2 * y - x**3 * z
F = (sp.expand(F1), sp.expand(F2), sp.expand(F3))

RESULTS = {"seed": SEED, "predictions": {}}
failures = []
undecided = []
LOG = []


def log(msg=""):
    print(msg)
    LOG.append(msg)


def check(name, ok, detail=""):
    log(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)
    return ok


def apply_F(p):
    """Exact image of a point under the announced map."""
    sub = {x: p[0], y: p[1], z: p[2]}
    return tuple(sp.simplify(sp.expand(f.subs(sub))) for f in F)


def gamma_basis(numer=4):
    """Reduced lex Groebner basis of (27c^2 F1 - numer, 3c F2 - 4, F3 - c, c v - 1) in Q[x,y,z,c,v]."""
    gb = sp.groebner([27 * c**2 * F[0] - numer, 3 * c * F[1] - 4, F[2] - c, c * v - 1],
                     x, y, z, c, v, order="lex")
    return list(gb.exprs)


def fiber_gb(target, order="grevlex"):
    return sp.groebner([sp.expand(f - t) for f, t in zip(F, target)], x, y, z, order=order)


def quotient_dim(gb):
    """Dimension of Q[x,y,z]/I from the staircase of the leading monomials; None if not zero-dimensional."""
    if list(gb.exprs) == [1]:
        return 0
    lms = [sp.Poly(g, x, y, z).monoms(order=gb.order)[0] for g in gb.exprs]
    bounds = []
    for i in range(3):
        pure = [m[i] for m in lms if all(m[j] == 0 for j in range(3) if j != i)]
        if not pure:
            return None
        bounds.append(min(pure))
    count = 0
    for e in itertools.product(*[range(b) for b in bounds]):
        if not any(all(e[j] >= m[j] for j in range(3)) for m in lms):
            count += 1
    return count


def plane_fiber_points(A0, B0):
    """Exact points of the fiber over (A0, B0, 0), solved from its lex Groebner basis."""
    gb = fiber_gb((A0, B0, sp.Integer(0)), order="lex")
    sols = sp.solve(list(gb.exprs), [x, y, z], dict=True)
    return sorted({tuple(s[var] for var in (x, y, z)) for s in sols}, key=str)


def plane_points_formula(A0, B0):
    """The paper's points over (A0, B0, 0): flat sheet plus the two points with x^2 (B^2 - 16A) = 4."""
    d = B0**2 - 16 * A0
    pts = [(sp.Integer(0), B0, A0 - 4 * B0**2)]
    if d != 0:
        r = sp.sqrt(d)
        for sg in (1, -1):
            xv = sg * 2 / r
            pts.append((xv, (B0 * xv - 6) / (4 * xv), (26 - 3 * B0 * xv) / (4 * xv**2)))
    return pts


def maps_to(p, target):
    img = apply_F(p)
    return all(sp.simplify(a - b) == 0 for a, b in zip(img, target))


def is_rational_square(q):
    q = sp.Rational(q)
    if q < 0:
        return False
    return math.isqrt(q.p) ** 2 == q.p and math.isqrt(q.q) ** 2 == q.q


def rnd_rat(rng, num=9, den=6, nonzero=False):
    while True:
        r = sp.Rational(rng.randint(-num, num), rng.randint(1, den))
        if not (nonzero and r == 0):
            return r


# ---------------------------------------------------------------------------------------------
# Fiber polynomial W and the reconstruction of a preimage from a simple root (EXP-007, Part 1)
# ---------------------------------------------------------------------------------------------
_p_seed = 2 * w - 3 * w**2
_, _, _, _prm = constructor_v2(_p_seed, 2)
PHI, MM, QV = _prm["Phi"], _prm["m"], _prm["q"]
W_GEN = sp.expand(4 * PHI - (w * B * C - A * C**2))
SIGMA = 27 * A**2 * C**2 - 18 * A * B * C + 16 * A + B**3 * C - B**2
S_GEN = (B * C - 4 * _p_seed) / MM            # s = -W'(w)/m
V_GEN = 2 * w / S_GEN - 1
T_GEN = QV.subs(jv, V_GEN) - S_GEN
X_GEN = C / S_GEN
Y_GEN = V_GEN / X_GEN
Z_GEN = T_GEN / X_GEN**2


def reconstruct(wval, A0, B0, C0):
    """Preimage from a simple root wval of W at the target (A0, B0, C0), C0 != 0."""
    sub = {A: A0, B: B0, C: C0, w: wval}
    return tuple(e.subs(sub) for e in (X_GEN, Y_GEN, Z_GEN))


def w_route(A0, B0, C0):
    """Exact data of W at a target: simple and multiple root counts and the exact count of real simple roots."""
    Wt = sp.Poly(W_GEN.subs({A: A0, B: B0, C: C0}), w)
    sqf = sp.sqf_list(Wt)[1]
    simple = [f for f, m in sqf if m == 1]
    return {"n_simple": sum(f.degree() for f in simple),
            "n_multiple_roots_with_mult": sum(f.degree() * m for f, m in sqf if m > 1),
            "n_real_simple": sum(f.count_roots() for f in simple), "simple_factors": simple}


def numeric_residual(A0, B0, C0, simple_factors, digits=80):
    """Reconstruct at the first real simple root; return the largest relative residual of F - target."""
    for f in simple_factors:
        rr = sp.real_roots(f)
        if rr:
            p = reconstruct(rr[0], A0, B0, C0)
            pv = [sp.N(q, digits) for q in p]
            img = [sp.N(f_.subs({x: pv[0], y: pv[1], z: pv[2]}), digits) for f_ in F]
            worst = max(abs(i - t) / max(1, abs(t)) for i, t in zip(img, (A0, B0, C0)))
            return float(worst), [str(sp.N(q, 20)) for q in p]
    return None, None


def main():
    t_start = time.time()
    log("=" * 76)
    log("Premise: det JF = -2 (EXP-001), the discriminant of W, the triple-root locus, the reconstruction")
    log("=" * 76)
    detJ = sp.expand(sp.Matrix(F).jacobian([x, y, z]).det())
    check("det JF == -2", detJ == -2, f"det = {detJ}")
    Dgen = sp.expand(sp.discriminant(sp.Poly(W_GEN, w), w))
    check("disc_w(W) == -16 C^2 Sigma", sp.expand(Dgen + 16 * C**2 * SIGMA) == 0)
    Wg = sp.expand(W_GEN.subs({A: sp.Rational(4, 27) / C**2, B: sp.Rational(4, 3) / C}))
    check("on Gamma(c): W == -4 (w - 1/3)^3 (a triple root, no simple root)",
          sp.expand(Wg + 4 * (w - sp.Rational(1, 3))**3) == 0)
    dom = sp.QQ.frac_field(A, B, C)
    ident_ok = True
    for f_, T in zip(F, (A, B, C)):
        e = sp.together(f_.subs({x: X_GEN, y: Y_GEN, z: Z_GEN}, simultaneous=True) - T)
        n, _d = sp.fraction(sp.cancel(e))
        r = sp.rem(sp.Poly(n, w, domain=dom), sp.Poly(W_GEN, w, domain=dom))
        ident_ok = ident_ok and r.is_zero
    check("reconstruction identity: F(x(w), y(w), z(w)) = (A, B, C) modulo W(w) in Q(A,B,C)[w]", ident_ok)
    RESULTS["premise"] = {"detJF": str(detJ), "disc_identity": True, "triple_root_on_gamma": True,
                          "reconstruction_identity": bool(ident_ok)}

    # ---- P1 -----------------------------------------------------------------------------------
    log()
    log("=" * 76)
    log("P1: the fiber over Gamma(c), c inverted, is empty (lex Groebner basis [1]); control C1")
    log("=" * 76)
    t0 = time.time()
    g1 = gamma_basis(4)
    t1 = time.time() - t0
    log(f"  basis (4/27): {g1}   [{t1:.2f} s]")
    p1_ok = check("P1: reduced lex Groebner basis over Gamma(c) with c inverted is [1]", g1 == [sp.Integer(1)])
    t0 = time.time()
    g1c = gamma_basis(5)
    t1c = time.time() - t0
    log(f"  control C1 (5/27): {len(g1c)} basis elements   [{t1c:.2f} s]")
    c1_ok = check("C1: with 5/27 the basis differs from [1] (the perturbed curve is in the image)",
                  g1c != [sp.Integer(1)])
    RESULTS["predictions"]["P1"] = {"basis_4_27": [str(g) for g in g1], "seconds": round(t1, 3), "pass": bool(p1_ok)}
    RESULTS["controls"] = {"C1": {"basis_5_27": [str(g) for g in g1c], "seconds": round(t1c, 3), "pass": bool(c1_ok)}}
    if t1 > KILL_SECONDS:
        undecided.append("P1")

    # ---- P2(a) --------------------------------------------------------------------------------
    log()
    log("=" * 76)
    log("P2(a): over C = 0 every target has the flat-sheet preimage (symbolic)")
    log("=" * 76)
    f0 = [sp.expand(f_.subs(x, 0)) for f_ in F]
    a1 = check("P2(a): F(0, y, z) == (z + 4 y^2, y, 0)", f0 == [z + 4 * y**2, y, 0], str(f0))
    a2 = check("P2(a): (0, B, A - 4 B^2) maps to (A, B, 0)",
               [sp.expand(f_.subs({x: 0, y: B, z: A - 4 * B**2})) for f_ in F] == [A, B, 0])
    RESULTS["predictions"]["P2a"] = {"F_on_x0": [str(e) for e in f0], "pass": bool(a1 and a2)}

    # ---- P2(b) --------------------------------------------------------------------------------
    log()
    log("=" * 76)
    log("P2(b): 40 targets with C != 0 off Gamma: proper fiber ideal, dimension 1..3, a real preimage")
    log("=" * 76)
    rng = random.Random(SEED)
    targets = []
    for _ in range(20):
        targets.append(("random", (rnd_rat(rng, 9, 6), rnd_rat(rng, 9, 6), rnd_rat(rng, 9, 6, nonzero=True)), None, None))
    # on Sigma = 0: W = -4 (w - w0)^2 (w - (1 - 2 w0)) with the double root w0 != 1/3 prescribed
    for w0 in [sp.Rational(r) for r in ("1/2", "-1/2", "2", "-1", "1/5", "3/2", "-2", "2/3", "3", "-1/3")]:
        w1 = 1 - 2 * w0
        C0 = rnd_rat(rng, 6, 4, nonzero=True)
        targets.append(("on-Sigma", (4 * w0**2 * w1 / C0**2, 4 * (w0**2 + 2 * w0 * w1) / C0, C0), None, None))
    # near Gamma: Gamma(c0) plus a rational perturbation of at most 1e-3 per coordinate
    for c0 in [sp.Rational(r) for r in ("1", "2", "1/2", "-1", "3", "-2", "1/3", "5/2", "-1/2", "4")]:
        g = (sp.Rational(4, 27) / c0**2, sp.Rational(4, 3) / c0, c0)
        while True:
            d3 = [sp.Rational(rng.randint(-10, 10), 10**4) for _ in range(3)]
            if any(d3):
                break
        targets.append(("near-Gamma", (g[0] + d3[0], g[1] + d3[1], g[2] + d3[2]), g, d3))

    rows = []
    for kind, (A0, B0, C0), g, d3 in targets:
        gam_dist = max(abs(q) for q in d3) if d3 else None
        on_gamma = (C0 != 0 and A0 == sp.Rational(4, 27) / C0**2 and B0 == sp.Rational(4, 3) / C0)
        sig = SIGMA.subs({A: A0, B: B0, C: C0})
        t0 = time.time()
        gb = fiber_gb((A0, B0, C0))
        el = time.time() - t0
        dim = quotient_dim(gb)
        wr = w_route(A0, B0, C0)
        resid, pt = numeric_residual(A0, B0, C0, wr["simple_factors"])
        ok = (C0 != 0 and not on_gamma and list(gb.exprs) != [1] and dim is not None and 1 <= dim <= 3
              and wr["n_real_simple"] >= 1 and resid is not None and resid < 1e-40
              and dim == wr["n_simple"]
              and ((kind == "on-Sigma") == (sig == 0))
              and (gam_dist is None or gam_dist <= sp.Rational(1, 1000)))
        if el > KILL_SECONDS:
            undecided.append(f"P2(b) {(A0, B0, C0)}")
        row = {"kind": kind, "target": [str(A0), str(B0), str(C0)], "Sigma": str(sig), "off_Gamma": not on_gamma,
               "grevlex_basis": [str(g_) for g_ in gb.exprs], "quotient_dim": dim,
               "W_route_simple_roots": wr["n_simple"], "W_route_multiple_roots_with_mult": wr["n_multiple_roots_with_mult"],
               "real_simple_roots": wr["n_real_simple"], "reconstructed_real_point_20_digits": pt,
               "reconstruction_residual_80_digits": resid, "seconds": round(el, 3), "pass": bool(ok)}
        if g is not None:
            row["nearest_Gamma_point"] = [str(q) for q in g]
            row["max_coordinate_distance"] = str(gam_dist)
        rows.append(row)
        log(f"  {kind:10s} ({A0}, {B0}, {C0}): dim {dim}, W simple roots {wr['n_simple']}, "
            f"real simple {wr['n_real_simple']}, residual {resid}  [{el:.2f} s]  {'ok' if ok else 'BAD'}")
    n_ok = sum(1 for r in rows if r["pass"])
    check("P2(b): all 40 targets pass (proper ideal, dim 1..3 = simple roots of W, real preimage reconstructed)",
          len(rows) == 40 and n_ok == 40, f"{n_ok}/40")
    for k in ("random", "on-Sigma", "near-Gamma"):
        log(f"  quotient dimensions, {k}: {sorted({r['quotient_dim'] for r in rows if r['kind'] == k})}")
    RESULTS["predictions"]["P2b"] = {"n_targets": len(rows), "n_pass": n_ok, "targets": rows}

    # ---- P3 -----------------------------------------------------------------------------------
    log()
    log("=" * 76)
    log("P3: the plane C = 0")
    log("=" * 76)
    xs = sp.Symbol("xs", nonzero=True)
    Fxs = [sp.simplify(f_.subs({x: xs, y: (B * xs - 6) / (4 * xs), z: (26 - 3 * B * xs) / (4 * xs**2)},
                               simultaneous=True)) for f_ in F]
    check("P3(a): F(x, (Bx - 6)/(4x), (26 - 3Bx)/(4x^2)) == (B^2/16 - 1/(4x^2), B, 0)",
          sp.simplify(Fxs[0] - (B**2 / 16 - 1 / (4 * xs**2))) == 0 and sp.simplify(Fxs[1] - B) == 0
          and sp.simplify(Fxs[2]) == 0, str(Fxs))
    check("P3(a): that first component equals A exactly on x^2 (B^2 - 16A) = 4",
          sp.simplify((B**2 / 16 - 1 / (4 * xs**2) - A) * 16 * xs**2 - (xs**2 * (B**2 - 16 * A) - 4)) == 0)

    rng3 = random.Random(SEED + 1)
    gen = []
    while len(gen) < 20:
        A0, B0 = rnd_rat(rng3, 9, 6), rnd_rat(rng3, 9, 6)
        if B0**2 != 16 * A0:
            gen.append((A0, B0))
    gen[0] = (sp.Rational(0), sp.Rational(1))         # B^2 - 16A = 1, a rational square
    gen[1] = (sp.Rational(-1, 4), sp.Rational(0))     # B^2 - 16A = 4, a rational square
    degen = []
    for _ in range(5):
        B0 = rnd_rat(rng3, 9, 6)
        degen.append((B0**2 / 16, B0))
    plane = []
    P3b_ok = True
    for (A0, B0) in gen + degen:
        d = B0**2 - 16 * A0
        t0 = time.time()
        gbg = fiber_gb((A0, B0, sp.Integer(0)))
        dim = quotient_dim(gbg)
        el = time.time() - t0
        want = 3 if d != 0 else 1
        pts = plane_points_formula(A0, B0)
        pts_ok = all(maps_to(p, (A0, B0, 0)) for p in pts)
        # radicality, second route: the x-eliminant of the lex basis (z > y > x) is squarefree of degree dim
        gbl = sp.groebner([sp.expand(f_ - t) for f_, t in zip(F, (A0, B0, 0))], z, y, x, order="lex")
        elim = [g_ for g_ in gbl.exprs if g_.free_symbols <= {x}]
        elim_ok = bool(elim) and sp.degree(elim[-1], x) == want and sp.gcd(elim[-1], sp.diff(elim[-1], x)) == 1
        distinct = len({sp.simplify(p[0]) for p in pts}) == len(pts)
        ok = dim == want and pts_ok and distinct and len(pts) == want and elim_ok
        P3b_ok = P3b_ok and ok
        if el > KILL_SECONDS:
            undecided.append(f"P3(b) {(A0, B0)}")
        plane.append({"target": [str(A0), str(B0), "0"], "B2_minus_16A": str(d),
                      "grevlex_basis": [str(g_) for g_ in gbg.exprs], "quotient_dim": dim, "expected_dim": want,
                      "points": [[str(sp.simplify(q)) for q in p] for p in pts],
                      "points_map_to_target": bool(pts_ok), "distinct": bool(distinct),
                      "x_eliminant": str(elim[-1]) if elim else None,
                      "eliminant_squarefree_of_degree_dim": bool(elim_ok),
                      "seconds": round(el, 3), "pass": bool(ok)})
        log(f"  ({A0}, {B0}, 0): B^2 - 16A = {d}, dim {dim} (want {want}), points map to target {pts_ok}, "
            f"x-eliminant squarefree of degree {want}: {elim_ok}  {'ok' if ok else 'BAD'}")
    check("P3(b): 20 targets with B^2 != 16A have dimension 3 and three distinct points (radical); "
          "5 targets with B^2 = 16A have dimension 1", P3b_ok and len(plane) == 25)

    log()
    log("  P3(c): the named fibers")
    c_res = {}
    for (A0, B0), expect in (
        ((sp.Rational(0), sp.Rational(1)),
         {(0, 1, -4), (2, sp.Rational(-1, 2), sp.Rational(5, 4)), (-2, 1, 2)}),
        ((sp.Rational(-1, 4), sp.Rational(0)),
         {(0, 0, sp.Rational(-1, 4)), (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
          (-1, sp.Rational(3, 2), sp.Rational(13, 2))}),
    ):
        got = set(plane_fiber_points(A0, B0))
        expect = {tuple(sp.Rational(q) for q in e) for e in expect}
        dim = quotient_dim(fiber_gb((A0, B0, sp.Integer(0))))
        ok = got == expect and dim == 3 and all(maps_to(p, (A0, B0, 0)) for p in got)
        check(f"P3(c): fiber over ({A0}, {B0}, 0) is exactly {sorted(map(str, expect))} (Groebner-solved), dim {dim}", ok)
        c_res[f"({A0}, {B0}, 0)"] = {"points": sorted(str(p) for p in got), "quotient_dim": dim, "pass": bool(ok)}
    RESULTS["predictions"]["P3"] = {"targets": plane, "named_fibers": c_res, "parametrization": [str(e) for e in Fxs]}

    # ---- C2 -----------------------------------------------------------------------------------
    log()
    log("=" * 76)
    log("C2: the C = 0 targets of EXP-007 item 4, read from its artifact: three points, exactly one rational")
    log("=" * 76)
    art = JC / "experiments" / "EXP-007-asymptotic-variety" / "artifacts" / "output-2026-07-20.txt"
    if not art.exists():
        log(f"MISSING INPUT: {art}")
        sys.exit(3)
    text = art.read_text(encoding="utf-8")
    seen = {}
    for a_, b_, fiber_str in re.findall(r"fiber over \(([^,()]+), ([^,()]+), 0\): (\[\([^\]]*\)\])", text):
        seen.setdefault((a_, b_), fiber_str)
    check("C2: the EXP-007 artifact lists C = 0 targets", len(seen) >= 2, f"{len(seen)} targets read")
    c2 = []
    for (a_, b_), fiber_str in seen.items():
        A0, B0 = sp.Rational(a_), sp.Rational(b_)
        d = B0**2 - 16 * A0
        dim = quotient_dim(fiber_gb((A0, B0, sp.Integer(0))))
        pts = plane_points_formula(A0, B0)
        verified = all(maps_to(p, (A0, B0, 0)) for p in pts)
        rat = [p for p in pts if all(sp.simplify(q).is_rational for q in p)]
        flat = (sp.Integer(0), B0, A0 - 4 * B0**2)
        recorded_one = fiber_str.replace(" ", "") == str([flat]).replace(" ", "")
        ok = (dim == 3 and verified and len(pts) == 3 and len(rat) == 1 and rat[0] == flat
              and not is_rational_square(d) and recorded_one)
        c2.append({"target": [a_, b_, "0"], "recorded_fiber": fiber_str, "B2_minus_16A": str(d),
                   "rational_square": is_rational_square(d), "quotient_dim": dim, "n_points": len(pts),
                   "n_rational_points": len(rat), "points": [[str(sp.simplify(q)) for q in p] for p in pts],
                   "recorded_matches_the_rational_point": bool(recorded_one), "pass": bool(ok)})
        log(f"  ({a_}, {b_}, 0): recorded {fiber_str}; B^2 - 16A = {d} (rational square: {is_rational_square(d)}); "
            f"dim {dim}; rational points {len(rat)} of {len(pts)}  {'ok' if ok else 'BAD'}")
    c2_ok = check("C2: each EXP-007 C = 0 target has three complex points of which exactly one is rational, "
                  "and the recorded single point is that one", bool(c2) and all(r["pass"] for r in c2))
    RESULTS["controls"]["C2"] = {"source": str(art.relative_to(JC)), "targets": c2, "pass": bool(c2_ok)}

    # ---- summary ------------------------------------------------------------------------------
    RESULTS["undecided"] = undecided
    RESULTS["failures"] = failures
    RESULTS["total_seconds"] = round(time.time() - t_start, 2)
    RESULTS["verdict"] = "PASS" if not failures and not undecided else "FAIL"
    log()
    if undecided:
        log(f"UNDECIDED (over the {KILL_SECONDS} s kill criterion): {undecided}")
    if failures:
        log(f"RESULT: {len(failures)} check(s) FAILED: {failures}")
    else:
        log("RESULT: ALL CHECKS PASS.")
    log(f"total {RESULTS['total_seconds']} s")
    art_dir = HERE / "artifacts"
    art_dir.mkdir(exist_ok=True)
    (art_dir / "results.json").write_text(json.dumps(RESULTS, indent=1, default=lambda o: int(o) if isinstance(o, sp.Integer) else str(o)), encoding="utf-8")
    (art_dir / "run-log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    sys.exit(0 if RESULTS["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
