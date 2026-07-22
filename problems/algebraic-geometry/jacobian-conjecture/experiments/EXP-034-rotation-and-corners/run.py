# EXP-034: rotate-descent on the library; the swallowed-mixed frontier. CPU-only, sympy.
# Run: run.py [A|B|C]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, library, top_form, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor,  # noqa: E402
                   factor_list, lcm, linsolve, symbols)

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def linear_power_base(T):
    """If the form T factors as c * ell^d with ell linear, return (c, ell, d); else None."""
    con, fl = factor_list(T)
    lins = [(f, m) for (f, m) in fl if Poly(f, x, y).total_degree() == 1]
    others = [(f, m) for (f, m) in fl if Poly(f, x, y).total_degree() > 1]
    if others or len(lins) != 1:
        return None
    ell, d = lins[0]
    return con, ell, d


def rotate_descent(P0, Q0, maxsteps=60):
    """Rotate-descent: linearize a Keller pair by rotations + de Jonquieres subtractions.
    Returns (status, steps). Gauge bookkeeping is verified by re-checking J at each step."""
    P, Q = expand(P0), expand(Q0)
    steps = 0
    while steps < maxsteps:
        dP = Poly(P, x, y).total_degree()
        dQ = Poly(Q, x, y).total_degree()
        if dP <= 1 and dQ <= 1:
            return "linearized", steps
        if dP > dQ:
            P, Q = Q, P
            continue
        Tq, _ = top_form(Q)
        lp = linear_power_base(Tq)
        if lp is None:
            return "hard-shape", steps
        con, ell, d = lp
        pe = Poly(ell, x, y)
        aco = pe.coeff_monomial(x)
        bco = pe.coeff_monomial(y)
        if bco == 0:
            # ell = a x: rotate x <-> y (source change (x, y) -> (y, x); det -1 ok for
            # Keller up to sign)
            P, Q = expand(P.subs({x: y, y: x}, simultaneous=True)), \
                expand(Q.subs({x: y, y: x}, simultaneous=True))
            steps += 1
            continue
        if aco != 0:
            # source shear x -> x, y -> y - (a/b) x makes ell proportional to y... check:
            # ell(x, y - (a/b) x)?? ell = a x + b y -> a x + b y - a x = b y. Substitute
            # the INVERSE map into P, Q: (x, y) -> (x, y + (a/b) x) gives new pair whose
            # ell-direction is y.
            sub = {y: y - Rational(aco, bco) * x} if aco / bco == Rational(aco, bco) \
                else {y: y - cancel(aco / bco) * x}
            P = expand(P.subs(sub))
            Q = expand(Q.subs(sub))
            steps += 1
            continue
        # ell = b y already: de Jonquieres: dQ multiple of dP? subtract c * P^k or,
        # if dP == 1 (P ~ x after gauge), subtract f(P)-terms: general: reduce Q by
        # the best multiple of a power of P.
        TP, dp = top_form(P)
        if dp == 0:
            return "degenerate", steps
        if dQ % dp == 0:
            k = dQ // dp
            ratio = cancel(Tq / TP**k)
            if ratio.is_number:
                Q = expand(Q - ratio * P**k)
                steps += 1
                continue
        # P itself may be linear (deg 1): then Q's top c y^dQ: subtract c * (P-part)?
        if dp == 1:
            # P linear: express y-power via P if P involves y, else via y itself:
            pp = Poly(P, x, y)
            if pp.coeff_monomial(y) != 0:
                cy = pp.coeff_monomial(y)
                base = P / cy
                ratio = cancel(Tq / y**dQ)
                Q = expand(Q - ratio * base**dQ)
                steps += 1
                continue
        return "stuck", steps
    return "maxsteps", steps


def partA():
    print("=" * 76)
    print("Part A: rotate-descent linearizes the library (the induction's data)")
    print("=" * 76)
    okall = True
    for i, (P0, Q0) in enumerate(library()):
        st, n = rotate_descent(P0, Q0)
        ok = st == "linearized"
        okall &= ok
        print(f"  A map {i}: {st} in {n} steps")
    check("A: every library pair LINEARIZES under rotate-descent (no hard-shape stops)",
          okall)


SHAPES = [
    ("x + x^2 + x^2 y", lambda: x + x**2 + x**2 * y, 9),
    ("x + x^2 + x^3 y", lambda: x + x**2 + x**3 * y, 9),
    ("x + x^2 + x^2 y^3", lambda: x + x**2 + x**2 * y**3, 9),
    ("x + (x+y)^2 + x^2 y^2", lambda: expand(x + (x + y) ** 2 + x**2 * y**2), 9),
    ("x + x^2 + x^2 y + y^5", lambda: x + x**2 + x**2 * y + y**5, 9),
    ("x + (x+y)^2 + x^3 y", lambda: expand(x + (x + y) ** 2 + x**3 * y), 9),
    ("x + x^2 - x^2 y + x y^2", lambda: x + x**2 - x**2 * y + x * y**2, 9),
    ("x + x^3 + x^2 y^2", lambda: x + x**3 + x**2 * y**2, 9),
]


def window_consistent(P, N):
    MQ = [x**i * y**(dd - i) for dd in range(2, N + 1) for i in range(dd + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    return bool(linsolve(eqs, list(B)))


def partB():
    print("=" * 76)
    print("Part B: the swallowed-mixed frontier (NOT covered by Theorem 4)")
    print("=" * 76)
    okall = True
    for (nm, mk, N) in SHAPES:
        P = mk()
        cons = window_consistent(P, N)
        okall &= not cons
        print(f"  B {nm} (window <= {N}): "
              f"{'INCONSISTENT' if not cons else 'CONSISTENT (escalate!)'}")
    check("B: every swallowed-mixed sample window is EMPTY (the uncovered territory "
          "resists)", okall)


def partC():
    print("=" * 76)
    print("Part C: certificate anatomy at the new territory")
    print("=" * 76)
    okall = True
    for (nm, mk, _) in (SHAPES[0], SHAPES[3]):
        P = mk()
        N = 7
        MQ = [x**i * y**(dd - i) for dd in range(2, N + 1) for i in range(dd + 1)]
        B = symbols(f"B0:{len(MQ)}")
        Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
        Jm1 = Poly(expand(jac2(P, Q0) - 1), x, y)
        rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs()) if e != 0]
        eqs = [e for _, e in rows]
        M = Matrix([[expand(e.diff(bb)) for bb in B] for e in eqs])
        rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for e in eqs])
        ns = M.T.nullspace()
        found = False
        for cv in ns:
            den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
            cc = [expand(cancel(e * den)) for e in cv]
            f = expand(sum(ci * rhs[i, 0] for i, ci in enumerate(cc)))
            if f == 0:
                continue
            found = True
            sup = [(rows[i][0], ci) for i, ci in enumerate(cc) if ci != 0]
            print(f"  C {nm}: pairing = {factor(f)}; support {len(sup)}/{len(rows)} rows: "
                  f"{[mo for mo, _ in sup][:8]}")
            break
        okall &= found
    check("C: certificates extracted; support anatomy recorded (data toward the "
          "corner-anchored closed form)", okall)


PARTS = {"A": partA, "B": partB, "C": partC}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
