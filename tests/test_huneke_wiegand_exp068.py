"""EXP-068: tensor factorization of extension ideals under gluing (hwcert.gluing)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "problems" / "commutative-algebra" / "huneke-wiegand" / "code"))

from hwcert.gluing import (  # noqa: E402
    TensorTorsion, Window, extension_generators, glue_generators, hilbert_identity_holds, ideal_from_generators,
    is_huneke_wiegand, minimal_generators, predicted_length, semigroup_mask, tensor_torsion,
)

PHAM = (56, 57, 58, 63, 64, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 87, 89, 90, 93, 95, 96, 97)


def test_window_shift_keeps_implicit_tail() -> None:
    w = Window(-5, 20)
    sg = semigroup_mask(w, (3, 5))
    assert w.tail_start(sg) == 8
    shifted = w.shift(sg, -4)
    assert w.contains(shifted, -4) and not w.contains(shifted, -3) and w.contains(shifted, 19)


def test_predicted_length_cross_term() -> None:
    t1 = TensorTorsion(length=3, jordan_at_least={1: 2, 2: 1})
    t2 = TensorTorsion(length=2, jordan_at_least={1: 1, 2: 1})
    assert predicted_length(2, 3, t1, t2) == 2 * 3 + 3 * 2 + (2 * 1 + 1 * 1)


def test_pham_counterexample_and_control() -> None:
    w = Window(-40, 900)
    sg = semigroup_mask(w, PHAM)
    assert w.tail_start(sg) - 1 == 181
    assert is_huneke_wiegand(w, sg, PHAM, (0, 14)) is False
    assert tensor_torsion(w, sg, PHAM, (0, 14)).length == 0
    assert is_huneke_wiegand(w, sg, PHAM, (0, 1)) is True


def test_small_gluing_length_law_and_mu() -> None:
    gens1, gens2, a1, a2 = (3, 5), (4, 5, 7), 5, 3
    w1, w2 = Window(-8, 400), Window(-8, 400)
    s1, s2 = semigroup_mask(w1, gens1), semigroup_mask(w2, gens2)
    i1, i2 = (0, 1), (0, 2)
    t1 = tensor_torsion(w1, s1, gens1, i1, y_degree=a2)
    t2 = tensor_torsion(w2, s2, gens2, i2, y_degree=a1)
    assert t1.length > 0 and t2.length > 0
    glued = glue_generators(a1, gens1, a2, gens2)
    ext = extension_generators(a1, i1, a2, i2)
    w = Window(-max(ext) - 4, 2000)
    sg = semigroup_mask(w, glued)
    ideal = ideal_from_generators(w, sg, ext)
    assert len(minimal_generators(w, ideal, glued)) == 4
    assert tensor_torsion(w, sg, glued, ext).length == predicted_length(a1, a2, t1, t2)
    assert hilbert_identity_holds(w, sg, a1, a2, ideal_from_generators(w1, s1, i1), w1,
                                  ideal_from_generators(w2, s2, i2), w2, ideal, upto=600)
