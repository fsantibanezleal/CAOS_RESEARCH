"""EXP-007 routine: the tangent space of the rank locus D_e at W_0 = <x^e, y^e>, ranks of mu_n(W) over the rationals and
over prime fields, the Betti table through `uhlib`, the orbit test, the families of the hypothesis and their seeded draws.

First instrument of EXP-007.  Every product goes through `uhlib` (`A.mono_mul`, `A.poly_mul`: the noncommutative product
of U(H), y x = x y - z) and is a LEFT multiplication: the rows of mu_n(W) are u * w for u a PBW monomial of degree n - e
and w in the basis of W.  Linear algebra is exact: python-flint `fmpz_mat` over the rationals (a rank over the rationals is
never a rank modulo a prime; rows with fractional entries are scaled to integers, which keeps rank and kernels) and
`nmod_mat` over a prime field.  No floating point.
"""
import random
import sys
from fractions import Fraction
from functools import lru_cache
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
SIBLING = HERE.parent / "EXP-006-odd-characteristic-below-2e"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))
if str(SIBLING) not in sys.path:
    sys.path.append(str(SIBLING))  # appended: EXP-006 has its own run.py and make_summary.py, which must not shadow this folder's

from flint import fmpz_mat, nmod_mat  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import tor  # noqa: E402
from uhlib.fastmod import quotient_module_np  # noqa: E402
from uhlib.fields import QQ, PrimeField  # noqa: E402
from uhlib.module import quotient_module  # noqa: E402

import exp006_routine as R6  # noqa: E402  (u, h_e, pure_table, target_rank and rank_mod_p, proven by the tests of EXP-006)

SEED_BASE = 20261120
u = R6.u
h_e = R6.h_e
pure_table = R6.pure_table
target_rank = R6.target_rank  # r = u(3e) - h_e(3e) = 2 u(2e) - 2


def hilbert_bound(e):
    return 4 * e + 2


def make_field(name):
    """'QQ' or 'GF(p)' for a prime p."""
    if name == "QQ":
        return QQ()
    assert name.startswith("GF(") and name.endswith(")"), name
    return PrimeField(int(name[3:-1]))


def fname(F):
    return "QQ" if F.char == 0 else "GF(%d)" % F.p


# ------------------------------------------------------------------ matrices
def to_matrix(F, rows, ncols):
    """Exact flint matrix of dense rows (Fractions over QQ, residues over GF(p)).  Over QQ each row is scaled by the lcm of its
    denominators (rank, row space and right kernel unchanged)."""
    if F.char == 0:
        flat = []
        for row in rows:
            den = lcm(*(Fraction(x).denominator for x in row)) if row else 1
            flat.extend(int(Fraction(x) * den) for x in row)
        return fmpz_mat(len(rows), ncols, flat)
    return nmod_mat(len(rows), ncols, [int(x) % F.p for row in rows for x in row], F.p)


def zero_matrix(F, nrows, ncols):
    return fmpz_mat(nrows, ncols, [0] * (nrows * ncols)) if F.char == 0 else nmod_mat(nrows, ncols, [0] * (nrows * ncols), F.p)


def mat_rank(M):
    return int(M.rank())


def entries_int(M):
    """Entries of a flint matrix as python ints (residues in [0, p) over GF(p))."""
    return [int(x) for x in M.entries()]


def kernel_columns(M):
    """Matrix whose columns are a basis of the right kernel of M, and its dimension (python-flint pads with zero columns)."""
    X, nul = M.nullspace()
    nul = int(nul)
    rows = [[int(X[i, j]) for j in range(nul)] for i in range(X.nrows())]
    return rows, nul


# ------------------------------------------------------------------ the product: sparse structure of left multiplication
@lru_cache(maxsize=None)
def prod_table(e, n):
    """[(iu, im, ((ic, k), ...))]: u_iu * m_im = sum k * (monomial ic), u of degree n - e, m of degree e, PBW (uhlib's mono_mul)."""
    mu, me, mn = A.monos(n - e), A.monos(e), A.monos(n)
    pos = {m: i for i, m in enumerate(mn)}
    out = []
    for iu, a in enumerate(mu):
        for im, b in enumerate(me):
            out.append((iu, im, tuple((pos[mm], kk) for mm, kk in A.mono_mul(a, b))))
    return tuple(out)


