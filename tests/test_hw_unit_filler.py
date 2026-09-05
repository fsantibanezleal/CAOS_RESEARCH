"""Exact unit-filler and low-complement regression; canonical artifacts stay untouched."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXP = (ROOT / "problems/commutative-algebra/huneke-wiegand/experiments"
       / "EXP-055-unit-filler-and-low-complement")
SPEC = importlib.util.spec_from_file_location("hw_exp055_audit", EXP / "audit.py")
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def test_independent_audit_matches_persisted_certificate() -> None:
    saved = json.loads((EXP / "artifacts/audit-certificate.json").read_text(encoding="utf-8"))
    assert saved == AUDIT.audit()
    assert saved["filler_count"] == 97
    assert [row["fixed_high_source_support"] for row in saved["training"]] == [7, 8, 9]
    assert all(row["correction_sign_mutation_detected"] for row in saved["training"])


def test_filler_boundary_and_source_grading() -> None:
    arithmetic = AUDIT.load_previous()
    for p in (4, 8, 9, 10, 100):
        column, row = AUDIT.independent_filler(p)
        assert len(column["exact_label"][1]) == 2 * p - 2
        assert sum(column["exact_label"][1]) + 6 * p == 4 * p * p + 6 * p - 1
        assert arithmetic.independent_boundary(p, [column]) == {row: -1}


def test_complement_orientation_and_sign_controls() -> None:
    certificate = AUDIT.verify_complements()
    assert certificate["signed_insertion_checks"] == 1793
    assert certificate["reversed_sign_mutations_rejected"] == 1793
    assert AUDIT.complement_sign([1, 3], [1, 2, 3, 4]) == -1


def test_cli_reruns_are_byte_identical_without_canonical_writes(tmp_path: Path) -> None:
    paths = [EXP / "artifacts/results.json", EXP / "artifacts/audit-certificate.json"]
    before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    for script, canonical in (("run.py", paths[0]), ("audit.py", paths[1])):
        output = tmp_path / script.replace(".py", ".json")
        subprocess.run([sys.executable, str(EXP / script), "--output", str(output)],
                       cwd=ROOT, check=True, capture_output=True, text=True, timeout=60)
        assert output.read_bytes() == canonical.read_bytes()
    assert before == {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
