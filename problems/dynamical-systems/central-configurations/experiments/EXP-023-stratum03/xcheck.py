"""Crosscheck the interval (0,3) matrix against the independent mpmath one."""
import importlib.util
from pathlib import Path
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 40
HERE = Path(__file__).resolve().parent
src = (HERE / "derive.py").read_text(encoding="utf-8")
ns = {"__file__": str(HERE / "derive.py")}
exec(src.split('rnd = random.Random')[0], ns)
positions, L_coeffs, ROWS = ns["positions"], ns["L_coeffs"], ns["ROWS"]
s = importlib.util.spec_from_file_location("cov", HERE / "cover.py")
cov = importlib.util.module_from_spec(s); s.loader.exec_module(cov)

import random
random.seed(9)
bad = 0
for _ in range(5):
    pt = (F(random.randint(8,63),64), F(random.randint(8,63),64),
          F(random.randint(-150,150),64), F(random.randint(-150,150),64))
    u2, u3, v2, v3 = pt
    J = cov.entry_factory("iv")([(x, x) for x in pt])
    P = positions(mp.mpf(1), mp.mpf(0), mp.mpf(u2.numerator)/u2.denominator,
                  mp.mpf(v2.numerator)/v2.denominator,
                  mp.mpf(u3.numerator)/u3.denominator,
                  mp.mpf(v3.numerator)/v3.denominator)
    for r, (i, j) in enumerate(ROWS):
        ref = L_coeffs(P, i, j)
        for c in range(3):
            got = (J[r][c].lo + J[r][c].hi) / 2
            if abs(mp.mpf(got.numerator)/got.denominator - ref[c]) > mp.mpf(10)**-10 * (1 + abs(ref[c])):
                print(f"MISMATCH row {r} col {c}: {float(got)} vs {mp.nstr(ref[c],10)}")
                bad += 1
print("CROSSCHECK:", "FAILED" if bad else "5/5 points agree with the mpmath derivation")
