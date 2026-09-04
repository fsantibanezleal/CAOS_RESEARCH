"""Exact structural invariants of small cubic graphs (standard library only)."""

from __future__ import annotations

import itertools
from collections import deque

from .graphs import Graph


def components(g: Graph, removed_edges: set[int] | None = None) -> list[list[int]]:
    removed = removed_edges or set()
    inc = g.incidence()
    seen = [False] * g.n
    comps = []
    for s in range(g.n):
        if seen[s]:
            continue
        comp = []
        dq = deque([s])
        seen[s] = True
        while dq:
            v = dq.popleft()
            comp.append(v)
            for ei in inc[v]:
                if ei in removed:
                    continue
                w = g.other_end(ei, v)
                if not seen[w]:
                    seen[w] = True
                    dq.append(w)
        comps.append(sorted(comp))
    return comps


def is_connected(g: Graph) -> bool:
    return len(components(g)) == 1


def girth(g: Graph) -> int:
    """Length of a shortest cycle (BFS from every vertex), or 0 when acyclic."""
    adj = g.adjacency()
    best = 0
    for s in range(g.n):
        dist = [-1] * g.n
        parent = [-1] * g.n
        dist[s] = 0
        dq = deque([s])
        while dq:
            v = dq.popleft()
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    parent[w] = v
                    dq.append(w)
                elif parent[v] != w:
                    cyc = dist[v] + dist[w] + 1
                    if best == 0 or cyc < best:
                        best = cyc
    return best


def _max_flow_edge_disjoint(adj: list[list[int]], s: int, t: int, cap: int) -> int:
    """Number of edge-disjoint s-t paths, stopping at cap (Edmonds-Karp on unit capacities)."""
    n = len(adj)
    flow: dict[tuple[int, int], int] = {}
    total = 0
    while total < cap:
        parent = [-2] * n
        parent[s] = -1
        dq = deque([s])
        while dq and parent[t] == -2:
            v = dq.popleft()
            for w in adj[v]:
                residual = 1 - flow.get((v, w), 0) + flow.get((w, v), 0)
                if residual > 0 and parent[w] == -2:
                    parent[w] = v
                    dq.append(w)
        if parent[t] == -2:
            break
        v = t
        while v != s:
            u = parent[v]
            if flow.get((v, u), 0) > 0:
                flow[(v, u)] -= 1
            else:
                flow[(u, v)] = flow.get((u, v), 0) + 1
            v = u
        total += 1
    return total


def edge_connectivity(g: Graph) -> int:
    """Global edge connectivity, exact: min over t of the s-t max flow from a fixed s."""
    if g.n < 2:
        return 0
    adj = g.adjacency()
    cap = min(len(a) for a in adj)
    best = cap
    for t in range(1, g.n):
        best = min(best, _max_flow_edge_disjoint(adj, 0, t, best))
        if best == 0:
            break
    return best


def is_bridgeless(g: Graph) -> bool:
    return is_connected(g) and edge_connectivity(g) >= 2


def has_cycle(g: Graph, vertices: list[int], removed_edges: set[int]) -> bool:
    """Whether the subgraph induced on `vertices` minus `removed_edges` contains a cycle."""
    vs = set(vertices)
    inc = g.incidence()
    m = 0
    for v in vertices:
        for ei in inc[v]:
            if ei in removed_edges:
                continue
            w = g.other_end(ei, v)
            if w in vs and w > v:
                m += 1
    # a forest on k vertices with c components has k - c edges
    sub_removed = set(removed_edges)
    for v in range(g.n):
        if v not in vs:
            for ei in inc[v]:
                sub_removed.add(ei)
    comps = [c for c in components(g, sub_removed) if c[0] in vs]
    return m > len(vertices) - len(comps)


def cyclic_edge_cut_below(g: Graph, k: int) -> tuple[int, ...] | None:
    """Return a cycle-separating edge cut of size < k, or None if none exists.

    Exhaustive over all edge subsets of size 1..k-1 (fine for k <= 4 on 168 edges). A cut is
    cycle-separating when its removal leaves at least two components that each contain a cycle.
    """
    m = len(g.edges)
    for size in range(1, k):
        for subset in itertools.combinations(range(m), size):
            removed = set(subset)
            comps = components(g, removed)
            if len(comps) < 2:
                continue
            cyclic = [c for c in comps if has_cycle(g, c, removed)]
            if len(cyclic) >= 2:
                return subset
    return None


def is_cycle_separating(g: Graph, cut: tuple[int, ...]) -> bool:
    removed = set(cut)
    comps = components(g, removed)
    return len([c for c in comps if has_cycle(g, c, removed)]) >= 2


def boundary_edges(g: Graph, vertex_set: set[int]) -> tuple[int, ...]:
    return tuple(i for i, (u, v) in enumerate(g.edges) if (u in vertex_set) != (v in vertex_set))


def basic_report(g: Graph) -> dict:
    return {
        "order": g.n,
        "size": len(g.edges),
        "cubic": g.is_cubic(),
        "connected": is_connected(g),
        "edge_connectivity": edge_connectivity(g),
        "girth": girth(g),
        "digest": g.digest(),
    }
