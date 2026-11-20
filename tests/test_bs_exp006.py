"""Gate G4 of EXP-006 (boij-soderberg-realizability): the rank routine of mu_3e(W) against the module construction of
`uhlib`, the seeded subspace generator, the enumeration of subspaces, the orbit test of family B2 and the formula h_e."""
import random
import sys
from pathlib import Path

EXP = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
       / "experiments" / "EXP-006-odd-characteristic-below-2e")
sys.path.insert(0, str(EXP))

import exp006_routine as R  # noqa: E402
import exp006_singular as Sg  # noqa: E402
import numpy as np  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib.module import quotient_module  # noqa: E402

FIELDS = ("GF(3)", "GF(5)", "GF(9)", "GF(13)")


def test_formula_against_typed_functions():
    typed = {
        3: [1, 2, 4, 4, 5, 4, 4, 2, 1] + [0] * 6,
        4: [1, 2, 4, 6, 7, 8, 8, 8, 7, 6, 4, 2, 1] + [0] * 6,
        5: [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 9, 6, 4, 2, 1] + [0] * 6,
    }
    for e, h in typed.items():
        assert [R.h_e(e, n) for n in range(len(h))] == h
        assert sum(h) == {3: 27, 4: 64, 5: 125}[e]  # the lengths stated in the hypothesis
    assert [R.u(n) for n in range(17)] == [1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36, 42, 49, 56, 64, 72, 81]
    assert [R.target_rank(e) for e in (3, 4, 5)] == [30, 48, 70]


def test_extension_field_moduli():
    for name, mod in (("GF(9)", [1, 0, 1]), ("GF(25)", None), ("GF(27)", None)):
        F = R.make_field(name)
        assert F.char ** F.degree == int(name[3:-1]) and len(F.modulus) == F.degree + 1 and F.modulus[-1] == 1
        if mod:
            assert F.modulus == mod
        rec = R.field_record(F)
        assert rec["name"] == name and rec["modulus"] == list(F.modulus)


