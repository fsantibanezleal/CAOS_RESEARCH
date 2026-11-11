"""EXP-011 steps 2 and 3: recheck every extremal graph independently and test the Bougard-Joret clique structure.

For each artifacts/extremal/<n>_<alpha>_<k>.g6 (from collect.py):
- independent recheck with networkx (no code shared with the C filter): edge count = c, independence number = alpha
  (maximum clique of the complement, networkx max_weight_clique with unit weights), vertex connectivity >= k
  (networkx node_connectivity);
- clique partition: an exact backtracking search for a proper alpha-colouring of the complement (each colour class
  is a clique of G); if one exists, the clique sizes, the edges inside cliques, the edges between cliques, and the
  minimum number of edges leaving one clique;
- comparison with the Bougard-Joret structure: sizes equal to the balanced Turan sizes, inside edges = t(n,alpha),
  between edges = ceil(k alpha/2).
Writes artifacts/structure.jsonl (one record per graph) and artifacts/structure-summary.md; exits 1 if a recheck fails.

Usage: python analyze.py
"""
import json
import sys
from collections import Counter
from math import ceil, comb
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent


def t(n, a):
    q, r = divmod(n, a)
    return r * comb(q + 1, 2) + (a - r) * comb(q, 2)


def balanced(n, a):
    q, r = divmod(n, a)
    return sorted([q + 1] * r + [q] * (a - r))


def colour_complement(G, a):
    """A partition of V(G) into at most a cliques of G (a proper a-colouring of the complement), or None."""
    H = nx.complement(G)
    order = sorted(H.nodes, key=lambda v: -H.degree(v))
    colour = {}

    def bt(i):
        if i == len(order):
            return True
        v = order[i]
        used = {colour[u] for u in H[v] if u in colour}
        top = max(colour.values(), default=-1)
        for c in range(min(a, top + 2)):      # symmetry: a new colour only as the next unused one
            if c not in used:
                colour[v] = c
                if bt(i + 1):
                    return True
                del colour[v]
        return False

    if not bt(0):
        return None
    parts = {}
    for v, c in colour.items():
        parts.setdefault(c, []).append(v)
    return list(parts.values())


def main():
    files = sorted((HERE / "artifacts" / "extremal").glob("*.g6"),
                   key=lambda p: tuple(int(x) for x in p.stem.split("_")))
    out, rows, bad = [], [], 0
    for f in files:
        n, a, k = (int(x) for x in f.stem.split("_"))
        c = t(n, a) + ceil(k * a / 2)
        graphs = [l for l in f.read_text(encoding="utf-8").split() if l]
        stats = Counter()
        for g6 in graphs:
            G = nx.from_graph6_bytes(g6.encode())
            m = G.number_of_edges()
            alpha = nx.max_weight_clique(nx.complement(G), weight=None)[1]
            kappa = nx.node_connectivity(G)
            ok = (m == c and alpha == a and kappa >= k and G.number_of_nodes() == n)
            bad += not ok
            stats["ok"] += ok
            parts = colour_complement(G, a)
            rec = {"n": n, "alpha": a, "k": k, "g6": g6, "edges": m, "alpha_nx": alpha, "kappa": kappa,
                   "recheck": ok, "clique_partition": parts is not None}
            if parts is not None:
                sizes = sorted(len(p) for p in parts)
                where = {v: i for i, p in enumerate(parts) for v in p}
                inside = sum(1 for u, v in G.edges if where[u] == where[v])
                out_edges = [sum(1 for u in p for v in G[u] if where[v] != where[u]) for p in parts]
                rec.update({"sizes": sizes, "inside": inside, "between": m - inside,
                            "min_out": min(out_edges), "balanced": sizes == balanced(n, a),
                            "bj_structure": sizes == balanced(n, a) and inside == t(n, a)
                            and m - inside == ceil(k * a / 2)})
                stats["partition"] += 1
                stats["bj"] += rec["bj_structure"]
            stats["graphs"] += 1
            stats[f"kappa={kappa}"] += 1
            out.append(rec)
        rows.append((n, a, k, c, stats))
        print(f"({n},{a},{k}) c={c}: {stats['graphs']} graphs, recheck ok {stats['ok']}, "
              f"clique partition {stats['partition']}, Bougard-Joret structure {stats['bj']}, "
              f"connectivity {sorted((x, y) for x, y in stats.items() if x.startswith('kappa'))}", flush=True)
    (HERE / "artifacts" / "structure.jsonl").write_text("\n".join(json.dumps(r) for r in out) + "\n",
                                                        encoding="utf-8")
    lines = ["| triple | c | extremal graphs | rechecked | clique partition | Bougard-Joret structure | connectivity |",
             "|---|---:|---:|---:|---:|---:|---|"]
    for n, a, k, c, s in rows:
        kap = ", ".join(f"{x.split('=')[1]}: {y}" for x, y in sorted(s.items()) if x.startswith("kappa"))
        lines.append(f"| ({n},{a},{k}) | {c} | {s['graphs']} | {s['ok']} | {s['partition']} | {s['bj']} | {kap} |")
    tot = sum(s["graphs"] for *_, s in rows)
    lines.append(f"\nGraphs: {tot}; independent recheck failures: {bad}; with a clique partition: "
                 f"{sum(s['partition'] for *_, s in rows)}; with the Bougard-Joret structure: "
                 f"{sum(s['bj'] for *_, s in rows)}.")
    (HERE / "artifacts" / "structure-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[-1:]))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
