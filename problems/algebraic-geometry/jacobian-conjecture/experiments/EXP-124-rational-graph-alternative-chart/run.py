"""EXP-124: select and reconstruct an alternative chart on the rational graph."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

from sympy import Poly, QQ, Rational, expand, factor_list, gcd, sympify, symbols


HERE = Path(__file__).resolve().parent
E123_PATH = HERE.parent / "EXP-123-direction-29-symbolic-lift" / "run.py"
E123_ARTIFACT = (
    HERE.parent
    / "EXP-123-direction-29-symbolic-lift"
    / "artifacts"
    / "results.json"
)
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
WORKER_ARTIFACT = HERE / "artifacts" / "symbolic-worker.json"
WORKER = HERE / "symbolic_worker.py"
PRIMES = (1009, 1013)
TARGET = (2, 9)
WORKER_TIMEOUT_SECONDS = 300
TOTAL_GATE_SECONDS = 390

spec = importlib.util.spec_from_file_location("exp123", E123_PATH)
exp123 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp123)
exp122 = exp123.exp122
exp112 = exp123.exp112
exp115 = exp123.exp115


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


def build_full_system():
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
    directions = {
        direction: exp112.coefficient_matrix(
            {direction: exp112.Fraction(1)},
            complete_rows,
            q_columns,
            include_rhs=False,
        )
        for direction in wanted
    }
    return base, directions


def mod_entry(value, prime: int) -> int:
    numerator, denominator = value.as_numer_denom()
    return int(numerator) % prime * pow(int(denominator) % prime, -1, prime) % prime


def polynomial_value_mod(expression, x, b, xv, bv, prime):
    value = 0
    for (x_power, b_power), coefficient in Poly(
        expression, x, b, domain=QQ
    ).terms():
        value += (
            mod_entry(coefficient, prime)
            * pow(xv, x_power, prime)
            * pow(bv, b_power, prime)
        )
    return value % prime


def combine_mod(base, da, db, dc, a, b, c, prime):
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


def select_modular_bases(base, directions, shared_rows, r, s, x, b):
    records = {}
    basis_primes: dict[tuple[int, ...], set[int]] = {}
    for prime in PRIMES:
        matrices = {
            "base": exp115.matrix_mod(base, prime),
            "A": exp115.matrix_mod(directions[(0, 1)], prime),
            "B": exp115.matrix_mod(directions[(0, 5)], prime),
            "C": exp115.matrix_mod(directions[TARGET], prime),
        }
        points = []
        profiles: dict[str, int] = {}
        candidates = []
        for a_value in range(1, 17):
            for b_value in range(16):
                xv = pow(a_value, 3, prime)
                rv = polynomial_value_mod(r, x, b, xv, b_value, prime)
                sv = polynomial_value_mod(s, x, b, xv, b_value, prime)
                if sv == 0:
                    continue
                yv = -rv * pow(sv, -1, prime) % prime
                c_value = yv * pow(a_value * a_value, -1, prime) % prime
                evaluated = combine_mod(
                    matrices["base"],
                    matrices["A"],
                    matrices["B"],
                    matrices["C"],
                    a_value,
                    b_value,
                    c_value,
                    prime,
                )
                shared_det = exp115.determinant_mod(
                    evaluated, shared_rows, prime
                )
                require(
                    shared_det == 0,
                    f"p={prime} point ({a_value},{b_value}) lies on graph",
                )
                basis = exp115.independent_row_basis(evaluated, prime)
                coefficient_basis = exp115.independent_row_basis(
                    [row[:124] for row in evaluated], prime
                )
                profile = f"{len(coefficient_basis)}/{len(basis)}"
                profiles[profile] = profiles.get(profile, 0) + 1
                points.append(
                    {
                        "A": a_value,
                        "B": b_value,
                        "X": xv,
                        "Y": yv,
                        "C": c_value,
                        "rank_profile": profile,
                    }
                )
                if len(basis) == 125 and tuple(basis) != tuple(shared_rows):
                    key = tuple(basis)
                    basis_primes.setdefault(key, set()).add(prime)
                    if not any(item["row_basis"] == basis for item in candidates):
                        candidates.append(
                            {
                                "row_basis": basis,
                                "row_replacements_from_shared": len(
                                    set(basis) - set(shared_rows)
                                ),
                                "first_point": points[-1],
                            }
                        )
                if len(points) >= 20 or len(candidates) >= 3:
                    break
            if len(points) >= 20 or len(candidates) >= 3:
                break
        records[str(prime)] = {
            "points": points,
            "rank_profiles": profiles,
            "candidates": candidates,
        }
        print(
            f"[INFO] p={prime}: {len(points)} graph points, "
            f"{len(candidates)} alternative bases",
            flush=True,
        )
    cross = [
        basis for basis, primes in basis_primes.items() if len(primes) == 2
    ]
    if cross:
        selected = min(
            cross,
            key=lambda basis: (len(set(basis) - set(shared_rows)), basis),
        )
        evidence = "cross_prime"
    else:
        selected = min(
            basis_primes,
            key=lambda basis: (
                -len(basis_primes[basis]),
                len(set(basis) - set(shared_rows)),
                basis,
            ),
        )
        evidence = "single_prime"
    return records, list(selected), evidence


def exact_candidate_profile(base, directions, rows):
    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: matrix.extract(rows, range(125))
        for direction, matrix in directions.items()
    }
    controls = (
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, 0),
        (1, 0, 1),
        (2, 1, 1),
        (-1, 1, 1),
    )
    attempts = []
    for a_value, b_value, c_value in controls:
        matrix = (
            selected_base
            + a_value * selected_directions[(0, 1)]
            + b_value * selected_directions[(0, 5)]
            + c_value * selected_directions[TARGET]
        )
        determinant = matrix.det(method="domain-ge")
        attempts.append(
            {
                "A": a_value,
                "B": b_value,
                "C": c_value,
                "determinant": str(determinant),
            }
        )
        if determinant != 0:
            inverse = matrix.inv()
            normalized = {
                direction: inverse * value
                for direction, value in selected_directions.items()
            }
            components = exp122.cyclic_components(list(normalized.values()))
            return (
                selected_base,
                selected_directions,
                matrix,
                determinant,
                normalized,
                components,
                (a_value, b_value, c_value),
                attempts,
            )
    raise AssertionError("no rational anchor found for selected graph basis")


def invariant_reduce(expression, a, b, c, x, y):
    polynomial = Poly(expression, a, b, c, domain=QQ)
    shifted = [
        (a_power - 2 * c_power, b_power, c_power, coefficient)
        for (a_power, b_power, c_power), coefficient in polynomial.terms()
    ]
    valuation = min(item[0] for item in shifted)
    require(
        all((item[0] - valuation) % 3 == 0 for item in shifted),
        "alternative determinant has one invariant A-residue class",
    )
    reduced = expand(
        sum(
            coefficient
            * x ** ((a_power - valuation) // 3)
            * b**b_power
            * y**c_power
            for a_power, b_power, c_power, coefficient in shifted
        )
    )
    require(
        expand(
            a**valuation
            * reduced.subs({x: a**3, y: a**2 * c})
            - expression
        )
        == 0,
        "reconstructed alternative determinant from invariant coordinates",
    )
    return valuation, reduced


def main() -> None:
    started = time.time()
    e123 = json.loads(E123_ARTIFACT.read_text(encoding="utf-8"))
    x, b, y = symbols("X B Y")
    a, c = symbols("A C")
    r = sympify(e123["invariant_reduction"]["R_X_B"], locals={"X": x, "B": b})
    s = sympify(e123["invariant_reduction"]["S_X_B"], locals={"X": x, "B": b})
    require(
        gcd(Poly(r, x, b, domain=QQ), Poly(s, x, b, domain=QQ)).total_degree()
        == 0,
        "reproduced EXP-123 primitive gcd one",
    )
    base, directions = build_full_system()
    shared_rows = list(e123["shared_rows"])
    modular, selected_rows, selection_evidence = select_modular_bases(
        base, directions, shared_rows, r, s, x, b
    )
    require(selected_rows != shared_rows, "selected basis differs from shared basis")
    payload: dict[str, object] = {
        "experiment": "EXP-124",
        "modular_selection": modular,
        "selected_rows": selected_rows,
        "selection_evidence": selection_evidence,
    }
    persist(payload, CHECKPOINT)

    (
        selected_base,
        selected_directions,
        anchor,
        anchor_det,
        normalized,
        components,
        anchor_point,
        anchor_attempts,
    ) = exact_candidate_profile(base, directions, selected_rows)
    largest = len(components[0])
    require(largest <= 60, "selected exact largest cyclic block is at most 60")
    payload.update(
        {
            "anchor": {
                "point": list(anchor_point),
                "determinant": str(anchor_det),
                "attempts": anchor_attempts,
            },
            "cyclic_component_sizes": [len(item) for item in components],
        }
    )
    persist(payload, CHECKPOINT)

    worker = subprocess.run(
        [sys.executable, str(WORKER)],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=WORKER_TIMEOUT_SECONDS,
        check=False,
    )
    print(worker.stdout, end="", flush=True)
    if worker.stderr:
        print(worker.stderr, file=sys.stderr, end="", flush=True)
    require(worker.returncode == 0, "exact symbolic worker completed")
    worker_record = json.loads(WORKER_ARTIFACT.read_text(encoding="utf-8"))
    expression = sympify(
        worker_record["determinant_ratio"],
        locals={"A": a, "B": b, "C": c},
    )
    valuation, invariant = invariant_reduce(expression, a, b, c, x, y)
    invariant_poly = Poly(invariant, y, domain="QQ[X,B]")
    y_degree = int(invariant_poly.degree())
    numerator = expand(
        sum(
            invariant_poly.nth(power)
            * (-r) ** power
            * s ** (y_degree - power)
            for power in range(y_degree + 1)
        )
    )
    numerator_poly = Poly(numerator, x, b, domain=QQ)
    require(not numerator_poly.is_zero, "alternative graph numerator is nonzero")
    factors = factor_list(numerator, x, b)
    controls = []
    for av, bv, cv in ((1, 0, 0), (1, 0, 1), (2, 1, 1), (-1, 1, 1)):
        direct = (
            selected_base
            + av * selected_directions[(0, 1)]
            + bv * selected_directions[(0, 5)]
            + cv * selected_directions[TARGET]
        ).det(method="domain-ge") / anchor_det
        predicted = expression.subs({a: av, b: bv, c: cv})
        require(direct == predicted, f"direct determinant control ({av},{bv},{cv})")
        controls.append(
            {
                "point": [av, bv, cv],
                "ratio": str(direct),
            }
        )
    payload.update(
        {
            "symbolic_worker": worker_record,
            "determinant_A_valuation": valuation,
            "invariant_determinant_X_B_Y": str(invariant),
            "invariant_Y_degree": y_degree,
            "graph_numerator": str(numerator),
            "graph_numerator_monomial_count": len(numerator_poly.terms()),
            "graph_numerator_total_degree": numerator_poly.total_degree(),
            "graph_numerator_factorization": {
                "coefficient": str(factors[0]),
                "factors": [
                    {"factor": str(factor), "multiplicity": multiplicity}
                    for factor, multiplicity in factors[1]
                ],
            },
            "gcd_with_R": str(
                gcd(numerator_poly, Poly(r, x, b, domain=QQ)).monic().as_expr()
            ),
            "gcd_with_S": str(
                gcd(numerator_poly, Poly(s, x, b, domain=QQ)).monic().as_expr()
            ),
            "direct_exact_controls": controls,
            "predictions": {
                "p1_rank_profile_124_125_both_primes": all(
                    item["rank_profiles"].get("124/125", 0) > 0
                    for item in modular.values()
                ),
                "p2_cross_prime_alternative_basis": (
                    selection_evidence == "cross_prime"
                ),
                "p3_largest_scc_at_most_60": largest <= 60,
                "p4_graph_restriction_nonzero": True,
                "p5_graph_numerator_nonconstant": (
                    numerator_poly.total_degree() > 0
                ),
            },
            "elapsed_seconds": time.time() - started,
            "scope": (
                "Exact alternative selected chart on the EXP-123 rational "
                "graph. A nonconstant numerator removes only a dense graph "
                "open and does not close the graph, A=0, the four-parameter "
                "restriction, (72,108), the degree floor, or JC(2)."
            ),
        }
    )
    require(
        payload["elapsed_seconds"] <= TOTAL_GATE_SECONDS,
        "EXP-124 remains within total compute gate",
    )
    persist(payload, ARTIFACT)
    digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(
        f"[INFO] graph numerator degree={numerator_poly.total_degree()}, "
        f"terms={len(numerator_poly.terms())}, "
        f"elapsed={payload['elapsed_seconds']:.2f} s",
        flush=True,
    )
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    main()
