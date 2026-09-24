from __future__ import annotations

import functools
import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = (
    ROOT
    / "problems/number-theory/riemann-hypothesis/experiments"
    / "EXP-009-wang-kernel-sharpening"
)
RUN_PATH = EXPERIMENT / "run.py"
SPEC = importlib.util.spec_from_file_location("riemann_exp009", RUN_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


@functools.lru_cache(maxsize=1)
def computed_result() -> dict[str, object]:
    return MODULE.compute_certificate(ROOT)


def as_fraction(record: dict[str, str]) -> Fraction:
    return Fraction(int(record["numerator"]), int(record["denominator"]))


def interval(record: dict[str, object]) -> tuple[Fraction, Fraction]:
    return as_fraction(record["lower"]), as_fraction(record["upper"])


def test_sharp_ratio_constant_and_equality_classification() -> None:
    result = computed_result()
    theorem = result["ratio_theorem"]
    assert theorem["proof_type"] == "exact symbolic reduction"
    assert theorem["unresolved_boxes"] == 0
    assert theorem["squared_residual"] == "(X^2-2)^2>=0"
    assert theorem["equality_cases"] == [
        ["alpha=0", "beta=1"],
        ["alpha=1", "beta=0"],
    ]


def test_kernel_constant_strictly_improves_declared_fallback_and_wang() -> None:
    result = computed_result()
    constants = result["constants"]
    d_dagger = interval(constants["d_dagger"])
    d_three_halves = interval(constants["d_three_halves"])
    d_wang = interval(constants["d_wang"])
    assert d_dagger[0] > d_three_halves[1] > d_wang[1]


def test_global_bound_is_strictly_better_than_wang_reproduction() -> None:
    result = computed_result()
    new_gain = interval(result["global"]["gain"])
    wang_gain = interval(result["wang_reproduction"]["gain"])
    new_simple = interval(result["global"]["simple_proportion"])
    assert wang_gain[0] > Fraction(666624, 10**13)
    assert wang_gain[1] < Fraction(666625, 10**13)
    assert new_gain[0] > wang_gain[1]
    assert new_simple[0] > Fraction(6725007995, 10**10)


def test_short_interval_gain_is_correlated_and_above_exp008() -> None:
    result = computed_result()
    short = result["short_interval"]
    reserve = interval(short["reserve_alpha_h6_minus_beta"])
    gain = interval(short["certified_gain"])
    old_gain = interval(result["exp008_spectral_gain"])
    assert reserve[0] > 0
    assert gain[0] > old_gain[1]
    assert gain[1] < Fraction(1, 10**29)


def test_all_exact_and_independent_checks_pass() -> None:
    result = computed_result()
    assert result["status"] == "pass"
    assert result["passed"] is True
    assert all(result["checks"].values())
    assert all(result["independent_overlap_checks"].values())
    assert result["claim_boundary"]["rh_solved"] is False
    assert result["claim_boundary"]["peer_reviewed"] is False


def test_execution_contract_is_cpu_bounded() -> None:
    assert MODULE.MAX_SECONDS == 600.0
    assert MODULE.GLOBAL_H == Fraction(372019, 100000)
    assert MODULE.SHORT_H == 140730

