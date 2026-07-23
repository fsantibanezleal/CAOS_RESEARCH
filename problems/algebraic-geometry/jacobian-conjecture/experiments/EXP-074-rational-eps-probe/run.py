# EXP-074: rational-in-eps probe at the 8 blocked operators. t = 1. Run: run.py
import importlib.util, sys, time
from fractions import Fraction
from math import comb
from pathlib import Path
import numpy as np

def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(Path(__file__).resolve().parents[1] / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

e72 = load("e72", "EXP-072-degree2-triple-supports/run.py")
e71 = e72.e71
failures = []

def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""), flush=True)
    if not ok:
        failures.append(name)

BLOCKED = [(1, 0), (3, 5), (4, 6), (4, 7), (5, 8), (7, 13), (8, 14), (8, 15)]

def main():
    print("=" * 76, flush=True)
    print("EXP-074: rational-in-eps probe (t = 1)", flush=True)
    print("=" * 76, flush=True)
    t0 = time.time()
    ok, ctxs, ops = e72.setup_ctxs()
    # b0 = L0 M0 (ncol vector), exact then per-prime
    PT = {(k, 8 + k): Fraction(comb(8, k) * (-1) ** (8 - k)) for k in range(9)}
    PT[(1, 0)] = Fraction(1)
    rows0 = e71.bracket_terms(PT)
    L0spec = {(2, 0): 576, (9, 16): 24, (16, 32): 51, (17, 33): 612, (18, 34): 4148}
    ncol = len(e71.NQ)
    b0 = [Fraction(0)] * ncol
    for r, cols in rows0.items():
        if r in L0spec:
            for c, v in cols.items():
                b0[c] += L0spec[r] * v
    nz = sum(1 for x in b0 if x != 0)
    check("1: setup + gate (b0 computed, nonzero)", ok and nz > 0,
          f"b0 nonzeros {nz} ({time.time() - t0:.0f} s)")
    if not ok or nz == 0:
        sys.exit(1)
    t0 = time.time()
    results = {}
    for pq in BLOCKED:
        verdicts = []
        for prime, ctx in ctxs.items():
            b0p = np.array([e71.modfrac(x, prime) for x in b0], dtype=np.int64)
            B = (ctx.T[pq] @ ctx.N.T) % prime
            rhs = (-(ctx.T[pq] @ ctx.P[pq])) % prime
            M = np.concatenate([B, b0p[:, None], rhs[:, None]], axis=1)
            verdicts.append(e71.modgauss_feasible(M, prime))
        results[pq] = verdicts
        print(f"  2: {pq}: feasible={verdicts}", flush=True)
    still = [pq for pq, v in results.items() if not any(v)]
    opened = [pq for pq, v in results.items() if all(v)]
    mixed = [pq for pq, v in results.items() if any(v) and not all(v)]
    check("2: the 8 relaxed blocks decided", not mixed,
          f"opened {opened}; still blocked {still}; mixed {mixed} "
          f"({time.time() - t0:.0f} s)")
    if still:
        print("  outcome: the rational relaxation does NOT clear "
              f"{still} at this order: those blocks obstruct even rationally "
              "(at order 2); route R3 narrows accordingly.", flush=True)
    elif opened and not still:
        print("  outcome: ALL 8 blocks clear under the d-term freedom: the "
              "rational route is OPEN at order 2; the full rational ladder is "
              "the staged follow-up (higher-order rational conditions).",
              flush=True)
    print("RESULT: " + ("ALL CHECKS PASS." if not failures else
                        f"{len(failures)} FAILED: {failures}"), flush=True)
    if failures:
        sys.exit(1)

if __name__ == "__main__":
    main()
