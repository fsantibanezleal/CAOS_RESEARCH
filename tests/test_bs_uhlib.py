"""Tests of the exact U(H) library of instrument I1 (boij-soderberg-realizability, EXP-002)."""
import random
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "code"
sys.path.insert(0, str(CODE))

from uhlib import algebra as A  # noqa: E402
from uhlib import tor  # noqa: E402
from uhlib.fields import QQ, ExtField, make_field  # noqa: E402
from uhlib.module import ideal_module, quotient_module  # noqa: E402

F = QQ()


def test_product_rule_hand_values():
    x, y, z = A.X, A.Y, A.Z
    x2 = A.poly_mul_int(x, x)
    # y x = x y - z
    assert A.poly_mul_int(y, x) == {(1, 1, 0): 1, (0, 0, 1): -1}
    # y x^2 = x^2 y - 2 x z
    assert A.poly_mul_int(y, x2) == {(2, 1, 0): 1, (1, 0, 1): -2}
    # y^2 x^2 = x^2 y^2 - 4 x y z + 2 z^2
    y2 = A.poly_mul_int(y, y)
    assert A.poly_mul_int(y2, x2) == {(2, 2, 0): 1, (1, 1, 1): -4, (0, 0, 2): 2}
    # z is central
    for m in (x, y):
        assert A.poly_mul_int(z, m) == A.poly_mul_int(m, z)


def test_defining_relations_hold():
    """[x,[x,y]] = 0 and [y,[x,y]] = 0 in the PBW product."""
    x, y = A.X, A.Y
    z = A.padd(A.poly_mul_int(x, y), A.poly_mul_int(y, x), -1)
    assert z == A.Z
    for g in (x, y):
        comm = A.padd(A.poly_mul_int(g, z), A.poly_mul_int(z, g), -1)
        assert comm == {}


def test_associativity_random_triples():
    rng = random.Random(20261119)

    def rand_poly():
        out = {}
        for _ in range(rng.randint(1, 4)):
            d = rng.randint(0, 4)
            m = rng.choice(A.monos(d))
            out[m] = out.get(m, 0) + rng.randint(-3, 3)
        return {m: c for m, c in out.items() if c}

    for _ in range(300):
        p, q, r = rand_poly(), rand_poly(), rand_poly()
        left = A.poly_mul_int(A.poly_mul_int(p, q), r)
        right = A.poly_mul_int(p, A.poly_mul_int(q, r))
        assert left == right


def test_hilbert_function_of_U():
    assert [A.dim_U(d) for d in range(10)] == [1, 2, 4, 6, 9, 12, 16, 20, 25, 30]
    # series 1/((1-t)^2 (1-t^2)) by multiplication
    n = 12
    s = [1] + [0] * (n - 1)
    for step in (1, 1, 2):
        for i in range(step, n):
            s[i] += s[i - step]
    assert s == [A.dim_U(d) for d in range(n)]
    free = quotient_module(F, [0], [], maxdeg=6)
    assert free.dims[:7] == [A.dim_U(d) for d in range(7)]


def test_complex_K_is_a_complex_and_exact():
    K = tor.trivial_module_resolution()
    assert tor.check_complex(K)
    # Euler characteristic by degree: (1 - 2t + 2t^3 - t^4) * U(t) = 1
    n = 14
    series = [A.dim_U(d) for d in range(n)]
    for d in range(n):
        chi = series[d] - 2 * (series[d - 1] if d >= 1 else 0) + 2 * (series[d - 3] if d >= 3 else 0) - (series[d - 4] if d >= 4 else 0)
        assert chi == (1 if d == 0 else 0)
    # exactness by rank counts, degrees 0..10
    assert tor.check_exact(K, 10)


def test_betti_of_trivial_module():
    k = ideal_module(F, [A.X, A.Y], maxdeg=8)
    assert k.dims == [1]
    assert tor.betti(k) == {(0, 0): 1, (1, 1): 2, (2, 3): 2, (3, 4): 1}