def _naive_rank(F, rows):
    """Gaussian elimination through the field API of uhlib (the reference for the expanded rank)."""
    rows = [list(r) for r in rows]
    r = 0
    for j in range(len(rows[0])):
        piv = next((i for i in range(r, len(rows)) if not F.is_zero(rows[i][j])), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = F.inv(rows[r][j])
        rows[r] = [F.mul(inv, x) for x in rows[r]]
        for i in range(len(rows)):
            if i != r and not F.is_zero(rows[i][j]):
                f = rows[i][j]
                rows[i] = [F.sub(x, F.mul(f, y)) for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def test_rank_over_extension_fields_against_naive_elimination():
    rng = random.Random(7)
    for name in ("GF(9)", "GF(25)", "GF(27)"):
        F = R.make_field(name)
        ctx = R.ctx_of(F)
        for _ in range(15):
            m, n = rng.randint(3, 7), rng.randint(2, 7)
            rows = [[F.random(rng) if rng.random() < 0.6 else F.zero for _ in range(n)] for _ in range(m)]
            if rng.random() < 0.5:  # force a dependency: the last row is a combination of the first two
                c1, c2 = F.random(rng), F.random(rng)
                rows[-1] = [F.add(F.mul(c1, a), F.mul(c2, b)) for a, b in zip(rows[0], rows[1])]
            E = R.coeff_array(F, rows)
            assert R.rank_field(ctx, E) == _naive_rank(F, rows)


def test_left_multiplication_structure_constants():
    """T[u, m, :] is the PBW expansion of u * m (left multiple), checked against the integer product of uhlib."""
    p, e, n = 13, 4, 7
    T = R.struct_tensor(p, e, n)
    pos = {m: i for i, m in enumerate(A.monos(n))}
    for iu, a in enumerate(A.monos(n - e)):
        for im, b in enumerate(A.monos(e)):
            prod = A.poly_mul_int({a: 1}, {b: 1})
            expect = np.zeros(len(pos), dtype=np.int64)
            for mm, c in prod.items():
                expect[pos[mm]] = c % p
            assert (T[iu, im] == expect).all()
    # the product is the left one: y * x = x y - z (and x * y = x y)
    assert A.poly_mul_int({(0, 1, 0): 1}, {(1, 0, 0): 1}) == {(1, 1, 0): 1, (0, 0, 1): -1}
    T2 = R.struct_tensor(13, 2, 3)  # (x or y) * (degree 2 monomial): y * x^2 has a z term, x * y^2 has none
    pos3 = {m: i for i, m in enumerate(A.monos(3))}
    iy = list(A.monos(1)).index((0, 1, 0))
    ix2 = list(A.monos(2)).index((2, 0, 0))
    assert T2[iy, ix2, pos3[(2, 1, 0)]] == 1 and T2[iy, ix2, pos3[(1, 0, 1)]] == (-2) % 13


def test_rank_at_3e_against_uhlib_module_construction():
    for e in (3, 4):
        for name in FIELDS:
            F = R.make_field(name)
            ctx = R.ctx_of(F)
            for i in range(20):
                C = R.draw_space(F, e, R.SEED_BASE + 500 + i)
                M = quotient_module(F, [0], R.polys_as_relations(F, C, e), maxdeg=3 * e)
                dims = list(M.dims) + [0] * (3 * e + 1 - len(M.dims))
                assert dims[3 * e] == R.u(3 * e) - R.rank_mu(ctx, C, e, 3 * e), (e, name, i)
                assert dims[e] == R.u(e) - 2


def test_generator_rank_two_and_determinism():
    for name in ("GF(3)", "GF(9)", "GF(13)", "GF(27)"):
        F = R.make_field(name)
        ctx = R.ctx_of(F)
        spaces = []
        for s in range(8):
            C = R.draw_space(F, 3, R.SEED_BASE + s)
            assert C.shape == (2, R.u(3), F.degree)
            assert R.rank_field(ctx, C) == 2
            spaces.append(C)
            assert (R.draw_space(F, 3, R.SEED_BASE + s) == C).all()  # the same seed, the same space
        assert len({C.tobytes() for C in spaces}) == len(spaces)  # different seeds, different spaces


def test_generator_redraws_until_rank_two():
    """With e = 1 (two monomials) over GF(3) a rank-deficient draw is common; the generator advances the same stream."""
    F = R.make_field("GF(3)")
    ctx = R.ctx_of(F)
    redrawn = 0
    for s in range(300):
        rng = random.Random(R.SEED_BASE + s)
        first = R.coeff_array(F, [[F.random(rng) for _ in range(R.u(1))] for _ in range(2)])
        C = R.draw_space(F, 1, R.SEED_BASE + s)
        assert R.rank_field(ctx, C) == 2
        if R.rank_field(ctx, first) < 2:
            redrawn += 1
            assert not (C == first).all()
        else:
            assert (C == first).all()
    assert redrawn > 0


def test_enumeration_counts():
    assert len(R.enumerated("GF(3)", 3)) == 11011  # [6 choose 2]_3
    assert len(R.enumerated("GF(3)", 2)) == 130  # [4 choose 2]_3
    assert len({C.tobytes() for C in R.enumerated("GF(3)", 2)}) == 130


def test_basis_round_trip_and_text():
    for name in ("GF(5)", "GF(9)"):
        F = R.make_field(name)
        C = R.draw_space(F, 3, R.SEED_BASE + 3)
        assert (R.basis_from_json(F, R.basis_json(F, C, 3), 3) == C).all()
    F = R.make_field("GF(5)")
    C = R.coeff_array(F, [[1 if m == (3, 0, 0) else 0 for m in A.monos(3)],
                          [4 if m == (1, 0, 1) else (1 if m == (0, 3, 0) else 0) for m in A.monos(3)]])
    assert [R.poly_text(F, p) for p in R.basis_json(F, C, 3)] == ["x^3", "y^3 - x*z"]  # 4 = -1 in GF(5)


def test_orbit_test_in_and_out_of_orbit():
    F = R.make_field("GF(11)")
    e = 4
    rng = random.Random(11)
    # five spaces <l1^4, l2^4> with forms over GF(11)
    for _ in range(5):
        while True:
            (a1, b1), (a2, b2) = [(rng.randrange(11), rng.randrange(11)) for _ in range(2)]
            if (a1, b1) != (0, 0) and (a2, b2) != (0, 0) and (a1 * b2 - a2 * b1) % 11:
                break
        C = R.orbit_space(F, e, (a1, b1), (a2, b2))
        res = R.orbit_test(F, C, e)
        assert res["in_orbit"] and res["kind"] == "two rational points" and res["points"] == 2, res
    # five spaces with a conjugate pair over GF(121): l = x + beta y, beta not in GF(11)
    K = R.make_field("GF(121)")
    for _ in range(5):
        beta = (rng.randrange(11), rng.randrange(1, 11))  # imaginary part nonzero
        C = R.conjugate_space(11, e, K.one, beta)
        assert R.rank_field(R.ctx_of(F), C) == 2
        res = R.orbit_test(F, C, e)
        assert res["in_orbit"] and res["kind"] == "conjugate pair" and res["irrational_points"] == 2, res
    # ten random spaces are outside the orbit
    for s in range(10):
        C = R.draw_space(F, e, R.SEED_BASE + 40 + s)
        assert not R.orbit_test(F, C, e)["in_orbit"]
    # one fourth power and a random form: one point only
    f1 = R.orbit_space(F, e, (1, 0), (0, 1))[0:1]
    other = R.draw_space(F, e, R.SEED_BASE + 99)[0:1]
    assert R.orbit_test(F, np.concatenate([f1, other], axis=0), e)["kind"] == "one point only"


def test_orbit_spaces_are_pure_over_gf11():
    F = R.make_field("GF(11)")
    ev = R.evaluate(F, R.orbit_space(F, 4, (1, 0), (0, 1)), 4, "B")
    assert ev["pure"] and ev["betti"] == [[0, 0, 1], [1, 4, 2], [2, 12, 2], [3, 16, 1]]
    assert R.evaluate(F, R.orbit_space(F, 4, (1, 3), (2, 5)), 4, "B")["pure"]  # GL_2 moves the family inside the family


def test_betti_table_of_the_known_pairs():
    expect = {("GF(7)", 3): True, ("GF(5)", 3): False, ("GF(3)", 3): False, ("GF(11)", 4): True, ("GF(7)", 4): False}
    for (name, e), pure in expect.items():
        F = R.make_field(name)
        rows = [[F.one if m == (e, 0, 0) else F.zero for m in A.monos(e)],
                [F.one if m == (0, e, 0) else F.zero for m in A.monos(e)]]
        t, _ = R.betti_table(F, R.coeff_array(F, rows), e)
        assert (t == R.pure_table(e)) is pure, (name, e)


def test_singular_script_carries_the_stored_modulus():
    F = R.make_field("GF(9)")
    C = R.draw_space(F, 3, R.SEED_BASE)
    script = Sg.build_script(R.field_record(F), 1, Sg.relations_of(R.basis_json(F, C, 3)))
    assert "ring r0 = (3,a)" in script and "minpoly = a^2+a^0;" in script and "mres(M, 0)" in script
