"""The exact decision layer: is there a congestion-good AND cost-good routing?

Congestion-good at budget ``alpha``: ``y_a <= x_a + alpha * d_max`` on every arc, with the
inequality INCLUSIVE (the conjecture states it that way; an exclusive reading would
misclassify tight instances).
Cost-good: ``c^T y <= c^T x``, also inclusive.

The programme's central quantities are computed here:

``alpha_for_routing``  the smallest budget at which a given routing is congestion-good.
``InstanceReport.alpha_instance``  the smallest budget at which SOME cost-good routing is
congestion-good, i.e. the violation this instance forces on any cost-preserving rounding.
An instance is a counterexample to Goemans' conjecture exactly when that value exceeds 1.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Optional

from .enumerate_routings import (
    Routing,
    all_routings,
    paths_by_terminal,
    routing_label,
    routing_load,
)
from .instance import Instance


def congestion_violations(
    instance: Instance, load: Mapping[int, Fraction], alpha: Fraction = Fraction(1)
) -> dict[int, Fraction]:
    """Arc index -> amount by which the load exceeds ``x_a + alpha * d_max``.

    Only strictly positive excesses appear, so an empty dict means congestion-good.
    """
    out: dict[int, Fraction] = {}
    for arc in instance.arcs:
        excess = load[arc.index] - instance.bound(arc, alpha)
        if excess > 0:
            out[arc.index] = excess
    return out


def alpha_for_routing(instance: Instance, load: Mapping[int, Fraction]) -> Fraction:
    """The smallest ``alpha`` making this routing congestion-good, exactly.

    That is ``max_a (y_a - x_a) / d_max``, floored at 0: the budget, in units of the
    maximum demand, that this routing consumes.
    """
    worst = Fraction(0)
    for arc in instance.arcs:
        need = (load[arc.index] - arc.x) / instance.d_max
        if need > worst:
            worst = need
    return worst


@dataclass(frozen=True)
class RoutingReport:
    label: str
    load: dict[int, Fraction]
    cost: Fraction
    alpha: Fraction
    congestion_good: bool
    cost_good: bool
    violations: dict[int, Fraction]


@dataclass(frozen=True)
class InstanceReport:
    instance_name: str
    fractional_cost: Fraction
    d_max: Fraction
    path_counts: dict[str, int]
    routings: tuple[RoutingReport, ...]
    good_routing_exists: bool
    congestion_good_count: int
    min_cost_among_congestion_good: Optional[Fraction]
    alpha_instance: Optional[Fraction]

    @property
    def is_counterexample(self) -> bool:
        """True exactly when no routing is both congestion-good and cost-good.

        Note the deliberate asymmetry with ``good_routing_exists``: an instance with NO
        routing at all (a terminal unreachable from the source) is not a counterexample to
        the conjecture, because the conjecture assumes a feasible fractional flow, which
        forces reachability. ``decide_instance`` checks feasibility first, so that case
        cannot arise here.
        """
        return not self.good_routing_exists


def decide_instance(instance: Instance, alpha: Fraction = Fraction(1)) -> InstanceReport:
    """Enumerate every routing and decide the instance exactly.

    Raises ``InfeasibleFlow`` if the supplied fractional flow is not feasible: the
    conjecture says nothing about instances that do not satisfy its hypothesis, so an
    infeasible instance must never be reported as a counterexample.
    """
    instance.check_feasible()

    per_terminal = paths_by_terminal(instance)
    path_counts = {t: len(per_terminal[t]) for t in instance.terminals}
    fractional_cost = instance.fractional_cost

    reports: list[RoutingReport] = []
    good_exists = False
    congestion_good_count = 0
    min_cost_good: Optional[Fraction] = None
    alpha_instance: Optional[Fraction] = None

    for routing in all_routings(instance):
        load = routing_load(instance, routing)
        cost = instance.cost_of(load)
        violations = congestion_violations(instance, load, alpha)
        congestion_good = not violations
        cost_good = cost <= fractional_cost
        routing_alpha = alpha_for_routing(instance, load)

        if congestion_good:
            congestion_good_count += 1
            if min_cost_good is None or cost < min_cost_good:
                min_cost_good = cost
        if cost_good:
            if alpha_instance is None or routing_alpha < alpha_instance:
                alpha_instance = routing_alpha
        if congestion_good and cost_good:
            good_exists = True

        reports.append(
            RoutingReport(
                label=routing_label(routing, instance),
                load=load,
                cost=cost,
                alpha=routing_alpha,
                congestion_good=congestion_good,
                cost_good=cost_good,
                violations=violations,
            )
        )

    return InstanceReport(
        instance_name=instance.name,
        fractional_cost=fractional_cost,
        d_max=instance.d_max,
        path_counts=path_counts,
        routings=tuple(reports),
        good_routing_exists=good_exists,
        congestion_good_count=congestion_good_count,
        min_cost_among_congestion_good=min_cost_good,
        alpha_instance=alpha_instance,
    )


def two_sided_feasible(
    instance: Instance, load: Mapping[int, Fraction], alpha: Fraction = Fraction(1)
) -> bool:
    """The Morell-Skutella two-sided bounds ``x - alpha d_max <= y <= x + alpha d_max``.

    Used to test whether an instance also touches Conjecture 1.3 or Conjecture 1.5, which a
    refutation of Goemans' conjecture does NOT automatically kill.
    """
    slack = alpha * instance.d_max
    for arc in instance.arcs:
        y = load[arc.index]
        if y > arc.x + slack or y < arc.x - slack:
            return False
    return True
