"""EXP-005: is there a k-connected graph of order n, independence number alpha and at most E edges?

Exact SAT search (z3) on n labelled vertices:
- at most E edges (pseudo-Boolean);
- no independent set of size alpha+1: one clause per (alpha+1)-set;
- vertices 0..alpha-1 independent (an alpha-set exists; by symmetry it can be fixed);
- minimum degree >= k;
- k-connectivity by lazy cuts: every model is checked by exact vertex connectivity (networkx); for a vertex cut S
  with |S| < k the components of G - S are split into nonempty U, W and the clause "some U-W pair is an edge"
  is added. A model with connectivity >= k is a witness.

Prints and appends one JSON line to artifacts/results.jsonl: status SAT (with the witness edges, re-verified
independently by networkx: order, edges, independence number, connectivity) or UNSAT or UNKNOWN (timeout).

Usage: python run.py <n> <alpha> <k> <E> [--timeout S] [--max-cuts N] [--eager M]
"""
import argparse
import itertools
import json
import time
from pathlib import Path

import networkx as nx
import z3

HERE = Path(__file__).resolve().parent


def independence_number(G):
    return max(len(c) for c in nx.find_cliques(nx.complement(G)))


def main():
    ap = argparse.ArgumentParser()
    for name in ("n", "alpha", "k", "E"):
        ap.add_argument(name, type=int)
    ap.add_argument("--timeout", type=int, default=3600)
    ap.add_argument("--max-cuts", type=int, default=100000)
    ap.add_argument("--eager", type=int, default=3, help="largest |U| of the eager neighbourhood cuts")
    a = ap.parse_args()
    n, alpha, k, E = a.n, a.alpha, a.k, a.E
    X = {(i, j): z3.Bool(f"e_{i}_{j}") for i, j in itertools.combinations(range(n), 2)}

    def e(i, j):
        return X[(min(i, j), max(i, j))]

    s = z3.Solver()
    s.add(z3.PbLe([(x, 1) for x in X.values()], E))
    for S in itertools.combinations(range(n), alpha + 1):
        s.add(z3.Or([e(i, j) for i, j in itertools.combinations(S, 2)]))
    for i, j in itertools.combinations(range(alpha), 2):
        s.add(z3.Not(e(i, j)))
    for v in range(n):
        s.add(z3.PbGe([(e(v, u), 1) for u in range(n) if u != v], k))
    # Eager neighbourhood cuts: in a k-connected graph every set U with |U| + k <= n - 1 has at least k
    # neighbours outside U (otherwise N(U) separates U from the rest). Sizes 2..a.eager.
    for size in range(2, a.eager + 1):
        if size + k > n - 1:
            break
        for U in itertools.combinations(range(n), size):
            ys = []
            for w in range(n):
                if w in U:
                    continue
                y = z3.Bool(f"n_{'_'.join(map(str, U))}_{w}")
                s.add(y == z3.Or([e(u, w) for u in U]))
                ys.append((y, 1))
            s.add(z3.PbGe(ys, k))
    t0 = time.time()
    cuts = 0
    rec = {"n": n, "alpha": alpha, "k": k, "E": E, "eager": a.eager}
    while True:
        left = a.timeout - (time.time() - t0)
        if left <= 0 or cuts >= a.max_cuts:
            rec["status"] = "UNKNOWN"
            break
        s.set("timeout", int(left * 1000))
        r = s.check()
        if r == z3.unsat:
            rec["status"] = "UNSAT"
            break
        if r != z3.sat:
            rec["status"] = "UNKNOWN"
            break
        m = s.model()
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(key for key, x in X.items() if z3.is_true(m.eval(x)))
        if not nx.is_connected(G):
            cut = set()
        elif nx.node_connectivity(G) >= k:
            cut = None
        else:
            cut = nx.minimum_node_cut(G)
        if cut is None:
            rec["status"] = "SAT"
            rec["edges"] = sorted(G.edges())
            rec["check"] = {"order": G.number_of_nodes(), "edges": G.number_of_edges(),
                            "alpha": independence_number(G), "connectivity": nx.node_connectivity(G)}
            break
        comps = list(nx.connected_components(G.subgraph(set(range(n)) - set(cut))))
        U, W = comps[0], set().union(*comps[1:])
        s.add(z3.Or([e(u, w) for u in U for w in W]))
        cuts += 1
    rec["cuts"] = cuts
    rec["seconds"] = round(time.time() - t0, 1)
    (HERE / "artifacts").mkdir(exist_ok=True)
    with open(HERE / "artifacts" / "results.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps({key: v for key, v in rec.items() if key != "edges"}), flush=True)


if __name__ == "__main__":
    main()
