"""EXP-123: exact symbolic lift in direction (2, 9).

CPU only. Modular arithmetic is reconnaissance; all verdict-bearing
determinant identities use exact arithmetic over QQ.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

from sympy import QQ, Matrix, Poly, Rational, expand, gcd, sympify, symbols


HERE = Path(__file__).resolve().parent
E122_PATH = (
    HERE.parent / "EXP-122-shared-basis-core-lift-audit" / "run.py"
)
E121_ARTIFACT = (
    HERE.parent
    / "EXP-121-finite-lq-row-bases"
    / "artifacts"
    / "results.json"
)
E122_ARTIFACT = (
    HERE.parent
    / "EXP-122-shared-basis-core-lift-audit"
    / "artifacts"
    / "results.json"
)
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
WORKER_ARTIFACT = HERE / "artifacts" / "symbolic-worker.json"
WORKER = HERE / "symbolic_worker.py"
TARGET = (2, 9)
MODULAR_PROBES = ((1009, 2, 3), (1013, 3, 5))
MAX_PROBE_DEGREE = 34
EXACT_DEGREE_GATE = 4
WORKER_TIMEOUT_SECONDS = 300
TOTAL_GATE_SECONDS = 360

spec = importlib.util.spec_from_file_location("exp122", E122_PATH)
exp122 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp122)
exp112 = exp122.exp112
exp115 = exp122.exp115


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def persist(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build_selected_system():
    e121_record = json.loads(E121_ARTIFACT.read_text(encoding="utf-8"))
    e122_record = json.loads(E122_ARTIFACT.read_text(encoding="utf-8"))
    forced = exp112.forced_polynomial()
    all_directions = sorted(exp112.exp071.LOWER)
    _, complete_rows = exp112.complete_row_labels(forced, all_directions)
    constant_column = exp112.exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp112.exp071.NQ))
        if index != constant_column
    ]
    base = exp112.coefficient_matrix(
        forced, complete_rows, q_columns, include_rhs=True
    )
    wanted = ((0, 1), (0, 5), TARGET)
    direction_matrices = {
        direction: exp112.coefficient_matrix(
            {direction: exp112.Fraction(1)},
            complete_rows,
            q_columns,
            include_rhs=False,
        )
        for direction in wanted
    }
    rows = list(e122_record["shared_rows"])
    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: matrix.extract(rows, range(125))
        for direction, matrix in direction_matrices.items()
    }
    anchor = selected_base + selected_directions[(0, 1)]
    anchor_det = anchor.det(method="domain-ge")
    expected_anchor = e121_record["exact_charts"]["L"][0]["anchor"][
        "determinant"
    ]
    require(
        str(anchor_det) == expected_anchor,
        "reproduced the EXP-121 anchor determinant",
    )
    inverse = anchor.inv()
    normalized = {
        direction: inverse * matrix
        for direction, matrix in selected_directions.items()
    }
    components = exp122.cyclic_components(
        [normalized[direction] for direction in wanted]
    )
    require(
        len(components[0]) == 34,
        "reproduced the EXP-122 size-34 union SCC",
    )
    return (
        e121_record,
        rows,
        selected_base,
        selected_directions,
        anchor,
        anchor_det,
        normalized,
        components,
    )


def mod_entry(value, prime: int) -> int:
    numerator, denominator = value.as_numer_denom()
    return int(numerator) % prime * pow(int(denominator) % prime, -1, prime) % prime


def matrix_mod(matrix: Matrix, prime: int) -> list[list[int]]:
    return [
        [mod_entry(matrix[row, column], prime) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def combine_mod(
    base: list[list[int]],
    da: list[list[int]],
    db: list[list[int]],
    dc: list[list[int]],
    a: int,
    b: int,
    c: int,
    prime: int,
) -> list[list[int]]:
    return [
        [
            (
                base[row][column]
                + a * da[row][column]
                + b * db[row][column]
                + c * dc[row][column]
            )
            % prime
            for column in range(len(base[row]))
        ]
        for row in range(len(base))
    ]


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    work = [row[:] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column] % prime
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column] % prime
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] * inverse % prime
            if multiplier == 0:
                continue
            for target in range(column, len(work)):
                work[row][target] = (
                    work[row][target]
                    - multiplier * work[column][target]
                ) % prime
    return determinant % prime


def finite_difference_degree(values: list[int], prime: int) -> int:
    row = [value % prime for value in values]
    degree = 0 if any(row) else -1
    for order in range(1, len(values)):
        row = [
            (row[index + 1] - row[index]) % prime
            for index in range(len(row) - 1)
        ]
        if row[0] != 0:
            degree = order
    return degree


def modular_degree_probes(
    selected_base: Matrix,
    selected_directions: dict[tuple[int, int], Matrix],
) -> list[dict[str, object]]:
    records = []
    for prime, a_value, b_value in MODULAR_PROBES:
        base_mod = matrix_mod(selected_base, prime)
        da_mod = matrix_mod(selected_directions[(0, 1)], prime)
        db_mod = matrix_mod(selected_directions[(0, 5)], prime)
        dc_mod = matrix_mod(selected_directions[TARGET], prime)
        values = [
            determinant_mod(
                combine_mod(
                    base_mod,
                    da_mod,
                    db_mod,
                    dc_mod,
                    a_value,
                    b_value,
                    c_value,
                    prime,
                ),
                prime,
            )
            for c_value in range(MAX_PROBE_DEGREE + 1)
        ]
        degree = finite_difference_degree(values, prime)
        records.append(
            {
                "prime": prime,
                "A": a_value,
                "B": b_value,
                "sample_count": len(values),
                "degree_in_C": degree,
                "value_sha256": hashlib.sha256(
                    json.dumps(values).encode("utf-8")
                ).hexdigest().upper(),
            }
        )
        print(
            f"[INFO] modular probe p={prime}, A={a_value}, B={b_value}: "
            f"degree_C={degree}",
            flush=True,
        )
    return records


def exact_control_checks(
    expression,
    selected_base: Matrix,
    selected_directions: dict[tuple[int, int], Matrix],
    anchor_det,
):
    a, b, c = symbols("A B C")
    points = (
        (Rational(1), Rational(0), Rational(1)),
        (Rational(2), Rational(1), Rational(1)),
        (Rational(1), Rational(1), Rational(-1)),
        (Rational(0), Rational(1), Rational(2)),
    )
    records = []
    for a_value, b_value, c_value in points:
        direct = (
            selected_base
            + a_value * selected_directions[(0, 1)]
            + b_value * selected_directions[(0, 5)]
            + c_value * selected_directions[TARGET]
        ).det(method="domain-ge") / anchor_det
        predicted = expression.subs(
            {a: a_value, b: b_value, c: c_value}
        )
        require(
            direct == predicted,
            (
                "direct 125 by 125 determinant agrees at "
                f"({a_value},{b_value},{c_value})"
            ),
        )
        records.append(
            {
                "A": str(a_value),
                "B": str(b_value),
                "C": str(c_value),
                "direct_ratio": str(direct),
                "predicted_ratio": str(predicted),
            }
        )
    return records


def reduce_a_residue_class(expression, a, b, x):
    polynomial = Poly(expression, a, b, domain=QQ)
    valuation = min(monomial[0] for monomial, _ in polynomial.terms())
    require(
        all(
            (monomial[0] - valuation) % 3 == 0
            for monomial, _ in polynomial.terms()
        ),
        f"A exponents occupy one residue class above valuation {valuation}",
    )
    reduced = expand(
        sum(
            coefficient
            * x ** ((monomial[0] - valuation) // 3)
            * b ** monomial[1]
            for monomial, coefficient in polynomial.terms()
        )
    )
    return valuation, reduced


def main() -> None:
    started = time.time()
    (
        e121_record,
        rows,
        selected_base,
        selected_directions,
        anchor,
        anchor_det,
        normalized,
        components,
    ) = build_selected_system()
    c = symbols("C")
    anchor_line = exp122.one_parameter_factor(normalized[TARGET])[0]
    require(
        expand(anchor_line - (1 + Rational(3, 544) * symbols("t"))) == 0,
        "reproduced the EXP-122 anchor-line factor",
    )
    payload: dict[str, object] = {
        "experiment": "EXP-123",
        "target_direction": list(TARGET),
        "shared_rows": rows,
        "anchor_determinant": str(anchor_det),
        "union_cyclic_component_sizes": [
            len(component) for component in components
        ],
        "anchor_line_factor": str(anchor_line),
    }
    persist(payload, CHECKPOINT)

    probes = modular_degree_probes(selected_base, selected_directions)
    payload["modular_degree_probes"] = probes
    persist(payload, CHECKPOINT)
    max_degree = max(record["degree_in_C"] for record in probes)
    if max_degree > EXACT_DEGREE_GATE:
        payload["decision"] = "stopped_at_modular_degree_gate"
        payload["elapsed_seconds"] = time.time() - started
        payload["scope"] = (
            "Modular reconnaissance only. No exact symbolic determinant "
            "claim is made."
        )
        persist(payload, ARTIFACT)
        print(
            f"[STOP] generic C-degree {max_degree} exceeds exact gate "
            f"{EXACT_DEGREE_GATE}",
            flush=True,
        )
        print("RESULT: INCONCLUSIVE AT DECLARED GATE", flush=True)
        return

    print("[INFO] launching exact symbolic worker", flush=True)
    try:
        worker = subprocess.run(
            [sys.executable, str(WORKER)],
            cwd=HERE,
            capture_output=True,
            text=True,
            timeout=WORKER_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        payload["decision"] = "stopped_at_symbolic_timeout"
        payload["worker_stdout"] = error.stdout or ""
        payload["worker_stderr"] = error.stderr or ""
        payload["elapsed_seconds"] = time.time() - started
        persist(payload, ARTIFACT)
        print("[STOP] exact symbolic worker reached five-minute gate", flush=True)
        print("RESULT: INCONCLUSIVE AT DECLARED GATE", flush=True)
        return
    print(worker.stdout, end="", flush=True)
    if worker.stderr:
        print(worker.stderr, file=sys.stderr, end="", flush=True)
    require(worker.returncode == 0, "exact symbolic worker completed")
    worker_record = json.loads(WORKER_ARTIFACT.read_text(encoding="utf-8"))
    a, b, c = symbols("A B C")
    expression = sympify(
        worker_record["determinant_ratio"],
        locals={"A": a, "B": b, "C": c},
    )
    polynomial = Poly(expression, c, domain="QQ[A,B]")
    exact_degree = int(polynomial.degree())
    coefficient_records = {
        str(power): str(expand(polynomial.nth(power)))
        for power in range(exact_degree + 1)
    }
    constant = expand(polynomial.nth(0))
    expected_constant = sympify(
        e121_record["exact_charts"]["L"][0][
            "determinant_d1_up_to_anchor_scalar"
        ],
        locals={"A": a, "B": b},
    )
    require(
        expand(constant - expected_constant) == 0,
        "C=0 specialization reproduces the EXP-121 exact chart",
    )
    require(
        expand(expression.subs({a: 1, b: 0}) - (1 + Rational(3, 544) * c))
        == 0,
        "symbolic determinant reproduces the EXP-122 anchor line",
    )
    controls = exact_control_checks(
        expression,
        selected_base,
        selected_directions,
        anchor_det,
    )
    affine = exact_degree == 1
    coefficient_gcd = None
    if affine:
        coefficient_gcd = gcd(
            Poly(constant, a, b, domain="QQ"),
            Poly(expand(polynomial.nth(1)), a, b, domain="QQ"),
        ).monic()
    x = symbols("X")
    constant_valuation, invariant_constant = reduce_a_residue_class(
        constant, a, b, x
    )
    coefficient_valuation, invariant_coefficient = reduce_a_residue_class(
        expand(polynomial.nth(1)), a, b, x
    )
    require(
        constant_valuation == 87 and coefficient_valuation == 89,
        "coefficient A-valuations are exactly 87 and 89",
    )
    primitive_gcd = gcd(
        Poly(invariant_constant, x, b, domain=QQ),
        Poly(invariant_coefficient, x, b, domain=QQ),
    ).monic()
    require(
        primitive_gcd.total_degree() == 0,
        "invariant coefficient polynomials are coprime",
    )
    require(
        expand(
            a**87
            * (
                invariant_constant.subs(x, a**3)
                + a**2 * c * invariant_coefficient.subs(x, a**3)
            )
            - expression
        )
        == 0,
        "reconstructed A^87*(R(A^3,B)+A^2*C*S(A^3,B))",
    )
    payload.update(
        {
            "symbolic_worker": worker_record,
            "exact_degree_in_C": exact_degree,
            "coefficient_polynomials": coefficient_records,
            "coefficient_gcd": (
                str(coefficient_gcd.as_expr())
                if coefficient_gcd is not None
                else None
            ),
            "invariant_reduction": {
                "formula": "A^87*(R(A^3,B)+A^2*C*S(A^3,B))",
                "constant_A_valuation": constant_valuation,
                "coefficient_A_valuation": coefficient_valuation,
                "R_X_B": str(invariant_constant),
                "S_X_B": str(invariant_coefficient),
                "R_monomial_count": len(
                    Poly(invariant_constant, x, b).terms()
                ),
                "S_monomial_count": len(
                    Poly(invariant_coefficient, x, b).terms()
                ),
                "R_total_degree_X_B": Poly(
                    invariant_constant, x, b
                ).total_degree(),
                "S_total_degree_X_B": Poly(
                    invariant_coefficient, x, b
                ).total_degree(),
                "primitive_gcd": str(primitive_gcd.as_expr()),
            },
            "direct_exact_controls": controls,
            "predictions": {
                "p1_c0_regression": True,
                "p2_affine_in_C": affine,
                "p3_nonzero_mixed_coefficient": (
                    exact_degree >= 1
                    and (
                        Poly(polynomial.nth(1), a, b).total_degree() > 0
                    )
                ),
                "p4_unit_coefficient_gcd": (
                    coefficient_gcd is not None
                    and coefficient_gcd.total_degree() == 0
                ),
            },
            "decision": (
                "confirmed_affine_symbolic_lift"
                if affine
                else "refuted_affine_prediction"
            ),
            "elapsed_seconds": time.time() - started,
            "scope": (
                "Exact selected-chart determinant on the d=1 "
                "A/B/(2,9) restriction. This is not a four-parameter "
                "chart cover and does not close the 24-parameter core, "
                "the 51-parameter family, (72,108), the degree floor, "
                "or JC(2)."
            ),
        }
    )
    require(
        payload["elapsed_seconds"] <= TOTAL_GATE_SECONDS,
        "EXP-123 remains within the six-minute total gate",
    )
    persist(payload, ARTIFACT)
    digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(
        f"[INFO] exact degree_C={exact_degree}, "
        f"elapsed={payload['elapsed_seconds']:.2f} s",
        flush=True,
    )
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    main()
