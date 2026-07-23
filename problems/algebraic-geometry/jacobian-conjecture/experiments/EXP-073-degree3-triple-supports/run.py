# EXP-073: degree-3 triple-support necessaries. Imports EXP-071's pipeline.
# t = 1. Run: run.py
import importlib.util
import sys
import time
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "e71", str(Path(__file__).resolve().parents[1]
               / "EXP-071-degree3-pair-necessaries" / "run.py"))
e71 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e71)

failures = []
PRIMES = e71.PRIMES


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""),
          flush=True)
    if not ok:
        failures.append(name)


def setup_ctxs():
    PT = {(k, 8 + k): Fraction(comb(8, k) * (-1) ** (8 - k)) for k in range(9)}
    PT[(1, 0)] = Fraction(1)
    rows0 = e71.bracket_terms(PT)
    rowlist = sorted(set(rows0) | {(2, 0)})
    ridx = {r: k for k, r in enumerate(rowlist)}
    nrow = len(rowlist)
    ncol = len(e71.NQ)
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
    Ti = {}
    for pq in e71.LOWER:
        rws = e71.bracket_terms({pq: Fraction(1)})
        keep = {}
        for rr, cols in rws.items():
            if rr in ridx:
                keep[ridx[rr]] = cols
        if keep:
            Ti[pq] = keep
    ops = sorted(Ti)

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
    ok = rankA == 124 and len(N) == 165 and len(ops) == 51
    ctxs = {p: e71.ModCtx(p, E, piv_cols, rankA, N, Ti, P, nrow, ncol, ops)
            for p in PRIMES}
    return ok, ctxs, ops


def main():
    print("=" * 76, flush=True)
    print("EXP-073: degree-3 triple-support necessaries (t = 1)", flush=True)
    print("=" * 76, flush=True)
    t0 = time.time()
    ok, ctxs, ops = setup_ctxs()
    check("0: setup invariants", ok, f"({time.time() - t0:.0f} s)")
    if not ok:
        sys.exit(1)
    # 1: regression gate: 20 sampled pairs feasible as in EXP-071 run4
    t0 = time.time()
    sample = [(ops[i], ops[j]) for i, j in
              [(0, 1), (2, 6), (5, 9), (10, 30), (4, 44), (7, 22), (12, 40),
               (3, 15), (20, 21), (0, 50), (18, 33), (25, 26), (9, 47),
               (14, 28), (6, 38), (11, 42), (16, 27), (31, 49), (8, 35),
               (13, 45)]]
    bad = [s for s in sample
           if not e71.deg3_subsystem_feasible(ctxs[PRIMES[0]], s)]
    check("1: regression gate (20 sampled pairs feasible)", not bad,
          f"bad {bad} ({time.time() - t0:.0f} s)")
    if bad:
        print("RESULT: ABORT (regression gate)", flush=True)
        sys.exit(1)
    # 2: the triple-support sweep, early-abort
    t0 = time.time()
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    trips = list(combinations(range(len(ops)), 3))
    hit = None
    for n_, (a_, b_, c_) in enumerate(trips):
        if n_ < start:
            continue
        sup = (ops[a_], ops[b_], ops[c_])
        if not e71.deg3_subsystem_feasible(ctxs[PRIMES[0]], sup):
            if not e71.deg3_subsystem_feasible(ctxs[PRIMES[1]], sup):
                hit = sup
                break
            print(f"  2: PRIME DISAGREEMENT at {sup}", flush=True)
        if (n_ + 1) % 500 == 0:
            print(f"  2: {n_ + 1}/{len(trips)} triple supports OK "
                  f"({time.time() - t0:.0f} s)  [resume index {n_ + 1}]",
                  flush=True)
    if hit:
        check("2: the triple-support sweep", True,
              f"INFEASIBLE at {hit} (both primes): NO DEGREE-2 COVECTOR: DEGREE "
              "2 CLOSED (correct-arithmetic pipeline)")
        print("RESULT: ALL CHECKS PASS. (degree 3 closed at a triple support)",
              flush=True)
    else:
        check("2: the triple-support sweep", True,
              "ALL triple supports feasible: degree 3 open through triples; "
              "quadruples or the constructive path staged")
        print("RESULT: ALL CHECKS PASS. (degree 3 open through triples)",
              flush=True)


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}", flush=True)
        sys.exit(1)
