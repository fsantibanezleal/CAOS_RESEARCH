"""Gate for the cutting-plane frontier evaluator and the odd-cycle instance family (UFB-065).

Exact arithmetic throughout; these tests never write artifacts (methodology/04 hard rule).
The oracle is checked against a brute-force minimum over ``all_routings``; the evaluator is
checked against the exact ``frontier_value`` wherever that one can run, and on Afrasyab's C5
instance (59,049 routings, where only the cutting plane can) against the recorded 79/120.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ufclib import Instance  # noqa: E402
from ufclib.cutting_plane import (  # noqa: E402
    cheapest_routing_below,
    frontier_value_cp,
    level_positive,
)
from ufclib.decide import alpha_for_routing  # noqa: E402
from ufclib.enumerate_routings import (  # noqa: E402
    all_routings,
    paths_by_terminal,
    routing_load,
)
from ufclib.frontier import frontier_value, spine_family_instance  # noqa: E402
from ufclib.graphs import is_acyclic  # noqa: E402
from ufclib.odd_cycle import afrasyab_uniform, odd_cycle_instance  # noqa: E402

F = Fraction


def v1() -> Instance:
    return Instance.build(
        source="s",
        demands={"t": 2},
        arcs=[("s", "t", 1, 5), ("s", "a", 1, 0), ("a", "t", 1, 0)],
        name="V1",
    )


def claim_2026() -> Instance:
    return Instance.build(
        source="s",
        demands={"t1": 15, "t2": 10, "t3": 15},
        arcs=[
            ("s", "t1", 10, 2), ("s", "t2", 6, 3), ("s", "u", 24, 0),
            ("u", "t3", 10, 2), ("u", "v", 14, 0), ("v", "t1", 5, 0),
            ("v", "w", 9, 0), ("w", "t2", 4, 0), ("w", "t3", 5, 0),
        ],
        name="2026",
    )


def parallel_instance() -> Instance:
    """Two parallel s-a arcs (distinct paths) feeding two terminals."""
    return Instance.build(
        source="s",
        demands={"t1": 2, "t2": 1},
        arcs=[
            ("s", "a", F(1, 2), 1),
            ("s", "a", F(5, 2), 0),
            ("a", "t1", 2, 1),
            ("a", "t2", 1, 0),
        ],
        name="parallel",
    )


def spine_members() -> list[Instance]:
    specs = [
        dict(demands=(15, 10, 15), exits=(2, 3, 3), early_exits=(0, 0, 1),
             rhos=(F(1, 3), F(2, 5), F(1, 3)), costs=(2, 3, 2), spine_length=3),
        dict(demands=(4, 6), exits=(2, 3), early_exits=(0, 1),
             rhos=(F(1, 2), F(1, 3)), costs=(1, 2), spine_length=3),
        dict(demands=(6, 6, 4), exits=(3, 2, 3), early_exits=(0, 1, 0),
             rhos=(F(1, 2), F(1, 3), F(1, 2)), costs=(1, 2, 3), spine_length=3),
        dict(demands=(10, 10), exits=(2, 2), early_exits=(0, 1),
             rhos=(F(1, 2), F(2, 5)), costs=(3, 1), spine_length=2),
    ]
    out = []
    for s in specs:
        inst = spine_family_instance(**s)
        assert inst is not None, s
        out.append(inst)
    return out


def small_instances() -> list[Instance]:
    return [
        v1(),
        claim_2026(),
        parallel_instance(),
        *spine_members(),
        afrasyab_uniform(1, F(1, 16)),
    ]


N_SMALL = 8
# The uniform C3 member (729 routings) is the last one; ``frontier_value`` does not finish on
# it (dense LP over up to 648 rows), so the exact-agreement tests stop before it and C3 has its
# own bracketing test below.
N_EXACT = 7


def brute_min(inst: Instance, costs, level):
    best = None
    for r in all_routings(inst):
        load = routing_load(inst, r)
        if alpha_for_routing(inst, load) >= level:
            continue
        c = sum((costs[a.index] * load[a.index] for a in inst.arcs), F(0))
        if best is None or c < best:
            best = c
    return best


def cost_vectors(inst: Instance):
    m = len(inst.arcs)
    yield [a.cost for a in inst.arcs]
    yield [F(1, m)] * m
    yield [F(i % 3, 3) for i in range(m)]  # zero entries
    yield [F((7 * i + 3) % 5, 11) for i in range(m)]  # zero entries, distinct values
    yield [F(0)] * m


def levels_of(inst: Instance):
    alphas = sorted({alpha_for_routing(inst, routing_load(inst, r)) for r in all_routings(inst)})
    return [F(0), *alphas, alphas[-1] + 1]


# -- oracle -------------------------------------------------------------------


def test_small_instance_count():
    assert len(small_instances()) == N_SMALL


@pytest.mark.parametrize("idx", range(N_SMALL))
def test_oracle_equals_brute_force(idx):
    inst = small_instances()[idx]
    for costs in cost_vectors(inst):
        for level in levels_of(inst):  # includes every attained alpha (strict inequality)
            got = cheapest_routing_below(inst, costs, level)
            want = brute_min(inst, costs, level)
            if want is None:
                assert got is None
            else:
                assert got is not None
                routing, load, cost = got
                assert cost == want
                assert alpha_for_routing(inst, load) < level
                assert load == routing_load(inst, routing)
                assert cost == sum((costs[a.index] * load[a.index] for a in inst.arcs), F(0))


def test_oracle_returns_none_when_nothing_is_below():
    inst = v1()
    lowest = min(alpha_for_routing(inst, routing_load(inst, r)) for r in all_routings(inst))
    assert cheapest_routing_below(inst, [F(1)] * len(inst.arcs), lowest) is None


def test_oracle_uses_arc_indices_for_parallel_arcs():
    inst = parallel_instance()
    # only the first parallel arc is expensive: the answer must use the second
    costs = [F(5), F(0), F(0), F(0)]
    routing, load, cost = cheapest_routing_below(inst, costs, F(100))
    assert cost == 0
    assert load[0] == 0 and load[1] == 3


def test_oracle_single_path_terminal():
    inst = Instance.build(source="s", demands={"t": 1}, arcs=[("s", "t", 1, 2)])
    assert len(paths_by_terminal(inst)["t"]) == 1
    routing, load, cost = cheapest_routing_below(inst, [F(2)], F(1))
    assert cost == 2


# -- evaluator ----------------------------------------------------------------


@pytest.mark.parametrize("idx", range(N_EXACT))
def test_frontier_cp_agrees_with_exact_frontier(idx):
    inst = small_instances()[idx]
    exact = frontier_value(inst)
    cp = frontier_value_cp(inst)
    assert cp.alpha_max == exact.alpha_max
    assert cp.ceiling == exact.ceiling
    assert cp.solves >= len(cp.tested) and cp.cuts >= 0
    assert cp.levels == tuple(sorted(set(exact.routing_alphas)))


@pytest.mark.parametrize("idx", range(N_SMALL))
def test_level_positivity_is_monotone_and_search_does_not_skip(idx):
    inst = small_instances()[idx]
    levels = list(frontier_value_cp(inst).levels)
    flags = [level_positive(inst, lv)[0] for lv in levels]
    assert flags[0] is True
    assert flags == sorted(flags, reverse=True)  # once not positive, never positive again
    assert frontier_value_cp(inst).alpha_max == levels[flags.count(True) - 1]


def test_some_instance_has_several_positive_levels():
    counts = []
    for inst in small_instances():
        levels = list(frontier_value_cp(inst).levels)
        counts.append(sum(level_positive(inst, lv)[0] for lv in levels))
    assert max(counts) >= 3


def test_witness_separates():
    inst = claim_2026()
    cp = frontier_value_cp(inst)
    assert cp.alpha_max > 1
    c = cp.witness_cost
    assert sum(c) == 1
    cx = sum((ci * a.x for ci, a in zip(c, inst.arcs)), F(0))
    for r in all_routings(inst):
        load = routing_load(inst, r)
        if alpha_for_routing(inst, load) < cp.alpha_max:
            assert sum((ci * load[a.index] for ci, a in zip(c, inst.arcs)), F(0)) > cx


def test_no_float_in_result():
    cp = frontier_value_cp(v1())
    assert isinstance(cp.alpha_max, Fraction) and isinstance(cp.ceiling, Fraction)
    assert all(isinstance(v, Fraction) for v in cp.witness_cost)


# -- odd-cycle family ---------------------------------------------------------


C5_EPS = F(1, 120)


def c5_table():
    """The report's D2 C5 arc table, written out independently of the builder."""
    arcs = []
    r, g, rs, fin, ap, di = F(101, 120), F(41, 120), F(101, 120), F(41, 120), F(1, 2), F(61, 120)
    inv = F(20, 17)
    for i in range(5):
        arcs += [
            ("s", f"a{i}", r, 0), (f"a{i}", f"b{i}", r, 0), (f"b{i}", f"c{i}", g, 0),
            (f"c{i}", f"d{i}", rs, 0), (f"d{i}", f"t{i}", fin, 0),
            ("s", f"c{i}", ap, inv), ("s", f"t{i}", di, inv),
        ]
    for i in range(5):
        j = (i + 1) % 5
        arcs += [(f"d{i}", f"e{i}", F(1, 2), 0), (f"b{j}", f"e{i}", F(1, 2), inv)]
    return arcs


