"""Bound one attributed local certificate and independently audit its lift."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import time

from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent
SOURCE_SHA = "65564079527487fde93b43bb83dd840a768acf9fb8db1f1f015d38c4faf3b7d4"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def as_arb(value):
    return arb(fmpq(value.numerator, value.denominator))


def source_packet(raw):
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, "attributed source bytes")
    text = raw.decode("utf-8")
    coeff_text = text.split("def cAMn : ℕ → ℤ", 1)[1].split("/-- the window coefficients", 1)[0]
    coefficients = {int(j): int(n) for j, n in re.findall(r"\| (\d+) => (-?\d+)", coeff_text)}
    require(set(coefficients) == set(range(13)), "window coefficient index domain")
    pairs_text = text.split("def aW7 : Fin 7 → Fin 7 → ℝ", 1)[1].split("def bW7", 1)[0]
    pairs = {(int(i), int(j)): Fraction(int(n), 100000000)
             for i, j, n in re.findall(r"\| (\d+), (\d+) => \((\d+) : ℝ\) / 100000000", pairs_text)}
    pressures_text = text.split("def bW7 : Fin 6 → ℝ", 1)[1].split("def W7", 1)[0]
    pressures = {int(i): Fraction(int(n), 100000000)
                 for i, n in re.findall(r"\| (\d+) => \((\d+) : ℝ\) / 100000000", pressures_text)}
    require(set(pairs) == {(i, j) for i in range(7) for j in range(i+1, 7)}, "pair index domain")
    require(set(pressures) == set(range(6)), "gap pressure index domain")
    functional = text.split("def G (g0 g1 g2 g3 g4 g5 : ℝ) : ℝ :=", 1)[1].split("/-- early exit", 1)[0]
    functional_pressures = {int(i): Fraction(int(n), 100000000)
        for n, i in re.findall(r"\((\d+) / \(SA:ℝ\)\) \* g(\d)", functional)}
    functional_pairs = {}
    for n, gap_sum in re.findall(r"\((\d+) / \(SA:ℝ\)\) \* wfun \(([^)]+)\)", functional):
        indices = [int(s[1:]) for s in gap_sum.split(" + ")]
        require(indices == list(range(indices[0], indices[-1]+1)), "nonconsecutive pair span")
        functional_pairs[indices[0], indices[-1]+1] = Fraction(int(n), 100000000)
    require(pairs == functional_pairs and pressures == functional_pressures, "source functional mismatch")
    require("def SA : ℕ := 100000000" in text and "def cN : ℕ := 787380" in text and
            "theorem cert_AM : ∀ g : Fin 6 → ℝ" in text, "source local target/interface")
    return [Fraction(coefficients[j], 10**9) for j in range(13)], pairs, [pressures[i] for i in range(6)]


def capacities(pairs):
    require(all(weight >= 0 for weight in pairs.values()), "negative pair weight")
    values = [sum((value for (i, j), value in pairs.items() if j-i == span), Fraction(0)) for span in range(1, 7)]
    require(all(value <= 2 for value in values), "span capacity")
    return values


def certify_window(coefficients):
    ctx.prec = 256
    cs = [as_arb(c) for c in coefficients]
    ws = [arb(2).sqrt()]+[2*j*arb.pi() for j in range(1, 13)]

    def inner(a, b):
        return (((a-b)/2).sinc()+((a+b)/2).sinc())/2

    def absolute_inner(a, b):
        return ((a/2).sin()/a+2*(a/2).cos()/(a*a))*(b/2).sinc()-2*inner(a, b)/(a*a)

    i1 = sum((c*(a/2).sinc() for c, a in zip(cs, ws)), arb(0))
    i2 = arb(0)
    j_value = arb(0)
    for ci, ai in zip(cs, ws):
        for cj, aj in zip(cs, ws):
            i2 += ci*cj*inner(ai, aj)
            ab, ba = absolute_inner(ai, aj), absolute_inner(aj, ai)
            require((ab-ba).contains(0), "absolute-integral symmetry")
            j_value += ci*cj*(ab+ba)/2
    positive_lower = (arb(2).sqrt()/2).cos()-sum((arb(c.abs_upper()) for c in cs[1:]), arb(0))
    require(positive_lower > 0 and i1 > 0, "window positive normalization")
    h = 2-(i2+j_value)/(i1*i1)
    hcert = Fraction(67217109258, 10**11)
    require(h >= as_arb(hcert), "independent window constant")
    penalty = sum((cs[j]**2*(arb(1)/2-1/(4*arb.pi()**2*j*j)) for j in range(1, 13)), arb(0))
    theta = arb(2).sqrt()/2
    source_h = arb(3)/2-theta.cos()/(arb(2).sqrt()*theta.sin())-penalty/(2*theta.sin()**2)
    require((h-source_h).contains(0), "source/independent energy expression")
    return hcert, h, {"precision_bits": 256, "I1": str(i1), "I2": str(i2), "J": str(j_value),
                     "H": str(h), "H_cert": str(hcert), "positive_window_lower": str(positive_lower),
                     "independent_source_formula_agrees": True, "symmetry_checks": 169}


def transfer(h, delta, pressure_sum):
    r, m = 6, 742
    tau, c = Fraction(12043, 5000), Fraction(17043, 5000)
    u = Fraction(m-r, m)
    d = delta*(m-r)
    a, beta = delta*u, pressure_sum*u
    residuals = {"block": tau*tau-d, "threshold1": c-1-tau,
                 "threshold2": c-2-tau/2, "high_multiplicity": 6*c-7-c*c-a,
                 "off_line": 4*c-2-c*c-2*a, "denominator": 2-a}
    require(all(value >= 0 for value in residuals.values()) and residuals["denominator"] > 0, "exact block/threshold residual")
    q = (1+h-beta)/(2-a)
    require(q-Fraction(836993, 10**6) > Fraction(1, 10000), "declared gain gate against conservative prior ceiling")
    return {"r": r, "m": m, "tau": str(tau), "c": str(c), "delta": str(delta),
            "pressure_sum": str(pressure_sum), "D": str(d), "a": str(a), "beta": str(beta),
            "residuals": {key: str(value) for key, value in residuals.items()},
            "liminf_fraction": str(q), "decimal_for_display_only": float(q),
            "gain_over_0_836993": str(q-Fraction(836993, 10**6))}


def run(source):
    start = time.monotonic()
    raw = source.read_bytes()
    coefficients, pairs, pressures = source_packet(raw)
    spans = capacities(pairs)
    require(all(value > 0 for value in pressures), "nonpositive gap pressure")
    pressure_sum = sum(pressures, Fraction(0))
    require(pressure_sum == Fraction(398386, 10**8), "source total pressure")
    require(all(pairs[i, j] == pairs[6-j, 6-i] for i, j in pairs) and pressures == pressures[::-1], "source reflection")
    hcert, h, window = certify_window(coefficients)
    delta = Fraction(787380, 10**8)
    result = transfer(hcert, delta, pressure_sum)
    controls = {}
    try:
        source_packet(raw+b"\n")
    except ValueError as error:
        controls["changed_source_rejected"] = str(error) == "attributed source bytes"
    bad_pairs = dict(pairs)
    bad_pairs[0, 6] += 1
    try:
        capacities(bad_pairs)
    except ValueError as error:
        controls["increased_pair_capacity_rejected"] = str(error) == "span capacity"
    controls["inflated_window_constant_rejected"] = not (h >= as_arb(hcert+Fraction(1, 1000)))
    try:
        transfer(hcert, delta+Fraction(1, 100), pressure_sum)
    except ValueError as error:
        controls["inflated_local_target_block_rejected"] = str(error) == "exact block/threshold residual"
    require(len(controls) == 4 and all(controls.values()), "negative control failure")
    require(time.monotonic()-start < 30, "declared preflight budget")
    return {"schema": "exp025-vector-pressure-preflight-v1", "passed_preflight": True,
            "unconditional_consequence_asserted": False, "full_transfer_review_complete": False,
            "external_local_formalization_rebuilt_here": False, "source_sha256": SOURCE_SHA,
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "hypothesis_sha256": hashlib.sha256((HERE/"hypothesis.md").read_bytes()).hexdigest(),
            "window_coefficients": [str(x) for x in coefficients],
            "pairs": [{"i": i, "j": j, "weight": str(value)} for (i, j), value in sorted(pairs.items())],
            "gap_pressures": [str(x) for x in pressures], "span_capacities": [str(x) for x in spans],
            "window": window, "conditional_transfer": result, "negative_controls": controls,
            "elapsed_seconds": time.monotonic()-start,
            "scope": "source-array binding, independent window constant and exact fixed transfer preflight; external local theorem attributed; full proof/overlap review pending"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    require(not args.receipt.exists(), "preserve previous receipt")
    result = run(args.source)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
