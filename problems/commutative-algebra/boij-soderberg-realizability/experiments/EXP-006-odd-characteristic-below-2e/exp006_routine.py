"""EXP-006 routine: pairs of forms of degree e in U(H), the rank of mu_n(W), the Hilbert function of U/(U W), the Betti
table through `uhlib`, the seeded random subspaces, the enumeration of subspaces and the orbit test of family B2.

First instrument of EXP-006.  It uses `uhlib` for the algebra (PBW monomials, the product, the fields, the enumeration
of subspaces, the module construction and the Betti table through Tor) and carries its OWN rank routine for
mu_n(W): U_(n-e) tensor W -> U_n, (a, w) -> a * w (LEFT multiplication), exact over GF(p) and GF(p^k).

Arithmetic.  A field element of GF(p^k) is a vector of k integers modulo p (uhlib's encoding, modulus
`F.modulus`, a^0, a^1, ... low to high).  The matrix of mu_n(W) over GF(q) has entries sum_m c_m T[u, m, col] with
T the integer structure constants of the product; it is built as an array E[row, col, j] over GF(p).  Its rank over
GF(q) is rank over GF(p) of the matrix with rows a^i * v_r (i = 0..k-1) in the coordinates (col, j), divided by k:
a GF(q)-subspace of dimension r has GF(p)-dimension k r.  For k = 1 this is the plain rank modulo p.  Integer
arithmetic modulo p (numpy int64) only; no floating point.
"""
import random
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

import numpy as np  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import structure as S  # noqa: E402
from uhlib import tor  # noqa: E402
from uhlib.fastmod import quotient_module_np  # noqa: E402
from uhlib.fields import ExtField, PrimeField  # noqa: E402
from uhlib.module import quotient_module  # noqa: E402

SEED_BASE = 20261120
PURE_TYPE = (1, 2, 2, 1)


# ------------------------------------------------------------------ the formula
def u(n):
    return A.dim_U(n)


def h_e(e, n):
    """Hilbert function of the pure table (1, 2, 2, 1) on (0, e, 3e, 4e)."""
    return u(n) - 2 * u(n - e) + 2 * u(n - 3 * e) - u(n - 4 * e)


def pure_table(e):
    return {(0, 0): 1, (1, e): 2, (2, 3 * e): 2, (3, 4 * e): 1}


def hilbert_bound(e):
    """Degrees 0..4e+2 are compared with h_e (two zero degrees after the top degree 4e - 4 of h_e)."""
    return 4 * e + 2


def target_rank(e):
    """rank mu_3e(W) of a space with the pure Hilbert function."""
    return u(3 * e) - h_e(e, 3 * e)


# ------------------------------------------------------------------ fields
def make_field(name):
    """'GF(q)' for a prime or a prime power q ('GF(9)' = 'GF(3^2)'), or 'GF(p^k)'; extension fields use the modulus of uhlib
    (first irreducible monic polynomial, lexicographic on the low coefficients)."""
    assert name.startswith("GF(") and name.endswith(")"), name
    body = name[3:-1]
    if "^" in body:
        p, k = (int(t) for t in body.split("^"))
        return ExtField(p, k) if k > 1 else PrimeField(p)
    q = int(body)
    for p in range(2, q + 1):
        if q % p == 0:
            k, t = 0, q
            while t % p == 0:
                t //= p
                k += 1
            assert t == 1, "q must be a prime power: %s" % name
            return ExtField(p, k) if k > 1 else PrimeField(p)
    raise ValueError(name)


def label(F):
    """The name of the field as the hypothesis writes it: GF(q) with q = p^k."""
    return "GF(%d)" % (F.char ** F.degree)


def field_record(F):
    return {"name": label(F), "uhlib_name": F.name, "char": F.char, "degree": F.degree,
            "modulus": list(getattr(F, "modulus", [])) or None}


def _vec(F, c):
    """Field element as a tuple of k residues."""
    return (int(c),) if F.degree == 1 else tuple(int(x) for x in c)


class Ctx:
    """One field: p, k and the k x k matrices of the multiplication by a^i over GF(p)."""

    def __init__(self, F):
        self.F = F
        self.p, self.k = F.char, F.degree
        self.P = []
        for i in range(self.k):
            ai = tuple(1 if t == i else 0 for t in range(self.k)) if self.k > 1 else (1,)
            cols = []
            for j in range(self.k):
                aj = tuple(1 if t == j else 0 for t in range(self.k))
                cols.append(_vec(F, F.mul(ai, aj)) if self.k > 1 else (1,))
            # P_i[j', j] = coefficient of a^j' in a^i * a^j
            self.P.append(np.array([[cols[j][jp] for j in range(self.k)] for jp in range(self.k)], dtype=np.int64))


