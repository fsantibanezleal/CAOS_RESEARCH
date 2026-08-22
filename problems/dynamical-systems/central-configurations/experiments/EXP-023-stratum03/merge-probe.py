"""Does a tube-style row rescale make the (0,3) merge face full rank?

Merge F3: pair B and pair C come together, (u2,v2) -> (u3,v3). Write the
midpoint w and the difference (u2-u3, v2-v3) = rho (alpha, beta), so the
B+C+ distance is exactly rho. Rows whose mass coefficients contain a
1/rho^3 term blow up; the areas spanning B+ and C+ vanish to first order,
so the product goes like 1/rho^2 and multiplying those rows by rho^2 is
the natural cure (exactly tube.py's recipe in EXP-022).

This probe measures which rows blow up, at what order, and whether the
rescaled face keeps rank 3.
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
NAMES = ["L13", "L14", "L15", "L16", "L35", "L36"]

def geom(rho, wu, wv, tau):
    o = 1 + tau * tau
    al, be = (1 - tau * tau) / o, 2 * tau / o
    u2 = wu + rho * al / 2; v2 = wv + rho * be / 2
    u3 = wu - rho * al / 2; v3 = wv - rho * be / 2
    return mp.mpf(1), mp.mpf(0), u2, v2, u3, v3

def M_at(rho, wu, wv, tau):
    P = positions(*geom(rho, wu, wv, tau))
    return [L_coeffs(P, i, j) for (i, j) in ROWS]

rnd = random.Random(4)
def rr(a, b, den=64):
    return mp.mpf(rnd.randint(int(a*den)+1, int(b*den)-1)) / den

print("A. row orders in rho at the B/C merge (|row| ratio over rho ratio 16)")
wu, wv, tau = mp.mpf(1)/2, mp.mpf(3)/4, mp.mpf(1)/3
mags = []
for k in range(3):
    rho = mp.mpf(1) / (16 ** (k + 1))
    M = M_at(rho, wu, wv, tau)
    mags.append([max(abs(x) for x in row) for row in M])
for i in range(6):
    a, b = mags[0][i], mags[2][i]
    o = math.log(float(a / b)) / math.log(256.0)
    print(f"   {NAMES[i]}: {float(a):.3e} -> {float(b):.3e}   order ~ {-o:+.2f}")

def s3(M, rowscale):
    A = [[float(M[i][j] * rowscale[i]) for j in range(3)] for i in range(6)]
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

print("\nB. sigma_3 with rows normalised (i.e. after ANY row rescale)")
for e_pow in (3, 5, 7):
    rho = mp.mpf(10) ** (-e_pow)
    vals = []
    for _ in range(30):
        wu2, wv2, tv = rr(0.15, 0.9), rr(-2.5, 2.5), rr(-0.9, 0.9)
        try:
            M = M_at(rho, wu2, wv2, tv)
            vals.append(s3(M, [mp.mpf(1)] * 6))
        except Exception:
            pass
    vals.sort()
    if vals:
        print(f"   rho=1e-{e_pow}: min sigma3 {vals[0]:.4e}  median {vals[len(vals)//2]:.4e}  n={len(vals)}")
