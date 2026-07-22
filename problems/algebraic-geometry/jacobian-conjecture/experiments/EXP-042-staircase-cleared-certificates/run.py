# EXP-042: cleared all-parameter certificates for the staircase family.
# CPU-only, sympy over QQ(a, b). Run: run.py [A|B|C|D]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, gcd_list,  # noqa: E402
                   lcm, linsolve, symbols)

failures = []
a, b, c3 = symbols("a b c3")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def build(P, N):
    MQ = [(i, d - i) for d in range(2, N + 1) for i in range(d + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * x**i * y**j for bb, (i, j) in zip(B, MQ))
    Jm1 = Poly(expand(jac2(P, Q0) - 1), x, y)
    rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs()) if e != 0]
    M = Matrix([[expand(e.diff(bb)) for bb in B] for _, e in rows])
    rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for _, e in rows])
    return MQ, rows, M, rhs


def cleared_certificate(P, N, params):
    """Polynomial covector with c^T M == 0 identically; returns (pairing, nrows)."""
    MQ, rows, M, rhs = build(P, N)
    for cv in M.T.nullspace():
        den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
        cc = [expand(cancel(e * den)) for e in cv]
        g = gcd_list([e for e in cc if e != 0])
        if g != 0 and g != 1:
            cc = [cancel(e / g) for e in cc]
        # soundness: verify the polynomial identity c^T M == 0
        resid = [expand(sum(cc[r] * M[r, k] for r in range(M.rows)))
                 for k in range(M.cols)]
        if any(rr != 0 for rr in resid):
            return None, None, "identity failed"
        f = expand(sum(cc[r] * rhs[r, 0] for r in range(M.rows)))
        if f != 0:
            sup = sum(1 for e in cc if e != 0)
            return f, sup, None
    return None, None, "no nonzero pairing"


def partA():
    print("=" * 76)
    print("Part A: cleared certificates over the (u, v, d) grid (window 7)")
    print("=" * 76)
    ok = True
    allb = 0
    for (u, v) in ((2, 1), (2, 2), (3, 1), (3, 2)):
        for d in (2, 3):
            P = x + a * x**u * y**v + b * x**d
            f, sup, err = cleared_certificate(P, 7, (a, b))
            if f is None:
                ok = False
                print(f"  A (u,v,d)=({u},{v},{d}): FAILED ({err})")
                continue
            ff = factor(f)
            pf = Poly(f, a, b)
            bfree = all(mb == 0 for (_, mb) in pf.monoms())
            allb += 1 if bfree else 0
            print(f"  A (u,v,d)=({u},{v},{d}): pairing {ff}  "
                  f"(support {sup} rows; b-free: {bfree})")
            # sound conclusion requires monomial pairing (vanishes only on a=0 / b=0)
            ok &= len(pf.monoms()) == 1
    check("A: every grid point has a cleared certificate with MONOMIAL pairing "
          "(all-parameter emptiness: a != 0 kills the window)", ok,
          f"{allb}/8 pairings b-free (exclude ALL b)")


def partB():
    print("=" * 76)
    print("Part B: window stability at (2, 1, 2), N = 5..9")
    print("=" * 76)
    forms = []
    ok = True
    for N in (5, 6, 7, 8, 9):
        P = x + a * x**2 * y + b * x**2
        f, sup, err = cleared_certificate(P, N, (a, b))
        if f is None:
            ok = False
            print(f"  B N={N}: FAILED ({err})")
            continue
        pf = Poly(f, a, b)
        mono = pf.monoms()[0] if len(pf.monoms()) == 1 else None
        forms.append((N, mono))
        print(f"  B N={N}: pairing {factor(f)} (support {sup})")
    # The declared "same form" prediction is adjudicated in the verdict: measure the law.
    ok &= all(m is not None and m[1] == 0 for (_, m) in forms)
    law = all(m[0] == N for (N, m) in forms if m is not None)
    check("B: at EVERY window N = 5..9 the pairing is a nonzero monomial in a alone "
          "(all-parameter, all-b emptiness at each window); measured law: exponent = N",
          ok, f"exponent==window: {law}; forms {[(N, m) for (N, m) in forms]}")


