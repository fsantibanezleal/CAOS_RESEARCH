"""Tests for EXP-146 (single-prime resultant-chain certificates with proven degree bounds, JCB-103).

Fast tests of the bound engine (M4), the degree-drop image formula (M5) and the tree on planted systems (G4 in
miniature). The production run and the real-system gates are in the experiment's run.py.
"""

import importlib
import itertools
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP = (
    ROOT / "problems" / "algebraic-geometry" / "jacobian-conjecture" / "experiments"
    / "EXP-146-case1-chain-certificate"
)
sys.path.insert(0, str(EXP))
cc = importlib.import_module("chaincert")
gates = importlib.import_module("gates")

PRIME = cc.Prime(536870909, 505390653)


def test_hungarian_matches_bruteforce():
    rng = np.random.default_rng(1)
    for _ in range(300):
        n = int(rng.integers(1, 7))
        M = rng.integers(-5, 20, size=(n, n)).astype(np.int64)
        M[rng.random((n, n)) < 0.3] = cc.NEG
        best = max(sum(int(M[i, s[i]]) for i in range(n)) for s in itertools.permutations(range(n)))
        assert cc.max_assignment(M) == best


def test_bound_engine_random_pairs_never_under_bounds():
    st = gates.g2_random(300, seed=7)
    assert st["pass"], st
    assert st["weights_checked"] > 5000
    assert st["planted_cancel"] > 30 and st["planted_monomial"] > 30 and st["split_cases"] > 50
    assert st["formal_degree_above_actual"] > 0   # loose supports really occur


def test_negative_weight_gives_tight_order_bound_on_a_monomial_factor():
    """f = v^2 (x + 1), g = v (x - 2) with v the split variable: Res = (-3)... times v^3, so order 3."""
    from flint import fmpz_mpoly_ctx
    ctx = fmpz_mpoly_ctx.get(["x", "v"], "lex")
    x, v = ctx.gens()
    f, g = v**2 * (x + 1), v * (x - 2)
    split = 1
    Bf = cc.exact_bound(sorted(tuple(m) for m in f.monoms()), 2, split)
    Bg = cc.exact_bound(sorted(tuple(m) for m in g.monoms()), 2, split)
    assert Bf.low(split) == 2 and Bg.low(split) == 1
    mf, zf = cc.formal_degree(Bf, 0, split)
    ng, zg = cc.formal_degree(Bg, 0, split)
    Bh = cc.res_bound(Bf, mf, zf, Bg, ng, zg, 0, split, 2)
    h = f.resultant(g, "x")
    assert h != 0 and min(m[1] for m in h.monoms()) == 3
    assert Bh.low(split) == 3


def test_degree_drop_image_formula_one_planted_case():
    """phi of the exact formal resultant = M5 image formula, with the leading coefficient of f vanishing at r."""
    st = gates.g3_degree_drop(40, PRIME, seed=11)
    assert st["pass"], st
    assert any(k > 0 for k in st["drops"])


def test_planted_unit_system_is_certified_and_common_root_is_not():
    st = gates.g4_controls(PRIME)
    assert st["planted_unit_certified"] is True
    assert st["planted_common_root_certified"] is False
    assert st["pass"]


def test_exact_division_by_a_power_is_refused_when_not_exact():
    from flint import nmod_mpoly_ctx
    ctx = nmod_mpoly_ctx.get(["w"], modulus=PRIME.p)
    w = ctx.gen(0)
    assert cc.shift_down(w**3 + w**5, 0, 3) == 1 + w**2
    with pytest.raises(cc.BoundViolation):
        cc.shift_down(w**2 + w**5, 0, 3)


def test_constant_member_needs_proven_zero_degree_bounds_not_a_constant_image():
    """Coordinator reading of M6: a member is a constant only if B(e_x) = 0 for every variable; an image that
    happens to be constant (leading coefficients vanishing mod p) does not count."""
    from flint import nmod_mpoly_ctx
    ctx = nmod_mpoly_ctx.get(["a", "b"], modulus=PRIME.p)
    loose = cc.exact_bound([(2, 0), (0, 0)], 2, None)
    tight = cc.exact_bound([(0, 0)], 2, None)
    g_loose = cc.Mem("m", None, ctx.from_dict({(0, 0): 5}), loose, 1)
    g_tight = cc.Mem("m", None, ctx.from_dict({(0, 0): 5}), tight, 1)
    assert not cc.is_constant_member(g_loose, 2)
    assert cc.is_constant_member(g_tight, 2)
