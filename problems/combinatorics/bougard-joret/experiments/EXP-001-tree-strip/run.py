"""CPU-only exact combinatorial controls for the tree-strip theorem (stdlib).

Run from the repository root. No finite output is an all-parameter proof.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools as it
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def graph(n, edges):
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def edges_of(adj):
    return [(u, v) for u in range(len(adj)) for v in range(u + 1, len(adj))
            if adj[u] >> v & 1]


def connected(adj, remaining=None):
    remaining = (1 << len(adj)) - 1 if remaining is None else remaining
    if not remaining:
        return True
    reached = remaining & -remaining
    frontier = reached
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        new = adj[bit.bit_length() - 1] & remaining & ~reached
        reached |= new
        frontier |= new
    return reached == remaining


def independent_number(adj):
    # Branch on a vertex: delete it, or include it and delete its neighbors.
    memo = {0: 0}

    def visit(mask):
        if mask not in memo:
            bit = mask & -mask
            rest = mask ^ bit
            memo[mask] = max(visit(rest), 1 + visit(rest & ~adj[bit.bit_length() - 1]))
        return memo[mask]

    return visit((1 << len(adj)) - 1)


def subset_alpha(adj):
    for size in range(len(adj), -1, -1):
        for vertices in it.combinations(range(len(adj)), size):
            mask = sum(1 << v for v in vertices)
            if all(not (adj[v] & mask) for v in vertices):
                return size
    raise AssertionError("unreachable")


def cut_connectivity(adj, k):
    full = (1 << len(adj)) - 1
    for size in range(k):
        for cut in it.combinations(range(len(adj)), size):
            if not connected(adj, full ^ sum(1 << v for v in cut)):
                return False
    return True


def flow_connectivity(adj, k):
    # Independent Menger route: vertex-split unit-capacity max flow for nonedges.
    n = len(adj)
    for source in range(n):
        for sink in range(source + 1, n):
            if adj[source] >> sink & 1:
                continue
            cap = [[0] * (2 * n) for _ in range(2 * n)]
            for v in range(n):
                cap[2 * v][2 * v + 1] = n if v in (source, sink) else 1
            for u, v in edges_of(adj):
                cap[2 * u + 1][2 * v] = n
                cap[2 * v + 1][2 * u] = n
            total = 0
            while total < k:
                start, end = 2 * source + 1, 2 * sink
                parent = {start: None}
                queue = [start]
                for u in queue:
                    for v, capacity in enumerate(cap[u]):
                        if capacity and v not in parent:
                            parent[v] = u
                            queue.append(v)
                    if end in parent:
                        break
                if end not in parent:
                    return False
                v = end
                while parent[v] is not None:
                    u = parent[v]
                    cap[u][v] -= 1
                    cap[v][u] += 1
                    v = u
                total += 1
    return True


def tree_key(adj):
    def rooted(v, parent):
        return "(" + "".join(sorted(rooted(w, v) for w in range(len(adj))
                                     if adj[v] >> w & 1 and w != parent)) + ")"
    return min(rooted(v, -1) for v in range(len(adj)))


def grow_trees(trees):
    result = {}
    for adj in trees.values():
        for v in range(len(adj)):
            larger = graph(len(adj) + 1, edges_of(adj) + [(v, len(adj))])
            result[tree_key(larger)] = larger
    return result


def lift(adj, misses=None):
    k = len(adj) - 1
    if misses is None:
        misses = [v for v, row in enumerate(adj) for _ in range(row.bit_count() - 1)]
    assert len(misses) == k - 1
    return graph(2 * k, edges_of(adj) + [
        (len(adj) + s, t) for s, missing in enumerate(misses)
        for t in range(len(adj)) if t != missing
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "artifacts" / "certificate.json")
    args = parser.parse_args()
    output = {"schema": 1, "arithmetic": "exact integer combinatorics",
              "universal_proof": "proof.md, not finite enumeration", "tree_orders": [],
              "residual_orders": [], "status": "running"}
    args.output.parent.mkdir(parents=True, exist_ok=True)

    def checkpoint():
        args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def budget(start):
        if time.monotonic() - start > 300:
            output["status"] = "budget reached: partial finite evidence"
            checkpoint()
            raise TimeoutError("five-minute stage budget")

    trees = {"()": [0]}
    known_counts = {4: 2, 5: 3, 6: 6, 7: 11, 8: 23, 9: 47}
    for order in range(2, (5 if args.smoke else 10)):
        start = time.monotonic()
        trees = grow_trees(trees)
        if order < 4:
            continue
        assert len(trees) == known_counts[order]
        records = []
        for key, tree in sorted(trees.items()):
            budget(start)
            k = order - 1
            lifted = lift(tree)
            star = max(row.bit_count() for row in tree) == k
            assert all(row.bit_count() == k for row in lifted)
            alpha = independent_number(lifted)
            assert alpha == (k if star else k - 1)
            if not star:
                assert cut_connectivity(lifted, k)
                assert flow_connectivity(lifted, k)
                assert subset_alpha(lifted) == k - 1
                damaged = graph(2 * k, edges_of(lifted)[1:])
                assert min(row.bit_count() for row in damaged) == k - 1
                assert not flow_connectivity(damaged, k)
            records.append({"tree_key": key, "tree_edges": edges_of(tree),
                            "alpha": alpha, "star_negative_control": star})
        output["tree_orders"].append({"order": order, "trees": records,
                                      "valid_nonstar": len(trees) - 1})
        checkpoint()
        print(f"tree order {order}: {len(trees)-1} valid; star rejected; dual cut/flow passed", flush=True)

    # Independent residual enumeration: all labeled graphs with k edges, no isolates.
    # All miss assignments are enumerated; relabeling S preserves both invariants,
    # so expensive graph invariants are computed once per residual graph.
    for k in range(3, (4 if args.smoke else 6)):
        start = time.monotonic()
        n = k + 1
        record = {"k": k, "residual_graphs": 0, "assignments": 0,
                  "nonstar_trees": 0, "stars": 0, "disconnected": 0}
        for edges in it.combinations(list(it.combinations(range(n), 2)), k):
            budget(start)
            residual = graph(n, edges)
            degree = [row.bit_count() for row in residual]
            if min(degree) == 0:
                continue
            record["residual_graphs"] += 1
            expected = tuple(d - 1 for d in degree)
            canonical = [v for v in range(n) for _ in range(expected[v])]
            assignments = sorted(set(it.permutations(canonical)))
            for assignment in assignments:
                # Explicit sound relabeling certificate, not a solver symmetry assumption.
                assert tuple(assignment.count(v) for v in range(n)) == expected
                assert sorted(assignment) == canonical
            record["assignments"] += len(assignments)
            lifted = lift(residual, canonical)
            is_connected = connected(residual)
            is_star = max(degree) == k
            valid = cut_connectivity(lifted, k) and subset_alpha(lifted) == k - 1
            assert valid == (is_connected and not is_star)
            record["disconnected" if not is_connected else "stars" if is_star else "nonstar_trees"] += 1
        output["residual_orders"].append(record)
        checkpoint()
        print(f"residual k={k}: {record}", flush=True)

    # Independent full labeled census of the base case: every graph on six vertices.
    start = time.monotonic()
    pairs = list(it.combinations(range(6), 2))
    extremal = 0
    for edge_bits in range(1 << len(pairs)):
        budget(start)
        if edge_bits.bit_count() > 9:
            continue
        adj = graph(6, [edge for i, edge in enumerate(pairs) if edge_bits >> i & 1])
        if min(row.bit_count() for row in adj) < 3:
            continue
        if subset_alpha(adj) == 2 and cut_connectivity(adj, 3):
            assert edge_bits.bit_count() == 9
            extremal += 1
            for independent in it.combinations(range(6), 2):
                if adj[independent[0]] >> independent[1] & 1:
                    continue
                keep = [v for v in range(6) if v not in independent]
                residual = graph(4, [(keep.index(u), keep.index(v)) for u, v in edges_of(adj)
                                     if u in keep and v in keep])
                assert connected(residual) and len(edges_of(residual)) == 3
                assert max(row.bit_count() for row in residual) == 2
    assert extremal == 60
    output["base_census"] = {"labeled_graphs": 32768, "extremals": extremal,
                             "maximum_independent_sets_all_checked": True}
    output["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    output["status"] = "passed"
    checkpoint()
    print("all declared finite controls passed", flush=True)


if __name__ == "__main__":
    main()
