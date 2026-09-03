"""Unit tests for pcclib (standard library plus pytest). Solver tests need WSL CaDiCaL."""

from __future__ import annotations

import itertools
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pcclib import checkers, cnf, encoders, graphs, invariants, solver  # noqa: E402

HAS_WSL = shutil.which("wsl.exe") is not None


def brute_force(f: cnf.CNF) -> list[set[int]]:
    models = []
    for bits in itertools.product([False, True], repeat=f.nvars):
        assign = {i + 1 for i, b in enumerate(bits) if b}
        if all(any((lit > 0) == (abs(lit) in assign) for lit in cl) for cl in f.clauses):
            models.append(assign)
    return models


def test_petersen_graph_shape():
    p = graphs.petersen()
    assert p.n == 10 and len(p.edges) == 15 and p.is_cubic()
    assert invariants.girth(p) == 5
    assert invariants.edge_connectivity(p) == 3
    assert invariants.cyclic_edge_cut_below(p, 5) is None


def test_flower_snark_j5():
    g = graphs.flower_snark(5)
    assert g.is_cubic() and g.n == 20
    assert invariants.girth(g) == 5
    assert invariants.is_bridgeless(g)


def test_k4_and_prism():
    assert invariants.girth(graphs.k4()) == 3
    assert invariants.girth(graphs.prism()) == 3
    assert invariants.edge_connectivity(graphs.prism()) == 3


def test_at_most_k_matches_brute_force():
    for n, k in [(3, 1), (4, 2), (5, 3)]:
        f = cnf.CNF()
        xs = [f.var(f"x_{i}") for i in range(n)]
        f.at_most_k(xs, k)
        models = brute_force(f)
        projected = {frozenset(m & set(xs)) for m in models}
        expected = {
            frozenset(xs[i] for i in idx)
            for r in range(k + 1)
            for idx in itertools.combinations(range(n), r)
        }
        assert projected == expected


def test_exactly_two_helpers():
    f = cnf.CNF()
    xs = [f.var(f"x_{i}") for i in range(4)]
    f.at_least_two(xs)
    f.at_most_two(xs)
    assert {len(m) for m in brute_force(f)} == {2}


def test_checkers_reject_corruption():
    p = graphs.petersen()
    identity = list(range(15))
    assert checkers.petersen_defect(p, identity) == 0
    corrupted = identity[:]
    corrupted[0], corrupted[1] = corrupted[1], corrupted[0]
    assert checkers.petersen_defect(p, corrupted) > 0
    k = graphs.k4()
    colors = [0, 1, 2, 2, 1, 0]  # edges (0,1),(0,2),(0,3),(1,2),(1,3),(2,3)
    assert checkers.check_proper(k, colors)
    assert checkers.normal_defect(k, colors) == 0
    assert not checkers.check_proper(k, [0, 0, 1, 1, 2, 2])
    assert not checkers.is_perfect_matching(k, {0, 1})
    assert checkers.is_perfect_matching(k, {0, 5})


def test_digest_convention_matches_public_value():
    data = Path(__file__).resolve().parents[2] / "data" / "putman-112-main.edgelist"
    g = graphs.load_edgelist(data)
    assert g.n == 112 and len(g.edges) == 168 and g.is_cubic()
    assert g.digest() == "dc16cc18600cf77c8661b7baf89c7019f265299308541961ff884ea7187b4e8b"


@pytest.mark.skipif(not HAS_WSL, reason="needs WSL CaDiCaL")
def test_solver_roundtrip(tmp_path: Path):
    p = graphs.petersen()
    f = encoders.petersen_coloring(p)
    cnf_path = tmp_path / "p.cnf"
    f.write(cnf_path)
    rec = solver.solve(cnf_path, tmp_path / "p.drat", timeout_s=60)
    assert rec["status"] == "SAT"
    model = set(rec["model"])
    images = checkers.edge_color_map(model, f.names, 15, 15, prefix="y")
    assert checkers.petersen_defect(p, images) == 0
    k = graphs.k4()
    f2 = encoders.proper_edge_coloring(k, 2)
    c2 = tmp_path / "k.cnf"
    f2.write(c2)
    rec2 = solver.solve(c2, tmp_path / "k.drat", timeout_s=60)
    assert rec2["status"] == "UNSAT" and rec2["drat_trim_verified"]


def test_oddness_checker_on_petersen_and_k4():
    p = graphs.petersen()
    for M in itertools.combinations(range(15), 5):
        if checkers.is_perfect_matching(p, set(M)):
            assert checkers.odd_cycles_of_two_factor(p, set(M)) == 2
            break
    k = graphs.k4()
    assert checkers.odd_cycles_of_two_factor(k, {0, 5}) == 0


@pytest.mark.skipif(not HAS_WSL, reason="needs WSL CaDiCaL")
def test_oddness_and_resistance_of_petersen(tmp_path: Path):
    p = graphs.petersen()
    f1 = encoders.oddness(p, 1)
    c1 = tmp_path / "o1.cnf"
    f1.write(c1)
    assert solver.solve(c1, tmp_path / "o1.drat", 60)["status"] == "UNSAT"
    f2 = encoders.oddness(p, 2)
    c2 = tmp_path / "o2.cnf"
    f2.write(c2)
    rec = solver.solve(c2, tmp_path / "o2.drat", 60)
    assert rec["status"] == "SAT"
    model = set(rec["model"])
    M = {e for e in range(15) if f2.names[f"m_{e}"] in model}
    assert checkers.odd_cycles_of_two_factor(p, M) == 2
    r1 = encoders.resistance(p, 1)
    c3 = tmp_path / "r1.cnf"
    r1.write(c3)
    assert solver.solve(c3, tmp_path / "r1.drat", 60)["status"] == "UNSAT"
    r2 = encoders.resistance(p, 2)
    c4 = tmp_path / "r2.cnf"
    r2.write(c4)
    assert solver.solve(c4, tmp_path / "r2.drat", 60)["status"] == "SAT"
