"""EXP-113: exact cycle stratification of the EXP-112 36-core."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

from sympy import Rational


HERE = Path(__file__).resolve().parent
E112_PATH = HERE.parent / "EXP-112-augmented-graph-core" / "run.py"
ARTIFACT = HERE / "artifacts" / "results.json"

spec = importlib.util.spec_from_file_location("exp112", E112_PATH)
exp112 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp112)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def profile(matrices) -> dict[str, object]:
    adjacency, _, _, _ = exp112.graph_from_matrices(matrices)
    components = exp112.strongly_connected_components(adjacency)
    sizes = sorted((len(component) for component in components), reverse=True)
    cyclic_sizes = sorted(
        (
            len(component)
            for component in components
            if len(component) > 1
            or any(node in adjacency[node] for node in component)
        ),
        reverse=True,
    )
    return {
        "component_sizes": sizes,
        "cyclic_component_sizes": cyclic_sizes,
        "largest_component": sizes[0],
        "strongly_connected": sizes[0] == len(adjacency),
        "edge_count": sum(len(targets) for targets in adjacency),
    }


def deletion_minimal_support(
    matrices,
    active_indices: list[int],
    order: list[int],
) -> list[int]:
    support = list(active_indices)
    for parameter_index in order:
        if parameter_index not in support:
            continue
        candidate = [
            index for index in support if index != parameter_index
        ]
        if profile([matrices[index] for index in candidate])[
            "strongly_connected"
        ]:
            support = candidate
    return support


def connected_components_undirected(adjacency: list[set[int]]) -> list[list[int]]:
    visited: set[int] = set()
    components: list[list[int]] = []
    for start in range(len(adjacency)):
        if start in visited:
            continue
        stack = [start]
        visited.add(start)
        component = []
        while stack:
            node = stack.pop()
            component.append(node)
            for target in sorted(adjacency[node], reverse=True):
                if target not in visited:
                    visited.add(target)
                    stack.append(target)
        components.append(sorted(component))
    return components


def main() -> None:
    started = time.time()
    forced = exp112.forced_polynomial()
    directions = sorted(exp112.exp071.LOWER)
    pinned_rows, complete_rows = exp112.complete_row_labels(
        forced, directions
    )
    constant_column = exp112.exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp112.exp071.NQ))
        if index != constant_column
    ]

    base_full = exp112.coefficient_matrix(
        forced, complete_rows, q_columns, include_rhs=True
    )
    direction_full = [
        exp112.coefficient_matrix(
            {direction: Fraction(1)},
            complete_rows,
            q_columns,
            include_rhs=False,
        )
        for direction in directions
    ]
    _, row_pivots = base_full.T.rref()
    selected_indices = list(row_pivots)
    require(
        len(selected_indices) == 125,
        "the EXP-112 pinned row basis reconstructs",
    )
    base = base_full[selected_indices, :]
    base_inverse = base.inv()
    normalized = [
        base_inverse * matrix[selected_indices, :]
        for matrix in direction_full
    ]
    adjacency, _, _, _ = exp112.graph_from_matrices(normalized)
    components = exp112.strongly_connected_components(adjacency)
    largest_component = max(components, key=len)
    require(
        len(largest_component) == 36,
        "the exact largest component has 36 columns",
    )
    core_matrices = [
        matrix.extract(largest_component, largest_component)
        for matrix in normalized
    ]

    active_indices = [
        index
        for index, matrix in enumerate(core_matrices)
        if not matrix.is_zero_matrix
    ]
    require(
        len(active_indices) == 24,
        "the 36-core has exactly 24 active parameter directions",
    )
    forced_index = directions.index((1, 0))
    forced_charpoly = (
        core_matrices[forced_index].charpoly().as_expr().factor()
    )
    require(
        str(forced_charpoly) == "lambda**23*(lambda - 1)**13",
        "the forced direction has the recorded 13-dimensional nonzero eigenspace",
    )

    groups = {
        "G0": [
            index for index in active_indices if directions[index][0] == 0
        ],
        "G1": [
            index for index in active_indices if directions[index][0] == 1
        ],
        "G2": [
            index for index in active_indices if directions[index][0] == 2
        ],
    }
    subset_indices = {
        "forced-only": [forced_index],
        "without-forced": [
            index for index in active_indices if index != forced_index
        ],
        "G0": groups["G0"],
        "G1": groups["G1"],
        "G2": groups["G2"],
        "G0+G1": groups["G0"] + groups["G1"],
        "G0+G2": groups["G0"] + groups["G2"],
        "G1+G2": groups["G1"] + groups["G2"],
        "known-pair": [
            directions.index((0, 1)),
            directions.index((1, 7)),
        ],
        "all-active": active_indices,
    }
    profiles = {
        name: profile([core_matrices[index] for index in indices])
        for name, indices in subset_indices.items()
    }

    known_pair_cyclic = bool(
        profiles["known-pair"]["cyclic_component_sizes"]
    )
    require(
        known_pair_cyclic
        and not profiles["known-pair"]["strongly_connected"],
        "the EXP-100 pair is cyclic but not fully 36-connected",
    )
    require(
        profiles["all-active"]["strongly_connected"],
        "all 24 active directions make the 36-core strongly connected",
    )

    forward_support = deletion_minimal_support(
        core_matrices, active_indices, list(active_indices)
    )
    reverse_support = deletion_minimal_support(
        core_matrices, active_indices, list(reversed(active_indices))
    )
    require(
        profile([core_matrices[index] for index in forward_support])[
            "strongly_connected"
        ]
        and profile([core_matrices[index] for index in reverse_support])[
            "strongly_connected"
        ],
        "both deletion-minimal controls retain full strong connectivity",
    )

    interaction_adjacency = [set() for _ in active_indices]
    interaction_records = []
    for local_left, left_index in enumerate(active_indices):
        for local_right in range(local_left, len(active_indices)):
            right_index = active_indices[local_right]
            left = core_matrices[left_index]
            right = core_matrices[right_index]
            trace = sum(
                left[row, column] * right[column, row]
                for row in range(36)
                for column in range(36)
            )
            if trace == 0:
                continue
            interaction_adjacency[local_left].add(local_right)
            interaction_adjacency[local_right].add(local_left)
            interaction_records.append(
                {
                    "left": list(directions[left_index]),
                    "right": list(directions[right_index]),
                    "trace": str(trace),
                }
            )
    interaction_components = connected_components_undirected(
        interaction_adjacency
    )

    predictions = {
        "without_forced_splits": not profiles["without-forced"][
            "strongly_connected"
        ],
        "single_group_splits": any(
            not profiles[name]["strongly_connected"]
            for name in ("G0", "G1", "G2")
        ),
        "forward_support_smaller_than_24": len(forward_support) < 24,
        "reverse_support_smaller_than_24": len(reverse_support) < 24,
    }
    for name, outcome in predictions.items():
        print(
            f"[{'PASS' if outcome else 'REFUTED'}] prediction {name}",
            flush=True,
        )

    result = {
        "experiment": "EXP-113",
        "directions": [list(direction) for direction in directions],
        "active_indices": active_indices,
        "active_points": [
            list(directions[index]) for index in active_indices
        ],
        "group_points": {
            name: [list(directions[index]) for index in indices]
            for name, indices in groups.items()
        },
        "profiles": profiles,
        "forward_deletion_minimal_indices": forward_support,
        "forward_deletion_minimal_points": [
            list(directions[index]) for index in forward_support
        ],
        "reverse_deletion_minimal_indices": reverse_support,
        "reverse_deletion_minimal_points": [
            list(directions[index]) for index in reverse_support
        ],
        "trace_interactions": interaction_records,
        "trace_interaction_component_sizes": sorted(
            (len(component) for component in interaction_components),
            reverse=True,
        ),
        "predictions": predictions,
        "elapsed_seconds": time.time() - started,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()

    print(
        "[INFO] forward deletion-minimal support: "
        f"{[directions[index] for index in forward_support]}",
        flush=True,
    )
    print(
        "[INFO] reverse deletion-minimal support: "
        f"{[directions[index] for index in reverse_support]}",
        flush=True,
    )
    print(
        "[INFO] trace-interaction components: "
        f"{result['trace_interaction_component_sizes']}",
        flush=True,
    )
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"RESULT: FAILED: {error}", file=sys.stderr, flush=True)
        raise
