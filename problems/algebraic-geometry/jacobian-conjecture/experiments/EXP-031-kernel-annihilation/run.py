# EXP-031: kernel identification, the annihilation lemma, danger certificates.
# CPU-only, sympy over QQ. Run: run.py [A|B|C]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, cancel, expand, factor, gcd, lcm, linsolve,  # noqa: E402
                   symbols)

failures = []
a, b, c = symbols("a_ b_ c_")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def wt(u, v, i, j):
    return v * i + (1 - u) * j


def class_ray(u, v, sigma, degmax):
    return sorted((i, j) for i in range(degmax + 1) for j in range(degmax + 1 - i)
                  if wt(u, v, i, j) == sigma and (i, j) != (0, 0))


def partA():
    print("=" * 76)
    print("Part A: kernels on classes kv are exactly the powers of P_top")
    print("=" * 76)
    okall = True
    for (u, v) in ((2, 2), (3, 2), (4, 6)):
        P0 = x + a * x**u * y**v
        for k in (1, 2, 3):
            degmax = k * (u + v) + u + v
            ray = class_ray(u, v, k * v, degmax)
            imgs = [expand(jac2(P0, x**i * y**j)) for (i, j) in ray]
            outm = sorted({mo for im in imgs if im != 0
                           for mo in Poly(im, x, y).monoms()})
            M = Matrix([[Poly(im, x, y).coeff_monomial(x**mi * y**mj) for im in imgs]
                        for (mi, mj) in outm])
            ker = M.nullspace()
            ok = len(ker) == 1
            if ok:
                kv = ker[0]
                Pk = Poly(expand((x + a * x**u * y**v) ** k), x, y)
                target = Matrix([Pk.coeff_monomial(x**i * y**j) for (i, j) in ray])
                r0 = next(idx for idx in range(len(ray)) if target[idx] != 0)
                scale = cancel(target[r0] / kv[r0]) if kv[r0] != 0 else None
                ok = scale is not None and all(
                    expand(kv[idx] * scale - target[idx]) == 0 for idx in range(len(ray)))
            okall &= ok
            print(f"  A (u={u},v={v}) class {k}*v: kernel dim {len(ker)}; equals "
                  f"P_top^{k}: {ok}")
    check("A: every kv-class kernel is 1-dimensional and equals P_top^k exactly", okall)


def pure_certificate(u, v, N):
    """Left-null vector (rows indexed by equation monomials) of the pure system."""
    MQ = [x**i * y**(dd - i) for dd in range(2, N + 1) for i in range(dd + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
    Jm1 = Poly(expand(jac2(x + a * x**u * y**v, Q0) - 1), x, y)
    rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs()) if e != 0]
    eqs = [e for _, e in rows]
    M = Matrix([[expand(e.diff(bb)) for bb in B] for e in eqs])
    rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for e in eqs])
    ns = M.T.nullspace()
    for cvec in ns:
        den = lcm([cancel(e).as_numer_denom()[1] for e in cvec])
        cc = [expand(cancel(e * den)) for e in cvec]
        f = expand(sum(ci * rhs[i, 0] for i, ci in enumerate(cc)))
        if f != 0:
            return rows, cc, f
    return rows, None, None


