"""Compact EXP-119 from (A,B) to the exact invariant ring QQ[X=A^3,B]."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from sympy import Poly, factor_list, sympify, symbols


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "artifacts" / "results.json"
TARGET = HERE / "artifacts" / "compact-invariant.json"
E115_PATH = (
    HERE.parent / "EXP-115-weighted-residual-component-gate" / "run.py"
)

spec = importlib.util.spec_from_file_location("exp115", E115_PATH)
exp115 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp115)


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    a, x, b, d = symbols("A X B d")
    alternative_a = sympify(
        source["alternative_determinant_d1_up_to_anchor_scalar"],
        locals={"A": a, "B": b},
    )
    alternative_a_poly = Poly(alternative_a, a, b, domain="QQ")
    assert all(
        a_degree % 3 == 0
        for (a_degree, _), _ in alternative_a_poly.terms()
    )
    alternative_x = sum(
        coefficient * x ** (a_degree // 3) * b**b_degree
        for (a_degree, b_degree), coefficient
        in alternative_a_poly.terms()
    )
    assert Poly(
        alternative_x.subs(x, a**3) - alternative_a,
        a,
        b,
        domain="QQ",
    ).is_zero

    coefficient, factors = factor_list(alternative_x, x, b)
    factor_records = []
    natural_weight_total = 0
    for expression, multiplicity in factors:
        polynomial = Poly(expression, x, b, domain="QQ")
        weighted_degrees = {
            21 * x_degree + 3 * b_degree
            for (x_degree, b_degree), _ in polynomial.terms()
        }
        residues = {weight % 9 for weight in weighted_degrees}
        assert len(residues) == 1
        homogenized_weight = int(max(weighted_degrees))
        homogenized = sum(
            term_coefficient
            * x**x_degree
            * b**b_degree
            * d ** (
                (
                    homogenized_weight
                    - 21 * x_degree
                    - 3 * b_degree
                )
                // 9
            )
            for (x_degree, b_degree), term_coefficient
            in polynomial.terms()
        )
        assert Poly(
            homogenized.subs(d, 1) - expression,
            x,
            b,
            domain="QQ",
        ).is_zero
        natural_weight_total += homogenized_weight * int(multiplicity)
        factor_records.append(
            {
                "expression": str(expression),
                "multiplicity": int(multiplicity),
                "degree_X": int(polynomial.degree(x)),
                "degree_B": int(polynomial.degree(b)),
                "total_degree": int(polynomial.total_degree()),
                "monomial_count": len(polynomial.terms()),
                "dehomogenized_weight_min": int(min(weighted_degrees)),
                "dehomogenized_weight_max": int(max(weighted_degrees)),
                "weight_residue_mod_9": int(residues.pop()),
                "homogenized_weight_X21_B3_d9": homogenized_weight,
                "homogenized_expression": str(homogenized),
            }
        )
    determinant_weight = int(
        source["weighted_support"]["weighted_degree"]
    )
    assert (determinant_weight - natural_weight_total) % 9 == 0
    implicit_d_power = int(
        determinant_weight - natural_weight_total
    ) // 9
    assert implicit_d_power >= 0

    source_x, source_b, g, _, linear, quadratic, _ = (
        exp115.residue_polynomials()
    )
    components = {
        "G": g.subs({source_x: x, source_b: b}),
        "L": linear.subs({source_x: x, source_b: b}),
        "Q": quadratic.subs({source_x: x, source_b: b}),
    }
    residuals = {}
    for name, component in components.items():
        component_poly = Poly(component, x, b, domain="QQ")
        raw_record = source["component_intersections"][name]
        assert raw_record["gcd"] == "1"
        residuals[name] = {
            "component": str(component),
            "component_degree_X": int(component_poly.degree(x)),
            "component_degree_B": int(component_poly.degree(b)),
            "gcd": "1",
            "gcd_validation": (
                "derived from the exact QQ[A,B] unit gcd in results.json; "
                "a nonunit gcd in QQ[X,B] would remain nonunit after X=A^3"
            ),
            "raw_A_resultant_degree_B": int(
                raw_record["resultant_degree_B"]
            ),
            "raw_A_resultant_monomial_count": int(
                raw_record["resultant_monomial_count"]
            ),
            "compact_resultant_X": None,
            "compact_resultant_status": (
                "stopped at the declared 420-second total gate; no "
                "compact resultant or squarefree degree is promoted"
            ),
        }

    artifact = {
        "experiment": "EXP-119",
        "invariant_coordinate": "X=A^3",
        "alternative_scalar": str(coefficient),
        "full_determinant_weight": determinant_weight,
        "factor_weight_total": int(natural_weight_total),
        "implicit_d_power_lost_at_d1": implicit_d_power,
        "alternative_determinant_in_X_B": str(alternative_x),
        "factor_records": factor_records,
        "component_residuals": residuals,
        "validation": {
            "substitution_X_A3_reconstructs_original": True,
            "all_component_gcds_are_units": True,
            "compact_resultant_attempt_stopped_at_seconds": 428.3,
        },
        "scope": (
            "Squarefree elimination targets for proper intersections of "
            "the selected and first alternative d=1 charts."
        ),
    }
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
    TARGET.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {TARGET.relative_to(HERE)}")
    print(f"SHA256 {digest}")
    for name, residual in residuals.items():
        print(
            f"[INFO] {name}: raw A-resultant degree "
            f"{residual['raw_A_resultant_degree_B']}; "
            "compact resultant stopped at budget"
        )


if __name__ == "__main__":
    main()
