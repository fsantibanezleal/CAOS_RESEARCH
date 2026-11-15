"""Rebuild the EXP-026 obligations (and four perturbed controls) and decide them with cvc5 and Z3.

The obligations are built by EXP-026's own `symbolic_certificate.py`, imported by path and never copied; the
only addition is a subclass that captures the solver instead of checking it. The controls reuse the same
code paths with one declared perturbation each (a hook on `cubic_candidate` or `solve_tail_case`).
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import time
from pathlib import Path

import z3

HERE = Path(__file__).resolve().parent
EXP026 = HERE.parent / "EXP-026-grevlex-staircase"
CERTIFICATE_PATH = EXP026 / "symbolic_certificate.py"
STORED_PATH = EXP026 / "artifacts" / "symbolic-certificate.json"

CONTROLS = {
    "C1": ("cubic-completeness", "the family X_p^3 = (p,p,p) removed from the cubic candidate set"),
    "C2": ("cubic-soundness", "the triple (0,0,0) added to the cubic candidate set"),
    "C3": ("tail-c1-first", "the declared tail (0,3p,10p) replaced by (0,3p,10p+1)"),
    "C4": ("tail-quartic", "the index range widened from i >= 2 to i >= 1"),
}


def load_exp026():
    if not CERTIFICATE_PATH.exists():
        raise FileNotFoundError(f"EXP-026 module missing: {CERTIFICATE_PATH}")
    spec = importlib.util.spec_from_file_location("exp026_symbolic_certificate", CERTIFICATE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["exp026_symbolic_certificate"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def build_obligation(label: str, control: str | None = None):
    """The z3 solver (not yet checked) of one obligation, built by EXP-026's code paths."""
    module = load_exp026()

    class Capturing(module.Certificate):
        captured: z3.Solver | None = None

        def solve_unsat(self, name: str, counterexample: z3.BoolRef) -> None:
            solver = z3.Solver()
            solver.add(self.p >= 4, counterexample)
            self.captured = solver

        def cubic_candidate(self, values):
            candidate = super().cubic_candidate(values)
            a, b, c = values
            if control == "C1":
                # children of Or(And(a=p,b=p,c=p), Exists(...)): keep only the indexed families
                return z3.Or(candidate.children()[1])
            if control == "C2":
                return z3.Or(candidate, z3.And(a == 0, b == 0, c == 0))
            return candidate

        def solve_tail_case(self, name, region, lead, tail):
            if control == "C3":
                tail = [tail[0], tail[1], tail[2] + 1]
            if control == "C4":
                region = z3.And(z3.Int("tail_index") >= 1, z3.Int("tail_index") <= self.p - 1)
            super().solve_tail_case(name, region, lead, tail)

    certificate = Capturing(timeout_ms=1000, budget_seconds=10**9)
    module.solve_named_leaf(certificate, label)
    assert certificate.captured is not None, "obligation was not captured"
    return certificate.captured


def z3_native_check(solver: z3.Solver, timeout_ms: int) -> dict:
    """The check EXP-026 ran on the solver itself; its query text is hashed after this call."""
    solver.set(timeout=timeout_ms)
    started = time.perf_counter()
    answer = solver.check()
    return {"result": str(answer), "seconds": time.perf_counter() - started, "timeout_ms": timeout_ms}


def cvc5_decide(smt2: str, tlimit_ms: int) -> dict:
    import cvc5

    solver = cvc5.Solver()
    solver.setOption("produce-models", "true")
    solver.setOption("tlimit-per", str(tlimit_ms))
    solver.setLogic("LIA")
    symbols = cvc5.SymbolManager(solver)
    parser = cvc5.InputParser(solver, symbols)
    parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6, smt2, "obligation")
    commands = 0
    while True:
        command = parser.nextCommand()
        if command.isNull():
            break
        if command.getCommandName() == "check-sat":
            continue  # z3's export ends with (check-sat); the timed checkSat below replaces it
        command.invoke(solver, symbols)
        commands += 1
    started = time.perf_counter()
    answer = solver.checkSat()
    elapsed = time.perf_counter() - started
    result = "sat" if answer.isSat() else "unsat" if answer.isUnsat() else "unknown"
    record = {"result": result, "seconds": elapsed, "commands": commands, "tlimit_ms": tlimit_ms}
    if result == "sat":
        record["model"] = {str(term): int(solver.getValue(term).getIntegerValue())
                           for term in symbols.getDeclaredTerms()}
    if result == "unknown":
        record["reason"] = str(answer.getUnknownExplanation())
    return record


def z3_decide(smt2: str, timeout_ms: int) -> dict:
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    solver.add(z3.parse_smt2_string(smt2))
    started = time.perf_counter()
    answer = solver.check()
    return {"result": str(answer), "seconds": time.perf_counter() - started, "timeout_ms": timeout_ms}


def cvc5_version() -> str:
    import cvc5

    version = cvc5.Solver().getVersion()
    return version.decode() if isinstance(version, bytes) else str(version)
