"""Probe: which vertices of X6 / X7 carry the three outgoing edges, up to automorphisms of X, in every s = 1 graph."""
import json
import sys
from collections import Counter
from pathlib import Path

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

X6 = nx.from_graph6_bytes(b"ETxO")
X7 = nx.from_graph6_bytes(b"FQjRo")
recs = [json.loads(l) for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
seen = Counter()
for r in recs:
    if r["s"] != 1:
        continue
    G = nx.convert_node_labels_to_integers(nx.from_graph6_bytes(r["g6"].encode()))
    for X in (X6, X7):
        gm = GraphMatcher(G, X)
        for m in gm.subgraph_isomorphisms_iter():      # induced copies of X in G (map G-node -> X-node)
            Vx = set(m)
            out = {m[v] for v in Vx if any(w not in Vx for w in G[v])}
            outcount = sum(1 for v in Vx for w in G[v] if w not in Vx)
            if outcount == 3:
                # canonical up to Aut(X): smallest sorted image
                best = min(tuple(sorted(phi[x] for x in out)) for phi in GraphMatcher(X, X).isomorphisms_iter())
                seen[(X.number_of_nodes(), best, tuple(sorted(d for _, d in X.degree)))] += 1
                break
        else:
            continue
        break
for k, c in sorted(seen.items()):
    print("X%d attaching vertices (canonical) %s | X degrees %s | graphs %d" % (k[0], k[1], k[2], c))
print("X6 degrees by vertex:", dict(X6.degree), "edges:", sorted(X6.edges))
print("X7 degrees by vertex:", dict(X7.degree), "edges:", sorted(X7.edges))
