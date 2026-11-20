"""Gate G3 of EXP-017 (boij-soderberg-realizability): the conversion between (alpha, beta) and the pair (f, g) against products computed with
the structure constants of `uhlib` on random members at e = 5; the filter on the 59 stored pure members and on ten stored members that fail
it; (F1) and (F2) by linear algebra against a brute-force search of c on every member of (e, p) = (5, 3) and on random members of (5, 5)
and (5, 7); the block test of (F1) against the exact one on 20,000 random members at (7, 5) and (9, 7); the seed and the order of the
members; the staged test of the pure Hilbert function; the plan of the cases."""
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path

import numpy as np

EXP17 = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
         / "EXP-017-odd-stratum-filter")
EXPS = EXP17.parent
sys.path.insert(0, str(EXP17))

import exp017_routine as R  # noqa: E402
from uhlib import algebra as A  # noqa: E402

STORED = {"EXP-010-weight-class-strata": ["C|5|5|3|0|2", "C|5|7|3|0|2", "C|7|11|4|0|3", "Q|7|3|4|0|3", "Q|7|5|4|0|3", "Q|7|7|4|0|3"],
          "EXP-014-middle-strata": ["K|5|7|3|0|2", "K|7|5|4|0|3", "K|7|11|4|0|3", "W|9|7|5|0|4"]}


def _stored():
    """(e, p, member) for every stored member of the strata of the 59 pure members, with the stored pure flag."""
    out = []
    for name, keys in STORED.items():
        res = json.loads((EXPS / name / "artifacts" / "results.json").read_text(encoding="utf-8"))
        for k in keys:
            st = res["strata"][k]
            out += [(st["e"], st["p"], mem) for mem in st["members"]]
    return out


def _mul(u, v, p):
    out = {}
    for m1, c1 in u.items():
        for m2, c2 in v.items():
            for mm, c in A.mono_mul(m1, m2):
                out[mm] = (out.get(mm, 0) + c1 * c2 * c) % p
    return {m: c for m, c in out.items() if c}


def _product_pair(e, p, alpha, beta):
    """f = x^e + alpha(xy, z) y and g = y^e + beta(xy, z) x, computed by multiplying out in U(H) with `mono_mul` (h = xy, z central)."""
    s = (e - 1) // 2
    h = {(1, 1, 0): 1}
    pw = [{(0, 0, 0): 1}]
    for _ in range(s):
        pw.append(_mul(pw[-1], h, p))

    def form(coefs):
        tot = {}
        for k, c in enumerate(coefs):
            for mm, v in _mul(pw[k], {(0, 0, s - k): c % p}, p).items():
                tot[mm] = (tot.get(mm, 0) + v) % p
        return tot

    f = _mul(form(alpha), {(0, 1, 0): 1}, p)
    g = _mul(form(beta), {(1, 0, 0): 1}, p)
    f[(e, 0, 0)] = (f.get((e, 0, 0), 0) + 1) % p
    g[(0, e, 0)] = (g.get((0, e, 0), 0) + 1) % p
    return {m: c for m, c in f.items() if c}, {m: c for m, c in g.items() if c}


def _as_dict(e, v):
    return {m: int(c) for m, c in zip(A.monos(e), v) if int(c)}


def test_conversion_against_products_in_u_on_random_members_at_e5():
    rng = random.Random(5)
    for p in (3, 5, 7, 11, 13):
        for _ in range(40):
            alpha = [rng.randrange(p) for _ in range(3)]
            beta = [rng.randrange(p) for _ in range(3)]
            f, g = R.pair_vectors(5, p, alpha, beta)
            pf, pg = _product_pair(5, p, alpha, beta)
            assert _as_dict(5, f) == pf, (p, alpha, beta)
            assert _as_dict(5, g) == pg, (p, alpha, beta)


