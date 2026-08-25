"""The REAL ladder: max distinct real roots of a tau-gate polynomial.

Completes the three-worlds table. Over F_p the answer is exactly 2^(tau-1)
(proved). Over Z the census gives 1,2,3,3,4,5,5,6. Over R the conjecture's
analogue is known to fail; this measures by how much, on the SAME enumerated
programs, so all three columns are comparable term by term.

Distinct real roots are counted EXACTLY: take the square-free part
f / gcd(f, f'), then count real roots by Sturm's theorem in exact rational
arithmetic. No floating point anywhere.
"""
import os
import sys
import time

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import census_polynomials

x = sp.Symbol("x")


def distinct_real_roots(coeffs):
    """coeffs: dense tuple, constant first. Returns count of distinct real roots."""
    if not coeffs or all(c == 0 for c in coeffs):
        return None                       # the zero polynomial: undefined
    p = sp.Poly(list(reversed(coeffs)), x, domain="ZZ")
    if p.degree() < 1:
        return 0                          # nonzero constant
    p = p.quo(sp.Poly(sp.gcd(p, p.diff(x)), x, domain="ZZ"))   # square-free part
    if p.degree() < 1:
        return 0
    return int(p.count_roots())


# --- known-answer gate, before any production number is produced -----------
GATE = [
    ((-1, 0, 1), 2, "x^2 - 1"),
    ((1, 0, 1), 0, "x^2 + 1"),
    ((0, 0, 1), 1, "x^2 (double root counts once)"),
    ((1, 0, -8, 0, 8), 4, "Chebyshev T_4 = 8x^4 - 8x^2 + 1"),
    ((-1, 0, 0, 0, 1), 2, "x^4 - 1"),
    ((0, -4, 0, 5, 0, -1), 5, "-x^5 + 5x^3 - 4x = -x(x^2-1)(x^2-4)"),
    ((-64, 0, 84, 0, -21, 0, 1), 6, "(x^2-1)(x^2-4)(x^2-16)"),
]
print("known-answer gate:")
ok = True
for coeffs, want, name in GATE:
    got = distinct_real_roots(coeffs)
    flag = "ok" if got == want else "FAIL"
    if got != want:
        ok = False
    print(f"  {name:<44} want {want}, got {got}   {flag}")
if not ok:
    print("GATE FAILED - not running the census")
    sys.exit(1)
print("gate passed\n")

DEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 5
t0 = time.time()
per_depth, first_seen, complete = census_polynomials(DEPTH)
print(f"census to depth {DEPTH}: {len(first_seen):,} distinct polynomials, "
      f"complete={complete}")

best = {}
t1 = time.time()
for i, (poly, tau) in enumerate(first_seen.items()):
    n = distinct_real_roots(poly)
    if n is None:
        continue
    if n > best.get(tau, (-1, None))[0]:
        best[tau] = (n, poly)
    if (i + 1) % 2000 == 0:
        print(f"    {i+1:,}/{len(first_seen):,}  ({time.time()-t1:.0f}s)")

print()
print(f"{'tau':>4} {'zmax(Z)':>8} {'zRmax(R)':>9} {'2^(tau-1)':>10}  witness")
print("-" * 84)
ZMAX = {1: 1, 2: 2, 3: 3, 4: 3, 5: 4, 6: 5, 7: 5, 8: 6}
for tau in sorted(best):
    n, poly = best[tau]
    w = str(poly)
    print(f"{tau:>4} {ZMAX.get(tau,'?'):>8} {n:>9} {2**(tau-1):>10}  "
          f"{w if len(w) < 40 else w[:37] + '...'}")
print(f"\ntotal {time.time()-t0:.0f}s")
