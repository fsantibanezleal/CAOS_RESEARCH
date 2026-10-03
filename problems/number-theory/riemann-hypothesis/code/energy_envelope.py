"""Exact sharp clipping envelope and pinned source-based consequence."""

from fractions import Fraction as F
from math import isqrt, sqrt

from mixed_gram_parameters import DELTA, ENERGY_GAIN, PRESSURE, SOURCE_Q, decimal_enclosure

EXP016_Q = F(69341429073721, 82845897125000)


def sqrt_bracket(value, digits=40):
    value = F(value)
    if value < 0 or not isinstance(digits, int) or digits < 1:
        raise ValueError("nonnegative radicand and positive integer precision required")
    scale = 10**digits
    k = isqrt(value.numerator * scale**2 // value.denominator)
    lo = F(k, scale)
    hi = lo if lo**2 == value else F(k+1, scale)
    assert lo**2 <= value <= hi**2
    return lo, hi


def envelope_bracket(m, tau, energy):
    if not isinstance(m, int) or isinstance(m, bool) or m < 2:
        raise ValueError("integer dimension at least two required")
    tau, energy = F(tau), F(energy)
    if tau <= 0 or energy < 0:
        raise ValueError("positive clipping threshold and nonnegative energy required")
    A = F(m-1, m)
    if A*energy <= tau*tau:
        return energy, energy
    lo, hi = sqrt_bracket(A*energy)
    return energy/m+2*tau*lo-tau*tau, energy/m+2*tau*hi-tau*tau


def clipped(x, tau):
    return x*x if x <= tau else 2*tau*x-tau*tau


def candidate(m, tau):
    if m < 7:
        raise ValueError("source block needs dimension at least seven")
    tau = F(tau)
    c = 1+tau
    D = DELTA*(m-6)
    flo, fhi = envelope_bracket(m, tau, D)
    a = flo/m
    beta = 6*PRESSURE*F(m-6, m)
    values = {
        "unit_diagonal_threshold": c-1-tau,
        "double_diagonal_threshold": c-2-tau/2,
        "high_multiplicity_residual": 6*c-7-c*c-a,
        "off_line_pair_residual": 4*c-2-c*c-2*a,
    }
    if min(values.values()) < 0:
        return None
    q = (1+ENERGY_GAIN-beta)/(2-a)
    return {"m": m, "tau": str(tau), "c": str(c), "D": str(D),
            "envelope_lower": str(flo), "envelope_upper": str(fhi),
            "a": str(a), "beta": str(beta), "q": str(q),
            "q_enclosure": decimal_enclosure(q),
            "slacks": {k: str(v) for k, v in values.items()}}


def locate_candidate(m):
    # Floats locate only; candidate() accepts all decisions over rationals.
    D = float(DELTA)*(m-6)
    A = (m-1)/m

    def residual(t):
        f = D if A*D <= t*t else D/m+2*t*sqrt(A*D)-t*t
        return 1+2*t-t*t-2*f/m

    low, high = 2.410, 2.413
    if residual(low) < 0:
        return None
    for _ in range(60):
        mid = (low+high)/2
        if residual(mid) >= 0:
            low = mid
        else:
            high = mid
    # Round downward and validate; one extra predecessor covers float ties.
    ticks = int(low*10**6)
    return candidate(m, F(ticks, 10**6)) or candidate(m, F(ticks-1, 10**6))


def certificate():
    rows = [row for m in range(1300, 1351) if (row := locate_candidate(m)) is not None]
    best = max(rows, key=lambda row: F(row["q"]))
    q = F(best["q"])
    assert q > EXP016_Q > SOURCE_Q
    controls = []
    for m, tau, s in [(2, F(1,2), F(1,4)), (7, F(1), F(1)),
                      (7, F(1), F(3)), (7, F(1), F(6))]:
        xs = [s]+[-s/F(m-1)]*(m-1)
        E = sum(x*x for x in xs)
        lo, hi = envelope_bracket(m, tau, E)
        value = sum(clipped(x, tau) for x in xs)
        assert lo == value == hi and min(1+x for x in xs) >= 0
        controls.append({"m": m, "tau": str(tau), "s": str(s),
                         "energy": str(E), "clipped_energy": str(value),
                         "displacements": [str(x) for x in xs]})
    return {"schema": "exp017-sharp-energy-envelope-v1", "experiment": "EXP-017",
            "candidate": best, "candidate_count": len(rows),
            "search": {"m_min": 1300, "m_max": 1350, "tau_denominator": 10**6,
                       "global_optimality_claimed": False},
            "gain_over_exp016": str(q-EXP016_Q), "gain_over_source": str(q-SOURCE_Q),
            "sharp_controls": controls,
            "arithmetic": "exact rational decisions; floats locate only",
            "source_inputs": {"delta": str(DELTA), "pressure": str(PRESSURE),
                              "energy_gain": str(ENERGY_GAIN)},
            "scope": "Sharp zero-sum clipping envelope and attributed distinct-strip consequence",
            "not_established": ["worldwide novelty", "source certificate independently replayed",
                                "global parameter optimum", "new short-window onset", "RH"]}