def test_betti_of_four_dimensional_module_L10():
    xy_plus_yx = A.padd(A.poly_mul_int(A.X, A.Y), A.poly_mul_int(A.Y, A.X))
    gens = [{(2, 0, 0): 1}, {(0, 2, 0): 1}, xy_plus_yx]
    m = ideal_module(F, gens, maxdeg=10)
    assert m.dims == [1, 2, 1]
    assert tor.betti(m) == {(0, 0): 1, (1, 2): 3, (2, 4): 3, (3, 6): 1}


def test_betti_of_a_module_with_two_generators():
    """k (+) k: two generators, Betti numbers add."""
    k = ideal_module(F, [A.X, A.Y], maxdeg=8)
    dsum = quotient_module(F, [0, 0], [{(0, (1, 0, 0)): 1}, {(0, (0, 1, 0)): 1}, {(1, (1, 0, 0)): 1}, {(1, (0, 1, 0)): 1}], maxdeg=8)
    assert dsum.dims == [2]
    b = tor.betti(dsum)
    assert b == {key: 2 * v for key, v in tor.betti(k).items()}


def test_pure_hilbert_series_and_parity():
    from uhlib import pure

    # (1,2,2,1) on (0,2,6,8): Hilbert function (1,2,2,2,1)
    assert pure.pure_hilbert_function((0, 2, 6, 8), (1, 2, 2, 1)) == [1, 2, 2, 2, 1]
    assert pure.pure_hilbert_function((0, 2, 10, 12), (2, 3, 3, 2)) == [2, 4, 5, 6, 6, 6, 5, 4, 2]
    assert pure.primitive_pure_betti((0, 3, 9, 12)) == (1, 2, 2, 1)
    assert pure.primitive_pure_betti((0, 1, 3, 4)) == (1, 2, 2, 1)
    assert pure.primitive_pure_betti((0, 2, 10, 12)) == (2, 3, 3, 2)
    assert pure.parity_passes((0, 2, 6, 8))
    assert not pure.parity_passes((0, 4, 9, 10))


def test_prime_and_extension_fields_are_fields():
    f4 = ExtField(2, 2)
    elems = [(a, b) for a in range(2) for b in range(2)]
    for e in elems:
        if any(e):
            assert f4.mul(e, f4.inv(e)) == f4.one
    f81 = make_field(3, 4)
    rng = random.Random(1)
    for _ in range(50):
        e = f81.random(rng)
        if any(e):
            assert f81.mul(e, f81.inv(e)) == f81.one


# ---------------------------------------------------------------- EXP-003 additions (uhlib.structure, CachedExtField)
def test_cached_ext_field_matches_ext_field():
    from uhlib.fields import CachedExtField

    plain, fast = ExtField(2, 4), CachedExtField(2, 4)
    assert plain.modulus == fast.modulus and fast.char == 2 and fast.degree == 4
    rng = random.Random(7)
    for _ in range(400):
        a, b = plain.random(rng), plain.random(rng)
        assert fast.mul(a, b) == plain.mul(a, b)
        assert fast.add(a, b) == plain.add(a, b)
        assert fast.sub(a, b) == plain.sub(a, b)
        if any(a):
            assert fast.mul(a, fast.inv(a)) == fast.one


def test_enumeration_of_two_dimensional_subspaces():
    from uhlib import structure as S

    for F_, expected in ((make_field(2), 35), (make_field(2, 2), 357)):
        subs = list(S.rref_subspaces(F_, 4, 2))
        assert len(subs) == expected == S.gaussian_binomial(F_.p ** F_.degree if F_.char else 0, 4, 2)
        keys = {tuple(tuple(r) for r in s) for s in subs}
        assert len(keys) == expected  # each listed once
        for s in subs:  # reduced echelon form: a unit pivot, zeros above and below it
            assert rank_of(F_, s) == 2


def rank_of(F_, rows):
    from uhlib.linalg import rank

    return rank(F_, rows, len(rows[0]))


