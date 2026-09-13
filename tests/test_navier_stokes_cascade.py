"""Repository-level guard for the navier-stokes cascade identities.

The problem keeps its own 49-test suite under
`problems/analysis-pde/navier-stokes/code/tests/`, but repository CI runs only `tests/`
(`testpaths = ["tests"]` in pyproject.toml), so that suite guards nothing here. This file
is the bridge, following the convention already used by the bougard-joret and
huneke-wiegand tests: add the problem's code directory to `sys.path` and exercise the
load-bearing claims.

Only the torch-free modules are exercised, because CI installs numpy and sympy but not
torch. That is deliberate: the identities that carry the problem's conclusions live in
`cascade` and `modulation`, and `nslib/__init__` imports the torch-backed modules lazily
so these stay reachable.

The central identity is checked SYMBOLICALLY with sympy rather than in floating point.
"""

from __future__ import annotations

import math
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "problems/analysis-pde/navier-stokes/code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from nslib import cascade as C  # noqa: E402
from nslib import modulation as M  # noqa: E402


def test_problem_code_and_suite_are_present():
    assert (CODE / "nslib" / "cascade.py").is_file()
    assert (CODE / "nslib" / "modulation.py").is_file()
    own_suite = sorted((CODE / "tests").glob("test_*.py"))
    assert len(own_suite) >= 4, "the problem's own suite should still be there"


def test_importing_nslib_does_not_require_torch():
    """The torch-backed modules must stay lazy, or this whole file becomes uncollectable.

    Checked in a SUBPROCESS with torch forced to be unimportable, so the assertion is
    real on a machine that happens to have torch installed. An in-process check like
    "torch not in sys.modules" would be vacuous here: another test may already have
    imported it.
    """
    script = textwrap.dedent(
        """
        import sys

        class Blocker:
            def find_spec(self, name, path=None, target=None):
                if name == "torch" or name.startswith("torch."):
                    raise ImportError("torch blocked for this check")
                return None

        sys.meta_path.insert(0, Blocker())
        sys.path.insert(0, CODE_DIR)
        import nslib
        from nslib import cascade, modulation
        assert "torch" not in sys.modules, "importing nslib pulled in torch"
        assert cascade.P_STAR > 1 and modulation.ALPHA0_OURS > 0
        print("ok")
        """
    ).replace("CODE_DIR", repr(str(CODE)))
    r = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert r.returncode == 0, f"nslib is not importable without torch:\n{r.stderr}"
    assert "ok" in r.stdout


def test_lazy_attribute_access_still_rejects_unknown_names():
    import nslib

    assert hasattr(nslib, "cascade") and hasattr(nslib, "modulation")
    with pytest.raises(AttributeError):
        _ = nslib.definitely_not_a_module


# --------------------------------------------------------------- the published threshold


def test_alpha0_matches_the_published_value():
    """Cordoba, Martinez-Zoroa, Zheng, ARMA 250 (2026) article 38, Theorem 1."""
    assert C.ALPHA0_CMZ == pytest.approx((22 - 8 * math.sqrt(7)) / 9, rel=1e-15)
    assert C.ALPHA0_CMZ == pytest.approx(0.09266550127591937, rel=1e-12)
    # their |grad|^alpha is our (-Laplacian)^(alpha/2), so classical viscosity is their 2
    assert M.alpha_ours_to_cmz(1.0) == pytest.approx(2.0)
    assert M.ALPHA0_OURS == pytest.approx(C.ALPHA0_CMZ / 2, rel=1e-15)


def test_calibration_identity_holds_symbolically():
    """1 / (2 * alpha_0) = (22 + 8 sqrt 7) / 8 = 11/4 + sqrt 7, EXACTLY.

    Checked in exact arithmetic rather than floating point: sympy simplifies the
    difference to zero, so this is an algebraic identity and not a numerical
    coincidence at 15 digits.
    """
    sympy = pytest.importorskip("sympy")
    s7 = sympy.sqrt(7)
    alpha0 = (22 - 8 * s7) / 9
    implied_p = 1 / (2 * alpha0)
    assert sympy.simplify(implied_p - (sympy.Rational(11, 4) + s7)) == 0
    # and the relation inverts: alpha_c(p) = 1/(4p) returns alpha_0 / 2
    assert sympy.simplify(1 / (4 * implied_p) - alpha0 / 2) == 0


