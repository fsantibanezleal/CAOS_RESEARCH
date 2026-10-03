"""Exact parameter audit of Knausgard's fixed mixed-Gram counting assembly.

The analytic and local interval inputs are attributed, not proved here.
All mathematical decisions use Fraction; decimal strings are display bounds.
"""

from fractions import Fraction as F

DELTA = F(891, 200000)
PRESSURE = F(1, 2736)
ENERGY_GAIN = F(3362285207, 5000000000)
SOURCE_Q = F(16260119298029, 19426831050000)


def coefficients(m: int) -> tuple[F, F]:
    if not isinstance(m, int) or isinstance(m, bool) or m < 7:
        raise ValueError("block size must be an integer at least seven")
    t = F(m - 6, m)
    return DELTA * t, 6 * PRESSURE * t


def bound(m: int) -> F:
    a, beta = coefficients(m)
    return (1 + ENERGY_GAIN - beta) / (2 - a)


def slacks(m: int, tau: F, c: F) -> dict[str, F]:
    a, _ = coefficients(m)
    return {
        "tau_nonnegative": tau,
        "block_clipping": tau * tau - DELTA * (m - 6),
        "unit_diagonal_threshold": c - 1 - tau,
        "double_diagonal_threshold": c - 2 - tau / 2,
        "high_multiplicity_residual": 6 * c - 7 - c * c - a,
        "off_line_pair_residual": 4 * c - 2 - c * c - 2 * a,
    }


def admissible(m: int, tau: F, c: F) -> bool:
    return all(value >= 0 for value in slacks(m, tau, c).values())


def boundary_obstruction(m: int) -> tuple[F, F]:
    """Positive returned values exclude m, using a necessary square-root bound."""
    a, _ = coefficients(m)
    z = DELTA * (m - 6) - 3 + 2 * a
    return z, z * z - 4 * (2 - 2 * a)


def decimal_enclosure(value: F, digits: int = 50) -> dict[str, str]:
    scale = 10**digits
    lo = value.numerator * scale // value.denominator
    hi = lo if value.denominator == 1 or F(lo, scale) == value else lo + 1

    def fmt(integer: int) -> str:
        sign = "-" if integer < 0 else ""
        integer = abs(integer)
        return f"{sign}{integer // scale}.{integer % scale:0{digits}d}"

    return {"lower": fmt(lo), "upper": fmt(hi), "width": str(F(hi - lo, scale))}


def certificate() -> dict:
    source = slacks(1298, F(12, 5), F(17, 5))
    candidate = slacks(1310, F(2411, 1000), F(3411, 1000))
    assert all(x >= 0 for x in source.values())
    assert all(x >= 0 for x in candidate.values())
    assert bound(1298) == SOURCE_Q
    gain = bound(1310) - SOURCE_Q
    assert gain > 0
    z, obstruction = boundary_obstruction(1311)
    assert z > 0 and obstruction > 0
    monotone = DELTA * (1 + ENERGY_GAIN) - 12 * PRESSURE
    assert monotone > 0
    return {
        "schema": "exp013-mixed-gram-parameter-cap-v1",
        "experiment": "EXP-013",
        "arithmetic": "exact-rational",
        "inputs": {"delta": str(DELTA), "pressure": str(PRESSURE), "energy_gain": str(ENERGY_GAIN)},
        "source": {"m": 1298, "tau": "12/5", "c": "17/5", "q": str(SOURCE_Q),
                   "slacks": {k: str(v) for k, v in source.items()}},
        "candidate": {"m": 1310, "tau": "2411/1000", "c": "3411/1000",
                      "q": str(bound(1310)), "q_enclosure": decimal_enclosure(bound(1310)),
                      "slacks": {k: str(v) for k, v in candidate.items()}},
        "gain": {"exact": str(gain), "enclosure": decimal_enclosure(gain)},
        "cap": {"maximum_integer_m": 1310, "first_excluded_m": 1311,
                "z": str(z), "squared_obstruction": str(obstruction),
                "q_monotonicity_numerator": str(monotone),
                "uniform_proof": "D(m) increases, 2-2a(m) decreases; exclusion at 1311 excludes every larger m"},
        "scope": "Fixed seven-point inputs and scalar clipping assembly only; global distinct-zero consequence attributed",
        "not_established": ["independent local-certificate replay", "worldwide priority", "new short-window onset", "RH"],
    }
