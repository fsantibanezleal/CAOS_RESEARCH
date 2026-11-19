"""Tests of the Kostant modules, presentations and duals of the U(H) library (run from the repository root)."""
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CODE))

import pytest  # noqa: E402

from uhlib import tor  # noqa: E402
from uhlib.fields import QQ, make_field  # noqa: E402
from uhlib.kostant import expected_table, kostant_module, weyl_dimension  # noqa: E402
from uhlib.module import dual, presentation, quotient_module, truncate  # noqa: E402

F = QQ()


def test_L11_hilbert_function_and_table():
    m = kostant_module(F, 1, 1)
    assert m.hilbert_list() == [2, 1, 2]
    assert m.check_relations()
    assert tor.betti(m) == {(0, 0): 2, (1, 1): 3, (2, 5): 3, (3, 6): 2}


def test_L20_hilbert_function_and_table():
    m = kostant_module(F, 2, 0)
    assert m.hilbert_list() == [1, 2, 4, 2, 1]
    assert tor.betti(m) == {(0, 0): 1, (1, 3): 4, (2, 5): 4, (3, 8): 1}


@pytest.mark.parametrize("p,q", [(p, q) for p in range(0, 4) for q in range(0, p + 1)])
def test_kostant_tables_match_table_F(p, q):
    m = kostant_module(F, p, q)
    assert m.total_dim() == weyl_dimension(p, q)
    assert m.check_relations()
    assert tor.betti(m) == expected_table(p, q)


def test_presentation_roundtrip_and_two_generators():
    m = kostant_module(F, 1, 1)
    shifts, rels = presentation(m)
    assert shifts == [0, 0]
    back = quotient_module(F, shifts, rels, maxdeg=12)
    assert back.dims == m.dims
    assert tor.betti(back) == tor.betti(m)


def test_dual_reverses_table_of_a_non_self_dual_module():
    # cokernel of a 3 x 5 matrix of linear forms, truncated: not self-dual
    m = truncate(quotient_module(F, [0, 0, 0], [
        {(0, (1, 0, 0)): 1, (1, (0, 1, 0)): 1}, {(1, (1, 0, 0)): 1, (2, (0, 1, 0)): 1},
        {(2, (1, 0, 0)): 1}, {(0, (0, 1, 0)): 1, (2, (0, 1, 0)): 2}, {(1, (0, 1, 0)): 1, (0, (1, 0, 0)): 3},
    ], maxdeg=14), 14)
    dm = dual(m)
    assert dm.check_relations()
    b, bd = tor.betti(m), tor.betti(dm)
    assert bd == {(3 - i, 4 - j): r for (i, j), r in b.items()}


def test_modules_over_prime_and_extension_fields():
    for char, deg in ((32003, 1), (2, 2), (3, 1)):
        f = make_field(char, deg)
        m = kostant_module(f, 1, 1) if char != 2 else kostant_module(f, 1, 0)
        assert m.check_relations()
