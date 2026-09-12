"""Declared, deterministic EXP-004 arithmetic; no numerical density is inferred."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import subprocess
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
ROOT = HERE.parents[4]
DECLARATION = "e03413b2301bf45ca68ff6e945f25add9a1c3a89"
SCHEMA = "riemann-exp004-results-v1"
FIELDS = ("N", "s", "r", "b", "O", "E", "Z")
C_GRID = tuple(map(Fraction, ("-2", "-1", "-1/2", "0", "1/2", "1", "2")))
O_GRID = tuple(map(Fraction, ("0", "1/10", "1/3", "1/2", "1", "2")))
CENSUS_SIZE = 3**9
BUDGET_SECONDS = 60
INPUTS = (
    "context/2026-09-12-critical-mass-and-multiplicity-route.md",
    "context/2026-09-12-parity-transfer-adversarial-audit.md",
    "context/2026-09-12-wang-transfer-audit.md",
    "experiments/EXP-003-odd-frame-pressure/mathematical-proof.md",
)


class VerificationError(ValueError):
    """An exact check failed; the run must not be recorded as verified."""


def require(condition, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canonical(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path: Path, value) -> None:
    with path.open("xb") as target:
        target.write(canonical(value))


def exact(value) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError("An exact integer or rational is required")
    return Fraction(value)


def positive_integer(value) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("Multiplicity must be a positive integer")
    return value


def atom(kind: str, multiplicity: int) -> dict:
    m = positive_integer(multiplicity)
    if kind == "real":
        simple = int(m == 1)
        return dict(zip(FIELDS, (m, simple, 1 - simple, 0, m % 2, max(0, m - 2), 1)))
    if kind == "pair":
        return dict(zip(FIELDS, (2 * m, 0, 0, 1, 0, 2 * (m - 1), 2)))
    raise ValueError("Atom kind must be real or pair")


def multiset(real_multiplicities=(), pair_multiplicities=()) -> dict:
    total = dict.fromkeys(FIELDS, 0)
    for kind, multiplicities in (("real", real_multiplicities), ("pair", pair_multiplicities)):
        for m in multiplicities:
            item = atom(kind, m)
            for field in FIELDS:
                total[field] += item[field]
    return total


def residuals(counts: dict, sigma=0, defect=0) -> dict:
    sigma, defect = exact(sigma), exact(defect)
    require(sigma >= 0 and defect >= 0, "Slack and Gram defect must be nonnegative")
    n, s, r, b, odd, excess, distinct = (counts[key] for key in FIELDS)
    require(excess == n - s - 2 * r - 2 * b, "Multiplicity excess identity")
    require(distinct == s + r + 2 * b, "Distinct count identity")
    charge = s + excess - odd
    require(charge >= 0, "Odd-support charge is negative")
    q = 4 * n - 3 * s - 4 * r - 4 * b + defect + sigma
    simple_left = 3 * s - (2 * n - q + 2 * odd + defect)
    distinct_left = 6 * distinct - (7 * n - 2 * q + odd + 2 * defect)
    require(simple_left == 2 * charge + sigma, "Simple residual identity")
    require(distinct_left == charge + 6 * b + 2 * sigma, "Distinct residual identity")
    require(simple_left >= 0 and distinct_left >= 0, "Residual nonnegativity")
    return {"charge": charge, "Q": q, "A": simple_left, "B": distinct_left}


def symbolic_checks() -> dict:
    import sympy as sp

    n, s, r, b, odd, d, sigma = sp.symbols("N s r b O D sigma")
    e, z = n - s - 2 * r - 2 * b, s + r + 2 * b
    q = 4 * n - 3 * s - 4 * r - 4 * b + d + sigma
    a = 3 * s - (2 * n - q + 2 * odd + d) - (2 * (s + e - odd) + sigma)
    bb = 6 * z - (7 * n - 2 * q + odd + 2 * d) - (s + e - odd + 6 * b + 2 * sigma)
    require(sp.expand(a) == 0 and sp.expand(bb) == 0, "Symbolic residual identities")
    j = sp.symbols("j", integer=True, nonnegative=True)
    charges = {
        "simple_real_m=1": sp.Integer(0),
        "even_real_m=2j+2": sp.expand((2 * j + 2) - 2),
        "odd_real_m=2j+3": sp.expand((2 * j + 3) - 2 - 1),
        "pair_m=j+1": sp.expand(2 * ((j + 1) - 1)),
    }
    require(all(expr.is_nonnegative is True for expr in charges.values()), "Symbolic atom signs")
    atoms = []
    for kind, m in itertools.product(("real", "pair"), range(1, 13)):
        counts = atom(kind, m)
        charge = counts["s"] + counts["E"] - counts["O"]
        expected = (0 if m == 1 else m - 2 - m % 2) if kind == "real" else 2 * (m - 1)
        require(charge == expected and charge >= 0, "Multiplicity regression")
        atoms.append({"kind": kind, "multiplicity": m, **counts, "charge": charge})
    return {
        "residual_identities": 2,
        "universal_atom_parameter": "j is an arbitrary nonnegative integer",
        "universal_atom_charges": {key: str(value) for key, value in charges.items()},
        "multiplicity_regression_cases": len(atoms),
        "atoms": atoms,
    }


def relaxation_witness(c, odd) -> dict:
    c, odd = exact(c), exact(odd)
    if odd < 0:
        raise ValueError("Odd density in the scalar relaxation must be nonnegative")
    candidates = (Fraction(0), c, (c + 2 * odd) / 3)
    optimum = max(candidates)
    excess = max(Fraction(0), odd - optimum)
    active = candidates.index(optimum)
    # Constraints: s>=0, e>=0, s-2e>=c, s+e>=o.
    duals = (
        (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(2), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 3), Fraction(2, 3)),
    )
    dual = duals[active]
    require(optimum >= 0 and excess >= 0, "Primal nonnegativity")
    require(optimum - 2 * excess >= c and optimum + excess >= odd, "Primal feasibility")
    require(all(v >= 0 for v in dual), "Dual nonnegativity")
    require(dual[0] + dual[2] + dual[3] == 1, "Dual objective coefficient of s")
    require(dual[1] - 2 * dual[2] + dual[3] == 0, "Dual objective coefficient of e")
    require(dual[2] * c + dual[3] * odd == optimum, "Exact primal-dual equality")
    return {"c": str(c), "o": str(odd), "s": str(optimum), "e": str(excess),
            "dual": list(map(str, dual)), "active_bound": ("zero", "c", "parity")[active]}


def relaxation_checks() -> dict:
    import sympy as sp

    c, o = sp.symbols("c o", real=True)
    parity_s, parity_e = (c + 2 * o) / 3, (o - c) / 3
    require(sp.expand(parity_s - 2 * parity_e - c) == 0, "Universal parity primal constraint")
    require(sp.expand(parity_s + parity_e - o) == 0, "Universal parity primal constraint")
    regimes = [
        {"active": "zero", "conditions": "o>=0, c<=-2o", "s": "0", "e": "o"},
        {"active": "c", "conditions": "c>=o>=0", "s": "c", "e": "0"},
        {"active": "parity", "conditions": "o>=0, o>=c, c+2o>=0",
         "s": "(c+2o)/3", "e": "(o-c)/3"},
    ]
    rows = [relaxation_witness(cval, oval) for cval, oval in itertools.product(C_GRID, O_GRID)]
    require(len(rows) == 42, "Declared relaxation case count")
    return {"cases": len(rows), "general_primal_regimes": regimes,
            "scope": "Optimality only for the stated scalar relaxation", "witnesses": rows}


def sinc_integer(gap: int):
    import sympy as sp

    return sp.Integer(1) if gap == 0 else sp.sin(sp.pi * gap) / (sp.pi * gap)


def sharpness_checks() -> dict:
    import sympy as sp

    rows = []
    for simple, double in itertools.product(range(6), repeat=2):
        weights = [1] * simple + [2] * double
        gram = sp.Matrix(len(weights), len(weights), lambda i, j: sinc_integer(i - j))
        require(gram == sp.eye(len(weights)), "Sinc features on distinct integers are orthogonal")
        q = sum(weights[i] * weights[j] * gram[i, j] ** 2
                for i in range(len(weights)) for j in range(len(weights)))
        counts = multiset(weights)
        require(q == simple + 4 * double, "Sharpness Hilbert--Schmidt moment")
        result = residuals(counts)
        require(q == result["Q"] and result["A"] == 0 and result["B"] == 0, "Sharpness residuals")
        rows.append({"s": simple, "r": double, "N": counts["N"], "Z": counts["Z"],
                     "Q": int(q), "E": 0, "gram_defect": 0, "A": 0, "B": 0})
    triple = multiset([3])
    wrong_residual = 2 * triple["Z"] - triple["N"] - triple["s"]
    require(wrong_residual == -1, "False distinct half-sum must be refuted")
    return {
        "cases": len(rows), "kernel": "sin(pi*x)/(pi*x), continuously 1 at x=0",
        "density": "Uniform density on [-1/2,1/2]; finite Hilbert example only",
        "geometry": "Distinct integer support points; weights 1 or 2; simple Gram defect zero",
        "witnesses": rows,
        "negative_control": {"real_multiplicities": [3], **triple,
                             "false_half_sum_residual": wrong_residual},
    }


def threshold_checks() -> dict:
    import sympy as sp

    theta = sp.symbols("theta", positive=True)
    c = 2 - theta / 2 - sp.cot(theta / sp.sqrt(2)) / sp.sqrt(2)
    derivative = sp.cot(theta / sp.sqrt(2)) ** 2 / 2
    require(sp.trigsimp(sp.diff(c, theta) - derivative) == 0, "Derivative formula")
    alpha = Fraction(51, 100)
    derivative_cap = 1 / alpha**2
    c_upper = 2 - 1 / alpha - alpha / 4
    require(derivative_cap == Fraction(10000, 2601) and derivative_cap < 4, "Rational derivative cap")
    require(c_upper == Fraction(-1801, 20400) and c_upper < 0, "Rational root comparison")
    require(1 - alpha**2 / 4 > 0, "Positive cosine lower numerator")
    return {
        "alpha": str(alpha), "derivative_formula_verified": True,
        "derivative_cap": str(derivative_cap), "derivative_cap_less_than": "4",
        "c_alpha_upper": str(c_upper), "c_alpha_upper_negative": True,
        "root_comparison": "alpha<theta0<1 by the recorded elementary analytic inequalities",
        "elementary_paper_inputs": ["cos(x)>=1-x^2/2", "sin(x)<=x", "tan(x)>x for 0<x<pi/2"],
        "delta_formula": "min((theta0-alpha)/2,kappa/4)",
        "theta1_formula": "theta0-delta",
        "simple_lower_formula": "max(0,c(theta),(c(theta)+2*kappa)/3)",
        "distinct_lower_formula": "max(kappa,(1+c(theta))/2,(3+2*c(theta)+kappa)/6)",
        "classical_a": None, "kappa": None, "theta0_numeric": None, "theta1_decimal": None,
        "scope": "Exact rational comparisons and symbolic differentiation; no numerical root or seed constant",
    }


def committed_input(path: Path, declaration: str = DECLARATION, root: Path = ROOT) -> dict:
    relative = path.relative_to(root).as_posix()
    recorded = subprocess.run(["git", "show", f"{declaration}:{relative}"], cwd=root,
                              check=True, capture_output=True).stdout
    require(recorded == path.read_bytes(), f"Committed input differs: {relative}")
    return {"path": relative, "sha256": sha(path), "source_commit": declaration}


def provenance() -> dict:
    return {
        "declaration_commit": DECLARATION,
        "hypothesis": committed_input(HERE / "hypothesis.md"),
        "inputs": [committed_input(PROBLEM / name) for name in INPUTS],
        "runner": {"path": Path(__file__).relative_to(ROOT).as_posix(), "sha256": sha(Path(__file__))},
    }


class Deadline:
    def __init__(self, seconds: float = BUDGET_SECONDS):
        self.started = time.monotonic()
        self.limit = self.started + seconds

    def check(self):
        if time.monotonic() >= self.limit:
            raise TimeoutError("Declared 60-second arithmetic budget exhausted")


def run_census(output: Path, source: dict, deadline, emit) -> dict:
    raw = output / "census.jsonl"
    checkpoint = output / "census-checkpoint.json"
    next_index = 0
    digest = hashlib.sha256()
    columns = ["index"] + [f"a_{m}" for m in range(1, 7)] + [f"b_{m}" for m in range(1, 4)]
    columns += list(FIELDS) + ["charge", "A_sigma0", "B_sigma0", "A_sigma1", "B_sigma1",
                              "A_sigma2", "B_sigma2"]

    def save(status):
        checkpoint.write_bytes(canonical({
            "schema": "riemann-exp004-census-checkpoint-v1", "status": status,
            "next_index": next_index, "total_vectors": CENSUS_SIZE,
            "raw_prefix_sha256": digest.hexdigest(), "source_identity": source,
            "policy": "Completed prefix is retained; any replay starts a fresh full census",
        }))

    with raw.open("xb") as stream:
        try:
            for index, vector in enumerate(itertools.product(range(3), repeat=9)):
                deadline.check()
                reals = [m for m, count in enumerate(vector[:6], 1) for _ in range(count)]
                pairs = [m for m, count in enumerate(vector[6:], 1) for _ in range(count)]
                counts = multiset(reals, pairs)
                row = [index, *vector, *(counts[field] for field in FIELDS)]
                results = [residuals(counts, sigma) for sigma in range(3)]
                row.append(results[0]["charge"])
                for result in results:
                    require(result["A"].denominator == 1 and result["B"].denominator == 1,
                            "Census residuals must be integers")
                    row.extend((int(result["A"]), int(result["B"])))
                encoded = canonical(row)
                stream.write(encoded)
                digest.update(encoded)
                next_index = index + 1
                if next_index % 2000 == 0:
                    stream.flush()
                    save("in_progress")
                    emit({"event": "census_progress", "completed_vectors": next_index})
            require(next_index == CENSUS_SIZE, "Complete declared census")
            stream.flush()
            save("complete")
            deadline.check()
        except Exception:
            stream.flush()
            save("incomplete")
            raise
    return {
        "vectors": next_index, "sigma_values": [0, 1, 2], "sigma_evaluations": 3 * next_index,
        "gram_defect": "0; the symbolic identities cancel arbitrary D",
        "raw_artifact": raw.name, "sha256": digest.hexdigest(), "columns": columns,
        "order": "Lexicographic Cartesian product {0,1,2}^9",
        "scope": "Exact scalar residual checks; sigma samples are not claimed geometric realizations",
    }


def run(output: Path) -> int:
    deadline = Deadline()
    output.mkdir(parents=True, exist_ok=False)
    stages = {}
    source = None
    with (output / "stdout.log").open("x", encoding="utf-8", newline="\n") as log:
        def emit(event):
            line = canonical(event).decode().rstrip("\n")
            print(line, flush=True)
            log.write(line + "\n")
            log.flush()

        emit({"event": "run_start", "experiment": "EXP-004", "budget_seconds": BUDGET_SECONDS})
        try:
            source = provenance()
            deadline.check()
            values = {}
            for name, function in (("symbolic", symbolic_checks), ("relaxation", relaxation_checks),
                                   ("sharpness", sharpness_checks), ("threshold", threshold_checks)):
                deadline.check()
                emit({"event": "stage_start", "stage": name})
                started = time.monotonic()
                values[name] = function()
                deadline.check()
                stages[name] = time.monotonic() - started
                emit({"event": "stage_pass", "stage": name})
            write_new(output / "symbolic.json", values["symbolic"])
            write_new(output / "relaxation.json", values["relaxation"])
            write_new(output / "sharpness.json", values["sharpness"])
            emit({"event": "stage_start", "stage": "census"})
            started = time.monotonic()
            values["census"] = run_census(output, source, deadline, emit)
            stages["census"] = time.monotonic() - started
            deadline.check()
            result = {
                "schema": SCHEMA, "experiment": "EXP-004-parity-density-transfer",
                "arithmetic_status": "verified", "provenance": source,
                "symbolic": {"residual_identities": values["symbolic"]["residual_identities"],
                             "multiplicity_regression_cases": values["symbolic"]["multiplicity_regression_cases"],
                             "raw_artifact": "symbolic.json", "sha256": sha(output / "symbolic.json")},
                "census": values["census"],
                "relaxation": {"cases": values["relaxation"]["cases"], "raw_artifact": "relaxation.json",
                               "sha256": sha(output / "relaxation.json")},
                "sharpness": {"cases": values["sharpness"]["cases"], "raw_artifact": "sharpness.json",
                              "sha256": sha(output / "sharpness.json"),
                              "negative_control": values["sharpness"]["negative_control"]},
                "threshold": values["threshold"],
                "proof_status": {
                    "preflight": "Independent paper and source audit committed with declaration",
                    "all_height_theorem": "Not proved by this computational runner",
                    "full_proof_and_final_verdict": "Separate required gate",
                    "classical_seed": "Imported Selberg theorem restated in Karatsuba; no numeric constant",
                },
                "scope": "Declared exact identities and finite controls only; no numerical exponent claim",
            }
            deadline.check()
            write_new(output / "result.json", result)
            emit({"event": "run_pass", "result_sha256": sha(output / "result.json")})
            status, exit_code = "verified", 0
        except Exception as error:
            status = "inconclusive_budget" if isinstance(error, TimeoutError) else "failed"
            failure = {"schema": SCHEMA, "arithmetic_status": status, "error_type": type(error).__name__,
                       "message": str(error), "provenance": source,
                       "completed_stages": list(stages), "all_height_theorem": "not_confirmed"}
            write_new(output / "failure.json", failure)
            emit({"event": "run_failed", "status": status, "message": str(error)})
            exit_code = 1
        elapsed = time.monotonic() - deadline.started
        write_new(output / "operational.json", {
            "status": status, "elapsed_seconds": elapsed, "budget_seconds": BUDGET_SECONDS,
            "stage_seconds": stages, "python": platform.python_version(), "platform": platform.platform(),
            "runtime_separate_from_deterministic_result": True,
            "stdout_log": "stdout.log", "stdout_sha256": sha(output / "stdout.log"),
        })
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New directory; existing paths are refused")
    args = parser.parse_args()
    return run(args.output.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
