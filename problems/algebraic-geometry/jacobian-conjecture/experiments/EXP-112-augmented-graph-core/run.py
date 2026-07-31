"""EXP-112: exact augmented dependency graph and cyclic-core gate.

CPU-only, exact SymPy arithmetic over QQ.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from collections import deque
from fractions import Fraction
from math import comb
from pathlib import Path

from sympy import Matrix, Rational, zeros


HERE = Path(__file__).resolve().parent
E71_PATH = HERE.parent / "EXP-071-degree3-pair-necessaries" / "run.py"
ARTIFACT = HERE / "artifacts" / "results.json"
RHS_LABEL = "rhs"

spec = importlib.util.spec_from_file_location("exp071", E71_PATH)
exp071 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp071)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def forced_polynomial() -> dict[tuple[int, int], Fraction]:
    terms = {
        (index, 8 + index): Fraction(
            comb(8, index) * (-1) ** (8 - index)
        )
        for index in range(9)
    }
    terms[(1, 0)] = Fraction(1)
    return terms


def complete_row_labels(
    forced: dict[tuple[int, int], Fraction],
    directions: list[tuple[int, int]],
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    pinned = set(exp071.bracket_terms(forced)) | {(2, 0)}
    complete = set(pinned)
    for direction in directions:
        complete.update(
            exp071.bracket_terms({direction: Fraction(1)})
        )
    complete.add((2, 0))
    return sorted(pinned), sorted(complete)


def coefficient_matrix(
    terms: dict[tuple[int, int], Fraction],
    row_labels: list[tuple[int, int]],
    q_columns: list[int],
    *,
    include_rhs: bool,
) -> Matrix:
    row_index = {label: index for index, label in enumerate(row_labels)}
    column_index = {
        source_column: local_column
        for local_column, source_column in enumerate(q_columns)
    }
    matrix = zeros(len(row_labels), len(q_columns) + 1)
    for label, columns in exp071.bracket_terms(terms).items():
        if label not in row_index:
            continue
        for source_column, value in columns.items():
            if source_column in column_index:
                matrix[
                    row_index[label], column_index[source_column]
                ] = Rational(value.numerator, value.denominator)
    if include_rhs:
        matrix[row_index[(2, 0)], len(q_columns)] = 1
    return matrix


def graph_from_matrices(
    matrices: list[Matrix],
) -> tuple[list[set[int]], dict[tuple[int, int], set[int]], list[int], str]:
    size = matrices[0].rows
    adjacency = [set() for _ in range(size)]
    edge_parameters: dict[tuple[int, int], set[int]] = {}
    nonzero_counts: list[int] = []
    digest = hashlib.sha256()
    for parameter_index, matrix in enumerate(matrices):
        count = 0
        for row in range(size):
            for column in range(size):
                value = matrix[row, column]
                if value == 0:
                    continue
                count += 1
                adjacency[column].add(row)
                edge_parameters.setdefault((column, row), set()).add(
                    parameter_index
                )
                digest.update(
                    f"{parameter_index}:{row}:{column}:{value}\n".encode(
                        "utf-8"
                    )
                )
        nonzero_counts.append(count)
    return adjacency, edge_parameters, nonzero_counts, digest.hexdigest().upper()


def strongly_connected_components(
    adjacency: list[set[int]],
) -> list[list[int]]:
    size = len(adjacency)
    reverse = [set() for _ in range(size)]
    for source, targets in enumerate(adjacency):
        for target in targets:
            reverse[target].add(source)

    visited: set[int] = set()
    finish_order: list[int] = []
    for start in range(size):
        if start in visited:
            continue
        stack: list[tuple[int, bool]] = [(start, False)]
        while stack:
            node, finishing = stack.pop()
            if finishing:
                finish_order.append(node)
                continue
            if node in visited:
                continue
            visited.add(node)
            stack.append((node, True))
            for target in sorted(adjacency[node], reverse=True):
                if target not in visited:
                    stack.append((target, False))

    components: list[list[int]] = []
    assigned: set[int] = set()
    for start in reversed(finish_order):
        if start in assigned:
            continue
        component: list[int] = []
        queue = [start]
        assigned.add(start)
        while queue:
            node = queue.pop()
            component.append(node)
            for target in sorted(reverse[node], reverse=True):
                if target not in assigned:
                    assigned.add(target)
                    queue.append(target)
        components.append(sorted(component))
    return components


def topological_order(adjacency: list[set[int]]) -> list[int] | None:
    indegree = [0] * len(adjacency)
    for targets in adjacency:
        for target in targets:
            indegree[target] += 1
    queue = deque(
        index for index, degree in enumerate(indegree) if degree == 0
    )
    order: list[int] = []
    while queue:
        source = queue.popleft()
        order.append(source)
        for target in sorted(adjacency[source]):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return order if len(order) == len(adjacency) else None


def cyclic_component_records(
    components: list[list[int]],
    adjacency: list[set[int]],
    edge_parameters: dict[tuple[int, int], set[int]],
    directions: list[tuple[int, int]],
    column_labels: list[tuple[int, int] | str],
) -> list[dict[str, object]]:
    records = []
    for component in components:
        component_set = set(component)
        cyclic = len(component) > 1 or any(
            node in adjacency[node] for node in component
        )
        if not cyclic:
            continue
        parameters: set[int] = set()
        internal_edges = 0
        for source in component:
            for target in adjacency[source] & component_set:
                internal_edges += 1
                parameters.update(edge_parameters[(source, target)])
        records.append(
            {
                "size": len(component),
                "vertices": component,
                "column_labels": [
                    column_labels[vertex] for vertex in component
                ],
                "internal_edges": internal_edges,
                "parameter_indices": sorted(parameters),
                "parameter_points": [
                    list(directions[index]) for index in sorted(parameters)
                ],
            }
        )
    return sorted(records, key=lambda record: int(record["size"]), reverse=True)


def main() -> None:
    started = time.time()
    forced = forced_polynomial()
    directions = sorted(exp071.LOWER)
    pinned_rows, complete_rows = complete_row_labels(forced, directions)
    constant_source_column = exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp071.NQ))
        if index != constant_source_column
    ]
    column_labels: list[tuple[int, int] | str] = [
        exp071.NQ[index] for index in q_columns
    ] + [RHS_LABEL]

    base_full = coefficient_matrix(
        forced, complete_rows, q_columns, include_rhs=True
    )
    direction_full = [
        coefficient_matrix(
            {direction: Fraction(1)},
            complete_rows,
            q_columns,
            include_rhs=False,
        )
        for direction in directions
    ]
    require(
        base_full.shape == (302, 125) and len(directions) == 51,
        "the complete effective augmented system is 302 by 125 with 51 directions",
    )

    recovered_rows = sorted(set(complete_rows) - set(pinned_rows))
    recovered_indices = [complete_rows.index(row) for row in recovered_rows]
    require(
        len(recovered_rows) == 13
        and all(
            all(base_full[index, column] == 0 for column in range(125))
            for index in recovered_indices
        ),
        "all 13 recovered rows vanish at the pinned point",
    )
    recovered_direction_nonzero = {
        row: [
            directions[parameter_index]
            for parameter_index, matrix in enumerate(direction_full)
            if any(
                matrix[complete_rows.index(row), column] != 0
                for column in range(125)
            )
        ]
        for row in recovered_rows
    }
    require(
        all(recovered_direction_nonzero[row] for row in recovered_rows),
        "every recovered row is active in at least one parameter direction",
    )

    print("[INFO] selecting exact pinned row basis", flush=True)
    _, row_pivots = base_full.T.rref()
    selected_indices = list(row_pivots)
    require(
        len(selected_indices) == 125,
        "the pinned effective augmented matrix has rank 125",
    )
    require(
        not (set(selected_indices) & set(recovered_indices)),
        "no zero recovered row enters the pinned basis",
    )
    selected_rows = [complete_rows[index] for index in selected_indices]
    base = base_full[selected_indices, :]
    base_determinant = base.det(method="domain-ge")
    require(
        base_determinant != 0,
        "the deterministic pinned augmented minor is exactly nonzero",
    )
    print(
        f"[INFO] pinned basis ready in {time.time() - started:.2f} s",
        flush=True,
    )

    inverse_started = time.time()
    base_inverse = base.inv()
    print(
        f"[INFO] exact pinned inverse in {time.time() - inverse_started:.2f} s",
        flush=True,
    )

    normalized: list[Matrix] = []
    for parameter_index, matrix in enumerate(direction_full):
        selected_direction = matrix[selected_indices, :]
        normalized.append(base_inverse * selected_direction)
        if (parameter_index + 1) % 5 == 0 or parameter_index == len(directions) - 1:
            print(
                f"[INFO] normalized {parameter_index + 1}/{len(directions)} "
                "directions",
                flush=True,
            )

    (
        adjacency,
        edge_parameters,
        nonzero_counts,
        support_hash,
    ) = graph_from_matrices(normalized)
    components = strongly_connected_components(adjacency)
    component_sizes = sorted(
        (len(component) for component in components), reverse=True
    )
    order = topological_order(adjacency)
    acyclic = order is not None
    exact_blocks = cyclic_component_records(
        components,
        adjacency,
        edge_parameters,
        directions,
        column_labels,
    )

    singleton_loop_factors = []
    for component in components:
        if len(component) != 1:
            continue
        vertex = component[0]
        coefficients = []
        for parameter_index, matrix in enumerate(normalized):
            value = matrix[vertex, vertex]
            if value != 0:
                coefficients.append(
                    {
                        "parameter_index": parameter_index,
                        "parameter_point": list(directions[parameter_index]),
                        "coefficient": str(value),
                    }
                )
        if coefficients:
            singleton_loop_factors.append(
                {
                    "vertex": vertex,
                    "column_label": (
                        column_labels[vertex]
                        if column_labels[vertex] == RHS_LABEL
                        else list(column_labels[vertex])
                    ),
                    "coefficients": coefficients,
                }
            )

    largest_component = max(components, key=len)
    forced_parameter_index = directions.index((1, 0))
    forced_core = normalized[forced_parameter_index].extract(
        largest_component, largest_component
    )
    forced_core_charpoly = forced_core.charpoly().as_expr().factor()
    require(
        str(forced_core_charpoly) == "lambda**23*(lambda - 1)**13",
        "the 36-core forced-axis characteristic polynomial is lambda^23*(lambda-1)^13",
    )
    require(
        len(singleton_loop_factors) == 3
        and all(
            factor["coefficients"]
            == [
                {
                    "parameter_index": forced_parameter_index,
                    "parameter_point": [1, 0],
                    "coefficient": "1",
                }
            ]
            for factor in singleton_loop_factors
        ),
        "the three cyclic singleton blocks each contribute the factor 1+eps_(1,0)",
    )

    historical_points = {
        (0, 0),
        *sorted(
            point
            for point in exp071.NP_PTS
            if point not in exp071.TOP
        )[:25],
    }
    historical_indices = [
        index
        for index, direction in enumerate(directions)
        if direction in historical_points
    ]
    (
        historical_adjacency,
        _,
        _,
        _,
    ) = graph_from_matrices(
        [normalized[index] for index in historical_indices]
    )
    historical_acyclic = topological_order(historical_adjacency) is not None
    require(
        not historical_acyclic and not acyclic,
        "the historical subset and full 51-direction graphs are cyclic",
    )

    if acyclic:
        decision = "confirmed_common_acyclic_flag"
        print("[PASS] exact common acyclic flag found", flush=True)
    elif component_sizes[0] < 125:
        decision = "confirmed_proper_cyclic_core"
        print(
            "[PASS] exact SCC compression found: "
            f"largest block {component_sizes[0]} of 125",
            flush=True,
        )
    else:
        decision = "refuted_compression_on_pinned_basis"
        print(
            "[REFUTED] the exact pinned graph is one 125-vertex cyclic core",
            flush=True,
        )

    mixed_values = [
        [Rational((index % 5) - 2) for index in range(len(directions))],
        [
            Rational((-1) ** index * (index % 3 + 1))
            for index in range(len(directions))
        ],
        [
            Rational(index + 1, index % 7 + 1)
            for index in range(len(directions))
        ],
    ]
    determinant_checks: list[str] = []
    for check_index, values in enumerate(mixed_values):
        mixed = base.copy()
        for value, matrix in zip(values, direction_full):
            if value:
                mixed += value * matrix[selected_indices, :]
        determinant = mixed.det(method="domain-ge")
        determinant_checks.append(str(determinant))
        print(
            f"[INFO] mixed determinant {check_index + 1}: "
            f"{'nonzero' if determinant else 'zero'}",
            flush=True,
        )

    result = {
        "experiment": "EXP-112",
        "decision": decision,
        "complete_shape": list(base_full.shape),
        "direction_count": len(directions),
        "directions": [list(direction) for direction in directions],
        "recovered_rows": [list(row) for row in recovered_rows],
        "recovered_row_directions": {
            str(row): [
                list(direction)
                for direction in recovered_direction_nonzero[row]
            ]
            for row in recovered_rows
        },
        "selected_rows": [list(row) for row in selected_rows],
        "selected_columns": [
            label if label == RHS_LABEL else list(label)
            for label in column_labels
        ],
        "base_determinant": str(base_determinant),
        "normalized_support_sha256": support_hash,
        "normalized_nonzero_counts": nonzero_counts,
        "union_graph_edges": sum(len(targets) for targets in adjacency),
        "union_graph_acyclic": acyclic,
        "historical_subset_direction_count": len(historical_indices),
        "historical_subset_acyclic": historical_acyclic,
        "component_sizes": component_sizes,
        "cyclic_components": exact_blocks,
        "singleton_loop_factors": singleton_loop_factors,
        "largest_core_forced_charpoly": str(forced_core_charpoly),
        "selected_minor_factorization": (
            "det(A_selected)=det(A0)*(1+eps_(1,0))^3*det(C36); "
            "C36 depends on 24 parameters and restricts on the forced axis "
            "to (1+eps_(1,0))^13"
        ),
        "topological_order": order,
        "mixed_determinants": determinant_checks,
        "elapsed_seconds": time.time() - started,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"RESULT: {decision.upper()}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"RESULT: FAILED: {error}", file=sys.stderr, flush=True)
        raise
