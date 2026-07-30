"""Convert EXP-117 shifted factors into the compact original (a,b) coordinates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from sympy import Poly, Rational, factor, gcd, sympify, symbols


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "artifacts" / "results.json"
TARGET = HERE / "artifacts" / "compact-factorization.json"


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    a, s, b, z = symbols("a s b z")
    coefficient = Rational(1)
    b_power = 0
    factors = []

    for block in source["block_factors"]:
        coefficient *= Rational(block["factor_coefficient"])
        for entry in block["factors"]:
            shifted = sympify(
                entry["expression"], locals={"a": a, "s": s}
            )
            original = factor(shifted.subs(s, b - 1))
            multiplicity = int(entry["multiplicity"])
            if original == b:
                b_power += multiplicity
                continue
            polynomial = Poly(original, a, b, domain="QQ")
            weighted_degrees = {
                7 * a_degree + 3 * b_degree
                for (a_degree, b_degree), _ in polynomial.terms()
            }
            assert len(weighted_degrees) == 1
            assert all(
                a_degree % 3 == 0
                for (a_degree, _), _ in polynomial.terms()
            )
            invariant = sum(
                coefficient_term * z ** (a_degree // 3)
                for (a_degree, _), coefficient_term in polynomial.terms()
            )
            factors.append(
                {
                    "expression": str(original),
                    "multiplicity": multiplicity,
                    "total_degree": int(polynomial.total_degree()),
                    "monomial_count": len(polynomial.terms()),
                    "source_block_size": int(block["size"]),
                    "weighted_degree_7_3": weighted_degrees.pop(),
                    "invariant_polynomial_z_a3_over_b7": str(invariant),
                }
            )

    assert b_power == 32
    assert len(factors) == 6
    large = next(
        entry for entry in factors if entry["source_block_size"] == 51
    )
    assert large["monomial_count"] == 5
    binomials = [
        entry for entry in factors if entry["source_block_size"] != 51
    ]
    assert len(binomials) == 5
    assert all(entry["monomial_count"] == 2 for entry in binomials)

    axis_exponent = b_power
    for entry in factors:
        specialized = Poly(
            sympify(entry["expression"], locals={"a": a, "b": b}).subs(
                a, 0
            ),
            b,
            domain="QQ",
        )
        axis_exponent += (
            specialized.degree() * entry["multiplicity"]
        )
    assert axis_exponent == 95
    invariant_product = Rational(1)
    for entry in factors:
        invariant_product *= sympify(
            entry["invariant_polynomial_z_a3_over_b7"],
            locals={"z": z},
        ) ** entry["multiplicity"]
    invariant_product = factor(invariant_product)
    invariant_poly = Poly(invariant_product, z, domain="QQ")
    assert invariant_poly.degree() == 9
    assert gcd(invariant_poly, invariant_poly.diff()).degree() == 0

    artifact = {
        "experiment": "EXP-117",
        "coordinates": ["a", "b"],
        "scalar": str(coefficient),
        "explicit_b_power": b_power,
        "factors": factors,
        "a_zero_total_b_exponent": axis_exponent,
        "b_nonzero_invariant": {
            "coordinate": "z=a^3/b^7",
            "polynomial": str(invariant_product),
            "degree": int(invariant_poly.degree()),
            "squarefree": True,
            "geometric_points": int(invariant_poly.degree()),
        },
        "normalized_anchor_check": (
            "scalar times all factors at (a,b)=(0,1) equals 1"
        ),
    }
    anchor = coefficient
    for entry in factors:
        expression = sympify(
            entry["expression"], locals={"a": a, "b": b}
        )
        anchor *= expression.subs({a: 0, b: 1}) ** entry[
            "multiplicity"
        ]
    assert anchor == 1

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
    TARGET.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] compact factorization written: {TARGET.relative_to(HERE)}")
    print(f"[PASS] explicit b power {b_power}; a=0 total exponent {axis_exponent}")
    print(f"SHA256 {digest}")


if __name__ == "__main__":
    main()
