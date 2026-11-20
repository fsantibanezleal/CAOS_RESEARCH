"""Gate G3 of EXP-011 (boij-soderberg-realizability): the constructor of f and g against hand-written polynomials for T1 and
T3, the commutator identity on T1, the resultant test on a coprime and a non-coprime pair, and the Hilbert function routine on
<x^4, y^4> over GF(13) against h_4."""
import sys
from pathlib import Path

EXPS = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
        / "experiments")
sys.path.insert(0, str(EXPS / "EXP-011-central-pair-machine-checks"))

import exp011_routine as R  # noqa: E402


def test_constructor_t1_against_hand_written_polynomials():
    # (e, p) = (3, 3), s = 1, A = x^3, B = y^3, l_1 = y, l_2 = x:  f = x^3 + y z,  g = y^3 + x z
    f, g = R.build_pair(3, 3, {(3, 0): 1}, {(0, 3): 1}, (0, 1), (1, 0))
    assert f == {(3, 0, 0): 1, (0, 1, 1): 1}
    assert g == {(0, 3, 0): 1, (1, 0, 1): 1}


def test_constructor_t3_against_hand_written_polynomials():
    # (5, 5), s = 2, l_1 = y, l_2 = x:  f = x^5 + y z^2,  g = y^5 + x z^2
    f, g = R.build_pair(5, 5, {(5, 0): 1}, {(0, 5): 1}, (0, 1), (1, 0))
    assert f == {(5, 0, 0): 1, (0, 1, 2): 1}
    assert g == {(0, 5, 0): 1, (1, 0, 2): 1}
    # T4: (l_1, l_2) = (2 y, 3 x)
    f, g = R.build_pair(5, 5, {(5, 0): 1}, {(0, 5): 1}, (0, 2), (3, 0))
    assert f == {(5, 0, 0): 1, (0, 1, 2): 2} and g == {(0, 5, 0): 1, (1, 0, 2): 3}


def test_constructor_in_x_p_y_p_expands_the_frobenius_powers():
    # G2: (5, 5), A = X + 2 Y, B = 3 X + 2 Y with X = x^5, Y = y^5
    A, B = R.xy_from_XY(5, {(1, 0): 1, (0, 1): 2}), R.xy_from_XY(5, {(1, 0): 3, (0, 1): 2})
    assert A == {(5, 0): 1, (0, 5): 2} and B == {(5, 0): 3, (0, 5): 2}
    # G1: (9, 3), A = X^3 + X Y^2 is x^9 + x^3 y^6
    assert R.xy_from_XY(3, {(3, 0): 1, (1, 2): 1}) == {(9, 0): 1, (3, 6): 1}


def test_commutator_identity_on_t1():
    f, g = R.build_pair(3, 3, {(3, 0): 1}, {(0, 3): 1}, (0, 1), (1, 0))
    comm = R.sub(R.mul(g, f, 3), R.mul(f, g, 3), 3)
    assert R.lam_formula((0, 1), (1, 0), 3) == 1            # [x, y] = z, so lambda = 1
    assert comm == {(0, 0, 3): 1}                           # g f - f g = z^3
    ident = R.identities(3, 3, f, g, {(3, 0, 0): 1}, {(0, 3, 0): 1})
    assert ident["all"] and ident["lambda"] == 1


def test_resultant_on_a_coprime_and_a_non_coprime_pair():
    # coprime: x^5 + 2 y^5 and 3 x^5 + 2 y^5 over GF(5) (the forms are (x + 2^(1/5) y)^5 type, no common factor)
    assert R.resultant_mod(5, {(5, 0): 1, (0, 5): 2}, {(5, 0): 3, (0, 5): 2}, 5) != 0
    # non-coprime: X^3 and X^2 Y with X = x^3 over GF(3) (common factor x^6)
    assert R.resultant_mod(3, {(9, 0): 1}, {(6, 3): 1}, 9) == 0
    # a classical pair: x^2 and y^2 are coprime, x^2 and x y are not
    assert R.resultant_mod(7, {(2, 0): 1}, {(0, 2): 1}, 2) != 0
    assert R.resultant_mod(7, {(2, 0): 1}, {(1, 1): 1}, 2) == 0


def test_hilbert_routine_on_x4_y4_over_gf13_against_h4():
    f, g = {(4, 0, 0): 1}, {(0, 4, 0): 1}
    dims = R.hilbert(13, 4, f, g, 4 * 4 + 2)
    assert dims == [R.h_e(4, n) for n in range(4 * 4 + 3)]
    assert sum(dims) == 4 ** 3
    # over GF(5) with e = 4 the pair is not pure: the Hilbert function differs somewhere
    assert R.hilbert(5, 4, f, g, 4 * 4 + 2) != dims
