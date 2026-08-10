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
    / "EXP-006-block-family"
    / "run_route_k.py"
)
SPEC = importlib.util.spec_from_file_location("hw_route_k", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

SEED_GENERATORS = (
    56, 57, 58, 63, 64, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
    82, 83, 87, 89, 90, 93, 95, 96, 97,
)


def seed_mask() -> int:
    present = bytearray(182)
    present[0] = 1
    for value in range(1, 182):
        present[value] = any(
            value >= generator and present[value - generator]
            for generator in SEED_GENERATORS
        )
    return sum(1 << value for value, flag in enumerate(present) if flag)


def test_route_k_formula_has_binding_block_units() -> None:
    shift = 14
    cnf, membership = MODULE.build_route_k_cnf(shift)
    for value in range(1, 4 * shift):
        assert (-membership[value],) in cnf.clauses
    assert (membership[4 * shift],) in cnf.clauses
    for value in range(5 * shift, 6 * shift):
        assert (membership[value],) in cnf.clauses


def test_route_k_requires_even_shift() -> None:
    for invalid in (0, 1, 12, 15):
        try:
            MODULE.build_route_k_cnf(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid Route K shift was accepted")


def test_seed_passes_every_route_k_invariant() -> None:
    result = MODULE.semantic_record(seed_mask(), 14)
    assert result["level4_offsets"] == [0, 1, 2, 7, 8]
    assert result["level6_offsets"] == [3, 5, 6, 9, 11, 12, 13]
    assert result["level6_count"] == 7
    assert result["invariant_checks"]["level4_level6_disjoint"] is True
    assert result["generalized_arithmetic_presentation"] is None


def test_corrupted_forced_block_is_rejected() -> None:
    corrupted = seed_mask() & ~(1 << 70)
    failures = MODULE.route_k_failures(corrupted, 14)
    assert any("full level-5 block fails at 70" in failure for failure in failures)
