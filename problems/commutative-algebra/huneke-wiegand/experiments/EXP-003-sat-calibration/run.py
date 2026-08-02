"""Run the declared EXP-003 Z3 calibration and independent checks."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import z3

from checker import analyze_model, semigroup_vector


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
CANDIDATE_G = (
    56, 57, 58, 63, 64, 70, 71, 72, 73, 74, 75, 76, 77,
    78, 79, 80, 81, 82, 83, 87, 89, 90, 93, 95, 96, 97,
)
CONTROL_G = (4, 5)
TIMEOUT_MS = 300_000


def log(message: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {message}"
    print(line, flush=True)
    with (ARTIFACTS / "run-log.txt").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    log(f"PASS {message}")


def membership_hash(membership: list[bool]) -> str:
    bits = "".join("1" if value else "0" for value in membership)
    return hashlib.sha256(bits.encode("ascii")).hexdigest()


def build_solver(
    frobenius: int,
    shift: int,
    pinned: list[bool] | None = None,
) -> tuple[z3.Solver, list[z3.BoolRef]]:
    solver = z3.Solver()
    solver.set(timeout=TIMEOUT_MS, random_seed=0)
    h = [z3.Bool(f"h_{value}") for value in range(frobenius + 1)]

    def member(value: int):
        if value < 0:
            return z3.BoolVal(False)
        if value > frobenius:
            return z3.BoolVal(True)
        return h[value]

    def inverse_member(value: int):
        return z3.And(member(value), member(value + shift))

    def square_inverse_member(value: int):
        return z3.And(member(value), member(value + shift), member(value + 2 * shift))

    solver.add(h[0], z3.Not(h[frobenius]), z3.Not(h[shift]))
    for value in range(frobenius + 1):
        solver.add(h[value] == z3.Not(h[frobenius - value]))
    for left in range(frobenius + 1):
        for right in range(left, frobenius + 1 - left):
            solver.add(z3.Implies(z3.And(h[left], h[right]), h[left + right]))
    for value in range(2 * frobenius + 2):
        decompositions = [
            z3.And(inverse_member(left), inverse_member(value - left))
            for left in range(value + 1)
        ]
        solver.add(z3.Implies(square_inverse_member(value), z3.Or(*decompositions)))
    if pinned is not None:
        if len(pinned) != frobenius + 1:
            raise ValueError("pinned model has wrong length")
        solver.add(*(variable == value for variable, value in zip(h, pinned, strict=True)))
    return solver, h


def solve_pinned(
    frobenius: int,
    shift: int,
    membership: list[bool],
) -> dict[str, object]:
    started = time.perf_counter()
    solver, variables = build_solver(frobenius, shift, membership)
    constraint_count = len(solver.assertions())
    status = solver.check()
    elapsed = time.perf_counter() - started
    result: dict[str, object] = {
        "status": str(status),
        "seconds": elapsed,
        "constraint_count": constraint_count,
    }
    if status == z3.sat:
        model = solver.model()
        extracted = [z3.is_true(model.evaluate(variable, model_completion=True)) for variable in variables]
        result["membership"] = extracted
        result["membership_sha256"] = membership_hash(extracted)
    return result


def run_checker(model_path: Path, report_path: Path, expected_accept: bool) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "checker.py"),
            "--model",
            str(model_path),
            "--report",
            str(report_path),
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    require(
        (completed.returncode == 0) == expected_accept,
        f"independent checker expected_accept={expected_accept}",
    )


def main() -> int:
    ARTIFACTS.mkdir(exist_ok=True)
    (ARTIFACTS / "run-log.txt").write_text("", encoding="utf-8")
    log(f"EXP-003 start; Z3 {z3.get_version_string()}")

    candidate_membership = semigroup_vector(CANDIDATE_G, 181)
    candidate = solve_pinned(181, 14, candidate_membership)
    require(candidate["status"] == "sat", "P1 pinned candidate is SAT")
    require(candidate["membership"] == candidate_membership, "P1 extracted model matches candidate")

    candidate_model_path = ARTIFACTS / "candidate-model.json"
    candidate_model_path.write_text(
        json.dumps(
            {"frobenius": 181, "shift": 14, "membership": candidate["membership"]},
            indent=2,
        ),
        encoding="utf-8",
    )
    run_checker(candidate_model_path, ARTIFACTS / "candidate-check.json", expected_accept=True)
    candidate_check = analyze_model(candidate["membership"], 181, 14)
    require(candidate_check["checked_window"] == [0, 363], "P2 exact finite window reaches 2F+1")
    require(candidate_check["tail_start"] <= 364, "P2 proved tail starts after encoded window")

    corrupted = list(candidate_membership)
    corrupted[1] = True
    corrupt_model_path = ARTIFACTS / "corrupt-model.json"
    corrupt_model_path.write_text(
        json.dumps({"frobenius": 181, "shift": 14, "membership": corrupted}, indent=2),
        encoding="utf-8",
    )
    run_checker(corrupt_model_path, ARTIFACTS / "corrupt-check.json", expected_accept=False)
    require(not analyze_model(corrupted, 181, 14)["accepted"], "P3 corrupted model is rejected")

    control_membership = semigroup_vector(CONTROL_G, 11)
    control_gaps = [value for value in range(1, 12) if not control_membership[value]]
    controls: dict[str, object] = {}
    for shift in control_gaps:
        direct = analyze_model(control_membership, 11, shift)
        query = solve_pinned(11, shift, control_membership)
        require(not direct["accepted"], f"P4 control gap s={shift} fails direct rigidity")
        require(bool(direct["missing_from_sum"]), f"P4 control gap s={shift} has explicit witness")
        require(query["status"] == "unsat", f"P4 pinned control gap s={shift} is UNSAT")
        controls[str(shift)] = {
            "solver": query,
            "first_missing_D_value": direct["missing_from_sum"][0],
        }

    require(candidate_check["accepted"], "P5 solver model passes independent exact checks")
    require(candidate["membership_sha256"] == membership_hash(candidate_membership), "P6 model hash recorded")
    output = {
        "verdict": "CONFIRMED",
        "predictions": {f"P{number}": "PASS" for number in range(1, 7)},
        "solver": {"name": "Z3", "version": z3.get_version_string(), "timeout_ms": TIMEOUT_MS},
        "candidate": candidate,
        "candidate_checker": candidate_check,
        "controls": controls,
    }
    (ARTIFACTS / "results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    log("EXP-003 CONFIRMED: P1-P6 pass")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        ARTIFACTS.mkdir(exist_ok=True)
        log(f"FAIL {type(exc).__name__}: {exc}")
        raise
