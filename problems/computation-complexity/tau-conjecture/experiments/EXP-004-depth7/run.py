"""EXP-004: exact z_max(7) via depth-6 frontier build + last-gate scan.

Optimized interned engine (polys as ids, op-result memo with size cap),
gated against EXP-001/002/003 anchors before stage 2 is trusted. Exact
arithmetic; no pruning beyond the proved normalization lemmas.

Usage: python run.py [--smoke]   (smoke: base depth 5, reproduces EXP-003)
"""

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

from tclib.enum import (  # noqa: E402
    integer_roots,
    padd,
    peval,
    pmul,
    psub,
    two_adic_valuations,
)

T0 = time.time()
ART = HERE / "artifacts"

EXPECTED_STATES = {1: 9, 2: 98, 3: 1462, 4: 29506, 5: 778087}
EXPECTED_NEW = {1: 9, 2: 34, 3: 177, 4: 1249, 5: 11377, 6: 134494}
EXPECTED_ZMAX = {1: 1, 2: 2, 3: 3, 4: 3, 5: 4, 6: 5}

CACHE_CAP = 40_000_000
STATE_CAP = 30_000_000


def log(msg):
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)


def checkpoint(payload):
    ART.mkdir(exist_ok=True)
    tmp = ART / "scan7.json.tmp"
    tmp.write_text(json.dumps(payload, indent=1, sort_keys=True),
                   encoding="utf-8")
    tmp.replace(ART / "scan7.json")


class Engine:
    def __init__(self):
        self.polys = [(-1,), (1,), (0, 1)]
        self.pid = {(-1,): 0, (1,): 1, (0, 1): 2}
        self.cache = {}
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
        if len(self.cache) < CACHE_CAP:
            self.cache[key] = r
        return r


def expand(eng, frontier, first_seen, depth, deadline):
    """One BFS level; returns (new_frontier, complete)."""
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
                    if r == eng.ZERO or r in oset:
                        continue
                    new_frontier.add(tuple(sorted(state + (r,))))
                    if r not in first_seen:
                        first_seen[r] = depth
        for ia in operands:
            for ib in operands:
                if ia != ib:
                    r = eng.op(2, ia, ib)
                    if r == eng.ZERO or r in oset:
                        continue
                    new_frontier.add(tuple(sorted(state + (r,))))
                    if r not in first_seen:
                        first_seen[r] = depth
        if time.time() > deadline or len(new_frontier) > STATE_CAP:
            return new_frontier, False
    return new_frontier, True


def scan(eng, frontier, known_ids, deadline, progress_every=1_000_000):
    new_ids = set()
    count = 0
    for state in frontier:
        operands = (0, 1, 2) + state
        n = len(operands)
        for i in range(n):
            ia = operands[i]
            for j in range(i, n):
                ib = operands[j]
                for o in (0, 1):
                    r = eng.op(o, ia, ib)
                    if r != eng.ZERO and r not in known_ids and \
                            r not in new_ids:
                        new_ids.add(r)
        for ia in operands:
            for ib in operands:
                if ia != ib:
                    r = eng.op(2, ia, ib)
                    if r != eng.ZERO and r not in known_ids and \
                            r not in new_ids:
                        new_ids.add(r)
        count += 1
        if count % progress_every == 0:
            log(f"  scanned {count} states, {len(new_ids)} new polys, "
                f"cache={len(eng.cache)}")
        if time.time() > deadline:
            return new_ids, False, count
    return new_ids, True, count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    base_depth = 5 if args.smoke else 6
    deadline1 = T0 + (240 if args.smoke else 6000)   # stage-1 kill
    deadline2 = T0 + (600 if args.smoke else 10200)  # overall kill (170 min)

    eng = Engine()
    first_seen = {}
    frontier = {()}
    log(f"EXP-004 stage 1: build frontier to depth {base_depth}")
    for depth in range(1, base_depth + 1):
        frontier, ok = expand(eng, frontier, first_seen, depth, deadline1)
        news = sum(1 for d in first_seen.values() if d == depth)
        log(f"  depth {depth}: states={len(frontier)} new_polys={news} "
            f"cache={len(eng.cache)}")
        if not ok:
            log("  stage 1 KILL (budget/memory)")
            checkpoint({"stage": 1, "aborted_depth": depth,
                        "states": len(frontier)})
            return 1
        exp_s, exp_n = EXPECTED_STATES.get(depth), EXPECTED_NEW.get(depth)
        if exp_s is not None and len(frontier) != exp_s:
            log(f"GATE FAIL: states at depth {depth}")
            checkpoint({"gate": "FAIL", "depth": depth})
            return 1
        if exp_n is not None and news != exp_n:
            log(f"GATE FAIL: new polys at depth {depth}")
            checkpoint({"gate": "FAIL", "depth": depth})
            return 1
        checkpoint({"stage": 1, "depth": depth, "states": len(frontier)})

    # z_max gate on the base depth (recompute from first_seen).
    zmax_base = 0
    for r, d in first_seen.items():
        if d <= base_depth:
            z = len(integer_roots(eng.polys[r]))
            if z > zmax_base:
                zmax_base = z
    if zmax_base != EXPECTED_ZMAX[base_depth]:
        log(f"GATE FAIL: z_max({base_depth}) = {zmax_base}")
        checkpoint({"gate": "FAIL", "zmax_base": zmax_base})
        return 1
    log(f"stage-1 gates PASS (z_max({base_depth}) = {zmax_base})")

    log("EXP-004 stage 2: last-gate scan")
    known_ids = set(first_seen) | {0, 1, 2}
    new_ids, complete, scanned = scan(eng, frontier, known_ids, deadline2)
    log(f"scan: complete={complete} states={scanned} "
        f"new_polys={len(new_ids)}")

    zmax, records, zcounts = zmax_base, [], {}
    for r in new_ids:
        z = len(integer_roots(eng.polys[r]))
        zcounts[z] = zcounts.get(z, 0) + 1
        if z > zmax:
            zmax, records = z, [r]
        elif z == zmax and z > zmax_base and len(records) < 40:
            records.append(r)
    log(f"z_max({base_depth + 1}) = {zmax} "
        f"(records beyond base: {len(records)})")

    rec_payload = []
    for r in sorted(records, key=lambda i: eng.polys[i]):
        p = eng.polys[r]
        roots = sorted(integer_roots(p))
        for rt in roots:
            assert peval(p, rt) == 0
        rec_payload.append({
            "poly": list(p),
            "roots": roots,
            "twoadic_valuations_nonzero_roots":
                sorted(two_adic_valuations(set(roots))),
        })

    payload = {
        "base_depth": base_depth,
        "stage1_states": len(frontier),
        "scan_complete": complete,
        "states_scanned": scanned,
        "new_polynomials": len(new_ids),
        "z_histogram_new": {str(k): v for k, v in sorted(zcounts.items())},
        "zmax": zmax,
        "records_beyond_base": rec_payload,
        "smoke": args.smoke,
    }
    checkpoint(payload)
    log("done; artifacts/scan7.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
