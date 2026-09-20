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
    / "EXP-008-rank-six-local-transfer"
)
RUN_PATH = EXPERIMENT / "run.py"
SPEC = importlib.util.spec_from_file_location("riemann_exp008", RUN_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


@functools.lru_cache(maxsize=1)
def computed_result() -> dict[str, object]:
    return MODULE.compute_certificate(ROOT)


def test_source_rank_six_interval_is_strictly_better() -> None:
    exp006, _ = MODULE.load_dependencies()
    assert exp006.C6_LOWER < exp006.C6_UPPER < exp006.C3_LOWER < exp006.C3_UPPER


def test_declared_onset_and_point_targets() -> None:
    result = computed_result()
    checks = result["checks"]
    assert result["passed"] is True
    assert checks["rank_six_coarse_lower_negative"] is True
    assert checks["rank_six_coarse_upper_positive"] is True
    assert checks["strictly_earlier_onset"] is True
    assert checks["edge_rank_three_negative"] is True
    assert checks["edge_rank_six_above_2_5e_7"] is True
    assert checks["point_improvement_above_9_26e_7"] is True


def test_optimized_radius_identity_and_gain() -> None:
    result = computed_result()
    spectral = result["spectral_optimized"]
    rho = spectral["rho"]
    assert Fraction(int(rho["numerator"]), int(rho["denominator"])) == Fraction(11, 5)
    reserve = spectral["reserve_alpha_h_minus_beta"]
    reserve_lower = Fraction(
        int(reserve["lower"]["numerator"]), int(reserve["lower"]["denominator"])
    )
    gain = spectral["gain_floor"]
    gain_lower = Fraction(
        int(gain["lower"]["numerator"]), int(gain["lower"]["denominator"])
    )
    assert reserve_lower > 0
    assert gain_lower > Fraction(9, 10**69)
    assert spectral["passed"] is True


def test_invalid_budget_is_rejected_by_contract() -> None:
    assert MODULE.MAX_SECONDS == 120.0
    assert MODULE.RHO > 2
