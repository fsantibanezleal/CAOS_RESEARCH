"""Independent NetworkX audit of persisted EXP-002 graphs; imports no CAOS checker.

Replay with ``python audit.py``. This verifies finite objects, not the universal
theorem. NetworkX node connectivity uses a separate flow implementation, and
independence is computed as maximum clique size in the complement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def from_edges(order, edges):
    assert all(len(edge) == 2 and 0 <= edge[0] < edge[1] < order for edge in edges)
    assert len(edges) == len(set(map(tuple, edges)))
    graph = nx.Graph()
    graph.add_nodes_from(range(order))
    graph.add_edges_from(edges)
    assert graph.number_of_edges() == len(edges)
    return graph


def independence(graph):
    return max(map(len, nx.find_cliques(nx.complement(graph))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/independent-audit.json")
    args = parser.parse_args()
    certificate_path = HERE / "artifacts/certificate.json"
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    assert certificate["status"] == "PASS"
    source_hashes = certificate["source_sha256"]
    assert set(source_hashes) == {"EXP-001-tree-strip/run.py", "EXP-002-next-shell/run.py"}
    for name, expected in source_hashes.items():
        assert digest(HERE.parent / name) == expected, (name, "source hash mismatch")
    assert len(certificate["cases"]) == 75
    assert {(case["k"], case["alpha"]) for case in certificate["cases"]} == {
        (k, a) for k in range(3, 13) for a in range(2, k + 2)
    }
    rows = []
    harary_count = 0
    odd_count = 0
    for case in certificate["cases"]:
        k, a, n = case["k"], case["alpha"], case["n"]
        assert n == a + k + 1
        graph = from_edges(n, case["edges"])
        epsilon = (n * k) % 2
        assert epsilon == case["epsilon"]
        degrees = [graph.degree(v) for v in range(n)]
        assert degrees == case["degrees"]
        assert sorted(degrees) == [k] * (n - epsilon) + [k + 1] * epsilon
        assert graph.number_of_edges() == (n * k + 1) // 2
        alpha = independence(graph)
        connectivity = nx.node_connectivity(graph)
        assert alpha == a
        assert connectivity == k
        removed = case["removed_edge_rejected"]
        assert graph.has_edge(*removed)
        damaged = graph.copy()
        damaged.remove_edge(*removed)
        damaged_connectivity = nx.node_connectivity(damaged)
        assert damaged_connectivity < k
        row = {"k": k, "alpha": alpha, "n": n, "connectivity": connectivity,
               "edges": graph.number_of_edges(), "epsilon": epsilon,
               "damaged_connectivity": damaged_connectivity}
        if case["case"] == "harary":
            base = from_edges(k + 1, case["base_edges"])
            residual = from_edges(k + 1, case["residual_edges"])
            base_connectivity = nx.node_connectivity(base)
            residual_connectivity = nx.node_connectivity(residual)
            assert base_connectivity == case["d"]
            assert residual_connectivity >= case["d"]
            row.update(base_connectivity=base_connectivity,
                       residual_connectivity=residual_connectivity)
            harary_count += 1
        odd_count += epsilon
        rows.append(row)
    assert harary_count == 36
    assert odd_count == 15
    controls = []
    assert len(certificate["controls"]) == 8
    for control in certificate["controls"]:
        lengths = control["complement_cycle_lengths"]
        graph = nx.complement(nx.disjoint_union_all([nx.cycle_graph(n) for n in lengths]))
        alpha_two = independence(graph) == 2
        k_connected = nx.node_connectivity(graph) >= len(graph) - 3
        assert alpha_two == control["alpha_two"]
        assert k_connected == control["k_connected"]
        assert (alpha_two and k_connected) == all(length >= 5 for length in lengths)
        controls.append({"cycle_lengths": lengths, "alpha_two": alpha_two,
                         "k_connected": k_connected})
    result = {
        "schema": 1, "status": "PASS", "networkx_version": nx.__version__,
        "certificate_sha256": digest(certificate_path),
        "audit_source_sha256": digest(Path(__file__)),
        "proof_sha256": digest(HERE / "proof.md"),
        "checked_source_sha256": source_hashes,
        "method": "Raw edge lists; NetworkX node_connectivity; complement maximal cliques",
        "scope": "Finite 75-case verification; not formal proof, peer review, or novelty certification",
        "summary": {"graphs": len(rows), "harary_bases": harary_count,
                    "odd_degree_sum_cases": odd_count, "damaged_edge_controls": len(rows),
                    "cycle_controls": len(controls)},
        "cases": rows, "cycle_controls": controls,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
