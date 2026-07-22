# EXP-032: the full-edge theorem. CPU-only, sympy over QQ. Run: run.py [A|B|C|D|E]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, gcd, lcm,  # noqa: E402
                   linsolve, symbols, together)

failures = []
a, b, cs = symbols("a_ b_ c_")
z = symbols("z_")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def phi_poly(g, coeffs):
    return 1 + sum(c * z**(j + 1) for j, c in enumerate(coeffs[:g]))


def partA():
    print("=" * 76)
    print("Part A: the multiplication formula J(x phi(z), g_s) = [(ms+1) phi + k z phi'] e_s")
    print("=" * 76)
    okall = True
    C = symbols("C1:4")
    for k in (1, 2, 3):
        for m in (1, 2, 3):
            for g in (1, 2, 3):
                phi = phi_poly(g, C)
                zc = x**k * y**m
                E = expand(x * phi.subs(z, zc))
                for s in range(5):
                    gs = x ** (k * s) * y ** (m * s + 1)
                    lhs = expand(jac2(E, gs))
                    mult = expand(((m * s + 1) * phi + k * z * phi.diff(z)) * z**s)
                    rhs = expand(mult.subs(z, zc) * y)
                    # e_s * y ... e_t = z^t; the ray g carries one extra y: J lands on
                    # z-powers exactly (weight 0): rhs = mult(z)|_{z=x^k y^m}; compare:
                    rhs = expand(mult.subs(z, zc))
                    if expand(lhs - rhs) != 0:
                        okall = False
                        print(f"  A MISMATCH k={k} m={m} g={g} s={s}")
    check("A: multiplication formula exact for all k, m, g <= 3 (symbolic coefficients), "
          "s <= 4", okall)


def class_matrix(k, m, phi, D):
    """Matrix of f -> m z phi f' + (phi + k z phi') f on deg <= D, rows deg <= D + g."""
    g = Poly(phi, z).degree()
    rows = D + g + 1
    M = Matrix.zeros(rows, D + 1)
    for s in range(D + 1):
        img = expand(m * z * phi * (z**s).diff(z) + (phi + k * z * phi.diff(z)) * z**s)
        pp = Poly(img, z)
        for (e_,), co in zip(pp.monoms(), pp.coeffs()):
            M[e_, s] += co
    return M


def partB():
    print("=" * 76)
    print("Part B: the univariate kill (inconsistency over QQ(coeffs), top inverted)")
    print("=" * 76)
    C = symbols("C1:4")
    okall = True
    for (k, m, g) in ((1, 1, 1), (1, 1, 2), (2, 1, 2), (1, 2, 2), (2, 3, 3), (3, 2, 2)):
        phi = phi_poly(g, C)
        top = C[g - 1]
        for D in (4, 8):
            M = class_matrix(k, m, phi, D)
            rhs = Matrix([1] + [0] * (M.rows - 1))
            ns = M.T.nullspace()
            fs = []
            for cv in ns:
                den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
                cc = Matrix([expand(cancel(e * den)) for e in cv])
                f = expand((cc.T * rhs)[0, 0])
                if f != 0:
                    fs.append(f)
            if not fs:
                okall = False
                print(f"  B (k={k},m={m},g={g},D={D}): NO certificate")
                continue
            gg = fs[0]
            for f in fs[1:]:
                gg = gcd(gg, f)
            gg = factor(gg)
            p_ = Poly(expand(gg), *C[:g])
            mono = len(p_.monoms()) == 1 and all(
                mo == 0 for mo in p_.monoms()[0][: g - 1])
            okall &= mono
            print(f"  B (k={k},m={m},g={g},D={D}): pairing gcd = {gg} "
                  f"{'(pure top-coeff power OK)' if mono else '(NOT pure!)'}")
    check("B: every truncated class system is inconsistent; the certificate is a pure "
          "power of the TOP edge coefficient", okall)


def partC():
    print("=" * 76)
    print("Part C: full windows for binomial and trinomial edges (incl. perfect powers)")
    print("=" * 76)
    okall = True
    CASES = [
        ("binomial (a,b)=(1,1)", x + 1 * x**2 * y + 1 * x**3 * y**2, 10),
        ("binomial perfect square (b,a)=(2,1)", x + 2 * x**2 * y + 1 * x**3 * y**2, 10),
        ("binomial (a,b)=(-1/2,3)", x + 3 * x**2 * y - Rational(1, 2) * x**3 * y**2, 10),
        ("trinomial (b,c,a)=(1,1,1)", x + x**2 * y + x**3 * y**2 + x**4 * y**3, 9),
        ("trinomial perfect cube (3,3,1)", x + 3 * x**2 * y + 3 * x**3 * y**2 + x**4 * y**3, 9),
    ]
    for (nm, P, N) in CASES:
        MQ = [x**i * y**(dd - i) for dd in range(2, N + 1) for i in range(dd + 1)]
        B = symbols(f"B0:{len(MQ)}")
        Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
        eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
        incons = not linsolve(eqs, list(B))
        okall &= incons
        print(f"  C {nm} (window <= {N}): "
              f"{'INCONSISTENT' if incons else 'CONSISTENT (rescue?! escalate)'}")
    check("C: every same-edge window is empty, including perfect-power phi", okall)