def mu_rows(F, C, e, n):
    """Dense rows (t, u) -> coordinates of u * w_t on the PBW monomials of degree n, C[t][im] the coefficient of the monomial im of
    U_e in w_t (Fractions over QQ, residues over GF(p)).  Row index t * u(n - e) + iu."""
    nu, nc = u(n - e), u(n)
    rows = [[0] * nc for _ in range(len(C) * nu)]
    tab = prod_table(e, n)
    for t, w in enumerate(C):
        for iu, im, terms in tab:
            c = w[im]
            if c == 0:
                continue
            row = rows[t * nu + iu]
            for ic, k in terms:
                row[ic] += c * k
    if F.char:
        rows = [[x % F.p for x in r] for r in rows]
    return rows


def mu_matrix(F, C, e, n):
    return to_matrix(F, mu_rows(F, C, e, n), u(n))


def rank_mu(F, C, e, n):
    return mat_rank(mu_matrix(F, C, e, n))


def hilbert_list(F, C, e, D):
    """[H_W(0), ..., H_W(D)] of M_W = U / (U W): u(n) - rank mu_n(W) for n >= e, u(n) below."""
    return [u(n) - (rank_mu(F, C, e, n) if n >= e else 0) for n in range(D + 1)]


# ------------------------------------------------------------------ spaces
def space_from_polys(F, e, polys):
    """Coefficient rows (on A.monos(e)) of forms given as {(i, j, k): integer or Fraction}; every monomial is a PBW monomial."""
    pos = {m: i for i, m in enumerate(A.monos(e))}
    rows = []
    for p in polys:
        row = [F.zero] * u(e)
        for m, c in p.items():
            assert A.deg(m) == e, (m, e)
            row[pos[m]] = F.from_int(c) if isinstance(c, int) else F.mul(F.from_int(Fraction(c).numerator), F.inv(F.from_int(Fraction(c).denominator)))
        rows.append(row)
    return rows


def coef_json(F, c):
    return str(Fraction(c)) if F.char == 0 else int(c)


def coef_from_json(F, c):
    return Fraction(c) if F.char == 0 else int(c)


def basis_json(F, C, e):
    """Each form as [[[i, j, k], coefficient], ...] (nonzero terms); the coefficient is "n/d" over QQ, an integer in [0, p) mod p."""
    mon = A.monos(e)
    return [[[list(m), coef_json(F, w[im])] for im, m in enumerate(mon) if w[im] != 0] for w in C]


def basis_from_json(F, js, e):
    pos = {m: i for i, m in enumerate(A.monos(e))}
    C = []
    for poly in js:
        row = [F.zero] * u(e)
        for m, c in poly:
            row[pos[tuple(m)]] = coef_from_json(F, c)
        C.append(row)
    return C


def coef_lists(F, C):
    """Coefficient lists of the forms on A.monos(e) (strings over QQ, integers modulo p)."""
    return [[coef_json(F, c) for c in w] for w in C]


def poly_text(F, poly_json):
    """Readable form: terms c*x^i*y^j*z^k in PBW order, highest degree first; coefficients over GF(p) read as symmetric residues."""
    terms = []
    for m, c in sorted(poly_json, key=lambda t: (-A.deg(tuple(t[0])), tuple(t[0]))):
        i, j, k = m
        mon = "*".join(v + ("^%d" % d if d > 1 else "") for v, d in (("x", i), ("y", j), ("z", k)) if d)
        if F.char == 0:
            cc = Fraction(c)
            ctext = str(cc)
        else:
            cc = int(c)
            if cc > F.p // 2:
                cc -= F.p
            ctext = str(cc)
        if ctext == "1" and mon:
            terms.append(mon)
        elif ctext == "-1" and mon:
            terms.append("-" + mon)
        else:
            terms.append(ctext + ("*" + mon if mon else ""))
    return " + ".join(terms).replace("+ -", "- ") if terms else "0"


def relations_of(F, C, e):
    return [{(0, m): w[im] for im, m in enumerate(A.monos(e)) if w[im] != 0} for w in C]


def betti_table(F, C, e):
    """(Betti table {(i, j): rank} or None when the module is not finite within the bound, module Hilbert list to 4e + 8)."""
    maxdeg = 4 * e + 8
    rels = relations_of(F, C, e)
    if F.char and F.p < 2 ** 31:
        M = quotient_module_np(F, [0], rels, maxdeg=maxdeg)
    else:
        M = quotient_module(F, [0], rels, maxdeg=maxdeg)
    hl = list(M.dims) + [0] * (maxdeg + 1 - len(M.dims))
    return (tor.betti(M) if M.finished else None), hl


def table_rows(t):
    return None if t is None else [[i, j, r] for (i, j), r in sorted(t.items())]


