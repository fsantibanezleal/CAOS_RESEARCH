"""EXP-118: exact weighted chart cover of the finite d=0 quotient residual.

CPU-only. Deterministic exact arithmetic over QQ, with finite-field row-basis
selection used only to choose candidate maximal minors.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from collections import deque
from pathlib import Path

from sympy import (
    Matrix,
    Poly,
    Rational,
    gcd,
    interpolate,
    primerange,
    sympify,
    symbols,
)


HERE = Path(__file__).resolve().parent
E116_PATH = HERE.parent / "EXP-116-boundary-kernel-quotient" / "run.py"
E117_COMPACT = (
    HERE.parent
    / "EXP-117-boundary-51-core-determinant"
    / "artifacts"
    / "compact-factorization.json"
)
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"

spec = importlib.util.spec_from_file_location("exp116", E116_PATH)
exp116 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp116)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def as_mod(value, prime: int) -> int:
    rational = Rational(value)
    numerator = int(rational.p) % prime
    denominator = int(rational.q) % prime
    if denominator == 0:
        raise ZeroDivisionError(f"denominator vanishes modulo {prime}")
    return numerator * pow(denominator, -1, prime) % prime


def matrix_mod(matrix: Matrix, prime: int) -> list[list[int]]:
    return [
        [as_mod(matrix[row, column], prime) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def pivot_columns_mod(transposed: list[list[int]], prime: int) -> list[int]:
    """Return deterministic pivot columns of a row matrix over F_p."""

    work = [row[:] for row in transposed]
    row_count = len(work)
    column_count = len(work[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        candidate = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column] % prime
            ),
            None,
        )
        if candidate is None:
            continue
        work[pivot_row], work[candidate] = work[candidate], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [
            value * inverse % prime for value in work[pivot_row]
        ]
        for row in range(pivot_row + 1, row_count):
            coefficient = work[row][column] % prime
            if coefficient:
                work[row] = [
                    (left - coefficient * right) % prime
                    for left, right in zip(
                        work[row], work[pivot_row], strict=True
                    )
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_columns


def determinant_mod(square: list[list[int]], prime: int) -> int:
    work = [row[:] for row in square]
    determinant = 1
    size = len(work)
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] % prime
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column] % prime
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, size):
            coefficient = work[row][column] * inverse % prime
            if coefficient:
                for inner in range(column + 1, size):
                    work[row][inner] = (
                        work[row][inner]
                        - coefficient * work[column][inner]
                    ) % prime
    return determinant % prime


def evaluate_mod(
    origin_mod: list[list[int]],
    a_mod: list[list[int]],
    b_mod: list[list[int]],
    av: int,
    bv: int,
    prime: int,
) -> list[list[int]]:
    return [
        [
            (
                origin_mod[row][column]
                + av * a_mod[row][column]
                + bv * b_mod[row][column]
            )
            % prime
            for column in range(len(origin_mod[0]))
        ]
        for row in range(len(origin_mod))
    ]


def transpose(values: list[list[int]]) -> list[list[int]]:
    return [list(column) for column in zip(*values, strict=True)]


def solve_covariance_weights(system) -> dict[str, object]:
    matrices = (
        (system["quotient_origin"], 0, "origin"),
        (system["quotient_a"], 7, "a"),
        (system["quotient_b"], 3, "b"),
    )
    row_count, column_count = system["quotient_origin"].shape
    node_count = row_count + column_count
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(node_count)
    ]
    support_counts = {}
    support_records: list[tuple[int, int, int, str]] = []
    for matrix, weight, label in matrices:
        count = 0
        for row in range(row_count):
            for column in range(column_count):
                if matrix[row, column] == 0:
                    continue
                count += 1
                column_node = row_count + column
                # u(row) - u(column_node) = parameter weight, with
                # column exponent c = -u(column_node).
                adjacency[row].append((column_node, weight))
                adjacency[column_node].append((row, -weight))
                support_records.append((row, column, weight, label))
        support_counts[label] = count

    potentials: list[int | None] = [None] * node_count
    components: list[list[int]] = []
    for root in range(node_count):
        if potentials[root] is not None:
            continue
        potentials[root] = 0
        queue = deque([root])
        component = []
        while queue:
            node = queue.popleft()
            component.append(node)
            for neighbor, difference in adjacency[node]:
                # u(node) - u(neighbor) = difference.
                candidate = potentials[node] - difference
                if potentials[neighbor] is None:
                    potentials[neighbor] = candidate
                    queue.append(neighbor)
                elif potentials[neighbor] != candidate:
                    raise AssertionError(
                        "weighted covariance support equations are inconsistent"
                    )
        components.append(component)

    row_weights = [int(potentials[row]) for row in range(row_count)]
    column_weights = [
        -int(potentials[row_count + column])
        for column in range(column_count)
    ]
    for row, column, weight, _ in support_records:
        if row_weights[row] + column_weights[column] != weight:
            raise AssertionError("covariance weight recheck failed")

    digest_payload = json.dumps(
        {
            "row_weights": row_weights,
            "column_weights": column_weights,
            "support_counts": support_counts,
        },
        sort_keys=True,
    ).encode("utf-8")
    return {
        "row_weights": row_weights,
        "column_weights": column_weights,
        "support_counts": support_counts,
        "component_sizes": sorted(
            (len(component) for component in components), reverse=True
        ),
        "sha256": hashlib.sha256(digest_payload).hexdigest().upper(),
    }


def load_residual():
    compact = json.loads(E117_COMPACT.read_text(encoding="utf-8"))
    z = symbols("z")
    expression = sympify(
        compact["b_nonzero_invariant"]["polynomial"], locals={"z": z}
    )
    polynomial = Poly(expression, z, domain="QQ")
    coefficient, factors = polynomial.factor_list()
    require(polynomial.degree() == 9, "EXP-117 invariant has degree nine")
    require(
        gcd(polynomial, polynomial.diff()).degree() == 0,
        "EXP-117 invariant is squarefree",
    )
    return z, polynomial, coefficient, factors


def roots_mod(polynomial: Poly, prime: int) -> list[int]:
    coefficients = [
        as_mod(coefficient, prime) for coefficient in polynomial.all_coeffs()
    ]
    return [
        value
        for value in range(prime)
        if sum(
            coefficient * pow(value, polynomial.degree() - index, prime)
            for index, coefficient in enumerate(coefficients)
        )
        % prime
        == 0
    ]


def candidate_basis_for_factor(
    factor: Poly,
    quotient_matrices: tuple[Matrix, Matrix, Matrix],
    start_prime: int,
) -> dict[str, object]:
    origin, direction_a, direction_b = quotient_matrices
    for prime in primerange(start_prime, 5000):
        if prime % 3 != 2:
            continue
        try:
            roots = roots_mod(factor, prime)
        except ZeroDivisionError:
            continue
        if not roots:
            continue
        origin_mod = matrix_mod(origin, prime)
        a_mod = matrix_mod(direction_a, prime)
        b_mod = matrix_mod(direction_b, prime)
        inverse_three = pow(3, -1, prime - 1)
        for root in roots:
            if root == 0:
                continue
            av = pow(root, inverse_three, prime)
            evaluated = evaluate_mod(
                origin_mod, a_mod, b_mod, av, 1, prime
            )
            rows = pivot_columns_mod(transpose(evaluated), prime)
            if len(rows) != 124:
                continue
            selected = [evaluated[row] for row in rows]
            value = determinant_mod(selected, prime)
            if value == 0:
                continue
            return {
                "prime": int(prime),
                "z": int(root),
                "a": int(av),
                "b": 1,
                "rows": rows,
                "determinant_mod_prime": int(value),
            }
    raise AssertionError(
        f"no full-rank modular representative found for {factor.as_expr()}"
    )


def determinant_weight(
    rows: list[int],
    covariance: dict[str, object],
) -> tuple[int, list[int]]:
    row_weights = covariance["row_weights"]
    column_weights = covariance["column_weights"]
    weight = sum(row_weights[row] for row in rows) + sum(column_weights)
    exponents = []
    for a_exponent in range(125):
        remainder = weight - 7 * a_exponent
        if remainder < 0 or remainder % 3:
            continue
        b_exponent = remainder // 3
        if a_exponent + b_exponent <= 124:
            exponents.append(a_exponent)
    if not exponents:
        raise AssertionError("weighted determinant has no admissible support")
    residue_classes = {exponent % 3 for exponent in exponents}
    require(
        len(residue_classes) == 1,
        "alternative determinant has one a-exponent residue class modulo three",
    )
    return weight, exponents


def exact_determinant_at_a(
    system,
    rows: list[int],
    av: int,
    bv: int = 1,
):
    matrix = (
        system["quotient_origin"]
        + Rational(av) * system["quotient_a"]
        + Rational(bv) * system["quotient_b"]
    )
    return matrix[rows, :].det(method="domain-ge")


def reconstruct_invariant(
    system,
    rows: list[int],
    covariance: dict[str, object],
    chart_index: int,
) -> dict[str, object]:
    z = symbols("z")
    weight, exponents = determinant_weight(rows, covariance)
    residue = exponents[0] % 3
    k_values = [(exponent - residue) // 3 for exponent in exponents]
    minimum_k = min(k_values)
    maximum_k = max(k_values)
    evaluation_count = maximum_k - minimum_k + 1
    if evaluation_count > 60:
        raise AssertionError(
            f"chart {chart_index} requires {evaluation_count} exact evaluations"
        )
    print(
        f"[INFO] chart {chart_index}: weight {weight}, residue {residue}, "
        f"invariant exponents {minimum_k}..{maximum_k}",
        flush=True,
    )

    samples = []
    timings = []
    for av in range(1, evaluation_count + 1):
        started = time.time()
        determinant = exact_determinant_at_a(system, rows, av)
        elapsed = time.time() - started
        if elapsed > 180:
            raise TimeoutError(
                f"chart {chart_index} determinant exceeded 180 seconds"
            )
        timings.append(elapsed)
        sample_z = Rational(av**3)
        invariant_value = determinant / av**residue
        reduced_value = invariant_value / sample_z**minimum_k
        samples.append((sample_z, reduced_value))
        print(
            f"[INFO] chart {chart_index}: exact determinant "
            f"{av}/{evaluation_count} in {elapsed:.2f} s",
            flush=True,
        )

    reduced = Poly(interpolate(samples, z), z, domain="QQ")
    interpolated = Poly(z**minimum_k * reduced.as_expr(), z, domain="QQ")
    require(
        all(
            interpolated.nth(exponent) == 0
            for exponent in range(interpolated.degree() + 1)
            if exponent not in range(
                min(k_values), max(k_values) + 1
            )
        ),
        "interpolated invariant respects the predicted support",
    )

    validation = []
    for av in (evaluation_count + 1, evaluation_count + 2):
        direct = exact_determinant_at_a(system, rows, av)
        predicted = av**residue * interpolated.eval(av**3)
        require(
            direct == predicted,
            f"chart {chart_index} interpolation matches unused a={av}",
        )
        validation.append(
            {"a": av, "b": 1, "determinant": str(direct)}
        )

    return {
        "rows": rows,
        "weighted_degree": int(weight),
        "a_residue_mod_3": int(residue),
        "invariant_min_degree": int(min(k_values)),
        "invariant_max_degree": int(max(k_values)),
        "invariant_polynomial": str(interpolated.as_expr()),
        "invariant_degree": int(interpolated.degree()),
        "invariant_monomial_count": len(interpolated.terms()),
        "exact_evaluation_count": evaluation_count,
        "exact_evaluation_seconds": timings,
        "validation": validation,
    }


def persist_checkpoint(payload: dict[str, object]) -> None:
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def axis_and_origin_checks(system, covariance) -> dict[str, object]:
    axis_matrix = system["quotient_origin"] + system["quotient_a"]
    _, pivots = axis_matrix.T.rref()
    axis_rows = list(pivots)
    require(
        len(axis_rows) == 124,
        "b=0 axis representative (1,0) has exact augmented rank 124",
    )
    axis_determinant = axis_matrix[axis_rows, :].det(method="domain-ge")
    require(
        axis_determinant != 0,
        "b=0 axis alternative minor is exactly nonzero at (1,0)",
    )
    axis_weight, axis_exponents = determinant_weight(axis_rows, covariance)
    require(
        axis_weight % 7 == 0
        and axis_weight // 7 in axis_exponents,
        "b=0 chart admits the required pure a monomial",
    )

    origin = system["quotient_origin"]
    origin_augmented_rank = 124 - len(origin.nullspace())
    origin_coefficient_rank = 123 - len(origin[:, :123].nullspace())
    require(
        (origin_coefficient_rank, origin_augmented_rank) == (112, 113),
        "origin exact quotient rank profile reproduces 112/113",
    )
    return {
        "axis_rows": axis_rows,
        "axis_determinant_at_1_0": str(axis_determinant),
        "axis_weighted_degree": int(axis_weight),
        "axis_a_exponent": int(axis_weight // 7),
        "origin_rank_profile": {
            "coefficient": origin_coefficient_rank,
            "augmented": origin_augmented_rank,
        },
    }


def fixed_chart_factor_control(
    system,
    factor: Poly,
    rows: list[int],
    start_prime: int,
) -> dict[str, object]:
    origin, direction_a, direction_b = (
        system["quotient_origin"],
        system["quotient_a"],
        system["quotient_b"],
    )
    for prime in primerange(start_prime, 10000):
        if prime % 3 != 2:
            continue
        try:
            roots = roots_mod(factor, prime)
        except ZeroDivisionError:
            continue
        if not roots:
            continue
        origin_mod = matrix_mod(origin, prime)
        a_mod = matrix_mod(direction_a, prime)
        b_mod = matrix_mod(direction_b, prime)
        inverse_three = pow(3, -1, prime - 1)
        for root in roots:
            if root == 0:
                continue
            av = pow(root, inverse_three, prime)
            evaluated = evaluate_mod(
                origin_mod, a_mod, b_mod, av, 1, prime
            )
            determinant = determinant_mod(
                [evaluated[row] for row in rows], prime
            )
            if determinant == 0:
                continue
            return {
                "factor": str(factor.as_expr()),
                "prime": int(prime),
                "z": int(root),
                "a": int(av),
                "b": 1,
                "determinant": int(determinant),
            }
    raise AssertionError(
        "fixed exact chart has no good-prime control for "
        f"{factor.as_expr()}"
    )


def main() -> None:
    started = time.time()
    system = exp116.build_quotient()
    exp116.kernel_recheck(system)
    covariance = solve_covariance_weights(system)
    require(
        covariance["support_counts"]["origin"] > 0
        and covariance["support_counts"]["a"] > 0
        and covariance["support_counts"]["b"] > 0,
        "complete quotient support carries exact (7,3) covariance",
    )
    print(
        f"[INFO] covariance digest {covariance['sha256']}",
        flush=True,
    )

    z, residual, residual_coefficient, factors = load_residual()
    factor_records = []
    chart_records = []
    running_gcd = residual.monic()
    quotient_matrices = (
        system["quotient_origin"],
        system["quotient_a"],
        system["quotient_b"],
    )

    for index, (factor, multiplicity) in enumerate(factors, start=1):
        factor_poly = Poly(factor, z, domain="QQ")
        require(multiplicity == 1, f"residual factor {index} is squarefree")
        selection = candidate_basis_for_factor(
            factor_poly, quotient_matrices, 1019 + 100 * index
        )
        print(
            f"[INFO] factor {index}/{len(factors)} selected at "
            f"p={selection['prime']}, z={selection['z']}",
            flush=True,
        )
        chart = reconstruct_invariant(
            system,
            selection["rows"],
            covariance,
            index,
        )
        chart_poly = Poly(
            sympify(
                chart["invariant_polynomial"], locals={"z": z}
            ),
            z,
            domain="QQ",
        )
        running_gcd = gcd(running_gcd, chart_poly).monic()
        factor_record = {
            "expression": str(factor_poly.as_expr()),
            "degree": int(factor_poly.degree()),
            "selection": selection,
            "gcd_after_chart": str(running_gcd.as_expr()),
            "gcd_degree_after_chart": int(running_gcd.degree()),
        }
        factor_records.append(factor_record)
        chart_records.append(chart)
        persist_checkpoint(
            {
                "experiment": "EXP-118",
                "covariance": covariance,
                "residual": str(residual.as_expr()),
                "factor_records": factor_records,
                "charts": chart_records,
                "running_gcd": str(running_gcd.as_expr()),
            }
        )
        print(
            f"[INFO] exact residual gcd degree {running_gcd.degree()}",
            flush=True,
        )
        if running_gcd.degree() == 0:
            break

    require(
        running_gcd.degree() == 0,
        "alternative invariant minors have unit gcd with EXP-117 residual",
    )
    axis_origin = axis_and_origin_checks(system, covariance)
    require(
        len(chart_records) == 1
        and chart_records[0]["invariant_monomial_count"] == 1,
        "one alternative chart reduces to one invariant monomial",
    )
    chart_expression = Poly(
        sympify(
            chart_records[0]["invariant_polynomial"], locals={"z": z}
        ),
        z,
        domain="QQ",
    )
    require(
        chart_records[0]["a_residue_mod_3"] == 2
        and chart_expression.degree() == 35,
        "alternative quotient determinant is a nonzero scalar times a^107",
    )

    # The exact gcd is the characteristic-zero certificate. Independent
    # finite-field representatives stress the selected chart construction.
    modular_controls = []
    for factor_record, chart in zip(
        factor_records, chart_records, strict=True
    ):
        selection = factor_record["selection"]
        prime = int(selection["prime"])
        evaluated = evaluate_mod(
            matrix_mod(system["quotient_origin"], prime),
            matrix_mod(system["quotient_a"], prime),
            matrix_mod(system["quotient_b"], prime),
            int(selection["a"]),
            1,
            prime,
        )
        selected_value = determinant_mod(
            [evaluated[row] for row in chart["rows"]], prime
        )
        require(
            selected_value == int(selection["determinant_mod_prime"]),
            "persisted modular row-basis determinant reproduces",
        )
        modular_controls.append(
            {
                "factor": factor_record["expression"],
                "prime": prime,
                "z": int(selection["z"]),
                "value": selected_value,
            }
        )

    two_prime_component_controls = []
    for factor_index, (factor, _) in enumerate(factors):
        factor_poly = Poly(factor, z, domain="QQ")
        first = fixed_chart_factor_control(
            system,
            factor_poly,
            chart_records[0]["rows"],
            1100 + 200 * factor_index,
        )
        second = fixed_chart_factor_control(
            system,
            factor_poly,
            chart_records[0]["rows"],
            int(first["prime"]) + 2,
        )
        require(
            first["prime"] != second["prime"],
            f"factor {factor_index + 1} has two distinct good-prime controls",
        )
        two_prime_component_controls.extend((first, second))

    artifact = {
        "experiment": "EXP-118",
        "covariance": covariance,
        "residual": {
            "expression": str(residual.as_expr()),
            "coefficient": str(residual_coefficient),
            "degree": int(residual.degree()),
            "factor_count": len(factors),
        },
        "factor_records": factor_records,
        "charts": chart_records,
        "final_gcd": str(running_gcd.as_expr()),
        "final_gcd_degree": int(running_gcd.degree()),
        "axis_and_origin": axis_origin,
        "modular_controls": modular_controls,
        "two_prime_component_controls": two_prime_component_controls,
        "predictions": {
            "complete_weighted_covariance": True,
            "single_a_residue_class_for_all_charts": True,
            "at_most_six_charts": len(chart_records) <= 6,
            "unit_invariant_gcd": running_gcd.degree() == 0,
            "b_zero_nonzero_orbit_covered": True,
            "origin_rank_gap_reproduced": True,
        },
        "scope": (
            "Complete d=0 TB quotient plane only. The d-nonzero proper "
            "intersections, 24-parameter core, full family, (72,108), "
            "degree floor, and JC(2) remain open."
        ),
        "elapsed_seconds": time.time() - started,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"[INFO] elapsed {time.time() - started:.2f} s", flush=True)
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"RESULT: FAILED: {error}", file=sys.stderr, flush=True)
        raise
