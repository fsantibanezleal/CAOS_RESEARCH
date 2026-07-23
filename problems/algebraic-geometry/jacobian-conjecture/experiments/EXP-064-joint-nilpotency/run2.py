# EXP-064 run2: the SAME declared computation (hypothesis.md, 2026-07-22), re-staged
# after the sympy run exceeded the cap with no flushed output. Changes are purely
# operational: exact Fraction arithmetic on plain lists (no sympy Matrix), an
# incremental-elimination span reducer replacing repeated rank() calls, and
# flushed per-step progress prints. The mathematics is unchanged.
# CPU-only, exact over Q at t = 1. Run: run2.py
import sys
import time
from fractions import Fraction
from math import comb

failures = []


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
    """rows dict: row -> {col: coeff} for [sum pterms, col-monomial]."""
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


class Reducer:
    """Incremental exact row-space reducer: holds a reduced basis; add() reduces a
    vector against it and absorbs a nonzero remainder, returning True if new."""

    def __init__(self, n):
        self.n = n
        self.rows = {}  # pivot index -> normalized vector (list of Fraction)

    def reduce(self, v):
        v = list(v)
        for p, row in self.rows.items():
            if v[p]:
                c = v[p]
                v = [a - c * b for a, b in zip(v, row)]
        return v

    def add(self, v):
        v = self.reduce(v)
        for p in range(self.n):
            if v[p]:
                inv = Fraction(1) / v[p]
                v = [a * inv for a in v]
                self.rows[p] = v
                return True
        return False

    @property
    def dim(self):
        return len(self.rows)


def main():
    print("=" * 76, flush=True)
    print("EXP-064 run2: termination as joint nilpotency (t = 1, Fraction backend)",
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
    # A = M0^T (ncol x nrow): A[c][k] = coeff of column-monomial c in pool row k
    A = [[Fraction(0)] * nrow for _ in range(ncol)]
    for r, cols in rows0.items():
        for c, v in cols.items():
            A[c][ridx[r]] = Fraction(v)
    print(f"  A: stage A built: M0^T is {ncol} x {nrow} ({time.time() - t0:.0f} s)",
          flush=True)
    # Gauss-Jordan on [A | I] with full transform
    t0 = time.time()
    W = [A[i] + [Fraction(1 if j == i else 0) for j in range(ncol)]
         for i in range(ncol)]
    piv_cols = []
    r = 0
    for c in range(nrow):
        sel = None
        for i in range(r, ncol):
            if W[i][c]:
                sel = i
                break
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
    zero_rows = list(range(rankA, ncol))
    print(f"  A: Gauss-Jordan done: rank {rankA}, {len(zero_rows)} consistency rows "
          f"({time.time() - t0:.0f} s)", flush=True)

    def solve(b):
        # y = E b; consistency on zero rows; particular solution via pivot columns
        y = [sum(E[i][j] * b[j] for j in range(ncol) if b[j]) for i in range(ncol)]
        for i in zero_rows:
            if y[i]:
                return None
        x = [Fraction(0)] * nrow
        for k in range(rankA):
            x[piv_cols[k]] = y[k]
        return x

    # T_i operators as row-dicts on the pool
    Ti = {}
    for pq in LOWER:
        rws = bracket_terms({pq: Fraction(1)})
        keep = {}
        for rr, cols in rws.items():
            if rr in ridx:
                keep[ridx[rr]] = cols
        if keep:
            Ti[pq] = keep
    print(f"  A: operators A_i: {len(Ti)}", flush=True)

    def applyT(lam, tmap):
        b = [Fraction(0)] * ncol
        for rk, cols in tmap.items():
            lv = lam[rk]
            if lv == 0:
                continue
            for c, v in cols.items():
                b[c] += lv * v
        return b

    L0 = [Fraction(0)] * nrow
    for (rr, v) in (((2, 0), 576), ((9, 16), 24), ((16, 32), 51),
                    ((17, 33), 612), ((18, 34), 4148)):
        if rr in ridx:
            L0[ridx[rr]] = Fraction(v)
    # 1: spot check on one first-order corrector
    pq0 = LOWER[0]
    ok1 = True
    if pq0 in Ti:
        b = [-a for a in applyT(L0, Ti[pq0])]
        x = solve(b)
        ok1 = x is not None
        if ok1:
            resid = [sum(A[i][j] * x[j] for j in range(nrow) if x[j]) - b[i]
                     for i in range(ncol)]
            ok1 = all(v == 0 for v in resid)
    check("1: the transform-based right-inverse solves and verifies a first-order "
          "corrector", ok1)
    # 2: Krylov closure of L0 under the A_i, incremental reducer
    t0 = time.time()
    red = Reducer(nrow)
    red.add(L0)
    basis = [L0]
    frontier = [L0]
    it = 0
    aborted = False
    while frontier and it < 60 and not aborted:
        it += 1
        newf = []
        for lam in frontier:
            for pq, tmap in Ti.items():
                b = [-a for a in applyT(lam, tmap)]
                if all(v == 0 for v in b):
                    continue
                x = solve(b)
                if x is None:
                    check("2: solvability inside the Krylov iteration", False,
                          f"unsolvable at {pq}")
                    aborted = True
                    break
                if any(v != 0 for v in x) and red.add(x):
                    basis.append(x)
                    newf.append(x)
            if aborted:
                break
        frontier = newf
        print(f"  2: Krylov iteration {it}: dim {red.dim} "
              f"({time.time() - t0:.0f} s)", flush=True)
        if red.dim > 400:
            break
    if aborted:
        print("RESULT: ABORT", flush=True)
        return
    dimV = red.dim
    check("2: the Krylov closure computed and bounded", 0 < dimV <= 400,
          f"dim {dimV}, iterations {it}")
    # 3: descending chain W_{k+1} = sum_i A_i W_k from V_inf
    t0 = time.time()
    Wb = basis
    step = 0
    while Wb and step < dimV + 2:
        step += 1
        redW = Reducer(nrow)
        newW = []
        for lam in Wb:
            for pq, tmap in Ti.items():
                b = [-a for a in applyT(lam, tmap)]
                if all(v == 0 for v in b):
                    continue
                x = solve(b)
                if x is None:
                    check("3: solvability in the chain", False, str(pq))
                    print("RESULT: ABORT", flush=True)
                    return
                if any(v != 0 for v in x) and redW.add(x):
                    newW.append(x)
        print(f"  3: chain step {step}: dim {len(newW)} ({time.time() - t0:.0f} s)",
              flush=True)
        if newW and len(newW) == len(Wb):
            # possible stabilization: is span(newW) == span(Wb)?
            redO = Reducer(nrow)
            for v_ in Wb:
                redO.add(v_)
            if all(not redO.add(v_) for v_ in newW):
                check("3: the descending chain reaches ZERO (joint nilpotency)",
                      False, f"STABILIZED NONZERO at dim {len(newW)}")
                print("  outcome: THIS sigma's ladder does not terminate; re-pin or "
                      "chart covers next (recorded).", flush=True)
                print(f"RESULT: {len(failures)} FAILED: {failures}", flush=True)
                sys.exit(1)
        Wb = newW
    check("3: the descending chain reaches ZERO (joint nilpotency): TERMINATION "
          "PROVED with order bound K", not Wb, f"K = {step}")
    print("  4: assembly: with 3, the polynomial covector Lambda(eps) exists for ALL "
          "interior coefficients simultaneously at t = 1 (all t != 0 by the gauge); "
          "the statement upgrade goes BACK TO FELIPE.", flush=True)


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}", flush=True)
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.", flush=True)