# ------------------------------------------------------------------ the orbit test
def linear_power(F, a, b, e):
    """(a x + b y)^e in U (noncommutative product through uhlib), as a uhlib polynomial over F."""
    ell = {}
    if not F.is_zero(a):
        ell[(1, 0, 0)] = a
    if not F.is_zero(b):
        ell[(0, 1, 0)] = b
    r = {(0, 0, 0): F.one}
    for _ in range(e):
        r = A.poly_mul(F, r, ell)
    return r


def poly_row(F, p, e):
    return [p.get(m, F.zero) for m in A.monos(e)]


def orbit_test(F, C, e):
    """S_e = span of (x + t y)^e, t = 0, 1, ..., e, together with y^e (dimension e + 1 in characteristic 0 or larger than e).
    W is outside the orbit of <x^e, y^e> when dim(S_e + W) > e + 1.  Returns both dimensions."""
    one, zero = F.one, F.zero
    rows = [poly_row(F, linear_power(F, one, F.from_int(t), e), e) for t in range(e + 1)]
    rows.append(poly_row(F, linear_power(F, zero, one, e), e))
    dim_s = mat_rank(to_matrix(F, rows, u(e)))
    dim_sw = mat_rank(to_matrix(F, rows + [list(w) for w in C], u(e)))
    return {"dim_S": dim_s, "dim_S_plus_W": dim_sw, "S_has_dim_e_plus_1": dim_s == e + 1, "outside_orbit": dim_sw > e + 1}


# ------------------------------------------------------------------ the tangent space of a determinantal locus
def tangent_dimension(F, A_mat, Bs):
    """Tangent space at a point A_mat of the locus rank <= rank(A_mat), in the chart whose coordinate c has the direction Bs[c]
    (a matrix of the shape of A_mat).  Let K be a basis of the left kernel of A_mat (k A = 0) and Lam a basis of the right
    kernel (the linear forms vanishing on the row space of A_mat).  T(c) = (k Bs[c] lam) over every k and lam; the tangent space
    is ker T, of dimension len(Bs) - rank T.  Returns the ranks and dimensions and the rows of T."""
    nr, nc = A_mat.nrows(), A_mat.ncols()
    rank_a = mat_rank(A_mat)
    Kcols, dim_k = kernel_columns(A_mat.transpose())  # columns k with A^T k = 0: left kernel
    Lcols, dim_l = kernel_columns(A_mat)  # columns lam with A lam = 0
    KT = to_mat_raw(F, [[Kcols[i][j] for i in range(nr)] for j in range(dim_k)], nr)
    Lam = to_mat_raw(F, Lcols, dim_l)
    Trows = []
    for B in Bs:
        prod = KT * B * Lam  # dim_k x dim_l
        Trows.append([int(prod[i, j]) for i in range(dim_k) for j in range(dim_l)])
    rank_t = mat_rank(to_mat_raw(F, Trows, dim_k * dim_l)) if dim_k * dim_l else 0
    return {"rows_A": nr, "cols_A": nc, "rank_A": rank_a, "dim_K": dim_k, "coker_dim": dim_l, "coordinates": len(Bs),
            "rank_T": rank_t, "tangent_dim": len(Bs) - rank_t, "T": Trows}


def to_mat_raw(F, rows, ncols):
    """Matrix of integer rows as they are (no scaling); over GF(p) the entries are reduced."""
    if F.char == 0:
        return fmpz_mat(len(rows), ncols, [int(x) for r in rows for x in r])
    return nmod_mat(len(rows), ncols, [int(x) % F.p for r in rows for x in r], F.p)


def chart_coordinates(e):
    """Pairs (i, m): i in {0, 1} the generator (0 for x^e + f, 1 for y^e + g), m a PBW monomial of degree e other than x^e, y^e."""
    return [(i, m) for i in (0, 1) for m in A.monos(e) if m not in ((e, 0, 0), (0, e, 0))]


def chart_matrix(F, e, i, m):
    """B(i, m): the rows of the block of generator i are the coordinates of u * m (u over the PBW monomials of degree 2e), zero
    elsewhere (the shape of mu_3e)."""
    nu, nc = u(2 * e), u(3 * e)
    mi = A.monos(e).index(m)
    flat = [0] * (2 * nu * nc)
    for iu, im, terms in prod_table(e, 3 * e):
        if im == mi:
            for ic, k in terms:
                flat[(i * nu + iu) * nc + ic] += k
    if F.char:
        flat = [x % F.p for x in flat]
    return fmpz_mat(2 * nu, nc, flat) if F.char == 0 else nmod_mat(2 * nu, nc, flat, F.p)


def power_pair_basis(F, e):
    return [[F.one if m == (e, 0, 0) else F.zero for m in A.monos(e)], [F.one if m == (0, e, 0) else F.zero for m in A.monos(e)]]


