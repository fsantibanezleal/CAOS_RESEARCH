"""EXP-012 routine: the class V_e, the data (A, beta_1, beta_2), D and n(f), the identities, the criterion, ranks and Betti tables.

Conventions (those of `uhlib`): a PBW monomial (a, b, c) is x^a y^b z^c, y x = x y - z, left modules.  X = x^p, Y = y^p are central
and so is z; a central monomial X^i Y^j z^l is the PBW monomial (p i, p j, l), of degree p (i + j) + 2 l.  Polynomials of U are
dicts {(a, b, c): coefficient mod p}; polynomials of Z = GF(p)[X, Y, z] are dicts {(i, j, l): coefficient mod p}.
f = A + beta_1 x + beta_2 y means the PBW polynomial A + beta_1 * x + beta_2 * y with the products taken in U.  First instrument:
`uhlib` (imported, not edited) for the module and its Betti table, python-flint for the ranks, sympy for the Groebner basis.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

import flint  # noqa: E402
import numpy as np  # noqa: E402
import sympy as sp  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import tor  # noqa: E402
from uhlib.fastmod import quotient_module_np  # noqa: E402
from uhlib.fields import make_field  # noqa: E402

XS, YS, ZS = sp.symbols("X Y z")
METHOD = "sympy groebner modulus p (grevlex)"


# ------------------------------------------------------------------ the numbers
def u(n):
    """dim U_n."""
    return 0 if n < 0 else (n + 2) ** 2 // 4


def h_e(e, n):
    """Hilbert function of a pure module with Betti table (1, 2, 2, 1) on (0, e, 3e, 4e)."""
    return u(n) - 2 * u(n - e) + 2 * u(n - 3 * e) - u(n - 4 * e)


def pure_table(e):
    return {(0, 0): 1, (1, e): 2, (2, 3 * e): 2, (3, 4 * e): 1}


# ------------------------------------------------------------------ polynomials of U modulo p
def pmod(poly, p):
    return {m: c % p for m, c in poly.items() if c % p}


def pmul(a, b, p):
    return pmod(A.poly_mul_int(a, b), p)


def padd_mod(a, b, p, sign=1):
    return pmod(A.padd(a, b, sign), p)


def pneg(a, p):
    return {m: (-c) % p for m, c in a.items() if c % p}


# ------------------------------------------------------------------ the class V_e
def central_basis(n, p):
    """The central monomials (i, j, l) of degree n, i.e. p (i + j) + 2 l = n, in lexicographic order."""
    out = []
    for i in range(n // p + 1):
        for j in range(n // p + 1):
            rest = n - p * (i + j)
            if rest >= 0 and rest % 2 == 0:
                out.append((i, j, rest // 2))
    return sorted(out)


def class_basis(e, p):
    """Basis of V_e: ('A', m) for the central monomials of degree e, then ('x', m) and ('y', m) for the central monomials of
    degree e - 1 (the elements m x and m y)."""
    z1 = central_basis(e - 1, p)
    return [("A", m) for m in central_basis(e, p)] + [("x", m) for m in z1] + [("y", m) for m in z1]


def vec_to_data(e, p, vec):
    """Coefficient vector on class_basis(e, p) to the data (A, beta_1, beta_2) as dicts {(i, j, l): c}."""
    out = {"A": {}, "x": {}, "y": {}}
    for (kind, m), c in zip(class_basis(e, p), vec):
        if c % p:
            out[kind][m] = c % p
    return out["A"], out["x"], out["y"]


def data_to_vec(e, p, Ad, b1, b2):
    d = {"A": Ad, "x": b1, "y": b2}
    return [d[kind].get(m, 0) % p for kind, m in class_basis(e, p)]


def data_to_pbw(Ad, b1, b2, p):
    """The PBW polynomial A + beta_1 x + beta_2 y (products in U, reduced modulo p)."""
    out = {}
    for cen, lin in ((Ad, None), (b1, A.X), (b2, A.Y)):
        for (i, j, l), c in cen.items():
            mono = {(p * i, p * j, l): c}
            out = padd_mod(out, mono if lin is None else A.poly_mul_int(mono, lin), p)
    return out


def pbw_to_data(poly, p):
    """The data (A, beta_1, beta_2) of a PBW polynomial of the class; ValueError when a monomial is outside it."""
    Ad, b1, b2 = {}, {}, {}
    for (a, b, c), v in poly.items():
        if a % p == 0 and b % p == 0:
            Ad[(a // p, b // p, c)] = v % p
        elif a % p == 1 and b % p == 0:
            b1[(a // p, b // p, c)] = v % p
        elif a % p == 0 and b % p == 1:
            b2[(a // p, b // p, c)] = v % p
        else:
            raise ValueError("monomial %s is outside the class" % ((a, b, c),))
    return Ad, b1, b2


def parse_pbw(text):
    """'x^3 z^2 + y z^3' to {(3, 0, 2): 1, (0, 1, 3): 1}: monomials in the PBW order x, y, z, coefficient 1."""
    out = {}
    for term in text.split("+"):
        a = b = c = 0
        for tok in term.split():
            name, _, ex = tok.partition("^")
            k = int(ex) if ex else 1
            if name == "x":
                a += k
            elif name == "y":
                b += k
            elif name == "z":
                c += k
            else:
                raise ValueError(tok)
        out[(a, b, c)] = 1
    return out


# ------------------------------------------------------------------ polynomials of Z = GF(p)[X, Y, z]
def zpoly(d, p):
    d = {m: c % p for m, c in d.items() if c % p}
    return sp.Poly.from_dict(d, XS, YS, ZS, modulus=p) if d else sp.Poly(0, XS, YS, ZS, modulus=p)


def zdict(P, p):
    return {tuple(int(t) for t in m): int(c) % p for m, c in P.terms() if int(c) % p}


def data_invariants(Ad, b1, b2, Bd, d1, d2, p):
    """D = beta_1 delta_2 - beta_2 delta_1, n(f) = A^p + beta_1^p X + beta_2^p Y and n(g), as dicts of Z."""
    PA, P1, P2 = zpoly(Ad, p), zpoly(b1, p), zpoly(b2, p)
    PB, Q1, Q2 = zpoly(Bd, p), zpoly(d1, p), zpoly(d2, p)
    X, Y = zpoly({(1, 0, 0): 1}, p), zpoly({(0, 1, 0): 1}, p)
    D = P1 * Q2 - P2 * Q1
    nf = PA ** p + P1 ** p * X + P2 ** p * Y
    ng = PB ** p + Q1 ** p * X + Q2 ** p * Y
    return zdict(D, p), zdict(nf, p), zdict(ng, p)


def central_to_pbw(d, p):
    """A central polynomial {(i, j, l): c} as a PBW polynomial of U."""
    return {(p * i, p * j, l): c % p for (i, j, l), c in d.items() if c % p}


def case_from_pbw(name, e, p, f, g):
    """Everything the identities and the criterion need, computed from the data of f and g (never from the answer)."""
    Ad, b1, b2 = pbw_to_data(f, p)
    Bd, d1, d2 = pbw_to_data(g, p)
    D, nf, ng = data_invariants(Ad, b1, b2, Bd, d1, d2, p)
    return {"name": name, "e": e, "p": p, "f": dict(f), "g": dict(g), "data_f": (Ad, b1, b2), "data_g": (Bd, d1, d2),
            "D": D, "nf": nf, "ng": ng}


def d_times_z(case, p):
    return zdict(zpoly(case["D"], p) * zpoly({(0, 0, 1): 1}, p), p)


# ------------------------------------------------------------------ identities
def identities(case, p):
    """The commutator identity g f - f g = - D z and the three identities of the complex, each an exact equality in U mod p."""
    f, g = case["f"], case["g"]
    c = pneg(central_to_pbw(d_times_z(case, p), p), p)
    gf, fg = pmul(g, f, p), pmul(f, g, p)
    out = {"commutator": padd_mod(gf, fg, p, -1) == c}
    s1 = (padd_mod(c, fg, p, -1), pmul(f, f, p))
    s2 = (pmul(g, g, p), pneg(padd_mod(gf, c, p), p))
    out["s1"] = padd_mod(pmul(s1[0], f, p), pmul(s1[1], g, p), p) == {}
    out["s2"] = padd_mod(pmul(s2[0], f, p), pmul(s2[1], g, p), p) == {}
    comp1 = padd_mod(pmul(g, s1[0], p), pmul(f, s2[0], p), p)
    comp2 = padd_mod(pmul(g, s1[1], p), pmul(f, s2[1], p), p)
    out["g_s1_plus_f_s2"] = comp1 == {} and comp2 == {}
    return out


# ------------------------------------------------------------------ the criterion
def criterion_detail(polys, p):
    """Zero dimensionality of the ideal of GF(p)[X, Y, z] generated by the dicts: a Groebner basis (grevlex) has a pure power of
    each variable among its leading monomials (a unit ideal counts as zero dimensional)."""
    ps = [zpoly(q, p) for q in polys]
    ps = [q for q in ps if not q.is_zero]
    if not ps:
        return {"holds": False, "method": METHOD, "basis_size": 0, "pure_powers": None}
    G = sp.groebner([q.as_expr() for q in ps], XS, YS, ZS, modulus=p, order="grevlex")
    leads = [sp.Poly(q, XS, YS, ZS, modulus=p).monoms(order="grevlex")[0] for q in G.exprs]
    if any(sum(m) == 0 for m in leads):
        return {"holds": True, "method": METHOD, "basis_size": len(leads), "pure_powers": "unit ideal"}
    pure = {}
    for v, name in enumerate("XYz"):
        ex = [m[v] for m in leads if m[v] > 0 and sum(m) == m[v]]
        if ex:
            pure[name] = min(ex)
    return {"holds": len(pure) == 3, "method": METHOD, "basis_size": len(leads), "pure_powers": pure}


def criterion_polys(polys, p):
    return criterion_detail(polys, p)["holds"]


def criterion(case, p):
    return criterion_detail([d_times_z(case, p), case["nf"], case["ng"]], p)


# ------------------------------------------------------------------ Hilbert function by ranks
def hilbert_dims(f, g, e, p, N, expected=None):
    """dim M_n for n = 0..N, M = U / (U f + U g), from the rank of (a, b) -> a f + b g on U_(n-e)^2; with `expected`, stops at the
    first degree where the dimension differs (the list then ends there).  After a degree with M_n = 0 the rest is zero (M is
    cyclic on a degree 0 generator)."""
    dims = []
    for n in range(N + 1):
        if n < e:
            d = u(n)
        else:
            cols = A.monos(n)
            idx = {m: i for i, m in enumerate(cols)}
            rows = []
            for gen in (f, g):
                for a in A.monos(n - e):
                    row = [0] * len(cols)
                    for m, c in gen.items():
                        for mm, k in A.mono_mul(a, m):
                            row[idx[mm]] = (row[idx[mm]] + c * k) % p
                    rows.append(row)
            d = len(cols) - flint.nmod_mat(rows, p).rank()
        dims.append(d)
        if expected is not None and d != expected[n]:
            return dims
        if d == 0:
            dims.extend([0] * (N - n))
            return dims
    return dims


def expected_hilbert(e):
    return [h_e(e, n) for n in range(4 * e + 4)]


def pure_hilbert(f, g, e, p):
    """(bool, dims): the Hilbert function of M equals h_e on degrees 0..4e+3 (zero from degree 4e on)."""
    exp = expected_hilbert(e)
    dims = hilbert_dims(f, g, e, p, 4 * e + 3, expected=exp)
    return dims == exp, dims


# ------------------------------------------------------------------ Betti table by uhlib
def betti_uhlib(f, g, e, p, maxdeg=None):
    """(Betti table {(i, j): rank} or None when M is not finished within maxdeg, dimensions of M)."""
    F = make_field(p, 1)
    rels = [{(0, m): c for m, c in poly.items()} for poly in (f, g)]
    M = quotient_module_np(F, [0], rels, maxdeg=maxdeg if maxdeg is not None else 4 * e + 8)
    return (tor.betti(M) if M.finished else None), list(M.dims)


# ------------------------------------------------------------------ random pairs of family R
def draw_pairs(e, p, seed, n):
    """n pairs (f, g) of coefficient vectors on class_basis(e, p), uniform on GF(p), drawn in order before any test."""
    rng = np.random.default_rng(seed)
    nb = len(class_basis(e, p))
    out = []
    for _ in range(n):
        fv = [int(c) for c in rng.integers(0, p, size=nb)]
        gv = [int(c) for c in rng.integers(0, p, size=nb)]
        out.append((fv, gv))
    return out


def pair_from_vectors(e, p, fv, gv):
    return data_to_pbw(*vec_to_data(e, p, fv), p), data_to_pbw(*vec_to_data(e, p, gv), p)


# ------------------------------------------------------------------ json forms
def pj(poly):
    """{(a, b, c): v} as a sorted list [[a, b, c, v], ...]."""
    return [[*m, c] for m, c in sorted(poly.items())]


def pj_inv(lst):
    return {(a, b, c): v for a, b, c, v in lst}
