"""Measure the ORIGINAL matrix's entry orders at a chart's face.

Row and column scalings must be chosen TOGETHER: the rescaled entry has
order  o_ij + r_i + c_j,  and the face matrix is finite and nonzero
exactly when min over each row and each column of that quantity is 0.
This probe measures o_ij directly from the original entry_matrix along the
chart's parametrization, so the scalings can be solved rather than
guessed. Orders are read from a geometric sequence in the face parameter.
"""
import math
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pipeline", HERE / "pipeline.py")
pl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pl)

NAMES = ["L13", "L15", "L23", "L25", "L35", "L36"]
COLS = ["m1", "m2", "mA", "mB"]

def circ(t):
    o = 1 + t * t
    return (1 - t * t) / o, 2 * t / o

def m1_geom(rhoq, rhoa=F(1, 8), tb=F(1, 3), tq=F(1, 5)):
    """M1 chart -> original (u, v, p, q)."""
    al_n, be = circ(tq)
    alpha = -al_n
    rr = 1 + rhoq * alpha
    ta = tb + rhoq * be
    ca, sa = circ(ta)
    cb, sb = circ(tb)
    return rhoa * ca, 1 + rhoa * sa, rr * rhoa * cb, 1 + rr * rhoa * sb

def fartube_geom(rhof, tf=F(1, 3), eB=F(1, 4), tB=F(1, 5)):
    """fartube chart -> original (u, v, p, q)."""
    opf = 1 + tf * tf
    alpha = -(1 - tf * tf) / opf
    beta = 2 * tf / opf
    r = 1 + rhof * alpha
    tA = tB + rhof * beta
    aA, bA = circ(tA)
    aB, bB = circ(tB)
    eA = r * eB
    return aA / eA, bA / eA, aB / eB, bB / eB

def orders(label, geom, base=F(1, 16)):
    mats = []
    for k in range(3):
        e = base / F(4 ** k)
        u, v, p, q = geom(e)
        J = pl.r21.entry_matrix((u, u), (v, v), (p, p), (q, q))
        mats.append([[abs(float((J[i][j].lo + J[i][j].hi) / 2)) for j in range(4)]
                     for i in range(6)])
    print(f"--- {label}: entry orders in the face parameter")
    print("        " + "".join(f"{c:>10s}" for c in COLS))
    O = []
    for i in range(6):
        row = []
        cells = []
        for j in range(4):
            a, b = mats[0][i][j], mats[2][i][j]
            if a <= 1e-300 or b <= 1e-300:
                row.append(None); cells.append("      zero")
            else:
                o = math.log(a / b) / math.log(16.0)
                row.append(o); cells.append(f"{o:+10.2f}")
        O.append(row)
        print(f"   {NAMES[i]}: " + "".join(cells))
    return O

def solve_scalings(O):
    """Pick integer row/col shifts making every row and column minimum 0."""
    # start with column shifts 0, iterate: r_i = -min_j(o_ij + c_j), then
    # c_j = -min_i(o_ij + r_i); two passes suffice for these matrices.
    c = [0.0] * 4
    for _ in range(3):
        r = []
        for i in range(6):
            vals = [O[i][j] + c[j] for j in range(4) if O[i][j] is not None]
            r.append(-min(vals) if vals else 0.0)
        c = []
        for j in range(4):
            vals = [O[i][j] + r[i] for i in range(6) if O[i][j] is not None]
            c.append(-min(vals) if vals else 0.0)
    print("   suggested row scalings   (multiply row i by eps^r_i): "
          + ", ".join(f"{NAMES[i]}:{r[i]:+.2f}" for i in range(6)))
    print("   suggested column scalings (multiply col j by eps^c_j): "
          + ", ".join(f"{COLS[j]}:{c[j]:+.2f}" for j in range(4)))
    surv = [(NAMES[i], COLS[j]) for i in range(6) for j in range(4)
            if O[i][j] is not None and abs(O[i][j] + r[i] + c[j]) < 0.1]
    print(f"   surviving entries on the face: {len(surv)} -> {surv[:10]}")

for label, geom in (("M1 (rhoq)", m1_geom), ("fartube (rhof)", fartube_geom)):
    O = orders(label, geom)
    solve_scalings(O)
    print()