def orbit_directions(e):
    """The derivatives at t = 0 of (x + t y)^e and of (y + t x)^e as integer polynomials: sum_i x^i y x^(e-1-i) and its mirror,
    products taken in U through uhlib."""
    out = []
    for first, second in ((A.X, A.Y), (A.Y, A.X)):
        tot = {}
        for i in range(e):
            term = A.ONE
            for fac in [first] * i + [second] + [first] * (e - 1 - i):
                term = A.poly_mul_int(term, fac)
            tot = A.padd(tot, term)
        out.append(tot)
    return out


def tangent_at_power_pair(F, e):
    """The tangent map of D_e at W_0 = <x^e, y^e>: ranks, dim K, the cokernel dimension, rank T, the tangent dimension and whether
    the two orbit directions lie in the tangent space (and are independent)."""
    C0 = power_pair_basis(F, e)
    coords = chart_coordinates(e)
    A_mat = mu_matrix(F, C0, e, 3 * e)
    Bs = [chart_matrix(F, e, i, m) for i, m in coords]
    d = tangent_dimension(F, A_mat, Bs)
    T = d.pop("T")
    dirs = orbit_directions(e)
    vecs = []
    for gen, poly in enumerate(dirs):
        assert (e, 0, 0) not in poly and (0, e, 0) not in poly
        vec = [0] * len(coords)
        for c, (i, m) in enumerate(coords):
            if i == gen:
                vec[c] = poly.get(m, 0)
        assert sum(1 for x in vec if x) == len(poly), "orbit direction has a monomial outside the chart"
        vecs.append(vec)
    p = F.p if F.char else None
    images = []
    for vec in vecs:
        img = [sum(vec[c] * T[c][j] for c in range(len(coords))) for j in range(len(T[0]) if T else 0)]
        images.append([x % p for x in img] if p else img)
    d["orbit_directions_in_tangent_space"] = all(not any(img) for img in images)
    d["orbit_directions_rank"] = mat_rank(to_mat_raw(F, [[x % p if p else x for x in v] for v in vecs], len(coords)))
    d["target_rank_r"] = target_rank(e)
    d["coker_expected_h_e_3e"] = h_e(e, 3 * e)
    d["tangent_bound_4e_minus_4"] = 4 * e - 4
    d["chart_coordinates"] = len(coords)
    return d


# ------------------------------------------------------------------ the routine of G2: all matrices as the chart
def tangent_all_matrices(F, A_rows, ncols):
    """The same tangent routine with the chart replaced by the whole space of matrices (Bs the unit matrices)."""
    A_mat = to_mat_raw(F, A_rows, ncols)
    nr = len(A_rows)
    Bs = []
    for i in range(nr):
        for j in range(ncols):
            flat = [0] * (nr * ncols)
            flat[i * ncols + j] = 1
            Bs.append(to_mat_raw(F, [flat[r * ncols:(r + 1) * ncols] for r in range(nr)], ncols))
    d = tangent_dimension(F, A_mat, Bs)
    d.pop("T")
    return d


def random_rank_matrix(F, nr, nc, rank, seed):
    """nr x nc matrix of the given rank (product of random small-integer factors), redrawn until the rank is exact."""
    rng = random.Random(seed)
    while True:
        P = [[rng.randint(-5, 5) for _ in range(rank)] for _ in range(nr)]
        Q = [[rng.randint(-5, 5) for _ in range(nc)] for _ in range(rank)]
        rows = [[sum(P[i][k] * Q[k][j] for k in range(rank)) for j in range(nc)] for i in range(nr)]
        if mat_rank(to_mat_raw(F, rows, nc)) == rank:
            return rows


# ------------------------------------------------------------------ evaluation of a space
def evaluate_space(F, C, e, hilbert_to=None, with_betti=True):
    """rank mu_3e, the Hilbert function (degrees 0..hilbert_to, default 4e + 2), the Betti table through uhlib and the orbit test."""
    D = hilbert_to if hilbert_to is not None else hilbert_bound(e)
    r3 = rank_mu(F, C, e, 3 * e)
    rec = {"rank_mu_3e": r3, "target_rank_r": target_rank(e), "hilbert": hilbert_list(F, C, e, D), "hilbert_to": D}
    rec["pure_hilbert"] = rec["hilbert"][: hilbert_bound(e) + 1] == [h_e(e, n) for n in range(hilbert_bound(e) + 1)]
    rec["betti"], rec["pure"], rec["hilbert_module"] = None, False, None
    if with_betti:
        t, hl = betti_table(F, C, e)
        rec["betti"] = table_rows(t)
        rec["pure"] = t == pure_table(e)
        rec["finite_length"] = t is not None
        rec["hilbert_module"] = hl
    rec["orbit"] = orbit_test(F, C, e)
    return rec


