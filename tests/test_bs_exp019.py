"""Gate G3 of EXP-019 (boij-soderberg-realizability): the conversion between (alpha, beta) and the pair (f, g) for t = 2, 3 against products
computed with the structure constants of `uhlib` on random members at e = 6, 7; the filter for t = 1 against `exp017_routine.filter_member`
on 2,000 random members at (7, 5) and (9, 7); (F1) and (F2) through the inverse modulo Delta against the linear algebra of EXP-017 for
t = 2 on random members of (8, 7); the supports of the strata of (13, 11), (14, 5) and (16, 17) against hand-written lists; the exponent of
each case; the seed and the order of the members; the plan of the cases; and G1 (a), the filter on every stored member with a table."""
import importlib.util
import random
import sys
from pathlib import Path

EXP19 = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
         / "EXP-019-filter-every-exponent")
sys.path.insert(0, str(EXP19))

import exp019_routine as R  # noqa: E402
from uhlib import algebra as A  # noqa: E402

R17 = R.R17


def _mul(u, v, p):
    out = {}
    for m1, c1 in u.items():
        for m2, c2 in v.items():
            for mm, c in A.mono_mul(m1, m2):
                out[mm] = (out.get(mm, 0) + c1 * c2 * c) % p
    return {m: c for m, c in out.items() if c}


def _product_pair(e, p, t, alpha, beta):
    """f = x^e + alpha(xy, z) y^t and g = y^e + beta(xy, z) x^t, computed by multiplying out in U(H) with `mono_mul` (h = xy, z central)."""
    d = (e - t) // 2
    h = {(1, 1, 0): 1}
    pw = [{(0, 0, 0): 1}]
    for _ in range(d):
        pw.append(_mul(pw[-1], h, p))

    def form(coefs):
        tot = {}
        for k, c in enumerate(coefs):
            for mm, v in _mul(pw[k], {(0, 0, d - k): c % p}, p).items():
                tot[mm] = (tot.get(mm, 0) + v) % p
        return tot

    f = _mul(form(alpha), {(0, t, 0): 1}, p)
    g = _mul(form(beta), {(t, 0, 0): 1}, p)
    f[(e, 0, 0)] = (f.get((e, 0, 0), 0) + 1) % p
    g[(0, e, 0)] = (g.get((0, e, 0), 0) + 1) % p
    return {m: c for m, c in f.items() if c}, {m: c for m, c in g.items() if c}


def _as_dict(e, v):
    return {m: int(c) for m, c in zip(A.monos(e), v) if int(c)}


def test_conversion_for_t_2_and_3_against_products_in_u_on_random_members_at_e6_and_e7():
    rng = random.Random(19)
    for e, t in ((6, 2), (6, 4), (7, 3), (7, 5), (7, 1)):
        d = (e - t) // 2
        for p in (5, 7, 11, 13):
            for _ in range(12):
                alpha = [rng.randrange(p) for _ in range(d + 1)]
                beta = [rng.randrange(p) for _ in range(d + 1)]
                f, g = R.pair_vectors(e, p, t, alpha, beta)
                pf, pg = _product_pair(e, p, t, alpha, beta)
                assert _as_dict(e, f) == pf, (e, t, p, alpha, beta)
                assert _as_dict(e, g) == pg, (e, t, p, alpha, beta)
                assert R.alpha_beta_of_pair(e, p, t, f, g) == (alpha, beta)
                # a stored pair is rescaled by 1/c0, 1/c1: a scalar multiple of f and of g gives the same member
                assert R.alpha_beta_of_pair(e, p, t, [3 * c % p for c in f], [2 * c % p for c in g]) == (alpha, beta)


def test_a_pair_outside_the_chart_has_no_member():
    e, t, p = 7, 3, 11
    f, g = R.pair_vectors(e, p, t, [1, 2, 3], [1, 1, 1])
    f2 = list(f)
    f2[A.monos(e).index((3, 2, 1))] = 4  # x^3 y^2 z is not of the form x^a y^(a+3) z^(2-a)
    assert R.alpha_beta_of_pair(e, p, t, f2, g) is None
    f3 = list(f)
    f3[A.monos(e).index((e, 0, 0))] = 0
    assert R.alpha_beta_of_pair(e, p, t, f3, g) is None


