# EXP-026: the composite-gcd frontier: (18, <= 27), gcd 9. CPU-only, sympy over QQ.
# Run: .\.venv\Scripts\python.exe ...\EXP-026-composite-gcd\run.py [A|B|C|D|E]
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, gcd, lcm,  # noqa: E402
                   linsolve, symbols)

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def mons(dmin, dmax):
    return [x**i * y**(d - i) for d in range(dmin, dmax + 1) for i in range(d + 1)]


def system(Pexpr, MQ, B):
    Q0 = y + sum(b * m for b, m in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(Pexpr, Q0) - 1), x, y).coeffs() if e != 0]
    M = Matrix([[expand(e.diff(b)) for b in B] for e in eqs])
    rhs = Matrix([-expand(e.subs({b: 0 for b in B})) for e in eqs])
    return M, rhs, eqs


def pairings(Pexpr, MQ, B, tag):
    t0 = time.time()
    M, rhs, _ = system(Pexpr, MQ, B)
    ns = M.T.nullspace()
    fs = []
    for c in ns:
        den = lcm([cancel(e).as_numer_denom()[1] for e in c])
        cc = Matrix([expand(cancel(e * den)) for e in c])
        assert all(expand(v) == 0 for v in (cc.T * M)), "cleared vector not left-null"
        f = expand((cc.T * rhs)[0, 0])
        if f != 0:
            fs.append(f)
    print(f"  {tag}: {M.rows} eqs, {M.cols} unknowns, {len(ns)} null vectors, "
          f"{len(fs)} nonzero pairings, {time.time() - t0:.1f} s")
    return fs


def gcd_all(fs):
    g = fs[0]
    for f in fs[1:]:
        g = gcd(g, f)
    return factor(g)


def pure_a_power(g, a, others):
    p = Poly(expand(g), a, *others)
    ms = p.monoms()
    return len(ms) == 1 and all(all(m[i] == 0 for i in range(1, 1 + len(others)))
                                for m in ms)


def consistent(Pexpr, MQ, B, tag):
    t0 = time.time()
    Q0 = y + sum(b * m for b, m in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(Pexpr, Q0) - 1), x, y).coeffs() if e != 0]
    ls = linsolve(eqs, list(B))
    ok = bool(ls)
    print(f"  {tag}: {'CONSISTENT (escalate!)' if ok else 'INCONSISTENT'} "
          f"({time.time() - t0:.1f} s)")
    return ok


def partA():
    print("=" * 76)
    print("Part A: instrument validation at scale (reproduce EXP-024 on this code path)")
    print("=" * 76)
    a = symbols("a_")
    MQ = mons(2, 6)
    B = symbols(f"B0:{len(MQ)}")
    fs = pairings(x + a * (x * y) ** 2, MQ, B, "A[(4,<=6)]")
    ok = bool(fs) and pure_a_power(gcd_all(fs), a, ())
    g = gcd_all(fs) if fs else None
    check("A: the (4, <= 6) pure-slice certificate reproduces (pure a-power gcd)", ok,
          f"gcd = {g}")


def partB():
    print("=" * 76)
    print("Part B: the (18, <= 27) window, h = x^4 y^5, numeric a")
    print("=" * 76)
    h = x**4 * y**5
    MQ = mons(2, 27)
    B = symbols(f"B0:{len(MQ)}")
    print(f"  window unknowns: {len(MQ)}")
    allempty = True
    for av in (1, -2, Rational(1, 3)):
        allempty &= not consistent(x + av * h**2, MQ, B, f"B[a={av}]")
    check("B: the (18, <= 27) window is EMPTY at every numeric sample", allempty)


def partC():
    print("=" * 76)
    print("Part C: h-shape sweep at a = 1 (monomial / split factor / binomial tail)")
    print("=" * 76)
    MQ = mons(2, 27)
    B = symbols(f"B0:{len(MQ)}")
    allempty = True
    for nm, h in (("x^5y^4", x**5 * y**4),
                  ("(xy)^4(x+y)", (x * y) ** 4 * (x + y)),
                  ("x^4y^5+y^9", x**4 * y**5 + y**9)):
        allempty &= not consistent(x + h**2, MQ, B, f"C[{nm}]")
    check("C: the window is EMPTY for every h shape", allempty)


def partD():
    print("=" * 76)
    print("Part D: the certificate, h = x^4 y^5, a symbolic (all a != 0)")
    print("=" * 76)
    a = symbols("a_")
    MQ = mons(2, 27)
    B = symbols(f"B0:{len(MQ)}")
    fs = pairings(x + a * (x**4 * y**5) ** 2, MQ, B, "D[(18,<=27)]")
    ok = False
    if fs:
        g = gcd_all(fs)
        print(f"  D: gcd of pairings = {g}")
        ok = pure_a_power(g, a, ())
    check("D: NO Keller partner of degree <= 27 for ANY a != 0 (gcd 9 territory: "
          "literature-uncovered)", ok)


def partE():
    print("=" * 76)
    print("Part E: reach test at gcd 12: the (24, <= 36) window, h = x^5 y^7, a = 1")
    print("=" * 76)
    MQ = mons(2, 36)
    B = symbols(f"B0:{len(MQ)}")
    print(f"  window unknowns: {len(MQ)}")
    empty = not consistent(x + (x**5 * y**7) ** 2, MQ, B, "E[a=1]")
    check("E: the (24, <= 36) window is EMPTY at the probe sample", empty)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD, "E": partE}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D", "E"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
