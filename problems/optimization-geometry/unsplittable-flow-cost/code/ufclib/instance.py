"""The SSUF instance model, exact and arc-indexed.

Arcs are carried in an indexed list rather than keyed by (tail, head), so PARALLEL ARCS
are representable and produce distinct paths. A model keyed on vertex pairs silently
merges them and undercounts routings, which is one of the two failure modes this problem
punishes (the other is incomplete path enumeration).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Iterable, Mapping, Sequence

Vertex = str
Rational = Fraction


class InfeasibleFlow(ValueError):
    """Raised when the supplied vector is not a feasible fractional flow."""


def _rat(value) -> Rational:
    """Coerce to an exact Fraction, refusing floats outright.

    Accepting a float here would let inexact data enter through the front door, so the
    constructor rejects it rather than converting it.
    """
    if isinstance(value, float):
        raise TypeError(
            "float values are not accepted in this problem; pass an int, a Fraction, "
            "or a string such as '1/2'"
        )
    return Fraction(value)


@dataclass(frozen=True)
class Arc:
    """One arc: its index, endpoints, fractional load and per-unit cost."""

    index: int
    tail: Vertex
    head: Vertex
    x: Rational
    cost: Rational

    def __str__(self) -> str:  # pragma: no cover - display only
        return f"a{self.index}:{self.tail}->{self.head}"


@dataclass
class Instance:
    """A single-source unsplittable-flow instance with costs.

    Capacities are the fractional flow ``x`` itself, which is the convention of the whole
    literature on this conjecture (see the literature dossier, section 1).
    """

    source: Vertex
    demands: Mapping[Vertex, Rational]
    arcs: Sequence[Arc]
    name: str = ""
    _vertices: tuple[Vertex, ...] = field(init=False, default=())

    @classmethod
    def build(
        cls,
        source: Vertex,
        demands: Mapping[Vertex, object],
        arcs: Iterable[tuple[Vertex, Vertex, object, object]],
        name: str = "",
    ) -> "Instance":
        """Build from ``(tail, head, x, cost)`` tuples, coercing to exact rationals."""
        built = tuple(
            Arc(index=i, tail=t, head=h, x=_rat(x), cost=_rat(c))
            for i, (t, h, x, c) in enumerate(arcs)
        )
        return cls(
            source=source,
            demands={t: _rat(d) for t, d in demands.items()},
            arcs=built,
            name=name,
        )

    def __post_init__(self) -> None:
        seen: list[Vertex] = []
        for v in [self.source, *self.demands.keys()]:
            if v not in seen:
                seen.append(v)
        for a in self.arcs:
            for v in (a.tail, a.head):
                if v not in seen:
                    seen.append(v)
        self._vertices = tuple(seen)

    # -- basic accessors ------------------------------------------------------

    @property
    def vertices(self) -> tuple[Vertex, ...]:
        return self._vertices

    @property
    def terminals(self) -> tuple[Vertex, ...]:
        return tuple(self.demands.keys())

    @property
    def d_max(self) -> Rational:
        return max(self.demands.values())

    @property
    def total_demand(self) -> Rational:
        return sum(self.demands.values(), Fraction(0))

    def x_vector(self) -> dict[int, Rational]:
        return {a.index: a.x for a in self.arcs}

    def cost_of(self, load: Mapping[int, Rational]) -> Rational:
        """Exact cost of an arc-load vector."""
        return sum(
            (a.cost * load.get(a.index, Fraction(0)) for a in self.arcs), Fraction(0)
        )

    @property
    def fractional_cost(self) -> Rational:
        return self.cost_of(self.x_vector())

    def bound(self, arc: Arc, alpha: Rational = Fraction(1)) -> Rational:
        """The congestion bound ``x_a + alpha * d_max`` for this arc."""
        return arc.x + alpha * self.d_max

    # -- feasibility ----------------------------------------------------------

    def divergence(self, v: Vertex) -> Rational:
        out = sum((a.x for a in self.arcs if a.tail == v), Fraction(0))
        inn = sum((a.x for a in self.arcs if a.head == v), Fraction(0))
        return out - inn

    def check_feasible(self) -> None:
        """Raise ``InfeasibleFlow`` unless x is a nonnegative feasible fractional flow.

        Checks, in order: nonnegative demands with at least one terminal; the source is
        not a terminal; nonnegative costs; nonnegative arc loads; and flow conservation
        with the correct excess at the source, deficit at each terminal and balance
        everywhere else.
        """
        if not self.demands:
            raise InfeasibleFlow("no terminals")
        if self.source in self.demands:
            raise InfeasibleFlow("the source is also a terminal")
        for t, d in self.demands.items():
            if d < 0:
                raise InfeasibleFlow(f"negative demand at {t}: {d}")
        for a in self.arcs:
            if a.x < 0:
                raise InfeasibleFlow(f"negative flow on {a}: {a.x}")
            if a.cost < 0:
                raise InfeasibleFlow(f"negative cost on {a}: {a.cost}")

        for v in self.vertices:
            div = self.divergence(v)
            if v == self.source:
                expected = self.total_demand
            elif v in self.demands:
                expected = -self.demands[v]
            else:
                expected = Fraction(0)
            if div != expected:
                raise InfeasibleFlow(
                    f"conservation fails at {v}: divergence {div}, expected {expected}"
                )

    def is_feasible(self) -> bool:
        try:
            self.check_feasible()
        except InfeasibleFlow:
            return False
        return True

    # -- adjacency ------------------------------------------------------------

    def out_arcs(self, v: Vertex) -> tuple[Arc, ...]:
        return tuple(a for a in self.arcs if a.tail == v)

    def undirected_edges(self) -> tuple[tuple[Vertex, Vertex], ...]:
        """The underlying undirected edge multiset, for graph-class questions."""
        return tuple((a.tail, a.head) for a in self.arcs)
