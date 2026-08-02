"""EXP-006: the [8,9] window, part 1 (the times-case, exact) + part 2 (hunt).

Deterministic, exact. See hypothesis.md (committed before the run).
Usage: python run.py [--smoke]
  smoke: decide "7-gate 6-rooter with final x" over the depth-5 frontier
  (must be EMPTY, since z_max(7) = 5) and check frontier gates.
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


def log(msg):
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)


def checkpoint(payload):
    ART.mkdir(exist_ok=True)
    tmp = ART / "window.json.tmp"
    tmp.write_text(json.dumps(payload, indent=1, sort_keys=True),
                   encoding="utf-8")
    tmp.replace(ART / "window.json")


class Engine:
    def __init__(self):
        self.polys = [(-1,), (1,), (0, 1)]
        self.pid = {(-1,): 0, (1,): 1, (0, 1): 2}
        self.cache = {}
        self.roots = {}   # id -> frozenset of integer roots
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


def expand(eng, frontier, depth_expected=None):
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
        for ia in operands:
            for ib in operands:
                if ia != ib:
                    r = eng.op(2, ia, ib)
                    if r != eng.ZERO and r not in oset:
                        new_frontier.add(tuple(sorted(state + (r,))))
    if depth_expected is not None and len(new_frontier) != depth_expected:
        raise SystemExit(f"GATE FAIL: frontier {len(new_frontier)} != "
                         f"{depth_expected}")
    return new_frontier


def times_case_scan(eng, frontier, deadline, progress_every=1_000_000):
    """Exact decision of the final-times case one depth past `frontier`.

    For each state S and each valid extension v (one op over S's operands),
    check whether |R_v union R_b| >= 6 for some operand b of S (or input).
    Returns (hits, complete, states_scanned, fiverooter_rootsets)."""
    hits = []
    fivesets = {}
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
            rv = eng.rootset(v)
            zv = len(rv)
            if zv == 5:
                fivesets[v] = rv
            if zv + maxz < 6:
                continue
            for b, rb in zip(operands, rsets):
                if len(rv | rb) >= 6:
                    hits.append({
                        "state": [list(eng.polys[i]) for i in state],
                        "v": list(eng.polys[v]),
                        "b": list(eng.polys[b]),
                        "union_roots": sorted(rv | rb),
                    })
        count += 1
        if count % progress_every == 0:
            log(f"  scanned {count} states, hits={len(hits)}, "
                f"5-rooter ids={len(fivesets)}")
        if time.time() > deadline:
            complete = False
            break
    return hits, complete, count, fivesets


def hunt_part2(eng):
    """Grammar-restricted construction hunt: generate EXPLICIT programs of
    <= 8 gates from the split-quadratic / DOS / shift schema families and
    test z >= 6. Sound upper bounds only (each candidate is an actual
    program; its gate count is exact by construction)."""
    found = []
    X = (0, 1)

    def build_const(n):
        """Return (gates, program-values) building integer constant n >= 2
        greedily by binary decomposition from 1; exact gate count."""
        # simple exact-ish builder: binary method
        vals = []
        gates = 0
        cur = 1
        # build by doubling/adding 1 from 1: cost = bits + popcount - 2-ish
        bits = bin(n)[3:]
        cur = 1
        for ch in bits:
            cur = cur * 2
            gates += 1
            vals.append(cur)
            if ch == "1":
                cur += 1
                gates += 1
                vals.append(cur)
        return gates, vals

    # Schema A: f = (q - c1)(q - c2)(q - c3), q = x^2 + a*x (a in {-1,0,1}
    # via 1-gate shifts), each factor splitting over Z.
    for a in (-1, 0, 1):
        # q gates: x*x (1) [+ x or - x (1 more) if a != 0]
        qgates = 1 + (1 if a else 0)
        q = (0, a, 1)
        for c1 in range(0, 31):
            for c2 in range(c1 + 1, 31):
                for c3 in range(c2 + 1, 31):
                    f = pmul(pmul(psub(q, (c1,)) if c1 else q,
                                  psub(q, (c2,))), psub(q, (c3,)))
                    roots = integer_roots(f)
                    if len(roots) >= 6:
                        # exact gate accounting: q + constants + subs + muls
                        g = qgates
                        built = {0: 0, 1: 0}
                        consts = [c for c in (c1, c2, c3) if c >= 2]
                        # share constant-building greedily: build max, reuse
                        # intermediate doubling values
                        allvals = set([1])
                        for c in sorted(set(consts)):
                            bg, vals = build_const(c)
                            new = [v for v in vals if v not in allvals]
                            g += len(new)
                            allvals.update(vals)
                        g += sum(1 for c in (c1, c2, c3) if c != 0)  # subs
                        g += 2  # two multiplications
                        if g <= 8:
                            found.append({
                                "schema": "A", "a": a,
                                "c": [c1, c2, c3],
                                "roots": sorted(roots), "gates": g,
                            })
    # Schema B: f = x * (five-rooter shapes): covered by the times-case
    # scan exactly; not repeated here.
    # Schema C: DOS on cubics: f = p^2 - r^2 with p cubic; p - r and p + r
    # both split. Parameterized: p = x^3 + u*x, r = w (constant) or r = x.
    for u in range(-10, 11):
        p = (0, u, 0, 1)
        for r0 in list(range(0, 40)):
            for rpoly, rgadd in (((r0,), 0), ((r0, 1), 1)):
                f = psub(pmul(p, p), pmul(rpoly, rpoly))
                if not f:
                    continue
                roots = integer_roots(f)
                if len(roots) >= 6:
                    found.append({
                        "schema": "C", "u": u, "r": list(rpoly),
                        "roots": sorted(roots),
                        "gates": "UNACCOUNTED (candidate; count by hand)",
                    })
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    base_depth = 5 if args.smoke else 6
    deadline = T0 + (600 if args.smoke else 12600)  # 3.5 h overall

    log("part 2 first: construction hunt (grammar-restricted)")
    eng0 = Engine()
    hunt = hunt_part2(eng0)
    hunt8 = [h for h in hunt if isinstance(h.get("gates"), int)
             and h["gates"] <= 8]
    log(f"hunt: {len(hunt)} candidate 6-rooters in schemas, "
        f"{len(hunt8)} with proved gates <= 8")
    checkpoint({"hunt": hunt, "hunt8": hunt8})
    if hunt8:
        log("HUNT FOUND an 8-gate 6-rooter candidate; scan continues anyway")

    eng = Engine()
    frontier = {()}
    log(f"part 1: rebuild frontier to depth {base_depth}")
    for depth in range(1, base_depth + 1):
        frontier = expand(eng, frontier, EXPECTED_STATES.get(depth))
        log(f"  depth {depth}: states={len(frontier)} "
            f"(cache={len(eng.cache)})")
    log("frontier gates PASS")

    hits, complete, scanned, fivesets = times_case_scan(
        eng, frontier, deadline)
    log(f"times-case scan: complete={complete} states={scanned} "
        f"hits={len(hits)}")

    fs_summary = {}
    for v, rs in fivesets.items():
        key = str(sorted(rs))
        fs_summary[key] = fs_summary.get(key, 0) + 1

    payload = {
        "base_depth": base_depth,
        "times_case_hits": hits[:50],
        "times_case_hit_count": len(hits),
        "scan_complete": complete,
        "states_scanned": scanned,
        "fiverooter_rootset_summary": fs_summary,
        "hunt_candidates": len(hunt),
        "hunt_8gate": hunt8,
        "smoke": args.smoke,
    }
    checkpoint(payload)
    log("done; artifacts/window.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
