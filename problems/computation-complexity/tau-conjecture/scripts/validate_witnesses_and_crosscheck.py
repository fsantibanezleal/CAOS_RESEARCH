"""Re-run the independent root-counter cross-check, and replay the stored witnesses.

Three things the earlier passes took on trust from prior runs:
  1. the SymPy cross-check on 284 polynomials (recorded in EXP-003's verdict);
  2. that all 50 stored 8-gate six-rooters really do have six distinct roots;
  3. that the minimal height among six-rooters really is 15.
"""
import json
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import census_polynomials, integer_roots, pmul

x = sp.Symbol("x")
FAIL = []


def sympy_int_roots(coeffs):
    """Independent counter: SymPy's exact factorization over ZZ."""
    if not coeffs or all(c == 0 for c in coeffs):
        return None
    p = sp.Poly(list(reversed(coeffs)), x, domain="ZZ")
    if p.degree() < 1:
        return set()
    return {r for r in p.ground_roots() if r.is_Integer}


# ---- 1. cross-check tclib against SymPy -----------------------------------
print("== Independent cross-check: tclib vs SymPy ==")
per, first_seen, comp = census_polynomials(5)
pool = [p for p, t in first_seen.items() if p and t <= 3]          # all tau <= 3
records = {}
for p, t in first_seen.items():
    if not p:
        continue
    n = len(integer_roots(p))
    if n >= records.get(t, (0,))[0]:
        records[t] = (n, p)
pool += [v[1] for v in records.values()]
# add every stored witness we have on disk
wf = "experiments/EXP-006-window-89/artifacts/window.json"
if os.path.exists(wf):
    for h in json.load(open(wf))["times_case_hits"]:
        pool.append(tuple(pmul(tuple(h["v"]), tuple(h["b"]))))
pool = list({tuple(p) for p in pool})

mismatch = 0
for p in pool:
    a = set(integer_roots(p))
    b = sympy_int_roots(p)
    if b is None:
        continue
    if a != {int(v) for v in b}:
        mismatch += 1
        if mismatch <= 3:
            print(f"  MISMATCH on {p}: tclib={sorted(a)} sympy={sorted(b)}")
print(f"  polynomials compared : {len(pool)}")
print(f"  mismatches           : {mismatch}")
if mismatch:
    FAIL.append("sympy cross-check")
else:
    print("  PASS  the two independent counters agree on every polynomial")

# ---- 2 & 3. replay all stored six-rooters ---------------------------------
print()
print("== Stored 8-gate six-rooters: replay and minimal height ==")
if os.path.exists(wf):
    hits = json.load(open(wf))["times_case_hits"]
    heights, bad = [], 0
    sets = set()
    for h in hits:
        f = pmul(tuple(h["v"]), tuple(h["b"]))
        r = sorted(integer_roots(f))
        if len(r) != 6:
            bad += 1
        if r != sorted(h["union_roots"]):
            bad += 1
        sets.add(tuple(r))
        heights.append(max(abs(c) for c in f))
    print(f"  witnesses replayed   : {len(hits)}")
    print(f"  disagreements        : {bad}")
    print(f"  distinct root sets   : {len(sets)} -> {sorted(sets)[:3]}")
    print(f"  minimal height       : {min(heights)}   (manuscript claims 15)")
    if bad:
        FAIL.append("six-rooter replay")
    if min(heights) != 15:
        FAIL.append("minimal height 15")
    if not bad and min(heights) == 15:
        print("  PASS  all replay to six roots, and the minimum height is 15")

print()
print("FAILURES:", FAIL if FAIL else "none")
sys.exit(1 if FAIL else 0)