def test_uniform_member_equals_the_report_table_arc_by_arc():
    inst = afrasyab_uniform(2, C5_EPS)
    want = c5_table()
    assert len(inst.arcs) == len(want) == 45
    for a, (tail, head, x, cost) in zip(inst.arcs, want):
        assert (a.tail, a.head, a.x, a.cost) == (tail, head, x, cost)
    expected = {f"t{i}": F(17, 20) for i in range(5)} | {f"e{i}": F(1) for i in range(5)}
    assert dict(inst.demands) == expected


def test_odd_cycle_instance_matches_uniform_on_the_uniform_parameters():
    k, eps = 2, C5_EPS
    n = 5
    t = F(k, 2 * (k + 1)) + eps
    b = F(1, 2) + eps + t
    inst = odd_cycle_instance(
        n, [b] * n, [F(1)] * n, [t + F(1, 2)] * n, [F(1, 2)] * n, [F(1, 2)] * n
    )
    ref = afrasyab_uniform(k, eps)
    assert inst is not None
    assert [(a.index, a.tail, a.head, a.x, a.cost) for a in inst.arcs] == [
        (a.index, a.tail, a.head, a.x, a.cost) for a in ref.arcs
    ]
    assert dict(inst.demands) == dict(ref.demands)


def test_odd_cycle_instance_rejects_invalid_parameters():
    n = 5
    t, b = F(41, 120), F(17, 20)
    ok = dict(b=[b] * n, delta=[F(1)] * n, r=[t + F(1, 2)] * n, u=[F(1, 2)] * n, approach=[F(1, 2)] * n)
    assert odd_cycle_instance(n, **ok) is not None
    assert odd_cycle_instance(4, **{k: v[:4] for k, v in ok.items()}) is None  # even n
    assert odd_cycle_instance(1, **{k: v[:1] for k, v in ok.items()}) is None  # n below 3
    assert odd_cycle_instance(n, **{**ok, "b": [F(0)] + [b] * 4}) is None  # nonpositive demand
    assert odd_cycle_instance(n, **{**ok, "delta": [F(-1)] + [F(1)] * 4}) is None
    assert odd_cycle_instance(n, **{**ok, "u": [F(3, 2)] + [F(1, 2)] * 4}) is None  # w negative
    assert odd_cycle_instance(n, **{**ok, "r": [F(1, 4)] + [t + F(1, 2)] * 4}) is None  # connector negative
    assert odd_cycle_instance(n, **{**ok, "b": [F(1, 10)] * n}) is None  # direct negative
    assert odd_cycle_instance(n, **{**ok, "approach": [F(-1, 2)] + [F(1, 2)] * 4}) is None
    assert odd_cycle_instance(n, **{**ok, "u": [F(1, 2)] * 4}) is None  # wrong length


