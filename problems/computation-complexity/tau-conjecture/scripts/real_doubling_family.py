"""Two gates per doubling of REAL roots: g -> g * (g - x^2).

The exhaustive real census gives zRmax(4) = 4 with g1 = (x^2-1)^2 - x^2 in four
gates, and zRmax(6) = 8 with a witness that factors as
(x^4-3x^2+1)(x^4-4x^2+1) = g1 * (g1 - x^2), i.e. TWO extra gates doubled the
real-root count. This tests whether the step iterates.

If it does, the real ladder admits 2^(tau/2), which beats the Chebyshev tower's
2^(tau/3) (T_2 = 2x^2 - 1 costs three gates per doubling).
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import pmul, psub, integer_roots

x = sp.Symbol("x")


def distinct_real_roots(coeffs):
    p = sp.Poly(list(reversed(coeffs)), x, domain="ZZ")
    if p.degree() < 1:
        return 0
    p = p.quo(sp.Poly(sp.gcd(p, p.diff(x)), x, domain="ZZ"))
    return int(p.count_roots()) if p.degree() >= 1 else 0


a = pmul((0, 1), (0, 1))          # 1: x^2
b = psub(a, (1,))                 # 2: x^2 - 1
c = pmul(b, b)                    # 3: (x^2-1)^2
g = psub(c, a)                    # 4: g1 = (x^2-1)^2 - x^2
gates = 4

print(f"{'gates':>6} {'degree':>7} {'real':>6} {'2^(g/2)':>8} {'int':>4}  polynomial")
print("-" * 78)
r = distinct_real_roots(g)
print(f"{gates:>6} {len(g)-1:>7} {r:>6} {2**(gates//2):>8} "
      f"{len(integer_roots(g)):>4}  {g}")

for step in range(4):
    h = psub(g, a)                # +1 gate: g - x^2
    g = pmul(g, h)                # +1 gate: g * (g - x^2)
    gates += 2
    r = distinct_real_roots(g)
    deg = len(g) - 1
    w = str(g)
    print(f"{gates:>6} {deg:>7} {r:>6} {2**(gates//2):>8} "
          f"{len(integer_roots(g)):>4}  {w if len(w) < 30 else w[:27] + '...'}")
    if r != deg:
        print(f"        ^ NOT totally real: {r} real roots of degree {deg}")

print()
print("census anchors: zRmax(4) = 4 and zRmax(6) = 8, both exhaustive.")
print("Chebyshev tower for comparison: T_2 = 2x^2-1 costs 3 gates per doubling,")
print("so it reaches only 2^(tau/3).")
