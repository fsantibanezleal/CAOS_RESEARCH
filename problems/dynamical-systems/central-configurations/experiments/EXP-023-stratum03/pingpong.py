"""Do the two charts cover each other's residues, or ping-pong?

narrow's residue sits at its own max corner (eps, c1, c2, h) ~ (0.5, 2, 2, 1).
Map it into mergeBC's gauge (divide all lengths by u_A so u_A = 1) and see
whether it lands inside mergeBC's declared box wu in [1/8, 5/4],
wv in [-4, 4].
"""
import json
from fractions import Fraction as F
from pathlib import Path
import itertools

p = Path("E:/_Datos/caos-research/central-configurations/EXP-023/narrow-certificates.jsonl")
lo_wu = hi_wu = lo_wv = hi_wv = None
n = 0
for line in p.open(encoding="utf-8"):
    if '"FAILED"' not in line:
        continue
    b = [[F(x) for x in ax] for ax in json.loads(line)["box"]]
    n += 1
    if n > 400:
        break
    for corner in itertools.product(*[(a, c) for a, c in b]):
        eps, c1, c2, h = corner
        if eps <= 0:
            continue
        uA, uB, uC = eps, eps * c1, eps * c2
        vA, vB, vC = F(0), F(1), h
        # to mergeBC's gauge: divide every length by uA
        s = F(1) / uA
        wu = (uB * s + uC * s) / 2
        wv = (vB * s + vC * s) / 2
        for val, name in ((wu, "wu"), (wv, "wv")):
            pass
        lo_wu = wu if lo_wu is None or wu < lo_wu else lo_wu
        hi_wu = wu if hi_wu is None or wu > hi_wu else hi_wu
        lo_wv = wv if lo_wv is None or wv < lo_wv else lo_wv
        hi_wv = wv if hi_wv is None or wv > hi_wv else hi_wv
print(f"narrow residue (first {min(n,400)} boxes) mapped into mergeBC's gauge:")
print(f"   wu in [{float(lo_wu):.4f}, {float(hi_wu):.4f}]   mergeBC covers [0.125, 1.25]")
print(f"   wv in [{float(lo_wv):.4f}, {float(hi_wv):.4f}]   mergeBC covers [-4, 4]")
inside = (lo_wu >= F(1,8) and hi_wu <= F(5,4) and lo_wv >= F(-4) and hi_wv <= F(4))
print("VERDICT:", "covered by mergeBC" if inside
      else "NOT covered by mergeBC -> the two charts PING-PONG their residues")
