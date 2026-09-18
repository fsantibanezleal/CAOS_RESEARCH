"""Extend the degree-bound check behind the F_p upper bound to tau = 6.

The proof of zpmax(tau) <= 2^(tau-1) rests on: a NON-MONOMIAL tau-gate
polynomial has at most tau-1 multiplicative gates, hence degree at most
2^(tau-1). That was checked on the depth-5 census. This checks it on every
tau = 6 polynomial too, via the last-gate lemma, and reports whether the bound
is attained.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import census_polynomials, last_gate_scan, integer_roots

t0 = time.time()
per_depth, first_seen, complete, frontier = census_polynomials(5, return_frontier=True)
new6, complete6, scanned = last_gate_scan(frontier, set(first_seen))
print(f"depth-6: {len(new6):,} new polynomials, complete={complete6} "
      f"({time.time()-t0:.0f}s)")

# gate: the integer maximum on this set must be 5
zint = max(len(integer_roots(p)) for p in new6)
print(f"GATE: max distinct integer roots at tau = 6 -> {zint} (must be 5)")
assert zint == 5, "enumeration gate failed"

by_tau = {}
for p, t in first_seen.items():
    if p:
        by_tau.setdefault(t, []).append(p)
by_tau[6] = [p for p in new6 if p]

print()
print(f"{'tau':>4} {'polys':>9} {'max deg (all)':>14} {'max deg (non-mono)':>19} "
      f"{'2^(tau-1)':>10}  verdict")
print("-" * 84)
ok = True
for tau in sorted(by_tau):
    ps = by_tau[tau]
    md_all = max(len(p) - 1 for p in ps)
    nm = [p for p in ps if sum(1 for c in p if c) > 1]
    md_nm = max((len(p) - 1 for p in nm), default=0)
    cap = 2 ** (tau - 1)
    good = md_nm <= cap
    ok = ok and good
    print(f"{tau:>4} {len(ps):>9,} {md_all:>14} {md_nm:>19} {cap:>10}  "
          f"{'ok' if good else 'VIOLATION'}"
          f"{' (attained)' if md_nm == cap else ''}")

print()
print("degree bound holds on every non-monomial through tau = 6:", ok)
print(f"total {time.time()-t0:.0f}s")
