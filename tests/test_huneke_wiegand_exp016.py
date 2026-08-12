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
    / "EXP-016-corrected-stability-defect"
    / "run.py"
)
SPEC = importlib.util.spec_from_file_location("hw_exp016", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_corrected_endpoints() -> None:
    for p in (4, 5, 31):
        row = MODULE.analyze_parameter(p)
        assert row["frobenius_gap_retained"] == 78 * p - 1
        assert row["terminal_endpoint_filled"] == 102 * p - 1


def test_exact_defect_formula_checkpoint() -> None:
    p = 17
    row = MODULE.analyze_parameter(p)
    assert row["defect_length"] == 14 * p
    assert row["level_counts"] == {
        "8": 2 * p,
        "9": p,
        "10": 3 * p,
        "11": 6 * p,
        "12": 2 * p - 1,
        "16": 1,
    }
    assert all(row["identity_checks"].values())


def test_large_parameter_controls() -> None:
    row = MODULE.analyze_parameter(300)
    assert row["defect_length"] == 4200
    assert all(row["controls"].values())
