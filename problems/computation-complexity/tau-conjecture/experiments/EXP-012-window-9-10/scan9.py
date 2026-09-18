"""EXP-012 phase B: the 9-gate seven-rooter decision (final gate times).

For every depth-7 state S7 in the stored frontier, every one-gate
extension v8, and every operand b of S7 (or an input), test
|R_v8 union R_b| >= THRESHOLD. Pruned by z(v8) + max_b z(b) >= THRESHOLD.

Usage:
  python scan9.py --gate      (known-answer: threshold 6 on one partition;
                               must find hits)
  python scan9.py             (production: threshold 7, all 256 partitions)

Resumable: per-partition JSON in artifacts/scan9_parts_<ns>/.
"""

import argparse
import json
import pickle
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

T0 = time.time()
ART = HERE / "artifacts"
ASSETS = Path("E:/_Datos/caos-research/tau-conjecture")
FRONTIER = ASSETS / "frontier7"
POLYS = ASSETS / "polys.pkl"
WIDTH = 7


def log(msg):
    print(f"[{time.time() - T0:9.1f}s] {msg}", flush=True)


def worker(task):
    part, threshold, ns = task
    out = ART / f"scan9_parts_{ns}" / f"part{part:03d}.json"
    if out.exists():
        return part
    sys.path.insert(0, str(HERE.parent.parent / "code"))
    from tclib.enum import integer_roots, padd, pmul, psub
    with open(POLYS, "rb") as fh:
        polys = pickle.load(fh)["polys"]
    f = FRONTIER / f"uniq{part:03d}.bin"
    if not f.exists():
        res = {"part": part, "states": 0, "hits": [], "hit_count": 0,
               "max_union": 0}
    else:
        arr = np.fromfile(f, dtype=np.int32).reshape(-1, WIDTH)
        opcache = {}
        rootmemo = {}
        fns = (padd, pmul, psub)
        hits = []
        max_union = 0

        def rootset(i):
            r = rootmemo.get(i)
            if r is None:
                p = polys[i]
                r = frozenset(integer_roots(p)) if p else frozenset()
                if len(rootmemo) < 3_000_000:
                    rootmemo[i] = r
            return r

        def rootset_poly(t, key):
            r = rootmemo.get(key)
            if r is None:
                r = frozenset(integer_roots(t))
                if len(rootmemo) < 3_000_000:
                    rootmemo[key] = r
            return r

        for row in arr:
            state = tuple(int(x) for x in row)
            operands = (0, 1, 2) + state
            opolys = [polys[i] for i in operands]
            rsets = [rootset(i) for i in operands]
            maxz = max(len(r) for r in rsets)
            if maxz == 0:
                continue          # would need z(v8) >= 7 > z_max(8) = 6
            need = threshold - maxz
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
                            if len(opcache) < 4_000_000:
                                opcache[key] = t
                        if not t:
                            continue
                        rv = rootset_poly(t, ("p",) + key)
                        if len(rv) < need:
                            continue
                        for bi, rb in zip(operands, rsets):
                            u = len(rv | rb)
                            if u > max_union:
                                max_union = u
                            if u >= threshold:
                                hits.append({
                                    "state": [int(x) for x in row],
                                    "v8": list(t),
                                    "b": list(polys[bi]),
                                    "union_roots": sorted(rv | rb),
                                })
        res = {"part": part, "states": int(arr.shape[0]),
               "hit_count": len(hits), "hits": hits[:20],
               "max_union": max_union}
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(res), "utf-8")
    tmp.replace(out)
    return part


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--nproc", type=int, default=20)
    args = ap.parse_args()

    if args.gate:
        log("known-answer gate: threshold 6 on partition 0")
        worker((0, 6, "gate"))
        d = json.loads((ART / "scan9_parts_gate" / "part000.json")
                       .read_text("utf-8"))
        ok = d["hit_count"] > 0
        log(f"GATE: states={d['states']} hits={d['hit_count']} "
            f"max_union={d['max_union']}: {'PASS' if ok else 'FAIL'}")
        (ART / "scan9_gate.json").write_text(json.dumps(d), "utf-8")
        return 0 if ok else 1

    parts = list(range(256))
    tasks = [(p, 7, "final") for p in parts]
    done = 0
    with Pool(processes=args.nproc) as pool:
        for _ in pool.imap_unordered(worker, tasks):
            done += 1
            if done % 16 == 0:
                log(f"  partitions done: {done}/256")
    states = hit_count = 0
    max_union = 0
    hits = []
    for p in parts:
        d = json.loads((ART / "scan9_parts_final" / f"part{p:03d}.json")
                       .read_text("utf-8"))
        states += d["states"]
        hit_count += d["hit_count"]
        max_union = max(max_union, d["max_union"])
        hits.extend(d["hits"])
    log(f"SCAN9: states={states} hits(z>=7)={hit_count} "
        f"max_union={max_union}")
    (ART / "scan9_final.json").write_text(json.dumps(
        {"states": states, "hit_count": hit_count, "max_union": max_union,
         "hits": hits[:50]}), "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
