"""EXP-021 routine: the monic members of the stratum S(d; 0, 1), d = (e - 1)/2, of the pairs
    f = x^e + [alpha part] + [gamma part],      g = y^e + [beta part] + [delta part]
(PBW monomials x^a y^b z^c of `uhlib`, left modules, yx = xy - z), their digits and index, the blocks of 20,000 consecutive indices, the
seeded random blocks of the controls, the stage of a member by the block ranks of mu_3e, and the census of a block.

Conventions (hypothesis.md, 'Definitions fixed here').
    delta part: g on x^(e-1) y, x^(e-2) z                         (2 coefficients)
    gamma part: f on x y^(e-1), y^(e-2) z                         (2 coefficients)
    alpha part: f on x^(d+1-c) y^(d-c) z^c, c = 0, ..., d         (d + 1 coefficients)
    beta part:  g on x^(d-c) y^(d+1-c) z^c, c = 0, ..., d         (d + 1 coefficients)
A member is its row of e + 5 digits in the order delta, gamma, alpha, beta; its index is the base p number with these digits, the first
digit the most significant; the complete list has p^(e+5) members, those of index below p^(e+3) have delta = 0 and those below p^(e+1)
have gamma = delta = 0.  The routine of EXP-010 is imported, not edited.

Stage of a member (0 to 3): the blocks of mu_3e (block diagonal by the class of the column modulo d) are tested in the order s1, s2,
then the other classes increasing, where (s1, s2) are the first two classes of the only admissible triple of S(d; 0, 1).  The block of
class k must have rank rows - (k == s1) - (k == s2).  The first block that fails ends the member: stage 0 for the first block, stage 1
for a later one; when every block holds, the staged test of EXP-010 on the degrees `hf_degrees(e)` gives stage 2 (it fails) or 3.
"""
import itertools
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPS = HERE.parent
_EXP10 = str(EXPS / "EXP-010-weight-class-strata")
if _EXP10 not in sys.path:
    sys.path.insert(0, _EXP10)

import exp010_routine as R  # noqa: E402

np, A = R.np, R.A

BLOCK = 20000
SEED_BASE = 20261120
MAX_FOUND = 20000  # members of stage 3 kept with their data (the count of all of them is exact)
EARLY_STOP_PURE = 5
MAX_TABLES = 40


# ------------------------------------------------------------------ the admissible triples and the pattern
def triples(e, m=None, i=0, j=1):
    """Every triple (s1, s2, t) of classes of the second and third syzygies that keeps the class-wise Hilbert function of a pure
    resolution nonnegative, for the stratum S(m; i, j) (default m = (e - 1)/2): the test `admissible` of EXP-010 listing every triple."""
    m = (e - 1) // 2 if m is None else m
    top = 4 * e + 6 * m + 2
    off = 4 * e
    U = np.array([R._uk(n, m) for n in range(-off, top + 1)], dtype=np.int64)
    base = U[off:off + top + 1]
    s1 = U[off - e:off - e + top + 1]
    s3 = U[off - 3 * e:off - 3 * e + top + 1]
    s4 = U[off - 4 * e:off - 4 * e + top + 1]
    low = base - np.roll(s1, i, axis=1) - np.roll(s1, j, axis=1)
    out = []
    for a, b in itertools.combinations_with_replacement(range(m), 2):
        mid = low + np.roll(s3, a, axis=1) + np.roll(s3, b, axis=1)
        for t in range(m):
            if (mid - np.roll(s4, t, axis=1)).min() >= 0:
                out.append((a, b, t))
    return out


def pattern(e):
    """(m, s1, s2, block order) of S((e - 1)/2; 0, 1): the classes of the two syzygies of degree 3e of the only admissible triple."""
    m = (e - 1) // 2
    tr = triples(e, m, 0, 1)
    assert len(tr) == 1, tr
    s1, s2, _ = tr[0]
    order = [s1] + ([s2] if s2 != s1 else []) + [k for k in range(m) if k not in (s1, s2)]
    return m, s1, s2, order


def block_rows(e):
    """Rows of the blocks of mu_3e by class k of the column: u_(k-0)(2e) + u_(k-1)(2e)."""
    m = (e - 1) // 2
    return [R._uk(2 * e, m)[k % m] + R._uk(2 * e, m)[(k - 1) % m] for k in range(m)]


# ------------------------------------------------------------------ the members
def n_digits(e):
    return e + 5


def n_members(e, p):
    return p ** n_digits(e)


