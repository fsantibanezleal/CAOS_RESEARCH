"""Native-free conditional parity and source-bound exponent audit."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import isqrt
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
SCALE = 10**65
DETECTOR_SHA = "74ed14a925bdd10f27d09d6fb23a8e43f9474f8e0e5280fceafac33e06f49464"


def audit():
    started = time.process_time()
    toolkit = HERE.parent / "EXP-026-multiplicity-defect-retention/independent_compact.py"
    spec = importlib.util.spec_from_file_location("rational_intervals026", toolkit)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    interval, trig = module.Interval, module.trig

    def sqrt_interval(value):
        assert value.lo >= 0
        low = isqrt(value.lo.numerator*SCALE*SCALE//value.lo.denominator)
        high = isqrt(value.hi.numerator*SCALE*SCALE//value.hi.denominator)+1
        assert F(low, SCALE)**2 <= value.lo and F(high, SCALE)**2 >= value.hi
        return interval(F(low, SCALE), F(high, SCALE))

    detector = HERE.parent / "EXP-010-levinson-parity-transfer/artifacts/canonical/result.json"
    raw = detector.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == DETECTOR_SHA
    receipt = json.loads(raw)
    theta, nu = F(5339, 10000), F(349, 10000)
    entry = next(x for x in receipt["detector_constants"] if F(x["nu"]) == nu)
    kappa = F(entry["kappa"]["lower"])
    # Independently add the actual normalization, coefficient norms,
    # one-variable separation and the two source theorem monomials.
    p, q, dual_n = nu, nu, 1+2*nu-2*theta
    normalization = -F(3, 4)*(p+q)-F(1, 4)
    coefficient_norms = F(1, 2)*(p+q)+F(1, 4)*dual_n
    separation = F(1, 4)*(dual_n+1-p-q)
    theorem_first = F(7, 20)*(dual_n+p+q)+F(1, 4)*max(p, q)
    theorem_second = F(3, 8)*(dual_n+p+q)+F(1, 8)*(dual_n+max(p, q))
    e1 = normalization+coefficient_norms+separation+theorem_first
    e2 = normalization+coefficient_norms+separation+theorem_second
    assert e1 == F(-9, 200000) and e2 == F(-189, 80000)
    assert e1 < 0 and e2 < 0
    assert not nu < theta-F(1, 2)
    assert e1+separation > 0 and e2+separation > 0
    root2 = sqrt_interval(interval(2))
    sine, cosine = trig(interval(theta)/root2)
    pair = 2-interval(theta)/2-cosine/(root2*sine)
    k = interval(kappa)
    parity = (3+k-sqrt_interval((1-k)*(9-k-8*pair)))/4
    assert parity.lo > F(3985, 10000000)
    wrong_parity = (3-sqrt_interval(9-8*pair))/4
    assert wrong_parity.hi < 0
    assert time.process_time()-started < 30
    return {"detector_receipt_sha256": DETECTOR_SHA,
            "interval_toolkit_sha256": hashlib.sha256(toolkit.read_bytes()).hexdigest(),
            "arithmetic": "Python stdlib Fraction outward intervals and integer square roots; no FLINT/Arb",
            "theta": str(theta), "nu": str(nu),
            "normalization_exponent": str(normalization),
            "coefficient_norm_exponent": str(coefficient_norms),
            "separation_exponent": str(separation),
            "source_first_exponent": str(theorem_first),
            "source_second_exponent": str(theorem_second),
            "E1": str(e1), "E2": str(e2),
            "pair_term": pair.receipt(), "conditional_parity": parity.receipt(),
            "negative_controls": {"old_length_range_rejects_nu": True,
                                  "doubled_separation_exponent_rejected": True,
                                  "zero_detector_parity_rejected": True},
            "analytic_moment_theorem_proved": False,
            "scope": "Conditional arithmetic only; no established onset improvement.",
            "cpu_seconds": time.process_time()-started}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    path = parser.parse_args().receipt
    if path.exists():
        raise SystemExit("Preserve previous receipt")
    result = {"schema": "exp028-independent-conditional-v1", "passed": False,
              "auditor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "declaration_sha256": hashlib.sha256((HERE / "independent-control-declaration.md").read_bytes()).hexdigest()}
    try:
        result["audit"] = audit()
        result["passed"] = True
    except AssertionError as error:
        result["failure"] = str(error) or "An independent obligation failed"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
    raise SystemExit(0 if result["passed"] else 1)
