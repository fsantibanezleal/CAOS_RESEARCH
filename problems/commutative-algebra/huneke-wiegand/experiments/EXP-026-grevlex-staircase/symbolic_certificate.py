"""All-parameter Presburger boundary certificate for EXP-026."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import z3


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "symbolic-certificate.json"


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return digest_text(raw)


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


class Certificate:
    def __init__(self, timeout_ms: int, budget_seconds: float) -> None:
        self.timeout_ms = timeout_ms
        self.budget_seconds = budget_seconds
        self.started = time.perf_counter()
        self.leaves: list[dict[str, object]] = []
        self.p = z3.Int("p")

    def elapsed(self) -> float:
        return time.perf_counter() - self.started

    @staticmethod
    def bounded(value: z3.ArithRef, lower: z3.ArithRef, upper: z3.ArithRef) -> z3.BoolRef:
        return z3.And(value >= lower, value <= upper)

    def generator(self, value: z3.ArithRef) -> z3.BoolRef:
        p = self.p
        return z3.Or(
            value == 0,
            self.bounded(value, 1, p),
            self.bounded(value, 3 * p, 4 * p - 2),
            self.bounded(value, 6 * p, 8 * p - 2),
            self.bounded(value, 8 * p, 10 * p - 2),
            value == 10 * p,
            self.bounded(value, 11 * p - 1, 12 * p - 1),
            self.bounded(value, 13 * p + 1, 14 * p - 2),
            self.bounded(value, 14 * p, 15 * p - 1),
            value == 16 * p,
            self.bounded(value, 17 * p - 1, 18 * p - 1),
        )

    def valid(self, values: list[z3.ArithRef]) -> z3.BoolRef:
        ordered = [values[index] <= values[index + 1] for index in range(len(values) - 1)]
        return z3.And(
            *[self.generator(value) for value in values],
            *ordered,
            sum(values) < 24 * self.p,
        )

    @staticmethod
    def lex_less(left: list[z3.ArithRef], right: list[z3.ArithRef]) -> z3.BoolRef:
        return z3.Or(
            *[
                z3.And(
                    *[left[prior] == right[prior] for prior in range(index)],
                    left[index] < right[index],
                )
                for index in range(len(left))
            ]
        )

    def standard(self, values: list[z3.ArithRef]) -> z3.BoolRef:
        alternative = [z3.FreshInt("alternative") for _value in values]
        smaller_same_fiber = z3.And(
            self.valid(alternative),
            sum(alternative) == sum(values),
            self.lex_less(alternative, values),
        )
        return z3.And(self.valid(values), z3.Not(z3.Exists(alternative, smaller_same_fiber)))

    def minimal_boundary(self, values: list[z3.ArithRef]) -> z3.BoolRef:
        divisors = [values[:index] + values[index + 1 :] for index in range(len(values))]
        return z3.And(
            *[self.generator(value) for value in values],
            *[values[index] <= values[index + 1] for index in range(len(values) - 1)],
            z3.Not(self.standard(values)),
            *[self.standard(divisor) for divisor in divisors],
        )

    def cubic_candidate(self, values: list[z3.ArithRef]) -> z3.BoolRef:
        a, b, c = values
        p = self.p
        index = z3.Int("cubic_index")
        return z3.Or(
            z3.And(a == p, b == p, c == p),
            z3.Exists(
                index,
                z3.And(
                    index >= 1,
                    index <= p,
                    z3.Or(
                        z3.And(a == index, b == p, c == 12 * p - 1),
                        z3.And(a == index, b == p, c == 15 * p - 1),
                        z3.And(a == index, b == p, c == 18 * p - 1),
                        z3.And(index <= p - 2, a == index, b == 4 * p - 2, c == 16 * p),
                        z3.And(a == index, b == 4 * p - 2, c == 18 * p - 1),
                    ),
                ),
            ),
        )

    def quartic_candidate(self, values: list[z3.ArithRef]) -> z3.BoolRef:
        a, b, c, d = values
        p = self.p
        index = z3.Int("quartic_index")
        return z3.Exists(
            index,
            z3.And(
                index >= 2,
                index <= p - 1,
                a == index,
                b == p,
                c == p,
                d == 4 * p - 2,
            ),
        )

    def solve_unsat(self, label: str, counterexample: z3.BoolRef) -> None:
        if self.elapsed() > self.budget_seconds:
            raise TimeoutError("symbolic certificate exceeded its declared total budget")
        solver = z3.Solver()
        solver.set(timeout=self.timeout_ms)
        solver.add(self.p >= 4, counterexample)
        started = time.perf_counter()
        result = solver.check()
        elapsed = time.perf_counter() - started
        leaf = {
            "label": label,
            "result": str(result),
            "query_sha256": digest_text(solver.sexpr()),
            "elapsed_seconds": elapsed,
        }
        if result == z3.unsat:
            self.leaves.append(leaf)
            return
        if result == z3.sat:
            raise AssertionError(f"{label}: symbolic counterexample: {solver.model()}")
        raise TimeoutError(f"{label}: unresolved solver result {result}")

    def solve_tail_case(
        self,
        label: str,
        region: z3.BoolRef,
        lead: list[z3.ArithRef],
        tail: list[z3.ArithRef],
    ) -> None:
        required = z3.And(
            self.standard(tail),
            sum(lead) == sum(tail),
            self.lex_less(tail, lead),
        )
        self.solve_unsat(label, z3.And(region, z3.Not(required)))


LEAF_LABELS = (
    "cubic-completeness",
    "cubic-soundness",
    "quartic-completeness",
    "quartic-soundness",
    "tail-c1-first",
    "tail-c1-interior",
    "tail-c1-last",
    "tail-c2-main",
    "tail-c2-last",
    "tail-c3-main",
    "tail-c3-last",
    "tail-c4",
    "tail-c5-first-two",
    "tail-c5-rest",
    "tail-c6-isolated",
    "tail-quartic",
)


def solve_named_leaf(certificate: Certificate, label: str) -> None:
    p = certificate.p
    if label.startswith("cubic-"):
        cubic = list(z3.Ints("cubic_a cubic_b cubic_c"))
        minimal = certificate.minimal_boundary(cubic)
        candidate = certificate.cubic_candidate(cubic)
        counterexample = (
            z3.And(minimal, z3.Not(candidate))
            if label.endswith("completeness")
            else z3.And(candidate, z3.Not(minimal))
        )
        certificate.solve_unsat(label, counterexample)
        return
    if label.startswith("quartic-"):
        quartic = list(z3.Ints("quartic_a quartic_b quartic_c quartic_d"))
        minimal = certificate.minimal_boundary(quartic)
        candidate = certificate.quartic_candidate(quartic)
        counterexample = (
            z3.And(minimal, z3.Not(candidate))
            if label.endswith("completeness")
            else z3.And(candidate, z3.Not(minimal))
        )
        certificate.solve_unsat(label, counterexample)
        return

    i = z3.Int("tail_index")
    cases = {
        "tail-c1-first": (i == 1, [i, p, 12 * p - 1], [0, 3 * p, 10 * p]),
        "tail-c1-interior": (
            z3.And(i >= 2, i <= p - 1),
            [i, p, 12 * p - 1],
            [0, 0, 13 * p + i - 1],
        ),
        "tail-c1-last": (i == p, [i, p, 12 * p - 1], [0, 1, 14 * p - 2]),
        "tail-c2-main": (
            z3.And(i >= 1, i <= p - 1),
            [i, p, 15 * p - 1],
            [0, i - 1, 16 * p],
        ),
        "tail-c2-last": (i == p, [i, p, 15 * p - 1], [0, 0, 17 * p - 1]),
        "tail-c3-main": (
            z3.And(i >= 1, i <= p - 1),
            [i, p, 18 * p - 1],
            [0, 3 * p + i - 1, 16 * p],
        ),
        "tail-c3-last": (i == p, [i, p, 18 * p - 1], [0, 3 * p, 17 * p - 1]),
        "tail-c4": (
            z3.And(i >= 1, i <= p - 2),
            [i, 4 * p - 2, 16 * p],
            [0, 3 * p, 17 * p + i - 2],
        ),
        "tail-c5-first-two": (
            z3.And(i >= 1, i <= 2),
            [i, 4 * p - 2, 18 * p - 1],
            [0, 7 * p + i - 2, 15 * p - 1],
        ),
        "tail-c5-rest": (
            z3.And(i >= 3, i <= p),
            [i, 4 * p - 2, 18 * p - 1],
            [0, 6 * p + i - 3, 16 * p],
        ),
        "tail-c6-isolated": (z3.BoolVal(True), [p, p, p], [0, 0, 3 * p]),
        "tail-quartic": (
            z3.And(i >= 2, i <= p - 1),
            [i, p, p, 4 * p - 2],
            [0, 0, 0, 6 * p + i - 2],
        ),
    }
    if label not in cases:
        raise ValueError(f"unknown leaf {label}")
    region, lead, tail = cases[label]
    certificate.solve_tail_case(label, region, lead, tail)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--solver-timeout-ms", type=int, default=120000)
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    parser.add_argument("--leaf", choices=LEAF_LABELS)
    args = parser.parse_args()
    if args.solver_timeout_ms <= 0 or args.budget_seconds <= 0:
        raise ValueError("certificate budgets must be positive")

    if args.leaf:
        certificate = Certificate(args.solver_timeout_ms, args.budget_seconds)
        solve_named_leaf(certificate, args.leaf)
        print("LEAF_JSON " + json.dumps(certificate.leaves[0], sort_keys=True), flush=True)
        return 0

    started = time.perf_counter()
    leaves: list[dict[str, object]] = []
    for label in LEAF_LABELS:
        if time.perf_counter() - started > args.budget_seconds:
            raise TimeoutError("symbolic certificate exceeded its declared total budget")
        completed = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--leaf",
                label,
                "--solver-timeout-ms",
                str(args.solver_timeout_ms),
                "--budget-seconds",
                str(args.budget_seconds),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=args.solver_timeout_ms / 1000 + 15,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"{label}: leaf process failed\nstdout={completed.stdout}\nstderr={completed.stderr}"
            )
        encoded = next(
            (line.removeprefix("LEAF_JSON ") for line in completed.stdout.splitlines() if line.startswith("LEAF_JSON ")),
            None,
        )
        if encoded is None:
            raise RuntimeError(f"{label}: leaf process emitted no result")
        leaves.append(json.loads(encoded))
        print(f"EXP-026 symbolic leaf PASS: {label}", flush=True)

    output = {
        "experiment": "EXP-026-grevlex-staircase",
        "status": "SYMBOLIC_CERTIFICATE_PASS",
        "solver": {"name": "Z3", "version": z3.get_version_string()},
        "domain": "all integers p>=4",
        "claims": {
            "minimal_cubic_boundary": "exactly the six declared families",
            "minimal_quartic_boundary": "exactly the declared p-2 family",
            "reduced_tails": "all declared tails are canonical, weight-equal, and grevlex-smaller",
        },
        "deductive_closure_outside_solver": {
            "degree_at_least_five": (
                "E_4=[0,24p-1] and X_0 last imply "
                "N_(n,s)=X_0^(n-4)N_(4,s) for every n>=4; the staircase has no later boundary"
            )
        },
        "execution_model": "one fresh solver subprocess per proof obligation",
        "leaf_query_count": len(leaves),
        "all_leaf_results": "unsat",
        "query_aggregate": digest([leaf["query_sha256"] for leaf in leaves]),
        "elapsed_seconds": time.perf_counter() - started,
        "leaves": leaves,
    }
    write_json_atomic(args.output, output)
    print(
        f"EXP-026 symbolic certificate PASS leaves={output['leaf_query_count']} "
        f"aggregate={output['query_aggregate']} elapsed={output['elapsed_seconds']:.3f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
