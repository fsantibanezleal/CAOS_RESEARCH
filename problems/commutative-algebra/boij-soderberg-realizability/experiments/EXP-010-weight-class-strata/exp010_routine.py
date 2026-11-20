"""EXP-010 routine: the weight classes of the monomials of U(H), the strata S(m; i, j), the admissible test of the note, the members
(enumerated or sampled), the exact rank of mu_n for a member (plain and block by weight class), the staged test of the pure Hilbert
function, the Betti table through `uhlib`, and the plan (the strata, their budgets) of the three families C, Q and E.

Conventions (hypothesis.md, 'Definitions fixed here').  Monomials of `uhlib` are tuples (a, b, c) for x^a y^b z^c (PBW order,
yx = xy - z, left modules).  The weight is w = b + c and the class of a monomial for m is w mod m.  S(m; i, j) is the set of
<f, g> with f supported on the monomials of class i and g on those of class j.  A member is the pair of coefficient vectors
(f, g) on `monos(e)`.  mu_n has the rows a * f and a * g for a in monos(n - e), written on monos(n); its rank is exact (python-flint
`nmod_mat`, integers modulo p).  The structure constants are those of `uhlib.algebra.mono_mul` reduced modulo p.

Block rank.  The product is homogeneous for the weight, so the row a * f has its support on the columns of class class(a) + i and the
row a * g on those of class class(a) + j.  mu_n is therefore block-diagonal by the class k of the column, and its rank is the sum of
the ranks of the blocks.  `rank_plain` is the plain matrix; the tests check that both agree.
"""
import itertools
import sys
import time
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

import flint  # noqa: E402
import numpy as np  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import tor  # noqa: E402
from uhlib.fastmod import quotient_module_np  # noqa: E402
from uhlib.fields import PrimeField  # noqa: E402

SEED_BASE = 20261120
EARLY_STOP_PURE = 5
MAX_TABLES = 40
MAX_STORED = 50  # members with the pure Hilbert function stored per stratum

FAMILY_C_PAIRS = [(4, 3), (4, 5), (5, 3), (5, 5), (5, 7), (6, 3), (6, 11), (7, 11), (7, 13)]
FAMILY_Q_PAIRS = [(6, 5), (6, 7), (7, 3), (7, 5), (7, 7)]
FAMILY_E_PAIRS = [(8, 11), (8, 13), (8, 3), (8, 5), (8, 7)]
FAMILIES = ("C", "Q", "E")


# ------------------------------------------------------------------ the numbers
def u(n):
    return A.dim_U(n)


def h_e(e, n):
    """Hilbert function of the pure table (1, 2, 2, 1) on (0, e, 3e, 4e)."""
    return u(n) - 2 * u(n - e) + 2 * u(n - 3 * e) - u(n - 4 * e)


def target_rank(e):
    """r = 2 u(2e) - 2: the rank of mu_3e for a pair with the pure Hilbert function."""
    return 2 * u(2 * e) - 2


def hf_degrees(e):
    """The degrees tested after mu_3e: 3e - 1 (injective), then 3e + 1, ..., 4e - 3 (rank u(n) - h_e(n))."""
    return [3 * e - 1] + list(range(3 * e + 1, 4 * e - 2))


def want_rank(e, n):
    return u(n) - h_e(e, n) if n >= 3 * e else 2 * u(n - e)


def pure_table(e):
    return {(0, 0): 1, (1, e): 2, (2, 3 * e): 2, (3, 4 * e): 1}


# ------------------------------------------------------------------ weights, supports, strata
def weight(mono):
    return mono[1] + mono[2]


def weights(e):
    return [weight(m) for m in A.monos(e)]


@lru_cache(maxsize=None)
def _support(e, m, i):
    return tuple(k for k, w in enumerate(weights(e)) if w % m == i)


def support(e, m, i):
    """Indices (into monos(e)) of the monomials of class i modulo m."""
    return list(_support(e, m, i))


def d_of(e, m, i):
    return len(_support(e, m, i))


