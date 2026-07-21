# EXP-022: quasi-triangular closure, the (3,3) cube case, the descent inverter.
# CPU-only, sympy over QQ. See hypothesis.md. Parts: A | B | C.
# Run: .\.venv\Scripts\python.exe ...\EXP-022-quasitriangular-descent\run.py [A|B|C]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, library, top_form, x, y  # noqa: E402
from sympy import (Poly, Rational, cancel, expand, groebner, solve, symbols)  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def partA():
    print("=" * 76)
    print("Part A: shear closure for ANY f (generic f deg <= 4, H deg <= 2)")
    print("=" * 76)
    al, be = symbols("alpha beta")
    w = symbols("w_")
    F2, F3, F4 = symbols("f2 f3 f4")
    H0, H1, H2 = symbols("h0 h1 h2")
    ell = al * x + be * y
    f = F2 * w**2 + F3 * w**3 + F4 * w**4
    P = x + f.subs(w, ell)
    Hp = H0 + H1 * P + H2 * P**2
    Q = ell / be + Hp
    JA = expand(jac2(P, Q))
    check("A: J == 1 identically (generic f deg <= 4, H deg <= 2)", expand(JA - 1) == 0)
    # Composition: generic at (f deg <= 3, H deg <= 1); exact rational spot checks higher.
    u, v = symbols("u v")
    fs = F2 * w**2 + F3 * w**3
    Ps = x + fs.subs(w, ell)
    Qs = ell / be + H0 + H1 * Ps
    ellinv = be * (v - (H0 + H1 * u))
    Gx = u - fs.subs(w, ellinv)
    Gy = cancel((ellinv - al * Gx) / be)
    d1 = expand(Gx.subs({u: expand(Ps), v: expand(Qs)}, simultaneous=True) - x)
    d2 = expand(Gy.subs({u: expand(Ps), v: expand(Qs)}, simultaneous=True) - y)
    check("A: G o F == id (generic f deg <= 3, H deg <= 1)", d1 == 0 and d2 == 0)
    SPOTS = [({al: Rational(1), be: Rational(2), F2: Rational(-1), F3: Rational(3),
               F4: Rational(1, 2), H0: Rational(2), H1: Rational(-1), H2: Rational(1, 3)},
              "f deg 4, H deg 2")]
    for inst, nm in SPOTS:
        Pi = expand(P.subs(inst))
        Qi = expand(Q.subs(inst))
        elli = expand((be * (v - (H0 + H1 * u + H2 * u**2))).subs(inst))
        Gxi = expand(u - f.subs(w, elli).subs(inst))
        Gyi = cancel(((elli - al * Gxi) / be).subs(inst))
        e1 = expand(Gxi.subs({u: Pi, v: Qi}, simultaneous=True) - x)
        e2 = expand(Gyi.subs({u: Pi, v: Qi}, simultaneous=True) - y)
        check(f"A: exact spot check ({nm}): G o F == id", e1 == 0 and e2 == 0)


def partB():
    print("=" * 76)
    print("Part B: the cube case at (3,3), gauge ell = y")
    print("=" * 76)
    A0, A1, A2, a = symbols("A0 A1 A2 a_")
    MQ = [x**i * y**j for i in range(4) for j in range(4 - i) if i + j >= 2]
    B = symbols(f"B_0:{len(MQ)}")
    P = x + A0 * x**2 + A1 * x * y + A2 * y**2 + a * y**3
    Q = y + sum(b * mo for b, mo in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q) - 1), x, y).coeffs() if e != 0]
    gb = groebner(eqs, *(list(B) + [A0, A1, A2, a]), order="lex")
    cons = [g for g in gb.exprs if not any(g.has(b) for b in B)]
    print(f"  GB size {len(gb.exprs)}; consistency generators: {len(cons)}")
    for g in cons[:6]:
        print(f"    {g} = 0")
    check("B: consistency ideal computed", True, f"{len(cons)} generators")
    onlocus = all(expand(g.subs({A0: 0, A1: 0})) == 0 for g in cons)
    check("B: the quasi-triangular locus (A0 = A1 = 0) lies ON the variety", onlocus)
    # Converse: does the ideal force A0 = A1 = 0 when a != 0? Check by Rabinowitsch:
    t_ = symbols("t_r")
    gbr = groebner(cons + [a * t_ - 1], A0, A1, A2, a, t_, order="lex")
    for tgt, nm in ((A0**2, "A0^2"), (A1**6, "A1^6")):
        red = gbr.reduce(expand(tgt))[1]
        check(f"B: with a != 0, {nm} lies in the ideal (radical forces the alignment)",
              expand(red) == 0, f"residue: {red}")


