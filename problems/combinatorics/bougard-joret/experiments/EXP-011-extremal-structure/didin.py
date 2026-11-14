"""EXP-011 step 4: Didin's core parameters on every extremal graph, and a test of his inequality.

Didin (Zenodo 10.5281/zenodo.22831382, preprint under review, read 2026-11-11): for a graph G with independence
number alpha, let p(G) be the largest number of connected components of an alpha-core (a spanning alpha-critical
subgraph with the same independence number) and s = alpha - p. His Theorem 3 states m >= t(n + s, alpha) - s.

Computation of p(G) [D]: alpha(G) <= sum of alpha(G[V_i]) for every partition V_1..V_q of V(G). If a partition
attains equality, the disjoint union of the G[V_i] is a spanning subgraph with independence number alpha(G), and an
alpha-core of it has at least q components; conversely the components of an alpha-core with p components partition
V(G) with equality. Hence p(G) is the largest q for which V(G) has a partition into q nonempty parts with
sum alpha(G[V_i]) <= alpha(G). The search below decides this exactly by backtracking (vertices assigned in order,
a new part only as the next index, a part's independence number computed exactly and memoized on bitmasks, the
branch cut as soon as the sum exceeds alpha(G)).

For each graph: p, s, Didin's bound t(n + s, alpha) - s and whether m reaches it; and whether s lies in the set the
inequality chain of Didin's Theorem 10 (case p >= 2: m >= t(n+s,alpha) - s + ceil(k p / 2); case p = 1:
m >= t(n+s,alpha) - s) allows at m = c. Writes artifacts/didin.jsonl and artifacts/didin-summary.md; exits 1 when a
graph violates the inequality or has an s outside the allowed set.

Usage: python didin.py [--selftest]
  --selftest  compare core_p with a brute force over all set partitions on 400 random graphs of orders 4 to 9
              (fixed seed) and exit 1 on any difference
"""
import json
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from math import ceil, comb
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent


def t(n, a):
    q, r = divmod(n, a)
    return r * comb(q + 1, 2) + (a - r) * comb(q, 2)


def allowed_s(n, a, k):
    c = t(n, a) + ceil(k * a / 2)
    out = {0}
    for s in range(1, a):
        p = a - s
        if t(n + s, a) - s + (ceil(k * p / 2) if p >= 2 else 0) <= c:
            out.add(s)
    return out


def core_p(G, alpha):
    n = G.number_of_nodes()
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

    def feasible(q):
        parts = []

        def bt(v, total):
            if v == n:
                return len(parts) == q
            if q - len(parts) > n - v:          # not enough vertices left to open the missing parts
                return False
            for i in range(len(parts)):
                old = parts[i]
                new = old | (1 << v)
                d = mis(new) - mis(old)
                if total + d <= alpha:
                    parts[i] = new
                    if bt(v + 1, total + d):
                        return True
                    parts[i] = old
            if len(parts) < q and total + 1 <= alpha:
                parts.append(1 << v)
                if bt(v + 1, total + 1):
                    return True
                parts.pop()
            return False

        return bt(0, 0)

    for q in range(alpha, 0, -1):
        if feasible(q):
            return q
    raise AssertionError("q = 1 is always feasible")


def brute_p(G, alpha):
    nodes = list(G.nodes)
    best = 0

    cache = {}

    def a_of(part):
        key = frozenset(part)
        if key not in cache:
            cache[key] = nx.max_weight_clique(nx.complement(G.subgraph(part)), weight=None)[1]
        return cache[key]

    def rec(i, parts):
        nonlocal best
        if i == len(nodes):
            if sum(a_of(p) for p in parts) <= alpha:
                best = max(best, len(parts))
            return
        for p in parts:
            p.append(nodes[i])
            rec(i + 1, parts)
            p.pop()
        parts.append([nodes[i]])
        rec(i + 1, parts)
        parts.pop()

    rec(0, [])
    return best


def selftest():
    import random
    rng = random.Random(20261111)
    diff = 0
    for _ in range(400):
        n = rng.randint(4, 9)
        G = nx.gnp_random_graph(n, rng.choice([0.3, 0.5, 0.7]), seed=rng.randrange(1 << 30))
        a = nx.max_weight_clique(nx.complement(G), weight=None)[1]
        x, y = core_p(G, a), brute_p(G, a)
        diff += x != y
    print(f"selftest: 400 graphs, {diff} differences between core_p and the brute force")
    return 1 if diff else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    recs = [json.loads(l) for l in (HERE / "artifacts" / "structure.jsonl").read_text(encoding="utf-8").splitlines()]
    out, bad = [], 0
    per = defaultdict(Counter)
    for r in recs:
        G = nx.convert_node_labels_to_integers(nx.from_graph6_bytes(r["g6"].encode()))
        n, a, k = r["n"], r["alpha"], r["k"]
        m = G.number_of_edges()
        p = core_p(G, a)
        s = a - p
        bound = t(n + s, a) - s
        ok_ineq = m >= bound
        ok_allowed = s in allowed_s(n, a, k)
        consistent = (s == 0) == r["clique_partition"]
        bad += (not ok_ineq) + (not ok_allowed) + (not consistent)
        out.append({"n": n, "alpha": a, "k": k, "g6": r["g6"], "edges": m, "p": p, "s": s, "didin_bound": bound,
                    "inequality_holds": ok_ineq, "s_allowed": ok_allowed, "s0_iff_partition": consistent})
        key = (n, a, k)
        per[key]["graphs"] += 1
        per[key][f"s={s}"] += 1
        per[key]["tight"] += m == bound
    (HERE / "artifacts" / "didin.jsonl").write_text("\n".join(json.dumps(x) for x in out) + "\n", encoding="utf-8")
    lines = ["| triple | graphs | s values (value: count) | allowed s at c | graphs tight in Didin's inequality |",
             "|---|---:|---|---|---:|"]
    for key in sorted(per):
        d = per[key]
        sv = ", ".join(f"{x[2:]}: {y}" for x, y in sorted(d.items()) if x.startswith("s="))
        al = ", ".join(str(x) for x in sorted(allowed_s(*key)))
        lines.append(f"| ({key[0]},{key[1]},{key[2]}) | {d['graphs']} | {sv} | {al} | {d['tight']} |")
    lines.append(f"\nGraphs: {len(out)}; violations (inequality, allowed s, s = 0 against the clique partition): {bad}.")
    (HERE / "artifacts" / "didin-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
