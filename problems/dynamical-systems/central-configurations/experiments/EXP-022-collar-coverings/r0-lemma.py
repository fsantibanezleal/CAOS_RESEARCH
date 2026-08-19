"""Piece 9-prep: R_0 meets the open stratum NOWHERE (exact, symbolic).

R_0 = {J identically zero}. Four entries of J are single s-terms with
monomial brackets nonzero on the stratum (u, p > 0, e12 = 2):
  J[L23][m1] =  s(r12, d1A) * u * e12   -> d1A = r12 = 2
  J[L13][m2] = -s(r12, d2A) * u * e12   -> d2A = 2
  J[L25][m1] =  s(r12, d1B) * p * e12   -> d1B = 2
  J[L15][m2] = -s(r12, d2B) * p * e12   -> d2B = 2
d1A = d2A forces (1-v)^2 = (-1-v)^2, i.e. v = 0; d1B = d2B forces q = 0.
Then f = v - q = 0: OFF the open stratum (distinct heights). So
R_0 meet {f != 0} is EMPTY. This script verifies the algebra exactly.
"""
import sympy as sp

u, v, p, q = sp.symbols("u v p q", real=True)
d1A2 = u**2 + (1 - v)**2
d2A2 = u**2 + (-1 - v)**2
d1B2 = p**2 + (1 - q)**2
d2B2 = p**2 + (-1 - q)**2

# d1A = d2A  <=>  d1A^2 - d2A^2 = 0 (distances nonnegative)
e1 = sp.expand(d1A2 - d2A2)
e2 = sp.expand(d1B2 - d2B2)
print("d1A^2 - d2A^2 =", e1)          # expect -4v... : (1-v)^2-(1+v)^2 = -4v
print("d1B^2 - d2B^2 =", e2)
solv = sp.solve(e1, v)
solq = sp.solve(e2, q)
print("v =", solv, " q =", solq)
assert solv == [0] and solq == [0]
# and with v = q = 0: f = v - q = 0: excluded by the stratum hypothesis.
# (The d = 2 conditions then also force u = p = sqrt(3), but emptiness is
# already decided by f = 0.)
print("R_0 meet {f != 0} = EMPTY: verified")
