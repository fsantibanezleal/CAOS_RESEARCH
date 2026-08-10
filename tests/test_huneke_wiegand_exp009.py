from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "problems"
    / "commutative-algebra"
    / "huneke-wiegand"
    / "experiments"
    / "EXP-009-growing-interval-family"
    / "run.py"
)
SPEC = importlib.util.spec_from_file_location("hw_exp009", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_boundary_parameters_fail_rigidity() -> None:
    for p in (2, 3):
        result = MODULE.analyze_p(p)
        assert not result["accepted"]
        assert result["rigidity"]["first_missing_D"] is not None


def test_first_parameters_reproduce_route_k_models() -> None:
    for p in (4, 5):
        result = MODULE.analyze_p(p)
        assert result["accepted"], result["failures"]
        assert result["membership_sha256"] == MODULE.ROUTE_K_HASHES[p]
        assert result["embedding_dimension"] == 11 * p


def test_large_parameter_passes_exact_checks() -> None:
    result = MODULE.analyze_p(40)
    assert result["accepted"], result["failures"]
    assert result["sumsets"]["passed"] is True
    assert result["generation_first_difference"] is None


def test_both_declared_corruptions_are_rejected() -> None:
    record = MODULE.corruption_record(4)
    assert record["endpoint_symmetry_failure"] is not None
    assert record["selector_symmetry_failure"] is not None
