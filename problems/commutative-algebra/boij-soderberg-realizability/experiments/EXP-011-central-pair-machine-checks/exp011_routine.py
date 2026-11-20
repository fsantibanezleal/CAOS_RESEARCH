"""EXP-011 routine: the central pair f = A + z^s l_1, g = B + z^s l_2 of U(H) in characteristic p dividing an odd e, its
identities (exact polynomial arithmetic in U modulo p, `uhlib.algebra`, left-module products in the stated order), the Hilbert
function of M = U/(Uf + Ug) from exact ranks of left multiplication (python-flint, `nmod_mat`), the resultant test, and the Betti
table by `uhlib` (module construction and `tor.betti`).

Polynomials of U are dicts {(a, b, c): coefficient} for x^a y^b z^c (PBW, yx = xy - z); forms in x, y are dicts {(a, b): c}.
Nothing here imports another experiment; `uhlib` is imported, not edited.
"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

import flint  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import fields as UF  # noqa: E402
from uhlib import tor  # noqa: E402
from uhlib.fastmod import quotient_module_np  # noqa: E402


# ------------------------------------------------------------------ the formula
def u(n):
    return A.dim_U(n)


def h_e(e, n):
    """Hilbert function of the pure table (1, 2, 2, 1) on (0, e, 3e, 4e)."""
    return u(n) - 2 * u(n - e) + 2 * u(n - 3 * e) - u(n - 4 * e)


def pure_table(e):
    return {(0, 0): 1, (1, e): 2, (2, 3 * e): 2, (3, 4 * e): 1}


# ------------------------------------------------------------------ polynomial arithmetic in U modulo p
def red(poly, p):
    return {m: c % p for m, c in poly.items() if c % p}


def mul(a, b, p):
    return red(A.poly_mul_int(a, b), p)


def add(a, b, p):
    return red(A.padd(a, b, 1), p)


def sub(a, b, p):
    return red(A.padd(a, b, -1), p)


def neg(a, p):
    return {m: (-c) % p for m, c in a.items() if c % p}


# ------------------------------------------------------------------ the pair
def xy_from_XY(p, poly):
    """A polynomial {(i, j): c} in X = x^p, Y = y^p as the form {(p i, p j): c} in x, y."""
    return {(p * i, p * j): c for (i, j), c in poly.items()}


def build_pair(e, p, Aform, Bform, l1, l2):
    """f = A + z^s l_1, g = B + z^s l_2 with s = (e - 1)/2; A, B forms {(a, b): c} of degree e in x, y; l_i = (coefficient of x,
    coefficient of y).  Returns the two polynomials of U modulo p."""
    s = (e - 1) // 2
    out = []
    for form, (cx, cy) in ((Aform, l1), (Bform, l2)):
        poly = {(a, b, 0): c for (a, b), c in form.items()}
        if cx % p:
            poly[(1, 0, s)] = cx % p
        if cy % p:
            poly[(0, 1, s)] = cy % p
        out.append(red(poly, p))
    return out[0], out[1]


def lam_formula(l1, l2, p):
    """lambda with [l_2, l_1] = lambda z: l_1 = a_1 x + b_1 y, l_2 = c_1 x + d_1 y give b_1 c_1 - a_1 d_1 (note F3)."""
    (a1, b1), (c1, d1) = l1, l2
    return (b1 * c1 - a1 * d1) % p


def identities(e, p, f, g, Aform, Bform):
    """The identities of the theorem as exact equalities of polynomials in U modulo p (Aform, Bform: A, B as polynomials of U).
    Returns a dict of booleans plus lambda read from the commutator (None when the commutator is not a multiple of z^e)."""
    x_, y_ = {(1, 0, 0): 1}, {(0, 1, 0): 1}
    central = all(mul(v, w, p) == mul(w, v, p) for v in (x_, y_) for w in (Aform, Bform))
    gf, fg = mul(g, f, p), mul(f, g, p)
    comm = sub(gf, fg, p)
    lam = comm[(0, 0, e)] if set(comm) == {(0, 0, e)} else None
    s1 = (sub(comm, fg, p), mul(f, f, p))
    s2 = (mul(g, g, p), neg(add(gf, comm, p), p))
    z1 = add(mul(s1[0], f, p), mul(s1[1], g, p), p)
    z2 = add(mul(s2[0], f, p), mul(s2[1], g, p), p)
    t = tuple(add(mul(g, s1[i], p), mul(f, s2[i], p), p) for i in range(2))
    out = {"A_B_central": central, "commutator_is_lambda_z_e": lam is not None and lam != 0, "syzygy_s1": not z1,
           "syzygy_s2": not z2, "third_relation": not t[0] and not t[1]}
    out["all"] = all(out.values())
    out["lambda"] = lam
    out["commutator"] = [[list(m), cc] for m, cc in sorted(comm.items())]
    return out


# ------------------------------------------------------------------ resultant of two forms of equal degree
def resultant_mod(p, A1, B1, d):
    """Homogeneous resultant modulo p of two binary forms of degree d ({(a, b): c}, a + b = d): the Sylvester determinant of
    the coefficient lists (coefficient of x^i y^(d - i) at index i), which vanishes exactly when the forms have a common factor."""
    a = [A1.get((i, d - i), 0) % p for i in range(d + 1)]
    b = [B1.get((i, d - i), 0) % p for i in range(d + 1)]
    n = 2 * d
    rows = []
    for k in range(d):
        rows.append([0] * k + a[::-1] + [0] * (n - d - 1 - k))
        rows.append([0] * k + b[::-1] + [0] * (n - d - 1 - k))
    flat = [v for r in rows for v in r]
    return int(flint.nmod_mat(n, n, flat, p).det())


# ------------------------------------------------------------------ the Hilbert function from exact ranks
def rank_mu(p, e, f, g, n):
    """rank of mu_n: the rows a * f and a * g for a in monos(n - e), written on monos(n), modulo p."""
    cols = {m: i for i, m in enumerate(A.monos(n))}
    ncol = len(cols)
    flat = []
    for a in A.monos(n - e):
        for h in (f, g):
            row = [0] * ncol
            for m, c in mul({a: 1}, h, p).items():
                row[cols[m]] = c
            flat.extend(row)
    nrow = 2 * len(A.monos(n - e))
    return int(flint.nmod_mat(nrow, ncol, flat, p).rank())


def hilbert(p, e, f, g, top, stop_at_zero=False):
    """[dim M_0, ..., dim M_top] with dim M_n = u(n) - rank mu_n.  With stop_at_zero the computation stops at the first zero
    degree n >= e (M is cyclic on 1 and generated by x, y, so every later degree is zero) and the list is padded with zeros."""
    dims = []
    for n in range(top + 1):
        if n < e:
            dims.append(u(n))
            continue
        d = u(n) - rank_mu(p, e, f, g, n)
        dims.append(d)
        if stop_at_zero and d == 0:
            dims.extend([0] * (top - n))
            break
    return dims


# ------------------------------------------------------------------ the Betti table through uhlib
def betti_uhlib(p, e, f, g, maxdeg=None):
    """(table {(i, j): rank} or None when the module is not finite within maxdeg, length or None, seconds)."""
    t0 = time.time()
    maxdeg = maxdeg if maxdeg is not None else 4 * e + 8
    F = UF.make_field(p, 1)
    rels = [{(0, m): c for m, c in f.items()}, {(0, m): c for m, c in g.items()}]
    M = quotient_module_np(F, [0], rels, maxdeg=maxdeg)
    if not M.finished:
        return None, None, time.time() - t0
    return tor.betti(M), M.total_dim(), time.time() - t0


def table_rows(t):
    return None if t is None else [[i, j, r] for (i, j), r in sorted(t.items())]


def rows_to_table(rows):
    return None if rows is None else {(i, j): r for i, j, r in rows}


def poly_list(poly):
    return [[list(m), c] for m, c in sorted(poly.items())]


def poly_from_list(lst):
    return {tuple(m): c for m, c in lst}


def poly_text(poly):
    def mono(m):
        a, b, c = m
        parts = ("x^%d" % a if a > 1 else "x" if a else "", "y^%d" % b if b > 1 else "y" if b else "",
                 "z^%d" % c if c > 1 else "z" if c else "")
        return "*".join(s for s in parts if s) or "1"
    terms = sorted(poly.items(), key=lambda kv: (-A.deg(kv[0]), kv[0]))
    return " + ".join((("%d*" % c) if c != 1 else "") + mono(m) if m != (0, 0, 0) else str(c) for m, c in terms) or "0"
