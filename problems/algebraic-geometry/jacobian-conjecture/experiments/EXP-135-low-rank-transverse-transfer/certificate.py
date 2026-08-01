"""EXP-135 deterministic characteristic-zero ambient identity certificate."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from sympy import eye, ilcm, prevprime

import preflight


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
ARTIFACT = HERE / "artifacts" / "certificate.json"
PRIME_COUNT = 30
PRIME_START = 1_000_000_000
TARGET = (2, 8)
GRAPH_DIRECTIONS = ((0, 1), (0, 5), (2, 9))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)
    print(f"[PASS] {message}", flush=True)


def rank_factor(matrix):
    _, pivot_columns = matrix.rref()
    left = matrix[:, list(pivot_columns)]
    _, pivot_rows = left.T.rref()
    pivot_rows = list(pivot_rows)
    right = left.extract(pivot_rows, range(left.cols)).inv() * matrix.extract(
        pivot_rows, range(matrix.cols)
    )
    require(left * right == matrix, "verified exact rank factorization")
    return left, right


def mod_entry(value, prime: int) -> int:
    numerator, denominator = value.as_numer_denom()
    return int(numerator) % prime * pow(int(denominator) % prime, -1, prime) % prime


def mod_matrix(matrix, prime: int) -> list[list[int]]:
    return [
        [mod_entry(matrix[row, column], prime) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def solve_mod(
    matrix: list[list[int]], right: list[list[int]], prime: int
) -> list[list[int]]:
    size = len(matrix)
    width = len(right[0])
    work = [matrix[row][:] + right[row][:] for row in range(size)]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column] % prime),
            None,
        )
        if pivot is None:
            raise RuntimeError("declared interpolation base is singular")
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
        inverse = pow(work[column][column] % prime, -1, prime)
        for row in range(column + 1, size):
            if not work[row][column] % prime:
                continue
            multiplier = work[row][column] * inverse % prime
            for target in range(column + 1, size + width):
                work[row][target] = (
                    work[row][target] - multiplier * work[column][target]
                ) % prime
    solution = [[0] * width for _ in range(size)]
    for row in range(size - 1, -1, -1):
        inverse = pow(work[row][row] % prime, -1, prime)
        for column in range(width):
            value = work[row][size + column]
            for target in range(row + 1, size):
                value -= work[row][target] * solution[target][column]
            solution[row][column] = value * inverse % prime
    return solution


def multiply_mod(
    left: list[list[int]], right: list[list[int]], prime: int
) -> list[list[int]]:
    inner = len(right)
    columns = len(right[0])
    return [
        [
            sum(left[row][index] * right[index][column] for index in range(inner))
            % prime
            for column in range(columns)
        ]
        for row in range(len(left))
    ]


def subtract_mod(
    left: list[list[int]], right: list[list[int]], prime: int
) -> list[list[int]]:
    return [
        [
            (left[row][column] - right[row][column]) % prime
            for column in range(len(left[0]))
        ]
        for row in range(len(left))
    ]


def scale_mod(matrix: list[list[int]], scalar: int, prime: int) -> list[list[int]]:
    return [[scalar * value % prime for value in row] for row in matrix]


def identity_mod(size: int) -> list[list[int]]:
    return [[int(row == column) for column in range(size)] for row in range(size)]


def coefficient_bound(matrices) -> tuple[int, int, list[int]]:
    denominator = 1
    for matrix in matrices:
        for value in matrix:
            denominator = ilcm(denominator, int(value.as_numer_denom()[1]))
    integer_matrices = [matrix * denominator for matrix in matrices]
    row_sums = []
    for row in range(matrices[0].rows):
        row_sum = 0
        for column in range(matrices[0].cols):
            row_sum += denominator if row == column else 0
            row_sum += 2 * abs(int(integer_matrices[0][row, column]))
            row_sum += sum(
                abs(int(matrix[row, column])) for matrix in integer_matrices[1:]
            )
        row_sums.append(row_sum)
    determinant_l1_bound = math.prod(row_sums)
    difference_coefficient_bound = 2 * determinant_l1_bound
    return int(denominator), difference_coefficient_bound, row_sums


def main() -> None:
    e124 = preflight.read_json(preflight.EXP124_RESULTS)
    rows = list(e124["selected_rows"])
    _, selected_base, directions = preflight.exp134.selected_system(
        preflight.exp124, rows
    )
    inverse = (selected_base + directions[(0, 1)]).inv()
    normalized = {
        direction: inverse * matrix for direction, matrix in directions.items()
    }
    components = preflight.exp124.exp122.cyclic_components(list(normalized.values()))
    core = max(components, key=len)
    require(len(core) == 33, "reproduced the exact size-33 core")
    graph = [normalized[key].extract(core, core) for key in GRAPH_DIRECTIONS]
    transverse = normalized[TARGET].extract(core, core)
    u, v_transpose = rank_factor(transverse)
    c_left, c_right = rank_factor(graph[2])
    require(u.cols == 7, "transverse update has exact rank seven")
    require(c_left.cols == 6, "C update has exact rank six")
    require(transverse**3 == eye(33) * 0, "transverse core is nilpotent of index at most three")
    require((transverse**2).rank() == 3, "transverse square has exact rank three")

    denominator, height_bound, row_sums = coefficient_bound([*graph, transverse])
    degree_bounds = [int(matrix.rank()) for matrix in (*graph, transverse)]
    require(degree_bounds == [25, 24, 6, 7], "proved separate determinant degree bounds")
    primes = []
    cursor = PRIME_START
    while len(primes) < PRIME_COUNT:
        cursor = int(prevprime(cursor))
        if denominator % cursor:
            primes.append(cursor)
        cursor -= 1
    prime_product = math.prod(primes)
    require(prime_product > 2 * height_bound, "CRT modulus exceeds twice the coefficient bound")

    a_nodes = list(range(1, degree_bounds[0] + 2))
    b_nodes = list(range(degree_bounds[1] + 1))
    c_nodes = list(range(degree_bounds[2] + 1))
    checked_controls = 0
    for prime_index, prime in enumerate(primes, start=1):
        ma, mb, _, _ = [mod_matrix(matrix, prime) for matrix in (*graph, transverse)]
        u_mod = mod_matrix(u, prime)
        vt_mod = mod_matrix(v_transpose, prime)
        c_left_mod = mod_matrix(c_left, prime)
        c_right_mod = mod_matrix(c_right, prime)
        right = [u_mod[row] + c_left_mod[row] for row in range(33)]
        for a_value in a_nodes:
            for b_value in b_nodes:
                base = [
                    [
                        (
                            int(row == column)
                            + (a_value - 1) * ma[row][column]
                            + b_value * mb[row][column]
                        )
                        % prime
                        for column in range(33)
                    ]
                    for row in range(33)
                ]
                solved = solve_mod(base, right, prime)
                xu = [row[:7] for row in solved]
                xc = [row[7:] for row in solved]
                vt_xu = multiply_mod(vt_mod, xu, prime)
                vt_xc = multiply_mod(vt_mod, xc, prime)
                ct_xu = multiply_mod(c_right_mod, xu, prime)
                ct_xc = multiply_mod(c_right_mod, xc, prime)
                for c_value in c_nodes:
                    middle = identity_mod(6)
                    for row in range(6):
                        for column in range(6):
                            middle[row][column] = (
                                middle[row][column] + c_value * ct_xc[row][column]
                            ) % prime
                    correction_rhs = scale_mod(ct_xu, c_value, prime)
                    correction = solve_mod(middle, correction_rhs, prime)
                    transfer = subtract_mod(
                        vt_xu,
                        multiply_mod(vt_xc, correction, prime),
                        prime,
                    )
                    square = multiply_mod(transfer, transfer, prime)
                    if any(any(row) for row in square):
                        raise RuntimeError(
                            f"square-zero failure at p={prime}, A={a_value}, "
                            f"B={b_value}, C={c_value}"
                        )
                    checked_controls += 1
        print(
            f"[PASS] prime {prime_index}/{len(primes)}: {prime} on "
            f"{len(a_nodes) * len(b_nodes) * len(c_nodes)} controls",
            flush=True,
        )

    payload = {
        "experiment": "EXP-135",
        "decision": "proved_ambient_transverse_determinant_inertness",
        "core_size": len(core),
        "transverse_rank": u.cols,
        "transverse_square_rank": int((transverse**2).rank()),
        "transverse_cube_zero": True,
        "c_update_rank": c_left.cols,
        "degree_bounds": {
            "A": degree_bounds[0],
            "B": degree_bounds[1],
            "C": degree_bounds[2],
            "T": degree_bounds[3],
        },
        "grid_nodes": {"A": a_nodes, "B": b_nodes, "C": c_nodes},
        "primes": primes,
        "prime_product_bits": prime_product.bit_length(),
        "clearing_denominator": denominator,
        "coefficient_bound_bits": height_bound.bit_length(),
        "row_l1_bound_bits": [value.bit_length() for value in row_sums],
        "checked_modular_controls": checked_controls,
        "proof": (
            "The determinant difference has separate degrees at most "
            "(25,24,6,7). At each A/B/C grid point, H is invertible and the "
            "rank-seven determinant lemma transfer squares to zero, so the "
            "difference is zero as a polynomial in T. Tensor interpolation "
            "makes every cleared integer coefficient zero modulo every listed "
            "prime. Their product exceeds twice the explicit row-l1 coefficient "
            "bound, hence every characteristic-zero coefficient is zero."
        ),
        "identity": (
            "det(H(A,B,C)+T*K_(2,8)) = det(H(A,B,C)) in QQ[A,B,C,T]"
        ),
        "scope": (
            "Exact ambient T-inertness of the selected EXP-124 section only. "
            "The other graph/base sections, transverse d=0 quotient, complete "
            "five-coefficient restriction, (72,108), floor, and JC(2) remain open."
        ),
        "source_sha256": {
            str(path.relative_to(EXPERIMENTS)): digest(path)
            for path in (
                preflight.EXP123_RESULTS,
                preflight.EXP124_RESULTS,
                preflight.EXP133_RESULTS,
                preflight.EXP134_TERMINAL,
            )
        },
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    require(preflight.read_json(ARTIFACT)["decision"] == payload["decision"], "reloaded certificate")
    print(f"[PASS] certificate SHA256 {digest(ARTIFACT)}", flush=True)


if __name__ == "__main__":
    main()