def all_strata(e):
    """Every (m, i, j), 2 <= m <= e + 1, i <= j, in the order of m, then i, then j."""
    return [(m, i, j) for m in range(2, e + 2) for i in range(m) for j in range(i, m)]


def stratum_index(e, m, i, j):
    """The fixed index of a stratum (its position in `all_strata(e)`), the offset of its seed."""
    return all_strata(e).index((m, i, j))


def n_members(e, p, m, i, j):
    """N = ((p^d_i - 1)/(p - 1)) ((p^d_j - 1)/(p - 1)) for i < j; None for i = j (never enumerated)."""
    if i == j:
        return None
    di, dj = d_of(e, m, i), d_of(e, m, j)
    return ((p ** di - 1) // (p - 1)) * ((p ** dj - 1) // (p - 1))


def plan_members(e, p, m, i, j, budget):
    """(planned members, all members?, enumerated?): all N members when i < j and N <= budget, else `budget` random members; an
    empty stratum (d < 2 for i = j, or a class without monomials) has none."""
    di, dj = d_of(e, m, i), d_of(e, m, j)
    if i == j:
        return (0, True, False) if di < 2 else (budget, False, False)
    if di == 0 or dj == 0:
        return 0, True, True
    N = n_members(e, p, m, i, j)
    return (N, True, True) if N <= budget else (budget, False, False)


# ------------------------------------------------------------------ the admissible strata (the note)
@lru_cache(maxsize=None)
def _uk(n, m):
    out = [0] * m
    if n < 0:
        return tuple(out)
    for c in range(n // 2 + 1):
        r = n - 2 * c
        for b in range(r + 1):
            out[(b + c) % m] += 1
    return tuple(out)


@lru_cache(maxsize=None)
def admissible(e, m, i, j):
    """Some classes (s1, s2, t) make H_k(n) >= 0 for every class k and every 0 <= n <= 4e + 6m + 2:
    H_k(n) = u_k(n) - u_(k-i)(n-e) - u_(k-j)(n-e) + u_(k-s1)(n-3e) + u_(k-s2)(n-3e) - u_(k-t)(n-4e)."""
    top = 4 * e + 6 * m + 2
    off = 4 * e
    U = np.array([_uk(n, m) for n in range(-off, top + 1)], dtype=np.int64)  # row n + off
    base = U[off:off + top + 1]
    s1 = U[off - e:off - e + top + 1]
    s3 = U[off - 3 * e:off - 3 * e + top + 1]
    s4 = U[off - 4 * e:off - 4 * e + top + 1]
    low = base - np.roll(s1, i, axis=1) - np.roll(s1, j, axis=1)
    for a, b in itertools.combinations_with_replacement(range(m), 2):
        mid = low + np.roll(s3, a, axis=1) + np.roll(s3, b, axis=1)
        for t in range(m):
            if (mid - np.roll(s4, t, axis=1)).min() >= 0:
                return True
    return False


@lru_cache(maxsize=None)
def _admissible_strata(e):
    return tuple(s for s in all_strata(e) if admissible(e, *s))


def admissible_strata(e):
    return list(_admissible_strata(e))


_ALL = "all"
NOTE_TABLE = {  # the table of the note context/2026-11-20-weight-class-strata.md (strata (i, j) with i <= j)
    4: {2: [(0, 0), (0, 1), (1, 1)], 3: [(0, 1), (0, 2), (1, 2)], 4: _ALL, 5: [(0, 4)]},
    5: {2: [(0, 1)], 3: [(0, 2)], 4: [(0, 1)], 5: _ALL, 6: [(0, 5)]},
    6: {2: [(0, 0), (0, 1), (1, 1)], 3: _ALL, 4: [(0, 2), (1, 3)], 5: [(0, 1)], 6: _ALL, 7: [(0, 6)]},
    7: {2: [(0, 1)], 3: [(0, 1)], 4: [(0, 3)], 5: [(0, 2)], 6: [(0, 1)], 7: _ALL, 8: [(0, 7)]},
    8: {2: [(0, 0), (0, 1), (1, 1)], 3: [(0, 1), (0, 2), (1, 2)], 4: _ALL, 5: [(0, 3)], 6: [(0, 2), (0, 4), (2, 4)], 7: [(0, 1)],
        8: _ALL, 9: [(0, 8)]},
}
NOTE_TOTALS = {4: 17, 5: 19, 6: 34, 7: 34, 8: 58}


def note_table(e):
    """The admissible strata of the note for e as a list of (m, i, j)."""
    out = []
    for m, row in NOTE_TABLE[e].items():
        pairs = [(i, j) for i in range(m) for j in range(i, m)] if row == _ALL else row
        out += [(m, i, j) for i, j in pairs]
    return out


# ------------------------------------------------------------------ the members
def unrank_normalized(d, p, t):
    """Normalized nonzero vectors of GF(p)^d (first nonzero coefficient 1), by index t (array) in [0, (p^d - 1)/(p - 1)): in order of
    the position s of the leading 1 (s = 0 first), then lexicographic on the d - 1 - s free coefficients after it."""
    t = np.asarray(t, dtype=np.int64)
    sizes = np.array([p ** (d - 1 - s) for s in range(d)], dtype=np.int64)
    cum = np.concatenate([[0], np.cumsum(sizes)])
    lead = np.searchsorted(cum, t, side="right") - 1
    rem = t - cum[lead]
    out = np.zeros((t.shape[0], d), dtype=np.int64)
    for q in range(d):
        digit = (rem // (p ** (d - 1 - q))) % p
        out[:, q] = np.where(lead == q, 1, np.where(lead < q, digit, 0))
    return out


def enumerate_members(e, p, m, i, j, start, end):
    """Members start .. end - 1 of S(m; i, j), i < j, as arrays of the coefficients on the two supports.  Member t is the pair
    (unrank(t // Ng), unrank(t % Ng)), Ng the number of normalized vectors on the support of g."""
    di, dj = d_of(e, m, i), d_of(e, m, j)
    ng = (p ** dj - 1) // (p - 1)
    t = np.arange(start, end, dtype=np.int64)
    return unrank_normalized(di, p, t // ng), unrank_normalized(dj, p, t % ng)


def sample_members(e, p, m, i, j, start, end, seed_index):
    """Random members start .. end - 1: uniform coefficients on the two supports, drawn by numpy's default_rng seeded with
    (20261120 + the index of the stratum, start); zero vectors are not excluded (they have rank below r and are counted)."""
    rng = np.random.default_rng([SEED_BASE + seed_index, start])
    n = end - start
    return (rng.integers(0, p, size=(n, d_of(e, m, i)), dtype=np.int64), rng.integers(0, p, size=(n, d_of(e, m, j)), dtype=np.int64))


# ------------------------------------------------------------------ the exact rank
@lru_cache(maxsize=64)
def struct_tensor(p, e, n):
    """T[im, a, col] = coefficient of the monomial `col` of monos(n) in a * m (a in monos(n - e), m = monos(e)[im]), modulo p."""
    me, ma, mn = A.monos(e), A.monos(n - e), A.monos(n)
    col = {mm: k for k, mm in enumerate(mn)}
    T = np.zeros((len(me), len(ma), len(mn)), dtype=np.int64)
    for im, mono in enumerate(me):
        for ia, a in enumerate(ma):
            for mm, c in A.mono_mul(a, mono):
                T[im, ia, col[mm]] += c
    return T % p


def _rank_rows(M, p):
    if M.shape[0] == 0 or M.shape[1] == 0:
        return 0
    return flint.nmod_mat(M.shape[0], M.shape[1], M.ravel().tolist(), p).rank()


def rank_plain(e, p, n, f, g):
    """Rank of mu_n for the pair of full coefficient vectors (f, g) on monos(e): the matrix with rows a * f and a * g."""
    T = struct_tensor(p, e, n)
    M = np.concatenate([np.tensordot(np.asarray(v, dtype=np.int64), T, axes=([0], [0])) for v in (f, g)], axis=0) % p
    return _rank_rows(M, p)


class Ranker:
    """Ranks of mu_n for the members of S(m; i, j) (m = 1: the whole space), block by block over the class of the column."""

    def __init__(self, e, p, m, i, j):
        self.e, self.p, self.m, self.i, self.j = e, p, m, i, j
        self.I, self.J = support(e, m, i), support(e, m, j)
        self._blocks = {}

    def blocks(self, n):
        b = self._blocks.get(n)
        if b is None:
            e, p, m, i, j = self.e, self.p, self.m, self.i, self.j
            T = struct_tensor(p, e, n)
            ca = np.array([weight(a) % m for a in A.monos(n - e)])
            cc = np.array([weight(c) % m for c in A.monos(n)])
            TI, TJ = T[self.I], T[self.J]
            b = []
            for k in range(m):
                rf, rg = np.flatnonzero(ca == (k - i) % m), np.flatnonzero(ca == (k - j) % m)
                cols = np.flatnonzero(cc == k)
                b.append((TI[:, rf][:, :, cols], TJ[:, rg][:, :, cols]))
            self._blocks[n] = b = tuple(b)
        return b

    def rank(self, fs, gs, n):
        """Rank of mu_n for the coefficients fs, gs on the two supports."""
        p, total = self.p, 0
        for TF, TG in self.blocks(n):
            if TF.shape[2] == 0 or TF.shape[1] + TG.shape[1] == 0:
                continue
            M = np.concatenate([np.tensordot(fs, TF, axes=([0], [0])), np.tensordot(gs, TG, axes=([0], [0]))], axis=0) % p
            total += _rank_rows(M, p)
        return total

    def evaluate(self, fs, gs):
        """(rank mu_3e, pure Hilbert function?, {degree: rank} for the degrees computed): the staged test, stopping at the first
        degree whose rank is not that of the pure Hilbert function."""
        e = self.e
        r3 = self.rank(fs, gs, 3 * e)
        ranks = {3 * e: r3}
        if r3 != target_rank(e):
            return r3, False, ranks
        for n in hf_degrees(e):
            ranks[n] = self.rank(fs, gs, n)
            if ranks[n] != want_rank(e, n):
                return r3, False, ranks
        return r3, True, ranks


@lru_cache(maxsize=256)
def ranker(e, p, m, i, j):
    return Ranker(e, p, m, i, j)


def pure_hilbert_full(e, p, f, g):
    """The staged test for full coefficient vectors (the whole space): True when the Hilbert function of U/(Uf + Ug) is h_e."""
    return ranker(e, p, 1, 0, 0).evaluate(np.asarray(f, dtype=np.int64), np.asarray(g, dtype=np.int64))[1]


# ------------------------------------------------------------------ the Betti table and the printed forms
def betti_table(e, p, f, g):
    """The Betti table {(i, degree): rank} of U / (U f + U g) by `uhlib` (module construction and Tor), or None when the module is
    not finite within the bound; f and g are full coefficient vectors on monos(e)."""
    F = PrimeField(p)
    rels = [{(0, mono): int(c) for mono, c in zip(A.monos(e), v) if int(c) % p} for v in (f, g)]
    M = quotient_module_np(F, [0], rels, maxdeg=4 * e + 8)
    return tor.betti(M) if M.finished else None


def table_rows(t):
    return None if t is None else [[i, j, r] for (i, j), r in sorted(t.items())]


def basis_json(e, p, f, g):
    """The two forms as [[[a, b, c], coefficient], ...] (nonzero terms, residues), the form the second instrument reads."""
    return [[[list(m), int(c)] for m, c in zip(A.monos(e), v) if int(c) % p] for v in (f, g)]


def poly_text(e, p, v):
    """Readable form of a form: signed residues, PBW monomials x^a y^b z^c, highest degree first."""
    terms = []
    for m, c in sorted(((m, int(c)) for m, c in zip(A.monos(e), v) if int(c) % p), key=lambda t: (-A.deg(t[0]), t[0])):
        c = c % p
        if c > p // 2:
            c -= p
        a, b, z = m
        mon = "*".join(s + ("^%d" % d if d > 1 else "") for s, d in (("x", a), ("y", b), ("z", z)) if d)
        terms.append(("-" + mon if c == -1 else mon) if c in (1, -1) and mon else "%d%s" % (c, "*" + mon if mon else ""))
    return " + ".join(terms).replace("+ -", "- ") if terms else "0"


# ------------------------------------------------------------------ the early stop
class EarlyStop:
    """Bookkeeping of the Betti tables of a stratum: the stratum stops once `limit` pure members are found; at most `max_tables` tables
    are started (the tables in flight count)."""

    def __init__(self, limit=EARLY_STOP_PURE, max_tables=MAX_TABLES):
        self.limit, self.max_tables = limit, max_tables
        self.pure = self.tables = self.inflight = 0

    @property
    def stopped(self):
        return self.pure >= self.limit

    def may_start_table(self):
        return not self.stopped and self.tables + self.inflight < self.max_tables

    def table_started(self):
        self.inflight += 1

    def table_done(self, pure):
        self.inflight -= 1
        self.tables += 1
        self.pure += 1 if pure else 0


# ------------------------------------------------------------------ the plan
def budget_q(e, p):
    return max(20000, 30 * p ** h_e(e, 3 * e))


def make_spec(family, e, p, m, i, j, budget, admissible):
    planned, all_members, enumerated = plan_members(e, p, m, i, j, budget)
    return {"key": "%s|%d|%d|%d|%d|%d" % (family, e, p, m, i, j), "family": family, "e": e, "p": p, "m": m, "i": i, "j": j,
            "admissible": bool(admissible), "d_i": d_of(e, m, i), "d_j": d_of(e, m, j), "N": n_members(e, p, m, i, j),
            "budget": budget, "planned": planned, "all_members": all_members, "enumerated": enumerated,
            "seed_index": stratum_index(e, m, i, j), "seed": None if enumerated else SEED_BASE + stratum_index(e, m, i, j)}


def plan_family(family, only=None):
    """The ordered list of strata of a family (specs).  Within a pair: decreasing m; pairs in the order of the hypothesis."""
    specs = []
    if family == "C":
        for e, p in FAMILY_C_PAIRS:
            adm = set(admissible_strata(e))
            for m, i, j in sorted(all_strata(e), key=lambda s: (-s[0], s[1], s[2])):
                specs.append(make_spec("C", e, p, m, i, j, 20000 if (m, i, j) in adm else 3000, (m, i, j) in adm))
    elif family == "Q":
        for e, p in FAMILY_Q_PAIRS:
            for m, i, j in sorted(admissible_strata(e), key=lambda s: (-s[0], s[1], s[2])):
                specs.append(make_spec("Q", e, p, m, i, j, budget_q(e, p), True))
    elif family == "E":
        for e, p in FAMILY_E_PAIRS:
            adm = sorted(admissible_strata(e), key=lambda s: (-s[0], s[1], s[2]))
            if p in (11, 13):
                chosen = [((7, 0, 1), 100000)]
            elif p == 3:
                chosen = [(s, 100000) for s in adm if 3 <= s[0] <= 7] + [(s, 600000) for s in adm if s[0] == 2]
            else:
                keep = [(7, 0, 1), (6, 0, 2), (6, 0, 4), (6, 2, 4), (5, 0, 3)]
                chosen = [(s, 2000000) for s in keep if s in adm]
            for (m, i, j), b in chosen:
                specs.append(make_spec("E", e, p, m, i, j, b, True))
    else:
        raise ValueError(family)
    if only:
        specs = [s for s in specs if (s["e"], s["p"]) in only]
    return specs


# ------------------------------------------------------------------ workers (top-level functions, picklable)
def chunk_job(spec):
    """Members start .. end - 1 of a stratum: the histogram of rank mu_3e, the number of rank r, the number with the pure Hilbert
    function, and the first MAX_STORED members with the pure Hilbert function (full coefficient vectors, ranks per degree)."""
    t0 = time.time()
    e, p, m, i, j = spec["e"], spec["p"], spec["m"], spec["i"], spec["j"]
    start, end = spec["start"], spec["end"]
    if spec["enumerated"]:
        FS, GS = enumerate_members(e, p, m, i, j, start, end)
    else:
        FS, GS = sample_members(e, p, m, i, j, start, end, spec["seed_index"])
    R = ranker(e, p, m, i, j)
    r = target_rank(e)
    hist, rank_r, pure_hf, members = {}, 0, 0, []
    for k in range(end - start):
        r3, pure, ranks = R.evaluate(FS[k], GS[k])
        hist[r3] = hist.get(r3, 0) + 1
        rank_r += r3 == r
        if pure:
            pure_hf += 1
            if len(members) < MAX_STORED:
                f = np.zeros(u(e), dtype=np.int64)
                g = np.zeros(u(e), dtype=np.int64)
                f[R.I] = FS[k]
                g[R.J] = GS[k]
                members.append({"index": start + k, "f": f.tolist(), "g": g.tolist(), "ranks": {str(n): v for n, v in ranks.items()}})
    return {"key": spec["key"], "start": start, "end": end, "n": end - start, "rank_hist": {str(k): v for k, v in hist.items()},
            "rank_r": rank_r, "pure_hf": pure_hf, "members": members, "seconds": round(time.time() - t0, 3)}


def betti_job(task):
    """The Betti table of one member: {'key', 'index', 'betti', 'pure', 'seconds'}."""
    t0 = time.time()
    t = betti_table(task["e"], task["p"], task["f"], task["g"])
    return {"key": task["key"], "index": task["index"], "betti": table_rows(t), "pure": t == pure_table(task["e"]),
            "seconds": round(time.time() - t0, 2)}


def gate_c_case(args):
    """Gate G1 (c), one pair: a random pair (alternately in the whole space, S(2; 0, 1), S(e - 1; 0, 1), S(3; 0, 1)) whose ranks of
    mu_n for n = 3e - 1, 3e, 3e + 1, 4e - 3 are compared with the dimensions of U / (U f + U g) from the module construction of
    `uhlib` (u(n) minus the rank), for the plain routine and, in a stratum, the block routine."""
    import random
    from uhlib.module import quotient_module
    e, p, k = args
    rng = random.Random(SEED_BASE + 100000 * e + 1000 * p + k)
    m, i, j = [(1, 0, 0), (2, 0, 1), (e - 1, 0, 1), (3, 0, 1)][k % 4]
    I, J = support(e, m, i), support(e, m, j)
    f = np.zeros(u(e), dtype=np.int64)
    g = np.zeros(u(e), dtype=np.int64)
    f[I] = [rng.randrange(p) for _ in I]
    g[J] = [rng.randrange(p) for _ in J]
    degs = [3 * e - 1, 3 * e, 3 * e + 1, 4 * e - 3]
    rels = [{(0, mono): int(c) for mono, c in zip(A.monos(e), v) if int(c)} for v in (f, g)]
    M = quotient_module_np(PrimeField(p), [0], rels, maxdeg=4 * e - 3)
    dims = list(M.dims) + [0] * (4 * e - 2 - len(M.dims))
    R = ranker(e, p, m, i, j)
    detail = []
    for n in degs:
        via_module = u(n) - dims[n]
        plain = rank_plain(e, p, n, f, g)
        block = R.rank(f[I], g[J], n)
        detail.append([n, via_module, plain, block])
    ok = all(a == b == c for _, a, b, c in detail)
    # the module of the pair also by the pure-python construction on the smallest degree (a second build of the same dimensions)
    M2 = quotient_module(PrimeField(p), [0], rels, maxdeg=3 * e) if k % 25 == 0 else None
    if M2 is not None:
        d2 = list(M2.dims) + [0] * (3 * e + 1 - len(M2.dims))
        ok = ok and d2[3 * e - 1] == u(3 * e - 1) - detail[0][2] and d2[3 * e] == u(3 * e) - detail[1][2]
    return {"e": e, "p": p, "k": k, "stratum": [m, i, j], "ok": bool(ok), "detail": detail}
