"""EXP-014 probe: how much of the additive search space does the WINDOW decide?

Confinement lemma: if f has 7 distinct integer roots and trailing coefficient c,
then |c| <= 395 forces every root into [-32,32] (1187 when 0 is not a root, 396
when it is). For an additive last gate f = t +- b the trailing coefficient comes
from the LOW coefficients of t and b alone, which compose trivially:

    c0(a+b)  = c0(a)+c0(b)      c1(a+b)  = c1(a)+c1(b)
    c0(a*b)  = c0(a)*c0(b)      c1(a*b)  = c0(a)c1(b) + c1(a)c0(b)
    c0(a-b)  = c0(a)-c0(b)      c1(a-b)  = c1(a)-c1(b)

so no polynomial construction is needed. This is a SAMPLED estimate over states
drawn from one partition, not the exhaustive count.

Candidates touching the 112 catalog polynomials with |c0| > 2^31 are excluded
from the vectorized pass and counted separately, which keeps every product
inside int64 exactly.
"""
import pickle
import sys
import time

import numpy as np

BIG = 2 ** 31
SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
PART = sys.argv[2] if len(sys.argv) > 2 else "000"
WIDTH = 7
t0 = time.time()

with open("E:/_Datos/caos-research/tau-conjecture/polys.pkl", "rb") as fh:
    polys = pickle.load(fh)["polys"]
n = len(polys)
c0 = np.zeros(n, dtype=np.int64)
c1 = np.zeros(n, dtype=np.int64)
big = np.zeros(n, dtype=bool)
for i, p in enumerate(polys):
    v0 = p[0] if p else 0
    v1 = p[1] if len(p) > 1 else 0
    if abs(v0) >= BIG or abs(v1) >= BIG:
        big[i] = True
    else:
        c0[i] = v0
        c1[i] = v1
print(f"catalog {n:,}; big-c0 polys excluded: {big.sum()} "
      f"({time.time()-t0:.0f}s)", flush=True)


def build_pairs(m):
    ai, aj, si, sj = [], [], [], []
    for i in range(m):
        for j in range(i, m):
            ai.append(i); aj.append(j)
    for i in range(m):
        for j in range(m):
            if i != j:
                si.append(i); sj.append(j)
    return (np.array(ai), np.array(aj), np.array(si), np.array(sj))


AI, AJ, SI, SJ = build_pairs(10)
arr = np.fromfile(f"E:/_Datos/caos-research/tau-conjecture/frontier7/uniq{PART}.bin",
                  dtype=np.int32).reshape(-1, WIDTH)
rng = np.random.default_rng(20260825)
idx = rng.choice(arr.shape[0], size=min(SAMPLE, arr.shape[0]), replace=False)
rows = arr[idx]
print(f"partition {PART}: {arr.shape[0]:,} states, sampling {len(rows):,}", flush=True)

inputs = np.array([0, 1, 2], dtype=np.int32)
tot = conf = undet = skipped = 0
CH = 250
for s in range(0, rows.shape[0], CH):
    r = rows[s:s + CH]
    B = r.shape[0]
    ids = np.concatenate([np.tile(inputs, (B, 1)), r], axis=1)     # (B,10)
    if big[ids].any(axis=1).sum():
        keep = ~big[ids].any(axis=1)
        skipped += int((~keep).sum()) * 200 * 10 * 2
        ids = ids[keep]
        B = ids.shape[0]
        if B == 0:
            continue
    A0, A1 = c0[ids], c1[ids]                                       # (B,10)
    t0c = np.concatenate([A0[:, AI] + A0[:, AJ],
                          A0[:, AI] * A0[:, AJ],
                          A0[:, SI] - A0[:, SJ]], axis=1)           # (B,200)
    t1c = np.concatenate([A1[:, AI] + A1[:, AJ],
                          A0[:, AI] * A1[:, AJ] + A1[:, AI] * A0[:, AJ],
                          A1[:, SI] - A1[:, SJ]], axis=1)
    for sign in (1, -1):
        f0 = t0c[:, :, None] + sign * A0[:, None, :]                # (B,200,10)
        f1 = t1c[:, :, None] + sign * A1[:, None, :]
        nz0 = f0 != 0
        ok = np.where(nz0, np.abs(f0) <= 1187,
                      np.where(f1 != 0, np.abs(f1) <= 395, False))
        both0 = (~nz0) & (f1 == 0)
        tot += ok.size
        conf += int(ok.sum())
        undet += int(both0.sum())

print()
print(f"candidates examined : {tot:,}")
print(f"CONFINED by the lemma: {conf:,}  ({100.0*conf/tot:.3f}%)")
print(f"  -> for these, emptiness on [-32,32] is CONCLUSIVE, not windowed")
print(f"window-limited       : {tot-conf-undet:,}  ({100.0*(tot-conf-undet)/tot:.3f}%)")
print(f"undetermined (c0=c1=0): {undet:,}  ({100.0*undet/tot:.3f}%)")
print(f"skipped (big-c0 states): {skipped:,}")
print(f"\n{time.time()-t0:.0f}s")
