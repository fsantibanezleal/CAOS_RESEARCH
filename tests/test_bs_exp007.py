"""Gate G4 of EXP-007 (boij-soderberg-realizability): the chart and the matrix B(f, g) against a direct product in `uhlib`, the
routine of G2 (the tangent routine with the chart replaced by all matrices), the orbit test, h_e and r, the exactness of the
ranks over the rationals, the seeded draws and the tangent space at W_0."""
import random
import sys
from fractions import Fraction
from pathlib import Path

EXP = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
       / "experiments" / "EXP-007-pure-family-at-the-power-pair")
sys.path.insert(0, str(EXP))

import exp007_routine as R  # noqa: E402
import exp007_singular as Sg  # noqa: E402
from flint import fmpz_mat  # noqa: E402
from uhlib import algebra as A  # noqa: E402

QQ = R.make_field("QQ")
GF = R.make_field("GF(32003)")


def test_formula_h_e_and_r():
    assert [R.u(n) for n in range(17)] == [1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36, 42, 49, 56, 64, 72, 81]
    typed_r = {4: 48, 5: 70, 6: 96, 7: 126}
    typed_h3e = {4: 1, 5: 2, 6: 4, 7: 6}
    for e in (4, 5, 6, 7):
        assert R.target_rank(e) == typed_r[e] == 2 * R.u(2 * e) - 2
        assert R.h_e(e, 3 * e) == typed_h3e[e]
    typed = [1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 2, 1]
    assert [R.h_e(4, n) for n in range(13)] == typed and sum(typed) == 64


def _direct_mu_rows(F, W, e, n):
    """Rows u * w by uhlib's product (poly_mul with the monomial u on the left), ordered (w, u), on the PBW basis of U_n."""
    pos = {m: i for i, m in enumerate(A.monos(n))}
    rows = []
    for w in W:
        for m in A.monos(n - e):
            pr = A.poly_mul(F, {m: F.one}, w)
            row = [F.zero] * A.dim_U(n)
            for mm, c in pr.items():
                row[pos[mm]] = c
            rows.append(row)
    return rows


def _rows_of(M):
    return [[int(M[i, j]) for j in range(M.ncols())] for i in range(M.nrows())]


def test_chart_and_B_against_direct_product_in_uhlib():
    for e in (4, 5):
        coords = R.chart_coordinates(e)
        assert len(coords) == 2 * (R.u(e) - 2)
        assert all(m not in ((e, 0, 0), (0, e, 0)) for _, m in coords)
        for seed in (1, 2, 3):
            rng = random.Random(seed)
            fcoef = {m: rng.randrange(GF.p) for i, m in coords if i == 0}
            gcoef = {m: rng.randrange(GF.p) for i, m in coords if i == 1}
            w0 = [{(e, 0, 0): 1}, {(0, e, 0): 1}]
            w1 = [dict(w0[0]), dict(w0[1])]
            for m, c in fcoef.items():
                w1[0][m] = c
            for m, c in gcoef.items():
                w1[1][m] = c
            direct1 = _direct_mu_rows(GF, w1, e, 3 * e)
            direct0 = _direct_mu_rows(GF, w0, e, 3 * e)
            # B(f, g) = sum of the coordinates times the chart matrices, entrywise modulo p
            tot = [[0] * A.dim_U(3 * e) for _ in range(len(direct0))]
            for i, m in coords:
                c = (fcoef if i == 0 else gcoef)[m]
                B = _rows_of(R.chart_matrix(GF, e, i, m))
                for r_ in range(len(tot)):
                    for c_ in range(len(tot[0])):
                        tot[r_][c_] = (tot[r_][c_] + c * B[r_][c_]) % GF.p
            diff = [[(direct1[r_][c_] - direct0[r_][c_]) % GF.p for c_ in range(len(tot[0]))] for r_ in range(len(tot))]
            assert diff == tot
            # and the routine's matrix of mu_3e(W) is the direct one
            C1 = R.space_from_polys(GF, e, w1)
            assert _rows_of(R.mu_matrix(GF, C1, e, 3 * e)) == [[x % GF.p for x in r_] for r_ in direct1]


def test_left_multiplication_is_noncommutative():
    # y * x = x * y - z, so the left multiple y * (x) differs from x * y: the coordinates of y * x^e contain the z term
    pr = A.poly_mul_int({(0, 1, 0): 1}, {(1, 0, 0): 1})
    assert pr == {(1, 1, 0): 1, (0, 0, 1): -1}
    assert A.poly_mul_int({(1, 0, 0): 1}, {(0, 1, 0): 1}) == {(1, 1, 0): 1}


def test_routine_of_G2_known_dimensions():
    for F in (QQ, GF):
        rows = R.random_rank_matrix(F, 3, 4, 2, seed=11)
        d = R.tangent_all_matrices(F, rows, 4)
        assert (d["rank_A"], d["dim_K"], d["coker_dim"], d["rank_T"], d["tangent_dim"]) == (2, 1, 2, 2, 10)
        rows = R.random_rank_matrix(F, 2, 2, 1, seed=12)
        d = R.tangent_all_matrices(F, rows, 2)
        assert (d["rank_A"], d["dim_K"], d["coker_dim"], d["rank_T"], d["tangent_dim"]) == (1, 1, 1, 1, 3)


