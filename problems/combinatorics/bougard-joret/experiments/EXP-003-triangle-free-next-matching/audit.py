"""Independent finite NetworkX audit; imports no CAOS graph/checker code.

Requires the adjacent EXP-002 requirements-audit.txt (networkx==3.4.1).
Run after proof.md is present. Finite verification is not a universal proof.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent


def digest(path):
    """Bind text artifacts independent of checkout CRLF conversion."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def reconstruct(n, edges):
    assert all(len(e) == 2 and 0 <= e[0] < e[1] < n for e in edges)
    assert len(edges) == len(set(map(tuple, edges)))
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(edges)
    return g


def main():
    assert nx.__version__ == "3.4.1"
    certificate_path = HERE / "artifacts/certificate.json"
    proof_path = HERE / "proof.md"
    assert proof_path.is_file(), "proof.md must exist before final audit"
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    assert certificate["status"] == "PASS"
    # Validate upstream raw-byte bindings without importing their implementations.
    for name, expected in certificate["source_sha256"].items():
        assert hashlib.sha256((HERE.parent / name).read_bytes()).hexdigest() == expected
    assert [r["d"] for r in certificate["degrees"]] == list(range(7, 31))
    rows = []
    for record in certificate["degrees"]:
        d, n, k = record["d"], 2 * record["d"] + 3, record["d"] + 2
        assert record["n"] == n and record["matching_budget"] == d + 1
        assert sorted(g["kind"] for g in record["graphs"]) == ["known-extremizer", "subdivided-crown"]
        for saved in record["graphs"]:
            kind = saved["kind"]
            g = reconstruct(n, saved["edges"])
            assert sum(nx.triangles(g).values()) == 0
            assert [g.degree(v) for v in range(n)] == [d] * (n - 1) + [4 if kind == "known-extremizer" else 2]
            assert saved["degrees"] == [g.degree(v) for v in range(n)]
            expected_edges = d * d + d + (2 if kind == "known-extremizer" else 1)
            assert g.number_of_edges() == expected_edges == saved["edge_count"]
            matching = nx.max_weight_matching(g, maxcardinality=True)
            assert len(matching) == d + 1
            inverse = nx.complement(g)
            assert inverse.number_of_edges() == saved["complement_edges"]
            alpha = max(map(len, nx.find_cliques(nx.complement(inverse))))
            assert alpha == 2
            connectivity = nx.node_connectivity(inverse)
            cut = saved["rejected_complement_cut"]
            if kind == "subdivided-crown":
                assert connectivity == k and cut is None
            else:
                assert connectivity < k
                assert len(cut) == len(set(cut)) == d + 1
                assert set(cut) <= set(inverse)
                assert not nx.is_connected(inverse.subgraph(set(inverse) - set(cut)))
            rows.append({"d": d, "kind": kind, "matching_number": len(matching),
                         "complement_alpha": alpha, "complement_connectivity": connectivity,
                         "rejected_cut_checked": cut is not None, "edge_count": expected_edges})
        print(f"d={d}: two NetworkX matching/clique/connectivity audits PASS", flush=True)

    boundary = certificate["boundary_control"]
    control = reconstruct(15, boundary["edges"])
    assert not any(nx.triangles(control).values())
    assert set(dict(control.degree()).values()) == {6}
    assert control.number_of_edges() == 45 > 44 == boundary["proposed_formula"]
    damaged = reconstruct(17, certificate["degrees"][0]["graphs"][0]["edges"])
    assert not damaged.has_edge(0, 1)
    damaged.add_edge(0, 1)
    assert any(nx.triangles(damaged).values())

    # All positive five-part compositions, without fixing a singleton position.
    # Construct each quotient's degree/deficit conditions independently.
    types = []
    for d in range(7, 11):
        n, count, singleton_count, survivors = 2 * d + 3, 0, 0, []
        for cuts in itertools.combinations(range(1, n), 4):
            endpoints = (0,) + cuts + (n,)
            sizes = [b - a for a, b in zip(endpoints, endpoints[1:])]
            count += 1
            if 1 not in sizes:
                continue
            singleton_count += 1
            quotient = nx.cycle_graph(5)
            degrees = {v: sum(sizes[w] for w in quotient[v]) for v in quotient}
            if max(degrees.values()) <= d and all(sizes[v] == 1 or degrees[v] == d for v in quotient):
                survivors.append(sizes)
        assert not survivors
        types.append({"d": d, "all_positive_compositions": count,
                      "compositions_with_singletons": singleton_count, "survivors": survivors})

    result = {"schema": 1, "status": "PASS", "networkx_version": nx.__version__,
              "scope": "Independent finite saved-graph audit; not a uniform theorem or arbitrary-graph census",
              "hash_normalization": "UTF-8 source bytes with CRLF replaced by LF",
              "sha256_lf": {"certificate.json": digest(certificate_path), "proof.md": digest(proof_path),
                            "audit.py": digest(Path(__file__)), "run.py": digest(HERE / "run.py")},
              "graphs": rows, "five_type_controls": types,
              "boundary_d6_edges": 45, "boundary_exceeds_formula": True,
              "triangle_corruption_rejected": True,
              "summary": {"graphs": len(rows), "full_connectivity_checks": len(rows),
                          "matching_checks": len(rows), "clique_checks": len(rows),
                          "rejected_cuts": sum(r["rejected_cut_checked"] for r in rows)}}
    output = HERE / "artifacts/independent-audit.json"
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
