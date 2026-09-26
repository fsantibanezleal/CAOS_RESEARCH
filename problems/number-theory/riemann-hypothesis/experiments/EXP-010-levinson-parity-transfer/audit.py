"""EXP-010 independent audit: replay the detector constants and the onset by different algorithms.

Device: CPU. The producer (run.py) expands P and Q into monomials and evaluates the Conrey
constant through exact exponential moments, c = A e^(2R) + B. This auditor never forms the
monomial expansion and never uses exact moments:

  * Q is evaluated by the three-term Chebyshev recurrence directly from its coefficients x_j,
    P by its truncated sinh series, and both derivatives by the corresponding recurrences;
  * every integral of the ORIGINAL integrand (w(v) P'(u) + nu w'(v) P(u))^2 is computed by
    validated Arb quadrature (acb.integral, rigorous error bounds), after the exact separation
    of the double integral into one-dimensional factors;
  * Wang's pair term, the parity root and the EXP-008 comparison are recomputed with
    mpmath.iv interval arithmetic at 100 decimal digits.

Every audit enclosure must overlap the producer's canonical enclosure, and every frozen
threshold must hold again. The audit reads the producer's result only for the comparison.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

from flint import acb, arb, ctx
from mpmath import iv

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

MAX_SECONDS = 1800.0
PREC_BITS = 1400
HERE = Path(__file__).resolve().parent
FROZEN = HERE / "frozen-parameters.json"
SINH_TERMS = 7


def arb_q(value: str | Fraction) -> arb:
    value = Fraction(value)
    return arb(value.numerator) / arb(value.denominator)


def acb_q(value: str | Fraction) -> acb:
    return acb(arb_q(value))


class Detector:
    """P and Q evaluated from their generators with acb arithmetic (valid on complex balls)."""

    def __init__(self, entry: dict[str, object]):
        self.x = [acb_q(value) for value in entry["x_j"]]
        self.r = acb_q(entry["r_P"])
        self.R = acb_q(entry["R"])
        self.nu = acb_q(entry["nu"])
        self.norm = self._sinh_series(self.r, 0)

    def q_and_derivative(self, y: acb) -> tuple[acb, acb]:
        """Q(y) and Q'(y) with Q(y) = 1 - y + sum_j x_j (T_(2j+1)(z) - z), z = 1 - 2y."""
        z = 1 - 2 * y
        # Chebyshev values and derivatives by the three-term recurrence T_{n+1} = 2 z T_n - T_{n-1},
        # T'_{n+1} = 2 T_n + 2 z T'_n - T'_{n-1}; dz/dy = -2.
        t_prev, t_cur = acb(1), z
        d_prev, d_cur = acb(0), acb(1)
        total, dtotal = acb(0), acb(0)
        n = 1
        for coefficient in self.x:
            for _ in range(2):
                t_prev, t_cur = t_cur, 2 * z * t_cur - t_prev
                d_prev, d_cur = d_cur, 2 * t_prev + 2 * z * d_cur - d_prev
                n += 1
            total += coefficient * (t_cur - z)
            dtotal += coefficient * (d_cur - 1)
        return 1 - y + total, -1 + (-2) * dtotal

    def _sinh_series(self, u: acb, derivative: int) -> acb:
        total = acb(0)
        for i in range(SINH_TERMS):
            power = 2 * i + 1
            if derivative == 0:
                total += u**power / math.factorial(power)
            else:
                total += u ** (power - 1) / math.factorial(power - 1)
        return total

    def p(self, x: acb) -> acb:
        return self._sinh_series(self.r * x, 0) / self.norm

    def dp(self, x: acb) -> acb:
        return self.r * self._sinh_series(self.r * x, 1) / self.norm


def integrate(function, tolerance_bits: int) -> arb:
    value = acb.integral(
        lambda z, analytic: function(z),
        0,
        1,
        rel_tol=arb(2) ** (-tolerance_bits),
        eval_limit=10**7,
        deg_limit=4000,
    )
    if abs(value.imag.mid()) > 0 and not value.imag.contains(0):
        raise ArithmeticError("imaginary part of a real integral excludes zero")
    return value.real


