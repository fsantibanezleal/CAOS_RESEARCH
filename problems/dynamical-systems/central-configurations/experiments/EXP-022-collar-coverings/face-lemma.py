"""Lemma piece 10: the corner-face rank floor (uniform in the shell index).

Setting (cb1 chart): pair B collapses onto axis body 1,
  p = rhoc * csig, q = 1 + rhoc * ssig,  csig^2 + ssig^2 = 1, csig >= 0,
pair A at a general bounded (u, v). The covering certifies every dyadic
shell {rhoc in [h 2^-k-1, h 2^-k]} but never a box containing rhoc = 0,
where the matrix genuinely drops to rank 2 (bodies 5, 6 sitting on body 1
is a collision, outside the stratum). A UNIFORM statement over all k
closes the collar in one step, and since R_2 is closed and every point of
the punctured collar lies in some shell, it closes the collar entirely.

This script computes, EXACTLY, the leading rhoc-order of the 3 x 3 minor
  M = det [ {L15, L23, L25} x {m1, m2, mA} ]
(the minor the interval covering itself selects on the shells) and prints
its leading coefficient, factored. Rank >= 3 for all small rhoc > 0 then
holds wherever that coefficient is nonzero; its zero set is the residual
locus, to be listed explicitly.

Exact clearings used (no radical cancellation):
  d2B^2 - 4 = rhoc (4 ssig + rhoc)      [so s(r12, d2B) = O(rhoc)]
  p^3 / d1B^3 = csig^3                  [d1B = rhoc exactly]
"""
import sympy as sp

rc, cs, ss, u, v = sp.symbols("rhoc csig ssig u v", real=True)

h1 = 1 - v
gam = -1 - v
p = rc * cs
q = 1 + rc * ss
g1 = 1 - q          # = -rc ss
g2 = -1 - q         # = -2 - rc ss
f = v - q
d1A = sp.sqrt(u**2 + h1**2)
d2A = sp.sqrt(u**2 + gam**2)
d1B = rc                     # exact
d2B = sp.sqrt(p**2 + (2 + rc * ss)**2)
cs_d = sp.sqrt((u - p)**2 + f**2)
cx_d = sp.sqrt((u + p)**2 + f**2)
r12 = 2
s = lambda a, b: 1 / a**3 - 1 / b**3

# rows (scaled as in cb1.py): L15 / rhoc, L23 / rhoc... but for the LEADING
# ORDER we work with the raw entries and read the rhoc-order off directly.
L15_m1 = 0
L15_m2 = s(r12, d2B) * (-p * 2)
L15_mA = s(d1A, cs_d) * (u * g1 - p * h1) + s(d1A, cx_d) * (-(p * h1 + u * g1))
L23_m1 = s(r12, d1A) * (u * 2)
L23_m2 = 0
L23_mA = s(d2A, 2 * u) * (-2 * u * gam)
L25_m1 = s(r12, d1B) * (p * 2)
L25_m2 = 0
L25_mA = s(d2A, cs_d) * (u * g2 - p * gam) + s(d2A, cx_d) * (-(p * gam + u * g2))

M = sp.Matrix([[L15_m1, L15_m2, L15_mA],
               [L23_m1, L23_m2, L23_mA],
               [L25_m1, L25_m2, L25_mA]])
# expand the determinant along the m2 column (only L15 has one):
#   det = -L15_m2 * det[[L23_m1, L23_mA], [L25_m1, L25_mA]]
sub2 = L23_m1 * L25_mA - L23_mA * L25_m1
det = -L15_m2 * sub2
print("det = -(L15,m2) * [(L23,m1)(L25,mA) - (L23,mA)(L25,m1)]")

# leading order of each factor in rhoc
def order_and_lead(expr, nmax=4):
    e = sp.simplify(sp.together(expr))
    for k in range(nmax + 1):
        lead = sp.limit(e / rc**k, rc, 0)
        if lead != 0 and lead != sp.zoo and not lead.has(sp.oo):
            return k, sp.simplify(lead)
    return None, None

k1, c1 = order_and_lead(L15_m2)
print(f"(L15,m2): order rhoc^{k1}, leading coefficient = {sp.factor(c1)}")

k2, c2 = order_and_lead(sub2)
print(f"2x2 block: order rhoc^{k2}, leading coefficient = {sp.factor(sp.simplify(c2))}")

if k1 is not None and k2 is not None:
    print(f"\nMINOR ORDER: rhoc^{k1 + k2}")
    lead = sp.factor(sp.simplify(-c1 * c2))
    print("LEADING COEFFICIENT (factored):")
    sp.pprint(lead)
    print("\nzero set of the leading coefficient = the residual locus")
    num, den = sp.fraction(sp.together(lead))
    print("numerator factors:")
    for fac, mult in sp.factor_list(sp.expand(num))[1]:
        print(f"   {fac}   (multiplicity {mult})")
