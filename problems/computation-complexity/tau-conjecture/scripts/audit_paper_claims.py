"""Audit every numerical claim in the new manuscript sections, recomputed.

A claim can be consistent across the note, the wiki and the paper and still be
false; the only check that counts is against a fresh computation. This re-derives
each number independently and compares it to what the manuscript states.
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import padd, psub, pmul, integer_roots

x = sp.Symbol("x")
FAIL = []


def check(name, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name:<52} got={got!r:<28} want={want!r}")
    if not ok:
        FAIL.append(name)


def height(p):
    return max(abs(c) for c in p) if p else 0


def zreal(p):
    q = sp.Poly(list(reversed(p)), x, domain="ZZ")
    if q.degree() < 1:
        return 0
    q = q.quo(sp.Poly(sp.gcd(q, q.diff(x)), x, domain="ZZ"))
    return int(q.count_roots()) if q.degree() >= 1 else 0


def run(slp):
    regs = []
    def val(r):
        if r[0] == "x":
            return (0, 1)
        if r[0] == "c":
            return () if r[1] == 0 else (r[1],)
        return regs[r[1]]
    for op, a, b in slp:
        regs.append({"+": padd, "-": psub, "*": pmul}[op](val(a), val(b)))
    return regs[-1], len(slp)


X = ("x",); C = lambda k: ("c", k); R = lambda i: ("r", i)

print("== Proposition: two ten-gate seven-rooters ==")
A = [("*", X, X), ("-", R(0), X), ("+", C(1), C(1)), ("*", R(2), R(2)),
     ("-", R(1), R(2)), ("-", R(4), R(3)), ("*", R(4), R(5)),
     ("*", R(6), R(1)), ("-", X, R(3)), ("*", R(7), R(8))]
pA, gA = run(A)
check("witness A gate count", gA, 10)
check("witness A distinct integer roots", sorted(integer_roots(pA)), [-2,-1,0,1,2,3,4])
check("witness A height", height(pA), 56)
six, _ = run(A[:8])
check("inner 8-gate factor roots", sorted(integer_roots(six)), [-2,-1,0,1,2,3])
check("inner 8-gate factor height", height(six), 15)

B = [("*", X, X), ("+", R(0), C(-1)), ("+", C(1), C(1)), ("*", R(2), R(2)),
     ("-", R(0), R(3)), ("*", R(3), R(3)), ("-", R(0), R(5)),
     ("*", R(0), R(1)), ("*", R(4), R(6)), ("*", R(7), R(8))]
pB, gB = run(B)
check("witness B gate count", gB, 10)
check("witness B distinct integer roots", sorted(integer_roots(pB)), [-4,-2,-1,0,1,2,4])
check("witness B height", height(pB), 84)

print("\n== Proposition: square-tower family z = 2m+3 at tau = 3m+4 ==")
for m in range(5):
    gates = 0
    y = pmul((0,1),(0,1)); gates += 1
    a = psub(y, (1,)); gates += 1
    fs = [y, a]
    if m > 0:
        t = 2; gates += 1
        for _ in range(m):
            t = t*t; gates += 1
            fs.append(psub(y, (t,))); gates += 1
    p = fs[0]
    for f in fs[1:]:
        p = pmul(p, f); gates += 1
    check(f"family m={m}: (gates, roots)", (gates, len(integer_roots(p))),
          (3 if m == 0 else 3*m+4, 2*m+3))

print("\n== Lemma: confinement bound 396 is tight ==")
import itertools
def mono(rs):
    p = (1,)
    for r in rs: p = pmul(p, (-r, 1))
    return p
def trail(p):
    for c in p:
        if c: return c
    return 0
best = None
for esc in (33, -33, 40, 64, 100):
    for combo in itertools.combinations(range(-8, 9), 6):
        rs = list(combo) + [esc]
        if len(set(rs)) != 7: continue
        c = abs(trail(mono(rs)))
        if best is None or c < best: best = c
check("minimum |trailing| with an escaping root", best, 396)
check("witness A trailing coefficient", trail(pA), 48)
check("witness B trailing coefficient", trail(pB), -64)

print("\n== Proposition: zpmax lower bound x^(2^k)-1 ==")
def first_prime_1_mod(m):
    n = m+1
    while True:
        if n > 2:
            d, isp = 2, True
            while d*d <= n:
                if n % d == 0: isp = False; break
                d += 1
            if isp: return n
        n += m
for k, wantp in zip(range(1,9), [3,5,17,17,97,193,257,257]):
    m = 2**k; p = first_prime_1_mod(m)
    roots = sum(1 for v in range(p) if pow(v, m, p) == 1 % p)
    check(f"k={k}: (prime, roots of x^(2^k)-1)", (p, roots), (wantp, m))

print("\n== The real ladder and its doubling family ==")
a = pmul((0,1),(0,1)); b = psub(a,(1,)); c = pmul(b,b); g = psub(c,a)
check("tau=4 record: (gates, real roots)", (4, zreal(g)), (4, 4))
e5 = pmul(b, g)
check("tau=5 record: (gates, real, integer)", (5, zreal(e5), len(integer_roots(e5))), (5, 6, 2))
check("tau=5 record factorization",
      str(sp.factor(sp.Poly(list(reversed(e5)), x).as_expr())),
      "(x - 1)*(x + 1)*(x**2 - x - 1)*(x**2 + x - 1)")
gg, gates, seq = g, 4, [(4, len(g)-1, zreal(g))]
for _ in range(4):
    h = psub(gg, a); gg = pmul(gg, h); gates += 2
    seq.append((gates, len(gg)-1, zreal(gg)))
check("doubling family (gates, degree, real)", seq,
      [(4,4,4),(6,8,8),(8,16,16),(10,32,28),(12,64,48)])

print("\n== Splitting is cheap: q^8 ==")
q = psub(pmul((0,1),(0,1)), (0,1))
p = q
for _ in range(3): p = pmul(p, p)
check("q^8: (gates, degree, distinct integer roots)",
      (5, len(p)-1, sorted(integer_roots(p))), (5, 16, [0, 1]))

print()
print("FAILURES:", FAIL if FAIL else "none")
sys.exit(1 if FAIL else 0)
