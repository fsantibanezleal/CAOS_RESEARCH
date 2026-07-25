"""EXP-002: adjudicate the 2026 claimed counterexample to Goemans' cost conjecture.

Deterministic, headless, CPU only. Exact rational arithmetic. No floats, no randomness,
no network, and NO use of the proposer's verifier (archived at
E:\\_Datos\\caos-research\\unsplittable-flow-cost\\claimed-counterexample\\, never imported
or executed; see the independence rule in the counterexample dossier).

Run from the repository root with the repo .venv:

    .venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-002-adjudicate-2026-claim/run.py

Exits nonzero on any failed prediction (H1-H16 of hypothesis.md).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM_ROOT = HERE.parent.parent
sys.path.insert(0, str(PROBLEM_ROOT / "code"))

from ufclib import Instance, decide_instance, is_acyclic  # noqa: E402
from ufclib.decide import (  # noqa: E402
    alpha_for_routing,
    congestion_violations,
    two_sided_feasible,
)
from ufclib.enumerate_routings import (  # noqa: E402
    all_routings,
    path_label,
    paths_by_terminal,
    routing_load,
)
from ufclib.graphs import (  # noqa: E402
    demands_are_multiples_of_one_another,
    has_k4_subdivision,
    kuratowski_planarity_by_degrees,
    underlying_adjacency,
)

ARTIFACTS = HERE / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)
_LOG: list[str] = []


def say(line: str = "") -> None:
    print(line)
    _LOG.append(line)


def _flush() -> None:
    (ARTIFACTS / "run-log.txt").write_text("\n".join(_LOG) + "\n", encoding="utf-8")


def check(name: str, condition: bool, detail: str = "") -> None:
    say(f"  [{'PASS' if condition else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not condition:
        _flush()
        raise SystemExit(f"prediction failed: {name} {detail}")


# ---------------------------------------------------------------------------
# The instance, re-entered by hand from the counterexample dossier's table.
# Deliberately NOT parsed from the proposer's JSON: a shared parse would hide a
# transcription error in either direction.
# ---------------------------------------------------------------------------

CLAIM = Instance.build(
    source="s",
    demands={"t1": 15, "t2": 10, "t3": 15},
    arcs=[
        ("s", "t1", 10, 2),
        ("s", "t2", 6, 3),
        ("s", "u", 24, 0),
        ("u", "t3", 10, 2),
        ("u", "v", 14, 0),
        ("v", "t1", 5, 0),
        ("v", "w", 9, 0),
        ("w", "t2", 4, 0),
        ("w", "t3", 5, 0),
    ],
    name="the 2026 claimed counterexample (7 vertices, 9 arcs)",
)


def main() -> None:
    say("EXP-002: adjudication of the 2026 claimed counterexample")
    say("=" * 66)
    inst = CLAIM
    d_max = inst.d_max

    say("\n### H1, H13 feasibility, nonnegativity, acyclicity")
    inst.check_feasible()
    check("H1 x is a feasible fractional flow (conservation at all 7 vertices)", True)
    check("H13 all costs are nonnegative", all(a.cost >= 0 for a in inst.arcs))
    acyclic = is_acyclic(inst)
    check("H13 the digraph is acyclic", acyclic)
    say(f"  d_max = {d_max}")

    say("\n### H2 path enumeration by our own search")
    per_terminal = paths_by_terminal(inst)
    for t in inst.terminals:
        for p in per_terminal[t]:
            say(f"    {t}: {path_label(p, inst)}   cost of routing d_{t} here = "
                f"{sum((a.cost * inst.demands[t] for a in p), Fraction(0))}")
    counts = {t: len(per_terminal[t]) for t in inst.terminals}
    check("H2 exactly two simple paths per terminal", counts == {"t1": 2, "t2": 2, "t3": 2}, str(counts))
    routings = list(all_routings(inst))
    check("H2 exactly eight unsplittable routings", len(routings) == 8, str(len(routings)))

    say("\n### H3, H4 the decision")
    report = decide_instance(inst)
    check("H3 c^T x = 58", report.fractional_cost == 58, str(report.fractional_cost))

    say("  the complete routing table:")
    for r in report.routings:
        marks = []
        if r.congestion_good:
            marks.append("congestion-good")
        if r.cost_good:
            marks.append("cost-good")
        viol = ", ".join(
            f"{inst.arcs[i]} by {amount}" for i, amount in sorted(r.violations.items())
        )
        say(f"    cost={r.cost:>3} alpha={str(r.alpha):>6} "
            f"[{', '.join(marks) or 'neither'}] {r.label}"
            + (f"   violations: {viol}" if viol else ""))

    check(
        "H4 exactly four routings are congestion-good",
        report.congestion_good_count == 4,
        str(report.congestion_good_count),
    )
    check(
        "H4 the minimum cost among congestion-good routings is 60",
        report.min_cost_among_congestion_good == 60,
        str(report.min_cost_among_congestion_good),
    )
    check("H4 60 > 58, so no routing is both congestion-good and cost-good",
          report.min_cost_among_congestion_good > report.fractional_cost)
    check("H4 THE DECISION: the instance IS a counterexample to Conjecture 1.2",
          report.is_counterexample)

    say("\n### H5 the quantitative content: what violation the instance forces")
    check("H5 alpha_instance = 16/15", report.alpha_instance == Fraction(16, 15),
          str(report.alpha_instance))
    say(f"  every cost-good routing needs budget at least {report.alpha_instance} d_max "
        f"= {report.alpha_instance * d_max} units; the conjecture allows {d_max}")

    say("\n### H6 the DGG floor (the theorem as an oracle on our data)")
    check("H6 at least one congestion-good routing exists", report.congestion_good_count >= 1)

    say("\n### H7 test C1: Skutella 2002 (demands multiples of one another)")
    check("H7 the demands are NOT all multiples of one another",
          not demands_are_multiples_of_one_another(inst),
          f"demands {sorted(set(inst.demands.values()))}")

    say("\n### H8 test C2: MSW25 (series-parallel digraphs)")
    quad = has_k4_subdivision(inst)
    check("H8 the underlying graph contains a K4 subdivision", quad is not None, str(quad))
    check("H8 its branch vertices are {s, u, v, w}",
          quad is not None and set(quad) == {"s", "u", "v", "w"}, str(quad))

    say("\n### H9 planarity by Kuratowski degree counting")
    adj = underlying_adjacency(inst.vertices, inst.undirected_edges())
    degrees = {v: len(ns) for v, ns in adj.items()}
    say(f"  degrees: {degrees}")
    planar = kuratowski_planarity_by_degrees(inst)
    check("H9 the graph is planar (too few high-degree vertices for K5 or K3,3)",
          planar is True,
          f"deg>=4: {sum(1 for d in degrees.values() if d >= 4)}, "
          f"deg>=3: {sum(1 for d in degrees.values() if d >= 3)}")

    say("\n### H10 test C5: does the cost-free two-sided conjecture (Conj 1.3) survive?")
    witnesses_13 = [
        r for r, routing in zip(report.routings, routings)
        if two_sided_feasible(inst, routing_load(inst, routing))
    ]
    check("H10 some routing meets x - d_max <= y <= x + d_max",
          len(witnesses_13) >= 1, f"{len(witnesses_13)} witnesses")
    if witnesses_13:
        say(f"  witness: {witnesses_13[0].label}")

    say("\n### H11 test C4: does Conjecture 1.5 (cost-good at 2 d_max) survive?")
    two_budget = [r for r in report.routings if r.cost_good and r.alpha <= 2]
    check("H11 some cost-good routing has violation at most 2 d_max",
          len(two_budget) >= 1, f"{len(two_budget)} witnesses")
    if two_budget:
        best = min(two_budget, key=lambda r: r.alpha)
        say(f"  cheapest-violation cost-good routing: alpha = {best.alpha}, "
            f"cost = {best.cost}, {best.label}")

    say("\n### H12 test C3: not a source-plus-two-layers network")
    longest = max(len(p) for paths in per_terminal.values() for p in paths)
    check("H12 some s-t path uses at least 3 arcs", longest >= 3, f"longest path has {longest} arcs")

    # ---------------------------------------------------------------------
    # H14, H15: the INDEPENDENT structural route. Fresh code, no reuse of the
    # enumerated costs above beyond the final comparison.
    # ---------------------------------------------------------------------
    say("\n### H14 independent second route: the conflict graph")

    cheap: dict[str, tuple] = {}
    dear: dict[str, tuple] = {}
    for t in inst.terminals:
        by_cost = sorted(
            per_terminal[t],
            key=lambda p: sum((a.cost * inst.demands[t] for a in p), Fraction(0)),
        )
        cheap[t] = by_cost[0]
        dear[t] = by_cost[-1]

    def routing_cost_of(paths: dict[str, tuple]) -> Fraction:
        return sum(
            (a.cost * inst.demands[t] for t in inst.terminals for a in paths[t]),
            Fraction(0),
        )

    cheap_costs = {t: routing_cost_of({t: cheap[t], **{o: () for o in inst.terminals if o != t}}) for t in inst.terminals}
    dear_costs = {t: routing_cost_of({t: dear[t], **{o: () for o in inst.terminals if o != t}}) for t in inst.terminals}
    say(f"  per-terminal cheap costs: { {t: str(c) for t, c in cheap_costs.items()} }")
    say(f"  per-terminal expensive costs: { {t: str(c) for t, c in dear_costs.items()} }")

    def pair_conflicts(t_i: str, t_j: str) -> bool:
        """True when selecting both cheap choices violates a bound for EVERY completion."""
        others = [t for t in inst.terminals if t not in (t_i, t_j)]
        for completion in product(*(per_terminal[t] for t in others)):
            choice = {t_i: cheap[t_i], t_j: cheap[t_j]}
            choice.update(dict(zip(others, completion)))
            load = routing_load(inst, tuple(choice[t] for t in inst.terminals))
            if not congestion_violations(inst, load):
                return False
        return True

    conflict_edges = [
        (a, b) for a, b in combinations(inst.terminals, 2) if pair_conflicts(a, b)
    ]
    say(f"  conflict edges among the cheap choices: {conflict_edges}")
    check("H14 the conflict graph is a triangle on the three cheap choices",
          len(conflict_edges) == 3, str(len(conflict_edges)))

    # A triangle has independence number 1, so at most one cheap choice is selectable.
    independent_sets = [
        subset
        for size in range(len(inst.terminals) + 1)
        for subset in combinations(inst.terminals, size)
        if all(
            not (a in subset and b in subset) for a, b in conflict_edges
        )
    ]
    alpha_number = max(len(s) for s in independent_sets)
    check("H14 the independence number of the conflict graph is 1", alpha_number == 1,
          str(alpha_number))

    structural_bound = sum(sorted(dear_costs.values())[: len(inst.terminals) - alpha_number], Fraction(0))
    say(f"  structural lower bound on the cost of any congestion-good routing: "
        f"{structural_bound} (the {len(inst.terminals) - alpha_number} cheapest expensive paths)")
    check("H14 the structural bound equals the enumerated minimum (60)",
          structural_bound == report.min_cost_among_congestion_good == 60,
          f"structural {structural_bound} vs enumerated {report.min_cost_among_congestion_good}")
    check("H14 the structural route alone refutes the conjecture on this instance",
          structural_bound > report.fractional_cost)

    say("\n### H15 the invariant: fractional selection mass on the conflict triangle")
    rho = {}
    for t in inst.terminals:
        cheap_arcs = set(a.index for a in cheap[t])
        # the fractional flow's share of this terminal's demand carried on the cheap
        # choice, read off the arc that is private to that choice
        private = [
            a for a in inst.arcs
            if a.index in cheap_arcs and all(
                a.index not in set(b.index for b in p)
                for other in inst.terminals if other != t
                for p in per_terminal[other]
            )
        ]
        if not private:
            raise SystemExit(f"no private arc identifies the cheap choice of {t}")
        rho[t] = private[0].x / inst.demands[t]
        say(f"  rho[{t}] = x({private[0]}) / d = {private[0].x}/{inst.demands[t]} = {rho[t]}")
    total = sum(rho.values(), Fraction(0))
    check("H15 rho = (1/3, 2/5, 1/3)",
          sorted(rho.values()) == sorted([Fraction(1, 3), Fraction(2, 5), Fraction(1, 3)]),
          str({t: str(r) for t, r in rho.items()}))
    check("H15 the triangle stable-set inequality is violated with value 16/15",
          total == Fraction(16, 15), str(total))
    say(f"  the fractional flow buys {total} of cheap routing; any congestion-good "
        f"integral routing buys at most {alpha_number}")

    say("\n### H16 comparison with the publicly reported numbers (after our decision)")
    reported = {"routings": 8, "congestion_good": 4, "fractional_cost": 58, "min_good_cost": 60}
    ours = {
        "routings": len(report.routings),
        "congestion_good": report.congestion_good_count,
        "fractional_cost": report.fractional_cost,
        "min_good_cost": report.min_cost_among_congestion_good,
    }
    check("H16 our independently computed numbers agree with the reported ones",
          ours == reported, f"ours {ours}")

    say("\n" + "=" * 66)
    say("EXP-002: all predictions H1-H16 hold.")
    say("VERDICT: the 2026 claimed counterexample is VALID under our own exact")
    say("enumeration. Goemans' Conjecture 1.2 is FALSE. The instance is acyclic, so")
    say("Morell-Skutella Conjecture 1.4 and the convex-combination form fall with it.")
    say("Conjecture 1.3, Conjecture 1.5, the DGG theorem, the series-parallel theorem")
    say("and the planar theorem all survive, and the O(d_max) question is untouched.")
    _flush()


if __name__ == "__main__":
    main()
