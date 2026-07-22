# EXP-014: the properness (escape) instrument for planar pairs.
# CPU-only, sympy over QQ. Run: run.py [A|B|C]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, library, x, y  # noqa: E402
from sympy import (Poly, expand, factor, resultant, solve, symbols)  # noqa: E402

failures = []
u, v = symbols("u v")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def lead_coeffs(P, Q):
    """(lcx, lcy): x-leading coeff of Res_y(P-u, Q-v) and y-leading of Res_x."""
    ry = resultant(expand(P - u), expand(Q - v), y)
    rx = resultant(expand(P - u), expand(Q - v), x)
    lcx = Poly(expand(ry), x).LC() if expand(ry) != 0 else None
    lcy = Poly(expand(rx), y).LC() if expand(rx) != 0 else None
    return expand(lcx), expand(lcy)


def is_const(e):
    return e is not None and not ({u, v} & e.free_symbols)


def partA():
    print("=" * 76)
    print("Part A: properness certificates for the 8 library automorphisms")
    print("=" * 76)
    ok = True
    for k, (P, Q) in enumerate(library()):
        lcx, lcy = lead_coeffs(P, Q)
        good = is_const(lcx) and is_const(lcy) and lcx != 0 and lcy != 0
        ok &= good
        print(f"  A map {k}: lc_x = {lcx}, lc_y = {lcy} -> "
              f"{'PROPER (certified)' if good else 'NOT CERTIFIED'}")
    check("A: both resultant leading coefficients are nonzero constants for every "
          "library pair (exact properness certificates)", ok)


def partB():
    print("=" * 76)
    print("Part B: controls")
    print("=" * 76)
    lcx, lcy = lead_coeffs(x * y, y)
    nonprop = (not is_const(lcx)) or (not is_const(lcy))
    print(f"  B (xy, y): lc_x = {lcx}, lc_y = {lcy}")
    okv = False
    for lc in (lcx, lcy):
        if lc is not None and not is_const(lc):
            sols = solve(lc, v)
            okv |= (sols == [0])
    check("B1: (xy, y) fails the certificate with asymptotic locus in {v = 0} "
          "(matches the exact fiber analysis)", nonprop and okv)
    # exact fiber check: over (u, 0) with u != 0 the fiber is empty
    okf = solve([x * y - 1, y], [x, y]) == []
    check("B2: fiber of (xy, y) over (1, 0) is EMPTY exactly (escape confirmed)", okf)
    lcx2, lcy2 = lead_coeffs(x**2, y)
    okp = is_const(lcx2) and is_const(lcy2)
    noninj = expand((x**2).subs(x, 2) - (x**2).subs(x, -2)) == 0
    print(f"  B (x^2, y): lc_x = {lcx2}, lc_y = {lcy2}")
    check("B3: (x^2, y) is certified proper yet non-injective: properness alone does "
          "not give injectivity (the Keller hypothesis is the upgrade)", okp and noninj)


def partC():
    print("=" * 76)
    print("Part C: the route statement + edge alignment observation")
    print("=" * 76)
    # [C] observation on the control: the escape direction of (xy, y) is y -> 0 with
    # x y bounded: the branch tracks the edge direction of the component xy (the
    # (1,1)-corner ray), while proper triangular components have no such branch.
    lcx, _ = lead_coeffs(x * y, y)
    fac = factor(lcx) if lcx is not None else None
    print(f"  C (xy, y): non-properness locus factor: {fac}; escape branch "
          f"(x, y) = (t, c/t), t -> inf, image -> (c, 0): tracks the corner ray of xy")
    print("  C route [D]: proper + Keller => covering of C^2 => invertible (classical); "
          "hence JC(2) <=> every planar Keller map has EMPTY Jelonek set: the escape "
          "picture is the dual of the staircase obstruction (EXP-035/037)")
    check("C: instrument + reduction recorded (observation level [C]/[D], no theorem "
          "claimed)", fac is not None)


PARTS = {"A": partA, "B": partB, "C": partC}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
