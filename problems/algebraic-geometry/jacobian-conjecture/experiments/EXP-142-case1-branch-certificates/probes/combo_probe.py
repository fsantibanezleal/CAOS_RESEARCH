"""Contingency probe for EXP-142 (not a result): E7 - lambda E3 and E13 - mu E3 on the branch q1 = +c, with lambda,
mu in L fixed by the q5 coefficients; reports the variables left, the terms and the heights (primitive over Z)."""
import os
from pathlib import Path as _P
_EXP141 = str(_P(__file__).resolve().parents[2] / "EXP-141-case1-modular-certificate")
_W141 = os.environ["JCB141_WORK"]   # cert.py build output (eqs.json)
_W142 = os.environ.get("JCB142_WORK", "")   # branches.py output (branch_plus/, branch_minus/)
import json
from math import gcd, lcm

from flint import fmpq, fmpq_poly

P = fmpq_poly([26, 0, 3, 3, -1, 1])
d = json.load(open(os.path.join(_W142, "branch_plus/eqs.json")))
names, eqs, src = d["names"], d["eqs"], d["from"]
E = {f: {tuple(m): fmpq_poly([fmpq(c) for c in cs]) for m, cs in e} for e, f in zip(eqs, src)}


def inv(a):
    r0, r1, s0, s1 = P, a % P, fmpq_poly([0]), fmpq_poly([1])
    while r1.degree() > 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    return (s1 * fmpq_poly([1 / r1[0]])) % P


def report(name, poly):
    poly = {k: v for k, v in poly.items() if v != 0}
    used = [names[i] for i in range(5) if any(k[i] for k in poly)]
    den = 1
    for v in poly.values():
        for i in range(5):
            den = lcm(den, int(v[i].q))
    ints = [int(v[i] * den) for v in poly.values() for i in range(5)]
    g = 0
    for x in ints:
        g = gcd(g, x)
    dig = max(len(str(abs(x // g))) for x in ints if x)
    degs = {names[i]: max(k[i] for k in poly) for i in range(5) if any(k[i] for k in poly)}
    print(f"{name}: variables {used}, terms {len(poly)}, degrees {degs}, max digits {dig}")
    return poly


k5 = (0, 0, 0, 0, 1)                      # the monomial q5 alone
combos = {}
for f in (7, 13):
    lam = (E[f][k5] * inv(E[3][k5])) % P
    combos[f] = {k: (E[f].get(k, fmpq_poly([0])) - lam * E[3].get(k, fmpq_poly([0]))) % P
                 for k in set(E[f]) | set(E[3])}
    report(f"E{f} - lambda E3", combos[f])
report("E3 (for reference)", E[3])
json.dump({f"E{f}c": [[list(k), [str(v[i]) for i in range(5)]] for k, v in combos[f].items() if v != 0]
           for f in combos}, open(os.path.join(_W142, "combos.json"), "w"))
