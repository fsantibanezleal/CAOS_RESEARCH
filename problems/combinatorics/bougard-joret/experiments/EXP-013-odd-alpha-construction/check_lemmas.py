"""EXP-013: exact check of every finite fact about X6 and X7 that the proof in proof.md uses.

For X in {X6, X7} and each recorded attaching triple A of X:
  F1  alpha(X) = 2 and theta(X) = 3 (clique cover number: least number of cliques partitioning V(X));
  F2  the vertices of X outside A contain a pair of non-adjacent vertices;
  F3  for every nonempty S contained in A: theta(X - S) + |S|/2 >= 5/2;
  F4  e(X) = e(K3 + K3) + 2 for X6 and e(K3 + K4) + 2 for X7;
  F5  for every set T of at most two vertices of X, every component of X - T contains a vertex of A - T;
  F6  X is 2-connected.
Prints one line per fact and exits 1 if any fails.

Usage: python check_lemmas.py
"""
import sys
from itertools import combinations

import networkx as nx

X6 = nx.from_graph6_bytes(b"ETxO")
X7 = nx.from_graph6_bytes(b"FQjRo")
CASES = [("X6", X6, [(0, 1, 5)], 3 + 3), ("X7", X7, [(0, 1, 2), (1, 2, 3), (1, 2, 6)], 3 + 6)]


def alpha(H):
    return nx.max_weight_clique(nx.complement(H), weight=None)[1] if H.number_of_nodes() else 0


def theta(H):
    """Least number of cliques partitioning V(H) (chromatic number of the complement), by exhaustive search."""
    nodes = list(H.nodes)
    if not nodes:
        return 0
    for q in range(1, len(nodes) + 1):
        for labels in __import__("itertools").product(range(q), repeat=len(nodes)):
            if labels[0] != 0:
                continue
            ok = all(H.has_edge(u, v) for (u, lu), (v, lv) in combinations(zip(nodes, labels), 2) if lu == lv)
            if ok and len(set(labels)) == q:
                return q
    return len(nodes)


def main():
    bad = 0
    for name, X, triples, base in CASES:
        f1 = alpha(X) == 2 and theta(X) == 3
        f4 = X.number_of_edges() == base + 2
        f6 = nx.node_connectivity(X) >= 2
        print(f"{name}: F1 alpha={alpha(X)} theta={theta(X)} {'ok' if f1 else 'FAIL'}; "
              f"F4 edges={X.number_of_edges()} vs {base}+2 {'ok' if f4 else 'FAIL'}; "
              f"F6 connectivity={nx.node_connectivity(X)} {'ok' if f6 else 'FAIL'}")
        bad += (not f1) + (not f4) + (not f6)
        for A in triples:
            rest = [v for v in X if v not in A]
            pair = next(((u, v) for u, v in combinations(rest, 2) if not X.has_edge(u, v)), None)
            f2 = pair is not None
            worst = min(theta(X.subgraph([v for v in X if v not in S])) + len(S) / 2
                        for r in (1, 2, 3) for S in combinations(A, r))
            f3 = worst >= 2.5
            f5 = all(all(set(comp) - set(T) & set(A) - set(T) for comp in
                         nx.connected_components(X.subgraph([v for v in X if v not in T])))
                     for r in (0, 1, 2) for T in combinations(list(X), r))
            print(f"  triple {A}: F2 unattached independent pair {pair} {'ok' if f2 else 'FAIL'}; "
                  f"F3 min theta(X-S)+|S|/2 = {worst} {'ok' if f3 else 'FAIL'}; "
                  f"F5 {'ok' if f5 else 'FAIL'}")
            bad += (not f2) + (not f3) + (not f5)
    print(f"failures: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
