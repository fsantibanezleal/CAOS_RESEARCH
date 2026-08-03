"""EXP-007: full-retention times-case re-scan (max union) + the digit census.

Deterministic, exact. See hypothesis.md (committed before the run).
Usage: python run.py [--smoke]
"""

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

from tclib.enum import integer_roots, padd, pmul, psub  # noqa: E402

T0 = time.time()
ART = HERE / "artifacts"
EXPECTED_STATES = {1: 9, 2: 98, 3: 1462, 4: 29506, 5: 778087, 6: 25844905}
EXPECTED_HITS_GE6 = 408  # EXP-006 anchor (full run only)


def log(msg):
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)


def checkpoint(payload):
    ART.mkdir(exist_ok=True)
    tmp = ART / "union7.json.tmp"
    tmp.write_text(json.dumps(payload, indent=1, sort_keys=True),
                   encoding="utf-8")
    tmp.replace(ART / "union7.json")


class Engine:
    def __init__(self):
        self.polys = [(-1,), (1,), (0, 1)]
        self.pid = {(-1,): 0, (1,): 1, (0, 1): 2}
        self.cache = {}
        self.roots = {}
        self.ZERO = -1

    def intern(self, t):
        i = self.pid.get(t)
        if i is None:
            i = len(self.polys)
            self.polys.append(t)
            self.pid[t] = i
        return i

    def op(self, o, ia, ib):
        key = (o, ia, ib)
        r = self.cache.get(key)
        if r is not None:
            return r
        a, b = self.polys[ia], self.polys[ib]
        v = padd(a, b) if o == 0 else pmul(a, b) if o == 1 else psub(a, b)
        r = self.ZERO if not v else self.intern(v)
        if len(self.cache) < 60_000_000:
            self.cache[key] = r
        return r

    def rootset(self, i):
        r = self.roots.get(i)
        if r is None:
            r = frozenset(integer_roots(self.polys[i]))
            self.roots[i] = r
        return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    base_depth = 5 if args.smoke else 6
    deadline = T0 + (600 if args.smoke else 12600)

    eng = Engine()
    first_seen = {}
    frontier = {()}
    log(f"stage 1: frontier to depth {base_depth} (with first_seen)")
    for depth in range(1, base_depth + 1):
        new_frontier = set()
        for state in frontier:
            operands = (0, 1, 2) + state
            oset = set(operands)
            n = len(operands)
            for i in range(n):
                ia = operands[i]
                for j in range(i, n):
                    ib = operands[j]
                    for o in (0, 1):
                        r = eng.op(o, ia, ib)
                        if r != eng.ZERO and r not in oset:
                            new_frontier.add(tuple(sorted(state + (r,))))
                            if r not in first_seen:
                                first_seen[r] = depth
        for state in frontier:
            operands = (0, 1, 2) + state
            oset = set(operands)
            for ia in operands:
                for ib in operands:
                    if ia != ib:
                        r = eng.op(2, ia, ib)
                        if r != eng.ZERO and r not in oset:
                            new_frontier.add(tuple(sorted(state + (r,))))
                            if r not in first_seen:
                                first_seen[r] = depth
        frontier = new_frontier
        if len(frontier) != EXPECTED_STATES[depth]:
            log(f"GATE FAIL depth {depth}: {len(frontier)}")
            return 1
        log(f"  depth {depth}: states={len(frontier)}")

    log("stage 2: full-retention times-case scan + depth catalog")
    hits = []
    fivepolys = {}
    top_depth = {}
    count = 0
    complete = True
    for state in frontier:
        operands = (0, 1, 2) + state
        oset = set(operands)
        rsets = [eng.rootset(i) for i in operands]
        maxz = max(len(r) for r in rsets)
        n = len(operands)
        cand = set()
        for i in range(n):
            ia = operands[i]
            for j in range(i, n):
                ib = operands[j]
                for o in (0, 1):
                    r = eng.op(o, ia, ib)
                    if r != eng.ZERO and r not in oset:
                        cand.add(r)
        for ia in operands:
            for ib in operands:
                if ia != ib:
                    r = eng.op(2, ia, ib)
                    if r != eng.ZERO and r not in oset:
                        cand.add(r)
        for v in cand:
            if v not in first_seen and v not in top_depth:
                top_depth[v] = base_depth + 1
            rv = eng.rootset(v)
            zv = len(rv)
            if zv == 5:
                fivepolys[v] = True
            if zv + maxz < 6:
                continue
            for b, rb in zip(operands, rsets):
                u = rv | rb
                if len(u) >= 6:
                    hits.append((len(u), list(eng.polys[v]),
                                 list(eng.polys[b]), sorted(u)))
        count += 1
        if count % 1_000_000 == 0:
            log(f"  scanned {count}, hits={len(hits)}")
        if time.time() > deadline:
            complete = False
            break
    log(f"scan: complete={complete} states={count} hits={len(hits)}")

    max_union = max((h[0] for h in hits), default=0)
    union_hist = {}
    for h in hits:
        union_hist[h[0]] = union_hist.get(h[0], 0) + 1

    # Digit census over the full catalog (tau <= base_depth+1).
    log("digit census")
    ladders = {}
    for p, digit in ((2, 1), (3, 1)):
        best = 0
        ladder = {}
        for d in range(1, base_depth + 2):
            for i, fd in list(first_seen.items()) + list(top_depth.items()):
                if fd == d:
                    c = sum(1 for r in eng.rootset(i) if r % p == digit)
                    if c > best:
                        best = c
            ladder[d] = best
        ladders[f"p{p}_digit{digit}"] = ladder

    payload = {
        "base_depth": base_depth,
        "scan_complete": complete,
        "states_scanned": count,
        "hit_count_ge6": len(hits),
        "union_histogram": union_hist,
        "max_union": max_union,
        "hits_ge7": [h for h in hits if h[0] >= 7][:50],
        "fiverooter_polys": [list(eng.polys[i]) for i in sorted(fivepolys)],
        "digit_ladders": ladders,
        "smoke": args.smoke,
    }
    if not args.smoke and complete and len(hits) != EXPECTED_HITS_GE6:
        payload["gate"] = "HIT-COUNT MISMATCH vs EXP-006"
        log("WARNING: hit count differs from EXP-006's 408")
    checkpoint(payload)
    log(f"done; max_union={max_union}; ladders={ladders}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
