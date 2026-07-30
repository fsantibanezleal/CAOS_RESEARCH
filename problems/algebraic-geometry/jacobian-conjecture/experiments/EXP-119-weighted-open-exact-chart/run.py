"""EXP-119: exact weighted-open alternative chart and component intersections.

CPU-only. All promoted determinants, factors, and resultants use exact QQ
arithmetic. Finite-field data are reproduced only as an adversarial control.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from collections import deque
from pathlib import Path

from sympy import (
    Matrix,
    Poly,
    Rational,
    factor,
    factor_list,
    resultant,
    symbols,
)


HERE = Path(__file__).resolve().parent
E115_PATH = (
    HERE.parent / "EXP-115-weighted-residual-component-gate" / "run.py"
)
E115_ARTIFACT = (
    HERE.parent
    / "EXP-115-weighted-residual-component-gate"
    / "artifacts"
    / "results.json"
)
ARTIFACT = HERE / "artifacts" / "results.json"

spec = importlib.util.spec_from_file_location("exp115", E115_PATH)
exp115 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp115)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def covariance_weights(matrices) -> dict[str, object]:
    row_count, column_count = matrices[0][0].shape
    node_count = row_count + column_count
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(node_count)
    ]
    records: list[tuple[int, int, int]] = []
    support_counts = {}
    for matrix, weight, label in matrices:
        count = 0
        for row in range(row_count):
            for column in range(column_count):
                if matrix[row, column] == 0:
                    continue
                count += 1
                column_node = row_count + column
                adjacency[row].append((column_node, weight))
                adjacency[column_node].append((row, -weight))
                records.append((row, column, weight))
        support_counts[label] = count

    potentials: list[int | None] = [None] * node_count
    components = []
    for root in range(node_count):
        if potentials[root] is not None:
            continue
        potentials[root] = 0
        queue = deque([root])
        component = []
        while queue:
            node = queue.popleft()
            component.append(node)
            for neighbor, difference in adjacency[node]:
                candidate = potentials[node] - difference
                if potentials[neighbor] is None:
                    potentials[neighbor] = candidate
                    queue.append(neighbor)
                elif potentials[neighbor] != candidate:
                    raise AssertionError(
                        "full weighted support covariance is inconsistent"
                    )
        components.append(component)

    row_weights = [int(potentials[index]) for index in range(row_count)]
    column_weights = [
        -int(potentials[row_count + index])
        for index in range(column_count)
    ]
    require(
        all(
            row_weights[row] + column_weights[column] == weight
            for row, column, weight in records
        ),
        "all full-system support weights recheck exactly",
    )
    digest_payload = json.dumps(
        {
            "row_weights": row_weights,
            "column_weights": column_weights,
            "support_counts": support_counts,
        },
        sort_keys=True,
    ).encode("utf-8")
    return {
        "row_weights": row_weights,
        "column_weights": column_weights,
        "support_counts": support_counts,
        "component_sizes": sorted(
            (len(component) for component in components), reverse=True
        ),
        "sha256": hashlib.sha256(digest_payload).hexdigest().upper(),
    }


def determinant_weight(rows, covariance) -> int:
    return sum(
        covariance["row_weights"][row] for row in rows
    ) + sum(covariance["column_weights"])


def cyclic_components(normalized_a, normalized_b):
    adjacency, edge_parameters, nonzero_counts, digest = (
        exp115.exp112.graph_from_matrices(
            [normalized_a, normalized_b]
        )
    )
    components = exp115.exp112.strongly_connected_components(adjacency)
    components = sorted(
        components, key=lambda component: (-len(component), component)
    )
    cyclic = []
    for component in components:
        block_a = normalized_a.extract(component, component)
        block_b = normalized_b.extract(component, component)
        has_loop = any(
            block_a[index, index] != 0 or block_b[index, index] != 0
            for index in range(len(component))
        )
        if len(component) > 1 or has_loop:
            cyclic.append(component)
    return {
        "all": components,
        "cyclic": cyclic,
        "edge_count": len(edge_parameters),
        "direction_nonzero_counts": nonzero_counts,
        "sha256": digest,
    }


def compute_blocks(normalized_a, normalized_b, graph):
    a, s = symbols("A s")
    records = []
    expressions = []
    largest_started = None
    for component in graph["cyclic"]:
        size = len(component)
        block = (
            Matrix.eye(size)
            + a * normalized_a.extract(component, component)
            + s * normalized_b.extract(component, component)
        )
        started = time.time()
        determinant = factor(block.det(method="domain-ge"))
        elapsed = time.time() - started
        if size == max(len(item) for item in graph["cyclic"]):
            largest_started = elapsed
        if elapsed > 240:
            raise TimeoutError(
                f"cyclic block {size} exceeded its 240-second budget"
            )
        polynomial = Poly(determinant, a, s, domain="QQ")
        coefficient, factors = factor_list(determinant, a, s)
        record = {
            "size": size,
            "columns": component,
            "expression": str(determinant),
            "total_degree": int(polynomial.total_degree()),
            "monomial_count": len(polynomial.terms()),
            "factor_coefficient": str(coefficient),
            "factors": [
                {
                    "expression": str(expression),
                    "multiplicity": int(multiplicity),
                }
                for expression, multiplicity in factors
            ],
            "elapsed_seconds": elapsed,
        }
        records.append(record)
        expressions.append(determinant)
        require(
            determinant.subs({a: 0, s: 0}) == 1,
            f"cyclic block {size} is normalized at the rational anchor",
        )
        print(
            f"[INFO] block {size}: degree {polynomial.total_degree()}, "
            f"{len(polynomial.terms())} monomials, {elapsed:.2f} s",
            flush=True,
        )
    return a, s, records, expressions, largest_started


def weighted_support_check(polynomial, weight: int, a, b) -> dict[str, object]:
    records = []
    for (a_degree, b_degree), coefficient in polynomial.terms():
        remainder = weight - 7 * a_degree - 3 * b_degree
        require(
            remainder >= 0 and remainder % 9 == 0,
            "alternative determinant monomial lifts to nonnegative d-degree",
        )
        d_degree = remainder // 9
        require(
            a_degree + b_degree + d_degree <= 125,
            "alternative determinant monomial respects determinant degree",
        )
        records.append(
            {
                "a": int(a_degree),
                "b": int(b_degree),
                "d": int(d_degree),
                "coefficient": str(coefficient),
            }
        )
    return {
        "weighted_degree": weight,
        "lifted_support": records,
        "monomial_count": len(records),
    }


def component_resultants(alternative, a, b):
    x, source_b, g, _, linear, quadratic, _ = (
        exp115.residue_polynomials()
    )
    components = {
        "G": g.subs({x: a**3, source_b: b}),
        "L": linear.subs({x: a**3, source_b: b}),
        "Q": quadratic.subs({x: a**3, source_b: b}),
    }
    results = {}
    for name, component in components.items():
        started = time.time()
        common = Poly(component, a, b, domain="QQ").gcd(
            Poly(alternative, a, b, domain="QQ")
        )
        require(
            common.total_degree() == 0,
            f"{name} shares no component with the alternative chart",
        )
        elimination = factor(resultant(component, alternative, a))
        elapsed = time.time() - started
        elimination_poly = Poly(elimination, b, domain="QQ")
        covered = elimination_poly.degree() == 0
        results[name] = {
            "component": str(component),
            "gcd": str(common.as_expr()),
            "resultant_eliminate_A": str(elimination),
            "resultant_degree_B": int(elimination_poly.degree()),
            "resultant_monomial_count": len(elimination_poly.terms()),
            "covered_by_two_charts": covered,
            "elapsed_seconds": elapsed,
        }
        print(
            f"[INFO] component {name}: resultant degree "
            f"{elimination_poly.degree()} in B, {elapsed:.2f} s",
            flush=True,
        )
    return results


def direct_checks(
    base,
    directions,
    rows,
    anchor_determinant,
    block_expressions,
    a,
    s,
):
    points = (
        (Rational(0), Rational(-4, 5)),
        (Rational(1), Rational(0)),
        (Rational(0), Rational(0)),
        (Rational(2), Rational(-1)),
        (Rational(-1), Rational(3, 2)),
    )
    checks = []
    for av, bv in points:
        normalized_value = Rational(1)
        for expression in block_expressions:
            normalized_value *= expression.subs(
                {a: av, s: bv + Rational(4, 5)}
            )
        predicted = anchor_determinant * normalized_value
        evaluated = (
            base
            + av * directions[(0, 1)]
            + bv * directions[(0, 5)]
        )
        direct = evaluated.extract(rows, range(125)).det(
            method="domain-ge"
        )
        require(
            predicted == direct,
            f"block product matches direct exact determinant at {(av, bv)}",
        )
        checks.append(
            {
                "point": {"A": str(av), "B": str(bv), "d": "1"},
                "determinant": str(direct),
            }
        )
    return checks


def modular_recheck(base, directions, rows) -> dict[str, object]:
    prime = 1009
    evaluated = exp115.combine_mod(
        exp115.matrix_mod(base, prime),
        exp115.matrix_mod(directions[(0, 1)], prime),
        exp115.matrix_mod(directions[(0, 5)], prime),
        exp115.matrix_mod(directions[(1, 0)], prime),
        0,
        201,
        1,
        prime,
    )
    determinant = exp115.determinant_mod(evaluated, rows, prime)
    require(
        determinant == 768,
        "EXP-115 H-linear modular determinant reproduces at p=1009",
    )
    return {
        "prime": prime,
        "point": {"A": 0, "B": 201, "d": 1},
        "determinant": determinant,
    }


def main() -> None:
    started = time.time()
    base, directions, pinned_rows = exp115.build_system()
    weighted_origin = base - directions[(1, 0)]
    covariance = covariance_weights(
        (
            (weighted_origin, 0, "origin_d0"),
            (directions[(0, 1)], 7, "a"),
            (directions[(0, 5)], 3, "b"),
            (directions[(1, 0)], 9, "d"),
        )
    )
    require(
        all(
            covariance["support_counts"][label] > 0
            for label in ("origin_d0", "a", "b", "d")
        ),
        "complete augmented system carries (7,3,9) covariance",
    )

    exp115_record = json.loads(E115_ARTIFACT.read_text(encoding="utf-8"))
    rows = exp115_record["open_chart"]["witnesses"]["components"][
        "H_linear"
    ]["row_basis"]
    require(len(rows) == 125, "persisted H-linear row basis has size 125")
    modular_control = modular_recheck(base, directions, rows)

    anchor = base - Rational(4, 5) * directions[(0, 5)]
    selected_anchor = anchor.extract(rows, range(125))
    anchor_determinant = selected_anchor.det(method="domain-ge")
    require(
        anchor_determinant != 0,
        "persisted H-linear basis is exactly nonzero at (0,-4/5,1)",
    )
    inverse = selected_anchor.inv()
    normalized_a = inverse * directions[(0, 1)].extract(
        rows, range(125)
    )
    normalized_b = inverse * directions[(0, 5)].extract(
        rows, range(125)
    )
    graph = cyclic_components(normalized_a, normalized_b)
    largest = max(len(component) for component in graph["cyclic"])
    print(
        f"[INFO] cyclic SCC sizes "
        f"{[len(component) for component in graph['cyclic']]}",
        flush=True,
    )
    require(
        largest <= 60,
        "largest cyclic block is within the declared 60-column gate",
    )

    a, s, block_records, block_expressions, largest_elapsed = (
        compute_blocks(normalized_a, normalized_b, graph)
    )
    b = symbols("B")
    normalized_product = Rational(1)
    for expression in block_expressions:
        normalized_product *= expression
    original_product = factor(
        normalized_product.subs(s, b + Rational(4, 5))
    )
    original_polynomial = Poly(original_product, a, b, domain="QQ")
    require(
        len(original_polynomial.terms()) <= 10000,
        "alternative determinant stays below the 10000-monomial gate",
    )
    weight = determinant_weight(rows, covariance)
    support = weighted_support_check(
        original_polynomial, weight, a, b
    )
    direct = direct_checks(
        base,
        directions,
        rows,
        anchor_determinant,
        block_expressions,
        a,
        s,
    )
    component_records = component_resultants(
        original_product, a, b
    )
    all_covered = all(
        record["covered_by_two_charts"]
        for record in component_records.values()
    )

    artifact = {
        "experiment": "EXP-119",
        "covariance": covariance,
        "row_basis": rows,
        "pinned_rows": pinned_rows,
        "anchor": {
            "point": {"A": "0", "B": "-4/5", "d": "1"},
            "determinant": str(anchor_determinant),
        },
        "modular_control": modular_control,
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
        "blocks": block_records,
        "normalized_coordinates": "A, s=B+4/5 at d=1",
        "normalized_alternative_determinant": str(normalized_product),
        "alternative_determinant_d1_up_to_anchor_scalar": str(
            original_product
        ),
        "alternative_determinant_total_degree": int(
            original_polynomial.total_degree()
        ),
        "alternative_determinant_monomial_count": len(
            original_polynomial.terms()
        ),
        "weighted_support": support,
        "direct_checks": direct,
        "component_intersections": component_records,
        "predictions": {
            "full_weighted_covariance": True,
            "largest_cyclic_block_at_most_60": largest <= 60,
            "determinant_at_most_500_monomials": len(
                original_polynomial.terms()
            )
            <= 500,
            "all_three_components_covered": all_covered,
        },
        "largest_block_elapsed_seconds": largest_elapsed,
        "elapsed_seconds": time.time() - started,
        "scope": (
            "Exact alternative chart on d=1 in the TB restriction. "
            "Any nonconstant component resultants are the remaining proper "
            "intersections; broader GGHV and JC(2) claims remain open."
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
