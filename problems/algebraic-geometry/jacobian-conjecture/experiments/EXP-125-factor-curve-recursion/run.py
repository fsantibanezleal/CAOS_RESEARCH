"""EXP-125: recurse on EXP-124's three residual factor curves."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from sympy import Poly, QQ, expand, factor_list, gcd, ground_roots, sympify, symbols


HERE = Path(__file__).resolve().parent
E124_PATH = HERE.parent / "EXP-124-rational-graph-alternative-chart" / "run.py"
E123_ARTIFACT = (
    HERE.parent
    / "EXP-123-direction-29-symbolic-lift"
    / "artifacts"
    / "results.json"
)
E124_ARTIFACT = (
    HERE.parent
    / "EXP-124-rational-graph-alternative-chart"
    / "artifacts"
    / "results.json"
)
ARTIFACT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
WORKER_ARTIFACT = HERE / "artifacts" / "symbolic-worker.json"
WORKER = HERE / "symbolic_worker.py"
PRIMES = (739, 811)
SAMPLES_PER_FACTOR = 4
WORKER_TIMEOUT_SECONDS = 300
MODULAR_GATE_SECONDS = 120
TOTAL_GATE_SECONDS = 450

spec = importlib.util.spec_from_file_location("exp124", E124_PATH)
exp124 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp124)


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


def load_polynomials():
    x, b, y = symbols("X B Y")
    e123 = json.loads(E123_ARTIFACT.read_text(encoding="utf-8"))
    e124 = json.loads(E124_ARTIFACT.read_text(encoding="utf-8"))
    r = sympify(e123["invariant_reduction"]["R_X_B"], locals={"X": x, "B": b})
    s = sympify(e123["invariant_reduction"]["S_X_B"], locals={"X": x, "B": b})
    factors = {}
    for record in e124["graph_numerator_factorization"]["factors"]:
        factor = sympify(record["factor"], locals={"X": x, "B": b})
        degree = int(Poly(factor, x, b, domain=QQ).total_degree())
        factors[f"F{degree}"] = factor
    require(set(factors) == {"F3", "F6", "F7"}, "reproduced three residual factors")
    product = expand(
        sympify(e124["graph_numerator_factorization"]["coefficient"])
        * factors["F3"]
        * factors["F6"]
        * factors["F7"]
    )
    require(
        expand(product - sympify(e124["graph_numerator"], locals={"X": x, "B": b}))
        == 0,
        "reproduced EXP-124 factorization",
    )
    for name, factor in factors.items():
        require(
            gcd(Poly(factor, x, b, domain=QQ), Poly(r, x, b, domain=QQ)).total_degree()
            == 0,
            f"{name} is coprime to R",
        )
        require(
            gcd(Poly(factor, x, b, domain=QQ), Poly(s, x, b, domain=QQ)).total_degree()
            == 0,
            f"{name} is coprime to S",
        )
    return x, b, y, r, s, factors, e123, e124


def modular_matrices(base, directions, prime):
    return {
        "base": exp124.exp115.matrix_mod(base, prime),
        "A": exp124.exp115.matrix_mod(directions[(0, 1)], prime),
        "B": exp124.exp115.matrix_mod(directions[(0, 5)], prime),
        "C": exp124.exp115.matrix_mod(directions[exp124.TARGET], prime),
    }


def independent_row_basis_fast(rows, prime):
    """Return the same ordered pivot-row basis using vectorized row arithmetic."""
    matrix = np.asarray(rows, dtype=np.int64)
    pivots: list[tuple[int, np.ndarray]] = []
    basis = []
    for row_index, source in enumerate(matrix):
        vector = source.copy()
        for column, pivot in pivots:
            coefficient = int(vector[column])
            if coefficient:
                vector = (vector - coefficient * pivot) % prime
        nonzero = np.flatnonzero(vector)
        if nonzero.size == 0:
            continue
        pivot_column = int(nonzero[0])
        inverse = pow(int(vector[pivot_column]), -1, prime)
        vector = vector * inverse % prime
        pivots.append((pivot_column, vector))
        basis.append(row_index)
        if len(basis) == matrix.shape[1]:
            break
    return basis


def determinant_mod_fast(rows, indices, prime):
    """Compute a selected modular determinant with vectorized elimination."""
    matrix = np.asarray([rows[index] for index in indices], dtype=np.int64)
    determinant = 1
    size = matrix.shape[0]
    for column in range(size):
        nonzero = np.flatnonzero(matrix[column:, column] % prime)
        if nonzero.size == 0:
            return 0
        pivot = column + int(nonzero[0])
        if pivot != column:
            matrix[[column, pivot]] = matrix[[pivot, column]]
            determinant = -determinant % prime
        pivot_value = int(matrix[column, column] % prime)
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        if column + 1 < size:
            coefficients = matrix[column + 1 :, column] * inverse % prime
            matrix[column + 1 :] = (
                matrix[column + 1 :]
                - coefficients[:, None] * matrix[column]
            ) % prime
    return determinant


def polynomial_terms_mod(expression, x, b, prime):
    return [
        (
            x_power,
            b_power,
            exp124.mod_entry(coefficient, prime),
        )
        for (x_power, b_power), coefficient in Poly(
            expression, x, b, domain=QQ
        ).terms()
    ]


def polynomial_terms_value(terms, xv, bv, prime):
    return (
        sum(
            coefficient
            * pow(xv, x_power, prime)
            * pow(bv, b_power, prime)
            for x_power, b_power, coefficient in terms
        )
        % prime
    )


def scan_factor(
    factor,
    r,
    s,
    x,
    b,
    prime,
    matrices,
    shared_rows,
    prior_rows,
    deadline,
):
    points = []
    candidates = []
    profiles: dict[str, int] = {}
    scanned = 0
    candidate_basis = None
    factor_terms = polynomial_terms_mod(factor, x, b, prime)
    r_terms = polynomial_terms_mod(r, x, b, prime)
    s_terms = polynomial_terms_mod(s, x, b, prime)
    for b_value in range(prime):
        for a_value in range(1, prime):
            if time.time() > deadline:
                raise TimeoutError("modular reconnaissance exceeded declared gate")
            scanned += 1
            xv = pow(a_value, 3, prime)
            fv = polynomial_terms_value(
                factor_terms, xv, b_value, prime
            )
            if fv != 0:
                continue
            sv = polynomial_terms_value(s_terms, xv, b_value, prime)
            if sv == 0:
                continue
            rv = polynomial_terms_value(r_terms, xv, b_value, prime)
            yv = -rv * pow(sv, -1, prime) % prime
            c_value = yv * pow(a_value * a_value, -1, prime) % prime
            evaluated = exp124.combine_mod(
                matrices["base"],
                matrices["A"],
                matrices["B"],
                matrices["C"],
                a_value,
                b_value,
                c_value,
                prime,
            )
            require(
                (rv + yv * sv) % prime == 0,
                f"p={prime} sampled point lies on shared graph",
            )
            require(
                fv == 0,
                f"p={prime} sampled point lies on EXP-124 residual",
            )
            if candidate_basis is not None and determinant_mod_fast(
                evaluated, candidate_basis, prime
            ):
                basis = candidate_basis
            else:
                basis = independent_row_basis_fast(evaluated, prime)
                if (
                    len(basis) == 125
                    and basis != shared_rows
                    and basis != prior_rows
                ):
                    candidate_basis = basis
            profile = "124/125" if len(basis) == 125 else f"<=124/{len(basis)}"
            profiles[profile] = profiles.get(profile, 0) + 1
            point = {
                "A": a_value,
                "B": b_value,
                "X": xv,
                "Y": yv,
                "C": c_value,
                "rank_profile": profile,
            }
            points.append(point)
            if (
                len(basis) == 125
                and basis != shared_rows
                and basis != prior_rows
                and not any(item["row_basis"] == basis for item in candidates)
            ):
                candidates.append(
                    {
                        "row_basis": basis,
                        "replacements_from_exp124": len(set(basis) - set(prior_rows)),
                        "first_point": point,
                    }
                )
            if len(points) >= SAMPLES_PER_FACTOR:
                return {
                    "points": points,
                    "rank_profiles": profiles,
                    "candidates": candidates,
                    "pairs_scanned": scanned,
                }
    return {
        "points": points,
        "rank_profiles": profiles,
        "candidates": candidates,
        "pairs_scanned": scanned,
    }


def modular_reconnaissance(
    base,
    directions,
    factors,
    r,
    s,
    x,
    b,
    shared_rows,
    prior_rows,
    started,
):
    records: dict[str, dict[str, object]] = {}
    basis_primes: dict[str, dict[tuple[int, ...], set[int]]] = {
        name: {} for name in factors
    }
    deadline = started + MODULAR_GATE_SECONDS
    for prime in PRIMES:
        matrices = modular_matrices(base, directions, prime)
        for name, factor in factors.items():
            record = scan_factor(
                factor,
                r,
                s,
                x,
                b,
                prime,
                matrices,
                shared_rows,
                prior_rows,
                deadline,
            )
            require(
                len(record["points"]) >= SAMPLES_PER_FACTOR,
                f"{name} supplies {SAMPLES_PER_FACTOR} points at p={prime}",
            )
            require(
                record["rank_profiles"].get("124/125", 0) >= SAMPLES_PER_FACTOR,
                f"{name} has rank profile 124/125 at p={prime}",
            )
            require(
                len(record["candidates"]) > 0,
                f"{name} supplies a new alternative basis at p={prime}",
            )
            for candidate in record["candidates"]:
                key = tuple(candidate["row_basis"])
                basis_primes[name].setdefault(key, set()).add(prime)
            records[f"{name}_p{prime}"] = record
            print(
                f"[INFO] {name} p={prime}: "
                f"{record['pairs_scanned']} pairs scanned",
                flush=True,
            )
            persist({"modular_reconnaissance": records}, CHECKPOINT)
    selected = {}
    for name in factors:
        cross = [
            basis for basis, primes in basis_primes[name].items() if len(primes) == 2
        ]
        require(bool(cross), f"{name} has a cross-prime alternative basis")
        basis = min(
            cross,
            key=lambda item: (len(set(item) - set(prior_rows)), item),
        )
        selected[name] = list(basis)
    require(
        time.time() - started <= MODULAR_GATE_SECONDS,
        "modular reconnaissance remains within gate",
    )
    return records, selected


def exact_profile(base, directions, rows):
    return exp124.exact_candidate_profile(base, directions, rows)


def restrict_to_graph(invariant, r, s, x, b, y):
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
    return y_degree, Poly(numerator, x, b, domain=QQ)


def main() -> None:
    started = time.time()
    require(
        all(
            prime % 3 == 1
            and pow(-pow(16, -1, prime) % prime, (prime - 1) // 3, prime) == 1
            for prime in PRIMES
        ),
        "redirected primes pass the exact F3 cubic-residue gate",
    )
    x, b, y, r, s, factors, e123, e124 = load_polynomials()
    a, c = symbols("A C")
    base, directions = exp124.build_full_system()
    shared_rows = list(e123["shared_rows"])
    prior_rows = list(e124["selected_rows"])
    modular, selected = modular_reconnaissance(
        base,
        directions,
        factors,
        r,
        s,
        x,
        b,
        shared_rows,
        prior_rows,
        started,
    )
    f3_rows = selected["F3"]
    (
        selected_base,
        selected_directions,
        anchor,
        anchor_det,
        normalized,
        components,
        anchor_point,
        anchor_attempts,
    ) = exact_profile(base, directions, f3_rows)
    largest = len(components[0])
    require(largest <= 60, "F3 exact largest cyclic block is at most 60")
    checkpoint = {
        "modular_reconnaissance": modular,
        "selected_rows": selected,
        "F3_anchor": {
            "point": list(anchor_point),
            "determinant": str(anchor_det),
            "attempts": anchor_attempts,
        },
        "F3_cyclic_component_sizes": [len(item) for item in components],
    }
    persist(checkpoint, CHECKPOINT)

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
        checkpoint["worker_timeout"] = {
            "seconds": WORKER_TIMEOUT_SECONDS,
            "stdout": error.stdout or "",
            "stderr": error.stderr or "",
        }
        persist(checkpoint, CHECKPOINT)
        raise AssertionError("exact symbolic worker exceeded declared gate") from error
    print(worker.stdout, end="", flush=True)
    if worker.stderr:
        print(worker.stderr, file=sys.stderr, end="", flush=True)
    require(worker.returncode == 0, "exact symbolic worker completed")
    worker_record = json.loads(WORKER_ARTIFACT.read_text(encoding="utf-8"))
    expression = sympify(
        worker_record["determinant_ratio"],
        locals={"A": a, "B": b, "C": c},
    )
    valuation, invariant = exp124.invariant_reduce(expression, a, b, c, x, y)
    y_degree, graph_numerator = restrict_to_graph(invariant, r, s, x, b, y)
    require(not graph_numerator.is_zero, "F3 basis is nonzero on the graph")

    f3_substitution = -((5 * b + 4) ** 3) / 16
    require(
        expand(factors["F3"].subs(x, f3_substitution)) == 0,
        "linear F3 substitution is exact",
    )
    quotient = Poly(
        expand(graph_numerator.as_expr().subs(x, f3_substitution)),
        b,
        domain=QQ,
    )
    require(not quotient.is_zero, "exact F3 quotient restriction is nonzero")
    quotient_monic = quotient.monic()
    quotient_factors = factor_list(quotient_monic.as_expr(), b)
    r_f3 = Poly(expand(r.subs(x, f3_substitution)), b, domain=QQ)
    s_f3 = Poly(expand(s.subs(x, f3_substitution)), b, domain=QQ)
    gcd_r = gcd(quotient_monic, r_f3).monic()
    gcd_s = gcd(quotient_monic, s_f3).monic()

    controls = []
    for av, bv, cv in ((1, 0, 0), (1, 0, 1), (2, 1, 1), (-1, 1, 1)):
        direct = (
            selected_base
            + av * selected_directions[(0, 1)]
            + bv * selected_directions[(0, 5)]
            + cv * selected_directions[exp124.TARGET]
        ).det(method="domain-ge") / anchor_det
        predicted = expression.subs({a: av, b: bv, c: cv})
        require(direct == predicted, f"direct determinant control ({av},{bv},{cv})")
        controls.append({"point": [av, bv, cv], "ratio": str(direct)})

    elapsed = time.time() - started
    require(elapsed <= TOTAL_GATE_SECONDS, "EXP-125 remains within total compute gate")
    payload = {
        "experiment": "EXP-125",
        "reproduced_factors": {name: str(value) for name, value in factors.items()},
        "modular_reconnaissance": modular,
        "selected_rows": selected,
        "F3_anchor": checkpoint["F3_anchor"],
        "F3_cyclic_component_sizes": checkpoint["F3_cyclic_component_sizes"],
        "symbolic_worker": worker_record,
        "determinant_A_valuation": valuation,
        "invariant_determinant_X_B_Y": str(invariant),
        "invariant_Y_degree": y_degree,
        "graph_numerator": str(graph_numerator.as_expr()),
        "graph_numerator_total_degree": graph_numerator.total_degree(),
        "F3_substitution_X": str(f3_substitution),
        "F3_quotient_monic": str(quotient_monic.as_expr()),
        "F3_quotient_degree": int(quotient_monic.degree()),
        "F3_quotient_factorization": {
            "coefficient": str(quotient_factors[0]),
            "factors": [
                {"factor": str(factor), "multiplicity": multiplicity}
                for factor, multiplicity in quotient_factors[1]
            ],
        },
        "F3_quotient_rational_roots": {
            str(root): multiplicity
            for root, multiplicity in ground_roots(quotient_monic).items()
        },
        "gcd_F3_quotient_with_R_restriction": str(gcd_r.as_expr()),
        "gcd_F3_quotient_with_S_restriction": str(gcd_s.as_expr()),
        "direct_exact_controls": controls,
        "predictions": {
            "p1_all_factors_rank_124_125": True,
            "p2_all_factors_new_basis": True,
            "p3_F3_cross_prime_and_scc_at_most_60": True,
            "p4_F3_exact_restriction_nonzero": True,
            "p5_F3_univariate_nonconstant": quotient_monic.degree() > 0,
        },
        "elapsed_seconds": elapsed,
        "scope": (
            "Exact dense-open cover of only the F3 component on the "
            "AS!=0 EXP-123 graph. Its quotient zeros, F6, F7, V(R,S), "
            "A=0, the full four-parameter restriction, (72,108), the "
            "degree floor, and JC(2) remain open."
        ),
    }
    persist(payload, ARTIFACT)
    digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(
        f"[INFO] F3 quotient degree={quotient_monic.degree()}, "
        f"factors={len(quotient_factors[1])}, elapsed={elapsed:.2f} s",
        flush=True,
    )
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    main()
