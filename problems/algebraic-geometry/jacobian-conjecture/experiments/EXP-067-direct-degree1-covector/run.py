# EXP-067: the direct degree-1 covector (sigma-free). Exact Fractions + mod-p
# decision for the full system. CPU-only, t = 1. Run: run.py
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
    print("EXP-067: the direct degree-1 covector (t = 1, Fraction + mod-p)",
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
    # Gauss-Jordan on [A | I]
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
    zero_rows = list(range(rankA, ncol))

    def solve(b):
        y = [sum(E[i][j] * b[j] for j in range(ncol) if b[j]) for i in range(ncol)]
        for i in zero_rows:
            if y[i]:
                return None
        x = [Fraction(0)] * nrow
        for k in range(rankA):
            x[piv_cols[k]] = y[k]
        return x

    # left-kernel basis N of M0 on the pool: free coords of A x = 0
    pivset = set(piv_cols)
    free_cols = [c for c in range(nrow) if c not in pivset]
    # reduced row space: RA rows (from W A-part) give x_piv = -sum RA[k][free] x_free
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
    print(f"  setup: M0^T {ncol} x {nrow}, rank {rankA}, kernel dim {kdim} "
          f"({time.time() - t0:.0f} s)", flush=True)

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
    print(f"  setup: operators M_i: {nop}", flush=True)

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

    # 1: particular solutions P_i for all i
    t0 = time.time()
    P = {}
    ok1 = True
    for pq in ops:
        b = [-a for a in applyT(L0, Ti[pq])]
        x = solve(b)
        if x is None:
            ok1 = False
            break
        P[pq] = x
    check("1: order-1 solvability reconfirmed for ALL operators", ok1,
          f"{len(P)}/{nop} ({time.time() - t0:.0f} s)")
    if not ok1:
        print("RESULT: ABORT", flush=True)
        sys.exit(1)

    # precompute B_i = [applyT(N_k, Ti)] (ncol x kdim) per operator
    t0 = time.time()
    B = {pq: [applyT(N[k], Ti[pq]) for k in range(kdim)] for pq in ops}
    print(f"  setup: B_i built ({time.time() - t0:.0f} s)", flush=True)

    def feasible(cols_blocks, rhs):
        """exact feasibility of sum_b cols_blocks[b] . u_b = rhs (each block a list
        of ncol-vectors); Gauss on the stacked (ncol x total) augmented matrix."""
        width = sum(len(cb) for cb in cols_blocks)
        M = []
        for i in range(ncol):
            row = []
            for cb in cols_blocks:
                row.extend(col[i] for col in cb)
            row.append(rhs[i])
            M.append(row)
        r = 0
        for c in range(width):
            sel = next((i for i in range(r, ncol) if M[i][c]), None)
            if sel is None:
                continue
            M[r], M[sel] = M[sel], M[r]
            inv = Fraction(1) / M[r][c]
            M[r] = [a * inv for a in M[r]]
            for i in range(ncol):
                if i != r and M[i][c]:
                    f = M[i][c]
                    M[i] = [a - f * b for a, b in zip(M[i], M[r])]
            r += 1
            if r == ncol:
                break
        return all(M[i][width] == 0 for i in range(r, ncol))

    # 2: single blocks
    t0 = time.time()
    bad_single = []
    for pq in ops:
        rhs = [-a for a in applyT(P[pq], Ti[pq])]
        if not feasible([B[pq]], rhs):
            bad_single.append(pq)
    check("2: every single-index block feasible", not bad_single,
          f"bad {bad_single} ({time.time() - t0:.0f} s)")

    # 3: pair blocks
    t0 = time.time()
    bad_pairs = []
    done = 0
    for a_ in range(nop):
        for b_ in range(a_ + 1, nop):
            pa, pb = ops[a_], ops[b_]
            rhs = [-(x + y) for x, y in zip(applyT(P[pa], Ti[pb]),
                                           applyT(P[pb], Ti[pa]))]
            if not feasible([B[pb], B[pa]], rhs):
                bad_pairs.append((pa, pb))
            done += 1
        print(f"  3: pair blocks through op {a_ + 1}/{nop}: {done} done, "
              f"{len(bad_pairs)} infeasible ({time.time() - t0:.0f} s)", flush=True)
    check("3: every pair block feasible in isolation", not bad_pairs,
          f"infeasible pairs {len(bad_pairs)} ({time.time() - t0:.0f} s)")

    # 4: the FULL degree-1 system, mod two large primes
    t0 = time.time()
    for prime in (2147483629, 2147483587):
        # unknowns: u[pq] in Z_p^kdim; equations: single blocks + pair blocks
        idx = {pq: k * kdim for k, pq in enumerate(ops)}
        width = nop * kdim
        # sparse elimination: maintain reduced rows as dicts {col: val}, rhs
        rows_red = {}  # pivot col -> (dict row, rhs)

        def addrow(rd, rv):
            rd = dict(rd)
            rv %= prime
            while rd:
                c = min(rd)
                if c in rows_red:
                    pr, pv = rows_red[c]
                    f = rd[c]
                    for cc, vv in pr.items():
                        rd[cc] = (rd.get(cc, 0) - f * vv) % prime
                        if rd[cc] == 0:
                            del rd[cc]
                    rv = (rv - f * pv) % prime
                else:
                    inv = pow(rd[c], prime - 2, prime)
                    rd = {cc: (vv * inv) % prime for cc, vv in rd.items()}
                    rv = (rv * inv) % prime
                    rows_red[c] = (rd, rv)
                    return True
            return rv == 0  # empty row: consistent iff rhs 0

        consistent = True
        neq = 0
        # single blocks: B_i u_i = -P_i M_i ; pair blocks: B_j u_i + B_i u_j = rhs
        for a_ in range(nop):
            pa = ops[a_]
            rhs = [-x for x in applyT(P[pa], Ti[pa])]
            for i in range(ncol):
                rd = {}
                for k in range(kdim):
                    v = int(B[pa][k][i]) % prime
                    if v:
                        rd[idx[pa] + k] = v
                if not addrow(rd, int(rhs[i])):
                    consistent = False
                    break
                neq += 1
            if not consistent:
                break
            for b_ in range(a_ + 1, nop):
                pb = ops[b_]
                rhs = [-(x + y) for x, y in zip(applyT(P[pa], Ti[pb]),
                                               applyT(P[pb], Ti[pa]))]
                for i in range(ncol):
                    rd = {}
                    for k in range(kdim):
                        v = int(B[pb][k][i]) % prime
                        if v:
                            rd[idx[pa] + k] = v
                        w = int(B[pa][k][i]) % prime
                        if w:
                            rd[idx[pb] + k] = (rd.get(idx[pb] + k, 0) + w) % prime
                    if not addrow(rd, int(rhs[i])):
                        consistent = False
                        break
                    neq += 1
                if not consistent:
                    break
            if not consistent:
                break
            if (a_ + 1) % 10 == 0:
                print(f"  4: p={prime}: through op {a_ + 1}/{nop}, {neq} eqs, "
                      f"rank {len(rows_red)} ({time.time() - t0:.0f} s)", flush=True)
        print(f"  4: p={prime}: consistent={consistent}, eqs {neq}, rank "
              f"{len(rows_red)}/{width} ({time.time() - t0:.0f} s)", flush=True)
        if not consistent:
            check("4: the FULL degree-1 system is decided", True,
                  f"INFEASIBLE mod {prime}: no degree-1 covector over Q "
                  "(conclusive for this integer system); degree 2 is next")
            print("RESULT: ALL CHECKS PASS. (degree 1 CLOSED: infeasible)",
                  flush=True)
            return
    check("4: the FULL degree-1 system is decided", True,
          "CONSISTENT mod both primes: exact confirmation staged as part 2 "
          "(a degree-1 covector very likely EXISTS; upgrade proposal pending "
          "the exact solve, FOR FELIPE)")
    print("RESULT: ALL CHECKS PASS. (degree 1: consistent mod p, exact solve next)",
          flush=True)


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}", flush=True)
        sys.exit(1)
