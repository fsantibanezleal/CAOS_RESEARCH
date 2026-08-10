from __future__ import annotations

import sys
from pathlib import Path


CODE_ROOT = (
    Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "huneke-wiegand" / "code"
)
sys.path.insert(0, str(CODE_ROOT))

from hwcert import (  # noqa: E402
    add_exact_cardinality,
    build_rigidity_cnf,
    build_selector_rigidity_cnf,
    projected_blocking_clause,
    shift_from_model,
)
from hwcert.cnf import CNF  # noqa: E402


def satisfiable_with_units(clauses: tuple[tuple[int, ...], ...], units: tuple[int, ...]) -> bool:
    pending = clauses + tuple((literal,) for literal in units)

    def search(current: tuple[tuple[int, ...], ...]) -> bool:
        while True:
            if any(not clause for clause in current):
                return False
            unit = next((clause[0] for clause in current if len(clause) == 1), None)
            if unit is None:
                break
            reduced: list[tuple[int, ...]] = []
            for clause in current:
                if unit in clause:
                    continue
                reduced.append(tuple(value for value in clause if value != -unit))
            current = tuple(reduced)
        if not current:
            return True
        branch = current[0][0]
        return search(current + ((branch,),)) or search(current + ((-branch,),))

    return search(pending)


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


def test_exact_cardinality_accepts_exactly_the_requested_assignments() -> None:
    for size in range(1, 5):
        for count in range(size + 1):
            cnf = CNF()
            variables = tuple(cnf.variable(f"x:{index}") for index in range(size))
            add_exact_cardinality(cnf, variables, count, "test")
            clauses = tuple(cnf.clauses)
            for assignment in range(1 << size):
                units = tuple(
                    variable if assignment & (1 << index) else -variable
                    for index, variable in enumerate(variables)
                )
                assert satisfiable_with_units(clauses, units) is (assignment.bit_count() == count)


def test_exact_cardinality_rejects_invalid_requests() -> None:
    cnf = CNF()
    variable = cnf.variable("x")
    for literals in ((variable, variable), (0, variable)):
        try:
            add_exact_cardinality(cnf, literals, 1, "invalid")
        except ValueError:
            pass
        else:
            raise AssertionError("invalid cardinality literals were accepted")


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


def test_projected_blocker_excludes_exactly_one_assignment() -> None:
    variables = (2, 5, 9)
    model = {2, 9, 1000}
    blocker = projected_blocking_clause(variables, model)
    assert blocker == (-2, 5, -9)

    def satisfied(true_variables: set[int]) -> bool:
        return any(
            literal > 0 and literal in true_variables or literal < 0 and -literal not in true_variables
            for literal in blocker
        )

    assert not satisfied({2, 9})
    assert not satisfied({2, 9, 1001})  # auxiliary assignments are irrelevant
    for changed in ({9}, {2, 5, 9}, {2}):
        assert satisfied(changed)


def test_projected_blocker_rejects_invalid_projection() -> None:
    for variables in ((), (1, 1), (0, 1), (-1, 2)):
        try:
            projected_blocking_clause(variables, set())
        except ValueError:
            pass
        else:
            raise AssertionError("invalid projected variable list was accepted")
