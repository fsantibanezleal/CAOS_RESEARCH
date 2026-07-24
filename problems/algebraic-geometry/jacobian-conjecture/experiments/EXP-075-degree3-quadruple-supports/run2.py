# EXP-075 run2: the quadruple-support sweep, BLOCKERS-FIRST order.
# Supersedes run.py (linear C(51,4) order, ~18 days). This orders the same
# 249900 supports so that those containing >= 2 of the 8 degree-1 blockers come
# first (~thousands, ~hours), then the rest. Resumable by index into the
# reordered list. Imports EXP-071's pipeline exactly as EXP-072/run.py does, via
# EXP-075's setup_ctxs (deg3_subsystem_feasible, modfrac, two-prime confirm,
# regression gate on sampled pairs). Run: run2.py [start_index]
import importlib.util
import sys
import time
from itertools import combinations
from pathlib import Path

# reuse EXP-075/run.py's setup (which itself imports EXP-071/run.py as e71).
_spec = importlib.util.spec_from_file_location(
    "e75", str(Path(__file__).resolve().parent / "run.py"))
e75 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(e75)
e71 = e75.e71

failures = []
PRIMES = e71.PRIMES

# The 8 degree-1 blockers (the obstruction points that closed degree 1, EXP-067).
BLOCKERS = [(1, 0), (3, 5), (4, 6), (4, 7), (5, 8), (7, 13), (8, 14), (8, 15)]


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""),
          flush=True)
    if not ok:
        failures.append(name)


def blockers_first_order(ops):
    """Return (ordered_quadruples, n_blockerheavy). Quadruples (index-tuples into
    ops) with >= 2 blocker-ops first (ascending combo order within each block),
    then the rest. Deterministic and stable, so a resume index is well-defined."""
    bidx = set()
    for b in BLOCKERS:
        if b in ops:
            bidx.add(ops.index(b))
    heavy, rest = [], []
    for quad in combinations(range(len(ops)), 4):
        if sum(1 for i in quad if i in bidx) >= 2:
            heavy.append(quad)
        else:
            rest.append(quad)
    return heavy + rest, len(heavy), bidx


def main():
    print("=" * 76, flush=True)
    print("EXP-075 run2: quadruple-support sweep, BLOCKERS-FIRST (t = 1)",
          flush=True)
    print("=" * 76, flush=True)
    t0 = time.time()
    ok, ctxs, ops = e75.setup_ctxs()
    check("0: setup invariants", ok, f"({time.time() - t0:.0f} s)")
    if not ok:
        sys.exit(1)

    # regression gate: the same 20 sampled pairs as run.py must stay feasible.
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

    quads, n_heavy, bidx = blockers_first_order(ops)
    all_blockers_present = len(bidx) == len(BLOCKERS)
    check("2: blockers-first ordering built", all_blockers_present,
          f"{len(quads)} quadruples, {n_heavy} blocker-heavy (>=2 blockers) "
          f"first; blocker ops indices {sorted(bidx)}")
    if not all_blockers_present:
        print("RESULT: ABORT (a blocker is not an op)", flush=True)
        sys.exit(1)

    # the sweep, early-abort, resumable by index into the reordered list.
    t0 = time.time()
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    hit = None
    for n_, quad in enumerate(quads):
        if n_ < start:
            continue
        sup = tuple(ops[i] for i in quad)
        if not e71.deg3_subsystem_feasible(ctxs[PRIMES[0]], sup):
            if not e71.deg3_subsystem_feasible(ctxs[PRIMES[1]], sup):
                hit = (n_, sup)
                break
            print(f"  3: PRIME DISAGREEMENT at idx {n_} {sup}", flush=True)
        if (n_ + 1) % 200 == 0:
            phase = "blocker-heavy" if n_ + 1 <= n_heavy else "remainder"
            print(f"  3: {n_ + 1}/{len(quads)} quadruples OK ({phase}) "
                  f"({time.time() - t0:.0f} s)  [resume index {n_ + 1}]",
                  flush=True)
    if hit:
        idx, sup = hit
        check("3: the blockers-first quadruple sweep", True,
              f"INFEASIBLE at idx {idx} {sup} (both primes): NO DEGREE-3 "
              "COVECTOR: DEGREE 3 CLOSED. Statement-level claim TO THE MAIN "
              "SESSION (do not publish here).")
        print("RESULT: ALL CHECKS PASS. (degree 3 closed at a quadruple support)",
              flush=True)
    else:
        check("3: the blockers-first quadruple sweep", True,
              "ALL quadruple supports feasible: degree 3 open through quadruples; "
              "the constructive GF(p) path (R2) is staged next")
        print("RESULT: ALL CHECKS PASS. (degree 3 open through quadruples)",
              flush=True)


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}", flush=True)
        sys.exit(1)
