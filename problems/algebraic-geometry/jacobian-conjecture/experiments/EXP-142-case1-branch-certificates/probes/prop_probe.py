"""Contingency probe for EXP-142 (not a result): are the coefficients of q5 (and q3) proportional over L across the
branch equations? If c_v(E_a) = lambda c_v(E_b) with lambda in L, then E_a - lambda E_b is free of v."""
import os
from pathlib import Path as _P
_EXP141 = str(_P(__file__).resolve().parents[2] / "EXP-141-case1-modular-certificate")
_W141 = os.environ["JCB141_WORK"]   # cert.py build output (eqs.json)
_W142 = os.environ.get("JCB142_WORK", "")   # branches.py output (branch_plus/, branch_minus/)
import json
from itertools import combinations

from flint import fmpq, fmpq_poly

P = fmpq_poly([26, 0, 3, 3, -1, 1])
d = json.load(open(os.path.join(_W142, "branch_plus/eqs.json")))
names, eqs, src = d["names"], d["eqs"], d["from"]


def el(cs):
    return fmpq_poly([fmpq(c) for c in cs])


def coeff(e, v):
    """coefficient of variable v (degree 1 part) as {monomial without v: L element}"""
    out = {}
    for m, cs in e:
        if m[v] == 1:
            k = tuple(x if j != v else 0 for j, x in enumerate(m))
            out[k] = el(cs)
    return out


def proportional(a, b):
    if set(a) != set(b):
        return False
    ks = sorted(a)
    k0 = ks[0]
    return all(((a[k] * b[k0] - b[k] * a[k0]) % P) == 0 for k in ks)


for v in (4, 2):
    cs = {f: coeff(e, v) for e, f in zip(eqs, src)}
    groups = []
    for f in src:
        for g in groups:
            if proportional(cs[f], cs[g[0]]):
                g.append(f)
                break
        else:
            groups.append([f])
    print(f"{names[v]}: classes of L-proportional coefficients (by equation): {groups}")
