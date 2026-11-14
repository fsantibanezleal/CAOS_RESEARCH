"""EXP-013 record: the construction with a quotient that is not 3-edge-connected.

At alpha = 5 the circular ladder on four parts (two double edges joined by two single edges) is the first quotient
construct.py tries. It has a 2-edge cut. For every order n = 16..19 this script builds the graph with that quotient
and --trials random attachments (random position of X, random clique order, random attaching triple and vertices),
checks each exactly with NetworkX (edges, independence number, vertex connectivity, a minimum vertex cut), and records
the quotient's edge connectivity. Writes artifacts/ladder.jsonl (one line per trial) and prints a summary.

Usage: python probe_ladder.py [--trials 20] [--seed 20261114]
"""
import argparse
import json
import random
from collections import Counter
from math import ceil
from pathlib import Path

import networkx as nx

from construct import build, parts_plan, t

HERE = Path(__file__).resolve().parent
LADDER4 = [(0, 1), (1, 0), (2, 3), (3, 2), (0, 2), (1, 3)]


def quotient_edge_connectivity(edges, m):
    Q = nx.MultiGraph()
    Q.add_nodes_from(range(m))
    Q.add_edges_from(edges)
    H = nx.Graph()
    for u, v in Q.edges():
        w = H[u][v]["capacity"] + 1 if H.has_edge(u, v) else 1
        H.add_edge(u, v, capacity=w)
    return min(nx.minimum_cut(H, 0, v)[0] for v in range(1, m))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20261114)
    args = ap.parse_args()
    a = 5
    lam = quotient_edge_connectivity(LADDER4, a - 1)
    out = HERE / "artifacts" / "ladder.jsonl"
    recs = []
    for n in range(3 * a + 1, 4 * a):
        sizes, xtype = parts_plan(n, a)
        c = t(n, a) + ceil(3 * a / 2)
        rng = random.Random(args.seed + 7 * n)
        done = 0
        while done < args.trials:
            G, parts = build(n, a, rng, LADDER4, xtype, sizes)
            if G is None:
                continue
            alpha = nx.max_weight_clique(nx.complement(G), weight=None)[1]
            kappa = nx.node_connectivity(G)
            cut = sorted(nx.minimum_node_cut(G))
            recs.append({"n": n, "alpha": a, "shape": xtype, "trial": done, "edges": G.number_of_edges(), "c": c,
                         "independence": alpha, "kappa": kappa, "min_vertex_cut": cut,
                         "quotient": LADDER4, "quotient_edge_connectivity": lam,
                         "g6": nx.to_graph6_bytes(G, header=False).decode().strip()})
            done += 1
    out.write_text("".join(json.dumps(r) + "\n" for r in recs), encoding="utf-8")
    print(f"quotient: circular ladder on 4 parts, edge connectivity {lam}")
    for n in range(3 * a + 1, 4 * a):
        rs = [r for r in recs if r["n"] == n]
        print(f"n={n} trials={len(rs)} edges=c {sum(r['edges'] == r['c'] for r in rs)} "
              f"independence=5 {sum(r['independence'] == a for r in rs)} kappa {dict(Counter(r['kappa'] for r in rs))}")
    print(f"total {len(recs)} graphs, kappa >= 3 in {sum(r['kappa'] >= 3 for r in recs)}")


if __name__ == "__main__":
    main()
