# EXP-028: the polygon strategy: lattice sieve, the decisive window, obstruction anatomy.
# CPU-only, sympy over QQ. Run: run.py [A|B|C|D]
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


def partA():
    print("=" * 76)
    print("Part A: the lattice sieve (similarity-admissible partner degrees)")
    print("=" * 76)
    for (p, q) in ((4, 5), (5, 7)):
        m = 2 * (p + q)
        verts = [(1, 0), (2 * p, 2 * q)]
        admissible = []
        for n in range(2, 61):
            r = Rational(n, m)
            ok = all((r * vx).is_integer and (r * vy).is_integer for vx, vy in verts)
            if ok:
                admissible.append(n)
        pred = [k for k in range(2, 61) if k % m == 0]
        print(f"  h = x^{p} y^{q} (m = {m}): admissible n <= 60: {admissible}")
        check(f"A: for m = {m}, similarity admits ONLY multiples of {m}",
              admissible == pred)


def system(Pexpr, MQ, B):
    Q0 = y + sum(b * mm for b, mm in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(Pexpr, Q0) - 1), x, y).coeffs() if e != 0]
    return eqs


def partB():
    print("=" * 76)
    print("Part B: the decisive window (18, <= 36): contains the divisible rung n = 36")
    print("=" * 76)
    h = x**4 * y**5
    MQ = mons(2, 36)
    B = symbols(f"B0:{len(MQ)}")
    print(f"  window unknowns: {len(MQ)}")
    allempty = True
    for av in (1, -2, Rational(1, 3)):
        t0 = time.time()
        eqs = system(x + av * h**2, MQ, B)
        ls = linsolve(eqs, list(B))
        tag = "CONSISTENT (conjecture dies: escalate!)" if ls else "INCONSISTENT"
        print(f"  B[a={av}]: {tag} ({time.time() - t0:.1f} s)")
        allempty &= not ls
    check("B: the (18, <= 36) window is EMPTY even across the divisible rung", allempty)


def partC():
    print("=" * 76)
    print("Part C: the certificate at (18, <= 36), a symbolic")
    print("=" * 76)
    a = symbols("a_")
    h = x**4 * y**5
    MQ = mons(2, 36)
    B = symbols(f"B0:{len(MQ)}")
    t0 = time.time()
    Q0 = y + sum(b * mm for b, mm in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(x + a * h**2, Q0) - 1), x, y).coeffs() if e != 0]
    M = Matrix([[expand(e.diff(b)) for b in B] for e in eqs])
    rhs = Matrix([-expand(e.subs({b: 0 for b in B})) for e in eqs])
    ns = M.T.nullspace()
    fs = []
    for c in ns:
        den = lcm([cancel(e).as_numer_denom()[1] for e in c])
        cc = Matrix([expand(cancel(e * den)) for e in c])
        assert all(expand(v) == 0 for v in (cc.T * M)), "not left-null"
        f = expand((cc.T * rhs)[0, 0])
        if f != 0:
            fs.append(f)
    g = None
    if fs:
        g = fs[0]
        for f in fs[1:]:
            g = gcd(g, f)
        g = factor(g)
    print(f"  C: {M.rows} eqs, {M.cols} unknowns, {len(ns)} null vectors, {len(fs)} "
          f"pairings, gcd = {g}, {time.time() - t0:.1f} s")
    ok = g is not None and len(Poly(expand(g), a).monoms()) == 1
    check("C: NO Keller partner of degree <= 36 for ANY a != 0 (past the divisible rung)",
          ok)


def partD():
    print("=" * 76)
    print("Part D: obstruction anatomy (certificate-vector support at (4, <= 6/10))")
    print("=" * 76)
    a = symbols("a_")
    for nmax in (6, 10):
        MQ = mons(2, nmax)
        B = symbols(f"B0:{len(MQ)}")
        Q0 = y + sum(b * mm for b, mm in zip(B, MQ))
        Jm1 = Poly(expand(jac2(x + a * (x * y) ** 2, Q0) - 1), x, y)
        rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs()) if e != 0]
        eqs = [e for _, e in rows]
        M = Matrix([[expand(e.diff(b)) for b in B] for e in eqs])
        rhs = Matrix([-expand(e.subs({b: 0 for b in B})) for e in eqs])
        ns = M.T.nullspace()
        found = False
        for c in ns:
            den = lcm([cancel(e).as_numer_denom()[1] for e in c])
            cc = [expand(cancel(e * den)) for e in c]
            f = expand(sum(ci * rhs[i, 0] for i, ci in enumerate(cc)))
            if f == 0:
                continue
            found = True
            sup = [(rows[i][0], ci) for i, ci in enumerate(cc) if ci != 0]
            degs = sorted({sum(mo) for mo, _ in sup})
            print(f"  D[<= {nmax}]: pairing = {factor(f)}; support rows: "
                  f"{len(sup)}/{len(rows)}; equation degrees in support: {degs}")
            for mo, ci in sup[:10]:
                print(f"    row x^{mo[0]} y^{mo[1]} (deg {sum(mo)}): weight {ci}")
            break
        check(f"D[<= {nmax}]: obstruction vector extracted and its support recorded",
              found)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
