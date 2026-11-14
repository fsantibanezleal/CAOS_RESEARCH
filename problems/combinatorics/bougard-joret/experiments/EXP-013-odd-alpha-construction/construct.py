"""EXP-013: explicit extremal candidates without a clique partition for odd alpha, k = 3 (see hypothesis.md).

For each (n, alpha): balanced clique orders of T(n, alpha); two K3 replaced by X6, or a K3 and a K4 by X7; the alpha - 1
parts joined along a cubic multigraph (circular ladder, Moebius ladder, then random loopless cubic multigraphs), each
clique using three distinct vertices and X its recorded attaching triple. Every candidate is checked exactly with
NetworkX: edge count c = t(n, alpha) + ceil(3 alpha / 2), independence number alpha, vertex connectivity >= 3, and
clique cover number alpha + 1 by two methods (the alpha-colouring backtracking of EXP-011 analyze.py and the
maximal-clique cover of EXP-011 verify.py). Writes artifacts/construct.jsonl (one record per (n, alpha): the first
passing graph in graph6, its parts and quotient, or the number of candidates tried) and prints a summary.

Usage: python construct.py [--alphas 3,5,7,9] [--tries 2000] [--seed 20261114]
"""
import argparse
import json
import random
import sys
import time
from math import ceil, comb
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "EXP-011-extremal-structure"))
from analyze import colour_complement  # noqa: E402
from verify import cover_number  # noqa: E402

X6 = nx.from_graph6_bytes(b"ETxO")
X7 = nx.from_graph6_bytes(b"FQjRo")
X6_TRIPLES = [(0, 1, 5)]
X7_TRIPLES = [(0, 1, 2), (1, 2, 3), (1, 2, 6)]


def t(n, a):
    q, r = divmod(n, a)
    return r * comb(q + 1, 2) + (a - r) * comb(q, 2)


def parts_plan(n, a):
    q, r = divmod(n, a)
    sizes = [q + 1] * r + [q] * (a - r)
    if sizes.count(3) >= 2:
        sizes.remove(3)
        sizes.remove(3)
        return sorted(sizes), "X6"
    if 3 in sizes and 4 in sizes:
        sizes.remove(3)
        sizes.remove(4)
        return sorted(sizes), "X7"
    return None, None


def cubic_multigraphs(m, rng, tries):
    """Loopless cubic multigraphs on m vertices: circular ladder, Moebius ladder, then random configurations."""
    out = []
    if m == 2:
        out.append([(0, 1)] * 3)
    if m >= 4 and m % 2 == 0:
        h = m // 2
        out.append([(i, (i + 1) % h) for i in range(h)] + [(h + i, h + (i + 1) % h) for i in range(h)]
                   + [(i, h + i) for i in range(h)])
        out.append([(i, (i + 1) % m) for i in range(m)] + [(i, i + h) for i in range(h)])
    while len(out) < tries:
        stubs = [v for v in range(m) for _ in range(3)]
        rng.shuffle(stubs)
        es = [(stubs[2 * i], stubs[2 * i + 1]) for i in range(len(stubs) // 2)]
        if all(u != v for u, v in es):
            out.append(es)
    return out


def build(n, a, rng, quot, xtype, sizes):
    G = nx.Graph()
    parts, start = [], 0
    X = X6 if xtype == "X6" else X7
    triples = X6_TRIPLES if xtype == "X6" else X7_TRIPLES
    xpos = rng.randrange(a - 1)
    k_sizes = list(sizes)
    rng.shuffle(k_sizes)
    attach = []
    for i in range(a - 1):
        if i == xpos:
            vs = list(range(start, start + X.number_of_nodes()))
            G.add_nodes_from(vs)
            G.add_edges_from((vs[u], vs[v]) for u, v in X.edges)
            tri = list(rng.choice(triples))
            rng.shuffle(tri)
            attach.append([vs[x] for x in tri])
        else:
            s = k_sizes.pop()
            vs = list(range(start, start + s))
            G.add_nodes_from(vs)
            G.add_edges_from((u, v) for j, u in enumerate(vs) for v in vs[j + 1:])
            attach.append(rng.sample(vs, 3))
        parts.append(vs)
        start += len(vs)
    used = [0] * (a - 1)
    for u, v in quot:
        x, y = attach[u][used[u]], attach[v][used[v]]
        used[u] += 1
        used[v] += 1
        if G.has_edge(x, y):
            return None, None
        G.add_edge(x, y)
    assert G.number_of_nodes() == n
    return G, parts


def check(G, a):
    alpha = nx.max_weight_clique(nx.complement(G), weight=None)[1]
    if alpha != a:
        return False, {"alpha": alpha}
    kappa = nx.node_connectivity(G)
    if kappa < 3:
        return False, {"alpha": alpha, "kappa": kappa}
    col = colour_complement(G, a)
    th = cover_number(G, a + 1)
    return col is None and th == a + 1, {"alpha": alpha, "kappa": kappa, "colouring_partition": col is not None,
                                         "theta": th}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alphas", default="3,5,7,9")
    ap.add_argument("--tries", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261114)
    a_ = ap.parse_args()
    out = (HERE / "artifacts")
    out.mkdir(exist_ok=True)
    recs = []
    for a in (int(x) for x in a_.alphas.split(",")):
        for n in range(3 * a + 1, 4 * a + 1):
            rng = random.Random(a_.seed + 1000 * a + n)
            c = t(n, a) + ceil(3 * a / 2)
            sizes, xtype = parts_plan(n, a)
            t0 = time.time()
            rec = {"n": n, "alpha": a, "k": 3, "c": c, "shape": xtype, "found": False, "tried": 0}
            if sizes is not None:
                for quot in cubic_multigraphs(a - 1, rng, a_.tries):
                    rec["tried"] += 1
                    G, parts = build(n, a, rng, quot, xtype, sizes)
                    if G is None or G.number_of_edges() != c:
                        continue
                    ok, info = check(G, a)
                    if ok:
                        rec.update(found=True, g6=nx.to_graph6_bytes(G, header=False).decode().strip(),
                                   parts=[len(p) for p in parts], quotient=quot, **info)
                        break
            rec["seconds"] = round(time.time() - t0, 1)
            recs.append(rec)
            print(json.dumps({k: v for k, v in rec.items() if k not in ("g6", "quotient")}), flush=True)
    (out / "construct.jsonl").write_text("\n".join(json.dumps(r) for r in recs) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
