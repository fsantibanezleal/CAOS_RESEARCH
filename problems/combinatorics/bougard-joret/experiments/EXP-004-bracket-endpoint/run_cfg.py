"""EXP-004 configuration-split SAT check at fixed d (corroboration of proof.md, not part of the proof).

Uses only the structure facts of proof.md Section 2 (re-derived by the independent audit): an extremal F has
an induced five-cycle 0-1-2-3-4; every other vertex either is typed (its cycle neighbours are exactly
c_(t-1), c_(t+1) for a type t in 0..4) or is defective (at most one cycle neighbour), with at most two defective
vertices. One configuration fixes the cycle neighbours of the defective vertices up to rotation and reflection:

  ""      no defective vertex
  "-"     one defective vertex without cycle neighbour
  "0"     one defective vertex adjacent to c_0
  "0,0" "0,1" "0,2"   two defective vertices adjacent to c_0 and c_q
  "-,0" "-,-"         two defective vertices, one or both without cycle neighbour

Each typed vertex carries a one-hot type; types are non-decreasing in vertex order (symmetry breaking among
typed vertices only). Constraints: triangle-free, maximum degree <= d, exactly d*d+d+2 edges, and, with --k2d,
no two vertices with d common neighbours. UNSAT with --k2d for every configuration corroborates Theorem 2 at
this d; --free runs are controls showing the encoding admits extremal graphs.

Usage: python run_cfg.py (--k2d | --free) [--timeout S] -- <d> <config>   (the "--" lets a config start with "-")
Appends one JSON line to artifacts/cfg-d<d>.jsonl.
"""
import argparse
import itertools
import json
import time
from pathlib import Path

import z3

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("d", type=int)
    ap.add_argument("config")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--k2d", action="store_true")
    g.add_argument("--free", action="store_true")
    ap.add_argument("--timeout", type=int, default=3600)
    a = ap.parse_args()
    d = a.d
    n = 2 * d + 3
    target = d * d + d + 2
    defects = [] if a.config == "" else [(None if c == "-" else int(c)) for c in a.config.split(",")]
    r = len(defects)
    C = list(range(5))
    D = list(range(5, 5 + r))
    T = list(range(5 + r, n))
    E = {(i, j): z3.Bool(f"e_{i}_{j}") for i, j in itertools.combinations(range(n), 2)}

    def e(i, j):
        return E[(min(i, j), max(i, j))]

    s = z3.Solver()
    s.set("timeout", a.timeout * 1000)
    for i in C:                                   # induced five-cycle
        for j in C:
            if i < j:
                s.add(e(i, j) if (j - i) % 5 in (1, 4) else z3.Not(e(i, j)))
    for x, c in zip(D, defects):                  # defective vertices: fixed cycle neighbourhood
        for j in C:
            s.add(e(x, j) if j == c else z3.Not(e(x, j)))
    typ = {v: [z3.Bool(f"t_{v}_{t}") for t in range(5)] for v in T}
    for v in T:                                   # typed vertices: one-hot type, cycle neighbours c_(t+-1)
        s.add(z3.PbEq([(b, 1) for b in typ[v]], 1))
        for t in range(5):
            for j in C:
                adj = (j - t) % 5 in (1, 4)
                s.add(z3.Implies(typ[v][t], e(v, j) if adj else z3.Not(e(v, j))))
    for u, v in zip(T, T[1:]):                    # non-decreasing types
        for t in range(5):
            s.add(z3.Implies(typ[v][t], z3.Or([typ[u][q] for q in range(t + 1)])))
    for i, j, k in itertools.combinations(range(n), 3):
        s.add(z3.Not(z3.And(e(i, j), e(j, k), e(i, k))))
    for v in range(n):
        s.add(z3.PbLe([(e(v, u), 1) for u in range(n) if u != v], d))
    s.add(z3.PbEq([(x, 1) for x in E.values()], target))
    if a.k2d:
        for u, v in itertools.combinations(range(n), 2):
            s.add(z3.PbLe([(z3.And(e(u, w), e(v, w)), 1) for w in range(n) if w not in (u, v)], d - 1))
    t0 = time.time()
    res = str(s.check())
    rec = {"d": d, "config": a.config, "mode": "k2d" if a.k2d else "free", "result": res,
           "seconds": round(time.time() - t0, 1), "timeout": a.timeout}
    if res == "sat":
        m = s.model()
        rec["edges"] = sorted([list(k) for k, x in E.items() if z3.is_true(m.eval(x))])
    (HERE / "artifacts").mkdir(exist_ok=True)
    with open(HERE / "artifacts" / f"cfg-d{d}.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "edges"}), flush=True)


if __name__ == "__main__":
    main()