def _agree_with_exp017(e, p, n, seed_index):
    alpha, beta = R.sample_block(e, p, 1, seed_index, 0, n, n)
    stages = []
    for k in range(n):
        a, b = [int(v) for v in alpha[k]], [int(v) for v in beta[k]]
        got, want = R.filter_t(e, p, 1, a, b), R17.filter_member(e, p, a, b)
        assert got == want, (e, p, a, b, got, want)
        stages.append(got[0])
    assert sum(1 for s in stages if s >= 2) > 0  # the comparison is not empty: members pass (F1)
    return stages


def test_the_filter_for_t_1_is_the_filter_of_exp017_on_2000_members_at_7_5():
    stages = _agree_with_exp017(7, 5, 2000, 1)
    assert sum(1 for s in stages if s >= 3) > 0


def test_the_filter_for_t_1_is_the_filter_of_exp017_on_2000_members_at_9_7():
    _agree_with_exp017(9, 7, 2000, 2)


def _reference_filter(e, p, t, alpha, beta):
    """(F0) to (F3) with the linear algebra of EXP-017 (`solve_mult`) in place of the inverse modulo Delta."""
    d = (e - t) // 2
    P = R17.P_
    ae = R17.a_poly(p, e - t)
    al, be = P(p, alpha), P(p, beta)
    bs = be(P(p, [(e - t) % p, 1]))
    delta = al * bs - ae
    if delta.degree() != 2 * d:
        return 0, None, None
    x = P(p, [1])
    xp = P(p, [1])
    for k in range(t):
        x = x * P(p, [-2 * t + k, 1])
        xp = xp * P(p, [e + k, 1])
    x = x * delta(P(p, [-(e + t) % p, 1]))
    xp = xp * delta(P(p, [(e + t) % p, 1]))
    if delta.gcd(x).degree() > 0 or delta.gcd(xp).degree() > 0:
        return 0, None, None
    c = R17.solve_mult(xp * al, x, delta, d, p)
    if c is None:
        return 1, None, None
    cp = R17.solve_mult(x * bs, xp, delta, d, p)
    if cp is None:
        return 2, R17.coeffs(c, d + 1), None
    cl, cpl = R17.coeffs(c, d + 1), R17.coeffs(cp, d + 1)
    return (3 if (c * cp - ae).degree() < 0 else 4), cl, cpl


def test_f1_and_f2_through_the_inverse_equal_the_linear_algebra_for_t_2_at_8_7():
    e, p, t = 8, 7, 2
    alpha, beta = R.sample_block(e, p, t, 3, 0, 6000, 6000)
    stages = []
    for k in range(6000):
        a, b = [int(v) for v in alpha[k]], [int(v) for v in beta[k]]
        got, want = R.filter_t(e, p, t, a, b), _reference_filter(e, p, t, a, b)
        assert got == want, (a, b, got, want)
        stages.append(got[0])
    assert sum(1 for s in stages if s >= 2) > 10 and sum(1 for s in stages if s >= 3) > 0


def test_the_filter_on_random_members_at_larger_exponents_equals_the_linear_algebra():
    for e, p, t, n in ((9, 11, 5, 4000), (9, 13, 3, 3000), (10, 11, 4, 2000)):
        alpha, beta = R.sample_block(e, p, t, 0, 0, n, n)
        for k in range(n):
            a, b = [int(v) for v in alpha[k]], [int(v) for v in beta[k]]
            assert R.filter_t(e, p, t, a, b) == _reference_filter(e, p, t, a, b), (e, p, t, a, b)


def _hand_support(e, t):
    d = (e - t) // 2
    return ({(e, 0, 0)} | {(a, a + t, d - a) for a in range(d + 1)}, {(0, e, 0)} | {(a + t, a, d - a) for a in range(d + 1)})


