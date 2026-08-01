"""EXP-132: transverse (2,8) multi-section Fitting-atlas preflight.

CPU only. Finite-field calculations select exact targets but never support a
characteristic-zero closure claim. Exact controls use SymPy rational arithmetic.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

from sympy import Poly, QQ, Rational, expand, factor, gcdex, sympify, symbols


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
E112_PATH = EXPERIMENTS / "EXP-112-augmented-graph-core" / "run.py"
E115_PATH = (
    EXPERIMENTS / "EXP-115-weighted-residual-component-gate" / "run.py"
)
E122_PATH = (
    EXPERIMENTS / "EXP-122-shared-basis-core-lift-audit" / "run.py"
)
E123_PATH = (
    EXPERIMENTS / "EXP-123-direction-29-symbolic-lift" / "run.py"
)
E124_PATH = (
    EXPERIMENTS / "EXP-124-rational-graph-alternative-chart" / "run.py"
)
E131_PATH = EXPERIMENTS / "EXP-131-a0-boundary-atlas" / "run.py"
E122_ARTIFACT = E122_PATH.parent / "artifacts" / "results.json"
E123_ARTIFACT = E123_PATH.parent / "artifacts" / "results.json"
E124_ARTIFACT = E124_PATH.parent / "artifacts" / "results.json"
E131_ARTIFACT = E131_PATH.parent / "artifacts" / "results.json"
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
EXACT_WORKER = HERE / "exact_worker.py"
EXACT_WORKER_ARTIFACT = HERE / "artifacts" / "exact-worker.json"

TARGET = (2, 8)
PRIMES = (1009, 1153)
FINITE_PRIMES = (109, 127)
FIBRES = ((1, 1), (2, 3))
MAX_T_DEGREE = 62
PREDICTED_DEGREE_GATE = 8
HARD_SECONDS = 20 * 60
EXACT_WORKER_SECONDS = 5 * 60


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


exp115 = load_module("exp115_for_132", E115_PATH)
exp112 = exp115.exp112


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def persist(payload: dict[str, object], path: Path = CHECKPOINT) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_system():
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
    matrices = {
        direction: exp112.coefficient_matrix(
            {direction: exp112.Fraction(1)},
            row_labels,
            q_columns,
            include_rhs=False,
        )
        for direction in ((0, 5), (2, 9), TARGET)
    }
    require(base.shape == (302, 125), "rebuilt the complete 302 by 125 system")
    return base, matrices


def row_bases() -> dict[str, list[int]]:
    e123 = load_json(E123_ARTIFACT)
    e124 = load_json(E124_ARTIFACT)
    e131 = load_json(E131_ARTIFACT)
    bases = {
        "exp131_primary": list(e131["primary_rows"]),
        "exp131_alternative": list(e131["alternative_rows"]),
        "exp123_shared": list(e123["shared_rows"]),
        "exp124_alternative": list(e124["selected_rows"]),
    }
    require(all(len(rows) == 125 for rows in bases.values()), "loaded four 125-row bases")
    require(
        len({tuple(rows) for rows in bases.values()}) == len(bases),
        "the four inherited row bases are distinct",
    )
    return bases


def mod_entry(value, prime: int) -> int:
    numerator, denominator = value.as_numer_denom()
    return (
        int(numerator) % prime
        * pow(int(denominator) % prime, -1, prime)
        % prime
    )


def matrix_mod(matrix, prime: int) -> list[list[int]]:
    return [
        [mod_entry(matrix[row, column], prime) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    work = [row[:] for row in matrix]
    determinant = 1
    size = len(work)
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
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
        pivot_row = work[column]
        for row in range(column + 1, size):
            multiplier = work[row][column] * inverse % prime
            if multiplier:
                target_row = work[row]
                for target in range(column, size):
                    target_row[target] = (
                        target_row[target] - multiplier * pivot_row[target]
                    ) % prime
    return determinant % prime


def pencil_values(
    fixed: list[list[int]],
    transverse: list[list[int]],
    prime: int,
) -> list[int]:
    values = []
    for t_value in range(MAX_T_DEGREE + 1):
        matrix = [
            [
                (fixed[row][column] + t_value * transverse[row][column])
                % prime
                for column in range(125)
            ]
            for row in range(125)
        ]
        values.append(determinant_mod(matrix, prime))
    return values


def trim(polynomial: list[int], prime: int) -> list[int]:
    result = [value % prime for value in polynomial]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def polynomial_degree(polynomial: list[int], prime: int) -> int:
    reduced = trim(polynomial, prime)
    return -1 if reduced == [0] else len(reduced) - 1


def multiply_linear(
    polynomial: list[int], constant: int, prime: int
) -> list[int]:
    result = [0] * (len(polynomial) + 1)
    for index, value in enumerate(polynomial):
        result[index] = (result[index] + constant * value) % prime
        result[index + 1] = (result[index + 1] + value) % prime
    return trim(result, prime)


def interpolate_consecutive(values: list[int], prime: int) -> list[int]:
    differences = [value % prime for value in values]
    deltas = []
    while differences:
        deltas.append(differences[0])
        differences = [
            (differences[index + 1] - differences[index]) % prime
            for index in range(len(differences) - 1)
        ]
    coefficients = [0] * len(values)
    binomial_basis = [1]
    for order, delta in enumerate(deltas):
        for index, value in enumerate(binomial_basis):
            coefficients[index] = (
                coefficients[index] + delta * value
            ) % prime
        if order + 1 < len(values):
            binomial_basis = multiply_linear(
                binomial_basis, -order, prime
            )
            inverse = pow(order + 1, -1, prime)
            binomial_basis = [
                value * inverse % prime for value in binomial_basis
            ]
    polynomial = trim(coefficients, prime)
    for point, expected in enumerate(values):
        observed = 0
        for coefficient in reversed(polynomial):
            observed = (observed * point + coefficient) % prime
        if observed != expected % prime:
            raise AssertionError(f"interpolation control failed at T={point}")
    require(True, "verified every modular interpolation sample")
    return polynomial


def polynomial_divmod(
    numerator: list[int], denominator: list[int], prime: int
) -> tuple[list[int], list[int]]:
    numerator = trim(numerator, prime)
    denominator = trim(denominator, prime)
    if denominator == [0]:
        raise ZeroDivisionError("polynomial divisor is zero")
    if len(numerator) < len(denominator):
        return [0], numerator
    quotient = [0] * (len(numerator) - len(denominator) + 1)
    inverse = pow(denominator[-1], -1, prime)
    while numerator != [0] and len(numerator) >= len(denominator):
        shift = len(numerator) - len(denominator)
        coefficient = numerator[-1] * inverse % prime
        quotient[shift] = coefficient
        for index, value in enumerate(denominator):
            numerator[index + shift] = (
                numerator[index + shift] - coefficient * value
            ) % prime
        numerator = trim(numerator, prime)
    return trim(quotient, prime), numerator


def polynomial_gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    left = trim(left, prime)
    right = trim(right, prime)
    while right != [0]:
        _, remainder = polynomial_divmod(left, right, prime)
        left, right = right, remainder
    inverse = pow(left[-1], -1, prime)
    return trim([value * inverse % prime for value in left], prime)


def exact_t0_controls(base, matrices, bases):
    b, c = symbols("B C")
    e131 = load_json(E131_ARTIFACT)
    primary = sympify(e131["primary_determinant"], locals={"B": b, "C": c})
    alternative = sympify(
        e131["alternative_determinant"], locals={"B": b, "C": c}
    )
    controls = []
    for b_value, c_value in ((0, 0), (1, 0), (0, 1), (2, 3)):
        matrix = base + b_value * matrices[(0, 5)] + c_value * matrices[(2, 9)]
        for name, expression in (
            ("exp131_primary", primary),
            ("exp131_alternative", alternative),
        ):
            direct = matrix.extract(bases[name], range(125)).det(method="domain-ge")
            expected = expression.subs({b: b_value, c: c_value})
            require(
                direct == expected,
                f"{name} exact T=0 control at ({b_value},{c_value})",
            )
            controls.append(
                {
                    "basis": name,
                    "B": b_value,
                    "C": c_value,
                    "determinant": str(direct),
                }
            )
    first_divisor = sympify(e131["primary_divisor"], locals={"B": b})
    second_divisor = sympify(e131["alternative_divisor"], locals={"B": b})
    u = sympify(e131["bezout"]["first_coefficient"], locals={"B": b})
    v = sympify(e131["bezout"]["second_coefficient"], locals={"B": b})
    require(
        expand(u * first_divisor + v * second_divisor) == 1,
        "reproduced the EXP-131 exact Bezout identity",
    )
    return controls


def main() -> None:
    started = time.time()
    payload: dict[str, object] = {
        "experiment": "EXP-132",
        "target_direction": list(TARGET),
        "parameterization": (
            "A=0, d=1, M0(B,C,T)=base+B*M_(0,5)+C*M_(2,9)+T*M_(2,8)"
        ),
        "source_sha256": {
            path.name + "@" + path.parent.name: sha256(path)
            for path in (E112_PATH, E115_PATH, E122_PATH, E123_PATH, E124_PATH, E131_PATH)
        },
    }
    e122 = load_json(E122_ARTIFACT)
    target_record = e122["direction_records"]["(2,8)"]
    require(target_record["one_parameter_factor"] == "(3*t + 68)/68", "reproduced the (2,8) anchor factor record")
    require(target_record["union_largest_cyclic_component"] == 35, "reproduced the size-35 union SCC record")
    payload["exp122_target_record"] = target_record
    base, matrices = build_system()
    bases = row_bases()
    payload["row_bases"] = bases
    payload["checkpoint"] = "matrix-built"
    persist(payload)

    controls = exact_t0_controls(base, matrices, bases)
    payload["exact_t0_controls"] = controls
    payload["checkpoint"] = "exact-t0-regression-complete"
    persist(payload)

    modular_records = []
    for prime in PRIMES:
        print(f"[INFO] starting modular atlas at p={prime}", flush=True)
        for name, rows in bases.items():
            selected = {
                "base": base.extract(rows, range(125)),
                "B": matrices[(0, 5)].extract(rows, range(125)),
                "C": matrices[(2, 9)].extract(rows, range(125)),
                "T": matrices[TARGET].extract(rows, range(125)),
            }
            selected_mod = {
                key: matrix_mod(matrix, prime)
                for key, matrix in selected.items()
            }
            for b_value, c_value in FIBRES:
                fixed = [
                    [
                        (
                            selected_mod["base"][row][column]
                            + b_value * selected_mod["B"][row][column]
                            + c_value * selected_mod["C"][row][column]
                        )
                        % prime
                        for column in range(125)
                    ]
                    for row in range(125)
                ]
                values = pencil_values(fixed, selected_mod["T"], prime)
                polynomial = interpolate_consecutive(values, prime)
                record = {
                    "prime": prime,
                    "basis": name,
                    "B": b_value,
                    "C": c_value,
                    "degree_T": polynomial_degree(polynomial, prime),
                    "coefficients_ascending": polynomial,
                    "values_sha256": hashlib.sha256(
                        json.dumps(values).encode("utf-8")
                    ).hexdigest().upper(),
                }
                modular_records.append(record)
                print(
                    f"[INFO] p={prime} {name} fibre=({b_value},{c_value}) "
                    f"degree_T={record['degree_T']}",
                    flush=True,
                )
                payload["modular_records"] = modular_records
                payload["checkpoint"] = f"p={prime}:{name}:{b_value},{c_value}"
                persist(payload)
                require(
                    time.time() - started < HARD_SECONDS,
                    "total run remains inside the 20-minute gate",
                )

    fibre_gcds = []
    for prime in PRIMES:
        for b_value, c_value in FIBRES:
            records = [
                record
                for record in modular_records
                if record["prime"] == prime
                and record["B"] == b_value
                and record["C"] == c_value
            ]
            common = records[0]["coefficients_ascending"]
            for record in records[1:]:
                common = polynomial_gcd(
                    common, record["coefficients_ascending"], prime
                )
            fibre_gcds.append(
                {
                    "prime": prime,
                    "B": b_value,
                    "C": c_value,
                    "gcd_degree_T": polynomial_degree(common, prime),
                    "monic_gcd_coefficients_ascending": common,
                }
            )
            require(
                len(common) == 1,
                f"four-section modular gcd is a unit at p={prime}, fibre=({b_value},{c_value})",
            )

    exp131_degrees = [
        record["degree_T"]
        for record in modular_records
        if record["basis"].startswith("exp131_")
    ]
    prediction_2 = max(exp131_degrees) <= PREDICTED_DEGREE_GATE
    generic_fibre_unit_gcd = all(
        record["gcd_degree_T"] == 0 for record in fibre_gcds
    )
    prediction_3 = all(
        any(
            record["basis"] == basis
            and record["degree_T"] >= 0
            for record in modular_records
        )
        for basis in (
            "exp131_primary",
            "exp131_alternative",
            "exp123_shared",
        )
    )

    residual_records = []
    residual_rows = None
    for prime in PRIMES:
        base_mod = matrix_mod(base, prime)
        db_mod = matrix_mod(matrices[(0, 5)], prime)
        dc_mod = matrix_mod(matrices[(2, 9)], prime)
        dt_mod = matrix_mod(matrices[TARGET], prime)
        linear_root = (-4 * pow(5, -1, prime)) % prime
        cases = [("linear", linear_root, 3200 % prime)]
        quadratic_roots = [
            value
            for value in range(prime)
            if (25 * value * value - 20 * value + 16) % prime == 0
        ]
        require(len(quadratic_roots) == 2, f"quadratic boundary splits modulo {prime}")
        cases.extend(
            (f"quadratic-{index}", value, (-4000 * value) % prime)
            for index, value in enumerate(quadratic_roots)
        )
        for name, b_value, rho in cases:
            at_unit_c = [
                [
                    (
                        base_mod[row][column]
                        + b_value * db_mod[row][column]
                        + dc_mod[row][column]
                        + rho * dt_mod[row][column]
                    )
                    % prime
                    for column in range(125)
                ]
                for row in range(302)
            ]
            current_rows = exp115.independent_row_basis(at_unit_c, prime)
            require(len(current_rows) == 125, f"{name} residual has rank 125 modulo {prime}")
            if residual_rows is None:
                residual_rows = current_rows
            else:
                require(current_rows == residual_rows, "residual row basis is stable across components and primes")
            values = []
            for c_value in (1, 2, 3, 5, 7, 11):
                t_value = rho * pow(c_value, -1, prime) % prime
                selected_matrix = [
                    [
                        (
                            base_mod[row][column]
                            + b_value * db_mod[row][column]
                            + c_value * dc_mod[row][column]
                            + t_value * dt_mod[row][column]
                        )
                        % prime
                        for column in range(125)
                    ]
                    for row in current_rows
                ]
                values.append(
                    {"C": c_value, "T": t_value, "determinant": determinant_mod(selected_matrix, prime)}
                )
            require(all(record["determinant"] for record in values), f"{name} residual section is nonzero on six controls modulo {prime}")
            residual_records.append(
                {
                    "prime": prime,
                    "component": name,
                    "B": b_value,
                    "rho_CT": rho,
                    "controls": values,
                }
            )
    assert residual_rows is not None
    payload["residual_selection"] = {
        "shared_rows": residual_rows,
        "records": residual_records,
        "exact_components": [
            {"factor": "5*B+4", "relation": "C*T=3200"},
            {"factor": "25*B**2-20*B+16", "relation": "C*T=-4000*B"},
        ],
    }
    payload["checkpoint"] = "residual-basis-selected"
    persist(payload)

    finite_records = []
    finite_rows = None
    for prime in FINITE_PRIMES:
        base_mod = matrix_mod(base, prime)
        db_mod = matrix_mod(matrices[(0, 5)], prime)
        dc_mod = matrix_mod(matrices[(2, 9)], prime)
        dt_mod = matrix_mod(matrices[TARGET], prime)
        linear_root = (-4 * pow(5, -1, prime)) % prime
        quadratic_roots = [
            value
            for value in range(prime)
            if (25 * value * value - 20 * value + 16) % prime == 0
        ]
        require(len(quadratic_roots) == 2, f"finite quadratic boundary splits modulo {prime}")
        cases = [("linear", linear_root, 3200 % prime)]
        cases.extend(
            (f"quadratic-{index}", value, (-4000 * value) % prime)
            for index, value in enumerate(quadratic_roots)
        )
        for name, b_value, rho in cases:
            c_roots = [
                c_value
                for c_value in range(1, prime)
                if (
                    15625 * pow(b_value, 6, prime) * pow(c_value, 3, prime)
                    + rho * (442368 - 437500 * pow(b_value, 6, prime))
                )
                % prime
                == 0
            ]
            require(len(c_roots) == 3, f"{name} cubic residual splits modulo {prime}")
            for c_value in c_roots:
                t_value = rho * pow(c_value, -1, prime) % prime
                matrix = [
                    [
                        (
                            base_mod[row][column]
                            + b_value * db_mod[row][column]
                            + c_value * dc_mod[row][column]
                            + t_value * dt_mod[row][column]
                        )
                        % prime
                        for column in range(125)
                    ]
                    for row in range(302)
                ]
                current_rows = exp115.independent_row_basis(matrix, prime)
                require(len(current_rows) == 125, f"{name} finite residual has rank 125 modulo {prime}")
                if finite_rows is None:
                    finite_rows = current_rows
                else:
                    require(current_rows == finite_rows, "finite residual row basis is stable across all 18 controls")
                finite_records.append(
                    {
                        "prime": prime,
                        "component": name,
                        "B": b_value,
                        "C": c_value,
                        "T": t_value,
                    }
                )
    assert finite_rows is not None
    payload["finite_selection"] = {
        "selection_primes": list(FINITE_PRIMES),
        "shared_rows": finite_rows,
        "controls": finite_records,
    }
    payload["checkpoint"] = "finite-basis-selected"
    persist(payload)

    print("[INFO] launching exact two-section worker", flush=True)
    worker_record = None
    worker_status = "not-run"
    exact_unit_certificate = None
    try:
        worker = subprocess.run(
            [sys.executable, str(EXACT_WORKER)],
            cwd=HERE,
            capture_output=True,
            text=True,
            timeout=EXACT_WORKER_SECONDS,
            check=False,
        )
        print(worker.stdout, end="", flush=True)
        if worker.stderr:
            print(worker.stderr, file=sys.stderr, end="", flush=True)
        require(worker.returncode == 0, "exact two-section worker completed")
        worker_record = load_json(EXACT_WORKER_ARTIFACT)
        worker_status = "complete"
        b, c, t = symbols("B C T")
        e131 = load_json(E131_ARTIFACT)
        primary = sympify(
            worker_record["primary"]["determinant"],
            locals={"B": b, "C": c, "T": t},
        )
        alternative = sympify(
            worker_record["alternative"]["determinant"],
            locals={"B": b, "C": c, "T": t},
        )
        require(
            expand(primary.subs(t, 0) - sympify(e131["primary_determinant"], locals={"B": b, "C": c})) == 0,
            "exact primary lift reproduces EXP-131 at T=0",
        )
        require(
            expand(alternative.subs(t, 0) - sympify(e131["alternative_determinant"], locals={"B": b, "C": c})) == 0,
            "exact alternative lift reproduces EXP-131 at T=0",
        )
        require(worker_record["primary"]["degree_T"] == 0, "primary section is exactly T-inert")
        require(worker_record["alternative"]["degree_T"] == 1, "alternative section is exactly affine in T")
        finite = sympify(
            worker_record["finite"]["determinant"],
            locals={"B": b, "C": c, "T": t},
        )
        primary_core = expand((5 * b + 4) ** 3 * (25 * b**2 - 20 * b + 16) ** 3)
        alternative_core = expand(
            b**95
            * (
                4785156250 * b**12
                + 9765625 * b**11 * c * t
                - 1050000000 * b**9
                - 10214400000 * b**6
                + 1061683200 * b**3
                + 5435817984
            )
        )
        finite_core = b**105 * c
        primary_scalar = factor(primary / primary_core)
        alternative_scalar = factor(alternative / alternative_core)
        finite_scalar = factor(finite / finite_core)
        require(not primary_scalar.has(b, c, t), "primary normalization scalar is constant")
        require(not alternative_scalar.has(b, c, t), "alternative normalization scalar is constant")
        require(not finite_scalar.has(b, c, t), "finite normalization scalar is constant")
        require(worker_record["finite"]["degree_T"] == 0, "fourth section is exactly T-inert")
        require(worker_record["finite"]["term_count"] == 1, "fourth section is exactly monomial")
        alternative_axis = expand(
            alternative_core - 9765625 * b * t * finite_core
        )
        require(not alternative_axis.has(c, t), "eliminated the CT term with the fourth section")
        bezout_primary, bezout_axis, bezout_gcd = gcdex(
            Poly(primary_core, b, domain=QQ),
            Poly(alternative_axis, b, domain=QQ),
        )
        require(bezout_gcd.as_expr() == 1, "normalized primary and axis sections have unit gcd")
        identity = expand(
            bezout_primary.as_expr() * primary_core
            + bezout_axis.as_expr() * alternative_axis
        )
        require(identity == 1, "verified the exact three-minor Bezout identity")
        exact_unit_certificate = {
            "normalized_primary": str(primary_core),
            "normalized_alternative": str(alternative_core),
            "normalized_fourth": str(finite_core),
            "ct_elimination": (
                "Q(B,C,T)-9765625*B*T*R(B,C,T)=Q0(B)"
            ),
            "axis_polynomial": str(alternative_axis),
            "bezout_primary_coefficient": str(bezout_primary.as_expr()),
            "bezout_axis_coefficient": str(bezout_axis.as_expr()),
            "gcd": str(bezout_gcd.as_expr()),
            "identity": (
                "u(B)*P(B)+v(B)*(Q(B,C,T)-9765625*B*T*R(B,C,T))=1"
            ),
            "normalization_scalars": {
                "primary": str(primary_scalar),
                "alternative": str(alternative_scalar),
                "fourth": str(finite_scalar),
            },
        }
    except subprocess.TimeoutExpired:
        worker_status = "timeout-at-five-minute-gate"
        print("[STOP] exact worker reached the five-minute gate", flush=True)

    payload.update(
        {
            "modular_records": modular_records,
            "fibre_gcds": fibre_gcds,
            "generic_fibre_unit_gcd": generic_fibre_unit_gcd,
            "exact_worker_status": worker_status,
            "exact_worker": worker_record,
            "exact_unit_certificate": exact_unit_certificate,
            "predictions": {
                "p1_t0_regression": True,
                "p2_exp131_degree_at_most_8": prediction_2,
                "p3_at_least_three_inherited_sections_nonzero": prediction_3,
                "p4_exact_joint_dimension_at_most_1": exact_unit_certificate is not None,
            },
            "decision": (
                "confirmed_complete_A0_transverse_fitting_atlas"
                if exact_unit_certificate is not None
                else "modular_preflight_complete_exact_worker_inconclusive"
            ),
            "elapsed_seconds": time.time() - started,
            "scope": (
                "Exact three-minor unit-ideal certificate for A=0,d=1 in the "
                "five-coefficient restriction when exact_unit_certificate is "
                "present. This does not close A!=0 or the full core."
            ),
        }
    )
    persist(payload, ARTIFACT)
    print(f"[INFO] artifact SHA-256: {sha256(ARTIFACT)}", flush=True)
    if exact_unit_certificate is not None:
        print("RESULT: CONFIRMED COMPLETE A=0 TRANSVERSE FITTING ATLAS", flush=True)
    else:
        print("RESULT: TRANSVERSE PREFLIGHT COMPLETE; EXACT JOINT IDEAL OPEN", flush=True)


if __name__ == "__main__":
    main()