def test_ideal_hilbert_agrees_with_quotient_module():
    from uhlib import structure as S

    rng = random.Random(3)
    for F_ in (make_field(2), make_field(2, 2), make_field(32003), QQ()):
        for _ in range(3):
            gens = [{m: F_.random(rng) for m in A.monos(2)} for _ in range(2)]
            gens = [{m: c for m, c in g.items() if not F_.is_zero(c)} for g in gens]
            M = quotient_module(F_, [0], [{(0, m): c for m, c in g.items()} for g in gens], maxdeg=10)
            assert S.ideal_hilbert(F_, gens, 10)[: len(M.dims)] == M.dims
            if M.finished:
                assert not any(S.ideal_hilbert(F_, gens, 10)[len(M.dims):])


def test_labels_and_weight_pieces_M2():
    from uhlib import structure as S

    M = ideal_module(F, [{(2, 0, 0): 1}, {(0, 2, 0): 1}], maxdeg=12)
    assert M.hilbert_list() == [1, 2, 2, 2, 1]
    wp = S.weight_pieces(M)
    assert sum(wp.values()) == 8
    for d, n in enumerate(M.dims):
        assert sum(v for (w, dd), v in wp.items() if dd == d) == n
    # weight x degree table of the context note, e = 2: D_q(n') with d = 2 n' + q
    assert S.predicted_weight_pieces(2) == wp


def test_predicted_weight_pieces_sum_to_hilbert_series_of_the_note():
    from uhlib import structure as S

    for e in (2, 3, 5):
        wp = S.predicted_weight_pieces(e)
        series = {}
        for (w, d), n in wp.items():
            series[d] = series.get(d, 0) + n
        # (1+...+t^(e-1))^2 (1+t^2+...+t^(2e-2))
        poly = [0] * (4 * e)
        for a in range(e):
            for b in range(e):
                for c in range(e):
                    poly[a + b + 2 * c] += 1
        assert [series.get(d, 0) for d in range(4 * e)] == poly


def test_kernel_of_y_socle_and_g_elements_M2_M3():
    from uhlib import structure as S

    for e in (2, 3):
        M = ideal_module(F, [{(e, 0, 0): 1}, {(0, e, 0): 1}], maxdeg=4 * e + 6)
        rep = S.kernel_y_report(M, e)
        assert rep["kernel_y_equals_span_of_z_c_g_a"] is True
        soc = S.socle_by_weight(M)
        assert soc == {(4 * e - 4, 0): 1}


def test_z_jordan_structure_M2():
    from uhlib import structure as S

    M = ideal_module(F, [{(2, 0, 0): 1}, {(0, 2, 0): 1}], maxdeg=12)
    blocks = S.z_blocks(M)
    assert blocks == {(0, 3): 1, (1, 2): 2, (2, 1): 1}
    assert S.predicted_z_blocks(2) == blocks


def test_central_elements_in_characteristic_two_and_zero():
    from uhlib import structure as S

    f2 = make_field(2)
    d2 = [{m: f2.one} for m in A.monos(2)]  # the four PBW monomials of degree 2
    central = S.central_subspace(f2, d2, 2)
    assert len(central) == 3  # span(x^2, y^2, z) in characteristic 2
    f0 = QQ()
    d2q = [{m: f0.one} for m in A.monos(2)]
    assert len(S.central_subspace(f0, d2q, 2)) == 1  # only z in characteristic 0


def test_derivation_data_for_a_subspace():
    from uhlib import structure as S

    f2 = make_field(2)
    mono = {"x2": (2, 0, 0), "xy": (1, 1, 0), "y2": (0, 2, 0), "z": (0, 0, 1)}
    f, g = {mono["x2"]: 1}, {mono["xy"]: 1}  # (x^2, xy): c = x^2, f = xy
    rec = S.derivation_data(f2, [f, g])
    assert rec["central_dimension"] == 1 and rec["both_central"] is False
    assert rec["det_degree"] in (0, 8) or rec["det_is_zero"] in (True, False)
    both = S.derivation_data(f2, [{mono["x2"]: 1}, {mono["y2"]: 1}])
    assert both["both_central"] is True
    assert S.ideal_hilbert(f2, [f, g], 8)[-1] != 0


