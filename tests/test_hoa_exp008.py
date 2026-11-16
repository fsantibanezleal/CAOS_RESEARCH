"""Tests for hoa-mnh EXP-008 (middle gadgets from the order-13 MNH graphs with a universal vertex)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / "problems" / "combinatorics" / "hoa-mnh" / "experiments"
          / "EXP-008-order13-gadgets" / "run.py")
SPEC = importlib.util.spec_from_file_location("hoa_exp008", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

FIRST = "L??EDERa{N~~~~"


def _nx_graph(g6: str) -> nx.Graph:
    return nx.from_graph6_bytes(g6.encode())


def test_loader_gives_286_order13_graphs_with_a_universal_vertex() -> None:
    graphs = MODULE.load_order13()
    assert len(graphs) == 286
    assert graphs[0] == FIRST
    for g6 in graphs:
        g = _nx_graph(g6)
        assert g.number_of_nodes() == 13
        assert any(d == 12 for _, d in g.degree())


def test_gadget_enumeration_matches_an_independent_count_of_admissible_x() -> None:
    g = _nx_graph(FIRST)
    admissible = []
    for x in g.nodes:
        h = g.copy()
        h.remove_node(x)
        nbrs = set(g[x])
        m = h.number_of_nodes()
        full = h.number_of_edges() == m * (m - 1) // 2
        if nx.is_connected(h) and not full and len(nbrs) != m and len(nbrs) >= 2:
            admissible.append(x)
    records, disagreements = MODULE.gadgets_of(FIRST)
    assert disagreements == 0
    assert sorted(r["x"] for r in records) == sorted(admissible)
    assert len(records) == 11  # hand count: 13 vertices minus the two universal ones
    assert all(r["m"] == 12 and r["n"] == 13 for r in records)


def test_mnh_recheck() -> None:
    n, adj = MODULE.decode(FIRST)
    assert MODULE.is_mnh(n, adj) is True
    # K4 is Hamiltonian, so not MNH
    n4, adj4 = MODULE.decode("C~")
    assert MODULE.is_mnh(n4, adj4) is False
    # an MNH graph minus an edge is never MNH (the removed pair no longer closes a Hamilton cycle)
    adj2 = [set(a) for a in adj]
    u = next(iter(adj2[0]))
    adj2[0].discard(u)
    adj2[u].discard(0)
    assert MODULE.is_mnh(n, adj2) is False


def test_canonical_form_separates_and_identifies() -> None:
    graphs = MODULE.load_order13()
    assert MODULE.pairwise_non_isomorphic(graphs[:20]) is True
    assert MODULE.pairwise_non_isomorphic([graphs[0], graphs[1], graphs[0]]) is False


def test_verification_helpers_on_known_small_graphs() -> None:
    # C5 plus one chord: circumference 5, Hamiltonian; the Petersen graph is hypohamiltonian: circumference 9
    c5 = [{1, 4}, {0, 2}, {1, 3}, {2, 4}, {3, 0}]
    assert MODULE.longest_cycle(c5)[0] == 5
    petersen = _nx_graph("IsP@OkWHG")
    adj = [set(petersen[v]) for v in range(10)]
    assert MODULE.longest_cycle(adj)[0] == 9
    assert MODULE.hamilton_path_dfs(c5, 0, 4) is True
    assert MODULE.hamilton_path_dfs(c5, 0, 2) is False


def test_dp_and_backtracking_agree_on_every_gadget_of_one_graph() -> None:
    _, disagreements = MODULE.gadgets_of(MODULE.load_order13()[5])
    assert disagreements == 0


def test_memoized_backtracking_equals_plain_backtracking_on_order_11_and_12_gadgets() -> None:
    lines = MODULE.read_graph6(MODULE.census_file(11))[:12] + MODULE.read_graph6(MODULE.census_file(12))[:12]
    for g6 in lines:
        memo, d1 = MODULE.gadgets_of(g6)
        plain, d2 = MODULE.gadgets_of(g6, MODULE.bt_invariants)
        assert d1 == 0 and d2 == 0
        assert memo == plain


def test_transposition_table_method_finds_zhans_known_positive() -> None:
    """Zhan's B_17 = A_18 - 18 (arXiv:2608.00957v3, built as in EXP-003 gate_zhan.py): d = 2, non-clique omitted set."""
    gamma = {1: [2, 3, 11, 15, 18], 2: [3, 14, 16], 3: [4, 5], 4: [5, 12, 17], 5: [6, 7, 11, 15], 6: [7],
             9: [10, 11], 10: [11], 11: [12, 13], 12: [13, 17], 13: [14, 15], 14: [15, 16], 15: [18]}
    verts = list(range(1, 19))
    edges = {(a, b) for a, bs in gamma.items() for b in bs} | {(8, v) for v in verts if v != 8}
    x = 18
    rest = [v for v in verts if v != x]
    idx = {v: i for i, v in enumerate(rest)}
    adj = [set() for _ in rest]
    for a, b in edges:
        if x in (a, b):
            continue
        adj[idx[a]].add(idx[b])
        adj[idx[b]].add(idx[a])
    n_set = sorted(idx[a if b == x else b] for a, b in edges if x in (a, b))
    assert sorted(rest[i] for i in n_set) == [1, 8, 15]
    memo = MODULE.bt_memo_invariants(len(rest), adj, n_set)
    dp = MODULE.dp_invariants(len(rest), adj, n_set)
    traceable, homog, _starts, d, nonclique = memo
    assert traceable and homog and d == 2 and nonclique is True
    assert tuple(memo) == tuple(dp)
