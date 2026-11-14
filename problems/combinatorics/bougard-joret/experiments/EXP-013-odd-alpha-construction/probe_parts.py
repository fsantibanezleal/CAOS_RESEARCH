"""Probe: for every extremal graph with s >= 1 (EXP-011 didin.jsonl), one partition attaining p(G) found by
backtracking (vertices in order, parts opened in order, exact part independence numbers on masks), and a description of
each part: clique, or order / edges / independence number / complement structure."""
import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import networkx as nx

recs = [json.loads(l) for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
summary, examples = Counter(), {}
for r in recs:
    if r["s"] == 0:
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

    assert bt(0, 0)
    desc = []
    inside = 0
    for m in found[0]:
        vs = [i for i in range(n) if m >> i & 1]
        H = G.subgraph(vs)
        inside += H.number_of_edges()
        if H.number_of_edges() == len(vs) * (len(vs) - 1) // 2:
            desc.append(f"K{len(vs)}")
        else:
            C = nx.complement(H)
            degs = sorted(d for _, d in C.degree)
            cyc = sorted(len(c) for c in nx.connected_components(C)) if all(d == 2 for d in degs) else None
            desc.append(f"X[n{len(vs)},e{H.number_of_edges()},a{mis(m)},compl:{'cycles' + str(cyc) if cyc else 'degs' + str(degs)}]")
    key = ((r["n"], a, r["k"]), r["s"], " + ".join(sorted(desc)), G.number_of_edges() - inside)
    summary[key] += 1
    examples.setdefault(key, r["g6"])
for (t, s, d, b), c in sorted(summary.items()):
    print(t, "s=%d" % s, "|", d, "| edges between parts:", b, "| graphs:", c, "| e.g.", examples[(t, s, d, b)])
