"""Adversarial controls for fixed-input tuning and phase collisions."""

from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROBLEM = ROOT / "problems/number-theory/riemann-hypothesis"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PARAM = load("rh_parameter_controls", PROBLEM / "code/mixed_gram_parameters.py")
PHASE = load("rh_phase_controls", PROBLEM / "code/short_window_phase.py")
AUDIT13 = load("rh_audit13_controls", PROBLEM / "experiments/EXP-013-mixed-gram-parameter-cap/audit.py")
AUDIT14 = load("rh_audit14_controls", PROBLEM / "experiments/EXP-014-short-window-phase-collision/audit.py")
SUPPORT = load("rh_squarefree_controls", PROBLEM / "code/squarefree_phase.py")
AUDIT15 = load("rh_audit15_controls", PROBLEM / "experiments/EXP-015-squarefree-phase-collision/audit.py")


def test_exact_source_and_independent_cap():
    data = PARAM.certificate()
    assert AUDIT13.audit(data)["passed"]
    assert PARAM.bound(1310) > PARAM.bound(1298)
    assert all(x > 0 for x in PARAM.boundary_obstruction(1311))


def test_offline_residual_cannot_be_dropped():
    # Enlarging the block satisfies clipping and the high-multiplicity
    # condition while breaking the off-line-pair condition.
    controls = PARAM.slacks(1400, F(5, 2), F(7, 2))
    assert all(v >= 0 for k, v in controls.items() if k != "off_line_pair_residual")
    assert controls["off_line_pair_residual"] < 0
    assert not PARAM.admissible(1400, F(5, 2), F(7, 2))


@pytest.mark.parametrize("field", ["bound", "input", "cap", "enclosure"])
def test_parameter_auditor_rejects_tampering(field):
    data = deepcopy(PARAM.certificate())
    if field == "bound":
        data["candidate"]["q"] = "1"
    elif field == "input":
        data["inputs"]["delta"] = "1/100"
    elif field == "cap":
        data["cap"]["maximum_integer_m"] = 1311
    else:
        data["candidate"]["q_enclosure"]["lower"] = "0.9"
    with pytest.raises(AssertionError):
        AUDIT13.audit(data)


def test_phase_auditor_and_scope_controls():
    data = PHASE.certificate()
    assert AUDIT14.audit(data)["passed"]
    low = PHASE.collision(100, 50, 5, 54)
    assert F(low["phase_upper"]) < F(1, 90)
    high = PHASE.collision(100, 50, 3, 54)
    assert F(high["phase_lower"]) > 90
    assert "not asserted nonzero" in low["mobius_weights"]


def test_phase_auditor_rejects_diagonal_and_wrong_limit():
    for key, value in (("hm_minus_kn", 0), ("limit", "infinity"), ("phase_upper", "1")):
        data = deepcopy(PHASE.certificate())
        data["cases"][0][key] = value
        with pytest.raises(AssertionError):
            AUDIT14.audit(data)


@pytest.mark.parametrize("m", [6, 1310.0, True])
def test_parameter_domain_controls(m):
    with pytest.raises(ValueError):
        PARAM.bound(m)


def test_supported_collision_and_squareful_control():
    data = SUPPORT.certificate()
    assert AUDIT15.audit(data)["passed"]
    assert not AUDIT15.squarefree(500000)
    assert F(data["phase_cases"][0]["upper"]) < F(1, 20)
    assert F(data["phase_cases"][-1]["lower"]) > 100


@pytest.mark.parametrize("field", ["h", "hm_minus_kn", "nonzero_mobius_weights", "prime_square_sum_upper", "uniform_comparison"])
def test_supported_auditor_rejects_tampering(field):
    data = deepcopy(SUPPORT.certificate())
    data[field] = 500000 if field == "h" else 0
    with pytest.raises((AssertionError, TypeError)):
        AUDIT15.audit(data)


@pytest.mark.parametrize("folder", ["EXP-013-mixed-gram-parameter-cap", "EXP-014-short-window-phase-collision", "EXP-015-squarefree-phase-collision"])
def test_canonical_replay_and_bindings(folder, tmp_path):
    here = PROBLEM / "experiments" / folder
    subprocess.run([sys.executable, str(here / "run.py"), "--output-dir", str(tmp_path)], check=True)
    canonical = (here / "artifacts/canonical/result.json").read_bytes()
    assert (tmp_path / "result.json").read_bytes() == canonical
    for relative, expected in json.loads(canonical)["bindings"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
