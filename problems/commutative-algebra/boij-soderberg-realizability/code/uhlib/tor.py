"""Graded Betti numbers of a finite length U(H)-module through the Tor complex.

beta_{i,j}(M) = dim Tor_i^U(k, M)_j, computed as the homology of K (x)_U M where K is the minimal free
resolution of the trivial RIGHT module k:

    0 -> U(-4) -> U(-3)^2 -> U(-1)^2 -> U -> k,     K_i = U(-s_i)^{r_i}, s = (0, 1, 3, 4).

Side convention: the K_i are free right modules; d(e_s) = sum_t f_t D[s][t] with the coefficients on the right.
Since d1(e_x) = x, d1(e_y) = y, the second differential comes from the two relations written LEFT-handed,
r_i = x a_i + y b_i (r1 = [x,[x,y]], r2 = [y,[x,y]]), and K (x) M has the maps  m -> (a m, b m)  (left
multiplication on M).  Composition rule: (D_n D_(n+1))[i][u] = sum_s D_n[s][u] * D_(n+1)[i][s].
"""
from fractions import Fraction
from functools import lru_cache

from . import algebra as A
from .fields import QQ
from .linalg import kernel, rank

SHIFTS = (0, 1, 3, 4)
RANKS = (1, 2, 2, 1)


def _mul(*ps):
    out = ps[0]
    for p in ps[1:]:
        out = A.poly_mul_int(out, p)
    return out


def _check_left_relation(a, b, r_zero=True):
    """x a + y b must be 0 in U(H)."""
    return A.padd(_mul(A.X, a), _mul(A.Y, b)) == {}


