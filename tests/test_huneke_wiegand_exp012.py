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
    / "EXP-012-endomorphism-type"
    / "run.py"
)
SPEC = importlib.util.spec_from_file_location("hw_exp012", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_first_type_family_member() -> None:
    row = MODULE.analyze_parameter(4)
    assert row["type"] == 40
    assert row["reduced_type"] == 40
    assert row["maximal_reduced_type"] is True
    assert row["almost_symmetric"] is False
    assert row["first_pf"] == 144
    assert row["last_pf"] == 215


def test_independent_parametric_checkpoint() -> None:
    p = 17
    row = MODULE.analyze_parameter(p)
    assert row["type"] == 10 * p
    assert row["reduced_type"] == 10 * p
    assert row["first_pf"] == 36 * p
    assert row["last_pf"] == 54 * p - 1


def test_large_parameter_preserves_controls() -> None:
    row = MODULE.analyze_parameter(300)
    assert row["controls"] == {
        "deleted_pf_rejected": True,
        "injected_lower_gap_rejected": True,
    }


def test_predicted_pf_cardinality() -> None:
    for p in (4, 5, 31):
        assert len(MODULE.predicted_pf(p)) == 10 * p
