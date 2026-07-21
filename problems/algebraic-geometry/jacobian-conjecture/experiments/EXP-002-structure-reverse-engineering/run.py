# EXP-002: reverse-engineer the structure of the counterexample F, exactly.
# CPU-only, exact rational arithmetic (sympy). See hypothesis.md for H1-H4.
#
# Run: .\.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-002-structure-reverse-engineering\run.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib import (F, P, Q, R, det_JF, is_polynomial_in_xyz, lam,  # noqa: E402
                   reduced_triple, to_invariants, u_v, v, t, w, x, y, z)
from sympy import (Matrix, Poly, Rational, degree, expand, factor,  # noqa: E402
                   simplify, solve, symbols)

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


print("=" * 76)
print("H1: weighted scaling symmetry, weights source (1,-1,-2) -> output (-2,-1,1)")
print("=" * 76)
scaled = [c.subs({x: lam * x, y: y / lam, z: z / lam**2}, simultaneous=True) for c in (P, Q, R)]
res = [
    expand(scaled[0] - P / lam**2),
    expand(scaled[1] - Q / lam),
    expand(scaled[2] - lam * R),
]
check("F(lam x, y/lam, z/lam^2) == (P/lam^2, Q/lam, lam R) identically", all(r == 0 for r in res))

print()
print("=" * 76)
print("H2: z-linearity with coefficient vector (u^3, 3x u^2, -x^3)")
print("=" * 76)
u = 1 + x * y
for comp, cname, coeff in ((P, "P", u**3), (Q, "Q", 3 * x * u**2), (R, "R", -(x**3))):
    pz = Poly(expand(comp), z)
    check(f"{cname} is degree <= 1 in z", pz.degree() <= 1)
    check(f"z-coefficient of {cname} equals {coeff}", expand(pz.coeff_monomial(z) - coeff) == 0)

print()
print("=" * 76)
print("H3: exact reduction to invariants v = xy, t = x^2 z")
print("=" * 76)
a1, b1, c1 = reduced_triple()
print(f"  a1 = x^2 P = {factor(a1)}")
print(f"  b1 = x Q   = {expand(b1)}")
print(f"  c1 = R / x = {expand(c1)}")
check("a1, b1, c1 are polynomials in (v, t) alone", True)  # reduced_triple raises otherwise
check("c1 == 2 - 3v - t", expand(c1 - (2 - 3 * v - t)) == 0)

print()
print("=" * 76)
print("Structural re-derivation of det JF (independent route, closes EXP-001 risk)")
print("=" * 76)
# Skew-product factorization: with output invariants V' = Q*R (weight 0), T' = P*R^2 (weight 0),
# the reduced 2-variable Jacobian J2 = det d(V', T')/d(v, t) must satisfy det JF = -J2 / c1^2.
Vp = expand(b1 * c1)
Tp = expand(a1 * c1**2)
J2 = expand(Matrix([[Vp.diff(v), Vp.diff(t)], [Tp.diff(v), Tp.diff(t)]]).det())
dJ = det_JF()
print(f"  det JF (direct expansion)          = {dJ}")
print(f"  J2 = det d(V',T')/d(v,t)           = {factor(J2)}")
check("reduced Keller identity J2 == 2 c1^2", expand(J2 - 2 * c1**2) == 0)
check("skew-product formula det JF == -J2/c1^2 (evaluates to -2)",
      expand(dJ + simplify(J2 / c1**2)) == 0)

print()
print("=" * 76)
print("H4: one-variable fiber identity with w = u c1 / 2, Phi(w) = w^2 - w^3")
print("=" * 76)
wexpr = expand(u_v * c1 / 2)
Phi = wexpr**2 - wexpr**3
residual = expand(Phi - (wexpr * Vp - Tp) / 4)
print(f"  w(v, t) = {factor(wexpr)}")
check("Phi(w) == (w * QR - P R^2)/4 identically in (v, t)", residual == 0)

# Consistency with EXP-001: at the target (-1/4, 0, 0) the fiber equation becomes Phi(w) = 0,
# roots w in {0, 0, 1}; verify w-values at the three preimages are exactly {1, 0, 0}.
pts = [(0, 0, Rational(-1, 4)), (1, Rational(-3, 2), Rational(13, 2)),
       (-1, Rational(3, 2), Rational(13, 2))]
wvals = []
for (px, py, pz_) in pts:
    wv = wexpr.subs({v: px * py, t: px**2 * pz_})
    wvals.append(simplify(wv))
print(f"  w at the three EXP-001 preimages: {wvals}")
check("w-values are (1, 0, 0), matching the roots of Phi(w) = 0 with multiplicity",
      wvals == [1, 0, 0])

print()
print("=" * 76)
print("Derived generating identity: a1 is DETERMINED by (b1, c1)")
print("=" * 76)
# From Phi(w) = (w V' - T')/4 with w = u c1/2 one gets, dividing by c1^2:
#   a1 = u b1 / 2 - u^2 + u^3 c1 / 2.
a1_pred = expand(u_v * b1 / 2 - u_v**2 + u_v**3 * c1 / 2)
check("a1 == u b1/2 - u^2 + u^3 c1/2", expand(a1 - a1_pred) == 0)

print()
if failures:
    print(f"RESULT: {len(failures)} check(s) FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS. Structure established exactly: weighted skew-product over")
print("invariants (v, t); Keller condition reduced to J2 = 2 c1^2 in TWO variables; fibers")
print("governed by the cubic Phi(w) = w^2 - w^3 at w = u c1/2; a1 determined by (b1, c1).")
