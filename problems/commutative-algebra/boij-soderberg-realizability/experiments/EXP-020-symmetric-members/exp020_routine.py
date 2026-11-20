"""EXP-020 routine: the members f = x^e + alpha(xy, z) y^t, g = y^e + beta(xy, z) x^t with beta = c alpha^omega, fixed by the exchange omega of x
and y (z -> -z), enumerated completely; the filter (F0) to (F3) of EXP-019 with (F1) and (F2) reported separately and (C1).

Conventions (hypothesis.md, 'Definitions fixed here').  d = (e - t)/2.  A member is (alpha, c): alpha = a_0 + a_1 h + ... + a_d h^d over GF(p), not
zero, and c in {1, nu}, nu the least positive integer that is not a square modulo p.  At z = 1,
    beta(h) = c * sum_i a_i (h - 1)^i (-1)^(d - i)        (alpha^omega(h, z) = alpha(h - z, -z)).
Enumeration: the alphas not zero in the lexicographic order of (a_0, ..., a_d), the last coefficient varying fastest; the RANK of alpha is its
position in that order counted from 0 (the integer sum a_i p^(d - i), minus 1); the INDEX of a member is 2 * rank + (0 for c = 1, 1 for c = nu).
A case has 2 (p^(d + 1) - 1) members with the indices 0 to 2 (p^(d + 1) - 1) - 1.  A block of a case is a range of ranks [r0, r1).

The filter is the filter of EXP-019 (`exp019_routine.filter_t`); `member_detail` computes the same stage with the same polynomials and in
addition decides (F1) and (F2) separately once (F0) holds, and (C1).  The two are compared on every member by the tests.
"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPS = HERE.parent
_EXP19 = str(EXPS / "EXP-019-filter-every-exponent")
if _EXP19 not in sys.path:
    sys.path.insert(0, _EXP19)

import exp019_routine as R19  # noqa: E402  (imports the routine of EXP-010 and sets the cache of tensors to 4 entries)

X = R19.X
np, A, P_ = R19.np, R19.A, R19.P_
a_poly, coeffs = R19.a_poly, R19.coeffs
stratum, exponent_of_pair, pair_vectors, hilbert_pure = R19.stratum, R19.exponent_of_pair, R19.pair_vectors, R19.hilbert_pure
MAX_STORED = 10 ** 9  # every passing member is stored (the lists are small)
MAX_TABLES = R19.MAX_TABLES
EARLY_STOP_PURE = R19.EARLY_STOP_PURE


# ------------------------------------------------------------------ the map alpha -> beta
def least_nonresidue(p):
    """The least positive integer that is not a square modulo the odd prime p."""
    return next(c for c in range(2, p) if pow(c, (p - 1) // 2, p) == p - 1)


def omega_matrix(p, d):
    """The matrix M (d + 1 by d + 1) with beta_k = c sum_i a_i M[i][k] mod p: M[i][k] = (-1)^(d - i) binom(i, k) (-1)^(i - k)."""
    from math import comb
    return np.array([[((-1) ** (d - i) * comb(i, k) * (-1) ** (i - k)) % p if k <= i else 0 for k in range(d + 1)] for i in range(d + 1)],
                    dtype=np.int64)


def beta_of(p, d, alpha, scalar):
    """The coefficient list of beta = scalar * alpha^omega at z = 1, from the coefficient list of alpha."""
    m = omega_matrix(p, d)
    return [int(v) for v in (np.array(alpha, dtype=np.int64) @ m * scalar) % p]


def betas(p, d, alphas, scalar):
    """beta for every row of the array `alphas` (rows of length d + 1)."""
    return (alphas @ omega_matrix(p, d) * scalar) % p


# ------------------------------------------------------------------ the enumeration
def n_members(p, d):
    return 2 * (p ** (d + 1) - 1)


def alpha_of_rank(p, d, rank):
    v = rank + 1
    return [(v // p ** (d - i)) % p for i in range(d + 1)]


def rank_of_alpha(p, d, alpha):
    return sum(int(a) * p ** (d - i) for i, a in enumerate(alpha)) - 1


def alpha_block(p, d, r0, r1):
    """The alphas of the ranks r0 .. r1 - 1 as an array of shape (r1 - r0, d + 1)."""
    v = np.arange(r0 + 1, r1 + 1, dtype=np.int64)
    return np.stack([(v // p ** (d - i)) % p for i in range(d + 1)], axis=1)


def index_of(p, d, alpha, flag):
    return 2 * rank_of_alpha(p, d, alpha) + flag


def member_of_index(p, d, index):
    """(alpha, c, beta) of the member with the given index; c is 1 or nu."""
    rank, flag = divmod(index, 2)
    alpha = alpha_of_rank(p, d, rank)
    scalar = (1, least_nonresidue(p))[flag]
    return alpha, scalar, beta_of(p, d, alpha, scalar)


# ------------------------------------------------------------------ the filter on one member
def case_context(e, p, t):
    """The polynomials of the filter that depend on the case only."""
    d = (e - t) // 2
    return {"e": e, "p": p, "t": t, "d": d, "ae": a_poly(p, e - t), "shift": P_(p, [(e - t) % p, 1]),
            "xa": R19.shifted_a(p, t, -2 * t), "xpa": R19.shifted_a(p, t, e), "sub_m": P_(p, [-(e + t) % p, 1]),
            "sub_p": P_(p, [(e + t) % p, 1])}


def member_detail(ctx, alpha, beta):
    """(stage, f1, f2, c, cp, c1) of a member.  `stage` is that of `exp019_routine.filter_t` (0 to 4; 4 passes (F0) to (F3)); f1 and f2 are
    None when (F0) fails and True or False, decided separately, once (F0) holds; c and cp are the forms of the filter as coefficient lists
    (None when the test does not hold); c1 is (C1), Delta coprime to A_(e - t), for a member with stage 4 and None otherwise."""
    p, d, ae = ctx["p"], ctx["d"], ctx["ae"]
    al, be = P_(p, alpha), P_(p, beta)
    bs = be(ctx["shift"])
    delta = al * bs - ae
    if delta.degree() != 2 * d:
        return 0, None, None, None, None, None
    x = ctx["xa"] * delta(ctx["sub_m"])
    xp = ctx["xpa"] * delta(ctx["sub_p"])
    if delta.gcd(x).degree() > 0 or delta.gcd(xp).degree() > 0:
        return 0, None, None, None, None, None
    c = R19.low_degree_multiplier(xp * al, x, delta, d, p)
    cp = R19.low_degree_multiplier(x * bs, xp, delta, d, p)
    f1, f2 = c is not None, cp is not None
    cl = coeffs(c, d + 1) if f1 else None
    cpl = coeffs(cp, d + 1) if f2 else None
    if not f1:
        return 1, f1, f2, None, None, None
    if not f2:
        return 2, f1, f2, cl, None, None
    if (c * cp - ae).degree() < 0:
        return 3, f1, f2, cl, cpl, None
    return 4, f1, f2, cl, cpl, delta.gcd(ae).degree() == 0


# ------------------------------------------------------------------ one block of a case
def block_job(spec):
    """The filter on every member of the ranks r0 .. r1 - 1 (both values of c each), spec: e, p, t, r0, r1.  Returns the counts, the number of
    members stopped at each stage, the passing members (stage 4) in the order of their index with (C1), the pair (f, g) as coefficient vectors
    and the forms of the filter, and the seconds."""
    t0 = time.time()
    e, p, t = spec["e"], spec["p"], spec["t"]
    d = (e - t) // 2
    ctx = case_context(e, p, t)
    nu = least_nonresidue(p)
    al = alpha_block(p, d, spec["r0"], spec["r1"])
    counts = {"examined": 0, "f0": 0, "f1": 0, "f2": 0, "f3": 0, "differ": 0, "c1": 0}
    stages = [0] * 5
    passing = []
    alist = al.tolist()
    for flag, scalar in enumerate((1, nu)):
        blist = betas(p, d, al, scalar).tolist()
        for k, (a, b) in enumerate(zip(alist, blist)):
            st, f1, f2, c, cp, c1 = member_detail(ctx, a, b)
            stages[st] += 1
            counts["examined"] += 1
            if st >= 1:
                counts["f0"] += 1
                if f1 != f2:
                    counts["differ"] += 1
            if st >= 2:
                counts["f1"] += 1
            if st >= 3:
                counts["f2"] += 1
            if st == 4:
                counts["f3"] += 1
                counts["c1"] += 1 if c1 else 0
                f, g = pair_vectors(e, p, t, a, b)
                passing.append({"index": 2 * (spec["r0"] + k) + flag, "alpha": a, "scalar": scalar, "beta": b, "form_c": c, "form_cp": cp,
                                "c1": bool(c1), "f": f, "g": g})
    passing.sort(key=lambda m: m["index"])
    return {"counts": counts, "stage_counts": stages, "passing": passing, "seconds": round(time.time() - t0, 3)}


def staged_job(task):
    """The staged test of the pure Hilbert function on one passing member: {'index', 'pure_hilbert', 'seconds'}."""
    t0 = time.time()
    ok = hilbert_pure(task["e"], task["p"], task["t"], task["f"], task["g"])
    return {"index": task["index"], "pure_hilbert": bool(ok), "seconds": round(time.time() - t0, 2)}


def betti_job(task):
    """The Betti table and the length of U / (U f + U g) by `uhlib` (the module construction and Tor of the routine of EXP-010), for the pair of
    a stored member: {'key', 'index', 'betti', 'length', 'pure', 'seconds'}.  Pure: the table is (1, 2, 2, 1) in degrees (0, e, 3e, 4e) and the
    length (the sum of the dimensions of the finite module) is e^3."""
    t0 = time.time()
    e, p = task["e"], task["p"]
    rels = [{(0, mono): int(c) for mono, c in zip(A.monos(e), v) if int(c) % p} for v in (task["f"], task["g"])]
    module = X.quotient_module_np(X.PrimeField(p), [0], rels, maxdeg=4 * e + 8)
    table = X.tor.betti(module) if module.finished else None
    length = int(sum(module.dims)) if module.finished else None
    pure = table is not None and table == X.pure_table(e) and length == e ** 3
    return {"key": task["key"], "index": task["index"], "betti": X.table_rows(table), "length": length, "pure": bool(pure),
            "seconds": round(time.time() - t0, 2)}
