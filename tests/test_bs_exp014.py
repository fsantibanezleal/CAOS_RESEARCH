"""Gate G3 of EXP-014 (boij-soderberg-realizability): the supports of the E-stratum and of the O-stratum against hand-written lists for
e = 6 and e = 7; N of the E-stratum at (8, 5); the enumeration of a small stratum (each normalized member once); the import of the
routine of EXP-010 on one known member (f = x^6 + y^6, g = x^3 y^3 + x^2 y^2 z + 3 z^3 over GF(7)); the plan of the cases."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

EXP14 = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
         / "EXP-014-middle-strata")
EXP10 = EXP14.parent / "EXP-010-weight-class-strata"
sys.path.insert(0, str(EXP10))

import exp010_routine as X  # noqa: E402
from uhlib import algebra as A  # noqa: E402


def _load_run():
    spec = importlib.util.spec_from_file_location("exp014_run", EXP14 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _monos(e, idx):
    return sorted(A.monos(e)[k] for k in idx)


def test_supports_of_the_e_stratum_at_e6_against_a_hand_written_list():
    # S(6; 0, 3): f on the weights 0 and 6, g on the weight 3 (x^(3-c) y^(3-c) z^c)
    run = _load_run()
    m, i, j = run.e_stratum(6)
    assert (m, i, j) == (6, 0, 3)
    assert _monos(6, X.support(6, m, i)) == sorted([(6, 0, 0), (0, 6, 0)])
    assert _monos(6, X.support(6, m, j)) == sorted([(3, 3, 0), (2, 2, 1), (1, 1, 2), (0, 0, 3)])


def test_supports_of_the_o_stratum_at_e7_against_a_hand_written_list():
    # S(4; 0, 3): f on the weights 0 and 4, g on the weights 3 and 7
    run = _load_run()
    m, i, j = run.o_stratum(7)
    assert (m, i, j) == (4, 0, 3)
    assert _monos(7, X.support(7, m, i)) == sorted([(7, 0, 0), (3, 4, 0), (2, 3, 1), (1, 2, 2), (0, 1, 3)])
    assert _monos(7, X.support(7, m, j)) == sorted([(4, 3, 0), (3, 2, 1), (2, 1, 2), (1, 0, 3), (0, 7, 0)])
    assert run.l_stratum(9) == (8, 0, 1)


def test_the_number_of_members_of_the_e_stratum_at_8_5():
    run = _load_run()
    m, i, j = run.e_stratum(8)
    assert X.n_members(8, 5, m, i, j) == 4686 == (5 + 1) * (5 ** 5 - 1) // (5 - 1)
    for e, p in ((4, 3), (6, 5), (10, 7), (12, 5)):
        m, i, j = run.e_stratum(e)
        assert X.n_members(e, p, m, i, j) == (p + 1) * (p ** (e // 2 + 1) - 1) // (p - 1)
    assert X.n_members(9, 17, *run.l_stratum(9)) == 94249


def test_enumeration_of_a_small_stratum_each_normalized_member_once():
    run = _load_run()
    e, p = 4, 3
    m, i, j = run.e_stratum(e)
    N = X.n_members(e, p, m, i, j)
    FS, GS = X.enumerate_members(e, p, m, i, j, 0, N)
    seen = {(tuple(f), tuple(g)) for f, g in zip(FS.tolist(), GS.tolist())}
    assert len(seen) == N
    for f, g in seen:
        assert next(c for c in f if c) == 1 and next(c for c in g if c) == 1


def test_the_plan_of_the_cases():
    run = _load_run()
    k = run.plan("K")
    assert [(s["e"], s["p"], s["m"], s["j"]) for s in k] == [(4, 3, 4, 2), (4, 5, 4, 2), (6, 5, 6, 3), (6, 7, 6, 3), (6, 11, 6, 3),
                                                              (6, 3, 6, 3), (5, 7, 3, 2), (7, 5, 4, 3), (7, 11, 4, 3)]
    # amendment-1.md: the control (7, 11) runs with budget 300000; every other control keeps 30000
    assert all(s["budget"] == (300000 if (s["e"], s["p"]) == (7, 11) else 30000) and s["admissible"] for s in k)
    v = run.plan("V")
    assert [(s["e"], s["p"]) for s in v] == [(8, 3), (8, 5), (8, 7), (8, 11), (8, 13), (10, 3), (10, 7), (10, 11), (10, 13), (10, 5),
                                              (12, 5), (12, 7)]
    assert [s["budget"] for s in v if s["e"] == 8] == [500000] * 5
    assert all(s["all_members"] for s in v if s["e"] == 8)
    w = run.plan("W")
    assert [(s["p"], (s["m"], s["i"], s["j"])) for s in w] == [(7, (5, 0, 4)), (11, (5, 0, 4)), (13, (5, 0, 4)), (5, (5, 0, 4)),
                                                              (11, (8, 0, 1)), (13, (8, 0, 1)), (17, (8, 0, 1))]


def test_the_routine_of_exp010_on_one_known_member():
    p, e = 7, 6
    f = np.zeros(A.dim_U(e), dtype=np.int64)
    g = np.zeros(A.dim_U(e), dtype=np.int64)
    pos = {mono: k for k, mono in enumerate(A.monos(e))}
    f[pos[(6, 0, 0)]] = f[pos[(0, 6, 0)]] = 1
    g[pos[(3, 3, 0)]] = 1
    g[pos[(2, 2, 1)]] = 1
    g[pos[(0, 0, 3)]] = 3
    assert X.pure_hilbert_full(e, p, f, g)
    assert X.betti_table(e, p, f, g) == X.pure_table(e)
    run = _load_run()
    m, i, j = run.e_stratum(e)
    assert run.in_stratum(e, m, i, j, f, g)