def layout(e):
    """(positions in monos(e) of the delta, gamma, alpha and beta digits in digit order; position of x^e; position of y^e)."""
    d = (e - 1) // 2
    idx = {m: k for k, m in enumerate(A.monos(e))}
    delta = [idx[(e - 1, 1, 0)], idx[(e - 2, 0, 1)]]
    gamma = [idx[(1, e - 1, 0)], idx[(0, e - 2, 1)]]
    alpha = [idx[(d + 1 - c, d - c, c)] for c in range(d + 1)]
    beta = [idx[(d - c, d + 1 - c, c)] for c in range(d + 1)]
    return delta, gamma, alpha, beta, idx[(e, 0, 0)], idx[(0, e, 0)]


def digits_of_indices(e, p, idx):
    """Digit rows (shape (n, e + 5)) of the members with the given indices (array), the first digit the most significant."""
    t = np.asarray(idx, dtype=np.int64)
    nd = n_digits(e)
    out = np.zeros((t.shape[0], nd), dtype=np.int64)
    for q in range(nd):
        out[:, nd - 1 - q] = (t // (p ** q)) % p
    return out


def digits_block(e, p, start, end, complete):
    """Digits of the members of a block: the indices start .. end - 1 (complete list) or the seeded random rows of the control."""
    if complete:
        return digits_of_indices(e, p, np.arange(start, end, dtype=np.int64))
    rng = np.random.default_rng([SEED_BASE + 1000 * e + p, start])
    return rng.integers(0, p, size=(end - start, n_digits(e)), dtype=np.int64)


def index_of_digits(p, digits):
    """The index of one digit row: the base p number, the first digit the most significant."""
    v = 0
    for c in digits:
        v = v * p + int(c)
    return v


def full_vectors(e, p, digits):
    """Full coefficient vectors (F, G) on monos(e) of the members with these digit rows."""
    delta, gamma, alpha, beta, xe, ye = layout(e)
    n, d1 = digits.shape[0], (e - 1) // 2 + 1
    F = np.zeros((n, A.dim_U(e)), dtype=np.int64)
    G = np.zeros((n, A.dim_U(e)), dtype=np.int64)
    F[:, xe] = 1
    G[:, ye] = 1
    G[:, delta] = digits[:, 0:2]
    F[:, gamma] = digits[:, 2:4]
    F[:, alpha] = digits[:, 4:4 + d1]
    G[:, beta] = digits[:, 4 + d1:4 + 2 * d1]
    return F, G


def digits_from_vectors(e, f, g):
    """The digit row of a member from its coefficient vectors (None when the vectors are not a monic member of the stratum)."""
    delta, gamma, alpha, beta, xe, ye = layout(e)
    f, g = np.asarray(f, dtype=np.int64), np.asarray(g, dtype=np.int64)
    used_f, used_g = {xe, *gamma, *alpha}, {ye, *delta, *beta}
    if f[xe] != 1 or g[ye] != 1 or any(f[k] for k in range(len(f)) if k not in used_f) or any(g[k] for k in range(len(g)) if k not in used_g):
        return None
    return [int(v) for v in list(g[delta]) + list(f[gamma]) + list(f[alpha]) + list(g[beta])]


def blocks_of(total, size=BLOCK):
    """The blocks [start, end) of a list of `total` members."""
    return [(s, min(total, s + size)) for s in range(0, total, size)]


# ------------------------------------------------------------------ the stage of a member
def stage_of(Rk, e, p, s1, s2, order, fs, gs):
    """The stage (0 to 3) of one member given by its coefficients on the two supports."""
    blocks = Rk.blocks(3 * e)
    for pos, k in enumerate(order):
        TF, TG = blocks[k]
        M = np.concatenate([np.tensordot(fs, TF, axes=([0], [0])), np.tensordot(gs, TG, axes=([0], [0]))], axis=0) % p
        want = M.shape[0] - (k == s1) - (k == s2)
        if R._rank_rows(M, p) != want:
            return 0 if pos == 0 else 1
    for n in R.hf_degrees(e):
        if Rk.rank(fs, gs, n) != R.want_rank(e, n):
            return 2
    return 3


def stage_direct(e, p, f, g):
    """The stage by the definition, ranking EVERY block of mu_3e (no early exit, no order) with the plain tensor of EXP-010."""
    m, s1, s2, _ = pattern(e)
    Rk = R.ranker(e, p, m, 0, 1)
    I, J = R.support(e, m, 0), R.support(e, m, 1)
    ranks, rows = [], []
    for TF, TG in Rk.blocks(3 * e):
        M = np.concatenate([np.tensordot(np.asarray(f)[I], TF, axes=([0], [0])), np.tensordot(np.asarray(g)[J], TG, axes=([0], [0]))],
                           axis=0) % p
        ranks.append(R._rank_rows(M, p))
        rows.append(M.shape[0])
    want = [rows[k] - (k == s1) - (k == s2) for k in range(m)]
    if ranks[s1] != want[s1]:
        return 0
    if any(ranks[k] != want[k] for k in range(m)):
        return 1
    pure_hf = Rk.evaluate(np.asarray(f)[I], np.asarray(g)[J])[1]
    return 3 if pure_hf else 2


# ------------------------------------------------------------------ the census of a block
def job(args):
    """Census of the members of one block: (e, p, start, end, complete[, plain]).  Returns the stage counts, the same counts for the members
    of index below p^(e+3) (delta = 0) and below p^(e+1) (gamma = delta = 0), the members of stage 3 in index order (index, digits, F, G),
    the number with the pure Hilbert function by the plain staged test when `plain`, and the seconds."""
    e, p, start, end, complete = args[:5]
    plain = bool(args[5]) if len(args) > 5 else False
    m, s1, s2, order = pattern(e)
    I, J = R.support(e, m, 0), R.support(e, m, 1)
    digits = digits_block(e, p, start, end, complete)
    F, G = full_vectors(e, p, digits)
    assert not np.delete(F, I, axis=1).any() and not np.delete(G, J, axis=1).any(), "a member leaves the stratum"
    Rk = R.ranker(e, p, m, 0, 1)
    lim_d, lim_gd = p ** (e + 3), p ** (e + 1)
    stages, below_d, below_gd, found, plain_n = [0] * 4, [0] * 4, [0] * 4, [], 0
    t0 = time.time()
    for k in range(end - start):
        s = stage_of(Rk, e, p, s1, s2, order, F[k, I], G[k, J])
        stages[s] += 1
        pos = start + k
        if complete and pos < lim_d:
            below_d[s] += 1
            if pos < lim_gd:
                below_gd[s] += 1
        if s == 3:
            found.append({"index": pos, "digits": digits[k].tolist(), "f": F[k].tolist(), "g": G[k].tolist()})
        if plain:
            plain_n += bool(Rk.evaluate(F[k, I], G[k, J])[1])
    return {"start": start, "end": end, "stages": stages, "below_delta0": below_d, "below_gamma_delta0": below_gd, "found": found,
            "plain": plain_n if plain else None, "seconds": round(time.time() - t0, 3)}


def nonmonic_job(args):
    """Family K, the non-monic members at (5, 3): the normalized members of S(2; 0, 1) (enumeration of EXP-010) in which the coefficient of
    x^5 in f or of y^5 in g is zero, members start .. end - 1 of the enumeration; their stages and the number with the pure Hilbert
    function by the plain staged test."""
    e, p, start, end = args
    m, s1, s2, order = pattern(e)
    I, J = R.support(e, m, 0), R.support(e, m, 1)
    monos = A.monos(e)
    lf = [k for k, i in enumerate(I) if monos[i] == (e, 0, 0)][0]
    lg = [k for k, j in enumerate(J) if monos[j] == (0, e, 0)][0]
    FS, GS = R.enumerate_members(e, p, m, 0, 1, start, end)
    Rk = R.ranker(e, p, m, 0, 1)
    stages, plain, other = [0] * 4, 0, 0
    t0 = time.time()
    for k in range(end - start):
        if FS[k, lf] and GS[k, lg]:
            other += 1  # a member with both leading coefficients nonzero (counted, not staged: the monic list covers them)
            continue
        stages[stage_of(Rk, e, p, s1, s2, order, FS[k], GS[k])] += 1
        plain += bool(Rk.evaluate(FS[k], GS[k])[1])
    return {"start": start, "end": end, "stages": stages, "plain": plain, "both_nonzero": other, "seconds": round(time.time() - t0, 3)}


# ------------------------------------------------------------------ the Betti table of a member
def betti_job(task):
    """The Betti table and the length of U / (U f + U g) by `uhlib` from the stored coefficient vectors of a member: {'index', 'betti',
    'length', 'pure', 'seconds'}.  Pure: the table is (1, 2, 2, 1) on (0, e, 3e, 4e) and the length (the sum of the dimensions of the
    finite module) is e^3."""
    t0 = time.time()
    e, p = task["e"], task["p"]
    rels = [{(0, mono): int(c) for mono, c in zip(A.monos(e), v) if int(c) % p} for v in (task["f"], task["g"])]
    module = R.quotient_module_np(R.PrimeField(p), [0], rels, maxdeg=4 * e + 8)
    table = R.tor.betti(module) if module.finished else None
    length = int(sum(module.dims)) if module.finished else None
    pure = table is not None and table == R.pure_table(e) and length == e ** 3
    return {"index": task["index"], "betti": R.table_rows(table), "length": length, "pure": bool(pure), "seconds": round(time.time() - t0, 2)}
