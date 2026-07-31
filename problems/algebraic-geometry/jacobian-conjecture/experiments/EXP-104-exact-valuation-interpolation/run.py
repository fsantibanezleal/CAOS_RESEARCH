"""EXP-104: exact valuation interpolation and residual-curve gcd proof."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

from sympy import Matrix, Poly, QQ, symbols
from sympy.polys.polyfuncs import interpolate


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
EXP103_DIR = ROOT.parent / "EXP-103-residual-curve-determinantal-divisor"
EXP103_RUN = EXP103_DIR / "run.py"
EXP103_ARTIFACT = EXP103_DIR / "artifacts" / "results.json"
u = symbols("u")


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


def exact_selected_matrices(exp103, coefficient_matrices, row_indices):
    return tuple(
        Matrix(matrix[row_indices, :].tolist()) for matrix in coefficient_matrices
    )


def exact_determinant(selected_matrices, value: int) -> int:
    powers = (1, value**7, value**9, value**14)
    matrix = sum(
        (coefficient * power for coefficient, power in zip(selected_matrices, powers)),
        Matrix.zeros(125, 125),
    )
    return int(matrix.det(method="domain-ge"))


def main() -> None:
    started = time.time()
    exp103 = load_module("exp103_tools", EXP103_RUN)
    source = exp103.load_module("exp099_for_exp104", exp103.EXP099_RUN)
    coefficient_matrices, row_labels, _ = exp103.build_polynomial_matrix(source)
    first_rows = exp103.checkpoint_row_indices(row_labels)
    min_bound, max_bound = exp103.assignment_bounds(
        coefficient_matrices, first_rows
    )
    require(
        (min_bound, max_bound) == (1547, 1646),
        "EXP-103 assignment bounds reconstruct exactly",
    )
    quotient_degree_bound = max_bound - min_bound
    require(quotient_degree_bound == 99, "the exact interpolation target has degree at most 99")

    selected_exact = exact_selected_matrices(
        exp103, coefficient_matrices, first_rows
    )
    values: list[tuple[int, int]] = []
    value_payload = hashlib.sha256()
    interpolation_started = time.time()
    for node in range(1, quotient_degree_bound + 2):
        determinant = exact_determinant(selected_exact, node)
        monomial = node**min_bound
        if determinant % monomial != 0:
            raise AssertionError(
                f"the determinant at u={node} is not divisible by the assignment monomial"
            )
        quotient_value = determinant // monomial
        values.append((node, quotient_value))
        value_payload.update(f"{node}:{quotient_value}\n".encode("ascii"))
        if node % 10 == 0:
            print(
                f"[INFO] exact determinant nodes {node}/100 in "
                f"{time.time() - interpolation_started:.1f} s",
                flush=True,
            )
        if time.time() - interpolation_started > 300:
            raise TimeoutError("five-minute exact determinant budget exceeded")

    print("[INFO] interpolating the exact degree-at-most-99 quotient", flush=True)
    quotient = Poly(interpolate(values, u), u, domain=QQ)
    require(
        quotient.degree() <= quotient_degree_bound,
        "the exact interpolant respects the degree bound",
    )
    coefficients = [quotient.nth(index) for index in range(quotient_degree_bound + 1)]
    require(
        all(coefficient.q == 1 for coefficient in coefficients),
        "all interpolated coefficients are integers",
    )
    require(
        all(coefficients[index] == 0 for index in range(81)),
        "coefficients 0 through 80 vanish exactly",
    )
    require(coefficients[81] != 0, "coefficient 81 is nonzero exactly")
    require(coefficients[99] != 0, "coefficient 99 is nonzero exactly")
    exact_valuation = min_bound + 81
    exact_degree = min_bound + quotient.degree()
    require(
        (exact_valuation, exact_degree) == (1628, 1646),
        "the EXP-102 determinant has exact support [1628,1646]",
    )

    for node in (101, -1):
        determinant = exact_determinant(selected_exact, node)
        monomial = node**min_bound
        require(
            determinant % monomial == 0,
            f"independent determinant at u={node} has the assignment monomial",
        )
        require(
            determinant // monomial == int(quotient.eval(node)),
            f"exact interpolation agrees independently at u={node}",
        )

    exact_normalized = [int(coefficients[index]) for index in range(81, 100)]
    require(
        exact_normalized[0] != 0 and exact_normalized[-1] != 0,
        "the exact normalized determinant has nonzero endpoints",
    )

    prior = json.loads(EXP103_ARTIFACT.read_text(encoding="utf-8"))
    first_prime_charts = prior["prime_runs"][0]["charts"]
    safe_chart = next(
        chart for chart in first_prime_charts if chart["name"] == "pivot-u2"
    )
    require(safe_chart["endpoint_gate"], "the EXP-103 u=2 chart is endpoint-safe")
    second_rows = safe_chart["row_indices"]

    prime_records = []
    for prime_data in exp103.PRIMES:
        prime = prime_data["prime"]
        primitive_root = prime_data["primitive_root"]
        prime_started = time.time()
        first_modular, first_record = exp103.determinant_polynomial(
            coefficient_matrices,
            first_rows,
            prime,
            primitive_root,
            "exact-valued-exp102",
        )
        require(
            first_modular
            == [coefficient % prime for coefficient in exact_normalized],
            f"exact normalized coefficients reduce correctly modulo {prime}",
        )
        second_modular, second_record = exp103.determinant_polynomial(
            coefficient_matrices,
            second_rows,
            prime,
            primitive_root,
            "endpoint-safe-u2",
        )
        require(
            second_record["endpoint_gate"],
            f"the u=2 chart preserves both endpoints modulo {prime}",
        )
        common = exp103.poly_gcd(first_modular, second_modular, prime)
        require(common == [1], f"the two exact-normalized minors have gcd one modulo {prime}")
        prime_records.append(
            {
                "prime": prime,
                "first_chart": first_record,
                "second_chart": second_record,
                "gcd_coefficients": common,
                "seconds": round(time.time() - prime_started, 3),
            }
        )

    result = {
        "experiment": "EXP-104",
        "assignment_bounds": [min_bound, max_bound],
        "interpolation_nodes": [1, 100],
        "interpolation_value_sha256": value_payload.hexdigest().upper(),
        "quotient_degree_bound": quotient_degree_bound,
        "quotient_degree": quotient.degree(),
        "zero_coefficient_interval": [0, 80],
        "exact_valuation": exact_valuation,
        "exact_degree": exact_degree,
        "exact_normalized_coefficients": exact_normalized,
        "independent_exact_checks": [101, -1],
        "prime_gcd_checks": prime_records,
        "decision": "complete_two_parameter_slice_exclusion",
        "proof_scope": (
            "the augmented matrix has rank 125 at every nonzero point of the "
            "EXP-101 normalized residual curve; with the first two EXP-101 "
            "charts, the declared (0,1)/(1,7) coefficient slice is excluded"
        ),
        "nonclaim": (
            "the other 49 GGHV coefficient directions, the full (72,108) "
            "family, and JC(2) remain open"
        ),
        "total_seconds": round(time.time() - started, 3),
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print("RESULT: COMPLETE_TWO_PARAMETER_SLICE_EXCLUSION", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESULT: FAILED: {exc}", file=sys.stderr, flush=True)
        raise
