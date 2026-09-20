"""Automorphisms of a connected simple graph by backtracking along a BFS order.

Only soundness matters downstream: every returned permutation is re-checked by `is_automorphism`,
and orbit arguments use nothing but the fact that the listed permutations are automorphisms.
"""

from __future__ import annotations

from .graphs import Graph


def is_automorphism(g: Graph, perm: list[int]) -> bool:
    if sorted(perm) != list(range(g.n)):
        return False
    es = {(min(u, v), max(u, v)) for u, v in g.edges}
    return all((min(perm[u], perm[v]), max(perm[u], perm[v])) in es for u, v in g.edges)


def automorphisms(g: Graph) -> list[list[int]]:
    adj = [set() for _ in range(g.n)]
    for u, v in g.edges:
        adj[u].add(v)
        adj[v].add(u)
    order, seen = [0], {0}
    for u in order:
        for w in sorted(adj[u]):
            if w not in seen:
                seen.add(w)
                order.append(w)
    if len(order) != g.n:
        raise ValueError("graph must be connected")
    pos = {v: i for i, v in enumerate(order)}
    # earlier neighbours of each vertex in the BFS order
    back = [[w for w in adj[v] if pos[w] < pos[v]] for v in range(g.n)]
    out: list[list[int]] = []
    image = [-1] * g.n
    used = [False] * g.n

    def rec(i: int) -> None:
        if i == g.n:
            out.append(list(image))
            return
        v = order[i]
        if i == 0:
            cands = range(g.n)
        else:
            cands = adj[image[back[v][0]]]
        for c in cands:
            if used[c] or len(adj[c]) != len(adj[v]):
                continue
            if any(image[w] not in adj[c] for w in back[v]):
                continue
            # non-neighbours among earlier vertices must stay non-neighbours
            if sum(1 for w in adj[c] if used[w]) != len(back[v]):
                continue
            image[v] = c
            used[c] = True
            rec(i + 1)
            used[c] = False
            image[v] = -1

    rec(0)
    return out


def edge_orbits(g: Graph, perms: list[list[int]]) -> list[list[int]]:
    index = {(min(u, v), max(u, v)): i for i, (u, v) in enumerate(g.edges)}
    parent = list(range(len(g.edges)))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for p in perms:
        for i, (u, v) in enumerate(g.edges):
            j = index[(min(p[u], p[v]), max(p[u], p[v]))]
            ra, rb = find(i), find(j)
            if ra != rb:
                parent[ra] = rb
    orbits: dict[int, list[int]] = {}
    for i in range(len(g.edges)):
        orbits.setdefault(find(i), []).append(i)
    return sorted(orbits.values())
