"""EXP-137 shared exact-arithmetic library (own code, written from the definitions).

Nothing here imports or executes any file of the external archive. The archive is
read as data only: text files, and pickles through `restricted_loads` below.

Conventions (hypothesis.md, Definitions): t = x*y^2, z = 1/y, [t,z]_{x,y} = -1,
x^2 = t^2 z^4. A lattice point (i,j) is x^i y^j = t^i z^(2i-j): t-exponent i, band 2i-j.
For P = sum P_{p,a} t^a z^p, Q = sum Q_{q,c} t^c z^q:
    [P,Q]_{x,y} = sum (p*c - a*q) P_{p,a} Q_{q,c} t^(a+c-1) z^(p+q-1).
"""

from __future__ import annotations

import io
import pickle
from fractions import Fraction

from flint import fmpq, fmpq_poly

CASE1_P = [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)]
CASE1_Q = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]
CASE2_P = [(0, 0), (1, 0), (8, 14), (8, 16)]
CASE2_Q = [(0, 0), (2, 1), (12, 21), (12, 24)]


# ----------------------------------------------------------------- lattice

def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def lattice_points(vertices):
    """All integer points of conv(vertices), boundary included, integer arithmetic only."""
    hull = convex_hull(vertices)
    xs = [v[0] for v in hull]
    ys = [v[1] for v in hull]
    out = []
    n = len(hull)
    for i in range(min(xs), max(xs) + 1):
        for j in range(min(ys), max(ys) + 1):
            ok = True
            for k in range(n):
                x1, y1 = hull[k]
                x2, y2 = hull[(k + 1) % n]
                if (x2 - x1) * (j - y1) - (y2 - y1) * (i - x1) < 0:
                    ok = False
                    break
            if ok:
                out.append((i, j))
    return out


def band_of(point):
    i, j = point
    return 2 * i - j


# --------------------------------------------------------- generic bracket

def bracket_terms(ppts, qpts):
    """Return {(m, k): [(pt_p, pt_q, weight)]} for [P,Q]_{x,y} in (t,z) coordinates.

    Computed from x,y exponents directly: [x^i y^j, x^k y^l]_{x,y} = (i*l - j*k) x^(i+k-1) y^(j+l-1);
    the result monomial x^I y^J is t^I z^(2I-J).
    """
    out: dict = {}
    for (i, j) in ppts:
        for (k, l) in qpts:
            w = i * l - j * k
            if w == 0:
                continue
            I, J = i + k - 1, j + l - 1
            out.setdefault((I, 2 * I - J), []).append(((i, j), (k, l), w))
    return out


# ------------------------------------------------------ restricted unpickler

class RefusedPickle(Exception):
    pass


_SAFE = {
    ("builtins", "dict"), ("builtins", "list"), ("builtins", "tuple"), ("builtins", "set"),
    ("builtins", "frozenset"), ("builtins", "int"), ("builtins", "str"), ("builtins", "float"),
    ("builtins", "bool"), ("builtins", "bytes"), ("builtins", "complex"),
    ("fractions", "Fraction"),
}


class RestrictedUnpickler(pickle.Unpickler):
    """Allows only builtins containers/scalars and fractions.Fraction; refuses everything else."""

    def find_class(self, module, name):
        if (module, name) in _SAFE:
            return super().find_class(module, name)
        raise RefusedPickle(f"refused global {module}.{name}")


def restricted_loads(data: bytes):
    return RestrictedUnpickler(io.BytesIO(data)).load()


def pickle_globals(data: bytes):
    """Static scan (pickletools, no execution): the set of GLOBAL/STACK_GLOBAL/REDUCE-like opcodes seen."""
    import pickletools

    seen = set()
    for op, arg, _ in pickletools.genops(data):
        if op.name in ("GLOBAL", "STACK_GLOBAL", "REDUCE", "INST", "OBJ", "NEWOBJ", "NEWOBJ_EX", "BUILD"):
            seen.add((op.name, arg))
    return sorted(seen, key=str)


# ----------------------------------------------------------- number fields

class NF:
    """Q[u]/(m(u)) with m an fmpq_poly checked irreducible over Q at construction."""

    def __init__(self, minpoly: fmpq_poly, check_irreducible=True):
        self.m = minpoly
        self.deg = minpoly.degree()
        if check_irreducible:
            _c, facs = minpoly.factor()
            if not (len(facs) == 1 and facs[0][1] == 1 and facs[0][0].degree() == self.deg):
                raise ValueError("minimal polynomial is not irreducible over Q")

    def el(self, x=0):
        if isinstance(x, fmpq_poly):
            return Kel(self, x % self.m)
        if isinstance(x, Kel):
            return x
        return Kel(self, fmpq_poly([fmpq(x.numerator, x.denominator) if isinstance(x, Fraction) else x]) % self.m)

    def gen(self):
        return Kel(self, fmpq_poly([0, 1]) % self.m)


