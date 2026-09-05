"""Exact uniform low-source identity and finite-artifact regression."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "problems/commutative-algebra/huneke-wiegand/experiments"
EXP = EXPERIMENTS / "EXP-056-uniform-low-source"
RESULTS = EXP / "artifacts/results.json"
RESULTS_SHA256 = "cf8678a5f39d9d0033f127cf92b28708cd59db1e3f4b0258add41da3e9cbafca"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUN = load("hw_exp056_run", EXP / "run.py")
ARITHMETIC = load("hw_exp056_independent", EXPERIMENTS / "EXP-054-full-source-boundary/audit.py")
CANDIDATE = load("hw_exp056_candidate", EXPERIMENTS / "EXP-052-semantic-unreduced-lifts/candidate.py")


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def independent_target(p: int) -> dict:
    intervals = {"L0": (1, p), "L1": (3 * p, 4 * p - 2),
                 "H0": (6 * p, 8 * p - 2), "H2": (10 * p, 10 * p)}

    def endpoint(token: list) -> int:
        tag, direction, offset = token
        first, last = intervals[tag]
        assert direction in ("L", "R") and 0 <= offset <= last - first
        return first + offset if direction == "L" else last - offset

    low = {*range(1, p + 1), *range(3 * p, 4 * p - 1)}
    target = {}
    for completion in (59, 62):
        for weight, token in CANDIDATE.candidate(p, 58, completion):
            missing = {endpoint(item) for item in token["l0_missing"] + token["l1_missing"]}
            high = {endpoint(item) for item in token["high_selected"]}
            assert high == {6 * p, 10 * p}
            row = ("D", tuple(sorted((low - missing) | high)), token["kind"],
                   token["product"][0] * p + token["product"][1])
            assert row not in target and weight != 0
            target[row] = weight
    return target


def independent_source(p: int) -> dict:
    low = {*range(1, p + 1), *range(3 * p, 4 * p - 1)}
    terms = {}
    for a in range(1, p + 1):
        for j in (1, 2):
            if j == 2 and 1 <= a <= p - 4:
                weight = -1 if a % 2 == 0 else 1
            elif j == 2 and a == p - 3:
                weight = -1 if p % 2 == 0 else 1
            elif j == 1 and a == p - 2:
                weight = -2 if p % 2 == 0 else 2
            elif j == 1 and a == p - 3:
                weight = 2 if p % 2 == 0 else -2
            else:
                continue
            exterior = tuple(sorted((low - {a, 3 * p, 3 * p + j}) | {6 * p, 10 * p}))
            terms[("S", exterior, a + j - 2)] = weight
    return terms


def test_complete_artifact_hash_and_all_93_rows() -> None:
    assert hashlib.sha256(RESULTS.read_bytes()).hexdigest() == RESULTS_SHA256
    result = json.loads(RESULTS.read_text(encoding="utf-8"))
    assert result["artifact_hash"] == digest({k: v for k, v in result.items() if k != "artifact_hash"})
    assert result["parameters"] == [8, 100]
    assert result["status"] == "COMPLETE" and result["training_recovery"] == [8, 9, 10]
    assert result["p11_original_source_accessed"] is False
    assert result["claims"]["uniform_nontriviality_or_order_two"] == "NOT_ESTABLISHED"
    assert len(result["rows"]) == 93
    assert [row["p"] for row in result["rows"]] == list(range(8, 101))
    for row in result["rows"]:
        p = row["p"]
        source, gamma = RUN.source_and_gamma(p)
        assert row["source_hash"] == digest(source)
        assert ARITHMETIC.sparse(source) == independent_source(p)
        assert row["source_support"] == row["gamma_support"] == len(gamma) == p - 1
        assert row["d_support"] == 6 * p - 30 + p * (p - 1) // 2 - 5
        assert all(row[name] is True for name in (
            "full_boundary_identity", "independent_agreement", "sign_mutation_rejected"))


def test_symbolic_source_recovers_half_of_saved_training_slice() -> None:
    path = EXPERIMENTS / "EXP-055-unit-filler-and-low-complement/artifacts/results.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "c54419a4b0de90ffc5caccaa6bc71ac7b3758bc88cd7bbc5ba9671831cad6bc7")
    training = json.loads(path.read_text(encoding="utf-8"))
    for row in training["training"]:
        assert ARITHMETIC.sparse(row["fixed_high_source"]) == {
            index: 2 * coefficient for index, coefficient in independent_source(row["p"]).items()}


@pytest.mark.parametrize("p", range(8, 13))
def test_independent_full_boundary_gamma_and_sign_corruption(p: int) -> None:
    source, gamma = RUN.source_and_gamma(p)
    assert ARITHMETIC.sparse(source) == independent_source(p)
    actual = ARITHMETIC.independent_boundary(p, source)
    expected_d = independent_target(p)
    assert ARITHMETIC.sparse(RUN.target_from_candidate(p, CANDIDATE)) == expected_d
    expected_gamma = {}
    for term in source:
        _, exterior, coefficient = term["exact_label"]
        low_face = tuple(value for value in exterior if value != 10 * p)
        expected_gamma[("K", low_face, 10 * p + coefficient)] = -term["coefficient"]
    assert ARITHMETIC.sparse(gamma) == expected_gamma
    assert not (expected_d.keys() & expected_gamma.keys())
    assert actual == expected_d | expected_gamma
    for index in range(len(source)):
        mutated = deepcopy(source)
        mutated[index]["coefficient"] *= -1
        assert ARITHMETIC.independent_boundary(p, mutated) != actual
    row = next(item for item in json.loads(RESULTS.read_text(encoding="utf-8"))["rows"] if item["p"] == p)
    assert row["boundary_hash"] == digest(ARITHMETIC.records(actual))


def test_small_cli_rerun_matches_canonical_prefix_deterministically(tmp_path: Path) -> None:
    original = RESULTS.read_bytes()
    canonical = json.loads(original)
    outputs = []
    for index in range(2):
        output = tmp_path / f"small-rerun-{index}.json"
        subprocess.run([sys.executable, str(EXP / "run.py"), "--maximum", "12", "--output", str(output)],
                       cwd=ROOT, check=True, capture_output=True, text=True, timeout=60)
        outputs.append(output.read_bytes())
    assert outputs[0] == outputs[1]
    rerun = json.loads(outputs[0])
    assert rerun["rows"] == canonical["rows"][:5]
    assert rerun["parameters"] == [8, 12]
    assert rerun["artifact_hash"] == digest({k: v for k, v in rerun.items() if k != "artifact_hash"})
    assert RESULTS.read_bytes() == original


@pytest.mark.parametrize("maximum", [7, 101])
def test_campaign_size_guards_do_not_write_artifacts(tmp_path: Path, maximum: int) -> None:
    output = tmp_path / "invalid-size.json"
    with pytest.raises(ValueError):
        RUN.run(output, maximum=maximum)
    assert not output.exists()


@pytest.mark.parametrize("budget", [0, -1, float("nan"), float("inf")])
def test_budget_guards_do_not_write_artifacts(tmp_path: Path, budget: float) -> None:
    output = tmp_path / "invalid-budget.json"
    with pytest.raises(ValueError):
        RUN.run(output, maximum=8, budget=budget)
    assert not output.exists()


def test_exhausted_tiny_budget_never_writes_complete_result(tmp_path: Path) -> None:
    output = tmp_path / "budget-checkpoint.json"
    with pytest.raises(RuntimeError):
        RUN.run(output, maximum=8, budget=1e-12)
    if output.exists():
        assert json.loads(output.read_text(encoding="utf-8"))["status"] == "CHECKPOINT"


def test_formula_domain_guard() -> None:
    with pytest.raises(ValueError, match="p>=8"):
        RUN.weighted_terms(7)
