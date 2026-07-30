"""EXP-121: select maximal-minor row bases on the finite L/Q residuals.

Modular arithmetic selects deterministic bases only. All component-closure
claims use exact Groebner bases over QQ[X,B].
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

from sympy import (
    Matrix,
    Poly,
    QQ,
    Rational,
    cancel,
    factor,
    groebner,
    sympify,
    symbols,
)


HERE = Path(__file__).resolve().parent
E120_PATH = HERE.parent / "EXP-120-third-open-chart-ideal" / "run.py"
E115_ARTIFACT = (
    HERE.parent
    / "EXP-115-weighted-residual-component-gate"
    / "artifacts"
    / "results.json"
)
E119_COMPACT = (
    HERE.parent
    / "EXP-119-weighted-open-exact-chart"
    / "artifacts"
    / "compact-invariant.json"
)
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
PRIMES = (1009, 1013, 1019, 1031, 1033, 1039, 1049)
MAX_CANDIDATES = 3
TOTAL_GATE_SECONDS = 1200

spec = importlib.util.spec_from_file_location("exp120", E120_PATH)
exp120 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp120)
exp119 = exp120.exp119
exp115 = exp119.exp115


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def persist(payload: dict[str, object], path: Path = CHECKPOINT) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def polynomial_terms(expression, x, b, prime: int):
    polynomial = Poly(expression, x, b, domain="QQ")
    return [
        (x_degree, b_degree, exp115.mod_entry(coefficient, prime))
        for (x_degree, b_degree), coefficient in polynomial.terms()
    ]


def evaluate_terms(terms, x_value: int, b_value: int, prime: int) -> int:
    return sum(
        coefficient
        * pow(x_value, x_degree, prime)
        * pow(b_value, b_degree, prime)
        for x_degree, b_degree, coefficient in terms
    ) % prime


def x_coefficient_terms(expression, x, b, prime: int):
    polynomial = Poly(expression, x, b, domain="QQ")
    coefficients: dict[int, list[tuple[int, int]]] = {}
    for (x_degree, b_degree), coefficient in polynomial.terms():
        coefficients.setdefault(x_degree, []).append(
            (b_degree, exp115.mod_entry(coefficient, prime))
        )
    return coefficients


def roots_in_x(
    coefficient_terms,
    b_value: int,
    prime: int,
    square_roots: dict[int, list[int]],
) -> list[int]:
    coefficients = {
        x_degree: sum(
            coefficient * pow(b_value, b_degree, prime)
            for b_degree, coefficient in terms
        )
        % prime
        for x_degree, terms in coefficient_terms.items()
    }
    degree = max(
        (degree for degree, value in coefficients.items() if value),
        default=-1,
    )
    if degree == -1:
        return list(range(prime))
    if degree == 0:
        return []
    if degree == 1:
        return [
            -coefficients.get(0, 0)
            * pow(coefficients[1], -1, prime)
            % prime
        ]
    if degree != 2:
        raise AssertionError("residual component is at most quadratic in X")
    a2 = coefficients[2]
    a1 = coefficients.get(1, 0)
    a0 = coefficients.get(0, 0)
    discriminant = (a1 * a1 - 4 * a2 * a0) % prime
    roots = square_roots.get(discriminant, [])
    inverse = pow(2 * a2 % prime, -1, prime)
    return sorted({(-a1 + root) * inverse % prime for root in roots})


def residual_points(
    component_name: str,
    component,
    factor_records,
    x,
    b,
    prime: int,
) -> list[dict[str, object]]:
    started = time.time()
    factors = [
        (
            record["expression"],
            polynomial_terms(
                sympify(record["expression"], locals={"X": x, "B": b}),
                x,
                b,
                prime,
            ),
        )
        for record in factor_records
    ]
    component_terms = polynomial_terms(component, x, b, prime)
    component_x_terms = x_coefficient_terms(component, x, b, prime)
    cube_roots: dict[int, list[int]] = {}
    for a_value in range(prime):
        cube_roots.setdefault(pow(a_value, 3, prime), []).append(a_value)
    square_roots: dict[int, list[int]] = {}
    for value in range(prime):
        square_roots.setdefault(value * value % prime, []).append(value)

    points: list[dict[str, object]] = []
    for b_value in range(prime):
        for x_value in roots_in_x(
            component_x_terms, b_value, prime, square_roots
        ):
            if (
                evaluate_terms(
                    component_terms, x_value, b_value, prime
                )
                != 0
            ):
                raise AssertionError(
                    f"{component_name} modular root violates its component"
                )
            zero_factors = [
                label
                for label, terms in factors
                if evaluate_terms(terms, x_value, b_value, prime) == 0
            ]
            if not zero_factors or x_value not in cube_roots:
                continue
            for a_value in cube_roots[x_value]:
                points.append(
                    {
                        "A": a_value,
                        "B": b_value,
                        "X": x_value,
                        "zero_factors": zero_factors,
                    }
                )
    points.sort(
        key=lambda point: (
            len(point["zero_factors"]),
            point["zero_factors"][0],
            point["B"],
            point["X"],
            point["A"],
        )
    )
    require(
        time.time() - started <= 180,
        f"{component_name} modular residual enumeration meets its gate",
    )
    print(
        f"[INFO] p={prime} {component_name}: "
        f"{len(points)} affine A-lifts on the first-chart residual",
        flush=True,
    )
    return points


def select_candidates(
    component_name: str,
    points: list[dict[str, object]],
    prime: int,
    matrices,
    pinned_rows,
    first_rows,
    forbidden_bases: set[tuple[int, ...]],
) -> tuple[list[dict[str, object]], dict[str, int]]:
    base_mod, da, db, dc = matrices
    candidates: list[dict[str, object]] = []
    rank_profiles: dict[str, int] = {}
    trials = 0
    for point in points:
        if trials >= 30 or len(candidates) >= MAX_CANDIDATES:
            break
        trials += 1
        evaluated = exp115.combine_mod(
            base_mod,
            da,
            db,
            dc,
            point["A"],
            point["B"],
            1,
            prime,
        )
        first_determinant = exp115.determinant_mod(
            evaluated, first_rows, prime
        )
        require(
            first_determinant == 0,
            f"{component_name} selection point lies on EXP-119 chart",
        )
        basis = exp115.independent_row_basis(evaluated, prime)
        coefficient_basis = exp115.independent_row_basis(
            [row[:124] for row in evaluated], prime
        )
        profile = f"{len(coefficient_basis)}/{len(basis)}"
        rank_profiles[profile] = rank_profiles.get(profile, 0) + 1
        if len(basis) != 125:
            continue
        basis_key = tuple(basis)
        if basis_key in forbidden_bases:
            continue
        determinant = exp115.determinant_mod(evaluated, basis, prime)
        require(
            determinant != 0,
            f"{component_name} residual-selected minor is nonzero mod {prime}",
        )
        forbidden_bases.add(basis_key)
        candidates.append(
            {
                "component": component_name,
                "prime": prime,
                "point": point,
                "row_basis": basis,
                "determinant_mod_p": determinant,
                "row_replacements": len(
                    set(basis) - set(pinned_rows)
                ),
            }
        )
    print(
        f"[INFO] p={prime} {component_name}: "
        f"{len(candidates)} distinct full-rank row bases from {trials} trials",
        flush=True,
    )
    return candidates, rank_profiles


def choose_anchor(base, directions, rows, component_name: str):
    controls = [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (2, 1),
        (1, 2),
        (-1, -1),
        (2, -1),
        (-2, 1),
        (2, 2),
        (-2, -2),
    ]
    attempts = []
    for a_value, b_value in controls:
        matrix = (
            base
            + Rational(a_value) * directions[(0, 1)]
            + Rational(b_value) * directions[(0, 5)]
        ).extract(rows, range(125))
        determinant = matrix.det(method="domain-ge")
        attempts.append(
            {
                "A": a_value,
                "B": b_value,
                "determinant": str(determinant),
            }
        )
        if determinant:
            require(
                True,
                f"{component_name} basis has rational anchor "
                f"{(a_value, b_value, 1)}",
            )
            return (
                Rational(a_value),
                Rational(b_value),
                matrix,
                determinant,
                attempts,
            )
    raise AssertionError(
        f"no deterministic rational anchor for {component_name} basis"
    )


def exact_chart(
    component_name: str,
    candidate: dict[str, object],
    base: Matrix,
    directions,
):
    started = time.time()
    rows = candidate["row_basis"]
    anchor_a, anchor_b, anchor, anchor_det, attempts = choose_anchor(
        base, directions, rows, component_name
    )
    inverse = anchor.inv()
    normalized_a = inverse * directions[(0, 1)].extract(
        rows, range(125)
    )
    normalized_b = inverse * directions[(0, 5)].extract(
        rows, range(125)
    )
    graph = exp119.cyclic_components(normalized_a, normalized_b)
    sizes = [len(component) for component in graph["cyclic"]]
    largest = max(sizes)
    print(
        f"[INFO] {component_name} candidate cyclic SCC sizes {sizes}",
        flush=True,
    )
    require(
        largest <= 60,
        f"{component_name} largest cyclic block is within gate 60",
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
        f"{component_name} determinant is below the expansion gate",
    )
    checks = exp120.direct_checks(
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
    x, coordinate_power, invariant = exp120.invariant_form(original, a, b)
    invariant_poly = Poly(invariant, x, b, domain="QQ")
    require(
        len(invariant_poly.terms()) <= 10000,
        f"{component_name} invariant is below the expansion gate",
    )
    if coordinate_power % 3 == 0:
        zero_locus_invariant = factor(
            x ** (coordinate_power // 3) * invariant
        )
        descent = "exact semi-invariant descent"
    else:
        zero_locus_invariant = factor(x**coordinate_power * invariant**3)
        descent = "mu3 norm with identical zero locus"
    require(
        time.time() - started <= 360,
        f"{component_name} exact determinant meets its six-minute gate",
    )
    return {
        "selection": candidate,
        "anchor": {
            "A": str(anchor_a),
            "B": str(anchor_b),
            "d": "1",
            "determinant": str(anchor_det),
            "attempts": attempts,
        },
        "graph": {
            "cyclic_component_sizes": sizes,
            "largest_cyclic_component": largest,
        },
        "blocks": blocks,
        "largest_block_elapsed_seconds": largest_elapsed,
        "direct_checks": checks,
        "coordinate_A_power": coordinate_power,
        "determinant_total_degree": int(original_poly.total_degree()),
        "determinant_monomial_count": len(original_poly.terms()),
        "determinant_d1_up_to_anchor_scalar": str(original),
        "invariant_degree_X": int(invariant_poly.degree(x)),
        "invariant_degree_B": int(invariant_poly.degree(b)),
        "invariant_monomial_count": len(invariant_poly.terms()),
        "invariant_reduced_X_B": str(invariant),
        "zero_locus_invariant_X_B": str(zero_locus_invariant),
        "descent_method": descent,
        "elapsed_seconds": time.time() - started,
    }, zero_locus_invariant


def ideal_record(component, first_chart, charts, x, b):
    started = time.time()
    basis = groebner(
        [component, first_chart, *charts],
        x,
        b,
        order="grlex",
        domain="QQ",
    )
    elapsed = time.time() - started
    require(elapsed <= 240, "component ideal meets its 240-second gate")
    expressions = [polynomial.as_expr() for polynomial in basis.polys]
    unit = len(expressions) == 1 and expressions[0] == 1
    record: dict[str, object] = {
        "unit_ideal": unit,
        "basis_size": len(expressions),
        "basis": [str(expression) for expression in expressions],
        "elapsed_seconds": elapsed,
    }
    if not unit:
        require(
            basis.is_zero_dimensional,
            "surviving component ideal is zero-dimensional",
        )
        record["zero_dimensional"] = True
    return record


def polynomial_digest(polynomial):
    payload = str(polynomial.monic().as_expr()).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def reduce_mod_quadratic(component, expression, x, b):
    component_x = Poly(component, x)
    require(
        component_x.degree() == 2,
        "split certificate component is quadratic in X",
    )
    leading = QQ.convert(component_x.nth(2))
    require(
        not getattr(leading, "free_symbols", set()),
        "split certificate quadratic has constant leading coefficient",
    )
    middle = Poly(component_x.nth(1), b, domain="QQ")
    constant = Poly(component_x.nth(0), b, domain="QQ")
    expression_x = Poly(expression, x)
    maximum = expression_x.degree()
    x_coefficients = [
        Poly(0, b, domain="QQ"),
        Poly(1, b, domain="QQ"),
    ]
    constants = [
        Poly(1, b, domain="QQ"),
        Poly(0, b, domain="QQ"),
    ]
    for _ in range(2, maximum + 1):
        x_coefficients.append(
            constants[-1]
            - x_coefficients[-1] * middle.mul_ground(1 / leading)
        )
        constants.append(
            -x_coefficients[-2] * constant.mul_ground(1 / leading)
        )
    reduced_x = Poly(0, b, domain="QQ")
    reduced_constant = Poly(0, b, domain="QQ")
    for degree in range(maximum + 1):
        coefficient = Poly(
            expression_x.nth(degree), b, domain="QQ"
        )
        reduced_x += coefficient * x_coefficients[degree]
        reduced_constant += coefficient * constants[degree]
    return (
        leading,
        middle,
        constant,
        reduced_x,
        reduced_constant,
    )


def split_q_ideal_record(component, first_chart, chart, x, b):
    started = time.time()
    first_poly = Poly(first_chart, x, b, domain="QQ")
    b_multiplicity = min(
        b_degree
        for (_, b_degree), _ in first_poly.terms()
    )
    require(
        b_multiplicity > 0,
        "first chart exposes a positive B-coordinate factor",
    )
    quotient_chart = cancel(first_chart / b**b_multiplicity)
    require(
        Poly(
            first_chart - b**b_multiplicity * quotient_chart,
            x,
            b,
            domain="QQ",
        ).is_zero,
        "B-coordinate split reconstructs the first chart exactly",
    )

    q_at_b0 = Poly(component.subs(b, 0), x, domain="QQ")
    chart_at_b0 = Poly(chart.subs(b, 0), x, domain="QQ")
    boundary_gcd = q_at_b0.gcd(chart_at_b0)
    require(
        boundary_gcd.degree() == 0,
        "B=0 branch has an exact unit univariate gcd",
    )

    (
        leading,
        middle,
        constant,
        first_x,
        first_constant,
    ) = reduce_mod_quadratic(component, quotient_chart, x, b)
    (
        chart_leading,
        chart_middle,
        chart_constant,
        chart_x,
        chart_constant_term,
    ) = reduce_mod_quadratic(component, chart, x, b)
    require(
        (
            leading == chart_leading
            and middle == chart_middle
            and constant == chart_constant
        ),
        "both reductions use the same exact quadratic relation",
    )

    exceptional_gcd = first_x.gcd(first_constant)
    require(
        exceptional_gcd.degree() == 0,
        "quotient-chart linear remainder has no exceptional coefficient root",
    )
    component_compatibility = (
        first_constant * first_constant.mul_ground(leading)
        - middle * first_x * first_constant
        + constant * first_x * first_x
    )
    chart_compatibility = (
        first_x * chart_constant_term
        - first_constant * chart_x
    )
    compatibility_gcd = component_compatibility.gcd(
        chart_compatibility
    )
    require(
        compatibility_gcd.degree() == 0,
        "quotient-chart compatibility polynomials have exact unit gcd",
    )
    elapsed = time.time() - started
    require(elapsed <= 240, "component ideal meets its 240-second gate")
    return {
        "unit_ideal": True,
        "method": (
            "exact B-coordinate zero-set split plus quadratic-X "
            "reduction and univariate QQ[B] gcds"
        ),
        "elapsed_seconds": elapsed,
        "B_coordinate_multiplicity": b_multiplicity,
        "B_zero_branch": {
            "component_at_B0": str(q_at_b0.as_expr()),
            "chart_at_B0": str(chart_at_b0.as_expr()),
            "gcd": str(boundary_gcd.monic().as_expr()),
        },
        "quotient_branch": {
            "first_remainder_X_coefficient_degree_B": (
                first_x.degree()
            ),
            "first_remainder_constant_degree_B": (
                first_constant.degree()
            ),
            "chart_remainder_X_coefficient_degree_B": (
                chart_x.degree()
            ),
            "chart_remainder_constant_degree_B": (
                chart_constant_term.degree()
            ),
            "exceptional_coefficient_gcd": str(
                exceptional_gcd.monic().as_expr()
            ),
            "component_compatibility_degree_B": (
                component_compatibility.degree()
            ),
            "component_compatibility_monomial_count": len(
                component_compatibility.terms()
            ),
            "component_compatibility_sha256": polynomial_digest(
                component_compatibility
            ),
            "chart_compatibility_degree_B": (
                chart_compatibility.degree()
            ),
            "chart_compatibility_monomial_count": len(
                chart_compatibility.terms()
            ),
            "chart_compatibility_sha256": polynomial_digest(
                chart_compatibility
            ),
            "compatibility_gcd": str(
                compatibility_gcd.monic().as_expr()
            ),
        },
    }


def main() -> None:
    started = time.time()
    base, directions, pinned_rows = exp115.build_system()
    require(base.shape == (302, 125), "complete system is 302 by 125")
    first_record = json.loads(E119_COMPACT.read_text(encoding="utf-8"))
    exp115_record = json.loads(E115_ARTIFACT.read_text(encoding="utf-8"))
    x, b = symbols("X B")
    first_chart = sympify(
        first_record["alternative_determinant_in_X_B"],
        locals={"X": x, "B": b},
    )
    factor_records = first_record["factor_records"]
    components = exp120.component_generators(x, b)
    first_rows = exp115_record["open_chart"]["witnesses"]["components"][
        "H_linear"
    ]["row_basis"]
    g_rows = exp115_record["open_chart"]["witnesses"]["components"]["G"][
        "row_basis"
    ]
    require(len(first_rows) == 125, "EXP-119 row basis has size 125")

    forbidden_bases = {
        name: {
            tuple(pinned_rows),
            tuple(first_rows),
            tuple(g_rows),
        }
        for name in ("L", "Q")
    }
    selections: dict[str, list[dict[str, object]]] = {"L": [], "Q": []}
    modular_records: dict[str, object] = {}
    for prime in PRIMES:
        base_mod = exp115.matrix_mod(base, prime)
        matrices = (
            base_mod,
            exp115.matrix_mod(directions[(0, 1)], prime),
            exp115.matrix_mod(directions[(0, 5)], prime),
            exp115.matrix_mod(directions[(1, 0)], prime),
        )
        modular_records[str(prime)] = {}
        for name in ("L", "Q"):
            if len(selections[name]) >= MAX_CANDIDATES:
                continue
            points = residual_points(
                name,
                components[name],
                factor_records,
                x,
                b,
                prime,
            )
            candidates, rank_profiles = select_candidates(
                name,
                points,
                prime,
                matrices,
                pinned_rows,
                first_rows,
                forbidden_bases[name],
            )
            selections[name].extend(
                candidates[: MAX_CANDIDATES - len(selections[name])]
            )
            modular_records[str(prime)][name] = {
                "residual_affine_lifts": len(points),
                "tested_rank_profiles_coefficient_augmented": rank_profiles,
                "selected_candidates": candidates,
            }
        if all(
            len(selections[name]) >= MAX_CANDIDATES for name in ("L", "Q")
        ):
            break
    for name in ("L", "Q"):
        require(
            bool(selections[name]),
            f"{name} has a full-rank modular residual-selected basis",
        )

    checkpoint: dict[str, object] = {
        "experiment": "EXP-121",
        "modular_selection": modular_records,
        "exact_charts": {"L": [], "Q": []},
        "component_ideals": {},
    }
    persist(checkpoint)

    exact_charts: dict[str, list[dict[str, object]]] = {"L": [], "Q": []}
    ideal_records: dict[str, object] = {}
    exact_cache = {}
    for name in ("L", "Q"):
        cumulative = []
        for index, candidate in enumerate(selections[name], start=1):
            print(
                f"[INFO] reconstructing exact {name} chart {index}",
                flush=True,
            )
            basis_key = tuple(candidate["row_basis"])
            if basis_key in exact_cache:
                print(
                    f"[INFO] reusing exact determinant already reconstructed "
                    f"for the same {name} row basis",
                    flush=True,
                )
                cached_record, chart = exact_cache[basis_key]
                chart_record = {
                    **cached_record,
                    "selection": candidate,
                    "reused_exact_row_basis": True,
                }
            else:
                chart_record, chart = exact_chart(
                    name, candidate, base, directions
                )
                exact_cache[basis_key] = (chart_record, chart)
            exact_charts[name].append(chart_record)
            cumulative.append(chart)
            if name == "Q" and len(cumulative) == 1:
                ideal = split_q_ideal_record(
                    components[name], first_chart, cumulative[0], x, b
                )
            else:
                ideal = ideal_record(
                    components[name], first_chart, cumulative, x, b
                )
            ideal_records[name] = ideal
            checkpoint["exact_charts"] = exact_charts
            checkpoint["component_ideals"] = ideal_records
            persist(checkpoint)
            print(
                f"[INFO] {name} after chart {index}: "
                f"{'UNIT' if ideal['unit_ideal'] else 'finite residual'}",
                flush=True,
            )
            if ideal["unit_ideal"]:
                break

    all_unit = all(
        ideal_records[name]["unit_ideal"] for name in ("L", "Q")
    )
    total_elapsed = time.time() - started
    require(
        total_elapsed <= TOTAL_GATE_SECONDS,
        "EXP-121 meets its total compute gate",
    )
    artifact = {
        "experiment": "EXP-121",
        "modular_selection": modular_records,
        "exact_charts": exact_charts,
        "component_ideals": ideal_records,
        "predictions": {
            "both_components_have_modular_full_rank_points": all(
                bool(selections[name]) for name in ("L", "Q")
            ),
            "all_selected_bases_at_most_ten_replacements": all(
                candidate["row_replacements"] <= 10
                for values in selections.values()
                for candidate in values
            ),
            "all_exact_charts_largest_scc_at_most_60": all(
                chart["graph"]["largest_cyclic_component"] <= 60
                for values in exact_charts.values()
                for chart in values
            ),
            "at_least_one_component_closed_by_first_new_chart": any(
                records
                and ideal_records[name]["unit_ideal"]
                and len(records) == 1
                for name, records in exact_charts.items()
            ),
            "both_L_Q_component_ideals_unit": all_unit,
        },
        "elapsed_seconds": total_elapsed,
        "scope": (
            "Exact finite chart cover on the L/Q components of the d!=0 "
            "three-parameter TB restriction. Even a complete L/Q closure "
            "does not close the 24-parameter core, the full 51-parameter "
            "family, (72,108), the degree floor, or JC(2)."
        ),
    }
    payload = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"[INFO] elapsed {total_elapsed:.2f} s", flush=True)
    print(
        "RESULT: COMPLETE"
        if all_unit
        else "RESULT: COMPLETE WITH FINITE RESIDUAL",
        flush=True,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"RESULT: FAILED: {error}", file=sys.stderr, flush=True)
        raise
