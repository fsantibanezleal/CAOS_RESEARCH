"""Measure each row's true order in the face parameter, per chart.

A chart's row scalings are correct when the rescaled matrix is finite AND
nonzero on the face. The face-rank gate found two charts whose face matrix
collapses: their rows were multiplied by a power of the face parameter
that the algebraic clearing had ALREADY removed, so the rows vanish. This
probe evaluates the chart matrix at a geometric sequence of face-parameter
values and reads each row's order off the ratios, giving the exact
correction to apply.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import math

HERE = Path(__file__).resolve().parent

def load(name, fname):
    spec = importlib.util.spec_from_file_location(name, HERE / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

NAMES = ["L13", "L15", "L23", "L25", "L35", "L36"]

def probe(label, fname, sgn, face_idx, others, base=F(1, 16)):
    mod = load(fname[:-3].replace("-", "_"), fname)
    ef = mod.entry_factory("iv") if sgn is None else mod.entry_factory(sgn, "iv")
    mags = []
    for k in range(3):
        eps = base / F(4 ** k)
        pt = others[:face_idx] + [eps] + others[face_idx:]
        J = ef([(x, x) for x in pt])
        row = []
        for i in range(6):
            m = 0.0
            for j in range(4):
                if J[i][j] is None:
                    continue
                m = max(m, abs(float((J[i][j].lo + J[i][j].hi) / 2)))
            row.append(m)
        mags.append(row)
    print(f"--- {label} (face parameter index {face_idx})")
    for i in range(6):
        a, b = mags[0][i], mags[2][i]
        if a <= 0 or b <= 0:
            print(f"    {NAMES[i]}: identically zero")
            continue
        order = math.log(a / b) / math.log(16.0)   # eps ratio 16 over two steps
        print(f"    {NAMES[i]}: |row| {a:.3e} -> {b:.3e}   order ~ {order:+.2f}")

probe("m1  (rhoq -> 0)", "m1chart.py", None, 2,
      [F(1, 8), F(1, 3), F(1, 5)])
probe("fartube (rhof -> 0)", "fartube.py", None, 0,
      [F(1, 3), F(1, 4), F(1, 5)])
