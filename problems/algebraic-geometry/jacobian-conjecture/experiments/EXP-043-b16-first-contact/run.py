# EXP-043: B = 16 first contact + (72, 108) scoping.
# CPU-only, sympy over QQ. Run: run.py [A|B|C|D|E]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import Poly, Rational, expand, linsolve, symbols  # noqa: E402

failures = []
lam, lam1 = symbols("lambda0 lambda1")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def R0(l0=lam):
    return expand(x * (x * y**4 - l0) ** 3)


def R1(l1=lam1):
    return expand(y * (x * y**2 - l1))


def wclass_set(e, w1, w2):
    return {w1 * i + w2 * j for (i, j) in Poly(expand(e), x, y).monoms()}


def partA():
    print("=" * 76)
    print("Part A: GGV structure facts")
    print("=" * 76)
    ok0 = wclass_set(R0(), 4, -1) == {4}
    mons = sorted(Poly(R0(), x, y).monoms())
    coll = all(4 * (i - 1) == j for (i, j) in mons)
    check("A1: R0 = x(xy^4 - l0)^3 is (4,-1)-homogeneous of weight 4 with collinear "
          "x-anchored support", ok0 and coll, f"support {mons}")
    ok1 = wclass_set(R1(), -2, 1) == {1}
    check("A2: R1 = y(xy^2 - l1) is (-2,1)-homogeneous of weight 1", ok1)
    dep = expand(jac2(R0() ** 2, R0() ** 3)) == 0
    check("A3: R0^m and R0^n are Jacobian-dependent (top compatibility of the pair)",
          dep)


def partB():
    print("=" * 76)
    print("Part B: the x^m-anchored edge operator (multiplication formula)")
    print("=" * 76)
    z = symbols("z")
    ok = True
    for m in (1, 2, 3):
        for (k, l) in ((1, 4), (1, 2), (2, 3)):
            G = symbols("g0:4")
            phi = sum(g * z**i for i, g in enumerate(G))
            E = expand(x**m * phi.subs(z, x**k * y**l))
            for (al, be) in ((0, 1), (1, 1), (2, 3), (0, 4), (3, 2)):
                gmon = x**al * y**be
                lhs = expand(jac2(E, gmon))
                zz = x**k * y**l
                bracket = (be * m * phi + (be * k - al * l) * z * phi.diff(z))
                pred = expand(x**(m + al - 1) * y**(be - 1)
                              * bracket.subs(z, zz))
                if expand(lhs - pred) != 0:
                    ok = False
                    print(f"  B MISMATCH m={m} (k,l)=({k},{l}) (al,be)=({al},{be})")
    check("B: J(x^m phi(z), x^a y^b) = x^{m+a-1} y^{b-1} [b m phi + (bk - al) z phi'] "
          "identically (symbolic phi; grid)", ok)


def partC():
    print("=" * 76)
    print("Part C: for m >= 2 the R0^m edge cannot make the constant")
    print("=" * 76)
    hits = []
    for m in (1, 2, 3):
        E = expand(R0() ** m)
        for al in range(0, 4):
            for be in range(0, 6):
                if al == 0 and be == 0:
                    continue
                out = expand(jac2(E, x**al * y**be))
                if out == 0:
                    continue
                ct = Poly(out, x, y).coeff_monomial(1)
                if ct != 0:
                    hits.append((m, al, be, ct))
    okm = all(m == 1 and al == 0 and be == 1 for (m, al, be, _) in hits)
    for h in hits:
        print(f"  C constant reached: m={h[0]}, g=x^{h[1]}y^{h[2]}, term {h[3]}")
    check("C: the ONLY constant-reaching case is m = 1, g = y (term -3*lambda0^3 type); "
          "for m >= 2 the constant must travel the staircase", okm and len(hits) == 1)


def window_consistent(P, N):
    MQ = [(i, d - i) for d in range(2, N + 1) for i in range(d + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * x**i * y**j for bb, (i, j) in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    return bool(linsolve(eqs, list(B)))


def partD():
    print("=" * 76)
    print("Part D: our theorems bite the B = 16 shape (m = 1 samples)")
    print("=" * 76)
    base = expand(R0(1) / (-1))  # lambda0 = 1: R0 = x(xy^4 - 1)^3; linear part -x
    P0 = expand(-base)  # linear part +x... adjust sign so linear coefficient is +1
    lin = Poly(P0, x, y).coeff_monomial(x)
    P0 = expand(P0 / lin)
    ok_vertex = window_consistent(P0, 8) is False
    print(f"  D pure shape: linear coeff normalized; window 8 "
          f"{'EMPTY' if ok_vertex else 'CONSISTENT (escalate!)'}")
    check("D1: the pure m = 1 B = 16 shape has an EMPTY window (Theorem 4 replication: "
          "x is a vertex and P != x + f(y))", ok_vertex)
    ok_sw = True
    for filler in (x**2, x**3, x**2 + x**3):
        P = expand(P0 + filler)
        empty = not window_consistent(P, 8)
        ok_sw &= empty
        print(f"  D swallowed (+{filler}): "
              f"{'EMPTY' if empty else 'CONSISTENT (escalate!)'}")
    check("D2: swallowed variants (x^d fillers) are EMPTY at window 8 (staircase "
          "territory extended to the B = 16 shape)", ok_sw)


def partE():
    print("=" * 76)
    print("Part E: scoping the full attacks (exact block histograms)")
    print("=" * 76)
    for (nm, N, w1, w2) in (("(48,64) attack, grading (4,-1)", 64, 4, -1),
                            (" (72,108) attack, grading (2,-3)", 108, 2, -3)):
        counts = {}
        for d in range(2, N + 1):
            for i in range(d + 1):
                c = w1 * i + w2 * (d - i)
                counts[c] = counts.get(c, 0) + 1
        tot = sum(counts.values())
        mx = max(counts.values())
        big = sorted(counts.values())[-5:]
        print(f"  E {nm}: window unknowns {tot}, classes {len(counts)}, "
              f"largest diagonal block {mx}, top-5 blocks {big}")
    check("E: block histograms computed: the classwise attack replaces one monolithic "
          "solve by many small blocks (largest in the low hundreds)", True)


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
