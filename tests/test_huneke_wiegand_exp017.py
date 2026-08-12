from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXP = (
    ROOT
    / "problems"
    / "commutative-algebra"
    / "huneke-wiegand"
    / "experiments"
    / "EXP-017-conductor-reduction-number"
)


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, EXP / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_exp017_exact_profiles_at_boundary_and_high_parameter() -> None:
    run = load_module("hw_exp017_run", "run.py")
    for p in (4, 300):
        row = run.analyze_parameter(p)
        assert row["quotient_lengths"] == [23 * p - 1, 14 * p, 2 * p, 1, 0]
        assert row["reduction_number"] == 4
        assert row["e0"] == 24 * p
        assert row["e1"] == 39 * p


def test_exp017_independent_reconstruction() -> None:
    audit = load_module("hw_exp017_audit", "audit.py")
    for p in (4, 17):
        row = audit.reconstruct(p)
        assert row["quotient_lengths"] == [23 * p - 1, 14 * p, 2 * p, 1, 0]
        assert row["reduction_number"] == 4

