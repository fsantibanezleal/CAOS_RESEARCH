"""EXP-014: price the windowed gap exactly, via x-adic valuation.

The confinement criterion needs the TRAILING (first nonzero) coefficient of
f = t +- b. Carrying the low K coefficients leaves every f divisible by x^K
unresolved. The valuation pair (v, L) = (index of first nonzero coefficient,
that coefficient) composes exactly and has no such horizon:

    mul: v = v_a + v_b,  L = L_a * L_b
    add/sub: if v_a < v_b -> (v_a, L_a); if v_a > v_b -> (v_b, +-L_b);
             if equal -> L = L_a +- L_b, and if L != 0 the pair is (v_a, L),
             otherwise the valuation rises and the case is UNRESOLVED here.

Criterion (confinement lemma): with 7 distinct integer roots and trailing
coefficient c, |c| <= 1187 confines when 0 is not a root (v = 0), and
|c| <= 395 when it is (v > 0). Confined means the [-32,32] window decides that
candidate outright, so emptiness there is conclusive and not merely windowed.

Sampled over states drawn from one partition; partitions are hash-partitioned,
so a sample is representative by construction.
"""
import pickle
import sys
import time

import numpy as np

INF = 10 ** 6
BIG = 2 ** 31
SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
PART = sys.argv[2] if len(sys.argv) > 2 else "000"
WIDTH = 7
t0 = time.time()

with open("E:/_Datos/caos-research/tau-conjecture/polys.pkl", "rb") as fh:
    polys = pickle.load(fh)["polys"]
n = len(polys)
val = np.full(n, INF, dtype=np.int64)
lead = np.zeros(n, dtype=np.int64)
big = np.zeros(n, dtype=bool)
for i, p in enumerate(polys):
    for k, c in enumerate(p):
        if c:
            if abs(c) >= BIG:
                big[i] = True
            else:
                val[i] = k
                lead[i] = c
            break
print(f"catalog {n:,}; excluded for |lead| >= 2^31: {big.sum()} "
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


def combine(va, La, vb, Lb):
    """Valuation pair of a +- b, with sign already folded into Lb.
    Returns (v, L, tie_cancel)."""
    lt, gt = va < vb, va > vb
    v = np.where(lt, va, np.where(gt, vb, va))
    L = np.where(lt, La, np.where(gt, Lb, La + Lb))
    tie = (~lt) & (~gt) & (L == 0) & (va < INF)
    return v, L, tie


AI, AJ, SI, SJ = build_pairs(10)
arr = np.fromfile(f"E:/_Datos/caos-research/tau-conjecture/frontier7/uniq{PART}.bin",
                  dtype=np.int32).reshape(-1, WIDTH)
rng = np.random.default_rng(20260825)
idx = rng.choice(arr.shape[0], size=min(SAMPLE, arr.shape[0]), replace=False)
rows = arr[idx]
print(f"partition {PART}: {arr.shape[0]:,} states, sampling {len(rows):,}", flush=True)

inputs = np.array([0, 1, 2], dtype=np.int32)
tot = conf = wl = unres = zero = skipped = 0
CH = 200
for s in range(0, rows.shape[0], CH):
    r = rows[s:s + CH]
    ids = np.concatenate([np.tile(inputs, (r.shape[0], 1)), r], axis=1)
    keep = ~big[ids].any(axis=1)
    skipped += int((~keep).sum()) * 200 * 10 * 2
    ids = ids[keep]
    if ids.shape[0] == 0:
        continue
    V, L = val[ids], lead[ids]                                   # (B,10)

    va, La, tie_a = combine(V[:, AI], L[:, AI], V[:, AJ], L[:, AJ])
    vs, Ls, tie_s = combine(V[:, SI], L[:, SI], V[:, SJ], -L[:, SJ])
    vm = V[:, AI] + V[:, AJ]
    Lm = L[:, AI] * L[:, AJ]
    tie_m = np.zeros_like(tie_a)
    Tv = np.concatenate([va, vm, vs], axis=1)                    # (B,200)
    TL = np.concatenate([La, Lm, Ls], axis=1)
    Tt = np.concatenate([tie_a, tie_m, tie_s], axis=1)

    for sign in (1, -1):
        fv, fL, ftie = combine(Tv[:, :, None], TL[:, :, None],
                               V[:, None, :], sign * L[:, None, :])
        bad = ftie | Tt[:, :, None]
        isz = (fv >= INF)
        limit = np.where(fv > 0, 395, 1187)
        ok = (~bad) & (~isz) & (np.abs(fL) <= limit)
        tot += ok.size
        conf += int(ok.sum())
        unres += int(bad.sum())
        zero += int((isz & ~bad).sum())
        wl += int(((~bad) & (~isz) & (np.abs(fL) > limit)).sum())

print()
print(f"candidates examined      : {tot:,}")
print(f"CONFINED by the lemma    : {conf:,}  ({100.0*conf/tot:.4f}%)")
print(f"WINDOW-LIMITED           : {wl:,}  ({100.0*wl/tot:.4f}%)")
print(f"unresolved (exact tie)   : {unres:,}  ({100.0*unres/tot:.4f}%)")
print(f"identically zero         : {zero:,}  ({100.0*zero/tot:.4f}%)")
print(f"skipped (large lead)     : {skipped:,}")
print(f"\n{time.time()-t0:.0f}s")
