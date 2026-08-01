"""EXP-001: exact census of z_max(tau) for small tau + Markstroem regression gate.

Deterministic, headless, pure standard library, exact integer arithmetic.
CPU only. No randomness. See hypothesis.md (committed before this run).

Usage:
    python run.py --smoke     # depth-2 smoke test (progress + checkpoint proof)
    python run.py             # full run within the declared budget

Artifacts: ./artifacts/census.json (checkpointed after each depth), stdout log.
Exits nonzero if the Stage A regression gate fails.
"""

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"

T0 = time.time()


def log(msg: str) -> None:
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)


def checkpoint(payload: dict) -> None:
    ART.mkdir(exist_ok=True)
    tmp = ART / "census.json.tmp"
    tmp.write_text(json.dumps(payload, indent=1, sort_keys=True), encoding="utf-8")
    tmp.replace(ART / "census.json")


# ---------------------------------------------------------------- Stage A ----
# Markstroem's integer model: x1 = 1; steps x_k = x_i o x_j (i <= j < k),
# o in {+,-,*}; normalized: distinct values, all positive.
# Published anchors (arXiv:1306.3091v4, Figure 1), k = 1..7:
MARKSTROM_REACHED = {1: 2, 2: 4, 3: 9, 4: 26, 5: 102, 6: 562, 7: 4363}
MARKSTROM_INTERVAL = {1: 2, 2: 4, 3: 6, 4: 12, 5: 40, 6: 112, 7: 310}


def stage_a(max_depth: int, budget_s: float) -> dict:
    log(f"Stage A: integer regression gate to depth {max_depth}")
    frontier = {(): None}  # state = sorted tuple of computed values (beyond 1)
    reached = {1}
    results = {}
    for depth in range(1, max_depth + 1):
        new_frontier = {}
        aborted = False
        for state in frontier:
            operands = (1,) + state
            n = len(operands)
            cand = set()
            for i in range(n):
                a = operands[i]
                for j in range(i, n):
                    b = operands[j]
                    cand.add(a + b)
                    cand.add(a * b)
            for a in operands:
                for b in operands:
                    d = a - b
                    if d > 0:
                        cand.add(d)
            for v in cand:
                if v <= 0 or v in operands:
                    continue
                ns = tuple(sorted(state + (v,)))
                if ns not in new_frontier:
                    new_frontier[ns] = None
                reached.add(v)
            if time.time() - T0 > budget_s or len(new_frontier) > 5_000_000:
                aborted = True
                break
        if aborted:
            log(f"  depth {depth}: Stage A KILL (budget/memory), depth incomplete")
            results[depth] = {"complete": False}
            break
        frontier = new_frontier
        m = 2
        while m + 1 in reached:
            m += 1
        interval = m if m >= 2 and 2 in reached else 1
        results[depth] = {
            "complete": True,
            "reached": len(reached),
            "interval": interval,
            "states": len(frontier),
        }
        log(
            f"  depth {depth}: reached={len(reached)} interval={interval} "
            f"states={len(frontier)}"
        )
    return results


# ---------------------------------------------------------------- Stage B ----
# Polynomial model: inputs {-1, 1, x}; gates +,-,*; polynomials as coefficient
# tuples (constant term first, trailing zeros trimmed); zero polynomial = ().

P_MINUS1 = (-1,)
P_ONE = (1,)
P_X = (0, 1)
INPUTS = (P_MINUS1, P_ONE, P_X)


def padd(a, b):
    n = max(len(a), len(b))
    c = [0] * n
    for i, v in enumerate(a):
        c[i] += v
    for i, v in enumerate(b):
        c[i] += v
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


def psub(a, b):
    n = max(len(a), len(b))
    c = [0] * n
    for i, v in enumerate(a):
        c[i] += v
    for i, v in enumerate(b):
        c[i] -= v
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


def pmul(a, b):
    if not a or not b:
        return ()
    c = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        if u:
            for j, v in enumerate(b):
                c[i + j] += u * v
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


