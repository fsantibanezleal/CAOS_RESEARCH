"""EXP-003: gadget invariants of every (MNH graph X, vertex x) from the EXP-001 census, and the triple search.

A gadget is (X, x) with G = X - x connected, not complete, and N = N_X(x) != V(G). For each gadget, computed by
subset dynamic programming AND independently by backtracking (they must agree):
  traceable, homogeneously traceable (every vertex starts a Hamilton path of G), the universal vertices of G[N]
  and whether G is traceable from each, d = |G| - (order of a longest (p, q)-path of G with p != q in N), and
  whether some longest (p, q)-path omits a set that is not a clique.
Triple search (hypothesis.md): a middle gadget with a non-clique omitted set and two end gadgets with d at least
the middle's, all traceable, at least two homogeneously traceable, at most one with a universal vertex in G[N],
and every gadget traceable from every universal vertex of its G[N]. Writes artifacts/gadgets.json and
artifacts/triples.json.

Usage: python gadgets.py <census artifacts dir> <max order> [suffix]   (outputs gadgets<suffix>.json, triples<suffix>.json)
"""
import json
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def decode(g6):
    data = [ord(c) - 63 for c in g6]
    n = data[0]
    bits = [(x >> (5 - i)) & 1 for x in data[1:] for i in range(6)]
    adj = [set() for _ in range(n)]
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i].add(j)
                adj[j].add(i)
            k += 1
    return n, adj


def is_clique(adj, S):
    return all(b in adj[a] for a, b in combinations(S, 2))


def connected(adj, V):
    V = set(V)
    if not V:
        return True
    seen, stack = set(), [next(iter(V))]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(w for w in adj[v] if w in V and w not in seen)
    return seen == V


# --- method 1: subset dynamic programming --------------------------------------------------------------
def dp_invariants(m, adj, N):
    full = (1 << m) - 1
    P = {}
    for v in range(m):
        P[(1 << v, v)] = 1 << v
    for S in range(1, full + 1):
        for v in range(m):
            st = P.get((S, v), 0)
            if not st:
                continue
            for w in adj[v]:
                if not (S >> w) & 1:
                    key = (S | (1 << w), w)
                    P[key] = P.get(key, 0) | st
    starts = 0
    for v in range(m):
        starts |= P.get((full, v), 0)
    traceable = starts != 0
    homog = starts == full
    Nmask = sum(1 << v for v in N)
    best, omitted = 0, []
    for (S, v), st in P.items():
        if (Nmask >> v) & 1 and st & Nmask & ~(1 << v):
            size = bin(S).count("1")
            if size > best:
                best, omitted = size, [S]
            elif size == best:
                omitted.append(S)
    nonclique = any(not is_clique(adj, [u for u in range(m) if not (S >> u) & 1]) for S in omitted)
    return traceable, homog, starts, m - best, nonclique


# --- method 2: backtracking ------------------------------------------------------------------------------
def bt_invariants(m, adj, N):
    def longest_from(start, allowed_end):
        best = [0, []]

        def dfs(v, seen):
            if v in allowed_end and v != start:
                if len(seen) > best[0]:
                    best[0], best[1] = len(seen), [frozenset(seen)]
                elif len(seen) == best[0]:
                    best[1].append(frozenset(seen))
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    dfs(w, seen)
                    seen.remove(w)

        dfs(start, {start})
        return best

    def ham_from(s):
        def dfs(v, seen):
            if len(seen) == m:
                return True
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    if dfs(w, seen):
                        return True
                    seen.remove(w)
            return False
        return dfs(s, {s})

    starts = {s for s in range(m) if ham_from(s)}
    best, sets = 0, []
    for p in N:
        b, ss = longest_from(p, set(N))
        if b > best:
            best, sets = b, ss
        elif b == best:
            sets += ss
    nonclique = any(not is_clique(adj, [u for u in range(m) if u not in S]) for S in sets)
    smask = sum(1 << s for s in starts)
    return bool(starts), len(starts) == m, smask, m - best, nonclique


def main():
    art, maxn = Path(sys.argv[1]), int(sys.argv[2])
    suffix = sys.argv[3] if len(sys.argv) > 3 else ""
    gadgets, disagreements = [], 0
    for n in range(4, maxn + 1):
        for line in (art / f"mnh-n{n}.txt").read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            g6 = line.split()[0]
            _, adjX = decode(g6)
            for x in range(n):
                rest = [v for v in range(n) if v != x]
                idx = {v: i for i, v in enumerate(rest)}
                m = n - 1
                adj = [set(idx[w] for w in adjX[v] if w != x) for v in rest]
                N = sorted(idx[w] for w in adjX[x])
                if not connected(adj, range(m)) or is_clique(adj, range(m)) or len(N) == m or len(N) < 2:
                    continue
                a = dp_invariants(m, adj, N)
                b = bt_invariants(m, adj, N)
                if a != b:
                    disagreements += 1
                traceable, homog, starts, d, nonclique = a
                univ = [u for u in N if all(w in adj[u] for w in N if w != u)]
                gadgets.append({"g6": g6, "n": n, "x": x, "m": m, "traceable": traceable, "homog": homog,
                                "univ": univ, "trace_from_univ": all((starts >> u) & 1 for u in univ),
                                "d": d, "nonclique_omit": nonclique})
    (HERE / "artifacts").mkdir(exist_ok=True)
    (HERE / "artifacts" / f"gadgets{suffix}.json").write_text(json.dumps(gadgets, indent=1) + "\n", encoding="utf-8")
    ok = [g for g in gadgets if g["traceable"] and g["trace_from_univ"]]
    mids = [g for g in ok if g["nonclique_omit"]]
    best = None
    for mid in mids:
        for e1 in ok:
            for e2 in ok:
                trio = (mid, e1, e2)
                if e1["d"] < mid["d"] or e2["d"] < mid["d"]:
                    continue
                if sum(bool(g["univ"]) for g in trio) > 1 or sum(g["homog"] for g in trio) < 2:
                    continue
                order = 3 + sum(g["m"] for g in trio)
                if best is None or order < best[0]:
                    best = (order, trio)
    summary = {"gadgets": len(gadgets), "dp_backtracking_disagreements": disagreements,
               "traceable_ok": len(ok), "middle_candidates": len(mids),
               "d_histogram": {str(k): sum(g["d"] == k for g in gadgets) for k in sorted({g["d"] for g in gadgets})},
               "best_triple": None if best is None else {"order": best[0], "gadgets": best[1]}}
    (HERE / "artifacts" / f"triples{suffix}.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "best_triple"}),
          "best order:", None if best is None else best[0])


if __name__ == "__main__":
    main()
