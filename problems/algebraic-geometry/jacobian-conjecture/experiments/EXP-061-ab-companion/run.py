# EXP-061: the a/b companion (Prop 4.3 sub-polygon cases).
# CPU-only, sympy. Run: run.py
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, gcd_list,  # noqa: E402
                   lcm, symbols)

failures = []
a0, a1 = symbols("a0 a1")


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


NQ_AB = sorted(hull_pts([(0, 0), (2, 1), (12, 21), (12, 24)]))


def h_certificate(P):
    B = symbols(f"B0:{len(NQ_AB)}")
    Q0 = sum(bb * x**i * y**j for bb, (i, j) in zip(B, NQ_AB))
    Jm1 = Poly(expand(jac2(P, Q0) - x**2), x, y)
    rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs())
            if e != 0 and mo[0] - mo[1] <= 2]
    keep = [c for c in range(len(NQ_AB))
            if any(expand(e.diff(B[c])) != 0 for _, e in rows)]
    M = Matrix([[expand(e.diff(B[c])) for c in keep] for _, e in rows])
    rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for _, e in rows])
    for cv in M.T.nullspace():
        den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
        cc = [expand(cancel(e * den)) for e in cv]
        g = gcd_list([e for e in cc if e != 0])
        if g not in (0, 1):
            cc = [cancel(e / g) for e in cc]
        resid = [expand(sum(cc[r] * M[r, k] for r in range(M.rows)))
                 for k in range(M.cols)]
        if any(rr != 0 for rr in resid):
            return None, len(rows)
        f = expand(sum(cc[r] * rhs[r, 0] for r in range(M.rows)))
        if f != 0:
            return f, len(rows)
    return None, len(rows)


def redge(u0, u1):
    return expand(x**8 * y**14 * (u0 + u1 * y) ** 2)


def main():
    print("=" * 76)
    print("EXP-061: the a/b companion (sub-polygon cases of Prop 4.3)")
    print("=" * 76)
    npts = hull_pts([(0, 0), (1, 0), (8, 14), (8, 16)])
    print(f"  P-polygon lattice points: {len(npts)}; Q-polygon: {len(NQ_AB)}")
    # 1: chart a1 = 1
    ok = True
    for (nm, Padd) in (("bare", 0),
                       ("interior sample 1", Rational(2) * x**4 * y**7),
                       ("interior sample 2",
                        Rational(3) * x**2 * y**4 - x**6 * y**11)):
        t0 = time.time()
        P = expand(x + redge(a0, 1) + Padd)
        f, nr = h_certificate(P)
        dt = time.time() - t0
        got = f is not None
        ok &= got
        print(f"  1: chart a1=1, {nm}: pairing "
              f"{factor(f) if got else 'NONE'} ({nr} H-rows, {dt:.0f} s)")
    check("1: chart a1 = 1 certificates exist (bare + two interior samples), pairing "
          "nonzero polynomial in a0", ok)
    # 2: chart a0 = 1
    t0 = time.time()
    P = expand(x + redge(1, a1))
    f, nr = h_certificate(P)
    dt = time.time() - t0
    ok2 = f is not None
    print(f"  2: chart a0=1, bare: pairing {factor(f) if ok2 else 'NONE'} ({dt:.0f} s)")
    check("2: chart a0 = 1 certificate exists, pairing nonzero polynomial in a1", ok2)
    print("  3: locus vs stratum: adjudicated in the verdict from the printed "
          "factorizations (R nonzero excludes a0 = a1 = 0; each chart's pairing "
          "covers the other's gauge boundary).")
    print("  4: assembly: with EXP-060 (case c) these certificates cover all three "
          "Prop 4.3 branches on their forced families (interior at sampled "
          "generality; free-coefficient upgrade + orientation swap queued).")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
