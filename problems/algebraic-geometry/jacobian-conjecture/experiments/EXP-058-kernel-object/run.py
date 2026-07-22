# EXP-058: the kernel object k(t).
# CPU-only, sympy over QQ(t). Run: run.py
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, binomial, cancel, expand, factor,  # noqa: E402
                   gcd_list, lcm, symbols, zeros)

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


NQ = sorted(hull_pts([(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]))
NP_PTS = hull_pts([(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)])
TOP = {(k, 8 + k) for k in range(9)}
LOWER = [pq for pq in NP_PTS if pq not in TOP]
P0 = expand(y**8 * (x * y - t) ** 8 + x)


def in_pool(r):
    return r[0] - r[1] <= 2 and r[0] <= 24 and r[1] <= 44


def build_M0():
    rows = {}
    PT = {(k, 8 + k): binomial(8, k) * (-t) ** (8 - k) for k in range(9)}
    PT[(1, 0)] = Rational(1)
    for c, (al, be) in enumerate(NQ):
        for (p, q), co in PT.items():
            fac = p * be - q * al
            if fac == 0:
                continue
            r = (p + al - 1, q + be - 1)
            if not in_pool(r):
                continue
            rows.setdefault(r, {})
            rows[r][c] = rows[r].get(c, 0) + co * fac
    rowlist = sorted(rows)
    M = zeros(len(rowlist), len(NQ))
    for kk, r in enumerate(rowlist):
        for c, v in rows[r].items():
            M[kk, c] = expand(v)
    return M, rowlist


def main():
    print("=" * 76)
    print("EXP-058: the kernel object k(t)")
    print("=" * 76)
    t0 = time.time()
    M, rowlist = build_M0()
    ns = M.nullspace()
    print(f"  nullspace over QQ(t): dim {len(ns)} ({time.time() - t0:.0f} s)")
    ok1 = len(ns) == 1
    if not ok1:
        check("1: kernel is one-dimensional over QQ(t)", False, f"dim {len(ns)}")
        return
    v = ns[0]
    den = lcm([cancel(e).as_numer_denom()[1] for e in v])
    kv = [expand(cancel(e * den)) for e in v]
    g = gcd_list([e for e in kv if e != 0])
    if g not in (0, 1):
        kv = [cancel(e / g) for e in kv]
    kpoly = expand(sum(kv[c] * x**i * y**j for c, (i, j) in enumerate(NQ)))
    nzc = sum(1 for e in kv if e != 0)
    (Path(__file__).parent / "artifacts" / "kernel-2026-07-22.txt").write_text(
        f"k(t) with {nzc} nonzero coefficients on N(Q):\n{kpoly}\n")
    check("1: kernel one-dimensional; k(t) computed, cleared, persisted", True,
          f"{nzc}/125 nonzero coefficients")
    supp = sorted(Poly(kpoly, x, y).monoms())
    print(f"  k support ({len(supp)} monomials): degree range "
          f"{min(a + b for a, b in supp)}..{max(a + b for a, b in supp)}; "
          f"i-j range {min(a - b for a, b in supp)}..{max(a - b for a, b in supp)}")
    # 2: exact bracket off-pool
    t0 = time.time()
    br = expand(jac2(P0, kpoly))
    if br == 0:
        check("2: [P0, k] nonzero and entirely off-pool", False, "bracket is ZERO")
    else:
        bm = Poly(br, x, y).monoms()
        offp = all(not in_pool(r) for r in bm)
        ijmin = min(a - b for (a, b) in bm)
        check("2: [P0, k] nonzero and supported entirely OFF-pool (x-heavy overflow)",
              offp, f"{len(bm)} monomials, min i-j = {ijmin} "
              f"({time.time() - t0:.0f} s)")
    # 3: annihilation mechanism: pool part of [m, k] in Col(M0)
    t0 = time.time()
    r0 = M.subs(t, Rational(1)).rank()
    ok3 = True
    for (p, q) in LOWER:
        src = expand(jac2(x**p * y**q, kpoly))
        if src == 0:
            continue
        pe = Poly(src, x, y)
        vv = Matrix([pe.coeff_monomial(x ** r[0] * y ** r[1]) for r in rowlist])
        vv1 = vv.subs(t, Rational(1))
        if all(e == 0 for e in vv1):
            continue
        aug = M.subs(t, Rational(1)).row_join(vv1)
        if aug.rank() != r0:
            ok3 = False
            print(f"  3: FAIL at m = x^{p} y^{q}: pool part NOT in column space")
    check("3: for every lower monomial m, the pool part of [m, k] lies in Col(M0) "
          "(rank tests at t = 1): the annihilation has the EXP-036 shape", ok3,
          f"{time.time() - t0:.0f} s")
    # 4: identification probes
    print("  4: identification probes:")
    # probe: is k proportional to the truncation of P0^c for small c on N(Q)?
    for c in (2,):
        cand = expand(P0 ** c)
        pc = Poly(cand, x, y)
        candQ = expand(sum(co * x**i * y**j for (i, j), co in pc.terms()
                           if (i, j) in set(NQ)))
        if candQ != 0:
            rat = None
            match = True
            kp = Poly(kpoly, x, y)
            cq = Poly(candQ, x, y)
            if set(kp.monoms()) == set(cq.monoms()):
                rats = {cancel(kp.coeff_monomial(x**i * y**j)
                               / cq.coeff_monomial(x**i * y**j))
                        for (i, j) in kp.monoms()}
                match = len(rats) == 1
                print(f"     P0^{c}|_NQ support match: {match}"
                      + (f", ratio {rats}" if match else ""))
            else:
                print(f"     P0^{c}|_NQ support differs "
                      f"({len(cq.monoms())} vs {len(kp.monoms())} monomials)")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
