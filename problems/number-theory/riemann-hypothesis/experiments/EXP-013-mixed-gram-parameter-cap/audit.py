"""Independent SymPy derivation; does not import the producer."""

import argparse
import hashlib
import json
from pathlib import Path
import time

import sympy as s


def audit(payload: dict) -> dict:
    started = time.monotonic()
    m = s.symbols("m", positive=True)
    delta, p, h0 = s.Rational(891, 200000), s.Rational(1, 2736), s.Rational(3362285207, 5000000000)
    t = 1 - 6 / m
    a, beta = delta * t, 6 * p * t
    q = (1 + h0 - beta) / (2 - a)
    assert s.factor(s.diff(q, m)) == s.factor(6 * (delta * (1 + h0) - 12 * p) / (m * m * (2 - a)**2))
    assert delta * (1 + h0) - 12 * p > 0
    published = s.Rational(16260119298029, 19426831050000)
    assert q.subs(m, 1298) == published
    improved = s.factor(q.subs(m, 1310))
    assert s.Rational(payload["candidate"]["q"]) == improved
    assert s.Rational(payload["source"]["q"]) == published
    assert s.Rational(payload["inputs"]["delta"]) == delta
    assert s.Rational(payload["inputs"]["pressure"]) == p
    assert s.Rational(payload["inputs"]["energy_gain"]) == h0
    assert payload["candidate"]["m"] == 1310
    assert payload["cap"]["maximum_integer_m"] == 1310
    assert payload["source"]["m"] == 1298
    assert s.Rational(payload["source"]["tau"]) == s.Rational(12, 5)
    assert s.Rational(payload["source"]["c"]) == s.Rational(17, 5)
    tau, c = s.Rational(payload["candidate"]["tau"]), s.Rational(payload["candidate"]["c"])
    aa = a.subs(m, 1310)
    checks = {"tau_nonnegative": tau, "block_clipping": tau**2 - delta * 1304,
              "unit_diagonal_threshold": c - 1 - tau,
              "double_diagonal_threshold": c - 2 - tau / 2,
              "high_multiplicity_residual": 6*c - 7 - c**2 - aa,
              "off_line_pair_residual": 4*c - 2 - c**2 - 2*aa}
    for key, value in checks.items():
        assert value >= 0 and value == s.Rational(payload["candidate"]["slacks"][key])
    z = delta * (m - 6) - 3 + 2 * a
    obstruction = s.factor(z*z - 4*(2 - 2*a))
    assert z.subs(m, 1311) > 0 and obstruction.subs(m, 1311) > 0
    assert payload["cap"]["first_excluded_m"] == 1311
    assert s.Rational(payload["cap"]["z"]) == z.subs(m, 1311)
    assert s.Rational(payload["cap"]["squared_obstruction"]) == obstruction.subs(m, 1311)
    assert s.Rational(payload["cap"]["q_monotonicity_numerator"]) == delta*(1+h0)-12*p
    assert s.diff(delta * (m - 6), m) > 0
    assert s.factor(s.diff(a, m)) == 6 * delta / m**2
    gain = improved - published
    assert gain == s.Rational(payload["gain"]["exact"]) and gain > 0
    for value, enc in ((improved, payload["candidate"]["q_enclosure"]), (gain, payload["gain"]["enclosure"])):
        assert s.Rational(enc["lower"]) <= value <= s.Rational(enc["upper"])
        assert s.Rational(enc["upper"]) - s.Rational(enc["lower"]) == s.Rational(enc["width"])
    if time.monotonic() - started > 30:
        raise TimeoutError("independent audit exceeded budget")
    return {"schema": "exp013-independent-audit-v1", "passed": True,
            "route": "SymPy differentiation and independent rational substitution",
            "q": str(improved), "gain": str(gain), "first_excluded_m": 1311,
            "boundary_polynomial": str(obstruction),
            "analytic_inputs_independently_replayed": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.artifact.read_bytes()
    payload = json.loads(raw)
    root = Path(__file__).resolve().parents[5]
    for path, expected in payload["bindings"].items():
        assert hashlib.sha256((root / path).read_bytes()).hexdigest() == expected, path
    result = audit(payload)
    result["result_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(result, indent=2, sort_keys=True) + "\n").encode())
    print("EXP-013 independent audit passed", flush=True)


if __name__ == "__main__":
    main()