# ------------------------------------------------------------------ the named spaces of T3
def named_spaces():
    """name -> (e, [f, g]) with f, g integer PBW polynomials {(i, j, k): coefficient}."""
    return {
        "W0_e4": (4, [{(4, 0, 0): 1}, {(0, 4, 0): 1}]),
        "W0_e5": (5, [{(5, 0, 0): 1}, {(0, 5, 0): 1}]),
        "P1": (4, [{(4, 0, 0): 1, (1, 3, 0): 1}, {(0, 4, 0): 1}]),
        "P2": (4, [{(4, 0, 0): 1, (2, 2, 0): 31, (1, 1, 1): -8}, {(0, 4, 0): 1}]),
        "P3": (4, [{(4, 0, 0): 1, (2, 2, 0): 59, (0, 0, 2): -4}, {(0, 4, 0): 1}]),
        "P4": (4, [{(4, 0, 0): 1, (1, 3, 0): 2, (0, 2, 1): -3}, {(0, 4, 0): 1, (3, 1, 0): 5, (2, 0, 1): 7}]),
        "P5": (5, [{(5, 0, 0): 1, (1, 4, 0): 2, (0, 3, 1): -3}, {(0, 5, 0): 1, (4, 1, 0): 5, (3, 0, 1): 7}]),
        "C1": (4, [{(4, 0, 0): 1, (2, 2, 0): 1}, {(0, 4, 0): 1}]),
        "C2": (4, [{(4, 0, 0): 1, (1, 3, 0): 1}, {(0, 4, 0): 1, (3, 1, 0): 1}]),
    }


def family_L(e, a, b, c, d):
    """L_e(a, b, c, d) = <x^e + a x y^(e-1) + b y^(e-2) z, y^e + c x^(e-1) y + d x^(e-2) z>."""
    return [{(e, 0, 0): 1, (1, e - 1, 0): a, (0, e - 2, 1): b}, {(0, e, 0): 1, (e - 1, 1, 0): c, (e - 2, 0, 1): d}]


def family_plane(alpha, beta, gamma):
    """<x^4 + alpha x^2 y^2 + beta x y z + gamma z^2, y^4>."""
    return [{(4, 0, 0): 1, (2, 2, 0): alpha, (1, 1, 1): beta, (0, 0, 2): gamma}, {(0, 4, 0): 1}]


def nonzero_terms(p):
    return {m: c for m, c in p.items() if c}


def space_of(F, e, polys):
    return space_from_polys(F, e, [nonzero_terms(p) for p in polys])


# ------------------------------------------------------------------ seeded random draws
def draw_L_params(p, index):
    """(a, b, c, d) of the random member `index` of L_e over GF(p): random.Random(SEED_BASE + index), four randrange(p) in the
    order a, b, c, d (the same four residues for e = 4 and e = 5)."""
    rng = random.Random(SEED_BASE + index)
    return [rng.randrange(p) for _ in range(4)]


def draw_common_factor_space(F, e, d, index):
    """Two forms of U_e whose images in U/(z) = k[x, y] are q a and q b: q a form of degree d, a and b forms of degree e - d, all with
    coefficients random.Random(SEED_BASE + index).randrange(p), drawn in the order q (d + 1), a (e - d + 1), b (e - d + 1), each
    redrawn while it is zero; the commutative products q a and q b are read as PBW polynomials in x^i y^j, and to each form a random
    multiple of every PBW monomial containing z (k >= 1) is added, in the order of A.monos(e): first the form of a, then that of b.
    Returns (rows, (q, a, b) as coefficient lists of x^(deg - j) y^j)."""
    assert F.char and F.degree == 1
    p = F.p
    rng = random.Random(SEED_BASE + index)

    def form(deg):
        while True:
            c = [rng.randrange(p) for _ in range(deg + 1)]
            if any(c):
                return c

    q, a, b = form(d), form(e - d), form(e - d)

    def conv(f, g):
        out = [0] * (len(f) + len(g) - 1)
        for i, x in enumerate(f):
            for j, y in enumerate(g):
                out[i + j] = (out[i + j] + x * y) % p
        return out

    rows = []
    for prod in (conv(q, a), conv(q, b)):
        row = []
        for m in A.monos(e):
            if m[2] == 0:
                row.append(prod[m[1]] % p)  # x^i y^j has the coefficient of y^j
            else:
                row.append(rng.randrange(p))
        rows.append(row)
    return rows, (q, a, b)
