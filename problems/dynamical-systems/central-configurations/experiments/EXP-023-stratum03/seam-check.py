"""Seam check: do mergeBC's residue boxes land inside narrow's region?

mergeBC works in (rho, tau, wu, wv) with pair A at (+-1, 0) and the merged
B/C cluster near (+-wu, wv). narrow works in (eps, c1, c2, h) with widths
eps*(1, c1, c2) and heights (0, 1, h). The map between them is a pure
rescaling: divide every length by the B height, so

    eps = u_A / v_B = 1 / v2,   c1 = u_B / u_A,   c2 = u_C / u_A,
    h   = v_C / v_B .

This reads every residue box's corners, maps them, and reports the range
narrow must cover for the seam to close.
"""
import json
from fractions import Fraction as F
from pathlib import Path
import itertools

p = Path("E:/_Datos/caos-research/central-configurations/EXP-023/mergeBC-certificates.jsonl")
rng = [[None, None] for _ in range(4)]
n = 0
def upd(i, v):
    if rng[i][0] is None or v < rng[i][0]: rng[i][0] = v
    if rng[i][1] is None or v > rng[i][1]: rng[i][1] = v

for line in p.open(encoding="utf-8"):
    if '"FAILED"' not in line:
        continue
    b = [[F(x) for x in ax] for ax in json.loads(line)["box"]]
    n += 1
    for corner in itertools.product(*[(a, c) for a, c in b]):
        rho, tau, wu, wv = corner
        o = 1 + tau * tau
        al, be = (1 - tau * tau) / o, 2 * tau / o
        u2 = wu + rho * al / 2; v2 = wv + rho * be / 2
        u3 = wu - rho * al / 2; v3 = wv - rho * be / 2
        if v2 == 0 or u2 <= 0 or u3 <= 0:
            continue
        eps = F(1) / v2            # u_A = 1 in mergeBC's gauge
        upd(0, eps); upd(1, u2); upd(2, u3); upd(3, v3 / v2)
print(f"{n} mergeBC residue boxes")
for lab, (lo, hi) in zip(["eps", "c1", "c2", "h"], rng):
    print(f"   {lab}: [{float(lo):.6f}, {float(hi):.6f}]")
print()
print("narrow's declared seed: eps [0, 0.25], c1 [0, 1], c2 [0, 1], h [-2, 2]")
need = []
if rng[0][1] > F(1,4): need.append(f"eps up to {float(rng[0][1]):.4f}")
if rng[1][1] > F(1): need.append(f"c1 up to {float(rng[1][1]):.4f}")
if rng[2][1] > F(1): need.append(f"c2 up to {float(rng[2][1]):.4f}")
if rng[3][1] > F(2) or rng[3][0] < F(-2): need.append("h beyond [-2,2]")
print("SEAM:", "closes as declared" if not need else "narrow must widen: " + ", ".join(need))
