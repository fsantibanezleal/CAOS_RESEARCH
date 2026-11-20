"""Gate G3 of EXP-012 (boij-soderberg-realizability): the basis of V_e against a hand-written list for (4, 3) and (6, 3); the
passage from (A, beta_1, beta_2) to the PBW polynomial on B1 and D1; n(f) and D on B1; the identity g f - f g = - D z on C1; the
criterion routine on the two ideals of G1; and the complex, the Hilbert function and the random draw of the routine."""
import sys
from pathlib import Path

EXPS = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
        / "experiments")
sys.path.insert(0, str(EXPS / "EXP-012-central-commutator-criterion"))

import exp012_routine as R  # noqa: E402


def test_basis_of_v_e_for_4_3_and_6_3_against_hand_written_lists():
    # (4, 3): Z_4 = <z^2>, Z_3 = <X, Y>; so V_4 = <z^2, X x, Y x, X y, Y y>
    assert R.class_basis(4, 3) == [("A", (0, 0, 2)), ("x", (0, 1, 0)), ("x", (1, 0, 0)), ("y", (0, 1, 0)), ("y", (1, 0, 0))]
    # (6, 3): Z_6 = <z^3, Y^2, X Y, X^2>, Z_5 = <Y z, X z>
    assert R.class_basis(6, 3) == [("A", (0, 0, 3)), ("A", (0, 2, 0)), ("A", (1, 1, 0)), ("A", (2, 0, 0)),
                                   ("x", (0, 1, 1)), ("x", (1, 0, 1)), ("y", (0, 1, 1)), ("y", (1, 0, 1))]


def test_passage_from_data_to_the_pbw_polynomial_on_b1_and_d1():
    # B1 (4, 3): f = x^4 + z^2 = z^2 + X x, g = y^4 + z^2 = z^2 + Y y
    assert R.data_to_pbw({(0, 0, 2): 1}, {(1, 0, 0): 1}, {}, 3) == {(4, 0, 0): 1, (0, 0, 2): 1}
    assert R.data_to_pbw({(0, 0, 2): 1}, {}, {(0, 1, 0): 1}, 3) == {(0, 4, 0): 1, (0, 0, 2): 1}
    # D1 (7, 3): f = x^7 + y z^3 + x^3 z^2 = X z^2 + X^2 x + z^3 y, g = y^7 + x z^3 = Y^2 y + z^3 x
    assert R.data_to_pbw({(1, 0, 2): 1}, {(2, 0, 0): 1}, {(0, 0, 3): 1}, 3) == {(7, 0, 0): 1, (0, 1, 3): 1, (3, 0, 2): 1}
    assert R.data_to_pbw({}, {(0, 0, 3): 1}, {(0, 2, 0): 1}, 3) == {(0, 7, 0): 1, (1, 0, 3): 1}
    # and back
    assert R.pbw_to_data({(7, 0, 0): 1, (0, 1, 3): 1, (3, 0, 2): 1}, 3) == ({(1, 0, 2): 1}, {(2, 0, 0): 1}, {(0, 0, 3): 1})
    assert R.pbw_to_data({(0, 7, 0): 1, (1, 0, 3): 1}, 3) == ({}, {(0, 0, 3): 1}, {(0, 2, 0): 1})


def test_n_f_and_d_on_b1():
    case = R.case_from_pbw("B1", 4, 3, {(4, 0, 0): 1, (0, 0, 2): 1}, {(0, 4, 0): 1, (0, 0, 2): 1})
    assert case["D"] == {(1, 1, 0): 1}                                    # D = X Y
    assert case["nf"] == {(0, 0, 6): 1, (4, 0, 0): 1}                     # z^6 + X^4
    assert case["ng"] == {(0, 0, 6): 1, (0, 4, 0): 1}                     # z^6 + Y^4


def test_commutator_identity_on_c1_and_the_complex():
    # C1 (6, 3): f = x^6 + z^3 + y^4 z, g = y^6 + x^4 z; D = - X Y z^2, - D z = X Y z^3 = x^3 y^3 z^3
    f = {(6, 0, 0): 1, (0, 0, 3): 1, (0, 4, 1): 1}
    g = {(0, 6, 0): 1, (4, 0, 1): 1}
    case = R.case_from_pbw("C1", 6, 3, f, g)
    assert case["D"] == {(1, 1, 2): 2}                                    # - X Y z^2 modulo 3
    assert R.pmul(g, f, 3) != R.pmul(f, g, 3)
    assert R.padd_mod(R.pmul(g, f, 3), R.pmul(f, g, 3), 3, -1) == {(3, 3, 3): 1}
    ids = R.identities(case, 3)
    assert ids["commutator"] and ids["s1"] and ids["s2"] and ids["g_s1_plus_f_s2"], ids


def test_criterion_routine_on_the_two_ideals_of_g1():
    assert R.criterion_polys([{(0, 0, 3): 1}, {(2, 0, 0): 1, (0, 0, 3): 1}, {(0, 2, 0): 1, (0, 0, 3): 1}], 3) is True
    assert R.criterion_polys([{(1, 1, 1): 1}, {(2, 0, 0): 1}, {(0, 2, 0): 1, (0, 0, 3): 1}], 3) is False
    # a unit ideal is zero dimensional; two generators never are
    assert R.criterion_polys([{(0, 0, 0): 1}], 3) is True
    assert R.criterion_polys([{(2, 0, 0): 1}, {(0, 2, 0): 1}], 3) is False


def test_hilbert_function_ranks_on_b1_and_a_non_pure_pair():
    f, g = {(4, 0, 0): 1, (0, 0, 2): 1}, {(0, 4, 0): 1, (0, 0, 2): 1}
    dims = R.hilbert_dims(f, g, 4, 3, 19)
    assert dims == [R.h_e(4, n) for n in range(20)] and sum(dims) == 64
    # <x^4, y^4> over GF(5) is not pure: its Hilbert function differs from h_4
    d2 = R.hilbert_dims({(4, 0, 0): 1}, {(0, 4, 0): 1}, 4, 5, 19)
    assert d2 != [R.h_e(4, n) for n in range(20)]


def test_betti_table_by_uhlib_on_b1():
    f, g = {(4, 0, 0): 1, (0, 0, 2): 1}, {(0, 4, 0): 1, (0, 0, 2): 1}
    t, dims = R.betti_uhlib(f, g, 4, 3)
    assert t == {(0, 0): 1, (1, 4): 2, (2, 12): 2, (3, 16): 1}
    assert dims[:3] == [1, 2, 4] and sum(dims) == 64


def test_random_draw_is_seeded_and_complete():
    a = R.draw_pairs(4, 3, 20261120, 200)
    b = R.draw_pairs(4, 3, 20261120, 200)
    assert a == b and len(a) == 200
    n = len(R.class_basis(4, 3))
    assert all(len(f) == n and len(g) == n and all(0 <= c < 3 for c in f + g) for f, g in a)


def test_h_e_is_a_length_e_cubed_function_supported_on_0_to_4e_and_parse():
    for e in range(3, 14):
        vals = [R.h_e(e, n) for n in range(0, 4 * e + 12)]
        assert sum(vals) == e ** 3 and all(v == 0 for v in vals[4 * e:]) and all(v >= 0 for v in vals)
    assert R.parse_pbw("x^3 z^2 + y z^3 + x^7") == {(3, 0, 2): 1, (0, 1, 3): 1, (7, 0, 0): 1}
