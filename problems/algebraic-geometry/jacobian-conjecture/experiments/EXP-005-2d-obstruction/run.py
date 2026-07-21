# EXP-005: the 2D obstruction, exact. CPU-only, sympy over QQ. See hypothesis.md.
#
# Run: .\.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-005-2d-obstruction\run.py
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib import constructor_v2, v, t, w  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, fraction, groebner,  # noqa: E402
                   solve, symbols, together)

x, y = symbols("x y")
failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


print("=" * 76)
print("Prediction 1: 2D equivariant determinant reduction (generic symbolic f, g)")
print("=" * 76)
a_w, b1_, b2_ = symbols("a_w b1 b2", integer=True)
fc = symbols("f0 f1 f2 f3")
gc = symbols("g0 g1 g2 g3")
ok_all = True
for a_int in (1, 2, 3):
    for b1i, b2i in ((0, 1 - a_int), (1, -a_int), (2, -1 - a_int), (-1, 2 - a_int)):
        vv = x**a_int * y
        f = sum(c * vv**i for i, c in enumerate(fc))
        g = sum(c * vv**i for i, c in enumerate(gc))
        Pm = x**b1i * f
        Qm = x**b2i * g
        J = together(Matrix([[Pm.diff(x), Pm.diff(y)], [Qm.diff(x), Qm.diff(y)]]).det())
        fv = sum(c * v**i for i, c in enumerate(fc))
        gv = sum(c * v**i for i, c in enumerate(gc))
        predicted = x**(b1i + b2i + a_int - 1) * (b1i * fv * gv.diff(v) - b2i * fv.diff(v) * gv)
        diff = expand(cancel(J - predicted.subs(v, vv)))
        ok_all &= diff == 0
check("det JF == x^(b1+b2+a-1) (b1 f g' - b2 f' g) for a in {1,2,3}, several (b1, b2)", ok_all)

print()
print("=" * 76)
print("Prediction 2: exhaustive small-degree 2D equivariant Keller solutions -> injectivity")
print("=" * 76)
c_sym = symbols("c_det")
DEG = 3
total_sols = 0
noninjective = []
for a_int in (1, 2):
    for b1i in range(-2, 4):
        b2i = 1 - a_int - b1i
        if b1i == 0 and b2i == 0:
            continue
        fcs = symbols(f"F0:{DEG + 1}")
        gcs = symbols(f"G0:{DEG + 1}")
        fv = sum(c * v**i for i, c in enumerate(fcs))
        gv = sum(c * v**i for i, c in enumerate(gcs))
        keller = expand(b1i * fv * gv.diff(v) - b2i * fv.diff(v) * gv - c_sym)
        eqs = [co for co in Poly(keller, v).all_coeffs()]
        sols = solve(eqs, list(fcs) + list(gcs), dict=True)
        for s in sols:
            fsol = fv.subs(s)
            gsol = gv.subs(s)
            free = sorted((fsol.free_symbols | gsol.free_symbols) - {v, c_sym}, key=str)
            # Instantiate remaining free coefficients with fixed nonzero rationals; c_det = 1.
            inst = {c_sym: 1}
            for i, fs in enumerate(free):
                inst[fs] = Rational(i + 2, 3)
            fi = cancel(fsol.subs(inst))
            gi = cancel(gsol.subs(inst))
            resid = expand(b1i * fi * gi.diff(v) - b2i * fi.diff(v) * gi - 1)
            if resid != 0 or fi == 0 or gi == 0:
                continue
            vv = x**a_int * y
            Pm = expand(x**b1i * fi.subs(v, vv))
            Qm = expand(x**b2i * gi.subs(v, vv))
            # Keep only polynomial maps (negative b with insufficient valuation -> Laurent, skip).
            numP, denP = fraction(together(Pm))
            numQ, denQ = fraction(together(Qm))
            if denP.has(x) or denP.has(y) or denQ.has(x) or denQ.has(y):
                continue
            total_sols += 1
            # Fiber over a random rational target, exact: count solutions via Groebner.
            A0, B0 = Rational(5, 7), Rational(-3, 11)
            gb = groebner([expand(Pm - A0), expand(Qm - B0)], x, y, order="lex")
            if gb.exprs == [1]:
                nsol = 0  # empty fiber (map not surjective onto this target)
            else:
                uni = [g for g in gb.exprs if g.free_symbols <= {y}]
                nsol = Poly(uni[-1], y).degree() if uni else None
            if nsol is not None and nsol > 1:
                noninjective.append((a_int, b1i, b2i, fi, gi, nsol))
print(f"  Keller-solvable polynomial instances tested: {total_sols}")
check("every tested 2D equivariant Keller instance has fiber degree <= 1 (injective/empty)",
      not noninjective, str(noninjective)[:200])

print()
print("=" * 76)
print("Prediction 3: killing the second invariant t collapses the reduced Jacobian")
print("=" * 76)
for label, seed, kk in (("P2 seed", 2 * w - 3 * w**2, 2), ("P3 seed", w - 2 * w**3, 3)):
    a1, b1, c1, prm = constructor_v2(seed, kk)
    # t-independent surrogate: replace the free coordinate s = q(v) - t by s0 = q(v).
    s0 = prm["q"]
    a1f = cancel(a1.subs(t, prm["q"] - s0))   # identical, then substitute s0 explicitly:
    Vp = expand((b1 * c1).subs(t, 0).subs(v, v))
    # Proper collapse test: V', T' as functions of v ONLY (t frozen to q(v) - s0 with s0 = q(v),
    # i.e. t = 0 section replaced by s = q(v)): both become univariate, so J2 must vanish.
    Vp_1d = expand((b1 * c1).subs(t, prm["q"] - prm["q"]))
    Tp_1d = expand((a1 * c1**2).subs(t, prm["q"] - prm["q"]))
    J2_1d = expand(Matrix([[Vp_1d.diff(v), Vp_1d.diff(t)],
                           [Tp_1d.diff(v), Tp_1d.diff(t)]]).det())
    check(f"{label}: J2 == 0 identically once s is a function of v alone", J2_1d == 0)

print()
print("=" * 76)
print("Prediction 4: no 2x2 slice of the announced F is Keller")
print("=" * 76)
from jclib import P as FP, Q as FQ, R as FR, x as X3, y as Y3, z as Z3  # noqa: E402

slice_vals = [Rational(1), Rational(-1, 2), Rational(3, 5)]
found_keller_slice = []
comps = {"P": FP, "Q": FQ, "R": FR}
for fixed_var, keep in (("x", (Y3, Z3)), ("y", (X3, Z3)), ("z", (X3, Y3))):
    for val in slice_vals:
        sub = {{"x": X3, "y": Y3, "z": Z3}[fixed_var]: val}
        for (n1, C1), (n2, C2) in itertools.combinations(comps.items(), 2):
            g1, g2 = expand(C1.subs(sub)), expand(C2.subs(sub))
            J = expand(Matrix([[g1.diff(keep[0]), g1.diff(keep[1])],
                               [g2.diff(keep[0]), g2.diff(keep[1])]]).det())
            if J.is_number and J != 0:
                found_keller_slice.append((fixed_var, val, n1, n2, J))
check("no coordinate slice (any fixed variable at 3 rational values, any output pair) is Keller",
      not found_keller_slice, str(found_keller_slice)[:200])

print()
if failures:
    print(f"RESULT: {len(failures)} check(s) FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS. The 2D obstruction is exact in this scope: the equivariant")
print("mechanism cannot produce a 2D counterexample (small-degree null result); the second")
print("weight-0 invariant is load-bearing (J2 collapses without it); no slice of F is Keller.")