def test_conversion_at_e7_and_e9_against_products_and_round_trip():
    rng = random.Random(7)
    for e, p in ((7, 5), (7, 11), (9, 7), (9, 13)):
        s = (e - 1) // 2
        for _ in range(15):
            alpha = [rng.randrange(p) for _ in range(s + 1)]
            beta = [rng.randrange(p) for _ in range(s + 1)]
            f, g = R.pair_vectors(e, p, alpha, beta)
            pf, pg = _product_pair(e, p, alpha, beta)
            assert _as_dict(e, f) == pf and _as_dict(e, g) == pg
            assert R.alpha_beta_of_pair(e, p, f, g) == (alpha, beta)
            # a stored pair is rescaled by 1/c0, 1/c1: a scalar multiple of f and of g gives the same member
            assert R.alpha_beta_of_pair(e, p, [3 * c % p for c in f], [2 * c % p for c in g]) == (alpha, beta)


def test_a_pair_outside_the_chart_has_no_member():
    e, p = 5, 7
    f, g = R.pair_vectors(e, p, [1, 2, 3], [1, 1, 1])
    f2 = list(f)
    f2[A.monos(e).index((2, 1, 1))] = 4  # a monomial x^2 y z is not of the form x^a y^(a+1) z^(s-a)
    assert R.alpha_beta_of_pair(e, p, f2, g) is None
    f3 = list(f)
    f3[A.monos(e).index((e, 0, 0))] = 0
    assert R.alpha_beta_of_pair(e, p, f3, g) is None


def test_the_filter_accepts_the_59_stored_pure_members():
    pure = [(e, p, m) for e, p, m in _stored() if m.get("pure") is True]
    assert len(pure) == 59
    for e, p, m in pure:
        ab = R.alpha_beta_of_pair(e, p, m["f"], m["g"])
        assert ab is not None
        stage, c, cp = R.filter_member(e, p, *ab)
        assert stage == 4 and c is not None and cp is not None, (e, p, m["index"], stage)


def test_the_filter_rejects_ten_stored_members_that_are_not_pure():
    bad, seen = [], set()
    for e, p, m in _stored():
        ident = (e, p, tuple(m["f"]), tuple(m["g"]))
        if m.get("pure") is False and ident not in seen:
            seen.add(ident)
            bad.append((e, p, m))
    assert len(bad) >= 10
    stages = []
    for e, p, m in bad[:10]:
        ab = R.alpha_beta_of_pair(e, p, m["f"], m["g"])
        stages.append("nochart" if ab is None else R.filter_member(e, p, *ab)[0])
    assert all(isinstance(s, int) and s < 4 for s in stages), stages
    assert {s for s in stages if isinstance(s, int)}  # at least one is a member of the chart that the filter rejects


def _all_polys(p, n):
    return itertools.product(range(p), repeat=n)


def _brute(e, p, alpha, beta):
    """The filter by brute force: (F0) by greatest common divisors, then a search of c and of c' among all polynomials of degree <= s."""
    s = (e - 1) // 2
    P = R.P_
    h = P(p, [0, 1])
    ae = R.a_poly(p, e - 1)
    al, be = P(p, alpha), P(p, beta)
    bs = be(P(p, [(e - 1) % p, 1]))
    delta = al * bs - ae
    if delta.degree() != 2 * s:
        return 0, None, None
    x = (h - 2) * delta(P(p, [-(e + 1) % p, 1]))
    xp = (h + e) * delta(P(p, [(e + 1) % p, 1]))
    if delta.gcd(x).degree() > 0 or delta.gcd(xp).degree() > 0:
        return 0, None, None
    c = next((list(cs) for cs in _all_polys(p, s + 1) if (P(p, cs) * x - xp * al) % delta == 0), None)
    if c is None:
        return 1, None, None
    cp = next((list(cs) for cs in _all_polys(p, s + 1) if (P(p, cs) * xp - x * bs) % delta == 0), None)
    if cp is None:
        return 2, c, None
    return (3 if (P(p, c) * P(p, cp) - ae).degree() < 0 else 4), c, cp


