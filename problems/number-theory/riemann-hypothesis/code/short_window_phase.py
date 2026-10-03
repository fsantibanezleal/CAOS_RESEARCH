"""Exact off-diagonal collision controls for the localized twisted lemma."""

from fractions import Fraction as F


def collision(base: int, a: int, b: int, d: int) -> dict:
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (base, a, b, d)):
        raise ValueError("integer parameters required")
    if base < 2 or not 1 <= b < a or not a < d < 2 * a:
        raise ValueError("require B>=2, 1<=b<a and 1/2<theta<1")
    big_t, big_m, r = 16 * base ** (2 * a), base**b, base ** (a - b)
    h, k = big_m, big_m - 1
    m, n, length = k * r + 1, h * r + 1, base**d
    difference = h * m - k * n
    assert difference == 1 and m * n < F(big_t, 8)
    lower, upper = F(length, k * n + 1), F(length, k * n)
    exponent = d - a - b
    scale = F(base) ** exponent
    ratio = upper / scale
    expected_ratio = 1 / ((1 - F(1, base**b)) * (1 + F(1, base**a)))
    assert ratio == expected_ratio
    return {
        "B": base, "a": a, "b": b, "d": d, "theta": str(F(d, 2 * a)),
        "nu": str(F(b, 2 * a)), "T": str(big_t), "H": str(length),
        "h": str(h), "k": str(k), "m": str(m), "n": str(n),
        "hm_minus_kn": difference, "product_over_T": str(F(m * n, big_t)),
        "phase_lower": str(lower), "phase_upper": str(upper),
        "scale_exponent": exponent, "upper_over_scale": str(ratio),
        "limit": "zero" if exponent < 0 else "one" if exponent == 0 else "infinity",
        "mobius_weights": "not asserted nonzero; controls the generic twisted lemma only",
    }


def certificate() -> dict:
    rows = [collision(base, 50, b, 54) for b in (5, 4, 3) for base in (2, 10, 100)]
    return {
        "schema": "exp014-short-window-phase-collision-v1", "experiment": "EXP-014",
        "arithmetic": "exact-integers-and-rational-log-bounds", "cases": rows,
        "uniform_identity": "upper/B^(d-a-b) = 1/((1-B^(-b))(1+B^(-a))) -> 1",
        "threshold": "d-a-b=0 iff nu=theta-1/2",
        "scope": "Obstruction to uniform pointwise large-phase elimination; not to signed cancellation",
        "not_established": ["nonzero Mobius weights", "lower bound on summed off-diagonal", "false moment asymptotic", "new onset", "RH"],
    }
