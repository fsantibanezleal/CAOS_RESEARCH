"""EXP-120: exact third weighted-open chart and common component ideals.

CPU-only. Modular arithmetic reproduces the persisted row-basis witness.
All chart and ideal conclusions use exact QQ arithmetic.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

from sympy import (
    Poly,
    Rational,
    factor,
    factor_list,
    groebner,
    sympify,
    symbols,
)


HERE = Path(__file__).resolve().parent
E119_PATH = HERE.parent / "EXP-119-weighted-open-exact-chart" / "run.py"
E119_COMPACT = (
    HERE.parent
    / "EXP-119-weighted-open-exact-chart"
    / "artifacts"
    / "compact-invariant.json"
)
E115_ARTIFACT = (
    HERE.parent
    / "EXP-115-weighted-residual-component-gate"
    / "artifacts"
    / "results.json"
)
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"

spec = importlib.util.spec_from_file_location("exp119", E119_PATH)
exp119 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp119)
exp115 = exp119.exp115


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def persist(payload) -> None:
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def modular_recheck(base, directions, rows):
    prime = 1009
    evaluated = exp115.combine_mod(
        exp115.matrix_mod(base, prime),
        exp115.matrix_mod(directions[(0, 1)], prime),
        exp115.matrix_mod(directions[(0, 5)], prime),
        exp115.matrix_mod(directions[(1, 0)], prime),
        64,
        4,
        1,
        prime,
    )
    determinant = exp115.determinant_mod(evaluated, rows, prime)
    require(
        determinant == 978,
        "EXP-115 G-basis determinant 978 reproduces at p=1009",
    )
    return {
        "prime": prime,
        "point": {"A": 64, "B": 4, "d": 1},
        "determinant": determinant,
    }


def choose_anchor(base, directions, rows):
    controls = (
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (2, 1),
        (1, 2),
        (-1, -1),
    )
    attempts = []
    for av, bv in controls:
        matrix = (
            base
            + Rational(av) * directions[(0, 1)]
            + Rational(bv) * directions[(0, 5)]
        ).extract(rows, range(125))
        determinant = matrix.det(method="domain-ge")
        attempts.append(
            {
                "point": {"A": av, "B": bv, "d": 1},
                "determinant": str(determinant),
            }
        )
        if determinant != 0:
            require(
                True,
                f"first exact G-basis anchor is nonzero at {(av, bv, 1)}",
            )
            return Rational(av), Rational(bv), matrix, determinant, attempts
    raise AssertionError("no deterministic rational G-basis anchor found")


def direct_checks(
    base,
    directions,
    rows,
    anchor_a,
    anchor_b,
    anchor_determinant,
    expressions,
    a,
    s,
):
    points = (
        (anchor_a, anchor_b),
        (Rational(0), Rational(0)),
        (Rational(1), Rational(0)),
        (Rational(0), Rational(1)),
        (Rational(-1), Rational(2)),
    )
    checks = []
    for av, bv in points:
        normalized = Rational(1)
        for expression in expressions:
            normalized *= expression.subs(
                {a: av - anchor_a, s: bv - anchor_b}
            )
        predicted = anchor_determinant * normalized
        direct = (
            base
            + av * directions[(0, 1)]
            + bv * directions[(0, 5)]
        ).extract(rows, range(125)).det(method="domain-ge")
        require(
            predicted == direct,
            f"third-chart block product matches at {(av, bv)}",
        )
        checks.append(
            {
                "point": {"A": str(av), "B": str(bv), "d": "1"},
                "determinant": str(direct),
            }
        )
    return checks


def invariant_form(expression, a, b):
    x = symbols("X")
    polynomial = Poly(expression, a, b, domain="QQ")
    residues = {
        a_degree % 3
        for (a_degree, _), _ in polynomial.terms()
    }
    require(
        len(residues) == 1,
        "third determinant has one A-exponent residue modulo three",
    )
    residue = residues.pop()
    minimum = min(
        a_degree for (a_degree, _), _ in polynomial.terms()
    )
    require(
        minimum % 3 == residue,
        "third determinant minimum A-power matches its residue",
    )
    invariant = sum(
        coefficient
        * x ** ((a_degree - minimum) // 3)
        * b**b_degree
        for (a_degree, b_degree), coefficient in polynomial.terms()
    )
    reconstructed = a**minimum * invariant.subs(x, a**3)
    require(
        Poly(reconstructed - expression, a, b, domain="QQ").is_zero,
        "third determinant reconstructs exactly under X=A^3",
    )
    return x, minimum, factor(invariant)


def component_generators(x, b):
    source_x, source_b, g, _, linear, quadratic, _ = (
        exp115.residue_polynomials()
    )
    return {
        "G": g.subs({source_x: x, source_b: b}),
        "L": linear.subs({source_x: x, source_b: b}),
        "Q": quadratic.subs({source_x: x, source_b: b}),
    }


def ideal_record(
    component,
    first_chart,
    third_chart,
    x,
    b,
    *,
    compute_lex: bool,
):
    started = time.time()
    basis = groebner(
        [component, first_chart, third_chart],
        x,
        b,
        order="grlex",
        domain="QQ",
    )
    elapsed = time.time() - started
    if elapsed > 180:
        raise TimeoutError("component Groebner basis exceeded 180 seconds")
    expressions = [polynomial.as_expr() for polynomial in basis.polys]
    unit = len(expressions) == 1 and expressions[0] == 1
    record = {
        "unit_ideal": unit,
        "grlex_basis": [str(expression) for expression in expressions],
        "grlex_basis_size": len(expressions),
        "elapsed_seconds": elapsed,
    }
    if unit:
        return record

    require(
        basis.is_zero_dimensional,
        "nonunit common component ideal is zero-dimensional",
    )
    record["zero_dimensional"] = True
    if not compute_lex:
        record["lex_status"] = (
            "FGLM conversion stopped at the declared 180-second gate; "
            "zero-dimensional grlex certificate is persisted"
        )
        return record

    lex_started = time.time()
    lex_basis = basis.fglm(order="lex")
    lex_elapsed = time.time() - lex_started
    if lex_elapsed > 180:
        raise TimeoutError("component FGLM conversion exceeded 180 seconds")
    lex_expressions = [
        polynomial.as_expr() for polynomial in lex_basis.polys
    ]
    univariate = [
        expression
        for expression in lex_expressions
        if not expression.has(x)
    ]
    require(
        len(univariate) == 1,
        "nonunit lex basis has one B-elimination polynomial",
    )
    elimination = Poly(univariate[0], b, domain="QQ")
    squarefree = elimination.sqf_part().monic()
    record.update(
        {
            "lex_basis": [str(expression) for expression in lex_expressions],
            "lex_basis_size": len(lex_expressions),
            "fglm_elapsed_seconds": lex_elapsed,
            "elimination_B": str(elimination.as_expr()),
            "elimination_degree_B": int(elimination.degree()),
            "squarefree_elimination_B": str(squarefree.as_expr()),
            "squarefree_degree_B": int(squarefree.degree()),
        }
    )
    return record


def split_product_ideal(component, first_chart, third_chart, x, b):
    coefficient, factors = factor_list(third_chart, x, b)
    records = []
    all_unit = True
    for expression, multiplicity in factors:
        started = time.time()
        basis = groebner(
            [component, first_chart, expression],
            x,
            b,
            order="grlex",
            domain="QQ",
        )
        elapsed = time.time() - started
        if elapsed > 180:
            raise TimeoutError(
                "factorwise G-component Groebner basis exceeded 180 seconds"
            )
        basis_expressions = [
            polynomial.as_expr() for polynomial in basis.polys
        ]
        unit = (
            len(basis_expressions) == 1
            and basis_expressions[0] == 1
        )
        all_unit = all_unit and unit
        record = {
            "factor": str(expression),
            "multiplicity": int(multiplicity),
            "unit_ideal": unit,
            "basis_size": len(basis_expressions),
            "basis": [str(value) for value in basis_expressions],
            "elapsed_seconds": elapsed,
        }
        if not unit:
            require(
                basis.is_zero_dimensional,
                "nonunit G factor ideal is zero-dimensional",
            )
            record["zero_dimensional"] = True
        records.append(record)
        print(
            f"[INFO] G factor {expression}: "
            f"{'unit' if unit else 'nonunit finite'} in {elapsed:.2f} s",
            flush=True,
        )
    return {
        "unit_ideal": all_unit,
        "method": "factorwise exact decomposition of the third determinant",
        "factor_coefficient": str(coefficient),
        "factor_ideals": records,
        "direct_full_product_attempt": (
            "stopped at the declared component gate before factorwise "
            "decomposition"
        ),
    }


def main() -> None:
    started = time.time()
    base, directions, _ = exp115.build_system()
    exp115_record = json.loads(E115_ARTIFACT.read_text(encoding="utf-8"))
    rows = exp115_record["open_chart"]["witnesses"]["components"]["G"][
        "row_basis"
    ]
    require(len(rows) == 125, "persisted G-component basis has size 125")
    modular = modular_recheck(base, directions, rows)
    anchor_a, anchor_b, anchor, anchor_det, anchor_attempts = (
        choose_anchor(base, directions, rows)
    )

    inverse = anchor.inv()
    selected_a = directions[(0, 1)].extract(rows, range(125))
    selected_b = directions[(0, 5)].extract(rows, range(125))
    normalized_a = inverse * selected_a
    normalized_b = inverse * selected_b
    graph = exp119.cyclic_components(normalized_a, normalized_b)
    largest = max(len(component) for component in graph["cyclic"])
    print(
        f"[INFO] third-chart cyclic SCC sizes "
        f"{[len(component) for component in graph['cyclic']]}",
        flush=True,
    )
    require(
        largest <= 60,
        "third-chart largest cyclic block is within gate 60",
    )

    shifted_a, shifted_b, blocks, expressions, largest_elapsed = (
        exp119.compute_blocks(normalized_a, normalized_b, graph)
    )
    a, b = symbols("A B")
    normalized_product = Rational(1)
    for expression in expressions:
        normalized_product *= expression
    original = factor(
        normalized_product.subs(
            {
                shifted_a: a - anchor_a,
                shifted_b: b - anchor_b,
            }
        )
    )
    original_poly = Poly(original, a, b, domain="QQ")
    require(
        len(original_poly.terms()) <= 10000,
        "third determinant is below the 10000-monomial gate",
    )
    checks = direct_checks(
        base,
        directions,
        rows,
        anchor_a,
        anchor_b,
        anchor_det,
        expressions,
        shifted_a,
        shifted_b,
    )
    x, coordinate_power, invariant = invariant_form(original, a, b)
    invariant_poly = Poly(invariant, x, b, domain="QQ")
    require(
        len(invariant_poly.terms()) <= 10000,
        "third invariant determinant is below the expansion gate",
    )
    require(
        coordinate_power % 3 == 0,
        "third coordinate A-power descends to an X-power",
    )
    full_invariant = factor(
        x ** (coordinate_power // 3) * invariant
    )
    full_invariant_poly = Poly(full_invariant, x, b, domain="QQ")

    first_record = json.loads(E119_COMPACT.read_text(encoding="utf-8"))
    first_chart = sympify(
        first_record["alternative_determinant_in_X_B"],
        locals={"X": x, "B": b},
    )
    components = component_generators(x, b)
    checkpoint = {
        "experiment": "EXP-120",
        "anchor": {
            "A": str(anchor_a),
            "B": str(anchor_b),
            "d": "1",
            "determinant": str(anchor_det),
        },
        "third_invariant_reduced": str(invariant),
        "third_invariant_full": str(full_invariant),
        "coordinate_A_power": coordinate_power,
        "component_ideals": {},
    }
    persist(checkpoint)

    print("[INFO] computing factorwise common ideal on G", flush=True)
    ideals = {
        "G": split_product_ideal(
            components["G"], first_chart, full_invariant, x, b
        )
    }
    checkpoint["component_ideals"] = ideals
    persist(checkpoint)
    for name in ("L", "Q"):
        component = components[name]
        print(f"[INFO] computing common ideal on {name}", flush=True)
        record = ideal_record(
            component,
            first_chart,
            full_invariant,
            x,
            b,
            compute_lex=name == "L",
        )
        ideals[name] = record
        checkpoint["component_ideals"] = ideals
        persist(checkpoint)
        print(
            f"[INFO] {name}: "
            f"{'unit' if record['unit_ideal'] else 'nonunit finite'} "
            f"in {record['elapsed_seconds']:.2f} s",
            flush=True,
        )

    all_unit = all(
        record["unit_ideal"] is True for record in ideals.values()
    )
    artifact = {
        "experiment": "EXP-120",
        "row_basis": rows,
        "modular_control": modular,
        "anchor_attempts": anchor_attempts,
        "anchor": checkpoint["anchor"],
        "graph": {
            "component_sizes": [
                len(component) for component in graph["all"]
            ],
            "cyclic_component_sizes": [
                len(component) for component in graph["cyclic"]
            ],
            "edge_count": graph["edge_count"],
            "direction_nonzero_counts": graph[
                "direction_nonzero_counts"
            ],
            "sha256": graph["sha256"],
        },
        "blocks": blocks,
        "normalized_product": str(normalized_product),
        "third_determinant_d1_up_to_anchor_scalar": str(original),
        "third_determinant_total_degree": int(
            original_poly.total_degree()
        ),
        "third_determinant_monomial_count": len(
            original_poly.terms()
        ),
        "coordinate_A_power": coordinate_power,
        "third_invariant_reduced_X_B": str(invariant),
        "third_invariant_full_X_B": str(full_invariant),
        "third_invariant_degree_X": int(
            full_invariant_poly.degree(x)
        ),
        "third_invariant_degree_B": int(
            full_invariant_poly.degree(b)
        ),
        "third_invariant_monomial_count": len(
            full_invariant_poly.terms()
        ),
        "direct_checks": checks,
        "component_ideals": ideals,
        "predictions": {
            "rational_anchor_in_first_nine": True,
            "largest_cyclic_block_at_most_60": largest <= 60,
            "determinant_at_most_500_monomials": len(
                original_poly.terms()
            )
            <= 500,
            "at_least_two_unit_component_ideals": sum(
                record["unit_ideal"] is True
                for record in ideals.values()
            )
            >= 2,
            "all_component_ideals_unit": all_unit,
        },
        "largest_block_elapsed_seconds": largest_elapsed,
        "elapsed_seconds": time.time() - started,
        "scope": (
            "Third exact d=1 chart on TB. All-unit component ideals "
            "close d!=0; nonunit ideals persist the common finite residual."
        ),
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"[INFO] elapsed {time.time() - started:.2f} s", flush=True)
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"RESULT: FAILED: {error}", file=sys.stderr, flush=True)
        raise
