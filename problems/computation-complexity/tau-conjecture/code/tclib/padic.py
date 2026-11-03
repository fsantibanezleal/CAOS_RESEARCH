"""Window-free p-adic filter for polynomials with many distinct integer roots.

Lemma (divisibility). Let f in Z[x] be nonzero with distinct integer roots
r_1..r_k, and write f = x^m g with g(0) != 0. Then prod_i (x - r_i) divides f
(Gauss: monic factors), and for every integer n with f(n) != 0

    v_p(f(n)) - max(m' - 1, 0) * v_p(n)  >=  sum_i v_p(n - r_i)        (*)

for every prime p and every integer 0 <= m' <= m. (If m >= 1, then 0 is a root
and x^m = x * x^(m-1); the factor x^(m-1) contributes (m-1) v_p(n) >= (m'-1) v_p(n)
and the root 0 is one of the r_i. If m' = 0 nothing is subtracted.)

The filter evaluates f at L = p^a consecutive points (a block, POINTS) modulo
p^e. Residues mod p^e are exact (ring homomorphism). A point where f(n) == 0 mod
p^e goes into the zero mask (it may or may not be a root); at every other point
v_p(f(n)) < e is known exactly. For a fixed mask, the least value of the
right-hand side of (*) summed over the non-mask points, over every choice of k
distinct integer roots, depends on the mask only:

- a root z among the mask points contributes C(z) = sum_{n not in mask} v_p(n - z);
- a root r outside the block contributes at least
  M = min_rho sum_{n not in mask} w(n - rho), rho = r mod p^a, where
  w(t) = v_p(t) if p^a does not divide t and a otherwise; distinct roots can
  share a residue, so M may be used k times;
- a root is never a non-mask point (f does not vanish there).

LB_k[mask] is the sum of the k smallest numbers in {C(z) : z in mask} + {M} * k.
Every polynomial with k distinct integer roots satisfies S >= LB_k[mask], where
S is the left-hand side of (*) summed over the non-mask points. A candidate with
S < LB_k[mask] has fewer than k distinct integer roots, wherever its roots lie.
"""
import numpy as np


def vp_int(t, p):
    """p-adic valuation of a nonzero Python integer."""
    t = abs(int(t))
    v = 0
    while t % p == 0:
        t //= p
        v += 1
    return v


class Layer:
    """One prime: points, modulus, the LB_k table and the per-point v_p(n)."""

    def __init__(self, p, a, e, k):
        self.p, self.a, self.e, self.k = p, a, e, k
        L = p ** a
        lo = -(L // 2)
        self.points = [lo + j for j in range(L)]
        self.L = L
        self.mod = p ** e
        # p = 2 uses e = 64: uint64 arithmetic wraps exactly mod 2^64. Odd p needs
        # p^e <= 2^32 so that a product of two residues fits in uint64 before reduction.
        if (p == 2 and e != 64) or (p != 2 and self.mod > (1 << 32)):
            raise ValueError("use p = 2 with e = 64, or an odd p with p^e <= 2^32")
        self.vpn = np.array([vp_int(n, p) if n else 0 for n in self.points], dtype=np.int32)
        self.table = self._table()

    def _table(self):
        p, a, L, n = self.p, self.a, self.L, self.points
        vz = np.zeros((L, L), dtype=np.int64)
        for i in range(L):
            for j in range(L):
                if i != j:
                    vz[i, j] = vp_int(n[j] - n[i], p)
        wr = np.zeros((L, L), dtype=np.int64)
        for rho in range(L):
            for j in range(L):
                t = n[j] - rho
                wr[rho, j] = a if t % L == 0 else vp_int(t, p)
        masks = np.arange(1 << L, dtype=np.int64)
        bits = ((masks[:, None] >> np.arange(L)) & 1).astype(bool)
        keep = (~bits).astype(np.int64)
        M = (keep @ wr.T).min(axis=1)
        C = keep @ vz.T                       # C[mask, i] = sum_{j not in mask} vz[i, j]
        Cz = np.where(bits, C, np.int64(1 << 40))
        pool = np.concatenate([Cz, np.repeat(M[:, None], self.k, axis=1)], axis=1)
        pool.sort(axis=1)
        return pool[:, :self.k].sum(axis=1).astype(np.int32)

    def values(self, poly):
        """Values of a polynomial (low-to-high coefficients) at the points, mod p^e."""
        out = np.zeros(self.L, dtype=np.uint64)
        for j, x in enumerate(self.points):
            acc = 0
            for c in reversed(poly):
                acc = (acc * x + c) % self.mod
            out[j] = acc
        return out

    def add(self, X, Y):
        return X + Y if self.p == 2 else (X + Y) % np.uint64(self.mod)

    def sub(self, X, Y):
        return X - Y if self.p == 2 else (X + (np.uint64(self.mod) - Y)) % np.uint64(self.mod)

    def mul(self, X, Y):
        return X * Y if self.p == 2 else (X * Y) % np.uint64(self.mod)

    def valuations(self, F):
        """(zero mask, v_p array) for uint64 residues F (..., L); v_p is meaningful off the mask."""
        zero = F == 0
        if self.p == 2:
            low = F & (~F + np.uint64(1))
            v = np.bitwise_count(low - np.uint64(1)).astype(np.int32)
        else:
            v = np.zeros(F.shape, dtype=np.int32)
            G = np.where(zero, np.uint64(1), F)
            pp = np.uint64(self.p)
            for _ in range(self.e):
                d = (G % pp) == 0
                if not d.any():
                    break
                v += d
                G = np.where(d, G // pp, G)
        mask = (zero.astype(np.int64) << np.arange(self.L, dtype=np.int64)).sum(axis=-1)
        return mask, v, zero

    def passes(self, F, mlow):
        """Boolean array: True where the candidate may have k distinct integer roots.

        F: uint64 residues (..., L); mlow: proven lower bound m' on the power of x
        dividing each candidate (same leading shape as F without the last axis)."""
        mask, v, zero = self.valuations(F)
        sub = np.maximum(mlow - 1, 0)[..., None] * self.vpn
        S = np.where(zero, 0, v - sub).sum(axis=-1)
        return S >= self.table[mask]