_CTX = {}


def ctx_of(F):
    c = _CTX.get(F.name)
    if c is None:
        c = _CTX[F.name] = Ctx(F)
    return c


# ------------------------------------------------------------------ exact rank
def rank_mod_p(M, p):
    """Rank of an integer matrix modulo the prime p (row echelon form, numpy int64)."""
    M = np.array(M, dtype=np.int64) % p
    m, n = M.shape
    r = 0
    for j in range(n):
        if r >= m:
            break
        nz = np.nonzero(M[r:, j])[0]
        if nz.size == 0:
            continue
        piv = r + int(nz[0])
        if piv != r:
            M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, j]), -1, p)
        M[r, j:] = (M[r, j:] * inv) % p
        below = r + 1 + np.nonzero(M[r + 1:, j])[0]
        if below.size:
            f = M[below, j]
            M[below, j:] = (M[below, j:] - f[:, None] * M[r, j:][None, :]) % p
        r += 1
    return r


def rank_field(ctx, E):
    """Rank over GF(p^k) of the matrix with entries E[row, col, :] (k residues each)."""
    rows, cols, k = E.shape
    if k == 1:
        return rank_mod_p(E[:, :, 0], ctx.p)
    blocks = []
    for i in range(k):
        # a^i * v: new[row, col, jp] = sum_j P_i[jp, j] E[row, col, j]
        blocks.append(np.tensordot(E, ctx.P[i], axes=([2], [1])) % ctx.p)
    big = np.stack(blocks, axis=1).reshape(rows * k, cols * k)  # row (r, i), column (col, jp)
    rk = rank_mod_p(big, ctx.p)
    assert rk % k == 0, "GF(p)-rank is not a multiple of k: the expansion is wrong"
    return rk // k


# ------------------------------------------------------------------ the structure constants and mu_n(W)
@lru_cache(maxsize=None)
def struct_tensor(p, e, n):
    """T[u, m, c] = coefficient of the PBW monomial c in (monomial u of degree n-e) * (monomial m of degree e), mod p."""
    mu, me, mn = A.monos(n - e), A.monos(e), A.monos(n)
    pos = {m: i for i, m in enumerate(mn)}
    T = np.zeros((len(mu), len(me), len(mn)), dtype=np.int64)
    for iu, a in enumerate(mu):
        for im, b in enumerate(me):
            for mm, kk in A.mono_mul(a, b):
                T[iu, im, pos[mm]] += kk % p
    return T % p


def mu_matrix(ctx, C, e, n):
    """E[(w, u), col, j] for the rows u * w_t (w_t the two basis forms, C[t, m, :] their coefficients), left multiples."""
    T = struct_tensor(ctx.p, e, n)
    out = np.tensordot(C, T, axes=([1], [1]))  # (t, j, u, c)
    out = np.transpose(out, (0, 2, 3, 1)) % ctx.p  # (t, u, c, j)
    return out.reshape(C.shape[0] * T.shape[0], T.shape[2], ctx.k)


def rank_mu(ctx, C, e, n):
    """rank mu_n(W) (n >= e)."""
    return rank_field(ctx, mu_matrix(ctx, C, e, n))


def hilbert_pair(ctx, C, e, D):
    """[H_W(0), ..., H_W(D)] of M_W = U/(U W), W given by the coefficient array C (2, u(e), k)."""
    return [u(n) - (rank_mu(ctx, C, e, n) if n >= e else 0) for n in range(D + 1)]


# ------------------------------------------------------------------ spaces: arrays, bases, seeds
def coeff_array(F, rows):
    """Array (len(rows), u(e), k) from rows of field elements on the monomial basis of U_e."""
    k = F.degree
    return np.array([[_vec(F, c) for c in row] for row in rows], dtype=np.int64).reshape(len(rows), len(rows[0]), k)


def draw_space(F, e, seed):
    """Uniformly random 2 x u(e) matrix over F from random.Random(seed), redrawn (same generator) until its rank is 2.

    Draw order: row 0 then row 1, monomials in A.monos(e) order, one F.random(rng) each."""
    rng = random.Random(seed)
    ctx = ctx_of(F)
    n = u(e)
    while True:
        rows = [[F.random(rng) for _ in range(n)] for _ in range(2)]
        C = coeff_array(F, rows)
        if rank_field(ctx, C) == 2:
            return C


