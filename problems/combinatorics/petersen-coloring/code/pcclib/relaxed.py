"""Relaxed encodings: the Petersen or normality condition is dropped at one designated unit."""

from __future__ import annotations

import itertools

from .cnf import CNF
from .encoders import _side_edges, _stars
from .graphs import Graph, petersen


def petersen_relaxed_vertex(g: Graph, relaxed: int, symmetry: bool = True) -> CNF:
    """Edge map into E(P) whose star condition may fail only at vertex `relaxed`."""
    inc = _stars(g)
    p = petersen()
    pedges = p.edges
    padj = [[j for j in range(15) if j != i and set(pedges[i]) & set(pedges[j])] for i in range(15)]
    f = CNF()
    y = {(e, t): f.var(f"y_{e}_{t}") for e in range(len(g.edges)) for t in range(15)}
    for e in range(len(g.edges)):
        f.exactly_one([y[e, t] for t in range(15)])
    for v in range(g.n):
        if v == relaxed:
            continue
        for a, b in itertools.combinations(inc[v], 2):
            for s in range(15):
                for t in range(15):
                    if s == t or t not in padj[s]:
                        f.add(-y[a, s], -y[b, t])
    if symmetry:
        # fix the image of one edge not incident with the relaxed vertex, and of one adjacent
        # edge sharing a non-relaxed endpoint (edge-transitivity and edge-stabilizer transitivity)
        e0 = next(e for e in range(len(g.edges)) if relaxed not in g.edges[e])
        u = g.edges[e0][0] if g.edges[e0][0] != relaxed else g.edges[e0][1]
        e1 = next(x for x in inc[u] if x != e0)
        f.add(y[e0, 0])
        f.add(y[e1, padj[0][0]])
    return f


def normal5_relaxed_edge(g: Graph, relaxed: int) -> CNF:
    """Proper 5-edge-coloring normal at every edge except possibly `relaxed`."""
    inc = _stars(g)
    k = 5
    f = CNF()
    x = {(e, c): f.var(f"x_{e}_{c}") for e in range(len(g.edges)) for c in range(k)}
    for e in range(len(g.edges)):
        f.exactly_one([x[e, c] for c in range(k)])
    for v in range(g.n):
        for a, b in itertools.combinations(inc[v], 2):
            for c in range(k):
                f.add(-x[a, c], -x[b, c])
    for e in range(len(g.edges)):
        if e == relaxed:
            continue
        (a1, a2), (b1, b2) = _side_edges(g, inc, e)
        r = f.var(f"r_{e}")
        for c in range(k):
            pc = f.var(f"p_{e}_{c}")
            qc = f.var(f"q_{e}_{c}")
            f.add(-pc, x[a1, c], x[a2, c])
            f.add(pc, -x[a1, c])
            f.add(pc, -x[a2, c])
            f.add(-qc, x[b1, c], x[b2, c])
            f.add(qc, -x[b1, c])
            f.add(qc, -x[b2, c])
            f.add(-r, -pc, -qc)
            f.add(r, -pc, qc)
            f.add(r, pc, -qc)
    return f
