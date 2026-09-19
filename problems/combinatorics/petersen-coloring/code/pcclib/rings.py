"""Alternating rings of 4-poles, and a fast search for small cycle-separating edge cuts.

`ring_of_poles` places copies of 4-poles around a cycle: the second connector of each block is
joined by two edges to the first connector of the next block (first end to first end).
`cyclic_cuts_below_4` finds every edge cut with at most three edges whose removal leaves two
components that both contain a cycle, by computing, for every pair of edges, the bridges of the
graph without that pair (plus the 1- and 2-edge cuts found on the way).
"""

from __future__ import annotations

import itertools

from .graphs import Graph
from .poles import Pole


def ring_of_poles(blocks: list[tuple[Pole, tuple[tuple[int, int], tuple[int, int]]]]) -> tuple[Graph, list[list[int]]]:
    """blocks: list of (pole, ((p, q), (r, s))) with connector 1 = dangling ends p, q and
    connector 2 = r, s. Returns the cubic graph and, per block, its vertex ids."""
    edges = []
    offset = 0
    vid = []
    for pl, _ in blocks:
        local = {v: offset + i for i, v in enumerate(pl.kept)}
        vid.append(local)
        for i in pl.internal:
            u, v = pl.parent.edges[i]
            edges.append((local[u], local[v]))
        offset += len(pl.kept)
    m = len(blocks)
    for b in range(m):
        pl, (_, (r, s)) = blocks[b]
        nxt, ((p, q), _) = blocks[(b + 1) % m]
        a1 = vid[b][pl.dangling[r][0]]
        a2 = vid[b][pl.dangling[s][0]]
        b1 = vid[(b + 1) % m][nxt.dangling[p][0]]
        b2 = vid[(b + 1) % m][nxt.dangling[q][0]]
        edges += [(a1, b1), (a2, b2)]
    g = Graph.from_edges(edges)
    return g, [sorted(d.values()) for d in vid]


def _bridges(n: int, adj: list[list[tuple[int, int]]], removed: set[int]) -> tuple[int, list[int]]:
    """Number of connected components and the bridges of the graph without `removed` edges."""
    disc = [-1] * n
    low = [0] * n
    bridges = []
    comps = 0
    t = 0
    for root in range(n):
        if disc[root] >= 0:
            continue
        comps += 1
        disc[root] = low[root] = t
        t += 1
        stack = [(root, -1, iter(adj[root]))]
        while stack:
            v, pe, it = stack[-1]
            advanced = False
            for w, ei in it:
                if ei in removed or ei == pe:
                    continue
                if disc[w] < 0:
                    disc[w] = low[w] = t
                    t += 1
                    stack.append((w, ei, iter(adj[w])))
                    advanced = True
                    break
                low[v] = min(low[v], disc[w])
            if not advanced:
                stack.pop()
                if stack:
                    u = stack[-1][0]
                    low[u] = min(low[u], low[v])
                    if low[v] > disc[u]:
                        bridges.append(pe)
    return comps, bridges


def _sides(n: int, adj, removed: set[int]) -> list[list[int]]:
    seen = [False] * n
    out = []
    for s in range(n):
        if seen[s]:
            continue
        comp, stack = [], [s]
        seen[s] = True
        while stack:
            v = stack.pop()
            comp.append(v)
            for w, ei in adj[v]:
                if ei not in removed and not seen[w]:
                    seen[w] = True
                    stack.append(w)
        out.append(comp)
    return out


def _has_cycle(comp: list[int], adj, removed: set[int]) -> bool:
    cs = set(comp)
    m = sum(1 for v in comp for w, ei in adj[v] if ei not in removed and w in cs) // 2
    return m >= len(comp)


def cyclic_cuts_below_4(g: Graph) -> list[tuple[int, ...]]:
    """All edge cuts with at most 3 edges whose sides both contain a cycle (empty list = none)."""
    n = g.n
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(g.edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    found = set()
    m = len(g.edges)

    def record(cut: tuple[int, ...]):
        removed = set(cut)
        comps = _sides(n, adj, removed)
        if len(comps) >= 2 and sum(1 for c in comps if _has_cycle(c, adj, removed)) >= 2:
            found.add(tuple(sorted(cut)))

    comps, br = _bridges(n, adj, set())
    if comps > 1:
        return [()]
    for b in br:
        record((b,))
    for e in range(m):
        _, br = _bridges(n, adj, {e})
        for b in br:
            record((e, b))
    for e, f in itertools.combinations(range(m), 2):
        _, br = _bridges(n, adj, {e, f})
        for b in br:
            record((e, f, b))
    return sorted(found)
