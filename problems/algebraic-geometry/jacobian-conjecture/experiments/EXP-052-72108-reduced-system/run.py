# EXP-052: first contact with the reduced (72, 108) system.
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


def hull_pts(verts):
    """Lattice points inside conv(verts) (small polygons: brute force)."""
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


NP_VERTS = [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)]
NQ_VERTS = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]


def partner_exists(P):
    qpts = hull_pts(NQ_VERTS)
    B = symbols(f"B0:{len(qpts)}")
    Q0 = sum(bb * x**i * y**j for bb, (i, j) in zip(B, qpts))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - x**2), x, y).coeffs() if e != 0]
    return bool(linsolve(eqs, list(B))), len(qpts), len(eqs)


def main():
    print("=" * 76)
    print("EXP-052: the reduced (72, 108) system: [P, Q] = x^2 on GGHV Prop 4.3 "
          "polygons")
    print("=" * 76)
    ppts = hull_pts(NP_VERTS)
    qpts = hull_pts(NQ_VERTS)
    print(f"  sizes: N(P) lattice points {len(ppts)}; N(Q) lattice points {len(qpts)}")
    check("1: both reduced polygons enumerated; the Q-side system is a few hundred "
          "unknowns", 0 < len(qpts) < 500, f"{len(ppts)} / {len(qpts)}")
    import random
    rng = random.Random(20260722)
    ok = True
    forced = [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)]
    for trial in range(4):
        coeffs = {}
        for pt in ppts:
            r = rng.randint(-3, 3)
            coeffs[pt] = Rational(r)
        for pt in forced:
            if coeffs.get(pt, 0) == 0:
                coeffs[pt] = Rational(rng.choice([1, -1, 2]))
        P = expand(sum(c * x**i * y**j for (i, j), c in coeffs.items() if c != 0))
        t0 = time.time()
        cons, nunk, neq = partner_exists(P)
        dt = time.time() - t0
        ok &= not cons
        print(f"  2: random P sample {trial}: {nunk} unknowns, {neq} equations, "
              f"{dt:.1f} s: {'EMPTY' if not cons else 'CONSISTENT (ESCALATE!)'}")
    # structured sample: top edge (0,8)-(8,16) as y^8 phi(xy), phi = (xy - 1)^8
    Ptop = expand(y**8 * (x * y - 1) ** 8)
    Pstruct = expand(Ptop + x + 1)
    t0 = time.time()
    cons, nunk, neq = partner_exists(Pstruct)
    dt = time.time() - t0
    ok &= not cons
    print(f"  2: structured P (top edge y^8 (xy - 1)^8 + x + 1): {nunk} unknowns, "
          f"{dt:.1f} s: {'EMPTY' if not cons else 'CONSISTENT (ESCALATE!)'}")
    check("2: every tested P on the reduced polygon has NO partner with [P, Q] = x^2 "
          "(sampled emptiness of the open case's reduced system)", ok)
    print("  3: framing: sampled evidence toward closing (72, 108); the parametrized "
          "certificate over ALL P (the system GGHV could not solve) is the next round's "
          "target with the transport + certificate instruments on THIS reduced object.")


if __name__ == "__main__":
    main()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
