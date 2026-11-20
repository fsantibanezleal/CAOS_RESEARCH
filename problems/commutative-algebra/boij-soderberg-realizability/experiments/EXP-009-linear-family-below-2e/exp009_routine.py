"""EXP-009 routine: the linear family L_e(a, b, c, d), its enumeration over GF(p), its seeded draws over GF(p^2), and the
three stages of the hypothesis (rank of mu_3e for every member; Hilbert function for the members of rank r; Betti table
for the members with the pure Hilbert function), on top of EXP-006's routine (imported, not edited) and `uhlib`.

L_e(a, b, c, d) = < x^e + a x y^(e-1) + b y^(e-2) z , y^e + c x^(e-1) y + d x^(e-2) z >, PBW monomials x^i y^j z^k (the
exponent triples (e,0,0), (1,e-1,0), (0,e-2,1) and (0,e,0), (e-1,1,0), (e-2,0,1)); the module is the left module U / (U f + U g).
EXP-006's `exp006_routine` already takes e as a parameter (structure constants, rank of mu_n(W) over GF(p^k), the Hilbert function,
the Betti table through uhlib), so this file adds the family, the enumeration, the three stages and the early-stop bookkeeping.
"""
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "EXP-006-odd-characteristic-below-2e"
if str(SIBLING) not in sys.path:
    sys.path.append(str(SIBLING))  # appended: EXP-006 has its own run.py and make_summary.py, which must not shadow this folder's

import exp006_routine as R  # noqa: E402
import numpy as np  # noqa: E402
from uhlib import algebra as A  # noqa: E402

SEED_BASE = R.SEED_BASE  # 20261120
EARLY_STOP_X = 40
EARLY_STOP_Y = 10
MAX_BETTI_Y = 40
Y_SAMPLE = 20000
RANK_CHUNK = 2000
S2_CHUNK_X = 8

CONTROL_PAIRS = [(4, 11), (4, 13), (5, 11), (5, 13), (6, 13)]
MAIN_PAIRS = [(4, 3), (4, 5), (4, 7), (5, 3), (5, 5), (5, 7), (6, 3), (6, 5), (6, 7), (6, 11), (7, 3), (7, 5), (7, 7),
              (7, 11), (7, 13)]
PAIRS = CONTROL_PAIRS + MAIN_PAIRS


def pair_key(e, p, fam):
    return "%d|%d|%s" % (e, p, fam)


def field_name(p, fam):
    return "GF(%d)" % p if fam == "X" else "GF(%d)" % (p * p)


# ------------------------------------------------------------------ the family
def family_monomials(e):
    """The exponent triples of the six monomials of L_e: [x^e, x y^(e-1), y^(e-2) z, y^e, x^(e-1) y, x^(e-2) z]."""
    return [(e, 0, 0), (1, e - 1, 0), (0, e - 2, 1), (0, e, 0), (e - 1, 1, 0), (e - 2, 0, 1)]


def family_coeff_array(F, e, params):
    """Coefficient array (2, u(e), k) of L_e(a, b, c, d) for params = (a, b, c, d) as field elements (int over GF(p), tuple of k
    residues over GF(p^k))."""
    k = F.degree
    pos = {m: i for i, m in enumerate(A.monos(e))}
    mon = family_monomials(e)
    C = np.zeros((2, R.u(e), k), dtype=np.int64)
    one = R._vec(F, F.one)
    a, b, c, d = (R._vec(F, x) for x in params)
    for row, (m0, m1, m2, coefs) in enumerate(((mon[0], mon[1], mon[2], (one, a, b)), (mon[3], mon[4], mon[5], (one, c, d)))):
        for m, co in zip((m0, m1, m2), coefs):
            C[row, pos[m]] = co
    return C


def family_polys_int(e, a, b, c, d):
    """The printed polynomials with integer coefficients as {(i, j, k): coefficient} (the form EXP-007 uses)."""
    return [{(e, 0, 0): 1, (1, e - 1, 0): a, (0, e - 2, 1): b}, {(0, e, 0): 1, (e - 1, 1, 0): c, (e - 2, 0, 1): d}]


# ------------------------------------------------------------------ the members
def x_params(p, index):
    """Member `index` (0 .. p^4 - 1) of L_e over GF(p) in lexicographic order of (a, b, c, d), the integers 0 .. p - 1."""
    a, r = divmod(index, p ** 3)
    b, r = divmod(r, p ** 2)
    c, d = divmod(r, p)
    return (a, b, c, d)


