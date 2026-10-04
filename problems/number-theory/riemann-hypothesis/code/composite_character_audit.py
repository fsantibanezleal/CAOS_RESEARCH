"""Exact controls for EXP-021; no analytic cancellation estimate."""

from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import product
import json
from math import gcd, lcm
from pathlib import Path
import time

import sympy as sp


class Cyclotomic:
    """Integer quotient Z[x]/Phi_M with canonical coefficient vectors."""

    def __init__(self, order):
        self.order = order
        x = sp.Symbol('x')
        self.modulus = [int(c) for c in reversed(sp.Poly(sp.cyclotomic_poly(order, x), x).all_coeffs())]
        self.degree = len(self.modulus)-1
        self.zero = (0,)*self.degree
        self.one = self.reduce([1])
        roots = [self.one]
        for _ in range(1, order):
            roots.append(self.reduce([0, *roots[-1]]))
        self.roots = roots
        assert self.reduce([0, *roots[-1]]) == self.one

    def reduce(self, coefficients):
        result = list(coefficients)
        while len(result) > self.degree:
            coefficient = result.pop()
            offset = len(result)-self.degree
            for j in range(self.degree):
                result[offset+j] -= coefficient*self.modulus[j]
        return tuple(result+[0]*(self.degree-len(result)))

    def root(self, exponent):
        return self.roots[exponent % self.order]

    def add(self, *values):
        return tuple(sum(terms) for terms in zip(*values)) if values else self.zero

    def scale(self, value, scalar):
        return tuple(scalar*c for c in value)

    def multiply(self, left, right):
        coefficients = [0]*(2*self.degree-1)
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                coefficients[i+j] += a*b
        return self.reduce(coefficients)


