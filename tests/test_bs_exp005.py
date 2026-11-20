"""Gate G4 of EXP-005 (boij-soderberg-realizability): field axioms of GF(4) and GF(16), the Hilbert function routine on
modules with known functions, the classifier, the seed rule and the left multiples."""
import sys
from itertools import product
from pathlib import Path

EXP = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
       / "experiments" / "EXP-005-characteristic-two-machine-checks")
sys.path.insert(0, str(EXP))

import exp005_routine as R  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib.fields import PrimeField  # noqa: E402


def elements(F):
    return [tuple(t) for t in product(range(2), repeat=F.k)]


def test_stated_moduli():
    assert R.make_field("GF(2^2)").modulus == [1, 1, 1]  # w^2 + w + 1
    assert R.make_field("GF(2^4)").modulus == [1, 1, 0, 0, 1]  # w^4 + w + 1
    assert R.make_field("GF(2^2)").name == "GF(2^2)" and R.make_field("GF(2^4)").name == "GF(2^4)"


def test_field_axioms_exhaustive():
    for name in ("GF(2^2)", "GF(2^4)"):
        F = R.make_field(name)
        E = elements(F)
        assert len(E) == len(set(E)) == 2 ** F.k
        zero, one = F.zero, F.one
        for a in E:
            assert F.add(a, zero) == a and F.mul(a, one) == a and F.add(a, a) == zero  # characteristic 2
            assert F.mul(a, zero) == zero
            if a != zero:
                assert F.mul(a, F.inv(a)) == one
        for a, b in product(E, repeat=2):
            assert F.add(a, b) == F.add(b, a) and F.mul(a, b) == F.mul(b, a)
            assert F.sub(a, b) == F.add(a, b)
            assert F.mul(a, b) != zero or a == zero or b == zero  # no zero divisors
        for a, b, c in product(E, repeat=3):
            assert F.add(F.add(a, b), c) == F.add(a, F.add(b, c))
            assert F.mul(F.mul(a, b), c) == F.mul(a, F.mul(b, c))
            assert F.mul(a, F.add(b, c)) == F.add(F.mul(a, b), F.mul(a, c))


def test_gf16_w_has_order_15_and_w4_is_w_plus_1():
    F = R.make_field("GF(2^4)")
    w = (0, 1, 0, 0)
    assert F.pow(w, 4) == (1, 1, 0, 0)  # w^4 = w + 1
    assert F.pow(w, 15) == F.one and all(F.pow(w, n) != F.one for n in (1, 3, 5))
    G = R.make_field("GF(2^2)")
    w2 = (0, 1)
    assert G.mul(w2, w2) == (1, 1) and G.pow(w2, 3) == G.one  # w^2 = w + 1


def test_left_multiple_is_a_left_multiple():
    F = PrimeField(32003)
    # y * x = x y - z, not x * y = x y
    assert R.left_multiple(F, (0, 1, 0), {(0, (1, 0, 0)): 1}) == {(0, (1, 1, 0)): 1, (0, (0, 0, 1)): 32002}
    assert R.left_multiple(F, (1, 0, 0), {(0, (0, 1, 0)): 1}) == {(0, (1, 1, 0)): 1}


def test_hilbert_of_U_itself():
    for name in ("GF(2)", "GF(2^2)", "GF(32003)"):
        F = R.make_field(name)
        assert R.hilbert_function(F, 1, [], 10) == [1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36]
        assert R.hilbert_function(F, 2, [], 5) == [2, 4, 8, 12, 18, 24]


def test_hilbert_of_the_trivial_module():
    for name in ("GF(2)", "GF(2^4)", "GF(32003)"):
        F = R.make_field(name)
        x, y = {(0, (1, 0, 0)): F.one}, {(0, (0, 1, 0)): F.one}
        assert R.hilbert_function(F, 1, [x, y], 8) == [1, 0, 0, 0, 0, 0, 0, 0, 0]


def x_pow(F, e):
    return {(0, (e, 0, 0)): F.one}


def y_pow(F, e):
    return {(0, (0, e, 0)): F.one}


def test_hilbert_of_the_pure_tables_over_gf32003():
    F = R.make_field("GF(32003)")
    hand = {2: [1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0], 3: [1, 2, 4, 4, 5, 4, 4, 2, 1, 0, 0, 0, 0]}
    for e in (2, 3):
        h = R.hilbert_function(F, 1, [x_pow(F, e), y_pow(F, e)], 12)
        assert h == hand[e]
        assert sum(h) == e ** 3
        table = [A.dim_U(n) - 2 * A.dim_U(n - e) + 2 * A.dim_U(n - 3 * e) - A.dim_U(n - 4 * e) for n in range(13)]
        assert h == table  # Betti table (1, 2, 2, 1) on (0, e, 3e, 4e)


