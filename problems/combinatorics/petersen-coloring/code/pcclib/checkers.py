"""Independent checkers: verify decoded witnesses from the graph alone (never from the CNF)."""

from __future__ import annotations

from .graphs import Graph, petersen


def decode(model: set[int], names: dict[str, int], prefix: str) -> dict[tuple[int, ...], bool]:
    """Extract named variables `prefix_i_j...` -> truth value from a model (set of true vars)."""
    out = {}
    for name, v in names.items():
        parts = name.split("_")
        if parts[0] != prefix:
            continue
        key = tuple(int(p) for p in parts[1:])
        out[key] = v in model
    return out


def edge_color_map(model: set[int], names: dict[str, int], m: int, k: int, prefix: str = "x") -> list[int]:
    vals = decode(model, names, prefix)
    colors = []
    for e in range(m):
        chosen = [c for c in range(k) if vals.get((e, c), False)]
        if len(chosen) != 1:
            raise ValueError(f"edge {e} has {len(chosen)} colors")
        colors.append(chosen[0])
    return colors


def check_proper(g: Graph, colors: list[int]) -> bool:
    inc = g.incidence()
    return all(len({colors[e] for e in inc[v]}) == len(inc[v]) for v in range(g.n))


def normal_defect(g: Graph, colors: list[int]) -> int:
    """Number of edges that are neither poor nor rich (requires a proper coloring)."""
    if not check_proper(g, colors):
        raise ValueError("not a proper edge coloring")
    inc = g.incidence()
    bad = 0
    for e, (u, v) in enumerate(g.edges):
        seen = {colors[x] for x in inc[u]} | {colors[x] for x in inc[v]}
        if len(seen) not in (3, 5):
            bad += 1
    return bad


def is_strong_normal(g: Graph, colors: list[int]) -> bool:
    inc = g.incidence()
    return check_proper(g, colors) and all(
        len({colors[x] for x in inc[u]} | {colors[x] for x in inc[v]}) == 5 for u, v in g.edges
    )


def petersen_defect(g: Graph, images: list[int]) -> int:
    """Number of vertices whose star does not map onto a star of the Petersen graph."""
    p = petersen()
    stars = {frozenset(s) for s in p.incidence()}
    inc = g.incidence()
    bad = 0
    for v in range(g.n):
        if frozenset(images[e] for e in inc[v]) not in stars or len({images[e] for e in inc[v]}) != 3:
            bad += 1
    return bad


def matchings_from_model(model: set[int], names: dict[str, int], m: int, count: int, prefix: str = "m") -> list[set[int]]:
    vals = decode(model, names, prefix)
    return [{e for e in range(m) if vals.get((e, i), False)} for i in range(count)]


def is_perfect_matching(g: Graph, edges: set[int]) -> bool:
    covered = [0] * g.n
    for e in edges:
        u, v = g.edges[e]
        covered[u] += 1
        covered[v] += 1
    return all(c == 1 for c in covered)


def check_berge_fulkerson(g: Graph, matchings: list[set[int]]) -> bool:
    if len(matchings) != 6 or not all(is_perfect_matching(g, M) for M in matchings):
        return False
    return all(sum(e in M for M in matchings) == 2 for e in range(len(g.edges)))


def check_berge_cover(g: Graph, matchings: list[set[int]]) -> bool:
    if not all(is_perfect_matching(g, M) for M in matchings):
        return False
    return all(any(e in M for M in matchings) for e in range(len(g.edges)))


def check_fan_raspaud(g: Graph, matchings: list[set[int]]) -> bool:
    if len(matchings) != 3 or not all(is_perfect_matching(g, M) for M in matchings):
        return False
    return not (matchings[0] & matchings[1] & matchings[2])


def is_even_subgraph(g: Graph, edges: set[int]) -> bool:
    deg = [0] * g.n
    for e in edges:
        u, v = g.edges[e]
        deg[u] += 1
        deg[v] += 1
    return all(d % 2 == 0 for d in deg)


def check_cycle_double_cover(g: Graph, cycles: list[set[int]]) -> bool:
    if not all(is_even_subgraph(g, C) for C in cycles):
        return False
    return all(sum(e in C for C in cycles) == 2 for e in range(len(g.edges)))


def check_flow(g: Graph, values: list[int], k: int) -> bool:
    if any(a % k == 0 for a in values):
        return False
    net = [0] * g.n
    for e, (u, v) in enumerate(g.edges):
        net[u] += values[e]
        net[v] -= values[e]
    return all(x % k == 0 for x in net)
