"""EXP-099: exact common-flag gate for the EXP-059 augmented minor.

CPU only. Exact SymPy arithmetic over QQ. No randomness.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from collections import deque
from math import comb
from pathlib import Path

from sympy import Matrix, Rational, zeros


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
RHS_LABEL = "rhs"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def hull_pts(vertices: list[tuple[int, int]]) -> list[tuple[int, int]]:
    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])

    points = sorted(set(vertices))
    lower: list[tuple[int, int]] = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[tuple[int, int]] = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    hull = lower[:-1] + upper[:-1]

    def inside(point):
        for index, origin in enumerate(hull):
            target = hull[(index + 1) % len(hull)]
            if cross(origin, target, point) < 0:
                return False
        return True

    max_x = max(point[0] for point in vertices)
    max_y = max(point[1] for point in vertices)
    return [
        (i, j)
        for i in range(max_x + 1)
        for j in range(max_y + 1)
        if inside((i, j))
    ]


NQ = sorted(hull_pts([(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]))
NP_POINTS = hull_pts([(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)])
TOP = {(k, 8 + k) for k in range(9)}
LOWER = sorted(point for point in NP_POINTS if point not in TOP)[:26]


def in_pool(point: tuple[int, int]) -> bool:
    return point[0] - point[1] <= 2 and point[0] <= 24 and point[1] <= 44


def pterms(values: list[Rational]) -> dict[tuple[int, int], Rational]:
    terms = {
        (k, 8 + k): Rational(comb(8, k) * (-1) ** (8 - k))
        for k in range(9)
    }
    terms[(1, 0)] = terms.get((1, 0), Rational(0)) + Rational(1)
    for index, point in enumerate(LOWER):
        value = values[index]
        if value:
            terms[point] = terms.get(point, Rational(0)) + value
    return {point: value for point, value in terms.items() if value}


def sparse_rows(values: list[Rational]) -> dict[tuple[int, int], dict[int, Rational]]:
    rows: dict[tuple[int, int], dict[int, Rational]] = {}
    for column, (alpha, beta) in enumerate(NQ):
        for (p, q), coefficient in pterms(values).items():
            factor = p * beta - q * alpha
            if factor == 0:
                continue
            row = (p + alpha - 1, q + beta - 1)
            if not in_pool(row):
                continue
            rows.setdefault(row, {})
            rows[row][column] = rows[row].get(column, Rational(0)) + coefficient * factor
    rows.setdefault((2, 0), {})
    return rows


def augmented_matrix(values: list[Rational]):
    rows = sparse_rows(values)
    row_labels = sorted(rows)
    matrix = zeros(len(row_labels), len(NQ) + 1)
    for row_index, label in enumerate(row_labels):
        for column, value in rows[label].items():
            matrix[row_index, column] = value
    matrix[row_labels.index((2, 0)), len(NQ)] = 1
    return matrix, row_labels


def selected_square(
    values: list[Rational],
    selected_row_labels: list[tuple[int, int]],
    selected_columns: list[int],
) -> Matrix:
    rows = sparse_rows(values)
    square = zeros(len(selected_row_labels), len(selected_columns))
    rhs_column = len(NQ)
    for row_index, label in enumerate(selected_row_labels):
        data = rows.get(label, {})
        for local_column, column in enumerate(selected_columns):
            if column == rhs_column:
                square[row_index, local_column] = 1 if label == (2, 0) else 0
            else:
                square[row_index, local_column] = data.get(column, 0)
    return square


def matrix_hash(matrix: Matrix) -> str:
    payload = "\n".join(str(entry) for entry in matrix)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()


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

    best: list[int] | None = None
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
    started = time.time()
    zero = [Rational(0)] * len(LOWER)
    augmented_base, base_row_labels = augmented_matrix(zero)
    require(len(NQ) == 125, "the reduced Q polygon has 125 coefficient columns")
    require(len(LOWER) == 26, "the EXP-059 lower family has 26 parameters")

    _, row_pivots = augmented_base.T.rref()
    selected_row_indices = list(row_pivots)[:125]
    require(len(selected_row_indices) == 125, "125 independent augmented rows selected")
    selected_row_labels = [base_row_labels[index] for index in selected_row_indices]

    row_block = augmented_base[selected_row_indices, :]
    _, column_pivots = row_block.rref()
    selected_columns = list(column_pivots)[:125]
    rhs_column = len(NQ)
    if rhs_column not in selected_columns:
        selected_columns = selected_columns[:124] + [rhs_column]
    require(rhs_column in selected_columns, "the selected square includes the RHS column")

    base = selected_square(zero, selected_row_labels, selected_columns)
    base_det = base.det(method="domain-ge")
    require(base_det != 0, f"the selected base minor is invertible with determinant {base_det}")
    print(f"[INFO] base selection and determinant: {time.time() - started:.2f} s", flush=True)

    inverse_started = time.time()
    base_inverse = base.inv()
    print(f"[INFO] exact base inverse: {time.time() - inverse_started:.2f} s", flush=True)

    normalized: list[Matrix] = []
    direction_hashes: list[str] = []
    adjacency = [set() for _ in range(base.rows)]
    edge_labels: dict[tuple[int, int], list[int]] = {}
    nonzero_counts: list[int] = []

    for parameter_index in range(len(LOWER)):
        values = list(zero)
        values[parameter_index] = Rational(1)
        direction = selected_square(values, selected_row_labels, selected_columns) - base
        normalized_direction = base_inverse * direction
        normalized.append(normalized_direction)
        direction_hashes.append(matrix_hash(normalized_direction))
        count = 0
        for row in range(normalized_direction.rows):
            for column in range(normalized_direction.cols):
                if normalized_direction[row, column] != 0:
                    count += 1
                    adjacency[column].add(row)
                    edge_labels.setdefault((column, row), []).append(parameter_index)
        nonzero_counts.append(count)
        if (parameter_index + 1) % 5 == 0 or parameter_index + 1 == len(LOWER):
            print(
                f"[INFO] normalized directions {parameter_index + 1}/{len(LOWER)}",
                flush=True,
            )

    order = topological_order(adjacency)
    acyclic = order is not None
    cycle = None if acyclic else shortest_cycle(adjacency)
    edge_count = sum(len(targets) for targets in adjacency)

    strict_flag_verified = False
    if acyclic and order is not None:
        position = {node: index for index, node in enumerate(order)}
        strict_flag_verified = all(
            position[source] < position[target]
            for source, targets in enumerate(adjacency)
            for target in targets
        )
        require(strict_flag_verified, "the topological order gives one common strict flag")
    else:
        print(f"[INFO] common strict flag refuted; cycle witness {cycle}", flush=True)

    trace_data = {}
    if cycle is not None and len(cycle) >= 2:
        labels = [
            edge_labels[(cycle[index], cycle[index + 1])][0]
            for index in range(len(cycle) - 1)
        ]
        product = Matrix.eye(base.rows)
        for label in labels:
            product = product * normalized[label]
        trace_data = {
            "parameter_indices": labels,
            "parameter_points": [list(LOWER[label]) for label in labels],
            "product_trace": str(product.trace()),
        }
        print(
            "[INFO] cycle labels "
            f"{trace_data['parameter_points']}; product trace "
            f"{trace_data['product_trace']}",
            flush=True,
        )

    adversarial_values = [
        [Rational((index % 5) - 2) for index in range(len(LOWER))],
        [Rational((-1) ** index * (index % 3 + 1)) for index in range(len(LOWER))],
        [Rational(index + 1, index % 7 + 1) for index in range(len(LOWER))],
    ]
    determinant_checks = []
    determinant_equal_base = []
    for check_index, values in enumerate(adversarial_values):
        determinant = selected_square(
            values, selected_row_labels, selected_columns
        ).det(method="domain-ge")
        determinant_checks.append(str(determinant))
        equal_base = determinant == base_det
        determinant_equal_base.append(equal_base)
        marker = "PASS" if equal_base else "REFUTED"
        print(
            f"[{marker}] adversarial mixed determinant {check_index + 1} "
            f"{'equals' if equal_base else 'differs from'} the base value",
            flush=True,
        )

    decision = (
        "confirmed_common_strict_flag"
        if strict_flag_verified
        else "refuted_common_strict_flag"
    )
    result = {
        "experiment": "EXP-099",
        "parameter_points": [list(point) for point in LOWER],
        "q_columns": len(NQ),
        "base_augmented_shape": list(augmented_base.shape),
        "selected_shape": list(base.shape),
        "selected_row_labels": [list(label) for label in selected_row_labels],
        "selected_columns": [
            RHS_LABEL if column == rhs_column else list(NQ[column])
            for column in selected_columns
        ],
        "base_determinant": str(base_det),
        "base_matrix_sha256": matrix_hash(base),
        "normalized_direction_sha256": direction_hashes,
        "normalized_direction_nonzeros": nonzero_counts,
        "union_graph_edges": edge_count,
        "union_graph_acyclic": acyclic,
        "common_strict_flag_verified": strict_flag_verified,
        "topological_order": order,
        "shortest_cycle": cycle,
        "cycle_trace_probe": trace_data,
        "adversarial_determinants": determinant_checks,
        "adversarial_determinants_equal_base": determinant_equal_base,
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
