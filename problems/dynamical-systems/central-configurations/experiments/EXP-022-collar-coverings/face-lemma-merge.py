"""Lemma piece 12: the pair-MERGE faces (quadruple cluster, and at infinity).

The face-rank gate found two charts whose face matrix has rank 2: M1 (the
quadruple cluster, rhoq -> 0, where the two mirror pairs coincide) and
fartube (rhof -> 0, where they merge at infinity). The entry-order probe
shows why, and shows it is the SAME structure as lemma piece 11:

    at the face the m1 and m2 columns vanish to FIRST order while the mA
    and mB columns survive,

so the face has rank 2, no box containing it can certify, and dividing the
two vanishing columns by the face parameter (a positive scalar: rank is
unchanged off the face) is exactly what restores it. Both faces are
excluded from the open stratum: rhoq = 0 is a collision between a body of
pair A and a body of pair B, and rhof = 0 is the same merge at infinity,
which is not a configuration at all.

This script builds the column-rescaled face matrix for each of the two
faces along its chart's parametrization, at a spread of interior sample
points, and reports its third singular value. A floor bounded away from
zero means rank >= 3 uniformly on the punctured collar, closing the face
by the piece 11 mechanism with no new machinery.
"""
import math
import random
from pathlib import Path
import importlib.util
import mpmath as mp

mp.mp.dps = 60
HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("fl2", HERE / "face-lemma-collapse.py")
_src = (HERE / "face-lemma-collapse.py").read_text(encoding="utf-8")
_ns = {"__file__": str(HERE / "face-lemma-collapse.py")}
exec(_src.split('print("A.')[0], _ns)
J_orig = _ns["J_orig"]

def F(a, b=1):
    return mp.mpf(a) / mp.mpf(b)

def circ(t):
    o = 1 + t * t
    return (1 - t * t) / o, 2 * t / o

def m1_geom(e, rhoa, tb, tq):
    al_n, be = circ(tq)
    alpha = -al_n
    rr = 1 + e * alpha
    ta = tb + e * be
    ca, sa = circ(ta)
    cb, sb = circ(tb)
    return rhoa * ca, 1 + rhoa * sa, rr * rhoa * cb, 1 + rr * rhoa * sb

def fartube_geom(e, tf, eB, tB):
    opf = 1 + tf * tf
    alpha = -(1 - tf * tf) / opf
    beta = 2 * tf / opf
    r = 1 + e * alpha
    tA = tB + e * beta
    aA, bA = circ(tA)
    aB, bB = circ(tB)
    eA = r * eB
    return aA / eA, bA / eA, aB / eB, bB / eB

def sigma3_rescaled(geom, params, e):
    """entry matrix with m1, m2 columns divided by e (piece 11 mechanism)."""
    u, v, p, q = geom(e, *params)
    if u <= 0 or p <= 0 or v == q:
        return None
    J = J_orig(u, v, p, q)
    col = [1 / e, 1 / e, mp.mpf(1), mp.mpf(1)]
    A = [[float(J[i][j] * col[j]) for j in range(4)] for i in range(6)]
    # normalise rows so the singular values are comparable across samples
    for i in range(6):
        n = max(abs(x) for x in A[i]) or 1.0
        A[i] = [x / n for x in A[i]]
    G = [[sum(A[k][i] * A[k][j] for k in range(6)) for j in range(4)]
         for i in range(4)]
    for _ in range(60):
        off = sum(G[i][j] ** 2 for i in range(4) for j in range(i + 1, 4))
        if off < 1e-28:
            break
        for pp in range(4):
            for qq in range(pp + 1, 4):
                if abs(G[pp][qq]) < 1e-300:
                    continue
                th = (G[qq][qq] - G[pp][pp]) / (2 * G[pp][qq])
                t = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(4):
                    a, b = G[k][pp], G[k][qq]
                    G[k][pp], G[k][qq] = c * a - s * b, s * a + c * b
                for k in range(4):
                    a, b = G[pp][k], G[qq][k]
                    G[pp][k], G[qq][k] = c * a - s * b, s * a + c * b
    ev = sorted((max(G[i][i], 0.0) ** 0.5 for i in range(4)), reverse=True)
    return ev[2]

rnd = random.Random(4242)
def rr_(lo, hi, den=64):
    return mp.mpf(rnd.randint(int(lo * den) + 1, int(hi * den) - 1)) / den

print("piece 12: sigma_3 of the COLUMN-RESCALED matrix as the face is approached")
print("(m1 and m2 columns divided by the face parameter; rows normalised)\n")
for label, geom, sampler in (
        ("M1  (quadruple cluster, rhoq -> 0)", m1_geom,
         lambda: [rr_(0.02, 0.2), rr_(-0.9, 0.9), rr_(-0.9, 0.9)]),
        ("fartube (merge at infinity, rhof -> 0)", fartube_geom,
         lambda: [rr_(-0.9, 0.9), rr_(0.05, 0.6), rr_(-0.9, 0.9)])):
    print(f"--- {label}")
    for e_pow in (4, 6, 8):
        e = F(1, 10 ** e_pow)
        vals = []
        for _ in range(40):
            v = sigma3_rescaled(geom, sampler(), e)
            if v is not None:
                vals.append(v)
        vals.sort()
        if vals:
            print(f"    eps=1e-{e_pow}: min sigma3 {vals[0]:.4e}   "
                  f"median {vals[len(vals)//2]:.4e}   n={len(vals)}")
    print()
