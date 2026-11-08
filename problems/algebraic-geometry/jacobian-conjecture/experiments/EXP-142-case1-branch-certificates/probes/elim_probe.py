"""Contingency probe for EXP-142 (not a result): elimination structure of the branch system q1 = +c.

For each kept equation: degree in each variable, and for each variable v of degree 1, whether the coefficient of v
is a constant (an element of L, no other variable), so that v can be solved for exactly and substituted. Also
factors each equation over L with PARI (nffactor on the multivariate polynomial is not available, so it reports
the content in L and whether the equation factors after setting the other variables to small random integers).
"""
import os
from pathlib import Path as _P
_EXP141 = str(_P(__file__).resolve().parents[2] / "EXP-141-case1-modular-certificate")
_W141 = os.environ["JCB141_WORK"]   # cert.py build output (eqs.json)
_W142 = os.environ.get("JCB142_WORK", "")   # branches.py output (branch_plus/, branch_minus/)
import json
from collections import defaultdict

d = json.load(open(os.path.join(_W142, "branch_plus/eqs.json")))
names, eqs, src = d["names"], d["eqs"], d["from"]
for e, f in zip(eqs, src):
    degs = [max(m[i] for m, _ in e) for i in range(5)]
    tot = max(sum(m) for m, _ in e)
    lin = []
    for i in range(5):
        if degs[i] == 1:
            coeff_monos = [tuple(x if j != i else 0 for j, x in enumerate(m)) for m, _ in e if m[i] == 1]
            const = all(sum(cm) == 0 for cm in coeff_monos)
            lin.append(f"{names[i]}({'const' if const else 'poly ' + str(len(coeff_monos)) + ' terms'})")
    print(f"E{f}: terms {len(e)}, total degree {tot}, degrees {dict(zip(names, degs))}, linear in {lin}")
