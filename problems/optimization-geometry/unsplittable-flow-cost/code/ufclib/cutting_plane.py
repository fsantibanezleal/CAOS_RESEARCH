"""A cutting-plane evaluator of the frontier value, exact and streaming.

``frontier.frontier_value`` stores every routing's load row and solves one dense LP over
all routings below each alpha level, which does not finish on instances with tens of
thousands of routings (Afrasyab's C5 has 59,049). The frontier value is the largest level A
such that some cost vector c >= 0 makes every routing in U_A = {y : alpha(y) < A} strictly
more expensive than x. This module finds it without ever holding U_A:

* one streaming pass over ``all_routings`` collects the distinct alpha levels (and the
  ceiling) and stores nothing else;
* positivity of a level is monotone (U_A grows with A), so a binary search over the sorted
  levels needs only O(log L) level tests;
* a level test is a cutting-plane loop. The separation LP (``simplex.max_min_margin``,
  Bland's rule) runs over the cut set only; its cost vector c is handed to an exact
  branch-and-bound oracle that returns the cheapest routing in U_A. If that routing is
  strictly more expensive than x under c, c separates all of U_A and the level is positive;
  otherwise the routing is a violated constraint and becomes a cut. If the LP over the
  cuts has optimum <= 0, the level is not positive, because the cuts are a subset of U_A's
  constraints.

All arithmetic is ``Fraction``; there are no floats.

Difference from ``frontier_value``: the result carries the sorted distinct alpha levels
(``levels``), not the sorted alpha of every routing (``routing_alphas``), because storing
that list is what this evaluator avoids. ``alpha_max`` and ``ceiling`` are the same
quantities with the same tie and edge conventions (the lowest level is always positive, as
U_A is empty there). ``witness_cost`` is a cost vector found at the returned level; it can
differ from the one ``frontier_value`` returns, since the LP optimum is not unique.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Sequence

from .decide import alpha_for_routing
from .enumerate_routings import Path, Routing, all_routings, paths_by_terminal, routing_load
from .instance import Instance
from .simplex import max_min_margin

Load = dict[int, Fraction]


@dataclass(frozen=True)
class CPResult:
    alpha_max: Fraction
    witness_cost: tuple[Fraction, ...]
    ceiling: Fraction
    levels: tuple[Fraction, ...]
    solves: int  # separation-LP solves, summed over every tested level
    cuts: int  # cut rows added, summed over every tested level
    tested: tuple[tuple[Fraction, bool, int, int], ...]  # (level, positive, solves, cuts)

    @property
    def is_counterexample(self) -> bool:
        return self.alpha_max > 1


def cheapest_routing_below(
    instance: Instance,
    costs: Sequence[Fraction],
    level: Fraction,
    _per_terminal: Optional[dict] = None,
) -> Optional[tuple[Routing, Load, Fraction]]:
    """The routing y with alpha(y) < ``level`` minimising ``costs^T y``, or None if none.

    Returns ``(routing, load, cost)``; ``costs`` is indexed by arc index. Exact
    branch-and-bound over the terminals, largest demand first. A branch is cut when a
    partial load already has an arc with ``y_a >= x_a + level * d_max`` (loads only grow
    as terminals are added, so no completion can be below the level) or when the partial
    cost plus the cheapest remaining path of every undecided terminal cannot beat the best
    found. Ties keep the first routing met, in a deterministic order (terminal order by
    demand then position, paths by cost then enumeration order).
    """
    per = _per_terminal if _per_terminal is not None else paths_by_terminal(instance)
    arcs = instance.arcs
    d_max = instance.d_max
    if level <= 0:
        return None  # alpha is floored at 0, so no routing has alpha < level
    limit = [a.x + level * d_max for a in arcs]

    order = sorted(range(len(instance.terminals)), key=lambda i: -instance.demands[instance.terminals[i]])
    # per terminal: (demand, [(path, arc indices, unit cost)]) sorted by cost, stable
    plan = []
    for ti in order:
        t = instance.terminals[ti]
        d = instance.demands[t]
        entries = []
        for p in per[t]:
            idx = [a.index for a in p]
            entries.append((p, idx, d * sum((costs[i] for i in idx), Fraction(0))))
        entries.sort(key=lambda e: e[2])  # stable: ties stay in enumeration order
        plan.append((ti, d, entries))
        if not entries:
            return None
    n = len(plan)
    # suffix_min[k] = sum over plan[k:] of the cheapest path cost
    suffix_min = [Fraction(0)] * (n + 1)
    for k in range(n - 1, -1, -1):
        suffix_min[k] = suffix_min[k + 1] + plan[k][2][0][2]

    load = [Fraction(0)] * len(arcs)
    chosen: list[Optional[Path]] = [None] * n
    best: list = [None, None]  # [cost, chosen copy]

    def dfs(k: int, partial: Fraction) -> None:
        if k == n:
            if best[0] is None or partial < best[0]:
                best[0] = partial
                best[1] = list(chosen)
            return
        _, d, entries = plan[k]
        for path, idx, cost in entries:
            if best[0] is not None and partial + cost + suffix_min[k + 1] >= best[0]:
                break  # entries are sorted by cost: every later one is at least as dear
            ok = True
            for i in idx:
                if load[i] + d >= limit[i]:
                    ok = False
                    break
            if not ok:
                continue
            for i in idx:
                load[i] += d
            chosen[k] = path
            dfs(k + 1, partial + cost)
            for i in idx:
                load[i] -= d

    dfs(0, Fraction(0))
    if best[0] is None:
        return None
    routing_by_pos: list[Optional[Path]] = [None] * n
    for k, (ti, _, _) in enumerate(plan):
        routing_by_pos[ti] = best[1][k]
    routing: Routing = tuple(routing_by_pos)  # type: ignore[arg-type]
    return routing, routing_load(instance, routing), best[0]


def level_positive(
    instance: Instance,
    level: Fraction,
    base_cuts: Sequence[Sequence[Fraction]] = (),
    _per_terminal: Optional[dict] = None,
) -> tuple[bool, tuple[Fraction, ...], int, list[list[Fraction]]]:
    """Is there a cost vector making every routing in U_level strictly dearer than x?

    ``base_cuts`` must be load rows of routings already known to lie in U_level (rows found
    at a smaller level qualify). Returns ``(positive, witness, solves, cuts)`` where
    ``cuts`` is the full cut list (base plus new) and ``witness`` is the separating cost
    vector when positive (otherwise the last LP vector).
    """
    arcs = instance.arcs
    m = len(arcs)
    x = [a.x for a in arcs]
    cuts: list[list[Fraction]] = [list(r) for r in base_cuts]
    solves = 0
    witness: tuple[Fraction, ...] = tuple(Fraction(1, m) for _ in range(m))
    while True:
        optimum, c = max_min_margin(cuts, x)
        solves += 1
        witness = c
        if optimum <= 0:
            return False, witness, solves, cuts
        found = cheapest_routing_below(instance, c, level, _per_terminal)
        if found is None:  # U_level is empty: any cost vector separates nothing to separate
            return True, witness, solves, cuts
        _, load, cost = found
        cx = sum((ci * xi for ci, xi in zip(c, x)), Fraction(0))
        if cost - cx > 0:
            return True, witness, solves, cuts
        cuts.append([load[a.index] for a in arcs])


def frontier_value_cp(instance: Instance) -> CPResult:
    """The frontier value, exactly, by streaming levels, binary search and cutting planes."""
    instance.check_feasible()
    arcs = list(instance.arcs)

    alphas: set[Fraction] = set()
    ceiling: Optional[Fraction] = None
    min_cost: Optional[Fraction] = None
    for routing in all_routings(instance):
        load = routing_load(instance, routing)
        alpha = alpha_for_routing(instance, load)
        alphas.add(alpha)
        cost = sum((a.cost * load[a.index] for a in arcs), Fraction(0))
        if min_cost is None or cost < min_cost:  # first cheapest, as frontier_value's min()
            min_cost, ceiling = cost, alpha
    if not alphas:
        raise ValueError("no routing exists; the instance cannot be feasible")
    levels = tuple(sorted(alphas))
    assert ceiling is not None

    per = paths_by_terminal(instance)
    m = len(arcs)
    best_idx = 0  # the lowest level is always positive: U is empty there
    best_witness: tuple[Fraction, ...] = tuple(Fraction(1, m) for _ in range(m))
    lo_cuts: list[list[Fraction]] = []  # cuts found at the highest positive level so far
    lo, hi = 0, len(levels)  # levels[lo] positive; levels[hi:] not positive
    tested = []
    total_solves = total_cuts = 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        ok, witness, solves, cuts = level_positive(instance, levels[mid], lo_cuts, per)
        new_cuts = len(cuts) - len(lo_cuts)
        tested.append((levels[mid], ok, solves, new_cuts))
        total_solves += solves
        total_cuts += new_cuts
        if ok:
            lo, best_idx, best_witness, lo_cuts = mid, mid, witness, cuts
        else:
            hi = mid
    return CPResult(
        alpha_max=levels[best_idx],
        witness_cost=best_witness,
        ceiling=ceiling,
        levels=levels,
        solves=total_solves,
        cuts=total_cuts,
        tested=tuple(tested),
    )
