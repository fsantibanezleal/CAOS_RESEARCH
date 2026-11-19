"""The universal enveloping algebra U(H) of the Heisenberg Lie algebra in the PBW basis.

Side conventions: U(H) = k<x,y>/([x,[x,y]], [y,[x,y]]), z = [x,y] = xy - yx is central, so yx = xy - z.
A monomial (a, b, c) stands for x^a y^b z^c; deg x = deg y = 1, deg z = 2.  Modules are LEFT modules.
A polynomial is a dict {(a, b, c): coefficient}.  Integer polynomials (coefficients int) are the structure
constants; polynomials over a field carry field elements.
"""
from functools import lru_cache
from math import comb, factorial


def deg(m):
    return m[0] + m[1] + 2 * m[2]


@lru_cache(maxsize=None)
def monos(d):
    """PBW monomials of degree d, in a fixed order."""
    out = []
    for c in range(d // 2 + 1):
        r = d - 2 * c
        for a in range(r + 1):
            out.append((a, r - a, c))
    return tuple(out)


def dim_U(d):
    return len(monos(d)) if d >= 0 else 0


@lru_cache(maxsize=None)
def mono_mul(m1, m2):
    """x^a y^b z^c * x^a' y^b' z^c' as a tuple of (monomial, integer) pairs.

    y^b x^a' = sum_k (-1)^k k! C(b,k) C(a',k) x^(a'-k) y^(b-k) z^k  (from y x = x y - z, z central).
    """
    a, b, c = m1
    a2, b2, c2 = m2
    out = []
    for k in range(min(b, a2) + 1):
        coef = (-1) ** k * factorial(k) * comb(b, k) * comb(a2, k)
        out.append(((a + a2 - k, b + b2 - k, c + c2 + k), coef))
    return tuple(out)


def poly_mul_int(p, q):
    """Product of two integer polynomials."""
    out = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            for m, k in mono_mul(m1, m2):
                out[m] = out.get(m, 0) + c1 * c2 * k
    return {m: c for m, c in out.items() if c}


def poly_mul(F, p, q):
    """Product of two polynomials with coefficients in the field F."""
    out = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            c12 = F.mul(c1, c2)
            for m, k in mono_mul(m1, m2):
                t = F.mul(c12, F.from_int(k))
                out[m] = F.add(out[m], t) if m in out else t
    return {m: c for m, c in out.items() if not F.is_zero(c)}


X = {(1, 0, 0): 1}
Y = {(0, 1, 0): 1}
Z = {(0, 0, 1): 1}
ONE = {(0, 0, 0): 1}


def padd(p, q, sign=1):
    out = dict(p)
    for m, c in q.items():
        out[m] = out.get(m, 0) + sign * c
    return {m: c for m, c in out.items() if c}


def pscale(p, s):
    return {m: c * s for m, c in p.items() if c * s}


def pstr(p):
    """Readable form of an integer polynomial."""
    if not p:
        return "0"
    terms = []
    for (a, b, c), co in sorted(p.items(), key=lambda t: (-deg(t[0]), t[0])):
        mon = "*".join(s for s in ("x^%d" % a if a else "", "y^%d" % b if b else "", "z^%d" % c if c else "") if s)
        terms.append("%s%s" % (co, "*" + mon if mon else ""))
    return " + ".join(terms)
