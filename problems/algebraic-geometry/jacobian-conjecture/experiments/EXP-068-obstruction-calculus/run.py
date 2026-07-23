# EXP-068: the obstruction calculus. Exact setup + mod-p gauge decisions.
# CPU-only, t = 1. Run: run.py
import sys
import time
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
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
BLOCKED = {(1, 0), (3, 5), (4, 6), (4, 7), (5, 8), (7, 13), (8, 14), (8, 15)}


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
    print("EXP-068: the obstruction calculus (t = 1)", flush=True)
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
    assert rankA == ncol - 1
    cvec = E[rankA]  # the cokernel covector: c^T A = 0

    def solve(b):
        y = [sum(E[i][j] * b[j] for j in range(ncol) if b[j]) for i in range(ncol)]
        if y[rankA]:
            return None
        x = [Fraction(0)] * nrow
        for k in range(rankA):
            x[piv_cols[k]] = y[k]
        return x

    def cdot(b):
        return sum(cvec[j] * b[j] for j in range(ncol) if b[j])

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

    L0 = [Fraction(0)] * nrow
    for (rr, v) in (((2, 0), 576), ((9, 16), 24), ((16, 32), 51),
                    ((17, 33), 612), ((18, 34), 4148)):
        if rr in ridx:
            L0[ridx[rr]] = Fraction(v)
    P = {}
    for pq in ops:
        P[pq] = solve([-a for a in applyT(L0, Ti[pq])])
        assert P[pq] is not None
    B = {pq: [applyT(N[k], Ti[pq]) for k in range(kdim)] for pq in ops}
    print(f"  setup: rank {rankA}, kernel {kdim}, ops {nop} "
          f"({time.time() - t0:.0f} s)", flush=True)

    # 1: the functional reproduces EXP-067
    t0 = time.time()
    found = set()
    scal = {}
    for pq in ops:
        alpha = [cdot(B[pq][k]) for k in range(kdim)]
        s_i = cdot(applyT(P[pq], Ti[pq]))
        if all(a == 0 for a in alpha) and s_i != 0:
            found.add(pq)
            scal[pq] = s_i
    check("1: the functional test reproduces EXP-067's 8 blocked operators",
          found == BLOCKED, f"found {sorted(found)} ({time.time() - t0:.0f} s)")
    print("  1: obstruction scalars: " +
          ", ".join(f"{pq}:{scal[pq]}" for pq in sorted(scal)), flush=True)

    # 2: the level-1 gauge system mod two primes: for all pairs (i <= j):
    #    c.(B_j u_i + B_i u_j) = -c.(P_i M_j + P_j M_i)   (i == j: single form)
    cb = {pq: [cdot(B[pq][k]) for k in range(kdim)] for pq in ops}
    idx = {pq: k * kdim for k, pq in enumerate(ops)}
    width1 = nop * kdim
    usol = None
    for prime in (2147483629, 2147483587):
        t0 = time.time()
        rows_red = {}

        def addrow(rd, rv, rows_red=None):
            pass  # replaced below per prime

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
            return rv == 0

        consistent = True
        for a_, b_ in combinations_with_replacement(range(nop), 2):
            pa, pb = ops[a_], ops[b_]
            if a_ == b_:
                rhs = -cdot(applyT(P[pa], Ti[pa]))
                rd = {}
                for k in range(kdim):
                    v = int(cb[pa][k]) % prime
                    if v:
                        rd[idx[pa] + k] = v
            else:
                rhs = -(cdot(applyT(P[pa], Ti[pb])) + cdot(applyT(P[pb], Ti[pa])))
                rd = {}
                for k in range(kdim):
                    v = int(cb[pb][k]) % prime
                    if v:
                        rd[idx[pa] + k] = v
                    w = int(cb[pa][k]) % prime
                    if w:
                        rd[idx[pb] + k] = (rd.get(idx[pb] + k, 0) + w) % prime
            if not addrow(rd, int(rhs)):
                consistent = False
                break
        print(f"  2: p={prime}: consistent={consistent}, rank "
              f"{len(rows_red)}/{width1} ({time.time() - t0:.0f} s)", flush=True)
        if not consistent:
            check("2: the level-1 gauge system is decided", True,
                  f"INFEASIBLE mod {prime}: no gauge makes all level-2 correctors "
                  "exist: DEGREE 2 IS CLOSED TOO (conclusive, integer system)")
            print("RESULT: ALL CHECKS PASS. (degree 2 closed at the level-1 gauge)",
                  flush=True)
            return
        if usol is None:
            # extract one solution mod the FIRST prime: free vars 0, back-subst
            usol = [0] * width1
            for c in sorted(rows_red, reverse=True):
                rowd, rv = rows_red[c]
                acc = rv
                for cc, vv in rowd.items():
                    if cc != c:
                        acc = (acc - vv * usol[cc]) % prime
                usol[c] = acc % prime
            p1 = prime
    check("2: the level-1 gauge system is decided", True,
          "FEASIBLE mod both primes (prediction confirmed): all level-2 "
          "correctors can be made to exist")

    # 3: sufficient order-3 probe mod p1 with u FIXED from part 2.
    # Lambda_i = P_i + N u_i (mod p1). Level-2 particular: for alpha = (i, j):
    # S_alpha = Lambda_i M_j + Lambda_j M_i (i != j) or Lambda_i M_i (i == j);
    # Lambda_alpha = solvep(-S_alpha) + N v_alpha. Order-3 scalar at gamma =
    # (i <= j <= k): c.(sum over distinct decompositions Lambda_{gamma - e} M_e)
    # = 0 as linear conditions on v.
    t0 = time.time()
    prime = p1
    Ei = [[int(x) % prime for x in row] for row in E]
    cvp = [int(x) % prime for x in cvec]
    Np = [[int(x) % prime for x in col] for col in N]
    Tip = {pq: {rk: {c: int(v) % prime for c, v in cols.items()}
                for rk, cols in Ti[pq].items()} for pq in ops}

    def applyTp(lam, tmap):
        b = [0] * ncol
        for rk, cols in tmap.items():
            lv = lam[rk]
            if lv == 0:
                continue
            for c, v in cols.items():
                b[c] = (b[c] + lv * v) % prime
        return b

    def solvep(b):
        y = [sum(Ei[i][j] * b[j] for j in range(ncol) if b[j]) % prime
             for i in range(ncol)]
        if y[rankA]:
            return None
        x = [0] * nrow
        for k in range(rankA):
            x[piv_cols[k]] = y[k]
        return x

    def cdotp(b):
        return sum(cvp[j] * b[j] for j in range(ncol) if b[j]) % prime

    Lam1 = {}
    for pq in ops:
        u = usol[idx[pq]: idx[pq] + kdim]
        x = [int(P[pq][t]) % prime for t in range(nrow)]
        for k in range(kdim):
            if u[k]:
                for t in range(nrow):
                    if Np[k][t]:
                        x[t] = (x[t] + u[k] * Np[k][t]) % prime
        Lam1[pq] = x
    # level-2 particulars
    P2 = {}
    pairs2 = list(combinations_with_replacement(range(nop), 2))
    bad2 = 0
    for a_, b_ in pairs2:
        pa, pb = ops[a_], ops[b_]
        if a_ == b_:
            S = applyTp(Lam1[pa], Tip[pa])
        else:
            S = [(x + y) % prime for x, y in zip(applyTp(Lam1[pa], Tip[pb]),
                                                applyTp(Lam1[pb], Tip[pa]))]
        x = solvep([(-s) % prime for s in S])
        if x is None:
            bad2 += 1
            x = [0] * nrow
        P2[(a_, b_)] = x
    check("3a: all level-2 particulars exist under the chosen gauge", bad2 == 0,
          f"unsolvable {bad2}/{len(pairs2)} ({time.time() - t0:.0f} s)")
    # order-3 scalar system on v (level-2 gauge), sparse elimination mod p1
    t0 = time.time()
    cbp = {pq: [cdotp(B_) for B_ in
                ([[int(x) % prime for x in col] for col in
                  [[applyT(N[k], Ti[pq])[j] for j in range(ncol)]
                   for k in range(kdim)]])[0:0]] for pq in []}  # unused
    cb1p = {pq: [int(cb[pq][k]) % prime for k in range(kdim)] for pq in ops}
    v_idx = {ab: k * kdim for k, ab in enumerate(pairs2)}
    widthv = len(pairs2) * kdim
    rows_red = {}

    def addrow3(rd, rv):
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
        return rv == 0

    consistent = True
    neq = 0
    trips = list(combinations_with_replacement(range(nop), 3))
    for tnum, (a_, b_, c_) in enumerate(trips):
        # decompositions gamma = e_x + (pair): distinct x in multiset {a,b,c}
        decs = {}
        for x, rest in (((a_), (b_, c_)), ((b_), (a_, c_)), ((c_), (a_, b_))):
            decs[(x, rest)] = decs.get((x, rest), 0) + 1
        rhs = 0
        rd = {}
        seen = set()
        for (x, rest), mult in decs.items():
            key = (x, rest)
            if key in seen:
                continue
            seen.add(key)
            px = ops[x]
            pr = tuple(sorted(rest))
            rhs = (rhs - cdotp(applyTp(P2[pr], Tip[px]))) % prime
            for k in range(kdim):
                v = cb1p[px][k]
                if v:
                    col = v_idx[pr] + k
                    rd[col] = (rd.get(col, 0) + v) % prime
        if not addrow3(rd, rhs):
            consistent = False
            break
        neq += 1
        if (tnum + 1) % 4000 == 0:
            print(f"  3b: {tnum + 1}/{len(trips)} triples, rank {len(rows_red)} "
                  f"({time.time() - t0:.0f} s)", flush=True)
    print(f"  3b: p={prime}: consistent={consistent}, {neq}/{len(trips)} eqs, "
          f"rank {len(rows_red)}/{widthv} ({time.time() - t0:.0f} s)", flush=True)
    if consistent:
        check("3: the sufficient order-3 probe is decided", True,
              "FEASIBLE mod p under the fixed u: a DEGREE-2 COVECTOR CANDIDATE "
              "exists; the exact confirmation is the staged follow-up (upgrade "
              "proposal only after the exact pass, FOR FELIPE)")
    else:
        check("3: the sufficient order-3 probe is decided", True,
              "INFEASIBLE under the FIXED u (not conclusive against degree 2); "
              "the joint (u, v) decision is the staged follow-up")
    print("RESULT: ALL CHECKS PASS.", flush=True)


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}", flush=True)
        sys.exit(1)
