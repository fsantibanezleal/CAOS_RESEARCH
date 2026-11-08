"""Contingency probe for EXP-142 (not a result): exact std over Q(y) (minpoly P) of the branch q1 = +c ideal, with
the small quadric S = E7 - lambda E3 added (it lies in the ideal), ordering dp on (q5, q3, q4, q2, q0). Writes a
Singular script; prints UNIT / NONUNIT and the time when it finishes."""
import os
from pathlib import Path as _P
_EXP141 = str(_P(__file__).resolve().parents[2] / "EXP-141-case1-modular-certificate")
_W141 = os.environ["JCB141_WORK"]   # cert.py build output (eqs.json)
_W142 = os.environ.get("JCB142_WORK", "")   # branches.py output (branch_plus/, branch_minus/)
import json
from fractions import Fraction
from pathlib import Path

d = json.load(open(os.path.join(_W142, "branch_plus/eqs.json")))
names, eqs = d["names"], d["eqs"]
combos = json.load(open(os.path.join(_W142, "combos.json")))


def lp(cs):
    parts = []
    for j, c in enumerate(cs):
        c = Fraction(c)
        if c:
            cstr = str(c.numerator) if c.denominator == 1 else f"{c.numerator}/{c.denominator}"
            parts.append(f"({cstr})" + (f"*y^{j}" if j > 1 else ("*y" if j == 1 else "")))
    return "(" + "+".join(parts) + ")"


def poly(terms):
    out = []
    for m, cs in terms:
        facs = [f"{names[i]}^{x}" if x > 1 else names[i] for i, x in enumerate(m) if x]
        out.append(lp(cs) + ("*" + "*".join(facs) if facs else ""))
    return "+".join(out)


gens = [poly(combos["E7c"])] + [poly(e) for e in eqs]
s = ("ring R=(0,y),(q5,q3,q4,q2,q0),dp;\nminpoly=y^5-y^4+3*y^3+3*y^2+26;\noption(redSB);\nideal I=\n" +
     ",\n".join(gens) + ";\nint t0=timer;\nideal J=std(I);\n"
     "if(size(J)==1 && deg(J[1])==0){ \"UNIT\"; } else { \"NONUNIT DIM=\"+string(dim(J))+\" SIZE=\"+string(size(J)); }\n"
     "\"SECONDS=\"+string(timer-t0);\nquit;\n")
Path(os.path.join(_W142, "exact_plus.sing")).write_text(s, encoding="utf-8", newline="\n")
print("written", len(s), "bytes")