@lru_cache(maxsize=None)
def _third_map():
    """(c1, c2) in U_1^2 with a1 c1 + a2 c2 = 0 and b1 c1 + b2 c2 = 0 (unique up to scalar)."""
    a1, b1, a2, b2 = _second_map_entries()
    basis = [(0, (1, 0, 0)), (0, (0, 1, 0)), (1, (1, 0, 0)), (1, (0, 1, 0))]  # (which c, monomial)
    F = QQ()
    images = []
    target = [(w, m) for w in range(2) for m in A.monos(3)]
    for which, m in basis:
        cm = {m: 1}
        # equation e_x: a1 c1 + a2 c2 ; equation e_y: b1 c1 + b2 c2
        ex = _mul(a1 if which == 0 else a2, cm)
        ey = _mul(b1 if which == 0 else b2, cm)
        vec = [Fraction(0)] * len(target)
        for w, poly in ((0, ex), (1, ey)):
            for mm, c in poly.items():
                vec[target.index((w, mm))] += c
        images.append(vec)
    ker = kernel(F, images, len(target))
    assert len(ker) == 1, "the third differential must be unique up to scalar"
    v = ker[0]
    den = 1
    for c in v:
        den = den * Fraction(c).denominator // _gcd(den, Fraction(c).denominator)
    ints = [int(c * den) for c in v]
    g = 0
    for c in ints:
        g = _gcd(g, abs(c))
    ints = [c // g for c in ints]
    c1 = {m: c for (w, m), c in zip(basis, ints) if w == 0 and c}
    c2 = {m: c for (w, m), c in zip(basis, ints) if w == 1 and c}
    return c1, c2


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


@lru_cache(maxsize=None)
def _second_map_entries():
    x, y = A.X, A.Y
    # r1 = [x,[x,y]] = x^2 y - 2 x y x + y x^2 = x (x y - 2 y x) + y (x^2)
    a1 = A.padd(_mul(x, y), A.pscale(_mul(y, x), 2), -1)
    b1 = _mul(x, x)
    # r2 = [y,[x,y]] = y x y - y^2 x - x y^2 + y x y = x (-y^2) + y (2 x y - y x)
    a2 = A.pscale(_mul(y, y), -1)
    b2 = A.padd(A.pscale(_mul(x, y), 2), _mul(y, x), -1)
    assert _check_left_relation(a1, b1) and _check_left_relation(a2, b2), "r1, r2 must vanish in U(H)"
    return a1, b1, a2, b2


@lru_cache(maxsize=None)
def trivial_module_resolution():
    """The matrices D1 (2x1), D2 (2x2), D3 (1x2) of polynomial entries (integer coefficients)."""
    a1, b1, a2, b2 = _second_map_entries()
    c1, c2 = _third_map()
    return {
        "D1": [[A.X], [A.Y]],
        "D2": [[a1, b1], [a2, b2]],
        "D3": [[c1, c2]],
    }


def _compose(Dn, Dn1):
    """(Dn Dn1)[i][u] = sum_s Dn[s][u] * Dn1[i][s]."""
    out = []
    for row in Dn1:
        out_row = []
        for u in range(len(Dn[0])):
            acc = {}
            for s, e in enumerate(row):
                acc = A.padd(acc, _mul(Dn[s][u], e))
            out_row.append(acc)
        out.append(out_row)
    return out


def check_complex(K):
    """d1 d2 = 0 and d2 d3 = 0 as identities in U(H)."""
    z12 = _compose(K["D1"], K["D2"])
    z23 = _compose(K["D2"], K["D3"])
    return all(not p for row in z12 for p in row) and all(not p for row in z23 for p in row)


def check_exact(K, N):
    """K -> k is exact in degrees 0..N: rank counts of the degree-j strands of the maps against the dimensions."""
    F = QQ()
    Ds = [K["D1"], K["D2"], K["D3"]]
    for j in range(N + 1):
        ranks = []
        for n, D in enumerate(Ds, start=1):  # d_n : K_n -> K_(n-1)
            src_shift, tgt_shift = SHIFTS[n], SHIFTS[n - 1]
            tgt_basis = [(t, m) for t in range(RANKS[n - 1]) for m in A.monos(j - tgt_shift)] if j >= tgt_shift else []
            tidx = {b: i for i, b in enumerate(tgt_basis)}
            vecs = []
            if j >= src_shift:
                for s in range(RANKS[n]):
                    for u in A.monos(j - src_shift):
                        v = [F.zero] * len(tgt_basis)
                        for t in range(RANKS[n - 1]):
                            for mm, c in A.poly_mul_int(D[s][t], {u: 1}).items():
                                v[tidx[(t, mm)]] += c
                        vecs.append(v)
            ranks.append(rank(F, vecs, len(tgt_basis)))

        def dimK(i):
            return RANKS[i] * A.dim_U(j - SHIFTS[i])

        r1, r2, r3 = ranks
        if dimK(0) - r1 != (1 if j == 0 else 0):
            return False
        if dimK(1) - r1 - r2 != 0 or dimK(2) - r2 - r3 != 0 or dimK(3) - r3 != 0:
            return False
    return True


def betti(M):
    """Graded Betti numbers of a finite length module: dict {(i, j): rank}, i = 0..3."""
    F = M.F
    K = trivial_module_resolution()
    out = {}
    for j in range(M.lo, M.hi + 5):
        dC = [M.dim(j), 2 * M.dim(j - 1), 2 * M.dim(j - 3), M.dim(j - 4)]
        rk = [0, 0, 0, 0, 0]
        # d1: C_1 -> C_0 : (m_x, m_y) -> x m_x + y m_y
        if dC[1] and dC[0]:
            vecs = []
            for s in range(2):
                for i in range(M.dim(j - 1)):
                    e = [F.one if t == i else F.zero for t in range(M.dim(j - 1))]
                    vecs.append(M.act_poly(K["D1"][s][0], j - 1, e))
            rk[1] = rank(F, vecs, dC[0])
        # d2: C_2 -> C_1 : f_t (x) m -> (D2[t][0] m, D2[t][1] m)
        if dC[2] and dC[1]:
            vecs = []
            n1 = M.dim(j - 1)
            for t in range(2):
                for i in range(M.dim(j - 3)):
                    e = [F.one if q == i else F.zero for q in range(M.dim(j - 3))]
                    vecs.append(M.act_poly(K["D2"][t][0], j - 3, e) + M.act_poly(K["D2"][t][1], j - 3, e))
            rk[2] = rank(F, vecs, 2 * n1)
        # d3: C_3 -> C_2 : m -> (D3[0][0] m, D3[0][1] m)
        if dC[3] and dC[2]:
            vecs = []
            n3 = M.dim(j - 3)
            for i in range(M.dim(j - 4)):
                e = [F.one if q == i else F.zero for q in range(M.dim(j - 4))]
                vecs.append(M.act_poly(K["D3"][0][0], j - 4, e) + M.act_poly(K["D3"][0][1], j - 4, e))
            rk[3] = rank(F, vecs, 2 * n3)
        for i in range(4):
            b = dC[i] - rk[i] - rk[i + 1]
            if b:
                out[(i, j)] = b
    return out


def complex_is_a_complex_on(M):
    """Sanity check on a module: the two composites of K (x) M vanish (needs M to be a U(H)-module)."""
    return M.check_relations()


def table_rows(table):
    """Sorted list of (i, degree, rank)."""
    return [(i, j, r) for (i, j), r in sorted(table.items())]
