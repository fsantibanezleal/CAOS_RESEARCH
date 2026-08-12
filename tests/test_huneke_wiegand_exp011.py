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
    / "EXP-011-endomorphism-family"
    / "run.py"
)
SPEC = importlib.util.spec_from_file_location("hw_exp011", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_first_endomorphism_family_member() -> None:
    row = MODULE.analyze_parameter(4)
    assert row["invariants"] == {
        "multiplicity": 96,
        "frobenius": 215,
        "conductor": 216,
        "genus": 151,
        "symmetric": False,
        "first_symmetry_failure": 1,
    }
    assert row["embedding_dimension"] == 48
    assert row["extra_count"] == 5


def test_parametric_invariants_at_independent_checkpoint() -> None:
    p = 17
    row = MODULE.analyze_parameter(p)
    assert row["invariants"]["frobenius"] == 54 * p - 1
    assert row["invariants"]["genus"] == 38 * p - 1
    assert row["embedding_dimension"] == 12 * p
    assert row["extra_count"] == p + 1


def test_large_parameter_preserves_both_controls() -> None:
    row = MODULE.analyze_parameter(300)
    assert row["controls"] == {
        "missing_q_rejected": True,
        "terminal_shift_rejected": True,
    }


def test_declared_q_block_has_cardinality_p() -> None:
    for p in (4, 5, 31):
        _, _, _, _, q = MODULE.family_sets(p)
        assert len(q) == p
