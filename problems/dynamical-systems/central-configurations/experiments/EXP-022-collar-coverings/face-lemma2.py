"""Lemma piece 10 (verified numerically-exactly): the corner-face rank floor.

Hand derivation, using the exact clearings (substitute-first; symbolic
radical limits hang):

  d2B^2 - 4 = rhoc (4 ssig + rhoc)  =>  s(r12, d2B) = rhoc (4 ssig + rhoc) G,
      G = (d2B^2 + 2 d2B + 4) / ((d2B + 2) 8 d2B^3),  G(rhoc=0) = 3/64.
  (L15, m2) = -2 p s(r12, d2B) = -2 rhoc^2 csig (4 ssig + rhoc) G
            = -(3/8) rhoc^2 csig ssig + O(rhoc^3).
  (L25, m1) = 2 p s(r12, d1B) = 2 rhoc csig (1/8 - rhoc^-3)
            = -2 csig rhoc^-2 + O(rhoc).
  (L25, mA) -> 0 as rhoc -> 0  (at rhoc = 0: cs = cx = d1A and the two
      brackets are +-2u, so the two s-terms cancel exactly).
  (L23, m1) = 2u s(r12, d1A) = O(1);  (L23, mA) = -2u gam s(d2A, wA) = O(1).

Hence for M = det[{L15,L23,L25} x {m1,m2,mA}] = -(L15,m2) * [(L23,m1)(L25,mA)
- (L23,mA)(L25,m1)]:

  M  ->  C  :=  -(3/2) * u * gam * csig^2 * ssig * s(d2A, 2u)     (order 0)

with gam = -1 - v and s(d2A, 2u) = 1/d2A^3 - 1/(2u)^3. So rank >= 3 holds
UNIFORMLY for all small rhoc > 0 wherever C != 0, i.e. off the five
hypersurfaces
     u = 0,  v = -1,  csig = 0,  ssig = 0,  d2A = 2u.
This script verifies C by exact rational evaluation at shrinking rhoc, and
then, ON each branch, searches the 80-minor menu for a second minor whose
own rhoc-limit is nonzero (the branch table).
"""
from fractions import Fraction as F
import mpmath as mp

mp.mp.dps = 50

def J_orig(u, v, p, q):
    h1 = 1 - v; gam = -1 - v; g1 = 1 - q; g2 = -1 - q; f = v - q
    d1A = mp.sqrt(u**2 + h1**2); d2A = mp.sqrt(u**2 + gam**2)
    d1B = mp.sqrt(p**2 + g1**2); d2B = mp.sqrt(p**2 + g2**2)
    cs = mp.sqrt((u - p)**2 + f**2); cx = mp.sqrt((u + p)**2 + f**2)
    wA = 2 * u; wB = 2 * p; r12 = mp.mpf(2)
    s = lambda a, b: a**-3 - b**-3
    J = [[mp.mpf(0)] * 4 for _ in range(6)]
    J[0][1] = s(r12, d2A) * (-2 * u); J[0][2] = s(d1A, wA) * (-2 * u * h1)
    J[0][3] = s(d1B, cs) * (p * h1 - u * g1) + s(d1B, cx) * (-(u * g1 + p * h1))
    J[1][1] = s(r12, d2B) * (-2 * p)
    J[1][2] = s(d1A, cs) * (u * g1 - p * h1) + s(d1A, cx) * (-(p * h1 + u * g1))
    J[1][3] = s(d1B, wB) * (-2 * p * g1)
    J[2][0] = s(r12, d1A) * (2 * u); J[2][2] = s(d2A, wA) * (-2 * u * gam)
    J[2][3] = s(d2B, cs) * (p * gam - u * g2) + s(d2B, cx) * (-(u * g2 + p * gam))
    J[3][0] = s(r12, d1B) * (2 * p)
    J[3][2] = s(d2A, cs) * (u * g2 - p * gam) + s(d2A, cx) * (-(p * gam + u * g2))
    J[3][3] = s(d2B, wB) * (-2 * p * g2)
    J[4][0] = s(d1A, d1B) * (p * h1 - u * g1); J[4][1] = s(d2A, d2B) * (p * gam - u * g2)
    J[4][2] = s(wA, cx) * (-2 * f * u); J[4][3] = s(cx, wB) * (-2 * f * p)
    J[5][0] = s(d1A, d1B) * (-(u * g1 + p * h1)); J[5][1] = s(d2A, d2B) * (-(u * g2 + p * gam))
    J[5][2] = s(wA, cs) * (-2 * f * u); J[5][3] = s(cs, wB) * (2 * f * p)
    return J

