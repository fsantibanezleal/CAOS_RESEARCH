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


def test_route_k_formula_has_binding_block_units() -> None:
    shift = 4
    cnf, membership = MODULE.build_route_k_cnf(shift)
    for value in range(1, 4 * shift):
        assert (-membership[value],) in cnf.clauses
    assert (membership[4 * shift],) in cnf.clauses
    for value in range(5 * shift, 6 * shift):
        assert (membership[value],) in cnf.clauses


def test_route_k_requires_even_shift() -> None:
    for invalid in (0, 1, 3, 15):
        try:
            MODULE.build_route_k_cnf(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid Route K shift was accepted")


def test_seed_passes_every_route_k_invariant() -> None:
    frobenius = 181
    mask = MODULE.generated_mask(MODULE.SEED_GENERATORS, frobenius)
    result = MODULE.validate_route_k_mask(mask, 14)
    assert result["accepted"], result["failures"]
    assert result["level4_residues"] == (0, 1, 2, 7, 8)
    assert result["level6_residues"] == (3, 5, 6, 9, 11, 12, 13)
    assert result["level6_count"] == 7
    assert result["level4_level6_overlap"] == ()
    assert result["generalized_arithmetic_presentation"] is None


def test_corrupted_forced_block_is_rejected() -> None:
    mask = MODULE.generated_mask(MODULE.SEED_GENERATORS, 181)
    corrupted = mask & ~(1 << 70)
    result = MODULE.validate_route_k_mask(corrupted, 14)
    assert not result["accepted"]
    assert any("level-5 block misses 70" in failure for failure in result["failures"])
