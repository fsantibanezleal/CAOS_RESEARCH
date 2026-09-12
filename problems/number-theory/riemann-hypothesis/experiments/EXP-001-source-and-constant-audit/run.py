"""Exact rational reproduction and symbolic audits; hypothesis predates execution.

The primary path uses Fraction alternating Taylor brackets, not Arb. Arb is a
separate comparison after all rational bounds have been constructed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import flint
import sympy as sp

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE_DIR = HERE.parents[1] / "context"
sys.path.insert(0, str(HERE.parents[1] / "code"))
from riemann_certificates import c_value  # noqa: E402

SOURCE_PINS = {
    "claude-original-20260810.pdf": "6792988e6cd0e17690621ce898abd5d534f98407741bc7cb14bbe7d07c77d72f",
    "claude-revised-20260811.pdf": "19f827bee5834d61aa6dd756cdaea582492703ddbfd6bdc2058de10b93f7e814",
    "lamzouri-2609.02882v2.pdf": "305df7fcbbf96e61ccca2cbae13dcb2b7f9251b054d02dd0c78551982621046b",
    "wang-2609.07918v1.pdf": "6e34a86265b7389a2cc1f4dcd1f6034578261c3b02b40c6581a8ddb316308079",
}


def check_sources(directory: Path) -> list[dict]:
    directory = directory.resolve()
    manifest = json.loads((directory / "source-manifest.json").read_text(encoding="utf-8-sig"))
    if manifest.get("schema") != "riemann-source-manifest-v1":
        raise ValueError("Unsupported source manifest schema")
    entries = {entry["filename"]: entry for entry in manifest["documents"]}
    results = []
    for name, expected in SOURCE_PINS.items():
        entry = entries[name]
        relative_cache = Path(entry["cache_path"])
        source_path = (directory / relative_cache).resolve()
        if relative_cache.is_absolute() or not source_path.is_relative_to(directory):
            raise ValueError(f"Source cache path escapes manifest directory: {name}")
        data = source_path.read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected or entry["sha256"].lower() != expected:
            raise ValueError(f"Source hash mismatch: {name}")
        if len(data) != entry["bytes"] or not entry.get("license") or not entry.get("source_url"):
            raise ValueError(f"Source metadata incomplete or changed: {name}")
        results.append({"filename": name, "sha256": actual, "bytes": len(data),
                        "source_url": entry["source_url"], "license": entry["license"],
                        "cache_path": relative_cache.as_posix(),
                        "version": entry.get("version"), "note": entry.get("note"),
                        "status": "PASS"})
    return results


def alternating(theta: F, odd: int, even_index: int = 40) -> tuple[F, F]:
    """Bracket cos(a) (odd=0) or sin(a)/a (odd=1), a^2=theta^2/2.

    The partial sum ending at even index is above the limit; adding the next
    negative term gives a lower bound. Term magnitudes decrease forever since
    0<a^2<=1/2 and the successive factorial denominator grows.
    """
    if not (0 < theta <= 1 and odd in (0, 1) and even_index >= 0 and even_index % 2 == 0):
        raise ValueError("Invalid alternating-series parameters")
    a_squared = theta * theta / 2
    term = F(1)
    partial = term
    for j in range(1, even_index + 1):
        term *= -a_squared / ((2 * j + odd - 1) * (2 * j + odd))
        partial += term
    next_term = term * -a_squared / ((2 * even_index + odd + 1) * (2 * even_index + odd + 2))
    assert next_term < 0 and abs(next_term) <= abs(term)
    lower, upper = partial + next_term, partial
    assert 0 < lower <= upper
    return lower, upper


def exact_c(theta: F) -> tuple[F, F]:
    cos_lo, cos_hi = alternating(theta, 0)
    sinc_lo, sinc_hi = alternating(theta, 1)
    # a cot(a)=cos(a)/sinc(a); cot(a)/sqrt(2)=(a cot(a))/theta.
    ratio_lo, ratio_hi = cos_lo / sinc_hi, cos_hi / sinc_lo
    base = 2 - theta / 2
    return base - ratio_hi / theta, base - ratio_lo / theta


def sqrt_two(digits: int = 100) -> tuple[F, F]:
    scale = 10 ** digits
    integer = math.isqrt(2 * scale * scale)
    assert integer * integer < 2 * scale * scale < (integer + 1) ** 2
    return F(integer, scale), F(integer + 1, scale)


def decimal_bound(value: F, digits: int, upward: bool) -> str:
    scale = 10 ** digits
    scaled = value.numerator * scale
    integer = -((-scaled) // value.denominator) if upward else scaled // value.denominator
    sign = "-" if integer < 0 else ""
    digits_text = str(abs(integer)).zfill(digits + 1)
    return sign + digits_text[:-digits] + "." + digits_text[-digits:]


def rational_bracket(bounds: tuple[F, F]) -> dict:
    lo, hi = bounds
    assert lo <= hi
    return {"lower": str(lo), "upper": str(hi), "width": str(hi - lo),
            "decimal_lower": decimal_bound(lo, 45, False),
            "decimal_upper": decimal_bound(hi, 45, True)}


def check_arb(bounds: tuple[F, F], value: flint.arb) -> dict:
    alo, ahi = F(str(value.lower().fmpq())), F(str(value.upper().fmpq()))
    lo, hi = bounds
    # The 256-bit Arb interval is wider than the >100-digit exact brackets.
    assert alo <= lo <= hi <= ahi, "Independent rational bounds disagree with Arb"
    return {"precision_bits": 256, "lower": str(alo), "upper": str(ahi),
            "exact_bracket_contained": True}


def symbolic_audits() -> dict:
    X, Y, q, sx, sy, cx, cy = sp.symbols("X Y q sx sy cx cy", real=True)
    ax, ay = q * cx - X * sx, q * cy - Y * sy
    az = q * (cx * cy - sx * sy) - (X + Y) * (sx * cy + cx * sy)
    lhs = (X * X + X * Y + Y * Y + q * q) * sx * sy
    rhs = ax * ay - X * ax * sy - Y * ay * sx - q * az
    residual = sp.expand(lhs - rhs)
    assert residual == 0
    circle_ideal = sp.groebner([sx * sx + cx * cx - 1, sy * sy + cy * cy - 1],
                              sx, cx, sy, cy, X, Y, q)
    assert circle_ideal.reduce(residual)[1] == 0
    # Actual positive roots satisfy tan(X)=q/X; expand its addition law.
    tangent_difference = ((q / X + q / Y) / (1 - q * q / (X * Y)) - q / (X + Y))
    numerator = sp.factor(sp.together(tangent_difference))
    expected = q * (X * X + X * Y + Y * Y + q * q) / ((X + Y) * (X * Y - q * q))
    assert sp.cancel(tangent_difference - expected) == 0

    T = sp.symbols("T", positive=True)
    def main_count(t):
        return t / (2 * sp.pi) * (sp.log(t / (2 * sp.pi)) - 1)
    continuous_dimension = T / (2 * sp.pi) * sp.log(T / (2 * sp.pi))
    difference = sp.simplify(sp.expand_log(main_count(2 * T) - main_count(T) - continuous_dimension))
    correction = T * (2 * sp.log(2) - 1) / (2 * sp.pi)
    assert sp.simplify(difference - correction) == 0
    # log 2 = 2*atanh(1/3) > 2/3, so 2 log 2 - 1 > 1/3 > 0.
    assert 2 * F(2, 3) - 1 == F(1, 3)
    return {
        "triple_numerator": {"status": "PASS", "expanded_residual": str(residual),
            "circle_ideal_remainder": "0", "circle_constraints_needed": False,
            "identity": "(X^2+XY+Y^2+q^2)sx*sy=Ax*Ay-X*Ax*sy-Y*Ay*sx-q*A(X+Y)"},
        "tangent_obstruction": {"status": "PASS", "difference": str(numerator),
            "positive_numerator": "q*(X^2+X*Y+Y^2+q^2) for X,Y,q>0",
            "excluded_denominator_case": "X*Y=q^2 makes tan(X+Y) undefined; it cannot be a kernel root",
            "removable_kernel_points": "X=+/-a are not automatically roots"},
        "dyadic_normalization": {"status": "PASS", "symbolic_difference": str(difference),
            "corrected_formula": "N(2T)-N(T)-floor(T*log(T/(2*pi))/(2*pi))=(2*log(2)-1)*T/(2*pi)+O(log(T))",
            "coefficient_positive_reason": "log(2)=2*atanh(1/3)>2/3, hence 2*log(2)-1>1/3",
            "floor_effect": "Replacing the continuous dimension by its floor adds a value in [0,1)",
            "relative_conclusion": "d/N(T,2T) tends to 1; an O(log T) absolute discrepancy is false",
            "source_scope": "Original Eq.(1.2) gives the correct count main term; revised section 2.2 asserts d=N(T,2T)+O(L)",
            "theorem_impact": "The correction is O(T)=o(N); it does not alone refute the limiting proportion"},
    }


def run(source_dir: Path = DEFAULT_SOURCE_DIR, *, math_only: bool = False) -> dict:
    sources = [] if math_only else check_sources(source_dir)
    source_verification = (
        {"status": "NOT_PERFORMED", "reason": "Explicit math-only mode; manifest and cached PDFs were not opened"}
        if math_only else {"status": "PASS", "required_pdfs_checked": len(sources)}
    )
    c0 = exact_c(F(1))
    c1 = ((1 + c0[0]) / 2, (1 + c0[1]) / 2)
    s2lo, s2hi = sqrt_two()
    c2 = (1 - 2 * (1 - c0[0]) / (3 + 2 * s2lo),
          1 - 2 * (1 - c0[1]) / (3 + 2 * s2hi))
    c34 = exact_c(F(3, 4))
    expected = {"c0": (F("0.672500703679"), F("0.672500703680")),
                "c1": (F("0.836250351839"), F("0.836250351840")),
                "c2": (F("0.887620008173"), F("0.887620008174")),
                "c_three_quarters": (F("0.419"), F("0.420"))}
    exact = {"c0": c0, "c1": c1, "c2": c2, "c_three_quarters": c34}
    for name, (lo, hi) in exact.items():
        assert expected[name][0] < lo <= hi < expected[name][1]
        assert hi - lo < F(1, 10 ** 95)
    # Only now call the independent Arb implementation.
    previous_precision = flint.ctx.prec
    try:
        flint.ctx.prec = 256
        a0 = c_value(F(1))
        a1 = (1 + a0) / 2
        a2 = (1 + 2 * flint.arb(2).sqrt() + 2 * a0) / (3 + 2 * flint.arb(2).sqrt())
        comparisons = {"c0": a0, "c1": a1, "c2": a2, "c_three_quarters": c_value(F(3, 4))}
        constants = {name: {"status": "PASS", "exact": rational_bracket(bounds),
                           "arb_comparison": check_arb(bounds, comparisons[name]),
                           "published_decimal_bracket": [str(x) for x in expected[name]]}
                     for name, bounds in exact.items()}
    finally:
        flint.ctx.prec = previous_precision
    return {"experiment": "EXP-001-source-and-constant-audit",
            "status": "PASS_MATH_ONLY" if math_only else "PASS", "math_status": "PASS",
            "source_verification": source_verification,
            "hypothesis_commit": "266486f", "primary_arithmetic": "Python Fraction, exact alternating Taylor sums",
            "series": {"a_squared": "theta^2/2", "upper_last_index": 40, "lower_last_index": 41,
                       "sqrt_two_decimal_scale_digits": 100},
            "dependencies": {"sympy": sp.__version__, "python_flint": flint.__version__},
            "sources": sources, "constants": constants, "symbolic_audits": symbolic_audits(),
            "scope": "Narrow reproduction, source normalization correction, and exact algebraic identity checks",
            "limitations": ["No independent proof of imported analytic theorems", "No finite-height zero-count certification",
                            "No novelty established by this experiment", "No local replay of upstream Lean developments"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR,
                        help="Manifest directory; PDF paths come from cache_path (default: problem/context)")
    parser.add_argument("--math-only", action="store_true",
                        help="Run exact certificates without opening sources; report source verification NOT_PERFORMED")
    parser.add_argument("--output-dir", type=Path, default=HERE / "artifacts")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    try:
        result = run(args.source_dir, math_only=args.math_only)
    except Exception as exc:
        (args.output_dir / "result.json").write_text(json.dumps({"experiment": HERE.name,
            "status": "INCONCLUSIVE", "error_type": type(exc).__name__, "error": str(exc)}, indent=2) + "\n")
        raise
    (args.output_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "source_verification": result["source_verification"], "constants": {
        name: item["exact"]["decimal_lower"] for name, item in result["constants"].items()},
        "symbolic_audits": {name: value["status"] for name, value in result["symbolic_audits"].items()}}, indent=2))


if __name__ == "__main__":
    main()
