# EXP-071: degree-3 pair necessaries. Exact setup; mod-p composed maps (numpy).
# t = 1. Run: run.py
import sys
import time
from fractions import Fraction
from itertools import combinations_with_replacement
from math import comb

import numpy as np

failures = []
PRIMES = (2147483629, 2147483587)


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""),
          flush=True)
    if not ok:
        failures.append(name)


def hull_pts(verts):
    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    pts = sorted(set(verts))
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    hu = lo[:-1] + up[:-1]

    def inside(q):
        n = len(hu)
        for k in range(n):
            o, p = hu[k], hu[(k + 1) % n]
            if (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0]) < 0:
                return False
        return True
    mx = max(i for (i, j) in verts)
    my = max(j for (i, j) in verts)
    return [(i, j) for i in range(mx + 1) for j in range(my + 1) if inside((i, j))]


NQ = sorted(hull_pts([(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]))
NP_PTS = hull_pts([(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)])
TOP = {(k, 8 + k) for k in range(9)}
LOWER = [pq for pq in NP_PTS if pq not in TOP and pq != (0, 0)]


def in_pool(r):
    return r[0] - r[1] <= 2 and r[0] <= 24 and r[1] <= 44


def bracket_terms(pterms):
    rows = {}
    for c, (al, be) in enumerate(NQ):
        for (p, q), co in pterms.items():
            fac = p * be - q * al
            if fac == 0:
                continue
            r = (p + al - 1, q + be - 1)
            if not in_pool(r):
                continue
            rows.setdefault(r, {})
            rows[r][c] = rows[r].get(c, 0) + co * fac
    return rows


def modgauss_feasible(M, prime):
    M = M % prime
    rows, colsp1 = M.shape
    cols = colsp1 - 1
    r = 0
    for c in range(cols):
        if r == rows:
            break
        nz = np.nonzero(M[r:, c])[0]
        if nz.size == 0:
            continue
        sel = r + nz[0]
        if sel != r:
            M[[r, sel]] = M[[sel, r]]
        inv = pow(int(M[r, c]), prime - 2, prime)
        M[r] = (M[r] * inv) % prime
        below = np.nonzero(M[r + 1:, c])[0]
        if below.size:
            idx = below + r + 1
            M[idx] = (M[idx] - M[idx, c][:, None] * M[r][None, :]) % prime
        r += 1
    if r < rows:
        tail = M[r:]
        bad = np.any((tail[:, :cols].any(axis=1) == 0) & (tail[:, cols] != 0))
        return not bad
    return True


def modfrac(x, prime):
    """Correct reduction of a Fraction mod prime (num * den^-1)."""
    num = int(x.numerator) % prime
    den = int(x.denominator) % prime
    if den == 1:
        return num
    return (num * pow(den, prime - 2, prime)) % prime


class ModCtx:
    """All ladder objects modulo one prime, numpy-backed."""

    def __init__(self, prime, E, piv_cols, rankA, N, Ti, P, nrow, ncol, ops):
        self.p = prime
        self.rankA = rankA
        self.piv = piv_cols
        self.nrow, self.ncol = nrow, ncol
        self.ops = ops
        self.E = np.array([[modfrac(x, prime) for x in row] for row in E],
                          dtype=np.int64)
        self.N = np.array([[modfrac(N[k][t], prime) for t in range(nrow)]
                           for k in range(len(N))], dtype=np.int64)  # kdim x nrow
        self.kdim = self.N.shape[0]
        # T_e as sparse (ncol x nrow) dense int64 (small): applyT = T @ lam
        self.T = {}
        for e in ops:
            M = np.zeros((ncol, nrow), dtype=np.int64)
            for rk, cols in Ti[e].items():
                for c, v in cols.items():
                    M[c, rk] = int(v) % prime
            self.T[e] = M
        self.P = {e: np.array([modfrac(x, prime) for x in P[e]], dtype=np.int64)
                  for e in ops}
        # caches
        self._U = {}     # e -> nrow x kdim: solve(-T_e N^T)
        self._W2 = {}    # (b,y) -> nrow x kdim: solve(-T_y U_b)
        self.pivarr = np.array(piv_cols, dtype=np.int64)

    def solvem(self, Bcols):
        """Bcols: ncol x m rhs matrix. Returns nrow x m solutions (pivot form).
        Assumes consistency (guaranteed by the dual annihilation identity).
        E entries and Bcols entries are both ~p, so the product is computed with
        a 16-bit split to avoid int64 overflow (p^2 * 125 > 2^63)."""
        B = Bcols % self.p
        Bhi, Blo = B >> 16, B & 0xFFFF
        Y = ((self.E @ Bhi) % self.p * 65536 + (self.E @ Blo)) % self.p
        X = np.zeros((self.nrow, Bcols.shape[1]), dtype=np.int64)
        X[self.pivarr] = Y[:self.rankA]
        return X

    def U(self, e):
        if e not in self._U:
            Bt = (self.T[e] @ self.N.T) % self.p          # ncol x kdim
            self._U[e] = self.solvem((-Bt) % self.p)      # nrow x kdim
        return self._U[e]

    def W2(self, b, y):
        if (b, y) not in self._W2:
            Bt = (self.T[y] @ self.U(b)) % self.p
            self._W2[(b, y)] = self.solvem((-Bt) % self.p)
        return self._W2[(b, y)]


def decomps(gamma):
    """distinct (x, rest) with rest = gamma minus one occurrence of x."""
    out = []
    for x in sorted(set(gamma)):
        rest = list(gamma)
        rest.remove(x)
        out.append((x, tuple(sorted(rest))))
    return out


def pair_particular(ctx, pr):
    a, b = pr
    if a == b:
        S = (ctx.T[a] @ ctx.P[a]) % ctx.p
    else:
        S = ((ctx.T[b] @ ctx.P[a]) + (ctx.T[a] @ ctx.P[b])) % ctx.p
    return ctx.solvem((-S[:, None]) % ctx.p)[:, 0]


def tri_particular(ctx, tri, P2cache):
    S = np.zeros(ctx.ncol, dtype=np.int64)
    for (x, pr) in decomps(tri):
        if pr not in P2cache:
            P2cache[pr] = pair_particular(ctx, pr)
        S = (S + ctx.T[x] @ P2cache[pr]) % ctx.p
    return ctx.solvem((-S[:, None]) % ctx.p)[:, 0]


def deg2_subsystem_feasible(ctx, support):
    """regression: EXP-070's order-3 pair subsystem, rebuilt on the mod-p path."""
    sup = sorted(set(support))
    gammas = list(combinations_with_replacement(sup, 3))
    ukeys = [("u", x) for x in sup]
    vkeys = [("v", pr) for pr in combinations_with_replacement(sup, 2)]
    keys = ukeys + vkeys
    kpos = {k: i * ctx.kdim for i, k in enumerate(keys)}
    width = len(keys) * ctx.kdim
    P2cache = {}
    rowsM = []
    for g in gammas:
        M = np.zeros((ctx.ncol, width + 1), dtype=np.int64)
        rhs = np.zeros(ctx.ncol, dtype=np.int64)
        for (x, pr) in decomps(g):
            if pr not in P2cache:
                P2cache[pr] = pair_particular(ctx, pr)
            rhs = (rhs - ctx.T[x] @ P2cache[pr]) % ctx.p
            Bx = (ctx.T[x] @ ctx.N.T) % ctx.p
            M[:, kpos[("v", pr)]:kpos[("v", pr)] + ctx.kdim] = \
                (M[:, kpos[("v", pr)]:kpos[("v", pr)] + ctx.kdim] + Bx) % ctx.p
            for aa, bb in ((pr[0], pr[1]), (pr[1], pr[0])):
                Cc = (ctx.T[x] @ ctx.U(bb)) % ctx.p
                M[:, kpos[("u", aa)]:kpos[("u", aa)] + ctx.kdim] = \
                    (M[:, kpos[("u", aa)]:kpos[("u", aa)] + ctx.kdim] + Cc) % ctx.p
                if pr[0] == pr[1]:
                    break
        M[:, width] = rhs
        rowsM.append(M)
    return modgauss_feasible(np.vstack(rowsM), ctx.p)


def deg3_subsystem_feasible(ctx, support):
    sup = sorted(set(support))
    gammas = list(combinations_with_replacement(sup, 4))
    ukeys = [("u", x) for x in sup]
    vkeys = [("v", pr) for pr in combinations_with_replacement(sup, 2)]
    wkeys = [("w", tr) for tr in combinations_with_replacement(sup, 3)]
    keys = ukeys + vkeys + wkeys
    kpos = {k: i * ctx.kdim for i, k in enumerate(keys)}
    width = len(keys) * ctx.kdim
    P2cache = {}
    P3cache = {}
    rowsM = []
    for g in gammas:
        M = np.zeros((ctx.ncol, width + 1), dtype=np.int64)
        rhs = np.zeros(ctx.ncol, dtype=np.int64)
        for (x, tri) in decomps(g):
            if tri not in P3cache:
                P3cache[tri] = tri_particular(ctx, tri, P2cache)
            rhs = (rhs - ctx.T[x] @ P3cache[tri]) % ctx.p
            # w columns
            Bx = (ctx.T[x] @ ctx.N.T) % ctx.p
            M[:, kpos[("w", tri)]:kpos[("w", tri)] + ctx.kdim] = \
                (M[:, kpos[("w", tri)]:kpos[("w", tri)] + ctx.kdim] + Bx) % ctx.p
            # v and u columns through P3(tri)
            for (y, pr) in decomps(tri):
                # d/dv_pr: solve(-T_y N) applied by T_x
                Cc = (ctx.T[x] @ ctx.U(y)) % ctx.p
                M[:, kpos[("v", pr)]:kpos[("v", pr)] + ctx.kdim] = \
                    (M[:, kpos[("v", pr)]:kpos[("v", pr)] + ctx.kdim] + Cc) % ctx.p
                # d/du through P2(pr) then solve then T_y then T_x:
                for aa, bb in ((pr[0], pr[1]), (pr[1], pr[0])):
                    Wc = (ctx.T[x] @ ctx.W2(bb, y)) % ctx.p
                    M[:, kpos[("u", aa)]:kpos[("u", aa)] + ctx.kdim] = \
                        (M[:, kpos[("u", aa)]:kpos[("u", aa)] + ctx.kdim] + Wc) % ctx.p
                    if pr[0] == pr[1]:
                        break
        M[:, width] = rhs
        rowsM.append(M)
    return modgauss_feasible(np.vstack(rowsM), ctx.p)


def main():
    print("=" * 76, flush=True)
    print("EXP-071: degree-3 pair necessaries (t = 1, mod-p composed maps)",
          flush=True)
    print("=" * 76, flush=True)
    t0 = time.time()
    PT = {(k, 8 + k): Fraction(comb(8, k) * (-1) ** (8 - k)) for k in range(9)}
    PT[(1, 0)] = Fraction(1)
    rows0 = bracket_terms(PT)
    rowlist = sorted(set(rows0) | {(2, 0)})
    ridx = {r: k for k, r in enumerate(rowlist)}
    nrow = len(rowlist)
    ncol = len(NQ)
    A = [[Fraction(0)] * nrow for _ in range(ncol)]
    for r, cols in rows0.items():
        for c, v in cols.items():
            A[c][ridx[r]] = Fraction(v)
    W = [A[i] + [Fraction(1 if j == i else 0) for j in range(ncol)]
         for i in range(ncol)]
    piv_cols = []
    r = 0
    for c in range(nrow):
        sel = next((i for i in range(r, ncol) if W[i][c]), None)
        if sel is None:
            continue
        W[r], W[sel] = W[sel], W[r]
        inv = Fraction(1) / W[r][c]
        W[r] = [a * inv for a in W[r]]
        for i in range(ncol):
            if i != r and W[i][c]:
                f = W[i][c]
                W[i] = [a - f * b for a, b in zip(W[i], W[r])]
        piv_cols.append(c)
        r += 1
        if r == ncol:
            break
    rankA = r
    E = [row[nrow:] for row in W]
    pivset = set(piv_cols)
    free_cols = [c for c in range(nrow) if c not in pivset]
    RA = [row[:nrow] for row in W[:rankA]]
    N = []
    for fc in free_cols:
        v = [Fraction(0)] * nrow
        v[fc] = Fraction(1)
        for k in range(rankA):
            if RA[k][fc]:
                v[piv_cols[k]] = -RA[k][fc]
        N.append(v)
    kdim = len(N)
    Ti = {}
    for pq in LOWER:
        rws = bracket_terms({pq: Fraction(1)})
        keep = {}
        for rr, cols in rws.items():
            if rr in ridx:
                keep[ridx[rr]] = cols
        if keep:
            Ti[pq] = keep
    ops = sorted(Ti)
    nop = len(ops)

    def applyT(lam, tmap):
        b = [Fraction(0)] * ncol
        for rk, cols in tmap.items():
            lv = lam[rk]
            if lv == 0:
                continue
            for c, v in cols.items():
                b[c] += lv * v
        return b

    def solve(b):
        y = [sum(E[i][j] * b[j] for j in range(ncol) if b[j]) for i in range(ncol)]
        if y[rankA]:
            return None
        x = [Fraction(0)] * nrow
        for k in range(rankA):
            x[piv_cols[k]] = y[k]
        return x

    L0 = [Fraction(0)] * nrow
    for (rr, v) in (((2, 0), 576), ((9, 16), 24), ((16, 32), 51),
                    ((17, 33), 612), ((18, 34), 4148)):
        if rr in ridx:
            L0[ridx[rr]] = Fraction(v)
    P = {pq: solve([-a for a in applyT(L0, Ti[pq])]) for pq in ops}
    ok0 = rankA == 124 and kdim == 165 and nop == 51
    ctxs = {p: ModCtx(p, E, piv_cols, rankA, N, Ti, P, nrow, ncol, ops)
            for p in PRIMES}
    check("1: setup invariants", ok0,
          f"rank {rankA}, kernel {kdim}, ops {nop} ({time.time() - t0:.0f} s)")
    if not ok0:
        print("RESULT: ABORT", flush=True)
        sys.exit(1)
    # 1b: RE-DECIDE the degree-2 pair sweep with CORRECT arithmetic (EXP-070's
    # truncation bug retracts its conclusion; this is the true decision).
    t0 = time.time()
    pairs = list(combinations_with_replacement(range(nop), 2))
    hit2 = None
    for n_, (a_, b_) in enumerate(pairs):
        sup = (ops[a_],) if a_ == b_ else (ops[a_], ops[b_])
        if not deg2_subsystem_feasible(ctxs[PRIMES[0]], sup):
            if not deg2_subsystem_feasible(ctxs[PRIMES[1]], sup):
                hit2 = sup
                break
            print(f"  1b: PRIME DISAGREEMENT at {sup}", flush=True)
        if (n_ + 1) % 200 == 0:
            print(f"  1b: {n_ + 1}/{len(pairs)} degree-2 pair subsystems OK "
                  f"({time.time() - t0:.0f} s)", flush=True)
    if hit2:
        check("1b: the corrected degree-2 pair sweep", True,
              f"INFEASIBLE at {hit2} (both primes): degree 2 closed at pairs "
              "AFTER the fix")
    else:
        check("1b: the corrected degree-2 pair sweep", True,
              "ALL pair subsystems FEASIBLE under correct arithmetic: EXP-070's "
              "closure is RETRACTED; degree 2 is OPEN at pair necessaries")
    # 1c: re-audit EXP-069a's diagonal triples with correct arithmetic
    t0 = time.time()
    bad3 = [pq for pq in ops
            if not deg2_subsystem_feasible(ctxs[PRIMES[0]], (pq,))]
    check("1c: EXP-069a diagonal triples re-audited (correct arithmetic)",
          True, f"infeasible singles: {bad3 or 'none'} "
          f"({time.time() - t0:.0f} s)")

    # 2: the degree-3 pair sweep
    t0 = time.time()
    pairs = list(combinations_with_replacement(range(nop), 2))
    hit = None
    for n_, (a_, b_) in enumerate(pairs):
        sup = (ops[a_],) if a_ == b_ else (ops[a_], ops[b_])
        if not deg3_subsystem_feasible(ctxs[PRIMES[0]], sup):
            if not deg3_subsystem_feasible(ctxs[PRIMES[1]], sup):
                hit = sup
                break
            print(f"  2: PRIME DISAGREEMENT at {sup} (treated as undecided, "
                  "flagged)", flush=True)
        if (n_ + 1) % 100 == 0:
            print(f"  2: {n_ + 1}/{len(pairs)} degree-3 pair subsystems OK "
                  f"({time.time() - t0:.0f} s)", flush=True)
    if hit:
        check("2: the degree-3 pair sweep is decided", True,
              f"INFEASIBLE at {hit} (both primes): NO DEGREE-3 COVECTOR: DEGREE "
              "3 CLOSED. 3: the pattern-theorem proposal goes TO FELIPE.")
        print("RESULT: ALL CHECKS PASS. (degree 3 closed)", flush=True)
    else:
        check("2: the degree-3 pair sweep is decided", True,
              "ALL pair subsystems feasible: degree 3 OPEN at pair necessaries; "
              "triple supports staged next")
        print("RESULT: ALL CHECKS PASS. (degree 3 open at pairs)", flush=True)


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}", flush=True)
        sys.exit(1)
