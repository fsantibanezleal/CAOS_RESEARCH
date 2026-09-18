"""Probe the cb1f corner cluster: rank at the triple-boundary point.

The two genuine failures sit at (rhoc, tauc, eps, tau) ~ (1.8e-4, 0,
1/3, -1): pair B collapsed onto axis body 1 (rhoc -> 0), pair A collapsed
on the axis at R_A = 3 (tau -> -1 gives aA = 0, i.e. u = 0), at the
chart's outer seam eps = 1/3.

Evaluates the cb1f chart matrix at the exact corner and at points
approaching it along each face, reporting singular values, to decide:
rank >= 3 at the corner (conditioning only, deeper bisection or a wider
neighbouring chart suffices) vs rank <= 2 (a further blow-up needed).
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cb1f", HERE / "cb1f.py")
cb1f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cb1f)

def svals(rc, tc, eps, tau):
    pt = [(x, x) for x in (rc, tc, eps, tau)]
    try:
        J = cb1f.entry_factory("iv")(pt)
    except AssertionError as e:
        return None, str(e)
    rows = []
    for i in range(6):
        rows.append([float((J[i][j].lo + J[i][j].hi) / 2) if J[i][j] is not None
                     else 0.0 for j in range(4)])
    # singular values by Jacobi on the 4x4 Gram matrix
    import math
    G = [[sum(rows[k][i] * rows[k][j] for k in range(6)) for j in range(4)]
         for i in range(4)]
    # symmetric eigenvalues via cyclic Jacobi
    A = [row[:] for row in G]
    for _ in range(80):
        off = 0.0
        for i in range(4):
            for j in range(i + 1, 4):
                off += A[i][j] ** 2
        if off < 1e-30:
            break
        for pq in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
            p, q = pq
            if abs(A[p][q]) < 1e-300:
                continue
            theta = (A[q][q] - A[p][p]) / (2 * A[p][q])
            t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
            c = 1 / math.sqrt(t * t + 1)
            s = t * c
            for k in range(4):
                akp, akq = A[k][p], A[k][q]
                A[k][p] = c * akp - s * akq
                A[k][q] = s * akp + c * akq
            for k in range(4):
                apk, aqk = A[p][k], A[q][k]
                A[p][k] = c * apk - s * aqk
                A[q][k] = s * apk + c * aqk
    ev = sorted((max(A[i][i], 0.0) ** 0.5 for i in range(4)), reverse=True)
    return ev, None

print("approach along each face (rhoc, tauc, eps, tau):")
CASES = [
    ("corner (rhoc=0, tau=-1, eps=1/3)", F(0), F(0), F(1, 3), F(-1)),
    ("rhoc=1e-4", F(1, 10000), F(0), F(1, 3), F(-1)),
    ("rhoc=1e-2", F(1, 100), F(0), F(1, 3), F(-1)),
    ("tau=-0.99", F(1, 10000), F(0), F(1, 3), F(-99, 100)),
    ("tau=-0.9", F(1, 10000), F(0), F(1, 3), F(-9, 10)),
    ("tau=-0.5", F(1, 10000), F(0), F(1, 3), F(-1, 2)),
    ("eps=1/4, tau=-1", F(1, 10000), F(0), F(1, 4), F(-1)),
    ("tauc=1/2", F(1, 10000), F(1, 2), F(1, 3), F(-1)),
    ("both mid", F(1, 100), F(1, 2), F(1, 4), F(-1, 2)),
]
for label, rc, tc, eps, tau in CASES:
    ev, err = svals(rc, tc, eps, tau)
    if err:
        print(f"  {label:34s} UNDEFINED ({err})")
    else:
        print(f"  {label:34s} sv = " + ", ".join(f"{x:.3e}" for x in ev))
