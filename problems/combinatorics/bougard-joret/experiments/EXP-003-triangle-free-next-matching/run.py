"""CPU-only exact finite controls; the uniform theorem is proved in proof.md."""

from __future__ import annotations

import argparse
import hashlib
import itertools as it
import json
import runpy
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "EXP-001-tree-strip/run.py"
CHECK = runpy.run_path(str(BASE))
graph, edges_of = CHECK["graph"], CHECK["edges_of"]


def crown_edges(d):
    p = d + 1
    return {(i, p + j) for i in range(p) for j in range(p) if i != j}


def construction(d, kind):
    p, v = d + 1, 2 * d + 2
    edges = crown_edges(d)
    if kind == "known-extremizer":
        edges.difference_update(((0, p + 1), (1, p)))
        edges.update((u, v) for u in (0, 1, p, p + 1))
    else:
        assert kind == "subdivided-crown"
        edges.remove((0, p + 1))
        edges.update(((0, v), (p + 1, v)))
    return graph(v + 1, sorted(edges))


def complement(adj):
    full = (1 << len(adj)) - 1
    return [full ^ row ^ (1 << v) for v, row in enumerate(adj)]


def triangle_free(adj):
    return all(not (adj[u] & adj[v]) for u, v in edges_of(adj))


def equality_types(sizes, d):
    adjacent = [sizes[(i - 1) % 5] + sizes[(i + 1) % 5] for i in range(5)]
    return all(b <= d and (sizes[i] == 1 or b == d) for i, b in enumerate(adjacent))


def blowup_cycle(sizes):
    groups, offset = [], 0
    for size in sizes:
        groups.append(list(range(offset, offset + size)))
        offset += size
    edges = [(u, v) for i in range(5) for u in groups[i] for v in groups[(i + 1) % 5]]
    return graph(offset, edges)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/certificate.json")
    args = parser.parse_args()
    result = {"schema": 1, "status": "running", "arithmetic": "exact integer combinatorics",
              "scope": "finite controls, not a universal proof or an arbitrary-order census",
              "source_sha256": {p.parent.name + "/run.py": hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (Path(__file__), BASE)}, "degrees": []}
    args.output.parent.mkdir(parents=True, exist_ok=True)

    def checkpoint():
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n",
                               encoding="utf-8", newline="\n")

    started = time.monotonic()
    for d in range(7, 10 if args.smoke else 31):
        if time.monotonic() - started > 300:
            result["status"] = "budget reached; partial finite evidence"
            checkpoint()
            raise TimeoutError("five-minute stage budget")
        n, p, k = 2 * d + 3, d + 1, d + 2
        record = {"d": d, "matching_budget": p, "n": n, "graphs": []}
        for kind in ("known-extremizer", "subdivided-crown"):
            adj = construction(d, kind)
            expected = d * d + d + (2 if kind == "known-extremizer" else 1)
            assert len(edges_of(adj)) == expected
            assert triangle_free(adj)
            assert [r.bit_count() for r in adj] == [d] * (n - 1) + [4 if kind == "known-extremizer" else 2]
            matching = [(i, p + (i + 2) % p) for i in range(p)]
            assert all(adj[u] >> v & 1 for u, v in matching)
            assert len({u for edge in matching for u in edge}) == 2 * p
            inverse = complement(adj)
            # Triangle-free plus a witnessed edge certifies complement independence exactly two.
            assert edges_of(adj)
            checked = d <= 18
            if checked:
                assert CHECK["independent_number"](inverse) == 2
                assert CHECK["flow_connectivity"](inverse, k) == (kind == "subdivided-crown")
            failure_cut = None
            if kind == "known-extremizer":
                common = adj[0] & adj[1]
                assert common.bit_count() == d
                surviving = common | 3
                failure_cut = [i for i in range(n) if not (surviving >> i & 1)]
                assert len(failure_cut) == d + 1
                assert not CHECK["connected"](inverse, surviving)
            record["graphs"].append({"kind": kind, "edges": edges_of(adj),
                                      "edge_count": expected, "degrees": [r.bit_count() for r in adj],
                                      "matching": matching, "triangle_free": True,
                                      "complement_edges": n * (n - 1) // 2 - expected,
                                      "complement_flow_checked": checked,
                                      "rejected_complement_cut": failure_cut})

        # Equality forces at least one singleton type. Rotate it to position zero.
        candidates = surviving_types = 0
        for dividers in it.combinations(range(1, 2 * d + 2), 3):
            a, b, c = dividers
            sizes = (1, a, b - a, c - b, 2 * d + 2 - c)
            assert sum(sizes) == n and min(sizes) >= 1
            candidates += 1
            surviving_types += equality_types(sizes, d)
        assert surviving_types == 0
        record.update(equality_type_candidates=candidates, equality_type_survivors=surviving_types,
                      bougard_lower=d * d + 4 * d + 1, bougard_upper=d * d + 4 * d + 2,
                      excess_lower=d // 2 - 2)
        result["degrees"].append(record)
        checkpoint()
        print(f"d={d}: both witnesses, rejected cut, {candidates} type constraints PASS", flush=True)

    boundary = blowup_cycle([3] * 5)
    assert triangle_free(boundary) and all(row.bit_count() == 6 for row in boundary)
    assert len(edges_of(boundary)) == 45 > 6 * 6 + 6 + 2
    assert equality_types([3] * 5, 6)
    corrupted = construction(7, "known-extremizer")
    corrupted[0] |= 1 << 1
    corrupted[1] |= 1
    assert not triangle_free(corrupted)
    result["boundary_control"] = {"d": 6, "type_sizes": [3] * 5, "edges": edges_of(boundary),
                                  "edge_count": 45, "proposed_formula": 44,
                                  "outside_theorem_range": True}
    result["triangle_corruption_rejected"] = True
    result["status"] = "PASS"
    result["summary"] = {"degrees": len(result["degrees"]), "graphs": 2 * len(result["degrees"]),
                         "flow_checked_graphs": 2 * sum(r["d"] <= 18 for r in result["degrees"]),
                         "equality_type_candidates": sum(r["equality_type_candidates"] for r in result["degrees"]),
                         "equality_type_survivors": 0,
                         "rejected_complement_cuts": len(result["degrees"])}
    checkpoint()
    print(json.dumps(result["summary"], sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