def test_odd_cycle_nonuniform_member_is_feasible_and_acyclic():
    n = 5
    t = F(41, 120)
    inst = odd_cycle_instance(
        n,
        b=[F(17, 20), F(4, 5), F(17, 20), F(9, 10), F(17, 20)],
        delta=[F(1)] * n,
        r=[t + F(1, 2)] * n,
        u=[F(1, 2)] * n,
        approach=[F(1, 2), F(2, 5), F(1, 2), F(1, 2), F(3, 5)],
    )
    assert inst is not None
    inst.check_feasible()
    assert is_acyclic(inst)
    assert inst.arcs[5].cost == F(20, 17)  # approach_0 costs 1/b_0
    assert inst.arcs[7 + 5].cost == F(5, 4)  # approach_1 costs 1/b_1


def test_afrasyab_uniform_refuses_out_of_range():
    for k, eps in [(2, F(0)), (2, F(-1, 100)), (2, F(1, 12)), (2, F(1, 6)), (0, F(1, 100))]:
        with pytest.raises(ValueError):
            afrasyab_uniform(k, eps)
    with pytest.raises(TypeError):
        afrasyab_uniform(2, 0.01)


def test_uniform_c3_frontier_agrees_with_exact_lp_at_the_bracketing_levels():
    """``frontier_value`` cannot run on C3, so reproduce its definition at two levels.

    Positivity is monotone, so the exact frontier value is the largest positive level: an
    exact ``max_min_margin`` over every routing below 11/16 (36 rows) is positive and over
    every routing below the next level 17/16 (52 rows) is not.
    """
    from ufclib.simplex import max_min_margin

    inst = afrasyab_uniform(1, F(1, 16))
    inst.check_feasible()
    cp = frontier_value_cp(inst)
    rows = []
    for r in all_routings(inst):
        load = routing_load(inst, r)
        rows.append((alpha_for_routing(inst, load), [load[a.index] for a in inst.arcs]))
    levels = sorted({a for a, _ in rows})
    x = [a.x for a in inst.arcs]
    exact_top = None
    for lv in levels:
        below = [y for a, y in rows if a < lv]
        if len(below) > 60:
            break
        if max_min_margin(below, x)[0] > 0:
            exact_top = lv
        else:
            nxt = lv
    assert exact_top == F(11, 16) == cp.alpha_max
    assert nxt == F(17, 16)


def test_c5_member_shape_and_frontier_value():
    """Production path: the instance the sweep starts from; the 2026-11-07 preflight gave 79/120."""
    inst = afrasyab_uniform(2, C5_EPS)
    inst.check_feasible()
    assert len(inst.arcs) == 45
    assert len(inst.vertices) == 31
    assert is_acyclic(inst)
    per = paths_by_terminal(inst)
    assert {len(p) for p in per.values()} == {3} and len(per) == 10
    n_routings = 1
    for p in per.values():
        n_routings *= len(p)
    assert n_routings == 59049
    assert inst.fractional_cost == F(905, 102)
    assert frontier_value_cp(inst).alpha_max == F(79, 120)