def basis_json(F, C, e):
    """Basis of W as [[ [i, j, k], coefficient ], ...] for each of the two forms (nonzero terms, PBW monomials)."""
    out = []
    for t in range(C.shape[0]):
        poly = []
        for im, m in enumerate(A.monos(e)):
            c = tuple(int(x) for x in C[t, im])
            if any(c):
                poly.append([list(m), c[0] if F.degree == 1 else list(c)])
        out.append(poly)
    return out


def basis_from_json(F, js, e):
    """Inverse of basis_json: the coefficient array of the two forms."""
    pos = {m: i for i, m in enumerate(A.monos(e))}
    C = np.zeros((len(js), u(e), F.degree), dtype=np.int64)
    for t, poly in enumerate(js):
        for m, c in poly:
            C[t, pos[tuple(m)]] = [c] if F.degree == 1 else c
    return C


def polys_of(F, C, e):
    """The two forms as uhlib polynomials {(i, j, k): field element}."""
    pos = list(A.monos(e))
    out = []
    for t in range(C.shape[0]):
        p = {}
        for im, m in enumerate(pos):
            c = tuple(int(x) for x in C[t, im])
            if any(c):
                p[m] = c[0] if F.degree == 1 else c
        out.append(p)
    return out


def poly_text(F, poly_json, signed=True):
    """Readable form of a stored form: terms c*x^i*y^j*z^k, PBW order (x before y before z), highest degree first."""
    p = F.char
    terms = []
    for m, c in sorted(poly_json, key=lambda t: (-A.deg(tuple(t[0])), tuple(t[0]))):
        i, j, k = m
        mon = "*".join(v + ("^%d" % d if d > 1 else "") for v, d in (("x", i), ("y", j), ("z", k)) if d)
        if F.degree == 1:
            cc = int(c)
            if signed and cc > p // 2:
                cc -= p
            ctext = str(cc)
        else:
            ctext = "(" + "+".join(("%d*a" % v if v > 1 else "a") + ("^%d" % t if t > 1 else "") if t else "%d" % v
                                   for t, v in enumerate(c) if v) + ")"
        if ctext == "1" and mon:
            terms.append(mon)
        elif ctext == "-1" and mon:
            terms.append("-" + mon)
        else:
            terms.append(ctext + ("*" + mon if mon else ""))
    return " + ".join(terms).replace("+ -", "- ") if terms else "0"


# ------------------------------------------------------------------ enumeration of all two-dimensional subspaces
def enumerate_subspaces(F, e):
    """Every 2-dimensional subspace of U_e once, as the coefficient array of its reduced row echelon basis (uhlib's order)."""
    for rows in S.rref_subspaces(F, u(e), 2):
        yield coeff_array(F, rows)


@lru_cache(maxsize=4)
def enumerated(fname, e):
    F = make_field(fname)
    return list(enumerate_subspaces(F, e))


# ------------------------------------------------------------------ the module and its Betti table through uhlib
def module_of(F, C, e, maxdeg=None):
    maxdeg = maxdeg if maxdeg is not None else 4 * e + 8
    rels = polys_as_relations(F, C, e)
    shifts = [0]
    if isinstance(F, PrimeField) and F.p < 2 ** 31:
        return quotient_module_np(F, shifts, rels, maxdeg=maxdeg)
    return quotient_module(F, shifts, rels, maxdeg=maxdeg)


def betti_table(F, C, e):
    """(dict {(i, j): rank} or None when the module is not finite within the bound, Hilbert list of the module)."""
    M = module_of(F, C, e)
    hl = list(M.dims) + [0] * (4 * e + 9 - len(M.dims))
    return (tor.betti(M) if M.finished else None), hl


def table_rows(t):
    return None if t is None else [[i, j, r] for (i, j), r in sorted(t.items())]


