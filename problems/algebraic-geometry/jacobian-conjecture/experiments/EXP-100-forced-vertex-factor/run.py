"""EXP-100: exact forced-vertex factor and residual common-flag gate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections import deque
from pathlib import Path

from sympy import Matrix, Rational


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
EXP099_RUN = ROOT.parent / "EXP-099-augmented-minor-flag" / "run.py"


def load_exp099():
    spec = importlib.util.spec_from_file_location("exp099_matrix", EXP099_RUN)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load EXP-099 matrix reconstruction")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def record(condition: bool, message: str) -> bool:
    print(f"[{'PASS' if condition else 'REFUTED'}] {message}", flush=True)
    return condition


def topological_order(adjacency: list[set[int]]):
    indegree = [0] * len(adjacency)
    for targets in adjacency:
        for target in targets:
            indegree[target] += 1
    queue = deque(index for index, degree in enumerate(indegree) if degree == 0)
    order: list[int] = []
    while queue:
        source = queue.popleft()
        order.append(source)
        for target in sorted(adjacency[source]):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return order if len(order) == len(adjacency) else None


def shortest_cycle(adjacency: list[set[int]]) -> list[int] | None:
    for source, targets in enumerate(adjacency):
        if source in targets:
            return [source, source]
    best = None
    for start in range(len(adjacency)):
        queue = deque([start])
        parent = {start: None}
        while queue:
            current = queue.popleft()
            for target in sorted(adjacency[current]):
                if target == start:
                    path = [current]
                    while path[-1] != start:
                        previous = parent[path[-1]]
                        if previous is None:
                            break
                        path.append(previous)
                    cycle = list(reversed(path)) + [start]
                    if best is None or len(cycle) < len(best):
                        best = cycle
                    queue.clear()
                    break
                if target not in parent:
                    parent[target] = current
                    queue.append(target)
    return best


def main() -> None:
    source = load_exp099()
    zero = [Rational(0)] * len(source.LOWER)
    augmented_base, base_row_labels = source.augmented_matrix(zero)

    _, row_pivots = augmented_base.T.rref()
    selected_row_indices = list(row_pivots)[:125]
    selected_row_labels = [base_row_labels[index] for index in selected_row_indices]
    row_block = augmented_base[selected_row_indices, :]
    _, column_pivots = row_block.rref()
    selected_columns = list(column_pivots)[:125]
    rhs_column = len(source.NQ)
    if rhs_column not in selected_columns:
        selected_columns = selected_columns[:124] + [rhs_column]

    base = source.selected_square(zero, selected_row_labels, selected_columns)
    base_det = base.det(method="domain-ge")
    require(base.shape == (125, 125) and base_det != 0, "the EXP-099 base minor reconstructs")
    base_inverse = base.inv()

    normalized: list[Matrix] = []
    directions: list[Matrix] = []
    for parameter_index in range(len(source.LOWER)):
        values = list(zero)
        values[parameter_index] = Rational(1)
        direction = (
            source.selected_square(values, selected_row_labels, selected_columns) - base
        )
        directions.append(direction)
        normalized.append(base_inverse * direction)

    constant_index = source.LOWER.index((0, 0))
    forced_index = source.LOWER.index((1, 0))
    constant_matrix = normalized[constant_index]
    forced_matrix = normalized[forced_index]

    constant_zero = record(
        constant_matrix == Matrix.zeros(125),
        "the (0,0) bracket direction is exactly zero",
    )
    forced_idempotent = record(
        forced_matrix * forced_matrix == forced_matrix,
        "the normalized (1,0) direction is idempotent",
    )
    forced_rank = forced_matrix.rank()
    forced_trace = forced_matrix.trace()
    forced_rank_trace = record(
        forced_rank == 16 and forced_trace == 16,
        f"the forced-vertex projector has rank {forced_rank} and trace {forced_trace}",
    )

    factor_checks = {}
    for value in (
        Rational(-2),
        Rational(-1),
        Rational(1, 2),
        Rational(1),
        Rational(3),
    ):
        determinant = (base + value * directions[forced_index]).det(method="domain-ge")
        expected = base_det * (1 + value) ** 16
        factor_checks[str(value)] = {
            "determinant": str(determinant),
            "expected": str(expected),
            "equal": determinant == expected,
        }
        record(
            determinant == expected,
            f"forced-axis determinant at u={value} equals det(A0)*(1+u)^16",
        )

    remaining_indices = [
        index
        for index, point in enumerate(source.LOWER)
        if point not in {(0, 0), (1, 0)}
    ]
    require(len(remaining_indices) == 24, "24 effective directions remain after normalization")

    adjacency = [set() for _ in range(base.rows)]
    edge_labels: dict[tuple[int, int], list[int]] = {}
    for parameter_index in remaining_indices:
        matrix = normalized[parameter_index]
        for row in range(matrix.rows):
            for column in range(matrix.cols):
                if matrix[row, column] != 0:
                    adjacency[column].add(row)
                    edge_labels.setdefault((column, row), []).append(parameter_index)

    order = topological_order(adjacency)
    acyclic = order is not None
    strict_flag = False
    if order is not None:
        position = {node: index for index, node in enumerate(order)}
        strict_flag = all(
            position[source_node] < position[target]
            for source_node, targets in enumerate(adjacency)
            for target in targets
        )
    record(acyclic and strict_flag, "the remaining 24 directions preserve one common strict flag")

    cycle = None if acyclic else shortest_cycle(adjacency)
    cycle_trace = {}
    if cycle is not None:
        labels = [
            edge_labels[(cycle[index], cycle[index + 1])][0]
            for index in range(len(cycle) - 1)
        ]
        product = Matrix.eye(base.rows)
        for label in labels:
            product = product * normalized[label]
        cycle_trace = {
            "basis_cycle": cycle,
            "parameter_indices": labels,
            "parameter_points": [list(source.LOWER[label]) for label in labels],
            "product_trace": str(product.trace()),
        }
        print(
            f"[INFO] residual cycle {cycle_trace['parameter_points']} "
            f"has labelled-product trace {cycle_trace['product_trace']}",
            flush=True,
        )

    mixed_inputs = []
    for mode in range(3):
        values = list(zero)
        for local_index, parameter_index in enumerate(remaining_indices):
            if mode == 0:
                value = Rational((local_index % 5) - 2)
            elif mode == 1:
                value = Rational((-1) ** local_index * (local_index % 3 + 1))
            else:
                value = Rational(local_index + 1, local_index % 7 + 1)
            values[parameter_index] = value
        mixed_inputs.append(values)

    mixed_checks = []
    for check_index, values in enumerate(mixed_inputs):
        determinant = source.selected_square(
            values, selected_row_labels, selected_columns
        ).det(method="domain-ge")
        equal = determinant == base_det
        mixed_checks.append({"determinant": str(determinant), "equal_base": equal})
        record(
            equal,
            f"normalized mixed determinant {check_index + 1} equals the base value",
        )

    full_pass = (
        constant_zero
        and forced_idempotent
        and forced_rank_trace
        and all(item["equal"] for item in factor_checks.values())
        and acyclic
        and strict_flag
        and all(item["equal_base"] for item in mixed_checks)
    )
    if full_pass:
        decision = "confirmed_24_parameter_simultaneous_exclusion"
    elif forced_idempotent and forced_rank_trace:
        decision = "confirmed_forced_factor_refuted_residual_flag"
    else:
        decision = "refuted_forced_vertex_factor"

    result = {
        "experiment": "EXP-100",
        "base_determinant": str(base_det),
        "constant_parameter_index": constant_index,
        "constant_direction_zero": constant_zero,
        "forced_parameter_index": forced_index,
        "forced_direction_idempotent": forced_idempotent,
        "forced_direction_rank": forced_rank,
        "forced_direction_trace": str(forced_trace),
        "forced_axis_factor": "(1+u)^16" if forced_idempotent else None,
        "forced_axis_checks": factor_checks,
        "remaining_parameter_indices": remaining_indices,
        "remaining_parameter_points": [
            list(source.LOWER[index]) for index in remaining_indices
        ],
        "residual_union_graph_edges": sum(len(targets) for targets in adjacency),
        "residual_union_graph_acyclic": acyclic,
        "residual_common_strict_flag": strict_flag,
        "residual_topological_order": order,
        "residual_cycle_trace": cycle_trace,
        "normalized_mixed_checks": mixed_checks,
        "decision": decision,
    }

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"RESULT: {decision.upper()}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESULT: FAILED: {exc}", file=sys.stderr, flush=True)
        raise
