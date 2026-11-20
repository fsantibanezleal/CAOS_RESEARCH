"""Gate G3 of EXP-015 (boij-soderberg-realizability): the supports of S(e - 1; 0, 1) at e = 10 against a hand-written list; N of
S(11; 0, 1) at (12, 23); the strata of family R against the admissible list of the note for e = 9; the plan of the cases; the import of
the routine of EXP-010 on the known member f = x^9 + x y^8, g = y^9 + x^7 z over GF(17)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

EXP15 = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
         / "EXP-015-linear-rule-and-e9")
EXP10 = EXP15.parent / "EXP-010-weight-class-strata"
sys.path.insert(0, str(EXP10))

import exp010_routine as X  # noqa: E402
from uhlib import algebra as A  # noqa: E402


def _load_run():
    spec = importlib.util.spec_from_file_location("exp015_run", EXP15 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _monos(e, idx):
    return sorted(A.monos(e)[k] for k in idx)


def test_supports_of_the_linear_stratum_at_e10_against_a_hand_written_list():
    # x^a y^b z^c with a + b + 2c = 10 and weight b + c: class 0 mod 9 has weights 0 and 9, class 1 has weights 1 and 10
    run = _load_run()
    m, i, j = run.l_stratum(10)
    assert (m, i, j) == (9, 0, 1)
    assert _monos(10, X.support(10, m, i)) == sorted([(10, 0, 0), (1, 9, 0), (0, 8, 1)])
    assert _monos(10, X.support(10, m, j)) == sorted([(9, 1, 0), (8, 0, 1), (0, 10, 0)])


def test_the_number_of_members_of_the_linear_stratum_at_12_23():
    run = _load_run()
    assert X.n_members(12, 23, *run.l_stratum(12)) == 553 ** 2 == 305809
    assert run.l_stratum(13) == (12, 0, 1)


def test_the_strata_of_family_r_against_the_admissible_list_of_the_note_at_e9():
    run = _load_run()
    note = [(2, 0, 1), (3, 0, 0), (3, 0, 1), (3, 0, 2), (3, 1, 1), (3, 1, 2), (3, 2, 2), (4, 0, 1), (5, 0, 4), (6, 0, 3), (6, 1, 4),
            (6, 2, 5), (7, 0, 2), (8, 0, 1)]
    listed = {(2, 0, 1), (3, 0, 0), (3, 0, 1), (3, 0, 2), (3, 1, 1), (3, 1, 2), (3, 2, 2), (4, 0, 1), (6, 0, 3), (6, 1, 4), (6, 2, 5),
              (7, 0, 2)}
    for s in note:
        assert X.admissible(9, *s), s
    plan = run.plan("R", {(9, 11)})
    assert [(s["m"], s["i"], s["j"]) for s in plan] == [(7, 0, 2), (6, 0, 3), (6, 1, 4), (6, 2, 5), (4, 0, 1), (3, 0, 0), (3, 0, 1),
                                                       (3, 0, 2), (3, 1, 1), (3, 1, 2), (3, 2, 2), (2, 0, 1)]
    assert set((s["m"], s["i"], s["j"]) for s in plan) == listed
    # family R plus the two strata already examined at e = 9 is exactly the note's list
    assert listed | {(5, 0, 4), (8, 0, 1)} == set(note)
    assert [s["budget"] for s in plan] == [500000, 200000, 200000, 200000, 200000] + [100000] * 6 + [300000]


def test_the_plan_of_the_cases():
    run = _load_run()
    k = run.plan("K")
    assert [(s["e"], s["p"], s["m"], s["i"], s["j"]) for s in k] == [(9, 17, 8, 0, 1), (9, 13, 8, 0, 1), (8, 13, 7, 0, 1), (8, 11, 7, 0, 1)]
    assert all(s["budget"] == 100000 and s["all_members"] for s in k)
    lf = run.plan("L")
    assert [(s["e"], s["p"]) for s in lf] == [(10, 17), (10, 19), (10, 13), (10, 11), (11, 19), (11, 17), (11, 13), (12, 23), (12, 19),
                                              (12, 17), (13, 23), (13, 19)]
    assert all((s["m"], s["i"], s["j"]) == (s["e"] - 1, 0, 1) and s["budget"] == 100000 for s in lf)
    r = run.plan("R")
    assert [(s["e"], s["p"]) for s in r][:12] == [(9, 5)] * 12 and len(r) == 36
    assert [s["p"] for s in r][12::12] == [11, 13]
    assert (5, 0, 4) not in [(s["m"], s["i"], s["j"]) for s in r]


def test_the_routine_of_exp010_on_the_known_member_over_gf17():
    p, e = 17, 9
    f = np.zeros(A.dim_U(e), dtype=np.int64)
    g = np.zeros(A.dim_U(e), dtype=np.int64)
    pos = {mono: k for k, mono in enumerate(A.monos(e))}
    f[pos[(9, 0, 0)]] = f[pos[(1, 8, 0)]] = 1
    g[pos[(0, 9, 0)]] = g[pos[(7, 0, 1)]] = 1
    assert X.pure_hilbert_full(e, p, f, g)
    assert X.betti_table(e, p, f, g) == X.pure_table(e)
    run = _load_run()
    m, i, j = run.l_stratum(9)
    assert run.in_stratum(e, m, i, j, f, g) and (m, i, j) == (8, 0, 1)


def test_the_tensor_reduced_modulo_p_equals_the_routine_where_it_fits_and_does_not_overflow_at_e13():
    run = _load_run()
    for e, p, n in ((6, 7, 18), (9, 17, 28), (12, 23, 36)):
        assert np.array_equal(run._struct_tensor_mod_p(p, e, n), run.struct_tensor_original(p, e, n))
    assert run.X.struct_tensor is not run.struct_tensor_original
    assert run._struct_tensor_mod_p(23, 13, 49).shape == (A.dim_U(13), A.dim_U(36), A.dim_U(49))
