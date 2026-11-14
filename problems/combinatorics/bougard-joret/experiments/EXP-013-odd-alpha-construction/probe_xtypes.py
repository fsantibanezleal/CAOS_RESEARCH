"""Probe: the isomorphism types of the independence-two part X in the s = 1 extremal graphs, and how the edges between
parts attach (which vertices of X and of the cliques carry them)."""
import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import networkx as nx

recs = [json.loads(l) for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
types, attach = {}, Counter()
for r in recs:
    if r["s"] != 1:
        continue
    G = nx.convert_node_labels_to_integers(nx.from_graph6_bytes(r["g6"].encode()))
    n, a, q = G.number_of_nodes(), r["alpha"], r["p"]
    adj = [0] * n
    for u, v in G.edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    @lru_cache(maxsize=None)
    def mis(mask):
        if not mask:
            return 0
        v = (mask & -mask).bit_length() - 1
        rest = mask & ~(1 << v)
        return max(mis(rest), 1 + mis(rest & ~adj[v]))

    parts, found = [], []

    def bt(v, total):
        if v == n:
            if len(parts) == q:
                found.append(list(parts))
                return True
            return False
        if q - len(parts) > n - v:
            return False
        for i in range(len(parts)):
            old = parts[i]
            new = old | (1 << v)
            if total + mis(new) - mis(old) <= a:
                parts[i] = new
                if bt(v + 1, total + mis(new) - mis(old)):
                    return True
                parts[i] = old
        if len(parts) < q and total + 1 <= a:
            parts.append(1 << v)
            if bt(v + 1, total + 1):
                return True
            parts.pop()
        return False

    bt(0, 0)
    P = [[i for i in range(n) if m >> i & 1] for m in found[0]]
    X = next(p for p in P if G.subgraph(p).number_of_edges() < len(p) * (len(p) - 1) // 2)
    H = G.subgraph(X)
    key = None
    for k2, rep in types.items():
        if nx.is_isomorphic(H, rep):
            key = k2
    if key is None:
        key = f"X{len(X)}-{len(types)}"
        types[key] = nx.Graph(H)
    where = {v: i for i, p in enumerate(P) for v in p}
    xi = P.index(X)
    deg_out_X = sorted(sum(1 for w in G[v] if where[w] != xi) for v in X)
    deg_out_cliques = sorted(sum(1 for w in G[v] if where[w] != where[c]) for p in P if p is not X
                             for c in [p[0]] for v in p if True) if False else None
    quotient = nx.MultiGraph()
    quotient.add_nodes_from(range(len(P)))
    for u, v in G.edges:
        if where[u] != where[v]:
            quotient.add_edge(where[u], where[v])
    qdeg = sorted(dict(quotient.degree).values())
    attach[(key, (r["n"], a, r["k"]), tuple(deg_out_X), tuple(qdeg), quotient.degree(xi))] += 1
for k2, H in types.items():
    C = nx.complement(H)
    print(k2, "edges", H.number_of_edges(), "graph6", nx.to_graph6_bytes(H, header=False).decode().strip(),
          "| complement edges", C.number_of_edges(), "triangle-free", sum(nx.triangles(C).values()) == 0,
          "| complement maximal triangle-free (adding any edge makes a triangle):",
          all(len(set(C[u]) & set(C[v])) > 0 for u in C for v in C if u < v and not C.has_edge(u, v)),
          "| complement cycles?", sorted(len(c) for c in nx.cycle_basis(C)))
for k, c in sorted(attach.items()):
    print(k, c)
