"""The separation LP: does ANY nonnegative cost vector make this instance a counterexample?

Derivation (EXP-003 hypothesis, our own words). Let U(x) be the set of load vectors of
congestion-good routings: finite, nonempty by the Dinitz-Garg-Goemans theorem, and
INDEPENDENT of the costs, which is what makes the reduction work. The instance admits a
counterexample cost vector exactly when some c >= 0, c != 0, has c^T y > c^T x for every
y in U(x). That condition is invariant under positive scaling, so normalise sum_a c_a = 1:

    max delta  s.t.  c^T (y - x) >= delta for all y in U(x),  sum_a c_a = 1,  c >= 0.

The instance admits a counterexample cost vector if and only if this optimum is > 0.

Solved with sympy's rational simplex, so the optimum and the witness are exact rationals.
No floating point is involved at any stage.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

from sympy import Rational, nsimplify
from sympy.solvers.simplex import linprog

from .decide import congestion_violations
from .enumerate_routings import all_routings, routing_load
from .instance import Instance


def _to_fraction(value) -> Fraction:
    """sympy Rational -> Fraction, refusing anything inexact."""
    r = nsimplify(value, rational=True)
    return Fraction(int(r.p), int(r.q))


@dataclass(frozen=True)
class SeparationResult:
    """The outcome of (SEP) for one instance."""

    optimum: Fraction
    witness_cost: tuple[Fraction, ...]
    congestion_good_count: int

    @property
    def admits_counterexample(self) -> bool:
        return self.optimum > 0


def separation_lp(instance: Instance) -> SeparationResult:
    """Solve (SEP) exactly. Raises if no congestion-good routing exists (impossible by DGG).

    Variables are ordered (delta, c_0, ..., c_{m-1}). sympy's ``linprog`` minimises subject
    to ``A z <= b`` and ``A_eq z = b_eq`` with all variables nonnegative, so delta is split
    into a difference of two nonnegative parts to allow the negative optima that instances
    obeying the conjecture will produce.
    """
    instance.check_feasible()
    arcs = list(instance.arcs)
    m = len(arcs)
    x = [Rational(a.x.numerator, a.x.denominator) for a in arcs]

    loads = []
    for routing in all_routings(instance):
        load = routing_load(instance, routing)
        if congestion_violations(instance, load):
            continue
        loads.append([Rational(load[a.index].numerator, load[a.index].denominator) for a in arcs])
    if not loads:
        raise ValueError(
            "no congestion-good routing exists, which contradicts the DGG theorem: "
            "the instance data or the enumeration is wrong"
        )

    # variables z = (delta_plus, delta_minus, c_0 .. c_{m-1}), all >= 0
    n = 2 + m
    objective = [Rational(-1), Rational(1)] + [Rational(0)] * m  # minimise -(d+ - d-)

    A, b = [], []
    for y in loads:
        # delta - c^T (y - x) <= 0
        row = [Rational(1), Rational(-1)] + [-(y[j] - x[j]) for j in range(m)]
        A.append(row)
        b.append(Rational(0))

    A_eq = [[Rational(0), Rational(0)] + [Rational(1)] * m]
    b_eq = [Rational(1)]

    value, solution = linprog(objective, A, b, A_eq, b_eq)
    optimum = -value  # we minimised the negative
    costs = tuple(_to_fraction(v) for v in solution[2:])
    return SeparationResult(
        optimum=_to_fraction(optimum),
        witness_cost=costs,
        congestion_good_count=len(loads),
    )


def with_costs(instance: Instance, costs: tuple[Fraction, ...]) -> Instance:
    """A copy of the instance carrying a different cost vector (for round-trip checks)."""
    return Instance.build(
        source=instance.source,
        demands=dict(instance.demands),
        arcs=[(a.tail, a.head, a.x, costs[i]) for i, a in enumerate(instance.arcs)],
        name=f"{instance.name} [reweighted]",
    )


def cheapest_path_routing(instance: Instance) -> Optional[tuple]:
    """One cheapest path per terminal, by exact cost of carrying that terminal's demand.

    Always cost-good (proved in the EXP-003 verdict); congestion-goodness is the question.
    """
    from .enumerate_routings import paths_by_terminal

    per_terminal = paths_by_terminal(instance)
    chosen = []
    for t in instance.terminals:
        if not per_terminal[t]:
            return None
        best = min(
            per_terminal[t],
            key=lambda p: sum((a.cost * instance.demands[t] for a in p), Fraction(0)),
        )
        chosen.append(best)
    return tuple(chosen)