def audit_constant(entry: dict[str, object]) -> dict[str, arb]:
    detector = Detector(entry)
    nu, r_value = detector.nu, detector.R

    def w_pair(v: acb) -> tuple[acb, acb]:
        q, dq = detector.q_and_derivative(v)
        e = (r_value * v).exp()
        return e * q, e * (r_value * q + dq)

    b_p = integrate(lambda u: detector.p(u) ** 2, 300)
    c_p = integrate(lambda u: detector.dp(u) ** 2, 300)
    d_p = integrate(lambda u: detector.p(u) * detector.dp(u), 300)
    ww = integrate(lambda v: w_pair(v)[0] ** 2, 300)
    wd = integrate(lambda v: w_pair(v)[0] * w_pair(v)[1], 300)
    dd = integrate(lambda v: w_pair(v)[1] ** 2, 300)
    nu_real, r_real = nu.real, r_value.real
    # |P(1)Q(0)|^2 = 1, then (1/nu) int int (w P' + nu w' P)^2 = (C_P/nu) ww + 2 D_P wd + nu B_P dd.
    c = 1 + c_p / nu_real * ww + 2 * d_p * wd + nu_real * b_p * dd
    kappa = 1 - c.log() / r_real
    return {"c": c, "kappa": kappa, "D_P": d_p}


def parse_arb_record(record: dict[str, str]) -> tuple[Fraction, Fraction]:
    return Fraction(record["lower"]), Fraction(record["upper"])


def arb_endpoints(value: arb) -> tuple[Fraction, Fraction]:
    mid_m, mid_e = value.mid().man_exp()
    rad_m, rad_e = value.rad().man_exp()
    mid = Fraction(int(mid_m)) * Fraction(2) ** int(mid_e)
    rad = Fraction(int(rad_m)) * Fraction(2) ** int(rad_e)
    return mid - rad, mid + rad


