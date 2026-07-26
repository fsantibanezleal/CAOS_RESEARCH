"""EXP-107: bivariate graded maximal minors for the first three-parameter lift."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment
from sympy import Poly, factor_list, gcd, groebner, symbols


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
CHECKPOINT = ROOT / "artifacts" / "checkpoint.json"
EXP103_DIR = ROOT.parent / "EXP-103-residual-curve-determinantal-divisor"
EXP103_RUN = EXP103_DIR / "run.py"
EXP103_ARTIFACT = EXP103_DIR / "artifacts" / "results.json"
EXP105_ARTIFACT = (
    ROOT.parent
    / "EXP-105-mu9-bezout-certificate"
    / "artifacts"
    / "results.json"
)
EXP106_RUN = ROOT.parent / "EXP-106-graded-direction-lift" / "run.py"

PRIME = 998244353
PRIMITIVE_ROOT = 3
Z_SIZE = 16
Y_SIZE = 64
z_symbol, y_symbol = symbols("z y")


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


def assignment_bounds(coefficient_matrices, exponents):
    size = coefficient_matrices[0].shape[0]
    maximum = np.full((size, size), -1000000, dtype=np.int64)
    minimum = np.full((size, size), 1000000, dtype=np.int64)
    for exponent, matrix in zip(exponents, coefficient_matrices):
        mask = matrix != 0
        maximum[mask] = np.maximum(maximum[mask], exponent)
        minimum[mask] = np.minimum(minimum[mask], exponent)
    max_rows, max_columns = linear_sum_assignment(maximum, maximize=True)
    min_rows, min_columns = linear_sum_assignment(minimum)
    return (
        int(minimum[min_rows, min_columns].sum()),
        int(maximum[max_rows, max_columns].sum()),
    )


def roots_of_unity(size: int):
    root = pow(PRIMITIVE_ROOT, (PRIME - 1) // size, PRIME)
    values = []
    current = 1
    for _ in range(size):
        values.append(current)
        current = current * root % PRIME
    return values


def bivariate_polynomial(
    exp103,
    base_coefficients,
    direction,
    row_indices,
    valuation,
    chart_name,
):
    selected_base = tuple(matrix[row_indices, :] % PRIME for matrix in base_coefficients)
    selected_direction = direction[row_indices, :] % PRIME
    z_values = roots_of_unity(Z_SIZE)
    y_values = roots_of_unity(Y_SIZE)
    inverse_nine = pow(9, -1, PRIME - 1)
    evaluations = [[0] * Y_SIZE for _ in range(Z_SIZE)]
    started = time.time()

    for z_index, value_z in enumerate(z_values):
        value_u = pow(value_z, inverse_nine, PRIME)
        base_at_u = exp103.matrix_at(selected_base, value_u, PRIME)
        direction_scale = pow(value_u, 8, PRIME)
        valuation_inverse = pow(pow(value_u, valuation, PRIME), -1, PRIME)
        for y_index, value_y in enumerate(y_values):
            matrix = (
                base_at_u
                + selected_direction * (direction_scale * value_y % PRIME)
            ) % PRIME
            evaluations[z_index][y_index] = (
                exp103.det_mod(matrix, PRIME) * valuation_inverse % PRIME
            )
        print(
            f"[INFO] {chart_name}: z-grid {z_index + 1}/{Z_SIZE} "
            f"in {time.time() - started:.1f} s",
            flush=True,
        )

    # Invert first in y and then in z.
    for row in evaluations:
        exp103.ntt(row, True, PRIME, PRIMITIVE_ROOT)
    for y_index in range(Y_SIZE):
        column = [evaluations[z_index][y_index] for z_index in range(Z_SIZE)]
        exp103.ntt(column, True, PRIME, PRIMITIVE_ROOT)
        for z_index, value in enumerate(column):
            evaluations[z_index][y_index] = value

    nonzero = [
        (z_index, y_index, int(evaluations[z_index][y_index]))
        for z_index in range(Z_SIZE)
        for y_index in range(Y_SIZE)
        if evaluations[z_index][y_index]
    ]
    require(nonzero, f"{chart_name}: reconstructed bivariate determinant is nonzero")
    z_degree = max(item[0] for item in nonzero)
    y_degree = max(item[1] for item in nonzero)

    # Direct off-grid control.
    check_z = 2
    check_y = 3
    check_u = pow(check_z, inverse_nine, PRIME)
    direct_matrix = (
        exp103.matrix_at(selected_base, check_u, PRIME)
        + selected_direction * (pow(check_u, 8, PRIME) * check_y % PRIME)
    ) % PRIME
    direct = (
        exp103.det_mod(direct_matrix, PRIME)
        * pow(pow(check_u, valuation, PRIME), -1, PRIME)
        % PRIME
    )
    predicted = 0
    for exponent_z, exponent_y, coefficient in nonzero:
        predicted = (
            predicted
            + coefficient
            * pow(check_z, exponent_z, PRIME)
            * pow(check_y, exponent_y, PRIME)
        ) % PRIME
    require(direct == predicted, f"{chart_name}: off-grid determinant check agrees")

    expression = sum(
        coefficient * z_symbol**exponent_z * y_symbol**exponent_y
        for exponent_z, exponent_y, coefficient in nonzero
    )
    polynomial = Poly(expression, z_symbol, y_symbol, modulus=PRIME)
    record = {
        "name": chart_name,
        "valuation_u": valuation,
        "z_degree": z_degree,
        "y_degree": y_degree,
        "terms": len(nonzero),
        "coefficients_sparse": nonzero,
        "off_grid_check": {"z": check_z, "y": check_y, "determinant": direct},
        "seconds": round(time.time() - started, 3),
    }
    return polynomial, record


def restriction_coefficients(polynomial: Poly):
    restricted = Poly(polynomial.as_expr().subs(y_symbol, 0), z_symbol, modulus=PRIME)
    return [int(restricted.nth(index)) % PRIME for index in range(restricted.degree() + 1)]


def proportional(left, right):
    length = max(len(left), len(right))
    left = left + [0] * (length - len(left))
    right = right + [0] * (length - len(right))
    pivot = next((index for index, value in enumerate(right) if value), None)
    if pivot is None or left[pivot] == 0:
        return False, None
    scale = left[pivot] * pow(right[pivot], -1, PRIME) % PRIME
    return all(a % PRIME == scale * (b % PRIME) % PRIME for a, b in zip(left, right)), scale


def main() -> None:
    started = time.time()
    exp103 = load_module("exp103_for_exp107", EXP103_RUN)
    exp106 = load_module("exp106_for_exp107", EXP106_RUN)
    source = exp103.load_module("exp099_for_exp107", exp103.EXP099_RUN)
    base_coefficients, row_labels, _ = exp103.build_polynomial_matrix(source)
    zero = [0] * len(source.LOWER)
    values = list(zero)
    values[source.LOWER.index((0, 7))] = 1
    base = base_coefficients[1]
    direction = exp106.dense_augmented(source, row_labels, values) - base

    exp103_result = json.loads(EXP103_ARTIFACT.read_text(encoding="utf-8"))
    exp105_result = json.loads(EXP105_ARTIFACT.read_text(encoding="utf-8"))
    first_rows = exp103.checkpoint_row_indices(row_labels)
    second_rows = next(
        chart["row_indices"]
        for chart in exp103_result["prime_runs"][0]["charts"]
        if chart["name"] == "pivot-u2"
    )

    chart_data = []
    for name, rows, expected_bounds, rank_bound in (
        ("exp102-chart", first_rows, (1520, 1646), 53),
        ("endpoint-safe-chart", second_rows, (777, 903), 41),
    ):
        selected_matrices = (
            base_coefficients[0][rows, :],
            base_coefficients[1][rows, :],
            direction[rows, :],
            base_coefficients[2][rows, :],
            base_coefficients[3][rows, :],
        )
        bounds = assignment_bounds(selected_matrices, (0, 7, 8, 9, 14))
        require(bounds == expected_bounds, f"{name}: assignment bounds reconstruct")
        require(
            (bounds[1] - bounds[0]) // 9 == 14,
            f"{name}: graded z-width is 14",
        )
        direction_rank = len(exp103.pivot_rows(direction[rows, :], PRIME))
        require(direction_rank == rank_bound, f"{name}: y-degree rank bound reconstructs")
        polynomial, record = bivariate_polynomial(
            exp103,
            base_coefficients,
            direction,
            rows,
            bounds[0],
            name,
        )
        record["assignment_bounds_u"] = list(bounds)
        record["direction_rank_bound"] = direction_rank
        chart_data.append((polynomial, record))
        checkpoint = {
            "experiment": "EXP-107",
            "prime": PRIME,
            "charts": [item[1] for item in chart_data],
            "state": "minor_reconstruction",
        }
        CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
        CHECKPOINT.write_text(
            json.dumps(checkpoint, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    first_polynomial, first_record = chart_data[0]
    second_polynomial, second_record = chart_data[1]

    first_primitive = exp105_result["first_determinant"][
        "primitive_coefficients_z_low_to_high"
    ]
    first_content = int(exp105_result["first_determinant"]["integer_content"]) % PRIME
    expected_first = [0] * 12 + [
        first_content * coefficient % PRIME for coefficient in first_primitive
    ]
    first_ok, first_scale = proportional(
        restriction_coefficients(first_polynomial), expected_first
    )
    require(first_ok and first_scale == 1, "first y=0 restriction equals z^12 times EXP-105 F")

    second_primitive = exp105_result["second_determinant"][
        "primitive_coefficients_z_low_to_high"
    ]
    second_content = int(exp105_result["second_determinant"]["integer_content"]) % PRIME
    expected_second = [
        second_content * coefficient % PRIME for coefficient in second_primitive
    ]
    second_ok, second_scale = proportional(
        restriction_coefficients(second_polynomial), expected_second
    )
    require(second_ok and second_scale == 1, "second y=0 restriction equals EXP-105 G")
    require(
        second_record["y_degree"] == 0,
        "endpoint-safe chart is exactly independent of the promoted coordinate y",
    )

    common_factor = gcd(first_polynomial, second_polynomial)
    common_factor_degree = common_factor.total_degree()
    print(f"[INFO] multivariate gcd total degree={common_factor_degree}", flush=True)

    groebner_started = time.time()
    basis = groebner(
        [first_polynomial.as_expr(), second_polynomial.as_expr()],
        y_symbol,
        z_symbol,
        modulus=PRIME,
        order="lex",
    )
    basis_strings = [str(item.as_expr()) for item in basis.polys]
    contains_one = any(item.total_degree() == 0 for item in basis.polys)
    zero_dimensional = basis.is_zero_dimensional
    print(
        f"[INFO] Groebner basis size={len(basis.polys)}, "
        f"contains_one={contains_one}, zero_dimensional={zero_dimensional}, "
        f"seconds={time.time() - groebner_started:.1f}",
        flush=True,
    )

    residual_z = -pow(8, -1, PRIME) % PRIME
    residual_polynomial = Poly(
        first_polynomial.as_expr().subs(z_symbol, residual_z),
        y_symbol,
        modulus=PRIME,
    )
    residual_derivative_gcd = gcd(residual_polynomial, residual_polynomial.diff())
    require(
        residual_polynomial.degree() == 12,
        "the reduced residual fiber has degree 12 in y",
    )
    require(
        residual_derivative_gcd.degree() == 0,
        "the reduced residual fiber is squarefree",
    )
    residual_content, residual_factors = factor_list(
        residual_polynomial.as_expr(),
        modulus=PRIME,
    )
    residual_factor_record = {
        "content": int(residual_content) % PRIME,
        "factors": [
            {
                "factor": str(factor),
                "degree": int(Poly(factor, y_symbol, modulus=PRIME).degree()),
                "multiplicity": int(multiplicity),
            }
            for factor, multiplicity in residual_factors
        ],
    }
    print(
        "[INFO] residual fiber factor degrees="
        f"{[item['degree'] for item in residual_factor_record['factors']]}",
        flush=True,
    )

    if contains_one:
        decision = "two_chart_modular_unit_ideal"
    elif zero_dimensional:
        decision = "finite_modular_residual"
    else:
        decision = "positive_dimensional_modular_residual"

    result = {
        "experiment": "EXP-107",
        "prime": PRIME,
        "invariant_coordinates": {"z": "u^9", "y": "v/u", "v_point": [0, 7]},
        "charts": [first_record, second_record],
        "restriction_controls": {
            "first_equals_z12_F": first_ok,
            "second_equals_G": second_ok,
        },
        "multivariate_gcd_total_degree": common_factor_degree,
        "multivariate_gcd": str(common_factor.as_expr()),
        "residual_support": {
            "z_equation": "(8*z + 1)^14",
            "z_value_mod_prime": residual_z,
            "fiber_degree_y": residual_polynomial.degree(),
            "fiber_coefficients_y_low_to_high": [
                int(residual_polynomial.nth(index)) % PRIME
                for index in range(residual_polynomial.degree() + 1)
            ],
            "fiber_squarefree": residual_derivative_gcd.degree() == 0,
            "fiber_factorization": residual_factor_record,
        },
        "factorizations": {
            "status": "skipped",
            "reason": "SymPy does not implement multivariate factorization over finite fields",
        },
        "groebner_basis": basis_strings,
        "groebner_basis_size": len(basis.polys),
        "contains_one": contains_one,
        "zero_dimensional": zero_dimensional,
        "decision": decision,
        "scope": (
            "modular pilot on the promoted three-parameter slice; no "
            "characteristic-zero coverage claim without exact lifting"
        ),
        "total_seconds": round(time.time() - started, 3),
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
