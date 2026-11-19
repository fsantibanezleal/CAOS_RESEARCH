"""Exact coefficient fields for the U(H) library: QQ, GF(p) and GF(p^k).

Elements: Fraction (QQ), int in [0, p) (GF(p)), tuple of k ints in [0, p) (GF(p^k), coefficients of
a polynomial in the generator a, lowest degree first, modulo a verified irreducible monic modulus).
Every field exposes the same small API so the linear algebra is written once.
"""
from fractions import Fraction
from itertools import product


class QQ:
    char = 0
    degree = 1
    name = "QQ"
    zero = Fraction(0)
    one = Fraction(1)

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def neg(self, a):
        return -a

    def mul(self, a, b):
        return a * b

    def inv(self, a):
        return 1 / a

    def from_int(self, n):
        return Fraction(n)

    def is_zero(self, a):
        return a == 0

    def random(self, rng, bound=7):
        return Fraction(rng.randint(-bound, bound))

    def to_json(self, a):
        return str(Fraction(a))


class PrimeField:
    degree = 1

    def __init__(self, p):
        assert p > 1 and all(p % q for q in range(2, int(p ** 0.5) + 1)), "p must be prime"
        self.p = p
        self.char = p
        self.name = "GF(%d)" % p
        self.zero = 0
        self.one = 1

    def add(self, a, b):
        return (a + b) % self.p

    def sub(self, a, b):
        return (a - b) % self.p

    def neg(self, a):
        return (-a) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def inv(self, a):
        return pow(a, -1, self.p)

    def from_int(self, n):
        return n % self.p

    def is_zero(self, a):
        return a == 0

    def random(self, rng):
        return rng.randrange(self.p)

    def to_json(self, a):
        return int(a)


def _poly_mod(a, m, p):
    """Remainder of the polynomial a (list, low to high) modulo the monic polynomial m over GF(p)."""
    a = list(a)
    dm = len(m) - 1
    for i in range(len(a) - 1, dm - 1, -1):
        c = a[i] % p
        if c:
            for j in range(dm + 1):
                a[i - dm + j] = (a[i - dm + j] - c * m[j]) % p
    out = [x % p for x in a[:dm]]
    return out + [0] * (dm - len(out))


def _is_irreducible(m, p):
    """Brute force: a monic polynomial of degree k is irreducible iff it has no monic factor of degree 1..k//2."""
    k = len(m) - 1
    for d in range(1, k // 2 + 1):
        for low in product(range(p), repeat=d):
            f = list(low) + [1]
            if not any(_poly_mod(m, f, p)):
                return False
    return True


def find_modulus(p, k):
    """First (lexicographic on the low coefficients) irreducible monic polynomial of degree k over GF(p)."""
    for low in product(range(p), repeat=k):
        m = list(low) + [1]
        if low[0] != 0 and _is_irreducible(m, p):
            return m
    raise ValueError("no irreducible polynomial found")


class ExtField:
    """GF(p^k), k >= 2, polynomial representation with a verified irreducible modulus."""

    def __init__(self, p, k):
        self.p = p
        self.k = k
        self.degree = k
        self.char = p
        self.modulus = find_modulus(p, k)
        assert _is_irreducible(self.modulus, p) and len(self.modulus) == k + 1
        self.name = "GF(%d^%d)" % (p, k)
        self.zero = (0,) * k
        self.one = (1,) + (0,) * (k - 1)

    def add(self, a, b):
        p = self.p
        return tuple((x + y) % p for x, y in zip(a, b))

    def sub(self, a, b):
        p = self.p
        return tuple((x - y) % p for x, y in zip(a, b))

    def neg(self, a):
        p = self.p
        return tuple((-x) % p for x in a)

    def mul(self, a, b):
        p = self.p
        prod = [0] * (2 * self.k - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    prod[i + j] += x * y
        return tuple(_poly_mod([c % p for c in prod], self.modulus, p))

    def pow(self, a, n):
        r = self.one
        while n:
            if n & 1:
                r = self.mul(r, a)
            a = self.mul(a, a)
            n >>= 1
        return r

    def inv(self, a):
        assert any(a), "zero has no inverse"
        return self.pow(a, self.p ** self.k - 2)

    def from_int(self, n):
        return ((n % self.p),) + (0,) * (self.k - 1)

    def is_zero(self, a):
        return not any(a)

    def random(self, rng):
        return tuple(rng.randrange(self.p) for _ in range(self.k))

    def to_json(self, a):
        return [int(x) for x in a]


def make_field(char, degree=1):
    """QQ for char 0, GF(p) for degree 1, GF(p^degree) otherwise."""
    if char == 0:
        return QQ()
    return PrimeField(char) if degree == 1 else ExtField(char, degree)
