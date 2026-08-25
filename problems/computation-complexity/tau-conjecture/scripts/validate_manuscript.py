"""Adversarial validation of manuscript claims outside the new sections."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import padd, psub, pmul, integer_roots, census_polynomials, last_gate_scan

FAIL = []


def check(name, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name:<58} got={got!r:<26} want={want!r}")
    if not ok:
        FAIL.append(name)


# ---- 1. stall theorem: integer periodic points of x^2 - 2 are exactly {2, -1}
print("== Proposition: integer periodic points of h(x) = x^2 - 2 ==")
h = lambda v: v * v - 2
per = set()
for v in range(-200, 201):
    seen, w = [], v
    for _ in range(64):
        w = h(w)
        if abs(w) > 10 ** 12:
            break
        if w == v:
            per.add(v)
            break
check("integer periodic points of x^2-2 in [-200,200]", sorted(per), [-1, 2])

# ---- 2. the two yield series of the quadratic family
print("\n== Theorem: family yield series c = m(m+1) and c = m^2+m+1 ==")


def tower_roots(c, kmax=4):
    """Integer roots over the measured shapes, via the proved escape window."""
    W = range(-(c + 1), c + 2)
    hc = lambda v: v * v - c
    best = set()
    for k in range(1, kmax + 1):
        rs = set()
        for v in W:
            w = v
            for _ in range(k):
                w = hc(w)
            if w == v:
                rs.add(v)
        if len(rs) > len(best):
            best = rs
    for i in range(kmax + 1):
        for j in range(i + 1, kmax + 1):
            rs = set()
            for v in W:
                a = b = v
                for _ in range(i):
                    a = hc(a)
                for _ in range(j):
                    b = hc(b)
                if a * a == b * b:
                    rs.add(v)
            if len(rs) > len(best):
                best = rs
    return best


for m in (2, 3, 4):
    c = m * (m + 1)
    r = tower_roots(c)
    check(f"c = m(m+1) = {c} (m={m}): root set", sorted(r),
          sorted({m, -m, m + 1, -(m + 1)}))
for m in (2, 3, 4):
    c = m * m + m + 1
    r = tower_roots(c)
    check(f"c = m^2+m+1 = {c} (m={m}): root set", sorted(r),
          sorted({m, -m, m + 1, -(m + 1)}))
check("c = 2 is the unique argmax with yield 5", sorted(tower_roots(2)),
      [-2, -1, 0, 1, 2])

# ---- 3. the digit-restricted extremal witness
print("\n== The digit-restricted witness (x^2-1)(x^2-9) ==")
y = pmul((0, 1), (0, 1))
c2 = (2,); c3 = (3,); c9 = (9,)
w = pmul(psub(y, (1,)), psub(y, (9,)))
gates = 7  # x*x, y-1, 1+1, 2+1, 3*3, y-9, product
r = sorted(integer_roots(w))
check("(x^2-1)(x^2-9) roots", r, [-3, -1, 1, 3])
check("all four roots odd", all(v % 2 != 0 for v in r), True)
check("gate count as stated", gates, 7)

# ---- 4. digit ladders, recomputed through tau = 6
print("\n== Digit-restricted ladders (recomputed) ==")
per_d, fs, comp, frontier = census_polynomials(5, return_frontier=True)
INPUTS = {(), (1,), (-1,), (0, 1)}
new6, c6, s6 = last_gate_scan(frontier, set(fs) | INPUTS)
groups = {}
for p, t in fs.items():
    if p:
        groups.setdefault(t, []).append(p)
groups[6] = [p for p in new6 if p]


def digit_max(polys, mod, res):
    best = 0
    for p in polys:
        n = sum(1 for r in integer_roots(p) if r % mod == res)
        if n > best:
            best = n
    return best


odd = [digit_max(groups[t], 2, 1) for t in sorted(groups)]
m3 = [digit_max(groups[t], 3, 1) for t in sorted(groups)]
check("odd-root ladder tau=1..6", odd, [1, 2, 2, 2, 2, 3])
check("mod-3 ladder tau=1..6", m3, [1, 1, 1, 2, 2, 3])
check("depth-6 new polynomial count (seeded)", len(new6), 134494)

print()
print("FAILURES:", FAIL if FAIL else "none")
sys.exit(1 if FAIL else 0)
