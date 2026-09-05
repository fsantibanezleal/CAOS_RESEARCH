"""Uniform low-source identity, exact CPU stress tests; no rank calculations."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def weighted_terms(p):
    if p < 8:
        raise ValueError("uniform formula requires p>=8")
    return [(a, 2, a, (-1) ** (a + 1)) for a in range(1, p - 3)] + [
        (p - 3, 2, p - 3, (-1) ** (p + 1)),
        (p - 2, 1, p - 3, 2 * (-1) ** (p + 1)),
        (p - 3, 1, p - 4, 2 * (-1) ** p),
    ]


def source_and_gamma(p):
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    source, gamma = [], []
    for a, j, coefficient, weight in weighted_terms(p):
        selected = low - {a, 3 * p, 3 * p + j}
        source.append({"coefficient": weight,
                       "exact_label": ["S", sorted(selected | {6 * p, 10 * p}), coefficient]})
        gamma.append({"coefficient": -weight,
                      "exact_label": ["K", sorted(selected | {6 * p}), 10 * p + coefficient]})
    return source, gamma


def decode_endpoint(token, p):
    tag, end, offset = token
    first, last = (1, p) if tag == "L0" else (3 * p, 4 * p - 2)
    return first + offset if end == "L" else last - offset


def target_from_candidate(p, candidate):
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    records = []
    for completion in (59, 62):
        for weight, token in candidate.candidate(p, 58, completion):
            missing = {decode_endpoint(item, p) for item in token["l0_missing"] + token["l1_missing"]}
            product = token["product"][0] * p + token["product"][1]
            records.append({"coefficient": weight,
                            "exact_label": ["D", sorted((low - missing) | {6 * p, 10 * p}),
                                            token["kind"], product]})
    return records


def run(output, maximum=100, budget=60):
    if not isinstance(maximum, int) or not 8 <= maximum <= 100:
        raise ValueError("maximum must be an integer in the declared range 8..100")
    if not math.isfinite(budget) or budget <= 0:
        raise ValueError("budget must be finite and positive")
    started = time.monotonic()
    exp054 = load("exp054_for_056", EXPERIMENTS / "EXP-054-full-source-boundary/run.py")
    independent = load("audit054_for_056", EXPERIMENTS / "EXP-054-full-source-boundary/audit.py")
    algebra = load("exp036_for_056", EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy/run.py")
    candidate = load("candidate_for_056", EXPERIMENTS / "EXP-052-semantic-unreduced-lifts/candidate.py")
    for path, expected_hash in exp054.PREMISES.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash
    training = json.loads(exp054.SOURCE.read_text())
    for row in training["rows"]:
        p = row["p"]
        low = algebra.low_offsets(p)
        selected = [{"coefficient": term["coefficient"], "exact_label": term["exact_label"]}
                    for term in row["inclusions"][0]["source_support"]
                    if term["exact_label"][0] == "S"
                    and set(term["exact_label"][1]) - low == {6 * p, 10 * p}]
        source, _ = source_and_gamma(p)
        assert independent.sparse(selected) == {
            key: 2 * value for key, value in independent.sparse(source).items()}
    result = {"experiment": "EXP-056", "status": "CHECKPOINT", "training_recovery": [8, 9, 10],
              "p11_original_source_accessed": False, "parameters": [8, maximum], "rows": []}
    for p in range(8, maximum + 1):
        if time.monotonic() - started > budget:
            raise RuntimeError("EXP-056 budget exhausted; checkpoint retained")
        source, gamma = source_and_gamma(p)
        target = target_from_candidate(p, candidate)
        expected = independent.sparse(target + gamma)
        primary = dict(exp054.multiply(p, source, algebra))
        secondary = independent.independent_boundary(p, source)
        assert primary == secondary == expected
        assert len(source) == len(gamma) == p - 1
        mutation = [dict(term) for term in source]
        mutation[0]["coefficient"] *= -1
        assert independent.independent_boundary(p, mutation) != expected
        row = {"p": p, "source_support": len(source), "gamma_support": len(gamma),
               "d_support": len(target), "full_boundary_identity": True, "independent_agreement": True,
               "sign_mutation_rejected": True, "source_hash": exp054.digest(source),
               "boundary_hash": exp054.digest(exp054.records(primary))}
        result["rows"].append(row)
        exp054.write_json(output, result)
        if p <= 12 or p % 10 == 0:
            print(f"p={p}: uniform D+K formula PASS, source={len(source)}", flush=True)
        if time.monotonic() - started > budget:
            raise RuntimeError("EXP-056 budget exhausted; checkpoint retained")
    result["status"] = "COMPLETE"
    result["claims"] = {"uniform_differential_identity": "DERIVED_IN_PROOF",
                        "uniform_nontriviality_or_order_two": "NOT_ESTABLISHED"}
    result["artifact_hash"] = exp054.digest(result)
    exp054.write_json(output, result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--maximum", type=int, default=100)
    args = parser.parse_args()
    run(args.output, args.maximum)