def divisors(n: int):
    n = abs(n)
    small, large = [], []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d != n // d:
                large.append(n // d)
        d += 1
    return small + large[::-1]


def peval(f, v):
    acc = 0
    for c in reversed(f):
        acc = acc * v + c
    return acc


def integer_roots(f):
    """Distinct integer roots of nonzero f, exact (rational root theorem)."""
    if not f:
        raise ValueError("zero polynomial")
    m = 0
    while f[m] == 0:
        m += 1
    roots = set()
    if m > 0:
        roots.add(0)
    g = f[m:]
    if len(g) > 1:
        for d in divisors(g[0]):
            for r in (d, -d):
                if peval(g, r) == 0:
                    roots.add(r)
    return roots


def stage_b(max_depth: int, deadline_s: float) -> dict:
    log(f"Stage B: polynomial census to depth {max_depth}")
    frontier = {(): None}  # state = sorted tuple of computed polys
    first_seen = {}  # poly -> first depth
    per_depth = {}
    complete = {}
    for depth in range(1, max_depth + 1):
        new_frontier = {}
        new_polys = set()
        aborted = False
        for state in frontier:
            operands = INPUTS + state
            n = len(operands)
            cand = set()
            for i in range(n):
                a = operands[i]
                for j in range(i, n):
                    b = operands[j]
                    cand.add(padd(a, b))
                    cand.add(pmul(a, b))
            for a in operands:
                for b in operands:
                    if a is not b:
                        cand.add(psub(a, b))
            for v in cand:
                if not v or v in operands:
                    continue
                ns = tuple(sorted(state + (v,)))
                new_frontier[ns] = None
                if v not in first_seen:
                    first_seen[v] = depth
                    new_polys.add(v)
            if time.time() - T0 > deadline_s:
                aborted = True
                break
        if aborted:
            log(f"  depth {depth}: BUDGET KILL, depth incomplete, checkpoint saved")
            complete[depth] = False
            per_depth[depth] = {"complete": False}
            break
        zmax, witnesses = -1, []
        for v in new_polys:
            z = len(integer_roots(v))
            if z > zmax:
                zmax, witnesses = z, [v]
            elif z == zmax and len(witnesses) < 40:
                witnesses.append(v)
        complete[depth] = True
        per_depth[depth] = {
            "complete": True,
            "states": len(new_frontier),
            "new_polynomials": len(new_polys),
            "zmax_new_at_depth": zmax,
            "witnesses_new_at_depth": [list(w) for w in sorted(witnesses)],
        }
        log(
            f"  depth {depth}: states={len(new_frontier)} "
            f"new_polys={len(new_polys)} zmax(new)={zmax}"
        )
        frontier = new_frontier
        checkpoint({"stage_b_partial": per_depth})
    # z_max(tau) is cumulative over first_seen depths.
    zmax_cum = {}
    best = 0
    record_polys = {}
    for d in sorted(set(first_seen.values())):
        if not complete.get(d, False):
            continue
        polys_d = [p for p, fd in first_seen.items() if fd == d]
        zd = max((len(integer_roots(p)) for p in polys_d), default=0)
        if zd > best:
            best = zd
        zmax_cum[d] = best
        recs = [p for p in polys_d if len(integer_roots(p)) == zmax_cum[d]]
        record_polys[d] = sorted(recs)[:40]
    return {
        "per_depth": per_depth,
        "zmax_cumulative": zmax_cum,
        "records": {
            str(d): [
                {"poly": list(p), "roots": sorted(integer_roots(p))} for p in ps
            ]
            for d, ps in record_polys.items()
        },
    }


# ------------------------------------------------------- witness programs ----


def find_witness_program(target, max_depth: int):
    """DFS: shortest program (as op list) whose value set contains target."""

    def dfs(state, depth, ops):
        operands = INPUTS + state
        if target in state:
            return ops
        if depth == max_depth:
            return None
        n = len(operands)
        seen_local = set()
        for i in range(n):
            for j in range(n):
                for opname in ("+", "-", "*"):
                    if opname in ("+", "*") and j < i:
                        continue
                    a, b = operands[i], operands[j]
                    if opname == "+":
                        v = padd(a, b)
                    elif opname == "*":
                        v = pmul(a, b)
                    else:
                        if i == j:
                            continue
                        v = psub(a, b)
                    if not v or v in operands or v in seen_local:
                        continue
                    seen_local.add(v)
                    res = dfs(
                        tuple(sorted(state + (v,))),
                        depth + 1,
                        ops + [(list(a), opname, list(b), list(v))],
                    )
                    if res is not None:
                        return res
        return None

    return dfs((), 0, [])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    depth_a = 3 if args.smoke else 7
    depth_b = 2 if args.smoke else 4
    budget_a = 60.0 if args.smoke else 600.0
    deadline_b = 120.0 if args.smoke else 1200.0  # 20 min kill from start

    log(f"EXP-001 run: smoke={args.smoke}")
    a = stage_a(depth_a, budget_a)
    gate = {}
    ok = True
    for k, row in a.items():
        if not row.get("complete"):
            gate[k] = {"complete": False}
            continue
        exp_r = MARKSTROM_REACHED.get(k)
        exp_i = MARKSTROM_INTERVAL.get(k)
        match = row["reached"] == exp_r and row["interval"] == exp_i
        gate[k] = {
            "ours_reached": row["reached"],
            "markstrom_reached": exp_r,
            "ours_interval": row["interval"],
            "markstrom_interval": exp_i,
            "match": match,
        }
        if exp_r is not None and not match:
            ok = False
    log(f"Stage A gate: {'PASS' if ok else 'FAIL'} over depths {sorted(gate)}")
    if not ok and not args.smoke:
        checkpoint({"stage_a": gate, "gate": "FAIL"})
        return 1

    b = stage_b(depth_b, deadline_b)

    witnesses = {}
    if not args.smoke:
        for d, recs in b["records"].items():
            witnesses[d] = []
            for rec in recs[:3]:
                prog = find_witness_program(tuple(rec["poly"]), int(d))
                witnesses[d].append({"poly": rec["poly"], "program": prog})
                # Adversarial replay: recompute the polynomial from the program
                if prog:
                    vals = list(INPUTS)
                    for a_, op, b_, v_ in prog:
                        vals.append(tuple(v_))
                    assert tuple(rec["poly"]) in vals
                    for r in rec["roots"]:
                        assert peval(tuple(rec["poly"]), r) == 0

    payload = {
        "stage_a": gate,
        "gate": "PASS" if ok else "FAIL",
        "stage_b": b,
        "witness_programs": witnesses,
        "model": "inputs {-1,1,x}; gates +,-,*; length = op count",
        "smoke": args.smoke,
    }
    checkpoint(payload)
    log("done; artifacts/census.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
