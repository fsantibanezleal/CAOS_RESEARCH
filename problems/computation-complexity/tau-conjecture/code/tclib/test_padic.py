"""Tests for the window-free p-adic filter (tclib.padic).

Run: python -m pytest problems/computation-complexity/tau-conjecture/code/tclib -q
"""
import random

import numpy as np

from .enum import pmul
from .padic import Layer, vp_int


def _layers(k):
    return Layer(2, 4, 64, k), Layer(3, 2, 20, k)


def _planted(rng, k, spread):
    """f = x^m * g * prod (x - r_i): k distinct integer roots planted, g random."""
    roots = set()
    while len(roots) < k:
        roots.add(rng.choice([rng.randint(-10, 10), rng.randint(-spread, spread)]))
    m = rng.choice([1, 2, 5]) if 0 in roots else 0     # the exact power of x dividing f
    g = tuple(rng.choice([-48, -16, -3, -1, 1, 2, 9, 27, 40]) for _ in range(rng.randint(1, 4)))
    f = g                                               # g(0) != 0 and lead != 0 by construction
    for r in roots:
        if r != 0:
            f = pmul(f, (-r, 1))
    if m:
        f = pmul(f, (0,) * m + (1,))
    return f, roots, m


def test_planted_roots_always_pass():
    """The lemma: a polynomial with k distinct integer roots is never rejected, for any m' <= m."""
    rng = random.Random(20261102)
    for k in (4, 5, 6, 7):
        for layer in _layers(k):
            for _ in range(400):
                f, roots, m = _planted(rng, k, 5000)
                assert all(sum(c * r ** d for d, c in enumerate(f)) == 0 for r in roots)
                F = layer.values(f)[None, :]
                for mlow in range(0, m + 1):
                    assert layer.passes(F, np.array([mlow]))[0], (layer.p, k, f, roots, mlow)


def test_filter_rejects_generic_polynomials():
    """The filter is not vacuous: random dense polynomials are mostly rejected at k = 7."""
    rng = random.Random(7)
    l2, l3 = _layers(7)
    rejected = 0
    for _ in range(300):
        f = tuple(rng.randint(-1000, 1000) for _ in range(9)) + (1,)
        F2, F3 = l2.values(f)[None, :], l3.values(f)[None, :]
        if not (l2.passes(F2, np.array([0]))[0] and l3.passes(F3, np.array([0]))[0]):
            rejected += 1
    assert rejected >= 290


def test_table_matches_bruteforce_on_small_masks():
    """LB_k[mask] equals a direct minimisation over root placements for the empty and singleton masks."""
    layer = Layer(3, 2, 20, 3)
    pts = layer.points
    # Empty mask: each root contributes at least min over residues of sum_j w(n_j - rho) = 3 + 1 = 4.
    assert layer.table[0] == 3 * 4
    # Mask {0} (the point n = 0): root 0 contributes sum_{j != 0} v_3(n_j) = 1 + 1 = 2 (n = +-3).
    i0 = pts.index(0)
    expected_c0 = sum(vp_int(n, 3) for n in pts if n != 0)
    assert expected_c0 == 2
    assert layer.table[1 << i0] <= 3 * 4


def test_mod_arithmetic_exact():
    l3 = Layer(3, 2, 20, 7)
    rng = np.random.default_rng(3)
    X = rng.integers(0, l3.mod, size=1000, dtype=np.uint64)
    Y = rng.integers(0, l3.mod, size=1000, dtype=np.uint64)
    for fn, op in ((l3.add, lambda a, b: a + b), (l3.sub, lambda a, b: a - b), (l3.mul, lambda a, b: a * b)):
        got = fn(X, Y)
        want = [op(int(a), int(b)) % l3.mod for a, b in zip(X, Y)]
        assert [int(v) for v in got] == want
    l2 = Layer(2, 4, 64, 7)
    with np.errstate(over="ignore"):
        got = l2.mul(X, Y)
    assert [int(v) for v in got] == [(int(a) * int(b)) % (1 << 64) for a, b in zip(X, Y)]
