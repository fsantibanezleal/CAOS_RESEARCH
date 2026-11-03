"""Instrument probe and known-answer gate for EXP-015 (design, not the production run).

On a random sample of depth-7 states:
  --gate K  : run the engine at threshold K and, independently, build EVERY
              candidate exactly and count its distinct integer roots; the number
              of candidates with >= K roots must equal the engine's hit count.
  --rate    : run the engine at k = 7 and report stage pass rates and states/s.

Usage: python probe.py <assets dir> <partition> <states> (--gate K | --rate) [seed]
"""
import json
import pickle
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
sys.path.insert(0, str(HERE))
from tclib.enum import integer_roots, padd, pmul, psub  # noqa: E402
from engine import KIND, LEFT, RIGHT, WIDTH, Engine, load_tables  # noqa: E402

ASSETS = Path(sys.argv[1])
PART = int(sys.argv[2])
NSTATES = int(sys.argv[3])
MODE = sys.argv[4]
K = int(sys.argv[5]) if MODE == "--gate" else 7
SEED = int(sys.argv[6]) if MODE == "--gate" and len(sys.argv) > 6 else 20261102

with open(ASSETS / "polys.pkl", "rb") as fh:
    polys = pickle.load(fh)["polys"]
arr = np.fromfile(ASSETS / "frontier7" / f"uniq{PART:03d}.bin", dtype=np.int32).reshape(-1, WIDTH)
rows = arr[np.random.default_rng(SEED).choice(arr.shape[0], size=NSTATES, replace=False)]

eng = Engine(polys, load_tables(ASSETS), K)
t0 = time.time()
hits = 0
for s in range(0, NSTATES, 48):
    hits += len(eng.scan(rows[s:s + 48]))
dt = time.time() - t0
st = eng.stats
print(json.dumps(st))
c = st["candidates"]
print(f"k={K}: {NSTATES} states in {dt:.1f}s ({NSTATES/dt:.1f} states/s); "
      f"pass2 {100*st['pass2']/c:.4f}%, pass3 {100*st['pass3']/c:.5f}%, exact {st['exact']:,}, "
      f"zero suspects {st['zero_suspect']:,}, hits {st['hits']}")

if MODE == "--gate":
    brute = 0
    for r in rows:
        op = [polys[i] for i in [0, 1, 2] + [int(v) for v in r]]
        for e in range(len(KIND)):
            a, b_ = op[LEFT[e]], op[RIGHT[e]]
            t = padd(a, b_) if KIND[e] == 0 else pmul(a, b_) if KIND[e] == 1 else psub(a, b_)
            if not t:
                continue
            for b in op:
                for f in (padd(t, b), psub(t, b)):
                    if f and len(integer_roots(f)) >= K:
                        brute += 1
    print(f"GATE k={K}: engine hits {st['hits']}, exhaustive exact count {brute}: "
          f"{'PASS' if brute == st['hits'] else 'FAIL'}")
