# EXP-051: the half-plane tower lemma.
# CPU-only, sympy. Run: run.py [A|B|C]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, gcd_list,  # noqa: E402
                   lcm, symbols)

failures = []
a, b = symbols("a b")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def build_H(P, N):
    """H-restricted window system: rows with i <= j (contains the constant row)."""
    MQ = [(i, d - i) for d in range(2, N + 1) for i in range(d + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * x**i * y**j for bb, (i, j) in zip(B, MQ))
    Jm1 = Poly(expand(jac2(P, Q0) - 1), x, y)
    rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs())
            if e != 0 and mo[0] <= mo[1]]
    M = Matrix([[expand(e.diff(bb)) for bb in B] for _, e in rows])
    rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for _, e in rows])
    return MQ, rows, M, rhs


def h_certificate(P, N):
    MQ, rows, M, rhs = build_H(P, N)
    for cv in M.T.nullspace():
        den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
        cc = [expand(cancel(e * den)) for e in cv]
        g = gcd_list([e for e in cc if e != 0])
        if g not in (0, 1):
            cc = [cancel(e / g) for e in cc]
        resid = [expand(sum(cc[r] * M[r, k] for r in range(M.rows)))
                 for k in range(M.cols)]
        if any(rr != 0 for rr in resid):
            return None, len(rows)
        f = expand(sum(cc[r] * rhs[r, 0] for r in range(M.rows)))
        if f != 0:
            return f, len(rows)
    return None, len(rows)


def R0(l0):
    return expand(x * (x * y**4 - l0) ** 3)


def partA():
    print("=" * 76)
    print("Part A: H-certificates at (2,2,2), symbolic (a,b), windows 7..10")
    print("=" * 76)
    ok = True
    P = x + a * (x * y) ** 2 + b * x**2
    for N in (7, 8, 9, 10):
        f, nr = h_certificate(P, N)
        got = f is not None
        ok &= got
        if got:
            ok &= len(Poly(f, a, b).monoms()) == 1
        print(f"  A N={N}: H-rows {nr}: pairing {factor(f) if got else 'NONE'}")
    check("A: the H-subsystem carries a cleared MONOMIAL-pairing certificate at every "
          "window 7..10 (all parameters)", ok)


def partB():
    print("=" * 76)
    print("Part B: case-c vacuity (T-output outside H implies column H-part zero)")
    print("=" * 76)
    ok = True
    for (nm, P) in (("(2,2,2)", x + Rational(2) * (x * y) ** 2 + Rational(3) * x**2),
                    ("P32", expand(x + R0(1) ** 2 + x**2))):
        Pp = Poly(expand(P), x, y)
        D = Pp.total_degree()
        T = expand(sum(co * x**i * y**j for (i, j), co in Pp.terms() if i + j == D))
        mu = min(i - j for (i, j) in Pp.monoms())
        muT = min(i - j for (i, j) in Poly(T, x, y).monoms())
        okm = mu == muT
        ok &= okm
        M0 = D + 3
        viol = 0
        for al in range(M0 + 1):
            be = M0 - al
            col = expand(jac2(expand(P), x**al * y**be))
            if col == 0:
                continue
            outs = Poly(col, x, y).monoms()
            tout = expand(jac2(T, x**al * y**be))
            if tout == 0:
                continue
            t_min = min(i - j for (i, j) in Poly(tout, x, y).monoms())
            if t_min > 0 and any(i <= j for (i, j) in outs):
                viol += 1
        ok &= viol == 0
        print(f"  B {nm}: mu = {mu} attained by T: {okm}; case-c violations at degree "
              f"{M0}: {viol}")
    check("B: T attains mu and no straddling column exists (case-c vacuous) on both "
          "shapes", ok)


def partC():
    print("=" * 76)
    print("Part C: THE FRONTIER PAYOFF: H-certificates on proper-power-top samples")
    print("=" * 76)
    ok = True
    P32 = expand(x + R0(1) ** 2 + x**2)
    f, nr = h_certificate(P32, 14)
    got = f is not None
    ok &= got
    print(f"  C P32 = x + R0(1)^2 + x^2 (deg 32, T = x^8 y^24): H-certificate at "
          f"N=14 ({nr} H-rows): pairing {f if got else 'NONE'}")
    g8 = expand((x**2 * y**7) ** 8)
    P72 = expand(x + Rational(2) * g8 + x**2)
    f2, nr2 = h_certificate(P72, 12)
    got2 = f2 is not None
    ok &= got2
    print(f"  C P72 = x + 2 g^8 + x^2 (deg 72, corner (16,56)): H-certificate at "
          f"N=12 ({nr2} H-rows): pairing {f2 if got2 else 'NONE'}")
    check("C: both frontier proper-power-top samples carry H-certificates: by the "
          "HALF-PLANE TOWER LEMMA they are excluded at ALL partner degrees", ok)


PARTS = {"A": partA, "B": partB, "C": partC}

if __name__ == "__main__":
    todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C"]
    for p_ in todo:
        PARTS[p_]()
        print()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
