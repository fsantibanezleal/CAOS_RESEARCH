"""Fast tests for EXP-145 (image of the announced map and its fibers over C = 0, exact)."""

import importlib.util
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
EXP = (
    ROOT / "problems" / "algebraic-geometry" / "jacobian-conjecture" / "experiments"
    / "EXP-145-image-and-plane-fibers"
)


def load():
    spec = importlib.util.spec_from_file_location("exp145_run", EXP / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp145_run"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_gamma_basis_with_c_inverted_is_unit_ideal():
    """P1: the fiber over Gamma(c), c inverted, has reduced Groebner basis [1]."""
    m = load()
    assert m.gamma_basis(4) == [sp.Integer(1)]


def test_control_c1_perturbed_curve_is_in_the_image():
    """C1: 4/27 replaced by 5/27 gives a basis different from [1]."""
    m = load()
    assert m.gamma_basis(5) != [sp.Integer(1)]


def test_three_points_over_0_1_0_map_there():
    """P3(c): the fiber over (0, 1, 0) is the three stated points and each maps there."""
    m = load()
    expected = {
        (sp.Integer(0), sp.Integer(1), sp.Integer(-4)),
        (sp.Integer(2), sp.Rational(-1, 2), sp.Rational(5, 4)),
        (sp.Integer(-2), sp.Integer(1), sp.Integer(2)),
    }
    pts = set(m.plane_fiber_points(sp.Integer(0), sp.Integer(1)))
    assert pts == expected
    for p in pts:
        assert m.apply_F(p) == (0, 1, 0)
