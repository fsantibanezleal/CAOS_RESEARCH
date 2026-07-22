# EXP-045: frontier mid-scale (routes N2 + M1).
# CPU-only, sympy over QQ. Run: run.py [A|B|C|D]
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, library, top_form, x, y  # noqa: E402
from sympy import Poly, Rational, expand, linsolve, symbols  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def R0(l0):
    return expand(x * (x * y**4 - l0) ** 3)


def window_consistent(P, N, allowed=None):
    MQ = [(i, d - i) for d in range(2, N + 1) for i in range(d + 1)]
    if allowed is not None:
        MQ = [m for m in MQ if allowed(m)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * x**i * y**j for bb, (i, j) in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    return bool(linsolve(eqs, list(B))), len(MQ)


def hull(points):
    """Monotone-chain convex hull of integer/rational points."""
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
        cr = (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
        if cr < 0:
            return False
    return True


def scaled_filter(P, ratio):
    """Membership test for the ratio-scaled N^0(P) polygon."""
    sup = list(Poly(expand(P), x, y).monoms()) + [(0, 0)]
    hu = hull([(Fraction(i) * ratio, Fraction(j) * ratio) for (i, j) in sup])
    return lambda m: inside(hu, (Fraction(m[0]), Fraction(m[1])))


def partA():
    print("=" * 76)
    print("Part A: the divisibility one-liner")
    print("=" * 76)
    z = symbols("z")
    G = symbols("g0:4")
    ok = True
    for m in (2, 3):
        for (k, l) in ((1, 4), (2, 3)):
            phi = sum(g * z**i for i, g in enumerate(G))
            E = expand(x**m * phi.subs(z, x**k * y**l))
            for (al, be) in ((0, 1), (1, 2), (3, 0), (2, 5)):
                J = expand(jac2(E, x**al * y**be))
                if J == 0:
                    continue
                q, r = Poly(J, x, y).div(Poly(x ** (m - 1), x, y))
                ok &= r.is_zero
    check("A: J(x^m psi(z), Q) is divisible by x^{m-1} (m >= 2, symbolic psi): pure R0^m "
          "is NEVER a Keller component, trivially, at every degree", ok)


def partB():
    print("=" * 76)
    print("Part B: degree-32 exclusions on the B = 16 flavor")
    print("=" * 76)
    P32 = expand(x + R0(1) ** 2)
    mons = sorted(Poly(P32, x, y).monoms())
    print(f"  B P32 = x + R0(1)^2: degree {Poly(P32, x, y).total_degree()}, "
          f"support {mons}")
    ok = True
    for N in (12, 16, 20):
        cons, nunk = window_consistent(P32, N)
        ok &= not cons
        print(f"  B window N={N} ({nunk} unknowns): "
              f"{'EMPTY' if not cons else 'CONSISTENT (escalate!)'}")
    check("B: P32 windows N = 12, 16, 20 all EMPTY (new certificates at degree 32, "
          "B = 16 flavor)", ok)


def partC():
    print("=" * 76)
    print("Part C: filter correctness on a genuine pair")
    print("=" * 76)
    ok = True
    tested = 0
    for (P, Q) in library():
        dP = Poly(expand(P), x, y).total_degree()
        dQ = Poly(expand(Q), x, y).total_degree()
        if dP < 2 or dQ < 2 or dP + dQ > 10:
            continue
        tested += 1
        filt = scaled_filter(P, Fraction(dQ, dP))
        badq = [m for m in Poly(expand(Q), x, y).monoms() if not filt(m)]
        if badq:
            ok = False
            print(f"  C pair degs ({dP},{dQ}): partner monomials OUTSIDE the scaled "
                  f"polygon: {badq}")
        else:
            print(f"  C pair degs ({dP},{dQ}): every partner monomial inside the "
                  f"scaled polygon")
    check("C: the similarity filter keeps every true partner on the tested library "
          "pairs (soundness on knowns)", ok and tested > 0, f"{tested} pairs")


def partD():
    print("=" * 76)
    print("Part D: measured filter value")
    print("=" * 76)
    P32 = expand(x + R0(1) ** 2)
    filt = scaled_filter(P32, Fraction(48, 32))
    full = [(i, d - i) for d in range(2, 49) for i in range(d + 1)]
    kept = [m for m in full if filt(m)]
    red = Rational(len(full), len(kept)) if kept else None
    print(f"  D P32 at partner degree 48: full window {len(full)} unknowns, filtered "
          f"{len(kept)} ({float(100 * len(kept) / len(full)):.1f} percent kept, "
          f"reduction x{float(red):.2f})")
    ok1 = len(kept) < len(full) / 2
    # the (48, 64) system: filter by the scaled polygon of the m = 3 shape
    P48 = expand(x + R0(1) ** 3)
    filt48 = scaled_filter(P48, Fraction(64, 48))
    full64 = [(i, d - i) for d in range(2, 65) for i in range(d + 1)]
    kept64 = [m for m in full64 if filt48(m)]
    print(f"  D (48, 64) shape: full window {len(full64)} unknowns, filtered "
          f"{len(kept64)} ({float(100 * len(kept64) / len(full64)):.1f} percent kept)")
    ok2 = len(kept64) < len(full64) / 2
    # end-to-end: the filtered window is still decisive on P32 (stays empty)
    cons, nunk = window_consistent(P32, 16, allowed=filt)
    print(f"  D filtered window N=16 on P32: {nunk} unknowns, "
          f"{'EMPTY' if not cons else 'CONSISTENT'}")
    check("D: the similarity filter cuts window unknowns by more than half on both "
          "systems and preserves the emptiness verdict", ok1 and ok2 and not cons)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD}

if __name__ == "__main__":
    todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D"]
    for p_ in todo:
        PARTS[p_]()
        print()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
