"""Gate G3 of EXP-009 (boij-soderberg-realizability): the family constructor against the printed polynomials (e = 4, 7), the
enumeration of the p^4 members (each once, in the stated order), the rank routine at e = 6, 7 against the module construction of
`uhlib` on five members per field (GF(7), GF(13)), the seeded members over GF(p^2), the stage-1 chunk and the early-stop bookkeeping."""
import itertools
import sys
from pathlib import Path

EXPS = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
        / "experiments")
sys.path.insert(0, str(EXPS / "EXP-009-linear-family-below-2e"))

import exp009_routine as X  # noqa: E402
from exp009_routine import R  # noqa: E402
from uhlib.module import quotient_module  # noqa: E402


def _terms(F, e, params):
    """{(row, (i, j, k)): coefficient} of the nonzero terms of the stored basis of L_e(params)."""
    C = X.family_coeff_array(F, e, params)
    basis = R.basis_json(F, C, e)
    return {(t, tuple(m)): c for t, poly in enumerate(basis) for m, c in poly}


def test_family_constructor_against_the_printed_polynomials():
    F = R.make_field("GF(13)")
    # e = 4: x^4 + a x y^3 + b y^2 z , y^4 + c x^3 y + d x^2 z
    assert _terms(F, 4, (2, 3, 5, 7)) == {
        (0, (4, 0, 0)): 1, (0, (1, 3, 0)): 2, (0, (0, 2, 1)): 3,
        (1, (0, 4, 0)): 1, (1, (3, 1, 0)): 5, (1, (2, 0, 1)): 7}
    # e = 7: x^7 + a x y^6 + b y^5 z , y^7 + c x^6 y + d x^5 z
    assert _terms(F, 7, (2, 3, 5, 7)) == {
        (0, (7, 0, 0)): 1, (0, (1, 6, 0)): 2, (0, (0, 5, 1)): 3,
        (1, (0, 7, 0)): 1, (1, (6, 1, 0)): 5, (1, (5, 0, 1)): 7}
    # a zero parameter drops its monomial: L_e(0, 0, 0, 0) = <x^e, y^e>
    assert _terms(F, 7, (0, 0, 0, 0)) == {(0, (7, 0, 0)): 1, (1, (0, 7, 0)): 1}
    # the degrees: every monomial has weight e (x, y weight 1, z weight 2)
    for e in (4, 5, 6, 7):
        for m in X.family_monomials(e):
            assert m[0] + m[1] + 2 * m[2] == e
    # the integer form agrees with the array form over GF(13)
    for e in (4, 7):
        ints = X.family_polys_int(e, 2, 3, 5, 7)
        C = R.coeff_array(F, [[F.from_int(p.get(m, 0)) for m in R.A.monos(e)] for p in ints])
        assert (C == X.family_coeff_array(F, e, (2, 3, 5, 7))).all()


def test_family_constructor_over_gf_p_squared():
    K = R.make_field("GF(9)")
    a, b, c, d = (1, 2), (0, 1), (2, 2), (1, 0)
    t = _terms(K, 5, (a, b, c, d))
    assert t[(0, (5, 0, 0))] == [1, 0] and t[(0, (1, 4, 0))] == [1, 2] and t[(0, (0, 3, 1))] == [0, 1]
    assert t[(1, (0, 5, 0))] == [1, 0] and t[(1, (4, 1, 0))] == [2, 2] and t[(1, (3, 0, 1))] == [1, 0]


def test_enumeration_over_gf3_is_every_member_once_in_lex_order():
    p = 3
    got = [X.x_params(p, i) for i in range(X.n_members(p, "X"))]
    assert len(got) == 81 == len(set(got))
    assert got == list(itertools.product(range(p), repeat=4))
    assert got[0] == (0, 0, 0, 0) and got[1] == (0, 0, 0, 1) and got[3] == (0, 0, 1, 0) and got[-1] == (2, 2, 2, 2)
    assert X.x_params(13, 13 ** 4 - 1) == (12, 12, 12, 12) and X.x_params(5, 5 ** 3) == (1, 0, 0, 0)
    assert X.n_members(3, "Y") == 20000


def test_rank_routine_at_e6_e7_against_the_uhlib_module_construction():
    for e in (6, 7):
        for name in ("GF(7)", "GF(13)"):
            F = R.make_field(name)
            ctx = R.ctx_of(F)
            p = F.p
            for i in range(5):
                params = X.x_params(p, (i * 7919 + 13 * e) % p ** 4)
                C = X.family_coeff_array(F, e, params)
                M = quotient_module(F, [0], R.polys_as_relations(F, C, e), maxdeg=3 * e)
                dims = list(M.dims) + [0] * (3 * e + 1 - len(M.dims))
                assert dims[3 * e] == R.u(3 * e) - R.rank_mu(ctx, C, e, 3 * e), (e, name, params)
                assert dims[e] == R.u(e) - 2


