"""CNF encodings of edge-coloring and cover properties of cubic graphs.

Independence from the public Putman encoders: the Petersen encoding uses edge-image variables
only (no vertex-witness variables) and pairwise adjacency constraints, which suffice because the
Petersen graph is triangle-free; the normal encoding uses side-presence variables instead of
missing-pair variables.
"""

from __future__ import annotations

import itertools

from .cnf import CNF
from .graphs import Graph, petersen

# --- helpers -------------------------------------------------------------------------------


def _stars(g: Graph) -> list[list[int]]:
    inc = g.incidence()
    if any(len(s) != 3 for s in inc):
        raise ValueError("graph must be cubic")
    return inc


def _side_edges(g: Graph, inc: list[list[int]], e: int) -> tuple[list[int], list[int]]:
    u, v = g.edges[e]
    return [x for x in inc[u] if x != e], [x for x in inc[v] if x != e]


# --- normal k-edge-colorings -------------------------------------------------------------


def normal_coloring(g: Graph, k: int, strong: bool = False, defect_bound: int | None = None) -> CNF:
    """Proper k-edge-coloring in which every edge is poor or rich.

    Variables x(e,c): edge e has color c. For each edge e = uv with side edges a1,a2 (at u) and
    b1,b2 (at v): p(e,c) <-> x(a1,c) or x(a2,c); q(e,c) <-> x(b1,c) or x(b2,c); r(e) = rich.
    rich: p and q disjoint for every c; poor: p(e,c) <-> q(e,c) for every c.
    With `strong`, every edge is forced rich. With `defect_bound = d`, each edge gets a bad
    indicator that switches its normality clauses off, and at most d indicators may be true.
    """
    inc = _stars(g)
    f = CNF()
    x = {(e, c): f.var(f"x_{e}_{c}") for e in range(len(g.edges)) for c in range(k)}
    for e in range(len(g.edges)):
        f.exactly_one([x[e, c] for c in range(k)])
    for v in range(g.n):
        for a, b in itertools.combinations(inc[v], 2):
            for c in range(k):
                f.add(-x[a, c], -x[b, c])
    bads = []
    for e in range(len(g.edges)):
        (a1, a2), (b1, b2) = _side_edges(g, inc, e)
        r = f.var(f"r_{e}")
        bad = f.var(f"bad_{e}") if defect_bound is not None else None
        if bad is not None:
            bads.append(bad)
        if strong:
            f.add(r)
        for c in range(k):
            p = f.var(f"p_{e}_{c}")
            q = f.var(f"q_{e}_{c}")
            # p <-> x(a1,c) or x(a2,c)
            f.add(-p, x[a1, c], x[a2, c])
            f.add(p, -x[a1, c])
            f.add(p, -x[a2, c])
            f.add(-q, x[b1, c], x[b2, c])
            f.add(q, -x[b1, c])
            f.add(q, -x[b2, c])
            guard = [bad] if bad is not None else []
            # rich: not (p and q)
            f.add(*guard, -r, -p, -q)
            # poor: p <-> q
            f.add(*guard, r, -p, q)
            f.add(*guard, r, p, -q)
    if defect_bound is not None:
        f.at_most_k(bads, defect_bound)
    return f


# --- Petersen colorings -----------------------------------------------------------------


def petersen_coloring(g: Graph, defect_bound: int | None = None, symmetry: bool = True) -> CNF:
    """Map E(G) -> E(P) such that adjacent edges of G go to distinct adjacent edges of P.

    Variables y(e,f). Because P is triangle-free, three pairwise adjacent distinct edges of P
    form a star, so pairwise constraints at every vertex give exactly the Petersen colorings.
    With `defect_bound = d`, each vertex gets a bad indicator switching off its pair
    constraints, and at most d may be true. Symmetry breaking uses the edge-transitivity of P
    and the transitivity of an edge stabilizer on the four edges adjacent to that edge.
    """
    inc = _stars(g)
    p = petersen()
    pedges = p.edges
    padj = [[j for j in range(15) if j != i and set(pedges[i]) & set(pedges[j])] for i in range(15)]
    f = CNF()
    y = {(e, t): f.var(f"y_{e}_{t}") for e in range(len(g.edges)) for t in range(15)}
    for e in range(len(g.edges)):
        f.exactly_one([y[e, t] for t in range(15)])
    bads = []
    for v in range(g.n):
        bad = f.var(f"bad_{v}") if defect_bound is not None else None
        if bad is not None:
            bads.append(bad)
        guard = [bad] if bad is not None else []
        for a, b in itertools.combinations(inc[v], 2):
            for s in range(15):
                for t in range(15):
                    if s == t or t not in padj[s]:
                        f.add(*guard, -y[a, s], -y[b, t])
    if symmetry and defect_bound is None:
        e0 = 0
        f.add(y[e0, 0])
        e1 = next(x for x in inc[g.edges[e0][0]] if x != e0)
        f.add(y[e1, padj[0][0]])
    if defect_bound is not None:
        f.at_most_k(bads, defect_bound)
    return f


