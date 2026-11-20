"""Pure Betti tables over U(H): Hilbert series, primitive points (Herzog-Kuhl), the parity test."""
from fractions import Fraction
from math import gcd

from . import algebra as A


def primitive_pure_betti(degrees):
    """Smallest positive integer Betti numbers of a pure table of type degrees = (0, d1, d2, d3):
    beta_i proportional to prod_(j != i) 1 / |d_j - d_i| (Herzog-Kuhl)."""
    vals = []
    for i, di in enumerate(degrees):
        p = Fraction(1)
        for j, dj in enumerate(degrees):
            if j != i:
                p /= abs(dj - di)
        vals.append(p)
    den = 1
    for v in vals:
        den = den * v.denominator // gcd(den, v.denominator)
    ints = [int(v * den) for v in vals]
    g = 0
    for n in ints:
        g = gcd(g, n)
    return tuple(n // g for n in ints)


def hilbert_series_coefficients(degrees, betas, n):
    """First n coefficients of sum (-1)^i beta_i t^(d_i) / ((1-t)^2 (1-t^2))."""
    out = [0] * n
    for i, (d, b) in enumerate(zip(degrees, betas)):
        sign = -1 if i % 2 else 1
        for t in range(d, n):
            out[t] += sign * b * A.dim_U(t - d)
    return out


def pure_hilbert_function(degrees, betas):
    """The Hilbert function (list from degree 0) of the pure table over U(H); raises ValueError when the series
    is not a polynomial (the table is not the table of a finite length module)."""
    n = degrees[-1] + 24
    s = hilbert_series_coefficients(degrees, betas, n)
    last = max((i for i, c in enumerate(s) if c), default=-1)
    if last >= degrees[-1] + 12:
        raise ValueError("series does not terminate")
    return s[: last + 1]


def parity_passes(degrees, betas=None):
    """The ray (and its primitive point, or the given Betti numbers) passes the parity test when the Hilbert
    series over U(H) is a polynomial with nonnegative coefficients."""
    betas = betas or primitive_pure_betti(degrees)
    try:
        h = pure_hilbert_function(degrees, betas)
    except ValueError:
        return False
    return all(c >= 0 for c in h)
