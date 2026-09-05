"""Deterministic finite controls for the first interior shell; see proof.md."""

from __future__ import annotations

import argparse
import hashlib
import itertools as it
import json
import runpy
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "EXP-001-tree-strip" / "run.py"
CHECK = runpy.run_path(str(BASE))
graph = CHECK["graph"]
edges_of = CHECK["edges_of"]
independent_number = CHECK["independent_number"]
subset_alpha = CHECK["subset_alpha"]
cut_connectivity = CHECK["cut_connectivity"]
flow_connectivity = CHECK["flow_connectivity"]


def complement(adj):
    full = (1 << len(adj)) - 1
    return [full ^ row ^ (1 << v) for v, row in enumerate(adj)]


def cycles(lengths):
    edges, offset = [], 0
    for length in lengths:
        edges.extend((offset + i, offset + (i + 1) % length) for i in range(length))
        offset += length
    return graph(offset, edges)


def harary(m, d):
    r = d // 2
    edges = {(min(i, (i + j) % m), max(i, (i + j) % m))
             for i in range(m) for j in range(1, r + 1)}
    high = None
    if d % 2:
        q = m // 2
        if m % 2:
            edges.update((i, i + q) for i in range(q + 1))
            high = q
        else:
            edges.update((i, i + q) for i in range(q))
    return graph(m, sorted(edges)), high


def add_complement_matching(adj, count, avoid=None):
    available = set(range(len(adj))) - ({avoid} if avoid is not None else set())
    result, added = list(adj), []
    for u, v in it.combinations(sorted(available), 2):
        if len(added) == count:
            break
        if u in available and v in available and not (adj[u] >> v & 1):
            result[u] |= 1 << v
            result[v] |= 1 << u
            available.difference_update((u, v))
            added.append((u, v))
    assert len(added) == count, (len(adj), count, avoid, added)
    return result, added


def lift(residual, misses):
    m = len(residual)
    return graph(m + len(misses), edges_of(residual) + [
        (m + s, t) for s, missing in enumerate(misses)
        for t in range(m) if t != missing
    ])