def partB():
    print("=" * 76)
    print("Part B: the annihilation lemma (adequate windows; truncation artifact recorded)")
    print("=" * 76)
    # First run used windows 6/10 for every source: sources whose support EXCEEDS the
    # window paired nonzero (truncation artifact, recorded in the artifact file); the lemma
    # concerns the full functional, so each source needs window >= deg J(m, P_top^k).
    u = v = 2
    okall = True
    DANGERS = (((1, 3), 1), ((2, 5), 1), ((0, 3), 2), ((1, 5), 2), ((0, 5), 3))
    cert = {}
    for N in (10, 16):
        cert[N] = pure_certificate(u, v, N)
        print(f"  B window {N}: pure pairing {factor(cert[N][2])}")
    for (m_, k) in DANGERS:
        mi, mj = m_
        lam = wt(u, v, mi, mj)
        assert lam == v + 1 - u - k * v, (m_, k, lam)
        src = expand(jac2(x**mi * y**mj, (x + a * x**u * y**v) ** k))
        sdeg = Poly(src, x, y).total_degree() if src != 0 else 0
        N = 10 if sdeg <= 10 else 16
        rows, cc, _ = cert[N]
        sp = Poly(src, x, y) if src != 0 else None
        val = 0
        if sp is not None:
            for idx, (mo, _) in enumerate(rows):
                coef = sp.coeff_monomial(x ** mo[0] * y ** mo[1])
                if coef:
                    val += cc[idx] * coef
        val = expand(val)
        ok = val == 0
        okall &= ok
        print(f"    danger m = x^{mi} y^{mj} (k = {k}, source deg {sdeg}, window {N}): "
              f"pairing = {val} {'OK' if ok else 'NONZERO!'}")
    # the reduction identity: J(m, P_top^k) = -k P_top^(k-1) J(P_top, m): the general lemma
    # reduces to k = 1 plus multiplicativity.
    idok = True
    P0 = x + a * x**u * y**v
    for (m_, k) in DANGERS:
        mi, mj = m_
        lhs = expand(jac2(x**mi * y**mj, P0**k))
        rhs = expand(-k * P0 ** (k - 1) * jac2(P0, x**mi * y**mj))
        idok &= expand(lhs - rhs) == 0
    check("B1: with ADEQUATE windows the functional annihilates every danger source",
          okall)
    check("B2: the reduction identity J(m, P_top^k) = -k P_top^(k-1) J(P_top, m) holds "
          "exactly (general lemma reduces to k = 1)", idok)


def pairing_gcd(P, N, gens):
    MQ = [x**i * y**(dd - i) for dd in range(2, N + 1) for i in range(dd + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    M = Matrix([[expand(e.diff(bb)) for bb in B] for e in eqs])
    rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for e in eqs])
    ns = M.T.nullspace()
    fs = []
    for cvec in ns:
        den = lcm([cancel(e).as_numer_denom()[1] for e in cvec])
        ccv = Matrix([expand(cancel(e * den)) for e in cvec])
        assert all(expand(vv) == 0 for vv in (ccv.T * M)), "not left-null"
        f = expand((ccv.T * rhs)[0, 0])
        if f != 0:
            fs.append(f)
    if not fs:
        return None
    g = fs[0]
    for f in fs[1:]:
        g = gcd(g, f)
    return factor(g)


def partC():
    print("=" * 76)
    print("Part C: danger-tail certificates over QQ(a, b[, c])")
    print("=" * 76)
    okall = True
    for (mi, mj) in ((1, 3), (0, 3)):
        g = pairing_gcd(x + a * (x * y) ** 2 + b * x**mi * y**mj, 10, (a, b))
        p_ = Poly(expand(g), a, b) if g is not None else None
        ok = p_ is not None and len(p_.monoms()) == 1 and p_.monoms()[0][1] == 0
        okall &= ok
        print(f"  C tail b x^{mi} y^{mj} (window <= 10): gcd = {g} "
              f"{'(b-free OK)' if ok else '(LEAKS b!)'}")
    g = pairing_gcd(x + a * (x * y) ** 2 + b * x * y**3 + c * y**3, 10, (a, b, c))
    p_ = Poly(expand(g), a, b, c) if g is not None else None
    ok = (p_ is not None and len(p_.monoms()) == 1
          and p_.monoms()[0][1] == 0 and p_.monoms()[0][2] == 0)
    okall &= ok
    print(f"  C combined danger tail (window <= 10): gcd = {g} "
          f"{'(b, c-free OK)' if ok else '(LEAKS!)'}")
    check("C: danger-tail pairing gcds are pure a-powers (b, c-free): the danger sources "
          "cannot rescue", okall)


PARTS = {"A": partA, "B": partB, "C": partC}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
