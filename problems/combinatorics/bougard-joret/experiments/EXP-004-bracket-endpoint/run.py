"""EXP-004 finite corroboration: exhaustive SMT search for a counterexample at fixed d.

Searches for a triangle-free graph F on n = 2d+3 vertices with maximum degree <= d
and at least d*d+d+2 edges whose complement is (d+2)-connected. The five-cycle
0-1-2-3-4-0 is fixed as an induced cycle (every such F is nonbipartite with a
shortest odd cycle of length five; proof.md Section 2, EXP-003 Lemma 3), which is
the only symmetry reduction.

Lazy cuts: every model is checked by an exact vertex-connectivity computation on
its complement (networkx). If the complement has a vertex cut S with |S| <= d+1,
the components of complement - S are split into two nonempty sides U, W; all U-W
pairs are edges of F, so the clause "some U-W pair is a non-edge" is added. A
model whose complement is (d+2)-connected is a counterexample and is written out.

Usage: python run.py <d> [--max-iter N] [--gate] [--no-k2d]
Writes artifacts/search-d<d>.json (artifacts/gate-d<d>.json with --gate).
"""
import argparse
import itertools
import json
import time
from pathlib import Path

import networkx as nx
import z3

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("d", type=int)
    ap.add_argument("--max-iter", type=int, default=200000)
    ap.add_argument("--gate", action="store_true",
                    help="known-answer gate: target d*d+d+1, where a good graph exists (must be found)")
    ap.add_argument("--no-k2d", action="store_true",
                    help="also forbid two vertices with d common neighbours (a K_(2,d), itself a cut on d+2 "
                         "vertices); UNSAT then implies UNSAT without it")
    a = ap.parse_args()
    d = a.d
    n = 2 * d + 3
    target = d * d + d + 2 - (1 if a.gate else 0)
    E = {}
    for i, j in itertools.combinations(range(n), 2):
        E[(i, j)] = z3.Bool(f"e_{i}_{j}")

    def e(i, j):
        return E[(min(i, j), max(i, j))]

    s = z3.Solver()
    for i, j, k in itertools.combinations(range(n), 3):
        s.add(z3.Not(z3.And(e(i, j), e(j, k), e(i, k))))
    for v in range(n):
        s.add(z3.PbLe([(e(v, u), 1) for u in range(n) if u != v], d))
    s.add(z3.PbGe([(x, 1) for x in E.values()], target))
    if a.no_k2d:
        for u, v in itertools.combinations(range(n), 2):
            s.add(z3.PbLe([(z3.And(e(u, w), e(v, w)), 1) for w in range(n) if w not in (u, v)], d - 1))
    for i in range(5):
        s.add(e(i, (i + 1) % 5))
        s.add(z3.Not(e(i, (i + 2) % 5)))
    t0 = time.time()
    cuts = 0
    status, witness = None, None
    sizes = {}
    while cuts < a.max_iter:
        r = s.check()
        if r == z3.unsat:
            status = "UNSAT"
            break
        if r != z3.sat:
            status = f"UNKNOWN ({r})"
            break
        m = s.model()
        F = nx.Graph()
        F.add_nodes_from(range(n))
        F.add_edges_from(k for k, x in E.items() if z3.is_true(m.eval(x)))
        G = nx.complement(F)
        cut = nx.minimum_node_cut(G)
        if len(cut) >= d + 2:
            status = "COUNTEREXAMPLE"
            witness = sorted(F.edges())
            break
        rest = G.subgraph(set(range(n)) - set(cut))
        comps = list(nx.connected_components(rest))
        U = comps[0]
        W = set().union(*comps[1:])
        assert all(F.has_edge(u, w) for u in U for w in W)
        key = f"{min(len(U), len(W))}x{max(len(U), len(W))}"
        sizes[key] = sizes.get(key, 0) + 1
        s.add(z3.Or([z3.Not(e(u, w)) for u in U for w in W]))
        cuts += 1
        if cuts % 200 == 0:
            print(f"[{time.time()-t0:7.0f}s] {cuts} cuts, shapes {sizes}", flush=True)
    out = {"d": d, "n": n, "no_k2d": a.no_k2d, "edges_at_least": target, "status": status, "cuts_added": cuts,
           "cut_shapes": sizes, "seconds": round(time.time() - t0, 1), "witness_edges": witness}
    (HERE / "artifacts").mkdir(exist_ok=True)
    (HERE / "artifacts" / f"{'gate' if a.gate else 'search'}-d{d}{'-k2d' if a.no_k2d else ''}.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "witness_edges"}), flush=True)


if __name__ == "__main__":
    main()
