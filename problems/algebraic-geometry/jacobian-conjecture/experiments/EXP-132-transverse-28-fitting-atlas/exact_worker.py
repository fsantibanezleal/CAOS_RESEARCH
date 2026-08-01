"""Exact determinant worker for the two EXP-131 sections in EXP-132."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from sympy import Poly, expand, factor, symbols


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
E115_PATH = (
    EXPERIMENTS / "EXP-115-weighted-residual-component-gate" / "run.py"
)
E122_PATH = (
    EXPERIMENTS / "EXP-122-shared-basis-core-lift-audit" / "run.py"
)
E131_ARTIFACT = (
    EXPERIMENTS
    / "EXP-131-a0-boundary-atlas"
    / "artifacts"
    / "results.json"
)
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
ARTIFACT = HERE / "artifacts" / "exact-worker.json"

spec = importlib.util.spec_from_file_location("exp115_for_132_worker", E115_PATH)
exp115 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp115)
exp112 = exp115.exp112

spec122 = importlib.util.spec_from_file_location("exp122_for_132_worker", E122_PATH)
exp122 = importlib.util.module_from_spec(spec122)
assert spec122.loader is not None
spec122.loader.exec_module(exp122)


def persist(payload: dict[str, object]) -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    e131 = json.loads(E131_ARTIFACT.read_text(encoding="utf-8"))
    forced = exp112.forced_polynomial()
    directions = sorted(exp112.exp071.LOWER)
    _, row_labels = exp112.complete_row_labels(forced, directions)
    constant_column = exp112.exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp112.exp071.NQ))
        if index != constant_column
    ]
    base = exp112.coefficient_matrix(
        forced, row_labels, q_columns, include_rhs=True
    )
    direction_matrices = {
        direction: exp112.coefficient_matrix(
            {direction: exp112.Fraction(1)},
            row_labels,
            q_columns,
            include_rhs=False,
        )
        for direction in ((0, 5), (2, 9), (2, 8))
    }
    b, c, t = symbols("B C T")
    family = (
        base
        + b * direction_matrices[(0, 5)]
        + c * direction_matrices[(2, 9)]
        + t * direction_matrices[(2, 8)]
    )
    payload: dict[str, object] = {"experiment": "EXP-132-exact-worker"}
    for name, rows in (
        ("primary", e131["primary_rows"]),
        ("alternative", e131["alternative_rows"]),
    ):
        print(f"[INFO] reconstructing exact {name} determinant", flush=True)
        determinant = factor(
            family.extract(rows, range(125)).det(method="domain-ge")
        )
        polynomial = Poly(determinant, t, domain="QQ[B,C]")
        payload[name] = {
            "determinant": str(determinant),
            "degree_B": int(Poly(determinant, b, c, t).degree(b)),
            "degree_C": int(Poly(determinant, b, c, t).degree(c)),
            "degree_T": int(polynomial.degree()),
            "coefficients_T": {
                str(power): str(factor(polynomial.nth(power)))
                for power in range(int(polynomial.degree()) + 1)
            },
        }
        persist(payload)
        print(
            f"[INFO] {name}: degrees "
            f"B={payload[name]['degree_B']} "
            f"C={payload[name]['degree_C']} "
            f"T={payload[name]['degree_T']}",
            flush=True,
        )

    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    residual_rows = checkpoint["residual_selection"]["shared_rows"]
    print("[INFO] reconstructing exact residual-selected determinant", flush=True)
    residual_determinant = factor(
        family.extract(residual_rows, range(125)).det(method="domain-ge")
    )
    residual_poly = Poly(residual_determinant, b, c, t)
    payload["residual"] = {
        "rows": residual_rows,
        "determinant": str(residual_determinant),
        "degree_B": int(residual_poly.degree(b)),
        "degree_C": int(residual_poly.degree(c)),
        "degree_T": int(residual_poly.degree(t)),
        "term_count": len(residual_poly.terms()),
    }
    persist(payload)
    print(
        "[INFO] residual: degrees "
        f"B={payload['residual']['degree_B']} "
        f"C={payload['residual']['degree_C']} "
        f"T={payload['residual']['degree_T']} "
        f"terms={payload['residual']['term_count']}",
        flush=True,
    )

    finite_rows = checkpoint["finite_selection"]["shared_rows"]
    print("[INFO] reconstructing exact finite-selected determinant by SCC blocks", flush=True)
    selected_base = base.extract(finite_rows, range(125))
    selected_directions = {
        direction: matrix.extract(finite_rows, range(125))
        for direction, matrix in direction_matrices.items()
    }
    anchor_point = (1, 1, 0)
    anchor = (
        selected_base
        + selected_directions[(0, 5)]
        + selected_directions[(2, 9)]
    )
    anchor_det = anchor.det(method="domain-ge")
    if anchor_det == 0:
        raise AssertionError("finite-selected anchor determinant is zero")
    inverse = anchor.inv()
    normalized = {
        direction: inverse * matrix
        for direction, matrix in selected_directions.items()
    }
    components = exp122.cyclic_components(list(normalized.values()))
    if any(len(component) != 1 for component in components):
        raise AssertionError("finite-selected normalized graph is not acyclic")
    ratio = 1
    factors = []
    for component in components:
        index = component[0]
        affine = expand(
            1
            + (b - 1) * normalized[(0, 5)][index, index]
            + (c - 1) * normalized[(2, 9)][index, index]
            + t * normalized[(2, 8)][index, index]
        )
        ratio = expand(ratio * affine)
        if affine != 1:
            factors.append(str(factor(affine)))
    finite_determinant = factor(anchor_det * ratio)
    finite_poly = Poly(finite_determinant, b, c, t)
    controls = []
    for b_value, c_value, t_value in ((1, 1, 0), (2, 3, 5), (-1, 2, 7)):
        direct = (
            selected_base
            + b_value * selected_directions[(0, 5)]
            + c_value * selected_directions[(2, 9)]
            + t_value * selected_directions[(2, 8)]
        ).det(method="domain-ge")
        predicted = finite_determinant.subs({b: b_value, c: c_value, t: t_value})
        if direct != predicted:
            raise AssertionError("finite-selected direct determinant control failed")
        controls.append(
            {
                "B": b_value,
                "C": c_value,
                "T": t_value,
                "determinant": str(direct),
            }
        )
    payload["finite"] = {
        "rows": finite_rows,
        "determinant": str(finite_determinant),
        "degree_B": int(finite_poly.degree(b)),
        "degree_C": int(finite_poly.degree(c)),
        "degree_T": int(finite_poly.degree(t)),
        "term_count": len(finite_poly.terms()),
        "anchor_point": list(anchor_point),
        "anchor_determinant": str(anchor_det),
        "cyclic_component_sizes": [len(component) for component in components],
        "nontrivial_affine_factors": factors,
        "direct_exact_controls": controls,
    }
    persist(payload)
    print(
        "[INFO] finite: degrees "
        f"B={payload['finite']['degree_B']} "
        f"C={payload['finite']['degree_C']} "
        f"T={payload['finite']['degree_T']} "
        f"terms={payload['finite']['term_count']}",
        flush=True,
    )


if __name__ == "__main__":
    main()
