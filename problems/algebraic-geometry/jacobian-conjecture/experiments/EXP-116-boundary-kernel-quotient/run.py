"""EXP-116: quotient the structural P-kernel on the d=0 boundary."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

from sympy import Matrix, Poly, Rational, factor, symbols


HERE = Path(__file__).resolve().parent
E115_PATH = HERE.parent / "EXP-115-weighted-residual-component-gate" / "run.py"
ARTIFACT = HERE / "artifacts" / "results.json"

spec = importlib.util.spec_from_file_location("exp115", E115_PATH)
exp115 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp115)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def build_quotient():
    base, directions, _ = exp115.build_system()
    q_labels = [
        label
        for label in exp115.exp112.exp071.NQ
        if label != (0, 0)
    ]
    removed = q_labels.index((0, 8))
    require(removed == 7, "the fixed kernel coordinate is the y^8 Q-column")

    boundary_base = base - directions[(1, 0)]
    keep_columns = [
        column for column in range(125) if column != removed
    ]
    quotient_origin = boundary_base[:, keep_columns]
    quotient_a = directions[(0, 1)][:, keep_columns]
    quotient_b = directions[(0, 5)][:, keep_columns]
    quotient_anchor = quotient_origin + quotient_b

    _, row_pivots = quotient_anchor.T.rref()
    selected_rows = list(row_pivots)
    require(
        quotient_origin.shape == (302, 124),
        "quotient augmented matrix has shape 302 by 124",
    )
    require(
        len(selected_rows) == 124,
        "quotient matrix has exact rank 124 at anchor (a,b)=(0,1)",
    )

    selected_base = quotient_anchor[selected_rows, :]
    selected_a = quotient_a[selected_rows, :]
    selected_b = quotient_b[selected_rows, :]
    inverse = selected_base.inv()
    normalized_a = inverse * selected_a
    normalized_b = inverse * selected_b
    return {
        "base": base,
        "directions": directions,
        "quotient_origin": quotient_origin,
        "quotient_anchor": quotient_anchor,
        "quotient_a": quotient_a,
        "quotient_b": quotient_b,
        "selected_rows": selected_rows,
        "selected_base": selected_base,
        "normalized_a": normalized_a,
        "normalized_b": normalized_b,
        "removed_column": removed,
        "removed_label": q_labels[removed],
    }


def kernel_recheck(system) -> None:
    base = system["base"]
    directions = system["directions"]
    boundary_base = base - directions[(1, 0)]
    k0 = Matrix.zeros(125, 1)
    for index, value in {
        7: 1,
        20: -8,
        34: 28,
        47: -56,
        59: 70,
        70: -56,
        80: 28,
        89: -8,
        97: 1,
    }.items():
        k0[index] = value
    ea = Matrix.zeros(125, 1)
    eb = Matrix.zeros(125, 1)
    ea[0] = 1
    eb[4] = 1
    da = directions[(0, 1)]
    db = directions[(0, 5)]
    checks = (
        boundary_base * k0,
        boundary_base * ea + da * k0,
        boundary_base * eb + db * k0,
        da * ea,
        da * eb + db * ea,
        db * eb,
    )
    require(
        all(all(value == 0 for value in vector) for vector in checks),
        "EXP-115 polynomial P-kernel rechecks coefficientwise",
    )


def block_determinant(system):
    normalized = [system["normalized_a"], system["normalized_b"]]
    adjacency, edge_parameters, nonzero_counts, graph_digest = exp115.exp112.graph_from_matrices(
        normalized
    )
    edge_count = len(edge_parameters)
    components = exp115.exp112.strongly_connected_components(adjacency)
    components = sorted(components, key=lambda component: (-len(component), component))
    a, s = symbols("a s")
    cyclic_records = []
    cyclic_components = []
    determinant = Rational(1)

    for component in components:
        block_a = normalized[0].extract(component, component)
        block_b = normalized[1].extract(component, component)
        has_loop = any(
            block_a[index, index] != 0 or block_b[index, index] != 0
            for index in range(len(component))
        )
        if len(component) == 1 and not has_loop:
            continue
        cyclic_components.append(component)
    largest_cyclic = max(len(component) for component in cyclic_components)
    if largest_cyclic > 36:
        print(
            f"[STOP] largest cyclic block is {largest_cyclic}, "
            "above the declared determinant gate 36",
            flush=True,
        )
        return {
            "a": a,
            "s": s,
            "components": components,
            "edge_count": edge_count,
            "direction_nonzero_counts": nonzero_counts,
            "graph_sha256": graph_digest,
            "cyclic_records": [
                {
                    "size": len(component),
                    "columns": component,
                    "factor": None,
                    "stopped_before_determinant": len(component) > 36,
                }
                for component in cyclic_components
            ],
            "determinant": None,
            "stopped": True,
            "stop_reason": (
                f"largest cyclic block {largest_cyclic} exceeds gate 36"
            ),
        }

    for component in cyclic_components:
        block_a = normalized[0].extract(component, component)
        block_b = normalized[1].extract(component, component)
        block = (
            Matrix.eye(len(component))
            + a * block_a
            + s * block_b
        )
        block_started = time.time()
        block_factor = factor(block.det(method="domain-ge"))
        elapsed = time.time() - block_started
        determinant = factor(determinant * block_factor)
        polynomial = Poly(block_factor, a, s, domain="QQ")
        cyclic_records.append(
            {
                "size": len(component),
                "columns": component,
                "factor": str(block_factor),
                "total_degree": polynomial.total_degree(),
                "monomial_count": len(polynomial.terms()),
                "elapsed_seconds": elapsed,
            }
        )
        print(
            f"[INFO] cyclic block {len(component)}: "
            f"degree {polynomial.total_degree()}, "
            f"{len(polynomial.terms())} monomials, {elapsed:.2f} s",
            flush=True,
        )

    return {
        "a": a,
        "s": s,
        "components": components,
        "edge_count": edge_count,
        "direction_nonzero_counts": nonzero_counts,
        "graph_sha256": graph_digest,
        "cyclic_records": cyclic_records,
        "determinant": factor(determinant),
        "stopped": False,
        "stop_reason": None,
    }


def direct_checks(system, block_result):
    a = block_result["a"]
    s = block_result["s"]
    determinant = block_result["determinant"]
    normalized_a = system["normalized_a"]
    normalized_b = system["normalized_b"]
    points = (
        (0, 0),
        (0, 1),
        (1, 0),
        (-9, Rational(12, 5)),
        (2, -3),
    )
    checks = []
    for av, bv in points:
        shifted_b = Rational(bv) - 1
        symbolic = Rational(determinant.subs({a: av, s: shifted_b}))
        direct = (
            Matrix.eye(124)
            + Rational(av) * normalized_a
            + shifted_b * normalized_b
        ).det(method="domain-ge")
        require(
            symbolic == direct,
            f"block determinant matches direct exact determinant at {(av, bv)}",
        )
        checks.append(
            {
                "point": [str(av), str(bv)],
                "value": str(symbolic),
            }
        )
    return checks


def rank_profiles(system):
    quotient_origin = system["quotient_origin"]
    quotient_a = system["quotient_a"]
    quotient_b = system["quotient_b"]
    profiles = {}
    for name, (a, b) in {
        "boundary_a_zero": (Fraction(0), Fraction(1)),
        "boundary_b_zero": (Fraction(1), Fraction(0)),
        "boundary_relation": (Fraction(-9), Fraction(12, 5)),
    }.items():
        augmented = (
            quotient_origin
            + Rational(a.numerator, a.denominator) * quotient_a
            + Rational(b.numerator, b.denominator) * quotient_b
        )
        coefficient = augmented[:, :123]
        augmented_nullity = len(augmented.nullspace())
        coefficient_nullity = len(coefficient.nullspace())
        require(
            augmented_nullity == 0,
            f"{name} quotient augmented rank is exactly 124",
        )
        require(
            coefficient_nullity == 0,
            f"{name} quotient coefficient rank is exactly 123",
        )
        profiles[name] = {
            "point": {"a": str(a), "b": str(b), "d": "0"},
            "coefficient_rank": 123,
            "augmented_rank": 124,
            "inconsistent": True,
        }
    return profiles


def main() -> None:
    started = time.time()
    system = build_quotient()
    kernel_recheck(system)
    origin_augmented_nullity = len(system["quotient_origin"].nullspace())
    origin_coefficient_nullity = len(
        system["quotient_origin"][:, :123].nullspace()
    )
    require(
        origin_augmented_nullity == 11,
        "quotient origin has exact augmented rank 113",
    )
    require(
        origin_coefficient_nullity == 11,
        "quotient origin has exact coefficient rank 112",
    )
    block_result = block_determinant(system)
    largest = max(len(component) for component in block_result["components"])
    require(
        largest < 124,
        "quotient dependency graph has a proper largest SCC",
    )
    profiles = rank_profiles(system)
    checks = []
    determinant = block_result["determinant"]
    constant_nonzero = False
    polynomial = None
    if not block_result["stopped"]:
        checks = direct_checks(system, block_result)
        constant_nonzero = determinant != 0 and not determinant.free_symbols
        print(
            f"[{'PASS' if constant_nonzero else 'REFUTED'}] "
            "prediction: first quotient determinant is constant nonzero",
            flush=True,
        )
        polynomial = Poly(
            determinant, block_result["a"], block_result["s"], domain="QQ"
        )

    artifact = {
        "experiment": "EXP-116",
        "quotient_shape": [302, 124],
        "removed_column": system["removed_column"],
        "removed_monomial": list(system["removed_label"]),
        "selected_rows": system["selected_rows"],
        "graph": {
            "edge_count": block_result["edge_count"],
            "direction_nonzero_counts": block_result[
                "direction_nonzero_counts"
            ],
            "graph_sha256": block_result["graph_sha256"],
            "component_sizes": [
                len(component) for component in block_result["components"]
            ],
            "cyclic_blocks": block_result["cyclic_records"],
        },
        "normalized_determinant": (
            str(determinant) if determinant is not None else None
        ),
        "normalized_coordinates": "a, s=b-1 around anchor (0,1)",
        "determinant_total_degree": (
            polynomial.total_degree() if polynomial is not None else None
        ),
        "determinant_monomial_count": (
            len(polynomial.terms()) if polynomial is not None else None
        ),
        "determinant_stopped": block_result["stopped"],
        "stop_reason": block_result["stop_reason"],
        "direct_checks": checks,
        "exact_rank_profiles": profiles,
        "origin_rank_profile": {
            "point": {"a": "0", "b": "0", "d": "0"},
            "coefficient_rank": 112,
            "augmented_rank": 113,
            "inconsistent": True,
        },
        "predictions": {
            "quotient_rank_124_at_origin": False,
            "origin_prediction_refuted": True,
            "quotient_rank_124_at_anchor_0_1": True,
            "proper_scc_compression": largest < 124,
            "largest_core_at_most_24": largest <= 24,
            "constant_nonzero_first_chart": constant_nonzero,
        },
        "elapsed_seconds": time.time() - started,
        "scope": (
            "One quotient chart on the d=0 TB plane; any determinant zero "
            "locus still requires alternative 124-column charts."
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
