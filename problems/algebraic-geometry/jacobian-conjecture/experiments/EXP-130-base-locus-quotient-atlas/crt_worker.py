"""Factorwise subresultant and CRT worker for EXP-130.

CPU only. All conclusions use exact arithmetic over QQ.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from sympy import Matrix, Poly, QQ, factor_list, invert, resultant, subresultants, sympify, symbols


HERE = Path(__file__).resolve().parent
E123_ARTIFACT = (
    HERE.parent
    / "EXP-123-direction-29-symbolic-lift"
    / "artifacts"
    / "results.json"
)
E124_ARTIFACT = (
    HERE.parent
    / "EXP-124-rational-graph-alternative-chart"
    / "artifacts"
    / "results.json"
)
E125_ARTIFACT = (
    HERE.parent
    / "EXP-125-factor-curve-recursion"
    / "artifacts"
    / "results.json"
)
E127_ARTIFACT = (
    HERE.parent
    / "EXP-127-f7-divisor-norm"
    / "artifacts"
    / "results.json"
)
E129_ARTIFACT = (
    HERE.parent
    / "EXP-129-f7-crt-minor-atlas"
    / "artifacts"
    / "results.json"
)
ALGEBRA_CHECKPOINT = HERE / "artifacts" / "algebra-checkpoint.json"
ARTIFACT = HERE / "artifacts" / "crt-worker.json"
CHECKPOINT = HERE / "artifacts" / "crt-checkpoint.json"


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


def reduce_b(expression, modulus: Poly, b) -> Poly:
    return Poly(expression, b, domain=QQ).rem(modulus)


def reduce_x_coefficients(expression, modulus: Poly, x, b) -> Poly:
    polynomial = Poly(expression, x, b, domain=QQ)
    by_x_degree: dict[int, object] = {}
    for (x_degree, b_degree), coefficient in polynomial.terms():
        by_x_degree[x_degree] = (
            by_x_degree.get(x_degree, 0) + coefficient * b**b_degree
        )
    reduced = 0
    for x_degree, coefficient in by_x_degree.items():
        coefficient_poly = Poly(coefficient, b, domain=QQ)
        reduced += coefficient_poly.rem(modulus).as_expr() * x**x_degree
    return Poly(reduced, x, b, domain=QQ)


def substitute_x_class(expression, x_class: Poly, modulus: Poly, x, b) -> Poly:
    polynomial = Poly(expression, x, b, domain=QQ)
    result = Poly(0, b, domain=QQ)
    for (x_degree, b_degree), coefficient in polynomial.terms():
        term = Poly(coefficient * b**b_degree, b, domain=QQ)
        term *= x_class**x_degree
        result = (result + term).rem(modulus)
    return result.rem(modulus)


def section_y_coefficients(expression, x_class: Poly, modulus: Poly, x, b, y) -> dict[int, Poly]:
    polynomial = Poly(expression, x, b, y, domain=QQ)
    result: dict[int, Poly] = {}
    for (x_degree, b_degree, y_degree), coefficient in polynomial.terms():
        term = Poly(coefficient * b**b_degree, b, domain=QQ)
        term *= x_class**x_degree
        result[y_degree] = (
            result.get(y_degree, Poly(0, b, domain=QQ)) + term
        ).rem(modulus)
    return {degree: value.rem(modulus) for degree, value in result.items()}


def multiplication_matrix(element: Poly, modulus: Poly, b) -> Matrix:
    degree = int(modulus.degree())
    columns = []
    for power in range(degree):
        remainder = (element * Poly(b**power, b, domain=QQ)).rem(modulus)
        columns.append(
            Matrix([remainder.nth(index) for index in range(degree)])
        )
    return Matrix.hstack(*columns)


def main() -> None:
    started = time.time()
    e123 = json.loads(E123_ARTIFACT.read_text(encoding="utf-8"))
    e124 = json.loads(E124_ARTIFACT.read_text(encoding="utf-8"))
    e125 = json.loads(E125_ARTIFACT.read_text(encoding="utf-8"))
    e127 = json.loads(E127_ARTIFACT.read_text(encoding="utf-8"))
    e129 = json.loads(E129_ARTIFACT.read_text(encoding="utf-8"))
    checkpoint = json.loads(ALGEBRA_CHECKPOINT.read_text(encoding="utf-8"))
    x, b, y, lam = symbols("X B Y lambda")
    locals_map = {"X": x, "B": b, "Y": y}
    r = Poly(sympify(e123["invariant_reduction"]["R_X_B"], locals=locals_map), x, b, domain=QQ)
    s = Poly(sympify(e123["invariant_reduction"]["S_X_B"], locals=locals_map), x, b, domain=QQ)
    require(int(e124["invariant_Y_degree"]) == 0, "EXP-124 section is independent of Y and C")
    require(int(e124["determinant_A_valuation"]) == 90, "EXP-124 section has A-valuation 90")
    require(int(e127["invariant_Y_degree"]) == 0, "EXP-127 section is independent of Y and C")
    candidate_sections = [
        {
            "name": "EXP-124-N",
            "A_valuation": int(e124["determinant_A_valuation"]),
            "Y_degree": int(e124["invariant_Y_degree"]),
            "expression": Poly(
                sympify(e124["invariant_determinant_X_B_Y"], locals=locals_map),
                x,
                b,
                y,
                domain=QQ,
            ),
        },
        {
            "name": "EXP-125-h36",
            "A_valuation": int(e125["determinant_A_valuation"]),
            "Y_degree": int(e125["invariant_Y_degree"]),
            "expression": Poly(
                sympify(e125["invariant_determinant_X_B_Y"], locals=locals_map),
                x,
                b,
                y,
                domain=QQ,
            ),
        },
        {
            "name": "EXP-127-h7",
            "A_valuation": int(e127["determinant_A_valuation"]),
            "Y_degree": int(e127["invariant_Y_degree"]),
            "expression": Poly(
                sympify(e127["invariant_determinant_X_B_Y"], locals=locals_map),
                x,
                b,
                y,
                domain=QQ,
            ),
        },
    ]
    for record in e129["exact_atlas"]:
        candidate_sections.append(
            {
                "name": f"EXP-129-atlas-{record['atlas_index']}",
                "A_valuation": int(record["determinant_A_valuation"]),
                "Y_degree": int(record["invariant_Y_degree"]),
                "expression": Poly(
                    sympify(record["invariant_determinant_X_B_Y"], locals=locals_map),
                    x,
                    b,
                    y,
                    domain=QQ,
                ),
            }
        )
    require(len(candidate_sections) >= 5, "loaded five existing exact sections")
    require(
        all(item["Y_degree"] <= 1 for item in candidate_sections),
        "all candidate sections are affine in Y",
    )

    b_factors = {
        int(record["degree"]): Poly(sympify(record["factor"], locals={"B": b}), b, domain=QQ).monic()
        for record in checkpoint["projection_resultants"]["eliminate_X_factors"]
        if int(record["degree"]) > 1
    }
    x_factors = {
        int(record["degree"]): Poly(sympify(record["factor"], locals={"X": x}), x, domain=QQ).monic()
        for record in checkpoint["projection_resultants"]["eliminate_B_factors"]
        if int(record["degree"]) > 1
    }
    require(sorted(b_factors) == [3, 6, 12, 69], "principal-open B blocks have degrees 3, 6, 12, 69")
    require(sorted(x_factors) == [3, 6, 12, 69], "principal-open X blocks have degrees 3, 6, 12, 69")

    print("[INFO] computing the X-subresultant sequence", flush=True)
    sequence = subresultants(r.as_expr(), s.as_expr(), x)
    sequence_records = [
        {
            "degree_X": int(Poly(item, x, b, domain=QQ).degree(x)),
            "monomial_count": len(Poly(item, x, b, domain=QQ).terms()),
        }
        for item in sequence
    ]
    payload: dict[str, object] = {
        "experiment": "EXP-130",
        "subresultant_sequence": sequence_records,
        "blocks": [],
        "candidate_sections": [
            {
                "name": item["name"],
                "A_valuation": item["A_valuation"],
                "Y_degree": item["Y_degree"],
            }
            for item in candidate_sections
        ],
    }
    persist(payload, CHECKPOINT)

    for degree in sorted(b_factors):
        modulus = b_factors[degree]
        irreducible_factors = factor_list(modulus.as_expr(), b)[1]
        require(
            len(irreducible_factors) == 1 and irreducible_factors[0][1] == 1,
            f"degree-{degree} B block is irreducible and squarefree",
        )
        specialized = [
            reduce_x_coefficients(item, modulus, x, b)
            for item in sequence
        ]
        nonzero = [item for item in specialized if not item.is_zero]
        require(bool(nonzero), f"degree-{degree} subresultant chain has a nonzero class")
        gcd_class = nonzero[-1]
        require(gcd_class.degree(x) == 1, f"degree-{degree} specialized gcd is linear in X")
        u = reduce_b(gcd_class.as_expr().coeff(x, 1), modulus, b)
        v = reduce_b(gcd_class.as_expr().subs(x, 0), modulus, b)
        require(u.gcd(modulus).degree() == 0, f"degree-{degree} linear X coefficient is a unit")
        x_class = reduce_b(-v.as_expr() * invert(u.as_expr(), modulus.as_expr()), modulus, b)
        r_check = substitute_x_class(r.as_expr(), x_class, modulus, x, b)
        s_check = substitute_x_class(s.as_expr(), x_class, modulus, x, b)
        require(r_check.is_zero, f"degree-{degree} reconstructed X class annihilates R")
        require(s_check.is_zero, f"degree-{degree} reconstructed X class annihilates S")

        x_minimal = Poly(
            resultant(modulus.as_expr(), lam - x_class.as_expr(), b),
            lam,
            domain=QQ,
        ).monic()
        expected_x = Poly(x_factors[degree].as_expr().subs(x, lam), lam, domain=QQ).monic()
        require(x_minimal == expected_x, f"degree-{degree} B and X projections describe the same points")

        section_tests = []
        for candidate in candidate_sections:
            coefficients = section_y_coefficients(
                candidate["expression"].as_expr(), x_class, modulus, x, b, y
            )
            constant_class = coefficients.get(0, Poly(0, b, domain=QQ))
            linear_class = coefficients.get(1, Poly(0, b, domain=QQ))
            require(
                all(key in (0, 1) for key in coefficients),
                f"degree-{degree} {candidate['name']} remains affine in Y",
            )
            constant_polynomial_unit = (
                linear_class.is_zero and constant_class.gcd(modulus).degree() == 0
            )
            section_tests.append(
                {
                    "name": candidate["name"],
                    "constant_class": str(constant_class.as_expr()),
                    "linear_class": str(linear_class.as_expr()),
                    "constant_polynomial_unit": constant_polynomial_unit,
                }
            )
        pair_tests = []
        pair_unit_found = False
        for left_index, left in enumerate(section_tests):
            for right in section_tests[left_index + 1 :]:
                left_constant = Poly(left["constant_class"], b, domain=QQ)
                left_linear = Poly(left["linear_class"], b, domain=QQ)
                right_constant = Poly(right["constant_class"], b, domain=QQ)
                right_linear = Poly(right["linear_class"], b, domain=QQ)
                y_resultant = (
                    left_linear * right_constant
                    - right_linear * left_constant
                ).rem(modulus)
                y_resultant_gcd = y_resultant.gcd(modulus).monic()
                is_unit = y_resultant_gcd.degree() == 0
                norm_matrix = None
                inverse_record = None
                if is_unit:
                    norm_matrix = multiplication_matrix(
                        y_resultant, modulus, b
                    ).det(method="domain-ge")
                    norm_resultant = resultant(
                        modulus.as_expr(), y_resultant.as_expr(), b
                    )
                    require(
                        norm_matrix == norm_resultant,
                        f"degree-{degree} {left['name']}/{right['name']} Y-resultant norm agrees",
                    )
                    require(
                        norm_matrix != 0,
                        f"degree-{degree} {left['name']}/{right['name']} Y-resultant norm is nonzero",
                    )
                    inverse = reduce_b(
                        invert(y_resultant.as_expr(), modulus.as_expr()), modulus, b
                    )
                    require(
                        (y_resultant * inverse).rem(modulus)
                        == Poly(1, b, domain=QQ),
                        f"degree-{degree} {left['name']}/{right['name']} Y-resultant inverse verifies",
                    )
                    inverse_record = str(inverse.as_expr())
                pair_tests.append(
                    {
                        "left": left["name"],
                        "right": right["name"],
                        "Y_resultant": str(y_resultant.as_expr()),
                        "is_unit": is_unit,
                        "inverse": inverse_record,
                        "norm": str(norm_matrix) if norm_matrix is not None else None,
                    }
                )
                if is_unit:
                    pair_unit_found = True
                    break
            if pair_unit_found:
                break
        constant_cover = next(
            (
                {"type": "constant", "section": item["name"]}
                for item in section_tests
                if item["constant_polynomial_unit"]
            ),
            None,
        )
        pair_cover = next(
            (
                {
                    "type": "affine-pair",
                    "sections": [item["left"], item["right"]],
                }
                for item in pair_tests
                if item["is_unit"]
            ),
            None,
        )
        cover_certificate = constant_cover or pair_cover
        covered = cover_certificate is not None
        block = {
            "degree": degree,
            "B_factor": str(modulus.as_expr()),
            "X_factor": str(x_factors[degree].as_expr()),
            "specialized_gcd": str(gcd_class.as_expr()),
            "X_class_mod_B_factor": str(x_class.as_expr()),
            "section_tests": section_tests,
            "pair_tests": pair_tests,
            "cover_certificate": cover_certificate,
            "same_point_projection_check": True,
            "covered": covered,
        }
        payload["blocks"].append(block)
        persist(payload, CHECKPOINT)
        print(f"[INFO] completed exact degree-{degree} CRT block", flush=True)

    r_x0 = Poly(r.as_expr().subs(x, 0), b, domain=QQ)
    s_x0 = Poly(s.as_expr().subs(x, 0), b, domain=QQ)
    r_b0 = Poly(r.as_expr().subs(b, 0), x, domain=QQ)
    s_b0 = Poly(s.as_expr().subs(b, 0), x, domain=QQ)
    gcd_x0 = r_x0.gcd(s_x0).monic()
    gcd_b0 = r_b0.gcd(s_b0).monic()
    require(gcd_x0.as_expr() == b**12, "X=0 common support is only B=0")
    require(gcd_b0.as_expr() == x**3, "B=0 common support is only X=0")
    payload["coordinate_boundary"] = {
        "gcd_R0B_S0B": str(gcd_x0.as_expr()),
        "gcd_RX0_SX0": str(gcd_b0.as_expr()),
        "projection_multiplicity_B": 27,
        "projection_multiplicity_X": 27,
        "support": "X=B=0",
        "classification": "A=0 boundary",
    }
    blocks_without_existing_unit = {
        block["degree"] for block in payload["blocks"] if not block["covered"]
    }
    all_blocks_covered = len(blocks_without_existing_unit) == 0
    block_certificates = {
        str(block["degree"]): block["cover_certificate"]
        for block in payload["blocks"]
    }
    payload["principal_open_algebra"] = {
        "dimension": sum(b_factors),
        "block_degrees": sorted(b_factors),
        "reduced": True,
        "all_blocks_covered": all_blocks_covered,
        "uncovered_degrees": sorted(blocks_without_existing_unit),
        "blocks_without_any_existing_unit": sorted(blocks_without_existing_unit),
        "block_cover_certificates_in_KY": block_certificates,
    }
    payload["decision"] = (
        "existing_exact_atlas_closes_principal_open_base_locus"
        if all_blocks_covered
        else "new_row_selection_required_on_uncovered_blocks"
    )
    payload["elapsed_seconds"] = time.time() - started
    persist(payload, ARTIFACT)
    digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest().upper()
    print(f"[PASS] CRT worker SHA256 {digest}", flush=True)


if __name__ == "__main__":
    main()
