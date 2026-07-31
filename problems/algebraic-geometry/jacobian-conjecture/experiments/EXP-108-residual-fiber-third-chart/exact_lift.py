"""Exact characteristic-zero lift for the EXP-108 residual-fiber charts."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import time
from functools import reduce
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment
from sympy import Matrix, Poly, QQ, Rational, factor_list, gcd, resultant, symbols
from sympy.polys.polyfuncs import interpolate


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "exact-results.json"
MODULAR_ARTIFACT = ROOT / "artifacts" / "results.json"
EXP107_DIR = ROOT.parent / "EXP-107-first-three-parameter-graded-lift"
EXP107_RUN = EXP107_DIR / "run.py"
EXP107_ARTIFACT = EXP107_DIR / "artifacts" / "results.json"
EXP105_RUN = (
    ROOT.parent / "EXP-105-mu9-bezout-certificate" / "run.py"
)
PILOT_PRIME = 998244353
y_symbol = symbols("y")


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


def matching_degree_bound(base: Matrix, direction: Matrix) -> int:
    size = base.rows
    weights = np.full((size, size), -1000000, dtype=np.int64)
    for row in range(size):
        for column in range(size):
            if base[row, column] != 0:
                weights[row, column] = 0
            if direction[row, column] != 0:
                weights[row, column] = 1
    selected_rows, selected_columns = linear_sum_assignment(weights, maximize=True)
    selected = weights[selected_rows, selected_columns]
    require(
        bool(np.all(selected >= 0)),
        "the exact fiber matrix has a structurally available perfect matching",
    )
    return int(selected.sum())


def exact_normalized_matrices(
    exp103,
    exp105,
    coefficient_matrices,
    raw_direction,
    row_indices,
) -> tuple[Matrix, Matrix, dict]:
    grading = exp105.grading_certificate(
        exp103,
        coefficient_matrices,
        row_indices,
    )
    require(grading["components"] == 1, "the selected chart grading is connected")
    z_value = Rational(-1, 8)
    size = len(row_indices)
    base_entries = [[Rational(0) for _ in range(size)] for _ in range(size)]
    direction_entries = [
        [Rational(0) for _ in range(size)] for _ in range(size)
    ]

    for local_row, source_row in enumerate(row_indices):
        for column in range(size):
            weight_sum = (
                grading["row_weights"][local_row]
                + grading["column_weights"][column]
            )
            for exponent, matrix in zip(exp103.EXPONENTS, coefficient_matrices):
                coefficient = int(matrix[source_row, column])
                if coefficient == 0:
                    continue
                require(
                    (exponent - weight_sum) % 9 == 0,
                    "base entry obeys the lifted integer grading",
                )
                base_entries[local_row][column] += (
                    coefficient * z_value ** ((exponent - weight_sum) // 9)
                )

            coefficient = int(raw_direction[source_row, column])
            if coefficient != 0:
                require(
                    (8 - weight_sum) % 9 == 0,
                    "promoted direction obeys the lifted integer grading",
                )
                direction_entries[local_row][column] += (
                    coefficient * z_value ** ((8 - weight_sum) // 9)
                )

    return Matrix(base_entries), Matrix(direction_entries), grading


def exact_determinant_polynomial(
    chart_name: str,
    base: Matrix,
    direction: Matrix,
) -> tuple[Poly, dict]:
    degree_bound = matching_degree_bound(base, direction)
    values = []
    started = time.time()
    value_hash = hashlib.sha256()
    for node in range(degree_bound + 1):
        determinant = (base + node * direction).det(method="domain-ge")
        values.append((node, determinant))
        value_hash.update(f"{node}:{determinant}\n".encode("ascii"))
        print(
            f"[INFO] {chart_name}: exact determinant "
            f"{node + 1}/{degree_bound + 1} in {time.time() - started:.1f} s",
            flush=True,
        )

    polynomial = Poly(interpolate(values, y_symbol), y_symbol, domain=QQ)
    require(
        polynomial.degree() <= degree_bound,
        f"{chart_name}: exact interpolant respects the matching bound",
    )
    control_node = degree_bound + 1
    control_determinant = (
        base + control_node * direction
    ).det(method="domain-ge")
    require(
        polynomial.eval(control_node) == control_determinant,
        f"{chart_name}: independent exact determinant confirms interpolation",
    )
    content, primitive = polynomial.primitive()
    require(
        all(coefficient.q == 1 for coefficient in primitive.all_coeffs()),
        f"{chart_name}: primitive polynomial has integer coefficients",
    )
    record = {
        "name": chart_name,
        "matching_degree_bound": degree_bound,
        "exact_degree": polynomial.degree(),
        "integer_content": str(content),
        "primitive_coefficients_y_low_to_high": [
            int(primitive.nth(index))
            for index in range(primitive.degree() + 1)
        ],
        "interpolation_nodes": degree_bound + 1,
        "interpolation_value_sha256": value_hash.hexdigest().upper(),
        "independent_check": {
            "y": control_node,
            "determinant": str(control_determinant),
        },
        "seconds": round(time.time() - started, 3),
    }
    return primitive, record


def proportional_mod_prime(exact: Poly, modular_coefficients: list[int]) -> bool:
    exact_coefficients = [
        int(exact.nth(index)) % PILOT_PRIME
        for index in range(exact.degree() + 1)
    ]
    length = max(len(exact_coefficients), len(modular_coefficients))
    exact_coefficients += [0] * (length - len(exact_coefficients))
    modular_coefficients += [0] * (length - len(modular_coefficients))
    pivot = next(
        (index for index, coefficient in enumerate(modular_coefficients) if coefficient),
        None,
    )
    if pivot is None or exact_coefficients[pivot] == 0:
        return False
    scale = (
        exact_coefficients[pivot]
        * pow(modular_coefficients[pivot], -1, PILOT_PRIME)
        % PILOT_PRIME
    )
    return all(
        left == scale * right % PILOT_PRIME
        for left, right in zip(exact_coefficients, modular_coefficients)
    )


def integer_bezout(first: Poly, second: Poly) -> dict:
    coefficient_first, coefficient_second, divisor = first.gcdex(second)
    require(divisor.degree() == 0, "exact polynomial gcd is one")
    coefficient_first = Poly(
        coefficient_first.as_expr() / divisor.as_expr(),
        y_symbol,
        domain=QQ,
    )
    coefficient_second = Poly(
        coefficient_second.as_expr() / divisor.as_expr(),
        y_symbol,
        domain=QQ,
    )
    denominators = [
        coefficient.q
        for polynomial in (coefficient_first, coefficient_second)
        for coefficient in polynomial.all_coeffs()
    ]
    constant = reduce(math.lcm, (int(value) for value in denominators), 1)
    integer_first = Poly(
        coefficient_first.as_expr() * constant,
        y_symbol,
        domain=QQ,
    )
    integer_second = Poly(
        coefficient_second.as_expr() * constant,
        y_symbol,
        domain=QQ,
    )
    require(
        all(
            coefficient.q == 1
            for polynomial in (integer_first, integer_second)
            for coefficient in polynomial.all_coeffs()
        ),
        "cleared Bezout coefficients are integral",
    )
    integer_first = Poly(integer_first.as_expr(), y_symbol, domain="ZZ")
    integer_second = Poly(integer_second.as_expr(), y_symbol, domain="ZZ")
    identity = integer_first * first + integer_second * second
    require(
        identity.degree() == 0 and int(identity.nth(0)) == constant,
        "exact integer Bezout identity verifies",
    )
    common_content = reduce(
        math.gcd,
        [
            abs(int(coefficient))
            for polynomial in (integer_first, integer_second)
            for coefficient in polynomial.all_coeffs()
        ]
        + [abs(constant)],
        0,
    )
    if common_content > 1:
        integer_first = Poly(
            integer_first.as_expr() // common_content,
            y_symbol,
            domain="ZZ",
        )
        integer_second = Poly(
            integer_second.as_expr() // common_content,
            y_symbol,
            domain="ZZ",
        )
        constant //= common_content
    return {
        "A_coefficients_y_low_to_high": [
            int(integer_first.nth(index))
            for index in range(integer_first.degree() + 1)
        ],
        "B_coefficients_y_low_to_high": [
            int(integer_second.nth(index))
            for index in range(integer_second.degree() + 1)
        ],
        "constant": str(constant),
        "identity": "A(y)*Q(y) + B(y)*H(y) = constant",
    }


def main() -> None:
    started = time.time()
    exp107 = load_module("exp107_for_exp108_exact", EXP107_RUN)
    exp103 = exp107.load_module("exp103_for_exp108_exact", exp107.EXP103_RUN)
    exp106 = exp107.load_module("exp106_for_exp108_exact", exp107.EXP106_RUN)
    exp105 = load_module("exp105_for_exp108_exact", EXP105_RUN)
    source = exp103.load_module("exp099_for_exp108_exact", exp103.EXP099_RUN)

    coefficient_matrices, row_labels, _ = exp103.build_polynomial_matrix(source)
    values = [0] * len(source.LOWER)
    values[source.LOWER.index((0, 7))] = 1
    raw_direction = (
        exp106.dense_augmented(source, row_labels, values)
        - coefficient_matrices[1]
    )
    first_rows = exp103.checkpoint_row_indices(row_labels)

    modular = json.loads(MODULAR_ARTIFACT.read_text(encoding="utf-8"))
    winning_name = modular["winning_chart"]
    winning = next(
        chart
        for chart in modular["candidate_charts"]
        if chart["name"] == winning_name
    )
    winning_rows = [
        row_labels.index(tuple(label)) for label in winning["row_labels"]
    ]
    require(
        len(winning_rows) == len(set(winning_rows)) == 125,
        "the modular winning chart supplies 125 distinct exact rows",
    )

    first_base, first_direction, first_grading = exact_normalized_matrices(
        exp103,
        exp105,
        coefficient_matrices,
        raw_direction,
        first_rows,
    )
    third_base, third_direction, third_grading = exact_normalized_matrices(
        exp103,
        exp105,
        coefficient_matrices,
        raw_direction,
        winning_rows,
    )
    first_polynomial, first_record = exact_determinant_polynomial(
        "residual-Q",
        first_base,
        first_direction,
    )
    third_polynomial, third_record = exact_determinant_polynomial(
        "third-chart-H",
        third_base,
        third_direction,
    )

    prior = json.loads(EXP107_ARTIFACT.read_text(encoding="utf-8"))
    require(
        proportional_mod_prime(
            first_polynomial,
            list(prior["residual_support"]["fiber_coefficients_y_low_to_high"]),
        ),
        "exact Q reduces proportionally to the EXP-107 pilot",
    )
    require(
        proportional_mod_prime(
            third_polynomial,
            list(winning["coefficients_y_low_to_high"]),
        ),
        "exact H reduces proportionally to the EXP-108 pilot",
    )
    common = gcd(first_polynomial, third_polynomial)
    require(common.degree() == 0, "the exact residual-fiber polynomials are coprime")
    first_factorization = factor_list(first_polynomial.as_expr())
    third_factorization = factor_list(third_polynomial.as_expr())
    require(
        len(first_factorization[1]) == 1
        and Poly(first_factorization[1][0][0], y_symbol).degree() == 12,
        "the exact degree-12 residual polynomial is irreducible over Q",
    )
    require(
        sorted(
            Poly(factor, y_symbol).degree()
            for factor, _ in third_factorization[1]
        )
        == [1, 2, 4, 6],
        "the exact third-chart polynomial factors in degrees 1, 2, 4, and 6",
    )
    bezout = integer_bezout(first_polynomial, third_polynomial)
    exact_resultant = resultant(
        first_polynomial.as_expr(),
        third_polynomial.as_expr(),
        y_symbol,
    )
    require(exact_resultant != 0, "the exact resultant is nonzero")

    result = {
        "experiment": "EXP-108-exact-lift",
        "fiber": "z=-1/8",
        "first_chart": first_record,
        "third_chart": third_record,
        "first_grading": first_grading,
        "third_grading": third_grading,
        "exact_gcd": str(common.as_expr()),
        "exact_factorizations": {
            "Q": str(first_factorization),
            "H": str(third_factorization),
        },
        "exact_resultant": str(exact_resultant),
        "integer_bezout": bezout,
        "decision": "exact_three_chart_residual_fiber_cover",
        "proof_scope": (
            "the first and third exact maximal minors have no common zero on "
            "the only fiber z=-1/8 left by G(z)=(8z+1)^14"
        ),
        "nonclaim": (
            "this closes the declared (0,1)/(1,7)/(0,7) coefficient slice, "
            "not the remaining GGHV coefficients or JC(2)"
        ),
        "seconds": round(time.time() - started, 3),
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print("RESULT: EXACT_THREE_CHART_RESIDUAL_FIBER_COVER", flush=True)


if __name__ == "__main__":
    main()
