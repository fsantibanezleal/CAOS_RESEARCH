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
    / "EXP-008-parametric-block-family"
    / "run.py"
)
SPEC = importlib.util.spec_from_file_location("hw_exp008", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_declared_q5_overlap_is_present() -> None:
    _, a_set, b_set, _ = MODULE.residue_sets(5)
    assert a_set & b_set == {14}


def test_first_three_declared_parameters_pass() -> None:
    for q in (6, 7, 8):
        result = MODULE.analyze_q(q)
        assert result["accepted"], result["failures"]
        assert result["lower_generation_first_difference"] is None


def test_q9_exposes_the_predicted_rigidity_gap() -> None:
    result = MODULE.analyze_q(9)
    assert not result["accepted"]
    assert result["rigidity"]["first_missing_D"] == 9 * result["shift"] + 7
