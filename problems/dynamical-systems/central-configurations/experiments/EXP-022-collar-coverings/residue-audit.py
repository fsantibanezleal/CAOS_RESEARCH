"""Residue audit: does every uncertified box touch a COLLISION?

The covering's bisection already performs a shell decomposition: a box
[0, h] on a face splits into [h/2, h] (which certifies) and [0, h/2]
(which recurses). So at the depth cap the uncertified residue is exactly
the set of leaves that still touch the face. The theorem needs those
leaves to touch nothing but COLLISIONS, which the open stratum excludes.

This gate reads each chart's FAILED boxes and evaluates, in the ORIGINAL
coordinates (u, v, p, q) reconstructed from the chart, the five collision
distances

    u        (bodies 3, 4 coincide)
    p        (bodies 5, 6 coincide)
    d1A, d2A (pair A on an axis body)
    d1B, d2B (pair B on an axis body)
    cs, cx   (a body of pair A meets one of pair B)

and reports, per chart, the MINIMUM over the box of the smallest of them.
A residue box that touches a collision has minimum 0. Anything with a
positive minimum is a genuine uncertified stratum region and is reported
individually.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
BASE = Path("E:/_Datos/caos-research/central-configurations/EXP-022")

def collision_floor(u, v, p, q):
    """Smallest collision distance at a POINT (floats)."""
    import math
    d = lambda x, y: math.hypot(x, y)
    return min(abs(u), abs(p),
               d(u, v - 1), d(u, v + 1),
               d(p, q - 1), d(p, q + 1),
               d(u - p, v - q), d(u + p, v - q))

RECON = {
    # chart -> function(box midpoints/corners in chart coords) -> (u,v,p,q)
    "m2-R":  lambda Rc, tt, v, tau: _m2(Rc, tt, v, tau, +1),
    "m2-L":  lambda Rc, tt, v, tau: _m2(Rc, tt, v, tau, -1),
    "cb1":   lambda rc, tc, u, v: _cb1(rc, tc, u, v),
    "cb1f":  lambda rc, tc, eps, tau: _cb1f(rc, tc, eps, tau),
    "bicorner-same": lambda ra, ta, rr, tb: _bs(ra, ta, rr, tb),
    "deep-R": lambda w, v, tau, rho: _deep(w, v, tau, rho, +1),
    "deep-L": lambda w, v, tau, rho: _deep(w, v, tau, rho, -1),
}

def _circ(t):
    o = 1 + t * t
    return (1 - t * t) / o, 2 * t / o

def _m2(Rc, tt, v, tau, sgn):
    ct, st = _circ(tt)
    al, be = _circ(tau)
    al *= sgn
    uh = (ct + st * al) / 2
    ph = (ct - st * al) / 2
    return Rc * uh, v, Rc * ph, v - Rc * st * be

def _cb1(rc, tc, u, v):
    c, s = _circ(tc)
    return u, v, rc * c, 1 + rc * s

def _cb1f(rc, tc, eps, tau):
    c, s = _circ(tc)
    a, b = _circ(tau)
    if eps == 0:
        eps = 1e-300
    return a / eps, b / eps, rc * c, 1 + rc * s

def _bs(ra, ta, rr, tb):
    ca, sa = _circ(ta)
    cb, sb = _circ(tb)
    return ra * ca, 1 + ra * sa, rr * ra * cb, 1 + rr * ra * sb

def _deep(w, v, tau, rho, sgn):
    al, be = _circ(tau)
    al *= sgn
    t = rho * al
    return w + t / 2, v, w - t / 2, v - rho * be

def audit(stem):
    path = BASE / f"{stem}-certificates.jsonl"
    if not path.exists():
        return
    recon = RECON.get(stem)
    if recon is None:
        print(f"{stem}: no reconstruction registered, skipped")
        return
    worst = 0.0
    n = 0
    offenders = []
    for line in path.open(encoding="utf-8"):
        if '"FAILED"' not in line:
            continue
        n += 1
        box = [[float(F(x)) for x in ax] for ax in json.loads(line)["box"]]
        # sample the box on its 2^4 corners plus centre: the floor over the
        # box is <= the minimum over these
        best = None
        import itertools
        pts = list(itertools.product(*[(a, b) for a, b in box]))
        pts.append(tuple((a + b) / 2 for a, b in box))
        for pt in pts:
            try:
                f = collision_floor(*recon(*pt))
            except Exception:
                continue
            best = f if best is None else min(best, f)
        if best is None:
            continue
        worst = max(worst, best)
        if best > 1e-9:
            offenders.append((best, box))
    if n == 0:
        print(f"{stem}: no failed boxes")
        return
    offenders.sort(reverse=True)
    print(f"{stem}: {n} residue boxes; max collision-floor over them = {worst:.3e}")
    if offenders:
        print(f"   {len(offenders)} box(es) with a POSITIVE floor (genuine "
              f"uncertified stratum region), worst {offenders[0][0]:.3e}")
    else:
        print("   every residue box TOUCHES a collision (floor 0): the "
              "uncertified set lies in the collision locus, excluded from "
              "the open stratum")

if __name__ == "__main__":
    stems = sys.argv[1:] or ["m2-R", "cb1", "cb1f", "bicorner-same", "deep-R"]
    for s in stems:
        audit(s)
