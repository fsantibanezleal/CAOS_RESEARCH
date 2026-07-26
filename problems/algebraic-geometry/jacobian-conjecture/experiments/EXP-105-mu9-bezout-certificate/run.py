"""EXP-105: exact mu_9 grading and Bezout certificate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from math import lcm
from pathlib import Path

from sympy import Poly, QQ, ZZ, gcdex, symbols
from sympy.polys.polyfuncs import interpolate


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
EXP103_DIR = ROOT.parent / "EXP-103-residual-curve-determinantal-divisor"
EXP103_RUN = EXP103_DIR / "run.py"
EXP103_ARTIFACT = EXP103_DIR / "artifacts" / "results.json"
EXP104_RUN = ROOT.parent / "EXP-104-exact-valuation-interpolation" / "run.py"
EXP104_ARTIFACT = (
    ROOT.parent
    / "EXP-104-exact-valuation-interpolation"
    / "artifacts"
    / "results.json"
)
z = symbols("z")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def grading_certificate(exp103, coefficient_matrices, row_indices):
    selected = tuple(matrix[row_indices, :] for matrix in coefficient_matrices)
    size = selected[0].shape[0]
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(2 * size)]
    equation_count = 0
    for row in range(size):
        for column in range(size):
            residues = []
            for exponent, matrix in zip(exp103.EXPONENTS, selected):
                if matrix[row, column] != 0:
                    residues.append(exponent % 9)
            if len(set(residues)) > 1:
                raise AssertionError(
                    "a matrix entry occupies multiple exponent residues modulo 9"
                )
            if not residues:
                continue
            residue = residues[0]
            adjacency[row].append((size + column, residue))
            adjacency[size + column].append((row, residue))
            equation_count += 1

    weights: list[int | None] = [None] * (2 * size)
    components = 0
    for root in range(2 * size):
        if weights[root] is not None:
            continue
        components += 1
        weights[root] = 0
        stack = [root]
        while stack:
            source = stack.pop()
            for target, residue in adjacency[source]:
                expected = (residue - int(weights[source])) % 9
                if weights[target] is None:
                    weights[target] = expected
                    stack.append(target)
                else:
                    if weights[target] != expected:
                        raise AssertionError(
                            "the row/column grading equations are inconsistent"
                        )

    row_weights = [int(value) for value in weights[:size]]
    column_weights = [int(value) for value in weights[size:]]
    determinant_residue = (sum(row_weights) + sum(column_weights)) % 9
    return {
        "row_weights": row_weights,
        "column_weights": column_weights,
        "determinant_residue": determinant_residue,
        "support_equations": equation_count,
        "components": components,
    }


def coefficients_low_to_high(poly: Poly) -> list[int]:
    return [int(poly.nth(index)) for index in range(poly.degree() + 1)]


def main() -> None:
    started = time.time()
    exp103 = load_module("exp103_for_exp105", EXP103_RUN)
    exp104 = load_module("exp104_for_exp105", EXP104_RUN)
    source = exp103.load_module("exp099_for_exp105", exp103.EXP099_RUN)
    coefficient_matrices, row_labels, _ = exp103.build_polynomial_matrix(source)
    first_rows = exp103.checkpoint_row_indices(row_labels)

    exp103_result = json.loads(EXP103_ARTIFACT.read_text(encoding="utf-8"))
    safe_chart = next(
        chart
        for chart in exp103_result["prime_runs"][0]["charts"]
        if chart["name"] == "pivot-u2"
    )
    second_rows = safe_chart["row_indices"]
    min_bound, max_bound = exp103.assignment_bounds(
        coefficient_matrices, second_rows
    )
    require(
        (min_bound, max_bound) == (777, 903),
        "the endpoint-safe chart bounds reconstruct as [777,903]",
    )

    first_grading = grading_certificate(
        exp103, coefficient_matrices, first_rows
    )
    second_grading = grading_certificate(
        exp103, coefficient_matrices, second_rows
    )
    require(
        first_grading["determinant_residue"] == 1628 % 9,
        "the first chart grading predicts residue 8 modulo 9",
    )
    require(
        second_grading["determinant_residue"] == min_bound % 9 == max_bound % 9,
        "the second chart grading predicts residue 3 modulo 9",
    )

    exp104_result = json.loads(EXP104_ARTIFACT.read_text(encoding="utf-8"))
    first_coefficients = exp104_result["exact_normalized_coefficients"]
    first_in_z = Poly(
        sum(first_coefficients[9 * index] * z**index for index in range(3)),
        z,
        domain=ZZ,
    )
    first_content, first_primitive = first_in_z.primitive()
    require(
        first_primitive == Poly(21 - 96 * z - 1024 * z**2, z, domain=ZZ),
        "the first primitive determinant is 21-96z-1024z^2",
    )

    selected_exact = exp104.exact_selected_matrices(
        exp103, coefficient_matrices, second_rows
    )
    points = []
    value_hash = hashlib.sha256()
    determinant_started = time.time()
    for node in range(1, 16):
        determinant = exp104.exact_determinant(selected_exact, node)
        monomial = node**min_bound
        if determinant % monomial != 0:
            raise AssertionError(
                f"the second determinant at u={node} lacks the assignment monomial"
            )
        value = determinant // monomial
        node_z = node**9
        points.append((node_z, value))
        value_hash.update(f"{node}:{node_z}:{value}\n".encode("ascii"))
        print(
            f"[INFO] exact second-chart nodes {node}/15 in "
            f"{time.time() - determinant_started:.1f} s",
            flush=True,
        )
        if time.time() - determinant_started > 300:
            raise TimeoutError("five-minute exact determinant budget exceeded")

    second_in_z = Poly(interpolate(points, z), z, domain=QQ)
    require(second_in_z.degree() <= 14, "the graded second determinant has degree at most 14")
    require(
        all(second_in_z.nth(index).q == 1 for index in range(15)),
        "all graded second-determinant coefficients are integers",
    )
    second_in_z = Poly(second_in_z.as_expr(), z, domain=ZZ)
    require(
        second_in_z.degree() == 14
        and second_in_z.nth(0) != 0
        and second_in_z.nth(14) != 0,
        "the exact graded second determinant attains both endpoint bounds",
    )

    for node in (-1, 16):
        determinant = exp104.exact_determinant(selected_exact, node)
        monomial = node**min_bound
        require(
            determinant % monomial == 0,
            f"the independent second determinant at u={node} has its monomial",
        )
        require(
            determinant // monomial == int(second_in_z.eval(node**9)),
            f"the graded interpolation agrees independently at u={node}",
        )

    second_content, second_primitive = second_in_z.primitive()
    require(
        first_primitive.gcd(second_primitive).degree() == 0,
        "the two primitive graded determinants are coprime over QQ[z]",
    )
    bezout_a, bezout_b, bezout_gcd = gcdex(
        Poly(first_primitive, z, domain=QQ),
        Poly(second_primitive, z, domain=QQ),
    )
    require(bezout_gcd == Poly(1, z, domain=QQ), "the rational Bezout gcd is one")
    denominators = [
        coefficient.q
        for poly in (bezout_a, bezout_b)
        for coefficient in poly.all_coeffs()
    ]
    multiplier = 1
    for denominator in denominators:
        multiplier = lcm(multiplier, int(denominator))
    integer_a = Poly(bezout_a.as_expr() * multiplier, z, domain=ZZ)
    integer_b = Poly(bezout_b.as_expr() * multiplier, z, domain=ZZ)
    identity = integer_a * first_primitive + integer_b * second_primitive
    require(
        identity == Poly(multiplier, z, domain=ZZ),
        "the cleared integer Bezout identity is exact",
    )

    result = {
        "experiment": "EXP-105",
        "grading_modulus": 9,
        "first_chart_grading": first_grading,
        "second_chart_grading": second_grading,
        "first_determinant": {
            "valuation_u": 1628,
            "integer_content": str(first_content),
            "primitive_coefficients_z_low_to_high": coefficients_low_to_high(
                first_primitive
            ),
        },
        "second_determinant": {
            "valuation_u": min_bound,
            "degree_u": max_bound,
            "integer_content": str(second_content),
            "primitive_coefficients_z_low_to_high": coefficients_low_to_high(
                second_primitive
            ),
            "interpolation_value_sha256": value_hash.hexdigest().upper(),
            "independent_u_checks": [-1, 16],
        },
        "bezout_identity": {
            "a_coefficients_z_low_to_high": coefficients_low_to_high(integer_a),
            "b_coefficients_z_low_to_high": coefficients_low_to_high(integer_b),
            "constant": str(multiplier),
            "identity": "A(z)*F(z)+B(z)*G(z)=constant",
        },
        "decision": "exact_bezout_curve_certificate",
        "proof_scope": (
            "the two normalized maximal minors generate the unit ideal over "
            "QQ[u,u^-1] on the EXP-101 residual curve"
        ),
        "nonclaim": (
            "no coverage of the other GGHV coefficient directions and no "
            "decision of the full (72,108) family or JC(2)"
        ),
        "total_seconds": round(time.time() - started, 3),
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print("RESULT: EXACT_BEZOUT_CURVE_CERTIFICATE", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESULT: FAILED: {exc}", file=sys.stderr, flush=True)
        raise
