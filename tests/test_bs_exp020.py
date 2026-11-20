"""Gate G3 of EXP-020 (boij-soderberg-realizability): the formula beta = c alpha^omega against the automorphism omega of U computed with the
structure constants of `uhlib` (random alpha at (e, t) = (6, 2) and (7, 3)); the enumeration at (8, 7) (order, index, number of members, the
least non-residue); the complete counts at (8, 7) with t = 2 (4,800 members, 0 where (F1) and (F2) differ, 28 passing, 18 with (C1)); the
stage against the filter of EXP-019 on 2,000 members; the exponent of each case; the plan of the cases."""
import importlib.util
import itertools
import random
import sys
from pathlib import Path

EXP20 = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
         / "EXP-020-symmetric-members")
sys.path.insert(0, str(EXP20))

import exp020_routine as R  # noqa: E402
from uhlib import algebra as A  # noqa: E402

R19 = R.R19


def _mul(u, v, p):
    out = {}
    for m1, c1 in u.items():
        for m2, c2 in v.items():
            for mm, c in A.mono_mul(m1, m2):
                out[mm] = (out.get(mm, 0) + c1 * c2 * c) % p
    return {m: c for m, c in out.items() if c}


def _product_pair(e, p, t, alpha, beta):
    """f = x^e + alpha(xy, z) y^t and g = y^e + beta(xy, z) x^t multiplied out in U(H) with `mono_mul` (h = xy, z central)."""
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


def _omega_image(f, p):
    """The image of f under the substitution x -> y, y -> x, z -> -z, a product of the images of the factors in the order x^a y^b z^c
    -> y^a x^b (-z)^c, reordered to PBW monomials with the structure constants of `uhlib`."""
    out = {}
    for (a, b, c), v in f.items():
        term = _mul({(0, a, 0): 1}, {(b, 0, 0): 1}, p)
        term = _mul(term, {(0, 0, c): (-1) ** c % p}, p)
        for mm, w in term.items():
            out[mm] = (out.get(mm, 0) + v * w) % p
    return {m: c for m, c in out.items() if c}


def test_beta_is_c_alpha_omega_against_the_exchange_of_x_and_y_computed_in_u_at_6_2_and_7_3():
    rng = random.Random(20)
    for e, t in ((6, 2), (7, 3)):
        d = (e - t) // 2
        for p in (5, 7, 11, 13):
            for _ in range(15):
                alpha = [rng.randrange(p) for _ in range(d + 1)]
                if not any(alpha):
                    continue
                beta = R.beta_of(p, d, alpha, 1)
                f, g = _product_pair(e, p, t, alpha, beta)
                assert _omega_image(f, p) == g, (e, t, p, alpha, beta)
                # the stored conversion gives the same pair, and omega is an involution on this family up to the sign of z
                fv, gv = R19.pair_vectors(e, p, t, alpha, beta)
                assert {m: int(c) for m, c in zip(A.monos(e), gv) if int(c)} == g
                c = rng.randrange(1, p)
                assert R.beta_of(p, d, alpha, c) == [c * b % p for b in beta]


def test_beta_of_agrees_with_the_polynomial_formula_of_the_hypothesis():
    rng = random.Random(21)
    for p, d in ((7, 3), (11, 5), (17, 4), (19, 4)):
        for _ in range(30):
            alpha = [rng.randrange(p) for _ in range(d + 1)]
            c = rng.choice([1, R.least_nonresidue(p)])
            hm1 = R19.P_(p, [-1, 1])
            want = R19.P_(p, [0])
            for i, a in enumerate(alpha):
                want = want + (hm1 ** i) * (a * (-1) ** (d - i) * c)
            assert R.beta_of(p, d, alpha, c) == R19.coeffs(want, d + 1)
        al = [[rng.randrange(p) for _ in range(d + 1)] for _ in range(20)]
        arr = R.np.array(al, dtype=R.np.int64)
        assert R.betas(p, d, arr, 3).tolist() == [R.beta_of(p, d, a, 3) for a in al]


def test_the_least_non_residue():
    assert [R.least_nonresidue(p) for p in (7, 11, 13, 17, 19)] == [3, 2, 2, 3, 2]


