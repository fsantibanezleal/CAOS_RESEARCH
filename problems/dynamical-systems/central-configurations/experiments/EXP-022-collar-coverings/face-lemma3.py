"""Lemma piece 10, combined branches: the loci that actually failed.

cb1's failures: ssig = 0 AND d2A = 2 (equidistance with body 2's mirror).
cb1f's failures: ssig = 0 AND u -> 0 (but u = 0 is a collision: excluded;
so we test u small but positive, the stratum side).
Also the pairwise intersections of the three stratum-relevant branches.
"""
import mpmath as mp
import importlib.util
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("fl", HERE / "face-lemma2.py")
src = (HERE / "face-lemma2.py").read_text(encoding="utf-8")
ns = {"__file__": str(HERE / "face-lemma2.py")}
exec(src.split('print("A.')[0], ns)
at, det3, MENU = ns["at"], ns["det3"], None
MENU = [((a, b, c), (x, y, z))
        for a in range(6) for b in range(a + 1, 6) for c in range(b + 1, 6)
        for x in range(4) for y in range(x + 1, 4) for z in range(y + 1, 4)]
mp.mp.dps = 50

def survivor(u, v, cg, sg, label):
    best = None
    for rows, cols in MENU:
        try:
            v4 = det3(at(u, v, cg, sg, mp.mpf(10) ** -4), rows, cols)
            v6 = det3(at(u, v, cg, sg, mp.mpf(10) ** -6), rows, cols)
        except Exception:
            continue
        if v4 == 0 or abs(v6) < mp.mpf(10) ** -8:
            continue
        ratio = abs(v6 / v4)
        if 0.2 < ratio < 5:                      # order 0 in rhoc
            if best is None or abs(v6) > abs(best[1]):
                best = ((rows, cols), v6, 0)
        elif 50 < ratio < 200:                   # order -1 (grows) : also fine
            if best is None:
                best = ((rows, cols), v6, -1)
    if best:
        print(f"  {label:44s} -> {best[0][0]}x{best[0][1]} "
              f"limit {mp.nstr(best[1], 6)} (order {best[2]})")
    else:
        print(f"  {label:44s} -> NO surviving minor")

# equidistance d2A = 2: u^2 + (1+v)^2 = 4, pick u = 1 => 1+v = sqrt3
u1 = mp.mpf(1); v1 = mp.sqrt(3) - 1
print("combined branches (all with u > 0, p > 0: inside the stratum):")
survivor(u1, v1, mp.mpf(1), mp.mpf(0), "ssig=0 AND d2A=2 (the cb1 failure)")
survivor(mp.mpf(1)/1000, mp.mpf(-3), mp.mpf(1), mp.mpf(0), "ssig=0 AND u small (the cb1f failure)")
survivor(mp.mpf(1)/100000, mp.mpf(-3), mp.mpf(1), mp.mpf(0), "ssig=0 AND u tiny")
gam_eq = mp.mpf(-1)
survivor(mp.mpf(3)/2, gam_eq, mp.mpf(1), mp.mpf(0), "ssig=0 AND v=-1")
# d2A = 2u with ssig = 0
uu = mp.mpf(1)
vv = -1 - mp.sqrt(3) * uu
survivor(uu, vv, mp.mpf(1), mp.mpf(0), "ssig=0 AND d2A=2u")