def overlaps(a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def iv_fraction(value: Fraction):
    return iv.mpf(value.numerator) / value.denominator


def _raw_to_fraction(raw: tuple) -> Fraction:
    sign, mantissa, exponent, _ = raw
    value = Fraction(int(mantissa)) * Fraction(2) ** int(exponent)
    return -value if sign else value


def iv_endpoints(value) -> tuple[Fraction, Fraction]:
    """Exact rational endpoints of an mpmath.iv interval."""
    low, high = value._mpi_
    return _raw_to_fraction(low), _raw_to_fraction(high)


def iv_record(value) -> dict[str, str]:
    low, high = iv_endpoints(value)
    return {
        "lower": str(float(low)),
        "upper": str(float(high)),
        "lower_exact": str(low),
        "upper_exact": str(high),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True, help="producer result.json")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--budget-seconds", type=float, default=MAX_SECONDS)
    args = parser.parse_args()
    if args.budget_seconds <= 0 or args.budget_seconds > MAX_SECONDS:
        raise ValueError(f"budget must be in (0, {MAX_SECONDS}]")
    out = args.output_dir
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("output directory must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    lines: list[str] = []

    def log(message: str) -> None:
        line = f"[{time.time() - started:8.2f}s] {message}"
        lines.append(line)
        print(line, flush=True)
        if time.time() - started > args.budget_seconds:
            raise TimeoutError("budget exceeded")

    ctx.prec = PREC_BITS
    iv.dps = 100
    canonical = json.loads(args.canonical.read_text(encoding="utf-8"))
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    if (
        canonical["bindings_sha256"]["frozen-parameters.json"]
        != hashlib.sha256(FROZEN.read_bytes()).hexdigest()
    ):
        raise RuntimeError("frozen parameter file differs from the one bound by the producer")
    producer = {Fraction(row["nu"]): row for row in canonical["detector_constants"]}
    source_manifest = HERE.parents[1] / "context" / "source-manifest-exp010.json"
    bindings = {
        name: hashlib.sha256(path.read_bytes()).hexdigest()
        for name, path in (
            ("audit.py", Path(__file__).resolve()),
            ("mathematical-proof.md", HERE / "mathematical-proof.md"),
            ("context/source-manifest-exp010.json", source_manifest),
        )
    }
    for name in ("hypothesis.md", "run.py"):
        if canonical["bindings_sha256"][name] != hashlib.sha256((HERE / name).read_bytes()).hexdigest():
            raise RuntimeError(f"{name} differs from the one bound by the producer")

    log("stage 1/2: detector constants by validated quadrature from the generators")
    constants = []
    kappa_audit: dict[Fraction, tuple[Fraction, Fraction]] = {}
    for entry in frozen["parameter_sets"]:
        nu = Fraction(entry["nu"])
        audited = audit_constant(entry)
        c_int, k_int = arb_endpoints(audited["c"]), arb_endpoints(audited["kappa"])
        kappa_audit[nu] = k_int
        row = producer[nu]
        c_ok = overlaps(c_int, parse_arb_record(row["c"]))
        k_ok = overlaps(k_int, parse_arb_record(row["kappa"]))
        threshold_ok = k_int[0] > Fraction(7170, 10000) * nu
        d_ok = arb_endpoints(audited["D_P"])[0] <= Fraction(1, 2) <= arb_endpoints(audited["D_P"])[1]
        constants.append(
            {
                "nu": str(nu),
                "c_audit": audited["c"].str(30, radius=True),
                "kappa_audit": audited["kappa"].str(30, radius=True),
                "kappa_audit_lower": str(float(k_int[0])),
                "overlap_c": c_ok,
                "overlap_kappa": k_ok,
                "kappa_gt_0_717_nu": threshold_ok,
                "D_P_contains_one_half": d_ok,
            }
        )
        log(
            f"  nu={str(nu):>10} kappa={audited['kappa'].str(25, radius=True)} overlap={c_ok and k_ok} threshold={threshold_ok}"
        )

    log("stage 2/2: pair term and parity root by mpmath.iv at 100 digits")
    sqrt2 = iv.sqrt(iv.mpf(2))
    rows = []
    for row in canonical["onset"]["rows"]:
        theta = Fraction(row["theta"])
        nu = Fraction(row["nu"])
        k = iv_fraction(kappa_audit[nu][0])
        t = iv_fraction(theta)
        c_theta = 2 - t / 2 - (iv.cos(t / sqrt2) / iv.sin(t / sqrt2)) / sqrt2
        h = (3 + k - iv.sqrt((1 - k) * (9 - k - 8 * c_theta))) / 4
        h_lo = iv_endpoints(h)[0]
        c_prod = parse_arb_record(row["wang_c"])
        c_iv = iv_endpoints(c_theta)
        passes = h_lo > Fraction(row["target"])
        rows.append(
            {
                "theta": row["theta"],
                "wang_c_iv": iv_record(c_theta),
                "overlap_wang_c": overlaps(c_iv, c_prod),
                "h_L_iv": iv_record(h),
                "target": row["target"],
                "pass": passes,
            }
        )
        log(f"  theta={row['theta']:>10} h_L>={float(h_lo):.12g} target>{row['target']} pass={passes}")

    center, radius = Fraction("0.6566338678379319741683641732"), Fraction("5.63e-18")
    c6 = iv.mpf([iv_fraction(center - radius).a, iv_fraction(center + radius).b])
    theta0 = iv.mpf("0.5459")
    k6 = (theta0 - iv.mpf(1) / 2) / (4 * iv.e * c6)
    c0 = 2 - theta0 / 2 - (iv.cos(theta0 / sqrt2) / iv.sin(theta0 / sqrt2)) / sqrt2
    h6 = (3 + k6 - iv.sqrt((1 - k6) * (9 - k6 - 8 * c0))) / 4
    h_l0 = next(r for r in rows if r["theta"] == "5459/10000")
    ratio_lo = Fraction(h_l0["h_L_iv"]["lower_exact"]) / iv_endpoints(h6)[1]
    checks = {
        "overlap_constants": all(r["overlap_c"] and r["overlap_kappa"] for r in constants),
        "kappa_thresholds": all(r["kappa_gt_0_717_nu"] for r in constants),
        "D_P_one_half": all(r["D_P_contains_one_half"] for r in constants),
        "overlap_wang_c": all(r["overlap_wang_c"] for r in rows),
        "onset_thresholds": all(r["pass"] for r in rows),
        "exp008_ratio": ratio_lo > 900,
    }
    accepted = all(checks.values())
    result = {
        "experiment": "EXP-010",
        "schema": "exp010-audit-v1",
        "method": "Chebyshev-recurrence and series evaluation from generators, acb.integral validated quadrature, mpmath.iv at 100 digits",
        "bindings_sha256": bindings,
        "precision_bits": PREC_BITS,
        "canonical_result_sha256": hashlib.sha256(args.canonical.read_bytes()).hexdigest(),
        "constants": constants,
        "onset_rows": rows,
        "exp008_ratio_lower": str(float(ratio_lo)),
        "checks": checks,
        "accepted": accepted,
    }
    (out / "audit.json").write_text(
        json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    log(f"accepted={accepted}")
    (out / "stdout.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
