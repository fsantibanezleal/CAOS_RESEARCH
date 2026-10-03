"""Trace-aware refinement of the attributed clipped-block assembly."""

from fractions import Fraction as F

from mixed_gram_parameters import DELTA, SOURCE_Q, bound, coefficients, decimal_enclosure, slacks


def trace_slacks(m, tau, c):
    result = slacks(m, tau, c)
    result["block_clipping"] = tau*tau-DELTA*F((m-6)*(m-1), m)
    return result


def trace_boundary(m):
    a, _ = coefficients(m)
    z = DELTA*F((m-6)*(m-1), m)-3+2*a
    return z, z*z-4*(2-2*a)


def clipped(x, tau):
    return x*x if x <= tau else 2*tau*x-tau*tau


def certificate():
    m, tau, c = 1311, F(2411, 1000), F(3411, 1000)
    values = trace_slacks(m, tau, c)
    assert all(value >= 0 for value in values.values())
    q = bound(m)
    assert q > bound(1310) > SOURCE_Q
    z, obstruction = trace_boundary(1312)
    assert z > 0 and obstruction > 0
    # PSD unit-diagonal equicorrelation matrix: one high displacement
    # and all complementary displacements equal and negative.
    example_m, example_tau = 7, F(12, 5)
    xs = [example_tau] + [-example_tau/F(example_m-1)]*(example_m-1)
    assert sum(xs) == 0 and all(1+x >= 0 for x in xs)
    energy = sum(clipped(x, example_tau) for x in xs)
    sharp = example_tau**2*F(example_m, example_m-1)
    assert energy == sharp
    control = [example_tau]+[F()]*(example_m-1)
    assert sum(clipped(x, example_tau) for x in control) < sharp
    return {
        "schema": "exp016-trace-aware-clipping-v1", "experiment": "EXP-016",
        "arithmetic": "exact-rational-and-symbolic",
        "candidate": {"m": m, "tau": str(tau), "c": str(c),
                      "q": str(q), "q_enclosure": decimal_enclosure(q),
                      "slacks": {key: str(value) for key, value in values.items()}},
        "gain_over_exp013": str(q-bound(1310)), "gain_over_source": str(q-SOURCE_Q),
        "cap": {"maximum_integer_m": 1311, "first_excluded_m": 1312,
                "z": str(z), "squared_obstruction": str(obstruction)},
        "sharp_control": {"m": example_m, "tau": str(example_tau),
                          "displacements": [str(x) for x in xs], "energy": str(energy),
                          "bound": str(sharp), "off_diagonal_entry": str(example_tau/F(example_m-1))},
        "missing_trace_control": {"displacements": [str(x) for x in control],
                                  "energy": str(example_tau**2), "violates_stronger_bound": True},
        "block_requirement": "delta(m-6)<=tau^2*m/(m-1)",
        "scope": "Trace-aware block dichotomy with the same attributed analytic/local inputs",
        "not_established": ["new matrix-method priority", "full external certificate replay", "new short-window onset", "RH"],
    }
