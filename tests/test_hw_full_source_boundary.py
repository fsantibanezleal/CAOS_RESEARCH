"""Permanent exact full-versus-projected source-boundary regression."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXP = (ROOT / "problems/commutative-algebra/huneke-wiegand/experiments"
       / "EXP-054-full-source-boundary")


def load(filename: str):
    spec = importlib.util.spec_from_file_location(f"hw_exp054_{filename.replace('.', '_')}", EXP / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT = load("audit.py")


def test_independent_audit_matches_persisted_certificate() -> None:
    certificate = json.loads((EXP / "artifacts/audit-certificate.json").read_text(encoding="utf-8"))
    assert AUDIT.audit() == certificate
    assert certificate["p3_status"] == "PASS_FINITE"
    assert [row["component_rows_checked"] for row in certificate["rows"]] == [2675, 4757, 7973]
    assert all(row["sign_mutation_detected"] for row in certificate["rows"])


def test_full_residual_is_even_single_kernel_row() -> None:
    source = json.loads(AUDIT.SOURCE.read_text(encoding="utf-8"))
    result = json.loads(AUDIT.RESULTS.read_text(encoding="utf-8"))
    for source_row, saved in zip(source["rows"], result["rows"], strict=True):
        p = source_row["p"]
        boundary = AUDIT.independent_boundary(p, source_row["inclusions"][0]["source_support"])
        assert boundary == AUDIT.sparse(saved["boundary"])
        assert all(coefficient % 2 == 0 for coefficient in boundary.values())
        assert saved["full_identity"] is False
        assert saved["residual"][0]["coefficient"] == 2 * (-1) ** p
        assert saved["residual"][0]["exact_label"][0] == "K"
        assert saved["residual"][0]["exact_label"][-1] == 13 * p


def test_independent_differential_rejects_invalid_grading() -> None:
    source = json.loads(AUDIT.SOURCE.read_text(encoding="utf-8"))
    row = source["rows"][0]
    support = deepcopy(row["inclusions"][0]["source_support"])
    support[0]["exact_label"][2] += 1
    with pytest.raises(AssertionError):
        AUDIT.independent_boundary(row["p"], support)


def test_direct_gap_intervals_partition_high_degree_range() -> None:
    for p in (4, 8, 9, 10, 20):
        for value in range(6 * p, 24 * p):
            assert AUDIT.degree_two_contains(p, value) != AUDIT.high_contains(p, value)
        assert not AUDIT.degree_two_contains(p, 6 * p - 1)
        assert not AUDIT.degree_two_contains(p, 24 * p)


def test_cli_reruns_are_deterministic_and_preserve_canonical_artifacts(tmp_path: Path) -> None:
    paths = [EXP / "artifacts/results.json", EXP / "artifacts/audit-certificate.json"]
    before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    for script, canonical in (("run.py", paths[0]), ("audit.py", paths[1])):
        output = tmp_path / script.replace(".py", ".json")
        subprocess.run([sys.executable, str(EXP / script), "--output", str(output)],
                       cwd=ROOT, check=True, capture_output=True, text=True, timeout=60)
        assert output.read_bytes() == canonical.read_bytes()
    assert before == {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
