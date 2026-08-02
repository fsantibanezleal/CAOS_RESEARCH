"""Solver-independent checker for EXP-003 semigroup models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def semigroup_vector(generators: tuple[int, ...], frobenius: int) -> list[bool]:
    """Return exact semigroup membership through the claimed Frobenius number."""
    member = [False] * (frobenius + 1)
    member[0] = True
    for value in range(1, frobenius + 1):
        member[value] = any(
            value >= generator and member[value - generator] for generator in generators
        )
    return member


def analyze_model(membership: list[bool], frobenius: int, shift: int) -> dict[str, object]:
    """Check the finite model and return exact witnesses without a SAT dependency."""
    violations: list[str] = []
    if len(membership) != frobenius + 1:
        raise ValueError("membership length must equal F+1")
    if frobenius <= 0 or frobenius % 2 == 0:
        violations.append("Frobenius number must be positive and odd")
    if not 0 < shift <= frobenius:
        violations.append("shift must lie in [1,F]")

    def member(value: int) -> bool:
        if value < 0:
            return False
        if value > frobenius:
            return True
        return membership[value]

    if not member(0):
        violations.append("zero is absent")
    if member(frobenius):
        violations.append("F is present")
    if member(shift):
        violations.append("shift is not a gap")

    symmetry_failures = [
        value
        for value in range(frobenius + 1)
        if member(value) == member(frobenius - value)
    ]
    if symmetry_failures:
        violations.append(f"symmetry fails first at {symmetry_failures[0]}")

    closure_failure = next(
        (
            (left, right)
            for left in range(frobenius + 1)
            if member(left)
            for right in range(frobenius + 1 - left)
            if member(right) and not member(left + right)
        ),
        None,
    )
    if closure_failure is not None:
        violations.append(f"closure fails at {closure_failure}")

    def inverse_member(value: int) -> bool:
        return member(value) and member(value + shift)

    def square_inverse_member(value: int) -> bool:
        return member(value) and member(value + shift) and member(value + 2 * shift)

    minimum_inverse = next(value for value in range(frobenius + 2) if inverse_member(value))
    window_end = 2 * frobenius + 1
    missing_from_sum: list[int] = []
    representations: dict[str, list[int]] = {}
    reverse_failures: list[tuple[int, int]] = []
    for value in range(window_end + 1):
        pairs = [
            (left, value - left)
            for left in range(value + 1)
            if inverse_member(left) and inverse_member(value - left)
        ]
        if square_inverse_member(value):
            if not pairs:
                missing_from_sum.append(value)
            else:
                representations[str(value)] = list(pairs[0])
        reverse_failures.extend(
            pair for pair in pairs if not square_inverse_member(value)
        )

    if missing_from_sum:
        violations.append(f"D is not contained in E+E first at {missing_from_sum[0]}")
    if reverse_failures:
        violations.append(f"E+E is not contained in D first at {reverse_failures[0]}")

    tail_start = minimum_inverse + frobenius + 1
    if tail_start > 2 * frobenius + 2:
        violations.append("tail bound exceeds encoded window")

    bitstring = "".join("1" if value else "0" for value in membership)
    return {
        "accepted": not violations,
        "violations": violations,
        "frobenius": frobenius,
        "shift": shift,
        "minimum_inverse": minimum_inverse,
        "checked_window": [0, window_end],
        "tail_start": tail_start,
        "missing_from_sum": missing_from_sum,
        "reverse_failures": reverse_failures,
        "representations": representations,
        "membership_bitstring": bitstring,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    model = json.loads(args.model.read_text(encoding="utf-8"))
    report = analyze_model(model["membership"], model["frobenius"], model["shift"])
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("accepted", "violations", "tail_start")}))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
