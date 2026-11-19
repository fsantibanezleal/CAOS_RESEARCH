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
