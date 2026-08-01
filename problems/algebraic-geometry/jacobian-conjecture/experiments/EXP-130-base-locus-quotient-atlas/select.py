"""EXP-130 modular row selection on the uncovered degree-3 and degree-6 blocks."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Poly, QQ, primerange, sympify, symbols


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
E125_PATH = ROOT / "EXP-125-factor-curve-recursion" / "run.py"
E123_ARTIFACT = ROOT / "EXP-123-direction-29-symbolic-lift" / "artifacts" / "results.json"
E124_ARTIFACT = ROOT / "EXP-124-rational-graph-alternative-chart" / "artifacts" / "results.json"
E125_ARTIFACT = ROOT / "EXP-125-factor-curve-recursion" / "artifacts" / "results.json"
E127_ARTIFACT = ROOT / "EXP-127-f7-divisor-norm" / "artifacts" / "results.json"
E129_ARTIFACT = ROOT / "EXP-129-f7-crt-minor-atlas" / "artifacts" / "results.json"
CRT_ARTIFACT = HERE / "artifacts" / "crt-worker.json"
ARTIFACT = HERE / "artifacts" / "selection.json"
EXPECTED_CRT_SHA256 = "7189D6C9DBD6CF3E006B937A9DE1547A43155985BEF6716FE544F58A0EE65CB2"
PRIMES_PER_BLOCK = 2
Y_VALUES = (0, 1)
TOTAL_GATE_SECONDS = 180

spec = importlib.util.spec_from_file_location("exp125_exp130", E125_PATH)
exp125 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp125)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def persist(payload: dict[str, object]) -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def eval_mod(expression, variables, values, prime: int) -> int:
    polynomial = Poly(expression, *variables, domain=QQ)
    value = 0
    for powers, coefficient in polynomial.terms():
        term = exp125.exp124.mod_entry(coefficient, prime)
        for scalar, power in zip(values, powers, strict=True):
            term = term * pow(int(scalar), int(power), prime) % prime
        value = (value + term) % prime
    return value


def evaluated_matrix(matrices, a_value, b_value, c_value, prime):
    return exp125.exp124.combine_mod(
        matrices["base"],
        matrices["A"],
        matrices["B"],
        matrices["C"],
        a_value,
        b_value,
        c_value,
        prime,
    )


def main() -> None:
    started = time.time()
    require(sha256(CRT_ARTIFACT) == EXPECTED_CRT_SHA256, "CRT source hash matches")
    crt = json.loads(CRT_ARTIFACT.read_text(encoding="utf-8"))
    e123 = json.loads(E123_ARTIFACT.read_text(encoding="utf-8"))
    e124 = json.loads(E124_ARTIFACT.read_text(encoding="utf-8"))
    e125 = json.loads(E125_ARTIFACT.read_text(encoding="utf-8"))
    e127 = json.loads(E127_ARTIFACT.read_text(encoding="utf-8"))
    e129 = json.loads(E129_ARTIFACT.read_text(encoding="utf-8"))
    x, b, _ = symbols("X B Y")
    r = sympify(e123["invariant_reduction"]["R_X_B"], locals={"X": x, "B": b})
    s = sympify(e123["invariant_reduction"]["S_X_B"], locals={"X": x, "B": b})
    blocks = []
    for record in crt["blocks"]:
        if int(record["degree"]) not in (3, 6):
            continue
        blocks.append(
            {
                "degree": int(record["degree"]),
                "factor": Poly(
                    sympify(record["B_factor"], locals={"B": b}), b, domain=QQ
                ).monic(),
                "X_class": sympify(
                    record["X_class_mod_B_factor"], locals={"B": b}
                ),
            }
        )
    require([item["degree"] for item in blocks] == [3, 6], "selection targets only degrees 3 and 6")

    base, directions = exp125.exp124.build_full_system()
    matrices_by_prime = {}
    probes = []
    accepted_primes = {3: set(), 6: set()}
    for prime in primerange(127, 5000):
        if all(len(values) >= PRIMES_PER_BLOCK for values in accepted_primes.values()):
            break
        matrices = None
        for block in blocks:
            degree = block["degree"]
            if len(accepted_primes[degree]) >= PRIMES_PER_BLOCK:
                continue
            roots_b = [
                value
                for value in range(prime)
                if eval_mod(block["factor"].as_expr(), (b,), (value,), prime) == 0
            ]
            accepted = None
            for b_value in roots_b:
                x_value = eval_mod(block["X_class"], (b,), (b_value,), prime)
                roots_a = [
                    value
                    for value in range(1, prime)
                    if pow(value, 3, prime) == x_value
                ]
                if roots_a:
                    accepted = (roots_a[0], b_value, x_value)
                    break
            if accepted is None:
                continue
            if matrices is None:
                matrices = {
                    "base": exp125.exp124.exp115.matrix_mod(base, prime),
                    "A": exp125.exp124.exp115.matrix_mod(directions[(0, 1)], prime),
                    "B": exp125.exp124.exp115.matrix_mod(directions[(0, 5)], prime),
                    "C": exp125.exp124.exp115.matrix_mod(
                        directions[exp125.exp124.TARGET], prime
                    ),
                }
                matrices_by_prime[prime] = matrices
            a_value, b_value, x_value = accepted
            require(
                eval_mod(r, (x, b), (x_value, b_value), prime) == 0,
                f"degree-{degree} modular point satisfies R at p={prime}",
            )
            require(
                eval_mod(s, (x, b), (x_value, b_value), prime) == 0,
                f"degree-{degree} modular point satisfies S at p={prime}",
            )
            for y_value in Y_VALUES:
                c_value = y_value * pow(a_value * a_value, -1, prime) % prime
                evaluated = evaluated_matrix(
                    matrices, a_value, b_value, c_value, prime
                )
                rows = exp125.independent_row_basis_fast(evaluated, prime)
                require(
                    len(rows) == 125,
                    f"degree-{degree} Y={y_value} probe has full row rank at p={prime}",
                )
                probes.append(
                    {
                        "degree": degree,
                        "prime": prime,
                        "A": a_value,
                        "B": b_value,
                        "C": c_value,
                        "X": x_value,
                        "Y": y_value,
                        "row_basis": rows,
                    }
                )
            accepted_primes[degree].add(prime)

    require(
        all(len(values) >= PRIMES_PER_BLOCK for values in accepted_primes.values()),
        "two admissible primes found for each uncovered block",
    )
    existing = {
        tuple(e123["shared_rows"]),
        tuple(e124["selected_rows"]),
        *(tuple(rows) for rows in e125["selected_rows"].values()),
        tuple(e127["selected_rows"]),
        *(tuple(record["rows"]) for record in e129["exact_atlas"]),
    }
    candidates = []
    for probe in probes:
        rows = probe["row_basis"]
        if tuple(rows) in existing or any(item["rows"] == rows for item in candidates):
            continue
        coverage = []
        for target in probes:
            matrices = matrices_by_prime[target["prime"]]
            evaluated = evaluated_matrix(
                matrices,
                target["A"],
                target["B"],
                target["C"],
                target["prime"],
            )
            nonzero = (
                exp125.determinant_mod_fast(
                    evaluated, rows, target["prime"]
                )
                != 0
            )
            coverage.append(
                {
                    "degree": target["degree"],
                    "prime": target["prime"],
                    "Y": target["Y"],
                    "nonzero": nonzero,
                }
            )
        candidates.append(
            {
                "rows": rows,
                "source_degree": probe["degree"],
                "source_Y": probe["Y"],
                "coverage": coverage,
            }
        )
    require(bool(candidates), "new row-basis candidates were found")
    uncovered = set(range(len(probes)))
    atlas = []
    while uncovered:
        best = max(
            candidates,
            key=lambda item: sum(
                1
                for index in uncovered
                if item["coverage"][index]["nonzero"]
            ),
        )
        newly_covered = {
            index
            for index in uncovered
            if best["coverage"][index]["nonzero"]
        }
        require(bool(newly_covered), "candidate atlas advances probe coverage")
        atlas.append(best)
        uncovered -= newly_covered
    require(not uncovered, "selected modular atlas covers every degree-3/6 probe")
    require(time.time() - started <= TOTAL_GATE_SECONDS, "selection remains within budget")
    payload = {
        "experiment": "EXP-130-selection",
        "crt_source_sha256": EXPECTED_CRT_SHA256,
        "blocks": [
            {
                "degree": item["degree"],
                "factor": str(item["factor"].as_expr()),
                "X_class": str(item["X_class"]),
            }
            for item in blocks
        ],
        "accepted_primes": {
            str(degree): sorted(values)
            for degree, values in accepted_primes.items()
        },
        "probes": probes,
        "candidate_count": len(candidates),
        "atlas_size": len(atlas),
        "single_basis_found": any(
            all(test["nonzero"] for test in item["coverage"])
            for item in candidates
        ),
        "selected_atlas": atlas,
        "scope": (
            "Modular row selection on the exact degree-3 and degree-6 base "
            "blocks. Characteristic-zero reconstruction and K[Y] unit tests "
            "are still required."
        ),
    }
    persist(payload)
    print(f"[PASS] selection SHA256 {sha256(ARTIFACT)}", flush=True)
    print(
        f"[INFO] candidates={len(candidates)} atlas_size={len(atlas)} "
        f"single_basis={payload['single_basis_found']}",
        flush=True,
    )


if __name__ == "__main__":
    main()

