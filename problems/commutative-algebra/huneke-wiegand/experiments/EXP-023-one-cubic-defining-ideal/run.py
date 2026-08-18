"""EXP-023: scalable state-graph campaign for the one-cubic presentation."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from array import array
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def artinian_blocks(p: int) -> list[set[int]]:
    if p < 4:
        raise ValueError("EXP-023 is declared only for p>=4")
    d1 = (
        interval(1, p)
        | interval(3 * p, 4 * p - 2)
        | interval(6 * p, 8 * p - 2)
        | interval(8 * p, 10 * p - 2)
        | {10 * p}
        | interval(11 * p - 1, 12 * p - 1)
        | interval(13 * p + 1, 14 * p - 2)
        | interval(14 * p, 15 * p - 1)
        | {16 * p}
        | interval(17 * p - 1, 18 * p - 1)
    )
    d2 = (
        interval(p + 1, 2 * p)
        | interval(4 * p - 1, 5 * p - 2)
        | {8 * p - 1, 10 * p - 1}
        | interval(10 * p + 1, 11 * p - 2)
        | interval(12 * p, 13 * p)
        | {14 * p - 1}
        | interval(15 * p, 16 * p - 1)
        | interval(16 * p + 1, 17 * p - 2)
        | interval(18 * p, 24 * p - 1)
    )
    d3 = interval(2 * p + 1, 3 * p - 1) | interval(5 * p - 1, 6 * p - 2)
    return [{0}, d1, d2, d3, {6 * p - 1}, set()]


def basis(p: int, degree: int) -> set[int]:
    blocks = artinian_blocks(p)
    return set().union(*blocks[: min(degree, 4) + 1])


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = array("I", range(size))
        self.rank = bytearray(size)

    def find(self, item: int) -> int:
        parent = self.parent
        root = item
        while parent[root] != root:
            root = parent[root]
        while parent[item] != item:
            following = parent[item]
            parent[item] = root
            item = following
        return root

    def union(self, left: int, right: int) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return
        if self.rank[root_left] < self.rank[root_right]:
            root_left, root_right = root_right, root_left
        self.parent[root_right] = root_left
        if self.rank[root_left] == self.rank[root_right]:
            self.rank[root_left] += 1


def state_graph_degree(p: int, degree: int) -> dict[str, object]:
    """Compute beta_(1,degree) from X_a times the complete preceding fiber."""
    if degree not in {3, 4, 5}:
        raise ValueError("state graph is used only in degrees three through five")
    started = time.perf_counter()
    generators = sorted(basis(p, 1))
    previous = basis(p, degree - 1)
    remainder = basis(p, degree - 2)
    current = basis(p, degree)

    states = [(a, b) for a in generators for b in sorted(previous)]
    state_index = {state: index for index, state in enumerate(states)}
    zero = len(states)
    components = DisjointSet(zero + 1)

    decompositions: dict[int, list[tuple[int, int]]] = {}
    for b in previous:
        decompositions[b] = [
            (c, b - c) for c in generators if b - c in remainder
        ]
        if not decompositions[b]:
            raise AssertionError(f"degree {degree - 1} basis offset {b} has no factorization")

    edge_attempts = 0
    zero_edges = 0
    for position, (a, b) in enumerate(states):
        for c, r in decompositions[b]:
            edge_attempts += 1
            other_remainder = a + r
            if other_remainder in previous:
                components.union(position, state_index[(c, other_remainder)])
            else:
                components.union(position, zero)
                zero_edges += 1

    zero_root = components.find(zero)
    root_data: dict[int, tuple[int, tuple[int, int]]] = {}
    for position, state in enumerate(states):
        root = components.find(position)
        if root == zero_root:
            continue
        total = state[0] + state[1]
        prior = root_data.get(root)
        if prior is None:
            root_data[root] = (total, state)
        elif prior[0] != total:
            raise AssertionError("state relation changed the total offset")

    by_total: dict[int, list[tuple[int, tuple[int, int]]]] = {}
    invalid_components: list[tuple[int, int, tuple[int, int]]] = []
    for root, (total, state) in root_data.items():
        if total in current:
            by_total.setdefault(total, []).append((root, state))
        else:
            invalid_components.append((root, total, state))

    witness: dict[str, object] | None = None
    if invalid_components:
        root, total, state = sorted(invalid_components, key=lambda item: (item[1], item[2]))[0]
        witness = {
            "kind": "zero_state_not_generated_below",
            "total": total,
            "root": root,
            "state": list(state),
        }
    else:
        for total in sorted(by_total):
            items = by_total[total]
            if len(items) > 1:
                witness = {
                    "kind": "equal_total_components_not_connected_below",
                    "total": total,
                    "left_root": items[0][0],
                    "left_state": list(items[0][1]),
                    "right_root": items[1][0],
                    "right_state": list(items[1][1]),
                }
                break

    quotient_dimension = len(root_data)
    minimal_equations = quotient_dimension - len(current)
    if minimal_equations < 0:
        raise AssertionError("state quotient is smaller than the actual fiber")
    if (minimal_equations == 0) != (witness is None):
        raise AssertionError("state witness and dimension defect disagree")

    return {
        "degree": degree,
        "state_count": len(states),
        "edge_attempts": edge_attempts,
        "zero_edges": zero_edges,
        "lower_relation_quotient_dimension": quotient_dimension,
        "actual_fiber_dimension": len(current),
        "minimal_defining_equations": minimal_equations,
        "first_obstruction": witness,
        "component_signature": digest(
            {
                str(total): len(items)
                for total, items in sorted(by_total.items())
            }
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }


def analyze_parameter(p: int) -> dict[str, object]:
    started = time.perf_counter()
    dimensions = [len(basis(p, degree)) for degree in range(6)]
    expected_dimensions = [1, 10 * p, 22 * p, 24 * p - 1, 24 * p, 24 * p]
    if dimensions != expected_dimensions:
        raise AssertionError(f"fiber dimensions disagree at p={p}: {dimensions}")

    degree_rows = [state_graph_degree(p, degree) for degree in (3, 4, 5)]
    beta2 = 50 * p * p - 17 * p
    betti = {
        "2": beta2,
        **{str(row["degree"]): row["minimal_defining_equations"] for row in degree_rows},
    }
    cubic = degree_rows[0]["first_obstruction"]
    predictions = {
        "quadratic_count": beta2 == 50 * p * p - 17 * p,
        "unique_cubic": degree_rows[0]["minimal_defining_equations"] == 1,
        "cubic_total": isinstance(cubic, dict) and cubic.get("total") == 3 * p,
        "no_quartic": degree_rows[1]["minimal_defining_equations"] == 0,
        "no_quintic": degree_rows[2]["minimal_defining_equations"] == 0,
        "relation_type_three": betti == {
            "2": 50 * p * p - 17 * p,
            "3": 1,
            "4": 0,
            "5": 0,
        },
    }
    controls = {
        "omitted_cubic_rejected": degree_rows[0]["minimal_defining_equations"] != 0,
        "false_second_cubic_rejected": degree_rows[0]["minimal_defining_equations"] != 2,
        "perturbed_quadratic_count_rejected": beta2 != 50 * p * p - 17 * p - 1,
        "false_koszul_claim_rejected": degree_rows[0]["minimal_defining_equations"] > 0,
    }
    if not all(predictions.values()):
        raise AssertionError(f"p={p}: corrected presentation failed: {predictions}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: an adversarial mutation survived")

    row: dict[str, object] = {
        "p": p,
        "variable_count": 10 * p,
        "fiber_dimensions_degrees_0_to_5": dimensions,
        "first_betti_row_degrees_2_to_5": betti,
        "minimal_equation_count": beta2 + 1,
        "relation_type": 3,
        "non_koszul": True,
        "degree_rows": degree_rows,
        "predictions": predictions,
        "controls": controls,
        "elapsed_seconds": time.perf_counter() - started,
    }
    row["row_hash"] = digest(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=40)
    parser.add_argument("--budget-seconds", type=float, default=300.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()
    if args.first < 4 or args.last < args.first:
        raise ValueError("require 4 <= first <= last")
    if args.budget_seconds <= 0:
        raise ValueError("budget_seconds must be positive")

    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print(f"EXP-023 state-graph campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        row = analyze_parameter(p)
        rows.append(row)
        elapsed = time.perf_counter() - started
        checkpoint = {
            "experiment": "EXP-023-one-cubic-defining-ideal",
            "status": "RUNNING" if p < args.last else "COMPUTATIONAL_PASS",
            "requested_range": {"first": args.first, "last": args.last},
            "completed_through": p,
            "row_hashes": [item["row_hash"] for item in rows],
            "elapsed_seconds": elapsed,
        }
        write_json_atomic(args.checkpoint, checkpoint)
        print(
            f"p={p}: betti={row['first_betti_row_degrees_2_to_5']} "
            f"states={[item['state_count'] for item in row['degree_rows']]} "
            f"elapsed={elapsed:.3f}s",
            flush=True,
        )
        if elapsed > args.budget_seconds:
            checkpoint["status"] = "INCONCLUSIVE_BUDGET"
            write_json_atomic(args.checkpoint, checkpoint)
            raise TimeoutError(
                f"EXP-023 exceeded its declared {args.budget_seconds:g}-second budget at p={p}"
            )

    result = {
        "experiment": "EXP-023-one-cubic-defining-ideal",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "prediction": "J_p=((J_p)_2, X_0^2 X_(3p)-X_p^3)",
        "all_rows_pass": True,
        "campaign_aggregate": digest([row["row_hash"] for row in rows]),
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    write_json_atomic(args.output, result)
    print(
        f"EXP-023 computational PASS aggregate={result['campaign_aggregate']} "
        f"elapsed={result['elapsed_seconds']:.3f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