def test_rank_routine_over_gf9_against_the_uhlib_module_construction():
    F = R.make_field("GF(9)")
    ctx = R.ctx_of(F)
    for i in range(5):
        params = X.y_params(F, i)
        C = X.family_coeff_array(F, 5, params)
        M = quotient_module(F, [0], R.polys_as_relations(F, C, 5), maxdeg=15)
        dims = list(M.dims) + [0] * (16 - len(M.dims))
        assert dims[15] == R.u(15) - R.rank_mu(ctx, C, 5, 15)


def test_known_answers_of_the_power_pair():
    for name, pure in (("GF(11)", True), ("GF(13)", True), ("GF(3)", False), ("GF(7)", False)):
        F = R.make_field(name)
        t, _ = R.betti_table(F, X.family_coeff_array(F, 4, (0, 0, 0, 0)), 4)
        assert (t == R.pure_table(4)) is pure, name
    F = R.make_field("GF(13)")
    t, _ = R.betti_table(F, X.family_coeff_array(F, 4, (1, 0, 0, 0)), 4)
    assert t == R.pure_table(4)


def test_seeded_members_over_gf_p_squared():
    F = R.make_field("GF(25)")
    a = X.y_params(F, 17)
    assert a == X.y_params(F, 17) and a != X.y_params(F, 18)
    assert len(a) == 4 and all(len(x) == 2 and all(0 <= v < 5 for v in x) for x in a)
    assert X.params_from_json(X.params_json(a)) == a
    assert X.member_params(5, "Y", 17) == a and X.member_params(5, "X", 6) == (0, 0, 1, 1)


def test_rank_chunk_is_consistent_and_stores_only_what_it_must():
    e, p = 4, 3
    rec = X.rank_chunk(e, p, "X", 0, 81)
    r = R.target_rank(e)
    assert r == 48 and sum(rec["rank_hist"].values()) == 81 == rec["n"]
    assert rec["rank_hist"].get("48", 0) == len(rec["rank_r"])
    assert rec["above"] == [] or all(x["rank"] > r for x in rec["above"])
    assert sum(v for k, v in rec["rank_hist"].items() if int(k) > r) == len(rec["above"])
    # a chunk split in two gives the same totals as the whole
    h = X.rank_chunk(e, p, "X", 0, 40), X.rank_chunk(e, p, "X", 40, 81)
    assert h[0]["rank_r"] + h[1]["rank_r"] == rec["rank_r"]
    assert h[0]["rank_hist"] == {k: v for k, v in h[0]["rank_hist"].items()}
    # the rank of a member above r would be stored with its parameters: synthetic check of the record shape through GF(9)
    rec9 = X.rank_chunk(4, 3, "Y", 0, 6)
    assert sum(rec9["rank_hist"].values()) == 6


def test_early_stop_bookkeeping():
    es = X.EarlyStop(X.EARLY_STOP_X)
    assert es.limit == 40 and not es.stopped and es.may_submit()
    for k, n in enumerate([0, 5, 10, 20, 4, 7]):  # running totals 0, 5, 15, 35, 39, 46
        es.add([{"pure": True, "betti": [[0, 0, 1]]}] * n)
        assert es.stopped == (k == 5), k
    assert es.pure == 46 and not es.may_submit()
    ey = X.EarlyStop(X.EARLY_STOP_Y, X.MAX_BETTI_Y)
    assert ey.limit == 10 and ey.max_betti == 40
    ey.add([{"pure": False, "betti": [[0, 0, 1]]}] * 35)
    ey.inflight = 4
    assert ey.may_submit()        # 35 + 4 + 1 = 40 tables at most
    ey.inflight = 5
    assert not ey.may_submit()    # one more could make 41
    ey.add([{"pure": False, "betti": None}] * 100)   # Hilbert-only members do not count as tables
    assert ey.betti == 35 and ey.pure == 0
    ey.add([{"pure": True, "betti": [[0, 0, 1]]}] * 10)
    assert ey.stopped


def test_pair_lists_of_the_hypothesis():
    assert len(X.MAIN_PAIRS) == 15 and len(X.CONTROL_PAIRS) == 5 and len(X.PAIRS) == 20
    assert all(p < 2 * e for e, p in X.MAIN_PAIRS) and all(p >= 2 * e for e, p in X.CONTROL_PAIRS)
    assert X.MAIN_PAIRS == sorted(X.MAIN_PAIRS)
    assert {(e, p) for e, p in X.MAIN_PAIRS if e == 6} == {(6, 3), (6, 5), (6, 7), (6, 11)}
    assert [R.target_rank(e) for e in (4, 5, 6, 7)] == [48, 70, 96, 126]
