"""Exact certificate for EXP-007 spectral-defect parity coupling.

Device: CPU. Arithmetic: exact fractions with directed Taylor bounds, plus an
independent 100-digit mpmath interval replay. Computation tests the declared
interfaces and frozen example. The universal theorem remains the responsibility
of mathematical-proof.md.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from types import ModuleType


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


SCHEMA = "riemann-exp007-results-v1"
DECLARATION_COMMIT = "a2abdcc8360399b3fa42aaea9245e4b83352c30f"
THETA = Fraction(5459, 10000)
SENSITIVITY_THETA = Fraction(3, 4)
MAX_SECONDS = 180.0

PINNED_INPUTS = {
    "problems/number-theory/riemann-hypothesis/context/2026-09-20-interdisciplinary-update-and-defect-parity.md":
        "da64258b4ecba32ab352983cdbb6de47fbe75f37c59e2d783194b5a1d8da4c11",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/hypothesis.md":
        "1041a7ecb357b47a448f3c75a3aa1f3328dad982fe223be7ee7a789698c2e27b",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-002-short-interval-stability/mathematical-proof.md":
        "36031922ed09440bdf769272431d98c111fb8155a50fc727628a0a65112fc54c",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/mathematical-proof.md":
        "9df9ff826772edb2d6097af58684c95b1d421de641eb0746ae459f5aa58bc6bc",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/artifacts/result.json":
        "4c6e6ae37dba53164092da631c2aa120d084bcb32e711723ee819e6f6095f85e",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/artifacts/canonical/result.json":
        "3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/artifacts/canonical/result.json":
        "82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf",
}


Interval = tuple[Fraction, Fraction]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def load_exp006(repo: Path) -> ModuleType:
    path = (
        repo
        / "problems/number-theory/riemann-hypothesis/experiments"
        / "EXP-006-hilbert-parity-compression/run.py"
    )
    spec = importlib.util.spec_from_file_location("riemann_exp006", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load EXP-006 exact arithmetic")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_record(value: Fraction, digits: int = 90) -> dict[str, str]:
    with localcontext() as context:
        context.prec = digits + 20
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": format(decimal, f".{digits}g"),
    }


def interval_record(value: Interval, digits: int = 90) -> dict[str, object]:
    return {
        "lower": fraction_record(value[0], digits),
        "upper": fraction_record(value[1], digits),
        "width": fraction_record(value[1] - value[0], digits),
    }


def add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def mul_positive(left: Interval, right: Interval) -> Interval:
    assert left[0] >= 0 and right[0] >= 0
    return left[0] * right[0], left[1] * right[1]


def div_positive(left: Interval, right: Interval) -> Interval:
    assert left[0] >= 0 and right[0] > 0
    return left[0] / right[1], left[1] / right[0]


def scale_positive(value: Interval, scalar: Fraction) -> Interval:
    assert scalar >= 0
    return value[0] * scalar, value[1] * scalar


def square_positive(value: Interval) -> Interval:
    assert value[0] >= 0
    return value[0] ** 2, value[1] ** 2


def atan_interval(x: Fraction, last_index: int = 160) -> Interval:
    assert 0 <= x <= 1 and last_index >= 1
    total = Fraction(0)
    power = x
    lower: Fraction | None = None
    upper: Fraction | None = None
    for index in range(last_index + 1):
        term = power / (2 * index + 1)
        total += term if index % 2 == 0 else -term
        if index in (last_index - 1, last_index):
            if index % 2 == 0:
                upper = total
            else:
                lower = total
        power *= x * x
    assert lower is not None and upper is not None and lower <= upper
    return lower, upper


def pi_interval() -> Interval:
    # Machin: pi = 16 atan(1/5) - 4 atan(1/239).
    a = atan_interval(Fraction(1, 5))
    b = atan_interval(Fraction(1, 239))
    lower = 16 * a[0] - 4 * b[1]
    upper = 16 * a[1] - 4 * b[0]
    assert lower < upper
    return lower, upper


def tan_interval(x: Interval, exp006: ModuleType) -> Interval:
    sin_lower = exp006.sin_interval(x[0])[0]
    sin_upper = exp006.sin_interval(x[1])[1]
    cos_lower = exp006.cos_interval(x[1])[0]
    cos_upper = exp006.cos_interval(x[0])[1]
    assert 0 < cos_lower <= cos_upper
    return sin_lower / cos_upper, sin_upper / cos_lower


def analytic_energy(
    theta: Fraction,
    h: Interval,
    sqrt2: Interval,
    pi: Interval,
    exp006: ModuleType,
) -> dict[str, Interval | bool]:
    assert h[0] > 0
    radius = Fraction(4) / h[1], Fraction(4) / h[0]
    a = theta / sqrt2[1], theta / sqrt2[0]
    tangent = tan_interval(a, exp006)
    q = mul_positive(a, tangent)
    span = mul_positive(mul_positive(pi, (theta, theta)), radius)
    span_sq = square_positive(span)
    a_sq = square_positive(a)
    ratio = div_positive(span_sq, a_sq)
    one_plus_ratio = 1 + ratio[0], 1 + ratio[1]
    big_b = mul_positive(q, one_plus_ratio)

    q4 = square_positive(square_positive(q))
    q_plus_span = add(q, span)
    first_den = scale_positive(square_positive(q_plus_span), Fraction(4))
    span_plus = add(span, scale_positive(q, Fraction(3, 2)))
    denominator = mul_positive(first_den, span_plus)
    b2 = div_positive(q4, denominator)
    q_half = scale_positive(q, Fraction(1, 2))
    branch_proved = b2[1] < q_half[0]
    if not branch_proved:
        raise AssertionError("analytic energy min branch was not certified")
    b = b2
    d = square_positive(div_positive(b, big_b))
    return {
        "radius": radius,
        "a": a,
        "tan_a": tangent,
        "q": q,
        "span": span,
        "B": big_b,
        "b2": b2,
        "q_half": q_half,
        "min_branch_b2": branch_proved,
        "d": d,
    }


def coupled_root_interval(
    c: Interval,
    kappa: Interval,
    alpha: Interval,
    beta: Interval,
    exp006: ModuleType,
) -> dict[str, Interval]:
    q_pair = Fraction(2) - c[1], Fraction(2) - c[0]
    one_minus_k = Fraction(1) - kappa[1], Fraction(1) - kappa[0]
    one_plus_alpha = Fraction(1) + alpha[0], Fraction(1) + alpha[1]
    product = mul_positive(one_plus_alpha, one_minus_k)
    linear = Fraction(4) - product[1], Fraction(4) - product[0]
    q_plus_beta = add(q_pair, beta)
    constant_product = mul_positive(one_minus_k, q_plus_beta)
    constant = Fraction(2) - constant_product[1], Fraction(2) - constant_product[0]
    assert linear[0] > 0
    linear_sq = square_positive(linear)
    discriminant = linear_sq[0] - 8 * constant[1], linear_sq[1] - 8 * constant[0]
    assert discriminant[0] > 0
    sqrt_lower = exp006.sqrt_fraction_interval(discriminant[0], digits=110)[0]
    sqrt_upper = exp006.sqrt_fraction_interval(discriminant[1], digits=110)[1]
    root = (linear[0] - sqrt_upper) / 4, (linear[1] - sqrt_lower) / 4
    return {
        "q_pair": q_pair,
        "one_minus_kappa": one_minus_k,
        "linear_coefficient": linear,
        "constant_coefficient": constant,
        "discriminant": discriminant,
        "root": root,
    }


def gc(t: Fraction, x: Fraction) -> Fraction:
    positive_part = max(x - t, Fraction(0))
    return x * x - t * x - positive_part * positive_part


def psi(t: Fraction, x: Fraction) -> Fraction:
    if x <= t:
        return (x - 1) ** 2
    return (t - 1) * (2 * x - t - 1)


def weak_compositions(total: int, parts: int) -> list[tuple[int, ...]]:
    if parts == 0:
        return [()] if total == 0 else []
    if parts == 1:
        return [(total,)]
    rows: list[tuple[int, ...]] = []
    for head in range(total + 1):
        rows.extend((head, *tail) for tail in weak_compositions(total - head, parts - 1))
    return rows


def spectral_census() -> dict[str, object]:
    cases = 0
    equality_points = 0
    strict_points = 0
    for t in (Fraction(2), Fraction(5, 2), Fraction(3), Fraction(7, 2), Fraction(4)):
        for support_size in range(7):
            for numerators in weak_compositions(4 * support_size, support_size):
                eigenvalues = tuple(Fraction(value, 4) for value in numerators)
                aggregate_psi = sum((psi(t, value) for value in eigenvalues), Fraction(0))
                aggregate_gc = sum((gc(t, value) for value in eigenvalues), Fraction(0))
                if aggregate_psi != aggregate_gc + (t - 1) * support_size:
                    raise AssertionError("affine spectral identity failed")
                for value in eigenvalues:
                    residual = psi(t, value) - psi(Fraction(2), value)
                    if residual < 0:
                        raise AssertionError("Psi_t monotonicity failed")
                    if residual == 0:
                        equality_points += 1
                    else:
                        strict_points += 1
                cases += 1
    return {
        "t_values": ["2", "5/2", "3", "7/2", "4"],
        "grid_denominator": 4,
        "support_size_cap": 6,
        "spectra": cases,
        "equality_eigenvalues": equality_points,
        "strict_eigenvalues": strict_points,
        "passed": cases > 10000 and strict_points > 0,
    }


def multiplicity_census(exp006: ModuleType) -> dict[str, object]:
    cases = 0
    defect_trials = 0
    equality = 0
    strict = 0
    empty_dimension = 0
    for real_count in range(5):
        for real in itertools.combinations_with_replacement(range(1, 8), real_count):
            for pair_count in range(4):
                for pairs in itertools.combinations_with_replacement(range(1, 6), pair_count):
                    if not real and not pairs:
                        continue
                    counts = exp006.profile_counts(real, pairs)
                    n, s, o, dimension = (
                        counts["N"], counts["S"], counts["O"], counts["d"]
                    )
                    cases += 1
                    if dimension == 0:
                        if not n == s == o:
                            raise AssertionError("empty-dimension branch failed")
                        empty_dimension += 1
                        continue
                    t = Fraction(n - s, dimension)
                    if t < 2:
                        raise AssertionError("optimizing parameter below two")
                    for d2, extra in (
                        (Fraction(0), Fraction(0)),
                        (Fraction(1, 7), Fraction(0)),
                        (Fraction(2, 9), Fraction(1, 11)),
                    ):
                        dt = d2 + extra
                        q_lower = Fraction(s) + Fraction((n - s) ** 2, dimension) + dt
                        residual = (
                            (q_lower - s - d2) * (n - o) - 2 * (n - s) ** 2
                        )
                        if residual < 0:
                            raise AssertionError("defect-parity product failed")
                        if residual == 0:
                            equality += 1
                        else:
                            strict += 1
                        defect_trials += 1
    return {
        "profiles": cases,
        "defect_trials": defect_trials,
        "equality_trials": equality,
        "strict_trials": strict,
        "empty_dimension_profiles": empty_dimension,
        "scope": {
            "real_support_cap": 4,
            "real_multiplicity_cap": 7,
            "nonreal_pair_support_cap": 3,
            "nonreal_pair_multiplicity_cap": 5,
        },
        "passed": cases == 18479 and equality > 0 and strict > 0 and empty_dimension > 0,
    }


def exact_target(exp006: ModuleType) -> dict[str, object]:
    sqrt2 = exp006.sqrt_integer_interval(2, digits=110)
    e_bounds = exp006.exp_one_interval(terms=120)
    pi = pi_interval()
    target = exp006.theta_certificate(THETA, sqrt2, e_bounds)
    c = target.c_lower, target.c_upper
    kappa = target.k_lower, target.k_upper
    h = target.strong_simple_lower, target.strong_simple_upper
    energy = analytic_energy(THETA, h, sqrt2, pi, exp006)
    d = energy["d"]
    assert isinstance(d, tuple)
    alpha = scale_positive(d, Fraction(2, 5))
    # Since R=4/h exactly, beta=4d/(5R)=d*h/5.
    beta = scale_positive(mul_positive(d, h), Fraction(1, 5))
    reserve = beta
    coupled = coupled_root_interval(c, kappa, alpha, beta, exp006)
    root = coupled["root"]
    naive_gain = root[0] - h[1], root[1] - h[0]
    # Let F be the strengthened upward-opening quadratic.  Its derivative on
    # [h,H] is negative and at least -4, while
    # F(h)=(1-kappa)(alpha*h-beta)=(1-kappa)*beta.  The mean value theorem
    # therefore gives H-h >= (1-kappa)*beta/4.  This correlated certificate
    # avoids subtracting two roots whose independent source intervals are much
    # wider than the deliberately tiny analytic improvement.
    gain_floor = scale_positive(
        mul_positive(
            (Fraction(1) - kappa[1], Fraction(1) - kappa[0]),
            beta,
        ),
        Fraction(1, 4),
    )
    gain = gain_floor[0], naive_gain[1]
    strengthened_root = max(root[0], h[0] + gain_floor[0]), root[1]
    if gain[0] <= 0 or gain[1] < gain[0]:
        raise AssertionError("frozen correlated gain is not strictly positive")
    records: dict[str, object] = {
        "theta": fraction_record(THETA),
        "c": interval_record(c),
        "kappa": interval_record(kappa),
        "h3": interval_record(h),
        "sqrt2": interval_record(sqrt2),
        "pi": interval_record(pi),
        "alpha": interval_record(alpha),
        "beta": interval_record(beta),
        "symbolic_reserve_alpha_h_minus_beta": interval_record(reserve),
        "H": interval_record(strengthened_root),
        "naive_independent_H_minus_h3": interval_record(naive_gain),
        "certified_gain_floor": interval_record(gain_floor),
        "gain_H_minus_h3": interval_record(gain),
    }
    for name, value in energy.items():
        records[f"energy_{name}"] = value if isinstance(value, bool) else interval_record(value)
    for name, value in coupled.items():
        records[f"quadratic_{name}"] = interval_record(value)
    records["passed"] = bool(gain[0] > 0 and energy["min_branch_b2"])
    return records


def sensitivity_target(exp006: ModuleType) -> dict[str, object]:
    sqrt2 = exp006.sqrt_integer_interval(2, digits=110)
    e_bounds = exp006.exp_one_interval(terms=120)
    target = exp006.theta_certificate(SENSITIVITY_THETA, sqrt2, e_bounds)
    c = target.c_lower, target.c_upper
    kappa = target.k_lower, target.k_upper
    h = target.strong_simple_lower, target.strong_simple_upper
    pressure = Fraction(1, 12500)
    epsilon = Fraction(443239, 1_000_000_000)
    k = 2256
    frame = 2 * k + 1
    alpha = (Fraction(k) * epsilon / frame,) * 2
    beta = (Fraction(2 * k) * pressure / frame,) * 2
    coupled = coupled_root_interval(c, kappa, alpha, beta, exp006)
    root = coupled["root"]
    gain = root[0] - h[1], root[1] - h[0]
    pressure_only = (
        (frame * c[0] - 2 * k * pressure) / (frame - k * epsilon),
        (frame * c[1] - 2 * k * pressure) / (frame - k * epsilon),
    )
    return {
        "theta": fraction_record(SENSITIVITY_THETA),
        "pressure": fraction_record(pressure),
        "epsilon": fraction_record(epsilon),
        "k": k,
        "frame": frame,
        "h3": interval_record(h),
        "coupled_product_root": interval_record(root),
        "coupled_gain_over_h3": interval_record(gain),
        "pressure_only_bound": interval_record(pressure_only),
        "headline_control": {
            "coupled_root_improves_h3": gain[0] > 0,
            "coupled_root_is_below_h3": gain[1] < 0,
            "pressure_only_remains_stronger": pressure_only[0] > root[1],
            "comparison_classified": gain[0] > 0 or gain[1] < 0,
        },
    }


def mpf_tuple_fraction(value: tuple[int, int, int, int]) -> Fraction:
    sign, mantissa, exponent, _bits = value
    result = Fraction(mantissa)
    result = result * 2**exponent if exponent >= 0 else result / 2 ** (-exponent)
    return -result if sign else result


def iv_endpoints(value: object) -> Interval:
    lower_obj = value.a  # type: ignore[attr-defined]
    upper_obj = value.b  # type: ignore[attr-defined]
    return (
        mpf_tuple_fraction(lower_obj._mpi_[0]),  # type: ignore[attr-defined]
        mpf_tuple_fraction(upper_obj._mpi_[1]),  # type: ignore[attr-defined]
    )


def independent_replay(exp006: ModuleType) -> dict[str, object]:
    import mpmath as mp

    mp.iv.dps = 100

    def iv_fraction(value: Fraction) -> object:
        return mp.iv.mpf(value.numerator) / value.denominator

    theta = iv_fraction(THETA)
    c3 = mp.iv.mpf(
        [
            iv_fraction(exp006.C3_LOWER).a,
            iv_fraction(exp006.C3_UPPER).b,
        ]
    )
    sqrt2 = mp.iv.sqrt(2)
    c = 2 - theta / 2 - mp.iv.cos(theta / sqrt2) / (
        sqrt2 * mp.iv.sin(theta / sqrt2)
    )
    kappa = (theta - mp.iv.mpf("0.5")) / (4 * mp.iv.exp(1) * c3)
    b0 = 1 - kappa
    q_pair = 2 - c
    h = (4 - b0 - mp.iv.sqrt(b0 * (b0 + 8 * (q_pair - 1)))) / 4
    radius = 4 / h
    a = theta / sqrt2
    q = a * mp.iv.sin(a) / mp.iv.cos(a)
    span = mp.iv.pi * theta * radius
    big_b = q * (1 + span**2 / a**2)
    b2 = q**4 / (4 * (q + span) ** 2 * (span + 3 * q / 2))
    d = (b2 / big_b) ** 2
    alpha = 2 * d / 5
    beta = d * h / 5
    linear = 4 - (1 + alpha) * (1 - kappa)
    constant = 2 - (1 - kappa) * (q_pair + beta)
    discriminant = linear**2 - 8 * constant
    coupled = (linear - mp.iv.sqrt(discriminant)) / 4
    gain = coupled - h
    gain_floor = (1 - kappa) * beta / 4
    intervals = {
        "c": c,
        "kappa": kappa,
        "h3": h,
        "radius": radius,
        "a": a,
        "q": q,
        "span": span,
        "B": big_b,
        "b2": b2,
        "d": d,
        "alpha": alpha,
        "beta": beta,
        "H": coupled,
        "gain": gain,
        "gain_floor": gain_floor,
    }
    return {
        "mpmath_version": mp.__version__,
        "dps": 100,
        "intervals": {
            name: {**interval_record(iv_endpoints(value)), "display": str(value)}
            for name, value in intervals.items()
        },
    }


def interval_from_record(record: dict[str, object]) -> Interval:
    lower = record["lower"]
    upper = record["upper"]
    assert isinstance(lower, dict) and isinstance(upper, dict)
    return (
        Fraction(int(lower["numerator"]), int(lower["denominator"])),
        Fraction(int(upper["numerator"]), int(upper["denominator"])),
    )


def check_replay_overlap(exact: dict[str, object], replay: dict[str, object]) -> dict[str, bool]:
    mapping = {
        "c": "c",
        "kappa": "kappa",
        "h3": "h3",
        "radius": "energy_radius",
        "a": "energy_a",
        "q": "energy_q",
        "span": "energy_span",
        "B": "energy_B",
        "b2": "energy_b2",
        "d": "energy_d",
        "alpha": "alpha",
        "beta": "beta",
        "H": "quadratic_root",
        "gain": "naive_independent_H_minus_h3",
        "gain_floor": "certified_gain_floor",
    }
    replay_intervals = replay["intervals"]
    assert isinstance(replay_intervals, dict)
    checks: dict[str, bool] = {}
    for replay_name, exact_name in mapping.items():
        exact_record = exact[exact_name]
        replay_record = replay_intervals[replay_name]
        assert isinstance(exact_record, dict) and isinstance(replay_record, dict)
        exact_interval = interval_from_record(exact_record)
        replay_interval = interval_from_record(replay_record)
        checks[replay_name] = max(exact_interval[0], replay_interval[0]) <= min(
            exact_interval[1], replay_interval[1]
        )
    return checks


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


def assemble_result(
    sources: dict[str, object],
    spectral: dict[str, object],
    multiplicity: dict[str, object],
    target: dict[str, object],
    sensitivity: dict[str, object],
    replay: dict[str, object],
) -> dict[str, object]:
    replay_checks = check_replay_overlap(target, replay)
    checks = {
        "source_hashes": sources["passed"],
        "spectral_census": spectral["passed"],
        "multiplicity_census": multiplicity["passed"],
        "frozen_exact_gain": target["passed"],
        "sensitivity_comparison_classified": sensitivity["headline_control"]["comparison_classified"],
        "sensitivity_headline_boundary": sensitivity["headline_control"]["pressure_only_remains_stronger"],
        "independent_replay_overlaps": all(replay_checks.values()),
    }
    return {
        "schema": SCHEMA,
        "status": "pass" if all(bool(value) for value in checks.values()) else "fail",
        "claim_boundary": {
            "finite_theorem": "requires the separate written proof and adversarial audit",
            "numerical_certificate": "directed rational intervals plus independent mpmath.iv overlap",
            "onset_exponent_improved": False,
            "global_record": False,
            "rh_solved": False,
        },
        "sources": sources,
        "spectral_census": spectral,
        "multiplicity_census": multiplicity,
        "target": target,
        "sensitivity": sensitivity,
        "independent_interval_replay": replay,
        "replay_overlap": replay_checks,
        "checks": checks,
        "passed": all(bool(value) for value in checks.values()),
    }


def compute(repo: Path) -> dict[str, object]:
    exp006 = load_exp006(repo)
    return assemble_result(
        check_sources(repo),
        spectral_census(),
        multiplicity_census(exp006),
        exact_target(exp006),
        sensitivity_target(exp006),
        independent_replay(exp006),
    )


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


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
        write_json(output / "checkpoint.json", {"schema": "riemann-exp007-checkpoint-v1", "stage": stage})
        if time.monotonic() - started > args.budget_seconds:
            raise TimeoutError(f"budget exhausted after {stage}")

    repo = repo_root()
    try:
        log("stage 1/6: validate clean committed execution and pinned inputs")
        identity = git_identity(repo)
        if not identity["tracked_clean_at_start"]:
            raise RuntimeError("tracked repository files must be clean before canonical execution")
        sources = check_sources(repo)
        if not sources["passed"]:
            raise RuntimeError("source hash validation failed")
        checkpoint("sources-validated")

        log("stage 2/6: enumerate exact spectral profiles")
        spectral = spectral_census()
        if not spectral["passed"]:
            raise AssertionError("spectral census failed")
        checkpoint("spectral-census-complete")

        log("stage 3/6: enumerate multiplicity and defect profiles")
        exp006 = load_exp006(repo)
        multiplicity = multiplicity_census(exp006)
        if not multiplicity["passed"]:
            raise AssertionError("multiplicity census failed")
        checkpoint("multiplicity-census-complete")

        log("stage 4/6: build directed rational target certificate")
        target = exact_target(exp006)
        sensitivity = sensitivity_target(exp006)
        checkpoint("exact-target-complete")

        log("stage 5/6: replay at 100-digit independent interval precision")
        replay = independent_replay(exp006)
        replay_checks = check_replay_overlap(target, replay)
        if not all(replay_checks.values()):
            failed = [name for name, passed in replay_checks.items() if not passed]
            raise AssertionError("replay overlap failed: " + ", ".join(failed))
        checkpoint("independent-replay-complete")

        log("stage 6/6: assemble canonical result")
        result = assemble_result(
            sources, spectral, multiplicity, target, sensitivity, replay
        )
        if not result["passed"]:
            failed = [name for name, passed in result["checks"].items() if not passed]
            raise AssertionError("failed checks: " + ", ".join(failed))
        script_path = Path(__file__).resolve()
        result["execution_identity"] = {
            **identity,
            "declaration_commit": DECLARATION_COMMIT,
            "run_py_sha256": sha256(script_path),
            "hypothesis_sha256": sha256(script_path.with_name("hypothesis.md")),
            "python": sys.version,
        }
        write_json(output / "result.json", result)
        write_json(
            output / "execution-receipt.json",
            {
                "schema": "riemann-exp007-execution-receipt-v1",
                "status": "pass",
                "elapsed_seconds": time.monotonic() - started,
                "budget_seconds": args.budget_seconds,
                "result_sha256": sha256(output / "result.json"),
                "git": identity,
            },
        )
        log("PASS: EXP-007 exact certificate completed")
        (output / "stdout.txt").write_text(
            "\n".join(log_lines) + "\n", encoding="utf-8", newline="\n",
        )
        return 0
    except Exception as error:
        log(f"FAIL: {type(error).__name__}: {error}")
        write_json(
            output / "failure.json",
            {
                "schema": "riemann-exp007-failure-v1",
                "error_type": type(error).__name__,
                "error": str(error),
                "elapsed_seconds": time.monotonic() - started,
            },
        )
        (output / "stdout.txt").write_text(
            "\n".join(log_lines) + "\n", encoding="utf-8", newline="\n",
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