def test_zero_and_dependent_relations_are_computed():
    F = R.make_field("GF(2^2)")
    f = {(0, (2, 0, 0)): F.one, (0, (0, 0, 1)): (1, 1)}
    base = R.hilbert_function(F, 1, [f], 8)
    assert R.hilbert_function(F, 1, [f, {}], 8) == base  # a zero relation
    assert R.hilbert_function(F, 1, [f, f], 8) == base  # a repeated relation
    assert R.hilbert_function(F, 1, [f, {(0, (2, 0, 0)): (1, 1), (0, (0, 0, 1)): F.mul((1, 1), (1, 1))}], 8) == base  # (1 + w) f
    assert base == [A.dim_U(n) - A.dim_U(n - 2) for n in range(9)]


def test_codecs_agree_on_a_prime_field_embedded_in_gf4():
    """The bitset path (GF(2)), the table path (GF(4)) and the generic path (field API) give one function."""
    F2, F4 = R.make_field("GF(2)"), R.make_field("GF(2^2)")
    rels2 = R.random_relations(F2, 1, 2, 3, R.SEED_BASE + 5)
    rels4 = [{key: (c, 0) for key, c in r.items()} for r in rels2]  # the same relations viewed in GF(4)
    h2 = R.hilbert_function(F2, 1, rels2, 12)
    h4 = R.hilbert_function(F4, 1, rels4, 12)
    codec = R._Codec(F4)
    codec.kind = "generic"
    assert h2 == h4
    # force the generic elimination
    rank_rows = []
    for n in (6, 9):
        dn = A.dim_U(n)
        pos = {m: i for i, m in enumerate(A.monos(n))}
        rows = list(R._row_entries(codec, 1, rels4, n, [3, 3], pos, dn))
        rank_rows.append(dn - R._rank_generic(F4, rows, dn))
    assert rank_rows == [h2[6], h2[9]]


def test_classifier_four_outcomes():
    assert R.classify([1, 2, 3, 2, 1, 0, 0, 0, 0]) == (R.FINITE, None)
    assert R.classify([1, 1, 3, 0, 5, 5, 5, 5, 5, 5, 5, 5]) == (R.FINITE, None)  # a zero anywhere, even if not last
    assert R.classify([1, 2, 5, 6, 7, 8, 8, 8, 8, 8, 8]) == (R.CONSTANT, 8)
    assert R.classify([1, 2, 5, 6, 7, 8, 9, 8, 8, 8, 8, 8, 8]) == (R.CONSTANT, 8)  # the last six decide
    assert R.classify([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]) == (R.GROWING, None)
    assert R.classify([1, 2, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]) == (R.GROWING, None)  # h(D) >= h(D - 6) > 0
    assert R.classify([1, 2, 3, 12, 11, 12, 11, 12, 11, 12, 11, 12, 11]) == (R.GROWING, None)  # the literal rule: h(D) >= h(D - 6)
    assert R.classify([5, 5, 9, 9, 9, 9, 9, 9, 9, 3]) == (R.UNCLASSIFIED, None)  # h(D) < h(D - 6)


def test_seed_rule():
    F = R.make_field("GF(2^4)")
    a, b, e = 1, 2, 4
    r1 = R.random_relations(F, a, b, e, R.SEED_BASE + 7)
    r2 = R.random_relations(F, a, b, e, R.SEED_BASE + 7)
    r3 = R.random_relations(F, a, b, e, R.SEED_BASE + 8)
    assert r1 == r2 and r1 != r3
    spec = {"id": "x", "family": "C2a", "field": "GF(2^4)", "index": 7, "shape": [1, 2, 4], "D": 6, "kind": "random"}
    rec = R.run_case(spec)
    assert rec["seed"] == 20261120 + 7
    assert rec["relations"] == [R.rel_to_json(F, r) for r in r1]
    rebuilt = [R.rel_from_json(F, js) for js in rec["relations"]]
    assert rebuilt == r1  # the case rebuilds from the stored relations
    assert rec["hilbert"] == R.hilbert_function(F, 1, rebuilt, 6)
    assert all(m in A.monos(4) for r in r1 for (_, m) in r)


def test_case_counts_of_the_hypothesis():
    specs = R.case_specs()
    fam = {}
    for s in specs:
        fam[(s["family"], s["field"])] = fam.get((s["family"], s["field"]), 0) + 1
    assert fam[("C1a", "GF(2)")] == 35 and fam[("C1b", "GF(2)")] == 651 and fam[("C1c", "GF(2)")] == 63
    for f in ("GF(2)", "GF(2^2)", "GF(2^4)"):
        assert fam[("C2a", f)] == 120 and fam[("C2b", f)] == 120 and fam[("C2e", f)] == 20
    assert fam[("C2c", "GF(2^4)")] == 10 and fam[("C2d", "GF(2^4)")] == 10
    assert fam[("C2f", "GF(2^4)")] == 20 and fam[("C2g", "GF(2^4)")] == 5 and fam[("C3", "GF(2^4)")] == 40
    assert len({s["id"] for s in specs}) == len(specs)


def test_s2_values():
    assert [R.s2_value(1, e) for e in range(2, 8)] == [2, 4, 8, 12, 18, 24]
    assert (R.s2_value(2, 2), R.s2_value(2, 3), R.s2_value(3, 2)) == (6, 12, 12)
