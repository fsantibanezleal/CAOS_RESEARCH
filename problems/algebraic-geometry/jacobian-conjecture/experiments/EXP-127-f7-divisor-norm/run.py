"""EXP-127: exact divisor and function-field norm on the F7 graph curve."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
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
WORKER = HERE / "symbolic_worker.py"
WORKER_ARTIFACT = HERE / "artifacts" / "symbolic-worker.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
ARTIFACT = HERE / "artifacts" / "results.json"
EXPECTED_E125_SHA256 = (
    "2470AB06210C5E8CDE09FB3F1FFA227520D6C810FBF70A8E0713BBCDC240D803"
)
EXPECTED_WORKER_SHA256 = (
    "8711AD526482CD16316719A4F60783378748157460F56BCA41689726A891571A"
)
ANCHOR_SCC_BUDGET_SECONDS = 60
WORKER_TIMEOUT_SECONDS = 360
QUOTIENT_BUDGET_SECONDS = 120
TOTAL_GATE_SECONDS = 540

spec = importlib.util.spec_from_file_location("exp125_f7", E125_PATH)
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
                "multiplicity": int(multiplicity),
            }
            for factor, multiplicity in factors
        ],
    }


def reduce_mod_b(expression, modulus, b):
    return Poly(expand(expression), b, domain=QQ).rem(modulus).as_expr()


def verify_modular_samples(base, directions, f7, r, s, x, b, rows, accepted):
    records = []
    for prime in exp125.PRIMES:
        matrices = exp125.modular_matrices(base, directions, prime)
        source = accepted["modular_reconnaissance"][f"F7_p{prime}"]
        require(
            len(source["points"]) == exp125.SAMPLES_PER_FACTOR,
            f"reloaded four accepted F7 samples at p={prime}",
        )
        factor_terms = exp125.polynomial_terms_mod(f7, x, b, prime)
        r_terms = exp125.polynomial_terms_mod(r, x, b, prime)
        s_terms = exp125.polynomial_terms_mod(s, x, b, prime)
        for point in source["points"]:
            av = int(point["A"])
            bv = int(point["B"])
            cv = int(point["C"])
            xv = int(point["X"])
            yv = int(point["Y"])
            require(
                exp125.polynomial_terms_value(factor_terms, xv, bv, prime) == 0,
                f"p={prime} sample lies on F7",
            )
            rv = exp125.polynomial_terms_value(r_terms, xv, bv, prime)
            sv = exp125.polynomial_terms_value(s_terms, xv, bv, prime)
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
            require(
                exp125.determinant_mod_fast(evaluated, rows, prime) != 0,
                f"p={prime} selected F7 minor is nonzero",
            )
            records.append(
                {
                    "prime": prime,
                    "point": [av, bv, cv],
                    "rank_profile": point["rank_profile"],
                }
            )
    return records


def classify_norm_factors(norm_factors, u, v, f7, r, s, x, b):
    """Use quotient arithmetic where the linear section has a unique root."""
    f7_x = Poly(f7, x, domain=QQ.frac_field(b))
    leading = expand(f7_x.LC())
    a1 = expand(f7_x.nth(1))
    records = []
    retained_degree = 0
    for factor, multiplicity in norm_factors:
        modulus = Poly(factor, b, domain=QQ)
        degree = int(modulus.degree())
        leading_vanishes = gcd(
            modulus, Poly(leading, b, domain=QQ)
        ).degree() > 0
        u_vanishes = gcd(modulus, Poly(u, b, domain=QQ)).degree() > 0
        v_vanishes = gcd(modulus, Poly(v, b, domain=QQ)).degree() > 0
        direct = None
        removed_boundary = False
        if not u_vanishes:
            x_class = reduce_mod_b(
                -v * invert(Poly(u, b, domain=QQ), modulus).as_expr(),
                modulus,
                b,
            )
            f_value = reduce_mod_b(f7.subs(x, x_class), modulus, b)
            r_value = reduce_mod_b(r.subs(x, x_class), modulus, b)
            s_value = reduce_mod_b(s.subs(x, x_class), modulus, b)
            require(f_value == 0, f"degree-{degree} section root lies on F7")
            direct = {
                "mode": "unique_linear_section_root",
                "X_class_mod_factor": str(x_class),
                "R_value": str(r_value),
                "S_value": str(s_value),
                "X_zero": x_class == 0,
                "R_zero": r_value == 0,
                "S_zero": s_value == 0,
            }
            removed_boundary = s_value == 0 or x_class == 0
        elif not leading_vanishes and u_vanishes and v_vanishes:
            f7_disc = Poly(discriminant(f7, x), b, domain=QQ)
            if gcd(modulus, f7_disc).degree() > 0:
                x_class = reduce_mod_b(
                    -a1
                    * invert(Poly(2 * leading, b, domain=QQ), modulus).as_expr(),
                    modulus,
                    b,
                )
                f_value = reduce_mod_b(f7.subs(x, x_class), modulus, b)
                require(
                    f_value == 0,
                    f"degree-{degree} vertical section has the double F7 root",
                )
                r_value = reduce_mod_b(r.subs(x, x_class), modulus, b)
                s_value = reduce_mod_b(s.subs(x, x_class), modulus, b)
                direct = {
                    "mode": "double_F7_root_with_zero_section",
                    "X_class_mod_factor": str(x_class),
                    "R_value": str(r_value),
                    "S_value": str(s_value),
                    "X_zero": x_class == 0,
                    "R_zero": r_value == 0,
                    "S_zero": s_value == 0,
                }
                removed_boundary = s_value == 0 or x_class == 0
        retained = bool(not removed_boundary)
        if retained:
            retained_degree += degree * int(multiplicity)
        records.append(
            {
                "factor": str(factor),
                "degree": degree,
                "multiplicity": int(multiplicity),
                "leading_coefficient_vanishes": leading_vanishes,
                "U_vanishes": u_vanishes,
                "V_vanishes": v_vanishes,
                "direct_same_point_classification": direct,
                "removed_as_A_or_S_boundary": removed_boundary,
                "retained_conservatively_on_A_S_nonzero": retained,
            }
        )
    return records, retained_degree


def main() -> None:
    started = time.time()
    x, b, y, r, s, factors, _, _ = exp125.load_polynomials()
    a, c = symbols("A C")
    f7 = factors["F7"]
    accepted = json.loads(E125_ARTIFACT.read_text(encoding="utf-8"))
    require(sha256(E125_ARTIFACT) == EXPECTED_E125_SHA256, "EXP-125 result hash")
    rows = list(accepted["selected_rows"]["F7"])
    require(
        rows != list(accepted["selected_rows"]["F3"])
        and rows != list(accepted["selected_rows"]["F6"]),
        "persisted F7 row basis is distinct from F3 and F6",
    )
    f7_factorization = factor_list(f7, x, b)
    require(
        len(f7_factorization[1]) == 1
        and f7_factorization[1][0][1] == 1,
        "F7 is irreducible over QQ[X,B]",
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
    ) = exp125.exact_profile(base, directions, rows)
    component_sizes = [len(component) for component in components]
    require(
        time.time() - anchor_started <= ANCHOR_SCC_BUDGET_SECONDS,
        "anchor and SCC computation remains within budget",
    )
    require(max(component_sizes) <= 60, "largest exact cyclic block is at most 60")
    checkpoint = {
        "experiment": "EXP-127",
        "source_hashes": {"EXP-125_results": EXPECTED_E125_SHA256},
        "selected_rows": rows,
        "anchor": {
            "point": list(anchor_point),
            "determinant": str(anchor_det),
            "attempts": anchor_attempts,
        },
        "cyclic_component_sizes": component_sizes,
    }
    persist(checkpoint, CHECKPOINT)

    if os.environ.get("EXP127_REUSE_WORKER") == "1":
        require(
            sha256(WORKER_ARTIFACT) == EXPECTED_WORKER_SHA256,
            "hash-verified exact symbolic worker reused for repeatability check",
        )
    else:
        worker = subprocess.run(
            [sys.executable, str(WORKER)],
            cwd=HERE,
            capture_output=True,
            text=True,
            timeout=WORKER_TIMEOUT_SECONDS,
            check=False,
        )
        print(worker.stdout, end="", flush=True)
        if worker.stderr:
            print(worker.stderr, file=sys.stderr, end="", flush=True)
        require(worker.returncode == 0, "exact symbolic worker completed")
        require(
            sha256(WORKER_ARTIFACT) == EXPECTED_WORKER_SHA256,
            "exact symbolic worker hash",
        )
    worker_record = json.loads(WORKER_ARTIFACT.read_text(encoding="utf-8"))
    expression = sympify(
        worker_record["determinant_ratio"],
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
    require(graph_numerator != 0, "F7 basis is nonzero on the shared graph")

    direct_controls = []
    for av, bv, cv in ((1, 1, 0), (1, 0, 1), (2, 1, 1), (-1, 1, 1)):
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
        base, directions, f7, r, s, x, b, rows, accepted
    )

    quotient_started = time.time()
    coefficient_field = QQ.frac_field(b)
    graph_poly = Poly(graph_numerator, x, domain=coefficient_field)
    f7_poly = Poly(f7, x, domain=coefficient_field)
    quotient, raw_remainder = graph_poly.div(f7_poly)
    require(
        graph_poly == quotient * f7_poly + raw_remainder,
        "reconstructed graph numerator from F7 quotient and remainder",
    )
    require(not raw_remainder.is_zero, "graph section is nonzero in QQ(B)[X]/(F7)")
    require(raw_remainder.degree() <= 1, "F7 quotient remainder has X-degree at most one")
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
    require(u != 0, "primitive F7 section is genuinely linear in X")

    norm_resultant = expand(resultant(f7, h, x))
    require(norm_resultant != 0, "Sylvester resultant norm is nonzero")
    f7_x = Poly(f7, x, domain=QQ.frac_field(b))
    leading = expand(f7_x.LC())
    a1 = expand(f7_x.nth(1))
    a0 = expand(f7_x.nth(0))
    multiplication_matrix = Matrix(
        [[v, -u * a0 / leading], [u, v - u * a1 / leading]]
    )
    norm_multiplication = expand(multiplication_matrix.det())
    require(
        expand(norm_resultant - leading * norm_multiplication) == 0,
        "resultant and quadratic multiplication norms agree",
    )
    norm_poly = Poly(norm_resultant, b, domain=QQ).monic()
    require(norm_poly.degree() > 0, "F7 norm is nonconstant")
    norm_factor_coefficient, norm_factors = factor_list(norm_poly.as_expr(), b)
    factor_roles, retained_degree = classify_norm_factors(
        norm_factors, u, v, f7, r, s, x, b
    )
    require(
        [
            record["degree"]
            for record in factor_roles
            if record["removed_as_A_or_S_boundary"]
        ]
        == [1, 12],
        "only degree-1 and degree-12 norm factors are A-or-S boundary",
    )
    require(
        [
            record["degree"]
            for record in factor_roles
            if record["retained_conservatively_on_A_S_nonzero"]
        ]
        == [3, 9, 18],
        "degree-3, degree-9, and degree-18 factors survive on AS nonzero",
    )
    require(retained_degree == 30, "effective F7 principal-open residual has degree 30")
    require(
        time.time() - quotient_started <= QUOTIENT_BUDGET_SECONDS,
        "quotient and norm arithmetic remains within budget",
    )
    elapsed = time.time() - started
    require(elapsed <= TOTAL_GATE_SECONDS, "EXP-127 remains within total compute gate")

    payload = {
        "experiment": "EXP-127",
        "source_artifact_hashes": checkpoint["source_hashes"],
        "selected_rows": rows,
        "anchor": checkpoint["anchor"],
        "cyclic_component_sizes": component_sizes,
        "symbolic_worker_sha256": sha256(WORKER_ARTIFACT),
        "determinant_A_valuation": valuation,
        "invariant_Y_degree": y_degree,
        "invariant_determinant_X_B_Y": str(invariant),
        "graph_numerator": str(graph_numerator),
        "F7": str(f7),
        "F7_irreducible_over_QQ_X_B": True,
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
        "norm_factor_roles": factor_roles,
        "retained_norm_degree_with_multiplicity": retained_degree,
        "effective_A_S_nonzero_residual_degree": retained_degree,
        "effective_normalized_B_values_over_algebraic_closure": retained_degree,
        "effective_lifted_A_B_C_points_over_algebraic_closure": 3
        * retained_degree,
        "direct_exact_controls": direct_controls,
        "modular_sample_controls": modular_controls,
        "predictions": {
            "p1_anchor_and_scc_at_most_60": True,
            "p2_four_direct_exact_controls": True,
            "p3_nonzero_F7_quotient_class": True,
            "p4_nonzero_nonconstant_norm": True,
            "p5_two_norm_routes_agree": True,
        },
        "scope": (
            "Exact dense-open cover of only the F7 component on the AS!=0 "
            "EXP-123 graph, leaving a finite divisor projected into the norm "
            "roots. The finite F3/F6/F7 residuals, V(R,S), A=0, the full "
            "four-parameter restriction, (72,108), the degree floor, and "
            "JC(2) remain open."
        ),
    }
    persist(payload, ARTIFACT)
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {sha256(ARTIFACT)}", flush=True)
    print(
        f"[INFO] F7 norm degree={norm_poly.degree()}, "
        f"retained_degree={retained_degree}, factors={len(norm_factors)}, "
        f"elapsed={elapsed:.2f} s",
        flush=True,
    )
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    main()
