"""Characterize the residual class the coefficient instrument leaves open.

Carrying the low 20 coefficients classifies ~98.5% of additive candidates as
CONFINED and ~0.076% as genuinely window-limited. The remaining ~1.5% have
c_0..c_19 all zero, i.e. x^20 divides f. This constructs those EXACTLY on a
small state sample and reports what they are.

If they are monomials, or have few distinct roots, they cannot be seven-rooters
and the residual is harmless.
"""
import pickle
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
from tclib.enum import padd, pmul, psub, integer_roots

K = 20
SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 120
PART = sys.argv[2] if len(sys.argv) > 2 else "000"
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
nA = len(AI)
arr = np.fromfile(f"E:/_Datos/caos-research/tau-conjecture/frontier7/uniq{PART}.bin",
                  dtype=np.int32).reshape(-1, WIDTH)
rng = np.random.default_rng(20260825)
rows = arr[rng.choice(arr.shape[0], size=SAMPLE, replace=False)]
print(f"sampling {SAMPLE} states from partition {PART}", flush=True)


def low_all_zero(p):
    return all(c == 0 for c in p[:K])


stats = {"total": 0, "monomial": 0, "zero": 0, "roots<=1": 0,
         "roots 2-6": 0, "roots>=7": 0, "confined_deep": 0, "wl_deep": 0}
maxroots = 0
for r in rows:
    ids = [0, 1, 2] + [int(v) for v in r]
    op = [polys[i] for i in ids]
    exts = ([padd(op[AI[k]], op[AJ[k]]) for k in range(nA)]
            + [pmul(op[AI[k]], op[AJ[k]]) for k in range(nA)]
            + [psub(op[SI[k]], op[SJ[k]]) for k in range(len(SI))])
    for t in exts:
        if not t:
            continue
        for b in op:
            for f in (padd(t, b), psub(t, b)):
                if not f or not low_all_zero(f):
                    continue
                stats["total"] += 1
                nz = [i for i, c in enumerate(f) if c]
                if not nz:
                    stats["zero"] += 1
                    continue
                if len(nz) == 1:
                    stats["monomial"] += 1
                R = integer_roots(f)
                maxroots = max(maxroots, len(R))
                if len(R) <= 1:
                    stats["roots<=1"] += 1
                elif len(R) < 7:
                    stats["roots 2-6"] += 1
                else:
                    stats["roots>=7"] += 1
                c = f[nz[0]]
                limit = 395 if nz[0] > 0 else 1187
                if abs(c) <= limit:
                    stats["confined_deep"] += 1
                else:
                    stats["wl_deep"] += 1

n = max(stats["total"], 1)
print()
print(f"residual candidates constructed exactly : {stats['total']:,}")
print(f"  monomials (at most one distinct root) : {stats['monomial']:,} "
      f"({100.0*stats['monomial']/n:.2f}%)")
print(f"  with <= 1 distinct integer root       : {stats['roots<=1']:,} "
      f"({100.0*stats['roots<=1']/n:.2f}%)")
print(f"  with 2-6 distinct integer roots       : {stats['roots 2-6']:,}")
print(f"  with >= 7 distinct integer roots      : {stats['roots>=7']:,}")
print(f"  max distinct integer roots seen       : {maxroots}")
print()
print(f"  CONFINED once the true trailing coefficient is used: "
      f"{stats['confined_deep']:,} ({100.0*stats['confined_deep']/n:.2f}%)")
print(f"  still window-limited                              : "
      f"{stats['wl_deep']:,} ({100.0*stats['wl_deep']/n:.2f}%)")
print(f"\n{time.time()-t0:.0f}s")