def test_the_enumeration_at_8_7_order_index_and_number_of_members():
    p, d = 7, 3
    assert R.n_members(p, d) == 2 * (7 ** 4 - 1) == 4800
    alphas = [list(v) for v in itertools.product(range(p), repeat=d + 1) if any(v)]
    assert len(alphas) == 2400
    assert alphas == sorted(alphas)  # the lexicographic order, the last coefficient fastest
    for rank in (0, 1, 2, 6, 7, 48, 342, 343, 2398, 2399):
        assert R.alpha_of_rank(p, d, rank) == alphas[rank]
        assert R.rank_of_alpha(p, d, alphas[rank]) == rank
    assert R.alpha_of_rank(p, d, 0) == [0, 0, 0, 1] and R.alpha_of_rank(p, d, 2399) == [6, 6, 6, 6]
    assert R.np.array_equal(R.alpha_block(p, d, 100, 140), R.np.array(alphas[100:140]))
    nu = R.least_nonresidue(p)
    assert nu == 3
    for rank in (0, 5, 2399):
        for flag in (0, 1):
            idx = 2 * rank + flag
            assert R.index_of(p, d, alphas[rank], flag) == idx
            alpha, scalar, beta = R.member_of_index(p, d, idx)
            assert alpha == alphas[rank] and scalar == (1, nu)[flag] and beta == R.beta_of(p, d, alpha, scalar)
    assert R.member_of_index(p, d, 4799)[0] == [6, 6, 6, 6]


