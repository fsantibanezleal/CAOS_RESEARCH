"""EXP-126: exact divisor and function-field norm on the F6 graph curve."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import (
    Matrix,
    Poly,
    QQ,
    discriminant,
    expand,
    factor_list,
    fraction,
    gcd,
    invert,
    resultant,
    sympify,
    symbols,
    together,
)


HERE = Path(__file__).resolve().parent
E125_DIR = HERE.parent / "EXP-125-factor-curve-recursion"
E125_PATH = E125_DIR / "run.py"
E125_ARTIFACT = E125_DIR / "artifacts" / "results.json"
E125_CHECKPOINT = E125_DIR / "artifacts" / "checkpoint.json"
E125_WORKER_ARTIFACT = E125_DIR / "artifacts" / "symbolic-worker.json"
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
EXPECTED_E125_SHA256 = (
    "2470AB06210C5E8CDE09FB3F1FFA227520D6C810FBF70A8E0713BBCDC240D803"
)
EXPECTED_WORKER_SHA256 = (
    "5133E1600F4AA484B91B96C8FBD85DF1A5BCC70670B12050F8303BA5EABA2375"
)
ANCHOR_SCC_BUDGET_SECONDS = 60
QUOTIENT_BUDGET_SECONDS = 90
TOTAL_GATE_SECONDS = 480

spec = importlib.util.spec_from_file_location("exp125", E125_PATH)
exp125 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp125)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def persist(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def factorization(expression, variable):
    coefficient, factors = factor_list(expression, variable)
    return {
        "coefficient": str(coefficient),
        "factors": [
            {
                "factor": str(factor),
                "degree": int(Poly(factor, variable, domain=QQ).degree()),
                "multiplicity": multiplicity,
            }
            for factor, multiplicity in factors
        ],
    }


def monic_gcd(left, right, variable):
    left_poly = Poly(left, variable, domain=QQ)
    right_poly = Poly(right, variable, domain=QQ)
    return gcd(left_poly, right_poly).monic()


def reduce_mod_b(expression, modulus, b):
    return Poly(expand(expression), b, domain=QQ).rem(modulus).as_expr()


def classify_norm_factors(
    norm_factors,
    u,
    v,
    f6,
    r,
    s,
    x,
    b,
    same_point_s,
    same_point_r,
    same_point_x_zero,
    f6_discriminant,
):
    """Classify norm factors on the geometric F6 section zero set."""
    u_poly = Poly(u, b, domain=QQ)
    diagnostic_polys = {
        "S": Poly(same_point_s, b, domain=QQ),
        "R": Poly(same_point_r, b, domain=QQ),
        "X_zero": Poly(same_point_x_zero, b, domain=QQ),
        "discriminant": Poly(f6_discriminant, b, domain=QQ),
    }
    f6_x = Poly(f6, x, domain=QQ.frac_field(b))
    leading = f6_x.LC()
    linear = f6_x.nth(1)
    records = []
    effective_degree = 0
    for factor, multiplicity in norm_factors:
        modulus = Poly(factor, b, domain=QQ)
        degree = int(modulus.degree())
        u_vanishes = gcd(u_poly, modulus).degree() > 0
        flags = {
            name: gcd(polynomial, modulus).degree() > 0
            for name, polynomial in diagnostic_polys.items()
        }
        resultant_flags = dict(flags)
        direct_point = None
        if degree <= 6:
            if not u_vanishes:
                inverse_u = invert(u_poly, modulus).as_expr()
                x_class = reduce_mod_b(-v * inverse_u, modulus, b)
                mode = "unique_linear_section_root"
            else:
                require(
                    reduce_mod_b(v, modulus, b) == 0,
                    f"degree-{degree} vertical factor also divides V",
                )
                require(
                    flags["discriminant"],
                    f"degree-{degree} vertical factor is a double F6 fiber",
                )
                x_class = reduce_mod_b(-linear / (2 * leading), modulus, b)
                mode = "double_F6_root_with_zero_section"
            f6_value = reduce_mod_b(f6.subs(x, x_class), modulus, b)
            f6_derivative = reduce_mod_b(f6.diff(x).subs(x, x_class), modulus, b)
            r_value = reduce_mod_b(r.subs(x, x_class), modulus, b)
            s_value = reduce_mod_b(s.subs(x, x_class), modulus, b)
            require(f6_value == 0, f"degree-{degree} classified point lies on F6")
            exact_flags = {
                "S": s_value == 0,
                "R": r_value == 0,
                "X_zero": x_class == 0,
            }
            if not u_vanishes:
                for name, value in exact_flags.items():
                    require(
                        value == flags[name],
                        f"degree-{degree} direct {name} classification matches resultant",
                    )
            else:
                # When U=V=0 modulo the factor, h vanishes on the whole
                # fiber and its resultants with R, S, or X vanish
                # automatically. The double-root evaluation supplies the
                # geometric same-point classification.
                flags.update(exact_flags)
                print(
                    f"[PASS] degree-{degree} double-root evaluation "
                    "resolves vertical-section resultants",
                    flush=True,
                )
            direct_point = {
                "mode": mode,
                "X_class_mod_factor": str(x_class),
                "F6_value": str(f6_value),
                "F6_X_derivative": str(f6_derivative),
                "R_value": str(r_value),
                "S_value": str(s_value),
            }
        retained = not flags["S"] and not flags["X_zero"]
        if retained:
            effective_degree += degree
        records.append(
            {
                "factor": str(factor),
                "degree": degree,
                "norm_multiplicity": multiplicity,
                "U_vanishes_mod_factor": u_vanishes,
                "projection_resultant_S_zero": resultant_flags["S"],
                "projection_resultant_R_zero": resultant_flags["R"],
                "projection_resultant_X_zero": resultant_flags["X_zero"],
                "same_point_S_zero": flags["S"],
                "same_point_R_zero": flags["R"],
                "same_point_X_zero": flags["X_zero"],
                "F6_projection_ramified": flags["discriminant"],
                "direct_point_classification": direct_point,
                "retained_on_A_S_nonzero": retained,
            }
        )
    return records, effective_degree


def verify_modular_samples(base, directions, f6, r, s, x, b, rows, e125):
    records = []
    for prime in exp125.PRIMES:
        matrices = exp125.modular_matrices(base, directions, prime)
        samples = e125["modular_reconnaissance"][f"F6_p{prime}"]["points"]
        require(len(samples) == 4, f"reloaded four accepted F6 samples at p={prime}")
        for sample in samples:
            av = int(sample["A"])
            bv = int(sample["B"])
            cv = int(sample["C"])
            xv = int(sample["X"])
            yv = int(sample["Y"])
            require(
                exp125.polynomial_terms_value(
                    exp125.polynomial_terms_mod(f6, x, b, prime),
                    xv,
                    bv,
                    prime,
                )
                == 0,
                f"p={prime} sample lies on F6",
            )
            rv = exp125.polynomial_terms_value(
                exp125.polynomial_terms_mod(r, x, b, prime),
                xv,
                bv,
                prime,
            )
            sv = exp125.polynomial_terms_value(
                exp125.polynomial_terms_mod(s, x, b, prime),
                xv,
                bv,
                prime,
            )
            require(sv != 0, f"p={prime} sample lies on S nonzero")
            require((rv + yv * sv) % prime == 0, f"p={prime} sample lies on graph")
            evaluated = exp125.exp124.combine_mod(
                matrices["base"],
                matrices["A"],
                matrices["B"],
                matrices["C"],
                av,
                bv,
                cv,
                prime,
            )
            coefficient_rank = len(
                exp125.independent_row_basis_fast(
                    [row[:124] for row in evaluated], prime
                )
            )
            augmented_rank = len(exp125.independent_row_basis_fast(evaluated, prime))
            require(
                (coefficient_rank, augmented_rank) == (124, 125),
                f"p={prime} reproduced F6 rank profile 124/125",
            )
            require(
                exp125.determinant_mod_fast(evaluated, rows, prime) != 0,
                f"p={prime} selected F6 minor is nonzero",
            )
            records.append(
                {
                    "prime": prime,
                    "point": [av, bv, cv],
                    "rank_profile": "124/125",
                }
            )
    return records


def main() -> None:
    started = time.time()
    x, b, y, r, s, factors, _, _ = exp125.load_polynomials()
    a, c = symbols("A C")
    f6 = factors["F6"]
    e125 = json.loads(E125_ARTIFACT.read_text(encoding="utf-8"))
    e125_checkpoint = json.loads(E125_CHECKPOINT.read_text(encoding="utf-8"))

    require(sha256(E125_ARTIFACT) == EXPECTED_E125_SHA256, "EXP-125 result hash")
    require(
        sha256(E125_WORKER_ARTIFACT) == EXPECTED_WORKER_SHA256,
        "EXP-125 worker hash",
    )
    f3_rows = list(e125["selected_rows"]["F3"])
    f6_rows = list(e125["selected_rows"]["F6"])
    require(f6_rows == f3_rows, "persisted F6 and exact F3 row bases are identical")
    require(
        f6_rows != list(e125["selected_rows"]["F7"]),
        "persisted F6 and F7 row bases are distinct",
    )
    f6_factorization = factor_list(f6, x, b)
    require(
        len(f6_factorization[1]) == 1
        and f6_factorization[1][0][1] == 1
        and Poly(f6_factorization[1][0][0], x, b, domain=QQ).total_degree() == 6,
        "F6 is irreducible over QQ[X,B]",
    )

    base, directions = exp125.exp124.build_full_system()
    anchor_started = time.time()
    (
        selected_base,
        selected_directions,
        _,
        anchor_det,
        _,
        components,
        anchor_point,
        anchor_attempts,
    ) = exp125.exp124.exact_candidate_profile(base, directions, f6_rows)
    anchor_elapsed = time.time() - anchor_started
    component_sizes = [len(component) for component in components]
    require(
        anchor_elapsed <= ANCHOR_SCC_BUDGET_SECONDS,
        "anchor and SCC computation remains within budget",
    )
    require(max(component_sizes) <= 60, "largest exact cyclic block is at most 60")
    require(
        list(anchor_point) == e125_checkpoint["F3_anchor"]["point"],
        "reproduced accepted exact anchor",
    )
    require(
        component_sizes == e125_checkpoint["F3_cyclic_component_sizes"],
        "reproduced accepted SCC profile",
    )
    checkpoint = {
        "experiment": "EXP-126",
        "selected_rows": f6_rows,
        "basis_identity": "EXP-125 F6 rows equal EXP-125 F3 rows",
        "anchor": {
            "point": list(anchor_point),
            "determinant": str(anchor_det),
            "attempts": anchor_attempts,
        },
        "cyclic_component_sizes": component_sizes,
        "source_hashes": {
            "EXP-125_results": EXPECTED_E125_SHA256,
            "EXP-125_symbolic_worker": EXPECTED_WORKER_SHA256,
        },
    }
    persist(checkpoint, CHECKPOINT)

    expression = sympify(
        e125["symbolic_worker"]["determinant_ratio"],
        locals={"A": a, "B": b, "C": c},
    )
    valuation, invariant = exp125.exp124.invariant_reduce(
        expression, a, b, c, x, y
    )
    invariant_poly = Poly(invariant, y, domain="QQ[X,B]")
    y_degree = int(invariant_poly.degree())
    graph_numerator = expand(
        sum(
            invariant_poly.nth(power)
            * (-r) ** power
            * s ** (y_degree - power)
            for power in range(y_degree + 1)
        )
    )
    require(
        expand(
            graph_numerator
            - sympify(e125["graph_numerator"], locals={"X": x, "B": b})
        )
        == 0,
        "reproduced accepted exact graph numerator",
    )

    direct_controls = []
    for av, bv, cv in ((1, 0, 0), (1, 0, 1), (2, 1, 1), (-1, 1, 1)):
        direct = (
            selected_base
            + av * selected_directions[(0, 1)]
            + bv * selected_directions[(0, 5)]
            + cv * selected_directions[exp125.exp124.TARGET]
        ).det(method="domain-ge") / anchor_det
        predicted = expression.subs({a: av, b: bv, c: cv})
        require(direct == predicted, f"direct determinant control ({av},{bv},{cv})")
        direct_controls.append({"point": [av, bv, cv], "ratio": str(direct)})

    modular_controls = verify_modular_samples(
        base, directions, f6, r, s, x, b, f6_rows, e125
    )

    quotient_started = time.time()
    coefficient_field = QQ.frac_field(b)
    graph_poly = Poly(graph_numerator, x, domain=coefficient_field)
    f6_poly = Poly(f6, x, domain=coefficient_field)
    quotient, raw_remainder = graph_poly.div(f6_poly)
    require(
        graph_poly == quotient * f6_poly + raw_remainder,
        "reconstructed graph numerator from F6 quotient and remainder",
    )
    require(not raw_remainder.is_zero, "graph section is nonzero in QQ(B)[X]/(F6)")
    require(raw_remainder.degree() <= 1, "F6 quotient remainder has X-degree at most one")

    remainder_numerator, remainder_denominator = fraction(
        together(raw_remainder.as_expr())
    )
    require(
        not remainder_denominator.has(x),
        "quotient remainder denominator is independent of X",
    )
    remainder_qq = Poly(remainder_numerator, x, b, domain=QQ)
    denominator_lcm, remainder_integer = remainder_qq.clear_denoms(convert=True)
    remainder_content, remainder_primitive = remainder_integer.primitive()
    if remainder_primitive.LC() < 0:
        remainder_primitive = -remainder_primitive
        remainder_content = -remainder_content
    h = remainder_primitive.as_expr()
    h_poly_x = Poly(h, x, domain=QQ.frac_field(b))
    u = expand(h_poly_x.nth(1))
    v = expand(h_poly_x.nth(0))
    require(u != 0, "primitive F6 section is genuinely linear in X")

    norm_resultant = expand(resultant(f6, h, x))
    require(norm_resultant != 0, "Sylvester resultant norm is nonzero")
    f6_x = Poly(f6, x, domain=QQ.frac_field(b))
    leading = expand(f6_x.LC())
    a1 = expand(f6_x.nth(1))
    a0 = expand(f6_x.nth(0))
    multiplication_matrix = Matrix(
        [
            [v, -u * a0 / leading],
            [u, v - u * a1 / leading],
        ]
    )
    norm_multiplication = expand(multiplication_matrix.det())
    require(
        expand(norm_resultant - leading * norm_multiplication) == 0,
        "resultant and quadratic multiplication norms agree",
    )
    norm_poly = Poly(norm_resultant, b, domain=QQ).monic()
    require(norm_poly.degree() > 0, "F6 norm is nonconstant")
    norm_factor_coefficient, norm_factors = factor_list(norm_poly.as_expr(), b)

    same_point_s = expand(resultant(h, s, x))
    same_point_r = expand(resultant(h, r, x))
    same_point_x_zero = expand(resultant(h, x, x))
    f6_discriminant = expand(discriminant(f6, x))
    diagnostic_polynomials = {
        "section_with_S": same_point_s,
        "section_with_R": same_point_r,
        "section_with_X_zero": same_point_x_zero,
        "F6_projection_discriminant": f6_discriminant,
        "coefficient_U": u,
    }
    diagnostics = {}
    for name, polynomial in diagnostic_polynomials.items():
        polynomial_b = Poly(polynomial, b, domain=QQ)
        common = monic_gcd(norm_poly.as_expr(), polynomial_b.as_expr(), b)
        diagnostics[name] = {
            "polynomial": str(polynomial_b.as_expr()),
            "degree": int(polynomial_b.degree()),
            "gcd_with_norm": str(common.as_expr()),
            "gcd_degree": int(common.degree()),
        }
    factor_roles, effective_degree = classify_norm_factors(
        norm_factors,
        u,
        v,
        f6,
        r,
        s,
        x,
        b,
        same_point_s,
        same_point_r,
        same_point_x_zero,
        f6_discriminant,
    )
    require(
        [record["degree"] for record in factor_roles if record["retained_on_A_S_nonzero"]]
        == [18, 30],
        "only the degree-18 and degree-30 norm factors survive on AS nonzero",
    )
    require(effective_degree == 48, "effective F6 principal-open residual has degree 48")

    quotient_elapsed = time.time() - quotient_started
    require(
        quotient_elapsed <= QUOTIENT_BUDGET_SECONDS,
        "quotient and norm arithmetic remains within budget",
    )
    elapsed = time.time() - started
    require(elapsed <= TOTAL_GATE_SECONDS, "EXP-126 remains within total compute gate")

    payload = {
        "experiment": "EXP-126",
        "source_artifact_hashes": checkpoint["source_hashes"],
        "selected_rows": f6_rows,
        "basis_identity_with_EXP125_F3": True,
        "anchor": checkpoint["anchor"],
        "cyclic_component_sizes": component_sizes,
        "determinant_A_valuation": valuation,
        "invariant_Y_degree": y_degree,
        "reproduced_graph_numerator": str(graph_numerator),
        "F6": str(f6),
        "F6_irreducible_over_QQ_X_B": True,
        "quotient_remainder_raw": str(raw_remainder.as_expr()),
        "quotient_remainder_denominator": str(remainder_denominator),
        "quotient_remainder_denominator_lcm": str(denominator_lcm),
        "quotient_remainder_content": str(remainder_content),
        "quotient_remainder_primitive": str(h),
        "quotient_U_B": str(u),
        "quotient_V_B": str(v),
        "norm_resultant_monic": str(norm_poly.as_expr()),
        "norm_degree": int(norm_poly.degree()),
        "norm_factorization": {
            **factorization(norm_poly.as_expr(), b),
            "monic_factor_coefficient": str(norm_factor_coefficient),
        },
        "norm_multiplication_matrix": [
            [str(value) for value in row]
            for row in multiplication_matrix.tolist()
        ],
        "norm_multiplication": str(norm_multiplication),
        "norm_resultant_scale_from_multiplication": str(leading),
        "projection_diagnostics": diagnostics,
        "norm_factor_roles": factor_roles,
        "effective_A_S_nonzero_residual_degree": effective_degree,
        "effective_normalized_B_values_over_algebraic_closure": effective_degree,
        "effective_lifted_A_B_C_points_over_algebraic_closure": 3
        * effective_degree,
        "direct_exact_controls": direct_controls,
        "modular_sample_controls": modular_controls,
        "predictions": {
            "p1_anchor_and_scc_at_most_60": True,
            "p2_four_direct_exact_controls": True,
            "p3_nonzero_F6_quotient_class": True,
            "p4_nonzero_nonconstant_norm": True,
            "p5_two_norm_routes_agree": True,
        },
        "scope": (
            "Exact dense-open cover of only the F6 component on the AS!=0 "
            "EXP-123 graph, leaving the finite divisor projected into the "
            "norm roots. Those roots, F7, the F3 finite residual, V(R,S), "
            "A=0, the full four-parameter restriction, (72,108), the "
            "degree floor, and JC(2) remain open."
        ),
    }
    persist(payload, ARTIFACT)
    digest = sha256(ARTIFACT)
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(
        f"[INFO] F6 norm degree={norm_poly.degree()}, "
        f"effective_degree={effective_degree}, factors={len(norm_factors)}, "
        f"elapsed={elapsed:.2f} s",
        flush=True,
    )
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    main()
