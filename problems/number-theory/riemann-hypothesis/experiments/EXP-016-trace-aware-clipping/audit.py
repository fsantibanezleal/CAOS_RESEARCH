"""Independent symbolic derivation of trace convexity, cap and count."""

import argparse
import hashlib
import json
from pathlib import Path
import time

import sympy as s


def audit(data):
    started = time.monotonic()
    m, tau, x = s.symbols("m tau x", positive=True)
    expression = 2*tau*x-tau**2+x**2/(m-1)
    assert s.factor(expression.subs(x,tau)) == m*tau**2/(m-1)
    assert s.diff(expression,x) == 2*tau+2*x/(m-1)
    delta, p, h0 = s.Rational(891,200000),s.Rational(1,2736),s.Rational(3362285207,5000000000)
    a, beta = delta*(1-6/m),6*p*(1-6/m)
    D = delta*(m-6)*(m-1)/m
    assert s.simplify(s.diff(D,m)-delta*(m*m-6)/(m*m)) == 0
    assert s.factor(s.diff(a,m)) == 6*delta/m**2
    q = (1+h0-beta)/(2-a)
    assert delta*(1+h0)-12*p > 0
    row = data["candidate"]
    assert row["m"] == 1311 and s.Rational(row["tau"]) == s.Rational(2411,1000)
    assert s.Rational(row["c"]) == s.Rational(3411,1000)
    tt, c = s.Rational(row["tau"]),s.Rational(row["c"])
    aa = a.subs(m,1311)
    values = {"tau_nonnegative": tt,"block_clipping": tt**2-D.subs(m,1311),
              "unit_diagonal_threshold":c-1-tt,"double_diagonal_threshold":c-2-tt/2,
              "high_multiplicity_residual":6*c-7-c*c-aa,
              "off_line_pair_residual":4*c-2-c*c-2*aa}
    for key,value in values.items():
        assert value >= 0 and value == s.Rational(row["slacks"][key])
    improved = s.factor(q.subs(m,1311))
    assert s.Rational(row["q"]) == improved
    assert improved-q.subs(m,1310) == s.Rational(data["gain_over_exp013"]) > 0
    assert improved-q.subs(m,1298) == s.Rational(data["gain_over_source"]) > 0
    enc = row["q_enclosure"]
    assert s.Rational(enc["lower"]) <= improved <= s.Rational(enc["upper"])
    assert s.Rational(enc["upper"])-s.Rational(enc["lower"]) == s.Rational(enc["width"]) == s.Rational(1,10**50)
    cap = data["cap"]
    assert cap["maximum_integer_m"] == 1311 and cap["first_excluded_m"] == 1312
    z = D-3+2*a
    obstruction = s.factor(z*z-4*(2-2*a))
    assert s.Rational(cap["z"]) == z.subs(m,1312) > 0
    assert s.Rational(cap["squared_obstruction"]) == obstruction.subs(m,1312) > 0
    control = data["sharp_control"]
    mm, t = control["m"],s.Rational(control["tau"])
    xs = list(map(s.Rational,control["displacements"]))
    assert mm == 7 and t == s.Rational(12,5)
    assert xs == [t]+[-t/(mm-1)]*(mm-1) and sum(xs) == 0
    U = (1-t/(mm-1))*s.eye(mm)+t/(mm-1)*s.ones(mm)
    assert list(U.diagonal()) == [1]*mm
    assert U.eigenvals() == {1+t:1,1-t/(mm-1):mm-1}
    assert all(value >= 0 for value in U.eigenvals())
    sharp = t*t*mm/(mm-1)
    assert sum(v*v for v in xs) == s.Rational(control["energy"]) == s.Rational(control["bound"]) == sharp
    assert s.Rational(control["off_diagonal_entry"]) == t/(mm-1)
    missing = data["missing_trace_control"]
    assert list(map(s.Rational,missing["displacements"])) == [t]+[0]*(mm-1)
    assert s.Rational(missing["energy"]) == t*t < sharp
    assert missing["violates_stronger_bound"] is True
    assert data["block_requirement"] == "delta(m-6)<=tau^2*m/(m-1)"
    if time.monotonic()-started > 30:
        raise TimeoutError("independent audit budget exceeded")
    return {"schema":"exp016-independent-audit-v1","passed":True,
            "route":"independent Jensen scalar derivative, matrix eigenvalues and rational cap",
            "q":str(improved),"first_excluded_m":1312,"analytic_inputs_independently_replayed":False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    raw = args.artifact.read_bytes()
    data = json.loads(raw)
    root = Path(__file__).resolve().parents[5]
    for path,expected in data["bindings"].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == expected
    report = audit(data)
    report["result_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes((json.dumps(report,indent=2,sort_keys=True)+"\n").encode())
    print("EXP-016 independent audit passed",flush=True)


if __name__ == "__main__":
    main()