@lru_cache(None)
def character_group(q):
    """All characters, also for non-cyclic 2-power unit groups."""
    units = [u for u in range(q) if gcd(u, q) == 1]
    if q == 1:
        return 1, units, [{0: 0}]
    components = []
    for prime, power in sorted(sp.factorint(q).items()):
        modulus = int(prime**power)
        if prime == 2 and power == 1:
            continue
        if prime == 2 and power >= 3:
            order = 2**(int(power)-2)
            signs, logs = {}, {}
            for sign, index in product(range(2), range(order)):
                residue = (-1)**sign*pow(5, index, modulus) % modulus
                signs[residue], logs[residue] = sign, index
            components.extend([(2, {u: signs[u % modulus] for u in units}),
                               (order, {u: logs[u % modulus] for u in units})])
        else:
            order = int(sp.totient(modulus))
            generator = int(sp.primitive_root(modulus))
            logs = {pow(generator, j, modulus): j for j in range(order)}
            components.append((order, {u: logs[u % modulus] for u in units}))
    root_order = lcm(q, *(order for order, _ in components))
    characters = []
    for dual in product(*(range(order) for order, _ in components)):
        characters.append({u: sum(j*logs[u]*(root_order//order)
                                  for j, (order, logs) in zip(dual, components)) % root_order
                           for u in units})
    assert len(characters) == len(units)
    return root_order, units, characters


def conductor(q, character):
    """Find the minimal modulus through which this unit character factors."""
    for f in sp.divisors(q):
        fibers = {}
        for u, value in character.items():
            residue = u % int(f)
            if residue in fibers and fibers[residue] != value:
                break
            fibers[residue] = value
        else:
            return int(f), fibers
    raise AssertionError('Every character must factor through its own modulus')


def gauss(field, modulus, values, conjugate=False):
    return field.add(*(field.root(u*(field.order//modulus)+(-v if conjugate else v))
                       for u, v in values.items()))


def character_controls(max_modulus=16):
    counts = {'moduli': 0, 'characters': 0, 'unit_fourier_identities': 0,
              'primitive_gauss_products': 0, 'squarefree_induction_identities': 0,
              'induced_euler_coefficients': 0}
    induced_norm_negative = False
    for q in range(1, max_modulus+1):
        order, units, characters = character_group(q)
        field = Cyclotomic(order)
        gausses = [gauss(field, q, chi, conjugate=True) for chi in characters]
        for a, m in product(units, repeat=2):
            right = field.add(*(field.multiply(tau, field.root(chi[a]+chi[m]))
                                for chi, tau in zip(characters, gausses)))
            assert right == field.scale(field.root(a*m*(order//q)), len(units))
            counts['unit_fourier_identities'] += 1
        for chi, tau in zip(characters, gausses):
            f, primitive = conductor(q, chi)
            primitive_tau = gauss(field, f, primitive, conjugate=True)
            if f == q:
                assert field.multiply(gauss(field, q, chi), tau) == field.scale(field.root(chi[(-1) % q]), q)
                counts['primitive_gauss_products'] += 1
            if sp.mobius(q) != 0:
                r = q//f
                expected = field.scale(field.multiply(field.root(-primitive[r % f]), primitive_tau), int(sp.mobius(r)))
                assert tau == expected
                counts['squarefree_induction_identities'] += 1
            # Finite Dirichlet coefficients of E_q(u)L(u,chi*) equal chi(n).
            extra_primes = [int(p) for p in sp.factorint(q) if f % int(p) != 0]
            for n in range(1, 33):
                terms = []
                for mask in product([0, 1], repeat=len(extra_primes)):
                    d = 1
                    sign = 1
                    for included, p in zip(mask, extra_primes):
                        if included:
                            d *= p
                            sign *= -1
                    if n % d == 0 and gcd(n//d, f) == 1:
                        # chi*(d)chi*(n/d) = chi*(n), unless a factor is non-unit.
                        if gcd(d, f) == 1:
                            terms.append(field.scale(field.root(primitive[d % f]+primitive[(n//d) % f]), sign))
                expected = field.root(chi[n % q]) if gcd(n, q) == 1 else field.zero
                assert field.add(*terms) == expected
                counts['induced_euler_coefficients'] += 1
            if q == 4 and f == 1:
                assert tau == field.zero
                induced_norm_negative = True
        counts['moduli'] += 1
        counts['characters'] += len(characters)
        print(f'character modulus={q} characters={len(characters)} exact PASS', flush=True)
    assert induced_norm_negative
    return counts


def shifted_prime_power(a, b, power):
    return sum((a**j*b**(power-j) for j in range(power+1)), Fraction(0)) if power >= 0 else Fraction(0)


def divisor_coefficient(n, alpha, beta):
    return sum((Fraction(int(u))**(-alpha)*Fraction(n//int(u))**(-beta)
                for u in sp.divisors(n)), Fraction(0))


def corrected_coefficient(d, m, q, alpha, beta):
    assert gcd(m, q) == 1
    result = Fraction(1)
    primes = set(sp.factorint(d)) | set(sp.factorint(m))
    for prime in primes:
        p = int(prime)
        b = int(sp.factorint(d).get(prime, 0))
        j = int(sp.factorint(m).get(prime, 0))
        a, c = Fraction(p)**(-alpha), Fraction(p)**(-beta)
        if q % p == 0:
            assert j == 0
            local = shifted_prime_power(a, c, b)
        else:
            local = (shifted_prime_power(a, c, b)*shifted_prime_power(a, c, j)
                     -a*c*shifted_prime_power(a, c, b-1)*shifted_prime_power(a, c, j-1))
        result *= local
    return result


def arithmetic_controls():
    a, b = sp.symbols('A B')
    symbolic = 0
    for base, extra in product(range(6), range(13)):
        assert sp.expand(shifted_prime_power(a, b, base)*shifted_prime_power(a, b, extra)
                         -a*b*shifted_prime_power(a, b, base-1)*shifted_prime_power(a, b, extra-1)
                         -shifted_prime_power(a, b, base+extra)) == 0
        symbolic += 1
    rational = 0
    for h, n, shifts in product(range(1, 25), range(1, 65), [(0, 0), (1, 2), (-1, 1)]):
        d = gcd(n, h)
        q, m = h//d, n//d
        assert corrected_coefficient(d, m, q, *shifts) == divisor_coefficient(n, *shifts)
        rational += 1
    # Deliberately discard the non-unit residue classes: n=h cannot survive.
    assert gcd(6, 6) != 1 and divisor_coefficient(6, 1, 2) != 0
    av, bv = Fraction(1, 2), Fraction(1, 4)
    wrong_sign = (av+bv)**2+av*bv
    assert wrong_sign != shifted_prime_power(av, bv, 2)
    x, avar, bvar = sp.symbols('x a b')
    assert sp.expand(x*(avar+bvar-avar*bvar*x)).subs({avar: 1, bvar: 1}) == 2*x-x*x
    return {'formal_prime_power_identities': symbolic, 'rational_gcd_shift_controls': rational,
            'negative_controls': {'omitted_nonunit_class_detected': True,
                                  'incorrect_local_sign_detected': True,
                                  'primitive_norm_at_induced_modulus_detected': True},
            'prime_unshifted_anchor': '2*x-x^2'}


def audit():
    started = time.monotonic()
    finite = character_controls()
    arithmetic = arithmetic_controls()
    problem = Path(__file__).resolve().parents[1]
    experiment = problem/'experiments/EXP-021-composite-character-layer'
    paths = [Path(__file__), experiment/'hypothesis.md', experiment/'proof.md']
    return {'schema': 'rh-composite-character-layer-v1', 'passed': True,
            'scope': 'exact supporting arithmetic layer; no analytic moment or cancellation gain',
            'finite_character_controls': finite, 'shifted_euler_controls': arithmetic,
            'bindings': {p.relative_to(problem).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            'elapsed_seconds': time.monotonic()-started,
            'not_established': ['uniform shifted short-window reciprocity', 'signed family cancellation',
                                'longer mollifier', 'new proportion', 'novel priority', 'RH']}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path, required=True)
    arguments = parser.parse_args()
    result = audit()
    arguments.receipt.parent.mkdir(parents=True, exist_ok=True)
    arguments.receipt.write_bytes((json.dumps(result, indent=2, sort_keys=True)+'\n').encode())
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