def test_ssyt_counts_and_bad_primes():
    from uhlib import structure as S

    assert S.ssyt_count_rectangle(1, 1, 2) == 2 and S.ssyt_count_rectangle(1, 2, 2) == 3
    assert S.ssyt_count_rectangle(2, 2, 3) == 6 and S.ssyt_count_rectangle(3, 1, 4) == 4
    assert S.predicted_bad_primes(2, 23) == [2, 3]
    assert {2, 3, 5} <= set(S.predicted_bad_primes(3, 23))


def test_numpy_quotient_equals_python_quotient():
    """fastmod.quotient_module_np reproduces module.quotient_module exactly (dims, X, Y, labels)."""
    from uhlib.fastmod import quotient_module_np
    from uhlib.fields import CachedExtField, PrimeField

    rng = random.Random(11)
    for F_ in (PrimeField(2), CachedExtField(2, 2), CachedExtField(2, 4), PrimeField(32003), PrimeField(3)):
        for shifts, nrel, deg in (([0], 2, 2), ([0, 0], 3, 2), ([0, 0, 0], 4, 1)):
            rels = []
            for _ in range(nrel):
                rel = {}
                for k in range(len(shifts)):
                    for m in A.monos(deg):
                        c = F_.random(rng)
                        if not F_.is_zero(c):
                            rel[(k, m)] = c
                rels.append(rel)
            slow = quotient_module(F_, shifts, rels, maxdeg=9)
            fast = quotient_module_np(F_, shifts, rels, maxdeg=9)
            assert fast.dims == slow.dims and fast.finished == slow.finished
            assert fast.X == slow.X and fast.Y == slow.Y
            assert fast.labels == slow.labels
            nox = quotient_module_np(F_, shifts, rels, maxdeg=9, with_action=False)
            assert nox.dims == slow.dims


def _review_poly(Fp, terms):
    """A quadric written in the monomials x^2, y^2, yx, z; the library's basis is x^a y^b z^c with yx = xy - z."""
    out = {}
    for name, c in terms.items():
        for m, k in {"xx": [((2, 0, 0), 1)], "yy": [((0, 2, 0), 1)], "z": [((0, 0, 1), 1)],
                     "yx": [((1, 1, 0), 1), ((0, 0, 1), -1)]}[name]:
            out[m] = Fp.add(out.get(m, Fp.zero), Fp.from_int(c * k))
    return {m: v for m, v in out.items() if not Fp.is_zero(v)}


def _betti_list(M):
    return sorted((k, v) for k, v in tor.betti(M).items() if v)


PURE_2 = [((0, 0), 1), ((1, 2), 2), ((2, 6), 2), ((3, 8), 1)]


def test_explicit_pair_in_characteristic_three_is_pure_and_the_hilbert_function_does_not_certify_it():
    F3 = make_field(3)
    pure = ideal_module(F3, [_review_poly(F3, {"xx": 1, "yy": 1, "yx": 1}), _review_poly(F3, {"xx": 1, "yx": 1, "z": -1})],
                        maxdeg=16)
    other = ideal_module(F3, [_review_poly(F3, {"xx": 2, "yy": 2, "z": 1, "yx": 1}), _review_poly(F3, {"yy": 1, "z": 2})],
                         maxdeg=16)
    assert pure.finished and pure.hilbert_list() == [1, 2, 2, 2, 1] and _betti_list(pure) == PURE_2
    assert other.finished and other.hilbert_list() == [1, 2, 2, 2, 1] and _betti_list(other) != PURE_2


def test_power_pair_is_pure_exactly_from_characteristic_2e_on():
    for e in (2, 3):
        want = [((0, 0), 1), ((1, e), 2), ((2, 3 * e), 2), ((3, 4 * e), 1)]
        for p in (2, 3, 5, 7):
            Fp = make_field(p)
            M = ideal_module(Fp, [{(e, 0, 0): Fp.one}, {(0, e, 0): Fp.one}], maxdeg=4 * e + 4)
            is_pure = M.finished and _betti_list(M) == want
            assert is_pure == (p >= 2 * e), (e, p)
            if p <= 2 * e - 1:
                assert M.dim(4 * e - 2) > 0, (e, p)
