"""Extend the real ladder to tau = 6 without holding a depth-6 census.

The depth-6 frontier is 25.8M states and RAM is contended. The last-gate lemma
avoids it: given the EXHAUSTED depth-5 frontier (778,087 states), one gate over
every state's operands enumerates every polynomial of tau exactly 6, storing
only the distinct new polynomials.

Built-in known-answer gate: the INTEGER maximum over the same set must come
out at 5, which is the exhaustively established z_max(6). If it does not, the
enumeration is wrong and the real number is not reported.
"""
import os
import sys
import time

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import census_polynomials, last_gate_scan, integer_roots

x = sp.Symbol("x")


def distinct_real_roots(coeffs):
    if not coeffs or all(c == 0 for c in coeffs):
        return None
    p = sp.Poly(list(reversed(coeffs)), x, domain="ZZ")
    if p.degree() < 1:
        return 0
    p = p.quo(sp.Poly(sp.gcd(p, p.diff(x)), x, domain="ZZ"))
    if p.degree() < 1:
        return 0
    return int(p.count_roots())


t0 = time.time()
per_depth, first_seen, complete, frontier = census_polynomials(5, return_frontier=True)
print(f"depth-5 frontier: {len(frontier):,} states, "
      f"{len(first_seen):,} known polys  ({time.time()-t0:.0f}s)", flush=True)

t1 = time.time()
new6, complete6, scanned = last_gate_scan(frontier, set(first_seen))
print(f"depth-6 scan: {len(new6):,} new polynomials from {scanned:,} states, "
      f"complete={complete6}  ({time.time()-t1:.0f}s)", flush=True)

# --- known-answer gate on the integer side --------------------------------
zint = 0
for p in new6:
    n = len(integer_roots(p))
    if n > zint:
        zint = n
print(f"GATE: max distinct INTEGER roots at tau = 6 -> {zint} (must be 5)", flush=True)
if zint != 5:
    print("GATE FAILED; not reporting the real number")
    sys.exit(1)
print("gate passed\n", flush=True)

t2 = time.time()
best, bp = -1, None
for i, p in enumerate(new6):
    n = distinct_real_roots(p)
    if n is not None and n > best:
        best, bp = n, p
    if (i + 1) % 20000 == 0:
        print(f"    {i+1:,}/{len(new6):,}  best so far {best}  "
              f"({time.time()-t2:.0f}s)", flush=True)

print()
print(f"zRmax(6) = {best}")
print(f"witness  = {bp}")
print(f"degree   = {len(bp)-1}, distinct integer roots = {sorted(integer_roots(bp))}")
print()
print("ladders:  tau      1  2  3  4  5  6")
print("          Z        1  2  3  3  4  5")
print(f"          R        1  2  3  4  6  {best}")
print("          F_p      1  2  4  8 16 32")
print(f"\ntotal {time.time()-t0:.0f}s")
