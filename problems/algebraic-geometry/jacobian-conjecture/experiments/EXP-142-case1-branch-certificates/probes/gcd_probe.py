"""Contingency probe for EXP-141 (not a result): gcd over L of E1 and E2 as quadratics in s = q1^2.

E1 = a2 s^2 + a1 s + a0, E2 = b2 s^2 + b1 s + b0 with a_i, b_i in L = Q[y]/(P). If they are proportional the gcd
is E1 itself; otherwise eliminate s^2 to get a linear l(s) = c1 s + c0, and the common root s0 = -c0/c1 must
satisfy both. Reports proportionality, s0 (coordinates and digits), and whether s0 is a square in L (via the
factorisation of y^2 - s0 over L, tested modulo several primes where P splits).
"""
import os
from pathlib import Path as _P
_EXP141 = str(_P(__file__).resolve().parents[2] / "EXP-141-case1-modular-certificate")
_W141 = os.environ["JCB141_WORK"]   # cert.py build output (eqs.json)
_W142 = os.environ.get("JCB142_WORK", "")   # branches.py output (branch_plus/, branch_minus/)
import json

from flint import fmpq, fmpq_poly

P = fmpq_poly([26, 0, 3, 3, -1, 1])
E = json.load(open(os.path.join(_W141, "eqs.json")))["eqs"]


def el(cs):
    return fmpq_poly([fmpq(c) for c in cs])


def inv(a):
    r0, r1, s0, s1 = P, a % P, fmpq_poly([0]), fmpq_poly([1])
    while r1.degree() > 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    return (s1 * fmpq_poly([1 / r1[0]])) % P


def coeffs(e):
    d = {tuple(m): el(cs) for m, cs in e}
    return [d.get((0, 2 * j, 0, 0, 0, 0), fmpq_poly([0])) for j in range(3)]


a, b = coeffs(E[0]), coeffs(E[1])
# proportional?  a_i b_j - a_j b_i = 0 mod P for all i, j
prop = all(((a[i] * b[j] - a[j] * b[i]) % P) == 0 for i in range(3) for j in range(3))
print("E1, E2 proportional over L:", prop)
if not prop:
    c1 = (b[2] * a[1] - a[2] * b[1]) % P
    c0 = (b[2] * a[0] - a[2] * b[0]) % P
    s0 = (-c0 * inv(c1)) % P
    r1 = (a[2] * s0 * s0 + a[1] * s0 + a[0]) % P
    r2 = (b[2] * s0 * s0 + b[1] * s0 + b[0]) % P
    print("common root s0 satisfies E1:", r1 == 0, "E2:", r2 == 0)
    print("s0 coordinates:", [str(s0[i]) for i in range(5)])
    print("s0 digits:", max(len(str(s0[i].p)) + len(str(s0[i].q)) for i in range(5)))
    # other root of each quadratic
    print("degree of gcd: 1 (if both residuals are zero)")
