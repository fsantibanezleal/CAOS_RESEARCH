"""Contingency probe for EXP-141 (not a result): does E2 (quadratic in s = q1^2) split over L, and are E5, E6
proportional over L? Writes a PARI script for nffactor and prints the proportionality test."""
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


def gp_el(cs):
    return "(" + "+".join(f"({c})*y^{j}" for j, c in enumerate(cs)) + ")"


d2 = {tuple(m): cs for m, cs in E[1]}
coef = [d2.get((0, 2 * j, 0, 0, 0, 0), [0] * 5) for j in range(3)]
s = ("nf=nfinit(y^5-y^4+3*y^3+3*y^2+26);\n"
     f"f=Mod({gp_el(coef[2])},nf.pol)*x^2+Mod({gp_el(coef[1])},nf.pol)*x+Mod({gp_el(coef[0])},nf.pol);\n"
     "F=nffactor(nf,lift(f)); print(\"E2 factors over L in s: \", #F[,1], \" factor(s) of degrees \", "
     "vector(#F[,1],i,poldegree(F[i,1],x)));\n"
     "g=nffactor(nf, subst(lift(f),x,x^2)); print(\"E2 factors over L in q1: degrees \", "
     "vector(#g[,1],i,poldegree(g[i,1],x)));\n")
open(os.path.join(_W141, "..", "e2factor.gp"), "w", newline="\n").write(s)
d5 = {tuple(m): el(cs) for m, cs in E[4]}
d6 = {tuple(m): el(cs) for m, cs in E[5]}
ms = sorted(d5)
m0 = ms[0]
prop = all(((d5[m] * d6[m0] - d6[m] * d5[m0]) % P) == 0 for m in ms)
print("E5, E6 proportional over L:", prop)
