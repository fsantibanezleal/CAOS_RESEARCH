"""EXP-012 fast known-answer gate: threshold 6 on a slice of partition 0.

Independent re-implementation of the scan's inner loop (deliberate: an
independent check of the same question). Must find hits: 9-gate
6-rooters via a final multiplication certainly exist, since 8-gate
6-rooters do.
"""

import json
import pickle
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
from tclib.enum import integer_roots, padd, pmul, psub  # noqa: E402

ASSETS = Path("E:/_Datos/caos-research/tau-conjecture")
ROWS = 150_000
THRESHOLD = 6

t0 = time.time()
with open(ASSETS / "polys.pkl", "rb") as fh:
    polys = pickle.load(fh)["polys"]
arr = np.fromfile(ASSETS / "frontier7" / "uniq000.bin",
                  dtype=np.int32).reshape(-1, 7)[:ROWS]
print(f"loaded {arr.shape[0]} states ({time.time()-t0:.1f}s)", flush=True)

fns = (padd, pmul, psub)
opcache, rootmemo = {}, {}
hits, max_union = [], 0


def rootset_id(i):
    r = rootmemo.get(("i", i))
    if r is None:
        p = polys[i]
        r = frozenset(integer_roots(p)) if p else frozenset()
        rootmemo[("i", i)] = r
    return r


def rootset_poly(t, key):
    r = rootmemo.get(key)
    if r is None:
        r = frozenset(integer_roots(t))
        if len(rootmemo) < 2_000_000:
            rootmemo[key] = r
    return r


for row in arr:
    state = tuple(int(x) for x in row)
    operands = (0, 1, 2) + state
    opolys = [polys[i] for i in operands]
    rsets = [rootset_id(i) for i in operands]
    maxz = max(len(r) for r in rsets)
    if maxz == 0:
        continue
    need = THRESHOLD - maxz
    n = len(operands)
    for i in range(n):
        for j in range(n):
            for o in (0, 1, 2):
                if o != 2 and j < i:
                    continue
                if o == 2 and i == j:
                    continue
                key = (o, operands[i], operands[j])
                t = opcache.get(key)
                if t is None:
                    t = fns[o](opolys[i], opolys[j])
                    if len(opcache) < 3_000_000:
                        opcache[key] = t
                if not t:
                    continue
                rv = rootset_poly(t, ("p",) + key)
                if len(rv) < need:
                    continue
                for bi, rb in zip(operands, rsets):
                    u = len(rv | rb)
                    max_union = max(max_union, u)
                    if u >= THRESHOLD and len(hits) < 10:
                        hits.append({"v8": list(t), "b": list(polys[bi]),
                                     "union": sorted(rv | rb)})

ok = len(hits) > 0
print(f"GATE(threshold {THRESHOLD}, {arr.shape[0]} states): hits={len(hits)} "
      f"max_union={max_union}: {'PASS' if ok else 'FAIL'} "
      f"({time.time()-t0:.1f}s)", flush=True)
for h in hits[:3]:
    print("  ", h)
(HERE / "artifacts").mkdir(exist_ok=True)
(HERE / "artifacts" / "gate_slice.json").write_text(json.dumps(
    {"rows": int(arr.shape[0]), "threshold": THRESHOLD,
     "hits": hits, "max_union": max_union, "pass": ok}), "utf-8")
sys.exit(0 if ok else 1)
