"""Exact endpoint reduction, CPU only; preserve the declared P3 sign refutation."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import math
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
PREMISES = {
    "EXP-057-four-row-kernel-normal-form/hypothesis.md":
        "308cd480eb32443414aa14d29768a8ef4c72effe8015a7daa5a2e0216cbf6687",
    "EXP-056-uniform-low-source/run.py":
        "ded8191bc1310f5d618651d1eacd6fcd81aa438e38ee7ce7bcafc904479a0fc5",
    "EXP-054-full-source-boundary/run.py":
        "bb6c35f36da17d4e4045670348416a18d9cbb28bf5f5774fcf1deabf28ed951f",
    "EXP-054-full-source-boundary/audit.py":
        "9e21b8a03694938e04dc7aba3555944fa511e4d1ac0d4dfc92727288ed7a1b63",
    "EXP-036-factor-two-torsion-anatomy/run.py":
        "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    "EXP-052-semantic-unreduced-lifts/candidate.py":
        "6a16d8cf2c112a800558d634f6cd058ea00be43986c7b92f7f9406a6d282ca0c",
}


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENTS / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dependencies():
    for relative, expected in PREMISES.items():
        actual = hashlib.sha256((EXPERIMENTS / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"premise hash mismatch: {relative}")
    return {
        "producer": load("producer054_for_057", "EXP-054-full-source-boundary/run.py"),
        "independent": load("independent054_for_057", "EXP-054-full-source-boundary/audit.py"),
        "source": load("source056_for_057", "EXP-056-uniform-low-source/run.py"),
        "algebra": load("algebra036_for_057", "EXP-036-factor-two-torsion-anatomy/run.py"),
        "candidate": load("candidate052_for_057", "EXP-052-semantic-unreduced-lifts/candidate.py"),
    }


def low_set(p):
    if p < 8:
        raise ValueError("endpoint formula requires p>=8")
    return set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))


def g_record(p, a, j, coefficient, weight):
    exterior = (low_set(p) - {a, 3 * p, 3 * p + j}) | {6 * p}
    return {"coefficient": weight,
            "exact_label": ["K", sorted(exterior), 10 * p + coefficient]}


def q_source(p):
    exterior = (low_set(p) - {3 * p, 3 * p + 2}) | {6 * p}
    return [{"coefficient": 1, "exact_label": ["K", sorted(exterior), 10 * p]}]


def q_boundary_formula(p):
    return [g_record(p, a, 2, a, (-1) ** (a - 1)) for a in range(1, p - 1)]


def eta_formula(p):
    sign = (-1) ** p
    return [
        g_record(p, p - 3, 2, p - 3, 2 * sign),
        g_record(p, p - 2, 2, p - 2, -sign),
        g_record(p, p - 2, 1, p - 3, 2 * sign),
        g_record(p, p - 3, 1, p - 4, -2 * sign),
    ]


def add_vectors(*vectors):
    total = Counter()
    for vector, multiplier in vectors:
        for key, value in vector.items():
            total[key] += multiplier * value
    return {key: value for key, value in total.items() if value}


def check_parameter(p, modules, include_counterexample=False):
    primary = modules["producer"]
    independent = modules["independent"]
    source = modules["source"]
    algebra = modules["algebra"]
    q = q_source(p)
    q_expected = independent.sparse(q_boundary_formula(p))
    q_actual = dict(primary.multiply(p, q, algebra))
    q_secondary = independent.independent_boundary(p, q)
    assert q_actual == q_secondary == q_expected, f"p={p}: q boundary disagreement"

    s, gamma_records = source.source_and_gamma(p)
    gamma = independent.sparse(gamma_records)
    eta_records = eta_formula(p)
    eta = independent.sparse(eta_records)
    assert add_vectors((gamma, 1), (q_actual, 1)) == eta, f"p={p}: eta reduction disagreement"
    assert len(eta) == 4
    odd = {key: value % 2 for key, value in eta.items() if value % 2}
    assert len(odd) == 1
    assert next(iter(odd)) == independent.key(g_record(p, p - 2, 2, p - 2, 1)["exact_label"])

    target = independent.sparse(source.target_from_candidate(p, modules["candidate"]))
    expected_plus = add_vectors((target, 1), (eta, 1))
    plus_primary = dict(primary.multiply(p, s + q, algebra))
    plus_secondary = independent.independent_boundary(p, s + q)
    assert plus_primary == plus_secondary == expected_plus, f"p={p}: corrected plus identity failed"

    mutated_q = [{**q[0], "coefficient": -1}]
    mutation_boundary = independent.independent_boundary(p, mutated_q)
    assert mutation_boundary != q_expected, f"p={p}: q sign mutation not rejected"
    altered_eta = [dict(term) for term in eta_records]
    altered_eta[1]["coefficient"] *= -1
    assert independent.sparse(altered_eta) != eta, f"p={p}: odd-row sign mutation not rejected"

    row = {
        "p": p,
        "q_source_support": 1,
        "q_boundary_support": len(q_actual),
        "eta_support": len(eta),
        "eta_odd_rows": len(odd),
        "corrected_source_support": len(s) + 1,
        "p1_identities": True,
        "independent_agreement": True,
        "corrected_plus_identity": True,
        "q_sign_mutation_rejected": True,
        "eta_sign_mutation_rejected": True,
        "q_boundary_hash": primary.digest(primary.records(q_actual)),
        "eta_hash": primary.digest(primary.records(eta)),
        "corrected_full_boundary_hash": primary.digest(primary.records(plus_primary)),
    }
    counterexample = None
    if include_counterexample:
        minus_primary = dict(primary.multiply(p, s + mutated_q, algebra))
        minus_secondary = independent.independent_boundary(p, s + mutated_q)
        assert minus_primary == minus_secondary
        discrepancy = add_vectors((minus_primary, 1), (expected_plus, -1))
        assert discrepancy == {key: -2 * value for key, value in q_actual.items()}
        assert discrepancy, "the declared minus identity unexpectedly passed"
        row["declared_minus_identity"] = False
        counterexample = {
            "p": p,
            "declared_identity": "M(s-q)=b_A+b_B+eta",
            "declared_identity_holds": False,
            "corrected_identity": "M(s+q)=b_A+b_B+eta",
            "difference_description": "M(s-q)-(b_A+b_B+eta)=-2Mq",
            "difference": primary.records(discrepancy),
            "difference_support": len(discrepancy),
            "difference_hash": primary.digest(primary.records(discrepancy)),
        }
    return row, counterexample


def run(output, maximum=100, budget=60, continue_retained=False):
    if not isinstance(maximum, int) or not 8 <= maximum <= 100:
        raise ValueError("maximum must be an integer in the declared range 8..100")
    if not math.isfinite(budget) or budget <= 0:
        raise ValueError("budget must be finite and positive")
    started = time.monotonic()
    modules = dependencies()
    producer = modules["producer"]
    result = {
        "experiment": "EXP-057",
        "status": "CHECKPOINT",
        "overall_verdict": "REFUTED",
        "parameters_requested": [8, maximum],
        "premises": PREMISES,
        "p11_original_source_accessed": False,
        "continuation_after_p3_refutation": continue_retained,
        "rows": [],
    }

    def checkpoint():
        result["artifact_hash"] = producer.digest(
            {key: value for key, value in result.items() if key != "artifact_hash"})
        producer.write_json(output, result)

    def budget_check():
        if time.monotonic() - started > budget:
            result["status"] = "BUDGET_STOP"
            checkpoint()
            raise RuntimeError("EXP-057 budget exhausted; checkpoint retained")

    first, counterexample = check_parameter(8, modules, include_counterexample=True)
    result["rows"].append(first)
    result["p3_counterexample"] = counterexample
    result["status"] = "REFUTED_AT_SMOKE"
    result["claims"] = {
        "P1": "DERIVED_IN_PROOF",
        "P2": "PARTIAL_FINITE",
        "P3": "REFUTED",
        "corrected_plus_identity": "DERIVED_IN_PROOF",
        "uniform_nontriviality_order_two_or_upper_bound": "NOT_ESTABLISHED",
    }
    checkpoint()
    print("p=8: P3 REFUTED, discrepancy=-2Mq (6 rows); P1/P2 local checks PASS", flush=True)
    budget_check()
    if not continue_retained:
        return result

    print("Separate continuation: validate retained P1/P2 and corrected plus identity", flush=True)
    for p in range(9, maximum + 1):
        row, _ = check_parameter(p, modules)
        result["rows"].append(row)
        result["status"] = "RETAINED_CLAIMS_CHECKPOINT"
        checkpoint()
        if p <= 12 or p % 10 == 0:
            print(f"p={p}: endpoint reduction PASS, eta=4 rows, one odd row", flush=True)
        budget_check()
    result["status"] = "COMPLETE"
    result["claims"]["P2"] = "PASS_FINITE"
    checkpoint()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--maximum", type=int, default=100)
    parser.add_argument("--budget", type=float, default=60)
    parser.add_argument("--continue-retained", action="store_true")
    args = parser.parse_args()
    run(args.output, args.maximum, args.budget, args.continue_retained)