def partC():
    print("=" * 76)
    print("Part C: the annihilation window criterion transfers to the family")
    print("=" * 76)
    P = x + a * x**2 * y + b * x**2
    ok_leib = True
    for k in (1, 2, 3):
        for (mi, mj) in ((1, 3), (0, 2), (2, 5)):
            m = x**mi * y**mj
            lhs = expand(jac2(m, P**k))
            rhs2 = expand(-k * jac2(P, expand(P ** (k - 1) * m)))
            if expand(lhs - rhs2) != 0:
                ok_leib = False
    check("C1: J(m, P^k) = -k L(P^{k-1} m) exactly on the family (P-agnostic Leibniz)",
          ok_leib)
    N = 8
    MQ, rows, M, rhs = build(P, N)
    cv = None
    for v_ in M.T.nullspace():
        den = lcm([cancel(e).as_numer_denom()[1] for e in v_])
        cc = [expand(cancel(e * den)) for e in v_]
        f = expand(sum(cc[r] * rhs[r, 0] for r in range(M.rows)))
        if f != 0:
            cv = cc
            break
    ok = cv is not None
    if ok:
        def pair(expr):
            if expr == 0:
                return 0
            pe = Poly(expand(expr), x, y)
            val = 0
            for idx, (mo, _) in enumerate(rows):
                co = pe.coeff_monomial(x ** mo[0] * y ** mo[1])
                if co:
                    val += cv[idx] * co
            return expand(val)
        for ((mi, mj), k) in (((1, 3), 1), ((0, 2), 2), ((1, 1), 2), ((0, 3), 3)):
            m = x**mi * y**mj
            src = expand(jac2(m, P**k))
            dpre = Poly(expand(P ** (k - 1) * m), x, y).total_degree()
            val = pair(src)
            inwin = dpre <= N
            agree = (val == 0) if inwin else True
            ok &= agree
            print(f"  C m=x^{mi}y^{mj}, k={k}: preimage degree {dpre} "
                  f"{'IN' if inwin else 'OUT'} window {N} -> pairing "
                  f"{'0' if val == 0 else 'nonzero'}")
    check("C2: in-window sources pair to ZERO (the annihilation criterion transfers "
          "verbatim: second Theorem 5 closure ingredient)", ok)


def partD():
    print("=" * 76)
    print("Part D: general above-weight tails")
    print("=" * 76)
    okw = True
    SAMPLES = [
        ("x + 2 x^2 y + 3 x^2 + 5 x^3", x + 2 * x**2 * y + 3 * x**2 + 5 * x**3),
        ("x + 2 x^2 y + 3 x^2 + 5 x^2 y^2 z?", None),
    ]
    ZOO = [
        ("x + 2 x^2y + 3 x^2 + 5 x^3", x + 2 * x**2 * y + 3 * x**2 + 5 * x**3),
        ("x + 2 x^2y + 3 x^2 + 5 x^3 y", x + 2 * x**2 * y + 3 * x**2
         + 5 * x**3 * y),
        ("x + 2 x^2y^2 + 3 x^2 + 5 x^2 y", x + 2 * x**2 * y**2 + 3 * x**2
         + 5 * x**2 * y),
        ("x + 2 x^2y + 3 x^2 + 5 x^4 y^2 + 7 x^3", x + 2 * x**2 * y + 3 * x**2
         + 5 * x**4 * y**2 + 7 * x**3),
    ]
    for (nm, P) in ZOO:
        MQ, rows, M, rhs = build(expand(P), 8)
        B = symbols(f"B0:{len(MQ)}")
        eqs = [sum(M[r, k] * B[k] for k in range(M.cols)) - rhs[r, 0]
               for r in range(M.rows)]
        cons = bool(linsolve(eqs, list(B)))
        okw &= not cons
        print(f"  D {nm}: {'EMPTY' if not cons else 'CONSISTENT (escalate!)'}")
    check("D1: multi-term above-weight tails: all sampled windows EMPTY", okw)
    P3 = x + a * x**2 * y + b * x**2 + c3 * x**3
    f, sup, err = cleared_certificate(P3, 7, (a, b, c3))
    ok3 = f is not None and len(Poly(f, a, b, c3).monoms()) == 1
    print(f"  D 3-parameter certificate: pairing {factor(f) if f is not None else err}")
    check("D2: the cleared certificate extends to the 3-parameter tail (monomial "
          "pairing: all-parameter emptiness)", ok3)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD}

if __name__ == "__main__":
    todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D"]
    for p_ in todo:
        PARTS[p_]()
        print()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
