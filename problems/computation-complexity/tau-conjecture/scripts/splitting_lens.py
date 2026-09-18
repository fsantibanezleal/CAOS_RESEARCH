"""V13, the splitting lens: are the census records FULLY SPLIT over Z?

If the record polynomials factor completely into integer linear factors, then
zmax(tau) is not really "how many roots fit" but "how much DEGREE a cheap
program can carry while splitting completely over Z". Degree alone reaches
2^(tau-1); splitting is the whole constraint. Measured, not assumed.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import census_polynomials, integer_roots


def deg(p):
    return len(p) - 1


def split_multiplicity(p):
    """Total multiplicity of integer roots. Fully split iff it equals deg(p)."""
    q = list(p)
    total = 0
    for r in integer_roots(tuple(q)):
        while True:
            # synthetic division by (x - r), exact only if remainder is 0
            n = len(q) - 1
            out = [0] * n
            carry = 0
            for i in range(n, 0, -1):
                carry = q[i] + carry * r if i < n else q[i]
                out[i - 1] = carry
            rem = q[0] + carry * r
            if rem != 0:
                break
            q = out
            total += 1
            while len(q) > 1 and q[-1] == 0:
                q.pop()
            if len(q) <= 1:
                break
    return total


DEPTH = 5
per_depth, first_seen, complete = census_polynomials(DEPTH)
print(f"census to depth {DEPTH}: {len(first_seen):,} polynomials, complete={complete}\n")

print(f"{'tau':>4} {'zmax':>5} {'record deg':>11} {'fully split?':>13} "
      f"{'S_nonmono':>10} {'2^(tau-1)':>10}  record witness")
print("-" * 100)
for tau in sorted({t for t in first_seen.values()}):
    polys = [p for p, t in first_seen.items() if t == tau and p]
    best_z, best_p = -1, None
    S = 0
    for p in polys:
        z = len(integer_roots(p))
        if z > best_z:
            best_z, best_p = z, p
        # A monomial c*x^k is trivially "fully split" (every root is 0) and
        # reaches degree 2^tau, which says nothing about packing roots. Exclude
        # it, as with every other zero-object degeneracy in this problem.
        monomial = sum(1 for c in p if c) <= 1
        if (not monomial) and deg(p) >= 1 and split_multiplicity(p) == deg(p) and deg(p) > S:
            S = deg(p)
    d = deg(best_p)
    fs = split_multiplicity(best_p) == d
    w = str(best_p)
    print(f"{tau:>4} {best_z:>5} {d:>11} {str(fs):>13} {S:>10} {2**(tau-1):>10}  "
          f"{w if len(w) < 34 else w[:31] + '...'}")

print()
print()
print("S_nonmono(tau) = the largest degree a NON-MONOMIAL tau-gate polynomial can")
print("reach while splitting completely over Z. Compare it with the degree ceiling")
print("2^(tau-1), which non-monomials DO attain (measured, frobenius_theorem.py):")
print("cheap programs reach exponential degree, and over F_p they even split")
print("completely at that degree; over Z the splitting collapses to the census.")