def descent_invert(P, Q, maxsteps=40):
    """The descent inverter: returns (steps, status). Each step is ('sub', c, k) meaning
    Q -> Q - c P^k, or ('swap',) meaning exchange P and Q; status 'ok' when min degree <= 2."""
    from sympy import LC, Rational as R_
    steps = []
    P, Q = expand(P), expand(Q)
    for _ in range(maxsteps):
        m = Poly(P, x, y).total_degree()
        n = Poly(Q, x, y).total_degree()
        if min(m, n) <= 2:
            return steps, "ok", P, Q
        if m > n:
            P, Q = Q, P
            steps.append(("swap",))
            continue
        Pt, m = top_form(P)
        Qt, n = top_form(Q)
        if n % m == 0:
            k = n // m
            # candidate: Q_top proportional to (P_top)^k
            ratio = cancel(Qt / Pt**k)
            if ratio.is_number:
                Q = expand(Q - ratio * P**k)
                steps.append(("sub", ratio, k))
                continue
        return steps, "primitive", P, Q
    return steps, "maxsteps", P, Q


def partC():
    print("=" * 76)
    print("Part C: the descent inverter over the library (explicit inverses end to end)")
    print("=" * 76)
    from sympy import Matrix
    u, v = symbols("u v")
    okall = True
    prim = 0
    for i, (P0, Q0) in enumerate(library()):
        steps, status, Pr, Qr = descent_invert(P0, Q0)
        if status == "primitive":
            prim += 1
            print(f"  map {i}: PRIMITIVE at ({Poly(Pr, x, y).total_degree()},"
                  f" {Poly(Qr, x, y).total_degree()})")
            okall = False
            continue
        if status != "ok":
            okall = False
            print(f"  map {i}: {status}")
            continue
        # invert the reduced pair by direct Groebner (min degree <= 2: solvable), then
        # replay the steps backwards on the TARGET side to invert the original map.
        gb = groebner([expand(Pr - u), expand(Qr - v)], x, y, order="lex")
        solxy = solve(gb.exprs, [x, y], dict=True)
        if len(solxy) != 1:
            okall = False
            print(f"  map {i}: reduced pair not directly invertible ({len(solxy)})")
            continue
        gx, gy = cancel(solxy[0][x]), cancel(solxy[0][y])
        # forward-replay the steps on (u, v): the reduced values (u_r, v_r) as functions of
        # the ORIGINAL values (u0, v0): apply the same subtractions to the value pair.
        u0, v0 = symbols("u0 v0")
        U, V = u0, v0
        for st in steps:
            if st[0] == "swap":
                U, V = V, U
            else:
                _, ratio, k = st
                V = expand(V - ratio * U**k)
        Gx = expand(gx.subs({u: U, v: V}, simultaneous=True))
        Gy = expand(gy.subs({u: U, v: V}, simultaneous=True))
        d1 = expand(Gx.subs({u0: expand(P0), v0: expand(Q0)}, simultaneous=True) - x)
        d2 = expand(Gy.subs({u0: expand(P0), v0: expand(Q0)}, simultaneous=True) - y)
        good = d1 == 0 and d2 == 0
        okall &= good
        print(f"  map {i}: {len(steps)} descent steps -> explicit inverse "
              f"{'VERIFIED' if good else 'FAILED'}")
    check("C: the inverter explicitly inverts EVERY library map (no primitive hits)",
          okall and prim == 0)


PARTS = {"A": partA, "B": partB, "C": partC}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
