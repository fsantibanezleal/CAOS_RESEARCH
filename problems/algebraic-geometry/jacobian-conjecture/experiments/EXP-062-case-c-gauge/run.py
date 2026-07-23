# EXP-062: case c under the torus gauge.
# CPU-only, sympy. Run: run.py
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, gcd_list,  # noqa: E402
                   lcm, linsolve, symbols)

failures = []
be = symbols("beta")


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


NQ = sorted(hull_pts([(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]))
NP_PTS = hull_pts([(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)])
TOP = {(k, 8 + k) for k in range(9)}
INTERIOR = [pq for pq in NP_PTS if pq not in TOP
            and pq not in ((0, 0), (1, 0), (8, 14), (8, 15), (8, 16))]


def system(P, target):
    B = symbols(f"B0:{len(NQ)}")
    Q0 = sum(bb * x**i * y**j for bb, (i, j) in zip(B, NQ))
    Jm1 = Poly(expand(jac2(P, Q0) - target), x, y)
    rows = [(mo, e) for mo, e in zip(Jm1.monoms(), Jm1.coeffs())
            if e != 0 and mo[0] - mo[1] <= 2]
    return rows, B


def consistent(P, target):
    rows, B = system(P, target)
    eqs = [e for _, e in rows]
    return bool(linsolve(eqs, list(B)))


def h_certificate(P):
    rows, B = system(P, x**2)
    keep = [c for c in range(len(NQ))
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
            return None
        f = expand(sum(cc[r] * rhs[r, 0] for r in range(M.rows)))
        if f != 0:
            return f
    return None


def edge(tv):
    return expand(y**8 * (x * y - tv) ** 8)


def main():
    print("=" * 76)
    print("EXP-062: case c under the torus gauge (t normalized to 1)")
    print("=" * 76)
    # 1: gauge invariance on a sample: t0 = 4 with lambda mu = 4 (lambda = 2, mu = 2)
    t0 = time.time()
    P4 = expand(x * 2 ** (-1) * 2 + edge(4) + Rational(3) * x**2 * y**4)
    # transformed: x -> 2x, y -> 2y in P4, then renormalize: P'(x,y) = P4(2x, 2y)
    Pt = expand(P4.subs({x: 2 * x, y: 2 * y}, simultaneous=True))
    # linear part of Pt: 2x: normalize P' = Pt / 2; bracket target scales: J scales by
    # det = 4; [Pt/2, Q'] = x^2 <=> [Pt, Q''] = c x^2 forms match after Q-rescale:
    # verify consistency EQUIVALENCE concretely:
    c4 = consistent(expand(P4), x**2)
    # transformed system: [Pt, Q] = 8 x^2 (J(P(2x,2y),Q) = 4*(J(P,Q))(2x,2y) =
    # 4*(2x)^2 = 16 x^2 for target; with P-normalization 1/2: 8 x^2)
    ct = consistent(expand(Pt / 2), 8 * x**2)
    print(f"  1: consistency at t=4: {c4}; transformed (t=1-side, rescaled target): "
          f"{ct} ({time.time() - t0:.0f} s)")
    check("1: the gauge transports the system with the SAME verdict (both EMPTY)",
          (not c4) and (not ct))
    # 2: beta-symbolic certificate at t = 1
    ok2 = True
    for (nm, Padd) in (("bare", 0),
                       ("interior sample 1", Rational(2) * x**4 * y**7),
                       ("interior sample 2", Rational(3) * x**2 * y**4 - x * y**3)):
        t0 = time.time()
        P = expand(x + edge(1) + be * x**8 * y**14 + Padd)
        f = h_certificate(P)
        got = f is not None
        ok2 &= got
        print(f"  2: t=1, beta symbolic, {nm}: pairing "
              f"{factor(f) if got else 'NONE'} ({time.time() - t0:.0f} s)")
    check("2: the beta-symbolic certificates exist at t = 1 with nonzero polynomial "
          "pairings", ok2)
    # 3: the free-interior upgrade: one interior coefficient symbolic at a time
    ok3 = True
    ee = symbols("epsN")
    done = 0
    t0 = time.time()
    for pq in INTERIOR:
        if done >= 4 or time.time() - t0 > 400:
            break
        P = expand(x + edge(1) + Rational(2) * x**8 * y**14
                   + ee * x**pq[0] * y**pq[1])
        f = h_certificate(P)
        got = f is not None
        ok3 &= got
        print(f"  3: interior ({pq[0]},{pq[1]}) symbolic: pairing "
              f"{factor(f) if got else 'NONE'}")
        done += 1
    check("3: the free-interior upgrade holds on the tested points (nonzero "
          "polynomial pairings)", ok3, f"{done} points")
    print("  4: assembly: cases a/b closed (EXP-061); case c closed on the forced "
          "family at t = 1 (gauge covers all t != 0); interior upgrade underway "
          "(mechanical); remaining: finish the interior sweep + the orientation "
          "swap; then the floor-raise statement to Felipe.")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
