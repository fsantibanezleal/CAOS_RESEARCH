"""TCB-030: measure polynomial HEIGHT (max |coefficient|) against root count
across every census record we have stored. Cheap proxy for the V11
evaluation-matrix question: does killing more columns at once force
larger intermediate magnitudes?"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "code"))
from tclib.enum import census_polynomials, integer_roots

def H(p):
    return max(abs(c) for c in p) if p else 0

rows = []
# depths 1..5 from a fresh census (cheap), grouped by z
per_depth, first_seen, complete = census_polynomials(5)
best = {}
for p, d in first_seen.items():
    z = len(integer_roots(p))
    key = (d, z)
    if key not in best or H(p) < H(best[key]):
        best[key] = p
for (d, z), p in sorted(best.items()):
    if z >= 2:
        rows.append((d, z, H(p), list(p)))

# five-rooters at tau <= 7 (EXP-007) and six-rooters at tau = 8 (EXP-006)
E = HERE.parent / "experiments"
five = json.loads((E / "EXP-007-union7-and-digit-census/artifacts/union7.json").read_text("utf-8"))
fp = [tuple(p) for p in five["fiverooter_polys"]]
rows.append(("<=7", 5, min(H(p) for p in fp), "min over %d five-rooters" % len(fp)))
six = json.loads((E / "EXP-006-window-89/artifacts/window.json").read_text("utf-8"))
from tclib.enum import pmul
sp = [pmul(tuple(h["v"]), tuple(h["b"])) for h in six["times_case_hits"]]
rows.append((8, 6, min(H(p) for p in sp), "min over %d six-rooters" % len(sp)))

print(f"{'tau':>5} {'z':>3} {'minH':>8}   witness/note")
for d, z, h, w in rows:
    print(f"{str(d):>5} {z:>3} {h:>8}   {w}")
