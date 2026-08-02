from __future__ import annotations

import sys
from pathlib import Path


CODE_ROOT = (
    Path(__file__).resolve().parents[1]
    / "problems"
    / "commutative-algebra"
    / "huneke-wiegand"
    / "code"
)
sys.path.insert(0, str(CODE_ROOT))

from hwcert import (  # noqa: E402
    analyze_rigidity,
    enumerate_symmetric_masks,
    gap_values,
    minimal_generators,
    validate_symmetric_mask,
)
from hwcert.semigroup import root_mask  # noqa: E402


def test_blanco_rosales_f11_tree() -> None:
    masks = enumerate_symmetric_masks(11)
    generators = {minimal_generators(mask, 11) for mask in masks}
    assert len(masks) == 6
    assert generators == {
        (2, 13),
        (3, 7),
        (4, 5),
        (4, 6, 9),
        (5, 7, 8, 9),
        (6, 7, 8, 9, 10),
    }


def test_f11_has_no_rigid_gap_case() -> None:
    for mask in enumerate_symmetric_masks(11):
        for shift in gap_values(mask, 11):
            result = analyze_rigidity(mask, 11, shift)
            assert result["rigid"] is False
            assert result["first_missing_D"] is not None
            assert result["first_reverse_failure"] is None


def test_declared_invalid_mutation_is_rejected() -> None:
    invalid = (root_mask(11) & ~(1 << 10)) | (1 << 1)
    failures = validate_symmetric_mask(invalid, 11)
    assert failures
    assert any("symmetry" in failure or "closure" in failure for failure in failures)
