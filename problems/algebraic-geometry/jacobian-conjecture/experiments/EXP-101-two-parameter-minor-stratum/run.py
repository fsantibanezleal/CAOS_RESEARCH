"""EXP-101: exact two-parameter augmented-minor stratum."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

from sympy import Matrix, Poly, Rational, factor, groebner, symbols


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
EXP099_RUN = ROOT.parent / "EXP-099-augmented-minor-flag" / "run.py"
s, t, lam = symbols("s t lambda")


def load_exp099():
    spec = importlib.util.spec_from_file_location("exp099_matrix", EXP099_RUN)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load EXP-099 matrix reconstruction")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def reduced_determinant(
    base: Matrix, direction_s: Matrix, direction_t: Matrix
) -> tuple[object, int, Matrix, Matrix]:
    """Return det(base+s*As+t*At)/det(base) by Sylvester reduction."""
    inverse = base.inv()
    normalized_s = inverse * direction_s
    normalized_t = inverse * direction_t
    combined = normalized_s.row_join(normalized_t)
    basis_columns = combined.columnspace()
    basis = Matrix.hstack(*basis_columns)
    rank = basis.cols
    _, pivot_rows = basis.T.rref()
    row_indices = list(pivot_rows)
    require(len(row_indices) == rank, "combined column basis has an invertible row block")
    row_block = basis[row_indices, :]
    row_inverse = row_block.inv()
    coefficients_s = row_inverse * normalized_s[row_indices, :]
    coefficients_t = row_inverse * normalized_t[row_indices, :]
    require(basis * coefficients_s == normalized_s, "low-rank factorization of B_s is exact")
    require(basis * coefficients_t == normalized_t, "low-rank factorization of B_t is exact")
    reduced_s = coefficients_s * basis
    reduced_t = coefficients_t * basis
    reduced_matrix = Matrix.eye(rank) + s * reduced_s + t * reduced_t
    polynomial = factor(reduced_matrix.det(method="domain-ge"))
    return polynomial, rank, normalized_s, normalized_t


def fixed_selected_square(source, values, row_labels, columns):
    return source.selected_square(values, row_labels, columns)


def main() -> None:
    started = time.time()
    source = load_exp099()
    zero = [Rational(0)] * len(source.LOWER)
    augmented_base, base_row_labels = source.augmented_matrix(zero)

    _, row_pivots = augmented_base.T.rref()
    selected_row_indices = list(row_pivots)[:125]
    selected_row_labels = [base_row_labels[index] for index in selected_row_indices]
    row_block = augmented_base[selected_row_indices, :]
    _, column_pivots = row_block.rref()
    selected_columns = list(column_pivots)[:125]
    rhs_column = len(source.NQ)
    if rhs_column not in selected_columns:
        selected_columns = selected_columns[:124] + [rhs_column]

    base = fixed_selected_square(source, zero, selected_row_labels, selected_columns)
    base_det = base.det(method="domain-ge")
    require(base_det != 0 and rhs_column in selected_columns, "the selected base minor reconstructs")
    base_inverse = base.inv()

    def direction(point):
        values = list(zero)
        values[source.LOWER.index(point)] = Rational(1)
        return (
            fixed_selected_square(source, values, selected_row_labels, selected_columns)
            - base
        )

    forced_direction = direction((1, 0))
    forced_normalized = base_inverse * forced_direction
    print("[INFO] computing forced-axis characteristic polynomial", flush=True)
    forced_charpoly = factor(forced_normalized.charpoly(lam).as_expr())
    expected_charpoly = lam**109 * (lam - 1) ** 16
    require(
        forced_charpoly == expected_charpoly,
        "the forced-axis characteristic polynomial is lambda^109*(lambda-1)^16",
    )

    direction_s = direction((0, 1))
    direction_t = direction((1, 7))
    print("[INFO] computing combined perturbation rank and reduced determinant", flush=True)
    determinant_ratio, combined_rank, normalized_s, normalized_t = reduced_determinant(
        base, direction_s, direction_t
    )
    print(f"[INFO] combined rank r={combined_rank}", flush=True)
    if combined_rank <= 48:
        print("[PASS] combined rank is inside the predicted symbolic bound", flush=True)
    else:
        print(
            "[REFUTED] combined rank exceeds the predicted bound, but the exact "
            "reduced determinant completed inside budget",
            flush=True,
        )

    ratio_poly = Poly(determinant_ratio, s, t, domain="QQ")
    require(ratio_poly.total_degree() > 0, "the bivariate selected minor is nonconstant")

    trace_s = normalized_s.trace()
    trace_t = normalized_t.trace()
    trace_st = (normalized_s * normalized_t).trace()
    expected_st = trace_s * trace_t - trace_st
    actual_s = ratio_poly.coeff_monomial(s)
    actual_t = ratio_poly.coeff_monomial(t)
    actual_st = ratio_poly.coeff_monomial(s * t)
    require(actual_s == trace_s, "the linear s coefficient matches trace(B_s)")
    require(actual_t == trace_t, "the linear t coefficient matches trace(B_t)")
    require(actual_st == expected_st, "the mixed quadratic coefficient matches the trace identity")
    print(
        f"[INFO] traces: s={trace_s}, t={trace_t}, st-product={trace_st}; "
        f"coefficient st={actual_st}",
        flush=True,
    )
    print(
        f"[INFO] determinant ratio factorization: {determinant_ratio}",
        flush=True,
    )

    direct_checks = []
    for value_s, value_t in (
        (Rational(1), Rational(1)),
        (Rational(2), Rational(-1)),
        (Rational(1, 2), Rational(3)),
    ):
        values = list(zero)
        values[source.LOWER.index((0, 1))] = value_s
        values[source.LOWER.index((1, 7))] = value_t
        direct = fixed_selected_square(
            source, values, selected_row_labels, selected_columns
        ).det(method="domain-ge")
        predicted = base_det * ratio_poly.eval({s: value_s, t: value_t})
        require(direct == predicted, f"direct determinant agrees at ({value_s},{value_t})")
        direct_checks.append(
            {
                "s": str(value_s),
                "t": str(value_t),
                "determinant": str(direct),
            }
        )

    rational_zero = None
    for value_s in range(-12, 13):
        for value_t in range(-12, 13):
            if ratio_poly.eval({s: value_s, t: value_t}) == 0:
                rational_zero = (Rational(value_s), Rational(value_t))
                break
        if rational_zero is not None:
            break

    if rational_zero is None:
        for value_s in range(-12, 13):
            univariate = Poly(ratio_poly.as_expr().subs(s, value_s), t, domain="QQ")
            for root in univariate.ground_roots():
                if abs(root.p) <= 144 and root.q <= 144:
                    rational_zero = (Rational(value_s), Rational(root))
                    break
            if rational_zero is not None:
                break

    zero_result = {
        "found": rational_zero is not None,
        "point": None,
        "augmented_rank": None,
        "bracket_rank": None,
        "alternative_minor": None,
    }
    alternative_polynomial = None
    cover_groebner = None

    if rational_zero is not None:
        value_s, value_t = rational_zero
        zero_result["point"] = [str(value_s), str(value_t)]
        values = list(zero)
        values[source.LOWER.index((0, 1))] = value_s
        values[source.LOWER.index((1, 7))] = value_t
        augmented_at_zero, row_labels_at_zero = source.augmented_matrix(values)
        augmented_rank = augmented_at_zero.rank()
        bracket_rank = augmented_at_zero[:, :rhs_column].rank()
        zero_result["augmented_rank"] = augmented_rank
        zero_result["bracket_rank"] = bracket_rank
        print(
            f"[INFO] first rational zero ({value_s},{value_t}): "
            f"rank M={bracket_rank}, rank [M|b]={augmented_rank}",
            flush=True,
        )
        require(
            augmented_rank == 125 and bracket_rank <= 124,
            "the first-minor zero remains exactly inconsistency-certified",
        )

        _, alternative_row_pivots = augmented_at_zero.T.rref()
        alternative_row_indices = list(alternative_row_pivots)[:125]
        alternative_rows = [
            row_labels_at_zero[index] for index in alternative_row_indices
        ]
        alternative_row_block = augmented_at_zero[alternative_row_indices, :]
        _, alternative_column_pivots = alternative_row_block.rref()
        alternative_columns = list(alternative_column_pivots)[:125]
        require(
            rhs_column in alternative_columns,
            "the alternative nonzero minor includes the RHS column",
        )
        alternative_at_zero = fixed_selected_square(
            source, values, alternative_rows, alternative_columns
        )
        alternative_det_at_zero = alternative_at_zero.det(method="domain-ge")
        require(
            alternative_det_at_zero != 0,
            "an explicit alternative augmented minor is nonzero on the first stratum",
        )
        zero_result["alternative_minor"] = {
            "row_labels": [list(label) for label in alternative_rows],
            "columns": [
                "rhs" if column == rhs_column else list(source.NQ[column])
                for column in alternative_columns
            ],
            "determinant_at_point": str(alternative_det_at_zero),
        }

        # Compute the alternative polynomial around the rational zero. At the
        # reference point it is invertible, so the same low-rank identity applies.
        alternative_base = alternative_at_zero
        values_s = list(values)
        values_s[source.LOWER.index((0, 1))] += 1
        values_t = list(values)
        values_t[source.LOWER.index((1, 7))] += 1
        alternative_direction_s = (
            fixed_selected_square(source, values_s, alternative_rows, alternative_columns)
            - alternative_base
        )
        alternative_direction_t = (
            fixed_selected_square(source, values_t, alternative_rows, alternative_columns)
            - alternative_base
        )
        shifted_ratio, alternative_rank, _, _ = reduced_determinant(
            alternative_base, alternative_direction_s, alternative_direction_t
        )
        alternative_polynomial = factor(
            alternative_det_at_zero
            * shifted_ratio.subs({s: s - value_s, t: t - value_t})
        )
        alternative_poly = Poly(alternative_polynomial, s, t, domain="QQ")
        require(
            alternative_poly.eval({s: value_s, t: value_t}) == alternative_det_at_zero,
            "the alternative minor polynomial reproduces its stratum value",
        )
        zero_result["alternative_minor"]["combined_rank"] = alternative_rank
        zero_result["alternative_minor"]["polynomial"] = str(alternative_polynomial)

        cover_basis = groebner(
            [ratio_poly.as_expr(), alternative_poly.as_expr()],
            s,
            t,
            order="lex",
            domain="QQ",
        )
        cover_groebner = [str(item) for item in cover_basis]
        print(f"[INFO] two-minor Groebner basis: {cover_groebner}", flush=True)

    decision = (
        "first_explicit_minor_transition"
        if rational_zero is not None
        else "exact_stratum_polynomial_no_bounded_rational_zero"
    )
    result = {
        "experiment": "EXP-101",
        "forced_characteristic_polynomial": str(forced_charpoly),
        "forced_axis_factor": "(1+u)^16",
        "cycle_parameters": [[0, 1], [1, 7]],
        "combined_rank": combined_rank,
        "determinant_ratio": str(determinant_ratio),
        "determinant_total_degree": ratio_poly.total_degree(),
        "determinant_terms": len(ratio_poly.terms()),
        "trace_s": str(trace_s),
        "trace_t": str(trace_t),
        "trace_st": str(trace_st),
        "coefficient_st": str(actual_st),
        "direct_checks": direct_checks,
        "rational_zero_search": {
            "integer_box": [-12, 12],
            "rational_height_bound": 144,
            **zero_result,
        },
        "alternative_minor_polynomial": (
            str(alternative_polynomial) if alternative_polynomial is not None else None
        ),
        "two_minor_groebner_basis": cover_groebner,
        "decision": decision,
        "runtime_under_budget": time.time() - started < 300,
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
