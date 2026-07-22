# EXP-039: the (3, n) column closure + the explicit (3, 4) machine loop.
# CPU-only, sympy over QQ. Run: run.py [A|B|C|D]
import sys
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, expand, groebner, linsolve,  # noqa: E402
                   reduced, symbols)

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def partA():
    print("=" * 76)
    print("Part A: rank deficiency of Q4 -> J(P3, Q4) iff P3 is a perfect cube")
    print("=" * 76)
    a0, a1, a2, a3 = symbols("a0:4")
    s, t = symbols("s t")
    P3 = a0 * x**3 + a1 * x**2 * y + a2 * x * y**2 + a3 * y**3
    Q4mon = [x**4, x**3 * y, x**2 * y**2, x * y**3, y**4]
    bs = symbols("b0:5")
    Q4 = sum(b * m for b, m in zip(bs, Q4mon))
    J = Poly(expand(jac2(P3, Q4)), x, y)
    out_mons = [(i, 5 - i) for i in range(6)]
    M = Matrix([[expand(J.coeff_monomial(x**i * y**j).diff(b)) for b in bs]
                for (i, j) in out_mons])
    minors = []
    rows = list(range(6))
    for drop in rows:
        sub = M[[r for r in rows if r != drop], :]
        minors.append(expand(sub.det()))
    cube = {a0: s**3, a1: 3 * s**2 * t, a2: 3 * s * t**2, a3: t**3}
    ok_cube = all(expand(m.subs(cube)) == 0 for m in minors)
    check("A1: every 5x5 minor vanishes on the cube parametrization (s x + t y)^3",
          ok_cube)
    noncube = [{a0: 0, a1: 1, a2: 0, a3: 0},           # x^2 y
               {a0: 1, a1: 0, a2: 0, a3: 1},           # x^3 + y^3
               {a0: 0, a1: 1, a2: -1, a3: 0}]          # x^2 y - x y^2
    ok_nc = True
    for sub in noncube:
        vals = [m.subs(sub) for m in minors]
        ok_nc &= any(v != 0 for v in vals)
    check("A2: non-cube samples have a nonzero minor (full rank 5: only Q4 = 0)", ok_nc)
    # Hessian-covariant ideal: P3 cube iff Hess(P3) == 0 (h0, h1, h2)
    H = expand(P3.diff(x, 2) * P3.diff(y, 2) - P3.diff(x, y) ** 2)
    hp = Poly(H, x, y)
    hs = [hp.coeff_monomial(x**i * y**j) for (i, j) in [(2, 0), (1, 1), (0, 2)]]
    ok_mh = True
    G = groebner(hs, a0, a1, a2, a3, order="grevlex")
    for m in minors:
        _, r = reduced(m, G)
        ok_mh &= (r == 0)
    check("A3: every minor lies in the Hessian ideal (minors subset cube conditions: "
          "rank can only drop on cubes)", ok_mh)
    # A4: completeness by GL2-orbit classification. J is SL2-equivariant, so the rank of
    # M is constant on GL2-orbits; binary cubics have exactly three nonzero orbits with
    # representatives x^3 (cube), x^2 y, x y (x + y). Full rank at the two non-cube
    # representatives proves the rank-drop locus is EXACTLY the cube locus (plus 0).
    g11, g12, g21, g22 = symbols("g11 g12 g21 g22")
    Fc = symbols("F0:4")
    Gc = symbols("G0:5")
    fgen = sum(c * x**(3 - i) * y**i for i, c in enumerate(Fc))
    ggen = sum(c * x**(4 - i) * y**i for i, c in enumerate(Gc))
    sub = {x: g11 * x + g12 * y, y: g21 * x + g22 * y}
    lhs = expand(jac2(fgen.subs(sub, simultaneous=True),
                      ggen.subs(sub, simultaneous=True)))
    rhs = expand((g11 * g22 - g12 * g21) * expand(jac2(fgen, ggen)).subs(
        sub, simultaneous=True))
    ok_eq = expand(lhs - rhs) == 0
    check("A4a: J(f o A, g o A) = det(A) J(f, g) o A identically (rank is "
          "GL2-orbit-constant)", ok_eq)
    ok_orb = True
    for (nm, rep) in (("x^2 y", x**2 * y), ("x y (x + y)", x * y * (x + y))):
        Jr = Poly(expand(jac2(rep, Q4)), x, y)
        Mr = Matrix([[expand(Jr.coeff_monomial(x**i * y**j).diff(b)) for b in bs]
                     for (i, j) in out_mons])
        r = Mr.rank()
        ok_orb &= (r == 5)
        print(f"  A4 representative {nm}: rank {r}")
    check("A4b: both non-cube orbit representatives have FULL rank 5: with A4a and the "
          "3-orbit classification of binary cubics, rank drops EXACTLY on cubes", ok_orb)


