"""EXP-102: exact third minor on the residual two-parameter curve."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

from sympy import (
    GF,
    Poly,
    Rational,
    cancel,
    factor,
    fraction,
    symbols,
    sympify,
    together,
)
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
EXP101_DIR = ROOT.parent / "EXP-101-two-parameter-minor-stratum"
EXP101_RUN = EXP101_DIR / "run.py"
EXP101_ARTIFACT = EXP101_DIR / "artifacts" / "results.json"
u = symbols("u")


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


def mod_value(value, prime: int) -> int:
    rational = Rational(value)
    return int(rational.p % prime) * pow(int(rational.q % prime), -1, prime) % prime


def pivot_columns_mod_prime(matrix, prime: int) -> list[int]:
    data = [
        [mod_value(matrix[row, column], prime) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(matrix.cols):
        selected = next(
            (row for row in range(pivot_row, matrix.rows) if data[row][column]),
            None,
        )
        if selected is None:
            continue
        data[pivot_row], data[selected] = data[selected], data[pivot_row]
        inverse = pow(data[pivot_row][column], -1, prime)
        for current_column in range(column, matrix.cols):
            data[pivot_row][current_column] = (
                data[pivot_row][current_column] * inverse
            ) % prime
        for row in range(pivot_row + 1, matrix.rows):
            coefficient = data[row][column]
            if coefficient:
                for current_column in range(column, matrix.cols):
                    data[row][current_column] = (
                        data[row][current_column]
                        - coefficient * data[pivot_row][current_column]
                    ) % prime
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == matrix.rows:
            break
    return pivot_columns


def main() -> None:
    started = time.time()
    exp101 = load_module("exp101_tools", EXP101_RUN)
    source = exp101.load_exp099()
    prior = json.loads(EXP101_ARTIFACT.read_text(encoding="utf-8"))
    zero = [Rational(0)] * len(source.LOWER)
    rhs_column = len(source.NQ)

    # Reconstruct the first selected minor.
    augmented_base, base_row_labels = source.augmented_matrix(zero)
    _, first_row_pivots = augmented_base.T.rref()
    first_row_indices = list(first_row_pivots)[:125]
    first_rows = [base_row_labels[index] for index in first_row_indices]
    first_row_block = augmented_base[first_row_indices, :]
    _, first_column_pivots = first_row_block.rref()
    first_columns = list(first_column_pivots)[:125]
    if rhs_column not in first_columns:
        first_columns = first_columns[:124] + [rhs_column]

    # Load the second minor selection persisted by EXP-101.
    second_data = prior["rational_zero_search"]["alternative_minor"]
    if second_data is None:
        raise RuntimeError("EXP-101 did not persist an alternative minor")
    second_rows = [tuple(label) for label in second_data["row_labels"]]
    second_columns = []
    for column in second_data["columns"]:
        if column == "rhs":
            second_columns.append(rhs_column)
        else:
            second_columns.append(source.NQ.index(tuple(column)))

    point_s = Rational(8)
    point_t = Rational(9)
    values = list(zero)
    values[source.LOWER.index((0, 1))] = point_s
    values[source.LOWER.index((1, 7))] = point_t

    first_ratio = sympify(prior["determinant_ratio"], locals={"s": exp101.s, "t": exp101.t})
    second_polynomial = sympify(
        prior["alternative_minor_polynomial"],
        locals={"s": exp101.s, "t": exp101.t},
    )
    first_det = cancel(first_ratio.subs({exp101.s: point_s, exp101.t: point_t}))
    second_det = cancel(
        second_polynomial.subs({exp101.s: point_s, exp101.t: point_t})
    )
    require(first_det == 0, "the first minor vanishes at the residual-curve point (8,9)")
    require(second_det == 0, "the second minor vanishes at the residual-curve point (8,9)")
    print(f"[INFO] old-minor check completed in {time.time() - started:.2f} s", flush=True)

    augmented_at_point, row_labels_at_point = source.augmented_matrix(values)
    rank_prime = 2147483629
    bracket_rank = (
        DomainMatrix.from_Matrix(augmented_at_point[:, :rhs_column])
        .convert_to(GF(rank_prime))
        .rank()
    )
    augmented_rank = (
        DomainMatrix.from_Matrix(augmented_at_point)
        .convert_to(GF(rank_prime))
        .rank()
    )
    print(
        f"[INFO] at (8,9): rank M={bracket_rank}, rank [M|b]={augmented_rank}",
        flush=True,
    )
    require(
        bracket_rank == 124 and augmented_rank == 125,
        "the residual-curve point remains exactly inconsistency-certified",
    )
    print(f"[INFO] rank check completed in {time.time() - started:.2f} s", flush=True)

    third_row_indices = pivot_columns_mod_prime(
        augmented_at_point.T, rank_prime
    )[:125]
    third_rows = [row_labels_at_point[index] for index in third_row_indices]
    third_row_block = augmented_at_point[third_row_indices, :]
    third_columns = pivot_columns_mod_prime(third_row_block, rank_prime)[:125]
    require(rhs_column in third_columns, "the third minor includes the RHS column")

    third_base = source.selected_square(values, third_rows, third_columns)
    third_det_reference = third_base.det(method="domain-ge")
    require(third_det_reference != 0, "the third minor is nonzero at (8,9)")
    print(f"[INFO] third-minor selection completed in {time.time() - started:.2f} s", flush=True)

    values_s = list(values)
    values_s[source.LOWER.index((0, 1))] += 1
    values_t = list(values)
    values_t[source.LOWER.index((1, 7))] += 1
    third_direction_s = (
        source.selected_square(values_s, third_rows, third_columns) - third_base
    )
    third_direction_t = (
        source.selected_square(values_t, third_rows, third_columns) - third_base
    )

    rank_prime = 2147483629

    def modular_rank(matrix):
        return DomainMatrix.from_Matrix(matrix).convert_to(GF(rank_prime)).rank()

    checkpoint = {
        "reference_point": {"s": "8", "t": "9"},
        "old_minor_determinants": [str(first_det), str(second_det)],
        "bracket_rank": bracket_rank,
        "augmented_rank": augmented_rank,
        "third_minor": {
            "row_labels": [list(label) for label in third_rows],
            "columns": [
                "rhs" if column == rhs_column else list(source.NQ[column])
                for column in third_columns
            ],
            "determinant_at_reference": str(third_det_reference),
            "rank_probe_prime": rank_prime,
            "direction_s_modular_rank": modular_rank(third_direction_s),
            "direction_t_modular_rank": modular_rank(third_direction_t),
            "combined_direction_modular_rank": modular_rank(
                third_direction_s.row_join(third_direction_t)
            ),
        },
    }
    checkpoint_path = ROOT / "artifacts" / "checkpoint.json"
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    checkpoint_payload = json.dumps(checkpoint, indent=2, sort_keys=True) + "\n"
    checkpoint_path.write_text(checkpoint_payload, encoding="utf-8", newline="\n")
    print(
        f"[PASS] wrote preflight checkpoint with combined direction rank "
        f"{checkpoint['third_minor']['combined_direction_modular_rank']} mod {rank_prime}",
        flush=True,
    )
    if os.environ.get("EXP102_PREFLIGHT_ONLY") == "1":
        print("RESULT: PREFLIGHT_CHECKPOINT_ONLY", flush=True)
        return

    print("[INFO] computing shifted third-minor polynomial", flush=True)
    shifted_ratio, combined_rank, _, _ = exp101.reduced_determinant(
        third_base, third_direction_s, third_direction_t
    )
    print(f"[INFO] third-minor combined rank r={combined_rank}", flush=True)
    symbol_s = exp101.s
    symbol_t = exp101.t
    third_polynomial = factor(
        third_det_reference
        * shifted_ratio.subs(
            {
                symbol_s: symbol_s - point_s,
                symbol_t: symbol_t - point_t,
            },
            simultaneous=True,
        )
    )
    require(
        Poly(third_polynomial, symbol_s, symbol_t, domain="QQ").eval(
            {symbol_s: point_s, symbol_t: point_t}
        )
        == third_det_reference,
        "the third polynomial reproduces its reference determinant",
    )

    parameter_s = 8 * u**7
    parameter_t = (8 * u**9 + 1) / u**7
    pullback = cancel(
        third_polynomial.subs(
            {symbol_s: parameter_s, symbol_t: parameter_t},
            simultaneous=True,
        )
    )
    pullback_numerator, pullback_denominator = fraction(together(pullback))
    pullback_numerator = factor(pullback_numerator)
    pullback_denominator = factor(pullback_denominator)
    require(pullback_numerator != 0, "the third minor does not vanish identically on the curve")

    numerator_poly = Poly(pullback_numerator, u, domain="QQ")
    numerator_terms = numerator_poly.terms()
    numerator_is_monomial = len(numerator_terms) == 1
    print(
        f"[INFO] pullback numerator degree={numerator_poly.degree()}, "
        f"terms={len(numerator_terms)}",
        flush=True,
    )
    print(f"[INFO] pullback numerator factorization: {pullback_numerator}", flush=True)

    direct_checks = []
    for value_u in (Rational(1), Rational(2), Rational(1, 2)):
        value_s = 8 * value_u**7
        value_t = (8 * value_u**9 + 1) / value_u**7
        direct_values = list(zero)
        direct_values[source.LOWER.index((0, 1))] = value_s
        direct_values[source.LOWER.index((1, 7))] = value_t
        direct_det = source.selected_square(
            direct_values, third_rows, third_columns
        ).det(method="domain-ge")
        predicted_det = cancel(pullback.subs(u, value_u))
        require(
            direct_det == predicted_det,
            f"direct third determinant agrees on the curve at u={value_u}",
        )
        direct_checks.append(
            {
                "u": str(value_u),
                "s": str(value_s),
                "t": str(value_t),
                "determinant": str(direct_det),
            }
        )

    rational_roots = {
        str(root): multiplicity
        for root, multiplicity in numerator_poly.ground_roots().items()
        if root != 0
    }

    if numerator_is_monomial:
        decision = "complete_two_parameter_slice_exclusion"
    else:
        decision = "finite_residual_on_normalized_curve"

    result = {
        "experiment": "EXP-102",
        "residual_curve": "32768*s^9-(s*t-8)^7=0",
        "parametrization": {
            "s": "8*u^7",
            "t": "(8*u^9+1)/u^7",
            "domain": "u != 0",
        },
        "reference_point": {"u": "1", "s": "8", "t": "9"},
        "old_minor_determinants": [str(first_det), str(second_det)],
        "bracket_rank": bracket_rank,
        "augmented_rank": augmented_rank,
        "third_minor": {
            "row_labels": [list(label) for label in third_rows],
            "columns": [
                "rhs" if column == rhs_column else list(source.NQ[column])
                for column in third_columns
            ],
            "determinant_at_reference": str(third_det_reference),
            "combined_rank": combined_rank,
            "bivariate_polynomial": str(third_polynomial),
        },
        "curve_pullback": {
            "rational_function": str(pullback),
            "numerator": str(pullback_numerator),
            "denominator": str(pullback_denominator),
            "numerator_degree": numerator_poly.degree(),
            "numerator_terms": len(numerator_terms),
            "numerator_is_monomial": numerator_is_monomial,
            "nonzero_rational_roots": rational_roots,
        },
        "direct_curve_checks": direct_checks,
        "decision": decision,
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
