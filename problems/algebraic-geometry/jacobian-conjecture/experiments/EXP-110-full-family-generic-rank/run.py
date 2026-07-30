# EXP-110: generic rank of the FULL 51-parameter GGHV reduced family.
# Reuses the canonical construction from EXP-071 (hull, bracket_terms, pool).
# Exact arithmetic only. Run: run.py
import importlib.util
import json
import random
import sys
import time
from fractions import Fraction
from math import comb
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
E71 = HERE.parents[0] / "EXP-071-degree3-pair-necessaries" / "run.py"
spec = importlib.util.spec_from_file_location("e71", str(E71))
e71 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e71)

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""),
          flush=True)
    if not ok:
        failures.append(name)


def build_pool():
    """The canonical reduced construction (EXP-064/067/071): forced top edge
    P_T = y^8(xy-1)^8 + x, bracket against the Q-polygon, restricted to the pool."""
    PT = {(k, 8 + k): Fraction(comb(8, k) * (-1) ** (8 - k)) for k in range(9)}
    PT[(1, 0)] = Fraction(1)
    rows0 = e71.bracket_terms(PT)
    rowlist = sorted(set(rows0) | {(2, 0)})
    ridx = {r: k for k, r in enumerate(rowlist)}
    ncol = len(e71.NQ)
    return PT, rows0, rowlist, ridx, ncol


def main():
    print("=" * 78, flush=True)
    print("EXP-110: generic rank of the FULL 51-parameter reduced family", flush=True)
    print("=" * 78, flush=True)
    t0 = time.time()

    PT, rows0, rowlist, ridx, ncol = build_pool()
    nrow = len(rowlist)
    LOWER = e71.LOWER
    print(f"  pool: {ncol} output columns (Q-polygon lattice points), "
          f"{nrow} pool rows; {len(LOWER)} lower-family directions", flush=True)
    check("1: the reduced construction builds with the recorded shape",
          ncol == 125 and len(LOWER) == 51,
          f"ncol={ncol} (expect 125), |LOWER|={len(LOWER)} (expect 51) "
          f"({time.time() - t0:.0f} s)")

    # M(eps): the FULL family. P = P_T + sum eps_i * monomial_i over the 51 lower
    # directions. The bracket [P,Q]'s coefficient map on Q's coefficients is
    # linear, so M(eps) = M_0 + sum eps_i M_i with M_i = bracket_terms({pq_i:1}).
    ops = sorted(LOWER)

    def matrix_at(vals):
        """M(eps) as an ncol x nrow exact matrix at the given parameter values."""
        terms = dict(PT)
        for pq, v in zip(ops, vals):
            if v:
                terms[pq] = terms.get(pq, Fraction(0)) + Fraction(v)
        rows = e71.bracket_terms(terms)
        M = sp.zeros(ncol, nrow)
        for r, cols in rows.items():
            if r in ridx:
                for c, val in cols.items():
                    M[c, ridx[r]] = sp.Rational(val)
        return M

    # P5 invariant-first: ONE random rational specialisation decides genericity.
    # rank is lower semicontinuous, so full rank at a single point PROVES the
    # generic rank over Q(eps) is full.
    print("\n  probing a random rational parameter point (invariant-first)...",
          flush=True)
    random.seed(20260726)
    results = {}
    best = 0
    for trial in range(3):
        vals = [Fraction(random.randint(-9, 9), random.randint(1, 5))
                for _ in ops]
        t1 = time.time()
        M = matrix_at(vals)
        r = M.rank()
        best = max(best, r)
        print(f"    trial {trial + 1}: rank = {r} of max {min(M.rows, M.cols)} "
              f"({time.time() - t1:.0f} s)", flush=True)
        results[f"trial{trial + 1}"] = {"rank": r, "shape": [M.rows, M.cols]}

    maxrank = min(ncol, nrow)
    check("2: generic rank is maximal over the full 51-parameter family",
          best == maxrank,
          f"best observed rank {best}, max possible {maxrank}")

    # Also record the rank of the constant term M_0 for contrast (EXP-064 recorded
    # rank 124 of 125 on the pinned pool; that is the eps = 0 point).
    M0 = matrix_at([0] * len(ops))
    r0 = M0.rank()
    print(f"\n  contrast: rank at eps = 0 (the pinned point) = {r0}", flush=True)

    out = {
        "ncol": ncol, "nrow": nrow, "n_params": len(ops),
        "generic_rank_observed": best, "max_possible": maxrank,
        "rank_at_eps_zero": r0, "trials": results,
    }
    (HERE / "artifacts").mkdir(exist_ok=True)
    (HERE / "artifacts" / "results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")

    print("\n  READING:", flush=True)
    if best == maxrank and r0 < maxrank:
        print("    The family has MAXIMAL generic rank while the pinned point eps=0", flush=True)
        print("    is rank-deficient. So the rank drop that the whole certificate", flush=True)
        print("    programme studies is a PROPER CLOSED condition, and the residual", flush=True)
        print("    stratum is exactly where the maximal minors vanish.", flush=True)
        print("    Next exact target (ONE computation for the whole family, not", flush=True)
        print("    C(51,k) slices): the ideal of maximal minors, or a witnessing", flush=True)
        print("    minor and its zero locus.", flush=True)
    elif best < maxrank:
        print("    GENERIC RANK IS DEFICIENT: a kernel exists over Q(eps).", flush=True)
        print("    That is a global covector over the function field: MAJOR.", flush=True)
        print("    Report to Felipe before any claim; verify exactly.", flush=True)

    print(f"\nRESULT: {'ALL CHECKS PASS.' if not failures else str(len(failures)) + ' FAILED: ' + str(failures)}",
          flush=True)
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
