"""Exact support controls for short-window off-diagonal collisions."""

from fractions import Fraction as F
from math import isqrt


def prime_square_sum_upper():
    return sum((F(1, p*p) for p in (2, 3, 5, 7)), F()) + F(1, 121) + F(1, 22)


def supported_pair(limit):
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1000000:
        raise ValueError("integer M>=1000000 required")
    squarefree = bytearray(b"\x01") * (limit+1)
    squarefree[0] = 0
    # Mark all square divisors, not just prime squares.
    for divisor in range(2, isqrt(limit)+1):
        square = divisor*divisor
        squarefree[square::square] = b"\x00" * (limit//square)
    return next(h for h in range((limit+1)//2, 3*limit//4+1)
                if squarefree[h] and squarefree[h-1])


def certificate():
    limit, r = 1000000, 1000000
    h = supported_pair(limit)
    k, m, n = h-1, (h-1)*r+1, h*r+1
    big_t = 16*(limit*r)**2
    assert h*m-k*n == 1 and m*n < F(big_t, 8)
    upper = prime_square_sum_upper()
    lower_count = F(limit, 100)-F(1, 25)-2*isqrt(limit)
    assert upper < F(12, 25) and lower_count > 0
    return {
        "schema": "exp015-squarefree-phase-v1", "experiment": "EXP-015",
        "M": limit, "r": r, "h": h, "k": k, "m": m, "n": n,
        "T": str(big_t), "hm_minus_kn": 1,
        "prime_square_sum_upper": str(upper),
        "uniform_count_lower_at_M": str(lower_count),
        "nonzero_mobius_weights": True,
        "nonzero_basic_polynomial_coefficients": True,
        "phase_cases": [{"H": str(H), "lower": str(F(H, h*m)),
                         "upper": str(F(H, k*n))} for H in (10**16, 10**18, 10**20)],
        "uniform_comparison": "(1/5) M^2 r <= kn < M^2 r for M>=1000000,r>=2",
        "threshold": "nu=theta-1/2; nonzero Mobius support does not remove slow phases",
        "summed_mollifier_barrier_established": False,
    }
