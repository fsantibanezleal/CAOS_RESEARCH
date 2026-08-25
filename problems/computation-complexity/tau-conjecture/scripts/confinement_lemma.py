"""Confinement lemma: when is the [-32,32] window CONCLUSIVE?

The additive nine-gate scan tests agreement on a window, so on its own it
excludes only seven-rooters whose roots all lie in [-32,32]. This turns that
caveat into a decidable criterion on the trailing coefficient.

LEMMA. Let f in Z[x], f != 0, have distinct integer roots r_1..r_k. Then
prod_i (n - r_i) divides f(n) for every integer n.
  Proof: prod (x - r_i) is monic in Z[x] and divides f in Q[x], so by Gauss
  the cofactor is in Z[x]; evaluate at n.

COROLLARY. Let c be the trailing (first nonzero) coefficient of f, and
suppose f has 7 distinct integer roots.
  - 0 not a root: c = f(0) and |c| >= prod|r_i|. If some |r_j| >= 33 then the
    other six are distinct nonzero, of minimal |product| |(-1)(1)(-2)(2)(-3)(3)|
    = 36, so |c| >= 33*36 = 1188.
  - 0 a root: f = x^m g, c = g(0), the other six roots are distinct nonzero.
    If some |r_j| >= 33 the other five give minimal |product| 12, so
    |c| >= 33*12 = 396.
  Hence |c| <= 395 implies EVERY integer root lies in [-32,32], and the
  windowed scan is conclusive for that f.

Both the lemma and the bound are checked numerically below.
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import pmul, psub, integer_roots


def evalp(p, n):
    return sum(c * n ** i for i, c in enumerate(p))


def trailing(p):
    for c in p:
        if c:
            return c
    return 0


def mono(roots):
    p = (1,)
    for r in roots:
        p = pmul(p, (-r, 1))
    return p


# --- 1. the lemma, on the two verified ten-gate witnesses ------------------
y = pmul((0, 1), (0, 1))
WA = pmul(pmul(pmul(psub(y, (0, 1)), psub(psub(y, (0, 1)), (2,))),
               psub(psub(psub(y, (0, 1)), (2,)), (4,))), psub((0, 1), (4,)))
WB = pmul(pmul(y, psub(y, (1,))), pmul(psub(y, (4,)), psub(y, (16,))))

ok = True
for name, f in [("A interval", WA), ("B tower", WB)]:
    rs = sorted(integer_roots(f))
    for n in range(-40, 41):
        prod = 1
        for r in rs:
            prod *= (n - r)
        fn = evalp(f, n)
        if prod == 0:
            continue
        if fn % prod != 0:
            ok = False
            print("LEMMA FAILS", name, n)
    print(f"lemma holds on {name:<11} roots={rs} trailing={trailing(f)}")
print("lemma check:", "PASS" if ok else "FAIL")

# --- 2. the bound: can a seven-rooter with an escaping root have small c? --
print()
print("searching for a counterexample to |c| >= 396 among seven-root sets")
print("with an escaping root (|r| >= 33), over small root choices:")
worst = None
small = [r for r in range(-8, 9)]
for escape in (33, -33, 40, 64, 100):
    for combo in itertools.combinations(small, 6):
        rs = list(combo) + [escape]
        if len(set(rs)) != 7:
            continue
        p = mono(rs)
        c = abs(trailing(p))
        if worst is None or c < worst[0]:
            worst = (c, rs)
print(f"minimum |trailing coefficient| found: {worst[0]}  at roots {sorted(worst[1])}")
print(f"predicted floor: 396 when 0 is a root, 1188 otherwise")
print("bound respected:", worst[0] >= 396)

# --- 3. what the criterion buys -------------------------------------------
print()
print("CRITERION: if |trailing coefficient of f| <= 395 then all integer roots")
print("of f lie in [-32,32], so the windowed additive scan is CONCLUSIVE for f.")
print("For f = v +- b the trailing coefficient is computable from the stored")
print("state alone (constant terms of v and b), so the fraction of the search")
print("space that is window-limited can be measured exactly. -> EXP-014")
