"""The EXACT algebraic system for the degenerate cross configuration.

PSLQ found nothing real (its best candidate had residual 1e-41 against a
tolerance of 1e-180, so it was spurious), which means the algebraic degree
is higher than a blind search reaches. The system can be written down
directly instead.

Bodies: (0, +-1) with mass m1, (+-u, 0) with mass mA, (+-p, 0) with mass
mB. Symmetry puts the centre of mass at the origin and forces the two axis
masses equal, so the central-configuration equations reduce to three
scalar conditions, each LINEAR in (m1, mA, mB, lambda):

  E1, at (u, 0):
     -2u C m1  -  mA/(4u^2)  +  mB [1/(p-u)^2 - 1/(p+u)^2]  +  lambda u = 0
  E2, at (p, 0):
     -2p D m1  -  mA [1/(p-u)^2 + 1/(p+u)^2]  -  mB/(4p^2)  + lambda p = 0
  E3, at (0, 1):
     -m1/4  -  2 C mA  -  2 D mB  +  lambda = 0

with C = (u^2+1)^(-3/2) and D = (p^2+1)^(-3/2), which are algebraic:
C^2 (u^2+1)^3 = 1 and D^2 (p^2+1)^3 = 1.

A degenerate configuration is one where this 3 x 4 matrix drops to rank 2,
so every 3 x 3 minor vanishes. Two independent minors, together with the
two algebraic relations for C and D, cut out the point. Eliminating C, D
and then p by resultants leaves a polynomial in u alone, which is the
exact object the numeric approximates.
"""
import sympy as sp

u, p, C, D, lam = sp.symbols("u p C D lam", positive=True)

A1 = sp.Rational(1, 4) / u**2
A2 = sp.Rational(1, 4) / p**2
B1 = 1 / (p - u)**2
B2 = 1 / (p + u)**2

M = sp.Matrix([
    [-2 * u * C, -A1, B1 - B2, u],
    [-2 * p * D, -(B1 + B2), -A2, p],
    [sp.Rational(-1, 4), -2 * C, -2 * D, 1],
])

print("the 3 x 4 system")
sp.pprint(M)

cols = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
minors = []
for cs in cols:
    d = M[:, list(cs)].det()
    num, den = sp.fraction(sp.together(sp.simplify(d)))
    minors.append(sp.expand(num))
    print("")
    print(f"minor on columns {cs}: numerator has "
          f"{len(sp.Poly(num, u, p, C, D).terms())} terms")

relC = sp.expand(C**2 * (u**2 + 1)**3 - 1)
relD = sp.expand(D**2 * (p**2 + 1)**3 - 1)

print("")
print("eliminating C and D by resultants")
f1, f2 = minors[0], minors[1]
step = sp.resultant(f1, relC, C)
print(f"  res(minor0, relC; C): degree in D = "
      f"{sp.Poly(step, D).degree() if step.has(D) else 0}")
step = sp.resultant(step, relD, D)
g1 = sp.factor(step)
print(f"  then in D: expression with "
      f"{len(sp.Poly(sp.expand(step), u, p).terms())} terms in (u, p)")

step2 = sp.resultant(f2, relC, C)
step2 = sp.resultant(step2, relD, D)
g2 = sp.factor(step2)
print(f"  second minor likewise: "
      f"{len(sp.Poly(sp.expand(step2), u, p).terms())} terms")

import pickle
with open("artifacts/cross-exact-g1g2.pkl", "wb") as fh:
    pickle.dump({"g1": sp.srepr(sp.expand(step)),
                 "g2": sp.srepr(sp.expand(step2))}, fh)
print("")
print("saved the two (u, p) polynomials to artifacts/cross-exact-g1g2.pkl")

print("")
print("numerical check: both must vanish at the known point")
uv = sp.Float("0.630918137106736797167988596864253187098618034747723407767631", 60)
pv = sp.Float("1.45090746590807305719166080680651095948633549667961704443288", 60)
for nm, g in (("g1", sp.expand(step)), ("g2", sp.expand(step2))):
    val = g.subs({u: uv, p: pv})
    scale = max(abs(float(t.subs({u: uv, p: pv})))
                for t in sp.Add.make_args(g)[:400])
    print(f"  {nm}({{u*, p*}}) = {sp.N(val, 20)}   (largest term ~ {scale:.3e})")
