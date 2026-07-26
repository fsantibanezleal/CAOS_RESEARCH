"""EXP-108: select a third maximal-minor chart on the EXP-107 residual fiber."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np
from sympy import Poly, factor_list, gcd, symbols


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
EXP107_DIR = ROOT.parent / "EXP-107-first-three-parameter-graded-lift"
EXP107_RUN = EXP107_DIR / "run.py"
EXP107_ARTIFACT = EXP107_DIR / "artifacts" / "results.json"
PRIME = 998244353
PRIMITIVE_ROOT = 3
TRANSFORM_SIZE = 64
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


def roots_of_unity() -> list[int]:
    root = pow(PRIMITIVE_ROOT, (PRIME - 1) // TRANSFORM_SIZE, PRIME)
    values: list[int] = []
    current = 1
    for _ in range(TRANSFORM_SIZE):
        values.append(current)
        current = current * root % PRIME
    return values


def polynomial_from_coefficients(coefficients: list[int]) -> Poly:
    expression = sum(
        coefficient * y_symbol**degree
        for degree, coefficient in enumerate(coefficients)
        if coefficient
    )
    return Poly(expression, y_symbol, modulus=PRIME)


def reconstruct_fiber_determinant(
    exp103,
    base_matrix: np.ndarray,
    direction_matrix: np.ndarray,
    row_indices: list[int],
    chart_name: str,
) -> tuple[Poly, dict]:
    selected_base = base_matrix[row_indices, :] % PRIME
    selected_direction = direction_matrix[row_indices, :] % PRIME
    direction_rank = len(exp103.pivot_rows(selected_direction, PRIME))
    require(
        direction_rank < TRANSFORM_SIZE,
        f"{chart_name}: direction rank fits the 64-point degree bound",
    )

    started = time.time()
    values = [
        exp103.det_mod(
            (selected_base + selected_direction * value_y) % PRIME,
            PRIME,
        )
        for value_y in roots_of_unity()
    ]
    coefficients = list(values)
    exp103.ntt(coefficients, True, PRIME, PRIMITIVE_ROOT)
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    polynomial = polynomial_from_coefficients(coefficients)
    require(not polynomial.is_zero, f"{chart_name}: determinant polynomial is nonzero")
    require(
        polynomial.degree() <= direction_rank,
        f"{chart_name}: degree obeys the direction-rank bound",
    )

    off_grid_checks = []
    for value_y in (2, 3):
        direct = exp103.det_mod(
            (selected_base + selected_direction * value_y) % PRIME,
            PRIME,
        )
        predicted = int(polynomial.eval(value_y)) % PRIME
        require(
            direct == predicted,
            f"{chart_name}: off-grid determinant check at y={value_y} agrees",
        )
        off_grid_checks.append({"y": value_y, "determinant": direct})

    record = {
        "name": chart_name,
        "row_indices": row_indices,
        "direction_rank_bound": direction_rank,
        "degree_y": polynomial.degree(),
        "terms": len(polynomial.terms()),
        "coefficients_y_low_to_high": [
            int(polynomial.nth(index)) % PRIME
            for index in range(polynomial.degree() + 1)
        ],
        "off_grid_checks": off_grid_checks,
        "seconds": round(time.time() - started, 3),
    }
    return polynomial, record


def factor_record(polynomial: Poly) -> dict:
    content, factors = factor_list(polynomial.as_expr(), modulus=PRIME)
    return {
        "content": int(content) % PRIME,
        "factors": [
            {
                "factor": str(factor),
                "degree": int(Poly(factor, y_symbol, modulus=PRIME).degree()),
                "multiplicity": int(multiplicity),
            }
            for factor, multiplicity in factors
        ],
    }


def main() -> None:
    started = time.time()
    exp107 = load_module("exp107_for_exp108", EXP107_RUN)
    exp103 = exp107.load_module("exp103_for_exp108", exp107.EXP103_RUN)
    exp106 = exp107.load_module("exp106_for_exp108", exp107.EXP106_RUN)
    source = exp103.load_module("exp099_for_exp108", exp103.EXP099_RUN)

    base_coefficients, row_labels, column_labels = exp103.build_polynomial_matrix(source)
    require(
        base_coefficients[0].shape == (289, 125) and len(column_labels) == 125,
        "the full augmented matrix has shape 289 by 125",
    )
    zero = [0] * len(source.LOWER)
    values = list(zero)
    values[source.LOWER.index((0, 7))] = 1
    raw_direction = (
        exp106.dense_augmented(source, row_labels, values) - base_coefficients[1]
    )

    residual_z = -pow(8, -1, PRIME) % PRIME
    residual_u = pow(residual_z, pow(9, -1, PRIME - 1), PRIME)
    require(
        pow(residual_u, 9, PRIME) == residual_z,
        "the unique ninth root reconstructs z=-1/8",
    )
    base_matrix = exp103.matrix_at(
        tuple(matrix % PRIME for matrix in base_coefficients),
        residual_u,
        PRIME,
    )
    direction_matrix = (
        raw_direction % PRIME * pow(residual_u, 8, PRIME)
    ) % PRIME

    prior = json.loads(EXP107_ARTIFACT.read_text(encoding="utf-8"))
    q_coefficients = prior["residual_support"]["fiber_coefficients_y_low_to_high"]
    residual_polynomial = polynomial_from_coefficients(q_coefficients)
    require(
        residual_polynomial.degree() == 12
        and gcd(residual_polynomial, residual_polynomial.diff()).degree() == 0,
        "EXP-107 residual polynomial is squarefree of degree 12",
    )

    row_count = len(row_labels)
    permutations = (
        np.arange(row_count),
        np.arange(row_count - 1, -1, -1),
        np.roll(np.arange(row_count), 73),
        np.roll(np.arange(row_count), 149),
    )
    probes = (1, 2, 3, 5)
    seen: set[tuple[int, ...]] = set()
    chart_records = []
    winning_record = None

    for candidate_index, (probe_y, order) in enumerate(zip(probes, permutations), start=1):
        full_matrix = (base_matrix + direction_matrix * probe_y) % PRIME
        local_rows = exp103.pivot_rows(full_matrix[order, :], PRIME)
        require(
            len(local_rows) == 125,
            f"candidate {candidate_index}: full column rank holds at y={probe_y}",
        )
        row_indices = [int(order[index]) for index in local_rows]
        key = tuple(row_indices)
        if key in seen:
            continue
        seen.add(key)
        chart_name = f"pivot-y{probe_y}-order{candidate_index}"
        determinant, record = reconstruct_fiber_determinant(
            exp103,
            base_matrix,
            direction_matrix,
            row_indices,
            chart_name,
        )
        common = gcd(residual_polynomial, determinant)
        record["probe_y"] = probe_y
        record["gcd_with_Q_degree"] = common.degree()
        record["gcd_with_Q"] = str(common.as_expr())
        record["row_labels"] = [
            list(row_labels[index]) for index in row_indices
        ]
        chart_records.append(record)
        print(
            f"[INFO] {chart_name}: gcd(Q,H) degree={common.degree()}",
            flush=True,
        )
        if common.degree() == 0:
            winning_record = record
            break

    require(chart_records, "at least one distinct candidate chart was reconstructed")
    if winning_record is not None:
        decision = "three_chart_modular_geometric_cover"
    else:
        decision = "residual_factor_survives_four_chart_search"

    result = {
        "experiment": "EXP-108",
        "prime": PRIME,
        "primitive_root": PRIMITIVE_ROOT,
        "residual_z_mod_prime": residual_z,
        "residual_u_mod_prime": residual_u,
        "residual_Q": {
            "degree": residual_polynomial.degree(),
            "coefficients_y_low_to_high": q_coefficients,
            "factorization": factor_record(residual_polynomial),
        },
        "candidate_charts": chart_records,
        "winning_chart": (
            None if winning_record is None else winning_record["name"]
        ),
        "decision": decision,
        "scope": (
            "pilot-prime geometric fiber cover; repeat and exact lifting are "
            "required before a characteristic-zero slice claim"
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
    print(f"RESULT: {decision.upper()}", flush=True)


if __name__ == "__main__":
    main()
