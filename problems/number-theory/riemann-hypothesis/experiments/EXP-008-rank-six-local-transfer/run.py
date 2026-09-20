"""Exact certificate for EXP-008 rank-six local Selberg transfer.

Device: CPU. Arithmetic: exact fractions with directed Taylor bounds and an
independent 100-digit mpmath interval replay. The analytic localization is
proved separately in mathematical-proof.md.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path
from types import ModuleType

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SCHEMA = "riemann-exp008-results-v1"
DECLARATION_COMMIT = "2297d2fc"
MAX_SECONDS = 120.0
THETA_EDGE = Fraction(545884, 1_000_000)
THETA_POINT = Fraction(5459, 10_000)
ROOT6_COARSE = (Fraction(545883, 1_000_000), Fraction(545884, 1_000_000))
ROOT6_FINE = (Fraction(5458837, 10_000_000), Fraction(5458838, 10_000_000))
ROOT3_FINE = (Fraction(5458846, 10_000_000), Fraction(5458847, 10_000_000))
RHO = Fraction(11, 5)

PINNED_INPUTS = {
    "problems/number-theory/riemann-hypothesis/context/source-cache/pearce-crump-2609.15329v1.pdf":
        "1476f60cf5f4a12239d0db3fdaaaf2b9d4de604c27f1a57b5a95f7b9f2a9f0be",
    "problems/number-theory/riemann-hypothesis/context/source-cache/pearce-crump-2609.15329v1.tar.gz":
        "24550f470d116b9a63148061e441d634a014d58dba1ce2dd6abe6edcfea061e4",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/artifacts/canonical/result.json":
        "3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/artifacts/canonical/result.json":
        "82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf",
    "problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/artifacts/canonical/result.json":
        "98094f267a78b88b8a976de6b6d816fbb25231869a6ad5dc8c941411bfa45947",
}

Interval = tuple[Fraction, Fraction]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def load_module(name: str, relative: str) -> ModuleType:
    path = repo_root() / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_dependencies() -> tuple[ModuleType, ModuleType]:
    exp006 = load_module(
        "riemann_exp006_for_exp008",
        "problems/number-theory/riemann-hypothesis/experiments/"
        "EXP-006-hilbert-parity-compression/run.py",
    )
    exp007 = load_module(
        "riemann_exp007_for_exp008",
        "problems/number-theory/riemann-hypothesis/experiments/"
        "EXP-007-spectral-defect-parity/run.py",
    )
    return exp006, exp007


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def interval_record(value: Interval, exp007: ModuleType) -> dict[str, object]:
    return exp007.interval_record(value)


def fraction_record(value: Fraction, exp007: ModuleType) -> dict[str, str]:
    return exp007.fraction_record(value)


def cert_interval(cert: object, stem: str) -> Interval:
    return getattr(cert, f"{stem}_lower"), getattr(cert, f"{stem}_upper")


def certificate_record(cert: object, exp007: ModuleType) -> dict[str, object]:
    names = (
        "c", "k", "root_function", "old_linear", "radicand", "weak_simple",
        "strong_discriminant", "strong_simple",
    )
    return {
        "theta": fraction_record(cert.theta, exp007),
        **{name: interval_record(cert_interval(cert, name), exp007) for name in names},
    }


def add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def analytic_energy_rho(
    theta: Fraction,
    h: Interval,
    rho: Fraction,
    sqrt2: Interval,
    pi: Interval,
    exp006: ModuleType,
    exp007: ModuleType,
) -> dict[str, Interval | bool]:
    assert h[0] > 0 and rho > 2
    radius = rho / h[1], rho / h[0]
    a = theta / sqrt2[1], theta / sqrt2[0]
    tangent = exp007.tan_interval(a, exp006)
    q = exp007.mul_positive(a, tangent)
    span = exp007.mul_positive(exp007.mul_positive(pi, (theta, theta)), radius)
    span_sq = exp007.square_positive(span)
    a_sq = exp007.square_positive(a)
    ratio = exp007.div_positive(span_sq, a_sq)
    big_b = exp007.mul_positive(q, (1 + ratio[0], 1 + ratio[1]))
    q4 = exp007.square_positive(exp007.square_positive(q))
    q_plus_span = add(q, span)
    first_den = exp007.scale_positive(exp007.square_positive(q_plus_span), Fraction(4))
    span_plus = add(span, exp007.scale_positive(q, Fraction(3, 2)))
    denominator = exp007.mul_positive(first_den, span_plus)
    b2 = exp007.div_positive(q4, denominator)
    q_half = exp007.scale_positive(q, Fraction(1, 2))
    branch_proved = b2[1] < q_half[0]
    if not branch_proved:
        raise AssertionError("analytic energy min branch was not certified")
    d = exp007.square_positive(exp007.div_positive(b2, big_b))
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


def spectral_target(
    cert: object,
    theta: Fraction,
    sqrt2: Interval,
    pi: Interval,
    exp006: ModuleType,
    exp007: ModuleType,
) -> dict[str, object]:
    c = cert_interval(cert, "c")
    kappa = cert_interval(cert, "k")
    h = cert_interval(cert, "strong_simple")
    energy = analytic_energy_rho(theta, h, RHO, sqrt2, pi, exp006, exp007)
    d = energy["d"]
    assert isinstance(d, tuple)
    alpha = exp007.scale_positive(d, Fraction(2, 5))
    beta = exp007.scale_positive(exp007.mul_positive(d, h), Fraction(4, 11))
    reserve = (
        alpha[0] * h[0] - beta[1],
        alpha[1] * h[1] - beta[0],
    )
    if reserve[0] <= 0:
        raise AssertionError("optimized spectral reserve is not positive")
    coupled = exp007.coupled_root_interval(c, kappa, alpha, beta, exp006)
    root = coupled["root"]
    gain_floor = exp007.scale_positive(
        exp007.mul_positive(
            (Fraction(1) - kappa[1], Fraction(1) - kappa[0]), reserve
        ),
        Fraction(1, 4),
    )
    strengthened = max(root[0], h[0] + gain_floor[0]), root[1]
    return {
        "rho": fraction_record(RHO, exp007),
        "h6": interval_record(h, exp007),
        "alpha": interval_record(alpha, exp007),
        "beta": interval_record(beta, exp007),
        "reserve_alpha_h_minus_beta": interval_record(reserve, exp007),
        "gain_floor": interval_record(gain_floor, exp007),
        "H6": interval_record(strengthened, exp007),
        "energy": {
            name: value if isinstance(value, bool) else interval_record(value, exp007)
            for name, value in energy.items()
        },
        "quadratic": {
            name: interval_record(value, exp007) for name, value in coupled.items()
        },
        "passed": gain_floor[0] > Fraction(9, 10**69),
    }


def independent_replay(exp006: ModuleType) -> dict[str, object]:
    import mpmath as mp

    mp.iv.dps = 100

    def iv_fraction(value: Fraction) -> object:
        return mp.iv.mpf(value.numerator) / value.denominator

    def endpoints(value: object, exp007: ModuleType) -> Interval:
        return exp007.iv_endpoints(value)

    exp007 = load_module(
        "riemann_exp007_replay_for_exp008",
        "problems/number-theory/riemann-hypothesis/experiments/"
        "EXP-007-spectral-defect-parity/run.py",
    )
    theta = iv_fraction(THETA_POINT)
    c6 = mp.iv.mpf([
        iv_fraction(exp006.C6_LOWER).a,
        iv_fraction(exp006.C6_UPPER).b,
    ])
    sqrt2 = mp.iv.sqrt(2)
    c = 2 - theta / 2 - mp.iv.cos(theta / sqrt2) / (
        sqrt2 * mp.iv.sin(theta / sqrt2)
    )
    kappa = (theta - mp.iv.mpf("0.5")) / (4 * mp.iv.exp(1) * c6)
    b0 = 1 - kappa
    q_pair = 2 - c
    h = (4 - b0 - mp.iv.sqrt(b0 * (b0 + 8 * (q_pair - 1)))) / 4
    rho = iv_fraction(RHO)
    radius = rho / h
    a = theta / sqrt2
    q = a * mp.iv.sin(a) / mp.iv.cos(a)
    span = mp.iv.pi * theta * radius
    big_b = q * (1 + span**2 / a**2)
    b2 = q**4 / (4 * (q + span) ** 2 * (span + 3 * q / 2))
    d = (b2 / big_b) ** 2
    alpha = 2 * d / 5
    beta = 4 * d * h / 11
    reserve = alpha * h - beta
    gain_floor = (1 - kappa) * reserve / 4
    linear = 4 - (1 + alpha) * (1 - kappa)
    constant = 2 - (1 - kappa) * (q_pair + beta)
    coupled = (linear - mp.iv.sqrt(linear**2 - 8 * constant)) / 4
    values = {
        "c": c,
        "kappa": kappa,
        "h6": h,
        "radius": radius,
        "d": d,
        "alpha": alpha,
        "beta": beta,
        "reserve": reserve,
        "gain_floor": gain_floor,
        "H6": coupled,
    }
    return {
        "mpmath_version": mp.__version__,
        "dps": 100,
        "intervals": {
            name: interval_record(endpoints(value, exp007), exp007)
            for name, value in values.items()
        },
    }


def record_to_interval(record: dict[str, object]) -> Interval:
    lower = record["lower"]
    upper = record["upper"]
    assert isinstance(lower, dict) and isinstance(upper, dict)
    return Fraction(int(lower["numerator"]), int(lower["denominator"])), Fraction(
        int(upper["numerator"]), int(upper["denominator"])
    )


def overlaps(left: Interval, right: Interval) -> bool:
    return max(left[0], right[0]) <= min(left[1], right[1])


def check_sources(repo: Path) -> dict[str, object]:
    rows = []
    for relative, expected in PINNED_INPUTS.items():
        path = repo / relative
        observed = sha256(path)
        rows.append({
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": observed,
            "expected_sha256": expected,
            "passed": observed == expected,
        })
    return {"inputs": rows, "passed": all(row["passed"] for row in rows)}


def git_identity(repo: Path) -> dict[str, object]:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    tracked_clean = (
        subprocess.run(["git", "diff", "--quiet"], cwd=repo).returncode == 0
        and subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo).returncode == 0
    )
    return {"head": head, "tracked_clean_at_start": tracked_clean}


def compute_certificate(repo: Path) -> dict[str, object]:
    exp006, exp007 = load_dependencies()
    sqrt2 = exp006.sqrt_integer_interval(2, digits=110)
    e_bounds = exp006.exp_one_interval(terms=120)
    pi = exp007.pi_interval()
    c3_bounds = (exp006.C3_LOWER, exp006.C3_UPPER)
    c6_bounds = (exp006.C6_LOWER, exp006.C6_UPPER)

    def cert(theta: Fraction, bounds: Interval) -> object:
        return exp006.theta_certificate(theta, sqrt2, e_bounds, bounds)

    edge3 = cert(THETA_EDGE, c3_bounds)
    edge6 = cert(THETA_EDGE, c6_bounds)
    point3 = cert(THETA_POINT, c3_bounds)
    point6 = cert(THETA_POINT, c6_bounds)
    coarse6 = (cert(ROOT6_COARSE[0], c6_bounds), cert(ROOT6_COARSE[1], c6_bounds))
    fine6 = (cert(ROOT6_FINE[0], c6_bounds), cert(ROOT6_FINE[1], c6_bounds))
    fine3 = (cert(ROOT3_FINE[0], c3_bounds), cert(ROOT3_FINE[1], c3_bounds))
    spectral = spectral_target(point6, THETA_POINT, sqrt2, pi, exp006, exp007)
    replay = independent_replay(exp006)

    point_exact = {
        "c": cert_interval(point6, "c"),
        "kappa": cert_interval(point6, "k"),
        "h6": cert_interval(point6, "strong_simple"),
        "radius": record_to_interval(spectral["energy"]["radius"]),
        "d": record_to_interval(spectral["energy"]["d"]),
        "alpha": record_to_interval(spectral["alpha"]),
        "beta": record_to_interval(spectral["beta"]),
        "reserve": record_to_interval(spectral["reserve_alpha_h_minus_beta"]),
        "gain_floor": record_to_interval(spectral["gain_floor"]),
        "H6": record_to_interval(spectral["H6"]),
    }
    replay_intervals = {
        name: record_to_interval(record)
        for name, record in replay["intervals"].items()
    }
    overlap_checks = {
        name: overlaps(point_exact[name], replay_intervals[name]) for name in point_exact
    }
    point_improvement = (
        point6.strong_simple_lower - point3.strong_simple_upper,
        point6.strong_simple_upper - point3.strong_simple_lower,
    )
    source_results = check_sources(repo)
    checks = {
        "source_hashes": source_results["passed"],
        "c6_interval_below_c3": exp006.C6_UPPER < exp006.C3_LOWER,
        "rank_six_coarse_lower_negative": coarse6[0].strong_simple_upper < 0,
        "rank_six_coarse_upper_positive": coarse6[1].strong_simple_lower > 0,
        "rank_six_fine_lower_negative": fine6[0].strong_simple_upper < 0,
        "rank_six_fine_upper_positive": fine6[1].strong_simple_lower > 0,
        "rank_three_fine_lower_negative": fine3[0].strong_simple_upper < 0,
        "rank_three_fine_upper_positive": fine3[1].strong_simple_lower > 0,
        "strictly_earlier_onset": fine6[1].theta < fine3[0].theta,
        "edge_rank_three_negative": edge3.strong_simple_upper < 0,
        "edge_rank_six_above_2_5e_7": edge6.strong_simple_lower > Fraction(25, 10**8),
        "point_h6_above_1_776e_5": point6.strong_simple_lower > Fraction(1776, 10**8),
        "point_improvement_above_9_26e_7": point_improvement[0] > Fraction(926, 10**9),
        "spectral_rho_above_two": RHO > 2,
        "spectral_gain_above_9e_69": spectral["passed"],
        "independent_interval_overlap": all(overlap_checks.values()),
    }
    passed = all(bool(value) for value in checks.values())
    return {
        "schema": SCHEMA,
        "status": "pass" if passed else "fail",
        "claim_boundary": {
            "rank_six_profile": "attributed source-certified input; coefficients not printed",
            "localization": "proved for every fixed finite rank in mathematical-proof.md",
            "scalar_certificate": "directed exact intervals plus independent replay",
            "effective_starting_height": False,
            "rh_solved": False,
        },
        "source_constants": {
            "C3": {
                "lower": fraction_record(exp006.C3_LOWER, exp007),
                "upper": fraction_record(exp006.C3_UPPER, exp007),
            },
            "C6": {
                "lower": fraction_record(exp006.C6_LOWER, exp007),
                "upper": fraction_record(exp006.C6_UPPER, exp007),
            },
        },
        "root_brackets": {
            "rank_six_coarse": {
                "lower": certificate_record(coarse6[0], exp007),
                "upper": certificate_record(coarse6[1], exp007),
            },
            "rank_six_fine": {
                "lower": certificate_record(fine6[0], exp007),
                "upper": certificate_record(fine6[1], exp007),
            },
            "rank_three_fine": {
                "lower": certificate_record(fine3[0], exp007),
                "upper": certificate_record(fine3[1], exp007),
            },
            "uniqueness": "F'=c'(1-k)+(2-c)k'>0 on the certified range",
        },
        "edge_theta": {
            "rank_three": certificate_record(edge3, exp007),
            "rank_six": certificate_record(edge6, exp007),
        },
        "point_theta": {
            "rank_three": certificate_record(point3, exp007),
            "rank_six": certificate_record(point6, exp007),
            "h6_minus_h3": interval_record(point_improvement, exp007),
        },
        "spectral_optimized": spectral,
        "independent_replay": replay,
        "independent_overlap_checks": overlap_checks,
        "elementary_intervals": {
            "sqrt2": interval_record(sqrt2, exp007),
            "e": interval_record(e_bounds, exp007),
            "pi": interval_record(pi, exp007),
        },
        "sources": source_results,
        "checks": checks,
        "passed": passed,
    }


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

    repo = repo_root()
    try:
        log("stage 1/4: validate clean identity and pinned inputs")
        identity = git_identity(repo)
        if not identity["tracked_clean_at_start"]:
            raise RuntimeError("tracked repository files must be clean before canonical execution")
        sources = check_sources(repo)
        if not sources["passed"]:
            raise RuntimeError("source hash validation failed")
        write_json(output / "checkpoint.json", {"schema": SCHEMA, "stage": "sources-validated"})

        log("stage 2/4: compute directed rank-three and rank-six intervals")
        result = compute_certificate(repo)
        if not result["passed"]:
            raise AssertionError("one or more EXP-008 checks failed")
        write_json(output / "checkpoint.json", {"schema": SCHEMA, "stage": "certificate-complete"})

        log("stage 3/4: write canonical result")
        elapsed = time.monotonic() - started
        if elapsed > args.budget_seconds:
            raise TimeoutError("budget exhausted before result write")
        result["execution"] = {
            "elapsed_seconds": elapsed,
            "budget_seconds": args.budget_seconds,
            "device": "CPU",
            "arithmetic": "exact fractions, directed Taylor bounds, mpmath.iv replay",
            "git": identity,
            "declaration_commit": DECLARATION_COMMIT,
        }
        result_path = output / "result.json"
        write_json(result_path, result)

        log("stage 4/4: bind execution receipt")
        receipt = {
            "schema": "riemann-exp008-execution-receipt-v1",
            "status": "pass",
            "result_sha256": sha256(result_path),
            "runner_sha256": sha256(Path(__file__)),
            "git": identity,
            "elapsed_seconds": time.monotonic() - started,
            "budget_seconds": args.budget_seconds,
        }
        write_json(output / "execution-receipt.json", receipt)
        write_json(output / "checkpoint.json", {"schema": SCHEMA, "stage": "complete"})
        (output / "stdout.txt").write_text(
            "\n".join(log_lines) + "\n", encoding="utf-8", newline="\n",
        )
        return 0
    except Exception as exc:
        log(f"FAIL: {type(exc).__name__}: {exc}")
        write_json(output / "failure.json", {
            "schema": "riemann-exp008-failure-v1",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "elapsed_seconds": time.monotonic() - started,
        })
        (output / "stdout.txt").write_text(
            "\n".join(log_lines) + "\n", encoding="utf-8", newline="\n",
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
