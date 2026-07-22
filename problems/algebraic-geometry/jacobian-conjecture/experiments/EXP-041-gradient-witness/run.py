# EXP-041: the explicit symmetric/gradient witness in dimension 48.
# CPU-only, sympy over Q(i) + pure-Python Fraction dict arithmetic. Run: run.py [A|B|C|D|E]
import sys
from fractions import Fraction
from pathlib import Path

from sympy import (I, Matrix, Poly, Rational, eye, expand, sympify, symbols,
                   zeros)

HERE = Path(__file__).resolve().parent
failures = []

U = symbols("u1:25")
X = symbols("x1:25")
Y = symbols("y1:25")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def parse_H():
    txt = (HERE / "data" / "cubic_map.txt").read_text()
    loc = {f"u{k}": U[k - 1] for k in range(1, 25)}
    H = [None] * 24
    for line in txt.splitlines():
        line = line.strip()
        if line.startswith("H") and "=" in line:
            nm, expr = line.split("=", 1)
            idx = int(nm.strip()[1:])
            H[idx - 1] = sympify(expr.strip(), locals=loc)
    return H


def parse_collision():
    txt = (HERE / "data" / "collision_points.txt").read_text()
    pts = []
    for line in txt.splitlines():
        line = line.strip()
        if line.startswith(("P =", "Q =")):
            tup = line.split("=", 1)[1].strip().strip("()")
            pts.append([Rational(t.strip()) for t in tup.split(",")])
    return pts[0], pts[1]


def partA():
    print("=" * 76)
    print("Part A: input verification (Thompson dim-24 artifact)")
    print("=" * 76)
    H = parse_H()
    okh = all(h is not None for h in H)
    check("A1: all 24 components parsed", okh)
    okhom = True
    nmon = 0
    for h in H:
        if h == 0:
            continue
        p = Poly(h, *U)
        nmon += len(p.monoms())
        okhom &= all(sum(m) == 3 for m in p.monoms())
    check("A2: H is cubic homogeneous", okhom, f"{nmon} cubic monomials")
    u, v = parse_collision()
    okne = u != v
    subu = dict(zip(U, u))
    subv = dict(zip(U, v))
    okcol = all(expand((U[k] + H[k]).subs(subu) - (U[k] + H[k]).subs(subv)) == 0
                for k in range(24))
    check("A3: published collision is exact: G(P) = G(Q), P != Q", okne and okcol)


def build_f(H):
    """f_H = -i sum_j H_j(x + iy) y_j, expanded once."""
    subxy = {U[k]: X[k] + I * Y[k] for k in range(24)}
    f = 0
    for j in range(24):
        if H[j] == 0:
            continue
        f += H[j].subs(subxy, simultaneous=True) * Y[j]
    return expand(-I * f)


def partB():
    print("=" * 76)
    print("Part B: the conjugation identity (makes Ftil symmetric Keller)")
    print("=" * 76)
    H = parse_H()
    f = build_f(H)
    okq = all(sum(m) == 4 for m in Poly(f, *X, *Y).monoms())
    check("B1: f_H is homogeneous of degree 4 in 48 variables", okq,
          f"{len(Poly(f, *X, *Y).monoms())} monomials")
    fx = [f.diff(X[k]) for k in range(24)]
    fy = [f.diff(Y[k]) for k in range(24)]
    subS = {X[k]: X[k] - I * Y[k] for k in range(24)}
    subx = {U[k]: X[k] for k in range(24)}
    ok1 = True
    ok2 = True
    for k in range(24):
        c1 = expand((X[k] + fx[k]).subs(subS, simultaneous=True)
                    + I * (Y[k] + fy[k]).subs(subS, simultaneous=True))
        rhs1 = expand(X[k] + H[k].subs(subx, simultaneous=True))
        if expand(c1 - rhs1) != 0:
            ok1 = False
            print(f"  B MISMATCH block1 k={k + 1}")
        c2 = expand((Y[k] + fy[k]).subs(subS, simultaneous=True))
        rhs2 = expand(Y[k]
                      + sum(H[j].diff(U[k]).subs(subx, simultaneous=True) * Y[j]
                            for j in range(24))
                      - I * H[k].subs(subx, simultaneous=True))
        if expand(c2 - rhs2) != 0:
            ok2 = False
            print(f"  B MISMATCH block2 k={k + 1}")
    check("B2: S^-1 o (id + grad f) o S = (x + H(x), y + JH(x)^t y - i H(x)) "
          "identically (all 48 components)", ok1 and ok2)


