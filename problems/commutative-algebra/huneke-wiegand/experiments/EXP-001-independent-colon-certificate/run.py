"""EXP-001: independent Huneke-Wiegand colon certificate.

Primary route: Singular/4ti2 toric quotient and ideal quotients.
Cross-check: standard-library-only numerical-semigroup arithmetic written from
the displayed input, without importing any upstream verifier or certificate.
"""

from __future__ import annotations

import json
import math
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
GENERATORS = (
    56, 57, 58, 63, 64, 70, 71, 72, 73, 74, 75, 76, 77,
    78, 79, 80, 81, 82, 83, 87, 89, 90, 93, 95, 96, 97,
)
EXPECTED_C1 = (56, 57, 58, 63, 64, 73, 75, 76, 79, 81, 82, 83)


def log(message: str) -> None:
    stamp = time.strftime("%H:%M:%S")
    line = f"[{stamp}] {message}"
    print(line, flush=True)
    with (ARTIFACTS / "run-log.txt").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


@dataclass(frozen=True)
class NumericalSemigroup:
    generators: tuple[int, ...]
    member: tuple[bool, ...]
    frobenius: int
    conductor: int
    multiplicity: int

    @classmethod
    def build(cls, generators: tuple[int, ...]) -> "NumericalSemigroup":
        if math.gcd(*generators) != 1:
            raise ValueError("generators must have gcd 1")
        multiplicity = min(generators)
        # A block of multiplicity consecutive members proves the infinite tail.
        limit = max(generators) + multiplicity * multiplicity * 4
        member = [False] * (limit + 1)
        member[0] = True
        for value in range(1, limit + 1):
            member[value] = any(value >= g and member[value - g] for g in generators)
        conductor = None
        for start in range(limit - multiplicity + 2):
            if all(member[start : start + multiplicity]):
                conductor = start
                break
        if conductor is None:
            raise RuntimeError("no conductor block within proved working limit")
        frobenius = conductor - 1
        return cls(generators, tuple(member), frobenius, conductor, multiplicity)

    def contains(self, value: int) -> bool:
        if value < 0:
            return False
        if value >= self.conductor:
            return True
        return self.member[value]

    def gaps(self) -> tuple[int, ...]:
        return tuple(value for value in range(self.conductor) if not self.contains(value))

    def relative_minima(self, predicate) -> tuple[int, ...]:
        first = next(value for value in range(self.conductor + self.multiplicity) if predicate(value))
        bound = self.frobenius + first
        values = [value for value in range(bound + 1) if predicate(value)]
        return tuple(
            value
            for value in values
            if not any(other < value and predicate(other) and self.contains(value - other) for other in values)
        )

    def ideal_contains(self, value: int, generators: tuple[int, ...]) -> bool:
        return any(self.contains(value - generator) for generator in generators)


def finite_route(generators: tuple[int, ...], step: int) -> dict[str, object]:
    semigroup = NumericalSemigroup.build(generators)

    def c1_predicate(value: int) -> bool:
        return semigroup.contains(value) and semigroup.contains(value + step)

    def c2_predicate(value: int) -> bool:
        return semigroup.contains(value) and semigroup.contains(value - step)

    c1 = semigroup.relative_minima(c1_predicate)
    c2 = semigroup.relative_minima(c2_predicate)
    intersection = semigroup.relative_minima(lambda x: c1_predicate(x) and c2_predicate(x))
    product_candidates = tuple(a + b for a in c1 for b in c2)
    product = tuple(
        value
        for value in sorted(set(product_candidates))
        if not any(other < value and semigroup.contains(value - other) for other in set(product_candidates))
    )
    intersection_in_product = all(semigroup.ideal_contains(value, product) for value in intersection)
    product_in_intersection = all(semigroup.ideal_contains(value, intersection) for value in product)
    return {
        "frobenius": semigroup.frobenius,
        "conductor": semigroup.conductor,
        "genus": len(semigroup.gaps()),
        "symmetric": all(
            semigroup.contains(value) != semigroup.contains(semigroup.frobenius - value)
            for value in range(semigroup.frobenius + 1)
        ),
        "colon_1_minima": c1,
        "colon_2_minima": c2,
        "intersection_minima": intersection,
        "product_minima": product,
        "equal": intersection_in_product and product_in_intersection,
        "intersection_only": tuple(
            value for value in intersection if not semigroup.ideal_contains(value, product)
        ),
    }


def wsl_path(path: Path) -> str:
    drive = path.drive.rstrip(":").lower()
    suffix = path.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{suffix}"


def run_singular(script: str, output: str, timeout: int = 600) -> str:
    log(f"Singular start: {script}")
    command = [
        "wsl.exe", "-d", "Ubuntu-24.04", "--",
        "Singular", "-q", wsl_path(ROOT / script),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    text = completed.stdout + completed.stderr
    (ARTIFACTS / output).write_text(text, encoding="utf-8")
    if completed.returncode != 0 or "? error occurred" in text:
        raise RuntimeError(f"Singular failed for {script}; see {output}")
    log(f"Singular done: {script}, return={completed.returncode}, bytes={len(text)}")
    return text


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    log(f"PASS {message}")


def main() -> int:
    ARTIFACTS.mkdir(exist_ok=True)
    (ARTIFACTS / "run-log.txt").write_text("", encoding="utf-8")
    log("EXP-001 start")

    finite_candidate = finite_route(GENERATORS, 14)
    finite_control = finite_route((4, 5), 1)
    (ARTIFACTS / "finite-results.json").write_text(
        json.dumps({"candidate": finite_candidate, "control": finite_control}, indent=2),
        encoding="utf-8",
    )

    require(finite_candidate["frobenius"] == 181, "P1 Frobenius is 181")
    require(finite_candidate["conductor"] == 182, "P1 conductor is 182")
    require(finite_candidate["genus"] == 91, "P1 genus is 91")
    require(finite_candidate["symmetric"] is True, "P1 Gamma is symmetric")
    require(finite_candidate["colon_1_minima"] == EXPECTED_C1, "P2 first colon minima")
    require(
        finite_candidate["colon_2_minima"] == tuple(value + 14 for value in EXPECTED_C1),
        "P2 second colon minima is the shift by 14",
    )
    require(finite_candidate["equal"] is True, "P5 finite candidate equality")
    require(finite_control["equal"] is False, "P5 finite control rejects equality")

    mutated = EXPECTED_C1[:-1] + (84,)
    require(finite_candidate["colon_1_minima"] != mutated, "P6 mutated expectation is rejected")

    control_output = run_singular("control.sing", "control-singular.txt", timeout=60)
    require("TORIC_DIMENSION=1" in control_output, "P4 control quotient dimension is one")
    require("COLON_EQUALITY=0" in control_output, "P4 Singular control rejects equality")
    require("CONTROL_WITNESS" in control_output, "P4 control emits residue witness")

    candidate_output = run_singular("candidate.sing", "candidate-singular.txt", timeout=600)
    require("TORIC_DIMENSION=1" in candidate_output, "P1 candidate quotient dimension is one")
    require("COLON_EQUALITY=1" in candidate_output, "P3 Singular candidate colon equality")

    summary = {
        "verdict": "CONFIRMED",
        "predictions": {f"P{number}": "PASS" for number in range(1, 7)},
        "finite": {"candidate": finite_candidate, "control": finite_control},
        "singular": {"candidate_equality": True, "control_equality": False},
    }
    (ARTIFACTS / "results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log("EXP-001 CONFIRMED: P1-P6 pass")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        ARTIFACTS.mkdir(exist_ok=True)
        log(f"FAIL {type(exc).__name__}: {exc}")
        raise
