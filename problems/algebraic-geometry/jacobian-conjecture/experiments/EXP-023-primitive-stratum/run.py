# EXP-023: first contact with the primitive stratum: the (4,6) scan.
# CPU-only, sympy over QQ. See hypothesis.md. Parts: A (h = xy) | B (rank sweep).
# Run: .\.venv\Scripts\python.exe ...\EXP-023-primitive-stratum\run.py [A|B]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import Poly, Rational, S, expand, linsolve, symbols  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def mons(dmin, dmax):
    return [x**i * y**(d - i) for d in range(dmin, dmax + 1) for i in range(d + 1)]


MQ = mons(2, 6)
B = symbols(f"B0:{len(MQ)}")


def complete(Pexpr):
    """Complete linear solve for Q = y + (deg 2..6 tail) with J(P, Q) = 1.
    Returns (Qgeneric, frees) or None when inconsistent. linsolve only (EXP-013 gotcha:
    nonlinear solve() returns [] on solvable systems; this system is LINEAR in B)."""
    Q0 = y + sum(b * m for b, m in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(Pexpr, Q0) - 1), x, y).coeffs() if e != 0]
    ls = linsolve(eqs, list(B))
    if not ls:
        return None
    tup = list(ls)[0]
    Qg = expand(y + sum(t * m for t, m in zip(tup, MQ)))
    frees = sorted(Qg.free_symbols & set(B), key=lambda s: s.name)
    return Qg, frees


def analyze(Qg, frees, htop3):
    """(deg6_any, realizable): can any completion reach true degree 6; can the top be a
    nonzero multiple of h^3 (the primitive signature)? Top-dependence forces these to agree
    when P_top = a h^2 (every solution-space point IS a Keller completion): disagreement is
    a bug or a discovery, flagged by the caller."""
    pol = Poly(Qg, x, y)
    c6 = {m: c for m, c in zip(pol.monoms(), pol.coeffs()) if sum(m) == 6}
    deg6_any = any(expand(c) != 0 for c in c6.values())
    # primitive purification: zero every deg-6 coefficient NOT in h^3's support, then ask
    # whether the h^3-aligned part can still be nonzero.
    h3 = Poly(expand(htop3), x, y)
    sup = set(h3.monoms())
    others = [c for m, c in c6.items() if m not in sup]
    aligned = [c6.get(m, S.Zero) for m in sup]
    if all(expand(o) == 0 for o in others):
        realizable = any(expand(c) != 0 for c in aligned)
    elif not frees:
        realizable = False
    else:
        ls = linsolve([expand(o) for o in others], frees)
        if not ls:
            realizable = False
        else:
            sub = dict(zip(frees, list(ls)[0]))
            realizable = any(expand(c.subs(sub)) != 0 for c in aligned)
    return deg6_any, realizable


def scan(tag, samples, h):
    """samples: list of (name, Pexpr). Returns (n_incons, n_cons, hits, agree_ok)."""
    htop3 = h**3
    ni = nc = hits = 0
    agree = True
    for nm, Pexpr in samples:
        r = complete(Pexpr)
        if r is None:
            ni += 1
            print(f"  {tag} {nm}: INCONSISTENT (no Keller completion at deg <= 6)")
            continue
        nc += 1
        Qg, frees = r
        d6, real = analyze(Qg, frees, htop3)
        gdeg = Poly(Qg, x, y).total_degree()
        print(f"  {tag} {nm}: consistent, {len(frees)} free; generic deg {gdeg}; "
              f"deg6-any={d6} primitive={real}")
        if d6 != real:
            agree = False
            print(f"  {tag} {nm}: *** deg6/primitive DISAGREE (bug or discovery) ***")
        if real:
            hits += 1
            print(f"  {tag} {nm}: *** PRIMITIVE (4,6) REALIZATION: escalate ***")
    return ni, nc, hits, agree


