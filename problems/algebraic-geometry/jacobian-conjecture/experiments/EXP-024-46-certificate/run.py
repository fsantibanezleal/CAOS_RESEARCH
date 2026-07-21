# EXP-024: the (4,6) window certificate. CPU-only, sympy over QQ. Parts: A | B.
# Run: .\.venv\Scripts\python.exe ...\EXP-024-46-certificate\run.py [A|B]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import Matrix, Poly, cancel, expand, factor, symbols  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


MQ = [x**i * y**(d - i) for d in range(2, 7) for i in range(d + 1)]
B = symbols(f"B0:{len(MQ)}")


def system(Pexpr):
    """M B = rhs from the coefficients of J(P, Q) - 1 (linear in B by bilinearity)."""
    Q0 = y + sum(b * m for b, m in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(Pexpr, Q0) - 1), x, y).coeffs() if e != 0]
    M = Matrix([[expand(e.diff(b)) for b in B] for e in eqs])
    rhs = Matrix([-expand(e.subs({b: 0 for b in B})) for e in eqs])
    return M, rhs


def certificates(Pexpr, tag, params):
    """Sound all-parameter certificates. A cleared left-null vector c (polynomial entries,
    c^T M = 0 as a polynomial identity) pairs with rhs to f = c^T rhs; f(params0) != 0
    proves inconsistency AT params0. RREF over the fraction field is NOT sound for specific
    values (it normalizes the obstruction to 1: generic-only). Returns the list of nonzero
    pairings f, plus (rows, cols)."""
    from sympy import gcd_list, lcm
    M, rhs = system(Pexpr)
    ns = M.T.nullspace()
    fs = []
    for c in ns:
        den = lcm([cancel(e).as_numer_denom()[1] for e in c])
        cc = Matrix([expand(cancel(e * den)) for e in c])
        assert all(expand(v) == 0 for v in (cc.T * M)), "cleared vector not left-null"
        f = expand((cc.T * rhs)[0, 0])
        if f != 0:
            fs.append(f)
    print(f"  {tag}: {M.rows} eqs, {M.cols} unknowns, {len(ns)} left-null vectors, "
          f"{len(fs)} nonzero pairings")
    return fs


def pure_a_power(f, a, others):
    """True when f = (rational unit) * a^k (no dependence on the other parameters)."""
    p = Poly(expand(f), a, *others)
    mons = p.monoms()
    return len(mons) == 1 and all(all(m[i] == 0 for i in range(1, 1 + len(others)))
                                  for m in mons)


def partA():
    print("=" * 76)
    print("Part A: pure slice P = x + a (xy)^2, all a != 0 (certificate)")
    print("=" * 76)
    from sympy import gcd
    a = symbols("a_")
    fs = certificates(x + a * (x * y) ** 2, "A", (a,))
    ok = False
    if fs:
        g = fs[0]
        for f in fs[1:]:
            g = gcd(g, f)
        g = factor(g)
        print(f"  gcd of certificate pairings: {g}")
        ok = pure_a_power(g, a, ())
    check("A: certificate pairings exist and their gcd is (unit) * a^k: the (4, <= 6) "
          "window is empty for EVERY a != 0 (sound, not merely generic)", ok)


def partB():
    print("=" * 76)
    print("Part B: full parameters (P2, P3 arbitrary), certificates over the 8-param field")
    print("=" * 76)
    a = symbols("a_")
    ps = symbols("p20 p11 p02 p30 p21 p12 p03")
    p20, p11, p02, p30, p21, p12, p03 = ps
    P = (x + p20 * x**2 + p11 * x * y + p02 * y**2 + p30 * x**3 + p21 * x**2 * y
         + p12 * x * y**2 + p03 * y**3 + a * (x * y) ** 2)
    fs = certificates(P, "B", (a,) + ps)
    if not fs:
        check("B: certificate pairings over the full parameter field", False, "none")
        return
    pure = [f for f in fs if pure_a_power(f, a, ps)]
    print(f"  {len(pure)}/{len(fs)} pairings are pure a-powers")
    if pure:
        print(f"    example: {factor(pure[0])}")
    check("B: some pairing is (unit) * a^k in ALL parameters: emptiness certified for "
          "every P2, P3 and a != 0", bool(pure))


PARTS = {"A": partA, "B": partB}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
