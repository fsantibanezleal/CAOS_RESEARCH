"""EXP-133: modular SCC preflight for the principal-open (2,8) lift."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import symbols, sympify


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
EXP124_RUN = EXPERIMENTS / "EXP-124-rational-graph-alternative-chart" / "run.py"
EXP123_RESULT = (
    EXPERIMENTS
    / "EXP-123-direction-29-symbolic-lift"
    / "artifacts"
    / "results.json"
)
EXP124_RESULT = (
    EXPERIMENTS
    / "EXP-124-rational-graph-alternative-chart"
    / "artifacts"
    / "results.json"
)
EXP129_RESULT = (
    EXPERIMENTS / "EXP-129-f7-crt-minor-atlas" / "artifacts" / "results.json"
)
EXP130_STRUCTURAL = (
    EXPERIMENTS
    / "EXP-130-base-locus-quotient-atlas"
    / "artifacts"
    / "structural-exact-worker.json"
)
PRIMES = (1009, 1153)
TARGET = (2, 8)
MAX_SECONDS = 300.0


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


exp124 = load_module("exp124_for_exp133", EXP124_RUN)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def persist(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def mod_entry(value, prime: int) -> int:
    numerator, denominator = value.as_numer_denom()
    return int(numerator) % prime * pow(int(denominator) % prime, -1, prime) % prime


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    size = len(work)
    determinant = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            multiplier = work[row][column] * inverse % prime
            for target in range(column + 1, size):
                work[row][target] = (
                    work[row][target] - multiplier * work[column][target]
                ) % prime
    return determinant % prime


def normalized_operator(
    matrix: list[list[int]], direction: list[list[int]], prime: int
) -> list[list[int]]:
    size = len(matrix)
    work = [
        [entry % prime for entry in matrix[row]]
        + [entry % prime for entry in direction[row]]
        for row in range(size)
    ]
    width = 2 * size
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot is None:
            raise ArithmeticError("singular normalization matrix")
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
        inverse = pow(work[column][column], -1, prime)
        for target in range(column, width):
            work[column][target] = work[column][target] * inverse % prime
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            for target in range(column, width):
                work[row][target] = (
                    work[row][target] - multiplier * work[column][target]
                ) % prime
    return [row[size:] for row in work]


def strongly_connected_components(adjacency: list[set[int]]) -> list[list[int]]:
    index = 0
    indices = [-1] * len(adjacency)
    low = [0] * len(adjacency)
    stack: list[int] = []
    on_stack = [False] * len(adjacency)
    components: list[list[int]] = []

    def visit(vertex: int) -> None:
        nonlocal index
        indices[vertex] = low[vertex] = index
        index += 1
        stack.append(vertex)
        on_stack[vertex] = True
        for target in adjacency[vertex]:
            if indices[target] < 0:
                visit(target)
                low[vertex] = min(low[vertex], low[target])
            elif on_stack[target]:
                low[vertex] = min(low[vertex], indices[target])
        if low[vertex] == indices[vertex]:
            component = []
            while True:
                target = stack.pop()
                on_stack[target] = False
                component.append(target)
                if target == vertex:
                    break
            components.append(sorted(component))

    for vertex in range(len(adjacency)):
        if indices[vertex] < 0:
            visit(vertex)
    return components


def cyclic_components(matrix: list[list[int]]) -> list[list[int]]:
    adjacency = [
        {column for column, value in enumerate(row) if value}
        for row in matrix
    ]
    components = strongly_connected_components(adjacency)
    cyclic = [
        component
        for component in components
        if len(component) > 1
        or matrix[component[0]][component[0]] != 0
    ]
    return sorted(cyclic, key=lambda component: (-len(component), component))


def poly_trim(poly: list[int], prime: int) -> list[int]:
    result = [coefficient % prime for coefficient in poly]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_add(left: list[int], right: list[int], prime: int) -> list[int]:
    size = max(len(left), len(right))
    result = [0] * size
    for index in range(size):
        result[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % prime
    return poly_trim(result, prime)


def poly_scale(poly: list[int], scalar: int, prime: int) -> list[int]:
    return poly_trim([scalar * coefficient for coefficient in poly], prime)


def poly_mul(left: list[int], right: list[int], prime: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a_value in enumerate(left):
        for j, b_value in enumerate(right):
            result[i + j] = (result[i + j] + a_value * b_value) % prime
    return poly_trim(result, prime)


def interpolate(values: list[int], prime: int) -> list[int]:
    result = [0]
    for index, value in enumerate(values):
        basis = [1]
        denominator = 1
        for other in range(len(values)):
            if other == index:
                continue
            basis = poly_mul(basis, [(-other) % prime, 1], prime)
            denominator = denominator * (index - other) % prime
        result = poly_add(
            result,
            poly_scale(basis, value * pow(denominator, -1, prime), prime),
            prime,
        )
    return poly_trim(result, prime)


def poly_divmod(
    numerator: list[int], denominator: list[int], prime: int
) -> tuple[list[int], list[int]]:
    remainder = poly_trim(numerator, prime)
    denominator = poly_trim(denominator, prime)
    if denominator == [0]:
        raise ZeroDivisionError
    quotient = [0] * max(1, len(remainder) - len(denominator) + 1)
    inverse = pow(denominator[-1], -1, prime)
    while remainder != [0] and len(remainder) >= len(denominator):
        degree = len(remainder) - len(denominator)
        coefficient = remainder[-1] * inverse % prime
        quotient[degree] = coefficient
        for index, value in enumerate(denominator):
            remainder[index + degree] = (
                remainder[index + degree] - coefficient * value
            ) % prime
        remainder = poly_trim(remainder, prime)
    return poly_trim(quotient, prime), remainder


def poly_gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    left = poly_trim(left, prime)
    right = poly_trim(right, prime)
    while right != [0]:
        _, remainder = poly_divmod(left, right, prime)
        left, right = right, remainder
    inverse = pow(left[-1], -1, prime)
    return poly_scale(left, inverse, prime)


def component_polynomial(
    operator: list[list[int]], component: list[int], prime: int
) -> list[int]:
    size = len(component)
    values = []
    for parameter in range(size + 1):
        block = [
            [
                ((1 if row == column else 0) + parameter * operator[source][target])
                % prime
                for column, target in enumerate(component)
            ]
            for row, source in enumerate(component)
        ]
        values.append(determinant_mod(block, prime))
    polynomial = interpolate(values, prime)
    require(
        all(
            sum(coefficient * pow(parameter, degree, prime) for degree, coefficient in enumerate(polynomial))
            % prime
            == value
            for parameter, value in enumerate(values)
        ),
        f"interpolated size-{size} cyclic determinant",
    )
    return polynomial


def section_polynomial(
    matrix: list[list[int]], direction: list[list[int]], prime: int
) -> dict[str, object]:
    operator = normalized_operator(matrix, direction, prime)
    components = cyclic_components(operator)
    polynomial = [1]
    component_records = []
    for component in components:
        factor = component_polynomial(operator, component, prime)
        polynomial = poly_mul(polynomial, factor, prime)
        component_records.append(
            {
                "size": len(component),
                "degree_T": len(factor) - 1,
                "vertices": component,
                "coefficients_ascending": factor,
            }
        )
    return {
        "degree_T": len(polynomial) - 1,
        "coefficients_ascending": polynomial,
        "cyclic_component_sizes": [len(component) for component in components],
        "cyclic_support": sum(len(component) for component in components),
        "components": component_records,
    }


def selected_matrix(
    arrays: dict[str, list[list[int]]],
    rows: list[int],
    a_value: int,
    b_value: int,
    c_value: int,
    prime: int,
) -> list[list[int]]:
    return [
        [
            (
                arrays["base"][row][column]
                + a_value * arrays["A"][row][column]
                + b_value * arrays["B"][row][column]
                + c_value * arrays["C"][row][column]
            )
            % prime
            for column in range(125)
        ]
        for row in rows
    ]


def selected_direction(
    arrays: dict[str, list[list[int]]], rows: list[int]
) -> list[list[int]]:
    return [arrays["T"][row][:] for row in rows]


def main() -> None:
    started = time.time()
    e123 = read_json(EXP123_RESULT)
    e124 = read_json(EXP124_RESULT)
    e129 = read_json(EXP129_RESULT)
    e130 = read_json(EXP130_STRUCTURAL)
    sections = {
        "EXP-123-shared": list(e123["shared_rows"]),
        "EXP-124-graph": list(e124["selected_rows"]),
        "EXP-129-atlas-1": list(e129["exact_atlas"][0]["rows"]),
        "EXP-129-atlas-2": list(e129["exact_atlas"][1]["rows"]),
        "EXP-130-structural": list(e130["rows"]),
    }
    require(all(len(rows) == 125 for rows in sections.values()), "loaded five accepted 125-row sections")
    require(all(len(set(rows)) == 125 for rows in sections.values()), "all persisted row sections have distinct rows")

    base, directions = exp124.build_full_system()
    forced = exp124.exp112.forced_polynomial()
    all_directions = sorted(exp124.exp112.exp071.LOWER)
    _, complete_rows = exp124.exp112.complete_row_labels(
        forced, all_directions
    )
    constant_column = exp124.exp112.exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp124.exp112.exp071.NQ))
        if index != constant_column
    ]
    directions[TARGET] = exp124.exp112.coefficient_matrix(
        {TARGET: exp124.exp112.Fraction(1)},
        complete_rows,
        q_columns,
        include_rhs=False,
    )
    require(base.shape == (302, 125), "rebuilt original 302 by 125 augmented matrix")
    for direction in ((0, 1), (0, 5), (2, 9), TARGET):
        require(direction in directions, f"rebuilt direction {direction}")

    x, b = symbols("X B")
    r_expression = sympify(e123["invariant_reduction"]["R_X_B"], locals={"X": x, "B": b})
    s_expression = sympify(e123["invariant_reduction"]["S_X_B"], locals={"X": x, "B": b})
    payload: dict[str, object] = {
        "experiment": "EXP-133",
        "decision": "preflight_running",
        "target_direction": list(TARGET),
        "sections": {name: {"rows": rows} for name, rows in sections.items()},
        "source_sha256": {
            str(path.relative_to(EXPERIMENTS)): digest(path)
            for path in (EXP123_RESULT, EXP124_RESULT, EXP129_RESULT, EXP130_STRUCTURAL)
        },
        "prime_records": {},
    }
    persist(payload, CHECKPOINT)

    for prime in PRIMES:
        require(time.time() - started < MAX_SECONDS, "preflight remains inside hard time gate")
        arrays = {
            "base": exp124.exp115.matrix_mod(base, prime),
            "A": exp124.exp115.matrix_mod(directions[(0, 1)], prime),
            "B": exp124.exp115.matrix_mod(directions[(0, 5)], prime),
            "C": exp124.exp115.matrix_mod(directions[(2, 9)], prime),
            "T": exp124.exp115.matrix_mod(directions[TARGET], prime),
        }
        controls = []
        for a_value in (1, 2, 3, 4, 5, 7):
            for b_value in (0, 1, 2, 3, 5, 7, 11):
                x_value = pow(a_value, 3, prime)
                r_value = exp124.polynomial_value_mod(
                    r_expression, x, b, x_value, b_value, prime
                )
                s_value = exp124.polynomial_value_mod(
                    s_expression, x, b, x_value, b_value, prime
                )
                if not s_value:
                    continue
                c_value = -r_value * pow(a_value * a_value * s_value, -1, prime) % prime
                matrices = {
                    name: selected_matrix(
                        arrays, rows, a_value, b_value, c_value, prime
                    )
                    for name, rows in sections.items()
                }
                determinants = {
                    name: determinant_mod(matrix, prime)
                    for name, matrix in matrices.items()
                }
                if not all(determinants.values()):
                    continue
                controls.append(
                    {
                        "A": a_value,
                        "B": b_value,
                        "C": c_value,
                        "X": x_value,
                        "R": r_value,
                        "S": s_value,
                        "determinants_T0": determinants,
                        "matrices": matrices,
                    }
                )
                if len(controls) == 2:
                    break
            if len(controls) == 2:
                break
        require(len(controls) == 2, f"found two common full-rank graph controls modulo {prime}")

        public_controls = []
        for control in controls:
            section_records = {}
            for name, rows in sections.items():
                require(time.time() - started < MAX_SECONDS, "preflight remains inside hard time gate")
                record = section_polynomial(
                    control["matrices"][name],
                    selected_direction(arrays, rows),
                    prime,
                )
                section_records[name] = record
                print(
                    f"[INFO] p={prime} A={control['A']} B={control['B']} "
                    f"{name}: degree_T={record['degree_T']} "
                    f"cyclic_support={record['cyclic_support']}",
                    flush=True,
                )
            gcd_records = {}
            names = list(sections)
            for left_index, left in enumerate(names):
                for right in names[left_index + 1 :]:
                    gcd_value = poly_gcd(
                        section_records[left]["coefficients_ascending"],
                        section_records[right]["coefficients_ascending"],
                        prime,
                    )
                    gcd_records[f"{left}|{right}"] = {
                        "degree_T": len(gcd_value) - 1,
                        "coefficients_ascending": gcd_value,
                    }
            public_controls.append(
                {
                    key: control[key]
                    for key in ("A", "B", "C", "X", "R", "S", "determinants_T0")
                }
                | {
                    "sections": section_records,
                    "pairwise_gcds": gcd_records,
                }
            )
        payload["prime_records"][str(prime)] = {"controls": public_controls}
        persist(payload, CHECKPOINT)

    all_controls = [
        control
        for record in payload["prime_records"].values()
        for control in record["controls"]
    ]
    section_degrees = {
        name: [control["sections"][name]["degree_T"] for control in all_controls]
        for name in sections
    }
    section_supports = {
        name: [control["sections"][name]["cyclic_support"] for control in all_controls]
        for name in sections
    }
    prediction_1 = all(len(set(degrees)) == 1 for degrees in section_degrees.values())
    prediction_2 = any(max(degrees) <= 1 for degrees in section_degrees.values())
    prediction_3 = all(max(supports) <= 45 for supports in section_supports.values())
    graph_pair = "EXP-123-shared|EXP-124-graph"
    prediction_4 = all(
        control["pairwise_gcds"][graph_pair]["degree_T"] == 0
        for control in all_controls
    )
    payload.update(
        {
            "decision": (
                "bounded_existing_atlas_lift_selected"
                if prediction_2 and prediction_3 and prediction_4
                else "residual_row_reselection_required"
            ),
            "elapsed_seconds": time.time() - started,
            "degree_ledger": section_degrees,
            "cyclic_support_ledger": section_supports,
            "predictions": {
                "p1_cross_prime_degree_stability": prediction_1,
                "p2_inert_or_affine_section_exists": prediction_2,
                "p3_all_cyclic_support_at_most_45": prediction_3,
                "p4_graph_pair_has_unit_T_gcd_on_controls": prediction_4,
            },
            "scope": (
                "Modular graph-control preflight selecting the next exact worker. "
                "No graph, base-locus, five-coefficient, (72,108), floor, or JC(2) closure."
            ),
        }
    )
    persist(payload, ARTIFACT)
    print(
        f"[DONE] {payload['decision']} in {payload['elapsed_seconds']:.2f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
