"""EXP-004: the frontier value of an instance, and a search for a larger forced violation.

Deterministic, headless, CPU only, exact rational arithmetic. No floats, no randomness,
no network.

    .venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-004-frontier-value/run.py

Exits nonzero on any failed prediction (F1-F6 of hypothesis.md).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM_ROOT = HERE.parent.parent
sys.path.insert(0, str(PROBLEM_ROOT / "code"))

from ufclib import Instance, decide_instance  # noqa: E402
from ufclib.decide import alpha_for_routing  # noqa: E402
from ufclib.enumerate_routings import all_routings, routing_load  # noqa: E402
from ufclib.frontier import frontier_value, spine_family_instance  # noqa: E402

ARTIFACTS = HERE / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)
_LOG: list[str] = []


def say(line: str = "") -> None:
    print(line, flush=True)
    _LOG.append(line)


def _flush() -> None:
    (ARTIFACTS / "run-log.txt").write_text("\n".join(_LOG) + "\n", encoding="utf-8")


def check(name: str, condition: bool, detail: str = "") -> None:
    say(f"  [{'PASS' if condition else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not condition:
        _flush()
        raise SystemExit(f"prediction failed: {name} {detail}")


CLAIM = Instance.build(
    source="s",
    demands={"t1": 15, "t2": 10, "t3": 15},
    arcs=[
        ("s", "t1", 10, 2), ("s", "t2", 6, 3), ("s", "u", 24, 0),
        ("u", "t3", 10, 2), ("u", "v", 14, 0), ("v", "t1", 5, 0),
        ("v", "w", 9, 0), ("w", "t2", 4, 0), ("w", "t3", 5, 0),
    ],
    name="the 2026 counterexample",
)


def max_alpha_over_routings(inst: Instance) -> Fraction:
    """Free pre-filter: alpha_max can exceed 1 only if some routing does."""
    worst = Fraction(0)
    for routing in all_routings(inst):
        a = alpha_for_routing(inst, routing_load(inst, routing))
        if a > worst:
            worst = a
    return worst


def arc_signature(inst: Instance, rename: dict[str, str] | None = None) -> set:
    """Arc multiset, optionally under an explicit vertex relabelling.

    The family names its spine v1, v2, v3 while the published instance names the same
    vertices u, v, w. Comparing raw names would report a difference that is only a
    naming convention, so the relabelling is passed in explicitly rather than the
    comparison being loosened.
    """
    rename = rename or {}
    return {
        (rename.get(a.tail, a.tail), rename.get(a.head, a.head), a.x, a.cost)
        for a in inst.arcs
    }


def main() -> None:
    say("EXP-004: the frontier value, and a search for a larger forced violation")
    say("=" * 72)

    say("\n### F1 the family contains the 2026 counterexample")
    rebuilt = spine_family_instance(
        demands=(15, 10, 15),
        exits=(2, 3, 3),
        early_exits=(0, 0, 1),
        rhos=(Fraction(1, 3), Fraction(2, 5), Fraction(1, 3)),
        costs=(2, 3, 2),
        spine_length=3,
        name="family point reproducing the 2026 counterexample",
    )
    check("F1 the family point builds", rebuilt is not None)
    spine_names = {"v1": "u", "v2": "v", "v3": "w"}
    same = arc_signature(rebuilt, spine_names) == arc_signature(CLAIM)
    check("F1 it reproduces the instance arc for arc (spine v1,v2,v3 named u,v,w)", same,
          "" if same else f"family {sorted(map(str, arc_signature(rebuilt, spine_names)))}")
    rep = decide_instance(rebuilt)
    check("F1 same verdict, cost and alpha",
          rep.is_counterexample and rep.fractional_cost == 58
          and rep.alpha_instance == Fraction(16, 15),
          f"cost {rep.fractional_cost}, alpha {rep.alpha_instance}")

    say("\n### F2 the instrument on instances that obey the conjecture")
    half = Fraction(1, 2)
    validation = {
        "V1": Instance.build("s", {"t": 2}, [("s", "t", 1, 5), ("s", "a", 1, 0), ("a", "t", 1, 0)], "V1"),
        "V2": Instance.build("s", {"t": 2}, [("s", "t", 1, 0), ("s", "t", 1, 7)], "V2"),
        "V3": Instance.build("s", {"t": 1},
                             [("s", "a", half, 1), ("a", "t", half, 0),
                              ("s", "b", half, 3), ("b", "t", half, 0)], "V3"),
        "V4": Instance.build("s", {"t1": 1, "t2": 1},
                             [("s", "u", 2, 0), ("u", "t1", 1, 0), ("u", "t2", 1, 0),
                              ("u", "m", 0, 0), ("m", "t1", 0, 0)], "V4"),
        "V5": Instance.build("s", {"t": 2},
                             [("s", "t", 1, 5), ("s", "a", 1, 0), ("a", "t", 1, 0),
                              ("a", "p", 0, 0), ("p", "q", 0, 0), ("q", "p", 0, 0),
                              ("q", "t", 0, 0)], "V5"),
    }
    for tag, inst in validation.items():
        res = frontier_value(inst)
        say(f"  {tag}: alpha_max = {res.alpha_max} (routing alphas {[str(a) for a in res.routing_alphas]})")
        check(f"F2 {tag} alpha_max <= 1", res.alpha_max <= 1, str(res.alpha_max))

    say("\n### F3 the frontier value of the 2026 instance")
    t0 = time.time()
    res = frontier_value(CLAIM)
    say(f"  routing alphas: {[str(a) for a in res.routing_alphas]}")
    say(f"  ceiling (alpha of the cheapest routing): {res.ceiling}")
    say(f"  alpha_max = {res.alpha_max}   ({time.time() - t0:.1f} s)")
    say(f"  witness c: {[str(v) for v in res.witness_cost]}")
    check("F3 the instance is a counterexample under the frontier instrument",
          res.is_counterexample)
    check("F3 alpha_max = 16/15", res.alpha_max == Fraction(16, 15), str(res.alpha_max))
    check("F5 alpha_max <= the all-cheapest ceiling", res.alpha_max <= res.ceiling,
          f"{res.alpha_max} vs {res.ceiling}")

    # ---------------------------------------------------------------------
    # Added AFTER the hypothesis was committed, and recorded as such in the
    # verdict: the sweep's first attempt died when sympy's rational simplex
    # cycled on a degenerate family member ("Oscillating system led to invalid
    # solution"), exactly the single-point-of-failure risk EXP-003 flagged as
    # UFB-033. The LP layer was replaced by our own Bland-rule exact simplex.
    # This cross-check keeps the two solvers honest against each other on the
    # cases where sympy does succeed.
    # ---------------------------------------------------------------------
    say("\n### X1 cross-check: our exact simplex against sympy's, where sympy succeeds")
    from ufclib.separation import separation_lp  # sympy-backed
    from ufclib.simplex import max_min_margin

    agreed = 0
    for tag, inst in [("2026 instance", CLAIM), *validation.items()]:
        sym = separation_lp(inst)
        loads = [
            [routing_load(inst, r)[a.index] for a in inst.arcs]
            for r in all_routings(inst)
            if alpha_for_routing(inst, routing_load(inst, r)) <= 1
        ]
        ours, _ = max_min_margin(loads, [a.x for a in inst.arcs])
        say(f"  {tag}: sympy {sym.optimum}, ours {ours}")
        check(f"X1 {tag} the two solvers agree", sym.optimum == ours,
              f"{sym.optimum} vs {ours}")
        agreed += 1
    say(f"  {agreed} instances cross-validated between independent LP implementations")

    say("\n### F4 the sweep: can any family member force more?")
    structures_k3 = [
        ((2, 3, 3), (0, 0, 1)),
        ((2, 3, 3), (0, 1, 1)),
        ((2, 3, 3), (1, 0, 1)),
        ((1, 2, 3), (0, 0, 0)),
        ((1, 2, 3), (0, 1, 2)),
        ((2, 2, 3), (0, 0, 1)),
        ((3, 3, 3), (0, 1, 2)),
        ((1, 3, 3), (0, 0, 1)),
        ((2, 3, 3), (0, 0, 2)),
        ((1, 2, 2), (0, 0, 1)),
    ]
    demand_sets_k3 = [
        (15, 10, 15), (12, 8, 12), (10, 10, 10), (15, 10, 12),
        (9, 6, 9), (12, 10, 15), (8, 6, 8), (6, 4, 6), (14, 10, 14), (10, 8, 12),
    ]
    fractions = [Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2), Fraction(3, 5), Fraction(2, 3)]

    best = (Fraction(16, 15), "the 2026 counterexample (baseline)")
    found: list[str] = []
    tested = counterexamples = built = 0
    t0 = time.time()
    for (exits, early) in structures_k3:
        for demands in demand_sets_k3:
            for rhos in product(fractions, repeat=3):
                inst = spine_family_instance(demands, exits, early, rhos, (1, 1, 1), 3)
                if inst is None:
                    continue
                built += 1
                if not inst.is_feasible():
                    continue
                tested += 1
                if max_alpha_over_routings(inst) <= 1:
                    continue  # cannot force more than d_max, no LP needed
                res = frontier_value(inst)
                if res.alpha_max > 1:
                    counterexamples += 1
                    label = f"{inst.name} rho={[str(r) for r in rhos]}"
                    found.append(f"alpha_max={res.alpha_max}  {label}")
                    say(f"  counterexample: alpha_max = {res.alpha_max}  {label}")
                    if res.alpha_max > best[0]:
                        best = (res.alpha_max, label)
                        say(f"  NEW BEST alpha_max = {res.alpha_max}")
    say(f"  k=3 sweep: {built} parameter points built, {tested} feasible, "
        f"{counterexamples} counterexamples, {time.time() - t0:.1f} s")

    structures_k4 = [
        ((2, 3, 4, 4), (0, 0, 1, 2)),
        ((1, 2, 3, 4), (0, 0, 1, 2)),
        ((2, 3, 3, 4), (0, 1, 1, 2)),
        ((2, 2, 3, 4), (0, 0, 1, 1)),
    ]
    demand_sets_k4 = [
        (15, 10, 15, 10), (12, 8, 12, 8), (10, 10, 10, 10), (15, 10, 12, 8),
    ]
    fractions4 = [Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2), Fraction(3, 5)]
    t0 = time.time()
    built4 = tested4 = ce4 = 0
    for (exits, early) in structures_k4:
        for demands in demand_sets_k4:
            for rhos in product(fractions4, repeat=4):
                inst = spine_family_instance(demands, exits, early, rhos, (1, 1, 1, 1), 4)
                if inst is None:
                    continue
                built4 += 1
                if not inst.is_feasible():
                    continue
                tested4 += 1
                if max_alpha_over_routings(inst) <= 1:
                    continue
                res = frontier_value(inst)
                if res.alpha_max > 1:
                    ce4 += 1
                    label = f"{inst.name} rho={[str(r) for r in rhos]}"
                    found.append(f"alpha_max={res.alpha_max}  {label}")
                    say(f"  counterexample: alpha_max = {res.alpha_max}  {label}")
                    if res.alpha_max > best[0]:
                        best = (res.alpha_max, label)
                        say(f"  NEW BEST alpha_max = {res.alpha_max}")
    say(f"  k=4 sweep: {built4} parameter points built, {tested4} feasible, "
        f"{ce4} counterexamples, {time.time() - t0:.1f} s")

    say(f"\n  BEST frontier value found: {best[0]}")
    say(f"  achieved by: {best[1]}")
    beat = best[0] > Fraction(16, 15)
    say(f"  F4 (a family member beats 16/15): {'CONFIRMED' if beat else 'REFUTED (null result)'}")
    check("F5 nothing in the sweep reaches alpha_max >= 2", best[0] < 2, str(best[0]))

    say("\n### F6 honest scope")
    say("  Any maximum above is a lower bound on alpha* obtained over a BOUNDED BOX of ONE")
    say("  structural family. It is not an estimate of alpha*, and it says nothing about")
    say("  whether Goemans' conjecture holds with O(d_max) violation.")

    say("\n" + "=" * 72)
    say(f"EXP-004: predictions checked. F4 outcome: {'confirmed' if beat else 'refuted (null)'}.")
    _flush()


if __name__ == "__main__":
    main()
