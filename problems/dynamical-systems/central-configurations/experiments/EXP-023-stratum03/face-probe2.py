"""Do the standard rescalings restore rank on the (0,3) faces?

Recipe from EXP-022: a collapsing pair's mass column is multiplied by
4 u_i^2 (clearing the 1/w_i^3 self-interaction), and if the OTHER mass
columns then vanish they are divided by the collapse parameter (piece 11).
This probe measures the resulting face rank in high precision, in the
ORIGINAL coordinates approached along each face, so the chart design is
decided by measurement rather than guess.
"""
import importlib.util, math, random
from pathlib import Path
import mpmath as mp
mp.mp.dps = 50
HERE = Path(__file__).resolve().parent
src = (HERE / "derive.py").read_text(encoding="utf-8")
ns = {"__file__": str(HERE / "derive.py")}
exec(src.split('rnd = random.Random')[0], ns)
positions, L_coeffs, ROWS = ns["positions"], ns["L_coeffs"], ns["ROWS"]

def matrix(u1, v1, u2, v2, u3, v3, colscale):
    P = positions(u1, v1, u2, v2, u3, v3)
    M = [L_coeffs(P, i, j) for (i, j) in ROWS]
    return [[M[i][j] * colscale[j] for j in range(3)] for i in range(6)]

def rank_and_s3(M, tol=mp.mpf(10)**-30):
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
                    a,b = G[k][p],G[k][q]; G[k][p],G[k][q] = c*a-s*b, s*a+c*b
                for k in range(3):
                    a,b = G[p][k],G[q][k]; G[p][k],G[q][k] = c*a-s*b, s*a+c*b
    ev = sorted((max(G[i][i],0.0)**0.5 for i in range(3)), reverse=True)
    return ev

rnd = random.Random(101)
def rr(a,b,den=64): return mp.mpf(rnd.randint(int(a*den)+1,int(b*den)-1))/den

print("F1: pair B collapsing (u2 -> 0), mB column x 4 u2^2")
for e_pow in (3, 5, 7):
    eps = mp.mpf(10)**(-e_pow); vals=[]
    for _ in range(30):
        u3, v2, v3 = rr(0.1,0.95), rr(-2.9,2.9), rr(-2.9,2.9)
        M = matrix(mp.mpf(1), mp.mpf(0), eps, v2, u3, v3,
                   [mp.mpf(1), 4*eps**2, mp.mpf(1)])
        vals.append(rank_and_s3(M)[2])
    vals.sort()
    print(f"   eps=1e-{e_pow}: min sigma3 {vals[0]:.4e}  median {vals[len(vals)//2]:.4e}")

print("\nF1 with the mA and mC columns ALSO divided by u2 (piece 11 mechanism)")
for e_pow in (3, 5, 7):
    eps = mp.mpf(10)**(-e_pow); vals=[]
    for _ in range(30):
        u3, v2, v3 = rr(0.1,0.95), rr(-2.9,2.9), rr(-2.9,2.9)
        M = matrix(mp.mpf(1), mp.mpf(0), eps, v2, u3, v3,
                   [1/eps, 4*eps**2, 1/eps])
        vals.append(rank_and_s3(M)[2])
    vals.sort()
    print(f"   eps=1e-{e_pow}: min sigma3 {vals[0]:.4e}  median {vals[len(vals)//2]:.4e}")

print("\nF3: pairs B and C merging (B+ -> C+), no rescale")
for e_pow in (3, 5, 7):
    eps = mp.mpf(10)**(-e_pow); vals=[]
    for _ in range(30):
        u2, v2 = rr(0.15,0.9), rr(-2.9,2.9)
        M = matrix(mp.mpf(1), mp.mpf(0), u2, v2, u2+eps, v2+eps,
                   [mp.mpf(1), mp.mpf(1), mp.mpf(1)])
        vals.append(rank_and_s3(M)[2])
    vals.sort()
    print(f"   eps=1e-{e_pow}: min sigma3 {vals[0]:.4e}  median {vals[len(vals)//2]:.4e}")

print("\nF4: pair B merging with pair A (B+ -> A+), no rescale")
for e_pow in (3, 5, 7):
    eps = mp.mpf(10)**(-e_pow); vals=[]
    for _ in range(30):
        u3, v3 = rr(0.15,0.9), rr(-2.9,2.9)
        M = matrix(mp.mpf(1), mp.mpf(0), 1+eps, eps, u3, v3,
                   [mp.mpf(1), mp.mpf(1), mp.mpf(1)])
        vals.append(rank_and_s3(M)[2])
    vals.sort()
    print(f"   eps=1e-{e_pow}: min sigma3 {vals[0]:.4e}  median {vals[len(vals)//2]:.4e}")
