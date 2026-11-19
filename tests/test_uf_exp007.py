"""Tests for unsplittable-flow-cost EXP-007: the certificate checker for planarity and the exact family builders."""
from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

import networkx as nx
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP = (ROOT / "problems" / "optimization-geometry" / "unsplittable-flow-cost" / "experiments"
       / "EXP-007-nikolenko-records-recheck")
sys.path.insert(0, str(EXP))
sys.path.insert(0, str(EXP.parent.parent / "code"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"uf_exp007_{name}", EXP / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


PL = _load("planarity")


def _edges(g: nx.Graph) -> list[tuple[str, str]]:
    return [(str(u), str(v)) for u, v in g.edges()]


def _relabel(g: nx.Graph) -> nx.Graph:
    return nx.relabel_nodes(g, {n: f"n{n}" for n in g.nodes()})


def _rotation_from_solver(g: nx.Graph) -> dict[str, list[str]]:
    ok, emb = nx.check_planarity(g)
    assert ok
    return {str(v): [str(w) for w in emb.neighbors_cw_order(v)] for v in g.nodes()}


def _petersen() -> nx.Graph:
    return _relabel(nx.petersen_graph())


def _k5() -> nx.Graph:
    return _relabel(nx.complete_graph(5))


def _k33() -> nx.Graph:
    return _relabel(nx.complete_bipartite_graph(3, 3))


# ---- planar certificates: accepted ----------------------------------------------------------------


def test_k4_embedding_is_accepted_with_euler_formula() -> None:
    g = _relabel(nx.complete_graph(4))
    res = PL.check_planar_certificate(list(g.nodes()), _edges(g), _rotation_from_solver(g))
    assert res["ok"], res
    assert (res["V"], res["E"], res["F"]) == (4, 6, 4)
    assert res["V"] - res["E"] + res["F"] == 2


def test_grid_embedding_is_accepted_with_euler_formula() -> None:
    g = _relabel(nx.convert_node_labels_to_integers(nx.grid_2d_graph(4, 3)))
    res = PL.check_planar_certificate(list(g.nodes()), _edges(g), _rotation_from_solver(g))
    assert res["ok"], res
    assert (res["V"], res["E"], res["F"]) == (12, 17, 7)


def test_euler_formula_is_per_component() -> None:
    g = nx.disjoint_union(nx.complete_graph(4), nx.cycle_graph(3))
    g = _relabel(g)
    res = PL.check_planar_certificate(list(g.nodes()), _edges(g), _rotation_from_solver(g))
    assert res["ok"], res
    assert res["components"] == 2
    assert res["F"] == 4 + 2  # K4 has 4 faces, a triangle 2


def test_tree_and_isolated_vertex_have_one_face_per_component() -> None:
    g = nx.path_graph(4)
    g.add_node(9)
    g = _relabel(g)
    res = PL.check_planar_certificate(list(g.nodes()), _edges(g), _rotation_from_solver(g))
    assert res["ok"], res
    assert res["components"] == 2


# ---- planar certificates: rejected ----------------------------------------------------------------


def test_tampered_embedding_of_k4_is_rejected() -> None:
    g = _relabel(nx.complete_graph(4))
    rot = _rotation_from_solver(g)
    # K4 has 2 rotation classes per vertex; flipping one vertex's order gives a torus embedding (V-E+F = 0)
    v = "n0"
    rot[v] = [rot[v][0], rot[v][2], rot[v][1]]
    res = PL.check_planar_certificate(list(g.nodes()), _edges(g), rot)
    assert not res["ok"]
    assert res["V"] - res["E"] + res["F"] != 2


def test_tampered_embedding_of_grid_is_rejected() -> None:
    g = _relabel(nx.convert_node_labels_to_integers(nx.grid_2d_graph(4, 3)))
    rot = _rotation_from_solver(g)
    v = next(v for v in rot if len(rot[v]) == 4)
    rot[v] = [rot[v][0], rot[v][2], rot[v][1], rot[v][3]]
    res = PL.check_planar_certificate(list(g.nodes()), _edges(g), rot)
    assert not res["ok"]


def test_embedding_with_foreign_neighbour_or_missing_vertex_is_rejected() -> None:
    g = _relabel(nx.complete_graph(4))
    rot = _rotation_from_solver(g)
    bad = dict(rot)
    bad["n0"] = ["n1", "n2", "zzz"]
    assert not PL.check_planar_certificate(list(g.nodes()), _edges(g), bad)["ok"]
    missing = {k: v for k, v in rot.items() if k != "n3"}
    assert not PL.check_planar_certificate(list(g.nodes()), _edges(g), missing)["ok"]
    dup = dict(rot)
    dup["n0"] = ["n1", "n1", "n2"]
    assert not PL.check_planar_certificate(list(g.nodes()), _edges(g), dup)["ok"]


def test_embedding_of_another_graph_is_rejected() -> None:
    k4 = _relabel(nx.complete_graph(4))
    grid = _relabel(nx.convert_node_labels_to_integers(nx.grid_2d_graph(2, 2)))  # C4 on n0..n3
    rot = _rotation_from_solver(k4)
    assert not PL.check_planar_certificate(list(grid.nodes()), _edges(grid), rot)["ok"]


def test_a_planar_embedding_cannot_certify_a_nonplanar_graph() -> None:
    k5 = _k5()
    k5_minus = k5.copy()
    k5_minus.remove_edge("n0", "n1")
    rot = _rotation_from_solver(k5_minus)
    assert not PL.check_planar_certificate(list(k5.nodes()), _edges(k5), rot)["ok"]


# ---- Kuratowski certificates ----------------------------------------------------------------------


@pytest.mark.parametrize("make,kind", [(_k5, "K5"), (_k33, "K3,3")])
def test_k5_and_k33_are_certified_nonplanar_by_themselves(make, kind) -> None:
    g = make()
    ok, sub = nx.check_planarity(g, counterexample=True)
    assert not ok
    res = PL.check_kuratowski_certificate(list(g.nodes()), _edges(g), _edges(sub))
    assert res["ok"], res
    assert res["type"] == kind


def test_petersen_is_certified_nonplanar() -> None:
    g = _petersen()
    ok, sub = nx.check_planarity(g, counterexample=True)
    assert not ok
    res = PL.check_kuratowski_certificate(list(g.nodes()), _edges(g), _edges(sub))
    assert res["ok"], res
    assert res["type"] in ("K5", "K3,3")
    assert res["suppressed_vertices"] >= 1  # Petersen contains a proper subdivision, not K5/K3,3 itself


def test_tampered_kuratowski_subgraph_is_rejected() -> None:
    g = _petersen()
    ok, sub = nx.check_planarity(g, counterexample=True)
    assert not ok
    edges = _edges(sub)
    # (1) an edge that is not in the instance
    absent = next((a, b) for a, b in combinations(sorted(g.nodes()), 2) if not g.has_edge(a, b))
    assert not PL.check_kuratowski_certificate(list(g.nodes()), _edges(g), edges + [absent])["ok"]
    # (2) one edge removed: no longer a subdivision of K5 or K3,3
    assert not PL.check_kuratowski_certificate(list(g.nodes()), _edges(g), edges[1:])["ok"]
    # (3) a planar subgraph of the instance (a spanning tree)
    tree = _edges(nx.minimum_spanning_tree(g))
    assert not PL.check_kuratowski_certificate(list(g.nodes()), _edges(g), tree)["ok"]
    # (4) an extra, genuine edge of the instance outside the subdivision
    extra = next((u, v) for u, v in _edges(g) if (u, v) not in edges and (v, u) not in edges)
    assert not PL.check_kuratowski_certificate(list(g.nodes()), _edges(g), edges + [extra])["ok"]


def test_a_kuratowski_subgraph_of_another_graph_is_rejected() -> None:
    k5 = _k5()
    other = _relabel(nx.complete_graph(4))
    assert not PL.check_kuratowski_certificate(list(other.nodes()), _edges(other), _edges(k5))["ok"]


def test_a_subdivision_that_makes_parallel_edges_is_rejected() -> None:
    # two paths between the same pair after suppression: K5 with one edge replaced by two parallel paths
    g = nx.complete_graph(5)
    g.remove_edge(0, 1)
    g.add_edges_from([(0, 7), (7, 1), (0, 8), (8, 1)])
    g = _relabel(g)
    res = PL.check_kuratowski_certificate(list(g.nodes()), _edges(g), _edges(g))
    assert not res["ok"]


def test_planar_graph_has_no_kuratowski_certificate() -> None:
    g = _relabel(nx.complete_graph(4))
    assert not PL.check_kuratowski_certificate(list(g.nodes()), _edges(g), _edges(g))["ok"]


# ---- the solver wrapper and the whole verdict -----------------------------------------------------


def test_decide_planarity_returns_checked_certificates() -> None:
    for g, planar in ((_relabel(nx.complete_graph(4)), True), (_petersen(), False), (_k33(), False)):
        out = PL.decide_planarity(list(g.nodes()), _edges(g))
        assert out["planar"] is planar
        assert out["certificate_ok"] is True


def test_face_trace_counts_darts_once() -> None:
    g = _relabel(nx.complete_graph(4))
    faces = PL.trace_faces(_rotation_from_solver(g))
    assert sum(len(f) for f in faces) == 2 * g.number_of_edges()


# ---- exact family builders ------------------------------------------------------------------------


def test_exact_expression_evaluator_is_exact_and_refuses_floats() -> None:
    FAM = _load("family")
    assert FAM.eval_expr("(1-t)^2", {"t": F(3, 20)}) == F(289, 400)
    assert FAM.eval_expr("d0*(1-f0)", {"d0": F(2), "f0": F(1, 4)}) == F(3, 2)
    assert FAM.eval_expr("1/d0", {"d0": F(8)}) == F(1, 8)
    assert FAM.eval_expr("2t-t^2", {"t": F(3, 20)}) == F(111, 400)  # implicit product as transcribed
    assert FAM.eval_expr("1-4t+t^2", {"t": F(3, 20)}) == F(169, 400)
    with pytest.raises(ValueError):
        FAM.eval_expr("0.5*t", {"t": F(1)})
    with pytest.raises(ValueError):
        FAM.eval_expr("__import__('os')", {})
    with pytest.raises(ValueError):
        FAM.eval_expr("sqrt(2)", {})


def test_sqrt41_bounds_are_verified_by_squaring() -> None:
    FAM = _load("family")
    lo, hi = FAM.sqrt41_bounds()
    assert lo * lo < 41 < hi * hi
    assert hi - lo <= F(1, 10**9)


FAM = _load("family")

# Fixture copied from instances.json (UF-4INT-FAMILY, symbolic) and UF-4INT-n68 (concrete integers).
_FAM4 = {
    "source_vertex": "v0",
    "demands": {"t0": "1", "t1": "(1-t)^2", "t2": "1-t", "t3": "1"},
    "x_symbols": {"d": ["1", "(1-t)^2", "1-t", "1"], "f": ["2t-t^2", "1-4t+t^2", "t", "t+eps"]},
    "arcs": [
        ("v0", "v1", "d0*f0+d1*f1+d2*(1-f2)+d2*f2+d3*(1-f3)+d3*f3", "0"),
        ("v1", "v2", "d0*f0+d1*f1+d2*f2+d3*(1-f3)+d3*f3", "0"),
        ("v2", "v3", "d0*f0+d1*f1+d2*f2+d3*f3", "0"),
        ("v3", "v4", "d1*f1+d2*f2+d3*f3", "0"),
        ("v4", "v5", "d1*f1+d2*f2", "0"),
        ("v0", "t0", "d0*(1-f0)", "1/d0"), ("v3", "t0", "d0*f0", "0"),
        ("v0", "t1", "d1*(1-f1)", "1/d1"), ("v5", "t1", "d1*f1", "0"),
        ("v1", "t2", "d2*(1-f2)", "1/d2"), ("v5", "t2", "d2*f2", "0"),
        ("v2", "t3", "d3*(1-f3)", "1/d3"), ("v4", "t3", "d3*f3", "0"),
    ],
}
_N68 = {
    "source_vertex": "v0",
    "demands": {"t0": "10880000", "t1": "7860800", "t2": "9248000", "t3": "10880000"},
    "arcs": [
        {"tail": "v0", "head": "v1", "x": "26468388", "cost": "0"},
        {"tail": "v1", "head": "v2", "x": "18607588", "cost": "0"},
        {"tail": "v2", "head": "v3", "x": "9519588", "cost": "0"},
        {"tail": "v3", "head": "v4", "x": "6500388", "cost": "0"},
        {"tail": "v4", "head": "v5", "x": "4708388", "cost": "0"},
        {"tail": "v0", "head": "t0", "x": "7860800", "cost": "289"},
        {"tail": "v3", "head": "t0", "x": "3019200", "cost": "0"},
        {"tail": "v0", "head": "t1", "x": "4539612", "cost": "400"},
        {"tail": "v5", "head": "t1", "x": "3321188", "cost": "0"},
        {"tail": "v1", "head": "t2", "x": "7860800", "cost": "340"},
        {"tail": "v5", "head": "t2", "x": "1387200", "cost": "0"},
        {"tail": "v2", "head": "t3", "x": "9088000", "cost": "289"},
        {"tail": "v4", "head": "t3", "x": "1792000", "cost": "0"},
    ],
}
_TERN10 = {
    "source_vertex": "v0",
    "demands": {"t0": "1", "t1": "29/40", "t2": "1"},
    "arcs": [
        {"tail": "v0", "head": "v1", "x": "1339/800", "cost": "0"},
        {"tail": "v1", "head": "v2", "x": "759/800", "cost": "0"},
        {"tail": "v2", "head": "v3", "x": "539/800", "cost": "0"},
        {"tail": "v0", "head": "t0", "x": "29/40", "cost": "1"},
        {"tail": "v2", "head": "t0", "x": "11/40", "cost": "0"},
        {"tail": "v0", "head": "t1", "x": "261/800", "cost": "40/29"},
        {"tail": "v3", "head": "t1", "x": "319/800", "cost": "0"},
        {"tail": "v1", "head": "t2", "x": "29/40", "cost": "1"},
        {"tail": "v3", "head": "t2", "x": "11/40", "cost": "0"},
    ],
}


def _fam4_entry() -> dict:
    return {
        "source_vertex": _FAM4["source_vertex"], "demands": _FAM4["demands"], "x_symbols": _FAM4["x_symbols"],
        "arcs": [{"tail": a, "head": b, "x": x, "cost": c} for a, b, x, c in _FAM4["arcs"]],
    }


def test_four_interval_builder_reproduces_the_concrete_member_n68() -> None:
    inst = FAM.four_interval_member(_fam4_entry(), F(3, 20), F(1, 68))
    rep = FAM.reproduces_entry(inst, _N68)
    assert rep["ok"], rep
    assert F(rep["flow_scale"]) == 160000 * 68
    assert F(rep["cost_scale"]) == 289


def test_reproduction_check_fires_on_a_one_unit_change() -> None:
    inst = FAM.four_interval_member(_fam4_entry(), F(3, 20), F(1, 68))
    bad = {**_N68, "arcs": [dict(a) for a in _N68["arcs"]]}
    bad["arcs"][2]["x"] = "9519589"
    assert not FAM.reproduces_entry(inst, bad)["ok"]
    inst67 = FAM.four_interval_member(_fam4_entry(), F(3, 20), F(1, 67))
    assert not FAM.reproduces_entry(inst67, _N68)["ok"]


def test_ternary_builder_reproduces_the_concrete_member_eta_one_tenth() -> None:
    rep = FAM.reproduces_entry(FAM.ternary_member(F(1, 10)), _TERN10)
    assert rep["ok"], rep
    assert F(rep["flow_scale"]) == 1 and F(rep["cost_scale"]) == 1


def test_generic_interval_builder_matches_the_symbolic_four_interval_member() -> None:
    t, eps = F(3, 20), F(1, 68)
    sym = FAM.four_interval_member(_fam4_entry(), t, eps)
    d = [F(1), (1 - t) ** 2, 1 - t, F(1)]
    f = [2 * t - t * t, 1 - 4 * t + t * t, t, t + eps]
    gen = FAM.interval_instance(((0, 2), (0, 4), (1, 4), (2, 3)), d, f)
    assert [(a.tail, a.head, a.x, a.cost) for a in gen.arcs] == [(a.tail, a.head, a.x, a.cost) for a in sym.arcs]


def test_exact_values_of_the_two_families() -> None:
    from ufclib.decide import decide_instance

    inst = FAM.four_interval_member(_fam4_entry(), F(3, 20), F(1, 68))
    assert decide_instance(inst).alpha_instance == F(182359, 160000) - F(1, 68)
    assert FAM.four_interval_closed_form(F(3, 20), F(1, 68)) == F(182359, 160000) - F(1, 68)
    tern = FAM.ternary_member(F(1, 10))
    assert decide_instance(tern).alpha_instance == F(841, 800) == FAM.ternary_closed_form(F(1, 10))


def test_checker_functions_do_not_touch_the_solver() -> None:
    import inspect

    for fn in (PL.trace_faces, PL.check_planar_certificate, PL.check_kuratowski_certificate):
        src = inspect.getsource(fn)
        assert "networkx" not in src and "nx." not in src and "decide_planarity" not in src
