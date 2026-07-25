"""EXP-001: the exact SSUF instance checker, validated on hand-built instances.

Deterministic, headless, CPU only. No randomness, no floats, no network.
Run from the repository root with the repo .venv:

    .venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-001-exact-instance-checker/run.py

Exits nonzero on any failed prediction (P1-P8 of hypothesis.md).
"""

from __future__ import annotations

import io
import sys
import tokenize
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM_ROOT = HERE.parent.parent
sys.path.insert(0, str(PROBLEM_ROOT / "code"))

from ufclib import (  # noqa: E402
    Instance,
    InfeasibleFlow,
    decide_instance,
    is_acyclic,
)
from ufclib.enumerate_routings import paths_by_terminal  # noqa: E402

ARTIFACTS = HERE / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)
_LOG: list[str] = []


def say(line: str = "") -> None:
    print(line)
    _LOG.append(line)


def check(prediction: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    say(f"  [{status}] {prediction}" + (f"  ({detail})" if detail else ""))
    if not condition:
        _flush()
        raise SystemExit(f"prediction failed: {prediction} {detail}")


def _flush() -> None:
    (ARTIFACTS / "run-log.txt").write_text("\n".join(_LOG) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# The validation set. Answers were fixed by inspection in hypothesis.md BEFORE
# this file was written; they are repeated here as literals so a reader can
# compare them against the hypothesis table without leaving the code.
# ---------------------------------------------------------------------------


def v1_two_paths() -> Instance:
    return Instance.build(
        source="s",
        demands={"t": 2},
        arcs=[
            ("s", "t", 1, 5),
            ("s", "a", 1, 0),
            ("a", "t", 1, 0),
        ],
        name="V1 one terminal, direct expensive path versus free detour",
    )


def v2_parallel_arcs() -> Instance:
    return Instance.build(
        source="s",
        demands={"t": 2},
        arcs=[
            ("s", "t", 1, 0),
            ("s", "t", 1, 7),
        ],
        name="V2 parallel arcs (a checker keyed on vertex pairs sees only one path)",
    )


def v3_capacity_free() -> Instance:
    half = Fraction(1, 2)
    return Instance.build(
        source="s",
        demands={"t": 1},
        arcs=[
            ("s", "a", half, 1),
            ("a", "t", half, 0),
            ("s", "b", half, 3),
            ("b", "t", half, 0),
        ],
        name="V3 congestion never binds; rational fractional loads",
    )


def v4_tight_boundary() -> Instance:
    return Instance.build(
        source="s",
        demands={"t1": 1, "t2": 1},
        arcs=[
            ("s", "u", 2, 0),
            ("u", "t1", 1, 0),
            ("u", "t2", 1, 0),
            ("u", "m", 0, 0),
            ("m", "t1", 0, 0),
        ],
        name="V4 a routing that loads an arc to exactly x_a + d_max",
    )


def v5_with_cycle() -> Instance:
    return Instance.build(
        source="s",
        demands={"t": 2},
        arcs=[
            ("s", "t", 1, 5),
            ("s", "a", 1, 0),
            ("a", "t", 1, 0),
            ("a", "p", 0, 0),
            ("p", "q", 0, 0),
            ("q", "p", 0, 0),
            ("q", "t", 0, 0),
        ],
        name="V5 V1 plus a directed cycle: enumeration must still terminate",
    )


EXPECTED = {
    # name: (path counts per terminal, routings, good routing exists, min cost among
    #        congestion-good routings)
    "V1": ({"t": 2}, 2, True, Fraction(0)),
    "V2": ({"t": 2}, 2, True, Fraction(0)),
    "V3": ({"t": 2}, 2, True, Fraction(1)),
    "V4": ({"t1": 2, "t2": 1}, 2, True, Fraction(0)),
    "V5": ({"t": 3}, 3, True, Fraction(0)),
}


def report(tag: str, instance: Instance) -> None:
    say(f"\n### {tag}: {instance.name}")
    rep = decide_instance(instance)
    say(f"  d_max = {rep.d_max}   c^T x = {rep.fractional_cost}")
    say(f"  paths per terminal: {rep.path_counts}")
    for r in rep.routings:
        flags = []
        if r.congestion_good:
            flags.append("congestion-good")
        if r.cost_good:
            flags.append("cost-good")
        say(
            f"    cost={r.cost} alpha={r.alpha} [{', '.join(flags) or 'neither'}] "
            f"{r.label}"
        )
    say(
        f"  congestion-good routings: {rep.congestion_good_count}; "
        f"min cost among them: {rep.min_cost_among_congestion_good}; "
        f"alpha_instance: {rep.alpha_instance}"
    )

    exp_paths, exp_routings, exp_good, exp_min_cost = EXPECTED[tag]
    check(f"P1 {tag} path counts", rep.path_counts == exp_paths, f"{rep.path_counts}")
    check(
        f"P2 {tag} routing count",
        len(rep.routings) == exp_routings,
        f"{len(rep.routings)}",
    )
    check(
        f"P4 {tag} a congestion-good routing exists (DGG floor)",
        rep.congestion_good_count >= 1,
    )
    check(
        f"P5 {tag} a congestion-good AND cost-good routing exists",
        rep.good_routing_exists is exp_good,
    )
    check(
        f"P5 {tag} minimum congestion-good cost",
        rep.min_cost_among_congestion_good == exp_min_cost,
        f"{rep.min_cost_among_congestion_good}",
    )
    check(
        f"P8 {tag} every reported quantity is an exact Fraction",
        all(
            isinstance(q, Fraction)
            for r in rep.routings
            for q in (r.cost, r.alpha, *r.load.values())
        ),
    )


def main() -> None:
    say("EXP-001: exact SSUF instance checker (calibration)")
    say("=" * 62)

    instances = {
        "V1": v1_two_paths(),
        "V2": v2_parallel_arcs(),
        "V3": v3_capacity_free(),
        "V4": v4_tight_boundary(),
        "V5": v5_with_cycle(),
    }
    for tag, inst in instances.items():
        report(tag, inst)

    say("\n### P3 feasibility is actually checked (negative control)")
    corrupted = Instance.build(
        source="s",
        demands={"t": 2},
        arcs=[("s", "t", 2, 5), ("s", "a", 1, 0), ("a", "t", 1, 0)],
        name="V1 corrupted: source outflow 3 against total demand 2",
    )
    rejected = False
    try:
        corrupted.check_feasible()
    except InfeasibleFlow as exc:
        rejected = True
        say(f"  corrupted instance rejected: {exc}")
    check("P3 an infeasible flow is rejected", rejected)
    check(
        "P3 the valid instances are accepted",
        all(inst.is_feasible() for inst in instances.values()),
    )

    say("\n### P6 boundary inclusivity on V4")
    v4 = instances["V4"]
    through_m = [
        r for r in decide_instance(v4).routings if "-> m ->" in r.label
    ]
    check("P6 the through-m routing exists", len(through_m) == 1)
    tight = through_m[0]
    arc_um = next(a for a in v4.arcs if (a.tail, a.head) == ("u", "m"))
    check(
        "P6 it loads u->m to exactly x + d_max and is congestion-good",
        tight.load[arc_um.index] == arc_um.x + v4.d_max and tight.congestion_good,
        f"load {tight.load[arc_um.index]} vs bound {arc_um.x + v4.d_max}",
    )

    say("\n### P7 cycles: termination and acyclicity detection")
    check(
        "P7 V5 path count equals 3 and enumeration terminated",
        len(paths_by_terminal(instances["V5"])["t"]) == 3,
    )
    check(
        "P7 acyclicity: True on V1-V4, False on V5",
        all(is_acyclic(instances[t]) for t in ("V1", "V2", "V3", "V4"))
        and not is_acyclic(instances["V5"]),
    )

    say("\n### P8 exactness: floats are refused at the door and absent from the code")
    refused = False
    try:
        # float-literal-ok: this is the negative control; feeding a float is the point.
        Instance.build(source="s", demands={"t": 1.0}, arcs=[("s", "t", 1, 0)])
    except TypeError:
        refused = True
    check("P8 a float demand is refused by the constructor", refused)

    float_literals: list[str] = []
    sources = sorted((PROBLEM_ROOT / "code" / "ufclib").glob("*.py")) + [Path(__file__)]
    for path in sources:
        text = path.read_text(encoding="utf-8")
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.NUMBER and (
                "." in tok.string or "e" in tok.string.lower()
            ):
                float_literals.append(f"{path.name}:{tok.start[0]} {tok.string}")
    check(
        "P8 no float literals in ufclib or in this experiment",
        not float_literals,
        "; ".join(float_literals),
    )

    say("\n" + "=" * 62)
    say("EXP-001: all predictions P1-P8 hold. Checker adopted as ground truth.")
    _flush()


if __name__ == "__main__":
    main()
