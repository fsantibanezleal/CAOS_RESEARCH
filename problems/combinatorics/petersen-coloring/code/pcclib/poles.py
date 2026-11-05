"""Multipoles cut from cubic graphs, their Petersen-coloring formulas, and the connector classes
they can conduct.

A 4-pole is a cubic graph with some vertices and edges removed so that exactly four dangling edge
ends remain. For a pairing of the four dangling ends into two connectors {p, q}, {r, s}, a map of
the 4-pole into E(P) with every vertex good has 1_s(p) + 1_s(q) + 1_s(r) + 1_s(s) in the cut space
of P, so the class of the connector {p, q} equals the class of {r, s}. The class of a pair of
labels (x, y) modulo the cut space is determined by the distance d(x, y) in the line graph of P
(0 when equal, 1 when adjacent, 2 or 3 otherwise), so a 4-pole with a pairing "conducts" a set of
distances D, a subset of {0, 1, 2, 3}.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

from .cnf import CNF
from .graphs import Graph, petersen


def line_distances() -> list[list[int]]:
    """Distances in the line graph of the Petersen graph (edge indices of graphs.petersen())."""
    p = petersen()
    m = len(p.edges)
    adj = [[j for j in range(m) if j != i and set(p.edges[i]) & set(p.edges[j])] for i in range(m)]
    dist = [[-1] * m for _ in range(m)]
    for s in range(m):
        dist[s][s] = 0
        frontier = [s]
        while frontier:
            nxt = []
            for x in frontier:
                for y in adj[x]:
                    if dist[s][y] < 0:
                        dist[s][y] = dist[s][x] + 1
                        nxt.append(y)
            frontier = nxt
    return dist


@dataclass
class Pole:
    """Kept vertices of a cubic graph, the internal edges among them, and the dangling ends.

    `items[v]` lists the three edge items at kept vertex v: ("e", i) for an internal edge i of the
    parent graph, ("d", j) for dangling end j. `dangling[j]` = (kept vertex, parent edge index)."""

    parent: Graph
    kept: list[int]
    internal: list[int]
    dangling: list[tuple[int, int]]
    items: dict[int, list[tuple[str, int]]] = field(default_factory=dict)


def pole(g: Graph, removed_vertices=(), removed_edges=()) -> Pole:
    rv, re_ = set(removed_vertices), set(removed_edges)
    kept = [v for v in range(g.n) if v not in rv]
    internal, dangling, items = [], [], {v: [] for v in kept}
    for i, (u, v) in enumerate(g.edges):
        if u in rv and v in rv:
            continue
        if i in re_:
            for w in (u, v):
                if w not in rv:
                    items[w].append(("d", len(dangling)))
                    dangling.append((w, i))
            continue
        if u in rv or v in rv:
            w = v if u in rv else u
            items[w].append(("d", len(dangling)))
            dangling.append((w, i))
            continue
        internal.append(i)
        items[u].append(("e", i))
        items[v].append(("e", i))
    return Pole(g, kept, internal, dangling, items)


def pole_formula(pl: Pole, fixed: dict[int, int] | None = None) -> tuple[CNF, dict]:
    """Map of the pole into E(P) with every kept vertex good; `fixed` pins dangling labels."""
    p = petersen()
    padj = [[j for j in range(15) if j != i and set(p.edges[i]) & set(p.edges[j])] for i in range(15)]
    f = CNF()
    y = {}
    keys = [("e", i) for i in pl.internal] + [("d", j) for j in range(len(pl.dangling))]
    for key in keys:
        for t in range(15):
            y[key, t] = f.var(f"y_{key[0]}{key[1]}_{t}")
        f.exactly_one([y[key, t] for t in range(15)])
    for v in pl.kept:
        for k1, k2 in itertools.combinations(pl.items[v], 2):
            for s in range(15):
                for t in range(15):
                    if s == t or t not in padj[s]:
                        f.add(-y[k1, s], -y[k2, t])
    for j, t in (fixed or {}).items():
        f.add(y[("d", j), t])
    return f, y


def check_pole(pl: Pole, lab: dict) -> bool:
    stars = {frozenset(s) for s in petersen().incidence()}
    for v in pl.kept:
        imgs = [lab[k] for k in pl.items[v]]
        if len(set(imgs)) != 3 or frozenset(imgs) not in stars:
            return False
    return True


def distance_representatives() -> dict[int, tuple[int, int]]:
    """For d = 0..3, a pair (x, y) of edge indices of P at distance d, with x = 0."""
    dist = line_distances()
    return {d: (0, min(t for t in range(15) if dist[0][t] == d)) for d in range(4)}
