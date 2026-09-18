"""The RATIONAL ladder: is the conjecture's difficulty integrality, or rationality?

The Shub-Smale conjecture counts INTEGER roots. The natural algebraic relaxation
counts rational ones. If zQmax(tau) tracks zmax(tau), then integrality adds
nothing beyond rationality and the hard part is already visible over Q. If it
runs ahead, then integrality itself is doing work.

Rational roots are computed exactly by sympy's ground_roots (rational root
theorem over ZZ), never numerically. The run carries a known-answer gate: the
INTEGER maximum recomputed on the same enumerated set must reproduce the
established census.
"""
import os
import sys
import time

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import census_polynomials, last_gate_scan, integer_roots

x = sp.Symbol("x")
DEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 5
ZMAX = {1: 1, 2: 2, 3: 3, 4: 3, 5: 4, 6: 5}
t0 = time.time()

if DEPTH <= 5:
    per, first_seen, comp = census_polynomials(DEPTH)
    groups = {}
    for p, t in first_seen.items():
        if p:
            groups.setdefault(t, []).append(p)
else:
    per, first_seen, comp, frontier = census_polynomials(5, return_frontier=True)
    new6, comp6, scanned = last_gate_scan(frontier, set(first_seen))
    groups = {}
    for p, t in first_seen.items():
        if p:
            groups.setdefault(t, []).append(p)
    groups[6] = [p for p in new6 if p]
    print(f"depth-6 via last-gate lemma: {len(groups[6]):,} new polynomials, "
          f"complete={comp6}", flush=True)

print(f"census ready ({time.time()-t0:.0f}s)", flush=True)
print()
print(f"{'tau':>4} {'polys':>9} {'zmax(Z)':>8} {'zQmax(Q)':>9} {'gate':>6}  rational witness")
print("-" * 92)
rows = []
for tau in sorted(groups):
    ps = groups[tau]
    zi = 0
    zq, wq = 0, None
    for p in ps:
        n = len(integer_roots(p))
        if n > zi:
            zi = n
    for p in ps:
        if len(p) - 1 < zq:          # cannot beat the record on degree alone
            continue
        g = sp.Poly(list(reversed(p)), x, domain="ZZ").ground_roots()
        if len(g) > zq:
            zq, wq = len(g), p
    gate = "ok" if zi == ZMAX.get(tau) else "GATE FAIL"
    rows.append((tau, zi, zq))
    w = str(wq)
    print(f"{tau:>4} {len(ps):>9,} {zi:>8} {zq:>9} {gate:>6}  "
          f"{w if len(w) < 36 else w[:33] + '...'}")

print()
print("ladders:")
print("  tau        " + " ".join(f"{r[0]:>3}" for r in rows))
print("  Z          " + " ".join(f"{r[1]:>3}" for r in rows))
print("  Q          " + " ".join(f"{r[2]:>3}" for r in rows))
if all(r[1] == r[2] for r in rows):
    print("\n  Q == Z throughout: rationality alone already forces the integer ladder.")
else:
    print("\n  Q exceeds Z somewhere: integrality is doing work beyond rationality.")
print(f"\n{time.time()-t0:.0f}s")