# --- perfect matching covers --------------------------------------------------------------


def _matchings(f: CNF, g: Graph, count: int, prefix: str = "m") -> dict[tuple[int, int], int]:
    inc = _stars(g)
    m = {(e, i): f.var(f"{prefix}_{e}_{i}") for e in range(len(g.edges)) for i in range(count)}
    for v in range(g.n):
        for i in range(count):
            f.exactly_one([m[e, i] for e in inc[v]])
    return m


def berge_fulkerson(g: Graph) -> CNF:
    """Six perfect matchings covering every edge exactly twice."""
    f = CNF()
    m = _matchings(f, g, 6)
    for e in range(len(g.edges)):
        lits = [m[e, i] for i in range(6)]
        f.at_least_two(lits)
        f.at_most_two(lits)
    f.add(m[0, 0])
    f.add(m[0, 1])
    return f


def berge_cover(g: Graph, count: int) -> CNF:
    """`count` perfect matchings whose union is E(G)."""
    f = CNF()
    m = _matchings(f, g, count)
    for e in range(len(g.edges)):
        f.add(*[m[e, i] for i in range(count)])
    f.add(m[0, 0])
    return f


def fan_raspaud(g: Graph) -> CNF:
    """Three perfect matchings with no common edge."""
    f = CNF()
    m = _matchings(f, g, 3)
    for e in range(len(g.edges)):
        f.add(-m[e, 0], -m[e, 1], -m[e, 2])
    f.add(m[0, 0])
    return f


# --- cycle double covers ------------------------------------------------------------------


def cycle_double_cover(g: Graph, count: int) -> CNF:
    """`count` even subgraphs (every vertex degree 0 or 2 inside each) covering every edge twice."""
    inc = _stars(g)
    f = CNF()
    z = {(e, i): f.var(f"z_{e}_{i}") for e in range(len(g.edges)) for i in range(count)}
    for v in range(g.n):
        a, b, c = inc[v]
        for i in range(count):
            # forbid degree 1 and degree 3
            f.add(-z[a, i], z[b, i], z[c, i])
            f.add(z[a, i], -z[b, i], z[c, i])
            f.add(z[a, i], z[b, i], -z[c, i])
            f.add(-z[a, i], -z[b, i], -z[c, i])
    for e in range(len(g.edges)):
        lits = [z[e, i] for i in range(count)]
        f.at_least_two(lits)
        f.at_most_two(lits)
    f.add(z[0, 0])
    f.add(z[0, 1])
    return f


# --- nowhere-zero Z_k flows ---------------------------------------------------------------


def nowhere_zero_flow(g: Graph, k: int) -> CNF:
    """Nowhere-zero Z_k flow with edges oriented from the smaller to the larger endpoint.

    Variables w(e,a): edge e carries value a in 1..k-1. Conservation at v: the signed sum over
    the star vanishes mod k; encoded by forbidding every violating triple of values.
    """
    inc = _stars(g)
    f = CNF()
    w = {(e, a): f.var(f"w_{e}_{a}") for e in range(len(g.edges)) for a in range(1, k)}
    for e in range(len(g.edges)):
        f.exactly_one([w[e, a] for a in range(1, k)])
    for v in range(g.n):
        signs = [1 if g.edges[e][0] == v else -1 for e in inc[v]]
        for vals in itertools.product(range(1, k), repeat=3):
            if sum(s * a for s, a in zip(signs, vals)) % k != 0:
                f.add(*[-w[e, a] for e, a in zip(inc[v], vals)])
    return f


# --- ordinary edge colorings -------------------------------------------------------------


def proper_edge_coloring(g: Graph, k: int) -> CNF:
    inc = _stars(g)
    f = CNF()
    x = {(e, c): f.var(f"x_{e}_{c}") for e in range(len(g.edges)) for c in range(k)}
    for e in range(len(g.edges)):
        f.exactly_one([x[e, c] for c in range(k)])
    for v in range(g.n):
        for a, b in itertools.combinations(inc[v], 2):
            for c in range(k):
                f.add(-x[a, c], -x[b, c])
    return f
