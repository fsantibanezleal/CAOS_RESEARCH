"""EXP-015 engine: every additive nine-gate candidate, decided without a window.

A depth-7 frontier state is a row of 7 polynomial ids; with the inputs -1, 1, x
it gives 10 operands. The eighth gate t is any of the 200 operations on them
(55 sums, 55 products, 90 ordered differences); the ninth gate is f = t + b or
f = t - b for one of the 10 operands b. This is the candidate space of EXP-013.

Stages (all sound; a candidate is dropped only when it provably has fewer than k
distinct integer roots, or is identically zero):

1. degree: f has degree at most max(deg t, deg b) (deg t is exact for products
   and at most the max for sums and differences); below k it cannot have k
   distinct roots.
2. 2-adic layer (tclib.padic, p = 2, 16 points, residues mod 2^64), with the
   proven lower bound m' on the power of x dividing f (the minimum of the
   operands' trailing indices; their sum for a product).
3. 3-adic layer (p = 3, 9 points, residues mod 3^20) on the survivors.
4. A survivor whose residues vanish at every point of both layers is tested for
   f == 0 EXACTLY (built from the exact operands), cached by operand ids.
5. Every other survivor is built exactly and its distinct integer roots are
   counted (rational root theorem, tclib.enum.integer_roots).

Residues, degrees and trailing indices of the operands come from the tables
written by residues.py (re-checked there against exact evaluation).
"""
import numpy as np

from tclib.enum import integer_roots, padd, pmul, psub
from tclib.padic import Layer

WIDTH = 7
NOPS = 10


def build_pairs(n=NOPS):
    ai, aj, si, sj = [], [], [], []
    for i in range(n):
        for j in range(i, n):
            ai.append(i); aj.append(j)
    for i in range(n):
        for j in range(n):
            if i != j:
                si.append(i); sj.append(j)
    # One operand-index pair per eighth gate, and its kind: 0 sum, 1 product, 2 difference.
    left = np.array(ai + ai + si)
    right = np.array(aj + aj + sj)
    kind = np.array([0] * len(ai) + [1] * len(ai) + [2] * len(si))
    return left, right, kind


LEFT, RIGHT, KIND = build_pairs()
NEXT = len(KIND)  # 200
INPUTS = np.array([0, 1, 2], dtype=np.int64)  # polynomial ids of -1, 1, x


class Engine:
    def __init__(self, polys, tables, k):
        self.polys = polys
        self.val2, self.val3, self.deg, self.tz = tables
        self.k = k
        self.l2 = Layer(2, 4, 64, k)
        self.l3 = Layer(3, 2, 20, k)
        self.zero_cache = {}      # (kind, a, c, b, sign) -> True when f == 0
        self.stats = dict(states=0, candidates=0, deg_drop=0, pass2=0, pass3=0,
                          zero_suspect=0, zero_exact=0, exact=0, hits=0)

    @staticmethod
    def _gate(layer, kind, A, C):
        out = np.empty_like(A)
        for code, fn in ((0, layer.add), (1, layer.mul), (2, layer.sub)):
            m = kind == code
            if m.any():
                out[m] = fn(A[m], C[m])
        return out

    def scan(self, rows):
        """Scan a batch of frontier rows (B, 7). Returns up to 50 hit records (>= k roots)."""
        B = rows.shape[0]
        ids = np.concatenate([np.tile(INPUTS, (B, 1)), rows.astype(np.int64)], axis=1)  # (B, 10)
        D = self.deg[ids].astype(np.int64)
        T = self.tz[ids].astype(np.int64)
        Ed = np.where(KIND == 1, D[:, LEFT] + D[:, RIGHT], np.maximum(D[:, LEFT], D[:, RIGHT]))
        Et = np.where(KIND == 1, T[:, LEFT] + T[:, RIGHT], np.minimum(T[:, LEFT], T[:, RIGHT]))
        alive = np.maximum(Ed[:, :, None], D[:, None, :]) >= self.k                     # (B, 200, 10)
        self.stats["states"] += B
        self.stats["candidates"] += 2 * B * NEXT * NOPS
        bi, ei, oi = np.nonzero(alive)
        self.stats["deg_drop"] += 2 * (B * NEXT * NOPS - len(bi))
        hits = []
        if not len(bi):
            return hits
        a_ids, c_ids, b_ids = ids[bi, LEFT[ei]], ids[bi, RIGHT[ei]], ids[bi, oi]
        kind = KIND[ei]
        mlow = np.minimum(Et[bi, ei], T[bi, oi])
        with np.errstate(over="ignore"):
            t2 = self._gate(self.l2, kind, self.val2[a_ids], self.val2[c_ids])
            t3 = self._gate(self.l3, kind, self.val3[a_ids], self.val3[c_ids])
            b2, b3 = self.val2[b_ids], self.val3[b_ids]
            for sign in (1, -1):
                F2 = self.l2.add(t2, b2) if sign == 1 else self.l2.sub(t2, b2)
                s2 = np.nonzero(self.l2.passes(F2, mlow))[0]
                self.stats["pass2"] += len(s2)
                if not len(s2):
                    continue
                F3 = self.l3.add(t3[s2], b3[s2]) if sign == 1 else self.l3.sub(t3[s2], b3[s2])
                ok3 = self.l3.passes(F3, mlow[s2])
                sel = s2[ok3]
                self.stats["pass3"] += len(sel)
                full = (F2[sel] == 0).all(axis=1) & (F3[ok3] == 0).all(axis=1)
                for q, is_full in zip(sel, full):
                    self._decide(int(kind[q]), int(a_ids[q]), int(c_ids[q]), int(b_ids[q]), sign,
                                 bool(is_full), rows[bi[q]], int(ei[q]), int(oi[q]), hits)
        return hits

    def _decide(self, kd, a_id, c_id, b_id, sign, is_full, row, e_, o_, hits):
        if is_full:
            self.stats["zero_suspect"] += 1
            key = (kd, a_id, c_id, b_id, sign)
            z = self.zero_cache.get(key)
            if z:
                return
            f = self._build(kd, a_id, c_id, b_id, sign)
            if z is None and len(self.zero_cache) < 2_000_000:
                self.zero_cache[key] = not f
            if not f:
                return
        else:
            f = self._build(kd, a_id, c_id, b_id, sign)
            if not f:
                self.stats["zero_exact"] += 1
                return
        self.stats["exact"] += 1
        R = integer_roots(f)
        if len(R) >= self.k:
            self.stats["hits"] += 1
            if len(hits) < 50:
                hits.append({"state": [int(x) for x in row], "gate8": e_, "operand": o_,
                             "sign": "+" if sign == 1 else "-", "roots": sorted(int(r) for r in R),
                             "f": [int(c) for c in f] if len(f) <= 140 else None})

    def _build(self, kd, a_id, c_id, b_id, sign):
        a, c, b = self.polys[a_id], self.polys[c_id], self.polys[b_id]
        t = padd(a, c) if kd == 0 else pmul(a, c) if kd == 1 else psub(a, c)
        if not t:
            return t
        return padd(t, b) if sign == 1 else psub(t, b)


def load_tables(assets):
    return tuple(np.load(assets / f"res_{n}.npy", mmap_mode="r") for n in ("val2", "val3", "deg", "tz"))
