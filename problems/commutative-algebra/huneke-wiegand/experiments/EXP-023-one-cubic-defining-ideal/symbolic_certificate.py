"""Bounded Presburger certificate for the EXP-023 factorization graphs."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import z3


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "symbolic-certificate.json"


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return digest_text(encoded)


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


@dataclass(frozen=True)
class Cell:
    """The half-open affine cell L*p/D <= t < U*p/D."""

    denominator: int
    lower: int
    upper: int
    depth: int = 0

    def condition(self, p: z3.ArithRef, t: z3.ArithRef) -> z3.BoolRef:
        return z3.And(
            self.denominator * t >= self.lower * p,
            self.denominator * t < self.upper * p,
        )

    def split(self) -> tuple[Cell, Cell]:
        return (
            Cell(2 * self.denominator, 2 * self.lower, self.lower + self.upper, self.depth + 1),
            Cell(2 * self.denominator, self.lower + self.upper, 2 * self.upper, self.depth + 1),
        )

    def record(self) -> dict[str, int]:
        return {
            "denominator": self.denominator,
            "lower": self.lower,
            "upper": self.upper,
            "depth": self.depth,
        }


class Certificate:
    def __init__(self, timeout_ms: int, max_split_depth: int, budget_seconds: float) -> None:
        self.timeout_ms = timeout_ms
        self.max_split_depth = max_split_depth
        self.budget_seconds = budget_seconds
        self.started = time.perf_counter()
        self.leaves: list[dict[str, object]] = []
        self.split_count = 0
        self.p, self.t, self.a = z3.Ints("p t a")

    def elapsed(self) -> float:
        return time.perf_counter() - self.started

    def bounded(self, value: z3.ArithRef, lower: z3.ArithRef, upper: z3.ArithRef) -> z3.BoolRef:
        return z3.And(value >= lower, value <= upper)

    def generators(self, value: z3.ArithRef) -> z3.BoolRef:
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

    def fiber(self, value: z3.ArithRef, degree: int) -> z3.BoolRef:
        p = self.p
        if degree == 1:
            return self.generators(value)
        if degree == 2:
            return z3.Or(
                self.bounded(value, 0, 2 * p),
                self.bounded(value, 3 * p, 5 * p - 2),
                self.bounded(value, 6 * p, 24 * p - 1),
            )
        if degree == 3:
            return z3.And(self.bounded(value, 0, 24 * p - 1), value != 6 * p - 1)
        if degree in {4, 5}:
            return self.bounded(value, 0, 24 * p - 1)
        raise ValueError(f"unsupported fiber degree {degree}")

    def vertex(self, value: z3.ArithRef, degree: int) -> z3.BoolRef:
        return z3.And(self.generators(value), self.fiber(self.t - value, degree - 1))

    def edge(self, left: z3.ArithRef, right: z3.ArithRef, degree: int) -> z3.BoolRef:
        return z3.And(
            self.vertex(left, degree),
            self.vertex(right, degree),
            self.fiber(self.t - left - right, degree - 2),
        )

    def reach(self, source: z3.ArithRef, hub: z3.ArithRef, degree: int, steps: int) -> z3.BoolRef:
        middle = [z3.FreshInt(f"reach_d{degree}") for _ in range(steps - 1)]
        path = [source, *middle, hub]
        clauses = [
            z3.Or(path[index] == path[index + 1], self.edge(path[index], path[index + 1], degree))
            for index in range(steps)
        ]
        return z3.Exists(middle, z3.And(*clauses)) if middle else z3.And(*clauses)

    def zero_direct(self, source: z3.ArithRef, degree: int) -> z3.BoolRef:
        other = z3.FreshInt(f"zero_d{degree}")
        return z3.Exists(
            other,
            z3.And(
                self.generators(other),
                self.fiber(self.t - source - other, degree - 2),
                z3.Not(self.fiber(self.t - other, degree - 1)),
            ),
        )

    def zero_with_one_move(self, source: z3.ArithRef, degree: int) -> z3.BoolRef:
        neighbor = z3.FreshInt(f"zero_neighbor_d{degree}")
        return z3.Or(
            self.zero_direct(source, degree),
            z3.Exists(
                neighbor,
                z3.And(
                    self.vertex(neighbor, degree),
                    self.edge(source, neighbor, degree),
                    self.zero_direct(neighbor, degree),
                ),
            ),
        )

    def solve(
        self,
        label: str,
        claim: z3.BoolRef,
        region: z3.BoolRef | None = None,
        cell: Cell | None = None,
    ) -> None:
        if self.elapsed() > self.budget_seconds:
            raise TimeoutError("symbolic certificate exceeded its declared total budget")
        solver = z3.Solver()
        solver.set(timeout=self.timeout_ms)
        solver.add(self.p >= 4, self.vertex(self.a, self._degree_from_label(label)))
        if region is not None:
            solver.add(region)
        if cell is not None:
            solver.add(cell.condition(self.p, self.t))
        solver.add(z3.Not(claim))
        started = time.perf_counter()
        result = solver.check()
        elapsed = time.perf_counter() - started
        query_hash = digest_text(solver.sexpr())
        if result == z3.unsat:
            self.leaves.append(
                {
                    "label": label,
                    "result": "unsat",
                    "cell": cell.record() if cell is not None else None,
                    "query_sha256": query_hash,
                    "elapsed_seconds": elapsed,
                }
            )
            return
        if result == z3.sat:
            raise AssertionError(f"{label}: symbolic counterexample: {solver.model()}")
        if cell is None or cell.depth >= self.max_split_depth:
            raise TimeoutError(f"{label}: unresolved solver result {result}")
        self.split_count += 1
        for child in cell.split():
            self.solve(label, claim, region=region, cell=child)

    @staticmethod
    def _degree_from_label(label: str) -> int:
        marker = label.split(":", 1)[0]
        return int(marker.removeprefix("d"))

    def cover_cells(
        self,
        label_prefix: str,
        first: int,
        last_exclusive: int,
        claim_factory: Callable[[], z3.BoolRef],
        region: z3.BoolRef | None = None,
    ) -> None:
        for coefficient in range(first, last_exclusive):
            self.solve(
                f"{label_prefix}:cell-{coefficient}",
                claim_factory(),
                region=region,
                cell=Cell(1, coefficient, coefficient + 1),
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--solver-timeout-ms", type=int, default=5000)
    parser.add_argument("--max-split-depth", type=int, default=5)
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    args = parser.parse_args()
    if args.solver_timeout_ms <= 0 or args.max_split_depth < 0 or args.budget_seconds <= 0:
        raise ValueError("certificate budgets must be positive")
    certificate = Certificate(args.solver_timeout_ms, args.max_split_depth, args.budget_seconds)
    p, t, a = certificate.p, certificate.t, certificate.a

    # Degree three: five valid regions with explicit hubs; t=3p is handled separately.
    degree_three_regions = (
        ("d3:low", certificate.bounded(t, 0, 2 * p), z3.IntVal(0)),
        ("d3:first-gap", certificate.bounded(t, 2 * p + 1, 3 * p - 1), t - 2 * p),
        ("d3:middle", certificate.bounded(t, 3 * p + 1, 5 * p - 2), z3.IntVal(0)),
        ("d3:second-gap", certificate.bounded(t, 5 * p - 1, 6 * p - 2), t - (5 * p - 2)),
    )
    for label, region, hub in degree_three_regions:
        certificate.solve(label, certificate.reach(a, hub, 3, 3), region=region)
    certificate.cover_cells(
        "d3:high-valid",
        6,
        24,
        lambda: certificate.reach(a, z3.IntVal(0), 3, 3),
    )

    # At total 3p the vertices are exactly 0,p,3p; 0 and 3p are joined and p is isolated.
    other_vertex = z3.And(a != 0, a != p, a != 3 * p)
    certificate.solve(
        "d3:exception-vertices",
        z3.Not(other_vertex),
        region=t == 3 * p,
    )
    certificate.solve(
        "d3:exception-main-edge",
        certificate.edge(z3.IntVal(0), 3 * p, 3),
        region=t == 3 * p,
    )
    certificate.solve(
        "d3:exception-isolation",
        z3.Not(z3.Or(certificate.edge(p, z3.IntVal(0), 3), certificate.edge(p, 3 * p, 3))),
        region=t == 3 * p,
    )

    # Invalid degree-three totals: the single hole and the high tail reach zero in <=1 move.
    certificate.solve(
        "d3:hole-zero",
        certificate.zero_with_one_move(a, 3),
        region=t == 6 * p - 1,
    )
    certificate.cover_cells(
        "d3:high-zero",
        24,
        42,
        lambda: certificate.zero_with_one_move(a, 3),
    )

    # Degree four: hub zero except at 6p-1, where p is an explicit hub.
    certificate.cover_cells(
        "d4:valid",
        0,
        24,
        lambda: certificate.reach(a, z3.IntVal(0), 4, 3),
        region=t != 6 * p - 1,
    )
    certificate.solve(
        "d4:hole-hub",
        certificate.reach(a, p, 4, 3),
        region=t == 6 * p - 1,
    )
    certificate.cover_cells(
        "d4:high-zero",
        24,
        42,
        lambda: certificate.zero_direct(a, 4),
    )

    # Degree five: zero is a hub within two moves; high totals die directly.
    certificate.cover_cells(
        "d5:valid",
        0,
        24,
        lambda: certificate.reach(a, z3.IntVal(0), 5, 2),
    )
    certificate.cover_cells(
        "d5:high-zero",
        24,
        42,
        lambda: certificate.zero_direct(a, 5),
    )

    output = {
        "experiment": "EXP-023-one-cubic-defining-ideal",
        "status": "SYMBOLIC_CERTIFICATE_PASS",
        "solver": {"name": "Z3", "version": z3.get_version_string()},
        "domain": "all integers p>=4",
        "claims": {
            "degree_three": "one component per valid total except two at 3p; invalid totals reach zero",
            "degree_four": "one component per valid total; invalid totals reach zero",
            "degree_five": "one component per valid total; invalid totals reach zero",
            "maximum_valid_path_lengths": {"3": 3, "4": 3, "5": 2},
        },
        "leaf_query_count": len(certificate.leaves),
        "split_count": certificate.split_count,
        "all_leaf_results": "unsat",
        "query_aggregate": digest([leaf["query_sha256"] for leaf in certificate.leaves]),
        "elapsed_seconds": certificate.elapsed(),
        "leaves": certificate.leaves,
    }
    write_json_atomic(args.output, output)
    print(
        f"EXP-023 symbolic certificate PASS leaves={output['leaf_query_count']} "
        f"splits={output['split_count']} aggregate={output['query_aggregate']} "
        f"elapsed={output['elapsed_seconds']:.3f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
