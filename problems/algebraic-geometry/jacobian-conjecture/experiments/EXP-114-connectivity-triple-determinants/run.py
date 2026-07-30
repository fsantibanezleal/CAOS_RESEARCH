"""EXP-114: exact determinants on full-connectivity 36-core triples."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

from sympy import Matrix, Poly, Rational, factor, factor_list, symbols


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


def build_core():
    forced = exp112.forced_polynomial()
    directions = sorted(exp112.exp071.LOWER)
    _, complete_rows = exp112.complete_row_labels(forced, directions)
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
    base = base_full[selected_indices, :]
    normalized = [
        base.inv() * matrix[selected_indices, :]
        for matrix in direction_full
    ]
    adjacency, _, _, _ = exp112.graph_from_matrices(normalized)
    components = exp112.strongly_connected_components(adjacency)
    largest_component = max(components, key=len)
    core = [
        matrix.extract(largest_component, largest_component)
        for matrix in normalized
    ]
    return directions, core


def polynomial_record(expression, variables) -> dict[str, object]:
    polynomial = Poly(expression, *variables, domain="QQ")
    coefficient, factors = factor_list(expression, *variables)
    return {
        "expression": str(expression),
        "total_degree": polynomial.total_degree(),
        "variable_degrees": {
            str(variable): polynomial.degree(variable)
            for variable in variables
        },
        "monomial_count": len(polynomial.terms()),
        "factor_coefficient": str(coefficient),
        "factors": [
            {
                "expression": str(factor_expression),
                "multiplicity": multiplicity,
                "total_degree": Poly(
                    factor_expression, *variables, domain="QQ"
                ).total_degree(),
                "monomial_count": len(
                    Poly(
                        factor_expression, *variables, domain="QQ"
                    ).terms()
                ),
            }
            for factor_expression, multiplicity in factors
        ],
    }


def main() -> None:
    started = time.time()
    directions, core = build_core()
    require(
        len(core) == 51 and all(matrix.shape == (36, 36) for matrix in core),
        "the exact 51-direction 36-core reconstructs",
    )

    triples = {
        "TA": [(0, 1), (0, 7), (2, 9)],
        "TB": [(0, 1), (0, 5), (1, 0)],
    }
    variables = symbols("a b c")
    test_points = [
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, -1),
        (2, -1, 3),
        (-2, 3, 1),
    ]
    results = {}

    for name, points in triples.items():
        indices = [directions.index(point) for point in points]
        symbolic = Matrix.eye(36)
        for variable, index in zip(variables, indices):
            symbolic += variable * core[index]
        determinant_started = time.time()
        determinant = factor(symbolic.det(method="domain-ge"))
        elapsed = time.time() - determinant_started
        record = polynomial_record(determinant, variables)
        record["parameter_points"] = [list(point) for point in points]
        record["elapsed_seconds"] = elapsed
        record["checks"] = []

        for values in test_points:
            substitution = dict(zip(variables, values))
            symbolic_value = Rational(determinant.subs(substitution))
            direct = Matrix.eye(36)
            for value, index in zip(values, indices):
                direct += value * core[index]
            direct_value = direct.det(method="domain-ge")
            require(
                symbolic_value == direct_value,
                f"{name} symbolic and direct determinants agree at {values}",
            )
            record["checks"].append(
                {
                    "point": list(values),
                    "value": str(symbolic_value),
                }
            )

        require(
            Rational(determinant.subs(dict(zip(variables, (0, 0, 0)))))
            == 1,
            f"{name} determinant is normalized to one at the origin",
        )
        results[name] = record
        print(
            f"[INFO] {name}: degree {record['total_degree']}, "
            f"{record['monomial_count']} monomials, "
            f"{len(record['factors'])} factor records, {elapsed:.2f} s",
            flush=True,
        )

    tb_expression = Poly(
        results["TB"]["expression"], *variables, domain="QQ"
    ).as_expr()
    forced_axis = factor(tb_expression.subs({variables[0]: 0, variables[1]: 0}))
    require(
        forced_axis == (1 + variables[2]) ** 13,
        "TB recovers the exact 36-core forced-axis factor (1+c)^13",
    )

    predictions = {
        "TA_nontrivial_factorization": len(results["TA"]["factors"]) > 1
        or any(
            factor_record["multiplicity"] > 1
            for factor_record in results["TA"]["factors"]
        ),
        "TB_nontrivial_factorization": len(results["TB"]["factors"]) > 1
        or any(
            factor_record["multiplicity"] > 1
            for factor_record in results["TB"]["factors"]
        ),
        "at_least_one_nontrivial_factorization": False,
        "distinct_expressions": results["TA"]["expression"]
        != results["TB"]["expression"],
    }
    predictions["at_least_one_nontrivial_factorization"] = (
        predictions["TA_nontrivial_factorization"]
        or predictions["TB_nontrivial_factorization"]
    )
    for prediction, outcome in predictions.items():
        print(
            f"[{'PASS' if outcome else 'REFUTED'}] prediction {prediction}",
            flush=True,
        )

    artifact = {
        "experiment": "EXP-114",
        "variables": [str(variable) for variable in variables],
        "triples": results,
        "tb_forced_axis": str(forced_axis),
        "predictions": predictions,
        "elapsed_seconds": time.time() - started,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"RESULT: FAILED: {error}", file=sys.stderr, flush=True)
        raise
