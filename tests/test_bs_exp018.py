"""Gate G3 of EXP-018 (boij-soderberg-realizability): the supports of S((e + t)/2; 0, (e - t)/2) for (e, t) = (11, 5) and (14, 10) against
hand-written lists; the tensor reduced modulo p against the original at e = 9; the plan of the cases; the import of the routine of EXP-010 on
the fixed member of G1 (pure, over GF(11))."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

EXP18 = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
         / "EXP-018-largest-exponent-strata")
EXP10 = EXP18.parent / "EXP-010-weight-class-strata"
sys.path.insert(0, str(EXP10))

import exp010_routine as X  # noqa: E402
from uhlib import algebra as A  # noqa: E402


def _load_run():
    spec = importlib.util.spec_from_file_location("exp018_run", EXP18 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _monos(e, idx):
    return sorted(A.monos(e)[k] for k in idx)


def test_supports_at_e11_t5_against_a_hand_written_list():
    # S(8; 0, 3): f on the weights 0 and 8, g on the weights 3 and 11
    run = _load_run()
    m, i, j = run.stratum_of(11, 5)
    assert (m, i, j) == (8, 0, 3)
    assert _monos(11, X.support(11, m, i)) == sorted([(11, 0, 0), (0, 5, 3), (1, 6, 2), (2, 7, 1), (3, 8, 0)])
    assert _monos(11, X.support(11, m, j)) == sorted([(0, 11, 0), (5, 0, 3), (6, 1, 2), (7, 2, 1), (8, 3, 0)])


def test_supports_at_e14_t10_against_a_hand_written_list():
    # S(12; 0, 2): f on the weights 0 and 12, g on the weights 2 and 14
    run = _load_run()
    m, i, j = run.stratum_of(14, 10)
    assert (m, i, j) == (12, 0, 2)
    assert _monos(14, X.support(14, m, i)) == sorted([(14, 0, 0), (0, 10, 2), (1, 11, 1), (2, 12, 0)])
    assert _monos(14, X.support(14, m, j)) == sorted([(0, 14, 0), (10, 0, 2), (11, 1, 1), (12, 2, 0)])


def test_the_plan_of_the_cases():
    run = _load_run()
    t = run.plan("T")
    assert [(s["e"], s["p"], s["m"], s["i"], s["j"], s["budget"]) for s in t] == [
        (11, 17, 9, 0, 2, 100000), (13, 19, 11, 0, 2, 100000), (14, 23, 12, 0, 2, 100000), (11, 13, 8, 0, 3, 1500000),
        (13, 17, 10, 0, 3, 1500000)]
    z = run.plan("Z")
    assert [(s["e"], s["p"], s["m"], s["i"], s["j"]) for s in z] == [(11, 13, 9, 0, 2), (11, 17, 10, 0, 1), (13, 17, 11, 0, 2),
                                                                    (13, 19, 12, 0, 1), (14, 23, 13, 0, 1)]
    assert all(s["budget"] == 50000 for s in z)
    k = run.plan("K")
    assert [(s["e"], s["p"], s["m"], s["i"], s["j"], s["budget"]) for s in k] == [(9, 11, 7, 0, 2, 20000), (9, 13, 6, 0, 3, 1000000)]
    # family Z has t + 2 of family T at the same pair
    assert [(a["e"], a["p"], run.t_of(a) + 2) for a in t if (a["e"], a["p"]) == (13, 17)] == [(13, 17, run.t_of(z[2]))]
    assert run.MAX_WORKERS == 12 and run.BUDGET_SECONDS == 7200


def test_the_tensor_reduced_modulo_p_equals_the_routine_at_e9_and_does_not_overflow_at_e13():
    run = _load_run()
    for e, p, n in ((6, 7, 18), (9, 11, 28), (9, 13, 28)):
        assert np.array_equal(run._struct_tensor_mod_p(p, e, n), run.struct_tensor_original(p, e, n))
    assert run.X.struct_tensor is not run.struct_tensor_original
    assert run._struct_tensor_mod_p(19, 13, 49).shape == (A.dim_U(13), A.dim_U(36), A.dim_U(49))


def test_the_routine_of_exp010_on_the_fixed_member_of_g1_over_gf11():
    run = _load_run()
    fm = run.fixed_member()
    assert fm["ok"] and fm["pure_hilbert"] and fm["in_stratum_S7_0_2"]
    assert [tuple(r) for r in fm["betti"]] == [tuple(r) for r in X.table_rows(X.pure_table(9))]
