"""The (0,3) outer region is really the ALL-NARROW region.

In the gauge v1 = 0, u1 = 1 (pair A widest), the heights are unbounded, so
a naive reading says the stratum needs inverted charts at infinity. It does
not. Rescale a configuration with |v| ~ V >> 1 by 1/V: the heights become
order 1 and every width becomes u_i/V <= 1/V. So the outer region maps
onto the region where ALL THREE pairs are narrow - a near-collinear
configuration - which is a COLLAPSE-type region, not a new kind of
infinity. The stratum therefore needs no chart at infinity at all, only
one more collapse-style chart.

This probe measures that region: heights normalised (v2 = 1), all three
widths scaled by a common eps, each mass column rescaled by 4 u_i^2 as in
the single-collapse chart. If the face keeps rank 3 the region is clean.
"""
import math, random
from pathlib import Path
import mpmath as mp
mp.mp.dps = 50
HERE = Path(__file__).resolve().parent
src = (HERE / "derive.py").read_text(encoding="utf-8")
ns = {"__file__": str(HERE / "derive.py")}
exec(src.split('rnd = random.Random')[0], ns)
positions, L_coeffs, ROWS = ns["positions"], ns["L_coeffs"], ns["ROWS"]

def s3_of(M):
    A = [[float(x) for x in row] for row in M]
    for i in range(6):
        n = max(abs(x) for x in A[i]) or 1.0
        A[i] = [x / n for x in A[i]]
    G = [[sum(A[k][i]*A[k][j] for k in range(6)) for j in range(3)] for i in range(3)]
    for _ in range(60):
        off = sum(G[i][j]**2 for i in range(3) for j in range(i+1,3))
        if off < 1e-28: break
        for p in range(3):
            for q in range(p+1,3):
                if abs(G[p][q]) < 1e-300: continue
                th = (G[q][q]-G[p][p])/(2*G[p][q])
                t = (1 if th>=0 else -1)/(abs(th)+math.sqrt(th*th+1))
                c = 1/math.sqrt(t*t+1); s = t*c
                for k in range(3):
                    x,y = G[k][p],G[k][q]; G[k][p],G[k][q] = c*x-s*y, s*x+c*y
                for k in range(3):
                    x,y = G[p][k],G[q][k]; G[p][k],G[q][k] = c*x-s*y, s*x+c*y
    return sorted((max(G[i][i],0.0)**0.5 for i in range(3)), reverse=True)[2]

rnd = random.Random(23)
def rr(a, b, den=64):
    return mp.mpf(rnd.randint(int(a*den)+1, int(b*den)-1)) / den

print("all three pairs narrow: u_i = eps * c_i, heights order 1")
print("(each mass column rescaled by 4 u_i^2, the single-collapse recipe)")
for e_pow in (2, 4, 6):
    eps = mp.mpf(10) ** (-e_pow)
    vals = []
    for _ in range(30):
        c1, c2, c3 = rr(0.3, 1.0), rr(0.3, 1.0), rr(0.3, 1.0)
        v2, v3 = mp.mpf(1), rr(-0.95, 0.95)
        if abs(v3) < mp.mpf(1)/8 or abs(v3 - 1) < mp.mpf(1)/8:
            continue
        u1, u2, u3 = eps * c1, eps * c2, eps * c3
        P = positions(u1, mp.mpf(0), u2, v2, u3, v3)
        M = [L_coeffs(P, i, j) for (i, j) in ROWS]
        cs = [4 * u1**2, 4 * u2**2, 4 * u3**2]
        M = [[M[i][j] * cs[j] for j in range(3)] for i in range(6)]
        vals.append(s3_of(M))
    vals.sort()
    if vals:
        print(f"   eps=1e-{e_pow}: min sigma3 {vals[0]:.4e}  median {vals[len(vals)//2]:.4e}  n={len(vals)}")
