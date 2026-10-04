"""Independent scalar minorant and rational consequence; no producer imports."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time

import sympy as sy


def above_envelope(m, tau, energy, value):
    A = sy.Rational(m-1, m)
    if A*energy <= tau*tau:
        return value >= energy
    t = value-energy/m+tau*tau
    return t >= 0 and t*t >= 4*tau*tau*A*energy


def audit(data):
    started = time.monotonic()
    nminus, s, tau, x, e = sy.symbols("nminus s tau x e", positive=True)
    m = nminus+1
    r = -s/(m-1)
    b = (s-tau)**2/(s-r)**2
    lam, mu, kap = 1-b, 2*b*r, -b*r*r
    low = x*x-lam*x*x-mu*x-kap
    high = 2*tau*x-tau*tau-lam*x*x-mu*x-kap
    assert sy.simplify(low-b*(x-r)**2) == 0
    assert sy.simplify(high.subs(x, s)) == 0
    assert sy.simplify(high-(s-x)/(s-tau)*low.subs(x,tau)-lam*(x-tau)*(s-x)) == 0
    energy = s*s*m/(m-1)
    assert sy.simplify(lam*energy-m*b*r*r-(energy-(s-tau)**2)) == 0
    A = (m-1)/m
    expr = e/m+2*tau*sy.sqrt(A*e)-tau*tau
    assert sy.simplify(expr.subs(e,tau*tau/A)-tau*tau/A) == 0
    assert sy.simplify(sy.diff(expr,e).subs(e,tau*tau/A)-1) == 0
    assert sy.simplify(sy.diff(expr,e,2)+tau*sy.sqrt(A)/(2*e**sy.Rational(3,2))) == 0
    assert data["schema"] == "exp017-sharp-energy-envelope-v1"
    row = data["candidate"]
    mm = row["m"]
    tt, c = sy.Rational(row["tau"]), sy.Rational(row["c"])
    assert mm == 1317 and tt == sy.Rational(1205537,500000) and c == 1+tt
    delta, p, h0 = sy.Rational(891,200000), sy.Rational(1,2736), sy.Rational(3362285207,5000000000)
    assert data["source_inputs"] == {"delta": str(delta), "pressure": str(p), "energy_gain": str(h0)}
    D, aa = delta*(mm-6), sy.Rational(row["a"])
    flo, fhi = sy.Rational(row["envelope_lower"]), sy.Rational(row["envelope_upper"])
    assert sy.Rational(row["D"]) == D and aa == flo/mm
    assert D*sy.Rational(mm-1,mm) > tt*tt
    slo, shi = (flo-D/mm+tt*tt)/(2*tt), (fhi-D/mm+tt*tt)/(2*tt)
    assert slo > 0 and slo*slo <= D*sy.Rational(mm-1,mm) <= shi*shi
    assert shi-slo == sy.Rational(1,10**40)
    beta = 6*p*sy.Rational(mm-6,mm)
    q = (1+h0-beta)/(2-aa)
    assert sy.Rational(row["beta"]) == beta and sy.Rational(row["q"]) == q
    values = {"unit_diagonal_threshold": c-1-tt, "double_diagonal_threshold": c-2-tt/2,
              "high_multiplicity_residual": 6*c-7-c*c-aa,
              "off_line_pair_residual": 4*c-2-c*c-2*aa}
    for k,v in values.items():
        assert v >= 0 and sy.Rational(row["slacks"][k]) == v
    prev, source = sy.Rational(69341429073721,82845897125000), sy.Rational(16260119298029,19426831050000)
    assert sy.Rational(data["gain_over_exp016"]) == q-prev > 0
    assert sy.Rational(data["gain_over_source"]) == q-source > 0
    enc = row["q_enclosure"]
    assert sy.Rational(enc["lower"]) <= q <= sy.Rational(enc["upper"])
    assert sy.Rational(enc["upper"])-sy.Rational(enc["lower"]) == sy.Rational(enc["width"]) == sy.Rational(1,10**50)
    assert data["search"]["global_optimality_claimed"] is False
    assert data["search"]["m_min"] == 1300 and data["search"]["m_max"] == 1350
    assert data["candidate_count"] == 51
    for control in data["sharp_controls"]:
        n, t, ss = control["m"], sy.Rational(control["tau"]), sy.Rational(control["s"])
        xs = list(map(sy.Rational,control["displacements"]))
        assert xs == [ss]+[-ss/(n-1)]*(n-1) and sum(xs) == 0
        U = (1-ss/(n-1))*sy.eye(n)+ss/(n-1)*sy.ones(n)
        assert list(U.diagonal()) == [1]*n
        assert U.eigenvals() == {1+ss:1,1-ss/(n-1):n-1}
        assert min(U.eigenvals()) >= 0
        ee = sum(y*y for y in xs)
        vv = sum(y*y if y <= t else 2*t*y-t*t for y in xs)
        assert sy.Rational(control["energy"]) == ee and sy.Rational(control["clipped_energy"]) == vv
        ff = ee if ss <= t else ee/n+2*t*ss-t*t
        assert ff == vv
    # Deterministic exact stress vectors; the proof, not this family,
    # establishes universality. Multi-clipped entries are included.
    count = 0
    for n in range(2,7):
        for prefix in itertools.product([sy.Rational(-1),sy.Rational(-1,2),sy.Rational(0),sy.Rational(1,2),sy.Rational(1)], repeat=n-1):
            xs = list(prefix)+[-sum(prefix)]
            for t in [sy.Rational(1,4),sy.Rational(1),sy.Rational(2)]:
                ee = sum(y*y for y in xs)
                vv = sum(y*y if y <= t else 2*t*y-t*t for y in xs)
                assert above_envelope(n,t,ee,vv)
                count += 1
    assert not above_envelope(7,sy.Rational(1),sy.Rational(9),sy.Rational(5))
    # Negative pressure breaks the Lipschitz transfer at large energy.
    # At n=2,tau=1,E=8,D=2,pW=-6 the premise holds but F(E)+pW=-1<D.
    assert 8-6 == 2 and (8/sy.Integer(2)+2*2-1)-6 < 2
    if time.monotonic()-started > 60:
        raise TimeoutError("audit budget exceeded")
    return {"schema": "exp017-independent-audit-v1", "passed": True,
            "route": "scalar quadratic minorant on the energy-constrained range",
            "exact_stress_checks": count, "candidate_q": str(q),
            "uniform_proof": "proof.md; finite stress alone is insufficient",
            "source_inputs_independently_replayed": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    raw = args.artifact.read_bytes()
    data = json.loads(raw)
    root = Path(__file__).resolve().parents[5]
    for path, expected in data["bindings"].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == expected
    report = audit(data)
    report["result_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes((json.dumps(report,indent=2,sort_keys=True)+"\n").encode())
    print("EXP-017 independent audit passed",flush=True)


if __name__ == "__main__":
    main()
