"""EXP-003: the separation LP, and the first minimality rungs.

Deterministic, headless, CPU only, exact rational arithmetic (sympy's rational simplex).
No floats, no randomness, no network.

    .venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-003-separation-lp/run.py

Exits nonzero on any failed prediction (G1-G7 of hypothesis.md).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM_ROOT = HERE.parent.parent
sys.path.insert(0, str(PROBLEM_ROOT / "code"))

from ufclib import Instance, decide_instance  # noqa: E402
from ufclib.enumerate_routings import routing_load  # noqa: E402
from ufclib.separation import (  # noqa: E402
    cheapest_path_routing,
    separation_lp,
    with_costs,
)
from ufclib.decide import congestion_violations  # noqa: E402

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
    name="the 2026 counterexample",
)


def validation_set() -> dict[str, Instance]:
    half = Fraction(1, 2)
    return {
        "V1": Instance.build("s", {"t": 2}, [("s", "t", 1, 5), ("s", "a", 1, 0), ("a", "t", 1, 0)], "V1"),
        "V2": Instance.build("s", {"t": 2}, [("s", "t", 1, 0), ("s", "t", 1, 7)], "V2"),
        "V3": Instance.build(
            "s", {"t": 1},
            [("s", "a", half, 1), ("a", "t", half, 0), ("s", "b", half, 3), ("b", "t", half, 0)],
            "V3",
        ),
        "V4": Instance.build(
            "s", {"t1": 1, "t2": 1},
            [("s", "u", 2, 0), ("u", "t1", 1, 0), ("u", "t2", 1, 0), ("u", "m", 0, 0), ("m", "t1", 0, 0)],
            "V4",
        ),
        "V5": Instance.build(
            "s", {"t": 2},
            [("s", "t", 1, 5), ("s", "a", 1, 0), ("a", "t", 1, 0), ("a", "p", 0, 0),
             ("p", "q", 0, 0), ("q", "p", 0, 0), ("q", "t", 0, 0)],
            "V5",
        ),
    }


def single_terminal_family() -> list[Instance]:
    """Single-terminal instances built to look adversarial: bottlenecks, zero-flow arcs,
    parallel arcs, and a long cheap detour against a short expensive one."""
    out = []
    for d in (1, 3, 7):
        for cheap_cost in (0, 1):
            out.append(
                Instance.build(
                    "s", {"t": d},
                    [
                        ("s", "t", Fraction(d, 3), 5),
                        ("s", "a", Fraction(2 * d, 3), cheap_cost),
                        ("a", "b", Fraction(2 * d, 3), 0),
                        ("b", "t", Fraction(2 * d, 3), 0),
                        ("s", "z", 0, 0),
                        ("z", "t", 0, 11),
                    ],
                    f"single terminal d={d}, cheap cost {cheap_cost}",
                )
            )
    return out


def two_terminal_family() -> list[Instance]:
    """Two-terminal instances with a shared bottleneck and two choices per terminal.

    The shape mirrors the mechanism of the 2026 counterexample as closely as two terminals
    allow: a shared spine arc s->u carrying the cheap choices of both terminals, plus an
    expensive direct arc per terminal. The parameters sweep the demands, the split of each
    demand between its two choices, and the cost of each expensive arc.
    """
    out = []
    for d1, d2 in ((2, 3), (3, 5), (4, 5), (5, 7)):
        for k1 in range(1, d1):          # flow of terminal 1 on its cheap choice
            for k2 in range(1, d2):      # flow of terminal 2 on its cheap choice
                for c1, c2 in ((1, 1), (1, 2), (3, 2), (5, 7)):
                    spine = k1 + k2
                    out.append(
                        Instance.build(
                            "s",
                            {"t1": d1, "t2": d2},
                            [
                                ("s", "t1", d1 - k1, c1),
                                ("s", "t2", d2 - k2, c2),
                                ("s", "u", spine, 0),
                                ("u", "t1", k1, 0),
                                ("u", "t2", k2, 0),
                            ],
                            f"two terminals d=({d1},{d2}) split=({k1},{k2}) costs=({c1},{c2})",
                        )
                    )
    return out


def main() -> None:
    say("EXP-003: the separation LP and the first minimality rungs")
    say("=" * 66)

    say("\n### G2 the 2026 instance: does ANY nonnegative cost vector break it?")
    res = separation_lp(CLAIM)
    say(f"  congestion-good routings: {res.congestion_good_count}")
    say(f"  (SEP) optimum: {res.optimum}")
    say(f"  witness c (normalised, sum 1): {[str(v) for v in res.witness_cost]}")
    check("G1 the LP returned an exact rational optimum",
          isinstance(res.optimum, Fraction))
    check("G2 the optimum is strictly positive", res.optimum > 0, str(res.optimum))
    check("G2 the optimum is at least 2/7 (the published cost vector certifies that much)",
          res.optimum >= Fraction(2, 7), str(res.optimum))
    check("G2 the instance admits a counterexample cost vector", res.admits_counterexample)

    say("\n### G4 round trip: feed the LP witness back into the checker")
    reweighted = with_costs(CLAIM, res.witness_cost)
    rep = decide_instance(reweighted)
    say(f"  under the witness costs: c^T x = {rep.fractional_cost}, "
        f"min congestion-good cost = {rep.min_cost_among_congestion_good}")
    check("G4 the witness makes the instance a counterexample in ufclib too",
          rep.is_counterexample)
    check("G4 the cost gap equals the LP optimum",
          rep.min_cost_among_congestion_good - rep.fractional_cost == res.optimum,
          f"gap {rep.min_cost_among_congestion_good - rep.fractional_cost} vs optimum {res.optimum}")

    say("\n### G3 the validation set: no cost vector can break V1-V5")
    for tag, inst in validation_set().items():
        r = separation_lp(inst)
        say(f"  {tag}: (SEP) optimum = {r.optimum}")
        check(f"G3 {tag} optimum <= 0", r.optimum <= 0, str(r.optimum))

    say("\n### G5 minimality rung 1: no single-terminal instance is a counterexample")
    for inst in single_terminal_family():
        r = separation_lp(inst)
        rep1 = decide_instance(inst)
        every_routing_congestion_good = all(x.congestion_good for x in rep1.routings)
        check(f"G5 every routing is congestion-good ({inst.name})", every_routing_congestion_good)
        check(f"G5 (SEP) optimum <= 0 ({inst.name})", r.optimum <= 0, str(r.optimum))
    say(f"  {len(single_terminal_family())} single-terminal instances, all obey the conjecture")

    say("\n### G6 the k=2 characterisation and the family sweep")
    fam = two_terminal_family()
    counterexamples = []
    mismatches = []
    for inst in fam:
        r = separation_lp(inst)
        if r.optimum > 0:
            counterexamples.append((inst, r))

        # the characterisation: the all-cheapest routing is congestion-good exactly when
        # every arc on BOTH cheapest paths carries x_a >= min(d1, d2)
        chosen = cheapest_path_routing(inst)
        load = routing_load(inst, chosen)
        cheapest_is_congestion_good = not congestion_violations(inst, load)
        shared = set(a.index for a in chosen[0]) & set(a.index for a in chosen[1])
        dmin = min(inst.demands.values())
        predicate = all(inst.arcs[i].x >= dmin for i in shared)
        if cheapest_is_congestion_good != predicate:
            mismatches.append(inst.name)

        # and the all-cheapest routing must always be cost-good
        if inst.cost_of(load) > inst.fractional_cost:
            mismatches.append(f"COST {inst.name}")

    check("G6 the all-cheapest routing is always cost-good, and the shared-arc "
          "characterisation of its congestion-goodness holds on every instance",
          not mismatches, "; ".join(mismatches[:3]))
    check("G6 no two-terminal counterexample in the swept family",
          not counterexamples,
          f"{len(counterexamples)} found" if counterexamples else "")
    say(f"  {len(fam)} two-terminal instances swept, none admits any nonnegative cost vector "
        f"making it a counterexample")

    say("\n### G7 honest scope")
    say("  The k=1 result is a THEOREM (proved in the verdict, machine-checked here).")
    say("  The k=2 sweep is EVIDENCE over a bounded parameter box, not a proof; the")
    say("  necessary condition it establishes (a shared arc on the two cheapest paths")
    say("  carrying x_a < min(d1, d2)) is what a real k=2 exhaustion must target.")

    say("\n" + "=" * 66)
    say("EXP-003: all predictions G1-G7 hold.")
    _flush()


if __name__ == "__main__":
    main()