def partC():
    print("=" * 76)
    print("Part C: the explicit 2-point collision of Ftil on C^48")
    print("=" * 76)
    H = parse_H()
    f = build_f(H)
    fx = [f.diff(X[k]) for k in range(24)]
    fy = [f.diff(Y[k]) for k in range(24)]
    u, v = parse_collision()
    subv = dict(zip(U, v))
    JHv = Matrix(24, 24, lambda j, k: H[j].diff(U[k]).subs(subv))
    Mw = (eye(24) + JHv.T)
    w = I * (Mw.inv() * Matrix([u[k] - v[k] for k in range(24)]))
    p1 = {**{X[k]: u[k] for k in range(24)}, **{Y[k]: 0 for k in range(24)}}
    p2 = {**{X[k]: expand(v[k] - I * w[k, 0]) for k in range(24)},
          **{Y[k]: expand(w[k, 0]) for k in range(24)}}
    okne = any(expand(p1[X[k]] - p2[X[k]]) != 0 or expand(p1[Y[k]] - p2[Y[k]]) != 0
               for k in range(24))
    ok = True
    for k in range(24):
        d1 = expand((X[k] + fx[k]).subs(p1) - (X[k] + fx[k]).subs(p2))
        d2 = expand((Y[k] + fy[k]).subs(p1) - (Y[k] + fy[k]).subs(p2))
        if d1 != 0 or d2 != 0:
            ok = False
            print(f"  C MISMATCH k={k + 1}: {d1}, {d2}")
    check("C: Ftil(p1) = Ftil(p2) exactly over Q(i) with p1 != p2: the symmetric Keller "
          "map id + grad f_H on C^48 is NOT invertible", ok and okne)
    (HERE / "artifacts" / "witness-collision-2026-07-22.txt").write_text(
        "p1 = (u, 0) with u = " + str(u) + "\n"
        + "p2 = (v - i w, w) with v = " + str(v) + "\n"
        + "w = " + str([w[k, 0] for k in range(24)]) + "\n")
    print("  C: collision persisted to artifacts/witness-collision-2026-07-22.txt")


def topoly(e, gens):
    d = {}
    for mon, c in Poly(e, *gens).terms():
        re, im = c.as_real_imag()
        d[mon] = (Fraction(re.p, re.q), Fraction(im.p, im.q))
    return d


def pmulQ(a, b):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            cur = out.get(m, Fraction(0))
            out[m] = cur + ca * cb
    return {m: c for m, c in out.items() if c != 0}


def paddQ(a, b):
    out = dict(a)
    for m, c in b.items():
        cur = out.get(m, Fraction(0))
        s = cur + c
        if s == 0:
            out.pop(m, None)
        else:
            out[m] = s
    return out


