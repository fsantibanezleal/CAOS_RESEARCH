"""Independent integer/polynomial auditor, without the producer's imports."""

import argparse
import hashlib
import json
from pathlib import Path
import sympy as s


def audit(payload: dict) -> dict:
    h, k, r = s.symbols("h k r", integer=True)
    assert s.expand(h*(k*r+1)-k*(h*r+1)) == h-k
    checked = 0
    for row in payload["cases"]:
        B, a, b, d = (row[key] for key in ("B", "a", "b", "d"))
        H = B**d
        hh, kk = B**b, B**b-1
        mm, nn = kk*B**(a-b)+1, hh*B**(a-b)+1
        assert hh*mm-kk*nn == 1
        assert [int(row[x]) for x in ("h", "k", "m", "n")] == [hh, kk, mm, nn]
        assert row["hm_minus_kn"] == 1 and int(row["H"]) == H
        assert int(row["T"]) == 16*B**(2*a)
        assert mm*nn < 2*B**(2*a)
        assert s.Rational(row["product_over_T"]) == s.Rational(mm*nn, 16*B**(2*a))
        lo, hi = s.Rational(H, hh*mm), s.Rational(H, kk*nn)
        assert s.Rational(row["phase_lower"]) == lo
        assert s.Rational(row["phase_upper"]) == hi
        expected = d-a-b
        assert expected == row["scale_exponent"]
        assert row["limit"] == ("zero" if expected < 0 else "one" if expected == 0 else "infinity")
        assert s.Rational(row["theta"]) == s.Rational(d, 2*a)
        assert s.Rational(row["nu"]) == s.Rational(b, 2*a)
        assert hi/s.Integer(B)**expected == 1/((1-s.Rational(1,B**b))*(1+s.Rational(1,B**a)))
        assert s.Rational(row["upper_over_scale"]) == hi/s.Integer(B)**expected
        # Swapping numerator and denominator reverses the logarithmic phase,
        # but not its absolute magnitude or its scale.
        assert kk*nn-hh*mm == -1
        checked += 1
    assert checked == 9
    x = s.symbols("x", nonnegative=True)
    assert s.simplify(s.diff(x-s.log(1+x), x)-x/(1+x)) == 0
    assert s.simplify(s.diff(s.log(1+x)-x/(1+x), x)) == x/(1+x)**2
    return {"schema": "exp014-independent-audit-v1", "passed": True,
            "route": "independent Bezout expansion and derivatives of both logarithm bounds",
            "cases_checked": checked, "summed_mollifier_barrier_established": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.artifact.read_bytes()
    payload = json.loads(raw)
    root = Path(__file__).resolve().parents[5]
    for path, expected in payload["bindings"].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == expected, path
    result = audit(payload)
    result["result_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(result, indent=2, sort_keys=True)+"\n").encode())
    print("EXP-014 independent audit passed", flush=True)


if __name__ == "__main__":
    main()
