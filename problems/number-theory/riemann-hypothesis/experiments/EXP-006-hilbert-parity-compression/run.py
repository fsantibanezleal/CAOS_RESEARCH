"""Exact certificate for EXP-006 Hilbert dimension and parity compression.

Device: CPU. Arithmetic: exact fractions plus an independent mpmath interval
replay. The finite census and interval calculation test the declared theorem
interfaces. They do not replace the universal proof in mathematical-proof.md.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import subprocess
import sys
import time
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


SCHEMA = "riemann-exp006-results-v1"
THETA = Fraction(5459, 10000)
ROOT_LOWER_THETA = Fraction(136471, 250000)
ROOT_UPPER_THETA = Fraction(109177, 200000)
SIMPLE_GATE = Fraction(1, 100000)
MAX_SECONDS = 120.0

C3_CENTER_TEXT = "0.6567752140190419405677628751089899133"
C3_RADIUS = Fraction(1, 10**17)
C6_CENTER_TEXT = "0.6566338678379319741683641732"
C6_RADIUS = Fraction(563, 10**20)
REPLAY_PAD = Fraction(1, 10**90)


def decimal_fraction(text: str) -> Fraction:
    sign = -1 if text.startswith("-") else 1
    body = text[1:] if text[:1] in "+-" else text
    if "." not in body:
        return Fraction(sign * int(body), 1)
    whole, fractional = body.split(".")
    return Fraction(
        sign * (int(whole) * 10 ** len(fractional) + int(fractional)),
        10 ** len(fractional),
    )


C3_CENTER = decimal_fraction(C3_CENTER_TEXT)
C3_LOWER = C3_CENTER - C3_RADIUS
C3_UPPER = C3_CENTER + C3_RADIUS
C6_CENTER = decimal_fraction(C6_CENTER_TEXT)
C6_LOWER = C6_CENTER - C6_RADIUS
C6_UPPER = C6_CENTER + C6_RADIUS


PINNED_INPUTS = {
    "problems/number-theory/riemann-hypothesis/context/source-manifest.json":
        "5e436bc857e24fc868aa2e3f334a6fdd658756f6ae3de459b55b417f82d8aa18",
    "problems/number-theory/riemann-hypothesis/context/source-cache/pearce-crump-2609.15329v1.pdf":
        "1476f60cf5f4a12239d0db3fdaaaf2b9d4de604c27f1a57b5a95f7b9f2a9f0be",
    "problems/number-theory/riemann-hypothesis/context/source-cache/pearce-crump-2609.15329v1.tar.gz":
        "24550f470d116b9a63148061e441d634a014d58dba1ce2dd6abe6edcfea061e4",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/mathematical-proof.md":
        "98f9f82212ecc28e1baf2e4a182d4d376be419581fe40888fcdcd96e19099f42",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/artifacts/canonical/result.json":
        "3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_record(value: Fraction, digits: int = 50) -> dict[str, str]:
    with localcontext() as context:
        context.prec = digits + 15
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": format(decimal, f".{digits}g"),
    }


def fraction_decimal_text(value: Fraction, digits: int = 140) -> str:
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


def sqrt_fraction_interval(value: Fraction, digits: int = 90) -> tuple[Fraction, Fraction]:
    if value < 0:
        raise ValueError("square-root input must be nonnegative")
    scale = 10**digits
    quotient = value.numerator * scale * scale // value.denominator
    floor = math.isqrt(quotient)
    while Fraction((floor + 1) ** 2, scale * scale) <= value:
        floor += 1
    while Fraction(floor**2, scale * scale) > value:
        floor -= 1
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
    upper = total + Fraction(1, terms * factorial)
    return total, upper


def sin_interval(x: Fraction, last_index: int = 41) -> tuple[Fraction, Fraction]:
    assert 0 <= x <= 1 and last_index >= 1
    total = Fraction(0)
    term = x
    lower: Fraction | None = None
    upper: Fraction | None = None
    for index in range(last_index + 1):
        total += term if index % 2 == 0 else -term
        if index in (last_index - 1, last_index):
            if index % 2 == 0:
                upper = total
            else:
                lower = total
        term *= x * x / Fraction((2 * index + 2) * (2 * index + 3))
    assert lower is not None and upper is not None and 0 < lower <= upper
    return lower, upper


def cos_interval(x: Fraction, last_index: int = 42) -> tuple[Fraction, Fraction]:
    assert 0 <= x <= 1 and last_index >= 1
    total = Fraction(0)
    term = Fraction(1)
    lower: Fraction | None = None
    upper: Fraction | None = None
    for index in range(last_index + 1):
        total += term if index % 2 == 0 else -term
        if index in (last_index - 1, last_index):
            if index % 2 == 0:
                upper = total
            else:
                lower = total
        term *= x * x / Fraction((2 * index + 1) * (2 * index + 2))
    assert lower is not None and upper is not None and 0 < lower <= upper
    return lower, upper


def cosine_curve_interval(
    theta: Fraction, sqrt2: tuple[Fraction, Fraction]
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
    c_lower = Fraction(2) - theta / 2 - cot_upper / sqrt_lower
    c_upper = Fraction(2) - theta / 2 - cot_lower / sqrt_upper
    assert c_lower <= c_upper
    return c_lower, c_upper


@dataclass(frozen=True)
class ThetaCertificate:
    theta: Fraction
    c_lower: Fraction
    c_upper: Fraction
    k_lower: Fraction
    k_upper: Fraction
    root_function_lower: Fraction
    root_function_upper: Fraction
    old_linear_lower: Fraction
    old_linear_upper: Fraction
    radicand_lower: Fraction
    radicand_upper: Fraction
    new_simple_lower: Fraction
    new_simple_upper: Fraction


def theta_certificate(
    theta: Fraction,
    sqrt2: tuple[Fraction, Fraction],
    exp_bounds: tuple[Fraction, Fraction],
    constant_bounds: tuple[Fraction, Fraction] = (C3_LOWER, C3_UPPER),
) -> ThetaCertificate:
    c_lower, c_upper = cosine_curve_interval(theta, sqrt2)
    exp_lower, exp_upper = exp_bounds
    constant_lower, constant_upper = constant_bounds
    delta = theta - Fraction(1, 2)
    # The exact Taylor bounds already enclose the value. The additional tiny
    # rational pad also contains the independently rounded 100-digit interval
    # replay, without affecting any declared sign or decimal conclusion.
    k_lower = delta / (4 * exp_upper * constant_upper) - REPLAY_PAD
    k_upper = delta / (4 * exp_lower * constant_lower) + REPLAY_PAD
    assert 0 < k_lower <= k_upper < 1 and c_upper < 2

    root_lower = c_lower + (2 - c_lower) * k_lower
    root_upper = c_upper + (2 - c_upper) * k_upper
    old_lower = (c_lower + 2 * k_lower) / 3
    old_upper = (c_upper + 2 * k_upper) / 3

    radicand_lower = (2 - c_upper) * (1 - k_upper) / 2
    radicand_upper = (2 - c_lower) * (1 - k_lower) / 2
    sqrt_lower = sqrt_fraction_interval(radicand_lower)[0]
    sqrt_upper = sqrt_fraction_interval(radicand_upper)[1]
    new_lower = 1 - sqrt_upper
    new_upper = 1 - sqrt_lower
    return ThetaCertificate(
        theta=theta,
        c_lower=c_lower,
        c_upper=c_upper,
        k_lower=k_lower,
        k_upper=k_upper,
        root_function_lower=root_lower,
        root_function_upper=root_upper,
        old_linear_lower=old_lower,
        old_linear_upper=old_upper,
        radicand_lower=radicand_lower,
        radicand_upper=radicand_upper,
        new_simple_lower=new_lower,
        new_simple_upper=new_upper,
    )


def profile_counts(real: tuple[int, ...], pairs: tuple[int, ...]) -> dict[str, int]:
    if any(m < 1 for m in (*real, *pairs)):
        raise ValueError("multiplicities must be positive")
    simple = sum(m == 1 for m in real)
    odd = sum(m % 2 == 1 for m in real)
    dimension = sum(m >= 2 for m in real) + len(pairs)
    total = sum(real) + 2 * sum(pairs)
    return {"N": total, "S": simple, "O": odd, "d": dimension}


def profile_certificate(real: tuple[int, ...], pairs: tuple[int, ...]) -> dict[str, object]:
    counts = profile_counts(real, pairs)
    total = counts["N"]
    simple = counts["S"]
    odd = counts["O"]
    dimension = counts["d"]
    if total == 0:
        raise ValueError("profile must be nonempty")
    mass_residual = total - simple - (2 * dimension + odd - simple)
    dimension_residual = total - odd - 2 * dimension
    if dimension == 0:
        passed = total == simple == odd and mass_residual == dimension_residual == 0
        q_min: Fraction | None = None
        hilbert_residual: Fraction | None = None
    else:
        q_min = Fraction((total - simple) ** 2, dimension)
        hilbert_residual = q_min * (total - odd) - 2 * (total - simple) ** 2
        passed = mass_residual >= 0 and dimension_residual >= 0 and hilbert_residual >= 0
    return {
        "real": list(real),
        "pairs": list(pairs),
        **counts,
        "mass_residual": mass_residual,
        "dimension_residual": dimension_residual,
        "q_min": None if q_min is None else str(q_min),
        "hilbert_residual": None if hilbert_residual is None else str(hilbert_residual),
        "passed": passed,
    }


def finite_census() -> dict[str, object]:
    cases = 0
    equality_cases = 0
    strict_cases = 0
    empty_dimension_cases = 0
    first_equality: dict[str, object] | None = None
    first_strict: dict[str, object] | None = None
    for real_count in range(5):
        real_profiles = itertools.combinations_with_replacement(range(1, 8), real_count)
        for real in real_profiles:
            for pair_count in range(4):
                for pairs in itertools.combinations_with_replacement(range(1, 6), pair_count):
                    if not real and not pairs:
                        continue
                    row = profile_certificate(real, pairs)
                    if not row["passed"]:
                        raise AssertionError(f"profile failed: {row}")
                    cases += 1
                    if row["d"] == 0:
                        empty_dimension_cases += 1
                        continue
                    residual = Fraction(str(row["hilbert_residual"]))
                    if residual == 0:
                        equality_cases += 1
                        if first_equality is None:
                            first_equality = row
                    else:
                        strict_cases += 1
                        if first_strict is None:
                            first_strict = row
    return {
        "scope": {
            "real_support_cap": 4,
            "real_multiplicity_cap": 7,
            "nonreal_pair_support_cap": 3,
            "nonreal_pair_multiplicity_cap": 5,
        },
        "cases": cases,
        "equality_cases": equality_cases,
        "strict_cases": strict_cases,
        "empty_dimension_cases": empty_dimension_cases,
        "first_equality": first_equality,
        "first_strict": first_strict,
        "universal_status": "diagnostic-only; the paper proof is required",
    }


def scalar_headline_witness(target: ThetaCertificate) -> dict[str, object]:
    # Use the certified odd lower endpoint. A mixture of real triples and real
    # doubles has S=0, O=o, N0=1, and Z=(1-o)/2.
    odd = target.k_lower
    triple_support = odd
    double_support = (1 - 3 * odd) / 2
    distinct = triple_support + double_support
    a_lower = 2 - target.c_upper
    checks = {
        "nonnegative_support": triple_support >= 0 and double_support >= 0,
        "simple_real_bound": target.c_upper <= 0,
        "exp004_linear_parity": target.old_linear_upper <= 0,
        "lamzouri_distinct": distinct >= Fraction(3, 2) - a_lower / 2,
        "lamzouri_simple_plus_critical": Fraction(1) >= 3 - a_lower,
        "lamzouri_union_hypothesis_inapplicable": a_lower >= 2,
    }
    return {
        "description": "normalized real triple/double mixture with zero simple support",
        "triple_support": fraction_record(triple_support),
        "double_support": fraction_record(double_support),
        "N": fraction_record(Fraction(1)),
        "S": fraction_record(Fraction(0)),
        "O": fraction_record(odd),
        "N0": fraction_record(Fraction(1)),
        "Ns": fraction_record(Fraction(0)),
        "Z": fraction_record(distinct),
        "A_lower": fraction_record(a_lower),
        "checks": checks,
        "passed": all(checks.values()),
    }


def mpf_tuple_fraction(value: tuple[int, int, int, int]) -> Fraction:
    sign, mantissa, exponent, _bit_count = value
    result = Fraction(mantissa)
    result = result * 2**exponent if exponent >= 0 else result / 2 ** (-exponent)
    return -result if sign else result


def interval_endpoints(value: object) -> tuple[Fraction, Fraction]:
    lower_obj = value.a  # type: ignore[attr-defined]
    upper_obj = value.b  # type: ignore[attr-defined]
    return (
        mpf_tuple_fraction(lower_obj._mpi_[0]),  # type: ignore[attr-defined]
        mpf_tuple_fraction(upper_obj._mpi_[1]),  # type: ignore[attr-defined]
    )


def independent_interval_replay(
    theta: Fraction, constant_bounds: tuple[Fraction, Fraction]
) -> dict[str, object]:
    import mpmath as mp

    mp.iv.dps = 100
    def iv_fraction(value: Fraction) -> object:
        return mp.iv.mpf(value.numerator) / value.denominator

    theta_iv = iv_fraction(theta)
    constant_iv = mp.iv.mpf(
        [
            iv_fraction(constant_bounds[0]).a,
            iv_fraction(constant_bounds[1]).b,
        ]
    )
    sqrt2_iv = mp.iv.sqrt(2)
    c_iv = 2 - theta_iv / 2 - mp.iv.cos(theta_iv / sqrt2_iv) / (
        sqrt2_iv * mp.iv.sin(theta_iv / sqrt2_iv)
    )
    k_iv = (theta_iv - mp.iv.mpf("0.5")) / (4 * mp.iv.exp(1) * constant_iv)
    root_iv = c_iv + (2 - c_iv) * k_iv
    old_iv = (c_iv + 2 * k_iv) / 3
    radicand_iv = (2 - c_iv) * (1 - k_iv) / 2
    new_iv = 1 - mp.iv.sqrt(radicand_iv)
    records: dict[str, object] = {"mpmath_version": mp.__version__, "dps": 100}
    for name, interval in {
        "c": c_iv,
        "k": k_iv,
        "root_function": root_iv,
        "old_linear": old_iv,
        "radicand": radicand_iv,
        "new_simple": new_iv,
    }.items():
        lower, upper = interval_endpoints(interval)
        records[name] = {
            "lower": fraction_record(lower),
            "upper": fraction_record(upper),
            "display": str(interval),
        }
    return records


def record_interval(record: dict[str, object], name: str) -> tuple[Fraction, Fraction]:
    value = record[name]
    assert isinstance(value, dict)
    lower = value["lower"]
    upper = value["upper"]
    assert isinstance(lower, dict) and isinstance(upper, dict)
    return (
        Fraction(int(lower["numerator"]), int(lower["denominator"])),
        Fraction(int(upper["numerator"]), int(upper["denominator"])),
    )


def check_sources(repo: Path) -> dict[str, object]:
    rows = []
    for relative, expected in PINNED_INPUTS.items():
        path = repo / relative
        observed = sha256(path)
        rows.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": observed,
                "expected_sha256": expected,
                "passed": observed == expected,
            }
        )
    return {"inputs": rows, "passed": all(bool(row["passed"]) for row in rows)}


def git_identity(repo: Path) -> dict[str, object]:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    tracked_clean = (
        subprocess.run(["git", "diff", "--quiet"], cwd=repo).returncode == 0
        and subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo).returncode == 0
    )
    return {"head": head, "tracked_clean_at_start": tracked_clean}


def certificate_record(value: ThetaCertificate) -> dict[str, object]:
    return {
        field: fraction_record(getattr(value, field))
        for field in (
            "theta",
            "c_lower",
            "c_upper",
            "k_lower",
            "k_upper",
            "root_function_lower",
            "root_function_upper",
            "old_linear_lower",
            "old_linear_upper",
            "radicand_lower",
            "radicand_upper",
            "new_simple_lower",
            "new_simple_upper",
        )
    }


def compute_certificate(repo: Path) -> dict[str, object]:
    sqrt2 = sqrt_integer_interval(2)
    exp_bounds = exp_one_interval()
    target = theta_certificate(THETA, sqrt2, exp_bounds)
    root_lower = theta_certificate(ROOT_LOWER_THETA, sqrt2, exp_bounds)
    root_upper = theta_certificate(ROOT_UPPER_THETA, sqrt2, exp_bounds)
    rank_six = theta_certificate(THETA, sqrt2, exp_bounds, (C6_LOWER, C6_UPPER))
    census = finite_census()
    scalar_witness = scalar_headline_witness(target)
    replay = independent_interval_replay(THETA, (C3_LOWER, C3_UPPER))

    replay_ranges = {
        name: record_interval(replay, name)
        for name in ("c", "k", "root_function", "old_linear", "radicand", "new_simple")
    }
    exact_ranges = {
        "c": (target.c_lower, target.c_upper),
        "k": (target.k_lower, target.k_upper),
        "root_function": (target.root_function_lower, target.root_function_upper),
        "old_linear": (target.old_linear_lower, target.old_linear_upper),
        "radicand": (target.radicand_lower, target.radicand_upper),
        "new_simple": (target.new_simple_lower, target.new_simple_upper),
    }
    interval_contains_replay = all(
        exact_ranges[name][0] <= replay_ranges[name][0]
        <= replay_ranges[name][1] <= exact_ranges[name][1]
        for name in exact_ranges
    )
    source_results = check_sources(repo)
    checks = {
        "source_hashes": source_results["passed"],
        "c3_interval_ordered": C3_LOWER < C3_CENTER < C3_UPPER,
        "c6_interval_ordered": C6_LOWER < C6_CENTER < C6_UPPER,
        "sqrt2_interval": sqrt2[0] * sqrt2[0] <= 2 < sqrt2[1] * sqrt2[1],
        "e_interval": exp_bounds[0] < exp_bounds[1],
        "finite_census": census["cases"] > 10000,
        "finite_census_has_all_regimes": (
            census["equality_cases"] > 0
            and census["strict_cases"] > 0
            and census["empty_dimension_cases"] > 0
        ),
        "target_below_wang_root": target.c_upper < 0,
        "old_linear_negative": target.old_linear_upper < 0,
        "new_bound_positive": target.new_simple_lower > SIMPLE_GATE,
        "root_lower_negative": root_lower.root_function_upper < 0,
        "root_upper_positive": root_upper.root_function_lower > 0,
        "root_monotone_conditions": (
            root_lower.k_upper < 1 and root_lower.c_upper < 2
            and root_upper.k_upper < 1 and root_upper.c_upper < 2
        ),
        "scalar_headlines_allow_zero": scalar_witness["passed"],
        "rank_six_sensitivity_stronger": rank_six.new_simple_lower > target.new_simple_lower,
        "independent_interval_contained": interval_contains_replay,
    }
    passed = all(bool(value) for value in checks.values())
    return {
        "schema": SCHEMA,
        "status": "pass" if passed else "fail",
        "claim_boundary": {
            "finite_certificate": "exact rational census and directed intervals",
            "analytic_theorem": "requires the separate universal proof and adversarial review",
            "rank_six": "source-only sensitivity because the profile is not printed",
            "rh_solved": False,
        },
        "parameters": {
            "theta": fraction_record(THETA),
            "root_lower_theta": fraction_record(ROOT_LOWER_THETA),
            "root_upper_theta": fraction_record(ROOT_UPPER_THETA),
            "simple_gate": fraction_record(SIMPLE_GATE),
        },
        "source_constants": {
            "C3": {
                "center": fraction_record(C3_CENTER),
                "radius": fraction_record(C3_RADIUS),
                "lower": fraction_record(C3_LOWER),
                "upper": fraction_record(C3_UPPER),
                "role": "canonical reproducible premise",
            },
            "C6": {
                "center": fraction_record(C6_CENTER),
                "radius": fraction_record(C6_RADIUS),
                "lower": fraction_record(C6_LOWER),
                "upper": fraction_record(C6_UPPER),
                "role": "source-attributed sensitivity only",
            },
        },
        "finite_census": census,
        "scalar_headline_barrier": scalar_witness,
        "target": certificate_record(target),
        "root_bracket": {
            "lower": certificate_record(root_lower),
            "upper": certificate_record(root_upper),
            "monotonicity": "F'=c'(1-k)+(2-c)k'>0 when k<1 and c<2",
        },
        "rank_six_sensitivity": certificate_record(rank_six),
        "elementary_intervals": {
            "sqrt2_lower": fraction_record(sqrt2[0]),
            "sqrt2_upper": fraction_record(sqrt2[1]),
            "e_lower": fraction_record(exp_bounds[0]),
            "e_upper": fraction_record(exp_bounds[1]),
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
    if args.budget_seconds <= 0 or args.budget_seconds > MAX_SECONDS:
        raise ValueError(f"budget must be in (0, {MAX_SECONDS}]")
    started = time.monotonic()
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
            {"schema": "riemann-exp006-checkpoint-v1", "stage": stage},
        )
        if time.monotonic() - started > args.budget_seconds:
            raise TimeoutError(f"budget exhausted after {stage}")

    repo = Path(__file__).resolve().parents[5]
    try:
        log("stage 1/5: validate committed identity and pinned inputs")
        identity = git_identity(repo)
        if not identity["tracked_clean_at_start"]:
            raise RuntimeError("tracked repository files must be clean before canonical execution")
        sources = check_sources(repo)
        if not sources["passed"]:
            raise RuntimeError("source hash validation failed")
        checkpoint("sources-validated")

        log("stage 2/5: enumerate exact multiplicity profiles")
        census = finite_census()
        if census["cases"] <= 10000:
            raise AssertionError("finite census unexpectedly small")
        checkpoint("finite-census-complete")

        log("stage 3/5: build rational transcendental certificate")
        result = compute_certificate(repo)
        checkpoint("exact-certificate-built")

        log("stage 4/5: require every declared control")
        if not result["passed"]:
            failed = [name for name, passed in result["checks"].items() if not passed]
            raise AssertionError("failed checks: " + ", ".join(failed))
        checkpoint("controls-passed")

        log("stage 5/5: write canonical result and receipt")
        script_path = Path(__file__).resolve()
        result["execution_identity"] = {
            **identity,
            "run_py_sha256": sha256(script_path),
            "hypothesis_sha256": sha256(script_path.with_name("hypothesis.md")),
            "python": sys.version,
        }
        write_json(output / "result.json", result)
        write_json(
            output / "execution-receipt.json",
            {
                "schema": "riemann-exp006-execution-receipt-v1",
                "status": "pass",
                "elapsed_seconds": time.monotonic() - started,
                "budget_seconds": args.budget_seconds,
                "result_sha256": sha256(output / "result.json"),
                "git": identity,
            },
        )
        log("PASS: finite EXP-006 certificate completed")
        (output / "stdout.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        return 0
    except Exception as error:
        log(f"FAIL: {type(error).__name__}: {error}")
        write_json(
            output / "failure.json",
            {
                "schema": "riemann-exp006-failure-v1",
                "error_type": type(error).__name__,
                "error": str(error),
                "elapsed_seconds": time.monotonic() - started,
            },
        )
        (output / "stdout.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
