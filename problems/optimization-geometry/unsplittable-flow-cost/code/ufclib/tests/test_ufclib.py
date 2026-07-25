"""Regression gate for the SSUF exact checker (EXP-001's predictions, kept in CI).

These tests are the permanent form of the EXP-001 calibration: any change to ufclib that
breaks a known answer fails here. They never write artifacts (methodology/04 hard rule).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ufclib import Instance, InfeasibleFlow, decide_instance, is_acyclic  # noqa: E402
from ufclib.decide import two_sided_feasible  # noqa: E402
from ufclib.enumerate_routings import paths_by_terminal, routing_load  # noqa: E402
from ufclib.graphs import (  # noqa: E402
    demands_are_multiples_of_one_another,
    has_k4_subdivision,
    kuratowski_planarity_by_degrees,
)


def v1() -> Instance:
    return Instance.build(
        source="s",
        demands={"t": 2},
        arcs=[("s", "t", 1, 5), ("s", "a", 1, 0), ("a", "t", 1, 0)],
        name="V1",
    )


def test_feasible_flow_accepted():
    v1().check_feasible()


def test_infeasible_flow_rejected():
    bad = Instance.build(
        source="s",
        demands={"t": 2},
        arcs=[("s", "t", 2, 5), ("s", "a", 1, 0), ("a", "t", 1, 0)],
    )
    with pytest.raises(InfeasibleFlow):
        bad.check_feasible()


def test_source_may_not_be_a_terminal():
    bad = Instance.build(source="s", demands={"s": 1}, arcs=[("s", "s", 1, 0)])
    with pytest.raises(InfeasibleFlow):
        bad.check_feasible()


def test_floats_are_refused():
    with pytest.raises(TypeError):
        Instance.build(source="s", demands={"t": 1.5}, arcs=[("s", "t", 1, 0)])


def test_parallel_arcs_give_distinct_paths():
    inst = Instance.build(
        source="s", demands={"t": 2}, arcs=[("s", "t", 1, 0), ("s", "t", 1, 7)]
    )
    assert len(paths_by_terminal(inst)["t"]) == 2


def test_enumeration_terminates_on_a_cyclic_digraph():
    inst = Instance.build(
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
    )
    assert len(paths_by_terminal(inst)["t"]) == 3
    assert not is_acyclic(inst)
    assert is_acyclic(v1())


def test_congestion_bound_is_inclusive():
    inst = Instance.build(
        source="s",
        demands={"t1": 1, "t2": 1},
        arcs=[
            ("s", "u", 2, 0),
            ("u", "t1", 1, 0),
            ("u", "t2", 1, 0),
            ("u", "m", 0, 0),
            ("m", "t1", 0, 0),
        ],
    )
    through_m = [r for r in decide_instance(inst).routings if "-> m ->" in r.label]
    assert len(through_m) == 1
    assert through_m[0].congestion_good
    assert through_m[0].alpha == Fraction(1)


def test_known_answers_on_v1():
    rep = decide_instance(v1())
    assert rep.path_counts == {"t": 2}
    assert rep.fractional_cost == Fraction(5)
    assert rep.good_routing_exists
    assert rep.min_cost_among_congestion_good == Fraction(0)
    assert rep.alpha_instance == Fraction(1, 2)


def test_exact_rationals_everywhere():
    rep = decide_instance(
        Instance.build(
            source="s",
            demands={"t": 1},
            arcs=[
                ("s", "a", Fraction(1, 2), 1),
                ("a", "t", Fraction(1, 2), 0),
                ("s", "b", Fraction(1, 2), 3),
                ("b", "t", Fraction(1, 2), 0),
            ],
        )
    )
    for r in rep.routings:
        assert isinstance(r.cost, Fraction)
        assert isinstance(r.alpha, Fraction)
        assert all(isinstance(v, Fraction) for v in r.load.values())


def test_two_sided_bounds_helper():
    inst = v1()
    rep = decide_instance(inst)
    loads = [r.load for r in rep.routings]
    # d_max = 2 dominates every arc value here, so both routings meet the two-sided
    # bounds; the helper must agree.
    assert all(two_sided_feasible(inst, load) for load in loads)


def test_k4_subdivision_detection():
    # K4 itself, as a digraph orientation: four mutually adjacent vertices.
    k4 = Instance.build(
        source="s",
        demands={"t": 1},
        arcs=[
            ("s", "b", 1, 0),
            ("b", "t", 1, 0),
            ("s", "c", 0, 0),
            ("b", "c", 0, 0),
            ("c", "t", 0, 0),
            ("s", "t", 0, 0),
        ],
    )
    assert has_k4_subdivision(k4) is not None

    # A path plus a parallel arc is series-parallel: no K4 subdivision.
    sp = Instance.build(
        source="s", demands={"t": 2}, arcs=[("s", "t", 1, 0), ("s", "t", 1, 7)]
    )
    assert has_k4_subdivision(sp) is None


def test_planarity_sufficient_test_is_honest():
    # V1 is far too small for either Kuratowski graph, so the test decides planar.
    assert kuratowski_planarity_by_degrees(v1()) is True


def test_demand_multiplicity_predicate():
    multiples = Instance.build(
        source="s",
        demands={"t1": 2, "t2": 4},
        arcs=[("s", "t1", 2, 0), ("s", "t2", 4, 0)],
    )
    assert demands_are_multiples_of_one_another(multiples)

    not_multiples = Instance.build(
        source="s",
        demands={"t1": 10, "t2": 15},
        arcs=[("s", "t1", 10, 0), ("s", "t2", 15, 0)],
    )
    assert not demands_are_multiples_of_one_another(not_multiples)


def test_separation_lp_on_a_conjecture_obeying_instance():
    from ufclib.separation import separation_lp

    result = separation_lp(v1())
    assert result.optimum <= 0
    assert not result.admits_counterexample


def test_separation_lp_finds_the_2026_counterexample():
    from ufclib.separation import separation_lp, with_costs

    claim = Instance.build(
        source="s",
        demands={"t1": 15, "t2": 10, "t3": 15},
        arcs=[
            ("s", "t1", 10, 2), ("s", "t2", 6, 3), ("s", "u", 24, 0),
            ("u", "t3", 10, 2), ("u", "v", 14, 0), ("v", "t1", 5, 0),
            ("v", "w", 9, 0), ("w", "t2", 4, 0), ("w", "t3", 5, 0),
        ],
    )
    result = separation_lp(claim)
    assert result.admits_counterexample
    assert result.optimum == Fraction(2, 7)
    # the witness must round-trip through the checker
    rep = decide_instance(with_costs(claim, result.witness_cost))
    assert rep.is_counterexample


def test_the_2026_instance_is_a_counterexample_under_its_published_costs():
    claim = Instance.build(
        source="s",
        demands={"t1": 15, "t2": 10, "t3": 15},
        arcs=[
            ("s", "t1", 10, 2), ("s", "t2", 6, 3), ("s", "u", 24, 0),
            ("u", "t3", 10, 2), ("u", "v", 14, 0), ("v", "t1", 5, 0),
            ("v", "w", 9, 0), ("w", "t2", 4, 0), ("w", "t3", 5, 0),
        ],
    )
    rep = decide_instance(claim)
    assert rep.fractional_cost == Fraction(58)
    assert len(rep.routings) == 8
    assert rep.congestion_good_count == 4
    assert rep.min_cost_among_congestion_good == Fraction(60)
    assert rep.is_counterexample
    assert rep.alpha_instance == Fraction(16, 15)


def test_routing_load_sums_demands():
    inst = v1()
    rep = decide_instance(inst)
    for r in rep.routings:
        # every routing delivers the full demand out of the source
        out_of_source = sum(
            r.load[a.index] for a in inst.arcs if a.tail == inst.source
        )
        assert out_of_source == inst.total_demand
