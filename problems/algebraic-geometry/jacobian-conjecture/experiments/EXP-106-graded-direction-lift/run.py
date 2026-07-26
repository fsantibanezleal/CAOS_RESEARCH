"""EXP-106: classify coefficient directions compatible with the mu_9 charts."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from sympy import Rational


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
EXP103_DIR = ROOT.parent / "EXP-103-residual-curve-determinantal-divisor"
EXP103_RUN = EXP103_DIR / "run.py"
EXP103_ARTIFACT = EXP103_DIR / "artifacts" / "results.json"
EXP105_ARTIFACT = (
    ROOT.parent
    / "EXP-105-mu9-bezout-certificate"
    / "artifacts"
    / "results.json"
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def dense_augmented(source, row_labels, values):
    rows = source.sparse_rows(values)
    matrix = np.zeros((len(row_labels), 125), dtype=np.int64)
    for row_index, label in enumerate(row_labels):
        entries = rows.get(label, {})
        for local_column, global_column in enumerate(range(1, len(source.NQ))):
            value = Rational(entries.get(global_column, 0))
            if value.q != 1:
                raise AssertionError("coefficient direction is not integral")
            matrix[row_index, local_column] = int(value)
    matrix[row_labels.index((2, 0)), -1] = 1
    return matrix


def compatibility(direction, row_indices, grading, exponent):
    selected = direction[row_indices, :]
    row_weights = grading["row_weights"]
    column_weights = grading["column_weights"]
    residues = set()
    support = 0
    for row in range(selected.shape[0]):
        for column in range(selected.shape[1]):
            if selected[row, column] != 0:
                support += 1
                residues.add(
                    (exponent - row_weights[row] - column_weights[column]) % 9
                )
    return {
        "compatible": len(residues) == 1,
        "variable_residues": sorted(residues),
        "selected_support": support,
    }


def main() -> None:
    exp103 = load_module("exp103_for_exp106", EXP103_RUN)
    source = exp103.load_module("exp099_for_exp106", exp103.EXP099_RUN)
    coefficient_matrices, row_labels, _ = exp103.build_polynomial_matrix(source)
    base = coefficient_matrices[1]
    zero = [Rational(0)] * len(source.LOWER)

    exp103_result = json.loads(EXP103_ARTIFACT.read_text(encoding="utf-8"))
    exp105_result = json.loads(EXP105_ARTIFACT.read_text(encoding="utf-8"))
    first_rows = exp103.checkpoint_row_indices(row_labels)
    second_rows = next(
        chart["row_indices"]
        for chart in exp103_result["prime_runs"][0]["charts"]
        if chart["name"] == "pivot-u2"
    )
    first_grading = exp105_result["first_chart_grading"]
    second_grading = exp105_result["second_chart_grading"]

    direction_s = coefficient_matrices[3] // 8
    direction_t = coefficient_matrices[0]
    controls = {
        "s_on_curve_exponent_14": [
            compatibility(direction_s, first_rows, first_grading, 14),
            compatibility(direction_s, second_rows, second_grading, 14),
        ],
        "t_on_curve_exponent_0": [
            compatibility(direction_t, first_rows, first_grading, 0),
            compatibility(direction_t, second_rows, second_grading, 0),
        ],
    }
    require(
        all(
            chart["compatible"]
            for control in controls.values()
            for chart in control
        ),
        "both existing curve directions pass both grading controls",
    )

    negative_direction = np.array(direction_s, copy=True)
    first_nonzero = np.argwhere(negative_direction[first_rows, :] != 0)[0]
    negative_selected = negative_direction[first_rows, :]
    negative_selected[int(first_nonzero[0]), int(first_nonzero[1])] = 0
    # Combine one genuine exponent-14 entry with an artificial exponent-15
    # copy at the same chart; the residue set must split.
    genuine = compatibility(direction_s, first_rows, first_grading, 14)
    artificial = compatibility(direction_s, first_rows, first_grading, 15)
    require(
        genuine["variable_residues"] != artificial["variable_residues"],
        "an artificial one-step exponent perturbation changes the grading residue",
    )

    records = []
    excluded = {(0, 1), (1, 7)}
    for point in source.LOWER:
        if point in excluded:
            continue
        values = list(zero)
        values[source.LOWER.index(point)] = Rational(1)
        direction = dense_augmented(source, row_labels, values) - base
        first = compatibility(direction, first_rows, first_grading, 7)
        second = compatibility(direction, second_rows, second_grading, 7)
        shared = (
            first["compatible"]
            and second["compatible"]
            and first["variable_residues"] == second["variable_residues"]
        )
        records.append(
            {
                "point": list(point),
                "first_chart": first,
                "second_chart": second,
                "shared_compatible_residue": (
                    first["variable_residues"][0] if shared else None
                ),
                "compatible_on_both": shared,
                "total_selected_support": (
                    first["selected_support"] + second["selected_support"]
                ),
            }
        )

    compatible = [record for record in records if record["compatible_on_both"]]
    compatible.sort(
        key=lambda record: (
            record["total_selected_support"],
            record["point"][0],
            record["point"][1],
        )
    )
    incompatible = [record for record in records if not record["compatible_on_both"]]
    require(
        len(compatible) + len(incompatible) == 24,
        "all 24 remaining lower-family directions are classified",
    )

    if compatible:
        decision = "graded_lift_candidates_found"
        promoted = compatible[0]
    else:
        decision = "mu9_grading_is_slice_specific"
        promoted = None

    result = {
        "experiment": "EXP-106",
        "grading_modulus": 9,
        "controls": controls,
        "negative_control": {
            "genuine_residue": genuine["variable_residues"],
            "perturbed_residue": artificial["variable_residues"],
            "passed": True,
        },
        "directions_tested": len(records),
        "compatible_count": len(compatible),
        "incompatible_count": len(incompatible),
        "compatible_directions": compatible,
        "incompatible_directions": incompatible,
        "promoted_direction": promoted,
        "decision": decision,
        "nonclaim": (
            "grading compatibility is only a compute filter and does not prove "
            "rank coverage after adding any coefficient"
        ),
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(
        f"[INFO] compatible directions: {len(compatible)}/24; "
        f"promoted={None if promoted is None else promoted['point']}",
        flush=True,
    )
    print(f"[PASS] wrote {ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"RESULT: {decision.upper()}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESULT: FAILED: {exc}", file=sys.stderr, flush=True)
        raise
