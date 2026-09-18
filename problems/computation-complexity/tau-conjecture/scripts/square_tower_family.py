"""The square-tower family: z = 2m+3 distinct integer roots in 3m+4 gates.

    p_m(x) = x^2 (x^2 - 1) prod_{i=2}^{m+1} (x^2 - t_i),   t_{i+1} = t_i^2, t_1 = 2

Every constant is one squaring past the previous one, and t_i is a perfect
square for i >= 2, so each additional gate-triple buys a genuine pair of new
integer roots. Verified here by exact expansion, not by hand-count.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import psub, pmul, integer_roots


def build(m):
    """Return (polynomial, gate_count) for p_m."""
    gates = 0
    y = pmul((0, 1), (0, 1)); gates += 1          # y = x^2
    a = psub(y, (1,)); gates += 1                 # y - 1   (free constant)
    factors = [y, a]
    if m > 0:
        t = 2; gates += 1                         # t_1 = 1 + 1
        for _ in range(m):
            t = t * t; gates += 1                 # t_{i+1} = t_i * t_i
            factors.append(psub(y, (t,))); gates += 1
    p = factors[0]
    for f in factors[1:]:
        p = pmul(p, f); gates += 1
    return p, gates


print(f"{'m':>2} {'gates':>6} {'3m+4':>6} {'roots':>6} {'2m+3':>6}  root set")
print("-" * 78)
for m in range(5):
    p, g = build(m)
    r = sorted(integer_roots(p))
    pred_g = 3 * m + 4 if m > 0 else 3
    ok = "ok" if (g == pred_g and len(r) == 2 * m + 3) else "MISMATCH"
    shown = str(r) if len(str(r)) < 42 else str(r[:3])[:-1] + " ... " + str(r[-3:])[1:]
    print(f"{m:>2} {g:>6} {pred_g:>6} {len(r):>6} {2*m+3:>6}  {shown}  {ok}")

print()
print("census (exhaustive)      : minimal tau for 3 roots = 3, 4 roots = 5,")
print("                           5 roots = 6, 6 roots = 8")
print("family at m=0            : 3 roots in 3 gates -> MEETS the exhaustive threshold")
print("family at m=1            : 5 roots in 7 gates -> census does it in 6, family is not optimal here")
print("family at m=2            : 7 roots in 10 gates -> upper bound for the open case")
