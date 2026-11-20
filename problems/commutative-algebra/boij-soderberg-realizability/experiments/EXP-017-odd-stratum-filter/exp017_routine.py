"""EXP-017 routine: the pairs f = x^e + alpha(xy, z) y, g = y^e + beta(xy, z) x of the odd-e stratum S((e + 1)/2; 0, (e - 1)/2), the filter
(F0) to (F3) of hypothesis.md, its block form, the random members of a case, and the staged test of the pure Hilbert function.

Conventions (hypothesis.md, 'Definitions fixed here').  A member is (alpha, beta): coefficient lists of 1, h, ..., h^s over GF(p), s = (e - 1)/2.
Its pair: f = x^e + sum_a gamma_a x^a y^(a+1) z^(s-a) with alpha = sum gamma_a A_a(h); g = y^e + sum_a gamma'_a x^(a+1) y^a z^(s-a) with
beta(h - 1) = sum gamma'_a A_a(h); A_a(h) = h (h + 1) ... (h + a - 1).  Vectors are on `uhlib.algebra.monos(e)` (PBW monomials (a, b, c)).

Filter (z = 1; Delta = alpha(h) beta(h + e - 1) - A_(e-1)(h), X = (h - 2) Delta(h - e - 1), X' = (h + e) Delta(h + e + 1)):
    (F0) Delta has degree 2s and is coprime to X and to X';  (F1) X' alpha = c X mod Delta, deg c <= s;
    (F2) X beta(h + e - 1) = c' X' mod Delta, deg c' <= s;  (F3) c c' is not equal to A_(e-1).
`filter_member` is the exact test (python-flint).  `BlockF1` is the test of (F1) on blocks with numpy (integers modulo p): it asks the
degree of Delta, the independence of the columns h^k X mod Delta (a consequence of (F0)) and the solvability of (F1), by Gaussian
elimination; it does not test the coprimality of (F0) itself, so it accepts every member that (F0) and (F1) accept and, besides, some
with a common factor; the exact test then decides.
"""
import sys
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPS = HERE.parent
for _p in (EXPS / "EXP-010-weight-class-strata",):
    if str(_p) not in sys.path:
        sys.path.append(str(_p))

import exp010_routine as X  # noqa: E402


def _struct_tensor_mod_p(p, e, n):
    """The tensor of exp010_routine.struct_tensor with every coefficient reduced modulo p before it is stored.  The routine of EXP-010
    stores the exact integer coefficients (k! C(b, k) C(a, k)) in an int64 array, which raises an overflow error at e = 13, n = 49
    (EXP-015 met it first and applied the same replacement); reducing first gives the same tensor modulo p.  Applied at import, so that
    every process that imports this module uses it; the routine of EXP-010 is not edited.  Added by the coordinating session when the
    case (13, 5) of family X stopped on that error."""
    me, ma, mn = X.A.monos(e), X.A.monos(n - e), X.A.monos(n)
    col = {mm: k for k, mm in enumerate(mn)}
    T = X.np.zeros((len(me), len(ma), len(mn)), dtype=X.np.int64)
    for im, mono in enumerate(me):
        for ia, a in enumerate(ma):
            for mm, c in X.A.mono_mul(a, mono):
                T[im, ia, col[mm]] += c % p
    return T % p


STRUCT_TENSOR_ORIGINAL = X.struct_tensor
X.struct_tensor = X.lru_cache(maxsize=64)(_struct_tensor_mod_p)
import flint  # noqa: E402
import numpy as np  # noqa: E402
from uhlib import algebra as A  # noqa: E402

SEED_BASE = X.SEED_BASE
BLOCK = 1 << 16  # members per block: member i belongs to block i // BLOCK, drawn by a generator seeded with (seed, block)
MAX_STORED = 50  # members with the pure Hilbert function stored per case
MAX_TABLES = 50
EARLY_STOP_PURE = 5
STAGES = ("F0", "F1", "F2", "F3")


