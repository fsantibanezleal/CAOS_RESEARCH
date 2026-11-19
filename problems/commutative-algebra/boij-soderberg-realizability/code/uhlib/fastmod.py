"""A numpy build of `module.quotient_module` for prime fields and GF(2^k) (same reduced echelon rule, same output).

The row space of the relations in each degree is brought to reduced row echelon form with vectorized row
operations (integers mod p, or table lookups for GF(2^k) with the bit encoding sum c_i 2^i, addition = xor).
Reduced row echelon form is unique, so the quotient basis (the non-pivot columns), the matrices of x and y and the
monomial labels coincide with those of the pure Python `quotient_module`; tests/test_bs_uhlib.py checks this.
"""
import numpy as np

from . import algebra as A
from .fields import ExtField, PrimeField
from .module import GradedModule, _free_basis, coef


class NumpyField:
    """Table-driven arithmetic on integer arrays for PrimeField (p < 2^31) and ExtField(2, k), k <= 8."""

    def __init__(self, F):
        self.F = F
        if isinstance(F, PrimeField):
            self.kind, self.p = "prime", F.p
            self.dtype = np.int64
            self.q = F.p
            self.inv_table = np.array([0] + [pow(a, -1, F.p) for a in range(1, F.p)], dtype=np.int64) if F.p < 70000 else None
        elif isinstance(F, ExtField) and F.p == 2 and F.k <= 8:
            self.kind, self.p, self.q = "bin", 2, 1 << F.k
            self.dtype = np.int64
            self.elts = [tuple((n >> i) & 1 for i in range(F.k)) for n in range(self.q)]
            self.MUL = np.array([[self.encode(F.mul(self.elts[a], self.elts[b])) for b in range(self.q)] for a in range(self.q)],
                                dtype=np.int64)
            self.inv_table = np.array([0] + [self.encode(F.inv(self.elts[a])) for a in range(1, self.q)], dtype=np.int64)
            assert all(self.MUL[a, self.inv_table[a]] == 1 for a in range(1, self.q)), "inverse table is wrong"
        else:
            raise TypeError("NumpyField supports prime fields and GF(2^k), k <= 8")

    def encode(self, a):
        if self.kind == "prime":
            return int(a)
        return sum(int(c) << i for i, c in enumerate(a))

    def decode(self, n):
        return int(n) if self.kind == "prime" else self.elts[int(n)]

    # scalar python-level helpers (used while assembling rows)
    def add(self, a, b):
        return (a + b) % self.p if self.kind == "prime" else a ^ b

    def mul_scalar(self, a, b):
        return (a * b) % self.p if self.kind == "prime" else int(self.MUL[a, b])

    def times_int(self, a, k):
        """a * (integer k), k any integer."""
        if self.kind == "prime":
            return (a * k) % self.p
        return a if k & 1 else 0

    # vector helpers
    def sub_scaled(self, rows, factors, pivrow):
        """rows - factors[:, None] * pivrow[None, :]."""
        if self.kind == "prime":
            return (rows - factors[:, None] * pivrow[None, :]) % self.p
        return rows ^ self.MUL[factors[:, None], pivrow[None, :]]

    def scale(self, a, row):
        if self.kind == "prime":
            return (row * a) % self.p
        return self.MUL[a, row]


def rref(NF, M):
    """Reduced row echelon form of the integer array M: (rows of the nonzero part, pivot columns)."""
    M = M.copy()
    m, n = M.shape
    cur, pivots = 0, []
    for j in range(n):
        if cur >= m:
            break
        nz = np.nonzero(M[cur:, j])[0]
        if nz.size == 0:
            continue
        r = cur + int(nz[0])
        if r != cur:
            M[[cur, r]] = M[[r, cur]]
        a = int(M[cur, j])
        if a != 1:
            M[cur] = NF.scale(int(NF.inv_table[a]), M[cur])
        others = np.nonzero(M[:, j])[0]
        others = others[others != cur]
        if others.size:
            M[others] = NF.sub_scaled(M[others], M[others, j], M[cur])
        pivots.append(j)
        cur += 1
    return M[:cur], pivots


def quotient_module_np(F, shifts, rels, maxdeg=24, name="", with_action=True):
    """Same contract as module.quotient_module; `with_action=False` skips the matrices of x and y (dims only)."""
    NF = NumpyField(F)
    rels_f, rel_deg = [], []
    for g in rels:
        g = {key: coef(F, c) for key, c in g.items() if not F.is_zero(coef(F, c))}
        if not g:
            continue
        degs = {shifts[k] + A.deg(m) for (k, m) in g}
        assert len(degs) == 1, "relation is not homogeneous"
        rel_deg.append(degs.pop())
        rels_f.append({key: NF.encode(c) for key, c in g.items()})
    lo = min(shifts) if shifts else 0
    maxshift = max(shifts) if shifts else 0
    R, piv, nonpiv, basis = {}, {}, {}, {}
    dims = []
    d, zeros, finished = lo, 0, False
    while d <= maxdeg:
        B = _free_basis(shifts, d)
        idx = {b: i for i, b in enumerate(B)}
        rows = []
        for g, e in zip(rels_f, rel_deg):
            if e > d:
                continue
            for u in A.monos(d - e):
                v = [0] * len(B)
                for (k, m), c in g.items():
                    for mm, kk in A.mono_mul(u, m):
                        i = idx[(k, mm)]
                        v[i] = NF.add(v[i], NF.times_int(c, kk))
                if any(v):
                    rows.append(v)
        if rows and B:
            Rd, pv = rref(NF, np.array(rows, dtype=NF.dtype))
        else:
            Rd, pv = np.zeros((0, len(B)), dtype=NF.dtype), []
        pset = set(pv)
        R[d], piv[d], basis[d] = Rd, pv, B
        nonpiv[d] = [j for j in range(len(B)) if j not in pset]
        dims.append(len(nonpiv[d]))
        zeros = zeros + 1 if dims[-1] == 0 else 0
        if d >= maxshift and zeros >= 3:
            finished = True
            break
        d += 1
    if finished:
        while len(dims) > 1 and dims[-1] == 0:
            dims.pop()
    last = lo + len(dims) - 1
    X, Y = [], []
    for d in range(lo, last + 1):
        i = d - lo
        if d == last or not with_action:
            X.append([[] for _ in range(dims[i])])
            Y.append([[] for _ in range(dims[i])])
            continue
        B1 = basis[d + 1]
        idx1 = {b: t for t, b in enumerate(B1)}
        npc = nonpiv[d + 1]
        pv1, R1 = piv[d + 1], R[d + 1]
        for gen, store in ((A.X, X), (A.Y, Y)):
            (gm,) = gen
            V = np.zeros((len(nonpiv[d]), len(B1)), dtype=NF.dtype)
            for r, c in enumerate(nonpiv[d]):
                k, m = basis[d][c]
                for mm, kk in A.mono_mul(gm, m):
                    V[r, idx1[(k, mm)]] = NF.add(int(V[r, idx1[(k, mm)]]), NF.times_int(1, kk))
            out = V[:, npc].copy()
            for rr, pcol in enumerate(pv1):
                f = V[:, pcol]
                if f.any():
                    out = NF.sub_scaled(out, f, R1[rr, npc])
            store.append([[NF.decode(t) for t in row] for row in out])
    M = GradedModule(F, lo, dims, X, Y, finished=finished, name=name)
    M.labels = [[basis[d][c] for c in nonpiv[d]] for d in range(lo, last + 1)]
    return M
