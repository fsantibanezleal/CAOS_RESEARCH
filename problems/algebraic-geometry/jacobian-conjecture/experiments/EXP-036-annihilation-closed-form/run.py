# EXP-036: the annihilation lemma in closed form (sources live in the image).
# CPU-only, sympy over QQ. Run: run.py [A|B|C|D]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, cancel, expand, factor, lcm, symbols)  # noqa: E402

failures = []
a = symbols("a_")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def mons(dmin, dmax):
    return [x**i * y**(d - i) for d in range(dmin, dmax + 1) for i in range(d + 1)]


def partA():
    print("=" * 76)
    print("Part A: the Leibniz identity J(f, f^{k-1} g) = f^{k-1} J(f, g)")
    print("=" * 76)
    F = symbols("F0:6")
    G = symbols("G0:6")
    f = (F[0] + F[1] * x + F[2] * y + F[3] * x * y + F[4] * x**2 + F[5] * y**2)
    g = (G[0] + G[1] * x + G[2] * y + G[3] * x * y + G[4] * x**2 + G[5] * y**2)
    ok = True
    for k in (1, 2, 3, 4):
        lhs = expand(jac2(f, expand(f ** (k - 1) * g)))
        rhs = expand(f ** (k - 1) * jac2(f, g))
        if expand(lhs - rhs) != 0:
            ok = False
            print(f"  A MISMATCH at k = {k}")
    check("A: identity exact for generic symbolic f, g and k <= 4 (J(f, f) = 0 route)", ok)


def partB():
    print("=" * 76)
    print("Part B: the sources are images of the FULL operator L = J(P, .)")
    print("=" * 76)
    # CORRECTION (first run refuted the P_top version): the sources that enter the
    # constant's equation are J(m, P^k) built from the FULL P, so the preimage is
    # w = P^{k-1} m and the image is under L = J(P, .), not L_top.
    ok = True
    for (u, v) in ((2, 2), (3, 2), (4, 6)):
        P = x + a * x**u * y**v
        for k in (1, 2, 3):
            for (mi, mj) in ((1, 3), (0, 2), (2, 5), (0, 3), (1, 1)):
                m = x**mi * y**mj
                src = expand(jac2(m, P**k))
                pre = expand(P ** (k - 1) * m)
                img = expand(-k * jac2(P, pre))
                if expand(img - src) != 0:
                    ok = False
                    print(f"  B MISMATCH u={u} v={v} k={k} m=x^{mi}y^{mj}")
    check("B: J(m, P^k) = -k L(P^{k-1} m) exactly (grid (u,v), k <= 3, 5 monomials): "
          "every source IS an image of L, with explicit preimage P^{k-1} m", ok)


def certificate(u, v, N):
    """(rows, covector, pairing) for the pure system P = x + a x^u y^v at window N."""
    MQ = mons(2, N)
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * mm for bb, mm in zip(B, MQ))
    Jm1 = Poly(expand(jac2(x + a * x**u * y**v, Q0) - 1), x, y)
    rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs()) if e != 0]
    eqs = [e for _, e in rows]
    M = Matrix([[expand(e.diff(bb)) for bb in B] for e in eqs])
    rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for e in eqs])
    for cv in M.T.nullspace():
        den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
        cc = [expand(cancel(e * den)) for e in cv]
        f = expand(sum(ci * rhs[i, 0] for i, ci in enumerate(cc)))
        if f != 0:
            return rows, cc, f, M, MQ
    return rows, None, None, None, MQ


def pair(rows, cc, expr):
    if expr == 0:
        return 0
    pe = Poly(expand(expr), x, y)
    val = 0
    for idx, (mo, _) in enumerate(rows):
        co = pe.coeff_monomial(x ** mo[0] * y ** mo[1])
        if co:
            val += cc[idx] * co
    return expand(val)


def partC():
    print("=" * 76)
    print("Part C: the window criterion (and EXP-031's artifact fully explained)")
    print("=" * 76)
    u = v = 2
    P = x + a * x**u * y**v
    DANGERS = (((1, 3), 1), ((2, 5), 1), ((0, 3), 2), ((1, 5), 2), ((0, 5), 3))
    ok = True
    for N in (6, 10, 16):
        rows, cc, f, _, _ = certificate(u, v, N)
        if cc is None:
            print(f"  C window {N}: no certificate")
            ok = False
            continue
        line = []
        for ((mi, mj), k) in DANGERS:
            m = x**mi * y**mj
            src = expand(jac2(m, P**k))
            pre = expand(P ** (k - 1) * m)
            dpre = Poly(pre, x, y).total_degree()
            val = pair(rows, cc, src)
            inwin = dpre <= N
            agree = (val == 0) if inwin else True
            ok &= agree
            line.append(f"m=x^{mi}y^{mj},k={k}: pre-deg {dpre} "
                        f"{'IN' if inwin else 'OUT'} -> pairing "
                        f"{'0' if val == 0 else str(val)}")
        print(f"  C window {N} (pairing {factor(f)}):")
        for ln in line:
            print(f"    {ln}")
    check("C: whenever the preimage fits the window, the pairing VANISHES; the earlier "
          "nonzeros were exactly the out-of-window preimages (artifact explained)", ok)


def partD():
    print("=" * 76)
    print("Part D: image membership in matrix form (rank test)")
    print("=" * 76)
    u = v = 2
    N = 10
    P = x + a * x**u * y**v
    rows, cc, _, M, MQ = certificate(u, v, N)
    if M is None:
        check("D: certificate available", False)
        return
    Mn = M.subs(a, 2)
    r0 = Mn.rank()
    ok = True
    for ((mi, mj), k) in (((1, 3), 1), ((0, 3), 2), ((2, 5), 1)):
        m = x**mi * y**mj
        src = expand(jac2(m, P**k).subs(a, 2))
        pe = Poly(src, x, y) if src != 0 else None
        vec = Matrix([pe.coeff_monomial(x ** mo[0] * y ** mo[1]) if pe else 0
                      for (mo, _) in rows])
        aug = Mn.row_join(vec)
        okk = aug.rank() == r0
        ok &= okk
        pred = Poly(expand(P ** (k - 1) * m), x, y).total_degree() <= N
        print(f"  D m=x^{mi}y^{mj}, k={k}: rank(M)={r0}, rank([M|S])={aug.rank()} "
              f"{'(in image)' if okk else '(NOT in image)'}; preimage in window: {pred}")
    check("D: each source vector lies in the column space of M (image membership, the "
          "matrix form of the closed-form lemma)", ok)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
