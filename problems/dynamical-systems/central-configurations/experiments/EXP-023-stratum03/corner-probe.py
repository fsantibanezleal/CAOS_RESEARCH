"""Is the mergeBC corner a rank-2 locus, or just the DFS corner?

The failures track the box corner wherever it is put, which suggests the
covering is failing at its own domain corner rather than on any feature.
This checks directly: singular values of the merge-chart matrix at the
failing corner, and at INTERIOR (wu, wv) scanning tau for a degeneracy.
If a genuine rank-2 curve exists in this chart it is part of the locus
where this stratum's central configurations live.
"""
import importlib.util, math
from pathlib import Path
from fractions import Fraction as F
HERE = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location("mg", HERE / "mergeBC.py")
mg = importlib.util.module_from_spec(s); s.loader.exec_module(mg)
cov = mg.cov
eiv = mg.entry_factory("iv")

def svals(rho, tau, wu, wv):
    J = eiv([(rho, rho), (tau, tau), (wu, wu), (wv, wv)])
    A = [[float((J[i][j].lo + J[i][j].hi) / 2) for j in range(3)] for i in range(6)]
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
                c = 1/math.sqrt(t*t+1); sn = t*c
                for k in range(3):
                    x,y = G[k][p],G[k][q]; G[k][p],G[k][q] = c*x-sn*y, sn*x+c*y
                for k in range(3):
                    x,y = G[p][k],G[q][k]; G[p][k],G[q][k] = c*x-sn*y, sn*x+c*y
    return sorted((max(G[i][i],0.0)**0.5 for i in range(3)), reverse=True)

print("A. at the failing corner (rho ~ 0, tau = 0.7855, wu = 5/4, wv = 4):")
for rp in (F(0), F(1,65536), F(1,4096)):
    sv = svals(rp, F(7855,10000), F(5,4), F(4))
    print(f"   rho={float(rp):.2e}  sv = " + ", ".join(f"{x:.4e}" for x in sv))

print("\nB. scan tau at INTERIOR (wu, wv) = (1, 2), rho = 0: any sigma3 dip?")
lo = None
for k in range(-20, 21):
    tau = F(k, 25)
    sv = svals(F(0), tau, F(1), F(2))
    if lo is None or sv[2] < lo[1]:
        lo = (float(tau), sv[2])
    if abs(k) % 5 == 0:
        print(f"   tau={float(tau):+.2f}  sigma3 = {sv[2]:.4e}")
print(f"   minimum over the scan: sigma3 = {lo[1]:.4e} at tau = {lo[0]:+.3f}")

print("\nC. the same scan at (wu, wv) = (5/4, 4) (the corner's coordinates):")
lo = None
for k in range(-20, 21):
    tau = F(k, 25)
    sv = svals(F(0), tau, F(5,4), F(4))
    if lo is None or sv[2] < lo[1]:
        lo = (float(tau), sv[2])
print(f"   minimum over the scan: sigma3 = {lo[1]:.4e} at tau = {lo[0]:+.3f}")