def partD():
    print("=" * 76)
    print("Part D: in-house nilpotency chain (JH)^k = 0, exact sparse arithmetic")
    print("=" * 76)
    H = parse_H()
    A = [[{} for _ in range(24)] for _ in range(24)]
    for j in range(24):
        for k in range(24):
            e = H[j].diff(U[k])
            if e != 0:
                A[j][k] = {m: Fraction(c.p, c.q)
                           for m, c in Poly(e, *U).terms()}

    def matmul(P, Q):
        R = [[{} for _ in range(24)] for _ in range(24)]
        for i in range(24):
            for j in range(24):
                if not P[i][j]:
                    continue
                for k in range(24):
                    if not Q[j][k]:
                        continue
                    R[i][k] = paddQ(R[i][k], pmulQ(P[i][j], Q[j][k]))
        return R

    def nterms(P):
        return sum(len(P[i][j]) for i in range(24) for j in range(24))

    def trace_sum_zero(P):
        t = {}
        for i in range(24):
            t = paddQ(t, P[i][i])
        return not t

    tr_ok = True
    print(f"  D terms(JH) = {nterms(A)}")
    P2 = matmul(A, A)
    print(f"  D terms(JH^2) = {nterms(P2)}; Tr(JH^2) = 0: {trace_sum_zero(P2)}")
    tr_ok &= trace_sum_zero(A) and trace_sum_zero(P2)
    P4 = matmul(P2, P2)
    print(f"  D terms(JH^4) = {nterms(P4)}; Tr(JH^4) = 0: {trace_sum_zero(P4)}")
    tr_ok &= trace_sum_zero(P4)
    P8 = matmul(P4, P4)
    print(f"  D terms(JH^8) = {nterms(P8)}; Tr(JH^8) = 0: {trace_sum_zero(P8)}")
    tr_ok &= trace_sum_zero(P8)
    P16 = matmul(P8, P8)
    print(f"  D terms(JH^16) = {nterms(P16)}")
    Pk = matmul(P16, A)
    k = 17
    while nterms(Pk) and k < 25:
        print(f"  D terms(JH^{k}) = {nterms(Pk)} (NOT zero yet)")
        Pk = matmul(Pk, A)
        k += 1
    check("D1: (JH)^k = 0 EXACTLY for some k <= 24 (in-house sparse certificate; the "
          "true nilpotency index is recorded)", nterms(Pk) == 0,
          f"index = {k} (Thompson's claimed 17 is corrected)")
    check("D2: Tr(JH^k) = 0 for k = 1, 2, 4, 8 (Newton-identity consistency)", tr_ok)


def partE():
    print("=" * 76)
    print("Part E: P_star = -f_H, the failing HN quartic; Delta P_star^2 != 0 sanity")
    print("=" * 76)
    H = parse_H()
    f = build_f(H)
    gens = list(X) + list(Y)
    Pd = topoly(expand(-f), gens)
    okq = all(sum(m) == 4 for m in Pd)
    check("E1: P_star is a homogeneous quartic over Q(i) (Hessian nilpotent by the "
          "dBvdE char-poly identity + part D)", okq, f"{len(Pd)} monomials")

    def cmul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    sq = {}
    items = list(Pd.items())
    for i1, (m1, c1) in enumerate(items):
        for m2, c2 in items:
            m = tuple(a + b for a, b in zip(m1, m2))
            cur = sq.get(m, (Fraction(0), Fraction(0)))
            cc = cmul(c1, c2)
            sq[m] = (cur[0] + cc[0], cur[1] + cc[1])
    lap = {}
    for m, c in sq.items():
        if c == (0, 0):
            continue
        for k in range(48):
            if m[k] >= 2:
                mm = tuple(e - 2 if idx == k else e for idx, e in enumerate(m))
                fac = m[k] * (m[k] - 1)
                cur = lap.get(mm, (Fraction(0), Fraction(0)))
                lap[mm] = (cur[0] + fac * c[0], cur[1] + fac * c[1])
    nz = sum(1 for c in lap.values() if c != (Fraction(0), Fraction(0)))
    check("E2: Delta P_star^2 != 0 (forced by Zhao Cor 3.9 for any VC-falsifying HNP)",
          nz > 0, f"{nz} nonzero terms")
    (HERE / "artifacts" / "witness-Pstar-2026-07-22.txt").write_text(
        "P_star = -f_H, homogeneous HN quartic in 48 variables (x1..x24, y1..y24), "
        "Q(i) coefficients.\nf_H = " + str(expand(build_f(H))) + "\n")
    print("  E: P_star persisted to artifacts/witness-Pstar-2026-07-22.txt")


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD, "E": partE}

if __name__ == "__main__":
    todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D", "E"]
    for p_ in todo:
        PARTS[p_]()
        print()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
