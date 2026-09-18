"""Eliminate p from the exact cross system to get u*'s minimal polynomial.

cross-exact-system.py produced two integer-coefficient polynomials g1 and
g2 in (u, p) that cut out the degenerate cross configuration, verified to
vanish at the numeric point to relative 1e-60. Taking their resultant in p
leaves a univariate polynomial that u* must satisfy, which turns the
forty-digit numeric into an exact algebraic statement.

The resultant of a 2027-term and a 936-term polynomial is large, so this
runs the elimination modulo several primes first to learn the degree
cheaply, and only then attempts it over the integers.
"""
import pickle
import sympy as sp

u, p = sp.symbols("u p")

with open("artifacts/cross-exact-g1g2.pkl", "rb") as fh:
    d = pickle.load(fh)
g1 = sp.sympify(d["g1"])
g2 = sp.sympify(d["g2"])

P1 = sp.Poly(g1, p)
P2 = sp.Poly(g2, p)
print(f"g1: degree in p = {P1.degree()}, in u = {sp.Poly(g1, u).degree()}")
print(f"g2: degree in p = {P2.degree()}, in u = {sp.Poly(g2, u).degree()}")
print("")

print("modular elimination, to learn the degree in u cheaply")
for q in (10007, 10009, 10037):
    try:
        R = sp.resultant(sp.Poly(g1, p, u, modulus=q),
                         sp.Poly(g2, p, u, modulus=q), p)
        Ru = sp.Poly(R, u, modulus=q)
        fac = sp.factor_list(Ru.as_expr(), modulus=q)
        degs = sorted(sp.Poly(f, u, modulus=q).degree() for f, _ in fac[1])
        print(f"  mod {q}: resultant degree in u = {Ru.degree()}, "
              f"irreducible factor degrees {degs}")
    except Exception as e:
        print(f"  mod {q}: failed ({type(e).__name__}: {e})")

print("")
print("elimination over the integers")
R = sp.resultant(g1, g2, p)
Ru = sp.Poly(sp.expand(R), u)
print(f"  degree in u = {Ru.degree()}, "
      f"largest coefficient has {len(str(max(abs(c) for c in Ru.all_coeffs())))} digits")

print("")
print("factoring, and locating the factor that vanishes at u*")
uv = sp.Float("0.630918137106736797167988596864253187098618034747723407767631", 70)
facs = sp.factor_list(Ru.as_expr())
print(f"  {len(facs[1])} irreducible factors")
best = None
for f, mult in facs[1]:
    dg = sp.Poly(f, u).degree()
    val = abs(sp.N(f.subs(u, uv), 60))
    coeffs = sp.Poly(f, u).all_coeffs()
    scale = max(abs(sp.N(c * uv**k, 60))
                for k, c in enumerate(reversed(coeffs)))
    rel = float(val / scale) if scale != 0 else float(val)
    print(f"    degree {dg:>4}  mult {mult}  |f(u*)|/scale = {rel:.3e}")
    if best is None or rel < best[0]:
        best = (rel, f, dg)

print("")
if best and best[0] < 1e-40:
    rel, f, dg = best
    print(f"MINIMAL POLYNOMIAL of u*: degree {dg}")
    print(f"  relative residual at u*: {rel:.3e}")
    co = sp.Poly(f, u).all_coeffs()
    print(f"  {len(co)} coefficients, largest has "
          f"{len(str(max(abs(c) for c in co)))} digits")
    with open("artifacts/cross-minimal-poly.txt", "w", encoding="utf-8") as fh:
        fh.write(f"degree {dg}\n")
        fh.write(sp.srepr(f) + "\n\n")
        fh.write(str(sp.expand(f)) + "\n")
    print("  written to artifacts/cross-minimal-poly.txt")
    print("")
    print("  roots near u* (real, in the search window):")
    for r in sp.Poly(f, u).nroots(n=50, maxsteps=200):
        if abs(sp.im(r)) < 1e-40 and 0 < sp.re(r) < 4:
            print(f"    {sp.N(sp.re(r), 40)}")
else:
    print("no factor vanishes at u* to the required tolerance; the "
          "elimination did not isolate it")