def test_the_complete_counts_at_8_7_with_t_2():
    e, p, t = 8, 7, 2
    out = R.block_job({"e": e, "p": p, "t": t, "r0": 0, "r1": 2400})
    cnt = out["counts"]
    assert cnt["examined"] == 4800 == R.n_members(p, (e - t) // 2)
    assert cnt["differ"] == 0
    assert sum(out["stage_counts"]) == 4800 and out["stage_counts"][4] == 28
    assert out["stage_counts"] == [2762, 1982, 0, 28, 28]  # the log of the probe of the coordinating session
    assert cnt["f3"] == 28 and cnt["c1"] == 18
    assert [m["index"] for m in out["passing"]] == sorted(m["index"] for m in out["passing"])
    assert sum(1 for m in out["passing"] if m["c1"]) == 18
    assert all(R19.filter_t(e, p, t, m["alpha"], m["beta"])[0] == 4 for m in out["passing"])
    # the blocks of ranks add up to the whole, whatever the split
    parts = [R.block_job({"e": e, "p": p, "t": t, "r0": a, "r1": b}) for a, b in ((0, 7), (7, 1000), (1000, 2400))]
    assert [sum(x["stage_counts"][k] for x in parts) for k in range(5)] == out["stage_counts"]
    assert [m["index"] for x in parts for m in x["passing"]] == [m["index"] for m in out["passing"]]
    assert sum(x["counts"]["differ"] for x in parts) == 0


def test_the_stage_equals_the_stage_of_the_filter_of_exp019_on_2000_members():
    rng = random.Random(22)
    for e, p, t, n in ((8, 7, 2, 800), (9, 13, 3, 600), (11, 17, 7, 600)):
        d = (e - t) // 2
        ctx = R.case_context(e, p, t)
        total = p ** (d + 1) - 1
        nu = R.least_nonresidue(p)
        for _ in range(n):
            alpha = R.alpha_of_rank(p, d, rng.randrange(total))
            scalar = rng.choice([1, nu])
            beta = R.beta_of(p, d, alpha, scalar)
            st, f1, f2, c, cp, c1 = R.member_detail(ctx, alpha, beta)
            want = R19.filter_t(e, p, t, alpha, beta)
            assert st == want[0], (e, p, alpha, scalar)
            assert (c, cp) == (want[1], want[2])
            if st >= 1:
                assert f1 == (st >= 2)  # (F1) holds exactly when the stage is at least 2
            if st >= 2:
                assert f2 == (st >= 3)
            if st == 4:
                ae = R19.a_poly(p, e - t)
                delta = R19.P_(p, alpha) * R19.P_(p, beta)(R19.P_(p, [(e - t) % p, 1])) - ae
                assert c1 == (delta.gcd(ae).degree() == 0)


def test_f1_and_f2_are_reported_separately_when_f1_fails():
    e, p, t = 8, 7, 2
    ctx = R.case_context(e, p, t)
    seen = 0
    for rank in range(0, 2400, 3):
        alpha = R.alpha_of_rank(p, 3, rank)
        for scalar in (1, 3):
            st, f1, f2, *_ = R.member_detail(ctx, alpha, R.beta_of(p, 3, alpha, scalar))
            if st == 1:
                assert f1 is False and f2 is False  # at (8, 7) (F2) fails together with (F1) (prediction P2 on a settled pair)
                seen += 1
    assert seen > 100


def test_the_exponent_of_each_case():
    for (e, p), t in {(11, 17): 7, (13, 11): 5, (14, 11): 4, (15, 11): 5, (15, 13): 5, (15, 17): 7, (16, 17): 8, (16, 19): 8}.items():
        assert R19.exponent_of_pair(e, p) == t, (e, p)
    assert R19.exponent_of_pair(9, 13) == 5  # the control (9, 13) uses t = 3 fixed by the table of the hypothesis, not the rule


def _load_run():
    spec = importlib.util.spec_from_file_location("exp020_run", EXP20 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp020_run"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_the_plan_of_the_cases_follows_the_hypothesis():
    run = _load_run()
    assert [(c["e"], c["p"], c["t"], c["d"], c["members"]) for c in run.plan("K")] == [
        (9, 13, 3, 3, 57_120), (11, 17, 7, 2, 9_824), (13, 11, 5, 4, 322_100)]
    assert [(c["e"], c["p"], c["t"], c["d"], c["members"], tuple(c["stratum"])) for c in run.plan("X")] == [
        (14, 11, 4, 5, 3_543_120, (9, 0, 5)), (15, 11, 5, 5, 3_543_120, (10, 0, 5)), (15, 13, 5, 5, 9_653_616, (10, 0, 5)),
        (15, 17, 7, 4, 2_839_712, (11, 0, 4)), (16, 17, 8, 4, 2_839_712, (12, 0, 4)), (16, 19, 8, 4, 4_952_196, (12, 0, 4))]
    allc = [c for fam in "KX" for c in run.plan(fam)]
    for c in allc:
        assert c["members"] == 2 * (c["p"] ** (c["d"] + 1) - 1)
        assert c["d"] == (c["e"] - c["t"]) // 2 and c["stratum"] == list(R19.stratum(c["e"], c["t"]))
        assert c["nu"] == R.least_nonresidue(c["p"])
        assert c["blocks"] == -(-(c["members"] // 2) // c["block_ranks"])
        if (c["e"], c["p"]) != (9, 13):
            assert c["t"] == R19.exponent_of_pair(c["e"], c["p"])
    assert [c["key"] for c in run.order()] == ["K|9|13", "K|11|17", "K|13|11", "X|14|11", "X|15|11", "X|15|13", "X|15|17", "X|16|17",
                                               "X|16|19"]
    assert run.plan("X", {(16, 17)})[0]["key"] == "X|16|17"
    assert sum(c["members"] for c in run.plan("X")) == 27_371_476


def test_the_betti_job_gives_the_table_and_the_length_e_cubed_of_a_passing_member_and_not_pure_for_a_generic_pair():
    out = R.block_job({"e": 9, "p": 13, "t": 3, "r0": 0, "r1": 400})
    assert out["passing"], "the first 400 ranks of (9, 13) hold passing members (the probe lists member 41)"
    m = out["passing"][0]
    res = R.betti_job({"key": "t", "index": m["index"], "e": 9, "p": 13, "f": m["f"], "g": m["g"]})
    assert res["betti"] == [[0, 0, 1], [1, 9, 2], [2, 27, 2], [3, 36, 1]]
    assert res["length"] == 9 ** 3 and res["pure"] is True
    f, g = R.pair_vectors(9, 13, 3, [1, 2, 3, 4], [1, 0, 5, 7])  # a pair outside the filter: not a pure table of length e^3
    bad = R.betti_job({"key": "t", "index": 0, "e": 9, "p": 13, "f": f, "g": g})
    assert bad["pure"] is False
