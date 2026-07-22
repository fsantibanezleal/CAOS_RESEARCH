# EXP-046: the Tower Lemma proof attempt.
# CPU-only, sympy. Run: run.py [A|B|C|D]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, gcd_list,  # noqa: E402
                   lcm, linsolve, symbols)

failures = []
a, b = symbols("a b")


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


def cleared_certificate(P, N):
    MQ, rows, M, rhs = build(P, N)
    for cv in M.T.nullspace():
        den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
        cc = [expand(cancel(e * den)) for e in cv]
        g = gcd_list([e for e in cc if e != 0])
        if g not in (0, 1):
            cc = [cancel(e / g) for e in cc]
        f = expand(sum(cc[r] * rhs[r, 0] for r in range(M.rows)))
        if f != 0:
            return f, cc, rows, M, MQ
    return None, None, None, None, None


def vec_of(expr, rows):
    pe = Poly(expand(expr), x, y) if expand(expr) != 0 else None
    return Matrix([pe.coeff_monomial(x ** mo[0] * y ** mo[1]) if pe else 0
                   for (mo, _) in rows])


def partA():
    print("=" * 76)
    print("Part A: bookkeeping, the top block, and its kernel")
    print("=" * 76)
    P = x + Rational(2) * x**2 * y + Rational(3) * x**2
    N = 8
    MQ, rows, M, rhs = build(P, N)
    MQ1, rows1, M1, rhs1 = build(P, N + 1)
    old_cols = {m: i for i, m in enumerate(MQ)}
    newrows = [r for r, (mo, _) in enumerate(rows1)
               if mo[0] + mo[1] == N + Poly(P, x, y).total_degree() - 1]
    ok0 = all(M1[r, old_cols[m]] == 0 for r in newrows for m in MQ
              if m in old_cols)
    check("A1: the old-column block over the NEW rows is zero (degree bookkeeping)", ok0,
          f"{len(newrows)} new rows")
    T = Rational(2) * x**2 * y
    ok1 = True
    for mnew in [m for m in MQ1 if m[0] + m[1] == N + 1]:
        full = expand(jac2(P, x**mnew[0] * y**mnew[1]))
        top = expand(jac2(T, x**mnew[0] * y**mnew[1]))
        dd = Poly(expand(full - top), x, y) if expand(full - top) != 0 else None
        if dd is not None and dd.total_degree() >= N + 2:
            ok1 = False
    check("A2: the new-block action is exactly J(T, .) with T the total-degree top form "
          "(lower parts land in old rows)", ok1)
    kers = []
    for mnew in [m for m in MQ1 if m[0] + m[1] == N + 1]:
        if expand(jac2(T, x**mnew[0] * y**mnew[1])) == 0:
            kers.append(mnew)
    ok2 = kers == [(6, 3)]
    check("A3: ker(D) at degree 9 is exactly the B-power (x^2 y)^3 (one resonance)", ok2,
          f"{kers}")


