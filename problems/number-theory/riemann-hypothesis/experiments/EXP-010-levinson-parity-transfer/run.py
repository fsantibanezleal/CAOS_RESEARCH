"""EXP-010 canonical certificate: localized Levinson-Conrey detector and the parity onset.

Device: CPU. Deterministic, exact-rational plus Arb ball arithmetic (python-flint).

Stages:
  1. bind the declaration, the frozen parameter file and the comparison sources by SHA-256;
  2. reproduce the published anchors (Young 2010: c=2.35...; Conrey 1989 note: kappa>=0.4088);
  3. for every frozen parameter set: exact constraints on P and Q, the exact reduction
     c = A e^(2R) + B with rational A, B, Arb enclosures of c and kappa, and Prediction C;
  4. Prediction D: directed enclosures of Wang's pair term c(theta), the parity root h_L(theta),
     the EXP-008 Selberg comparison, and every frozen threshold;
  5. write the canonical result, receipt and log.

The constant is Conrey's (Crelle 399, Theorem 2), in the form of Young (1.3) and CFKL (15)-(16):
    c = 1 + (1/nu) int_0^1 int_0^1 (w(v) P'(u) + nu w'(v) P(u))^2 du dv,   w(v) = e^(R v) Q(v),
    kappa = 1 - log(c)/R.
Expanding the square separates the variables:
    c = 1 + (C_P/nu) L(Q^2) + 2 D_P L(Q(RQ+Q')) + nu B_P L((RQ+Q')^2),
with B_P = int P^2, C_P = int P'^2, D_P = int P P' and L(p) = int_0^1 e^(2Rv) p(v) dv. For a
polynomial p, L(p) = A e^(2R) - B exactly with rational A, B, so c needs one exponential.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx, fmpq, fmpq_poly

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

MAX_SECONDS = 900.0
PREC_BITS = 4000
HERE = Path(__file__).resolve().parent
FROZEN = HERE / "frozen-parameters.json"
DECLARATION = HERE / "hypothesis.md"

# Prediction C and D thresholds, exactly as declared.
KAPPA_OVER_NU = Fraction(7170, 10000)
KAPPA_POINT_TARGETS = {Fraction(339, 10000): Fraction(243, 10000), Fraction(349, 10000): Fraction(250, 10000)}
SELBERG_UPPER_TARGETS = {
    Fraction(534, 1000): Fraction(477, 100000),
    Fraction(535, 1000): Fraction(491, 100000),
}
H_TARGETS = {
    Fraction(534, 1000): Fraction(1, 100000),
    Fraction(535, 1000): Fraction(15, 10000),
    Fraction(54, 100): Fraction(90, 10000),
    Fraction(5459, 10000): Fraction(177, 10000),
    Fraction(55, 100): Fraction(237, 10000),
    Fraction(60, 100): Fraction(929, 10000),
}
GAP = Fraction(1, 10000)
EXP008_RATIO_TARGET = Fraction(900)
C6_CENTER = Fraction("0.6566338678379319741683641732")
C6_RADIUS = Fraction("5.63e-18")
EXP008_H6_REFERENCE = "1.7764e-5"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=HERE, text=True).strip())


def git_identity(repo: Path) -> dict[str, object]:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    clean = (
        subprocess.run(["git", "diff", "--quiet"], cwd=repo).returncode == 0
        and subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo).returncode == 0
    )
    return {"head": head, "tracked_tree_clean": clean}


# ---------------------------------------------------------------------------------------------
# exact rational layer
# ---------------------------------------------------------------------------------------------
def fq(value: str | int | Fraction) -> fmpq:
    value = Fraction(value)
    return fmpq(value.numerator, value.denominator)


def to_fraction(value: fmpq) -> Fraction:
    return Fraction(int(value.p), int(value.q))


def chebyshev_t(n: int, z: fmpq_poly) -> fmpq_poly:
    t_prev, t_cur = fmpq_poly([1]), z
    if n == 0:
        return t_prev
    for _ in range(n - 1):
        t_prev, t_cur = t_cur, 2 * z * t_cur - t_prev
    return t_cur


def build_q(x_j: list[str]) -> fmpq_poly:
    """Q(y) = 1 - y + sum_j x_j (T_(2j+1)(1-2y) - (1-2y))."""
    z = fmpq_poly([1, -2])
    q = fmpq_poly([1, -1])
    for index, coefficient in enumerate(x_j, start=1):
        q += fq(coefficient) * (chebyshev_t(2 * index + 1, z) - z)
    return q


def build_p(r: str, terms: int = 7) -> fmpq_poly:
    """P(x) = S(r x)/S(r), S(u) = sum_{i<terms} u^(2i+1)/(2i+1)!."""
    rr = fq(r)
    coefficients = [fmpq(0)] * (2 * terms)
    for i in range(terms):
        coefficients[2 * i + 1] = rr ** (2 * i + 1) / fmpq(math.factorial(2 * i + 1))
    s = fmpq_poly(coefficients)
    return s * (fmpq(1) / s(fmpq(1)))


def integral01(p: fmpq_poly) -> fmpq:
    antiderivative = p.integral()
    return antiderivative(fmpq(1)) - antiderivative(fmpq(0))


def exponential_moments(r_value: fmpq, n: int) -> tuple[list[fmpq], list[fmpq]]:
    """Exact a_k, b_k with int_0^1 e^(t v) v^k dv = a_k e^t - b_k, t = 2R."""
    t = 2 * r_value
    a, b = [fmpq(1) / t], [fmpq(1) / t]
    for k in range(1, n + 1):
        a.append(fmpq(1) / t - fmpq(k) / t * a[-1])
        b.append(-fmpq(k) / t * b[-1])
    return a, b


def weighted_integral(p: fmpq_poly, moments: tuple[list[fmpq], list[fmpq]]) -> tuple[fmpq, fmpq]:
    a, b = moments
    big, small = fmpq(0), fmpq(0)
    for k, coefficient in enumerate(p.coeffs()):
        if coefficient != 0:
            big += coefficient * a[k]
            small -= coefficient * b[k]
    return big, small


def conrey_constant_exact(p: fmpq_poly, q: fmpq_poly, r_value: fmpq, nu: fmpq) -> tuple[fmpq, fmpq]:
    """Exact (A, B) with c(P, Q, R, nu) = A e^(2R) + B."""
    dp = p.derivative()
    b_p, c_p, d_p = integral01(p * p), integral01(dp * dp), integral01(p * dp)
    v = r_value * q + q.derivative()
    moments = exponential_moments(r_value, max((q * q).degree(), (q * v).degree(), (v * v).degree()))
    a0, b0 = weighted_integral(q * q, moments)
    a1, b1 = weighted_integral(q * v, moments)
    a2, b2 = weighted_integral(v * v, moments)
    big = c_p / nu * a0 + 2 * d_p * a1 + nu * b_p * a2
    small = 1 + c_p / nu * b0 + 2 * d_p * b1 + nu * b_p * b2
    return big, small


def check_constraints(p: fmpq_poly, q: fmpq_poly) -> dict[str, str]:
    mirror = q(fmpq_poly([1, -1]))
    symmetric = q + mirror
    beta = symmetric(fmpq(0))
    record = {
        "P(0)": str(p(fmpq(0))),
        "P(1)": str(p(fmpq(1))),
        "Q(0)": str(q(fmpq(0))),
        "Q(y)+Q(1-y)": str(symmetric) if symmetric.degree() > 0 else str(beta),
    }
    if p(fmpq(0)) != 0 or p(fmpq(1)) != 1 or q(fmpq(0)) != 1 or symmetric.degree() > 0 or beta != 1:
        raise AssertionError(f"admissibility failed: {record}")
    return record


# ---------------------------------------------------------------------------------------------
# ball layer
# ---------------------------------------------------------------------------------------------
def ball(value: fmpq | Fraction | int) -> arb:
    value = Fraction(value) if not isinstance(value, fmpq) else to_fraction(value)
    return arb(fmpq(value.numerator, value.denominator))


def dyadic(value: arb) -> Fraction:
    mantissa, exponent = value.man_exp()
    return Fraction(int(mantissa)) * (Fraction(2) ** int(exponent))


def endpoints(value: arb) -> tuple[Fraction, Fraction]:
    """Exact rational lower and upper endpoints of an Arb ball."""
    if not value.is_finite():
        raise ArithmeticError("non-finite enclosure")
    mid = dyadic(value.mid())
    rad = dyadic(value.rad())
    return mid - rad, mid + rad


def _format_scaled(q: int, digits: int) -> str:
    sign = "-" if q < 0 else ""
    q = abs(q)
    return f"{sign}{q // 10**digits}.{q % 10**digits:0{digits}d}"


def decimal_floor(value: Fraction, digits: int = 40) -> str:
    """Largest decimal with `digits` places that is <= value (outward for lower bounds)."""
    return _format_scaled(math.floor(value * 10**digits), digits)


def decimal_ceil(value: Fraction, digits: int = 40) -> str:
    """Smallest decimal with `digits` places that is >= value (outward for upper bounds)."""
    return _format_scaled(math.ceil(value * 10**digits), digits)


def interval_record(value: arb, digits: int = 40) -> dict[str, str]:
    lo, hi = endpoints(value)
    return {
        "lower": decimal_floor(lo, digits),
        "upper": decimal_ceil(hi, digits),
        "arb": value.str(30, radius=True),
    }


def kappa_ball(big: fmpq, small: fmpq, r_value: fmpq) -> tuple[arb, arb]:
    c = ball(big) * (2 * ball(r_value)).exp() + ball(small)
    return c, 1 - c.log() / ball(r_value)


def wang_pair_term(theta: Fraction) -> arb:
    t = ball(theta)
    sqrt2 = arb(2).sqrt()
    return 2 - t / 2 - (t / sqrt2).cot() / sqrt2


def parity_root(k: arb, c_theta: arb) -> arb:
    """h(theta) = (3 + k - sqrt((1-k)(9-k-8c)))/4, the EXP-006 lower root."""
    return (3 + k - ((1 - k) * (9 - k - 8 * c_theta)).sqrt()) / 4


def selberg_k6(theta: Fraction) -> arb:
    c6 = ball(C6_CENTER).union(ball(C6_CENTER - C6_RADIUS)).union(ball(C6_CENTER + C6_RADIUS))
    return (ball(theta) - ball(Fraction(1, 2))) / (4 * arb(1).exp() * c6)


# ---------------------------------------------------------------------------------------------
# stages
# ---------------------------------------------------------------------------------------------
def anchors() -> dict[str, object]:
    young_p, young_q = fmpq_poly([0, 1]), fmpq_poly([1, -1])
    big, small = conrey_constant_exact(young_p, young_q, fq("13/10"), fq("1/2"))
    c_young, k_young = kappa_ball(big, small, fq("13/10"))
    lo, hi = endpoints(c_young)
    if not (Fraction("2.3500677") < lo and hi < Fraction("2.3500678")):
        raise AssertionError("Young anchor c=2.35006... not reproduced")
    z = fmpq_poly([1, -2])
    conrey_q = (
        fq("492/1000") + fq("602/1000") * z - fq("8/100") * z**3 - fq("6/100") * z**5 + fq("46/1000") * z**7
    )
    if conrey_q(fmpq(0)) != 1:
        raise AssertionError("Conrey Q(0) != 1")
    conrey_p = build_p("100638/100000")
    big, small = conrey_constant_exact(conrey_p, conrey_q, fq("128/100"), fq("4/7"))
    c_conrey, k_conrey = kappa_ball(big, small, fq("128/100"))
    if not endpoints(k_conrey)[0] > Fraction("0.4088"):
        raise AssertionError("Conrey anchor kappa>=0.4088 not reproduced")
    beta = (conrey_q + conrey_q(fmpq_poly([1, -1])))(fmpq(0))
    return {
        "young_2010": {
            "P": "x",
            "Q": "1-x",
            "R": "13/10",
            "nu": "1/2",
            "c": interval_record(c_young),
            "kappa": interval_record(k_young),
            "published": "c = 2.35..., kappa >= 0.34...",
        },
        "conrey_1989_note": {
            "Q": "0.492+0.602(1-2x)-0.08(1-2x)^3-0.06(1-2x)^5+0.046(1-2x)^7",
            "beta": str(beta),
            "P": "S_13(r x)/S_13(r), r=100638/100000",
            "R": "32/25",
            "nu": "4/7",
            "kappa": interval_record(k_conrey),
            "published": "kappa >= 0.4088",
        },
    }


def certify_set(entry: dict[str, object]) -> dict[str, object]:
    nu, r_value = fq(entry["nu"]), fq(entry["R"])
    p = build_p(entry["r_P"])
    q = build_q(entry["x_j"])
    if q.degree() != 2 * int(entry["K"]) + 1:
        raise AssertionError("unexpected degree of Q")
    constraints = check_constraints(p, q)
    big, small = conrey_constant_exact(p, q, r_value, nu)
    c, kappa = kappa_ball(big, small, r_value)
    kappa_lo, _ = endpoints(kappa)
    c_lo, c_hi = endpoints(c)
    if (c_hi - c_lo) / c_lo > Fraction(1, 10**30):
        raise AssertionError("relative radius of c is not below 1e-30")
    nu_fraction = to_fraction(nu)
    passes = kappa_lo > KAPPA_OVER_NU * nu_fraction
    point_target = KAPPA_POINT_TARGETS.get(nu_fraction)
    point_pass = None if point_target is None else kappa_lo > point_target
    return {
        "nu": str(nu_fraction),
        "theta_target": str(nu_fraction + Fraction(1, 2) + GAP),
        "R": entry["R"],
        "r_P": entry["r_P"],
        "degree_Q": q.degree(),
        "constraints": constraints,
        "c_exact": {"A": str(big), "B": str(small), "form": "c = A exp(2R) + B"},
        "c": interval_record(c),
        "kappa": interval_record(kappa),
        "kappa_lower_rational": str(kappa_lo),
        "kappa_over_nu_lower": decimal_floor(kappa_lo / nu_fraction, 12),
        "prediction_c_kappa_gt_0_717_nu": passes,
        "point_target": None if point_target is None else str(point_target),
        "point_target_pass": point_pass,
    }


def onset_and_curve(certified: dict[Fraction, dict[str, object]]) -> dict[str, object]:
    rows = []
    for theta, target in H_TARGETS.items():
        nu = theta - Fraction(1, 2) - GAP
        kappa_lo = Fraction(certified[nu]["kappa_lower_rational"])
        k = ball(kappa_lo)
        c_theta = wang_pair_term(theta)
        h_value = parity_root(k, c_theta)
        h_lo, _ = endpoints(h_value)
        linear = (c_theta + 2 * k) / 3
        rows.append(
            {
                "theta": str(theta),
                "nu": str(nu),
                "kappa_lower_used": decimal_floor(kappa_lo, 30),
                "wang_c": interval_record(c_theta),
                "needed_k_one_minus_2_over_A": interval_record(1 - 2 / (2 - c_theta)),
                "h_L": interval_record(h_value),
                "linear_branch": interval_record(linear),
                "target": str(target),
                "pass": h_lo > target,
            }
        )
    selberg = {}
    for theta, upper in SELBERG_UPPER_TARGETS.items():
        k6 = selberg_k6(theta)
        _, hi = endpoints(k6)
        selberg[str(theta)] = {"k6": interval_record(k6), "upper_target": str(upper), "pass": hi < upper}
    theta0 = Fraction(5459, 10000)
    h6 = parity_root(selberg_k6(theta0), wang_pair_term(theta0))
    h6_lo, h6_hi = endpoints(h6)
    row = next(r for r in rows if Fraction(r["theta"]) == theta0)
    hl_lo = Fraction(row["h_L"]["lower"])
    ratio_lower = hl_lo / h6_hi
    monotone = {
        "c_increasing": "c'(theta) = -1/2 + csc^2(theta/sqrt2)/2 > 0 on (0,1)",
        "h_increasing_in_c_and_k": "for 0<=k<1 and 9-k-8c>0, h increases with c and with k",
        "consequence": "every fixed theta >= 0.534 is covered by the fixed admissible nu = 0.0339",
    }
    return {
        "rows": rows,
        "selberg_comparison": selberg,
        "exp008_comparison": {
            "theta": str(theta0),
            "h6_selberg_rank_six": interval_record(h6),
            "exp008_reference_value": EXP008_H6_REFERENCE,
            "ratio_h_L_over_h6_lower": decimal_floor(ratio_lower, 6),
            "ratio_target": str(EXP008_RATIO_TARGET),
            "pass": ratio_lower > EXP008_RATIO_TARGET,
        },
        "monotone_extension": monotone,
    }


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--budget-seconds", type=float, default=MAX_SECONDS)
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only; never canonical")
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
    repo = repo_root()
    identity = git_identity(repo)
    if not identity["tracked_tree_clean"] and not args.allow_dirty:
        raise RuntimeError("tracked repository files must be clean before canonical execution")
    log("stage 1/5: bind sources")
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    bindings = {
        "hypothesis.md": sha256(DECLARATION),
        "frozen-parameters.json": sha256(FROZEN),
        "run.py": sha256(Path(__file__)),
    }
    log("stage 2/5: published anchors")
    anchor_record = anchors()
    log(f"  Young c = {anchor_record['young_2010']['c']['arb']}")
    log(f"  Conrey note kappa = {anchor_record['conrey_1989_note']['kappa']['arb']}")
    log("stage 3/5: frozen detector constants")
    certified: dict[Fraction, dict[str, object]] = {}
    for entry in frozen["parameter_sets"]:
        record = certify_set(entry)
        certified[Fraction(record["nu"])] = record
        log(
            f"  nu={record['nu']:>10} kappa={record['kappa']['arb']} kappa/nu>={record['kappa_over_nu_lower']} pass={record['prediction_c_kappa_gt_0_717_nu']}"
        )
    log("stage 4/5: parity onset and curve")
    onset = onset_and_curve(certified)
    for row in onset["rows"]:
        log(f"  theta={row['theta']:>10} h_L={row['h_L']['arb']} target>{row['target']} pass={row['pass']}")
    log(f"  EXP-008 ratio at 0.5459 >= {onset['exp008_comparison']['ratio_h_L_over_h6_lower']}")
    checks = {
        "anchors": True,
        "prediction_c_all": all(r["prediction_c_kappa_gt_0_717_nu"] for r in certified.values()),
        "prediction_c_points": all(
            r["point_target_pass"] for r in certified.values() if r["point_target"] is not None
        ),
        "selberg_comparison": all(v["pass"] for v in onset["selberg_comparison"].values()),
        "prediction_d_thresholds": all(r["pass"] for r in onset["rows"]),
        "exp008_ratio": onset["exp008_comparison"]["pass"],
    }
    accepted = all(checks.values())
    result = {
        "experiment": "EXP-010",
        "schema": "exp010-canonical-v1",
        "precision_bits": PREC_BITS,
        "bindings_sha256": bindings,
        "anchors": anchor_record,
        "detector_constants": [certified[k] for k in sorted(certified)],
        "onset": onset,
        "checks": checks,
        "accepted": accepted,
    }
    log("stage 5/5: write canonical result")
    write_json(out / "result.json", result)
    receipt = {
        "experiment": "EXP-010",
        "git": identity,
        "python": sys.version.split()[0],
        "python_flint": __import__("flint").__version__,
        "result_sha256": sha256(out / "result.json"),
        "elapsed_seconds": round(time.time() - started, 2),
        "budget_seconds": args.budget_seconds,
        "accepted": accepted,
    }
    write_json(out / "execution-receipt.json", receipt)
    log(f"accepted={accepted}")
    (out / "stdout.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
