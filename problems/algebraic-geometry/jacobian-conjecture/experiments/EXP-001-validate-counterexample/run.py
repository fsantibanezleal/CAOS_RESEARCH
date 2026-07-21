# Validate the claimed N=3 counterexample to the Jacobian conjecture
# (attributed to Levent Alpoge, 2026). All checks are EXACT (rational arithmetic).
#
# Claimed map F : C^3 -> C^3
#   F1 = (1+xy)^3 z + y^2 (1+xy)(4+3xy)
#   F2 = y + 3x(1+xy)^2 z + 3xy^2(4+3xy)
#   F3 = 2x - 3x^2 y - x^3 z
#
# Claims to verify:
#   (A) det Jacobian(F) is the CONSTANT -2 (so F is a Keller map).
#   (B) F(0,0,-1/4) = F(1,-3/2,13/2) = F(-1,3/2,13/2) = (-1/4, 0, 0)
#       (three distinct preimages of one point: F is NOT injective, hence has
#        no inverse map at all, polynomial or otherwise -> the Jacobian
#        conjecture is FALSE for N=3 if (A) and (B) both hold).
#   (C) Best-effort: the full fiber F^{-1}(-1/4, 0, 0) via a lex Groebner basis
#       (fibers of a Keller map are 0-dimensional, so this terminates in theory;
#        guarded so a blow-up does not sink the run).
#
# Run:  .\.venv\Scripts\python.exe wip/caos-research/validation/validate_alpoge_counterexample.py

import sys
from sympy import (Matrix, Rational, expand, factor, groebner, simplify,
                   symbols)

x, y, z = symbols("x y z")

F1 = (1 + x * y) ** 3 * z + y**2 * (1 + x * y) * (4 + 3 * x * y)
F2 = y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y**2 * (4 + 3 * x * y)
F3 = 2 * x - 3 * x**2 * y - x**3 * z
F = Matrix([F1, F2, F3])

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


print("=" * 72)
print("Claim (A): det J(F) == -2 identically")
print("=" * 72)
J = F.jacobian([x, y, z])
detJ = expand(J.det())
print(f"  det J (expanded) = {detJ}")
check("det J is the constant -2", detJ == -2)

print()
print("=" * 72)
print("Claim (B): three distinct points map to (-1/4, 0, 0)")
print("=" * 72)
pts = [
    (Rational(0), Rational(0), Rational(-1, 4)),
    (Rational(1), Rational(-3, 2), Rational(13, 2)),
    (Rational(-1), Rational(3, 2), Rational(13, 2)),
]
target = (Rational(-1, 4), Rational(0), Rational(0))
for p in pts:
    img = tuple(simplify(f.subs({x: p[0], y: p[1], z: p[2]})) for f in (F1, F2, F3))
    print(f"  F{p} = {img}")
    check(f"F{p} == (-1/4, 0, 0)", img == target)
check("the three preimages are pairwise distinct", len(set(pts)) == 3)

print()
print("=" * 72)
print("Consequence: F is a Keller map (det J = -2 != 0, constant) that is NOT")
print("injective, hence NOT invertible: the Jacobian conjecture fails for N=3")
print("(and, by adding dummy coordinates, for every N >= 3).")
print("=" * 72)

print()
print("=" * 72)
print("Claim (C): full fiber over (-1/4, 0, 0) via lex Groebner basis")
print("=" * 72)
try:
    eqs = [expand(F1 + Rational(1, 4)), expand(F2), expand(F3)]
    gb = groebner(eqs, x, y, z, order="lex")
    print("  lex Groebner basis of the fiber ideal:")
    for g in gb.exprs:
        print(f"    {factor(g)} = 0")
    # The last lex basis element is (generically) univariate in z.
    from sympy import Poly, roots

    uni = [g for g in gb.exprs if g.free_symbols <= {z}]
    if uni:
        pz = Poly(uni[-1], z)
        print(f"  univariate eliminant in z: {pz.as_expr()} (degree {pz.degree()})")
        rt = roots(pz.as_expr(), z)
        print(f"  its roots (with multiplicity): {rt}")
except Exception as e:  # Groebner blow-up is acceptable; (A)+(B) already decide.
    print(f"  Groebner computation not completed: {e!r}")

print()
if failures:
    print(f"RESULT: VALIDATION FAILED on {len(failures)} check(s): {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS. The counterexample is VALID: the Jacobian")
print("conjecture is false for N >= 3 over C (exact symbolic verification).")
