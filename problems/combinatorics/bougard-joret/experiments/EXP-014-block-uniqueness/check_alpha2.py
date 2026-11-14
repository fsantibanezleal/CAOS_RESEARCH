"""EXP-014 record for the alpha = 2 remark: f(7, 2, 3) and its extremal graphs without a partition into 2 cliques.

The characterisation of EXP-014 assumes alpha >= 3, as Proposition prop:where does. This script checks, over every
graph on 7 vertices (NetworkX graph atlas, 1,044 graphs, OEIS A000088), the least number of edges of a 3-connected
graph with independence number exactly 2, the conjectured value t(7, 2) + ceil(3 * 2 / 2) = 12, and which graphs at
the least size have no partition into 2 cliques (clique cover number 3, that is, a complement that is not
bipartite). Writes artifacts/alpha2.json and prints a summary.

Usage: python check_alpha2.py
"""
import json
from math import ceil, comb
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent


def t(n, a):
    q, r = divmod(n, a)
    return r * comb(q + 1, 2) + (a - r) * comb(q, 2)


def main():
    n, a, k = 7, 2, 3
    graphs = [G for G in nx.graph_atlas_g() if G.number_of_nodes() == n]
    qual = []
    for G in graphs:
        if nx.max_weight_clique(nx.complement(G), weight=None)[1] != a:
            continue
        if not nx.is_connected(G) or nx.node_connectivity(G) < k:
            continue
        qual.append(G)
    least = min(G.number_of_edges() for G in qual)
    at_least = [G for G in qual if G.number_of_edges() == least]
    rows = []
    for G in at_least:
        partition2 = nx.is_bipartite(nx.complement(G))
        rows.append({"g6": nx.to_graph6_bytes(G, header=False).decode().strip(), "edges": G.number_of_edges(),
                     "kappa": nx.node_connectivity(G), "partition_into_2_cliques": partition2})
    out = {"n": n, "alpha": a, "k": k, "atlas_graphs": len(graphs), "qualifying": len(qual),
           "least_edges": least, "conjectured": t(n, a) + ceil(k * a / 2), "graphs_at_least": rows}
    (HERE / "artifacts" / "alpha2.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"graphs on 7 vertices {len(graphs)}; 3-connected with alpha 2: {len(qual)}; least edges {least}; "
          f"conjectured {out['conjectured']}")
    for r in rows:
        print(f"  {r['g6']} edges {r['edges']} kappa {r['kappa']} partition into 2 cliques {r['partition_into_2_cliques']}")


if __name__ == "__main__":
    main()
