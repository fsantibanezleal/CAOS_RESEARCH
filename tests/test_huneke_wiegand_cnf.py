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

from hwcert import build_rigidity_cnf  # noqa: E402


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
