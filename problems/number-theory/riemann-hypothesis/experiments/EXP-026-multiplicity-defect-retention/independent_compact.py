"""Closed-form compact Gram audit using standard-library rational intervals."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial, isqrt
from pathlib import Path
import re
import time

HERE = Path(__file__).resolve().parent
SCALE = 10**65
SOURCE_SHA = "65564079527487fde93b43bb83dd840a768acf9fb8db1f1f015d38c4faf3b7d4"


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Interval:
    """Every operation rounds outwards to a rational grid with 65 decimals."""
    def __init__(self, lo, hi=None):
        lo, hi = F(lo), F(lo if hi is None else hi)
        require(lo <= hi, "reversed interval")
        self.lo = F((lo*SCALE).__floor__(), SCALE)
        self.hi = F((hi*SCALE).__ceil__(), SCALE)

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Interval) else Interval(x)

    def __add__(self, other):
        other = self.coerce(other)
        return Interval(self.lo+other.lo, self.hi+other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self+-self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other)+-self

    def __mul__(self, other):
        other = self.coerce(other)
        products = [x*y for x in (self.lo, self.hi) for y in (other.lo, other.hi)]
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        require(other.lo > 0 or other.hi < 0, "denominator crosses zero")
        return self*Interval(1/other.hi, 1/other.lo)

    def __rtruediv__(self, other):
        return self.coerce(other)/self

    def square(self):
        lo = 0 if self.lo <= 0 <= self.hi else min(self.lo**2, self.hi**2)
        return Interval(lo, max(self.lo**2, self.hi**2))

    def abs_upper(self):
        return max(abs(self.lo), abs(self.hi))

    def receipt(self, digits=40):
        scale = 10**digits
        return {"lower": str(F((self.lo*scale).__floor__(), scale)),
                "upper": str(F((self.hi*scale).__ceil__(), scale))}


def atan(x):
    x = F(x)
    n = 50
    total = sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)), F())
    return Interval(total, total+x**(2*n+1)/F(2*n+1))


def trig(x):
    require(x.abs_upper() < 2, "reduced trig argument")
    square = x.square()
    ps, pc = x, Interval(1)
    sine, cosine = Interval(0), Interval(0)
    n = 32
    for k in range(n):
        sine += ((-1)**k)*ps/factorial(2*k+1)
        cosine += ((-1)**k)*pc/factorial(2*k)
        ps *= square
        pc *= square
    # Taylor's theorem, using |derivative|<=1 on the real axis.
    se = x.abs_upper()**(2*n)/factorial(2*n)
    ce = x.abs_upper()**(2*n-1)/factorial(2*n-1)
    return sine+Interval(-se, se), cosine+Interval(-ce, ce)


def validate_brackets(brackets):
    require(len(brackets) == 6, "root count")
    require(all(F(1, 2) <= lo < hi <= 8 and hi-lo <= F(1, 2**40) for lo, hi in brackets), "root width/domain")
    require(all(brackets[j][1] < brackets[j+1][0] for j in range(5)), "overlapping brackets")


def audit(native):
    start = time.process_time()
    source = HERE.parent / "EXP-025-vector-pressure-distinct-lift/artifacts/input/Solution.lean"
    raw = source.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, "changed source")
    text = raw.decode("utf-8")
    coefficients_text = text.split("def cAMn : ℕ → ℤ", 1)[1].split("/-- the window coefficients", 1)[0]
    coefficients = {int(j): F(int(n), 10**9) for j, n in re.findall(r"\| (\d+) => (-?\d+)", coefficients_text)}
    require(set(coefficients) == set(range(13)) and coefficients[0] == 1, "coefficient domain")
    functional = text.split("def G (g0 g1 g2 g3 g4 g5 : ℝ) : ℝ :=", 1)[1].split("/-- early exit", 1)[0]
    matches = re.findall(r"\((\d+) / \(SA:ℝ\)\) \* g(\d)", functional)
    require([int(j) for _, j in matches] == list(range(6)), "pressure indices")
    pressures = [F(int(n), 10**8) for n, _ in matches]
    pi = 16*atan(F(1, 5))-4*atan(F(1, 239))
    root_floor = isqrt(2*SCALE*SCALE)
    theta = Interval(F(root_floor, 2*SCALE), F(root_floor+1, 2*SCALE))
    sine_theta, cosine_theta = trig(theta)
    norm = sine_theta/theta
    require(norm.lo > 0, "kernel normalization")
    positivity = cosine_theta-sum((abs(coefficients[j]) for j in range(1, 13)), F())
    require(positivity.lo > 0, "positive Gram window")

    def kernel(x):
        require(time.process_time()-start < 60, "CPU audit budget")
        n = ((x.lo+x.hi)/2+F(1, 2)).__floor__()
        sx, cx = trig(pi*(x-n))
        sx, cx = ((-1)**n)*sx, ((-1)**n)*cx
        result = (theta*sine_theta*cx-pi*x*cosine_theta*sx)/(theta.square()-(pi*x).square())
        for j in range(1, 13):
            result += coefficients[j]*((-1)**j)*x*sx/(pi*(x.square()-j*j))
        return result/norm

    roots = native["certificate"]["root_intervals"]
    require(len(roots) == 6, "root count")
    brackets = [(F(r["lo"]), F(r["hi"])) for r in roots]
    validate_brackets(brackets)
    negative_controls = {}
    for name, bad in [("reversed_bracket_rejected", [(brackets[0][1], brackets[0][0])]+brackets[1:]),
                      ("overlapping_brackets_rejected", [brackets[0], brackets[0]]+brackets[2:])]:
        try:
            validate_brackets(bad)
        except ValueError:
            negative_controls[name] = True
        else:
            raise ValueError("negative bracket control accepted")
    negative_controls["changed_source_rejected"] = hashlib.sha256(raw+b"\n").hexdigest() != SOURCE_SHA
    require(all(negative_controls.values()), "negative controls")
    endpoints = []
    for lo, hi in brackets:
        kl, kh = kernel(Interval(lo)), kernel(Interval(hi))
        require((kl.lo > 0 and kh.hi < 0) or (kl.hi < 0 and kh.lo > 0), "root signs")
        endpoints.append({"K_lo": kl.receipt(), "K_hi": kh.receipt()})
    points = [Interval(0)]+[Interval(lo, hi) for lo, hi in brackets]
    rows = [F(1) for _ in range(7)]
    energy = Interval(0)
    for i in range(1, 7):
        for j in range(i+1, 7):
            value = kernel(points[j]-points[i])
            rows[i] += value.abs_upper()
            rows[j] += value.abs_upper()
            energy += 2*value.square()
    require(all(row < F(17043, 5000) for row in rows) and F(2) < F(17043, 5000), "spectral clipping")
    require(energy.lo > 0, "simple energy")
    gaps = [points[j+1]-points[j] for j in range(6)]
    charge = sum((p*gap for p, gap in zip(pressures, gaps)), Interval(0))
    require(charge.hi < F(39369, 5000000), "local pressure budget")
    return {"source_sha256": SOURCE_SHA, "arithmetic": "Python stdlib Fraction outward-rounded intervals, 65 decimal grid",
            "pi": pi.receipt(), "theta": theta.receipt(), "positive_window_lower": positivity.receipt(),
            "endpoint_sign_certificates": endpoints, "simple_pair_checks": 15,
            "unit_row_upper_bounds": [Interval(row).receipt() for row in rows],
            "weighted_doubled_row": "2", "simple_block_energy": energy.receipt(),
            "pressure_charge": charge.receipt(), "exact_root_remainder": "0",
            "scope": "Independent compact point-Gram obstruction; not a zeta-zero improvement.",
            "negative_controls": negative_controls,
            "cpu_seconds": time.process_time()-start}


def run(input_path, receipt):
    require(not receipt.exists(), "preserve audit receipt")
    native_raw = input_path.read_bytes()
    native = json.loads(native_raw)
    require(native["passed"] is True, "native witness input")
    result = {"schema": "exp026-independent-compact-v1", "passed": False,
              "native_receipt_sha256": hashlib.sha256(native_raw).hexdigest(),
              "auditor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "declaration_sha256": hashlib.sha256((HERE / "independent-compact-declaration.md").read_bytes()).hexdigest()}
    try:
        result["audit"] = audit(native)
        result["passed"] = True
    except ValueError as error:
        result["failure"] = str(error)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.input, args.receipt))
