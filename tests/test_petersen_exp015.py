"""Tests of EXP-015 (rings of superedges cut from the cyclically 5-edge-connected snarks of order at most 28).

Run from the repository root:  .venv/Scripts/python.exe -m pytest tests/test_petersen_exp015.py -q
The sources are the House of Graphs lists under the data root (G0 hashes are checked by `run.py gates`).
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "problems" / "combinatorics" / "petersen-coloring" / "experiments" / "EXP-015-snark-superedge-rings"
sys.path.insert(0, str(ROOT / "problems" / "combinatorics" / "petersen-coloring" / "code"))

from pcclib import graphs, invariants, transfer  # noqa: E402


def load_run():
    spec = importlib.util.spec_from_file_location("exp015_run", EXP / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp015_run"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def run():
    return load_run()


@pytest.fixture(scope="module")
def petersen_block(run):
    gs = run.load_g6(run.SOURCES / "Generated_graphs.10.05.sn.cyc5.g6")
    assert len(gs) == 1
    u, w, _ = run.orbit_pairs(gs[0])[0][0]
    blk = run.superedge_block(gs[0], u, w, "P")
    return blk, transfer.sector_matrices(blk)


def test_loader_and_g0_on_order_10(run):
    gs = run.load_g6(run.SOURCES / "Generated_graphs.10.05.sn.cyc5.g6")
    assert len(gs) == 1
    g = gs[0]
    assert g.n == 10 and len(g.edges) == 15 and g.is_cubic()
    rec = run.g0_graph(g)
    assert rec["cubic"] and rec["simple"] and rec["girth"] == 5
    assert rec["cyclically_5_edge_connected"] is True
    assert rec["three_edge_colorable"] is False


def test_g0_rejects_a_three_edge_colorable_graph(run):
    rec = run.g0_graph(graphs.prism())
    assert rec["three_edge_colorable"] is True and rec["girth"] == 3


def test_orbits_of_pairs_of_the_petersen_graph(run):
    g = run.load_g6(run.SOURCES / "Generated_graphs.10.05.sn.cyc5.g6")[0]
    reps, naut = run.orbit_pairs(g)
    assert naut == 120
    assert len(reps) == 1 and reps[0][2] == 2  # all 30 pairs at distance 2 form one orbit; none at distance 3 or more


def test_superedge_block_of_p_equals_the_exp014_s_entries(petersen_block):
    blk, mats = petersen_block
    assert len(blk.pole.kept) == 8
    ones = {o: int(m.sum()) for o, m in mats.items()}
    assert ones == {"0": 120, "E": 296, "D3": 0, "D2": 8, "T1": 0, "T2": 0}


def test_left_and_right_are_ordered_by_the_former_neighbor(run):
    g = run.load_g6(run.SOURCES / "Generated_graphs.10.05.sn.cyc5.g6")[0]
    u, w, _ = run.orbit_pairs(g)[0][0]
    blk = run.superedge_block(g, u, w, "P")
    adj = g.adjacency()
    lnb = [blk.pole.dangling[j][0] for j in blk.left]
    rnb = [blk.pole.dangling[j][0] for j in blk.right]
    assert lnb == sorted(adj[u]) and rnb == sorted(adj[w])


def test_generators_are_twelve_before_dedup_and_distinct_after(run, petersen_block):
    _, mats = petersen_block
    gens = run.block_generators(mats)
    assert len(gens) == 12
    assert {(o, p) for o, p, _ in gens} == {(o, p) for o in "fr" for p in range(6)}


def test_packed_pair_trace_matches_the_library_product(run, petersen_block):
    _, mats = petersen_block
    gens = [g for _, _, g in run.block_generators(mats)]
    rng = random.Random(7)
    for _ in range(60):
        a, b = rng.choice(gens), rng.choice(gens)
        lib = bool(transfer.colorable_sectors(transfer.product([a, b])))
        assert run.packed_pair_trace(transfer.pack(a), transfer.pack(b)) == lib
    # the diagonal (a block with itself) and every unordered pair of the twelve
    for a, b in itertools.combinations_with_replacement(gens, 2):
        lib = bool(transfer.colorable_sectors(transfer.product([a, b])))
        assert run.packed_pair_trace(transfer.pack(a), transfer.pack(b)) == lib


def test_bulk_pair_search_matches_the_packed_test(run, petersen_block):
    _, mats = petersen_block
    gens = [g for _, _, g in run.block_generators(mats)]
    # a random sparse perturbation family so that some pairs have a zero trace
    rng = np.random.default_rng(3)
    fam = []
    for g in gens[:6]:
        h = {o: m & (rng.random(m.shape) < 0.05) for o, m in g.items()}
        fam.append(h)
    fam += gens
    packed = np.array([np.frombuffer(transfer.pack(g), dtype=np.uint8) for g in fam])
    hits, per_sector = run.bulk_pair_hits(packed, chunk=5)
    n = len(fam)
    zero = set()
    for i in range(n):
        for j in range(i, n):
            bit = bool(hits[i, j // 8] >> (7 - j % 8) & 1)
            lib = bool(transfer.colorable_sectors(transfer.product([fam[i], fam[j]])))
            assert bit == lib
            if not lib:
                zero.add((i, j))
    assert zero, "the perturbed family must contain zero-trace pairs for this test to mean something"
    assert set(run.zero_pairs(hits, n)) == zero
    assert sum(per_sector.values()) >= 0


def test_ring_of_two_blocks_is_simple_cubic_of_the_expected_order(run, petersen_block):
    blk, _ = petersen_block
    ring = transfer.build_ring([(blk, (0, 1, 2)), (blk, (1, 0, 2))])
    assert ring.n == 16 and ring.is_cubic() and len(ring.edges) == 24


def test_analytic_simplicity_matches_build_ring(run, petersen_block):
    blk, _ = petersen_block  # distance 2: one vertex adjacent to both u and w, the only way a ring of two is not simple
    assert run.double_ends(blk) is not None
    for o1, o2 in itertools.product("fr", repeat=2):
        for p1, p2 in itertools.product(range(6), repeat=2):
            t1, t2 = (o1, p1), (o2, p2)
            b1 = blk if o1 == "f" else blk.reversed()
            b2 = blk if o2 == "f" else blk.reversed()
            try:
                transfer.build_ring([(b1, transfer.PERMS[p1]), (b2, transfer.PERMS[p2])])
                simple = True
            except ValueError:
                simple = False
            assert run.ring2_is_simple(run.triple_frame(blk, *t1), run.triple_frame(blk, *t2)) == simple


def test_nonsimple_count_is_analytic_and_exact(run, petersen_block):
    blk, _ = petersen_block
    triples = [(0, o, p) for o in "fr" for p in range(6)]
    frames = [run.triple_frame(blk, o, p) for _, o, p in triples]
    brute = sum(1 for i in range(12) for j in range(i, 12) if not run.ring2_is_simple(frames[i], frames[j]))
    assert run.count_nonsimple_pairs(frames) == brute
    assert brute > 0


def test_cyclic_cut_helper_agrees_with_the_library(run):
    p = graphs.petersen()
    cube = graphs.Graph.from_edges([(a, a ^ (1 << k)) for a in range(8) for k in range(3) if a < a ^ (1 << k)])
    assert invariants.cyclic_edge_cut_below(p, 5) is None
    assert run.cyclic_connectivity(p) == 5  # at least 5
    assert run.cyclic_connectivity(graphs.prism()) == 3  # the three rungs separate the two triangles
    assert run.cyclic_connectivity(cube) == 4  # the four edges between two opposite faces
    assert run.cyclic_connectivity(graphs.flower_snark(5)) == 5  # J5 is a cyclically 5-edge-connected snark