def det3(J, rows, cols):
    a, b, c = rows; x, y, z = cols
    return (J[a][x] * (J[b][y] * J[c][z] - J[b][z] * J[c][y])
            - J[a][y] * (J[b][x] * J[c][z] - J[b][z] * J[c][x])
            + J[a][z] * (J[b][x] * J[c][y] - J[b][y] * J[c][x]))

def at(u, v, csig, ssig, rhoc):
    p = rhoc * csig
    q = 1 + rhoc * ssig
    return J_orig(u, v, p, q)

def C_pred(u, v, csig, ssig):
    gam = -1 - v
    d2A = mp.sqrt(u**2 + gam**2)
    s = lambda a, b: a**-3 - b**-3
    return mp.mpf(-3) / 2 * u * gam * csig**2 * ssig * s(d2A, 2 * u)

print("A. the O(1) limit of M = det[{L15,L23,L25} x {m1,m2,mA}] vs the")
print("   predicted C = -(3/2) u gam csig^2 ssig s(d2A, 2u):")
CASES = [(mp.mpf(3)/2, mp.mpf(1)/3, mp.mpf(3)/5, mp.mpf(4)/5),
         (mp.mpf(1)/2, -mp.mpf(2)/3, mp.mpf(12)/13, mp.mpf(5)/13),
         (mp.mpf(9)/4, mp.mpf(7)/4, mp.mpf(8)/17, mp.mpf(15)/17)]
for (u, v, cg, sg) in CASES:
    pred = C_pred(u, v, cg, sg)
    row = []
    for e in (3, 5, 7):
        rc = mp.mpf(10) ** (-e)
        M = det3(at(u, v, cg, sg, rc), (1, 2, 3), (0, 1, 2))
        row.append(M)
    print(f"  u={float(u):.3f} v={float(v):+.3f} csig={float(cg):.3f}: "
          f"M(1e-3)={mp.nstr(row[0],8)} M(1e-5)={mp.nstr(row[1],8)} "
          f"M(1e-7)={mp.nstr(row[2],8)}  C={mp.nstr(pred,8)}")

print("\nB. branch table: on each zero-branch of C, the best surviving minor")
MENU = [((a, b, c), (x, y, z))
        for a in range(6) for b in range(a + 1, 6) for c in range(b + 1, 6)
        for x in range(4) for y in range(x + 1, 4) for z in range(y + 1, 4)]
BRANCHES = [
    ("ssig = 0  (B displaced horizontally)", mp.mpf(3)/2, mp.mpf(1)/3, mp.mpf(1), mp.mpf(0)),
    ("csig = 0  (B displaced vertically)", mp.mpf(3)/2, mp.mpf(1)/3, mp.mpf(0), mp.mpf(1)),
    ("u = 0     (pair A on the axis)", mp.mpf(0), mp.mpf(1)/3, mp.mpf(3)/5, mp.mpf(4)/5),
    ("v = -1    (A at body 2 height)", mp.mpf(3)/2, mp.mpf(-1), mp.mpf(3)/5, mp.mpf(4)/5),
    ("d2A = 2u  (equidistance)", mp.sqrt(mp.mpf(4)/3)/1, mp.mpf(-1) - mp.sqrt(mp.mpf(4)/3)*mp.sqrt(3),
     mp.mpf(3)/5, mp.mpf(4)/5),
]
for label, u, v, cg, sg in BRANCHES:
    best = None
    for rows, cols in MENU:
        vals = []
        ok = True
        for e in (4, 6):
            rc = mp.mpf(10) ** (-e)
            try:
                d = det3(at(u, v, cg, sg, rc), rows, cols)
            except Exception:
                ok = False
                break
            vals.append(d)
        if not ok or vals[0] == 0:
            continue
        ratio = abs(vals[1] / vals[0]) if vals[0] != 0 else 0
        # keep minors whose value STABILISES (order 0) and is not tiny
        if 0.2 < ratio < 5 and abs(vals[1]) > mp.mpf(10) ** -6:
            if best is None or abs(vals[1]) > abs(best[1]):
                best = ((rows, cols), vals[1])
    if best:
        print(f"  {label:38s} -> minor {best[0][0]}x{best[0][1]} "
              f"limit {mp.nstr(best[1], 6)}")
    else:
        print(f"  {label:38s} -> NO order-0 minor found")