# ------------------------------------------------------------------ evaluation of one space
def evaluate(F, C, e, mode):
    """Everything the experiment computes for one space.

    mode 'A' (families A and C): rank mu_3e first; the Hilbert function (degrees 0..4e+2) and the Betti table only
    when rank mu_3e equals the value of h_e.  mode 'B' (family B, e = 4): the same, but the Hilbert function is
    computed for every space with rank mu_3e at most the value of h_e (at most 48 for e = 4).
    Returns a dict: rank3e, pure_hilbert (bool), hilbert (list or None), betti (rows or None), pure (bool)."""
    ctx = ctx_of(F)
    r3 = rank_mu(ctx, C, e, 3 * e)
    tgt = target_rank(e)
    rec = {"rank3e": r3, "hilbert": None, "pure_hilbert": False, "betti": None, "pure": False}
    if (mode == "A" and r3 != tgt) or (mode == "B" and r3 > tgt):
        return rec
    D = hilbert_bound(e)
    hf = hilbert_pair(ctx, C, e, D)
    rec["hilbert"] = hf
    rec["pure_hilbert"] = hf == [h_e(e, n) for n in range(D + 1)]
    if rec["pure_hilbert"]:
        t, _ = betti_table(F, C, e)
        rec["betti"] = table_rows(t)
        rec["pure"] = t == pure_table(e)
    return rec


# ------------------------------------------------------------------ the orbit test (family B2)
def _linear_power(K, a, b, e):
    """(a x + b y)^e in U (noncommutative product), as a uhlib polynomial over K."""
    ell = {}
    if not K.is_zero(a):
        ell[(1, 0, 0)] = a
    if not K.is_zero(b):
        ell[(0, 1, 0)] = b
    r = {(0, 0, 0): K.one}
    for _ in range(e):
        r = A.poly_mul(K, r, ell)
    return r


def projective_points(K):
    """Representatives (a, b) of the projective line over K: (1, b) for every b, then (0, 1)."""
    els = S.field_elements(K)
    return [(K.one, b) for b in els] + [(K.zero, K.one)]


_ORBIT_CACHE = {}


def _orbit_data(p, e):
    """The quadratic extension K = GF(p^2), the points of P^1(K) and the vectors (a x + b y)^e on the basis of U_e."""
    key = (p, e)
    if key not in _ORBIT_CACHE:
        K = make_field("GF(%d)" % (p * p))
        ctx = ctx_of(K)
        pts = projective_points(K)
        mon = list(A.monos(e))
        vecs = []
        for a, b in pts:
            pw = _linear_power(K, a, b, e)
            vecs.append(np.array([_vec(K, pw.get(m, K.zero)) for m in mon], dtype=np.int64))
        rational = [all(x[1] == 0 for x in (a, b)) for a, b in pts]
        _ORBIT_CACHE[key] = (K, ctx, pts, vecs, rational)
    return _ORBIT_CACHE[key]


def orbit_test(F, C, e):
    """Whether W (over the prime field F = GF(p), basis array C) lies in the orbit of <x^e, y^e> under GL_2.

    W is in the orbit when it contains the e-th powers of two distinct linear forms a x + b y.  Every point of the
    projective line over GF(p^2) is tested (the points over GF(p) are among them: second coordinate 0 in the extension
    encoding), which covers a pair of points of GF(p) and a conjugate pair over GF(p^2): (a x + b y)^e is in W tensor K
    iff the rank of [f; g; (a x + b y)^e] over K is 2.  Returns {points, rational_points, in_orbit, kind}."""
    assert F.degree == 1
    K, ctx, pts, vecs, rational = _orbit_data(F.p, e)
    base = np.zeros((2, C.shape[1], 2), dtype=np.int64)
    base[:, :, 0] = C[:, :, 0]  # W embedded in K: coefficient c -> (c, 0)
    found = []
    for idx, v in enumerate(vecs):
        E = np.concatenate([base, v[None, :, :]], axis=0)
        if rank_field(ctx, E) == 2:
            found.append(idx)
    n_rat = sum(1 for i in found if rational[i])
    n_irr = len(found) - n_rat
    in_orbit = len(found) >= 2
    kind = "none"
    if in_orbit:
        kind = "two rational points" if n_irr == 0 and n_rat == 2 else (
            "conjugate pair" if n_rat == 0 and n_irr == 2 else "other (%d rational, %d irrational)" % (n_rat, n_irr))
    elif found:
        kind = "one point only"
    return {"points": len(found), "rational_points": n_rat, "irrational_points": n_irr, "in_orbit": in_orbit,
            "kind": kind}


def orbit_space(F, e, ell1, ell2):
    """Coefficient array of <l1^e, l2^e> over the prime field F for two linear forms l = (a, b) = a x + b y over F."""
    assert F.degree == 1
    rows = []
    for a, b in (ell1, ell2):
        f = _linear_power(F, a, b, e)
        rows.append([f.get(m, 0) for m in A.monos(e)])
    return coeff_array(F, rows)


