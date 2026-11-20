"""EXP-016 routine: the lists L(e, q) of monic forms G of degree m = e/2 over GF(q) (q = p or p^2) that satisfy (C) and (b) of hypothesis.md,
and the pair (f, g) = (x^e + y^e, G(xy, z)) of each form in PBW monomials.

Definitions (hypothesis.md, 'Definitions fixed here'), with G_j(h) = G(h + j), A_n(h) = h (h + 1) ... (h + n - 1), B_n(h) = (h - 1) ... (h - n):
  P_plus = G_(2e) A_e, P_minus = G_(-2e) B_e;  F_r = G_(r-2e) B_(e-r) for 1 <= r <= e - 1 and F_r = G_(r+2e) A_(e+r) for -e <= r <= -1;
  (C): gcd(G_r, F_r) = 1 for 1 <= |r| <= e - 1 and r = -e, and gcd(G, P_plus) = 1 or gcd(G, P_minus) = 1;
  (b): the remainders of P_minus and P_plus modulo G are both nonzero and the first is a scalar multiple lambda of the second.
Enumeration: the coefficients of 1, h, ..., h^(m-1) read as a number in base q, lowest coefficient as the lowest digit; over GF(p^2) the
element a + b t is the digit a + b p, with t^2 + c1 t + c0 the modulus of `uhlib` (the same one Singular gets as minpoly).

Fast test: P_minus and P_plus are linear in the coefficient vector of G, so two integer matrices (m + 1) x (m + e + 1) give them for a block of
forms by one product each; the remainder modulo the monic G is a synthetic division on the block; (b) is the vanishing of the 2 x 2 minors of
the two remainder vectors with both vectors nonzero.  Every intermediate stays below 2^62.  The exact test (python-flint, fq_default_poly) is
applied to the forms that pass.
"""
import sys
import time
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

import flint  # noqa: E402
import numpy as np  # noqa: E402
from uhlib import fastmod  # noqa: E402
from uhlib import tor  # noqa: E402
from uhlib.fields import CachedExtField, PrimeField, find_modulus  # noqa: E402

BLOCK = 1 << 16
PURE_BETTI = lambda e: {(0, 0): 1, (1, e): 2, (2, 3 * e): 2, (3, 4 * e): 1}  # noqa: E731


