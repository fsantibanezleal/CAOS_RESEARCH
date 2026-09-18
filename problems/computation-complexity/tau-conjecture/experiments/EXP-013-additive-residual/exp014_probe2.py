"""EXP-014 probe, deeper: resolve the x^m | f cases by carrying K low coefficients.

The confinement criterion needs the TRAILING (first nonzero) coefficient. When
0 is a root of multiplicity m the trailing coefficient is c_m, so carrying only
c0 and c1 leaves every f divisible by x^2 undetermined. Low coefficients
convolve, c_k(a*b) = sum_{i+j=k} c_i(a) c_j(b), so carrying K of them is the
same vectorized pass.

Bound used: |c| <= 1187 confines when 0 is NOT a root, |c| <= 395 when it is.
"""
import pickle
import sys
import time

import numpy as np

K = int(sys.argv[3]) if len(sys.argv) > 3 else 6
BIG = 2 ** 27                    # keeps sum_k c_i c_j inside int64 exactly
SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
PART = sys.argv[2] if len(sys.argv) > 2 else "000"
WIDTH = 7
t0 = time.time()

with open("E:/_Datos/caos-research/tau-conjecture/polys.pkl", "rb") as fh:
    polys = pickle.load(fh)["polys"]
n = len(polys)
C = np.zeros((n, K), dtype=np.int64)
big = np.zeros(n, dtype=bool)
for i, p in enumerate(polys):
    for k in range(min(K, len(p))):
        if abs(p[k]) >= BIG:
            big[i] = True
            break
    else:
        for k in range(min(K, len(p))):
            C[i, k] = p[k]
print(f"catalog {n:,}; excluded for large low coefficients: {big.sum()} "
      f"({100.0*big.sum()/n:.4f}%)   [{time.time()-t0:.0f}s]", flush=True)


def build_pairs(m):
    ai, aj, si, sj = [], [], [], []
    for i in range(m):
        for j in range(i, m):
            ai.append(i); aj.append(j)
    for i in range(m):
        for j in range(m):
            if i != j:
                si.append(i); sj.append(j)
    return np.array(ai), np.array(aj), np.array(si), np.array(sj)


AI, AJ, SI, SJ = build_pairs(10)
arr = np.fromfile(f"E:/_Datos/caos-research/tau-conjecture/frontier7/uniq{PART}.bin",
                  dtype=np.int32).reshape(-1, WIDTH)
rng = np.random.default_rng(20260825)
idx = rng.choice(arr.shape[0], size=min(SAMPLE, arr.shape[0]), replace=False)
rows = arr[idx]
print(f"partition {PART}: {arr.shape[0]:,} states, sampling {len(rows):,}", flush=True)

inputs = np.array([0, 1, 2], dtype=np.int32)
tot = conf = undet = skipped = 0
CH = 200
for s in range(0, rows.shape[0], CH):
    r = rows[s:s + CH]
    ids = np.concatenate([np.tile(inputs, (r.shape[0], 1)), r], axis=1)
    keep = ~big[ids].any(axis=1)
    skipped += int((~keep).sum()) * 200 * 10 * 2
    ids = ids[keep]
    if ids.shape[0] == 0:
        continue
    A = C[ids]                                             # (B,10,K)
    add = A[:, AI] + A[:, AJ]
    sub = A[:, SI] - A[:, SJ]
    mul = np.zeros((ids.shape[0], len(AI), K), dtype=np.int64)
    for i in range(K):
        for j in range(K - i):
            mul[:, :, i + j] += A[:, AI, i] * A[:, AJ, j]
    T = np.concatenate([add, mul, sub], axis=1)            # (B,200,K)

    for sign in (1, -1):
        F = T[:, :, None, :] + sign * A[:, None, :, :]     # (B,200,10,K)
        nz = F != 0
        anynz = nz.any(axis=3)
        first = np.argmax(nz, axis=3)                      # index of trailing coeff
        trail = np.take_along_axis(F, first[..., None], axis=3)[..., 0]
        zero_is_root = first > 0
        limit = np.where(zero_is_root, 395, 1187)
        ok = anynz & (np.abs(trail) <= limit)
        tot += ok.size
        conf += int(ok.sum())
        undet += int((~anynz).sum())

wl = tot - conf - undet
print()
print(f"candidates examined    : {tot:,}")
print(f"CONFINED by the lemma  : {conf:,}  ({100.0*conf/tot:.3f}%)")
print(f"window-limited         : {wl:,}  ({100.0*wl/tot:.4f}%)")
print(f"undetermined (c0..c{K-1} all 0): {undet:,}  ({100.0*undet/tot:.4f}%)")
print(f"skipped (large low coeffs): {skipped:,}  ({100.0*skipped/(tot+skipped):.4f}%)")
print(f"\n{time.time()-t0:.0f}s")
