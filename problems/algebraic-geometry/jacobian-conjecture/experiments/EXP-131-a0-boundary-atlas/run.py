"""EXP-131: exact two-minor atlas on the direct A=0 boundary."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from sympy import Poly, expand, factor, gcdex, symbols


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
E115_PATH = (
    EXPERIMENTS / "EXP-115-weighted-residual-component-gate" / "run.py"
)
ARTIFACT = HERE / "artifacts" / "results.json"
PRIMES = (1009, 1153)

spec = importlib.util.spec_from_file_location("exp115", E115_PATH)
exp115 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp115)
exp112 = exp115.exp112


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def persist(payload: dict[str, object]) -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build_boundary_system():
    forced = exp112.forced_polynomial()
    directions = sorted(exp112.exp071.LOWER)
    _, row_labels = exp112.complete_row_labels(forced, directions)
    constant_column = exp112.exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp112.exp071.NQ))
        if index != constant_column
    ]
    base = exp112.coefficient_matrix(
        forced, row_labels, q_columns, include_rhs=True
    )
    db = exp112.coefficient_matrix(
        {(0, 5): exp112.Fraction(1)},
        row_labels,
        q_columns,
        include_rhs=False,
    )
    dc = exp112.coefficient_matrix(
        {(2, 9): exp112.Fraction(1)},
        row_labels,
        q_columns,
        include_rhs=False,
    )
    require(base.shape == (302, 125), "rebuilt the complete 302 by 125 system")
    return base, db, dc


def matrix_mod_at(base_mod, db_mod, dc_mod, b_value, c_value, prime):
    return [
        [
            (
                base_mod[row][column]
                + b_value * db_mod[row][column]
                + c_value * dc_mod[row][column]
            )
            % prime
            for column in range(125)
        ]
        for row in range(302)
    ]


def main() -> None:
    base, db, dc = build_boundary_system()
    b, c = symbols("B C")

    modular_records = []
    primary_rows = None
    alternative_rows = None
    for prime in PRIMES:
        base_mod = exp115.matrix_mod(base, prime)
        db_mod = exp115.matrix_mod(db, prime)
        dc_mod = exp115.matrix_mod(dc, prime)
        at_origin = matrix_mod_at(
            base_mod, db_mod, dc_mod, 0, 0, prime
        )
        current_primary = exp115.independent_row_basis(at_origin, prime)
        require(
            len(current_primary) == 125,
            f"generic boundary control has rank 125 modulo {prime}",
        )
        linear_root = (-4 * pow(5, -1, prime)) % prime
        at_linear = matrix_mod_at(
            base_mod, db_mod, dc_mod, linear_root, 0, prime
        )
        current_alternative = exp115.independent_row_basis(at_linear, prime)
        require(
            len(current_alternative) == 125,
            f"linear residual fibre has rank 125 modulo {prime}",
        )
        if primary_rows is None:
            primary_rows = current_primary
            alternative_rows = current_alternative
        else:
            require(
                current_primary == primary_rows,
                "primary row basis is stable across selection primes",
            )
            require(
                current_alternative == alternative_rows,
                "alternative row basis is stable across selection primes",
            )
        quadratic_roots = [
            value
            for value in range(prime)
            if (25 * value * value - 20 * value + 16) % prime == 0
        ]
        residual_controls = []
        for name, b_value in (
            [("linear", linear_root)]
            + [
                (f"quadratic-{index}", value)
                for index, value in enumerate(quadratic_roots)
            ]
        ):
            ranks = []
            for c_value in (0, 1, 2, 3, 5):
                matrix = matrix_mod_at(
                    base_mod,
                    db_mod,
                    dc_mod,
                    b_value,
                    c_value,
                    prime,
                )
                ranks.append(
                    len(exp115.independent_row_basis(matrix, prime))
                )
            require(
                ranks == [125] * 5,
                f"{name} residual controls retain rank 125 modulo {prime}",
            )
            residual_controls.append(
                {"name": name, "B": b_value, "ranks": ranks}
            )
        modular_records.append(
            {
                "prime": prime,
                "linear_root": linear_root,
                "quadratic_roots": quadratic_roots,
                "residual_controls": residual_controls,
            }
        )

    assert primary_rows is not None and alternative_rows is not None
    columns = range(125)
    primary_matrix = (base + b * db + c * dc).extract(
        primary_rows, columns
    )
    alternative_matrix = (base + b * db + c * dc).extract(
        alternative_rows, columns
    )
    print("[INFO] reconstructing the primary exact determinant", flush=True)
    primary = factor(primary_matrix.det(method="domain-ge"))
    print("[INFO] reconstructing the alternative exact determinant", flush=True)
    alternative = factor(alternative_matrix.det(method="domain-ge"))
    primary_poly = Poly(primary, b, c)
    alternative_poly = Poly(alternative, b, c)
    require(primary_poly.degree(c) == 0, "primary section is independent of C")
    require(
        alternative_poly.degree(c) == 0,
        "alternative section is independent of C",
    )

    linear = 5 * b + 4
    quadratic = 25 * b**2 - 20 * b + 16
    first_divisor = expand(linear * quadratic)
    second_divisor = expand(
        b
        * (109375 * b**6 - 110592)
        * (21875 * b**6 - 4800 * b**3 - 24576)
    )
    expected_primary_without_scalar = expand(linear**3 * quadratic**3)
    primary_quotient = factor(primary / expected_primary_without_scalar)
    require(
        not primary_quotient.has(b, c),
        "primary determinant has exactly the declared two residual fibres",
    )
    alternative_quotient = factor(
        alternative
        / (
            b**95
            * (109375 * b**6 - 110592)
            * (21875 * b**6 - 4800 * b**3 - 24576)
        )
    )
    require(
        not alternative_quotient.has(b, c),
        "alternative determinant has the reconstructed exact factorization",
    )

    bezout_first, bezout_second, divisor_gcd = gcdex(
        Poly(first_divisor, b, domain="QQ"),
        Poly(second_divisor, b, domain="QQ"),
    )
    require(divisor_gcd.as_expr() == 1, "the two determinant divisors have unit gcd")
    bezout_check = expand(
        bezout_first.as_expr() * first_divisor
        + bezout_second.as_expr() * second_divisor
    )
    require(bezout_check == 1, "verified the exact Bezout identity")

    exact_controls = []
    for b_value, c_value in ((0, 0), (1, 0), (0, 1), (2, 3)):
        direct_primary = (
            base + b_value * db + c_value * dc
        ).extract(primary_rows, columns).det(method="domain-ge")
        direct_alternative = (
            base + b_value * db + c_value * dc
        ).extract(alternative_rows, columns).det(method="domain-ge")
        require(
            direct_primary == primary.subs({b: b_value, c: c_value}),
            f"primary direct control agrees at ({b_value},{c_value})",
        )
        require(
            direct_alternative
            == alternative.subs({b: b_value, c: c_value}),
            f"alternative direct control agrees at ({b_value},{c_value})",
        )
        exact_controls.append(
            {
                "B": b_value,
                "C": c_value,
                "primary": str(direct_primary),
                "alternative": str(direct_alternative),
            }
        )

    payload = {
        "experiment": "EXP-131",
        "decision": "confirmed_complete_A0_boundary_atlas",
        "source_sha256": {
            "EXP-112-run.py": sha256(exp112.HERE / "run.py"),
            "EXP-115-run.py": sha256(E115_PATH),
        },
        "matrix_shape": list(base.shape),
        "parameterization": "A=0, d=1, M0(B,C)=base+B*M_(0,5)+C*M_(2,9)",
        "selection_primes": list(PRIMES),
        "primary_rows": primary_rows,
        "alternative_rows": alternative_rows,
        "modular_controls": modular_records,
        "primary_determinant": str(primary),
        "primary_scalar": str(primary_quotient),
        "primary_divisor": str(first_divisor),
        "primary_degree_B": int(primary_poly.degree(b)),
        "primary_degree_C": int(primary_poly.degree(c)),
        "alternative_determinant": str(alternative),
        "alternative_scalar": str(alternative_quotient),
        "alternative_divisor": str(second_divisor),
        "alternative_degree_B": int(alternative_poly.degree(b)),
        "alternative_degree_C": int(alternative_poly.degree(c)),
        "bezout": {
            "first_coefficient": str(bezout_first.as_expr()),
            "second_coefficient": str(bezout_second.as_expr()),
            "gcd": str(divisor_gcd.as_expr()),
            "identity": "u(B)*first_divisor+v(B)*second_divisor=1",
        },
        "direct_exact_controls": exact_controls,
        "predictions": {
            "p1_generic_rank_125": True,
            "p2_two_fibre_primary_divisor": True,
            "p3_alternative_covers_both_fibres": True,
            "p4_unit_gcd": True,
        },
        "scope": (
            "Closes A=0 on the normalized d=1 four-coefficient restriction. "
            "Together with EXP-118 and EXP-123/129/130 this closes that "
            "declared restriction, not the 24-parameter core, full 51-parameter "
            "family, (72,108), the degree floor, or JC(2)."
        ),
    }
    persist(payload)
    print(f"[INFO] artifact SHA-256: {sha256(ARTIFACT)}", flush=True)
    print("RESULT: CONFIRMED COMPLETE A=0 BOUNDARY ATLAS", flush=True)


if __name__ == "__main__":
    main()