def psamples(h, a_sym):
    """Structured P-coefficient samples: pure top (generic + numeric), single-coefficient
    patterns, dense rationals. All with a != 0."""
    p20, p11, p02, p30, p21, p12, p03 = symbols("p20 p11 p02 p30 p21 p12 p03")
    base = {p20: 0, p11: 0, p02: 0, p30: 0, p21: 0, p12: 0, p03: 0}
    P2 = p20 * x**2 + p11 * x * y + p02 * y**2
    P3 = p30 * x**3 + p21 * x**2 * y + p12 * x * y**2 + p03 * y**3
    Pfull = x + P2 + P3 + symbols("a_") * h**2
    a_ = symbols("a_")
    out = [("pure-generic-a", Pfull.subs(base).subs(a_, a_sym)),
           ("pure-a1", Pfull.subs(base).subs(a_, 1))]
    for s_ in (p20, p11, p02, p30, p21, p12, p03):
        inst = dict(base)
        inst[s_] = 1
        out.append((f"single-{s_}", Pfull.subs(inst).subs(a_, 1)))
    dense = [
        ("dense-1", {p20: 1, p11: -2, p02: Rational(1, 2), p30: 0, p21: 1, p12: -1,
                     p03: 3, a_: 1}),
        ("dense-2", {p20: -1, p11: 1, p02: 2, p30: Rational(1, 3), p21: -1, p12: 2,
                     p03: -1, a_: Rational(1, 2)}),
        ("dense-3", {p20: 2, p11: 3, p02: -1, p30: 1, p21: 2, p12: 1, p03: 1,
                     a_: -2}),
        ("dense-4", {p20: 0, p11: 1, p02: 0, p30: 0, p21: 0, p12: 1, p03: 0,
                     a_: 3}),
    ]
    out += [(nm, Pfull.subs(inst)) for nm, inst in dense]
    return out


def partA():
    print("=" * 76)
    print("Part A: the (4,6) primitive scan, h = xy (rank 2)")
    print("=" * 76)
    a_gen = symbols("a_")
    h = x * y
    ni, nc, hits, agree = scan("A", psamples(h, a_gen), h)
    print(f"  totals: {ni} inconsistent, {nc} consistent, {hits} primitive hits")
    check("A: no primitive (4,6) realization over the declared samples", hits == 0,
          f"{ni + nc} samples")
    check("A: deg6-any and primitive-realizable agree on every sample (dependence "
          "cross-check)", agree)


def partB():
    print("=" * 76)
    print("Part B: rank sweep h_gamma = x^2 + gamma y^2, gamma in {1, -1, 0}")
    print("=" * 76)
    a_gen = symbols("a_")
    allhits = 0
    agreeall = True
    for gam in (1, -1, 0):
        h = x**2 + gam * y**2
        sams = psamples(h, a_gen)
        keep = [s for s in sams if s[0] in
                ("pure-generic-a", "pure-a1", "single-p11", "single-p03", "dense-1",
                 "dense-2")]
        ni, nc, hits, agree = scan(f"B[g={gam}]", keep, h)
        print(f"  gamma={gam}: {ni} inconsistent, {nc} consistent, {hits} hits")
        allhits += hits
        agreeall &= agree
    check("B: no primitive (4,6) realization at any gamma (incl. rank-1 control)",
          allhits == 0)
    check("B: dependence cross-check agrees on every sample", agreeall)


def partC():
    print("=" * 76)
    print("Part C: positive controls (the all-inconsistent scan must not be vacuous)")
    print("=" * 76)
    # C1: quasi-triangular deg-4 P: completions EXIST (Q = ell + H(P), deg H <= 1 within
    # the deg <= 6 window: generic deg 4) and the deg-6 region is empty (H deg 2 needs 8).
    ell = x + y
    r = complete(x + ell**4)
    ok = r is not None
    if ok:
        Qg, frees = r
        d6, real = analyze(Qg, frees, (ell**4) ** 3)
        gdeg = Poly(Qg, x, y).total_degree()
        print(f"  C1 x+(x+y)^4: consistent, {len(frees)} free, generic deg {gdeg}, "
              f"deg6-any={d6}")
        ok = gdeg == 4 and not d6
    check("C1: harness FINDS completions when they exist (quasi-triangular deg 4)", ok)
    # C2: deg-2 P: the window reaches deg 6 (H deg <= 3 -> Q deg 6 with top prop. to
    # (ell^2)^3): the detector's positive path MUST fire here.
    r = complete(x + ell**2)
    ok = r is not None
    if ok:
        Qg, frees = r
        d6, real = analyze(Qg, frees, (ell**2) ** 3)
        print(f"  C2 x+(x+y)^2: consistent, {len(frees)} free, deg6-any={d6}, "
              f"top-prop-h3 realizable={real}")
        ok = d6 and real
    check("C2: the detector FIRES on a genuine deg-6 realization (positive path)", ok)


PARTS = {"A": partA, "B": partB, "C": partC}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
