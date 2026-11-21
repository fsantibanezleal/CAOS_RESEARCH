"""Gate G3 of EXP-021 (boij-soderberg-realizability): the admissible triples of S(d; 0, 1) for e = 5, 7, 9, 11, 13; the rows of the blocks of
mu_33 at e = 11; the digits, the index and the monomials of a member (the members of indices 0, 1, 3^14 and 3^16 - 1 at e = 11 written out,
the index recovered from the coefficient vectors, every member in S(d; 0, 1)); the blocks of indices; the seeded random blocks; the stages of
the first 3,000 members at (5, 3) against a direct computation that ranks every block; a member of stage 3 passes the plain staged test; the
census of a block is additive; the plan of the cases.  No test computes a member of (11, 3) beyond writing its polynomials."""
import importlib.util
import random
import sys
from pathlib import Path

EXP21 = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
         / "EXP-021-three-term-stratum")
sys.path.insert(0, str(EXP21))

import exp021_routine as X  # noqa: E402

R, np, A = X.R, X.np, X.A


def _load_run():
    spec = importlib.util.spec_from_file_location("exp021_run", EXP21 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp021_run"] = mod
    spec.loader.exec_module(mod)
    return mod


def _terms(e, v):
    return {m: int(c) for m, c in zip(A.monos(e), v) if int(c)}


def test_the_admissible_triples_of_s_d_0_1_for_e_5_to_13():
    assert X.triples(5) == [(0, 1, 0)]
    for e in (7, 9, 11, 13):
        assert X.triples(e) == [(1, 2, 2)], e
    assert X.pattern(5) == (2, 0, 1, [0, 1])
    assert X.pattern(11) == (5, 1, 2, [1, 2, 0, 3, 4])


def test_the_rows_of_the_blocks_of_mu_33_at_e_11():
    assert X.block_rows(11) == [57, 59, 59, 57, 56]
    Rk = R.ranker(11, 3, 5, 0, 1)
    assert [TF.shape[1] + TG.shape[1] for TF, TG in Rk.blocks(33)] == [57, 59, 59, 57, 56]
    assert sum(TF.shape[2] for TF, _ in Rk.blocks(33)) == A.dim_U(33)


def test_the_members_of_indices_0_1_3_14_and_3_16_minus_1_at_e_11_written_out():
    e, p = 11, 3
    assert X.n_members(e, p) == 3 ** 16 == 43_046_721
    got = {}
    for idx in (0, 1, 3 ** 14, 3 ** 16 - 1):
        dg = X.digits_of_indices(e, p, [idx])
        F, G = X.full_vectors(e, p, dg)
        assert X.digits_from_vectors(e, F[0], G[0]) == dg[0].tolist()
        assert X.index_of_digits(p, dg[0]) == idx
        got[idx] = (_terms(e, F[0]), _terms(e, G[0]), R.poly_text(e, p, F[0]), R.poly_text(e, p, G[0]))
    xe, ye = {(11, 0, 0): 1}, {(0, 11, 0): 1}
    assert got[0][:2] == (xe, ye) and got[0][2:] == ("x^11", "y^11")
    assert got[1][0] == xe and got[1][1] == {(0, 11, 0): 1, (0, 1, 5): 1}  # last digit: beta on y z^5
    assert got[1][3] == "y*z^5 + y^11"
    assert got[3 ** 14][0] == xe and got[3 ** 14][1] == {(0, 11, 0): 1, (9, 0, 1): 1}  # second digit: delta on x^9 z
    assert got[3 ** 14][3] == "y^11 + x^9*z"
    f_all = {(11, 0, 0): 1, (1, 10, 0): 2, (0, 9, 1): 2, **{(6 - c, 5 - c, c): 2 for c in range(6)}}
    g_all = {(0, 11, 0): 1, (10, 1, 0): 2, (9, 0, 1): 2, **{(5 - c, 6 - c, c): 2 for c in range(6)}}
    assert got[3 ** 16 - 1][:2] == (f_all, g_all)
    assert got[3 ** 16 - 1][2] == ("-y^9*z - x*z^5 - x*y^10 - x^2*y*z^4 - x^3*y^2*z^3 - x^4*y^3*z^2 - x^5*y^4*z - x^6*y^5 + x^11")


def test_every_member_is_in_the_stratum_and_the_index_is_recovered():
    rng = random.Random(21)
    for e, p in ((5, 3), (7, 5), (11, 3), (11, 7), (13, 3)):
        m = (e - 1) // 2
        total = X.n_members(e, p)
        idx = np.array([0, total - 1] + [rng.randrange(total) for _ in range(200)], dtype=np.int64)
        dg = X.digits_of_indices(e, p, idx)
        F, G = X.full_vectors(e, p, dg)
        for k in range(len(idx)):
            fk, gk = _terms(e, F[k]), _terms(e, G[k])
            assert all((b + c) % m == 0 for (a, b, c) in fk) and all((b + c) % m == 1 for (a, b, c) in gk)
            assert fk[(e, 0, 0)] == 1 and gk[(0, e, 0)] == 1
            assert X.digits_from_vectors(e, F[k], G[k]) == dg[k].tolist()
            assert X.index_of_digits(p, dg[k]) == int(idx[k])
    # the thresholds: the members below p^(e+3) have delta = 0, below p^(e+1) gamma = delta = 0
    e, p = 5, 3
    dg = X.digits_of_indices(e, p, np.arange(0, p ** (e + 3), 97))
    assert not dg[:, 0:2].any()
    dg = X.digits_of_indices(e, p, np.arange(0, p ** (e + 1), 7))
    assert not dg[:, 0:4].any()


def test_the_blocks_of_indices_cover_the_list_once():
    total = 3 ** 16
    bl = X.blocks_of(total)
    assert len(bl) == 2153 and bl[0] == (0, 20000) and bl[-1] == (43_040_000, 43_046_721)
    assert all(b[1] == c[0] for b, c in zip(bl, bl[1:])) and sum(b - a for a, b in bl) == total
    assert X.blocks_of(59049)[-1] == (40000, 59049) and len(X.blocks_of(400_000)) == 20


def test_the_random_blocks_are_seeded_by_the_pair_and_the_start():
    e, p = 7, 5
    a = X.digits_block(e, p, 20000, 20050, False)
    want = np.random.default_rng([20261120 + 1000 * e + p, 20000]).integers(0, p, size=(50, e + 5))
    assert np.array_equal(a, want) and a.shape == (50, 12)
    assert not np.array_equal(a, X.digits_block(e, p, 0, 50, False))
    assert np.array_equal(X.digits_block(5, 3, 100, 120, True), X.digits_of_indices(5, 3, np.arange(100, 120)))


def test_the_stages_of_the_first_3000_members_at_5_3_equal_the_direct_computation():
    e, p = 5, 3
    out = X.job((e, p, 0, 3000, True))
    F, G = X.full_vectors(e, p, X.digits_block(e, p, 0, 3000, True))
    direct = [0] * 4
    for k in range(3000):
        direct[X.stage_direct(e, p, F[k], G[k])] += 1
    assert out["stages"] == direct and sum(direct) == 3000
    assert direct[3] > 0 and direct[0] > direct[1] > 0  # all four stages that the census distinguishes are seen except possibly stage 2
    assert [m["index"] for m in out["found"]][:3] == [124, 142, 159]  # the first indices of stage 3 of the probe
    assert len(out["found"]) == direct[3]
    # a member of stage 3 passes the plain staged test, a member of another stage with the pattern does not
    Rk = R.ranker(e, p, 2, 0, 1)
    I, J = R.support(e, 2, 0), R.support(e, 2, 1)
    for m in out["found"][:20]:
        assert Rk.evaluate(np.array(m["f"])[I], np.array(m["g"])[J])[1] is True
        assert X.digits_from_vectors(e, m["f"], m["g"]) == m["digits"] and X.index_of_digits(p, m["digits"]) == m["index"]
    assert out["below_delta0"][3] == sum(1 for m in out["found"] if m["index"] < p ** (e + 3))
    assert out["below_gamma_delta0"][3] == sum(1 for m in out["found"] if m["index"] < p ** (e + 1))


def test_the_census_of_a_block_is_additive_and_the_plain_count_is_the_plain_staged_test():
    e, p = 5, 3
    whole = X.job((e, p, 0, 3000, True, True))
    parts = [X.job((e, p, a, b, True, True)) for a, b in ((0, 500), (500, 1700), (1700, 3000))]
    for key in ("stages", "below_delta0", "below_gamma_delta0"):
        assert [sum(x[key][k] for x in parts) for k in range(4)] == whole[key]
    assert sum(x["plain"] for x in parts) == whole["plain"]
    assert whole["plain"] >= whole["stages"][3]  # every member of stage 3 has the pure Hilbert function
    F, G = X.full_vectors(e, p, X.digits_block(e, p, 0, 3000, True))
    Rk = R.ranker(e, p, 2, 0, 1)
    I, J = R.support(e, 2, 0), R.support(e, 2, 1)
    assert whole["plain"] == sum(bool(Rk.evaluate(F[k, I], G[k, J])[1]) for k in range(3000))
    assert [m["index"] for x in parts for m in x["found"]] == [m["index"] for m in whole["found"]]


def test_the_non_monic_members_at_5_3_are_split_off_the_enumeration_of_exp010():
    e, p = 5, 3
    assert R.n_members(e, p, 2, 0, 1) == 132_496
    out = X.nonmonic_job((e, p, 0, 3000))
    assert sum(out["stages"]) + out["both_nonzero"] == 3000 and sum(out["stages"]) > 0
    assert out["stages"][3] == 0  # none of the non-monic members of the hypothesis reaches stage 3


def test_a_stage_3_member_has_the_pure_table_of_length_e_cubed_and_a_non_pure_one_does_not():
    e, p = 5, 3
    F, G = X.full_vectors(e, p, X.digits_of_indices(e, p, [866, 124]))
    pure = X.betti_job({"index": 866, "e": e, "p": p, "f": F[0].tolist(), "g": G[0].tolist()})
    assert pure["betti"] == [[0, 0, 1], [1, 5, 2], [2, 15, 2], [3, 20, 1]] and pure["length"] == 125 and pure["pure"] is True
    assert R.poly_text(e, p, F[0]) == "y^3*z - x*z^2 + x^2*y*z + x^5" and R.poly_text(e, p, G[0]) == "-y*z^2 + y^5"
    other = X.betti_job({"index": 124, "e": e, "p": p, "f": F[1].tolist(), "g": G[1].tolist()})
    assert other["pure"] is False


def test_the_plan_of_the_cases_follows_the_hypothesis():
    run = _load_run()
    assert [(c["e"], c["p"], c["mode"], c["members"], c["total"]) for c in run.plan("K")] == [
        (5, 3, "complete", 59049, 59049), (7, 5, "random", 400_000, 5 ** 12), (11, 7, "random", 200_000, 7 ** 16)]
    x = run.plan("X")
    assert [(c["e"], c["p"], c["mode"], c["members"], c["blocks"]) for c in x] == [(11, 3, "complete", 43_046_721, 2153)]
    assert x[0]["table_rule"] == "early" and run.plan("K")[0]["table_rule"] == "all"
    assert [c["key"] for c in run.order()] == ["K|5|3", "K|7|5", "K|11|7", "X|11|3"]
    assert run.NONMONIC == {"e": 5, "p": 3, "members": 132_496, "monic": 59_049, "non_monic": 73_447}
    assert run.KNOWN["K|5|3"]["stages"] == [44175, 7526, 5684, 1664] and run.KNOWN["K|11|7"]["found"] == 0
    assert run.plan("X", {(11, 7)}) == [] and run.plan("K", {(11, 7)})[0]["key"] == "K|11|7"
