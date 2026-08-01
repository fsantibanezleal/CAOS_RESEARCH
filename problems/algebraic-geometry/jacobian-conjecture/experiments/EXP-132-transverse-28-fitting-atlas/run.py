"""EXP-132: transverse (2,8) multi-section Fitting-atlas preflight.

CPU only. Finite-field calculations select exact targets but never support a
characteristic-zero closure claim. Exact controls use SymPy rational arithmetic.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Rational, expand, sympify, symbols


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

TARGET = (2, 8)
PRIMES = (1009, 1153)
FIBRES = ((1, 1), (2, 3))
MAX_T_DEGREE = 62
PREDICTED_DEGREE_GATE = 8
HARD_SECONDS = 20 * 60


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
                    "degree_T": len(polynomial) - 1,
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
                    "gcd_degree_T": len(common) - 1,
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
    prediction_3 = all(record["gcd_degree_T"] == 0 for record in fibre_gcds)
    payload.update(
        {
            "modular_records": modular_records,
            "fibre_gcds": fibre_gcds,
            "predictions": {
                "p1_t0_regression": True,
                "p2_exp131_degree_at_most_8": prediction_2,
                "p3_modular_generic_fibre_unit_gcd": prediction_3,
                "p4_exact_joint_dimension_at_most_1": None,
            },
            "decision": "modular_preflight_complete_exact_joint_ideal_open",
            "elapsed_seconds": time.time() - started,
            "scope": (
                "Exact T=0 regression plus finite-field target selection only. "
                "No characteristic-zero Fitting-ideal closure is claimed."
            ),
        }
    )
    persist(payload, ARTIFACT)
    print(f"[INFO] artifact SHA-256: {sha256(ARTIFACT)}", flush=True)
    print("RESULT: MODULAR PREFLIGHT COMPLETE; EXACT JOINT IDEAL OPEN", flush=True)


if __name__ == "__main__":
    main()