def y_params(F, index):
    """Member `index` of the sample over GF(p^2): random.Random(SEED_BASE + index), four F.random draws in the order a, b, c, d."""
    rng = random.Random(SEED_BASE + index)
    return tuple(F.random(rng) for _ in range(4))


def member_params(p, fam, index):
    if fam == "X":
        return x_params(p, index)
    return y_params(R.make_field("GF(%d)" % (p * p)), index)


def params_json(params):
    return [list(x) if isinstance(x, tuple) else int(x) for x in params]


def params_from_json(params):
    return tuple(tuple(x) if isinstance(x, list) else x for x in params)


def n_members(p, fam):
    return p ** 4 if fam == "X" else Y_SAMPLE


# ------------------------------------------------------------------ stage 1: the rank of mu_3e for a range of members
def rank_chunk(e, p, fam, start, end):
    """rank mu_3e for the members start .. end - 1: the histogram, every member above r (index, parameters, rank) and the indices of
    the members of rank exactly r.  Nothing else per member."""
    t0 = time.time()
    F = R.make_field(field_name(p, fam))
    ctx = R.ctx_of(F)
    r = R.target_rank(e)
    hist, above, at_r = {}, [], []
    for idx in range(start, end):
        params = member_params(p, fam, idx)
        rk = R.rank_mu(ctx, family_coeff_array(F, e, params), e, 3 * e)
        hist[str(rk)] = hist.get(str(rk), 0) + 1
        if rk > r:
            above.append({"index": idx, "params": params_json(params), "rank": rk})
        elif rk == r:
            at_r.append(idx)
    return {"e": e, "p": p, "family": fam, "start": start, "end": end, "n": end - start, "rank_hist": hist, "above": above,
            "rank_r": at_r, "seconds": round(time.time() - t0, 2)}


# ------------------------------------------------------------------ stage 2: Hilbert function and Betti table of rank-r members
def evaluate_member(F, ctx, e, params, want_betti=True):
    """Hilbert function to degree 4e + 2 and, when it is h_e, the Betti table (computed by uhlib, never inferred).  Returns a dict."""
    C = family_coeff_array(F, e, params)
    D = R.hilbert_bound(e)
    hf = R.hilbert_pair(ctx, C, e, D)
    pure_h = hf == [R.h_e(e, n) for n in range(D + 1)]
    rec = {"hilbert": hf, "pure_hilbert": pure_h, "betti": None, "pure": False, "basis": None}
    if pure_h and want_betti:
        t, _ = R.betti_table(F, C, e)
        rec["betti"] = R.table_rows(t)
        rec["pure"] = t == R.pure_table(e)
        rec["basis"] = R.basis_json(F, C, e)
    return rec


def s2_task(e, p, fam, indices):
    """The second stage on a list of rank-r member indices (in order); returns one record per member."""
    t0 = time.time()
    F = R.make_field(field_name(p, fam))
    ctx = R.ctx_of(F)
    out = []
    for idx in indices:
        params = member_params(p, fam, idx)
        ev = evaluate_member(F, ctx, e, params)
        ev["index"] = idx
        ev["params"] = params_json(params)
        out.append(ev)
    return {"records": out, "seconds": round(time.time() - t0, 2)}


class EarlyStop:
    """Early-stop bookkeeping of the second stage of a pair.  Tasks are handed out in index order; once the finished tasks hold `limit`
    pure members no further task is handed out (tasks already running finish and are counted).  For family Y `max_betti` also
    caps the Betti tables: a task is handed out only while the Betti tables finished plus the tasks running (each task of family Y
    is one member, so at most one table) stay below the cap."""

    def __init__(self, limit, max_betti=None):
        self.limit = limit
        self.max_betti = max_betti
        self.pure = 0
        self.betti = 0
        self.inflight = 0

    def add(self, records):
        self.pure += sum(1 for r in records if r["pure"])
        self.betti += sum(1 for r in records if r["betti"] is not None)

    @property
    def stopped(self):
        return self.pure >= self.limit

    def may_submit(self, tasks=1):
        if self.stopped:
            return False
        return self.max_betti is None or self.betti + self.inflight + tasks <= self.max_betti