def test_python_constants_agree_with_the_symbolic_identity():
    assert C.P_STAR == pytest.approx(11 / 4 + math.sqrt(7), rel=1e-15)
    assert C.implied_p(C.ALPHA0_CMZ) == pytest.approx(C.P_STAR, rel=1e-13)
    assert C.alpha_c(C.P_STAR) == pytest.approx(M.ALPHA0_OURS, rel=1e-13)


# ------------------------------------------------------------------- the growth rate


def test_growth_rate_is_sqrtA_times_sin_phi():
    """Settles the mangled-radical ambiguity in the source PDF by computing the matrix."""
    import numpy as np

    for A, phi, lam, r in ((12.5, 0.37, 410.4, 1.0), (4.0, 1.1, 7.0, 1.3), (30.0, 2.0, 91.0, 0.8)):
        zeta = r * M.rot(phi)
        got = M.growth_rate(zeta, -A * np.array([0.0, 1.0]), lam)
        assert got == pytest.approx(math.sqrt(A) * math.sin(phi), rel=1e-10)
        assert abs(got - math.sqrt(A * math.sin(phi))) > 1e-6


def test_growth_rate_carries_no_frequency():
    """Frequency buys gradient, not growth. Everything downstream rests on this."""
    import numpy as np

    zeta, G = M.rot(1.1), -9.0 * np.array([0.0, 1.0])
    rates = [M.growth_rate(zeta, G, lam) for lam in (1.0, 1e2, 1e5, 1e9)]
    assert max(rates) - min(rates) < 1e-8


def test_dissipative_eigenvalue_closed_form():
    import numpy as np

    for alpha in (0.05, 0.25, 0.5, 1.0):
        A, phi, lam, r, nu = 9.0, 1.1, 7.0, 1.0, 1e-3
        got = M.growth_rate(r * M.rot(phi), -A * np.array([0.0, 1.0]), lam, nu=nu, alpha=alpha)
        assert got == pytest.approx(math.sqrt(A) * math.sin(phi) - nu * (lam * r) ** (2 * alpha),
                                    abs=1e-12)


# ------------------------------------------------------------------ cascade constraints


def test_c1_forces_the_frequency_to_outgrow_the_gradient():
    assert not C.Schedule(g=1.0, p=0.9, alpha=0.01, nu=1e-6).c1_amplitude_summable()
    assert C.Schedule(g=1.0, p=2.0, alpha=0.01, nu=1e-6).c1_amplitude_summable()


def test_hold_damping_does_not_move_the_exponent():
    """C4 must never bind while C2 holds, or the threshold would be below 1/(4p)."""
    for p in (2.0, 4.0, C.P_STAR, 9.0):
        for alpha in (0.2 * C.alpha_c(p), 0.8 * C.alpha_c(p)):
            s = C.Schedule(g=1.0, p=p, alpha=alpha, nu=1e-10)
            if s.c2_growth_positive(stages=150):
                worst = max(s.c4_log_survival_exponent(q, 150) for q in range(0, 150, 10))
                assert worst <= 6.9


def test_finite_horizon_bound_uses_the_last_inspected_stage():
    """The binding stage of a Q-stage run is Q-1. Using Q leaves apparent violations."""
    nu, g, Q = 1e-10, 1.0, 400
    got = C.detectable_alpha_p(nu, g, Q)
    assert got == pytest.approx(0.25 + math.log(1 / nu) / (2 * g * (Q - 1)), rel=1e-15)
    assert got > 0.25
    # the overshoot shrinks like 1/Q
    a, b = C.detectable_alpha_p(nu, g, 400) - 0.25, C.detectable_alpha_p(nu, g, 800) - 0.25
    assert a / b == pytest.approx(2.0, rel=0.01)


def test_classical_viscosity_is_out_of_reach_for_every_admissible_p():
    """alpha = 1 is classical. C1 forces p > 1, so alpha_c < 1/4 always."""
    for p in (1.0001, 2.0, C.P_STAR, 50.0):
        assert C.alpha_c(p) <= 0.25
    assert C.alpha_c(C.P_STAR) < M.ALPHA0_OURS * 1.0001
