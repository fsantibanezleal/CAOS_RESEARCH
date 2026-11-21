"""EXP-029 gate G4: the concavity rule for the extremes of G on [N, N + 1] against a dense scan, the explicit formula at x = 1,
the von Mangoldt blocks and the block carries."""
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "problems/number-theory/riemann-hypothesis/experiments/EXP-029-weighted-chebyshev-control/run.py"
spec = importlib.util.spec_from_file_location("exp029_run", RUN)
R = importlib.util.module_from_spec(spec)
sys.modules["exp029_run"] = R
spec.loader.exec_module(R)


def mangoldt_naive(n):
    if n < 2:
        return 0.0
    for p in range(2, int(n ** 0.5) + 1):
        if n % p == 0:
            m = n
            while m % p == 0:
                m //= p
            return math.log(p) if m == 1 else 0.0
    return math.log(n)


def test_mangoldt_blocks_match_the_definition():
    base = R.small_primes(100)
    lam, npr = R.mangoldt_block(1, 3001, base)
    want = np.array([mangoldt_naive(n) for n in range(1, 3001)])
    assert np.allclose(lam, want, rtol=0, atol=1e-13)
    assert npr == sum(1 for n in range(2, 3001) if mangoldt_naive(n) > 0 and all(n % p for p in range(2, int(n ** 0.5) + 1)))
    lam2, _ = R.mangoldt_block(2500, 3001, base)
    assert np.allclose(lam2, want[2499:], rtol=0, atol=1e-13)


def test_block_carries_do_not_depend_on_the_block_size(monkeypatch):
    monkeypatch.setattr(R, "BLOCK", 700)
    got = {}
    for a, b, n, t, psi in R.Sums(5000).blocks():
        for k in (0, len(n) - 1):
            got[int(n[k])] = (float(t[k]), float(psi[k]))
    lam = [mangoldt_naive(n) for n in range(1, 5001)]
    for N, (t, psi) in got.items():
        assert abs(t - math.fsum(lam[k] / (k + 1) for k in range(N))) < 1e-12
        assert abs(psi - math.fsum(lam[:N])) < 1e-10


def test_concavity_rule_against_a_dense_scan():
    for a, b, n, t, psi in R.Sums(2000).blocks():
        gmax, gmin = R.interval_extremes(n, t, psi)
        for k in range(0, len(n), 37):
            N = float(n[k])
            xs = N + np.linspace(0.0, 1.0, 2001)[:-1]
            vals = R.g_value(xs, t[k], psi[k])
            right = float(R.g_value(N + 1.0, t[k], psi[k]))
            assert gmax[k] >= vals.max() - 1e-9 and gmax[k] <= max(vals.max(), right) + 1e-6
            assert gmin[k] <= vals.min() + 1e-9 and gmin[k] >= min(vals.min(), right) - 1e-9


def test_explicit_formula_at_one_is_an_identity_of_constants():
    # (2) at x = 1: G(1) = 1 + gamma = log 2 pi + (2 + gamma - log 4 pi) - (1 - log 2)
    assert abs((1.0 + R.EULER_GAMMA) - (R.LOG_2PI + R.K_CONST - R.TRIVIAL_CONST)) < 1e-14
    assert abs(float(R.g_value(1.0, 0.0, 0.0)) - (1.0 + R.EULER_GAMMA)) < 1e-14


def test_explicit_formula_with_a_few_zeros_is_close_at_small_x():
    zeros = np.array([14.134725141734693, 21.022039638771555, 25.010857580145688, 30.424876125859513, 32.935061587739189])
    lam = [mangoldt_naive(n) for n in range(1, 201)]
    for x in (10.5, 57.25, 199.5):
        N = int(x)
        t = math.fsum(lam[k] / (k + 1) for k in range(N))
        psi = math.fsum(lam[:N])
        g = float(R.g_value(x, t, psi))
        e = R.explicit_formula(x, zeros)
        tail = R.K_CONST - R.partial_constant(zeros)
        assert abs(g - e) <= tail * math.sqrt(x) + 1e-9
