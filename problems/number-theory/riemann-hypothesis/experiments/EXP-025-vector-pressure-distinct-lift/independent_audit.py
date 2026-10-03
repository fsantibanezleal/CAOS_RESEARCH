"""Stdlib rational enclosures and vector-pressure counting for EXP-025."""

from fractions import Fraction as F
import hashlib
import json
from math import factorial, isqrt
from pathlib import Path
import re
import time

HERE = Path(__file__).resolve().parent
SOURCE_SHA = "65564079527487fde93b43bb83dd840a768acf9fb8db1f1f015d38c4faf3b7d4"


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Bounds:
    def __init__(self, low, high=None):
        self.low = F(low)
        self.high = F(low if high is None else high)
        require(self.low <= self.high, "reversed interval")

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Bounds) else Bounds(value)

    def __add__(self, other):
        other = self.coerce(other)
        return Bounds(self.low+other.low, self.high+other.high)

    __radd__ = __add__

    def __neg__(self):
        return Bounds(-self.high, -self.low)

    def __sub__(self, other):
        return self+-self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other)+-self

    def __mul__(self, other):
        other = self.coerce(other)
        products = [a*b for a in [self.low, self.high] for b in [other.low, other.high]]
        return Bounds(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        require(other.low > 0 or other.high < 0, "division interval contains zero")
        return self*Bounds(1/other.high, 1/other.low)

    def __rtruediv__(self, other):
        return self.coerce(other)/self

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "invalid interval power")
        result = Bounds(1)
        for _ in range(exponent):
            result *= self
        return result

    def decimal_enclosure(self, digits=40):
        scale = 10**digits
        low = self.low.numerator*scale//self.low.denominator
        high = -((-self.high.numerator*scale)//self.high.denominator)
        return {"lower": str(F(low, scale)), "upper": str(F(high, scale))}


def arctangent_small(value, terms=40):
    value = F(value)
    require(0 < value < 1, "arctangent argument")
    total = sum(((-1)**k*value**(2*k+1)/F(2*k+1) for k in range(terms)), F(0))
    error = value**(2*terms+1)/F(2*terms+1)
    return Bounds(total, total+error) if terms % 2 == 0 else Bounds(total-error, total)


def sine_cosine(value, terms=24):
    require(0 < value.low <= value.high < 1, "trigonometric range")
    sine = Bounds(0)
    cosine = Bounds(0)
    for k in range(terms):
        sine += ((-1)**k)*value**(2*k+1)/factorial(2*k+1)
        cosine += ((-1)**k)*value**(2*k)/factorial(2*k)
    sine_error = value.high**(2*terms+1)/F(factorial(2*terms+1))
    cosine_error = value.high**(2*terms)/F(factorial(2*terms))
    return sine+Bounds(-sine_error, sine_error), cosine+Bounds(-cosine_error, cosine_error)


def rational_window(coefficients, hcert):
    scale = 10**60
    sqrt_floor = isqrt(2*scale*scale)
    require(sqrt_floor**2 < 2*scale*scale < (sqrt_floor+1)**2, "square-root bracket")
    root2 = Bounds(F(sqrt_floor, scale), F(sqrt_floor+1, scale))
    pi = 16*arctangent_small(F(1, 5))-4*arctangent_small(F(1, 239))
    sine, cosine = sine_cosine(root2/2)
    penalty = sum((F(value)**2*(Bounds(F(1, 2))-1/(4*pi*pi*j*j))
                   for j, value in enumerate(coefficients[1:], start=1)), Bounds(0))
    h = Bounds(F(3, 2))-cosine/(root2*sine)-penalty/(2*sine*sine)
    lower = cosine-sum((abs(F(value)) for value in coefficients[1:]), F(0))
    require(F(coefficients[0]) == 1 and lower.low > 0 and h.low >= hcert, "rational window energy/positivity")
    return h, {"arithmetic": "Python standard-library Fraction integer interval arithmetic",
               "sqrt2": root2.decimal_enclosure(), "pi": pi.decimal_enclosure(),
               "H": h.decimal_enclosure(), "positive_window_lower": lower.decimal_enclosure(),
               "arctangent_terms": 40, "sine_cosine_terms": 24,
               "H_cert": str(hcert)}


def certify_counting(pairs, pressures):
    r = len(pressures)
    b = sum(pressures, F(0))
    block_pair_checks = 0
    for m in [7, 14, 20]:
        charged = {}
        for start in range(m-r):
            for (i, j), weight in pairs.items():
                key = i+start, j+start
                charged[key] = charged.get(key, F(0))+weight
        require(all(value <= 2 for value in charged.values()), "block pair capacity")
        block_pair_checks += len(charged)
    cases = 0
    for m in [7, 14, 20]:
        for length in range(3*m+r+1):
            for varying in [False, True]:
                gaps = [F(1+(j % 7), 5) if varying else F(1) for j in range(max(length-1, 0))]
                span = sum(gaps, F(0))
                blocks = 0
                total_pressure = F(0)
                occurrences = [0 for _ in range(max(length-r, 0))]
                for offset in range(m):
                    for start in range(offset, length-m+1, m):
                        blocks += 1
                        for window_start in range(start, start+m-r):
                            occurrences[window_start] += 1
                            total_pressure += sum((pressures[j]*gaps[window_start+j] for j in range(r)), F(0))
                require(blocks == max(length-m+1, 0), "offset block count")
                require(F(blocks, m) >= F(length, m)-1, "endpoint block loss")
                require(all(count <= m-r for count in occurrences), "local window occurrence")
                require(total_pressure <= (m-r)*b*span, "vector pressure charge")
                cases += 1
    return {"exact_list_block_cases": cases, "block_pair_checks": block_pair_checks,
            "unequal_pressure_vector_used": True, "window_occurrence_bound": True,
            "global_pressure_charge_bound": True, "endpoint_block_identity": True}


def run():
    started = time.monotonic()
    raw = (HERE/"artifacts/input/Solution.lean").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, "external source hash")
    evidence_raw = (HERE/"artifacts/preflight.json").read_bytes()
    evidence = json.loads(evidence_raw)
    require(evidence["passed_preflight"] is True and evidence["source_sha256"] == SOURCE_SHA, "preflight input")
    require(evidence["runner_sha256"] == hashlib.sha256((HERE/"run.py").read_bytes()).hexdigest(), "preflight source binding")
    text = raw.decode("utf-8")
    functional = text.split("def G (g0 g1 g2 g3 g4 g5 : ℝ) : ℝ :=", 1)[1].split("/-- early exit", 1)[0]
    pressure_matches = re.findall(r"\((\d+) / \(SA:ℝ\)\) \* g(\d)", functional)
    require([int(index) for _, index in pressure_matches] == list(range(6)), "certified pressure indices")
    pressures = [F(int(n), 100000000) for n, _ in pressure_matches]
    require([str(value) for value in pressures] == evidence["gap_pressures"], "certified pressure values")
    pairs = {}
    for n, expression in re.findall(r"\((\d+) / \(SA:ℝ\)\) \* wfun \(([^)]+)\)", functional):
        indices = [int(part[1:]) for part in expression.split(" + ")]
        require(indices == list(range(indices[0], indices[-1]+1)), "certified consecutive span")
        pairs[indices[0], indices[-1]+1] = F(int(n), 100000000)
    require(len(pairs) == 21 and pairs == {(item["i"], item["j"]): F(item["weight"]) for item in evidence["pairs"]}, "certified pair values")
    span_capacities = [sum((weight for (i, j), weight in pairs.items() if j-i == s), F(0)) for s in range(1, 7)]
    require(all(value <= 2 for value in span_capacities), "certified span capacities")
    coeff_text = text.split("def cAMn : ℕ → ℤ", 1)[1].split("/-- the window coefficients", 1)[0]
    coeffs = {int(index): F(int(value), 10**9) for index, value in re.findall(r"\| (\d+) => (-?\d+)", coeff_text)}
    require([str(coeffs[j]) for j in range(13)] == evidence["window_coefficients"], "certified window values")
    hcert = F(67217109258, 10**11)
    h, scalar = rational_window([coeffs[j] for j in range(13)], hcert)
    counting = certify_counting(pairs, pressures)
    m, r = 742, 6
    delta = F(39369, 5000000)
    b = sum(pressures, F(0))
    tau, c = F(12043, 5000), F(17043, 5000)
    a = delta*F(m-r, m)
    beta = b*F(m-r, m)
    d = delta*(m-r)
    residuals = {"block": tau*tau-d, "threshold1": c-1-tau,
                 "threshold2": c-2-tau/2, "high_multiplicity": 6*c-7-c*c-a,
                 "off_line": 4*c-2-c*c-2*a, "denominator": 2-a}
    require(all(value >= 0 for value in residuals.values()) and 2-a > 0, "independent transfer residual")
    q = (1+hcert-beta)/(2-a)
    require(q == F(30945470743359, 36955122080000) == F(evidence["conditional_transfer"]["liminf_fraction"]), "independent final fraction")
    require(b == F(evidence["conditional_transfer"]["pressure_sum"]), "pressure total")
    require(q-F(836993, 10**6) > F(1, 10000), "independent gain gate")
    controls = {"inflated_H_rejected": h.high < hcert+F(1, 1000),
                "minimum_pressure_undercount_rejected": r*min(pressures) != b,
                "source_change_rejected": hashlib.sha256(raw+b"\n").hexdigest() != SOURCE_SHA}
    require(all(controls.values()), "independent negative control")
    require(time.monotonic()-started < 30, "independent audit budget")
    return {"schema": "exp025-independent-rational-audit-v1", "passed": True,
            "source_sha256": SOURCE_SHA, "preflight_sha256": hashlib.sha256(evidence_raw).hexdigest(),
            "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "declaration_sha256": hashlib.sha256((HERE/"independent-audit-declaration.md").read_bytes()).hexdigest(),
            "window": scalar, "counting_controls": counting, "negative_controls": controls,
            "pressure_total": str(b), "span_capacities": [str(value) for value in span_capacities],
            "residuals": {key: str(value) for key, value in residuals.items()},
            "liminf_fraction": str(q), "elapsed_seconds": time.monotonic()-started,
            "external_local_formalization_rebuilt_here": False,
            "scope": "independent rational scalar and exact vector-pressure accounting/transfer; general proof and external local theorem remain explicit dependencies"}


if __name__ == "__main__":
    receipt = HERE/"artifacts/independent-rational-audit.json"
    require(not receipt.exists(), "preserve independent receipt")
    result = run()
    receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
