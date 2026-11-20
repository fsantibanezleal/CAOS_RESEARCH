"""EXP-004 (boij-soderberg-realizability): unit tests of liftcert.py, the gate G4 of the frozen hypothesis.

The monomial bookkeeping of the two constructions is checked on modules whose Hilbert functions are known by hand:
S/(a,b,c)^k, a complete intersection, the truncated ring T, and one small level module. Every check compares the
ranks mod p and over QQ, which must agree on these (the matrices are 0/1 matrices of small rank).
"""
from __future__ import annotations

import sys
from math import comb
from pathlib import Path

import pytest

EXP = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
       / "experiments" / "EXP-004-lift-certificates")
sys.path.insert(0, str(EXP))
sys.dont_write_bytecode = True
import liftcert as L  # noqa: E402

P = 32003


def poly(text):
    return L.parse_poly(text)


# ------------------------------------------------------------------------------------------------ parser

@pytest.mark.parametrize("text,expected", [
    ("-3125*a^2*b", {(2, 1, 0): -3125}),
    ("a^3", {(3, 0, 0): 1}),
    ("15921*c^3", {(0, 0, 3): 15921}),
    ("a", {(1, 0, 0): 1}),
    ("-b", {(0, 1, 0): -1}),
    ("7", {(0, 0, 0): 7}),
    ("-12", {(0, 0, 0): -12}),
    ("0", {}),
    ("14651*a^3-3125*a^2*b+c^2*b-a*b*c+9", {(3, 0, 0): 14651, (2, 1, 0): -3125, (0, 1, 2): 1,
                                           (1, 1, 1): -1, (0, 0, 0): 9}),
    ("2*a*b+3*a*b", {(1, 1, 0): 5}),
    ("a*b-a*b", {}),
])
def test_parse_poly(text, expected):
    assert poly(text) == expected


@pytest.mark.parametrize("text", ["a^", "2*d", "a**2", "1.5*a", "(a+b)", "a b", "", "a^-1"])
def test_parse_poly_rejects(text):
    with pytest.raises(ValueError):
        poly(text)


def test_symmetric_lift():
    assert L.symmetric(0, P) == 0
    assert L.symmetric(16001, P) == 16001
    assert L.symmetric(16002, P) == 16002 - P
    assert L.symmetric(P - 1, P) == -1
    assert L.symmetric(-3125, P) == -3125
    assert L.symmetric(-3125 + P, P) == -3125
    assert L.symmetric(5, 3) == -1 and L.symmetric(2, 3) == -1 and L.symmetric(1, 3) == 1


def test_parse_hit_text():
    text = ('-- EXP-001 hit x\n'
            'hitD = {0, 1, 2, 3}; hitM = 1; hitGen = "module"; hitSeed = 1; hitP = 32003;\n'
            'hitPres = {{a, b}};\n'
            'hitF = {{a-3*b, 20000*c^2}, {0, 5}};\n')
    h = L.parse_hit_text(text)
    assert h.d == (0, 1, 2, 3) and h.m == 1 and h.gen == "module" and h.seed == 1 and h.p == P
    assert h.F[0][0] == {(1, 0, 0): 1, (0, 1, 0): -3}
    assert h.F[0][1] == {(0, 0, 2): 20000}
    assert h.F[1] == [{}, {(0, 0, 0): 5}]
    lifted = L.lift_matrix(h.F, h.p)
    assert lifted[0][1] == {(0, 0, 2): 20000 - P}


def test_parse_hit_text_rejects_truncated():
    with pytest.raises(ValueError):
        L.parse_hit_text("")
    with pytest.raises(ValueError):
        L.parse_hit_text('-- x\nhitD = {0, 1, 2, 3}; hitM = 1; hitGen = "module"; hitSeed = 1; hitP = 7;\n')


# ------------------------------------------------------------------------------------------------ form (a)

def coker_hilbert(F, col_degs, dmax, p=P):
    """dim M_d for d = 0..dmax, with the ranks mod p and over QQ checked equal."""
    out = []
    for d in range(dmax + 1):
        mat = L.build_form_a(F, col_degs, d)
        rp, rq = L.rank_mod_p(mat, p), L.rank_qq(mat)
        assert rp == rq
        out.append(mat.rows - rp)
    return out


@pytest.mark.parametrize("k", [1, 2, 3, 4])
def test_form_a_power_of_maximal_ideal(k):
    # the row of all monomials of degree k: coker = S/(a,b,c)^k
    mons = sorted(L.monomials(k))
    F = [[{mu: 1} for mu in mons]]
    h = coker_hilbert(F, [k] * len(mons), k + 2)
    assert h == [comb(d + 2, 2) if d < k else 0 for d in range(k + 3)]


def test_form_a_complete_intersection():
    F = [[{(2, 0, 0): 1}, {(0, 2, 0): 1}, {(0, 0, 3): 1}]]
    # (1+t)^2 (1+t+t^2) = 1 + 3t + 4t^2 + 3t^3 + t^4
    assert coker_hilbert(F, [2, 2, 3], 6) == [1, 3, 4, 3, 1, 0, 0]


