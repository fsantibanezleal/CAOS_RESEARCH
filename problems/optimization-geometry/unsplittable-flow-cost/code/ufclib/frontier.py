"""The frontier value of an instance: how much violation it can force.

For a fixed (G, d, x), each routing y consumes a budget
alpha(y) = max_a (y_a - x_a)^+ / d_max. Given costs c, the best a cost-preserving
rounding can do is alpha_inst(c) = min{alpha(y) : c^T y <= c^T x}. The FRONTIER
VALUE is that maximised over prices:

    alpha_max(G, d, x) = max_{c >= 0} alpha_inst(c).

Since there are finitely many routings, alpha_max is the largest threshold A such
that some c >= 0 makes every routing BELOW A strictly more expensive than x, which
is the EXP-003 separation LP with its constraint set restricted to those routings.
An instance is a counterexample to Goemans' conjecture exactly when alpha_max > 1,
so the separation LP is the special case of this at the threshold just above 1.

Ceiling: routing every terminal on a cheapest path is always cost-good, so
alpha_max never exceeds that routing's own alpha.

All arithmetic exact (Fraction in, Fraction out), on our own Bland-rule simplex
(``ufclib.simplex``): sympy's rational simplex cycles on degenerate members of the
spine family, which EXP-004 hit in practice.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

from .decide import alpha_for_routing
from .enumerate_routings import all_routings, routing_load
from .instance import Instance
from .simplex import max_min_margin


@dataclass(frozen=True)
class FrontierResult:
    alpha_max: Fraction
    witness_cost: tuple[Fraction, ...]
    routing_alphas: tuple[Fraction, ...]
    ceiling: Fraction

    @property
    def is_counterexample(self) -> bool:
        return self.alpha_max > 1


def _separation_over(instance: Instance, loads) -> tuple[Fraction, tuple[Fraction, ...]]:
    """max delta s.t. c^T(y - x) >= delta for the given loads, sum c = 1, c >= 0.

    Uses our own exact simplex with Bland's rule (``ufclib.simplex``) rather than
    sympy's, which cycles on degenerate members of the spine family (EXP-004).
    """
    x = [a.x for a in instance.arcs]
    return max_min_margin(loads, x)


def frontier_value(instance: Instance) -> FrontierResult:
    """Compute alpha_max exactly, with a witnessing cost vector."""
    instance.check_feasible()
    arcs = list(instance.arcs)

    rows = []
    for routing in all_routings(instance):
        load = routing_load(instance, routing)
        rows.append(
            (
                alpha_for_routing(instance, load),
                [load[a.index] for a in arcs],
                sum((a.cost * load[a.index] for a in arcs), Fraction(0)),
            )
        )
    if not rows:
        raise ValueError("no routing exists; the instance cannot be feasible")

    alphas = sorted({r[0] for r in rows})
    ceiling = min(rows, key=lambda r: r[2])[0]  # alpha of a cheapest routing

    best_alpha = alphas[0]
    best_cost: tuple[Fraction, ...] = tuple(Fraction(0) for _ in arcs)
    for candidate in alphas:
        below = [r[1] for r in rows if r[0] < candidate]
        optimum, witness = _separation_over(instance, below)
        if optimum > 0:
            best_alpha, best_cost = candidate, witness

    return FrontierResult(
        alpha_max=best_alpha,
        witness_cost=best_cost,
        routing_alphas=tuple(sorted(r[0] for r in rows)),
        ceiling=ceiling,
    )


# ---------------------------------------------------------------------------
# The spine family. The 2026 counterexample is the parameter point
# k = 3, m = 3, d = (15, 10, 15), e = (2, 3, 3), f = (0, 0, 1),
# rho = (1/3, 2/5, 1/3), costs = (2, 3, 2).
# ---------------------------------------------------------------------------


def spine_family_instance(
    demands: tuple[int, ...],
    exits: tuple[int, ...],
    early_exits: tuple[int, ...],
    rhos: tuple[Fraction, ...],
    costs: tuple[int, ...],
    spine_length: int,
    name: str = "",
) -> Optional[Instance]:
    """Build one member, or None if the parameters are inconsistent.

    Each terminal i sends rho_i * d_i along the spine to v_{exits[i]} then to t_i
    (free), and (1 - rho_i) * d_i to v_{early_exits[i]} then to t_i (cost c_i).
    Requires early_exits[i] < exits[i] <= spine_length and rho_i in (0, 1) with
    rho_i * d_i an integer.
    """
    k = len(demands)
    if not (len(exits) == len(early_exits) == len(rhos) == len(costs) == k):
        return None
    if any(not (0 <= f < e <= spine_length) for f, e in zip(early_exits, exits)):
        return None
    cheap = []
    for d, rho in zip(demands, rhos):
        value = Fraction(d) * rho
        if value.denominator != 1 or value <= 0 or value >= d:
            return None
        cheap.append(int(value))

    spine = [f"v{r}" for r in range(spine_length + 1)]
    spine[0] = "s"
    arcs = []
    for r in range(1, spine_length + 1):
        load = sum(cheap[i] for i in range(k) if exits[i] >= r) + sum(
            demands[i] - cheap[i] for i in range(k) if early_exits[i] >= r
        )
        if load <= 0:
            return None
        arcs.append((spine[r - 1], spine[r], load, 0))
    for i in range(k):
        arcs.append((spine[exits[i]], f"t{i + 1}", cheap[i], 0))
        arcs.append((spine[early_exits[i]], f"t{i + 1}", demands[i] - cheap[i], costs[i]))

    return Instance.build(
        source="s",
        demands={f"t{i + 1}": demands[i] for i in range(k)},
        arcs=arcs,
        name=name or f"spine k={k} m={spine_length} d={demands} e={exits} f={early_exits}",
    )
