"""Uniform unit-filler regression and finite fixed-high source slice; exact CPU."""

from __future__ import annotations

import argparse
import json
import time
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent


def load(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def filler(p):
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    exterior = sorted(low - {2, 3 * p})
    return ({"coefficient": 1, "exact_label": ["K", sorted(exterior + [7 * p]), 6 * p]},
            ("K", tuple(exterior), 13 * p))


def shuffle_sign(selected, universe):
    rest = set(universe) - set(selected)
    inversions = sum(left > right for left in selected for right in rest)
    return (-1) ** inversions


def complement_certificate():
    checks = 0
    for size in range(1, 9):
        universe = tuple(range(size))
        for degree in range(1, size + 1):
            for selected in combinations(universe, degree):
                missing = sorted(set(universe) - set(selected))
                for position, value in enumerate(selected):
                    face = selected[:position] + selected[position + 1:]
                    left = (-1) ** position * shuffle_sign(face, universe)
                    insertion = sum(other < value for other in missing)
                    right = (-1) ** (degree - 1 + insertion) * shuffle_sign(selected, universe)
                    assert left == right
                    checks += 1
    return {"universe_sizes": [1, 8], "signed_insertion_checks": checks, "passed": True}


def run(output, budget=60):
    start = time.monotonic()
    exp054 = load("exp054_for_055", EXPERIMENTS / "EXP-054-full-source-boundary/run.py")
    algebra = load("exp036_for_055", EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy/run.py")
    for path, expected in exp054.PREMISES.items():
        import hashlib
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
    source = json.loads(exp054.SOURCE.read_text())
    target = json.loads(exp054.TARGET.read_text())
    result = {"experiment": "EXP-055", "status": "CHECKPOINT", "p11_source_accessed": False,
              "premises": {path.relative_to(EXPERIMENTS).as_posix(): value
                           for path, value in exp054.PREMISES.items()},
              "uniform_filler_regressions": [], "training": []}
    for p in range(4, 101):
        column, row = filler(p)
        boundary = exp054.multiply(p, [column], algebra)
        assert dict(boundary) == {row: -1}
        result["uniform_filler_regressions"].append({"p": p, "boundary": exp054.records(boundary)})
    print("p=4..100: single-column filler PASS", flush=True)
    exp054.write_json(output, result)
    for source_row, target_row in zip(source["rows"], target["rows"], strict=True):
        p = source_row["p"]
        support = source_row["inclusions"][0]["source_support"]
        correction, _ = filler(p)
        correction["coefficient"] = 2 * (-1) ** p
        corrected = support + [correction]
        boundary = exp054.multiply(p, corrected, algebra)
        expected = exp054.expected_boundary(target_row)
        assert boundary == expected
        low = algebra.low_offsets(p)
        selected = [term for term in support if term["exact_label"][0] == "S"
                    and set(term["exact_label"][1]) - low == {6 * p, 10 * p}]
        sliced_boundary = exp054.multiply(p, selected, algebra)
        d_boundary = {key: value for key, value in sliced_boundary.items() if key[0] == "D"}
        assert d_boundary == dict(expected)
        k_boundary = {key: value for key, value in sliced_boundary.items() if key[0] == "K"}
        missing_records = []
        for term in selected:
            kind, exterior, coefficient = term["exact_label"]
            missing = sorted(low - set(exterior))
            assert len(missing) == 3
            assert sum(missing) - coefficient == 6 * p + 2
            missing_records.append({"coefficient": term["coefficient"], "missing_low": missing,
                                    "source_coefficient": coefficient,
                                    "complement_sign": shuffle_sign(sorted(set(exterior) & low), sorted(low))})
        row = {"p": p, "corrected_full_identity": True,
               "source_support_before": len(support), "source_support_after": len(corrected),
               "even_correction": correction, "fixed_high_source_support": len(selected),
               "fixed_high_source": selected, "missing_set_source": missing_records,
               "d_identity": True, "k_boundary_support": len(k_boundary),
               "k_boundary": exp054.records(k_boundary)}
        row["row_hash"] = exp054.digest(row)
        result["training"].append(row)
        exp054.write_json(output, result)
        print(f"p={p}: corrected full identity PASS; fixed-high S support {len(selected)}; K rows {len(k_boundary)}", flush=True)
        if time.monotonic() - start > budget:
            raise RuntimeError("EXP-055 budget exhausted; checkpoint retained")
    result["complement_certificate"] = complement_certificate()
    result["status"] = "COMPLETE"
    result["p1_status"] = "UNIFORM_FILLER_PROVED_FINITE_SOURCES_REPAIRED"
    result["p2_status"] = "PASS_FINITE"
    result["artifact_hash"] = exp054.digest(result)
    exp054.write_json(output, result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/results.json")
    args = parser.parse_args()
    run(args.output)
