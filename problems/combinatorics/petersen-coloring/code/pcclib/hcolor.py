"""H-colorings with an unknown target: is a cubic graph G colored by some cubic multigraph on k vertices?

Target H: k vertices, three slots each; a perfect matching on the 3k slots with no pair inside a
vertex is the edge set of a loopless cubic multigraph. A coloring sends each vertex v of G to a
target vertex and its three incident edges bijectively to the three slots of that vertex; along an
edge uv of G the two slots coincide or are matched (the same edge of H seen from both ends).
Target vertices are numbered in order of first use; the founder of each class fixes its slot order.
"""

from __future__ import annotations

import itertools

from .cnf import CNF
from .graphs import Graph


def amo_ladder(f: CNF, lits: list[int]) -> None:
    """At most one of `lits`, sequential encoding (3n clauses)."""
    n = len(lits)
    if n <= 4:
        for a, b in itertools.combinations(lits, 2):
            f.add(-a, -b)
        return
    s = [f.fresh() for _ in range(n - 1)]
    f.add(-lits[0], s[0])
    for i in range(1, n - 1):
        f.add(-lits[i], s[i])
        f.add(-s[i - 1], s[i])
        f.add(-lits[i], -s[i - 1])
    f.add(-lits[n - 1], -s[n - 2])


def exactly_one_ladder(f: CNF, lits: list[int]) -> None:
    f.add(*lits)
    amo_ladder(f, lits)


class HColorInstance:
    def __init__(self, g: Graph, k: int, reduced: bool = False):
        if any(len(s) != 3 for s in g.incidence()):
            raise ValueError("G must be cubic")
        self.g, self.k = g, k
        self.f = CNF()
        self.inc = g.incidence()
        f = self.f
        n = g.n
        self.x = {(v, i): f.var(f"x_{v}_{i}") for v in range(n) for i in range(k)}
        self.z = {(v, r, s): f.var(f"z_{v}_{r}_{s}") for v in range(n) for r in range(3) for s in range(3)}
        self.slots = [(i, s) for i in range(k) for s in range(3)]
        self.p = {}
        for a, b in itertools.combinations(self.slots, 2):
            if a[0] != b[0]:
                self.p[(a, b)] = f.var(f"p_{a[0]}_{a[1]}_{b[0]}_{b[1]}")
        self._build()
        self.q = None
        if reduced:
            self._reduce()

    def pvar(self, a, b) -> int:
        return self.p[(a, b)] if a < b else self.p[(b, a)]

    def _build(self) -> None:
        f, g, k, n = self.f, self.g, self.k, self.g.n
        x, z = self.x, self.z
        # vertex map: exactly one class
        for v in range(n):
            exactly_one_ladder(f, [x[v, i] for i in range(k)])
        # slot bijection at every vertex
        for v in range(n):
            for r in range(3):
                f.exactly_one([z[v, r, s] for s in range(3)])
            for s in range(3):
                f.exactly_one([z[v, r, s] for r in range(3)])
        # perfect matching on slots
        for a in self.slots:
            exactly_one_ladder(f, [self.pvar(a, b) for b in self.slots if b[0] != a[0]])
        # w(v,r,i,s) <-> x(v,i) and z(v,r,s)
        w = {}
        for v in range(n):
            for r in range(3):
                for i in range(k):
                    for s in range(3):
                        t = f.fresh()
                        w[v, r, i, s] = t
                        f.add(-t, x[v, i])
                        f.add(-t, z[v, r, s])
                        f.add(t, -x[v, i], -z[v, r, s])
        self.w = w
        # consistency along each edge of G
        for e, (u, v) in enumerate(g.edges):
            ru = self.inc[u].index(e)
            rv = self.inc[v].index(e)
            for (i, s) in self.slots:
                for (j, t) in self.slots:
                    if (i, s) == (j, t):
                        continue
                    if i == j:
                        f.add(-w[u, ru, i, s], -w[v, rv, j, t])
                    else:
                        f.add(-w[u, ru, i, s], -w[v, rv, j, t], self.pvar((i, s), (j, t)))
        # symmetry: classes numbered by first use; founders fix the slot order
        used = {}
        for v in range(n):
            for i in range(k):
                uvar = f.fresh()
                used[v, i] = uvar
                f.add(-x[v, i], uvar)
                if v > 0:
                    f.add(-used[v - 1, i], uvar)
                    f.add(-uvar, x[v, i], used[v - 1, i])
                else:
                    f.add(-uvar, x[v, i])
        f.add(x[0, 0])
        for v in range(n):
            for i in range(1, k):
                if v == 0:
                    f.add(-x[0, i])
                else:
                    f.add(-x[v, i], used[v - 1, i - 1])
        for v in range(n):
            for i in range(k):
                # founder: x(v,i) and class i unused before v  =>  identity slot assignment
                prior = [used[v - 1, i]] if v > 0 else []
                for r in range(3):
                    f.add(-x[v, i], *prior, z[v, r, r])
        self.used = used

    def _reduce(self) -> None:
        """Sound restrictions (context/2026-09-18-hcoloring-reduction-lemmas.md): all fibers of the
        vertex map have the same parity q (Lemma A); at most one target vertex is unused (Lemma B);
        even fibers need at most n/2 used vertices."""
        f, k, n = self.f, self.k, self.g.n
        q = f.var("q_fibers_odd")
        self.q = q
        for i in range(k):
            acc = self.x[0, i]
            for v in range(1, n):
                t = f.fresh()
                a, b = acc, self.x[v, i]
                f.add(-t, a, b)
                f.add(-t, -a, -b)
                f.add(t, -a, b)
                f.add(t, a, -b)
                acc = t
            f.add(-acc, q)
            f.add(acc, -q)
            f.add(-q, self.used[n - 1, i])
        if k >= 2:
            f.add(self.used[n - 1, k - 2])
        if 2 * (k - 1) > n:
            f.add(q)

    def decode(self, model: set[int]):
        g, k = self.g, self.k
        vmap = [next(i for i in range(k) if self.x[v, i] in model) for v in range(g.n)]
        partner = {}
        for (a, b), var in self.p.items():
            if var in model:
                partner[a] = b
                partner[b] = a
        hedges = sorted({(min(a, b), max(a, b)) for a, b in partner.items()})
        edge_image = []
        for e, (u, v) in enumerate(g.edges):
            ru = self.inc[u].index(e)
            s = next(s for s in range(3) if self.z[u, ru, s] in model)
            a = (vmap[u], s)
            edge_image.append((min(a, partner[a]), max(a, partner[a])))
        return vmap, hedges, edge_image

    def cut_clause(self, side: set[int], exclude=None) -> tuple[int, ...]:
        """Some slot pair (other than `exclude`) joins a target vertex in `side` to one outside."""
        lits = []
        for (a, b), var in self.p.items():
            if (a[0] in side) != (b[0] in side) and (a, b) != exclude:
                lits.append(var)
        return tuple(lits)


