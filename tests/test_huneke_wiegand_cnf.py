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
    build_rigidity_cnf,
    build_selector_rigidity_cnf,
    shift_from_model,
)


def test_cnf_has_no_tautologies_or_duplicate_literals() -> None:
    cnf, h = build_rigidity_cnf(11, 1)
    assert len(h) == 12
    assert cnf.names["h:0"] == h[0]
    for clause in cnf.clauses:
        assert len(clause) == len(set(clause))
        assert all(-literal not in clause for literal in clause)


def test_cnf_is_deterministic() -> None:
    left, left_h = build_rigidity_cnf(11, 3)
    right, right_h = build_rigidity_cnf(11, 3)
    assert left_h == right_h
    assert left.names == right.names
    assert left.clauses == right.clauses


def test_cnf_expected_scale() -> None:
    cnf, _ = build_rigidity_cnf(11, 1)
    assert len(cnf.names) > 100
    assert len(cnf.clauses) > len(cnf.names)


def test_selector_cnf_is_deterministic_and_well_formed() -> None:
    left, left_h, left_q = build_selector_rigidity_cnf(11)
    right, right_h, right_q = build_selector_rigidity_cnf(11)
    assert left_h == right_h
    assert left_q == right_q
    assert left.names == right.names
    assert left.clauses == right.clauses
    assert len(left_h) == 12
    assert len(left_q) == 11
    for clause in left.clauses:
        assert len(clause) == len(set(clause))
        assert all(-literal not in clause for literal in clause)


def test_selector_cnf_has_exactly_one_shift_constraints() -> None:
    cnf, h, q = build_selector_rigidity_cnf(5)
    assert tuple(q) in cnf.clauses
    for left in range(len(q)):
        assert (-q[left], -h[left + 1]) in cnf.clauses
        for right in range(left + 1, len(q)):
            assert (-q[left], -q[right]) in cnf.clauses


def test_shift_model_decoder_rejects_non_one_hot_models() -> None:
    _, _, q = build_selector_rigidity_cnf(5)
    assert shift_from_model(q, {q[2]}) == 3
    for invalid in (set(), {q[0], q[1]}):
        try:
            shift_from_model(q, invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid selector assignment was accepted")
