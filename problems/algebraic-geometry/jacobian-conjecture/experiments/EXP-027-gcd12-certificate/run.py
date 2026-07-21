# EXP-027: the gcd-12 certificate at (24, <= 36). CPU-only, sympy over QQ.
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import Matrix, Poly, cancel, expand, factor, gcd, lcm, symbols  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def mons(dmin, dmax):
    return [x**i * y**(d - i) for d in range(dmin, dmax + 1) for i in range(d + 1)]


def pairings_gcd(Pexpr, nmax, tag):
    t0 = time.time()
    MQ = mons(2, nmax)
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(b * m for b, m in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(Pexpr, Q0) - 1), x, y).coeffs() if e != 0]
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
    print(f"  {tag}: {M.rows} eqs, {M.cols} unknowns, {len(ns)} null vectors, "
          f"{len(fs)} pairings, gcd = {g}, {time.time() - t0:.1f} s")
    return g


def pure_a_power(g, a):
    if g is None:
        return False
    p = Poly(expand(g), a)
    return len(p.monoms()) == 1


a = symbols("a_")
g1 = pairings_gcd(x + a * (x**4 * y**5) ** 2, 27, "validate (18,<=27)")
check("validation: EXP-026 certificate reproduces", pure_a_power(g1, a), f"gcd = {g1}")
g2 = pairings_gcd(x + a * (x**5 * y**7) ** 2, 36, "certify (24,<=36)")
check("THE CERTIFICATE: no Keller partner of degree <= 36 for ANY a != 0 (gcd 12)",
      pure_a_power(g2, a), f"gcd = {g2}")
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