# ------------------------------------------------------------------ the field and the enumeration
class Field:
    """GF(p) (k = 1) or GF(p^2) (k = 2); elements are ints (k = 1) or pairs (a, b) for a + b t (k = 2)."""

    def __init__(self, p, k=1):
        assert k in (1, 2)
        self.p, self.k, self.q = p, k, p ** k
        self.modulus = list(find_modulus(p, 2)) if k == 2 else None
        self.name = "GF(%d)" % p if k == 1 else "GF(%d^2)" % p

    def elem(self, n):
        n = int(n)
        return n if self.k == 1 else (n % self.p, n // self.p)

    def index(self, el):
        return int(el) if self.k == 1 else int(el[0]) + int(el[1]) * self.p

    def comps(self, el):
        return (int(el),) if self.k == 1 else (int(el[0]), int(el[1]))

    def record(self):
        """The field record read by the second instrument."""
        return {"name": self.name, "uhlib_name": self.name, "char": self.p, "degree": self.k, "modulus": self.modulus}

    def uhlib_field(self):
        return PrimeField(self.p) if self.k == 1 else CachedExtField(self.p, 2)


def form_from_index(e, F, idx):
    """The coefficients of 1, h, ..., h^(m-1) of the form numbered idx."""
    out, idx = [], int(idx)
    for _ in range(e // 2):
        out.append(F.elem(idx % F.q))
        idx //= F.q
    return out


def jsonable(F, el):
    return int(el) if F.k == 1 else [int(el[0]), int(el[1])]


def poly_text(F, coeffs):
    """The monic form as a polynomial in h, highest degree first."""
    m = len(coeffs)
    terms = ["h^%d" % m if m > 1 else "h"]
    for k in range(m - 1, -1, -1):
        c = coeffs[k]
        if F.comps(c) == (0,) * F.k:
            continue
        cs = str(int(c)) if F.k == 1 else "(%d + %d t)" % (c[0], c[1])
        mon = "" if k == 0 else (" h" if k == 1 else " h^%d" % k)
        terms.append(cs + mon if k else cs)
    return " + ".join(terms)


# ------------------------------------------------------------------ integer polynomials and the two matrices
def _imul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


@lru_cache(maxsize=None)
def _A_int(n, shift=0):
    r = [1]
    for i in range(n):
        r = _imul(r, [shift + i, 1])
    return tuple(r)


@lru_cache(maxsize=None)
def _B_int(n):
    r = [1]
    for i in range(1, n + 1):
        r = _imul(r, [-i, 1])
    return tuple(r)


@lru_cache(maxsize=None)
def matrices(e, p):
    """(M_minus, M_plus), each (m + 1) x (m + e + 1) modulo p: row k holds the coefficients of (h - 2e)^k B_e(h) and of (h + 2e)^k A_e(h)."""
    m = e // 2
    mm, mp = np.zeros((m + 1, m + e + 1), dtype=np.int64), np.zeros((m + 1, m + e + 1), dtype=np.int64)
    pw_m, pw_p = [1], [1]
    for k in range(m + 1):
        for target, pw, base in ((mm, pw_m, _B_int(e)), (mp, pw_p, _A_int(e))):
            row = _imul(pw, list(base))
            target[k, :len(row)] = [c % p for c in row]
        pw_m, pw_p = _imul(pw_m, [-2 * e, 1]), _imul(pw_p, [2 * e, 1])
    return mm, mp


# ------------------------------------------------------------------ the fast test
def ext_mul(F, a, b):
    """Product in GF(p^2) of arrays of shape (2, ...) (components of a + b t), reduced modulo p; modulus t^2 + c1 t + c0."""
    p, (c0, c1, _) = F.p, F.modulus
    a0, a1, b0, b1 = a[0], a[1], b[0], b[1]
    hi = a1 * b1
    return np.stack([(a0 * b0 - hi * c0) % p, (a0 * b1 + a1 * b0 - hi * c1) % p])


def _block_prime(e, p, s, t):
    m, n = e // 2, t - s
    mm, mp = matrices(e, p)
    C = np.empty((m + 1, n), dtype=np.int64)
    x = np.arange(s, t, dtype=np.int64)
    for j in range(m):
        C[j] = x % p
        x //= p
    C[m] = 1
    out = []
    for M in (mm, mp):
        P = (M.T @ C) % p
        Gc = C[:m]
        for i in range(m + e, m - 1, -1):
            q = P[i] % p
            P[i - m:i] -= q[None, :] * Gc
        out.append(P[:m] % p)
    Rm, Rp = out
    ok = Rm.any(axis=0) & Rp.any(axis=0)
    sel = np.nonzero(ok)[0]
    if sel.size == 0:
        return np.empty(0, dtype=np.int64)
    Rm, Rp = Rm[:, sel], Rp[:, sel]
    keep = ((Rm[0] * Rp[1] - Rm[1] * Rp[0]) % p) == 0
    sel, Rm, Rp = sel[keep], Rm[:, keep], Rp[:, keep]
    keep = np.ones(sel.size, dtype=bool)
    for i in range(m):
        for j in range(i + 1, m):
            keep &= ((Rm[i] * Rp[j] - Rm[j] * Rp[i]) % p) == 0
    return sel[keep] + s


def _block_ext(e, F, s, t):
    p, m, n = F.p, e // 2, t - s
    mm, mp = matrices(e, p)
    C = np.zeros((m + 1, 2, n), dtype=np.int64)
    x = np.arange(s, t, dtype=np.int64)
    for j in range(m):
        d = x % F.q
        C[j, 0], C[j, 1] = d % p, d // p
        x //= F.q
    C[m, 0] = 1
    out = []
    for M in (mm, mp):
        P = np.stack([(M.T @ C[:, c, :]) % p for c in range(2)])          # (2, m + e + 1, n)
        Gc = C[:m].transpose(1, 0, 2)                                    # (2, m, n)
        for i in range(m + e, m - 1, -1):
            q = P[:, i, :] % p
            P[:, i - m:i, :] = (P[:, i - m:i, :] - ext_mul(F, q[:, None, :], Gc)) % p
        out.append(P[:, :m, :] % p)
    Rm, Rp = out
    keep = Rm.any(axis=(0, 1)) & Rp.any(axis=(0, 1))
    for i in range(m):
        for j in range(i + 1, m):
            minor = (ext_mul(F, Rm[:, i], Rp[:, j]) - ext_mul(F, Rm[:, j], Rp[:, i])) % p
            keep &= ~minor.any(axis=0)
    return np.nonzero(keep)[0] + s


def fast_passing(e, F, start, end):
    """The indices in [start, end) whose form passes the fast test of (b), as an int64 array."""
    parts = []
    for s in range(start, end, BLOCK):
        t = min(end, s + BLOCK)
        parts.append(_block_prime(e, F.p, s, t) if F.k == 1 else _block_ext(e, F, s, t))
    return np.concatenate(parts) if parts else np.empty(0, dtype=np.int64)


# ------------------------------------------------------------------ the exact tests (python-flint)
@lru_cache(maxsize=None)
def _fl(p, k):
    if k == 1:
        ctx = flint.fq_default_ctx(p, 1)
    else:
        ctx = flint.fq_default_ctx(modulus=flint.fmpz_mod_poly_ctx(p)(find_modulus(p, 2)))
    return ctx, flint.fq_default_poly_ctx(ctx)


def _to_fl(F, el):
    ctx, _ = _fl(F.p, F.k)
    return ctx(int(el)) if F.k == 1 else ctx(int(el[0])) + ctx(int(el[1])) * ctx.gen()


def _from_fl(F, x):
    lst = [int(v) for v in x.to_list()]
    lst += [0] * (F.k - len(lst))
    return lst[0] if F.k == 1 else (lst[0], lst[1])


class _Exact:
    """The polynomials of one form: G and the shifts G_j, A_n, B_n over the field."""

    def __init__(self, e, F, coeffs):
        self.e, self.F = e, F
        ctx, self.P = _fl(F.p, F.k)
        self.ctx = ctx
        self.one = ctx(1)
        self.G = self.P([_to_fl(F, c) for c in coeffs] + [self.one])
        self.h = self.P([ctx(0), self.one])
        self._shift = {}

    def shifted(self, j):
        if j not in self._shift:
            self._shift[j] = self.G.compose(self.h + self.P([self.ctx(j % self.F.p)]))
        return self._shift[j]

    def A(self, n):
        return _ab(self.F.p, self.F.k, self.e)[0][n]

    def B(self, n):
        return _ab(self.F.p, self.F.k, self.e)[1][n]


@lru_cache(maxsize=None)
def _ab(p, k, e):
    """[A_0, ..., A_e] and [B_0, ..., B_e] as polynomials over the field (they do not depend on the form)."""
    ctx, P = _fl(p, k)
    h = P([ctx(0), ctx(1)])
    As, Bs = [P([ctx(1)])], [P([ctx(1)])]
    for i in range(e):
        As.append(As[-1] * (h + P([ctx(i % p)])))
        Bs.append(Bs[-1] * (h + P([ctx((-(i + 1)) % p)])))
    return As, Bs


def exact_b(e, F, coeffs):
    """lambda (an element of the field) when (b) holds, else None."""
    X = _Exact(e, F, coeffs)
    m = e // 2
    rp = (X.shifted(2 * e) * X.A(e)) % X.G
    rm = (X.shifted(-2 * e) * X.B(e)) % X.G
    if rm.is_zero() or rp.is_zero():
        return None
    zero = X.ctx(0)
    cp = list(rp.coeffs()) + [zero] * (m - len(rp.coeffs()))
    i = next(i for i, c in enumerate(cp) if c != 0)
    cm = list(rm.coeffs()) + [zero] * (m - len(rm.coeffs()))
    lam = cm[i] / cp[i]
    if lam == 0 or rm != X.P([lam]) * rp:
        return None
    return _from_fl(F, lam)


def exact_C(e, F, coeffs):
    """Hypothesis (C), by greatest common divisors, for every r with the two choices at r = 0."""
    X = _Exact(e, F, coeffs)

    def coprime(a, b):
        return a.gcd(b).degree() <= 0

    for r in range(-e, e):
        Gr = X.shifted(r)
        if r == 0:
            pplus, pminus = X.shifted(2 * e) * X.A(e), X.shifted(-2 * e) * X.B(e)
            if not (coprime(X.G, pplus) or coprime(X.G, pminus)):
                return False
        elif r > 0:
            if not coprime(Gr, X.shifted(r - 2 * e) * X.B(e - r)):
                return False
        else:
            if not coprime(Gr, X.shifted(r + 2 * e) * X.A(e + r)):
                return False
    return True


# ------------------------------------------------------------------ ranges, lists and negative controls
def scan_range(e, F, start, end):
    """The forms with index in [start, end): the number passing the fast test, those with (b) (exact), those with (b) and without (C),
    and the list (index, coefficients, lambda) of those with (b) and (C)."""
    idxs = fast_passing(e, F, start, end).tolist()
    n_b, n_noC, bad, lst = 0, 0, 0, []
    for i in idxs:
        cs = form_from_index(e, F, i)
        lam = exact_b(e, F, cs)
        if lam is None:
            bad += 1
            continue
        n_b += 1
        if exact_C(e, F, cs):
            lst.append({"index": int(i), "coeffs": [jsonable(F, c) for c in cs], "lam": jsonable(F, lam)})
        else:
            n_noC += 1
    return {"n_fast": len(idxs), "n_b": n_b, "n_b_noC": n_noC, "n_fast_not_exact": bad, "list": lst}


def scan_negatives(e, F, count=5, block=4096):
    """The first `count` forms in the order of the enumeration with (C) and without (b): [(index, coefficients)]."""
    out, total = [], F.q ** (e // 2)
    for s in range(0, total, block):
        t = min(total, s + block)
        passing = set(fast_passing(e, F, s, t).tolist())
        for i in range(s, t):
            if i in passing:
                continue
            cs = form_from_index(e, F, i)
            if exact_C(e, F, cs):
                out.append((i, cs))
                if len(out) == count:
                    return out
    return out


# ------------------------------------------------------------------ the pair in PBW monomials
def pbw_g(e, F, coeffs):
    """g = G(xy, z) as {(a, a, m - a): coefficient}: G = sum gamma_a A_a(h) gives g = sum gamma_a x^a y^a z^(m-a) (componentwise over GF(p))."""
    m, p, k = e // 2, F.p, F.k
    gam = [[0] * (m + 1) for _ in range(k)]
    for t in range(k):
        rest = [F.comps(c)[t] % p for c in coeffs] + [1 if t == 0 else 0]
        for a in range(m, -1, -1):
            c = rest[a] % p
            gam[t][a] = c
            if c:
                for i, v in enumerate(_A_int(a)):
                    rest[i] = (rest[i] - c * v) % p
        assert not any(rest)
    out = {}
    for a in range(m + 1):
        el = tuple(gam[t][a] for t in range(k))
        if any(el):
            out[(a, a, m - a)] = el[0] if k == 1 else el
    return out


def basis_json(e, g):
    """The two forms f, g as [[[a, b, c], coefficient], ...] (the form the second instrument reads)."""
    ext = any(not isinstance(c, int) for c in g.values())
    one = [1, 0] if ext else 1
    f = [[[e, 0, 0], one], [[0, e, 0], one]]
    return [f, [[list(mono), c if isinstance(c, int) else list(c)] for mono, c in sorted(g.items())]]


# ------------------------------------------------------------------ the first instrument (uhlib)
class _TableField:
    """Table-driven arithmetic on integer arrays for GF(p^2) (p odd, q = p^2 small): element a + b t is the integer a + b p.
    Offered to `uhlib.fastmod.quotient_module_np` in place of NumpyField (which serves prime fields and GF(2^k) only)."""
    kind = "tab"

    def __init__(self, F):
        self.F, self.p = F, F.p
        self.q = q = F.p * F.p
        self.dtype = np.int64
        els = [(n % F.p, n // F.p) for n in range(q)]
        self.MUL = np.array([[self.encode(F.mul(a, b)) for b in els] for a in els], dtype=np.int64)
        self.ADD = np.array([[self.encode(F.add(a, b)) for b in els] for a in els], dtype=np.int64)
        self.NEG = np.array([self.encode(F.neg(a)) for a in els], dtype=np.int64)
        self.inv_table = np.array([0] + [self.encode(F.inv(els[n])) for n in range(1, q)], dtype=np.int64)

    def encode(self, a):
        return int(a[0]) + int(a[1]) * self.p

    def decode(self, n):
        return (int(n) % self.p, int(n) // self.p)

    def add(self, a, b):
        return int(self.ADD[a, b])

    def times_int(self, a, k):
        return int(self.MUL[a, k % self.p])

    def sub_scaled(self, rows, factors, pivrow):
        return self.ADD[rows, self.NEG[self.MUL[factors[:, None], pivrow[None, :]]]]

    def scale(self, a, row):
        return self.MUL[a, row]


def first_instrument(e, F, g, maxdeg=None):
    """Betti table and length of U / (U f + U g) by `uhlib` (module construction, then tor.betti).  g is a dict {(a, b, c): coefficient}."""
    maxdeg = 4 * e + 3 if maxdeg is None else maxdeg
    UF = F.uhlib_field()
    rels = [{(0, (e, 0, 0)): 1, (0, (0, e, 0)): 1}, {(0, mono): c for mono, c in g.items()}]
    orig = fastmod.NumpyField
    t0 = time.time()
    if F.k == 2:
        fastmod.NumpyField = lambda FF: _TableField(FF)
    try:
        M = fastmod.quotient_module_np(UF, [0], rels, maxdeg=maxdeg)
    finally:
        fastmod.NumpyField = orig
    length = M.total_dim()
    if not M.finished:
        return {"finished": False, "length": None, "betti": None, "pure": False, "seconds": round(time.time() - t0, 1),
                "note": "module not finite within degree %d" % maxdeg}
    table = tor.betti(M)
    pure = bool(length == e ** 3 and table == PURE_BETTI(e))
    return {"finished": True, "length": int(length), "betti": [[i, j, r] for (i, j), r in sorted(table.items())], "pure": pure,
            "seconds": round(time.time() - t0, 1)}


def length_only(e, F, g, maxdeg=None):
    """The length of U / (U f + U g) (None when the module is not finite within the degree bound)."""
    maxdeg = 4 * e + 3 if maxdeg is None else maxdeg
    UF = F.uhlib_field()
    rels = [{(0, (e, 0, 0)): 1, (0, (0, e, 0)): 1}, {(0, mono): c for mono, c in g.items()}]
    orig = fastmod.NumpyField
    if F.k == 2:
        fastmod.NumpyField = lambda FF: _TableField(FF)
    try:
        M = fastmod.quotient_module_np(UF, [0], rels, maxdeg=maxdeg, with_action=False)
    finally:
        fastmod.NumpyField = orig
    return int(M.total_dim()) if M.finished else None


# ------------------------------------------------------------------ tasks run in worker processes
def scan_task(args):
    """(e, p, k, start, end) -> (start, end, result of scan_range, seconds)."""
    e, p, k, s, t = args
    t0 = time.time()
    return s, t, scan_range(e, Field(p, k), s, t), time.time() - t0


def throughput(e, p, n):
    """Forms per second of one process on the first n forms of (e, p): fast test only, then fast test plus exact tests."""
    F = Field(p)
    t0 = time.time()
    c = len(fast_passing(e, F, 0, n))
    t1 = time.time() - t0
    t0 = time.time()
    scan_range(e, F, 0, n)
    t2 = time.time() - t0
    return {"e": e, "p": p, "forms": n, "passing_fast": c, "fast_test_seconds": round(t1, 2), "forms_per_second_fast": round(n / t1),
            "with_exact_seconds": round(t2, 2), "forms_per_second_with_exact": round(n / t2)}


def _job(conn, kind, e, p, k, g_items, maxdeg):
    try:
        F = Field(p, k)
        g = {tuple(m): (c if k == 1 else tuple(c)) for m, c in g_items}
        out = first_instrument(e, F, g, maxdeg) if kind == "betti" else {"length": length_only(e, F, g, maxdeg)}
    except Exception as exc:  # reported, never swallowed
        out = {"error": repr(exc)[:300]}
    conn.send(out)


def run_isolated(kind, e, F, g, timeout, maxdeg=None):
    """A Betti table ('betti') or a length ('length') in a process of its own, killed at the timeout (seconds)."""
    import multiprocessing as mp
    ctx = mp.get_context("spawn")
    parent, child = ctx.Pipe(False)
    items = [[list(mono), c if isinstance(c, int) else list(c)] for mono, c in g.items()]
    proc = ctx.Process(target=_job, args=(child, kind, e, F.p, F.k, items, maxdeg))
    t0 = time.time()
    proc.start()
    child.close()
    if parent.poll(timeout):
        out = parent.recv()
    else:
        out = {"timeout": True, "seconds": round(time.time() - t0, 1), "note": "no result within %d s; killed" % timeout}
    if proc.is_alive():
        proc.terminate()
    proc.join()
    return out


def negatives_task(args):
    """(e, p, k, count) -> the first `count` forms with (C) and without (b), each with g and the length of its module."""
    e, p, k, count = args
    F = Field(p, k)
    out = []
    for i, cs in scan_negatives(e, F, count):
        g = pbw_g(e, F, cs)
        out.append({"index": int(i), "coeffs": [jsonable(F, c) for c in cs], "poly": poly_text(F, cs),
                    "g": [[list(mo), c if isinstance(c, int) else list(c)] for mo, c in sorted(g.items())]})
    return out
