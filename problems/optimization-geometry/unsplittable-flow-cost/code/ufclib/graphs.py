"""Graph-class decisions needed to locate an instance against the proved theorems.

Three questions matter for the consistency battery (literature dossier, section 5):

* acyclicity, because the Morell-Skutella conjectures are stated for acyclic digraphs, so
  a counterexample only kills them if it is acyclic;
* the presence of a K4 subdivision, because series-parallel digraphs (where the conjecture
  is PROVED, Majthoub Almoghrabi-Skutella-Warode) are exactly the K4-subdivision-free
  ones, so a valid counterexample must contain one;
* planarity, because the conjecture is proved for planar graphs at twice the violation
  (Traub-Vargas Koch-Zenklusen), so a planar counterexample pins that constant between 1
  and 2.

Everything here is exact combinatorics on tiny graphs; no heuristics, no floats.
"""

from __future__ import annotations

from itertools import combinations
from typing import Iterable, Optional, Sequence

from .instance import Instance, Vertex

Edge = tuple[Vertex, Vertex]


def is_acyclic(instance: Instance) -> bool:
    """Kahn-style topological peel on the directed graph."""
    indeg = {v: 0 for v in instance.vertices}
    for a in instance.arcs:
        indeg[a.head] += 1
    ready = [v for v, d in indeg.items() if d == 0]
    seen = 0
    while ready:
        v = ready.pop()
        seen += 1
        for a in instance.arcs:
            if a.tail == v:
                indeg[a.head] -= 1
                if indeg[a.head] == 0:
                    ready.append(a.head)
    return seen == len(instance.vertices)


def underlying_adjacency(
    vertices: Sequence[Vertex], edges: Iterable[Edge]
) -> dict[Vertex, list[Vertex]]:
    """Undirected adjacency (parallel arcs collapse; self-loops dropped)."""
    adj: dict[Vertex, set[Vertex]] = {v: set() for v in vertices}
    for u, v in edges:
        if u == v:
            continue
        adj[u].add(v)
        adj[v].add(u)
    return {v: sorted(ns) for v, ns in adj.items()}


def _disjoint_paths_exist(
    adj: dict[Vertex, list[Vertex]],
    pairs: Sequence[tuple[Vertex, Vertex]],
    branch: frozenset[Vertex],
) -> bool:
    """Can the given endpoint pairs be joined by internally disjoint paths?

    Internal vertices must avoid the branch vertices and each other. Backtracking over
    pairs, depth-first within a pair. Exponential in principle, trivial at our sizes.
    """
    used_internal: set[Vertex] = set()

    def route(idx: int) -> bool:
        if idx == len(pairs):
            return True
        a, b = pairs[idx]

        def walk(current: Vertex, visited: set[Vertex]) -> bool:
            for nxt in adj[current]:
                if nxt == b:
                    if route(idx + 1):
                        return True
                    continue
                if nxt in branch or nxt in used_internal or nxt in visited:
                    continue
                visited.add(nxt)
                used_internal.add(nxt)
                if walk(nxt, visited):
                    return True
                used_internal.discard(nxt)
                visited.discard(nxt)
            return False

        # the direct edge a-b is the length-one path, handled by walk's b branch
        return walk(a, {a})

    return route(0)


def has_k4_subdivision(instance: Instance) -> Optional[tuple[Vertex, ...]]:
    """Return four branch vertices of a K4 subdivision, or None.

    A K4 subdivision needs four vertices of degree at least 3 in the underlying undirected
    graph, pairwise joined by six internally disjoint paths. Graphs with no K4 subdivision
    are exactly the series-parallel (K4-minor-free) ones, which is the class where the
    conjecture is proved.
    """
    adj = underlying_adjacency(instance.vertices, instance.undirected_edges())
    candidates = [v for v in instance.vertices if len(adj[v]) >= 3]
    for quad in combinations(candidates, 4):
        branch = frozenset(quad)
        pairs = list(combinations(quad, 2))
        if _disjoint_paths_exist(adj, pairs, branch):
            return quad
    return None


def kuratowski_planarity_by_degrees(instance: Instance) -> Optional[bool]:
    """Decide planarity when the degree sequence alone settles it, else None.

    A K5 subdivision needs five vertices of degree at least 4; a K3,3 subdivision needs six
    of degree at least 3. If the graph has too few of either, Kuratowski's theorem makes it
    planar with no embedding computation at all. This is a sufficient test, not a full
    planarity algorithm, and it returns None when it cannot decide, so it can never
    silently assert planarity it has not established.
    """
    adj = underlying_adjacency(instance.vertices, instance.undirected_edges())
    deg3 = sum(1 for v in adj if len(adj[v]) >= 3)
    deg4 = sum(1 for v in adj if len(adj[v]) >= 4)
    if deg4 < 5 and deg3 < 6:
        return True
    return None


def demands_are_multiples_of_one_another(instance: Instance) -> bool:
    """Skutella 2002 proves the conjecture in this case, so a counterexample must fail it.

    The condition: the demands can be ordered so that each divides the next. Exact test on
    rationals via the ratio being an integer.
    """
    values = sorted(set(instance.demands.values()))
    for smaller, larger in zip(values, values[1:]):
        if smaller == 0:
            continue
        ratio = larger / smaller
        if ratio.denominator != 1:
            return False
    return True
