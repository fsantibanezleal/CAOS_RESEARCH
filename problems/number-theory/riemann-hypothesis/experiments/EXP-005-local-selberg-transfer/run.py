"""Exact certificate for EXP-005 local Selberg transfer.

Device: CPU.  Arithmetic: fractions plus an independent mpmath interval replay.
The finite calculation certifies constants and strict exponent margins.  It does
not replace the analytic localization proof in mathematical-proof.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


SCHEMA = "riemann-exp005-results-v1"
THETA = Fraction(273, 500)
MOLLIFIER_EXPONENT = Fraction(2299, 100000)
C3_CENTER_TEXT = "0.6567752140190419405677628751089899133"
C3_RADIUS = Fraction(1, 10**17)
NEGATIVE_THETA = Fraction(5459, 10000)
SIMPLE_GATE = Fraction(9, 100000)
MAX_SECONDS = 60.0


def decimal_fraction(text: str) -> Fraction:
    sign = -1 if text.startswith("-") else 1
    body = text[1:] if text[:1] in "+-" else text
    if "." not in body:
        return Fraction(sign * int(body), 1)
    whole, fractional = body.split(".")
    denominator = 10 ** len(fractional)
    return Fraction(sign * (int(whole) * denominator + int(fractional)), denominator)


C3_CENTER = decimal_fraction(C3_CENTER_TEXT)
C3_LOWER = C3_CENTER - C3_RADIUS
C3_UPPER = C3_CENTER + C3_RADIUS


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_record(value: Fraction, digits: int = 45) -> dict[str, object]:
    with localcontext() as context:
        context.prec = digits + 15
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": format(decimal, f".{digits}g"),
    }


def fraction_decimal_text(value: Fraction, digits: int = 130) -> str:
    with localcontext() as context:
        context.prec = digits
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return format(decimal, "f")


def sqrt_integer_interval(value: int, digits: int = 90) -> tuple[Fraction, Fraction]:
    scale = 10**digits
    floor = math.isqrt(value * scale * scale)
    lower = Fraction(floor, scale)
    upper = Fraction(floor + 1, scale)
    assert lower * lower <= value < upper * upper
    return lower, upper


def exp_one_interval(terms: int = 100) -> tuple[Fraction, Fraction]:
    total = Fraction(1)
    factorial = 1
    for n in range(1, terms + 1):
        factorial *= n
        total += Fraction(1, factorial)
    # For n=terms, the omitted positive tail is strictly below 1/(n*n!).
    upper = total + Fraction(1, terms * factorial)
    return total, upper


def sin_interval(x: Fraction, last_index: int = 41) -> tuple[Fraction, Fraction]:
    """Alternating Taylor enclosure for sin(x), 0 <= x <= 1.

    last_index is the largest k in x^(2k+1)/(2k+1)!.  Odd truncations are
    lower bounds and even truncations are upper bounds.
    """

    assert 0 <= x <= 1 and last_index >= 1
    total = Fraction(0)
    term = x
    lower: Fraction | None = None
    upper: Fraction | None = None
    for k in range(last_index + 1):
        total += term if k % 2 == 0 else -term
        if k == last_index - 1:
            if (last_index - 1) % 2 == 0:
                upper = total
            else:
                lower = total
        if k == last_index:
            if last_index % 2 == 0:
                upper = total
            else:
                lower = total
        term *= x * x / Fraction((2 * k + 2) * (2 * k + 3))
    assert lower is not None and upper is not None and 0 < lower <= upper
    return lower, upper


def cos_interval(x: Fraction, last_index: int = 42) -> tuple[Fraction, Fraction]:
    """Alternating Taylor enclosure for cos(x), 0 <= x <= 1."""

    assert 0 <= x <= 1 and last_index >= 1
    total = Fraction(0)
    term = Fraction(1)
    lower: Fraction | None = None
    upper: Fraction | None = None
    for k in range(last_index + 1):
        total += term if k % 2 == 0 else -term
        if k == last_index - 1:
            if (last_index - 1) % 2 == 0:
                upper = total
            else:
                lower = total
        if k == last_index:
            if last_index % 2 == 0:
                upper = total
            else:
                lower = total
        term *= x * x / Fraction((2 * k + 1) * (2 * k + 2))
    assert lower is not None and upper is not None and 0 < lower <= upper
    return lower, upper


@dataclass(frozen=True)
class ThetaCertificate:
    theta: Fraction
    c_lower: Fraction
    c_upper: Fraction
    kappa_curve_lower: Fraction
    kappa_curve_upper: Fraction
    simple_curve_lower: Fraction
    simple_curve_upper: Fraction


def cosine_curve_interval(
    theta: Fraction,
    sqrt2: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    sqrt_lower, sqrt_upper = sqrt2
    x_lower = theta / sqrt_upper
    x_upper = theta / sqrt_lower
    sin_lower_at_lower, _ = sin_interval(x_lower)
    _, sin_upper_at_upper = sin_interval(x_upper)
    _, cos_upper_at_lower = cos_interval(x_lower)
    cos_lower_at_upper, _ = cos_interval(x_upper)
    cot_upper = cos_upper_at_lower / sin_lower_at_lower
    cot_lower = cos_lower_at_upper / sin_upper_at_upper
    product_upper = cot_upper / sqrt_lower
    product_lower = cot_lower / sqrt_upper
    c_lower = Fraction(2) - theta / 2 - product_upper
    c_upper = Fraction(2) - theta / 2 - product_lower
    assert c_lower <= c_upper
    return c_lower, c_upper


def theta_certificate(
    theta: Fraction,
    sqrt2: tuple[Fraction, Fraction],
    exp_interval: tuple[Fraction, Fraction],
) -> ThetaCertificate:
    c_lower, c_upper = cosine_curve_interval(theta, sqrt2)
    exp_lower, exp_upper = exp_interval
    delta = theta - Fraction(1, 2)
    kappa_lower = delta / (4 * exp_upper * C3_UPPER)
    kappa_upper = delta / (4 * exp_lower * C3_LOWER)
    simple_lower = (c_lower + 2 * kappa_lower) / 3
    simple_upper = (c_upper + 2 * kappa_upper) / 3
    return ThetaCertificate(
        theta=theta,
        c_lower=c_lower,
        c_upper=c_upper,
        kappa_curve_lower=kappa_lower,
        kappa_curve_upper=kappa_upper,
        simple_curve_lower=simple_lower,
        simple_curve_upper=simple_upper,
    )


def mpf_tuple_fraction(value: tuple[int, int, int, int]) -> Fraction:
    sign, mantissa, exponent, _bit_count = value
    result = Fraction(mantissa)
    if exponent >= 0:
        result *= 2**exponent
    else:
        result /= 2 ** (-exponent)
    return -result if sign else result


def interval_endpoints(value: object) -> tuple[Fraction, Fraction]:
    # mpmath.iv endpoints are zero-width interval objects.  Their internal mpf
    # tuples are exact binary rationals, so this conversion loses no bits.
    lower_obj = value.a  # type: ignore[attr-defined]
    upper_obj = value.b  # type: ignore[attr-defined]
    return (
        mpf_tuple_fraction(lower_obj._mpi_[0]),  # type: ignore[attr-defined]
        mpf_tuple_fraction(upper_obj._mpi_[1]),  # type: ignore[attr-defined]
    )


def independent_interval_replay(theta: Fraction, u: Fraction) -> dict[str, object]:
    import mpmath as mp

    mp.iv.dps = 100
    theta_iv = mp.iv.mpf([fraction_decimal_text(theta)] * 2)
    u_iv = mp.iv.mpf([fraction_decimal_text(u)] * 2)
    c3_iv = mp.iv.mpf(
        [
            fraction_decimal_text(C3_LOWER),
            fraction_decimal_text(C3_UPPER),
        ]
    )
    sqrt2_iv = mp.iv.sqrt(2)
    c_iv = 2 - theta_iv / 2 - mp.iv.cos(theta_iv / sqrt2_iv) / (
        sqrt2_iv * mp.iv.sin(theta_iv / sqrt2_iv)
    )
    kappa_curve_iv = (theta_iv - mp.iv.mpf("0.5")) / (4 * mp.iv.exp(1) * c3_iv)
    kappa_fixed_iv = u_iv / (2 * mp.iv.exp(1) * c3_iv)
    simple_curve_iv = (c_iv + 2 * kappa_curve_iv) / 3
    simple_fixed_iv = (c_iv + 2 * kappa_fixed_iv) / 3
    records: dict[str, object] = {"mpmath_version": mp.__version__, "dps": 100}
    for name, interval in {
        "c": c_iv,
        "kappa_curve": kappa_curve_iv,
        "kappa_fixed": kappa_fixed_iv,
        "simple_curve": simple_curve_iv,
        "simple_fixed": simple_fixed_iv,
    }.items():
        lower, upper = interval_endpoints(interval)
        records[name] = {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
            "display": str(interval),
        }
    return records


def check_source_hashes(repo: Path) -> dict[str, object]:
    context = repo / "problems/number-theory/riemann-hypothesis/context"
    manifest_path = context / "source-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    wanted_documents = {
        "pearce-crump-2609.15329v1.pdf",
        "pearce-crump-2609.15329v1.tar.gz",
    }
    document_results: list[dict[str, object]] = []
    for row in manifest["documents"]:
        if row.get("filename") not in wanted_documents:
            continue
        path = context / row["cache_path"]
        observed_hash = sha256(path)
        observed_bytes = path.stat().st_size
        passed = observed_hash == row["sha256"] and observed_bytes == row["bytes"]
        document_results.append(
            {
                "filename": row["filename"],
                "bytes": observed_bytes,
                "sha256": observed_hash,
                "passed": passed,
            }
        )
    repo_row = next(
        row
        for row in manifest["repositories"]
        if row.get("commit") == "02dfc0b1c63d12e6d39649a0bbe08dfc7ef6cf75"
    )
    archive = context / repo_row["archive_path"]
    archive_result = {
        "path": repo_row["archive_path"],
        "bytes": archive.stat().st_size,
        "sha256": sha256(archive),
    }
    archive_result["passed"] = (
        archive_result["bytes"] == repo_row["bytes"]
        and archive_result["sha256"] == repo_row["sha256"]
    )
    passed = (
        len(document_results) == len(wanted_documents)
        and all(bool(row["passed"]) for row in document_results)
        and bool(archive_result["passed"])
    )
    return {
        "manifest_sha256": sha256(manifest_path),
        "documents": document_results,
        "repository_archive": archive_result,
        "passed": passed,
    }


def git_identity(repo: Path) -> dict[str, object]:
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()
    tracked_clean = (
        subprocess.run(["git", "diff", "--quiet"], cwd=repo).returncode == 0
        and subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo).returncode
        == 0
    )
    return {"head": head, "tracked_clean_at_start": tracked_clean}


def compute_certificate(repo: Path) -> dict[str, object]:
    sqrt2 = sqrt_integer_interval(2)
    exp_bounds = exp_one_interval()
    positive = theta_certificate(THETA, sqrt2, exp_bounds)
    negative = theta_certificate(NEGATIVE_THETA, sqrt2, exp_bounds)

    fixed_kappa_lower = MOLLIFIER_EXPONENT / (2 * exp_bounds[1] * C3_UPPER)
    fixed_kappa_upper = MOLLIFIER_EXPONENT / (2 * exp_bounds[0] * C3_LOWER)
    fixed_simple_lower = (positive.c_lower + 2 * fixed_kappa_lower) / 3
    fixed_simple_upper = (positive.c_upper + 2 * fixed_kappa_upper) / 3
    exponent_margin = THETA - Fraction(1, 2) - 2 * MOLLIFIER_EXPONENT
    boundary_u = (THETA - Fraction(1, 2)) / 2

    replay = independent_interval_replay(THETA, MOLLIFIER_EXPONENT)
    replay_c = replay["c"]
    replay_curve = replay["simple_curve"]
    replay_fixed = replay["simple_fixed"]
    assert isinstance(replay_c, dict)
    assert isinstance(replay_curve, dict)
    assert isinstance(replay_fixed, dict)
    c_iv_lower = Fraction(replay_c["lower"]["numerator"], replay_c["lower"]["denominator"])  # type: ignore[index]
    c_iv_upper = Fraction(replay_c["upper"]["numerator"], replay_c["upper"]["denominator"])  # type: ignore[index]
    curve_iv_lower = Fraction(replay_curve["lower"]["numerator"], replay_curve["lower"]["denominator"])  # type: ignore[index]
    curve_iv_upper = Fraction(replay_curve["upper"]["numerator"], replay_curve["upper"]["denominator"])  # type: ignore[index]
    fixed_iv_lower = Fraction(replay_fixed["lower"]["numerator"], replay_fixed["lower"]["denominator"])  # type: ignore[index]
    fixed_iv_upper = Fraction(replay_fixed["upper"]["numerator"], replay_fixed["upper"]["denominator"])  # type: ignore[index]

    checks = {
        "source_hashes": check_source_hashes(repo)["passed"],
        "c3_interval_ordered": C3_LOWER < C3_CENTER < C3_UPPER,
        "sqrt2_interval": sqrt2[0] * sqrt2[0] <= 2 < sqrt2[1] * sqrt2[1],
        "e_interval": exp_bounds[0] < exp_bounds[1],
        "strict_localization_margin": exponent_margin == Fraction(1, 50000),
        "mollifier_below_quarter": MOLLIFIER_EXPONENT < Fraction(1, 4),
        "baseline_negative": positive.c_upper < 0,
        "curve_simple_positive": positive.simple_curve_lower > SIMPLE_GATE,
        "fixed_u_simple_positive": fixed_simple_lower > SIMPLE_GATE,
        "negative_theta_control": negative.simple_curve_upper < 0,
        "boundary_rejected": THETA - Fraction(1, 2) - 2 * boundary_u == 0,
        "interval_contains_c": positive.c_lower <= c_iv_lower <= c_iv_upper <= positive.c_upper,
        "interval_contains_curve": positive.simple_curve_lower <= curve_iv_lower <= curve_iv_upper <= positive.simple_curve_upper,
        "interval_contains_fixed": fixed_simple_lower <= fixed_iv_lower <= fixed_iv_upper <= fixed_simple_upper,
    }
    source_results = check_source_hashes(repo)
    checks["source_hashes"] = bool(source_results["passed"])
    passed = all(checks.values())
    return {
        "schema": SCHEMA,
        "status": "pass" if passed else "fail",
        "claim_boundary": {
            "finite_certificate": "exact rational and interval checks",
            "analytic_theorem": "requires the separate localization proof review",
            "rh_solved": False,
        },
        "parameters": {
            "theta": fraction_record(THETA),
            "mollifier_exponent_u": fraction_record(MOLLIFIER_EXPONENT),
            "negative_control_theta": fraction_record(NEGATIVE_THETA),
            "simple_gate": fraction_record(SIMPLE_GATE),
        },
        "source_constant": {
            "name": "C[q3]",
            "center": fraction_record(C3_CENTER),
            "radius": fraction_record(C3_RADIUS),
            "lower": fraction_record(C3_LOWER),
            "upper": fraction_record(C3_UPPER),
        },
        "elementary_intervals": {
            "sqrt2_lower": fraction_record(sqrt2[0]),
            "sqrt2_upper": fraction_record(sqrt2[1]),
            "e_lower": fraction_record(exp_bounds[0]),
            "e_upper": fraction_record(exp_bounds[1]),
        },
        "positive_point": {
            "c_lower": fraction_record(positive.c_lower),
            "c_upper": fraction_record(positive.c_upper),
            "kappa_curve_lower": fraction_record(positive.kappa_curve_lower),
            "kappa_curve_upper": fraction_record(positive.kappa_curve_upper),
            "simple_curve_lower": fraction_record(positive.simple_curve_lower),
            "simple_curve_upper": fraction_record(positive.simple_curve_upper),
            "fixed_u_kappa_lower": fraction_record(fixed_kappa_lower),
            "fixed_u_kappa_upper": fraction_record(fixed_kappa_upper),
            "fixed_u_simple_lower": fraction_record(fixed_simple_lower),
            "fixed_u_simple_upper": fraction_record(fixed_simple_upper),
            "localization_exponent_margin": fraction_record(exponent_margin),
        },
        "negative_control": {
            "theta": fraction_record(negative.theta),
            "simple_curve_lower": fraction_record(negative.simple_curve_lower),
            "simple_curve_upper": fraction_record(negative.simple_curve_upper),
        },
        "boundary_control": {
            "u": fraction_record(boundary_u),
            "margin": fraction_record(THETA - Fraction(1, 2) - 2 * boundary_u),
            "accepted": False,
        },
        "independent_interval_replay": replay,
        "sources": source_results,
        "checks": checks,
        "passed": passed,
    }


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--budget-seconds", type=float, default=MAX_SECONDS)
    args = parser.parse_args()
    started = time.monotonic()
    if args.budget_seconds <= 0 or args.budget_seconds > MAX_SECONDS:
        raise ValueError(f"budget must be in (0, {MAX_SECONDS}]")
    output = args.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"refusing to overwrite nonempty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    log_lines: list[str] = []

    def log(message: str) -> None:
        line = f"[{time.monotonic() - started:0.6f}s] {message}"
        log_lines.append(line)
        print(line, flush=True)

    def checkpoint(stage: str) -> None:
        write_json(
            output / "checkpoint.json",
            {"schema": "riemann-exp005-checkpoint-v1", "stage": stage},
        )
        if time.monotonic() - started > args.budget_seconds:
            raise TimeoutError(f"budget exhausted after {stage}")

    repo = Path(__file__).resolve().parents[5]
    try:
        log("stage 1/4: validate committed identity and source hashes")
        identity = git_identity(repo)
        if not identity["tracked_clean_at_start"]:
            raise RuntimeError("tracked repository files must be clean before canonical execution")
        sources = check_source_hashes(repo)
        if not sources["passed"]:
            raise RuntimeError("source hash validation failed")
        checkpoint("sources-validated")

        log("stage 2/4: build exact rational Taylor certificate")
        result = compute_certificate(repo)
        checkpoint("exact-certificate-built")

        log("stage 3/4: require every declared control")
        if not result["passed"]:
            failed = [name for name, passed in result["checks"].items() if not passed]
            raise AssertionError("failed checks: " + ", ".join(failed))
        checkpoint("controls-passed")

        log("stage 4/4: write canonical result and execution receipt")
        script_path = Path(__file__).resolve()
        result["execution_identity"] = {
            **identity,
            "run_py_sha256": sha256(script_path),
            "hypothesis_sha256": sha256(script_path.with_name("hypothesis.md")),
            "python": sys.version,
        }
        write_json(output / "result.json", result)
        receipt = {
            "schema": "riemann-exp005-execution-receipt-v1",
            "status": "pass",
            "elapsed_seconds": time.monotonic() - started,
            "budget_seconds": args.budget_seconds,
            "result_sha256": sha256(output / "result.json"),
            "git": identity,
        }
        write_json(output / "execution-receipt.json", receipt)
        log("PASS: finite EXP-005 certificate completed")
        (output / "stdout.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        return 0
    except Exception as error:
        log(f"FAIL: {type(error).__name__}: {error}")
        write_json(
            output / "failure.json",
            {
                "schema": "riemann-exp005-failure-v1",
                "error_type": type(error).__name__,
                "error": str(error),
                "elapsed_seconds": time.monotonic() - started,
            },
        )
        (output / "stdout.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