def test_the_supports_of_the_strata_of_13_11_14_5_and_16_17_against_hand_written_lists():
    hand = {
        (13, 5): ({(13, 0, 0), (0, 5, 4), (1, 6, 3), (2, 7, 2), (3, 8, 1), (4, 9, 0)},
                  {(0, 13, 0), (5, 0, 4), (6, 1, 3), (7, 2, 2), (8, 3, 1), (9, 4, 0)}),
        (14, 2): ({(14, 0, 0), (0, 2, 6), (1, 3, 5), (2, 4, 4), (3, 5, 3), (4, 6, 2), (5, 7, 1), (6, 8, 0)},
                  {(0, 14, 0), (2, 0, 6), (3, 1, 5), (4, 2, 4), (5, 3, 3), (6, 4, 2), (7, 5, 1), (8, 6, 0)}),
        (16, 8): ({(16, 0, 0), (0, 8, 4), (1, 9, 3), (2, 10, 2), (3, 11, 1), (4, 12, 0)},
                  {(0, 16, 0), (8, 0, 4), (9, 1, 3), (10, 2, 2), (11, 3, 1), (12, 4, 0)}),
    }
    for (e, t), (want_f, want_g) in hand.items():
        m, i, j = R.stratum(e, t)
        assert (m, i, j) == ((e + t) // 2, 0, (e - t) // 2)
        mons = A.monos(e)
        assert {mons[k] for k in R.X.support(e, m, i)} == want_f == _hand_support(e, t)[0]
        assert {mons[k] for k in R.X.support(e, m, j)} == want_g == _hand_support(e, t)[1]
    assert [R.stratum(e, t) for e, t in ((13, 5), (14, 2), (16, 8))] == [(9, 0, 4), (8, 0, 6), (12, 0, 4)]


CASES = {  # (e, p): the exponent of the plan
    (9, 11): 5, (11, 17): 7, (13, 17): 7,
    (13, 11): 5, (13, 7): 3, (14, 5): 2, (14, 11): 4,
    (15, 29): 13, (16, 29): 14, (16, 31): 14, (15, 23): 11, (15, 19): 9, (16, 23): 10, (15, 17): 7, (16, 17): 8, (16, 19): 8,
}


def test_the_exponent_of_each_case_by_the_rule_of_the_hypothesis():
    for (e, p), t in CASES.items():
        assert R.exponent_of_pair(e, p) == t, (e, p)
    # (9, 13) is a control with the exponent t = 3 fixed by the table of family K (the rule would give 5): the rule's own value
    assert R.exponent_of_pair(9, 13) == 5
    # (11, 3) is outside the family: 2t <= p - 1 leaves t = 1, and 3 divides (11 + 1)/2 = 6 with p <= e, so no exponent is left
    assert R.exponent_of_pair(11, 3) is None


def test_the_seed_and_the_order_of_the_members():
    e, p, t, bs = 9, 11, 5, 5000
    a1, b1 = R.sample_block(e, p, t, 4, 0, bs, bs)
    a2, b2 = R.sample_block(e, p, t, 4, 0, bs, bs)
    assert (a1 == a2).all() and (b1 == b2).all()
    assert a1.shape == (bs, 3) and a1.min() >= 0 and a1.max() < p
    a3, b3 = R.sample_block(e, p, t, 4, 0, 100, bs)  # the members of a block do not depend on how many of them a caller takes
    assert (a3 == a1[:100]).all() and (b3 == b1[:100]).all()
    a4, _ = R.sample_block(e, p, t, 4, 1, bs, bs)
    assert not (a4 == a1).all()
    a5, _ = R.sample_block(e, p, t, 5, 0, bs, bs)
    assert not (a5 == a1).all()
    assert R.case_seed(4) == 20261120 + 4
    ref = np_rng(4, 0, bs, 3, p)
    keep = ref[0].any(axis=1)  # the rows of a zero alpha are drawn again, every other row is the documented draw
    assert (a1[keep] == ref[0][keep]).all() and (b1 == ref[1]).all()  # default_rng([seed, block]): alpha first, then beta
    assert (~keep).sum() < 20
    assert a1.any(axis=1).all()  # alpha is never zero


def np_rng(seed_index, block, n, width, p):
    import numpy as np
    rng = np.random.default_rng([20261120 + seed_index, block])
    return (rng.integers(0, p, size=(n, width), dtype=np.int64), rng.integers(0, p, size=(n, width), dtype=np.int64))


def test_a_zero_alpha_is_drawn_again():
    a, _ = R.sample_block(5, 3, 3, 0, 0, 65536, 65536)  # d = 1, p = 3: alpha has 9 values, one of them zero
    assert a.any(axis=1).all()


def test_the_staged_hilbert_test_on_stored_pure_members_and_on_a_failing_member():
    import json
    res = json.loads((EXP19.parent / "EXP-018-largest-exponent-strata" / "artifacts" / "results.json").read_text(encoding="utf-8"))
    n = 0
    for st in res["strata"].values():
        e, p, m, i, j = st["e"], st["p"], st["m"], st["i"], st["j"]
        if (e, p) == (9, 11) and i == 0 and m + j == e and m - j == 5:
            for mem in [x for x in st["members"] if x.get("pure") is True][:3]:
                assert R.hilbert_pure(e, p, 5, mem["f"], mem["g"])
                n += 1
    assert n == 3
    f, g = R.pair_vectors(9, 11, 5, [1, 2, 3], [1, 0, 0])  # a generic member: not the pure Hilbert function
    assert not R.hilbert_pure(9, 11, 5, f, g)


def test_block_job_counts_are_ordered_and_its_members_have_the_pure_hilbert_function():
    spec = {"e": 9, "p": 11, "t": 5, "seed_index": 0, "block": 0, "count": 20000, "block_size": 20000}
    out = R.block_job(spec)
    c = out["counts"]
    assert c["examined"] == 20000
    assert c["f0"] >= c["f1"] >= c["f2"] >= c["f3"] >= c["pure_hilbert"] > 0
    assert len(out["found"]) == c["pure_hilbert"]
    assert [m["index"] for m in out["found"]] == sorted(m["index"] for m in out["found"])
    for m in out["found"]:
        assert R.filter_t(9, 11, 5, m["alpha"], m["beta"])[0] == 4
        assert R.alpha_beta_of_pair(9, 11, 5, m["f"], m["g"]) == (m["alpha"], m["beta"])
        assert R.hilbert_pure(9, 11, 5, m["f"], m["g"])
    again = R.block_job(spec)
    assert again["counts"] == c and again["found"] == out["found"]
    half = R.block_job(dict(spec, count=10000))  # a smaller count examines the first members of the same block
    assert [m["index"] for m in half["found"]] == [m["index"] for m in out["found"] if m["index"] < 10000]


def _load_run():
    spec = importlib.util.spec_from_file_location("exp019_run", EXP19 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp019_run"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_the_plan_of_the_cases_follows_the_hypothesis():
    run = _load_run()
    assert [(c["e"], c["p"], c["t"], c["budget"]) for c in run.plan("K")] == [
        (9, 11, 5, 100_000), (9, 13, 3, 2_000_000), (11, 17, 7, 100_000), (13, 17, 7, 5_000_000)]
    assert [(c["e"], c["p"], c["t"], c["budget"]) for c in run.plan("X")] == [
        (13, 11, 5, 300_000_000), (13, 7, 3, 1_000_000_000), (14, 5, 2, 1_500_000_000), (14, 11, 4, 3_000_000_000)]
    assert [(c["e"], c["p"], c["t"], c["budget"]) for c in run.plan("Y")] == [
        (15, 29, 13, 200_000), (16, 29, 14, 200_000), (16, 31, 14, 200_000), (15, 23, 11, 1_000_000), (15, 19, 9, 50_000_000),
        (16, 23, 10, 50_000_000), (15, 17, 7, 1_500_000_000), (16, 17, 8, 1_500_000_000), (16, 19, 8, 2_000_000_000)]
    allc = [c for fam in "KXY" for c in run.plan(fam)]
    assert [c["seed"] for c in allc] == [20261120 + k for k in range(17)]
    assert [c["seed_index"] for c in run.plan("Y")] == list(range(8, 17))
    assert run.plan("Y", {(16, 17)})[0]["key"] == "Y|16|17"
    for c in allc:
        assert c["d"] == (c["e"] - c["t"]) // 2 and c["stratum"] == list(R.stratum(c["e"], c["t"]))
        if (c["e"], c["p"]) != (9, 13):
            assert c["t"] == R.exponent_of_pair(c["e"], c["p"])
        assert c["blocks"] == -(-c["budget"] // c["block_size"])
    assert [c["key"] for c in run.order()] == [
        "K|9|11", "K|9|13", "K|11|17", "K|13|17", "Y|15|29", "Y|16|29", "Y|16|31", "Y|15|23", "Y|15|19", "Y|16|23", "X|13|11",
        "X|13|7", "X|14|5", "Y|15|17", "Y|16|17", "Y|16|19", "X|14|11"]


def test_g1_a_the_filter_on_every_stored_member_with_a_table():
    rec = R.stored_members_record()
    assert rec["not_of_the_form"] == 0
    assert rec["pure_by_stage"][:4] == [0, 0, 0, 0]  # every pure member passes (F0) to (F3)
    assert rec["other_by_stage"][4] == 0  # no member with another table passes
    assert (rec["pure"], rec["other"]) == (317, 128), (rec["pure"], rec["other"])  # the counts of the probe
    assert rec["other_by_stage"] == [108, 0, 0, 20, 0]
    assert rec["ok"] is True
