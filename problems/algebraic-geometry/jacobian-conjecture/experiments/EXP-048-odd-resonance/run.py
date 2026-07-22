# EXP-048: the proper-power odd resonance mechanism.
# CPU-only, sympy. Run: run.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, gcd_list, lcm,  # noqa: E402
                   symbols)

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


def certificates(P, N):
    """All cleared left-null vectors + rows."""
    MQ, rows, M, rhs = build(P, N)
    out = []
    for cv in M.T.nullspace():
        den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
        cc = [expand(cancel(e * den)) for e in cv]
        g = gcd_list([e for e in cc if e != 0])
        if g not in (0, 1):
            cc = [cancel(e / g) for e in cc]
        f = expand(sum(cc[r] * rhs[r, 0] for r in range(M.rows)))
        out.append((cc, f))
    return out, rows, M


def vec_of(expr, rows):
    pe = Poly(expand(expr), x, y) if expand(expr) != 0 else None
    return Matrix([pe.coeff_monomial(x ** mo[0] * y ** mo[1]) if pe else 0
                   for (mo, _) in rows])


def main():
    print("=" * 76)
    print("EXP-048: the proper-power odd resonance at (2,2,2)")
    print("=" * 76)
    # 1: operator form
    ok1 = True
    Psym = x + a * (x * y) ** 2 + b * x**2
    for s in (3, 5, 7):
        lhs = expand(jac2(Psym, (x * y) ** s))
        pred = expand(s * x**s * y ** (s - 1) * (1 + 2 * b * x))
        ok1 &= expand(lhs - pred) == 0
    check("1: L((xy)^s) = s x^s y^{s-1} (1 + 2bx) identically", ok1)
    # 2: not an image (numeric a, b)
    Pnum = x + Rational(2) * (x * y) ** 2 + Rational(3) * x**2
    MQ, rows, M, rhs = build(Pnum, 9)
    v = vec_of(expand(jac2(Pnum, (x * y) ** 5)), rows)
    r0 = M.rank()
    r1 = M.row_join(v).rank()
    check("2: L((xy)^5) is NOT in the column space at N = 9 (the key identity cannot "
          "be the mechanism)", r1 > r0, f"rank {r0} -> {r1}")
    # 3: EXISTENCE of a pairing-nonzero, resonance-killing certificate (the declared
    # universal-kill prediction is adjudicated in the verdict; here we measure)
    for (s, N) in ((5, 9), (6, 11)):
        certs, rows, M = certificates(Psym, N)
        nz = [c for c in certs if c[1] != 0]
        dim = len(certs)
        src = expand(jac2(Psym, (x * y) ** s))
        vv = vec_of(src, rows)
        src_supp = set(Poly(expand(src), x, y).monoms())
        good = []
        for (cc, f) in nz:
            val = expand(sum(cc[i] * vv[i, 0] for i in range(len(rows))))
            supp = {rows[i][0] for i in range(len(rows)) if cc[i] != 0}
            good.append((val == 0, sorted(supp), f))
        kills = [g for g in good if g[0]]
        print(f"  3: N={N}, s={s}: left-null dim {dim}, pairing-nonzero {len(nz)}, "
              f"of which kill the resonance: {len(kills)}")
        check(f"3: a pairing-nonzero certificate EXISTS that kills L((xy)^{s}) at "
              f"N = {N}", len(kills) >= 1)
        for (k_, supp, f) in good:
            band = [i - j for (i, j) in supp]
            print(f"     cert kills={k_}: support {supp}")
            print(f"       row invariant i - j (class band): {sorted(set(band))}; "
                  f"source rows i - j: {sorted({i - j for (i, j) in src_supp})}")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
