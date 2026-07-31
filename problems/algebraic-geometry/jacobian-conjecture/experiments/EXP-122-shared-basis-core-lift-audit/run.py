"""EXP-122: exact shared-basis core lift activity audit.

CPU only. Every mathematical decision uses exact SymPy arithmetic over QQ.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Matrix, Rational, eye, expand, factor, symbols


HERE = Path(__file__).resolve().parent
E121_PATH = HERE.parent / "EXP-121-finite-lq-row-bases" / "run.py"
E121_ARTIFACT = (
    HERE.parent
    / "EXP-121-finite-lq-row-bases"
    / "artifacts"
    / "results.json"
)
E112_ARTIFACT = (
    HERE.parent
    / "EXP-112-augmented-graph-core"
    / "artifacts"
    / "results.json"
)
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
TB = ((0, 1), (0, 5), (1, 0))
FIXED_D_BASELINE = ((0, 1), (0, 5))
VALIDATION_VALUES = (Rational(1), Rational(-1, 2))
TOTAL_GATE_SECONDS = 300

spec = importlib.util.spec_from_file_location("exp121", E121_PATH)
exp121 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp121)
exp115 = exp121.exp115
exp112 = exp115.exp112


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def persist(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def direction_key(direction: tuple[int, int]) -> str:
    return f"({direction[0]},{direction[1]})"


def is_cyclic_component(
    component: list[int], adjacency: list[set[int]]
) -> bool:
    return len(component) > 1 or any(
        vertex in adjacency[vertex] for vertex in component
    )


def cyclic_components(matrices: list[Matrix]) -> list[list[int]]:
    adjacency, _, _, _ = exp112.graph_from_matrices(matrices)
    components = exp112.strongly_connected_components(adjacency)
    return sorted(
        [
            component
            for component in components
            if is_cyclic_component(component, adjacency)
        ],
        key=lambda component: (-len(component), component),
    )


def one_parameter_factor(matrix: Matrix):
    """Compute det(I+tK) from the exact cyclic diagonal blocks of K."""
    t = symbols("t")
    components = cyclic_components([matrix])
    expression = Rational(1)
    block_records = []
    for component in components:
        block = matrix.extract(component, component)
        block_factor = factor(
            (eye(len(component)) + t * block).det(method="domain-ge")
        )
        expression = expand(expression * block_factor)
        block_records.append(
            {
                "size": len(component),
                "vertices": component,
                "factor": str(block_factor),
            }
        )
    return factor(expression), block_records


def trace_product(left: Matrix, right: Matrix):
    return sum(
        left[row, column] * right[column, row]
        for row in range(left.rows)
        for column in range(left.cols)
    )


def exact_rank(matrix: Matrix) -> int:
    return int(matrix.rank())


def active_directions(record: dict[str, object]) -> list[tuple[int, int]]:
    components = record["cyclic_components"]
    core = next(component for component in components if component["size"] == 36)
    return [tuple(point) for point in core["parameter_points"]]


def shared_rows(record: dict[str, object]) -> list[int]:
    l_candidate = record["modular_selection"]["1013"]["L"][
        "selected_candidates"
    ][0]
    q_candidate = record["modular_selection"]["1033"]["Q"][
        "selected_candidates"
    ][0]
    require(
        l_candidate["row_basis"] == q_candidate["row_basis"],
        "EXP-121 selected exactly the same L/Q row basis",
    )
    return list(l_candidate["row_basis"])


def matrix_digest(matrices: dict[tuple[int, int], Matrix]) -> str:
    digest = hashlib.sha256()
    for direction in sorted(matrices):
        matrix = matrices[direction]
        for row in range(matrix.rows):
            for column in range(matrix.cols):
                value = matrix[row, column]
                if value:
                    digest.update(
                        (
                            f"{direction}:{row}:{column}:{value}\n"
                        ).encode("utf-8")
                    )
    return digest.hexdigest().upper()


def main() -> None:
    started = time.time()
    e112_record = json.loads(E112_ARTIFACT.read_text(encoding="utf-8"))
    e121_record = json.loads(E121_ARTIFACT.read_text(encoding="utf-8"))
    directions = active_directions(e112_record)
    require(len(directions) == 24, "restored exactly 24 cyclic-core directions")
    require(
        directions == [tuple(point) for point in e112_record["directions"][:24]],
        "restored directions reproduce the EXP-112 active prefix",
    )

    forced = exp112.forced_polynomial()
    all_directions = sorted(exp112.exp071.LOWER)
    _, complete_rows = exp112.complete_row_labels(forced, all_directions)
    constant_column = exp112.exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp112.exp071.NQ))
        if index != constant_column
    ]
    base = exp112.coefficient_matrix(
        forced, complete_rows, q_columns, include_rhs=True
    )
    direction_matrices = {
        direction: exp112.coefficient_matrix(
            {direction: exp112.Fraction(1)},
            complete_rows,
            q_columns,
            include_rhs=False,
        )
        for direction in directions
    }
    require(base.shape == (302, 125), "rebuilt complete 302 by 125 system")
    rows = shared_rows(e121_record)
    require(len(rows) == 125, "EXP-121 shared row basis has size 125")

    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: matrix.extract(rows, range(125))
        for direction, matrix in direction_matrices.items()
    }
    anchor = selected_base + selected_directions[(0, 1)]
    anchor_det = anchor.det(method="domain-ge")
    expected_anchor_det = e121_record["exact_charts"]["L"][0]["anchor"][
        "determinant"
    ]
    require(
        str(anchor_det) == expected_anchor_det,
        "reproduced the EXP-121 rational anchor determinant",
    )
    inverse = anchor.inv()
    normalized = {
        direction: inverse * matrix
        for direction, matrix in selected_directions.items()
    }
    print("[INFO] normalized all 24 directions exactly", flush=True)

    tb_components = cyclic_components(
        [normalized[direction] for direction in FIXED_D_BASELINE]
    )
    require(bool(tb_components), "T_B normalized graph is cyclic")
    tb_core = set(tb_components[0])
    require(
        len(tb_core) == 26,
        "reproduced the EXP-121 size-26 fixed-d T_B core",
    )
    normalized_sha = matrix_digest(normalized)

    payload: dict[str, object] = {
        "experiment": "EXP-122",
        "anchor": {
            "A": 1,
            "B": 0,
            "d": 1,
            "determinant": str(anchor_det),
        },
        "directions": [list(direction) for direction in directions],
        "shared_rows": rows,
        "normalized_sha256": normalized_sha,
        "tb": {
            "directions": [list(direction) for direction in TB],
            "fixed_d_graph_directions": [
                list(direction) for direction in FIXED_D_BASELINE
            ],
            "cyclic_component_sizes": [
                len(component) for component in tb_components
            ],
            "largest_component_vertices": sorted(tb_core),
        },
        "direction_records": {},
    }
    persist(payload, CHECKPOINT)

    records: dict[str, object] = {}
    for index, direction in enumerate(directions, start=1):
        matrix = normalized[direction]
        single_factor, factor_blocks = one_parameter_factor(matrix)
        internal_edges = sum(
            1
            for row in tb_core
            for column in tb_core
            if matrix[row, column] != 0
        )
        union_components = cyclic_components(
            [normalized[item] for item in FIXED_D_BASELINE] + [matrix]
        )
        union_largest = len(union_components[0]) if union_components else 0
        pair_coefficients = {}
        pair_symmetry = {}
        trace_value = matrix.trace()
        for tb_direction in TB:
            tb_matrix = normalized[tb_direction]
            forward = trace_product(matrix, tb_matrix)
            reverse = trace_product(tb_matrix, matrix)
            require(
                forward == reverse,
                (
                    f"trace pairing symmetry for {direction_key(direction)} "
                    f"and {direction_key(tb_direction)}"
                ),
            )
            coefficient = trace_value * tb_matrix.trace() - forward
            pair_coefficients[direction_key(tb_direction)] = str(coefficient)
            pair_symmetry[direction_key(tb_direction)] = True

        direct_checks = []
        for value in VALIDATION_VALUES:
            direct_ratio = (
                anchor + value * selected_directions[direction]
            ).det(method="domain-ge") / anchor_det
            predicted_ratio = single_factor.subs({"t": value})
            require(
                direct_ratio == predicted_ratio,
                (
                    f"direct determinant ratio for "
                    f"{direction_key(direction)} at t={value}"
                ),
            )
            direct_checks.append(
                {
                    "t": str(value),
                    "direct_ratio": str(direct_ratio),
                    "predicted_ratio": str(predicted_ratio),
                }
            )

        in_tb = direction in TB
        flags = {
            "tb_baseline": in_tb,
            "anchor_line_determinant_inert": single_factor == 1,
            "active_in_existing_26_block": internal_edges > 0,
            "scc_increasing": union_largest > len(tb_core),
            "low_order_determinant_participation": (
                trace_value != 0
                or any(value != "0" for value in pair_coefficients.values())
            ),
        }
        if in_tb:
            classification = "tb_baseline"
        elif flags["active_in_existing_26_block"]:
            classification = "active_in_existing_26_block"
        elif flags["scc_increasing"]:
            classification = "scc_increasing"
        else:
            classification = "acyclic_off_block_relative_to_tb"

        records[direction_key(direction)] = {
            "direction": list(direction),
            "classification": classification,
            "flags": flags,
            "selected_direction_rank": exact_rank(
                selected_directions[direction]
            ),
            "normalized_nonzero_count": sum(
                1 for value in matrix if value != 0
            ),
            "trace": str(trace_value),
            "anchor_directional_derivative_ratio": str(trace_value),
            "one_parameter_factor": str(single_factor),
            "one_parameter_cyclic_blocks": factor_blocks,
            "direct_determinant_checks": direct_checks,
            "tb_core_internal_edges": internal_edges,
            "union_cyclic_component_sizes": [
                len(component) for component in union_components
            ],
            "union_largest_cyclic_component": union_largest,
            "pairwise_mixed_coefficients_with_tb": pair_coefficients,
            "pairing_symmetry_checks": pair_symmetry,
        }
        payload["direction_records"] = records
        if index % 4 == 0 or index == len(directions):
            payload["checkpoint_completed_directions"] = index
            payload["checkpoint_elapsed_seconds"] = time.time() - started
            persist(payload, CHECKPOINT)
            print(
                f"[INFO] completed {index}/{len(directions)} directions",
                flush=True,
            )
        require(
            time.time() - started <= TOTAL_GATE_SECONDS,
            "EXP-122 remains within the five-minute compute gate",
        )

    restored = [
        record
        for key, record in records.items()
        if tuple(record["direction"]) not in TB
    ]
    prediction_2 = any(
        record["flags"]["anchor_line_determinant_inert"]
        for record in restored
    )
    prediction_3 = (
        any(
            record["flags"]["active_in_existing_26_block"]
            for record in restored
        )
        and any(record["flags"]["scc_increasing"] for record in restored)
    )
    prediction_4 = any(
        record["flags"]["low_order_determinant_participation"]
        for record in restored
    )
    class_counts: dict[str, int] = {}
    for record in restored:
        classification = record["classification"]
        class_counts[classification] = class_counts.get(classification, 0) + 1
    inert_count = sum(
        record["flags"]["anchor_line_determinant_inert"]
        for record in restored
    )
    active_count = sum(
        record["flags"]["active_in_existing_26_block"]
        for record in restored
    )
    increasing_count = sum(
        record["flags"]["scc_increasing"] for record in restored
    )
    low_order_count = sum(
        record["flags"]["low_order_determinant_participation"]
        for record in restored
    )
    payload["summary"] = {
        "restored_direction_count": len(restored),
        "classification_counts": class_counts,
        "anchor_line_inert_count": inert_count,
        "active_in_existing_26_block_count": active_count,
        "scc_increasing_count": increasing_count,
        "low_order_participation_count": low_order_count,
        "predictions": {
            "p1_anchor_and_tb_regression": True,
            "p2_at_least_one_anchor_line_inert": prediction_2,
            "p3_internal_and_scc_increasing_both_exist": prediction_3,
            "p4_at_least_one_low_order_participant": prediction_4,
        },
    }
    payload["elapsed_seconds"] = time.time() - started
    payload["scope"] = (
        "Exact anchor-local activity audit on the EXP-121 shared row basis. "
        "This does not prove a higher-dimensional chart cover and does not "
        "close the 24-parameter core, the 51-parameter family, (72,108), "
        "the degree floor, or JC(2)."
    )
    persist(payload, ARTIFACT)
    artifact_bytes = ARTIFACT.read_bytes()
    digest = hashlib.sha256(artifact_bytes).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"[INFO] elapsed {payload['elapsed_seconds']:.2f} s", flush=True)
    print(
        "[INFO] restored-direction counts: "
        f"inert={inert_count}, active26={active_count}, "
        f"scc-increasing={increasing_count}, low-order={low_order_count}",
        flush=True,
    )
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    main()
