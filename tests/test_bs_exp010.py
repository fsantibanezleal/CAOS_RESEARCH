"""Gate G3 of EXP-010 (boij-soderberg-realizability): the weights and supports against a hand-written list for e = 4; the number of
members N and the enumeration (each normalized member once) on two small strata; the admissible list for e = 5 (and the totals of the
note for e = 4 to 8); the rank routine against the module construction of `uhlib`; the pure Hilbert function test on <x^4, y^4> over
GF(13) (true) and GF(5) (false); the early stop (bookkeeping and on a real stratum through the scheduler of run.py)."""
import importlib.util
import itertools
import random
import sys
from pathlib import Path

import numpy as np

EXP = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
       / "EXP-010-weight-class-strata")
sys.path.insert(0, str(EXP))

import exp010_routine as X  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib.fields import PrimeField  # noqa: E402
from uhlib.module import quotient_module  # noqa: E402


def _load_run():
    spec = importlib.util.spec_from_file_location("exp010_run", EXP / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_weights_and_supports_for_e4_against_a_hand_written_list():
    # the order of uhlib's monos(4): x^a y^b z^c as (a, b, c); the weight is b + c
    hand = [((0, 4, 0), 4), ((1, 3, 0), 3), ((2, 2, 0), 2), ((3, 1, 0), 1), ((4, 0, 0), 0), ((0, 2, 1), 3), ((1, 1, 1), 2),
            ((2, 0, 1), 1), ((0, 0, 2), 2)]
    assert [(m, X.weight(m)) for m in A.monos(4)] == hand
    assert X.weights(4) == [w for _, w in hand]
    # supports (indices into monos(4)) of the classes: m = 2, m = 3, m = 5
    assert X.support(4, 2, 0) == [0, 2, 4, 6, 8] and X.support(4, 2, 1) == [1, 3, 5, 7]
    assert X.support(4, 3, 0) == [1, 4, 5] and X.support(4, 3, 1) == [0, 3, 7] and X.support(4, 3, 2) == [2, 6, 8]
    assert X.support(4, 5, 4) == [0] and X.support(4, 5, 0) == [4] and X.support(4, 5, 3) == [1, 5]
    # the classes partition the monomials; d_i is the size of the support
    for e in (4, 5, 6, 7):
        for m in range(2, e + 2):
            idx = sorted(k for i in range(m) for k in X.support(e, m, i))
            assert idx == list(range(A.dim_U(e)))
            assert [X.d_of(e, m, i) for i in range(m)] == [len(X.support(e, m, i)) for i in range(m)]
    # the dimension formula of the note: monomials of degree e and weight w number min(w, e - w) + 1
    for e in (6, 7):
        for w in range(e + 1):
            assert sum(1 for m in A.monos(e) if X.weight(m) == w) == min(w, e - w) + 1


def test_the_stratum_lists_and_indices():
    for e in (4, 5, 6, 7, 8):
        L = X.all_strata(e)
        assert len(L) == sum((m * (m + 1)) // 2 for m in range(2, e + 2)) == len(set(L))
        assert [X.stratum_index(e, *s) for s in L] == list(range(len(L)))
        assert L[0] == (2, 0, 0) and L[1] == (2, 0, 1) and L[2] == (2, 1, 1) and L[3] == (3, 0, 0)


def test_member_count_and_enumeration_each_normalized_member_once():
    for e, p, m, i, j in ((4, 3, 4, 0, 2), (5, 3, 5, 0, 2), (4, 5, 2, 0, 1)):
        di, dj = X.d_of(e, m, i), X.d_of(e, m, j)
        N = X.n_members(e, p, m, i, j)
        assert N == ((p ** di - 1) // (p - 1)) * ((p ** dj - 1) // (p - 1))
        F, G = X.enumerate_members(e, p, m, i, j, 0, N)
        assert F.shape == (N, di) and G.shape == (N, dj)
        pairs = {(tuple(f), tuple(g)) for f, g in zip(F.tolist(), G.tolist())}
        assert len(pairs) == N  # no member twice
        for v in list(F.tolist()) + list(G.tolist()):
            first = next(c for c in v if c)  # normalized: the first nonzero coefficient is 1, and the vector is nonzero
            assert first == 1 and all(0 <= c < p for c in v)
        # every normalized pair of vectors appears (the product of the two sets of normalized vectors)
        def normalized(d):
            return {v for v in itertools.product(range(p), repeat=d) if any(v) and next(c for c in v if c) == 1}
        assert pairs == {(f, g) for f in normalized(di) for g in normalized(dj)}
        # a sub-range is the same members
        F2, G2 = X.enumerate_members(e, p, m, i, j, 3, 11)
        assert (F2 == F[3:11]).all() and (G2 == G[3:11]).all()
    assert X.n_members(4, 3, 2, 0, 0) is None  # i = j: never enumerated
    assert X.n_members(4, 3, 2, 0, 1) == X.n_members(4, 3, 2, 0, 1)
    # the example of the hypothesis: 3,529,470 members in S(2; 0, 1) is the budget at (7, 7), N is larger
    assert X.budget_q(7, 7) == 3529470 and X.budget_q(6, 5) == 20000 and X.budget_q(6, 7) == 72030
    assert X.budget_q(7, 3) == 21870 and X.budget_q(7, 5) == 468750


def test_sampled_members_are_reproducible_from_the_seed():
    a = X.sample_members(7, 5, 2, 0, 1, 2000, 2010, seed_index=11)
    b = X.sample_members(7, 5, 2, 0, 1, 2000, 2010, seed_index=11)
    c = X.sample_members(7, 5, 2, 0, 1, 2000, 2010, seed_index=12)
    assert (a[0] == b[0]).all() and (a[1] == b[1]).all()
    assert not (a[0] == c[0]).all()
    assert a[0].shape == (10, X.d_of(7, 2, 0)) and a[0].max() < 5 and a[0].min() >= 0


def test_the_admissible_list_for_e5_equals_the_note():
    assert X.admissible_strata(5) == [(2, 0, 1), (3, 0, 2), (4, 0, 1)] + [(5, i, j) for i in range(5) for j in range(i, 5)] + [
        (6, 0, 5)]
    assert len([s for s in X.admissible_strata(5) if s[0] == 5]) == 15
    for e, total in ((4, 17), (5, 19), (6, 34), (7, 34), (8, 58)):
        assert len(X.admissible_strata(e)) == total
        assert X.admissible_strata(e) == X.note_table(e)
    # the stratum of the power pair <x^e, y^e> (weights 0 and e) is admissible for every m
    for e in (4, 5, 6, 7, 8):
        for m in range(2, e + 2):
            i, j = sorted((0, e % m))
            assert (m, i, j) in X.admissible_strata(e)


def _random_member(rng, e, p, m, i, j):
    I, J = X.support(e, m, i), X.support(e, m, j)
    f = np.zeros(A.dim_U(e), dtype=np.int64)
    g = np.zeros(A.dim_U(e), dtype=np.int64)
    f[I] = [rng.randrange(p) for _ in I]
    g[J] = [rng.randrange(p) for _ in J]
    return f, g


def test_rank_routine_against_the_uhlib_module_construction_on_a_small_case():
    rng = random.Random(7)
    for e, p, m, i, j in ((4, 5, 1, 0, 0), (4, 5, 2, 0, 1), (5, 7, 3, 0, 2), (5, 5, 4, 0, 1), (4, 13, 5, 0, 4)):
        F = PrimeField(p)
        for _ in range(4):
            f, g = _random_member(rng, e, p, m, i, j) if m > 1 else (
                np.array([rng.randrange(p) for _ in range(A.dim_U(e))]), np.array([rng.randrange(p) for _ in range(A.dim_U(e))]))
            rels = [{(0, mono): int(c) for mono, c in zip(A.monos(e), v) if c} for v in (f, g)]
            M = quotient_module(F, [0], rels, maxdeg=4 * e - 3)
            dims = list(M.dims) + [0] * (4 * e - 2 - len(M.dims))
            for n in (3 * e - 1, 3 * e, 3 * e + 1, 4 * e - 3):
                assert dims[n] == A.dim_U(n) - X.rank_plain(e, p, n, f, g), (e, p, n)


def test_block_rank_equals_the_plain_rank_on_random_members():
    rng = random.Random(11)
    for e, p, m, i, j in ((5, 5, 2, 0, 1), (5, 7, 3, 0, 2), (6, 5, 4, 0, 2), (6, 3, 6, 1, 3), (4, 3, 2, 0, 0), (7, 3, 7, 0, 1)):
        R = X.Ranker(e, p, m, i, j)
        for _ in range(6):
            f, g = _random_member(rng, e, p, m, i, j)
            fs, gs = f[X.support(e, m, i)], g[X.support(e, m, j)]
            for n in [3 * e - 1, 3 * e] + X.hf_degrees(e)[1:]:
                assert R.rank(fs, gs, n) == X.rank_plain(e, p, n, f, g), (e, p, m, i, j, n)


def test_pure_hilbert_function_test_on_x4_y4():
    def vecs(e):
        f = np.zeros(A.dim_U(e), dtype=np.int64)
        g = np.zeros(A.dim_U(e), dtype=np.int64)
        f[list(A.monos(e)).index((e, 0, 0))] = 1
        g[list(A.monos(e)).index((0, e, 0))] = 1
        return f, g
    f, g = vecs(4)
    assert X.pure_hilbert_full(4, 13, f, g) is True
    assert X.pure_hilbert_full(4, 5, f, g) is False
    # the Betti table is computed by uhlib: pure over GF(13), not over GF(5)
    t13 = X.betti_table(4, 13, f, g)
    assert t13 == X.pure_table(4) == {(0, 0): 1, (1, 4): 2, (2, 12): 2, (3, 16): 1}
    assert X.betti_table(4, 5, f, g) != X.pure_table(4)
    # the target ranks and the Hilbert function of the pure table
    assert X.target_rank(4) == 2 * A.dim_U(8) - 2 == 2 * 25 - 2
    assert [X.h_e(4, n) for n in (13, 14, 15)] == [0, 0, 0]
    assert X.h_e(6, 18) == 4 and X.h_e(7, 21) == 6 and X.target_rank(6) == 96 and X.target_rank(7) == 126


def test_early_stop_bookkeeping():
    es = X.EarlyStop(limit=5, max_tables=40)
    assert es.may_start_table() and not es.stopped
    for _ in range(3):
        es.table_started()
        es.table_done(pure=True)
    assert es.pure == 3 and es.tables == 3 and not es.stopped
    es.table_started()
    es.table_started()
    es.table_done(pure=True)
    es.table_done(pure=True)
    assert es.stopped and es.pure == 5 and not es.may_start_table()
    # the cap of 40 tables: never more than 40 started, with the tables in flight counted
    es = X.EarlyStop(limit=5, max_tables=40)
    started = 0
    while es.may_start_table():
        es.table_started()
        started += 1
        if started % 7 == 0:
            es.table_done(pure=False)
            es.table_done(pure=False)
        if started > 100:
            break
    assert es.tables + es.inflight <= 40 and not es.stopped


def test_early_stop_on_a_real_stratum_through_the_scheduler():
    run = _load_run()
    spec = run.make_spec("T", 4, 13, 2, 0, 1, budget=20000, admissible=True)
    res = {"strata": {}, "gates": {}, "runs": [], "budget": {"used_seconds": 0.0}}
    # a tiny chunk size so that several chunks exist and the early stop is visible
    rc = run.run_specs(res, [spec], workers=2, chunk=300, deadline=None, save_fn=lambda r: None, quiet=True)
    assert rc == 0
    rec = res["strata"][spec["key"]]
    assert rec["pure"] >= 5 and rec["stopped_early"] is True and rec["complete"] is False
    assert rec["examined"] < rec["planned"] and rec["examined"] % 300 == 0 or rec["examined"] == rec["planned"]
    assert rec["tables"] <= 40 and rec["pure_hilbert"] >= rec["pure"]
    assert sum(rec["rank_hist"].values()) == rec["examined"]
    # a stratum the early stop never reaches is run to its budget and reported complete or sampled
    spec2 = run.make_spec("T", 4, 3, 4, 0, 2, budget=20000, admissible=True)
    res2 = {"strata": {}, "gates": {}, "runs": [], "budget": {"used_seconds": 0.0}}
    run.run_specs(res2, [spec2], workers=2, chunk=300, deadline=None, save_fn=lambda r: None, quiet=True)
    r2 = res2["strata"][spec2["key"]]
    assert r2["examined"] == r2["planned"] and r2["all_members"] is True
