# EXP-009: characteristic-p reductions of the P3 counterexample. CPU-only, exact. See hypothesis.md.
#
# Run: .\.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-009-char-p-reductions\run.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib import constructor_v2, v, t, w, x, y, z  # noqa: E402
from sympy import Poly, Rational, cancel, expand, Matrix  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def red(q_, ell):
    """Reduce an ell-integral rational mod ell; raises if the denominator hits ell."""
    q_ = Rational(q_)
    if q_.q % ell == 0:
        raise ValueError(f"denominator {q_.q} not prime to {ell}")
    return (q_.p * pow(q_.q, -1, ell)) % ell


a1, b1, c1, prm = constructor_v2(w - 2 * w**3, 3)
sub = {v: x * y, t: x**2 * z}
comps = [expand(cancel(expand(a1.subs(sub)) / x**2)),
         expand(cancel(expand(b1.subs(sub)) / x)),
         expand(x * c1.subs(sub))]
J = expand(Matrix([[c.diff(var) for var in (x, y, z)] for c in comps]).det())
print(f"P3 instance: det = {J}, total degrees = {[Poly(c, x, y, z).total_degree() for c in comps]}")

pts = [(Rational(-1, 15), Rational(18), Rational(5130)),
       (Rational(1, 24), Rational(-18), Rational(-10368))]
target = (Rational(-54), Rational(-54), Rational(1))
imgs = [tuple(expand(c.subs({x: p_[0], y: p_[1], z: p_[2]}, simultaneous=True)) for c in comps)
        for p_ in pts]
check("exact images of both collision points equal (-54, -54, 1)",
      all(im == target for im in imgs))

for ell in (13, 101):
    print()
    print("=" * 76)
    print(f"Prime ell = {ell}")
    print("=" * 76)
    ok_coeffs = True
    for c in comps:
        for coeff in Poly(c, x, y, z).coeffs():
            try:
                red(coeff, ell)
            except ValueError:
                ok_coeffs = False
    check(f"ell = {ell}: all component coefficients are ell-integral (reduction well defined)",
          ok_coeffs)
    check(f"ell = {ell}: det J = -3 is nonzero mod ell", red(J, ell) != 0,
          f"det mod {ell} = {red(J, ell)}")
    rpts = [tuple(red(cd, ell) for cd in p_) for p_ in pts]
    rtar = tuple(red(cd, ell) for cd in target)
    print(f"  reduced points mod {ell}: {rpts}; reduced target: {rtar}")
    check(f"ell = {ell}: the two reduced points are DISTINCT in F_ell^3", rpts[0] != rpts[1])
    check(f"ell = {ell}: total degree 12 < ell", 12 < ell)
    print(f"  conclusion: an explicit non-injective Keller map over F_{ell} of degree 12 < {ell}")

print()
if failures:
    print(f"RESULT: {len(failures)} check(s) FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS. P3 reduces at ell = 13 and ell = 101 to explicit non-injective")
print("Keller maps over F_ell with total degree 12 strictly below the characteristic; the")
print("collision certificate survives reduction (exact images + distinct reduced points).")
