"""EXP-011 second check of the clique-partition answers, by a method that shares no code with analyze.py.

V(G) splits into at most a cliques if and only if a maximal cliques of G cover V(G) (trim the overlaps). For every
graph in artifacts/structure.jsonl this script lists the maximal cliques (networkx find_cliques, Bron-Kerbosch) and
decides by an exhaustive search over a-subsets of them, with a bitmask union, whether a cover exists; the answer must
equal the clique_partition field. It also computes, for every graph, the clique cover number theta(G) (the least number
of maximal cliques covering V(G)), the clique number omega(G), the degree sequence and the size of the automorphism
group (networkx isomorphism matcher), and writes artifacts/verify.jsonl and artifacts/verify-summary.md.
Exits 1 on any disagreement with analyze.py.

Usage: python verify.py
"""
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

HERE = Path(__file__).resolve().parent


def cover_number(G, cap):
    """The least m <= cap such that m maximal cliques cover V(G), or None when no m <= cap works."""
    full = (1 << G.number_of_nodes()) - 1
    masks = sorted({sum(1 << v for v in c) for c in nx.find_cliques(G)}, key=lambda m: -bin(m).count("1"))
    for m in range(1, cap + 1):
        for combo in combinations(masks, m):
            u = 0
            for x in combo:
                u |= x
            if u == full:
                return m
    return None


def main():
    recs = [json.loads(l) for l in (HERE / "artifacts" / "structure.jsonl").read_text(encoding="utf-8").splitlines()]
    out, bad = [], 0
    per = defaultdict(Counter)
    for r in recs:
        G = nx.from_graph6_bytes(r["g6"].encode())
        a = r["alpha"]
        th = cover_number(G, a + 2)
        part = th is not None and th <= a
        bad += part != r["clique_partition"]
        aut = sum(1 for _ in GraphMatcher(G, G).isomorphisms_iter())
        omega = max(len(c) for c in nx.find_cliques(G))
        degs = sorted((d for _, d in G.degree), reverse=True)
        v = {"n": r["n"], "alpha": a, "k": r["k"], "g6": r["g6"], "theta": th, "partition_by_cover": part,
             "agrees": part == r["clique_partition"], "omega": omega, "aut": aut, "degrees": degs,
             "bj_structure": r.get("bj_structure", False)}
        out.append(v)
        key = (r["n"], a, r["k"])
        per[key]["graphs"] += 1
        per[key][f"theta={th}"] += 1
        per[key]["agree"] += v["agrees"]
    (HERE / "artifacts" / "verify.jsonl").write_text("\n".join(json.dumps(v) for v in out) + "\n", encoding="utf-8")
    lines = ["| triple | graphs | agree with analyze.py | clique cover number (value: count) |", "|---|---:|---:|---|"]
    for key in sorted(per):
        c = per[key]
        th = ", ".join(f"{x[6:]}: {y}" for x, y in sorted(c.items()) if x.startswith("theta="))
        lines.append(f"| ({key[0]},{key[1]},{key[2]}) | {c['graphs']} | {c['agree']} | {th} |")
    lines.append(f"\nGraphs: {len(out)}; disagreements with analyze.py: {bad}; theta(G) = alpha: "
                 f"{sum(1 for v in out if v['theta'] == v['alpha'])}; theta(G) = alpha + 1: "
                 f"{sum(1 for v in out if v['theta'] == v['alpha'] + 1)}; theta(G) > alpha + 1 or none within "
                 f"alpha + 2: {sum(1 for v in out if v['theta'] is None or v['theta'] > v['alpha'] + 1)}.")
    (HERE / "artifacts" / "verify-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
