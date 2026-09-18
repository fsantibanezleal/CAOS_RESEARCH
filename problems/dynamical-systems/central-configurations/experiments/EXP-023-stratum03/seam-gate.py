"""Seam gate for the (0,3) compact atlas, with negative controls.

The compact gauge is: translation v1 = 0, scale
max(u1, u2, u3, |v2|, |v3|) = 1. Five charts claim the cases where the
maximum is attained by u1, u2, u3, |v2| or |v3|. This gate samples
configurations, normalises them into the gauge, and asks whether each is
claimed by at least one chart AND kept (not discarded to a face chart).

As in EXP-022's atlas gate, the controls matter more than the pass:
dropping any single chart must OPEN a gap, otherwise the predicates are
too permissive to be evidence of anything.
"""
import random
from fractions import Fraction as F

SIXT = F(1, 16)

def normalise(u, v):
    """translation v1 = 0 then scale so the largest coordinate is 1."""
    v = [x - v[0] for x in v]
    m = max([abs(x) for x in u] + [abs(x) for x in v])
    if m == 0:
        return None
    return [x / m for x in u], [x / m for x in v]

def collision(u, v):
    """is this configuration inside a collision neighbourhood?"""
    for x in u:
        if x < SIXT:
            return True
    for a in range(3):
        for b in range(a + 1, 3):
            if abs(u[a] - u[b]) < SIXT and abs(v[a] - v[b]) < SIXT:
                return True
    return False

def charts_claiming(u, v, drop=None):
    out = []
    if u[0] == 1: out.append("U1")
    if u[1] == 1: out.append("U2")
    if u[2] == 1: out.append("U3")
    if abs(v[1]) == 1: out.append("V2")
    if abs(v[2]) == 1: out.append("V3")
    if drop:
        out = [c for c in out if c != drop]
    return out

def run(n, drop=None, seed=99, verbose=True):
    rnd = random.Random(seed)
    gaps = tested = skipped = 0
    for _ in range(n):
        u = [F(rnd.randint(1, 400), 64) for _ in range(3)]
        v = [F(rnd.randint(-400, 400), 64) for _ in range(3)]
        r = normalise(u, v)
        if r is None:
            continue
        un, vn = r
        if collision(un, vn):
            skipped += 1
            continue                     # face charts own it
        tested += 1
        if not charts_claiming(un, vn, drop):
            gaps += 1
    if verbose:
        tag = "full atlas" if drop is None else f"atlas MINUS {drop}"
        print(f"  {tag:18s} tested {tested:6d}  (collision-skipped {skipped:6d})  GAPS {gaps}")
    return tested, gaps

print("(0,3) compact-atlas seam gate")
t, g = run(60000)
print()
print("negative controls (dropping a chart must open a gap):")
bad = []
for c in ("U1", "U2", "U3", "V2", "V3"):
    t2, g2 = run(60000, drop=c, verbose=False)
    status = "gap opens (OK)" if g2 > 0 else "NO GAP: predicate too permissive"
    print(f"   drop {c}: {g2:6d} unclaimed   {status}")
    if g2 == 0:
        bad.append(c)
print()
print("VERDICT:", "atlas covers the sample" if g == 0 else f"{g} GAPS in the full atlas",
      "|", "all controls fired" if not bad else f"NOT DISCRIMINATING for {bad}")
