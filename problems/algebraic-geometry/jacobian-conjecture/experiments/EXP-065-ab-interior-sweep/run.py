# EXP-065: the a/b interior sweep (hardening 1b).
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
    print("EXP-065: the a/b interior sweep (chart a1 = 1, a0 = 2)")
    print("=" * 76)
    import time as _t
    from sympy import symbols as _sym
    ee = _sym("epsN")
    npts = hull_pts([(0, 0), (1, 0), (8, 14), (8, 16)])
    corners = {(0, 0), (1, 0), (8, 14), (8, 15), (8, 16)}
    interior = [pq for pq in npts if pq not in corners]
    print(f"  interior points: {len(interior)}")
    bad = []
    t0 = _t.time()
    for pq in interior:
        P = expand(x + redge(Rational(2), 1) + ee * x**pq[0] * y**pq[1])
        f, nr = h_certificate(P)
        got = f is not None
        if not got:
            bad.append(pq)
        print(f"  1: interior ({pq[0]},{pq[1]}): pairing "
              f"{factor(f) if got else 'NONE'}  [{_t.time() - t0:.0f} s]")
    check("1: EVERY a/b interior point admits a one-symbol certificate with nonzero "
          "polynomial pairing", not bad, f"{len(interior)} points, failures {bad}")
    print("  2: with EXP-063, hardening task 1 is COMPLETE on both polygon families; "
          "the simultaneous statement remains gated on EXP-064.")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
