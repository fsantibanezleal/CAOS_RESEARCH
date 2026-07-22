# EXP-056: the order-2 corrector ladder + termination test.
# CPU-only, sympy over QQ(t). Run: run.py
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from sympy import (Matrix, Rational, binomial, expand, linsolve, symbols,  # noqa: E402
                   zeros)

failures = []
t = symbols("t")


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
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


NP_PTS = hull_pts([(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)])
NQ = sorted(hull_pts([(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]))
TOP = {(k, 8 + k) for k in range(9)}
LOWER = [pq for pq in NP_PTS if pq not in TOP]
PTOP = {(k, 8 + k): binomial(8, k) * (-t) ** (8 - k) for k in range(9)}
PTOP[(1, 0)] = Rational(1)
LAM0 = {(2, 0): Rational(576), (9, 16): Rational(24), (16, 32): Rational(51),
        (17, 33): 612 * t, (18, 34): 4148 * t**2}


def apply_left(lam, pterms):
    """Covector (dict row->val) times the matrix of P-monomials: dict col->val."""
    out = {}
    for c, qm in enumerate(NQ):
        v = 0
        for pm, co in pterms.items():
            (p, q) = pm
            (al, be) = qm
            fac = p * be - q * al
            if fac == 0:
                continue
            row = (p + al - 1, q + be - 1)
            if row in lam:
                v += lam[row] * co * fac
        if v != 0:
            v = expand(v)
            if v != 0:
                out[c] = v
    return out


def solve_batch(rhs_cols, rows_pool, label):
    """Solve lam^T M0 = rhs for each rhs column; returns list of covector dicts."""
    rowlist = sorted(rows_pool)
    ridx = {r: k for k, r in enumerate(rowlist)}
    A = zeros(len(NQ), len(rowlist))
    for c, qm in enumerate(NQ):
        for pm, co in PTOP.items():
            (p, q) = pm
            (al, be) = qm
            fac = p * be - q * al
            if fac == 0:
                continue
            row = (p + al - 1, q + be - 1)
            if row in ridx:
                A[c, ridx[row]] += co * fac
    U = symbols(f"u0:{len(rowlist)}")
    sols = []
    for rhs in rhs_cols:
        eqs = []
        for c in range(len(NQ)):
            e = sum(U[k] * A[c, k] for k in range(len(rowlist)) if A[c, k] != 0)
            e = e - rhs.get(c, 0)
            if e != 0:
                eqs.append(expand(e))
        if (2, 0) in ridx:
            eqs.append(U[ridx[(2, 0)]])
        sol = linsolve(eqs, list(U))
        if not sol:
            sols.append(None)
            continue
        vec = list(sol)[0]
        free = vec.free_symbols & set(U)
        vec = [v.subs({f: 0 for f in free}) for v in vec]
        sols.append({rowlist[k]: expand(vec[k]) for k in range(len(rowlist))
                     if expand(vec[k]) != 0})
    return sols


def rows_pool_for(offset_monos, depth):
    pool = set(LAM0)
    frontier = set(LAM0)
    for _ in range(depth):
        newf = set()
        for (i, j) in frontier:
            for (p, q) in offset_monos:
                r = (i - p + 1, j - q + 1)
                if r[0] >= 0 and r[1] >= 0:
                    newf.add(r)
                for pm in PTOP:
                    r2 = (r[0] + pm[0] - 1, r[1] + pm[1] - 1)
                    if r2[0] >= 0 and r2[1] >= 0:
                        newf.add(r2)
        pool |= newf
        frontier = newf
    return {r for r in pool if r[0] - r[1] <= 2 and r[0] <= 24 and r[1] <= 44}


def main():
    print("=" * 76)
    print("EXP-056: order-2 correctors + order-3 termination test")
    print("=" * 76)
    t0 = time.time()
    Mi = {}
    for pq in LOWER:
        r = apply_left(LAM0, {pq: Rational(1)})
        if r:
            Mi[pq] = {c: expand(-v) for c, v in r.items()}
    entering = sorted(Mi)
    pool = rows_pool_for(entering, 2)
    print(f"  entering monomials {len(entering)}; row pool {len(pool)}")
    sols = solve_batch([Mi[pq] for pq in entering], pool, "order1")
    LAMi = dict(zip(entering, sols))
    n1 = sum(1 for v in LAMi.values() if v is not None)
    dt = time.time() - t0
    check("1: first-order correctors recomputed and persisted", n1 == len(entering),
          f"{n1}/{len(entering)} in {dt:.0f} s")
    (Path(__file__).parent / "artifacts" / "lambda1-2026-07-22.txt").write_text(
        "\n".join(f"{pq}: {LAMi[pq]}" for pq in entering))
    # order-2 residuals over ALL pairs
    t0 = time.time()
    import itertools
    rhs2 = {}
    for pi, pj in itertools.combinations_with_replacement(entering, 2):
        v = {}
        for (a_, b_) in (((pi), (pj)), ((pj), (pi))):
            la = LAMi[a_]
            if la is None:
                continue
            r = apply_left(la, {b_: Rational(1)})
            for c, val in r.items():
                v[c] = expand(v.get(c, 0) + val)
        v = {c: -val for c, val in v.items() if expand(val) != 0}
        if v:
            rhs2[(pi, pj)] = v
    print(f"  order-2: {len(rhs2)}/{sum(1 for _ in itertools.combinations_with_replacement(entering, 2))} "
          f"pairs need correctors ({time.time() - t0:.0f} s)")
    t0 = time.time()
    keys2 = sorted(rhs2)
    sols2 = solve_batch([rhs2[k] for k in keys2], pool, "order2")
    LAM2 = dict(zip(keys2, sols2))
    n2 = sum(1 for v in LAM2.values() if v is not None)
    check("2: ALL nonzero order-2 pairs admit correctors with the (2,0)-pin",
          n2 == len(keys2), f"{n2}/{len(keys2)} in {time.time() - t0:.0f} s")
    # order-3 residuals on the triples generated by corrected pairs (sampled fully
    # over pairs-with-correctors x entering)
    t0 = time.time()
    bad3 = 0
    tested = 0
    for (pi, pj) in keys2:
        lam = LAM2[(pi, pj)]
        if lam is None:
            continue
        for pk in entering:
            v = {}
            r = apply_left(lam, {pk: Rational(1)})
            for c, val in r.items():
                v[c] = expand(v.get(c, 0) + val)
            for (a_, b_) in ((pi, pj), (pj, pi)):
                # cross terms Lambda_{a,k} M_b contribute at the same order; include
                key = tuple(sorted((a_, pk)))
                lam_ak = LAM2.get(key)
                if lam_ak:
                    r2 = apply_left(lam_ak, {b_: Rational(1)})
                    for c, val in r2.items():
                        v[c] = expand(v.get(c, 0) + val)
            nz = any(expand(val) != 0 for val in v.values())
            tested += 1
            if nz:
                bad3 += 1
    print(f"  order-3: {tested} triple combinations tested, {bad3} nonzero "
          f"({time.time() - t0:.0f} s)")
    check("3: order-3 residuals VANISH (termination at order 2: the UNIVERSAL covector "
          "is explicit and the stratum closes)", bad3 == 0,
          f"{tested - bad3}/{tested}")
    if bad3:
        print("  4: ladder profile recorded; order-3 correctors are the next rung "
              "(same mechanism).")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