def check_hcoloring(g: Graph, k: int, hedges, edge_image) -> dict:
    """Independent check from the definition; hedges are slot pairs ((i,s),(j,t))."""
    rep = {"cubic_loopless": True, "coloring": True}
    deg = [0] * k
    for a, b in hedges:
        if a[0] == b[0]:
            rep["cubic_loopless"] = False
        deg[a[0]] += 1
        deg[b[0]] += 1
    if any(d != 3 for d in deg) or len(hedges) * 2 != 3 * k:
        rep["cubic_loopless"] = False
    hset = set(hedges)
    stars = {}
    for i in range(k):
        stars[i] = frozenset(h for h in hedges if h[0][0] == i or h[1][0] == i)
    star_sets = set(stars.values())
    inc = g.incidence()
    for v in range(g.n):
        imgs = [edge_image[e] for e in inc[v]]
        if any(h not in hset for h in imgs) or len(set(imgs)) != 3 or frozenset(imgs) not in star_sets:
            rep["coloring"] = False
    # connectivity and bridges of H as a multigraph
    adj = {i: [] for i in range(k)}
    for idx, (a, b) in enumerate(hedges):
        adj[a[0]].append((b[0], idx))
        adj[b[0]].append((a[0], idx))

    def comps(skip=None):
        seen, out = set(), []
        for s in range(k):
            if s in seen:
                continue
            stack, comp = [s], set()
            seen.add(s)
            while stack:
                y = stack.pop()
                comp.add(y)
                for t, idx in adj[y]:
                    if idx == skip or t in seen:
                        continue
                    seen.add(t)
                    stack.append(t)
            out.append(comp)
        return out

    cs = comps()
    rep["components"] = [sorted(c) for c in cs] if len(cs) > 1 else 1
    rep["connected"] = len(cs) == 1
    bridge = None
    if rep["connected"]:
        for idx in range(len(hedges)):
            c2 = comps(skip=idx)
            if len(c2) > 1:
                bridge = (idx, sorted(c2[0]))
                break
    rep["bridge"] = bridge
    rep["ok"] = rep["cubic_loopless"] and rep["coloring"] and rep["connected"] and bridge is None
    return rep


def target_as_graph(k: int, hedges) -> Graph:
    """The target multigraph as a Graph with repeated edges kept (incidence works per edge)."""
    es = sorted((min(a[0], b[0]), max(a[0], b[0])) for a, b in hedges)
    return Graph(k, tuple(es))
