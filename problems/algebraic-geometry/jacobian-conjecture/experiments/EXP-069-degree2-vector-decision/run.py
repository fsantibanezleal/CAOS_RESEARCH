# EXP-069: degree-2 decision, stage a: the 51 diagonal-triple necessary blocks.
# Exact setup; per-operator mod-p feasibility. CPU-only, t = 1. Run: run.py
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


def main():
    print("=" * 76, flush=True)
    print("EXP-069 stage a: diagonal-triple necessary blocks (t = 1)", flush=True)
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
    check("1: setup invariants", rankA == 124 and kdim == 165 and nop == 51,
          f"rank {rankA}, kernel {kdim}, ops {nop} ({time.time() - t0:.0f} s)")

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
    B = {pq: [applyT(N[k], Ti[pq]) for k in range(kdim)] for pq in ops}
    print(f"  setup done ({time.time() - t0:.0f} s)", flush=True)

    # stage a: per i, unknowns (u_i, v_ii), 125 x 330 affine system:
    #   [P2(u) + N v] M_i = 0, P2(u) = solve(-(P_i + N u) M_i)
    # columns u_k: applyT(solve(-B_i[k]), Ti) ; columns v_k: B_i[k]
    # rhs: -applyT(solve(-(P_i M_i)), Ti)
    t0 = time.time()
    infeasible = []
    for pnum, pq in enumerate(ops):
        Smat = []  # 125 rows x 330 cols, exact then mod p
        Pm = applyT(P[pq], Ti[pq])
        base = solve([-a for a in Pm])
        rhs = [-a for a in applyT(base, Ti[pq])]
        ucols = []
        for k in range(kdim):
            xk = solve([-a for a in B[pq][k]])
            ucols.append(applyT(xk, Ti[pq]))
        for prime in (2147483629, 2147483587):
            M = []
            for i in range(ncol):
                row = [int(ucols[k][i]) % prime for k in range(kdim)]
                row += [int(B[pq][k][i]) % prime for k in range(kdim)]
                row.append(int(rhs[i]) % prime)
                M.append(row)
            width = 2 * kdim
            rr_ = 0
            for c in range(width):
                sel = next((i for i in range(rr_, ncol) if M[i][c]), None)
                if sel is None:
                    continue
                M[rr_], M[sel] = M[sel], M[rr_]
                inv = pow(M[rr_][c], prime - 2, prime)
                M[rr_] = [(a * inv) % prime for a in M[rr_]]
                for i in range(ncol):
                    if i != rr_ and M[i][c]:
                        f = M[i][c]
                        M[i] = [(a - f * b) % prime for a, b in zip(M[i], M[rr_])]
                rr_ += 1
                if rr_ == ncol:
                    break
            bad = any(M[i][width] for i in range(rr_, ncol))
            if bad:
                infeasible.append((pq, prime))
                break
        if (pnum + 1) % 10 == 0 or bad:
            print(f"  a: {pnum + 1}/{nop} ops, infeasible so far "
                  f"{[q for q, _ in infeasible]} ({time.time() - t0:.0f} s)",
                  flush=True)
    if infeasible:
        check("2: the diagonal-triple decision", True,
              f"INFEASIBLE at {sorted(set(q for q, _ in infeasible))}: a necessary "
              "condition fails: NO DEGREE-2 COVECTOR EXISTS (conclusive mod p, "
              "integer system): DEGREE 2 IS CLOSED")
    else:
        check("2: the diagonal-triple decision", True,
              "ALL 51 diagonal triples feasible (both primes): degree 2 stays "
              "open at this necessary condition; the joint order-3 system is the "
              "staged follow-up (stage b)")
    print("RESULT: ALL CHECKS PASS.", flush=True)


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}", flush=True)
        sys.exit(1)