class Kel:
    __slots__ = ("F", "p")

    def __init__(self, F, p):
        self.F = F
        self.p = p

    def _c(self, o):
        return o if isinstance(o, Kel) else self.F.el(o)

    def __add__(self, o):
        return Kel(self.F, self.p + self._c(o).p)

    __radd__ = __add__

    def __neg__(self):
        return Kel(self.F, -self.p)

    def __sub__(self, o):
        return Kel(self.F, self.p - self._c(o).p)

    def __rsub__(self, o):
        return Kel(self.F, self._c(o).p - self.p)

    def __mul__(self, o):
        if isinstance(o, int):
            return Kel(self.F, self.p * o)
        return Kel(self.F, (self.p * self._c(o).p) % self.F.m)

    __rmul__ = __mul__

    def inv(self):
        g, s, _t = self.p.xgcd(self.F.m)
        if g.degree() != 0:
            raise ZeroDivisionError("element not invertible")
        return Kel(self.F, (s / g[0]) % self.F.m)

    def __truediv__(self, o):
        return self * self._c(o).inv()

    def __bool__(self):
        return not self.p.is_zero()

    def __eq__(self, o):
        return (self.p - self._c(o).p).is_zero()

    def __hash__(self):
        return hash(str(self.p))


# ------------------------------------------- multivariate polys over K (dict)

class MP:
    """Sparse multivariate polynomial over a number field: {exponent tuple: Kel}."""

    __slots__ = ("F", "n", "d")

    def __init__(self, F, n, d=None):
        self.F = F
        self.n = n
        self.d = d or {}

    @staticmethod
    def const(F, n, c):
        c = F.el(c)
        return MP(F, n, {(0,) * n: c} if c else {})

    @staticmethod
    def var(F, n, i):
        e = [0] * n
        e[i] = 1
        return MP(F, n, {tuple(e): F.el(1)})

    def copy(self):
        return MP(self.F, self.n, dict(self.d))

    def __add__(self, o):
        r = dict(self.d)
        for m, c in o.d.items():
            v = r[m] + c if m in r else c
            if v:
                r[m] = v
            else:
                r.pop(m, None)
        return MP(self.F, self.n, r)

    def __neg__(self):
        return MP(self.F, self.n, {m: -c for m, c in self.d.items()})

    def __sub__(self, o):
        return self + (-o)

    def scale(self, k):
        k = self.F.el(k)
        if not k:
            return MP(self.F, self.n)
        return MP(self.F, self.n, {m: c * k for m, c in self.d.items()})

    def __mul__(self, o):
        r: dict = {}
        for m, c in self.d.items():
            for n_, e in o.d.items():
                k = tuple(a + b for a, b in zip(m, n_))
                v = c * e
                r[k] = r[k] + v if k in r else v
        return MP(self.F, self.n, {m: c for m, c in r.items() if c})

    def __bool__(self):
        return bool(self.d)

    def subs_var(self, i, rep: "MP"):
        """Substitute variable i by the polynomial rep."""
        out = MP(self.F, self.n)
        pw = {0: MP.const(self.F, self.n, 1)}
        for m, c in self.d.items():
            e = m[i]
            if e not in pw:
                top = max(pw)
                cur = pw[top]
                for k in range(top + 1, e + 1):
                    cur = cur * rep
                    pw[k] = cur
            mm = list(m)
            mm[i] = 0
            out = out + (MP(self.F, self.n, {tuple(mm): c}) * pw[e])
        return out

    def is_const(self):
        return all(sum(m) == 0 for m in self.d)


def rref(F, rows, rhs):
    """Gauss-Jordan over K. rows: list of K-lists; rhs: list of MP. Returns (piv, free, solved, compat).

    solved[i] = (pivot col, MP rhs after elimination, row coefficients on free cols).
    """
    rows = [r[:] for r in rows]
    rhs = [x.copy() for x in rhs]
    m = len(rows)
    ncol = len(rows[0]) if rows else 0
    piv = []
    rr = 0
    for col in range(ncol):
        k = next((i for i in range(rr, m) if rows[i][col]), None)
        if k is None:
            continue
        rows[rr], rows[k] = rows[k], rows[rr]
        rhs[rr], rhs[k] = rhs[k], rhs[rr]
        inv = rows[rr][col].inv()
        rows[rr] = [x * inv for x in rows[rr]]
        rhs[rr] = rhs[rr].scale(inv)
        for i in range(m):
            if i != rr and rows[i][col]:
                q = rows[i][col]
                rows[i] = [x - q * y for x, y in zip(rows[i], rows[rr])]
                rhs[i] = rhs[i] - rhs[rr].scale(q)
        piv.append(col)
        rr += 1
    free = [j for j in range(ncol) if j not in piv]
    compat = [rhs[i] for i in range(rr, m) if rhs[i]]
    return rows, rhs, piv, free, compat