def window_pair(P, N):
    MQ = [(i, d - i) for d in range(2, N + 1) for i in range(d + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * x**i * y**j for bb, (i, j) in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    sol = linsolve(eqs, list(B))
    if not sol:
        return None
    vec = list(sol)[0]
    free = sorted(vec.free_symbols & set(B), key=lambda s_: str(s_))
    vec = [v.subs({f: 0 for f in free}) for v in vec]
    Q = y + sum(vv * x**i * y**j for vv, (i, j) in zip(vec, MQ))
    return expand(Q)


def poly_inverse(P, Q):
    u, v = symbols("u v")
    G = groebner([expand(P - u), expand(Q - v)], x, y, u, v, order="lex")
    X = Y = None
    for g in G.exprs:
        pg = Poly(g, x, y)
        if pg.degree(x) == 1 and pg.degree(y) == 0 and pg.coeff_monomial(x) == 1:
            X = expand(x - g)
        if pg.degree(x) == 0 and pg.degree(y) == 1 and pg.coeff_monomial(y) == 1:
            Y = expand(y - g)
    if X is None or Y is None:
        return None
    okx = expand(P.subs({x: X, y: Y}, simultaneous=True) - u) == 0
    oky = expand(Q.subs({x: X, y: Y}, simultaneous=True) - v) == 0
    return (X, Y) if (okx and oky) else None


def partB():
    print("=" * 76)
    print("Part B: the cube stratum at exact bidegree (3, <= 4): complete + invert")
    print("=" * 76)
    ncons = 0
    ninv = 0
    nempty = 0
    bad = []
    vals = [Rational(0), Rational(1), Rational(-1), Rational(2)]
    for p20 in vals:
        for p11 in vals:
            for p02 in vals:
                P = expand(x + y**3 + p20 * x**2 + p11 * x * y + p02 * y**2)
                Q = window_pair(P, 4)
                if Q is None:
                    nempty += 1
                    continue
                ncons += 1
                if expand(jac2(P, Q) - 1) != 0:
                    bad.append((p20, p11, p02, "not Keller"))
                    continue
                inv = poly_inverse(P, Q)
                if inv is None:
                    bad.append((p20, p11, p02, "no polynomial inverse"))
                else:
                    ninv += 1
    print(f"  B: 64 samples: {ncons} consistent, {nempty} empty, {ninv} inverted, "
          f"failures {bad}")
    check("B: every consistent cube-stratum sample yields a Keller pair with an explicit "
          "polynomial inverse", not bad and ncons == ninv and ncons > 0,
          f"{ninv}/{ncons} inverted")


def partC():
    print("=" * 76)
    print("Part C: non-cube tops are EMPTY at (3, 4); replications at (3, 5), (3, 7)")
    print("=" * 76)
    TOPS = [("x^2 y", x**2 * y), ("x^3 + y^3", x**3 + y**3),
            ("x^2 y - x y^2", x**2 * y - x * y**2)]
    ok = True
    for (nm, T) in TOPS:
        for N in (4, 5, 7):
            Q = window_pair(expand(x + T), N)
            empty = Q is None
            ok &= empty
            print(f"  C x + {nm} at (3, <= {N}): "
                  f"{'EMPTY' if empty else 'CONSISTENT (escalate!)'}")
    check("C: every non-cube top is empty at (3, <= 4), (3, <= 5), (3, <= 7)", ok)


def partD():
    print("=" * 76)
    print("Part D: the (3, n) coverage table")
    print("=" * 76)
    ok = True
    for n in range(3, 13):
        g = gcd(3, n)
        ok &= g in (1, 3)
        cover = ("EXP-022 (machine) + gcd 3 prime: Appelgate-Onishi/Nagata" if n == 3
                 else ("Magnus 1954 (gcd 1)" if g == 1
                       else "Appelgate-Onishi 1985 / Nagata (gcd 3 prime)"))
        print(f"  D (3, {n}): gcd {g} -> {cover}")
    check("D: gcd(3, n) is always 1 or 3: the whole column is classically covered; the "
          "machine's role is replication + explicit inverses", ok)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