def conjugate_space(p, e, a, b):
    """<l^e, conj(l)^e> as a space over GF(p), for l = a x + b y with a, b in GF(p^2) (tuples) and l not proportional to a
    form over GF(p): the span of the two conjugate powers over GF(p^2) is spanned by the components of l^e on 1 and a."""
    K = make_field("GF(%d)" % (p * p))
    pw = _linear_power(K, a, b, e)
    mon = list(A.monos(e))
    re = [pw.get(m, K.zero)[0] for m in mon]
    im = [pw.get(m, K.zero)[1] for m in mon]
    return coeff_array(PrimeField(p), [re, im])


def polys_as_relations(F, C, e):
    """The two forms as relations {(0, mono): coefficient} of a one-generator presentation (uhlib's input)."""
    return [{(0, m): c for m, c in p.items()} for p in polys_of(F, C, e)]


# ------------------------------------------------------------------ the families and the worker
# family: (e, fields, kind, number of spaces, mode of `evaluate`, orbit test of the pure spaces)
FAMILIES = {
    "A1": (3, ("GF(3)",), "enum", 11011, "A", False),
    "A2": (3, ("GF(5)", "GF(9)", "GF(25)", "GF(27)"), "random", 2000, "A", False),
    "B1": (4, ("GF(3)", "GF(5)", "GF(7)"), "random", 20000, "B", False),
    "B2": (4, ("GF(11)", "GF(13)"), "random", 20000, "B", True),
    "B3": (4, ("GF(9)",), "random", 20000, "B", False),
    "C": (5, ("GF(3)",), "random", 50000, "A", False),
}
CHUNK = 250


def chunk_id(family, field, start, end):
    return "%s|%s|%05d-%05d" % (family, field, start, end)


def chunk_specs(only=None):
    """Every chunk of the hypothesis: contiguous index ranges of CHUNK spaces of a (family, field)."""
    out = []
    for fam, (e, fields, kind, n, mode, orbit) in FAMILIES.items():
        if only and fam not in only:
            continue
        for fname in fields:
            for s in range(0, n, CHUNK):
                t = min(s + CHUNK, n)
                out.append({"id": chunk_id(fam, fname, s, t), "family": fam, "field": fname, "e": e, "kind": kind,
                            "mode": mode, "orbit": orbit, "start": s, "end": t})
    return out


def run_chunk(spec):
    """Evaluate the spaces start..end-1 of a (family, field); returns the aggregate and the stored spaces."""
    import time
    t0 = time.time()
    F = make_field(spec["field"])
    e, mode = spec["e"], spec["mode"]
    tgt = target_rank(e)
    agg = {"id": spec["id"], "family": spec["family"], "field": spec["field"], "e": e, "start": spec["start"],
           "end": spec["end"], "n": 0, "rank_hist": {}, "hilbert_computed": 0, "hilbert_other": {}, "pure_hilbert": 0,
           "pure": 0, "nonpure_tables": {}, "spaces": []}
    pool = enumerated(spec["field"], e) if spec["kind"] == "enum" else None
    for idx in range(spec["start"], spec["end"]):
        seed = None if pool is not None else SEED_BASE + idx
        C = pool[idx] if pool is not None else draw_space(F, e, seed)
        ev = evaluate(F, C, e, mode)
        agg["n"] += 1
        agg["rank_hist"][str(ev["rank3e"])] = agg["rank_hist"].get(str(ev["rank3e"]), 0) + 1
        if ev["hilbert"] is not None:
            agg["hilbert_computed"] += 1
            if not ev["pure_hilbert"]:
                key = ",".join(str(x) for x in ev["hilbert"])
                agg["hilbert_other"][key] = agg["hilbert_other"].get(key, 0) + 1
        agg["pure_hilbert"] += ev["pure_hilbert"]
        agg["pure"] += ev["pure"]
        if ev["pure_hilbert"] and not ev["pure"]:
            key = str(ev["betti"])
            agg["nonpure_tables"][key] = agg["nonpure_tables"].get(key, 0) + 1
        keep = ev["pure_hilbert"] if mode == "A" else ev["rank3e"] <= tgt
        if keep:
            rec = {"index": idx, "seed": seed, "rank3e": ev["rank3e"], "hilbert": ev["hilbert"],
                   "pure_hilbert": ev["pure_hilbert"], "pure": ev["pure"], "betti": ev["betti"],
                   "basis": basis_json(F, C, e)}
            if spec["orbit"] and ev["pure"]:
                rec["orbit"] = orbit_test(F, C, e)
            agg["spaces"].append(rec)
    agg["seconds"] = round(time.time() - t0, 2)
    return agg
