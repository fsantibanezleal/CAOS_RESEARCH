"""Exact finite-algebra worker for EXP-130.

CPU only. Every persisted claim uses exact arithmetic over QQ or ZZ.
"""

from __future__ import annotations

import hashlib
import json
import time
from itertools import product
from pathlib import Path

from sympy import Matrix, Poly, QQ, factor_list, groebner, resultant, sympify, symbols


HERE = Path(__file__).resolve().parent
E123_ARTIFACT = (
    HERE.parent
    / "EXP-123-direction-29-symbolic-lift"
    / "artifacts"
    / "results.json"
)
ARTIFACT = HERE / "artifacts" / "algebra-worker.json"
CHECKPOINT = HERE / "artifacts" / "algebra-checkpoint.json"


def persist(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def cleared_primitive(poly: Poly) -> Poly:
    _, cleared = poly.clear_denoms(convert=True)
    _, primitive = cleared.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return primitive


def leading_monomials(basis) -> list[tuple[int, ...]]:
    return [tuple(poly.monoms()[0]) for poly in basis.polys]


def standard_monomials(basis) -> list[tuple[int, ...]]:
    leading = leading_monomials(basis)
    variable_count = len(basis.gens)
    bounds: list[int] = []
    for index in range(variable_count):
        pure = [
            monomial[index]
            for monomial in leading
            if monomial[index] > 0
            and all(
                exponent == 0
                for other, exponent in enumerate(monomial)
                if other != index
            )
        ]
        require(bool(pure), f"leading ideal contains a pure power in variable {index}")
        bounds.append(min(pure))
    result = []
    for monomial in product(*(range(bound) for bound in bounds)):
        if not any(
            all(monomial[index] >= lead[index] for index in range(variable_count))
            for lead in leading
        ):
            result.append(tuple(monomial))
    return result


def monomial_expression(exponents: tuple[int, ...], variables) -> object:
    expression = 1
    for variable, exponent in zip(variables, exponents, strict=True):
        expression *= variable**exponent
    return expression


def normal_vector(expression, basis, standard) -> list[object]:
    variables = basis.gens
    _, remainder = basis.reduce(expression)
    polynomial = Poly(remainder, *variables, domain=QQ)
    coefficients = polynomial.as_dict()
    return [coefficients.get(monomial, QQ.zero) for monomial in standard]


def multiplication_matrix(variable, basis, standard) -> Matrix:
    columns = []
    for monomial in standard:
        expression = variable * monomial_expression(monomial, basis.gens)
        columns.append(normal_vector(expression, basis, standard))
    return Matrix.hstack(*(Matrix(column) for column in columns))


def factor_record(expression, variable) -> list[dict[str, object]]:
    coefficient, factors = factor_list(expression, variable)
    return [
        {
            "factor": str(factor),
            "degree": int(Poly(factor, variable).degree()),
            "multiplicity": int(multiplicity),
        }
        for factor, multiplicity in factors
    ], str(coefficient)


def main() -> None:
    started = time.time()
    source = json.loads(E123_ARTIFACT.read_text(encoding="utf-8"))
    x, b, t, lam = symbols("X B T lambda")
    locals_map = {"X": x, "B": b}
    r = Poly(
        sympify(source["invariant_reduction"]["R_X_B"], locals=locals_map),
        x,
        b,
        domain=QQ,
    )
    s = Poly(
        sympify(source["invariant_reduction"]["S_X_B"], locals=locals_map),
        x,
        b,
        domain=QQ,
    )
    r_zz = cleared_primitive(r)
    s_zz = cleared_primitive(s)
    payload: dict[str, object] = {
        "experiment": "EXP-130",
        "R": str(r.as_expr()),
        "S": str(s.as_expr()),
        "R_primitive_ZZ": str(r_zz.as_expr()),
        "S_primitive_ZZ": str(s_zz.as_expr()),
        "R_degree_X": int(r.degree(x)),
        "S_degree_X": int(s.degree(x)),
        "R_degree_B": int(r.degree(b)),
        "S_degree_B": int(s.degree(b)),
    }
    persist(payload, CHECKPOINT)
    print("[INFO] loaded and cleared R,S", flush=True)

    res_x = Poly(resultant(r.as_expr(), s.as_expr(), x), b, domain=QQ)
    res_b = Poly(resultant(r.as_expr(), s.as_expr(), b), x, domain=QQ)
    require(not res_x.is_zero and not res_b.is_zero, "both projection resultants are nonzero")
    res_x_monic = res_x.monic()
    res_b_monic = res_b.monic()
    factors_b, scale_b = factor_record(res_x_monic.as_expr(), b)
    factors_x, scale_x = factor_record(res_b_monic.as_expr(), x)
    payload["projection_resultants"] = {
        "eliminate_X": str(res_x_monic.as_expr()),
        "eliminate_X_degree_B": int(res_x_monic.degree()),
        "eliminate_X_factors": factors_b,
        "eliminate_X_factor_scale": scale_b,
        "eliminate_B": str(res_b_monic.as_expr()),
        "eliminate_B_degree_X": int(res_b_monic.degree()),
        "eliminate_B_factors": factors_x,
        "eliminate_B_factor_scale": scale_x,
    }
    persist(payload, CHECKPOINT)
    print(
        f"[INFO] resultants degrees B={res_x_monic.degree()} X={res_b_monic.degree()}",
        flush=True,
    )

    original_xb = groebner([r.as_expr(), s.as_expr()], x, b, order="lex", domain=QQ)
    original_bx = groebner([r.as_expr(), s.as_expr()], b, x, order="lex", domain=QQ)
    require(original_xb.is_zero_dimensional, "original base-locus ideal is zero-dimensional")
    require(original_bx.is_zero_dimensional, "reverse-order base-locus ideal is zero-dimensional")
    original_standard = standard_monomials(original_xb)
    payload["original_ideal"] = {
        "groebner_X_B": [str(poly.as_expr()) for poly in original_xb.polys],
        "groebner_B_X": [str(poly.as_expr()) for poly in original_bx.polys],
        "leading_monomials_X_B": [list(item) for item in leading_monomials(original_xb)],
        "quotient_dimension": len(original_standard),
        "standard_monomials_X_B": [list(item) for item in original_standard],
    }
    persist(payload, CHECKPOINT)
    print(f"[INFO] original quotient dimension={len(original_standard)}", flush=True)

    saturation_elimination = groebner(
        [r.as_expr(), s.as_expr(), t * x - 1],
        t,
        x,
        b,
        order="lex",
        domain=QQ,
    )
    saturation_generators = [
        poly.as_expr()
        for poly in saturation_elimination.polys
        if not poly.as_expr().has(t)
    ]
    require(bool(saturation_generators), "saturation contraction has generators")
    saturated_xb = groebner(saturation_generators, x, b, order="lex", domain=QQ)
    saturated_bx = groebner(saturation_generators, b, x, order="lex", domain=QQ)
    saturated_empty = any(poly.as_expr() == 1 for poly in saturated_xb.polys)
    payload["saturation_by_X"] = {
        "elimination_generators": [str(item) for item in saturation_generators],
        "groebner_X_B": [str(poly.as_expr()) for poly in saturated_xb.polys],
        "groebner_B_X": [str(poly.as_expr()) for poly in saturated_bx.polys],
        "empty": saturated_empty,
    }
    if saturated_empty:
        payload["saturation_by_X"]["quotient_dimension"] = 0
        payload["decision"] = "principal_open_base_locus_empty"
        payload["elapsed_seconds"] = time.time() - started
        persist(payload, ARTIFACT)
        digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest().upper()
        print(f"[PASS] saturated algebra is zero; SHA256 {digest}", flush=True)
        return

    require(saturated_xb.is_zero_dimensional, "saturated base-locus ideal is zero-dimensional")
    require(saturated_bx.is_zero_dimensional, "reverse-order saturated ideal is zero-dimensional")
    saturated_standard = standard_monomials(saturated_xb)
    mx = multiplication_matrix(x, saturated_xb, saturated_standard)
    mb = multiplication_matrix(b, saturated_xb, saturated_standard)
    require(mx * mb == mb * mx, "quotient multiplication matrices commute")
    require(mx.det() != 0, "multiplication by X is invertible after saturation")
    char_x = Poly(mx.charpoly(lam).as_expr(), lam, domain=QQ).monic()
    char_b = Poly(mb.charpoly(lam).as_expr(), lam, domain=QQ).monic()
    min_x_factors, min_x_scale = factor_record(char_x.as_expr(), lam)
    min_b_factors, min_b_scale = factor_record(char_b.as_expr(), lam)
    payload["saturation_by_X"].update(
        {
            "quotient_dimension": len(saturated_standard),
            "standard_monomials_X_B": [list(item) for item in saturated_standard],
            "leading_monomials_X_B": [list(item) for item in leading_monomials(saturated_xb)],
            "multiplication_X_determinant": str(mx.det()),
            "multiplication_X_characteristic": str(char_x.as_expr()),
            "multiplication_X_characteristic_factors": min_x_factors,
            "multiplication_X_characteristic_scale": min_x_scale,
            "multiplication_B_characteristic": str(char_b.as_expr()),
            "multiplication_B_characteristic_factors": min_b_factors,
            "multiplication_B_characteristic_scale": min_b_scale,
            "multiplication_matrices_commute": True,
        }
    )

    r_x0 = Poly(r.as_expr().subs(x, 0), b, domain=QQ)
    s_x0 = Poly(s.as_expr().subs(x, 0), b, domain=QQ)
    boundary_gcd = r_x0.gcd(s_x0).monic()
    payload["X_zero_boundary"] = {
        "R_at_X_zero": str(r_x0.as_expr()),
        "S_at_X_zero": str(s_x0.as_expr()),
        "gcd_monic": str(boundary_gcd.as_expr()),
        "gcd_degree": int(boundary_gcd.degree()),
        "removed_length": len(original_standard) - len(saturated_standard),
    }

    trace_gram = Matrix(
        len(saturated_standard),
        len(saturated_standard),
        lambda row, column: (
            (mx ** (saturated_standard[row][0] + saturated_standard[column][0]))
            * (mb ** (saturated_standard[row][1] + saturated_standard[column][1]))
        ).trace(),
    )
    trace_determinant = trace_gram.det(method="domain-ge")
    payload["saturation_by_X"]["trace_form_determinant"] = str(trace_determinant)
    payload["saturation_by_X"]["reduced_over_Q"] = trace_determinant != 0
    require(trace_determinant != 0, "saturated quotient trace form is nondegenerate")

    payload["decision"] = "nonempty_reduced_principal_open_base_locus"
    payload["elapsed_seconds"] = time.time() - started
    persist(payload, ARTIFACT)
    digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest().upper()
    print(
        f"[PASS] wrote exact finite algebra dimension={len(saturated_standard)} "
        f"SHA256 {digest}",
        flush=True,
    )


if __name__ == "__main__":
    main()

