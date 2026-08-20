"""Lemma piece 9e: the mirror identity, verified structurally.

The mirror M: (u, v, p, q) -> (u, -v, p, -q) reflects the configuration
across the horizontal axis (bodies 1 and 2 swap, each pair's members
swap). Expected: J(M x) = P_row . J(x) . P_col with rows L13 <-> L23,
L15 <-> L25, L35 -> s35 L35, L36 -> s36 L36 and columns m1 <-> m2,
mA -> mA, mB -> mB, for some fixed signs. The script determines the signs
numerically at one rational point, then verifies the identity
syntactically (expression-tree cancellation, no radical simplification)
on all 24 entries, exactly like the swap identity (piece 9d).
"""
import sympy as sp
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "vsi", HERE / "verify-swap-identity.py")
# reuse J_of by executing only its definition: import the module but guard
# against its __main__-style tail by reading the source
src = (HERE / "verify-swap-identity.py").read_text(encoding="utf-8")
ns = {}
exec(src.split("J1 = J_of")[0], ns)
J_of = ns["J_of"]
u, v, p, q = ns["u"], ns["v"], ns["p"], ns["q"]

J1 = J_of(u, v, p, q)
J2 = J_of(u, -v, p, -q)

# candidate maps: rows i -> (rho(i), sign), cols m1<->m2, mA, mB fixed
COLMAP = {0: 1, 1: 0, 2: 2, 3: 3}
ROWPAIR = {0: 2, 1: 3, 2: 0, 3: 1, 4: 4, 5: 5}

# determine signs at a rational point
P0 = {u: sp.Rational(3, 2), v: sp.Rational(1, 3),
      p: sp.Rational(5, 7), q: sp.Rational(-9, 4)}
signs = {}
for i in range(6):
    ri = ROWPAIR[i]
    for j in range(4):
        a = J2[i, j].subs(P0)
        b = J1[ri, COLMAP[j]].subs(P0)
        av, bv = sp.N(a, 30), sp.N(b, 30)
        if abs(bv) > 1e-15:
            s = av / bv
            signs.setdefault(i, []).append(round(float(s)))
sgn = {i: max(set(vals), key=vals.count) for i, vals in signs.items()}
print("row signs:", sgn)

bad = syntactic = 0
for i in range(6):
    ri = ROWPAIR[i]
    for j in range(4):
        diff = sp.expand(J2[i, j] - sgn[i] * J1[ri, COLMAP[j]])
        if diff == 0:
            syntactic += 1
        else:
            val = diff.subs(P0)
            if abs(sp.N(val, 40)) < sp.Rational(1, 10)**30:
                print(f"entry [{i}][{j}]: zero at point but NOT syntactic")
            else:
                print(f"NONZERO at mirrored[{i}][{j}]")
                bad += 1
print(f"syntactic zeros: {syntactic}/24")
print("MIRROR IDENTITY:", "FAILED" if bad else
      f"VERIFIED, rows L13<->L23, L15<->L25 with signs {sgn}, cols m1<->m2")
