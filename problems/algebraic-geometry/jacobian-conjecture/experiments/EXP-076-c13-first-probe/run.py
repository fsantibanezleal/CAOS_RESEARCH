# EXP-076: C13 first probe (arithmetic of the sibling discard vs (8,40)).
from math import gcd
import sys
failures = []
def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""), flush=True)
    if not ok: failures.append(name)
def v(rho, sig, a, b, l=1):
    from fractions import Fraction
    return rho * Fraction(a, l) + sig * b
# 1: the (8,32) sibling arithmetic
check("1a: v_{4,-1}(A1) = v_{4,-1}(A2) = 4 (direction well-defined)",
      v(4,-1,8,28) == 4 and v(4,-1,11,7,4) == 4, f"{v(4,-1,8,28)}, {v(4,-1,11,7,4)}")
check("1b: (8,28) = 4*(2,7), gcd(2,7) = 1", (8,28) == (4*2,4*7) and gcd(2,7) == 1)
# R = x^2 y^7 (y-1): bidegree (2,8); (R^{4m}) bidegree (8m, 32m) = m*(8,32)
check("1c: R = x^2 y^7 (y-1) bidegree (2,8); R^{4m} matches st (8m,32m)",
      (2*4, 8*4) == (8, 32))
check("1d: post-shift corner (8, 32-28) = (8,4)", (8, 32-28) == (8,4))
# 2: the (8,40) analogues
check("2a: v_{4,-1}((8,40)) = -8 (DIFFERS from sibling's 0: recorded)",
      v(4,-1,8,40) == -8 and v(4,-1,8,32) == 0)
check("2b: (8,40) = 8*(1,5), gcd(1,5) = 1", (8,40) == (8*1,8*5) and gcd(1,5) == 1)
check("2c: R' = x y^4 (y-1) bidegree (1,5); R'^{8m} matches st (8m,40m)",
      (1*8, 5*8) == (8, 40))
check("2d: post-shift corner (8, 40-28) = (8,12)", (8, 40-28) == (8,12))
print("  3: [D] GAP LIST (UNVERIFIED, primary-source fetch next round): "
      "(i) q' = 8 | d0 divisibility (Cor 7.4 hypothesis at (8,40)); "
      "(ii) [GGV2, Prop 3.29] exclusion at the post-shift corner (8,12) "
      "(the sibling used it at (8,4)); (iii) whether v_{4,-1}(A0) = -8 vs 0 "
      "changes the en-point computation. Until these are sourced, NO discard "
      "claim for C13.", flush=True)
print("RESULT: " + ("ALL CHECKS PASS." if not failures else f"{len(failures)} FAILED: {failures}"), flush=True)
if failures: sys.exit(1)
