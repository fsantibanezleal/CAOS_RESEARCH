# EXP-047: the filtered (48, <= 64) sweep (route N2).
# CPU-only, sympy over QQ. Run: run.py
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import Poly, Rational, expand, linsolve, symbols  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
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
    return lo[:-1] + up[:-1]


def inside(hu, q):
    n = len(hu)
    for k in range(n):
        o, p = hu[k], hu[(k + 1) % n]
        if (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0]) < 0:
            return False
    return True


def scaled_filter(P, ratio):
    sup = list(Poly(expand(P), x, y).monoms()) + [(0, 0)]
    hu = hull([(Fraction(i) * ratio, Fraction(j) * ratio) for (i, j) in sup])
    return lambda m: inside(hu, (Fraction(m[0]), Fraction(m[1])))


def filtered_consistent(P, N, ratio):
    filt = scaled_filter(P, ratio)
    MQ = [(i, d - i) for d in range(2, N + 1) for i in range(d + 1) if filt((i, d - i))]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * x**i * y**j for bb, (i, j) in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    return bool(linsolve(eqs, list(B))), len(MQ), len(eqs)


def R0(l0):
    return expand(x * (x * y**4 - l0) ** 3)


def main():
    print("=" * 76)
    print("EXP-047: filtered (48, <= 64) sweep; ratio 64/48; any partner deg <= 64 "
          "must fit the scaled polygon (similarity, both degs > 1)")
    print("=" * 76)
    SAMPLES = [
        ("pure F1 shape: x + R0(1)^3", expand(x + R0(1) ** 3)),
        ("swallowed variant: x + R0(1)^3 + x^2", expand(x + R0(1) ** 3 + x**2)),
        ("mixed variant: x + R0(1)^3 + x^2 + 5 x^3 y^4",
         expand(x + R0(1) ** 3 + x**2 + Rational(5) * x**3 * y**4)),
    ]
    ok = True
    for (nm, P) in SAMPLES:
        d = Poly(P, x, y).total_degree()
        t0 = time.time()
        cons, nunk, neq = filtered_consistent(P, 64, Fraction(64, 48))
        dt = time.time() - t0
        ok &= not cons
        print(f"  {nm}: deg {d}; filtered window N=64: {nunk} unknowns, {neq} "
              f"equations, {dt:.1f} s: "
              f"{'EMPTY' if not cons else 'CONSISTENT (escalate!)'}")
    check("A+B: all three degree-48 samples have EMPTY filtered windows at N = 64: no "
          "Keller partner of ANY degree <= 64 exists for these samples", ok)
    print("  C framing: these are the classical case-64 degrees (Moh detailed case; "
          "Heitmann): sampled-level machine replication on frontier-shaped polynomials; "
          "the same pipeline at max degree > 150 or at (72, 108) produces NEW territory "
          "at comparable cost.")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
