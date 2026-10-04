"""Exact modular Fourier controls and shifted Estermann normalization."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

from flint import acb, arb, ctx, fmpq

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(poly):
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def divide(poly, divisor):
    remainder = trim(list(poly))
    quotient = [0]*max(1, len(remainder)-len(divisor)+1)
    require(divisor[-1] == 1, "monic divisor")
    while len(remainder) >= len(divisor) and any(remainder):
        degree = len(remainder)-len(divisor)
        leading = remainder[-1]
        quotient[degree] = leading
        for j, coefficient in enumerate(divisor):
            remainder[degree+j] -= leading*coefficient
        trim(remainder)
    return trim(quotient), remainder


def modular_controls(started):
    polynomials = {}
    cases = 0
    for q in range(1, 13):
        poly = [-1]+[0]*(q-1)+[1]
        for d in range(1, q):
            if q % d == 0:
                poly, remainder = divide(poly, polynomials[d])
                require(not any(remainder), "cyclotomic exact division")
        polynomials[q] = poly
        for numerator in sorted({1 % q, (q-1) % q}):
            inverse = pow(numerator, -1, q) if q > 1 else 0
            for n in range(q):
                for m in range(q):
                    require(time.process_time()-started < 60, "CPU budget")
                    counts = [0]*q
                    for r in range(q):
                        for t in range(q):
                            counts[(numerator*r*t+n*r+m*t) % q] += 1
                    counts[(-n*m*inverse) % q] -= q
                    _, remainder = divide(counts, poly)
                    require(not any(remainder), "double Fourier phase")
                    cases += 1
    # A reversed phase must fail on a genuinely nonsymmetric q=3 case.
    q, numerator, n, m = 3, 1, 1, 1
    counts = [0]*q
    for r in range(q):
        for t in range(q):
            counts[(numerator*r*t+n*r+m*t) % q] += 1
    counts[(n*m) % q] -= q
    _, remainder = divide(counts, polynomials[q])
    require(any(remainder), "reversed inverse phase accepted")
    return {"arithmetic": "Python stdlib integer cyclotomic reduction",
            "moduli": list(range(1, 13)), "complete_residue_cases": cases,
            "reversed_inverse_phase_rejected": True}


def rat(x):
    x = F(x)
    return arb(fmpq(x.numerator, x.denominator))


def interval_controls(started):
    ctx.prec = 256
    pi = arb.pi()
    shifts = [(acb(0), acb(0)), (acb(rat(F(1, 10))), acb(rat(F(-1, 20)))),
              (acb(rat(F(1, 20)), rat(F(1, 30))), acb(rat(F(-1, 25)), rat(F(1, 40)))),
              (acb(rat(F(1, 20))), acb(rat(F(1, 20))))]
    ss = [acb(rat(F(2, 5)), rat(F(3, 4))), acb(rat(F(-1, 4)), rat(F(5, 4)))]

    def estermann(s, a, b, numerator, q, unit_only=False):
        require(time.process_time()-started < 60, "CPU budget")
        left = [(s+a).zeta(acb(rat(F(r, q)))) for r in range(1, q+1)]
        right = [(s+b).zeta(acb(rat(F(t, q)))) for t in range(1, q+1)]
        total = acb(0)
        for r in range(1, q+1):
            for t in range(1, q+1):
                if unit_only and (r % 2 == 0 or r % 3 == 0 or t % 2 == 0 or t % 3 == 0):
                    continue
                total += acb(0, 2*pi*rat(F(numerator*r*t, q))).exp()*left[r-1]*right[t-1]
        return acb(q)**(-2*s-a-b)*total

    def functional(s, a, b, numerator, q, reverse=False, wrong_shift=False):
        inverse = pow(numerator, -1, q) if q > 1 else 0
        if reverse:
            inverse = -inverse
        dual_b = b if wrong_shift else -b
        positive = estermann(1-s, -a, dual_b, inverse, q)
        negative = estermann(1-s, -a, dual_b, -inverse, q)
        factor = 2*acb(q)**(1-2*s-a-b)*acb(2*pi)**(2*s+a+b-2)*(1-s-a).gamma()*(1-s-b).gamma()
        return factor*((pi*(a-b)/2).cos()*positive-(pi*(s+(a+b)/2)).cos()*negative)

    cases = []
    for q in [1, 3, 6, 8]:
        numerator = 1 if q == 1 else q-1
        for shift_index, (a, b) in enumerate(shifts):
            for s in ss:
                direct = estermann(s, a, b, numerator, q)
                dual = functional(s, a, b, numerator, q)
                error = direct-dual
                require(error.contains(0), "shifted functional equation enclosure")
                cases.append({"q": q, "numerator": numerator, "shift_case": shift_index,
                              "s": str(s), "residual": str(error)})
    s, a, b = ss[0], shifts[1][0], shifts[1][1]
    direct = estermann(s, a, b, 1, 3)
    require(not (direct-functional(s, a, b, 1, 3, reverse=True)).contains(0), "inverse phase mutation accepted")
    require(not (direct-functional(s, a, b, 1, 3, wrong_shift=True)).contains(0), "dual shift mutation accepted")
    require(not (estermann(s, a, b, 1, 6)-estermann(s, a, b, 1, 6, unit_only=True)).contains(0), "nonunit deletion accepted")
    return {"precision_bits": 256, "cases": cases,
            "negative_controls": {"inverse_phase_reversal_rejected": True,
                                  "dual_shift_reversal_rejected": True,
                                  "composite_nonunit_deletion_rejected": True},
            "trust": "Hurwitz and gamma paths share FLINT/Arb; uniform proof is analytic."}


def run(receipt):
    require(not receipt.exists(), "preserve previous receipt")
    started = time.process_time()
    result = {"schema": "exp027-shifted-voronoi-controls-v1", "passed": False,
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "hypothesis_sha256": hashlib.sha256((HERE / "hypothesis.md").read_bytes()).hexdigest()}
    try:
        result["exact_modular"] = modular_controls(started)
        print(json.dumps({"event": "exact-modular-pass", "cases": result["exact_modular"]["complete_residue_cases"]}), flush=True)
        result["interval_functional_equation"] = interval_controls(started)
        result["passed"] = True
    except ValueError as error:
        result["failure"] = str(error)
    result["cpu_seconds"] = time.process_time()-started
    result["scope"] = "Normalization controls only; no signed average, new moment range or onset gain."
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    raise SystemExit(run(parser.parse_args().receipt))