def stratum(e):
    return ((e + 1) // 2, 0, (e - 1) // 2)


def P_(p, cs):
    return flint.nmod_poly([int(c) % p for c in cs], p)


def a_poly(p, a):
    """A_a(h) = h (h + 1) ... (h + a - 1) as a polynomial over GF(p)."""
    r = P_(p, [1])
    for k in range(a):
        r = r * P_(p, [k, 1])
    return r


def a_coeffs(p, a):
    return [int(c) for c in a_poly(p, a).coeffs()]


def coeffs(poly, n):
    cs = [int(c) for c in poly.coeffs()]
    return cs + [0] * (n - len(cs))


def in_a_basis(p, cs, s):
    """gamma_a with sum gamma_a A_a(h) = the polynomial with coefficients cs (degree <= s): triangular, from the top."""
    rest = P_(p, cs)
    out = [0] * (s + 1)
    for a in range(s, -1, -1):
        c = int(rest[a]) if rest.degree() >= a else 0
        if c:
            out[a] = c
            rest = rest - a_poly(p, a) * c
    return out


# ------------------------------------------------------------------ the conversions
def pair_vectors(e, p, alpha, beta):
    """The pair (f, g) of the member (alpha, beta) as coefficient vectors (lists of ints in [0, p)) on monos(e)."""
    s = (e - 1) // 2
    pos = {m: k for k, m in enumerate(A.monos(e))}
    f = [0] * len(pos)
    g = [0] * len(pos)
    f[pos[(e, 0, 0)]] = 1
    g[pos[(0, e, 0)]] = 1
    for a, c in enumerate(in_a_basis(p, alpha, s)):
        f[pos[(a, a + 1, s - a)]] = c
    tb = P_(p, beta)(P_(p, [-1, 1]))  # beta(h - 1)
    for a, c in enumerate(in_a_basis(p, coeffs(tb, s + 1), s)):
        g[pos[(a + 1, a, s - a)]] = c
    return f, g


def alpha_beta_of_pair(e, p, fv, gv):
    """The member (alpha, beta) of a stored pair, rescaled by 1/c0 and 1/c1 (the coefficients of x^e and y^e); None when the pair is not
    of the form of the stratum (a monomial outside it, or a missing x^e or y^e)."""
    s = (e - 1) // 2
    mons = A.monos(e)
    f = {m: int(c) % p for m, c in zip(mons, fv) if int(c) % p}
    g = {m: int(c) % p for m, c in zip(mons, gv) if int(c) % p}
    c0, c1 = f.get((e, 0, 0), 0), g.get((0, e, 0), 0)
    if not c0 or not c1:
        return None
    al, tb = P_(p, [0]), P_(p, [0])
    for (a, b, c), v in f.items():
        if (a, b, c) == (e, 0, 0):
            continue
        if not (b == a + 1 and c == s - a):
            return None
        al = al + a_poly(p, a) * (v * pow(c0, -1, p) % p)
    for (a, b, c), v in g.items():
        if (a, b, c) == (0, e, 0):
            continue
        if not (a == b + 1 and c == s - b):
            return None
        tb = tb + a_poly(p, b) * (v * pow(c1, -1, p) % p)
    return coeffs(al, s + 1), coeffs(tb(P_(p, [1, 1])), s + 1)  # beta(h) = tb(h + 1)


# ------------------------------------------------------------------ the exact filter
def _vec(q, delta, m):
    cs = [int(c) for c in (q % delta).coeffs()]
    return cs + [0] * (m - len(cs))


def solve_mult(target, x, delta, s, p):
    """The polynomial c of degree <= s with target = c x modulo delta, or None (exact linear algebra over GF(p))."""
    m = delta.degree()
    cols = [_vec(P_(p, [0] * k + [1]) * x, delta, m) for k in range(s + 1)]
    tv = _vec(target, delta, m)
    amat = flint.nmod_mat([[cols[k][r] for k in range(s + 1)] for r in range(m)], p)
    aug = flint.nmod_mat([[cols[k][r] for k in range(s + 1)] + [tv[r]] for r in range(m)], p)
    if amat.rank() != aug.rank():
        return None
    red, rk = aug.rref()
    sol = [0] * (s + 1)
    for r in range(rk):
        lead = next(k for k in range(s + 2) if int(red[r, k]) != 0)
        if lead <= s:
            sol[lead] = int(red[r, s + 1])
    return P_(p, sol)


def filter_member(e, p, alpha, beta):
    """The exact filter on a member.  Returns (stage, c, c') with stage = the number of the tests (F0, F1, F2, F3) the member passes in
    turn, 0 to 4 (4 = passes all); c and c' are coefficient lists of length s + 1 once (F1), respectively (F2), has passed, else None."""
    s = (e - 1) // 2
    h = P_(p, [0, 1])
    ae = a_poly(p, e - 1)
    al, be = P_(p, alpha), P_(p, beta)
    bs = be(P_(p, [(e - 1) % p, 1]))
    delta = al * bs - ae
    if delta.degree() != 2 * s:
        return 0, None, None
    x = (h - 2) * delta(P_(p, [-(e + 1) % p, 1]))
    xp = (h + e) * delta(P_(p, [(e + 1) % p, 1]))
    if delta.gcd(x).degree() > 0 or delta.gcd(xp).degree() > 0:
        return 0, None, None
    c = solve_mult(xp * al, x, delta, s, p)
    if c is None:
        return 1, None, None
    cp = solve_mult(x * bs, xp, delta, s, p)
    if cp is None:
        return 2, coeffs(c, s + 1), None
    cl, cpl = coeffs(c, s + 1), coeffs(cp, s + 1)
    if (c * cp - ae).degree() < 0:
        return 3, cl, cpl
    return 4, cl, cpl


# ------------------------------------------------------------------ the block test of (F1)
def shift_matrix(n, c, p):
    """S with (S q)_i = coefficient of h^i of q(h + c), for q with n + 1 coefficients."""
    S = np.zeros((n + 1, n + 1), dtype=np.int64)
    for j in range(n + 1):
        for i in range(j + 1):
            S[i, j] = comb(j, i) * pow(c, j - i, p) % p
    return S


class BlockF1:
    """(F1) on arrays of members, with numpy: the degree of Delta is 2s, and X' alpha lies in the span of h^k X (k <= s) modulo Delta
    (rank of the columns h^k X mod Delta, k = 0..s, against the same with the column X' alpha, by elimination modulo p on the batch)."""

    def __init__(self, e, p, dtype=np.int32):
        self.e, self.p, self.s, self.dt = e, p, (e - 1) // 2, dtype
        s = self.s
        self.Sb = shift_matrix(s, e - 1, p).T.astype(dtype)  # beta(h) -> beta(h + e - 1), applied on the right
        self.Sx = shift_matrix(2 * s, -(e + 1) % p, p).T.astype(dtype)
        self.Sxp = shift_matrix(2 * s, (e + 1) % p, p).T.astype(dtype)
        self.Ae = np.array(a_coeffs(p, e - 1), dtype=dtype)
        self.inv = np.zeros(p, dtype=dtype)
        for v in range(1, p):
            self.inv[v] = pow(v, -1, p)

    def _reduce(self, M, dn):
        """Remainders of the rows of M (polynomials, low degree first) modulo the monic rows dn of degree 2s."""
        p, m = self.p, 2 * self.s
        for k in range(M.shape[1] - 1, m - 1, -1):
            M[:, k - m:k + 1] -= M[:, k:k + 1] * dn
            M[:, k - m:k + 1] %= p
        return M[:, :m]

    def passes(self, alpha, beta):
        """Boolean mask of the members of the batch that pass: degree of Delta = 2s and (F1) solvable.  alpha, beta: (N, s + 1) arrays."""
        p, s, dt = self.p, self.s, self.dt
        alpha = alpha.astype(dt)
        beta = beta.astype(dt)
        n = alpha.shape[0]
        m = 2 * s
        out = np.zeros(n, dtype=bool)
        bs = (beta @ self.Sb) % p
        d = np.zeros((n, m + 1), dtype=dt)
        for i in range(s + 1):
            d[:, i:i + s + 1] += alpha[:, i:i + 1] * bs
        d = (d - self.Ae) % p
        keep = np.flatnonzero(d[:, m] != 0)
        if keep.size == 0:
            return out
        d, alpha = d[keep], alpha[keep]
        k = keep.size
        dn = (d * self.inv[d[:, m]][:, None]) % p
        dm = (d @ self.Sx) % p
        dp = (d @ self.Sxp) % p
        x = np.zeros((k, m + 2), dtype=dt)
        x[:, 1:] += dm
        x[:, :m + 1] -= 2 * dm
        x %= p
        xp = np.zeros((k, m + 2), dtype=dt)
        xp[:, 1:] += dp
        xp[:, :m + 1] += self.e * dp
        xp %= p
        t = np.zeros((k, m + 2 + s), dtype=dt)
        for i in range(s + 1):
            t[:, i:i + m + 2] += alpha[:, i:i + 1] * xp
        t %= p
        mat = np.empty((k, m, s + 2), dtype=dt)
        r = self._reduce(x, dn).copy()
        mat[:, :, 0] = r
        for col in range(1, s + 1):
            nxt = np.zeros((k, m + 1), dtype=dt)
            nxt[:, 1:] = r
            nxt[:, :m + 1] -= nxt[:, m:m + 1] * dn
            nxt %= p
            r = nxt[:, :m].copy()
            mat[:, :, col] = r
        mat[:, :, s + 1] = self._reduce(t, dn)
        out[keep] = self._solvable(mat)
        return out

    def _solvable(self, mat):
        """Whether the last column of each matrix of the batch (k, rows, s + 2) lies in the span of the others (elimination modulo p)."""
        p = self.p
        k, rows, nc = mat.shape
        used = np.zeros((k, rows), dtype=bool)
        for col in range(nc - 1):
            cand = (mat[:, :, col] != 0) & ~used
            has = cand.any(axis=1)
            ar = np.flatnonzero(has)
            if ar.size == 0:
                continue
            pr = cand[ar].argmax(axis=1)
            piv = mat[ar, pr, :]
            pivn = (piv * self.inv[piv[:, col]][:, None]) % p
            sub = mat[ar]
            fac = sub[:, :, col].copy()
            fac[np.arange(ar.size), pr] = 0
            sub = (sub - fac[:, :, None] * pivn[:, None, :]) % p
            sub[np.arange(ar.size), pr, :] = pivn
            mat[ar] = sub
            used[ar, pr] = True
        # (F0) makes X a unit modulo Delta, so the columns h^k X (k <= s < 2s) are independent: a member whose columns are dependent fails
        # (F0), and dropping it here never rejects a member that the exact test accepts
        return ~((mat[:, :, nc - 1] != 0) & ~used).any(axis=1) & (used.sum(axis=1) == nc - 1)


# ------------------------------------------------------------------ the members of a case
def case_seed(index):
    return SEED_BASE + index


def sample_block(e, p, seed_index, block, count=BLOCK):
    """Members block * BLOCK .. block * BLOCK + count - 1 of a case: (alpha, beta) arrays of shape (count, s + 1), uniform coefficients,
    alpha not zero (a zero alpha is drawn again); numpy's default_rng seeded with (20261120 + the index of the case, block)."""
    s = (e - 1) // 2
    rng = np.random.default_rng([case_seed(seed_index), block])
    alpha = rng.integers(0, p, size=(BLOCK, s + 1), dtype=np.int64)
    beta = rng.integers(0, p, size=(BLOCK, s + 1), dtype=np.int64)
    zero = np.flatnonzero(~alpha.any(axis=1))
    while zero.size:
        alpha[zero] = rng.integers(0, p, size=(zero.size, s + 1), dtype=np.int64)
        zero = zero[~alpha[zero].any(axis=1)]
    return alpha[:count], beta[:count]


# ------------------------------------------------------------------ the staged test of the pure Hilbert function
def hilbert_pure(e, p, f, g):
    """The staged test of EXP-010 for the pair (f, g) of the stratum (rank of mu_n through its Ranker on the supports of the stratum)."""
    m, i, j = stratum(e)
    rk = X.ranker(e, p, m, i, j)
    return bool(rk.evaluate(np.asarray(f, dtype=np.int64)[rk.I], np.asarray(g, dtype=np.int64)[rk.J])[1])


def block_job(spec):
    """One block of a case: the filter on its members and the staged test on those that pass.  spec: e, p, seed_index, block, count.
    Returns the counts (the members examined, those the block test of (F1) accepts, and the exact stages in turn: (F0), (F1), (F2), (F3)),
    the members with the pure Hilbert function found in the order of their index (the caller keeps MAX_STORED) and the seconds."""
    import time
    t0 = time.time()
    e, p = spec["e"], spec["p"]
    alpha, beta = sample_block(e, p, spec["seed_index"], spec["block"], spec["count"])
    bf = block_f1(e, p)
    t1 = time.time()
    mask = bf.passes(alpha, beta)
    t2 = time.time()
    base = spec["block"] * BLOCK
    counts = {"examined": int(alpha.shape[0]), "block_f1": int(mask.sum()), "f0": 0, "f1": 0, "f2": 0, "f3": 0, "pure_hilbert": 0,
              "inconsistent": 0}
    found = []
    for k in np.flatnonzero(mask):
        a, b = [int(v) for v in alpha[k]], [int(v) for v in beta[k]]
        stage, c, cp = filter_member(e, p, a, b)
        if stage == 1:  # (F0) holds and the block test of (F1) accepted: the exact (F1) must hold too
            counts["inconsistent"] += 1
        counts["f0"] += stage >= 1
        counts["f1"] += stage >= 2
        counts["f2"] += stage >= 3
        if stage < 4:
            continue
        counts["f3"] += 1
        f, g = pair_vectors(e, p, a, b)
        if hilbert_pure(e, p, f, g):
            counts["pure_hilbert"] += 1
            found.append({"index": base + int(k), "alpha": a, "beta": b, "c": c, "cp": cp, "f": f, "g": g})
    return {"counts": counts, "found": found, "seconds": round(time.time() - t0, 3), "sample_seconds": round(t1 - t0, 3),
            "block_seconds": round(t2 - t1, 3)}


def betti_job(task):
    """The Betti table of one member through the routine of EXP-010: {'key', 'index', 'betti', 'pure', 'seconds'}."""
    return X.betti_job(task)


_BLOCKS = {}


def block_f1(e, p):
    key = (e, p)
    if key not in _BLOCKS:
        _BLOCKS[key] = BlockF1(e, p)
    return _BLOCKS[key]
