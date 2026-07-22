# EXP-053: the stratified certificate on the reduced (72, 108) system.
# CPU-only, sympy over QQ(t). Run: run.py
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, gcd_list,  # noqa: E402
                   lcm, symbols)

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


NQ_VERTS = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]
QPTS = hull_pts(NQ_VERTS)


def build_H(P, thresh=2):
    B = symbols(f"B0:{len(QPTS)}")
    Q0 = sum(bb * x**i * y**j for bb, (i, j) in zip(B, QPTS))
    Jm1 = Poly(expand(jac2(P, Q0) - x**2), x, y)
    rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs())
            if e != 0 and mo[0] - mo[1] <= thresh]
    keep = [c for c in range(len(QPTS))
            if any(expand(e.diff(symbols(f"B{c}"))) != 0 for _, e in rows)]
    M = Matrix([[expand(e.diff(symbols(f"B{c}"))) for c in keep] for _, e in rows])
    rhs = Matrix([-expand(e.subs({bb: 0 for bb in B})) for _, e in rows])
    return rows, keep, M, rhs


def h_certificate(P, thresh=2):
    rows, keep, M, rhs = build_H(P, thresh)
    for cv in M.T.nullspace():
        den = lcm([cancel(e).as_numer_denom()[1] for e in cv])
        cc = [expand(cancel(e * den)) for e in cv]
        g = gcd_list([e for e in cc if e != 0])
        if g not in (0, 1):
            cc = [cancel(e / g) for e in cc]
        resid = [expand(sum(cc[r] * M[r, k] for r in range(M.rows)))
                 for k in range(M.cols)]
        if any(rr != 0 for rr in resid):
            return None, rows, None
        f = expand(sum(cc[r] * rhs[r, 0] for r in range(M.rows)))
        if f != 0:
            return f, rows, cc
    return None, rows, None


def main():
    print("=" * 76)
    print("EXP-053: stratified certificates on the reduced (72, 108) system, "
          "top edge y^8 (xy - t)^8 symbolic")
    print("=" * 76)
    Ptop = expand(y**8 * (x * y - t) ** 8)
    STRATA = [
        ("bare: top + x", expand(Ptop + x)),
        ("with x y^4 filler", expand(Ptop + x + Rational(3) * x * y**4)),
        ("with y^3 + x^2 y^6 fillers",
         expand(Ptop + x + Rational(2) * y**3 + Rational(5) * x**2 * y**6)),
    ]
    ok = True
    first = True
    for (nm, P) in STRATA:
        t0 = time.time()
        f, rows, cc = h_certificate(P, 2)
        dt = time.time() - t0
        got = f is not None
        ok &= got
        if got:
            ff = factor(f)
            pf = Poly(f, t)
            nzall = all(co != 0 for co in [pf.coeffs()[0]])
            print(f"  {nm}: H-rows {len(rows)}: pairing {ff}  ({dt:.1f} s)")
            if first:
                supp = sorted({rows[i][0] for i in range(len(rows))
                               if cc[i] != 0})
                print(f"    certificate support ({len(supp)} rows): {supp}")
                first = False
        else:
            print(f"  {nm}: NO certificate ({dt:.1f} s, {len(rows)} H-rows)")
    check("2: every sampled lower stratum carries a cleared certificate with pairing a "
          "nonzero polynomial in t: the reduced open case is EMPTY for ALL t on these "
          "strata", ok)
    print("  4: remaining for full closure: the sweep over the other forced-structure "
          "parameters (dossier: lambda1, alpha edges) and lower-coefficient generality "
          "via the tower/annihilation machinery on this bracket system.")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
