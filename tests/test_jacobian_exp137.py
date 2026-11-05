"""Fast tests for EXP-137 (independent verification of the claimed (72,108) exclusion)."""

import importlib.util
import pickle
import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
EXP = (
    ROOT / "problems" / "algebraic-geometry" / "jacobian-conjecture" / "experiments"
    / "EXP-137-helali-72108-independent-verification"
)


def load(name):
    if str(EXP) not in sys.path:
        sys.path.insert(0, str(EXP))
    spec = importlib.util.spec_from_file_location(name, EXP / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def lib():
    return load("exp137_lib")


@pytest.fixture(scope="module")
def derive(lib):
    return load("derive")


def test_bracket_t_z_and_x2_identity():
    x, y = sp.symbols("x y")
    t = x * y**2
    z = 1 / y
    jac = sp.simplify(sp.diff(t, x) * sp.diff(z, y) - sp.diff(t, y) * sp.diff(z, x))
    assert jac == -1
    assert sp.simplify(x**2 - t**2 * z**4) == 0


def test_lattice_counts(lib):
    assert len(lib.lattice_points(lib.CASE2_P)) == 25
    assert len(lib.lattice_points(lib.CASE2_Q)) == 47
    assert len(lib.lattice_points(lib.CASE1_P)) == 61
    assert len(lib.lattice_points(lib.CASE1_Q)) == 125


def test_band_extraction_toy_support(derive):
    # P = x + x y^2? use supports {(1,0),(2,2)}, {(0,0),(1,1)}: direct hand computation.
    # [x, x y] = 1*1 - 0*1 = 1 -> x^1 y^0 ; [x^2 y^2, x y] = 2*1 - 2*1 = 0 ; [x,1]=0 ; [x^2y^2,1]=0
    bands = derive.band_equations([(1, 0), (2, 2)], [(0, 0), (1, 1)])
    # monomial x^1 y^0 = t^1 z^2: band 2, t-degree 1
    assert set(bands) == {2}
    (m, expr), = bands[2].items()
    assert m == 1
    p10, q11 = sp.symbols("p_1_0 q_1_1")
    assert sp.expand(expr - p10 * q11) == 0


def test_J_formulas_match_direct_bracket_case2(derive):
    res = derive.compare_with_helali("case2")
    assert res["J4_residual_constant"] == 1
    assert all(res[f"J{k}_equal"] for k in range(5))


def test_adverse_polygon_changes_bands(derive):
    ctrl = derive.adverse_polygon_control()
    assert ctrl["band_system_changed"] is True
    assert ctrl["extra_bands"]


def test_restricted_unpickler_refuses_class(lib):
    with pytest.raises(lib.RefusedPickle):
        lib.restricted_loads(pickle.dumps(pickle.Pickler))
    # data-only payload is accepted, including Fraction
    from fractions import Fraction

    payload = {"a": [1, (2, 3)], "b": Fraction(1, 3)}
    assert lib.restricted_loads(pickle.dumps(payload)) == payload


def test_restricted_unpickler_refuses_reduce_payload(lib):
    class Evil:
        def __reduce__(self):
            return (eval, ("1+1",))

    with pytest.raises(lib.RefusedPickle):
        lib.restricted_loads(pickle.dumps(Evil()))


def test_number_field_irreducibility_check(lib):
    from flint import fmpq_poly

    # w^5 - w^4 + 3w^3 + 3w^2 + 26 (Helali's L) irreducible; x^2-1 reducible
    lib.NF(fmpq_poly([26, 0, 3, 3, -1, 1]))
    with pytest.raises(ValueError):
        lib.NF(fmpq_poly([-1, 0, 1]))
