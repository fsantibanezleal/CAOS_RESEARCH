"""Descend to the near-rank-2 point the merge covering keeps hitting.

sigma_3 ~ 1.1e-5 was measured at (tau, wu, wv) ~ (0.7855, 1.25, 4) and is
INDEPENDENT of rho, so it is a feature of the underlying configuration,
not of the merge. In this stratum the rank <= 2 locus is exactly where
central configurations live, so if sigma_3 goes to zero there and the
kernel is POSITIVE, that is a central configuration.

Works in the ORIGINAL coordinates (the merge chart's rho only reparametrises):
pair A at (+-1, 0), pairs B and C at (+-u, v +- something). At rho = 0 the
B and C pairs coincide, which is a collision, so the descent is run with
the two pairs SEPARATE: u2 = wu + d, u3 = wu - d, v2 = wv + e, v3 = wv - e
with (d, e) a genuine separation, and it reports whether sigma_3 -> 0 with
the separation kept away from zero.
"""
import math, random
import mpmath as mp
mp.mp.dps = 50
from pathlib import Path
HERE = Path(__file__).resolve().parent
src = (HERE / "derive.py").read_text(encoding="utf-8")
ns = {"__file__": str(HERE / "derive.py")}
exec(src.split('rnd = random.Random')[0], ns)
positions, L_coeffs, ROWS = ns["positions"], ns["L_coeffs"], ns["ROWS"]

def M_of(u2, v2, u3, v3):
    P = positions(mp.mpf(1), mp.mpf(0), u2, v2, u3, v3)
    return [L_coeffs(P, i, j) for (i, j) in ROWS]

def svd3(M):
    A = [[float(x) for x in row] for row in M]
    for i in range(6):
        n = max(abs(x) for x in A[i]) or 1.0
        A[i] = [x / n for x in A[i]]
    G = [[sum(A[k][i]*A[k][j] for k in range(6)) for j in range(3)] for i in range(3)]
    for _ in range(80):
        off = sum(G[i][j]**2 for i in range(3) for j in range(i+1,3))
        if off < 1e-30: break
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

def obj(p):
    u2, v2, u3, v3 = p
    if u2 <= 0 or u3 <= 0: return mp.mpf(10)
    if abs(u2-u3) < mp.mpf(1)/10000 and abs(v2-v3) < mp.mpf(1)/10000:
        return mp.mpf(10)                       # keep the two pairs separate
    return mp.mpf(svd3(M_of(u2, v2, u3, v3))[2])

# start from the corner geometry, pairs genuinely separated
tau = mp.mpf("0.7855"); o = 1 + tau*tau
al, be = (1-tau*tau)/o, 2*tau/o
wu, wv, rho = mp.mpf("1.25"), mp.mpf(4), mp.mpf("0.05")
x = [wu + rho*al/2, wv + rho*be/2, wu - rho*al/2, wv - rho*be/2]
print("start:", [mp.nstr(t, 8) for t in x], " sigma3 =", mp.nstr(obj(x), 6))
random.seed(2)
step = mp.mpf(1)/32
best = obj(x)
for it in range(3000):
    y = [x[i] + step*(mp.mpf(random.random())-mp.mpf(1)/2) for i in range(4)]
    v = obj(y)
    if v < best:
        best, x = v, y
    if it % 500 == 499:
        step /= 4
        print(f"   it {it+1}: sigma3 = {mp.nstr(best, 6)}  step={mp.nstr(step,3)}")
print("\nfinal point (u2, v2, u3, v3):", [mp.nstr(t, 12) for t in x])
print("sigma values:", [mp.nstr(s, 8) for s in svd3(M_of(*x))])
print("pair separation |B-C| =", mp.nstr(mp.sqrt((x[0]-x[2])**2 + (x[1]-x[3])**2), 8))
# kernel
M = M_of(*x)
A = mp.matrix(6, 3)
for i in range(6):
    for j in range(3): A[i, j] = M[i][j]
try:
    U, S, V = mp.svd_r(A)
    ker = [V[2, j] for j in range(3)]
    nrm = max(abs(k) for k in ker)
    ker = [k / nrm for k in ker]
    print("kernel (mA, mB, mC) =", [mp.nstr(k, 10) for k in ker])
    print("all same sign (=> POSITIVE masses possible):",
          all(k > 0 for k in ker) or all(k < 0 for k in ker))
except Exception as e:
    print("kernel failed:", e)