def _agree(e, p, alpha, beta):
    got = R.filter_member(e, p, alpha, beta)
    want = _brute(e, p, alpha, beta)
    assert got == want, (e, p, alpha, beta, got, want)
    return got[0]


def test_f1_by_linear_algebra_equals_brute_force_on_every_member_at_5_3():
    stages = [_agree(5, 3, list(a), list(b)) for a in _all_polys(3, 3) for b in _all_polys(3, 3)]
    assert len(stages) == 729


def test_f1_and_f2_by_linear_algebra_equal_brute_force_on_random_members_at_5_5_and_5_7():
    rng = random.Random(55)
    seen = []
    for p, n in ((5, 250), (7, 250)):
        for _ in range(n):
            seen.append(_agree(5, p, [rng.randrange(p) for _ in range(3)], [rng.randrange(p) for _ in range(3)]))
    assert sum(1 for s in seen if s >= 2) > 5  # the comparison is not empty: members pass (F1) and some pass (F2)
    assert sum(1 for s in seen if s >= 3) > 0


def _block_vs_exact(e, p, n, seed_index):
    alpha, beta = R.sample_block(e, p, seed_index, 0, n)
    mask = R.BlockF1(e, p).passes(alpha, beta)
    stage = np.array([R.filter_member(e, p, [int(v) for v in alpha[k]], [int(v) for v in beta[k]])[0] for k in range(n)])
    exact = stage >= 2
    assert not (exact & ~mask).any(), "the block test rejected a member that the exact test accepts"
    assert (stage[mask & ~exact] == 0).all(), "a member accepted by the block test and not by the exact one must fail (F0)"
    assert exact.sum() > 0
    return int(mask.sum()), int(exact.sum())


def test_block_f1_against_the_exact_test_on_20000_members_at_7_5():
    blk, ex = _block_vs_exact(7, 5, 20000, 1)
    assert blk >= ex


def test_block_f1_against_the_exact_test_on_20000_members_at_9_7():
    blk, ex = _block_vs_exact(9, 7, 20000, 3)
    assert blk >= ex


def test_block_f1_agrees_with_the_exact_test_for_int64_and_int32_and_at_the_stored_pure_members():
    e, p = 7, 5
    alpha, beta = R.sample_block(e, p, 1, 0, 3000)
    m32 = R.BlockF1(e, p, np.int32).passes(alpha, beta)
    m64 = R.BlockF1(e, p, np.int64).passes(alpha, beta)
    assert (m32 == m64).all()
    pure = [(e2, p2, m) for e2, p2, m in _stored() if m.get("pure") is True]
    for (e2, p2, m) in pure:
        a, b = R.alpha_beta_of_pair(e2, p2, m["f"], m["g"])
        assert bool(R.BlockF1(e2, p2).passes(np.array([a]), np.array([b]))[0]), (e2, p2, m["index"])


def test_the_seed_and_the_order_of_the_members():
    e, p = 9, 11
    a1, b1 = R.sample_block(e, p, 4, 0)
    a2, b2 = R.sample_block(e, p, 4, 0)
    assert (a1 == a2).all() and (b1 == b2).all()
    assert a1.shape == (R.BLOCK, 5) and a1.min() >= 0 and a1.max() < p
    a3, b3 = R.sample_block(e, p, 4, 0, 100)  # the members of a block do not depend on how many of them a caller takes
    assert (a3 == a1[:100]).all() and (b3 == b1[:100]).all()
    a4, _ = R.sample_block(e, p, 4, 1)
    assert not (a4 == a1).all()
    a5, _ = R.sample_block(e, p, 5, 0)
    assert not (a5 == a1).all()
    assert R.case_seed(4) == 20261120 + 4
    ref = np.random.default_rng([20261120 + 4, 0]).integers(0, p, size=(R.BLOCK, 5), dtype=np.int64)
    assert (a1 == ref).all()  # the documented generator: default_rng([seed, block]), alpha first, then beta
    assert a1.any(axis=1).all()  # alpha is never zero


