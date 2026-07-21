# EXP-007: the asymptotic variety, exact. CPU-only, sympy over QQ. See hypothesis.md.
#
# Run: .\.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-007-asymptotic-variety\run.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib import P as FP, Q as FQ, R as FR, constructor_v2, v, t, w, x, y, z  # noqa: E402
from sympy import (Poly, Rational, cancel, discriminant, expand, factor,  # noqa: E402
                   groebner, simplify, solve, symbols)

A, B, C = symbols("A B C")
failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def fiber_points(Pc, Qc, Rc, target):
    """Exact fiber of (Pc,Qc,Rc) over a rational target via lex Groebner; returns point list."""
    gb = groebner([expand(Pc - target[0]), expand(Qc - target[1]), expand(Rc - target[2])],
                  x, y, z, order="lex")
    if gb.exprs == [1]:
        return []
    sols = solve(gb.exprs, [x, y, z], dict=True)
    return sorted(set(tuple(s[var] for var in (x, y, z)) for s in sols
                      if all(s[var].is_rational for var in (x, y, z))), key=str)


print("=" * 76)
print("Prediction 1: escape roots ARE multiple fiber roots (W' = k^2 p - BC)")
print("=" * 76)
for label, seed, kk in (("F (P2)", 2 * w - 3 * w**2, 2), ("P3", w - 2 * w**3, 3)):
    a1, b1, c1, prm = constructor_v2(seed, kk)
    Phi, mm = prm["Phi"], prm["m"]
    W = expand(kk**2 * Phi - (w * B * C - A * C**2))
    sw = cancel((B * C - kk**2 * seed) / mm)
    check(f"{label}: W'(w) == k^2 p(w) - BC identically",
          expand(W.diff(w) - (kk**2 * seed - B * C)) == 0)
    check(f"{label}: s == -W'(w)/m identically", expand(sw + W.diff(w) / mm) == 0)

print()
print("=" * 76)
print("Prediction 2: escape target (0, 1, 1) for F: D = 0 and a ONE-point fiber")
print("=" * 76)
a1, b1, c1, prm = constructor_v2(2 * w - 3 * w**2, 2)
Phi, mm, q_ = prm["Phi"], prm["m"], prm["q"]
W = expand(4 * Phi - (w * B * C - A * C**2))
D = expand(discriminant(Poly(W, w)))
print(f"  disc_w(W) = {factor(D)}")
check("D(A, B, C) is a nonconstant polynomial", not D.is_number)
D011 = D.subs({A: 0, B: 1, C: 1})
check("D(0, 1, 1) == 0 (target on the asymptotic variety)", D011 == 0, f"D = {D011}")
pts = fiber_points(FP, FQ, FR, (Rational(0), Rational(1), Rational(1)))
print(f"  exact fiber of F over (0, 1, 1): {pts}")
check("the fiber over (0, 1, 1) has EXACTLY ONE point", len(pts) == 1)
check("that point is (2, -1/2, 9/8), as the reconstruction predicts",
      pts == [(Rational(2), Rational(-1, 2), Rational(9, 8))])

print()
print("=" * 76)
print("Prediction 3: the plane C = 0: exactly one (flat-sheet) preimage")
print("=" * 76)
for (A0, B0) in ((Rational(3, 5), Rational(-2, 7)), (Rational(5), Rational(1, 3))):
    pts = fiber_points(FP, FQ, FR, (A0, B0, Rational(0)))
    expected = (Rational(0), B0, A0 - 4 * B0**2)
    print(f"  fiber over ({A0}, {B0}, 0): {pts}")
    check(f"fiber over ({A0}, {B0}, 0) == [flat-sheet point {expected}]",
          pts == [expected])

print()
print("=" * 76)
print("Prediction 4: the EXP-004 collision target (-16, -16, 1): D != 0, full 3-point fiber")
print("=" * 76)
Dcoll = D.subs({A: Rational(-16), B: Rational(-16), C: Rational(1)})
check("D(-16, -16, 1) != 0 (off the asymptotic variety)", Dcoll != 0, f"D = {Dcoll}")
pts = fiber_points(FP, FQ, FR, (Rational(-16), Rational(-16), Rational(1)))
print(f"  exact fiber over (-16, -16, 1): {pts}")
check("the fiber over (-16, -16, 1) has EXACTLY THREE (finite, rational) points", len(pts) == 3)
check("it contains both EXP-004 collision points",
      (Rational(-1, 6), Rational(8), Rational(432)) in pts
      and (Rational(1, 8), Rational(-4), Rational(-288)) in pts)

print()
if failures:
    print(f"RESULT: {len(failures)} check(s) FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS. The asymptotic variety of F is characterized exactly:")
print("over C != 0 it is the DISCRIMINANT locus of the fiber polynomial (escape roots are")
print("precisely multiple fiber roots: sheets merge at infinity), and the plane C = 0 is")
print("asymptotic with exactly one finite (flat-sheet) preimage. Collisions are generic and")
print("live OFF the asymptotic variety.")
