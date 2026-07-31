"""EXP-115: test every weighted residual component with alternative row bases."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

from sympy import Matrix, Poly, Rational, expand, factor, factor_list, symbols


HERE = Path(__file__).resolve().parent
E112_PATH = HERE.parent / "EXP-112-augmented-graph-core" / "run.py"
ARTIFACT = HERE / "artifacts" / "results.json"
PRIMES = (1009, 1013, 1019, 1031)

spec = importlib.util.spec_from_file_location("exp112", E112_PATH)
exp112 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp112)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def build_system():
    forced = exp112.forced_polynomial()
    directions = sorted(exp112.exp071.LOWER)
    _, complete_rows = exp112.complete_row_labels(forced, directions)
    constant_column = exp112.exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp112.exp071.NQ))
        if index != constant_column
    ]
    base = exp112.coefficient_matrix(
        forced, complete_rows, q_columns, include_rhs=True
    )
    wanted = ((0, 1), (0, 5), (1, 0))
    direction_matrices = {
        direction: exp112.coefficient_matrix(
            {direction: Fraction(1)},
            complete_rows,
            q_columns,
            include_rhs=False,
        )
        for direction in wanted
    }
    _, pinned_rows = base.T.rref()
    return base, direction_matrices, list(pinned_rows)


def matrix_at(base, directions, a, b, d):
    return (
        base
        + Rational(a.numerator, a.denominator) * directions[(0, 1)]
        + Rational(b.numerator, b.denominator) * directions[(0, 5)]
        + Rational(d.numerator - d.denominator, d.denominator)
        * directions[(1, 0)]
    )


def residue_polynomials():
    a, x, b = symbols("A X B")
    g = (
        30720000 * x**2 * b**4
        + 48828125 * x * b**11
        + 150000000 * x * b**8
        + 64000000 * x * b**5
        - 39321600 * x * b**2
        + 16777216
    )
    h = (
        4096 * x**3
        + 184320 * x**2 * b
        - 1800000 * x * b**5
        + 1843200 * x * b**2
        + 1953125 * b**9
        + 3000000 * b**6
        + 1536000 * b**3
        + 262144
    )
    linear = 125 * b**3 + 300 * b**2 + 240 * b + 16 * x + 64
    quadratic = (
        15625 * b**6
        - 37500 * b**5
        + 60000 * b**4
        - 2000 * b**3 * x
        - 56000 * b**3
        - 4800 * b**2 * x
        + 38400 * b**2
        + 7680 * b * x
        - 15360 * b
        + 256 * x**2
        - 1024 * x
        + 4096
    )
    require(expand(linear * quadratic) == h, "H63(d=1) factors as linear times quadratic in X=A^3")
    g_factorization = factor_list(g, x, b)
    require(
        len(g_factorization[1]) == 1
        and g_factorization[1][0][1] == 1
        and expand(g_factorization[1][0][0]) == g,
        "G54(d=1) is irreducible over Q[X,B]",
    )
    for name, expression in {
        "G54": g,
        "H_linear": linear,
        "H_quadratic": quadratic,
    }.items():
        specialization = expand(expression.subs(x, a**3))
        specialized_factors = factor_list(specialization, a, b)
        require(
            len(specialized_factors[1]) == 1
            and specialized_factors[1][0][1] == 1
            and expand(specialized_factors[1][0][0]) == specialization,
            f"{name}(A^3,B) is irreducible over Q[A,B]",
        )
    boundary = factor(
        x**4 * b**4 * (30720000 * x + 48828125 * b**7)
    )
    return x, b, g, h, linear, quadratic, boundary


def mod_entry(value, prime: int) -> int:
    numerator, denominator = value.as_numer_denom()
    denominator_mod = int(denominator) % prime
    if denominator_mod == 0:
        raise ZeroDivisionError(f"denominator vanishes modulo {prime}")
    return (
        int(numerator) % prime
        * pow(denominator_mod, -1, prime)
    ) % prime


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
    d: int,
    prime: int,
) -> list[list[int]]:
    c = (d - 1) % prime
    return [
        [
            (
                base[row][column]
                + a * da[row][column]
                + b * db[row][column]
                + c * dc[row][column]
            )
            % prime
            for column in range(len(base[0]))
        ]
        for row in range(len(base))
    ]


def independent_row_basis(
    rows: list[list[int]], prime: int
) -> list[int]:
    pivots: list[tuple[int, list[int]]] = []
    basis: list[int] = []
    for row_index, source in enumerate(rows):
        vector = source[:]
        for column, pivot in pivots:
            coefficient = vector[column]
            if coefficient:
                vector = [
                    (value - coefficient * pivot_value) % prime
                    for value, pivot_value in zip(vector, pivot)
                ]
        pivot_column = next(
            (column for column, value in enumerate(vector) if value),
            None,
        )
        if pivot_column is None:
            continue
        inverse = pow(vector[pivot_column], -1, prime)
        vector = [(value * inverse) % prime for value in vector]
        pivots.append((pivot_column, vector))
        basis.append(row_index)
        if len(basis) == len(rows[0]):
            break
    return basis


def determinant_mod(
    rows: list[list[int]], indices: list[int], prime: int
) -> int:
    matrix = [rows[index][:] for index in indices]
    determinant = 1
    size = len(matrix)
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if matrix[row][column] % prime
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            determinant = (-determinant) % prime
        pivot_value = matrix[column][column] % prime
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, size):
            coefficient = matrix[row][column] * inverse % prime
            if not coefficient:
                continue
            for target_column in range(column, size):
                matrix[row][target_column] = (
                    matrix[row][target_column]
                    - coefficient * matrix[column][target_column]
                ) % prime
    return determinant


def component_values(a: int, b: int, prime: int) -> dict[str, int]:
    x = pow(a, 3, prime)
    values = {
        "G": (
            30720000 * x**2 * b**4
            + 48828125 * x * b**11
            + 150000000 * x * b**8
            + 64000000 * x * b**5
            - 39321600 * x * b**2
            + 16777216
        ),
        "H_linear": (
            125 * b**3 + 300 * b**2 + 240 * b + 16 * x + 64
        ),
        "H_quadratic": (
            15625 * b**6
            - 37500 * b**5
            + 60000 * b**4
            - 2000 * b**3 * x
            - 56000 * b**3
            - 4800 * b**2 * x
            + 38400 * b**2
            + 7680 * b * x
            - 15360 * b
            + 256 * x**2
            - 1024 * x
            + 4096
        ),
    }
    return {name: value % prime for name, value in values.items()}


def modular_component_witnesses(
    base: Matrix,
    directions: dict[tuple[int, int], Matrix],
    pinned_rows: list[int],
) -> tuple[int, dict[str, object]]:
    targets = ("G", "H_linear", "H_quadratic")
    for prime in PRIMES:
        print(f"[INFO] trying good prime {prime}", flush=True)
        base_mod = matrix_mod(base, prime)
        da = matrix_mod(directions[(0, 1)], prime)
        db = matrix_mod(directions[(0, 5)], prime)
        dc = matrix_mod(directions[(1, 0)], prime)
        pinned_control = determinant_mod(base_mod, pinned_rows, prime)
        if not pinned_control:
            print(f"[INFO] prime {prime} rejects the pinned basis", flush=True)
            continue

        witnesses: dict[str, object] = {}
        for target in targets:
            candidates = 0
            decided = False
            for b in range(prime):
                if decided:
                    break
                for a in range(prime):
                    values = component_values(a, b, prime)
                    if values[target] != 0:
                        continue
                    if any(
                        values[other] == 0
                        for other in targets
                        if other != target
                    ):
                        continue
                    candidates += 1
                    evaluated = combine_mod(
                        base_mod, da, db, dc, a, b, 1, prime
                    )
                    selected = determinant_mod(
                        evaluated, pinned_rows, prime
                    )
                    if selected != 0:
                        raise AssertionError(
                            f"selected determinant nonzero on {target}"
                        )
                    basis = independent_row_basis(evaluated, prime)
                    if len(basis) != 125:
                        if candidates >= 24:
                            break
                        continue
                    alternative = determinant_mod(evaluated, basis, prime)
                    require(
                        alternative != 0,
                        f"{target} has a nonzero alternative minor mod {prime}",
                    )
                    replacements = len(set(basis) - set(pinned_rows))
                    witnesses[target] = {
                        "point": {"a": a, "b": b, "d": 1},
                        "factor_values": values,
                        "selected_determinant_mod_p": selected,
                        "alternative_determinant_mod_p": alternative,
                        "row_basis": basis,
                        "row_replacements": replacements,
                        "candidates_tested": candidates,
                    }
                    decided = True
                    break
            if not decided:
                print(
                    f"[INFO] no full-rank {target} witness mod {prime}",
                    flush=True,
                )
                break
        if len(witnesses) == len(targets):
            require(
                all(
                    witness["factor_values"][target] == 0
                    for target, witness in witnesses.items()
                ),
                "every modular witness lies on its declared component",
            )
            return prime, {
                "pinned_control_determinant": pinned_control,
                "components": witnesses,
            }
    raise RuntimeError("no declared good prime decided all open components")


def exact_witness(
    name: str,
    point: tuple[Fraction, Fraction, Fraction],
    base: Matrix,
    directions: dict[tuple[int, int], Matrix],
    pinned_rows: list[int],
    prime: int,
) -> dict[str, object]:
    evaluated = matrix_at(base, directions, *point)
    reduced = matrix_mod(evaluated, prime)
    basis = independent_row_basis(reduced, prime)
    require(len(basis) == 125, f"{name} has row rank 125 modulo {prime}")
    selected = evaluated.extract(pinned_rows, range(125)).det(
        method="domain-ge"
    )
    require(selected == 0, f"{name} lies on the selected-minor residual")
    alternative = evaluated.extract(basis, range(125)).det(
        method="domain-ge"
    )
    require(alternative != 0, f"{name} has an exact nonzero alternative minor")
    alternative_mod = determinant_mod(reduced, basis, prime)
    require(
        mod_entry(alternative, prime) == alternative_mod != 0,
        f"{name} exact determinant agrees modulo {prime}",
    )
    determinant_text = str(alternative)
    return {
        "point": {
            "a": str(point[0]),
            "b": str(point[1]),
            "d": str(point[2]),
        },
        "selected_determinant": "0",
        "alternative_determinant": determinant_text,
        "alternative_determinant_sha256": hashlib.sha256(
            determinant_text.encode("utf-8")
        ).hexdigest().upper(),
        "row_basis": basis,
        "row_replacements": len(set(basis) - set(pinned_rows)),
    }


def boundary_kernel_analysis(
    base: Matrix,
    directions: dict[tuple[int, int], Matrix],
) -> dict[str, object]:
    base_boundary = base - directions[(1, 0)]
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

    coefficient_checks = {
        "constant": base_boundary * k0,
        "a": base_boundary * ea + da * k0,
        "b": base_boundary * eb + db * k0,
        "a2": da * ea,
        "ab": da * eb + db * ea,
        "b2": db * eb,
    }
    for name, vector in coefficient_checks.items():
        require(
            all(value == 0 for value in vector),
            f"d=0 universal kernel coefficient {name} vanishes exactly",
        )

    points = {
        "boundary_a_zero": (
            Fraction(0),
            Fraction(1),
            Fraction(0),
        ),
        "boundary_b_zero": (
            Fraction(1),
            Fraction(0),
            Fraction(0),
        ),
        "boundary_relation": (
            Fraction(-9),
            Fraction(12, 5),
            Fraction(0),
        ),
    }
    profiles: dict[str, object] = {}
    for name, point in points.items():
        evaluated = matrix_at(base, directions, *point)
        augmented_kernel = evaluated.nullspace()
        matrix_kernel = evaluated[:, :124].nullspace()
        require(
            len(augmented_kernel) == 1,
            f"{name} has exact augmented rank 124",
        )
        require(
            len(matrix_kernel) == 1,
            f"{name} has exact coefficient rank 123",
        )
        predicted = k0 + Rational(point[0]) * ea + Rational(point[1]) * eb
        require(
            evaluated * predicted == Matrix.zeros(302, 1),
            f"{name} specializes the universal right kernel",
        )
        require(
            predicted[124] == 0,
            f"{name} kernel has zero target-column coordinate",
        )
        profiles[name] = {
            "point": {
                "a": str(point[0]),
                "b": str(point[1]),
                "d": str(point[2]),
            },
            "coefficient_rank": 123,
            "augmented_rank": 124,
            "inconsistent": True,
        }

    support = {
        str(index): str(value)
        for index, value in enumerate(k0)
        if value
    }
    support["0"] = "a"
    support["4"] = "b"
    return {
        "universal_kernel_support": support,
        "identity": (
            "A(a,b,d=0) * (k0 + a*e_0 + b*e_4) = 0 "
            "coefficientwise over Q[a,b]"
        ),
        "target_coordinate": 0,
        "exact_component_profiles": profiles,
        "uniform_consequence": (
            "rank(M)<=123 and rank([M|b])<=124 on d=0; "
            "a uniform nonzero 124-minor cover is still required."
        ),
    }


def main() -> None:
    started = time.time()
    base, directions, pinned_rows = build_system()
    require(base.shape == (302, 125), "complete effective system is 302 by 125")
    require(len(pinned_rows) == 125, "pinned exact row basis has size 125")

    x, b, g, h, linear, quadratic, boundary = residue_polynomials()
    require(
        Poly(g, x, b, domain="QQ").total_degree() == 12,
        "G54(d=1) has total degree 12 in (X,B)",
    )
    require(
        expand(linear.subs({x: 0, b: Rational(-4, 5)})) == 0
        and expand(quadratic.subs({x: 0, b: Rational(-4, 5)}))
        != 0,
        "(a,b,d)=(0,-4/5,1) isolates the H-linear component",
    )

    prime, modular = modular_component_witnesses(
        base, directions, pinned_rows
    )

    rational = {
        "H_linear_open": exact_witness(
            "H_linear_open",
            (Fraction(0), Fraction(-4, 5), Fraction(1)),
            base,
            directions,
            pinned_rows,
            prime,
        )
    }

    require(
        30720000 * (-9) ** 3
        + Rational(48828125) * Rational(12, 5) ** 7
        == 0,
        "the rational boundary-relation witness satisfies its component equation",
    )
    boundary_analysis = boundary_kernel_analysis(base, directions)

    replacements = [
        witness["row_replacements"]
        for witness in modular["components"].values()
    ] + [
        witness["row_replacements"]
        for witness in rational.values()
    ]
    prediction_small_transition = max(replacements) <= 5
    print(
        f"[{'PASS' if prediction_small_transition else 'REFUTED'}] "
        "prediction: every witness needs at most five row replacements",
        flush=True,
    )

    artifact = {
        "experiment": "EXP-115",
        "open_chart": {
            "coordinates": "a=A*u^7, b=B*u^3, d=u^9",
            "G_in_X_B": str(g),
            "H_in_X_B": str(h),
            "H_linear": str(linear),
            "H_quadratic": str(quadratic),
            "good_prime": prime,
            "witnesses": modular,
        },
        "boundary": {
            "selected_factor_support": str(boundary),
            "kernel_analysis": boundary_analysis,
        },
        "pinned_rows": pinned_rows,
        "predictions": {
            "G_irreducible_over_Q_X_B": True,
            "H_splits_linear_quadratic_over_Q_X_B": True,
            "all_open_components_have_alternative_minor": True,
            "all_boundary_components_have_alternative_minor": False,
            "boundary_rank_125_prediction_refuted": True,
            "boundary_universal_right_kernel_confirmed": True,
            "all_transitions_at_most_five_rows": prediction_small_transition,
        },
        "elapsed_seconds": time.time() - started,
        "scope": (
            "The d!=0 components are generically removed. On d=0 a universal "
            "right kernel lowers the relevant rank test to 123/124; a uniform "
            "124-minor cover, the 24-parameter core, (72,108), and JC(2) remain open."
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
