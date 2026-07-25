"""Path and routing enumeration.

The one rule this module exists to enforce: PATHS ARE NEVER SUPPLIED, THEY ARE ALWAYS
SEARCHED FOR. The documented failure mode of candidate counterexamples in this problem is
that only the intended paths were checked, so every routing enumeration in this programme
derives its path set from the digraph itself and asserts the count.

A path is simple in the vertex sense (no repeated vertex), which is the standard reading
of "an s-t path" in the conjecture statement. Restricting to simple paths is without loss
of generality for both conditions: appending a cycle can only add arc load, and since
costs are nonnegative it can only add cost, so a non-simple routing is never better than
the simple routing obtained by deleting its cycles.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterator, Mapping, Sequence

from .instance import Arc, Instance, Vertex

Path = tuple[Arc, ...]
Routing = tuple[Path, ...]


def simple_paths(instance: Instance, target: Vertex) -> list[Path]:
    """Every simple ``source``-``target`` path, as a tuple of arcs.

    Depth-first over arcs, forbidding revisits of vertices, so the search terminates on
    cyclic digraphs. Parallel arcs give distinct paths because arcs, not vertex pairs,
    are the units of a path.
    """
    result: list[Path] = []
    visited: set[Vertex] = {instance.source}

    def dfs(v: Vertex, prefix: Path) -> None:
        if v == target:
            result.append(prefix)
            return
        for arc in instance.out_arcs(v):
            if arc.head in visited:
                continue
            visited.add(arc.head)
            dfs(arc.head, prefix + (arc,))
            visited.discard(arc.head)

    dfs(instance.source, ())
    return result


def paths_by_terminal(instance: Instance) -> dict[Vertex, list[Path]]:
    return {t: simple_paths(instance, t) for t in instance.terminals}


def all_routings(instance: Instance) -> Iterator[Routing]:
    """Every unsplittable routing: one simple path per terminal, in terminal order."""
    per_terminal = paths_by_terminal(instance)
    for t in instance.terminals:
        if not per_terminal[t]:
            return  # a terminal with no path admits no routing at all
    yield from product(*(per_terminal[t] for t in instance.terminals))


def routing_load(instance: Instance, routing: Routing) -> dict[int, Fraction]:
    """The arc-load vector of a routing, indexed by arc index, exact."""
    load: dict[int, Fraction] = {a.index: Fraction(0) for a in instance.arcs}
    for terminal, path in zip(instance.terminals, routing):
        d = instance.demands[terminal]
        for arc in path:
            load[arc.index] += d
    return load


def path_label(path: Path, instance: Instance) -> str:
    """Human-readable ``s -> u -> t`` label for reports."""
    if not path:
        return instance.source
    return " -> ".join([path[0].tail] + [arc.head for arc in path])


def routing_label(routing: Routing, instance: Instance) -> str:
    return " | ".join(
        f"{t}: {path_label(p, instance)}"
        for t, p in zip(instance.terminals, routing)
    )


def count_routings(per_terminal: Mapping[Vertex, Sequence[Path]]) -> int:
    total = 1
    for paths in per_terminal.values():
        total *= len(paths)
    return total
