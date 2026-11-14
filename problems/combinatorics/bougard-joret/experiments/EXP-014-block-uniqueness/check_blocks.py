"""EXP-014: which blocks (X, A) satisfy the necessary conditions C1 to C5 of hypothesis.md?

Every graph on 5, 6 and 7 vertices from NetworkX's graph atlas (one per isomorphism class) is tested against
C1 (order and size), C2 (connected, independence number 2, every edge critical) and C3 (clique cover number at least 3);
for each survivor every 3-subset A is tested against C4 (degrees) and C5 (every component of X - T meets A \\ T for
|T| <= 2). Independence and clique cover numbers are computed twice, by subset brute force and by a second method
(maximum clique of the complement; enumeration of set partitions). Survivors are grouped by isomorphism of the marked
graph (X, A) and compared with X6, X7 and the attaching triples observed in EXP-011 and used in EXP-013.

Writes artifacts/check-blocks.json and prints a summary (tee it into artifacts/run-output.txt).
Usage: python check_blocks.py
"""
import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx
from networkx.algorithms import isomorphism

HERE = Path(__file__).resolve().parent
SIZES = {5: 5, 6: 8, 7: 11}  # m -> e(X) = t(m+1, 2) - 1
OEIS_A000088 = {5: 34, 6: 156, 7: 1044}
OBSERVED = {"X6": (b"ETxO", [(0, 1, 5)]), "X7": (b"FQjRo", [(0, 1, 2), (1, 2, 3), (1, 2, 6)])}


def t(n, a):
    q, r = divmod(n, a)
    return r * (q + 1) * q // 2 + (a - r) * q * (q - 1) // 2


def alpha_brute(G):
    nodes = list(G)
    for size in range(len(nodes), 0, -1):
        for S in itertools.combinations(nodes, size):
            if all(not G.has_edge(u, v) for u, v in itertools.combinations(S, 2)):
                return size
    return 0


def alpha_clique(G):
    return nx.max_weight_clique(nx.complement(G), weight=None)[1]


def is_clique(G, S):
    return all(G.has_edge(u, v) for u, v in itertools.combinations(S, 2))


def theta_colouring(G):
    """Least k such that V(G) splits into k cliques: backtracking colouring of the complement."""
    nodes = list(G)
    for k in range(1, len(nodes) + 1):
        colour = {}

        def place(i):
            if i == len(nodes):
                return True
            v = nodes[i]
            used = set(colour.values())
            for c in range(k):
                if c > len(used):
                    break
                if all(G.has_edge(v, u) for u, cu in colour.items() if cu == c):
                    colour[v] = c
                    if place(i + 1):
                        return True
                    del colour[v]
            return False

        if place(0):
            return k
    return len(nodes)


def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part


def theta_partitions(G):
    return min(len(p) for p in set_partitions(list(G)) if all(is_clique(G, b) for b in p))


def every_edge_critical(G, a):
    for e in list(G.edges):
        H = G.copy()
        H.remove_edge(*e)
        if alpha_brute(H) <= a:
            return False
    return True


def c5_holds(X, A):
    nodes = list(X)
    for size in range(0, 3):
        for T in itertools.combinations(nodes, size):
            R = X.copy()
            R.remove_nodes_from(T)
            rest = set(A) - set(T)
            for comp in nx.connected_components(R):
                if not comp & rest:
                    return False
    return True


def marked(X, A):
    M = X.copy()
    nx.set_node_attributes(M, {v: v in A for v in M}, "a")
    return M


def same_marked(M1, M2):
    return nx.is_isomorphic(M1, M2, node_match=isomorphism.categorical_node_match("a", False))


def main():
    atlas = nx.graph_atlas_g()
    counts = Counter(G.number_of_nodes() for G in atlas)
    atlas_ok = all(counts[m] == OEIS_A000088[m] for m in SIZES)
    survivors, stage = [], Counter()
    method_disagreements = 0
    for idx, X in enumerate(atlas):
        m = X.number_of_nodes()
        if m not in SIZES:
            continue
        stage["graphs"] += 1
        if X.number_of_edges() != SIZES[m] or t(m + 1, 2) - 1 != SIZES[m]:
            continue
        stage["C1"] += 1
        if not nx.is_connected(X):
            continue
        a1, a2 = alpha_brute(X), alpha_clique(X)
        method_disagreements += a1 != a2
        if a1 != 2 or not every_edge_critical(X, 2):
            continue
        stage["C2"] += 1
        th1, th2 = theta_colouring(X), theta_partitions(X)
        method_disagreements += th1 != th2
        if th1 < 3:
            continue
        stage["C3"] += 1
        for A in itertools.combinations(sorted(X), 3):
            if any(X.degree(v) < 3 for v in X if v not in A) or any(X.degree(v) < 2 for v in A):
                continue
            stage["C4 pairs"] += 1
            if not c5_holds(X, A):
                continue
            stage["C5 pairs"] += 1
            survivors.append({"atlas_index": idx, "m": m, "edges": X.number_of_edges(), "A": list(A),
                              "g6": nx.to_graph6_bytes(X, header=False).decode().strip(), "theta": th1})
    # group survivors by isomorphism of the marked graph
    classes = []
    for s in survivors:
        X = nx.from_graph6_bytes(s["g6"].encode())
        M = marked(X, s["A"])
        for c in classes:
            if same_marked(c["rep"], M):
                c["members"].append(s)
                break
        else:
            classes.append({"rep": M, "members": [s]})
    # compare with the observed blocks and triples
    observed = []
    for name, (g6, triples) in OBSERVED.items():
        Xo = nx.from_graph6_bytes(g6)
        for A in triples:
            observed.append((name, A, marked(Xo, A)))
    report = []
    for c in classes:
        match = [f"{name} {list(A)}" for name, A, Mo in observed if same_marked(c["rep"], Mo)]
        s0 = c["members"][0]
        report.append({"m": s0["m"], "g6": s0["g6"], "A": s0["A"], "members": len(c["members"]),
                       "matches_observed": match})
    unmatched_observed = [f"{name} {list(A)}" for name, A, Mo in observed
                          if not any(same_marked(c["rep"], Mo) for c in classes)]
    out = {"atlas_counts": {m: counts[m] for m in SIZES}, "atlas_matches_A000088": atlas_ok,
           "stages": dict(stage), "method_disagreements": method_disagreements,
           "classes": report, "observed_not_found": unmatched_observed,
           "P1": not any(r["m"] == 5 for r in report),
           "P2_P3": all(r["matches_observed"] for r in report) and not unmatched_observed}
    (HERE / "artifacts").mkdir(exist_ok=True)
    (HERE / "artifacts" / "check-blocks.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"atlas counts {out['atlas_counts']} (A000088: {atlas_ok})")
    print(f"stages {dict(stage)}; method disagreements {method_disagreements}")
    for r in report:
        print(f"class m={r['m']} g6={r['g6']} A={r['A']} members={r['members']} observed={r['matches_observed']}")
    print(f"observed triples not found: {unmatched_observed}")
    print(f"P1 {out['P1']}  P2 and P3 {out['P2_P3']}")


if __name__ == "__main__":
    main()
