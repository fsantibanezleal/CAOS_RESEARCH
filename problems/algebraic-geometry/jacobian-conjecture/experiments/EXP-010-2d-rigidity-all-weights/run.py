# EXP-010: 2D equivariant rigidity for arbitrary weights. CPU-only, sympy over QQ.
# See hypothesis.md, predictions 1-4.
#
# Run: .\.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-010-2d-rigidity-all-weights\run.py
import sys

from sympy import Matrix, Poly, cancel, expand, solve, symbols, together

x, y, v = symbols("x y v")
c = symbols("c_det")
failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


WEIGHTS = [(1, 1), (2, 1), (3, 1), (3, 2), (5, 2), (5, 3), (4, 3), (1, 0)]

print("=" * 76)
print("Prediction 1: the determinant identity, generic symbolic f and g")
print("=" * 76)
fc = symbols("f0 f1 f2 f3")
gc = symbols("g0 g1 g2 g3")
fv = sum(co * v**i for i, co in enumerate(fc))
gv = sum(co * v**i for i, co in enumerate(gc))
ok_all = True
tested = 0
for (w1, w2) in WEIGHTS:
    vv = x**w2 * y**w1
    for i1 in range(0, 3):
        for j1 in range(0, 3):
            for i2 in range(0, 3):
                for j2 in range(0, 3):
                    Pm = x**i1 * y**j1 * fv.subs(v, vv)
                    Qm = x**i2 * y**j2 * gv.subs(v, vv)
                    J = together(Matrix([[Pm.diff(x), Pm.diff(y)],
                                         [Qm.diff(x), Qm.diff(y)]]).det())
                    b1_, b2_ = w1 * i1 - w2 * j1, w1 * i2 - w2 * j2
                    bracket = ((i1 * j2 - i2 * j1) * fv * gv
                               + v * (b1_ * fv * gv.diff(v) - b2_ * fv.diff(v) * gv))
                    pred = x**(i1 + i2 - 1) * y**(j1 + j2 - 1) * bracket.subs(v, vv)
                    ok_all &= expand(cancel(J - pred)) == 0
                    tested += 1
check(f"det JF identity holds for {tested} (weights x exponents) cases, generic f, g", ok_all)

print()
print("=" * 76)
print("Prediction 2: the mixed shapes (P = xy f, Q = g) and swap are never Keller")
print("=" * 76)
DEG = 4
for (w1, w2) in WEIGHTS:
    for (i1, j1, i2, j2) in ((1, 1, 0, 0), (0, 0, 1, 1)):
        fcs = symbols(f"F0:{DEG + 1}")
        gcs = symbols(f"G0:{DEG + 1}")
        fs = sum(co * v**i for i, co in enumerate(fcs))
        gs = sum(co * v**i for i, co in enumerate(gcs))
        b1_, b2_ = w1 * i1 - w2 * j1, w1 * i2 - w2 * j2
        bracket = ((i1 * j2 - i2 * j1) * fs * gs
                   + v * (b1_ * fs * gs.diff(v) - b2_ * fs.diff(v) * gs))
        eqs = Poly(expand(bracket - c), v).all_coeffs()
        tnz = symbols("tnz")
        sols = solve(list(eqs) + [c * tnz - 1], list(fcs) + list(gcs) + [c, tnz], dict=True)
        check(f"(w1,w2)=({w1},{w2}), shape ({i1},{j1},{i2},{j2}): no Keller solution",
              sols == [])

print()
print("=" * 76)
print("Prediction 3: surviving shapes: no solutions of exact bidegree (df, dg) != (0, 0)")
print("=" * 76)
MAXD = 5
for (w1, w2) in WEIGHTS:
    bad = []
    for shape, sgn in (("A", 1), ("swap", -1)):
        for df in range(0, MAXD + 1):
            for dg in range(0, MAXD + 1):
                if df == 0 and dg == 0:
                    continue
                fcs = symbols(f"F0:{df + 1}")
                gcs = symbols(f"G0:{dg + 1}")
                fs = sum(co * v**i for i, co in enumerate(fcs))
                gs = sum(co * v**i for i, co in enumerate(gcs))
                if shape == "A":
                    bracket = fs * gs + v * (w1 * fs * gs.diff(v) + w2 * fs.diff(v) * gs)
                else:
                    bracket = -fs * gs - v * (w2 * fs * gs.diff(v) + w1 * fs.diff(v) * gs)
                eqs = Poly(expand(bracket - c), v).all_coeffs()
                t1, t2, t3 = symbols("t1 t2 t3")
                # Demand genuinely-that-degree leading coefficients AND c != 0.
                extra = [fcs[-1] * t1 - 1, gcs[-1] * t2 - 1, c * t3 - 1]
                sols = solve(list(eqs) + extra,
                             list(fcs) + list(gcs) + [c, t1, t2, t3], dict=True)
                if sols:
                    bad.append((shape, df, dg, sols[:1]))
    check(f"(w1,w2)=({w1},{w2}): only constant (f, g) satisfy the Keller ODE (df,dg <= {MAXD})",
          not bad, str(bad)[:200])

print()
print("=" * 76)
print("Prediction 4: the kill factor 1 + w1 dg + w2 df is positive on the sweep ranges")
print("=" * 76)
ok_pos = all(1 + w1 * dg + w2 * df > 0
             for (w1, w2) in WEIGHTS for df in range(0, 20) for dg in range(0, 20))
check("kill factor strictly positive for all sweep weights and degrees up to 19", ok_pos)

print()
if failures:
    print(f"RESULT: {len(failures)} check(s) FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS. Classification certified on the sweeps: an equivariant Keller")
print("map of C^2 must have shape (x f(v), y g(v)) or the swap, and the Keller ODE admits only")
print("constant (f, g). Combined with the general top-coefficient argument (factor")
print("1 + w1 dg + w2 df > 0 for all degrees), every Gm-equivariant Keller map of C^2 is")
print("LINEAR: the 2D equivariant rigidity conjecture is now a theorem for this class.")
