"""Adversarial checks of EXP-004's count conventions and fail-closed runner."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / (
    "problems/number-theory/riemann-hypothesis/"
    "experiments/EXP-004-parity-density-transfer/run.py"
)
SPEC = importlib.util.spec_from_file_location("riemann_parity_runner", RUNNER)
parity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(parity)


@pytest.mark.parametrize("multiplicity", range(1, 13))
def test_real_and_conjugate_atom_conventions(multiplicity):
    m = multiplicity
    real = parity.atom("real", m)
    pair = parity.atom("pair", m)
    assert real["N"] == m and real["Z"] == 1
    assert real["s"] == (m == 1)
    assert real["O"] == (m % 2)
    assert real["E"] == (m - 2 if m >= 2 else 0)
    assert pair == {"N": 2 * m, "s": 0, "r": 0, "b": 1, "O": 0, "E": 2 * m - 2, "Z": 2}
    assert real["s"] + real["E"] - real["O"] >= 0


@pytest.mark.parametrize("bad", [True, 0, -1, "3", Fraction(3), 1.5])
def test_multiplicity_requires_an_actual_positive_integer(bad):
    with pytest.raises(ValueError, match="positive integer"):
        parity.atom("real", bad)


def test_mixed_multiplicity_counts_and_rational_slack():
    # 1+2+3 real copies and conjugate pairs of multiplicities 1 and 3.
    counts = parity.multiset([1, 2, 3], [1, 3])
    assert counts == {"N": 14, "s": 1, "r": 2, "b": 2, "O": 2, "E": 5, "Z": 7}
    value = parity.residuals(counts, "1/3", "2/5")
    assert value["charge"] == 4
    assert value["A"] == Fraction(25, 3)
    assert value["B"] == Fraction(50, 3)
    assert value["Q"] == Fraction(566, 15)


def test_odd_mass_cannot_replace_distinct_odd_support():
    triple = parity.multiset([3])
    forged = {**triple, "O": 3}
    with pytest.raises(parity.VerificationError, match="Odd-support charge"):
        parity.residuals(forged)
    assert parity.residuals(triple)["charge"] == 0
    assert 2 * triple["Z"] < triple["N"] + triple["s"]


def test_nonreal_pair_cannot_be_counted_as_one_copy_or_one_support():
    pair = parity.multiset([], [1])
    with pytest.raises(parity.VerificationError, match="Multiplicity excess"):
        parity.residuals({**pair, "N": 1})
    with pytest.raises(parity.VerificationError, match="Distinct count"):
        parity.residuals({**pair, "Z": 1})
    assert parity.residuals(pair)["B"] == 6


def test_negative_slack_and_float_input_fail_closed():
    for sigma, defect in [(-1, 0), (0, "-1/3"), (0.1, 0), (True, 0)]:
        with pytest.raises(ValueError):
            parity.residuals(parity.multiset([1]), sigma, defect)


@pytest.mark.parametrize("c,odd,s,e,active", [
    ("-2", "1/2", "0", "1/2", "zero"),
    ("-1", "1/2", "0", "1/2", "zero"),
    ("2", "1", "2", "0", "c"),
    ("1", "1", "1", "0", "c"),
    ("-1/2", "1", "1/2", "1/2", "parity"),
    ("1/2", "1", "5/6", "1/6", "parity"),
])
def test_relaxation_primal_dual_regimes(c, odd, s, e, active):
    witness = parity.relaxation_witness(c, odd)
    assert witness["s"] == s and witness["e"] == e
    assert witness["active_bound"] == active
    dual = list(map(Fraction, witness["dual"]))
    # Independently combine the declared constraint normals.
    normals = ((1, 0), (0, 1), (1, -2), (1, 1))
    assert tuple(sum(y * row[j] for y, row in zip(dual, normals)) for j in range(2)) == (1, 0)
    assert dual[2] * Fraction(c) + dual[3] * Fraction(odd) == Fraction(s)


def test_relaxation_rejects_negative_odd_count():
    with pytest.raises(ValueError, match="nonnegative"):
        parity.relaxation_witness(0, "-1/10")


def test_universal_symbolic_and_sharpness_controls():
    symbolic = parity.symbolic_checks()
    assert symbolic["residual_identities"] == 2
    assert symbolic["multiplicity_regression_cases"] == 24
    assert symbolic["universal_atom_charges"]["odd_real_m=2j+3"] == "2*j"
    relaxation = parity.relaxation_checks()
    assert relaxation["cases"] == 42
    assert {row["active_bound"] for row in relaxation["witnesses"]} == {"zero", "c", "parity"}
    sharpness = parity.sharpness_checks()
    assert sharpness["cases"] == 36
    assert sharpness["negative_control"]["false_half_sum_residual"] == -1
    assert all(row["A"] == row["B"] == 0 for row in sharpness["witnesses"])


def test_threshold_keeps_unproved_numeric_constants_null():
    result = parity.threshold_checks()
    assert Fraction(result["c_alpha_upper"]) == Fraction(-1801, 20400)
    assert Fraction(result["derivative_cap"]) == Fraction(10000, 2601) < 4
    for field in ("classical_a", "kappa", "theta0_numeric", "theta1_decimal"):
        assert result[field] is None


def test_census_stop_preserves_exact_prefix_and_provenance(tmp_path):
    class StopAfterFive:
        calls = 0

        def check(self):
            self.calls += 1
            if self.calls > 5:
                raise TimeoutError("test budget stop")

    source = {"declaration_commit": parity.DECLARATION, "runner": {"sha256": "test-only"}}
    with pytest.raises(TimeoutError, match="test budget stop"):
        parity.run_census(tmp_path, source, StopAfterFive(), lambda _: None)
    checkpoint = json.loads((tmp_path / "census-checkpoint.json").read_text())
    raw = (tmp_path / "census.jsonl").read_bytes()
    rows = [json.loads(line) for line in raw.splitlines()]
    assert len(rows) == checkpoint["next_index"] == 5
    assert [row[0] for row in rows] == list(range(5))
    assert rows[0][1:10] == [0] * 9
    assert rows[4][1:10] == [0] * 7 + [1, 1]
    assert checkpoint["raw_prefix_sha256"] == hashlib.sha256(raw).hexdigest()
    assert checkpoint["source_identity"] == source
    assert checkpoint["status"] == "incomplete"
    assert not (tmp_path / "result.json").exists()


def test_committed_input_requires_exact_bytes_including_line_endings(tmp_path, monkeypatch):
    path = tmp_path / "input.md"
    original = b"Committed source\nsecond line\n"
    path.write_bytes(original)
    monkeypatch.setattr(parity.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(stdout=original))
    receipt = parity.committed_input(path, "test-commit", tmp_path)
    assert receipt["sha256"] == hashlib.sha256(original).hexdigest()
    path.write_bytes(original.replace(b"\n", b"\r\n"))
    with pytest.raises(parity.VerificationError, match="Committed input differs"):
        parity.committed_input(path, "test-commit", tmp_path)


def test_runner_writes_budget_failure_and_refuses_existing_output(tmp_path, monkeypatch):
    output = tmp_path / "failed-run"
    original_deadline = parity.Deadline
    monkeypatch.setattr(parity, "Deadline", lambda: original_deadline(0))
    monkeypatch.setattr(parity, "provenance", lambda: {"test": "synthetic-source"})
    assert parity.run(output) == 1
    failure = json.loads((output / "failure.json").read_text())
    assert failure["arithmetic_status"] == "inconclusive_budget"
    assert not (output / "result.json").exists()
    before = {path.name: path.read_bytes() for path in output.iterdir()}
    with pytest.raises(FileExistsError):
        parity.run(output)
    assert before == {path.name: path.read_bytes() for path in output.iterdir()}
    operational = json.loads((output / "operational.json").read_text())
    assert operational["stdout_sha256"] == hashlib.sha256((output / "stdout.log").read_bytes()).hexdigest()


def test_runner_source_failure_is_not_a_pass(tmp_path, monkeypatch):
    def fail_source():
        raise parity.VerificationError("Committed input differs: test fixture")

    monkeypatch.setattr(parity, "provenance", fail_source)
    output = tmp_path / "source-failure"
    assert parity.run(output) == 1
    failure = json.loads((output / "failure.json").read_text())
    assert failure["arithmetic_status"] == "failed"
    assert failure["all_height_theorem"] == "not_confirmed"
    assert not (output / "result.json").exists()


def test_canonical_encoding_is_deterministic_and_immutable(tmp_path):
    assert parity.canonical({"b": 1, "a": [2, 3]}) == b'{"a":[2,3],"b":1}\n'
    target = tmp_path / "artifact.json"
    parity.write_new(target, {"first": True})
    with pytest.raises(FileExistsError):
        parity.write_new(target, {"second": True})
    assert target.read_bytes() == b'{"first":true}\n'