def partD():
    print("=" * 76)
    print("Part D: certificate over QQ(a, b) for the binomial edge; kernel structure")
    print("=" * 76)
    P = x + b * x**2 * y + a * x**3 * y**2
    N = 8
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
        assert all(expand(vv) == 0 for vv in (cc.T * M)), "not left-null"
        f = expand((cc.T * rhs)[0, 0])
        if f != 0:
            fs.append(f)
    gg = None
    if fs:
        gg = fs[0]
        for f in fs[1:]:
            gg = gcd(gg, f)
        gg = factor(gg)
    print(f"  D certificate gcd (window <= {N}) = {gg}")
    p_ = Poly(expand(gg), a) if gg is not None else None
    ok = p_ is not None and Poly(expand(gg), a, b).monoms() and all(
        mo[1] == 0 for mo in Poly(expand(gg), a, b).monoms()) and len(
        Poly(expand(gg), a, b).monoms()) == 1
    check("D1: the pairing gcd vanishes ONLY where the top coefficient a = 0 (b-free pure "
          "a-power)", ok, f"gcd = {gg}")
    # kernels on classes j*v: for the edge E, expect ker = <E^j>. Weights here are
    # (v, 1-u) = (2, -2) (u = 3, v = 2): weight(x^i y^jj) = 2 i - 2 jj.
    okk = True
    E = P
    for j in (1, 2):
        deg = 5 * j + 5
        ray = [(i, jj) for i in range(deg + 1) for jj in range(deg + 1 - i)
               if 2 * i - 2 * jj == 2 * j and (i, jj) != (0, 0)]
        imgs = [expand(jac2(E, x**i * y**jj)) for (i, jj) in ray]
        outm = sorted({mo for im in imgs if im != 0 for mo in Poly(im, x, y).monoms()})
        MM = Matrix([[Poly(im, x, y).coeff_monomial(x**mi * y**mj) for im in imgs]
                     for (mi, mj) in outm])
        ker = MM.nullspace()
        ok1 = len(ker) == 1
        if ok1:
            Ej = Poly(expand(E**j), x, y)
            tgt = Matrix([Ej.coeff_monomial(x**i * y**jj) for (i, jj) in ray])
            r0 = next(idx for idx in range(len(ray)) if tgt[idx] != 0)
            sc = cancel(tgt[r0] / ker[0][r0]) if ker[0][r0] != 0 else None
            ok1 = sc is not None and all(
                expand(ker[0][idx] * sc - tgt[idx]) == 0 for idx in range(len(ray)))
        okk &= ok1
        print(f"  D kernel on class {2*j}: dim {len(ker)}; equals E^{j}: {ok1}")
    check("D2: kernels are exactly the powers of the FULL edge E", okk)


def partE():
    print("=" * 76)
    print("Part E: tails on the full edge; the quasi-triangular control")
    print("=" * 76)
    okall = True
    for (nm, P, N) in (
            ("edge + tail y^2", x + x**2 * y + x**3 * y**2 + 2 * y**2, 10),
            ("edge + tails xy^2, y^3", x + 2 * x**2 * y + x**3 * y**2
             + x * y**2 - y**3, 10)):
        MQ = [x**i * y**(dd - i) for dd in range(2, N + 1) for i in range(dd + 1)]
        B = symbols(f"B0:{len(MQ)}")
        Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
        eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
        incons = not linsolve(eqs, list(B))
        okall &= incons
        print(f"  E {nm}: {'INCONSISTENT' if incons else 'CONSISTENT (escalate)'}")
    Pc = x + (x + y) ** 2
    N = 6
    MQ = [x**i * y**(dd - i) for dd in range(2, N + 1) for i in range(dd + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(Pc, Q0) - 1), x, y).coeffs() if e != 0]
    cons = bool(linsolve(eqs, list(B)))
    okall &= cons
    print(f"  E control x + (x+y)^2: {'CONSISTENT (as it must be)' if cons else 'FAIL'}")
    check("E: tails never rescue the full edge; the quasi-triangular control stays "
          "consistent", okall)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD, "E": partE}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D", "E"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