def construct(k, a):
    assert k >= 3 and 2 <= a <= k + 1
    m, n = k + 1, a + k + 1
    data = {"k": k, "alpha": a, "n": n, "epsilon": (n * k) % 2}
    if a == 2:
        data["case"] = "complement-cycle"
        return complement(cycles([n])), data
    if a == k + 1:
        data["case"] = "crown"
        return lift([0] * m, list(range(m))), data
    if a == k:
        data["case"] = "matching"
        residual = graph(m, [(2 * i, 2 * i + 1) for i in range((k + 1) // 2)])
        misses = [v for v, row in enumerate(residual) if row][:a]
    elif a == k - 1:
        data["case"] = "tree-strip"
        residual = graph(m, [(v, v + 1) for v in range(m - 1)])
        misses = list(range(1, m - 1))
    else:
        d = k - a
        base, high = harary(m, d)
        assert sorted(row.bit_count() for row in base) == (
            [d] * m if high is None else [d] * (m - 1) + [d + 1])
        count = (a + data["epsilon"] - (high is not None)) // 2
        residual, added = add_complement_matching(base, count, high)
        higher = [v for v, row in enumerate(residual) if row.bit_count() == d + 1]
        assert len(higher) == a + data["epsilon"]
        assert all(row.bit_count() in (d, d + 1) for row in residual)
        misses = higher[:a]
        data.update(case="harary", d=d, base_edges=edges_of(base),
                    exceptional_vertex=high, added_matching=added)
    data.update(residual_edges=edges_of(residual), misses=misses)
    return lift(residual, misses), data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "artifacts" / "certificate.json")
    args = parser.parse_args()
    result = {"schema": 1, "status": "running", "arithmetic": "exact integer combinatorics",
              "universal_proof": "proof.md; finite controls do not prove the theorem",
              "source_sha256": {p.parent.name + "/run.py": hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (Path(__file__), BASE)}, "cases": [], "controls": []}
    args.output.parent.mkdir(parents=True, exist_ok=True)

    def checkpoint():
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8", newline="\n")

    started = time.monotonic()
    for k in range(3, 7 if args.smoke else 13):
        for a in range(2, k + 2):
            if time.monotonic() - started > 300:
                result["status"] = "budget reached: partial finite evidence"
                checkpoint()
                raise TimeoutError("five-minute grid budget")
            adj, data = construct(k, a)
            degrees = [row.bit_count() for row in adj]
            assert sorted(degrees) == [k] * (len(adj) - data["epsilon"]) + [k + 1] * data["epsilon"]
            assert len(edges_of(adj)) == (len(adj) * k + 1) // 2
            assert independent_number(adj) == a
            assert flow_connectivity(adj, k)
            direct = len(adj) <= 16
            if direct:
                assert subset_alpha(adj) == a
                assert cut_connectivity(adj, k)
            if data["case"] == "harary":
                base = graph(k + 1, data["base_edges"])
                residual = graph(k + 1, data["residual_edges"])
                assert flow_connectivity(base, data["d"])
                assert cut_connectivity(base, data["d"])
                assert flow_connectivity(residual, data["d"])
                assert cut_connectivity(residual, data["d"])
            # Deliberately damage a degree-k vertex. Connectivity must fail.
            u = degrees.index(k)
            v = (adj[u] & -adj[u]).bit_length() - 1
            broken = list(adj)
            broken[u] ^= 1 << v
            broken[v] ^= 1 << u
            assert min(row.bit_count() for row in broken) < k
            assert not flow_connectivity(broken, k)
            if direct:
                assert not cut_connectivity(broken, k)
            data.update(edges=edges_of(adj), degrees=degrees, independent_number=a,
                        max_flow_check=True, direct_subset_and_cut_check=direct,
                        removed_edge_rejected=[u, v])
            result["cases"].append(data)
            checkpoint()
        print(f"k={k}: all {k} independence targets and damaged-edge controls PASS", flush=True)

    for lengths in ([3, 3], [4, 4], [4, 5], [5, 5], [5, 6], [6], [7], [8]):
        adj = complement(cycles(lengths))
        k = len(adj) - 3
        alpha_ok = independent_number(adj) == 2
        connectivity_ok = flow_connectivity(adj, k)
        assert connectivity_ok == cut_connectivity(adj, k)
        assert alpha_ok == (3 not in lengths)
        assert (alpha_ok and connectivity_ok) == all(length >= 5 for length in lengths)
        result["controls"].append({"complement_cycle_lengths": lengths, "alpha_two": alpha_ok,
                                   "k_connected": connectivity_ok})

    # Independently census all labeled order-six graphs against the cycle characterization.
    pairs = list(it.combinations(range(6), 2))
    accepted = expected = 0
    for mask in range(1 << len(pairs)):
        adj = graph(6, [edge for i, edge in enumerate(pairs) if mask >> i & 1])
        if any(row.bit_count() != 3 for row in adj):
            continue
        is_extremal = independent_number(adj) == 2 and flow_connectivity(adj, 3)
        inverse = complement(adj)
        is_cycle = all(row.bit_count() == 2 for row in inverse) and CHECK["connected"](inverse)
        assert is_extremal == is_cycle
        accepted += is_extremal
        expected += is_cycle
    assert accepted == expected == 60
    result["order_six_census"] = {"labeled_graphs": 32768, "extremals": accepted,
                                  "complements_of_six_cycles": expected}
    # Compare the independently regenerated count with the prior certified baseline.
    old = json.loads((BASE.parent / "artifacts" / "certificate.json").read_text())
    result["exp001_baseline_lf_sha256"] = hashlib.sha256(
        (BASE.parent / "artifacts" / "certificate.json").read_bytes().replace(b"\r\n", b"\n")
    ).hexdigest()
    assert old["status"] == "passed"
    assert old["base_census"]["extremals"] == accepted
    result["status"] = "PASS"
    result["summary"] = {"graphs": len(result["cases"]),
                         "direct_checks": sum(c["direct_subset_and_cut_check"] for c in result["cases"]),
                         "harary_cases": sum(c["case"] == "harary" for c in result["cases"]),
                         "odd_degree_sum_cases": sum(c["epsilon"] for c in result["cases"]),
                         "damaged_edge_controls": len(result["cases"]),
                         "cycle_controls": len(result["controls"])}
    checkpoint()
    print(json.dumps(result["summary"], sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