def partB():
    print("=" * 76)
    print("Part B: the key identity (resonances reduce in-window mod ker L)")
    print("=" * 76)
    CASES = [
        ("d < u+v: (2,1,2), kappa = B^3, N = 8",
         x + a * x**2 * y + b * x**2, (x**2 * y) ** 3, a ** (-3),
         (x + b * x**2), 8),
        ("d < u+v: (2,1,2), kappa = B^4, N = 11",
         x + a * x**2 * y + b * x**2, (x**2 * y) ** 4, a ** (-4),
         (x + b * x**2), 11),
        ("d = u+v: (2,1,3), kappa = T^3, N = 8",
         x + a * x**2 * y + b * x**3, (a * x**2 * y + b * x**3) ** 3, 1, x, 8),
    ]
    ok = True
    for (nm, P, kap, lam, low, N) in CASES:
        k = 3 if "^3" in nm else 4
        red = expand(kap - lam * (P - low) ** 0)  # placeholder replaced below
        red = expand(kap - lam * ((P - low) ** k) + lam * ((P - low) ** k)
                     - lam * P ** k)
        # kappa = lam (P - low)^k identically; kappa - lam P^k = lam[(P-low)^k - P^k]
        ident = expand(kap - lam * (P - low) ** k) == 0
        rem = expand(lam * ((P - low) ** k - P ** k))
        din = Poly(rem, x, y).total_degree() if rem != 0 else 0
        okc = ident and din <= N
        ok &= okc
        print(f"  B {nm}: kappa = lam (P - low)^k {ident}; deg(kappa - lam P^k) = {din} "
              f"<= N = {N}: {okc}")
    check("B1: each resonance kappa equals lam (P - low)^k with kappa - lam P^k "
          "supported in-window", ok)
    # rank test: L(kappa) lies in the old-column space (numeric a, b)
    P = x + Rational(2) * x**2 * y + Rational(3) * x**2
    N = 8
    MQ, rows, M, rhs = build(P, N)
    kap = expand(((x**2 * y)) ** 3)
    src = expand(jac2(P, kap))
    v = vec_of(src, rows)
    r0 = M.rank()
    okr = M.row_join(v).rank() == r0
    check("B2: rank test: L(kappa) is in the old-column space at (2,1,2), N = 8 "
          "(every certificate annihilates it)", okr, f"rank {r0}")


def partC():
    print("=" * 76)
    print("Part C: end-to-end extension across the active resonance (8 -> 9)")
    print("=" * 76)
    P = x + Rational(2) * x**2 * y + Rational(3) * x**2
    f8, c8, rows8, M8, MQ8 = cleared_certificate(P, 8)
    f9, c9, rows9, M9, MQ9 = cleared_certificate(P, 9)
    ok = f8 is not None and f9 is not None
    if ok:
        pos8 = {rows8[i][0]: c8[i] for i in range(len(rows8))}
        pos9 = {rows9[i][0]: c9[i] for i in range(len(rows9))}
        common = [mo for mo in pos8 if mo in pos9]
        ratios = {cancel(pos9[mo] / pos8[mo]) for mo in common
                  if pos8[mo] != 0 and pos9[mo] != 0}
        zero8 = [mo for mo in pos8 if pos8[mo] != 0 and pos9.get(mo, 0) == 0]
        ok &= len(ratios) == 1 and not zero8
        print(f"  C common rows {len(common)}, ratio(s) {ratios}, "
              f"dropped rows {len(zero8)}")
        rp = cancel(f9 / f8)
        print(f"  C pairing ratio f9/f8 = {rp}")
        ok &= rp != 0
    check("C: the certificate extends across the ACTIVE resonance 8 -> 9 with one "
          "ratio and nonzero pairing (the Tower Lemma's step, realized)", ok)


def partD():
    print("=" * 76)
    print("Part D: the proper-power case (2,2,2): odd resonances")
    print("=" * 76)
    P = x + Rational(2) * (x * y) ** 2 + Rational(3) * x**2
    ok = True
    for N in (9, 11):
        f, cc, rows, M, MQ = cleared_certificate(P, N)
        if f is None:
            ok = False
            continue
        # odd resonance at degree N+1: (xy)^s with 2s = N+1 impossible for even N+1;
        # kernel forms of J(T, .) with T = 2(xy)^2: all (xy)^s of degree 2s = N+1
        s2 = N + 1
        if s2 % 2 == 1:
            print(f"  D N={N}: degree {N + 1} odd: no (xy)^s resonance at all")
            continue
        s = s2 // 2
        kap = expand((x * y) ** s)
        src = expand(jac2(P, kap))
        v = vec_of(src, rows)
        val = expand(sum(cc[i] * v[i, 0] for i in range(len(rows))))
        parity = "EVEN (reduces mod C[P])" if s % 2 == 0 else "ODD (needs its own kill)"
        print(f"  D N={N}: resonance (xy)^{s} [{parity}]: certificate pairing "
              f"{'0' if val == 0 else val}")
        ok &= (val == 0)
    check("D: at (2,2,2) every tested resonance (even AND odd powers of xy) pairs to "
          "ZERO: the tower persists in the proper-power case too (mechanism recorded "
          "for the odd case as measured, not yet derived)", ok)


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
