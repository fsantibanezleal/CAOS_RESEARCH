"""Graph containers, loaders, the Petersen graph, and small control graphs."""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path

Edge = tuple[int, int]


@dataclass(frozen=True)
class Graph:
    n: int
    edges: tuple[Edge, ...]

    @staticmethod
    def from_edges(edges) -> "Graph":
        es = sorted({(min(u, v), max(u, v)) for u, v in edges})
        for u, v in es:
            if u == v:
                raise ValueError(f"loop at {u}")
        verts = {x for e in es for x in e}
        n = max(verts) + 1 if verts else 0
        if verts != set(range(n)):
            raise ValueError("vertices must be 0..n-1 without gaps")
        return Graph(n, tuple(es))

    def adjacency(self) -> list[list[int]]:
        adj: list[list[int]] = [[] for _ in range(self.n)]
        for u, v in self.edges:
            adj[u].append(v)
            adj[v].append(u)
        return [sorted(a) for a in adj]

    def incidence(self) -> list[list[int]]:
        """Edge indices at each vertex, in increasing edge-index order."""
        inc: list[list[int]] = [[] for _ in range(self.n)]
        for i, (u, v) in enumerate(self.edges):
            inc[u].append(i)
            inc[v].append(i)
        return inc

    def is_cubic(self) -> bool:
        return all(len(a) == 3 for a in self.adjacency())

    def digest(self) -> str:
        """Putman's convention: SHA-256 of the compact JSON of the sorted edge list."""
        payload = json.dumps([list(e) for e in self.edges], separators=(",", ":")).encode()
        return hashlib.sha256(payload).hexdigest()

    def other_end(self, edge_index: int, v: int) -> int:
        u, w = self.edges[edge_index]
        if v == u:
            return w
        if v == w:
            return u
        raise ValueError("vertex not on edge")


def load_edgelist(path: Path | str) -> Graph:
    edges = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        a, b = line.split()
        edges.append((int(a), int(b)))
    return Graph.from_edges(edges)


def petersen() -> Graph:
    """Kneser graph K(5,2): vertices are the 2-subsets of {0..4}, adjacent when disjoint."""
    verts = list(itertools.combinations(range(5), 2))
    index = {s: i for i, s in enumerate(verts)}
    edges = [
        (index[a], index[b])
        for a, b in itertools.combinations(verts, 2)
        if set(a).isdisjoint(b)
    ]
    g = Graph.from_edges(edges)
    assert g.n == 10 and len(g.edges) == 15
    return g


def k4() -> Graph:
    return Graph.from_edges(itertools.combinations(range(4), 2))


def prism() -> Graph:
    """The triangular prism, 3-edge-colorable."""
    return Graph.from_edges([(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3), (1, 4), (2, 5)])


def flower_snark(k: int) -> Graph:
    """Isaacs' flower snark J_k for odd k >= 3 (J_3 has a triangle; J_5 is the 20-vertex snark).

    Vertices: a_i (hub), b_i, c_i, d_i for i in Z_k. Edges: a_i b_i, a_i c_i, a_i d_i,
    b_i b_{i+1}, c_i c_{i+1} for i < k-1, d_i d_{i+1} for i < k-1, and the twisted closing edges
    c_{k-1} d_0 and d_{k-1} c_0.
    """
    if k < 3 or k % 2 == 0:
        raise ValueError("k must be odd and at least 3")
    a = lambda i: 4 * i  # noqa: E731
    b = lambda i: 4 * i + 1  # noqa: E731
    c = lambda i: 4 * i + 2  # noqa: E731
    d = lambda i: 4 * i + 3  # noqa: E731
    edges = []
    for i in range(k):
        edges += [(a(i), b(i)), (a(i), c(i)), (a(i), d(i)), (b(i), b((i + 1) % k))]
    for i in range(k - 1):
        edges += [(c(i), c(i + 1)), (d(i), d(i + 1))]
    edges += [(c(k - 1), d(0)), (d(k - 1), c(0))]
    g = Graph.from_edges(edges)
    assert g.n == 4 * k and len(g.edges) == 6 * k
    return g


def petersen_minus_adjacent_pair() -> tuple[Graph, list[int]]:
    """The 4-pole F as an 8-vertex graph with four degree-2 vertices (the semiedge owners).

    Returns the graph and the list of the four vertices of degree 2 in the original Petersen
    labeling order.
    """
    p = petersen()
    adj = p.adjacency()
    u, v = 0, adj[0][0]
    keep = [x for x in range(10) if x not in (u, v)]
    relabel = {x: i for i, x in enumerate(keep)}
    edges = [(relabel[a], relabel[b]) for a, b in p.edges if a in relabel and b in relabel]
    g = Graph.from_edges(edges)
    owners = [relabel[x] for x in keep if len([y for y in adj[x] if y in relabel]) == 2]
    assert g.n == 8 and len(g.edges) == 10 and len(owners) == 4
    return g, owners
