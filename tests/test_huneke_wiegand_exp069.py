"""EXP-069 tests: rebuilt queries are the certified ones; controls are sat for both solvers; the evaluator is exact."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP026 = ROOT / "problems/commutative-algebra/huneke-wiegand/experiments/EXP-026-grevlex-staircase"
EXP069 = ROOT / "problems/commutative-algebra/huneke-wiegand/experiments/EXP-069-staircase-certificate-second-solver"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_leaf(*args: str) -> dict:
    done = subprocess.run([sys.executable, str(EXP069 / "run.py"), *args], capture_output=True, text=True,
                          timeout=900, cwd=ROOT)
    assert done.returncode == 0, done.stderr + done.stdout
    line = next(x for x in done.stdout.splitlines() if x.startswith("RECORD_JSON "))
    return json.loads(line.removeprefix("RECORD_JSON "))


def test_rebuilt_digest_equals_stored_digest() -> None:
    stored = json.loads((EXP026 / "artifacts/symbolic-certificate.json").read_text(encoding="utf-8"))
    expected = {leaf["label"]: leaf["query_sha256"] for leaf in stored["leaves"]}
    record = run_leaf("--leaf", "tail-c6-isolated", "--rebuild-only")
    assert record["query_sha256"] == expected["tail-c6-isolated"]
    assert record["digest_match"] is True


def test_cheapest_control_is_sat_for_both_solvers_and_exactly_evaluated() -> None:
    record = run_leaf("--control", "C3", "--tlimit-ms", "120000")
    assert record["cvc5"]["result"] == "sat"
    assert record["z3"]["result"] == "sat"
    assert record["evaluator"]["verdict"] is True


def test_evaluator_is_exact_on_small_quantified_formulas() -> None:
    exact = load("exp069_exact_eval", EXP069 / "exact_eval.py")
    text = """(declare-fun n () Int)
(assert (exists ((k Int) (m Int)) (and (>= k 0) (<= k n) (>= m k) (<= m 5) (= (+ k m) 7) (> k 1))))"""
    assert exact.evaluate_assertions(text, {"n": 3}) is True   # k=2, m=5
    assert exact.evaluate_assertions(text, {"n": 1}) is False  # k>1 impossible
    nested = """(declare-fun n () Int)
(assert (not (exists ((k Int)) (and (>= k 0) (<= k n) (= (* 2 k) 3)))))"""
    assert exact.evaluate_assertions(nested, {"n": 10}) is True
    lets = """(declare-fun n () Int)
(assert (let (($x (>= n 4))) (let (($y (or $x (= n 0)))) (and $y (not (= n 7))))))"""
    assert exact.evaluate_assertions(lets, {"n": 4}) is True
    assert exact.evaluate_assertions(lets, {"n": 7}) is False
    assert exact.evaluate_assertions(lets, {"n": 2}) is False


def test_evaluator_refuses_an_unbounded_quantifier() -> None:
    exact = load("exp069_exact_eval_unbounded", EXP069 / "exact_eval.py")
    text = "(declare-fun n () Int)\n(assert (exists ((k Int)) (> k n)))"
    with pytest.raises(exact.Unevaluable):
        exact.evaluate_assertions(text, {"n": 1})
