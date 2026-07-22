# EXP-050: first contact at the (72, 108) degrees.
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


def filtered_consistent(P, N, ratio):
    sup = list(Poly(expand(P), x, y).monoms()) + [(0, 0)]
    hu = hull([(Fraction(i) * ratio, Fraction(j) * ratio) for (i, j) in sup])
    MQ = [(i, d - i) for d in range(2, N + 1) for i in range(d + 1)
          if inside(hu, (Fraction(i), Fraction(d - i)))]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * x**i * y**j for bb, (i, j) in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    return bool(linsolve(eqs, list(B))), len(MQ), len(eqs)


def main():
    print("=" * 76)
    print("EXP-050: first contact at the (72, 108) degrees; corner (16, 56)")
    print("=" * 76)
    g8 = expand((x**2 * y**7) ** 8)
    SAMPLES = [
        ("x + 2 g^8 + x^2 (g = x^2 y^7)", expand(x + 2 * g8 + x**2)),
        ("x + 2 g^8 + 3 x^8 y^28 + x^2 (two-term top ladder)",
         expand(x + 2 * g8 + 3 * x**8 * y**28 + x**2)),
    ]
    ok = True
    for (nm, P) in SAMPLES:
        d = Poly(P, x, y).total_degree()
        t0 = time.time()
        cons, nunk, neq = filtered_consistent(P, 108, Fraction(108, 72))
        dt = time.time() - t0
        ok &= not cons
        print(f"  {nm}: deg {d}; filtered N=108: {nunk} unknowns, {neq} equations, "
              f"{dt:.1f} s: {'EMPTY' if not cons else 'CONSISTENT (escalate!)'}")
    check("1: both degree-72 corner-(16,56) samples have EMPTY filtered windows at "
          "N = 108: the first machine certificates at the open pair's degrees", ok)
    print("  2: cost verdict recorded above; systematic sweep awaits the GGHV shape "
          "transcription (queued).")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
