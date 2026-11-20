"""Gate G3 of EXP-008 (boij-soderberg-realizability): h_6 and r at e = 6 against the formula, the rank routine at degree 18
against the module construction of `uhlib` on random spaces over GF(3) and GF(13), the early-stop bookkeeping on a small
synthetic run, and the seed rule (the same seed gives the same space)."""
import sys
from pathlib import Path

EXPS = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
        / "experiments")
sys.path.insert(0, str(EXPS / "EXP-008-odd-characteristic-e5-e6"))

import exp008_routine as X  # noqa: E402
import numpy as np  # noqa: E402
from exp008_routine import R  # noqa: E402
from uhlib.module import quotient_module  # noqa: E402


def test_formula_h6_and_r():
    # u(n) = (m + 1)(n + 1 - m), m = n // 2, typed independently of uhlib
    def u(n):
        return 0 if n < 0 else (n // 2 + 1) * (n + 1 - n // 2)

    assert u(18) == 100 and u(12) == 49 and u(6) == 16 and u(2) == 4
    h6 = [u(n) - 2 * u(n - 6) + 2 * u(n - 18) - u(n - 24) for n in range(27)]
    assert [R.h_e(6, n) for n in range(27)] == h6
    assert h6[:8] == [1, 2, 4, 6, 9, 12, 14, 16]  # 16 - 2 and 20 - 4 at degrees 6, 7
    assert sum(h6) == 216 and h6[25] == h6[26] == 0
    assert 2 * u(12) - 2 == 96 and R.target_rank(6) == 96 and u(18) - h6[18] == 96
    assert 2 * u(10) - 2 == 70 and R.target_rank(5) == 70
    assert R.h_e(6, 18) == 4 and R.h_e(5, 15) == 2  # codimension 2 h_e(3e): 8 and 4


def test_rank_at_degree_18_against_uhlib_module_construction():
    e = 6
    for name in ("GF(3)", "GF(13)"):
        F = R.make_field(name)
        ctx = R.ctx_of(F)
        for i in range(10):
            C = R.draw_space(F, e, R.SEED_BASE + 700 + i)
            M = quotient_module(F, [0], R.polys_as_relations(F, C, e), maxdeg=3 * e)
            dims = list(M.dims) + [0] * (3 * e + 1 - len(M.dims))
            assert dims[3 * e] == R.u(3 * e) - R.rank_mu(ctx, C, e, 3 * e), (name, i)
            assert dims[e] == R.u(e) - 2


def test_early_stop_bookkeeping_on_a_synthetic_run():
    es = X.EarlyStop(limit=40)
    assert not es.stopped
    for k, n in enumerate([0, 5, 10, 20, 4, 7]):  # running totals 0, 5, 15, 35, 39, 46
        es.add(n)
        assert es.stopped == (k == 5), k
    assert es.pure == 46
    specs = X.chunk_specs(["C"])
    assert [s["start"] for s in specs][:3] == [0, 500, 1000] and specs[-1]["end"] == 1000000
    assert sum(s["end"] - s["start"] for s in X.chunk_specs()) == 150000 + 300000 + 1000000
    spec = {"id": "T|0-8", "family": "A", "field": "GF(5)", "e": 5, "start": 0, "end": 8}
    rec = X.run_chunk(spec)
    assert rec["n"] == 8 and sum(rec["rank_hist"].values()) == 8
    assert rec["pure"] <= rec["pure_hilbert"] <= rec["hilbert_computed"] <= 8


def test_same_seed_same_space():
    F, C1 = X.space_of("GF(3)", 6, 123)
    _, C2 = X.space_of("GF(3)", 6, 123)
    _, C3 = X.space_of("GF(3)", 6, 124)
    assert C1.shape == (2, R.u(6), 1) and (C1 == C2).all() and not (C1 == C3).all()
    assert R.rank_field(R.ctx_of(F), C1) == 2
    rows = R.basis_json(F, C1, 6)
    assert np.array_equal(R.basis_from_json(F, rows, 6), C1)
    assert R.SEED_BASE == 20261120
