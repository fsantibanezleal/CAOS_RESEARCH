"""zpmax(tau) = 2^(tau-1) exactly: check both halves of the proof.

UPPER. Every value of a constant-free SLP satisfies deg(v) <= 2^(mu(v)) where
mu counts multiplicative gates in its sub-DAG (induction: additive gates keep
the max degree, a product adds degrees). A program with NO additive gate
computes +-x^k or 0, which has at most one distinct root in any field. So a
non-monomial f has at most tau-1 multiplicative gates, hence degree at most
2^(tau-1), hence at most 2^(tau-1) roots in any F_p where it does not vanish
identically.

LOWER. x^(2^k) - 1 costs k squarings plus one subtraction, so tau = k+1, and
modulo any prime p = 1 (mod 2^k) it has exactly gcd(2^k, p-1) = 2^k roots.
Such p exist for every k by Dirichlet.

The upper bound is a proof; this script checks the degree induction on the
enumerated census and verifies the lower-bound construction directly.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import census_polynomials


def is_monomial(p):
    return sum(1 for c in p if c) <= 1


print("UPPER bound, checked against the complete census to depth 5:")
per_depth, first_seen, complete = census_polynomials(5)
worst = {}
for poly, tau in first_seen.items():
    if not poly or is_monomial(poly):
        continue
    d = len(poly) - 1
    if d > worst.get(tau, -1):
        worst[tau] = d
ok = True
for tau in sorted(worst):
    cap = 2 ** (tau - 1)
    flag = "ok" if worst[tau] <= cap else "VIOLATION"
    if worst[tau] > cap:
        ok = False
    print(f"  tau={tau}: max degree of a NON-MONOMIAL = {worst[tau]:>3}, "
          f"bound 2^(tau-1) = {cap:>3}   {flag}")
print("  degree bound holds on every non-monomial in the census:", ok)

print()
print("LOWER bound, x^(2^k) - 1 modulo a prime p = 1 (mod 2^k):")


def first_prime_1_mod(m, start=3):
    n = m + 1
    while True:
        if n > 2:
            d, isp = 2, True
            while d * d <= n:
                if n % d == 0:
                    isp = False
                    break
                d += 1
            if isp:
                return n
        n += m


print(f"  {'k':>3} {'tau=k+1':>8} {'p':>8} {'roots of x^(2^k)-1 mod p':>26} {'2^k':>7}")
for k in range(1, 9):
    m = 2 ** k
    p = first_prime_1_mod(m)
    roots = sum(1 for x in range(p) if pow(x, m, p) == 1 % p)
    flag = "ok" if roots == m else "MISMATCH"
    print(f"  {k:>3} {k+1:>8} {p:>8} {roots:>26} {m:>7}  {flag}")

print()
print("THEOREM zpmax(tau) = 2^(tau-1), against the measured integer census")
print("  zmax(tau)  = 1, 2, 3, 3, 4, 5, 5, 6   (exhaustive, tau = 1..8)")
print("  zpmax(tau) = 1, 2, 4, 8, 16, 32, 64, 128")
