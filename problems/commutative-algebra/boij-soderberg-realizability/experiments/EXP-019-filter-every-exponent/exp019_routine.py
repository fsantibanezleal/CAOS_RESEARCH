"""EXP-019 routine: the pairs f = x^e + alpha(xy, z) y^t, g = y^e + beta(xy, z) x^t of the stratum S((e + t)/2; 0, (e - t)/2), the filter
(F0) to (F3) of hypothesis.md written for the exponent t, the random members of a case, and the staged test of the pure Hilbert function.

Conventions (hypothesis.md, 'Definitions fixed here').  d = (e - t)/2.  A member is (alpha, beta): coefficient lists of 1, h, ..., h^d over
GF(p).  Its pair: f = x^e + sum_a gamma_a x^a y^(a+t) z^(d-a) with alpha = sum gamma_a A_a(h); g = y^e + sum_a gamma'_a x^(a+t) y^a z^(d-a)
with beta(h - t) = sum gamma'_a A_a(h); A_a(h) = h (h + 1) ... (h + a - 1).  Vectors are on `uhlib.algebra.monos(e)` (PBW monomials (a, b, c)).

Filter (z = 1; Delta = alpha(h) beta(h + e - t) - A_(e-t)(h); X = (h - t - 1) ... (h - 2t) Delta(h - e - t);
X' = (h + e) ... (h + e + t - 1) Delta(h + e + t)):
    (F0) Delta has degree 2d and is coprime to X and to X';  (F1) X' alpha = c X mod Delta, deg c <= d;
    (F2) X beta(h + e - t) = c' X' mod Delta, deg c' <= d;  (F3) c c' is not equal to A_(e-t).
`filter_t` is the exact test: once (F0) holds X and X' are units modulo Delta, so (F1) and (F2) are decided by the inverse (extended greatest
common divisor) and the degree of the reduced quotient.  For t = 1 it is the filter of EXP-017 (`exp017_routine.filter_member`).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPS = HERE.parent
for _p in (EXPS / "EXP-017-odd-stratum-filter", EXPS / "EXP-010-weight-class-strata"):
    if str(_p) not in sys.path:
        sys.path.append(str(_p))

import exp017_routine as R17  # noqa: E402  (imports the routine of EXP-010 and replaces its tensor of structure constants)

X = R17.X
flint, np, A = R17.flint, R17.np, R17.A

# EXP-018 met memory exhaustion with twelve workers each holding the tensors of the routine of EXP-010: the cache of tensors is cut to 4
X.struct_tensor = X.lru_cache(maxsize=4)(R17._struct_tensor_mod_p)

SEED_BASE = X.SEED_BASE  # 20261120
MAX_STORED = 50  # members with the pure Hilbert function stored per case
MAX_TABLES = 40
EARLY_STOP_PURE = 5
STAGES = ("F0", "F1", "F2", "F3")
P_ = R17.P_
a_poly = R17.a_poly
coeffs = R17.coeffs
in_a_basis = R17.in_a_basis


def stratum(e, t):
    return ((e + t) // 2, 0, (e - t) // 2)


def shifted_a(p, a, start):
    """(h + start) (h + start + 1) ... (h + start + a - 1) as a polynomial over GF(p)."""
    r = P_(p, [1])
    for k in range(a):
        r = r * P_(p, [start + k, 1])
    return r


def exponent_of_pair(e, p):
    """The largest t of the parity of e with t <= e - 2, 2t <= p - 1 and, when p <= e, p not dividing (e + t)/2 (hypothesis.md), or None."""
    best = None
    for t in range(e % 2 if e % 2 else 2, e - 1, 2):
        if 2 * t <= p - 1 and not (p <= e and ((e + t) // 2) % p == 0):
            best = t
    return best


# ------------------------------------------------------------------ the conversions
def pair_vectors(e, p, t, alpha, beta):
    """The pair (f, g) of the member (alpha, beta) as coefficient vectors (lists of ints in [0, p)) on monos(e)."""
    d = (e - t) // 2
    pos = {m: k for k, m in enumerate(A.monos(e))}
    f = [0] * len(pos)
    g = [0] * len(pos)
    f[pos[(e, 0, 0)]] = 1
    g[pos[(0, e, 0)]] = 1
    for a, c in enumerate(in_a_basis(p, alpha, d)):
        f[pos[(a, a + t, d - a)]] = c
    tb = P_(p, beta)(P_(p, [-t, 1]))  # beta(h - t)
    for a, c in enumerate(in_a_basis(p, coeffs(tb, d + 1), d)):
        g[pos[(a + t, a, d - a)]] = c
    return f, g


def alpha_beta_of_pair(e, p, t, fv, gv):
    """The member (alpha, beta) of a stored pair, rescaled by 1/c0 and 1/c1 (the coefficients of x^e and y^e); None when the pair is not of
    the form of the stratum (a monomial outside it, or a missing x^e or y^e)."""
    d = (e - t) // 2
    f = {m: int(c) % p for m, c in zip(A.monos(e), fv) if int(c) % p}
    g = {m: int(c) % p for m, c in zip(A.monos(e), gv) if int(c) % p}
    c0, c1 = f.get((e, 0, 0), 0), g.get((0, e, 0), 0)
    if not c0 or not c1:
        return None
    al, tb = P_(p, [0]), P_(p, [0])
    for (a, b, c), v in f.items():
        if (a, b, c) == (e, 0, 0):
            continue
        if not (b == a + t and c == d - a):
            return None
        al = al + a_poly(p, a) * (v * pow(c0, -1, p) % p)
    for (a, b, c), v in g.items():
        if (a, b, c) == (0, e, 0):
            continue
        if not (a == b + t and c == d - b):
            return None
        tb = tb + a_poly(p, b) * (v * pow(c1, -1, p) % p)
    return coeffs(al, d + 1), coeffs(tb(P_(p, [t, 1])), d + 1)  # beta(h) = tb(h + t)


# ------------------------------------------------------------------ the exact filter
def low_degree_multiplier(target, x, delta, d, p):
    """The polynomial c of degree <= d with target = c x modulo delta (x a unit modulo delta), or None."""
    g, s, _ = x.xgcd(delta)  # s x + _ delta = g, a nonzero constant when x is coprime to delta
    if g.degree() != 0:
        return None
    c = (target * s * P_(p, [pow(int(g[0]), -1, p)])) % delta
    return c if c.degree() <= d else None


def filter_t(e, p, t, alpha, beta):
    """The exact filter on a member.  Returns (stage, c, c') with stage = the number of the tests (F0, F1, F2, F3) the member passes in turn,
    0 to 4 (4 = passes all); c and c' are coefficient lists of length d + 1 once (F1), respectively (F2), has passed, else None."""
    d = (e - t) // 2
    ae = a_poly(p, e - t)
    al, be = P_(p, alpha), P_(p, beta)
    bs = be(P_(p, [(e - t) % p, 1]))
    delta = al * bs - ae
    if delta.degree() != 2 * d:
        return 0, None, None
    x = shifted_a(p, t, -2 * t) * delta(P_(p, [-(e + t) % p, 1]))
    xp = shifted_a(p, t, e) * delta(P_(p, [(e + t) % p, 1]))
    if delta.gcd(x).degree() > 0 or delta.gcd(xp).degree() > 0:
        return 0, None, None
    c = low_degree_multiplier(xp * al, x, delta, d, p)
    if c is None:
        return 1, None, None
    cp = low_degree_multiplier(x * bs, xp, delta, d, p)
    if cp is None:
        return 2, coeffs(c, d + 1), None
    cl, cpl = coeffs(c, d + 1), coeffs(cp, d + 1)
    if (c * cp - ae).degree() < 0:
        return 3, cl, cpl
    return 4, cl, cpl


def stage_only(e, p, t, alpha, beta):
    """The stage of `filter_t` without the coefficient lists (the hot loop of a case)."""
    return filter_t(e, p, t, alpha, beta)[0]


# ------------------------------------------------------------------ the members of a case
def case_seed(index):
    return SEED_BASE + index


def sample_block(e, p, t, seed_index, block, count, block_size):
    """Members block * block_size .. block * block_size + count - 1 of a case: (alpha, beta) arrays of shape (count, d + 1), uniform
    coefficients, alpha not zero (a zero alpha is drawn again); numpy's default_rng seeded with (20261120 + the index of the case, block),
    which draws `block_size` rows of alpha, then `block_size` rows of beta, then redraws the rows of a zero alpha."""
    d = (e - t) // 2
    rng = np.random.default_rng([case_seed(seed_index), block])
    alpha = rng.integers(0, p, size=(block_size, d + 1), dtype=np.int64)
    beta = rng.integers(0, p, size=(block_size, d + 1), dtype=np.int64)
    zero = np.flatnonzero(~alpha.any(axis=1))
    while zero.size:
        alpha[zero] = rng.integers(0, p, size=(zero.size, d + 1), dtype=np.int64)
        zero = zero[~alpha[zero].any(axis=1)]
    return alpha[:count], beta[:count]


# ------------------------------------------------------------------ the staged test of the pure Hilbert function
def hilbert_pure(e, p, t, f, g):
    """The staged test of EXP-010 for the pair (f, g) of the stratum S((e + t)/2; 0, (e - t)/2)."""
    m, i, j = stratum(e, t)
    rk = X.ranker(e, p, m, i, j)
    return bool(rk.evaluate(np.asarray(f, dtype=np.int64)[rk.I], np.asarray(g, dtype=np.int64)[rk.J])[1])


def block_job(spec):
    """One block of a case.  spec: e, p, t, seed_index, block, count, block_size.  The exact filter on every member and the staged test on
    those that pass (F3).  Returns the counts (the members examined and those passing (F0), (F1), (F2), (F3) in turn, those with the pure
    Hilbert function), the members with the pure Hilbert function in the order of their index (the caller keeps MAX_STORED), and the
    seconds of the filter and of the staged test."""
    import time
    t0 = time.time()
    e, p, t = spec["e"], spec["p"], spec["t"]
    alpha, beta = sample_block(e, p, t, spec["seed_index"], spec["block"], spec["count"], spec["block_size"])
    al, be = alpha.tolist(), beta.tolist()
    base = spec["block"] * spec["block_size"]
    counts = {"examined": int(alpha.shape[0]), "f0": 0, "f1": 0, "f2": 0, "f3": 0, "pure_hilbert": 0}
    passing = []
    t1 = time.time()
    for k in range(alpha.shape[0]):
        stage, c, cp = filter_t(e, p, t, al[k], be[k])
        if stage >= 1:
            counts["f0"] += 1
        if stage >= 2:
            counts["f1"] += 1
        if stage >= 3:
            counts["f2"] += 1
        if stage == 4:
            counts["f3"] += 1
            passing.append((k, c, cp))
    t2 = time.time()
    found = []
    for k, c, cp in passing:
        f, g = pair_vectors(e, p, t, al[k], be[k])
        if hilbert_pure(e, p, t, f, g):
            counts["pure_hilbert"] += 1
            found.append({"index": base + k, "alpha": al[k], "beta": be[k], "c": c, "cp": cp, "f": f, "g": g})
    return {"counts": counts, "found": found, "seconds": round(time.time() - t0, 3), "filter_seconds": round(t2 - t1, 3),
            "staged_seconds": round(time.time() - t2, 3), "sample_seconds": round(t1 - t0, 3)}


def betti_job(task):
    """The Betti table of one member through the routine of EXP-010: {'key', 'index', 'betti', 'pure', 'seconds'}."""
    return X.betti_job(task)


# ------------------------------------------------------------------ G1 (a): the stored members
SOURCES = ("EXP-010-weight-class-strata", "EXP-014-middle-strata", "EXP-015-linear-rule-and-e9", "EXP-018-largest-exponent-strata")
PROBE_COUNTS = {"pure": 317, "other": 128}  # the counts of the probe of the coordinating session (hypothesis.md, 'Evidence')


def stored_members_record():
    """The filter on every member with a computed Betti table that the four experiments stored in a stratum S((e + t)/2; 0, (e - t)/2) with
    t >= 1 (the flag `pure` is True or False; a stratum stored by two experiments is counted twice).  Returns the totals by kind and stage,
    the per-stratum rows, and the members not of the form of the stratum."""
    import json
    rows, tot = [], {"pure": [0] * 5, "other": [0] * 5, "not_of_the_form": 0}
    for name in SOURCES:
        res = json.loads((EXPS / name / "artifacts" / "results.json").read_text(encoding="utf-8"))
        for key, st in res["strata"].items():
            e, p, m, i, j = st["e"], st["p"], st["m"], st["i"], st["j"]
            t = m - j
            if i != 0 or m + j != e or t < 1 or not st.get("members"):
                continue
            row = {"source": name, "stratum": key, "e": e, "p": p, "t": t, "pure": [0] * 5, "other": [0] * 5, "not_of_the_form": 0}
            for mem in st["members"]:
                if mem.get("pure") not in (True, False):
                    continue
                kind = "pure" if mem["pure"] else "other"
                ab = alpha_beta_of_pair(e, p, t, mem["f"], mem["g"])
                if ab is None:
                    row["not_of_the_form"] += 1
                    tot["not_of_the_form"] += 1
                    continue
                stage = filter_t(e, p, t, *ab)[0]
                row[kind][stage] += 1
                tot[kind][stage] += 1
            if sum(row["pure"]) + sum(row["other"]) + row["not_of_the_form"]:
                rows.append(row)
    return {"sources": list(SOURCES), "rows": rows, "pure_by_stage": tot["pure"], "other_by_stage": tot["other"],
            "pure": sum(tot["pure"]), "other": sum(tot["other"]), "not_of_the_form": tot["not_of_the_form"],
            "probe_counts": PROBE_COUNTS,
            "ok": tot["pure"][:4] == [0, 0, 0, 0] and tot["other"][4] == 0 and tot["not_of_the_form"] == 0 and sum(tot["pure"]) > 0}
