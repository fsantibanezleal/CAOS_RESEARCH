"""EXP-117: exact determinant factors of the 51-core boundary quotient chart."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

from sympy import Matrix, Poly, Rational, factor, factor_list, symbols


HERE = Path(__file__).resolve().parent
E116_PATH = HERE.parent / "EXP-116-boundary-kernel-quotient" / "run.py"
ARTIFACT = HERE / "artifacts" / "results.json"

spec = importlib.util.spec_from_file_location("exp116", E116_PATH)
exp116 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp116)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def multiplicity_at_minus_one(expression, variable) -> int:
    polynomial = Poly(expression, variable, domain="QQ")
    divisor = Poly(variable + 1, variable, domain="QQ")
    multiplicity = 0
    while polynomial.degree() >= 1:
        quotient, remainder = polynomial.div(divisor)
        if not remainder.is_zero:
            break
        multiplicity += 1
        polynomial = quotient
    return multiplicity


def factor_record(expression, a, s) -> dict[str, object]:
    polynomial = Poly(expression, a, s, domain="QQ")
    coefficient, factors = factor_list(expression, a, s)
    axis = factor(expression.subs(a, 0))
    return {
        "expression": str(expression),
        "total_degree": int(polynomial.total_degree()),
        "monomial_count": len(polynomial.terms()),
        "factor_coefficient": str(coefficient),
        "factors": [
            {
                "expression": str(factor_expression),
                "multiplicity": int(multiplicity),
                "total_degree": int(Poly(
                    factor_expression, a, s, domain="QQ"
                ).total_degree()),
                "monomial_count": len(
                    Poly(factor_expression, a, s, domain="QQ").terms()
                ),
            }
            for factor_expression, multiplicity in factors
        ],
        "axis_a_zero": str(axis),
        "origin_b_zero_multiplicity": multiplicity_at_minus_one(axis, s),
    }


def main() -> None:
    started = time.time()
    system = exp116.build_quotient()
    exp116.kernel_recheck(system)
    normalized = [system["normalized_a"], system["normalized_b"]]
    adjacency, edge_parameters, nonzero_counts, graph_digest = (
        exp116.exp115.exp112.graph_from_matrices(normalized)
    )
    components = exp116.exp115.exp112.strongly_connected_components(
        adjacency
    )
    components = sorted(
        components, key=lambda component: (-len(component), component)
    )
    component_sizes = [len(component) for component in components]
    require(
        component_sizes[:6] == [51, 11, 10, 9, 8, 7],
        "quotient SCC sizes reproduce EXP-116",
    )

    a, s = symbols("a s")
    records = []
    block_expressions = []
    total_degree = 0
    total_origin_multiplicity = 0
    largest_elapsed = None

    for component in components:
        block_a = normalized[0].extract(component, component)
        block_s = normalized[1].extract(component, component)
        has_loop = any(
            block_a[index, index] != 0 or block_s[index, index] != 0
            for index in range(len(component))
        )
        if len(component) == 1 and not has_loop:
            continue
        block = (
            Matrix.eye(len(component))
            + a * block_a
            + s * block_s
        )
        block_started = time.time()
        determinant = factor(block.det(method="domain-ge"))
        elapsed = time.time() - block_started
        if len(component) == 51:
            largest_elapsed = elapsed
            require(
                elapsed <= 300,
                "51-core determinant completes inside its 300-second budget",
            )
        record = factor_record(determinant, a, s)
        record.update(
            {
                "size": int(len(component)),
                "columns": [int(column) for column in component],
                "elapsed_seconds": elapsed,
            }
        )
        require(
            Rational(determinant.subs({a: 0, s: 0})) == 1,
            f"block {len(component)} is normalized to one at the anchor",
        )
        records.append(record)
        block_expressions.append(determinant)
        total_degree += record["total_degree"]
        total_origin_multiplicity += record[
            "origin_b_zero_multiplicity"
        ]
        print(
            f"[INFO] block {len(component)}: "
            f"degree {record['total_degree']}, "
            f"{record['monomial_count']} monomials, "
            f"{len(record['factors'])} factor records, {elapsed:.2f} s",
            flush=True,
        )

    points = (
        (0, 0),
        (0, -1),
        (1, -1),
        (-9, Rational(7, 5)),
        (2, -4),
    )
    checks = []
    for av, sv in points:
        factored_value = Rational(1)
        for expression in block_expressions:
            factored_value *= Rational(
                expression.subs({a: av, s: sv})
            )
        direct = (
            Matrix.eye(124)
            + Rational(av) * normalized[0]
            + Rational(sv) * normalized[1]
        ).det(method="domain-ge")
        require(
            factored_value == direct,
            f"block product matches direct quotient determinant at {(av, sv)}",
        )
        checks.append(
            {
                "point_shifted": {"a": str(av), "s": str(sv)},
                "point_original": {
                    "a": str(av),
                    "b": str(Rational(sv) + 1),
                },
                "value": str(direct),
            }
        )

    nontrivial_refactor = any(
        len(record["factors"]) > 1
        or any(
            factor_entry["multiplicity"] > 1
            for factor_entry in record["factors"]
        )
        for record in records
        if record["size"] > 1
    )
    print(
        f"[{'PASS' if nontrivial_refactor else 'REFUTED'}] "
        "prediction: a nontrivial SCC block factors further",
        flush=True,
    )
    require(
        total_origin_multiplicity > 0,
        "the a=0 axis exposes a positive b=s+1 multiplicity at the origin",
    )

    artifact = {
        "experiment": "EXP-117",
        "coordinates": {"a": "a", "s": "b-1"},
        "graph": {
            "component_sizes": component_sizes,
            "edge_count": len(edge_parameters),
            "direction_nonzero_counts": nonzero_counts,
            "sha256": graph_digest,
        },
        "block_factors": records,
        "combined_total_degree": total_degree,
        "combined_origin_b_zero_multiplicity": total_origin_multiplicity,
        "direct_checks": checks,
        "predictions": {
            "largest_block_within_300_seconds": largest_elapsed is not None
            and largest_elapsed <= 300,
            "largest_block_degree_below_51": records[0]["total_degree"] < 51,
            "largest_block_at_most_200_monomials": records[0][
                "monomial_count"
            ]
            <= 200,
            "nontrivial_block_refactor": nontrivial_refactor,
            "positive_origin_axis_multiplicity": total_origin_multiplicity
            > 0,
            "all_direct_checks_match": True,
        },
        "elapsed_seconds": time.time() - started,
        "scope": (
            "Selected 124-column quotient chart on the d=0 TB plane; "
            "the exact factor locus requires alternative quotient charts."
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
