# EXP-033: k = 0, m = 0 edges and the vertex dichotomy. CPU-only, sympy over QQ.
# Run: run.py [A|B|C|D]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, gcd, lcm,  # noqa: E402
                   linsolve, symbols)

failures = []
yv = symbols("Y_")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def window_consistent(P, N):
    MQ = [x**i * y**(dd - i) for dd in range(2, N + 1) for i in range(dd + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    return bool(linsolve(eqs, list(B)))


def partA():
    print("=" * 76)
    print("Part A: k = 0 class structure, kill, kernels")
    print("=" * 76)
    C = symbols("C1:4")
    phi = 1 + C[0] * y + C[1] * y**2 + C[2] * y**3
    P = expand(x * phi)
    okf = True
    for s in range(5):
        for qexp in range(4):
            g = x**s * y**qexp
            lhs = expand(jac2(P, g))
            q = y**qexp
            rhs = expand(x**s * (phi * q.diff(y) - s * phi.diff(y) * q))
            if expand(lhs - rhs) != 0:
                okf = False
                print(f"  A MISMATCH s={s} q=y^{qexp}")
    check("A1: L(x^s q(y)) = x^s (phi q' - s phi' q) exact (symbolic phi deg 3)", okf)
    # s = 0 truncated systems: phi h' = 1 with deg h <= D: inconsistent over QQ(C)
    okk = True
    for D in (3, 6):
        H = symbols(f"H1:{D + 1}")
        h = sum(Hc * y**(j + 1) for j, Hc in enumerate(H))
        eqs = Poly(expand(phi * h.diff(y) - 1), y).coeffs()
        ls = linsolve([expand(e) for e in eqs], list(H))
        okk &= not ls
        print(f"  A2 s=0 truncation D={D}: {'INCONSISTENT' if not ls else 'CONSISTENT!'}")
    check("A2: the constant's class (phi h' = 1) is inconsistent at every truncation", okk)
    # kernels: class s kernel = (x phi)^s: verify via q with phi q' = s phi' q -> q = phi^s
    okr = True
    for s in (1, 2):
        q = expand(phi**s)
        res = expand(phi * q.diff(y) - s * phi.diff(y) * q)
        okr &= res == 0
        # and uniqueness at truncation: solve phi q' - s phi' q = 0, deg q <= s*3: space dim 1
        Dq = 3 * s
        Hc = symbols(f"K0:{Dq + 1}")
        qq = sum(hc * y**j for j, hc in enumerate(Hc))
        eqs = Poly(expand(phi * qq.diff(y) - s * phi.diff(y) * qq), y).coeffs()
        M = Matrix([[expand(e.diff(hc)) for hc in Hc] for e in eqs])
        ns = M.nullspace()
        okr &= len(ns) == 1
        print(f"  A3 class {s}: phi^{s} in kernel: {res == 0}; kernel dim {len(ns)}")
    check("A3: class-s kernels are exactly (x phi)^s", okr)


def partB():
    print("=" * 76)
    print("Part B: k = 0 windows and certificate; m = 0 windows")
    print("=" * 76)
    okall = True
    for (nm, P, N) in (
            ("x(1+y)", x * (1 + y), 8),
            ("x(1+y)^2", expand(x * (1 + y) ** 2), 8),
            ("x(1+y+y^2)", expand(x * (1 + y + y**2)), 8),
            ("x(1+y) + y^3", expand(x * (1 + y) + y**3), 8),
            ("x + x^2 (m=0)", x + x**2, 8),
            ("x + x^2 + x^3 (m=0)", x + x**2 + x**3, 8)):
        cons = window_consistent(P, N)
        okall &= not cons
        print(f"  B {nm}: {'INCONSISTENT' if not cons else 'CONSISTENT (refutes!)'}")
    check("B1: every k = 0 and m = 0 window is empty (incl. pure-y tails)", okall)
    c1 = symbols("c1_")
    P = expand(x * (1 + c1 * y))
    N = 6
    MQ = [x**i * y**(dd - i) for dd in range(2, N + 1) for i in range(dd + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    M = Matrix([[expand(e.diff(bb)) for bb in B] for e in eqs])
    rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for e in eqs])
    ns = M.T.nullspace()
    fs = []
    for cv in ns:
        den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
        cc = Matrix([expand(cancel(e * den)) for e in cv])
        f = expand((cc.T * rhs)[0, 0])
        if f != 0:
            fs.append(f)
    gg = None
    if fs:
        gg = fs[0]
        for f in fs[1:]:
            gg = gcd(gg, f)
        gg = factor(gg)
    p_ = Poly(expand(gg), c1) if gg is not None else None
    ok = p_ is not None and len(p_.monoms()) == 1
    check("B2: certificate for x(1 + c1 y): pairing gcd a pure c1-power", ok,
          f"gcd = {gg}")


def partC():
    print("=" * 76)
    print("Part C: the vertex dichotomy, three sides")
    print("=" * 76)
    okall = True
    # (i) vertex x + mixed monomials: excluded shapes
    for (nm, P, N) in (
            ("x + xy^2 + y^5", expand(x + x * y**2 + y**5), 9),
            ("x + x^2 y + y^4", expand(x + x**2 * y + y**4), 9),
            ("x + x^2 y^3", expand(x + x**2 * y**3), 9),
            ("x + xy + y^2 (vertex-x mixed)", expand(x + x * y + y**2), 9)):
        cons = window_consistent(P, N)
        okall &= not cons
        print(f"  C(i) {nm}: {'INCONSISTENT' if not cons else 'CONSISTENT (refutes!)'}")
    # (ii) triangular: components
    for (nm, P, N) in (("x + y^2", x + y**2, 6),
                       ("x + y^3 - 2y^2", x + y**3 - 2 * y**2, 6)):
        cons = window_consistent(P, N)
        okall &= cons
        print(f"  C(ii) {nm}: {'CONSISTENT (component, as derived)' if cons else 'FAIL'}")
    # (iii) x swallowed: components exist
    for (nm, P, N) in (("x + (x+y)^2", expand(x + (x + y) ** 2), 6),
                       ("x + (x+2y)^3", expand(x + (x + 2 * y) ** 3), 8)):
        cons = window_consistent(P, N)
        okall &= cons
        print(f"  C(iii) {nm}: {'CONSISTENT (escape route real)' if cons else 'FAIL'}")
    check("C: all three sides of the dichotomy behave exactly as derived", okall)


PARTS = {"A": partA, "B": partB, "C": partC}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
