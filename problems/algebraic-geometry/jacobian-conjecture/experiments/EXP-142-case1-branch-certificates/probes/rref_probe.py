"""Contingency probe for EXP-142 (not a result): reduced row echelon form over L of the nine branch equations
(branch q1 = +c), columns ordered so that monomials with q5 come first, then q3, q4, q2, q0 (lexicographic on
(q5, q3, q4, q2, q0) descending). The L-span, hence the ideal, is unchanged. Reports each row's variables, terms,
degrees and height (primitive over Z)."""
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
names, eqs, src = d["names"], d["eqs"], d["from"]   # names q0, q2, q3, q4, q5
E = [{tuple(m): fmpq_poly([fmpq(c) for c in cs]) for m, cs in e} for e in eqs]


def inv(a):
    r0, r1, s0, s1 = P, a % P, fmpq_poly([0]), fmpq_poly([1])
    while r1.degree() > 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    return (s1 * fmpq_poly([1 / r1[0]])) % P


def key(m):          # m = (q0, q2, q3, q4, q5)
    return (m[4], m[2], m[3], m[1], m[0])


cols = sorted({k for e in E for k in e}, key=key, reverse=True)
rows = [[e.get(c, fmpq_poly([0])) for c in cols] for e in E]
r = 0
pivcols = []
for ci in range(len(cols)):
    piv = next((i for i in range(r, len(rows)) if rows[i][ci] != 0), None)
    if piv is None:
        continue
    rows[r], rows[piv] = rows[piv], rows[r]
    iv = inv(rows[r][ci])
    rows[r] = [(x * iv) % P for x in rows[r]]
    for i in range(len(rows)):
        if i != r and rows[i][ci] != 0:
            f = rows[i][ci]
            rows[i] = [(a - f * b) % P for a, b in zip(rows[i], rows[r])]
    pivcols.append(ci)
    r += 1
    if r == len(rows):
        break
for i, row in enumerate(rows):
    poly = {cols[j]: row[j] for j in range(len(cols)) if row[j] != 0}
    if not poly:
        print(f"row {i}: zero")
        continue
    used = [names[t] for t in range(5) if any(k[t] for k in poly)]
    degs = {names[t]: max(k[t] for k in poly) for t in range(5) if any(k[t] for k in poly)}
    den = 1
    for v in poly.values():
        for t in range(5):
            den = lcm(den, int(v[t].q))
    ints = [int(v[t] * den) for v in poly.values() for t in range(5)]
    g = 0
    for x in ints:
        g = gcd(g, x)
    dig = max(len(str(abs(x // g))) for x in ints if x)
    lead = cols[pivcols[i]] if i < len(pivcols) else None
    print(f"row {i}: lead {dict((names[t], x) for t, x in enumerate(lead) if x) if lead else None}, variables {used}, "
          f"terms {len(poly)}, degrees {degs}, max digits {dig}")


# dump the nonzero rows in cert.py format (integer coordinates, primitive), with their heights
dump, info = [], []
for i, row in enumerate(rows):
    poly = {cols[j]: row[j] for j in range(len(cols)) if row[j] != 0}
    if not poly:
        continue
    den = 1
    for v in poly.values():
        for t in range(5):
            den = lcm(den, int(v[t].q))
    ints = [(list(k), [int(v[t] * den) for t in range(5)]) for k, v in poly.items()]
    g = 0
    for _, cs in ints:
        for x in cs:
            g = gcd(g, x)
    ints = [(k, [x // g for x in cs]) for k, cs in ints]
    dump.append(ints)
    info.append(max(len(str(abs(x))) for _, cs in ints for x in cs))
json.dump({"nvars": 5, "names": names, "eqs": dump, "digits": info}, open(os.path.join(_W142, "rref_plus/eqs.json"), "w"))
print("dumped", len(dump), "rows; digits", info)
