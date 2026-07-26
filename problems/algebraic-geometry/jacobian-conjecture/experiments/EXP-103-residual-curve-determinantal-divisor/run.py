"""EXP-103: maximal-minor gcd on the normalized residual GGHV curve."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment
from sympy import Rational


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"
CHECKPOINT = ROOT / "artifacts" / "checkpoint.json"
EXP099_RUN = (
    ROOT.parent / "EXP-099-augmented-minor-flag" / "run.py"
)
EXP102_CHECKPOINT = (
    ROOT.parent
    / "EXP-102-residual-curve-third-chart"
    / "artifacts"
    / "checkpoint.json"
)

# Both primes admit roots of unity of order 2048.
PRIMES = (
    {"prime": 998244353, "primitive_root": 3},
    {"prime": 1004535809, "primitive_root": 3},
)
PARAMETER_POINTS = (1, 2, -1, 3, -2, 5, 7)
EXPONENTS = (0, 7, 9, 14)


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


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_eval(poly: list[int], value: int, prime: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * value + coefficient) % prime
    return result


def poly_mod(dividend: list[int], divisor: list[int], prime: int) -> list[int]:
    work = trim(list(dividend))
    divisor = trim(list(divisor))
    if divisor == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    inverse = pow(divisor[-1], -1, prime)
    while len(work) >= len(divisor) and work != [0]:
        shift = len(work) - len(divisor)
        coefficient = work[-1] * inverse % prime
        for index, value in enumerate(divisor):
            work[index + shift] = (
                work[index + shift] - coefficient * value
            ) % prime
        trim(work)
    return work


def poly_gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    left = trim(list(left))
    right = trim(list(right))
    while right != [0]:
        left, right = right, poly_mod(left, right, prime)
    inverse = pow(left[-1], -1, prime)
    return trim([(value * inverse) % prime for value in left])


def ntt(values: list[int], invert: bool, prime: int, primitive_root: int) -> None:
    size = len(values)
    target = 0
    for source in range(1, size):
        bit = size >> 1
        while target & bit:
            target ^= bit
            bit >>= 1
        target ^= bit
        if source < target:
            values[source], values[target] = values[target], values[source]

    length = 2
    while length <= size:
        root = pow(primitive_root, (prime - 1) // length, prime)
        if invert:
            root = pow(root, -1, prime)
        for start in range(0, size, length):
            current = 1
            half = length // 2
            for offset in range(half):
                even = values[start + offset]
                odd = values[start + offset + half] * current % prime
                values[start + offset] = (even + odd) % prime
                values[start + offset + half] = (even - odd) % prime
                current = current * root % prime
        length *= 2

    if invert:
        inverse_size = pow(size, -1, prime)
        for index in range(size):
            values[index] = values[index] * inverse_size % prime


def det_mod(matrix: np.ndarray, prime: int) -> int:
    work = np.array(matrix, dtype=np.int64, copy=True) % prime
    size = work.shape[0]
    determinant = 1
    for column in range(size):
        candidates = np.flatnonzero(work[column:, column])
        if candidates.size == 0:
            return 0
        pivot_row = column + int(candidates[0])
        if pivot_row != column:
            work[[column, pivot_row], :] = work[[pivot_row, column], :]
            determinant = -determinant
        pivot = int(work[column, column])
        determinant = determinant * pivot % prime
        if column + 1 == size:
            continue
        inverse = pow(pivot, -1, prime)
        factors = work[column + 1 :, column] * inverse % prime
        update = factors[:, None] * work[column, column:]
        work[column + 1 :, column:] = (
            work[column + 1 :, column:] - update
        ) % prime
    return determinant % prime


def pivot_rows(matrix: np.ndarray, prime: int) -> list[int]:
    work = np.array(matrix, dtype=np.int64, copy=True) % prime
    original_rows = np.arange(work.shape[0])
    pivot_row = 0
    chosen: list[int] = []
    for column in range(work.shape[1]):
        candidates = np.flatnonzero(work[pivot_row:, column])
        if candidates.size == 0:
            continue
        selected = pivot_row + int(candidates[0])
        if selected != pivot_row:
            work[[pivot_row, selected], :] = work[[selected, pivot_row], :]
            original_rows[[pivot_row, selected]] = original_rows[[selected, pivot_row]]
        pivot = int(work[pivot_row, column])
        inverse = pow(pivot, -1, prime)
        work[pivot_row, column:] = work[pivot_row, column:] * inverse % prime
        if pivot_row + 1 < work.shape[0]:
            factors = work[pivot_row + 1 :, column]
            update = factors[:, None] * work[pivot_row, column:]
            work[pivot_row + 1 :, column:] = (
                work[pivot_row + 1 :, column:] - update
            ) % prime
        chosen.append(int(original_rows[pivot_row]))
        pivot_row += 1
        if pivot_row == work.shape[1]:
            break
    return chosen


def matrix_at(
    coefficient_matrices: tuple[np.ndarray, ...], value: int, prime: int
) -> np.ndarray:
    powers = (1, pow(value, 7, prime), pow(value, 9, prime), pow(value, 14, prime))
    result = np.zeros_like(coefficient_matrices[0], dtype=np.int64)
    for coefficient_matrix, power in zip(coefficient_matrices, powers):
        result = (result + coefficient_matrix * power) % prime
    return result


def assignment_bounds(
    coefficient_matrices: tuple[np.ndarray, ...], row_indices: list[int]
) -> tuple[int, int]:
    selected = [matrix[row_indices, :] for matrix in coefficient_matrices]
    size = selected[0].shape[0]
    maximum = np.full((size, size), -1000000, dtype=np.int64)
    minimum = np.full((size, size), 1000000, dtype=np.int64)
    for exponent, matrix in zip(EXPONENTS, selected):
        mask = matrix != 0
        maximum[mask] = np.maximum(maximum[mask], exponent)
        minimum[mask] = np.minimum(minimum[mask], exponent)
    max_rows, max_columns = linear_sum_assignment(maximum, maximize=True)
    min_rows, min_columns = linear_sum_assignment(minimum)
    max_bound = int(maximum[max_rows, max_columns].sum())
    min_bound = int(minimum[min_rows, min_columns].sum())
    require(
        max_bound < 1000000 and min_bound < 1000000,
        "the selected chart has perfect support matchings",
    )
    return min_bound, max_bound


def determinant_polynomial(
    coefficient_matrices: tuple[np.ndarray, ...],
    row_indices: list[int],
    prime: int,
    primitive_root: int,
    chart_name: str,
) -> tuple[list[int] | None, dict]:
    min_bound, max_bound = assignment_bounds(coefficient_matrices, row_indices)
    transform_size = 1
    while transform_size <= max_bound:
        transform_size *= 2
    require(
        (prime - 1) % transform_size == 0,
        f"{chart_name}: NTT length {transform_size} is supported",
    )

    selected = tuple(matrix[row_indices, :] % prime for matrix in coefficient_matrices)
    omega = pow(primitive_root, (prime - 1) // transform_size, prime)
    values: list[int] = []
    current = 1
    chart_started = time.time()
    for index in range(transform_size):
        values.append(det_mod(matrix_at(selected, current, prime), prime))
        current = current * omega % prime
        if (index + 1) % 256 == 0:
            print(
                f"[INFO] {chart_name} p={prime}: "
                f"{index + 1}/{transform_size} determinant evaluations "
                f"in {time.time() - chart_started:.1f} s",
                flush=True,
            )

    coefficients = list(values)
    ntt(coefficients, True, prime, primitive_root)
    trim(coefficients)
    nonzero = [index for index, value in enumerate(coefficients) if value]
    require(nonzero, f"{chart_name}: determinant polynomial is nonzero modulo {prime}")
    valuation = nonzero[0]
    degree = nonzero[-1]
    endpoint_gate = (
        valuation == min_bound
        and degree == max_bound
        and coefficients[min_bound] != 0
        and coefficients[max_bound] != 0
    )
    print(
        f"[INFO] {chart_name}: assignment bounds [{min_bound},{max_bound}], "
        f"recovered support [{valuation},{degree}], "
        f"endpoint_gate={endpoint_gate}",
        flush=True,
    )

    direct_checks = []
    for value in (1, 2, prime - 1):
        direct = det_mod(matrix_at(selected, value, prime), prime)
        predicted = poly_eval(coefficients, value, prime)
        require(
            direct == predicted,
            f"{chart_name}: recovered polynomial agrees at u={-1 if value == prime - 1 else value}",
        )
        direct_checks.append(
            {
                "u": "-1" if value == prime - 1 else str(value),
                "determinant_mod_prime": direct,
            }
        )

    normalized = trim(coefficients[valuation:])
    require(normalized[0] != 0 and normalized[-1] != 0, f"{chart_name}: recovered endpoints remain nonzero")
    payload = ",".join(str(value) for value in coefficients).encode("ascii")
    record = {
        "name": chart_name,
        "row_indices": row_indices,
        "minimum_assignment_bound": min_bound,
        "maximum_assignment_bound": max_bound,
        "valuation": valuation,
        "degree": degree,
        "endpoint_gate": endpoint_gate,
        "terms_mod_prime": len(nonzero),
        "constant_coefficient_after_normalization": normalized[0],
        "leading_coefficient": normalized[-1],
        "coefficient_sha256": hashlib.sha256(payload).hexdigest().upper(),
        "direct_checks": direct_checks,
        "seconds": round(time.time() - chart_started, 3),
    }
    return normalized, record


def write_checkpoint(data: dict) -> None:
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build_polynomial_matrix(source):
    zero = [Rational(0)] * len(source.LOWER)
    values_s = list(zero)
    values_s[source.LOWER.index((0, 1))] = Rational(1)
    values_t = list(zero)
    values_t[source.LOWER.index((1, 7))] = Rational(1)

    rows_zero = source.sparse_rows(zero)
    rows_s = source.sparse_rows(values_s)
    rows_t = source.sparse_rows(values_t)
    row_labels = sorted(set(rows_zero) | set(rows_s) | set(rows_t) | {(2, 0)})
    column_labels = list(source.NQ[1:]) + ["rhs"]
    rhs_local = len(column_labels) - 1

    def dense(rows):
        matrix = np.zeros((len(row_labels), len(column_labels)), dtype=np.int64)
        for row_index, label in enumerate(row_labels):
            entries = rows.get(label, {})
            for local_column, global_column in enumerate(range(1, len(source.NQ))):
                value = Rational(entries.get(global_column, 0))
                if value.q != 1:
                    raise AssertionError("polynomial-matrix coefficients are not integral")
                matrix[row_index, local_column] = int(value)
        matrix[row_labels.index((2, 0)), rhs_local] = 1
        return matrix

    base = dense(rows_zero)
    direction_s = dense(rows_s) - base
    direction_t = dense(rows_t) - base
    # u^7 A(8u^7, 8u^2+u^-7)
    coefficient_matrices = (
        direction_t,
        base,
        8 * direction_t,
        8 * direction_s,
    )
    return coefficient_matrices, row_labels, column_labels


def checkpoint_row_indices(row_labels: list[tuple[int, int]]) -> list[int]:
    prior = json.loads(EXP102_CHECKPOINT.read_text(encoding="utf-8"))
    labels = [tuple(label) for label in prior["third_minor"]["row_labels"]]
    return [row_labels.index(label) for label in labels]


def main() -> None:
    started = time.time()
    source = load_module("exp099_matrix", EXP099_RUN)
    coefficient_matrices, row_labels, column_labels = build_polynomial_matrix(source)
    require(
        coefficient_matrices[0].shape == (289, 125),
        "the structural zero column is removed from the 289-by-126 augmented matrix",
    )
    require(
        column_labels[-1] == "rhs" and len(set(row_labels)) == len(row_labels),
        "the 125-column polynomial matrix contains the RHS and distinct rows",
    )

    # NTT implementation control independent of the determinant computation.
    for prime_data in PRIMES:
        prime = prime_data["prime"]
        primitive_root = prime_data["primitive_root"]
        control = [3, 5, 7, 11, 13] + [0] * (16 - 5)
        transformed = list(control)
        ntt(transformed, False, prime, primitive_root)
        ntt(transformed, True, prime, primitive_root)
        require(transformed == control, f"NTT round trip passes modulo {prime}")

    first_prime = PRIMES[0]["prime"]
    initial_rows = checkpoint_row_indices(row_labels)
    require(
        len(initial_rows) == len(set(initial_rows)) == 125,
        "EXP-102 supplies 125 distinct rows",
    )
    reference = matrix_at(coefficient_matrices, 1, first_prime)
    reference_det = det_mod(reference[initial_rows, :], first_prime)
    prior = json.loads(EXP102_CHECKPOINT.read_text(encoding="utf-8"))
    prior_det = int(Rational(prior["third_minor"]["determinant_at_reference"])) % first_prime
    require(
        reference_det == prior_det != 0,
        "the polynomial matrix reproduces EXP-102's exact determinant at u=1",
    )

    chart_rows: list[tuple[str, list[int]]] = [("exp102-u1", initial_rows)]
    seen = {tuple(initial_rows)}
    permutations = (
        np.arange(len(row_labels)),
        np.arange(len(row_labels))[::-1],
        np.roll(np.arange(len(row_labels)), 37),
        np.array(
            sorted(
                range(len(row_labels)),
                key=lambda index: ((137 * index + 41) % len(row_labels), index),
            ),
            dtype=np.int64,
        ),
    )
    for candidate_index, value in enumerate(PARAMETER_POINTS):
        matrix = matrix_at(coefficient_matrices, value % first_prime, first_prime)
        order = permutations[candidate_index % len(permutations)]
        local_rows = pivot_rows(matrix[order, :], first_prime)
        rows = [int(order[index]) for index in local_rows]
        require(len(rows) == 125, f"full column rank holds modulo {first_prime} at u={value}")
        key = tuple(rows)
        if key not in seen:
            chart_rows.append((f"pivot-u{value}", rows))
            seen.add(key)
        if len(chart_rows) >= 4:
            break
    require(len(chart_rows) >= 2, "at least two distinct row charts are available")

    smoke = os.environ.get("EXP103_SMOKE") == "1"
    primes_to_run = PRIMES[:1] if smoke else PRIMES
    result = {
        "experiment": "EXP-103",
        "matrix_shape": [289, 125],
        "entry_exponents": list(EXPONENTS),
        "residual_parametrization": {
            "s": "8*u^7",
            "t": "8*u^2+u^-7",
            "domain": "u != 0",
        },
        "prime_runs": [],
        "decision": "inconclusive",
    }

    charts_used: list[tuple[str, list[int]]] = []
    for prime_index, prime_data in enumerate(primes_to_run):
        prime = prime_data["prime"]
        primitive_root = prime_data["primitive_root"]
        prime_started = time.time()
        common_gcd: list[int] | None = None
        exploratory_gcd: list[int] | None = None
        records = []
        current_charts = chart_rows if prime_index == 0 else charts_used
        for chart_name, rows in current_charts:
            normalized, record = determinant_polynomial(
                coefficient_matrices,
                rows,
                prime,
                primitive_root,
                chart_name,
            )
            exploratory_gcd = (
                normalized
                if exploratory_gcd is None
                else poly_gcd(exploratory_gcd, normalized, prime)
            )
            if record["endpoint_gate"]:
                common_gcd = (
                    normalized
                    if common_gcd is None
                    else poly_gcd(common_gcd, normalized, prime)
                )
                if prime_index == 0:
                    charts_used.append((chart_name, rows))
            record["cumulative_gcd_degree"] = (
                None if common_gcd is None else len(common_gcd) - 1
            )
            record["exploratory_gcd_degree"] = len(exploratory_gcd) - 1
            records.append(record)
            print(
                f"[INFO] {chart_name} p={prime}: certified gcd degree "
                f"{record['cumulative_gcd_degree']}; exploratory gcd degree "
                f"{record['exploratory_gcd_degree']}",
                flush=True,
            )
            result["prime_runs"] = result["prime_runs"] + [
                {
                    "prime": prime,
                    "primitive_root": primitive_root,
                    "charts": records,
                    "gcd_degree": None if common_gcd is None else len(common_gcd) - 1,
                    "gcd_coefficients": (
                        common_gcd
                        if common_gcd is not None and len(common_gcd) <= 65
                        else None
                    ),
                    "exploratory_gcd_degree": len(exploratory_gcd) - 1,
                    "seconds": round(time.time() - prime_started, 3),
                }
            ]
            write_checkpoint(result)
            result["prime_runs"].pop()
            if common_gcd == [1]:
                break
            if time.time() - prime_started > 300:
                raise TimeoutError(f"five-minute budget exceeded for prime {prime}")

        if not smoke:
            require(common_gcd == [1], f"normalized chart gcd is one modulo {prime}")
        result["prime_runs"].append(
            {
                "prime": prime,
                "primitive_root": primitive_root,
                "charts": records,
                "gcd_degree": None if common_gcd is None else len(common_gcd) - 1,
                "gcd_coefficients": (
                    common_gcd
                    if common_gcd is not None and len(common_gcd) <= 65
                    else None
                ),
                "seconds": round(time.time() - prime_started, 3),
            }
        )
        write_checkpoint(result)

    if not smoke:
        require(
            len(result["prime_runs"]) == 2
            and all(run["gcd_degree"] == 0 for run in result["prime_runs"]),
            "two independent NTT primes reproduce the gcd-one certificate",
        )
        result["decision"] = "complete_two_parameter_slice_exclusion"
        result["proof_scope"] = (
            "rank 125 for every u != 0 on the EXP-101 residual curve; "
            "together with the first two charts, the declared two-parameter "
            "slice is inconsistency-certified"
        )
    else:
        result["decision"] = (
            "smoke_gcd_one"
            if result["prime_runs"][0]["gcd_degree"] == 0
            else "endpoint_gate_inconclusive"
        )

    result["total_seconds"] = round(time.time() - started, 3)
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"RESULT: {result['decision'].upper()}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESULT: FAILED: {exc}", file=sys.stderr, flush=True)
        raise
