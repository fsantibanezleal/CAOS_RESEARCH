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
    / "EXP-013-trace-conductor"
    / "run.py"
)
SPEC = importlib.util.spec_from_file_location("hw_exp013", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_first_family_member() -> None:
    row = MODULE.analyze_parameter(4)
    assert row["colength"] == 5
    assert row["first_trace_value"] == 96
    assert row["full_intermediate_start"] == 216
    assert row["tail_start"] == 312


def test_parametric_checkpoint() -> None:
    row = MODULE.analyze_parameter(17)
    assert row["colength"] == 18
    assert row["first_trace_value"] == 408
    assert row["full_intermediate_start"] == 918
    assert row["tail_start"] == 1326


def test_reflected_obstruction() -> None:
    for p in (4, 5, 31):
        s, _, _, _, q, h = MODULE.family_sets(p)
        assert h == {s - 1 - residue for residue in q}
        assert len(h) == p


def test_large_parameter_controls() -> None:
    row = MODULE.analyze_parameter(300)
    assert all(row["controls"].values())
