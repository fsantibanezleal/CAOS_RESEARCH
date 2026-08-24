"""Are the two cross polynomials coprime? That decides FINITENESS exactly.

g1 and g2 cut out the degenerate cross configurations. They have degree 56
in p and 54 in u, so eliminating p over the integers is out of reach and a
univariate minimal polynomial is not worth chasing. But the question that
actually matters is cheaper: if g1 and g2 share no common factor, their
common zero set is zero-dimensional, so there are FINITELY many degenerate
cross configurations, exactly, and the numerical census claiming one is a
statement about which of finitely many are real and admissible.

A common factor would instead mean a CURVE of degenerate configurations,
which would be a much bigger deal and would break the dimension count.
"""
import pickle
import sympy as sp

u, p, C, D, lam = sp.symbols("u p C D lam", positive=True)

with open("artifacts/cross-exact-g1g2.pkl", "rb") as fh:
    d = pickle.load(fh)
g1 = sp.sympify(d["g1"])
g2 = sp.sympify(d["g2"])

P1 = sp.Poly(g1, u, p)
P2 = sp.Poly(g2, u, p)
print(f"g1: total degree {P1.total_degree()}, "
      f"deg_u {P1.degree(u)}, deg_p {P1.degree(p)}, {len(P1.terms())} terms")
print(f"g2: total degree {P2.total_degree()}, "
      f"deg_u {P2.degree(u)}, deg_p {P2.degree(p)}, {len(P2.terms())} terms")
print("")

print("content and primitive parts (a shared monomial factor is not a curve")
print("of configurations, it is the coordinate axes, so strip it first)")
c1, pp1 = P1.primitive()
c2, pp2 = P2.primitive()
print(f"  content(g1) = {c1}")
print(f"  content(g2) = {c2}")

mon1 = sp.factor_list(pp1.as_expr())
mon2 = sp.factor_list(pp2.as_expr())
print(f"  g1 factors into {len(mon1[1])} irreducible pieces: "
      + ", ".join(f"deg {sp.Poly(f, u, p).total_degree()}^{m}"
                  for f, m in mon1[1]))
print(f"  g2 factors into {len(mon2[1])} irreducible pieces: "
      + ", ".join(f"deg {sp.Poly(f, u, p).total_degree()}^{m}"
                  for f, m in mon2[1]))
print("")

G = sp.gcd(pp1.as_expr(), pp2.as_expr())
PG = sp.Poly(G, u, p)
print(f"gcd(g1, g2) has total degree {PG.total_degree()}")
if PG.total_degree() == 0:
    print("  COPRIME: the common zero set is zero-dimensional, so there are")
    print("  FINITELY many degenerate cross configurations. Exactly.")
else:
    print(f"  COMMON FACTOR: {sp.factor(G)}")
    print("  a curve of degenerate configurations would break the count;")
    print("  check whether the factor is physical or a coordinate artifact")

print("")
print("which irreducible factor of each actually vanishes at the point?")
uv = sp.Float("0.630918137106736797167988596864253187098618034747723407767631", 70)
pv = sp.Float("1.45090746590807305719166080680651095948633549667961704443288", 70)


def rel_at(f):
    P = sp.Poly(f, u, p)
    val = abs(sp.N(f.subs({u: uv, p: pv}), 60))
    scale = max(abs(sp.N(co * uv**mu * pv**mp, 60))
                for (mu, mp), co in zip(P.monoms(), P.coeffs()))
    return float(val / scale) if scale != 0 else float(val)


live = []
for tag, facs in (("g1", mon1[1]), ("g2", mon2[1])):
    for f, m in facs:
        r = rel_at(f)
        P = sp.Poly(f, u, p)
        mark = "  <== vanishes at the point" if r < 1e-40 else ""
        print(f"  {tag} factor deg {P.total_degree():>3} "
              f"(u {P.degree(u)}, p {P.degree(p)}) mult {m}: "
              f"relative value {r:.2e}{mark}")
        if r < 1e-40:
            live.append((tag, f))

if len(live) >= 2:
    print("")
    f1 = live[0][1]
    f2 = next(f for t, f in live if t != live[0][0])
    G2 = sp.gcd(f1, f2)
    dg = sp.Poly(G2, u, p).total_degree()
    print(f"gcd of the two LIVE factors has total degree {dg}")
    if dg == 0:
        print("  coprime, so the point is an isolated common zero of the two")
        print("  irreducible curves that actually pass through it")
        b1 = sp.Poly(f1, u, p).total_degree()
        b2 = sp.Poly(f2, u, p).total_degree()
        print(f"  Bezout bound on their intersections: {b1} * {b2} = "
              f"{b1 * b2} points counted with multiplicity over C")
    else:
        print(f"  they share {sp.factor(G2)}")