def test_ranks_over_QQ_are_exact_not_modulo_a_prime():
    assert R.mat_rank(fmpz_mat(2, 2, [13, 0, 0, 1])) == 2  # rank 2 over QQ, rank 1 modulo 13
    assert R.mat_rank(R.to_matrix(R.make_field("GF(13)"), [[13, 0], [0, 1]], 2)) == 1
    F = QQ
    rows = [[Fraction(1, 2), Fraction(1, 3)], [Fraction(1), Fraction(2, 3)]]
    assert R.mat_rank(R.to_matrix(F, rows, 2)) == 1
    # a rational space whose rank mu_12 over QQ is 48: the same space has rank 48 modulo 13 and 32003 (the power pair)
    C = R.space_of(F, 4, R.named_spaces()["W0_e4"][1])
    assert R.rank_mu(F, C, 4, 12) == 48
    # rank of mu_12 against the rank routine of EXP-006 over GF(13)
    F13 = R.make_field("GF(13)")
    C13 = R.space_of(F13, 4, R.named_spaces()["P1"][1])
    rows = R.mu_rows(F13, C13, 4, 12)
    assert R.rank_mu(F13, C13, 4, 12) == R.R6.rank_mod_p(rows, 13)


def test_orbit_test_inside_and_outside():
    rng = random.Random(7)
    for e in (4, 5):
        for F in (QQ, GF):
            def draw_form():
                return (F.from_int(rng.randint(-9, 9)), F.from_int(rng.randint(-9, 9)))
            while True:
                (a1, b1), (a2, b2) = draw_form(), draw_form()
                if a1 * b2 - a2 * b1 != 0:
                    break
            rows = [R.poly_row(F, R.linear_power(F, a, b, e), e) for a, b in ((a1, b1), (a2, b2))]
            t = R.orbit_test(F, rows, e)
            assert (t["dim_S"], t["dim_S_plus_W"], t["outside_orbit"]) == (e + 1, e + 1, False)
            t0 = R.orbit_test(F, R.power_pair_basis(F, e), e)
            assert (t0["dim_S"], t0["dim_S_plus_W"], t0["outside_orbit"]) == (e + 1, e + 1, False)
            # a random W is outside
            rr = random.Random(100 + e)
            W = [[F.from_int(rr.randint(-9, 9)) for _ in range(R.u(e))] for _ in range(2)]
            tw = R.orbit_test(F, W, e)
            assert tw["outside_orbit"] and tw["dim_S_plus_W"] > e + 1
    # <x^4 + x y^3, y^4> is outside the orbit
    P1 = R.space_of(QQ, 4, R.named_spaces()["P1"][1])
    assert R.orbit_test(QQ, P1, 4)["dim_S_plus_W"] == 6


def test_tangent_space_at_the_power_pair_typed_values():
    expect = {4: (48, 2, 1, 2, 12), 5: (70, 2, 2, 4, 16), 6: (96, 2, 4, 8, 20), 7: (126, 2, 6, 12, 24)}
    for e, (rk, dk, co, rt, td) in expect.items():
        d = R.tangent_at_power_pair(QQ, e)
        assert (d["rank_A"], d["dim_K"], d["coker_dim"], d["rank_T"], d["tangent_dim"]) == (rk, dk, co, rt, td)
        assert d["orbit_directions_in_tangent_space"] and d["orbit_directions_rank"] == 2


def test_pure_and_hilbert_of_named_spaces():
    sp = R.named_spaces()
    C = R.space_of(QQ, 4, sp["P1"][1])
    ev = R.evaluate_space(QQ, C, 4)
    assert ev["rank_mu_3e"] == 48 and ev["pure"] and ev["pure_hilbert"] and ev["hilbert"] == ev["hilbert_module"][:len(ev["hilbert"])]
    assert ev["orbit"]["outside_orbit"]
    C1 = R.space_of(QQ, 4, sp["C1"][1])
    ev1 = R.evaluate_space(QQ, C1, 4)
    assert ev1["rank_mu_3e"] == 49 and not ev1["pure"]


def test_seeded_draws_are_reproducible_and_have_the_common_factor():
    assert R.draw_L_params(32003, 5) == R.draw_L_params(32003, 5) != R.draw_L_params(32003, 6)
    rows, (q, a, b) = R.draw_common_factor_space(GF, 4, 1, 3)
    rows2, _ = R.draw_common_factor_space(GF, 4, 1, 3)
    assert rows == rows2
    mon = A.monos(4)
    for row, other in ((rows[0], a), (rows[1], b)):
        prod = [0] * 5
        for i, x in enumerate(q):
            for j, y in enumerate(other):
                prod[i + j] = (prod[i + j] + x * y) % GF.p
        for im, m in enumerate(mon):
            if m[2] == 0:
                assert row[im] == prod[m[1]]
    # the claim of T6 on one draw: rank mu_12 <= 48
    assert R.rank_mu(GF, rows, 4, 12) <= 48


def test_singular_script_over_the_rationals():
    C = R.space_of(QQ, 4, R.named_spaces()["P2"][1])
    js = R.basis_json(QQ, C, 4)
    script = Sg.build_script(Sg.QQ_RECORD, 1, Sg.relations_of(js))
    assert script.startswith("ring r0 = 0,(x,y,z),wp(1,1,2);")
    assert "(31)*x^2*y^2" in script and "(-8)*x^1*y^1*z^1" in script
    assert R.basis_from_json(QQ, js, 4) == C
