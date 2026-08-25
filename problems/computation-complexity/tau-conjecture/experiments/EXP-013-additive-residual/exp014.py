"""EXP-014: price the windowed gap in the additive nine-gate scan, EXACTLY.

Confinement lemma (proved, constant sharp): if f has 7 distinct integer roots
and trailing coefficient c, then |c| <= 1187 when 0 is not a root and
|c| <= 395 when it is; either way |c| <= 395 forces every integer root of f into
[-32,32]. For such f the additive scan's emptiness on that window is CONCLUSIVE
rather than windowed.

This classifies additive candidates f = t +- b by constructing every one of them
EXACTLY and reading its true trailing coefficient. No coefficient horizon, no
proxy. Sampled over states drawn from hash-partitioned files, so the sample is
representative by construction.

An earlier vectorized version carrying only the low 20 coefficients reported
~1.5% "undetermined"; exact construction showed every one of those is the
IDENTICALLY ZERO polynomial, and that no nonzero candidate is divisible by
x^20 at all. The zero polynomial is not a seven-rooter and the scan excludes it,
so it is reported separately here rather than counted against the window.
"""
import pickle
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
from tclib.enum import padd, pmul, psub

SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
PARTS = sys.argv[2].split(",") if len(sys.argv) > 2 else ["000"]
WIDTH = 7
t0 = time.time()

with open("E:/_Datos/caos-research/tau-conjecture/polys.pkl", "rb") as fh:
    polys = pickle.load(fh)["polys"]


def build_pairs(m):
    ai, aj, si, sj = [], [], [], []
    for i in range(m):
        for j in range(i, m):
            ai.append(i); aj.append(j)
    for i in range(m):
        for j in range(m):
            if i != j:
                si.append(i); sj.append(j)
    return ai, aj, si, sj


AI, AJ, SI, SJ = build_pairs(10)
nA, nS = len(AI), len(SI)

tot = conf = wl = zero = lowdeg = 0
wl_examples = []
for PART in PARTS:
    arr = np.fromfile(
        f"E:/_Datos/caos-research/tau-conjecture/frontier7/uniq{PART}.bin",
        dtype=np.int32).reshape(-1, WIDTH)
    rng = np.random.default_rng(20260825 + int(PART))
    rows = arr[rng.choice(arr.shape[0], size=min(SAMPLE, arr.shape[0]),
                          replace=False)]
    for r in rows:
        ids = [0, 1, 2] + [int(v) for v in r]
        op = [polys[i] for i in ids]
        exts = ([padd(op[AI[k]], op[AJ[k]]) for k in range(nA)]
                + [pmul(op[AI[k]], op[AJ[k]]) for k in range(nA)]
                + [psub(op[SI[k]], op[SJ[k]]) for k in range(nS)])
        for t in exts:
            for b in op:
                for f in (padd(t, b), psub(t, b)):
                    tot += 1
                    nz = -1
                    for i, c in enumerate(f):
                        if c:
                            nz = i
                            break
                    if nz < 0:
                        zero += 1
                        continue
                    c = f[nz]
                    limit = 395 if nz > 0 else 1187
                    if abs(c) <= limit:
                        conf += 1
                    elif len(f) - 1 < 7:
                        # A polynomial with 7 DISTINCT roots has degree >= 7.
                        # Below that the candidate is excluded outright, with no
                        # reference to the window at all.
                        lowdeg += 1
                    else:
                        wl += 1
                        wl_examples.append((nz, abs(c), len(f) - 1, tuple(f)))
    print(f"  partition {PART} done ({time.time()-t0:.0f}s)", flush=True)

nonzero = tot - zero
print()
print(f"candidates constructed exactly : {tot:,}")
print(f"identically zero (excluded)    : {zero:,}  ({100.0*zero/tot:.3f}%)")
print(f"nonzero candidates             : {nonzero:,}")
print()
print(f"CONFINED by the lemma          : {conf:,}  "
      f"({100.0*conf/nonzero:.4f}% of nonzero)")
print(f"  -> the [-32,32] window DECIDES these outright")
print(f"excluded by degree < 7         : {lowdeg:,}  "
      f"({100.0*lowdeg/nonzero:.4f}% of nonzero)")
print(f"  -> cannot have 7 distinct roots at all, window irrelevant")
print(f"WINDOW-LIMITED (deg >= 7)      : {wl:,}  "
      f"({100.0*wl/nonzero:.6f}% of nonzero)")
if wl_examples:
    import collections
    print()
    cs = sorted(set(e[1] for e in wl_examples))
    print(f"  distinct |trailing coefficient| values: {len(cs)}")
    print(f"  min |c| = {min(cs)}   max |c| = {max(cs)}")
    print(f"  values: {cs[:20]}{' ...' if len(cs) > 20 else ''}")
    dg = collections.Counter(e[2] for e in wl_examples)
    print(f"  degrees: {dict(sorted(dg.items()))}")
    # A seven-rooter needs 7 distinct nonzero roots dividing c, and the least
    # |product| of 7 distinct nonzero integers is 1*1*2*2*3*3*4 = 144; if one
    # root escapes [-32,32] the least product is 33*36 = 1188. Check whether c
    # even ADMITS 7 distinct divisors.
    def ndiv(n):
        d = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                d.add(i); d.add(n // i)
            i += 1
        return len(d) * 2          # counting signs
    bad = [c for c in cs if ndiv(c) < 7]
    print(f"  |c| values with fewer than 7 distinct signed divisors: "
          f"{len(bad)} of {len(cs)}")
print(f"\n{time.time()-t0:.0f}s")
