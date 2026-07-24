# EXP-082: C13 literature-exclusion arithmetic check.
from fractions import Fraction as F
from math import gcd
fail=[]
def ck(n,ok,d=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {n}"+(f"  {d}" if d else ""),flush=True)
    if not ok: fail.append(n)
# 1: (8,4) in the excluded family wp(n', n'-1), n'>=2
def is_excluded(a,b):
    # a = wp*n', b = wp*(n'-1); so a-b = wp, b = wp*(n'-1) => n'-1 = b/wp, n' = a/wp
    wp = a-b
    if wp<=0: return False
    if a%wp or b%wp: return False
    nprime = a//wp
    return nprime>=2 and b//wp==nprime-1
ck("1: (8,4)=4*(2,1) is in the excluded family wp(n',n'-1), n'>=2",
   is_excluded(8,4), f"wp={8-4}, n'={8//(8-4)}")
# sibling and the other named corners from the remark
for (a,b,name) in [(2,1,"(2,1)"),(3,2,"(3,2)"),(6,3,"(6,3)"),(8,4,"(8,4)"),(9,6,"(9,6)")]:
    ck(f"1: {name} excluded (named in GGV2 remark)", is_excluded(a,b))
# 2: the forcing arithmetic (independent of GGV2's assertion): q1=4, d0=4
# bottom vertex of max-x edge = A1 = (8,28) shared; d0 | gcd(8,28)
ck("2: d0 | gcd(8,28) = 4 (shared bottom vertex forces d0<=4)", gcd(8,28)==4)
# (8,12) perfect-cube corner is NOT in the excluded family (the residual EXP-077 flagged)
ck("2: (8,12)=4*(2,3) is NOT wp(n',n'-1) (the naive residual)", not is_excluded(8,12),
   "resolved by GGV2 finitas-direcciones per their stated assertion, not by the naive shift")
print("  3: [D] C13 is discarded in GGV2 (arXiv 1605.09430) remark tex ~1053: "
      "'B_0=(8,28) and B_1=(8,40) lead to A_0=(8,4), impossible'. NO novel floor "
      "progress. RE-AUDIT the 24 [125,150] configs vs this remark + Heitmann "
      "before treating any as open.", flush=True)
print("RESULT: "+("ALL CHECKS PASS." if not fail else f"{len(fail)} FAILED: {fail}"),flush=True)
if fail: raise SystemExit(1)