def test_form_a_free_module_and_zero_matrix():
    # coker of the zero map S^2 <- 0: free of rank 2, dimension 2*binom(d+2,2)
    F = [[{}], [{}]]
    assert coker_hilbert(F, [1], 3) == [2 * comb(d + 2, 2) for d in range(4)]


def test_form_a_two_components():
    # coker of (a, b) as S(-1)^2 -> S^1 together with a second component killed by c: S/(a,b) + S/(c)
    F = [[{(1, 0, 0): 1}, {(0, 1, 0): 1}, {}], [{}, {}, {(0, 0, 1): 1}]]
    h = coker_hilbert(F, [1, 1, 1], 4)
    assert h == [1 + 1, 1 + 2, 1 + 3, 1 + 4, 1 + 5]


def test_form_a_rejects_wrong_degree():
    with pytest.raises(ValueError):
        L.build_form_a([[{(1, 0, 0): 1, (0, 0, 0): 1}]], [1], 1)


# ------------------------------------------------------------------------------------------------ form (b)

def image_hilbert(F, r, e, dmax, p=P):
    out = []
    for d in range(dmax + 1):
        mat = L.build_form_b(F, r, e, d)
        rp, rq = L.rank_mod_p(mat, p), L.rank_qq(mat)
        assert rp == rq
        out.append(rp)
    return out


def t_hilbert(r):
    out = [0] * (3 * r + 1)
    for i in range(r + 1):
        for j in range(r + 1):
            for k in range(r + 1):
                out[i + j + k] += 1
    return out


@pytest.mark.parametrize("r", [1, 2, 3])
def test_form_b_identity_is_t(r):
    h = image_hilbert([[{(0, 0, 0): 1}]], r, 0, 3 * r + 2)
    assert h == t_hilbert(r) + [0, 0]


def test_form_b_small_level_module():
    # r = 1, T = k[a,b,c]/(a^2,b^2,c^2), image of (a, b): T^2 -> T (degree 1 entries): the ideal (a,b)T.
    # degree 1: a, b -> 2; degree 2: ab, ac, bc -> 3; degree 3: abc -> 1 (hand count)
    F = [[{(1, 0, 0): 1}, {(0, 1, 0): 1}]]
    assert image_hilbert(F, 1, 1, 4) == [2, 3, 1, 0, 0]


def test_form_b_truncation_kills_high_exponents():
    # the entry a^2 is zero in T when r = 1
    assert image_hilbert([[{(2, 0, 0): 1}]], 1, 2, 2) == [0, 0, 0]


def test_form_b_rows_are_target_degree_d_plus_e():
    mat = L.build_form_b([[{(1, 0, 0): 1}, {(0, 1, 0): 1}]], 1, 1, 0)
    assert (mat.rows, mat.cols) == (3, 2)          # T_1 has 3 monomials, 2 generators, nu = 1
    mat = L.build_form_b([[{(1, 0, 0): 1}, {(0, 1, 0): 1}]], 1, 1, 3)
    assert (mat.rows, mat.cols) == (0, 2)          # T_4 = 0 (no rows); one monomial abc of T_3, two generators


# ------------------------------------------------------------------------------------------------ ranks

def test_rank_detects_p_torsion():
    mat = L.Mat(2, 2, [(0, 0, 7), (1, 1, 1)])
    assert L.rank_qq(mat) == 2 and L.rank_mod_p(mat, 7) == 1


def test_empty_matrix_rank_zero():
    for mat in (L.Mat(0, 3, []), L.Mat(3, 0, []), L.Mat(0, 0, [])):
        assert L.rank_qq(mat) == 0 and L.rank_mod_p(mat, P) == 0


def test_rank_qq_is_exact_with_large_entries():
    big = 10 ** 30
    mat = L.Mat(2, 2, [(0, 0, big), (0, 1, big + 1), (1, 0, big - 1), (1, 1, big)])
    assert L.rank_qq(mat) == 2                      # det = big^2 - (big^2 - 1) = 1


def test_gp_text_round_trip_shape():
    mat = L.Mat(2, 3, [(0, 0, 5), (1, 2, -7)])
    text = L.gp_text(mat, 11)
    assert "matrix(2,3)" in text and "matrank" in text and "-7" in text


# ------------------------------------------------------------------------------------------------ pure Hilbert function

def test_hilbert_pure():
    assert L.hilbert_pure((0, 1, 2, 3), 1) == [1]
    assert L.hilbert_pure((0, 1, 2, 3), 4) == [4]
    h = L.hilbert_pure((0, 2, 3, 4), 1)        # primitive point (1, 6, 8, 3): H(0) = 1, degrees 0 and 1
    assert h[0] == 1 and len(h) == 2 and sum(h) > 0


def test_form_a_reproduces_pure_hilbert_on_koszul_power():
    # k = S/(a,b,c) has the pure table (0,1,2,3); its Hilbert function is 1 in degree 0 only
    F = [[{(1, 0, 0): 1}, {(0, 1, 0): 1}, {(0, 0, 1): 1}]]
    assert coker_hilbert(F, [1, 1, 1], 2) == L.hilbert_pure((0, 1, 2, 3), 1) + [0, 0]