def test_a_zero_alpha_is_drawn_again():
    a, _ = R.sample_block(5, 3, 0, 0)  # p^3 = 27 forms of alpha: about 2,400 of the 65,536 draws are zero before the second draw
    assert a.any(axis=1).all()


def test_the_staged_hilbert_test_on_stored_pure_members_and_on_a_failing_member():
    pure = [(e, p, m) for e, p, m in _stored() if m.get("pure") is True and (e, p) in ((5, 7), (7, 5), (9, 7))]
    assert {(e, p) for e, p, _ in pure} == {(5, 7), (7, 5), (9, 7)}
    done = set()
    for e, p, m in pure:
        if (e, p) not in done:
            done.add((e, p))
            assert R.hilbert_pure(e, p, m["f"], m["g"])
    f, g = R.pair_vectors(7, 5, [1, 2, 3, 4], [1, 0, 0, 0])  # a generic member: not the pure Hilbert function
    assert not R.hilbert_pure(7, 5, f, g)


def test_block_job_counts_are_ordered_and_its_members_have_the_pure_hilbert_function():
    spec = {"e": 5, "p": 7, "seed_index": 0, "block": 0, "count": 20000}
    out = R.block_job(spec)
    c = out["counts"]
    assert c["examined"] == 20000 and c["inconsistent"] == 0
    assert c["block_f1"] >= c["f0"] >= c["f1"] >= c["f2"] >= c["f3"] >= c["pure_hilbert"] > 0
    assert len(out["found"]) == c["pure_hilbert"]
    assert [m["index"] for m in out["found"]] == sorted(m["index"] for m in out["found"])
    for m in out["found"]:
        assert R.filter_member(5, 7, m["alpha"], m["beta"])[0] == 4
        assert R.hilbert_pure(5, 7, m["f"], m["g"])
    again = R.block_job(spec)
    assert again["counts"] == c and again["found"] == out["found"]


def _load_run():
    spec = importlib.util.spec_from_file_location("exp017_run", EXP17 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp017_run"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_the_plan_of_the_cases_follows_the_hypothesis():
    run = _load_run()
    assert [(c["e"], c["p"], c["budget"]) for c in run.plan("K")] == [(5, 7, 200_000), (7, 5, 2_000_000), (7, 11, 20_000_000),
                                                                      (9, 7, 60_000_000)]
    assert [(c["e"], c["p"], c["budget"]) for c in run.plan("Q")] == [(9, 11, 200_000_000), (9, 13, 400_000_000)]
    assert [(c["e"], c["p"], c["budget"]) for c in run.plan("X")] == [(11, 7, 300_000_000), (13, 5, 200_000_000)]
    seeds = [c["seed"] for fam in "KQX" for c in run.plan(fam)]
    assert seeds == [20261120 + k for k in range(8)]
    assert run.plan("Q", {(9, 13)})[0]["key"] == "Q|9|13"
    assert run.FIXED["e"] == 9 and run.FIXED["p"] == 7


def test_the_fixed_member_of_g1_passes_the_filter():
    run = _load_run()
    out = run.fixed_member()
    assert out["filter_stage"] == 4 and out["ok"] is True, out


def test_the_record_of_the_filter_on_the_stored_members_with_a_table():
    spec = importlib.util.spec_from_file_location("exp017_stored_members", EXP17 / "stored_members.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = json.loads(json.dumps(mod.compute()))
    assert data == json.loads(mod.OUT.read_text(encoding="utf-8"))
    tot = data["totals"]
    assert (tot["tabled"], tot["pure"], tot["other"], tot["not_of_the_form"]) == (130, 59, 71, 0)
    assert tot["pure_by_stage"] == [0, 0, 0, 0, 59]
    assert tot["other_by_stage"] == [65, 0, 0, 6, 0]
    assert [tuple(q) for q in data["pairs"]] == [(5, 5), (5, 7), (7, 3), (7, 5), (7, 7), (7, 11), (7, 13), (9, 7)]
