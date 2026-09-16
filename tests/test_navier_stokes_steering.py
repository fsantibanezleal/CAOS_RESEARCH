"""Repository-level guard for the transcribed steering control (EXP-005 gate A).

The control that turns a grown layer back into a stationary background is the piece of
the Alpoge-Buckmaster construction the cascade bookkeeping quietly assumes and never
checks. `problems/analysis-pde/navier-stokes/code/nslib/steering.py` transcribes it from
their Subsections 3.3 and 3.6.2; this file asserts, in the CI lane, that what is
implemented still satisfies every assertion their Lemma 3.7 proves about it.

Only numpy is needed: the control law is deliberately kept free of torch, and the
co-rotating PDE solver that uses it lives in a separate module (`nslib.corotating`) so
that this guard stays reachable in CI, which installs no torch.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "problems/analysis-pde/navier-stokes/code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from nslib import steering as S  # noqa: E402

# Their (3.9) and (3.24) with c_p = 3 and the sin-squared profile: Lambda = 2 c_p H = 12.
PAPER = S.SteeringDesign(Lam=12.0, cp=3.0, profile="sin2")


def test_the_design_used_is_the_one_the_lemma_covers():
    assert PAPER.satisfies_lemma_37_condition
    assert PAPER.H == pytest.approx(2.0, abs=1e-6)
    assert PAPER.tau_b == pytest.approx(1.0 + 1.0 / 12.0)


def test_every_assertion_of_lemma_3_7():
    rep = S.lemma_37_report(PAPER, n_mu=40)
    assert rep["P_positive_all_trials"], "P must stay positive for EVERY trial pulse"
    assert rep["v_bounds_on_first_part"]["holds"], "1/(1+tau) <= v <= 1 on the ramp"
    assert rep["integral_in_log2_to_1"], "log 2 <= int v <= 1 on the ramp"
    assert rep["endpoint_map_strictly_decreasing"], "the endpoint map must be monotone"
    assert rep["endpoint_positive_at_0"] > 0.0
    assert rep["endpoint_negative_at_cp"] < 0.0
    assert rep["mu_star_in_proof_interval"], "their (3.28): mu* in [1/2 - 1/(4 Lambda), 1]"
    assert rep["log_gain_in_log2_to_1_plus_inv_Lambda"], "their (3.29)"
    assert abs(rep["v_endpoint_at_mu_star"]) < 1e-10


def test_the_pulse_returns_the_vorticity_and_keeps_the_temperature():
    """The property the whole cycle rests on, stated in physical variables.

    A layer that ended steering with vorticity left over would keep shearing the next
    layer, and the frozen-background assumption of the cascade bookkeeping would be
    false. A layer that lost its temperature gain would hand the next layer nothing.
    """
    lam = math.hypot(4, 31)
    stage = S.FirstStage(A=4.0, lam=lam, sin_s=4.0 / lam, design=PAPER,
                         mu=S.select_mu(PAPER), L_growth=5.0)
    ts, Theta, Omega = stage.integrate(-1e-5, stage.t_b + 3.0 / stage.Gamma, 2e-4)
    j1 = int(round(stage.t1 / 2e-4))
    jb = int(round(stage.t_b / 2e-4))
    peak = float(np.abs(Omega).max())

    assert abs(stage.Z(stage.t_b)) < 1e-12                  # zeta_1 = 0 at the end
    assert abs(Omega[jb]) / peak < 1e-3                     # Omega = 0 at the end
    assert abs(Omega[-1]) / peak < 1e-3                     # and through the hold
    assert Theta[-1] == pytest.approx(Theta[jb], rel=1e-9)  # the hold is stationary
    assert abs(Theta[jb]) >= 2.0 * abs(Theta[j1])           # their log 2 gain, retained


def test_dissipation_is_an_exact_exponential_factor_on_the_cycle():
    """Derived in this problem: equal damping factorizes, so mu* does not move with nu.

    This is what lets the dissipative cascade reuse the inviscid steering unchanged, and
    it is the reason a holding interval costs exactly `exp(-nu lambda^(2 alpha) T)`.
    """
    lam = math.hypot(4, 31)
    common = {"A": 4.0, "lam": lam, "sin_s": 4.0 / lam, "design": PAPER,
              "mu": S.select_mu(PAPER), "L_growth": 5.0}
    inviscid = S.FirstStage(**common)
    viscous = S.FirstStage(**common, nu=1e-3, alpha=0.5)
    d = viscous.damping
    assert d == pytest.approx(1e-3 * lam)

    t_end = inviscid.t_b + 2.0 / inviscid.Gamma
    _, Th_i, Om_i = inviscid.integrate(-1e-5, t_end, 2e-4)
    ts, Th_v, Om_v = viscous.integrate(-1e-5, t_end, 2e-4)
    scale = np.exp(d * ts)
    assert np.allclose(Th_v * scale, Th_i, rtol=1e-8)
    assert np.allclose(Om_v * scale, Om_i, rtol=1e-8)


def test_the_control_law_module_needs_no_torch():
    """The split that keeps this guard reachable in CI must not silently regress."""
    src = (CODE / "nslib" / "steering.py").read_text(encoding="utf-8")
    assert "import torch" not in src
    assert "boussinesq" not in src.split('"""')[2]  # not in the code, only in prose
