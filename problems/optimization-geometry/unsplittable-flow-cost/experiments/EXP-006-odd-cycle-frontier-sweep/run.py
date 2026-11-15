"""EXP-006: the frontier value on Afrasyab's odd-cycle family on C5 (hypothesis.md, frozen at b3aea839).

Exact rationals throughout; no floats in any decision. Stages:
  A  uniform calibration, eps in {1/120, 1/60, 1/24, 1/16, 1/13} (P1: frontier = 2/3 - eps);
  B  symmetric members, (b, delta) with max = 1, r, u, approach in sixths, every valid combination;
  C  2,000 valid non-uniform members drawn with seed 20261114;
  D  first-improvement local search (steps of 1/24) from the 10 best members of B and C, 150 evaluations per start.
Each evaluated member is one JSON line in artifacts/stage-<X>.jsonl (resumable: a member already recorded is not
re-evaluated). Run from the repository root:

    .venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-006-odd-cycle-frontier-sweep/run.py --stages ABCD --jobs 14

At the end it writes artifacts/summary.json and prints the verdict lines; exit 0 even when a prediction fails (the
verdict records it).
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from fractions import Fraction as F
from itertools import product
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

from ufclib.cutting_plane import frontier_value_cp  # noqa: E402
from ufclib.odd_cycle import afrasyab_uniform, odd_cycle_instance  # noqa: E402

ART = HERE / "artifacts"
N = 5
K = 2
NINE_EIGHTHS = F(9, 8)
EPS_A = [F(1, 120), F(1, 60), F(1, 24), F(1, 16), F(1, 13)]
PARAMS = ("b", "delta", "r", "u", "approach")


def key_of(p: dict) -> str:
    return json.dumps({k: [str(v) for v in p[k]] for k in PARAMS}, sort_keys=True)


def r4(p: dict) -> F:
    """The odd-cycle violation sum_i x(final_i)/b_i - k of the spec (R4), from the parameters."""
    total = F(0)
    for i in range(N):
        rsecond = p["r"][i] - p["u"][i - 1] + p["approach"][i]
        final = rsecond - (p["delta"][i] - p["u"][i])
        total += final / p["b"][i]
    return total - K


def build(p: dict):
    return odd_cycle_instance(N, p["b"], p["delta"], p["r"], p["u"], p["approach"])


def evaluate(task):
    stage, p = task
    inst = build(p)
    if inst is None:
        return {"stage": stage, "key": key_of(p), "valid": False}
    t0 = time.time()
    res = frontier_value_cp(inst)
    return {"stage": stage, "key": key_of(p), "valid": True,
            "params": {k: [str(v) for v in p[k]] for k in PARAMS},
            "alpha_max": str(res.alpha_max), "ceiling": str(res.ceiling),
            "witness_cost": [str(c) for c in res.witness_cost], "r4": str(r4(p)),
            "seconds": round(time.time() - t0, 2)}


def load(stage: str) -> dict:
    path = ART / f"stage-{stage}.jsonl"
    done = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done[r["key"]] = r
    return done


def run_pool(stage: str, members: list, jobs: int) -> dict:
    done = load(stage)
    todo = [(stage, p) for p in members if key_of(p) not in done]
    path = ART / f"stage-{stage}.jsonl"
    with path.open("a", encoding="utf-8") as fh, Pool(jobs) as pool:
        for r in pool.imap_unordered(evaluate, todo):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            done[r["key"]] = r
    return done


def uniform_params(eps: F) -> dict:
    T = F(K, 2 * (K + 1))
    t = T + eps
    s0 = F(1, 2) + eps
    b = s0 + t
    return {"b": [b] * N, "delta": [F(1)] * N, "r": [t + F(1, 2)] * N, "u": [F(1, 2)] * N,
            "approach": [F(1, 2)] * N}


def stage_a(jobs: int) -> list:
    rows = []
    for eps in EPS_A:
        p = uniform_params(eps)
        inst = build(p)
        ref = afrasyab_uniform(K, eps)
        same = inst is not None and [(a.tail, a.head, a.x) for a in inst.arcs] == [(a.tail, a.head, a.x) for a in ref.arcs]
        rows.append((eps, p, same))
    done = run_pool("A", [p for _, p, _ in rows], jobs)
    out = []
    for eps, p, same in rows:
        r = done[key_of(p)]
        out.append({"eps": str(eps), "alpha_max": r["alpha_max"], "predicted": str(F(2, 3) - eps),
                    "equal": F(r["alpha_max"]) == F(2, 3) - eps, "builder_equals_afrasyab_uniform": same})
    return out


def stage_b_members() -> list:
    sixths = [F(i, 6) for i in range(7)]
    pairs = [(F(1, 3), F(1)), (F(2, 3), F(1)), (F(1), F(1)), (F(1), F(1, 3)), (F(1), F(2, 3))]
    members = []
    for (b, d), r, u, ap in product(pairs, sixths, sixths, sixths):
        p = {"b": [b] * N, "delta": [d] * N, "r": [r] * N, "u": [u] * N, "approach": [ap] * N}
        if build(p) is not None:
            members.append(p)
    return members


def normalise(p: dict) -> dict:
    dmax = max(max(p["b"]), max(p["delta"]))
    return {k: [v / dmax for v in p[k]] for k in PARAMS}


def stage_c_members(count: int, seed: int) -> tuple[list, int]:
    rng = random.Random(seed)
    big = [F(i, 6) for i in range(1, 7)]
    small = [F(i, 12) for i in range(13)]
    members, invalid, seen = [], 0, set()
    while len(members) < count:
        p = {"b": [rng.choice(big) for _ in range(N)], "delta": [rng.choice(big) for _ in range(N)],
             "r": [rng.choice(small) for _ in range(N)], "u": [rng.choice(small) for _ in range(N)],
             "approach": [rng.choice(small) for _ in range(N)]}
        p = normalise(p)
        if build(p) is None:
            invalid += 1
            continue
        k = key_of(p)
        if k in seen:
            continue
        seen.add(k)
        members.append(p)
    return members, invalid


def neighbours(p: dict):
    step = F(1, 24)
    for name in PARAMS:
        for i in range(N):
            for sgn in (1, -1):
                q = {k: list(v) for k, v in p.items()}
                q[name][i] += sgn * step
                if q[name][i] < 0 or (name in ("b", "delta") and q[name][i] <= 0):
                    continue
                if build(q) is not None:
                    yield q


def climb(task):
    start, budget = task
    current = start
    cur = evaluate(("D", current))
    trace, evals = [cur], 1
    improved = True
    while improved and evals < budget:
        improved = False
        for q in neighbours(current):
            if evals >= budget:
                break
            r = evaluate(("D", q))
            evals += 1
            trace.append(r)
            if F(r["alpha_max"]) > F(cur["alpha_max"]):
                current, cur, improved = q, r, True
                break
    return {"start_key": key_of(start), "best": cur, "evaluations": evals, "trace": trace}


def from_record(r: dict) -> dict:
    return {k: [F(v) for v in r["params"][k]] for k in PARAMS}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stages", default="ABCD")
    ap.add_argument("--jobs", type=int, default=14)
    ap.add_argument("--count-c", type=int, default=2000)
    ap.add_argument("--starts-d", type=int, default=10)
    ap.add_argument("--budget-d", type=int, default=150)
    args = ap.parse_args()
    ART.mkdir(exist_ok=True)
    summary = {"hypothesis": "b3aea839", "instrument": "ufclib frontier_value_cp, PR #425 (2e064021)"}
    t0 = time.time()
    if "A" in args.stages:
        summary["A"] = stage_a(args.jobs)
        print("A", json.dumps(summary["A"]), flush=True)
    if "B" in args.stages:
        mb = stage_b_members()
        done = run_pool("B", mb, args.jobs)
        summary["B"] = {"members": len(mb)}
        print("B members", len(mb), "evaluated", sum(1 for r in done.values() if r["valid"]), flush=True)
    if "C" in args.stages:
        mc, invalid = stage_c_members(args.count_c, 20261114)
        done = run_pool("C", mc, args.jobs)
        summary["C"] = {"members": len(mc), "invalid_draws": invalid}
        print("C members", len(mc), "invalid draws", invalid, flush=True)
    if "D" in args.stages:
        pool_bc = [r for s in "BC" for r in load(s).values() if r["valid"]]
        pool_bc.sort(key=lambda r: F(r["alpha_max"]), reverse=True)
        starts = [from_record(r) for r in pool_bc[: args.starts_d]]
        path = ART / "stage-D.jsonl"
        with path.open("w", encoding="utf-8") as fh, Pool(min(args.jobs, len(starts) or 1)) as pool:
            for res in pool.imap_unordered(climb, [(s, args.budget_d) for s in starts]):
                fh.write(json.dumps(res) + "\n")
                fh.flush()
        summary["D"] = {"starts": len(starts)}
    # summary over every evaluated member
    allrec = []
    for s in "ABC":
        allrec += [r for r in load(s).values() if r.get("valid")]
    dpath = ART / "stage-D.jsonl"
    if dpath.exists():
        for line in dpath.read_text(encoding="utf-8").splitlines():
            if line.strip():
                allrec += json.loads(line)["trace"]
    best = {}
    for s in "ABCD":
        rs = [r for r in allrec if r["stage"] == s]
        if rs:
            top = max(rs, key=lambda r: F(r["alpha_max"]))
            best[s] = {"count": len(rs), "max_alpha": top["alpha_max"], "params": top["params"], "r4": top["r4"],
                       "witness_cost": top["witness_cost"],
                       "above_9_8": sum(1 for r in rs if F(r["alpha_max"]) > NINE_EIGHTHS),
                       "above_1": sum(1 for r in rs if F(r["alpha_max"]) > 1)}
    summary["best"] = best
    bcd = [r for r in allrec if r["stage"] in "BCD"]
    summary["P1"] = all(x["equal"] for x in summary.get("A", [])) if "A" in summary else None
    summary["P2"] = all(F(r["alpha_max"]) <= NINE_EIGHTHS for r in bcd) if bcd else None
    summary["P3"] = all(F(r["alpha_max"]) <= 1 for r in bcd) if bcd else None
    summary["wall_seconds"] = round(time.time() - t0, 1)
    (ART / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("P1", summary["P1"], "P2", summary["P2"], "P3", summary["P3"], flush=True)
    for s, b in best.items():
        print(s, b["count"], "max", b["max_alpha"], "above 9/8", b["above_9_8"], "above 1", b["above_1"], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
