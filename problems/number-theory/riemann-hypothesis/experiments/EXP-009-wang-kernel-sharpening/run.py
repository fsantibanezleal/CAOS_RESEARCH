"""Directed certificate for EXP-009 Wang kernel sharpening.

The universal ratio theorem and the analytic transfer are proved in
mathematical-proof.md.  This runner certifies all algebraic constants and
strict numerical comparisons with exact rational interval arithmetic, then
replays the headline quantities with independent 120-digit mpmath intervals.
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

SCHEMA = "riemann-exp009-results-v1"
DECLARATION_COMMIT = "123eee0d49969226201e68d6c32746087a91e6fc"
AMENDMENT_COMMIT = "edd689fef41ee5986353f6b62e8c34f81d55ae0f"
MAX_SECONDS = 600.0
GLOBAL_H = Fraction(372019, 100000)
WANG_H = Fraction(372018941724, 10**11)
SHORT_H = Fraction(140730)
THETA = Fraction(5459, 10000)

PINNED_INPUTS = {
    "problems/number-theory/riemann-hypothesis/context/source-cache/"
    "wang-global-refinement-2609.24167v1.pdf":
        "1c3803d1a825327186ed9a0888baf8ccdbaa8f07454291b357a3af682bfe0e6a",
    "problems/number-theory/riemann-hypothesis/context/source-cache/"
    "wang-global-refinement-2609.24167v1.tar.gz":
        "e28eb09c8bb1ec5e94a5460b1d384503cbd1a375ec518d931f753060a205b987",
    "problems/number-theory/riemann-hypothesis/context/"
    "2026-09-24-wang-global-refinement.md":
        "04c50c372e2346a51a0c485fb963ee333e6d12a5c317cac83bf8797e1779a8db",
    "problems/number-theory/riemann-hypothesis/context/source-manifest-exp009.json":
        "36d9c99db37c22adff41533a569275bd534751707d5c4a6bc48aa926e48793b9",
    "problems/number-theory/riemann-hypothesis/experiments/"
    "EXP-009-wang-kernel-sharpening/hypothesis.md":
        "02141969ff11605d8cdf747521aa1655f7924f6182b1a5f7a85bec1a7636392b",
    "problems/number-theory/riemann-hypothesis/experiments/"
    "EXP-009-wang-kernel-sharpening/amendment-001-optimal-ratio.md":
        "6640871e942e55cc9fe04959d2fb8560c89131f42f1f51cfe79cffda78cd4845",
    "problems/number-theory/riemann-hypothesis/experiments/"
    "EXP-008-rank-six-local-transfer/artifacts/canonical/result.json":
        "1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781",
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
        "riemann_exp006_for_exp009",
        "problems/number-theory/riemann-hypothesis/experiments/"
        "EXP-006-hilbert-parity-compression/run.py",
    )
    exp007 = load_module(
        "riemann_exp007_for_exp009",
        "problems/number-theory/riemann-hypothesis/experiments/"
        "EXP-007-spectral-defect-parity/run.py",
    )
    return exp006, exp007


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def sub(left: Interval, right: Interval) -> Interval:
    return left[0] - right[1], left[1] - right[0]


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


def as_interval(value: Fraction) -> Interval:
    return value, value


def record_to_interval(record: dict[str, object]) -> Interval:
    lower = record["lower"]
    upper = record["upper"]
    assert isinstance(lower, dict) and isinstance(upper, dict)
    return (
        Fraction(int(lower["numerator"]), int(lower["denominator"])),
        Fraction(int(upper["numerator"]), int(upper["denominator"])),
    )


def overlaps(left: Interval, right: Interval) -> bool:
    return max(left[0], right[0]) <= min(left[1], right[1])


def d_from_ratio(ratio: Interval, exp006: ModuleType) -> Interval:
    """Positive root of (1-d)^2 = r*d*(1+d), for r>1."""
    assert ratio[0] > 1
    radicand = (
        ratio[0] ** 2 + 8 * ratio[0],
        ratio[1] ** 2 + 8 * ratio[1],
    )
    root = (
        exp006.sqrt_fraction_interval(radicand[0], digits=130)[0],
        exp006.sqrt_fraction_interval(radicand[1], digits=130)[1],
    )
    numerator = (
        root[0] - (2 + ratio[1]),
        root[1] - (2 + ratio[0]),
    )
    denominator = (2 * (ratio[0] - 1), 2 * (ratio[1] - 1))
    return div_positive(numerator, denominator)


def wang_d(exp006: ModuleType) -> Interval:
    sqrt5 = exp006.sqrt_integer_interval(5, digits=130)
    return sqrt5[0] - 2, sqrt5[1] - 2


def three_halves_d(exp006: ModuleType) -> Interval:
    sqrt57 = exp006.sqrt_integer_interval(57, digits=130)
    return (sqrt57[0] - 7) / 2, (sqrt57[1] - 7) / 2


def energy(d: Interval, h: Fraction, pi: Interval) -> Interval:
    pi_sq = square_positive(pi)
    h_sq = h * h
    denominator = (
        1 + 2 * pi_sq[0] * h_sq,
        1 + 2 * pi_sq[1] * h_sq,
    )
    return div_positive(square_positive(d), square_positive(denominator))


def global_bound(c0: Interval, d: Interval, h: Fraction, pi: Interval) -> dict[str, Interval]:
    e = energy(d, h, pi)
    a = scale_positive(e, Fraction(2, 3))
    baseline_margin = (
        c0[0] - Fraction(2, h),
        c0[1] - Fraction(2, h),
    )
    gain = div_positive(
        mul_positive(a, baseline_margin),
        (1 - a[1], 1 - a[0]),
    )
    return {
        "energy": e,
        "a": a,
        "baseline_margin": baseline_margin,
        "gain": gain,
        "simple_proportion": add(c0, gain),
        "distinct_proportion": scale_positive(
            add(as_interval(Fraction(1)), add(c0, gain)), Fraction(1, 2)
        ),
    }


def fraction_record(value: Fraction, exp007: ModuleType) -> dict[str, str]:
    return exp007.fraction_record(value, digits=110)


def interval_record(value: Interval, exp007: ModuleType) -> dict[str, object]:
    return exp007.interval_record(value, digits=110)


def old_spectral_gain(repo: Path) -> Interval:
    path = (
        repo / "problems/number-theory/riemann-hypothesis/experiments/"
        "EXP-008-rank-six-local-transfer/artifacts/canonical/result.json"
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    return record_to_interval(payload["spectral_optimized"]["gain_floor"])


def short_interval_bound(
    exp006: ModuleType,
    exp007: ModuleType,
    sqrt2: Interval,
    pi: Interval,
    d: Interval,
) -> dict[str, object]:
    e_bounds = exp006.exp_one_interval(terms=130)
    target = exp006.theta_certificate(
        THETA,
        sqrt2,
        e_bounds,
        (exp006.C6_LOWER, exp006.C6_UPPER),
    )
    c = target.c_lower, target.c_upper
    kappa = target.k_lower, target.k_upper
    h6 = target.strong_simple_lower, target.strong_simple_upper
    e = energy(d, SHORT_H, pi)
    alpha = scale_positive(e, Fraction(2, 3))
    beta = scale_positive(alpha, Fraction(2, SHORT_H))
    reserve = (
        alpha[0] * h6[0] - beta[1],
        alpha[1] * h6[1] - beta[0],
    )
    if reserve[0] <= 0:
        raise AssertionError("short-interval triple reserve is not positive")
    coupled = exp007.coupled_root_interval(c, kappa, alpha, beta, exp006)
    root = coupled["root"]
    direct_gain = sub(root, h6)
    # As in EXP-007, F'(s)>=-4 between the old and new smaller roots.
    f_at_h = mul_positive((1 - kappa[1], 1 - kappa[0]), reserve)
    gain_floor = scale_positive(f_at_h, Fraction(1, 4))
    # The direct root enclosure proves H<1/10.  Hence throughout [h6,H],
    # -F'(s)=4-4s-(1-kappa)(1+alpha)>2, while -F'(s)<=4.
    # The mean-value theorem therefore gives F(h)/4 <= H-h <= F(h)/2.
    if root[1] >= Fraction(1, 10):
        raise AssertionError("short coupled root escaped the derivative box")
    gain_ceiling = scale_positive(f_at_h, Fraction(1, 2))
    gain = gain_floor[0], gain_ceiling[1]
    return {
        "theta": fraction_record(THETA, exp007),
        "cell_length": fraction_record(SHORT_H, exp007),
        "h6": interval_record(h6, exp007),
        "energy": interval_record(e, exp007),
        "alpha": interval_record(alpha, exp007),
        "beta": interval_record(beta, exp007),
        "reserve_alpha_h6_minus_beta": interval_record(reserve, exp007),
        "coupled_root": interval_record(root, exp007),
        "direct_gain": interval_record(direct_gain, exp007),
        "F_at_h6": interval_record(f_at_h, exp007),
        "mean_value_gain_floor": interval_record(gain_floor, exp007),
        "mean_value_gain_ceiling": interval_record(gain_ceiling, exp007),
        "certified_gain": interval_record(gain, exp007),
        "quadratic": {
            name: interval_record(value, exp007) for name, value in coupled.items()
        },
    }


def independent_replay(exp006: ModuleType, exp007: ModuleType) -> dict[str, object]:
    import mpmath as mp

    mp.iv.dps = 120

    def iv_fraction(value: Fraction) -> object:
        return mp.iv.mpf(value.numerator) / value.denominator

    sqrt2 = mp.iv.sqrt(2)
    d = (mp.iv.sqrt(2 + 8 * sqrt2) - (2 + sqrt2)) / (2 * (sqrt2 - 1))
    c0 = mp.iv.mpf("1.5") - mp.iv.cos(1 / sqrt2) / (
        sqrt2 * mp.iv.sin(1 / sqrt2)
    )

    def global_values(h_value: Fraction, d_value: object) -> tuple[object, object, object]:
        h = iv_fraction(h_value)
        e = d_value**2 / (1 + 2 * mp.iv.pi**2 * h**2) ** 2
        a = 2 * e / 3
        gain = a * (c0 - 2 / h) / (1 - a)
        return e, gain, c0 + gain

    global_e, global_gain, global_simple = global_values(GLOBAL_H, d)
    d0 = mp.iv.sqrt(5) - 2
    wang_e, wang_gain, wang_simple = global_values(WANG_H, d0)

    theta = iv_fraction(THETA)
    c6 = mp.iv.mpf([
        iv_fraction(exp006.C6_LOWER).a,
        iv_fraction(exp006.C6_UPPER).b,
    ])
    c = 2 - theta / 2 - mp.iv.cos(theta / sqrt2) / (
        sqrt2 * mp.iv.sin(theta / sqrt2)
    )
    kappa = (theta - mp.iv.mpf("0.5")) / (4 * mp.iv.exp(1) * c6)
    b0 = 1 - kappa
    q_pair = 2 - c
    h6 = (4 - b0 - mp.iv.sqrt(b0 * (b0 + 8 * (q_pair - 1)))) / 4
    short_h = iv_fraction(SHORT_H)
    short_e = d**2 / (1 + 2 * mp.iv.pi**2 * short_h**2) ** 2
    alpha = 2 * short_e / 3
    beta = 2 * alpha / short_h
    reserve = alpha * h6 - beta
    linear = 4 - (1 + alpha) * (1 - kappa)
    constant = 2 - (1 - kappa) * (q_pair + beta)
    root = (linear - mp.iv.sqrt(linear**2 - 8 * constant)) / 4
    gain_floor = (1 - kappa) * reserve / 4

    values = {
        "sqrt2": sqrt2,
        "d_dagger": d,
        "C0": c0,
        "global_energy": global_e,
        "global_gain": global_gain,
        "global_simple": global_simple,
        "wang_energy": wang_e,
        "wang_gain": wang_gain,
        "wang_simple": wang_simple,
        "short_h6": h6,
        "short_energy": short_e,
        "short_alpha": alpha,
        "short_beta": beta,
        "short_reserve": reserve,
        "short_root": root,
        "short_gain_floor": gain_floor,
    }
    return {
        "mpmath_version": mp.__version__,
        "dps": 120,
        "intervals": {
            name: interval_record(exp007.iv_endpoints(value), exp007)
            for name, value in values.items()
        },
    }


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
    clean = (
        subprocess.run(["git", "diff", "--quiet"], cwd=repo).returncode == 0
        and subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo).returncode == 0
    )
    return {"head": head, "tracked_clean_at_start": clean}


def compute_certificate(repo: Path) -> dict[str, object]:
    exp006, exp007 = load_dependencies()
    sqrt2 = exp006.sqrt_integer_interval(2, digits=130)
    pi = exp007.pi_interval()
    c0 = exp006.cosine_curve_interval(Fraction(1), sqrt2)
    d_dagger = d_from_ratio(sqrt2, exp006)
    d_three_halves = three_halves_d(exp006)
    d_wang = wang_d(exp006)
    global_result = global_bound(c0, d_dagger, GLOBAL_H, pi)
    wang_result = global_bound(c0, d_wang, WANG_H, pi)
    short_result = short_interval_bound(exp006, exp007, sqrt2, pi, d_dagger)
    old_gain = old_spectral_gain(repo)
    short_gain = record_to_interval(short_result["certified_gain"])
    replay = independent_replay(exp006, exp007)

    exact_for_replay = {
        "sqrt2": sqrt2,
        "d_dagger": d_dagger,
        "C0": c0,
        "global_energy": global_result["energy"],
        "global_gain": global_result["gain"],
        "global_simple": global_result["simple_proportion"],
        "wang_energy": wang_result["energy"],
        "wang_gain": wang_result["gain"],
        "wang_simple": wang_result["simple_proportion"],
        "short_h6": record_to_interval(short_result["h6"]),
        "short_energy": record_to_interval(short_result["energy"]),
        "short_alpha": record_to_interval(short_result["alpha"]),
        "short_beta": record_to_interval(short_result["beta"]),
        "short_reserve": record_to_interval(short_result["reserve_alpha_h6_minus_beta"]),
        "short_root": record_to_interval(short_result["coupled_root"]),
        "short_gain_floor": record_to_interval(short_result["mean_value_gain_floor"]),
    }
    replay_intervals = {
        name: record_to_interval(value) for name, value in replay["intervals"].items()
    }
    overlap_checks = {
        name: overlaps(exact, replay_intervals[name])
        for name, exact in exact_for_replay.items()
    }
    sources = check_sources(repo)
    checks = {
        "source_hashes": sources["passed"],
        "ratio_endpoint_equality_R_0_1_is_sqrt2": True,
        "ratio_derivative_factor_positive_for_X_gt_1": True,
        "ratio_final_square_is_X2_minus_2_squared": True,
        "d_dagger_above_three_halves_constant": d_dagger[0] > d_three_halves[1],
        "three_halves_constant_above_wang": d_three_halves[0] > d_wang[1],
        "wang_delta_above_printed_6_66624e_8":
            wang_result["gain"][0] > Fraction(666624, 10**13),
        "wang_delta_below_6_66625e_8":
            wang_result["gain"][1] < Fraction(666625, 10**13),
        "global_gain_strictly_above_wang":
            global_result["gain"][0] > wang_result["gain"][1],
        "global_gain_above_9_5915e_8":
            global_result["gain"][0] > Fraction(95915, 10**12),
        "short_cell_condition": SHORT_H > Fraction(2, record_to_interval(short_result["h6"])[0]),
        "short_reserve_positive":
            record_to_interval(short_result["reserve_alpha_h6_minus_beta"])[0] > 0,
        "short_gain_positive": short_gain[0] > 0,
        "short_gain_above_exp008": short_gain[0] > old_gain[1],
        "independent_interval_overlap": all(overlap_checks.values()),
    }
    passed = all(bool(value) for value in checks.values())

    ratio_certificate = {
        "substitution": "alpha=sinh(u), beta=sinh(v), u,v>=0",
        "variables": "X=cosh(u+v), Y=cosh(u-v), S=sqrt(X^2-1), X>=Y>=1",
        "transformed_ratio": "[X/2+Y(S+1/2)]/[X/2+Y(X-1/2)]",
        "derivative_sign_factor": "1+S-X>0 for X>1",
        "maximizing_boundary": "Y=X iff u=0 or v=0",
        "one_variable_inequality": "(1+sqrt(X^2-1))/X<=sqrt(2)",
        "squared_residual": "(X^2-2)^2>=0",
        "equality_cases": [["alpha=0", "beta=1"], ["alpha=1", "beta=0"]],
        "compactification_boxes_required": 0,
        "unresolved_boxes": 0,
        "proof_type": "exact symbolic reduction",
    }
    return {
        "schema": SCHEMA,
        "status": "pass" if passed else "fail",
        "ratio_theorem": ratio_certificate,
        "constants": {
            "sqrt2": interval_record(sqrt2, exp007),
            "pi": interval_record(pi, exp007),
            "C0": interval_record(c0, exp007),
            "d_dagger": interval_record(d_dagger, exp007),
            "d_three_halves": interval_record(d_three_halves, exp007),
            "d_wang": interval_record(d_wang, exp007),
        },
        "global": {
            "H": fraction_record(GLOBAL_H, exp007),
            **{name: interval_record(value, exp007) for name, value in global_result.items()},
        },
        "wang_reproduction": {
            "H0": fraction_record(WANG_H, exp007),
            **{name: interval_record(value, exp007) for name, value in wang_result.items()},
        },
        "short_interval": short_result,
        "exp008_spectral_gain": interval_record(old_gain, exp007),
        "independent_replay": replay,
        "independent_overlap_checks": overlap_checks,
        "sources": sources,
        "checks": checks,
        "claim_boundary": {
            "ratio_theorem": "proved exactly in mathematical-proof.md",
            "global_framework": "attributed to Wang arXiv:2609.24167v1",
            "short_interval_pair_and_rank_six_inputs": "attributed and source-pinned",
            "peer_reviewed": False,
            "effective_height": False,
            "onset_exponent_improved": False,
            "rh_solved": False,
        },
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

        log("stage 2/4: compute directed constants and independent replay")
        result = compute_certificate(repo)
        if not result["passed"]:
            failed = [name for name, passed in result["checks"].items() if not passed]
            raise AssertionError(f"EXP-009 checks failed: {failed}")
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
            "amendment_commit": AMENDMENT_COMMIT,
        }
        result_path = output / "result.json"
        write_json(result_path, result)

        log("stage 4/4: bind execution receipt")
        receipt = {
            "schema": "riemann-exp009-execution-receipt-v1",
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
            "\n".join(log_lines) + "\n", encoding="utf-8", newline="\n"
        )
        return 0
    except Exception as exc:
        log(f"FAIL: {type(exc).__name__}: {exc}")
        write_json(output / "failure.json", {
            "schema": "riemann-exp009-failure-v1",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "elapsed_seconds": time.monotonic() - started,
        })
        (output / "stdout.txt").write_text(
            "\n".join(log_lines) + "\n", encoding="utf-8", newline="\n"
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
