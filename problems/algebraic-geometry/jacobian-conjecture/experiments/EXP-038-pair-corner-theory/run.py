# EXP-038: pair-level corner theory (matched-pair law; obstruction depth).
# CPU-only, sympy over QQ. Run: run.py [A|B|C]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, library, sqf_radical, top_form, x, y  # noqa: E402
from sympy import (Poly, Rational, expand, linsolve, simplify, symbols)  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def graded(expr, s):
    p = Poly(expand(expr), x, y)
    return expand(sum(co * x**i * y**j for (i, j), co in p.terms() if i + j == s))


def partA():
    print("=" * 76)
    print("Part A: top dependence + top-2 bookkeeping on the library")
    print("=" * 76)
    ok_dep = True
    ok_rad = True
    ok_two = True
    for k, (P, Q) in enumerate(library()):
        Pt, dP = top_form(P)
        Qt, dQ = top_form(Q)
        if dP + dQ <= 2:
            continue
        dep = expand(jac2(Pt, Qt)) == 0
        ok_dep &= dep
        rp = sqf_radical(Pt)
        rq = sqf_radical(Qt)
        # proportionality test: same monomial support and one common coefficient ratio
        pp = Poly(rp, x, y)
        qq = Poly(rq, x, y)
        prop = False
        if pp.monoms() and qq.monoms() and pp.monoms() == qq.monoms():
            ratios = {simplify(a / b) for a, b in zip(pp.coeffs(), qq.coeffs())}
            prop = len(ratios) == 1
        ok_rad &= prop
        # top-2 class bookkeeping: classes dP+dQ-2 and dP+dQ-3 of J(P,Q) vanish
        # (J(P,Q) is a nonzero constant) when those classes are above 0
        J = expand(jac2(P, Q))
        two = True
        for s in (dP + dQ - 2, dP + dQ - 3):
            if s > 0:
                two &= graded(J, s) == 0
        ok_two &= two
        print(f"  A map {k}: degs ({dP},{dQ}), top-dep {dep}, common-radical {prop}, "
              f"top-2 classes vanish {two}")
    check("A1: J(P_top, Q_top) = 0 for every library pair", ok_dep)
    check("A2: top radicals are proportional (common base) for every library pair", ok_rad)
    check("A3: the top-2 class pieces of J(P, Q) vanish identically (bookkeeping)", ok_two)


def partB():
    print("=" * 76)
    print("Part B: the matched-pair law at the second class (symbolic)")
    print("=" * 76)
    al, be = symbols("alpha beta")
    ok = True
    for (i, j, p, q) in ((1, 1, 2, 3), (2, 1, 1, 2), (1, 2, 2, 3), (1, 1, 1, 2)):
        B = x**i * y**j
        DP = p * (i + j)
        DQ = q * (i + j)
        # generic subtops
        msP = [(c, DP - 1 - c) for c in range(DP)]
        msQ = [(a, DQ - 1 - a) for a in range(DQ)]
        pc = symbols(f"p0:{len(msP)}")
        qc = symbols(f"q0:{len(msQ)}")
        Psub = sum(cc * x**c * y**d for cc, (c, d) in zip(pc, msP))
        Qsub = sum(cc * x**a * y**b for cc, (a, b) in zip(qc, msQ))
        P = al * B**p + Psub
        Q = be * B**q + Qsub
        lhs = graded(jac2(P, Q), DP + DQ - 3)
        pred = 0
        for cc, (a, b) in zip(qc, msQ):
            pred += al * p * (i * b - j * a) * cc * x**(i * p + a - 1) * y**(j * p + b - 1)
        for cc, (c, d) in zip(pc, msP):
            pred -= be * q * (i * d - j * c) * cc * x**(i * q + c - 1) * y**(j * q + d - 1)
        okk = expand(lhs - pred) == 0
        ok &= okk
        print(f"  B (i,j,p,q)=({i},{j},{p},{q}): matched-pair law "
              f"{'EXACT' if okk else 'MISMATCH'}")
    check("B: second class of J(P, Q) == alpha p (ib - ja) q_ab - beta q (id - jc) p_cd "
          "on matched outputs, exactly", ok)


def window_system(P, N, constrain=None):
    """constrain: None for free Q; else (i, j) of the base B: at every degree s in the
    TOP band (s == N), only the monomial B^{s/(i+j)} (if integral) is allowed."""
    MQ = [(ii, d - ii) for d in range(2, N + 1) for ii in range(d + 1)]
    if constrain is not None:
        i, j = constrain
        keep = []
        for (a, b) in MQ:
            s = a + b
            if s == N:
                if s % (i + j) == 0 and (a, b) == (i * s // (i + j), j * s // (i + j)):
                    keep.append((a, b))
            else:
                keep.append((a, b))
        MQ = keep
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * x**a * y**b for bb, (a, b) in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    return eqs, list(B), len(MQ)


def min_inconsistent(P, constrain, Nmax=8):
    for N in range(3, Nmax + 1):
        eqs, B, nunk = window_system(P, N, constrain)
        if not bool(linsolve(eqs, B)):
            return N, nunk
    return None, None


def partC():
    print("=" * 76)
    print("Part C: obstruction depth, free Q vs pair-constrained Q")
    print("=" * 76)
    a2 = Rational(2)
    SAMPLES = [
        ("x + x^2 + 2(xy)^2, B=xy", x + x**2 + a2 * (x * y) ** 2, (1, 1)),
        ("x + x^3 + 2(xy)^2, B=xy", x + x**3 + a2 * (x * y) ** 2, (1, 1)),
        ("x + x^2 + 2 x^2 y (corner x^2 y)", x + x**2 + a2 * x**2 * y, (2, 1)),
        ("x + x^2 + 2 x^3 y^2 (corner x^3 y^2)", x + x**2 + a2 * x**3 * y**2, (3, 2)),
    ]
    ok_same = True
    ok_small = True
    for (nm, P, ij) in SAMPLES:
        nf, uf = min_inconsistent(expand(P), None)
        nc, uc = min_inconsistent(expand(P), ij)
        same = (nf == nc)
        ok_same &= same
        if nf is not None and nf == nc:
            _, _, kf = window_system(expand(P), nf, None)
            _, _, kc = window_system(expand(P), nf, ij)
            ok_small &= kc < kf
            print(f"  C {nm}: free first-inconsistent N={nf} ({kf} unknowns), "
                  f"constrained N={nc} ({kc} unknowns) "
                  f"{'SAME DEPTH' if same else 'DIFFERENT DEPTH'}")
        else:
            print(f"  C {nm}: free N={nf}, constrained N={nc} "
                  f"{'SAME' if same else 'DIFFERENT'}")
    check("C1: the pair constraint does NOT change the first-inconsistent window depth "
          "(no added obstruction power on these samples)", ok_same)
    check("C2: the constrained system is strictly smaller at equal window (efficiency "
          "value quantified)", ok_small)


PARTS = {"A": partA, "B": partB, "C": partC}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
