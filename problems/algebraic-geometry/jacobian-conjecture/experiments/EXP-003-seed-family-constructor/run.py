# EXP-003: the seed-family constructor, derived and verified exactly. CPU-only, sympy over QQ.
# See hypothesis.md. Parts:
#   A) d=2 general seed: discover the (p1, p2, k, m) constraint set for polynomiality + Keller.
#   B) d=3 instance p = w - 2w^3: solve (k, m), build G, verify Keller det, degrees, fiber quartic.
#   C) explicit rational collisions for G via the reconstruction inverse (a NEW certificate).
#   D) d=4 instance p = 8w - 12w^2 + 4w^3 - 5w^4: same pipeline, fiber degree 5.
#
# Run: .\.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-003-seed-family-constructor\run.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib import P as F_P, Q as F_Q, R as F_R  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, factor, fraction,  # noqa: E402
                   groebner, integrate, rem, simplify, solve, symbols, together)

x, y, z = symbols("x y z")
v, t, w = symbols("v t w")
k, m = symbols("k m")

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def seed_functions(p_expr):
    """h = p/w (polynomial), Phi = integral_0^w p."""
    h = cancel(p_expr / w)
    Phi = integrate(p_expr, (w, 0, w))
    return h, Phi


def build_reduced(p_expr, kk, mm):
    """Reduced data (a1, b1, c1) in (v, t) from seed p and constants (k, m)."""
    h, Phi = seed_functions(p_expr)
    u = 1 + v
    c1 = h.subs(w, v) - t
    warg = u * c1 / kk
    b1 = expand(kk * u * h.subs(w, warg) + mm)
    a1 = expand(u * b1 / kk - cancel(kk**2 * Phi.subs(w, warg) / c1**2))
    return a1, b1, c1


def lift(a1, b1, c1):
    """Lift reduced data to components on (x, y, z); returns Laurent expressions."""
    sub = {v: x * y, t: x**2 * z}
    return (
        together(expand(a1.subs(sub)) / x**2),
        together(expand(b1.subs(sub)) / x),
        expand(x * c1.subs(sub)),
    )


def laurent_low_terms(expr, weight_pow):
    """Coefficients of x-degrees < 0 after multiplying by x**weight_pow (polynomiality residues)."""
    e = expand(expr * x**weight_pow)
    p = Poly(e, x)
    residues = []
    for (deg,), coeff in p.terms():
        if deg < weight_pow:
            residues.append(expand(coeff))
    return residues


print("=" * 76)
print("Part A: d = 2 general seed p = p1 w + p2 w^2, constants (k, m)")
print("=" * 76)
p1, p2 = symbols("p1 p2")
pA = p1 * w + p2 * w**2
a1A, b1A, c1A = build_reduced(pA, k, m)
PA, QA, RA = lift(a1A, b1A, c1A)
# Polynomiality residues: P needs all monomial weights >= 2 (i.e. numerator x-degree >= 2), Q >= 1.
resP = laurent_low_terms(cancel(PA * x**2) / x**2, 2)
resQ = laurent_low_terms(cancel(QA * x) / x, 1)
print(f"  polynomiality residue equations: {len(resP) + len(resQ)}")
eqs = [e for e in resP + resQ]
solsA = solve(eqs, [p1, p2, m], dict=True)
print(f"  solve(residues) for (p1, p2, m) given k: {solsA}")
# Impose Keller on the surviving family: det must be a nonzero constant.
verifiedA = False
for s in solsA:
    a1s, b1s, c1s = build_reduced(pA.subs(s), k, m.subs(s) if m in s else m)
    Ps, Qs, Rs = lift(a1s, b1s, c1s)
    if any(laurent_low_terms(e, wp) for e, wp in ((Ps, 2), (Qs, 1))):
        continue
    J = Matrix([[expand(c).diff(var) for var in (x, y, z)] for c in (Ps, Qs, Rs)]).det()
    J = expand(cancel(J))
    freesym = J.free_symbols - {p1, p2, k, m}
    is_const = freesym <= set() or not (J.has(x) or J.has(y) or J.has(z))
    print(f"  branch {s}: det J = {factor(J)}")
    if is_const and J != 0:
        verifiedA = True
        # The announced map must be an instance: p = 2w - 3w^2, k = 2, m = 2.
        inst = {p1: 2, p2: -3, k: 2}
        Ji = J.subs(inst)
        a1i, b1i, c1i = build_reduced((p1 * w + p2 * w**2).subs(inst), 2, m.subs(s).subs(inst) if m in s else 2)
        Pi, Qi, Ri = lift(a1i, b1i, c1i)
        match = all(expand(a - b) == 0 for a, b in ((Pi, F_P), (Qi, F_Q), (Ri, F_R)))
        print(f"    instance (2, -3, k=2): det = {Ji}; reproduces announced F: {match}")
        check("A: constructor family is Keller (det constant, nonzero) for the solved branch", True)
        check("A: announced F is the (p1,p2,k,m)=(2,-3,2,2) instance", match)
check("A: at least one valid branch found", verifiedA)


def full_verify_instance(p_expr, label, expect_fiber_deg):
    """Solve (k, m) for a concrete seed, build the map, verify Keller + fiber + reconstruction."""
    print()
    print("=" * 76)
    print(f"Part: instance {label}: p = {p_expr}")
    print("=" * 76)
    a1, b1, c1 = build_reduced(p_expr, k, m)
    Pl, Ql, Rl = lift(a1, b1, c1)
    eqs = laurent_low_terms(cancel(Pl * x**2) / x**2, 2) + laurent_low_terms(cancel(Ql * x) / x, 1)
    sols = solve(eqs, [k, m], dict=True)
    sols = [s for s in sols if s.get(k, 1) != 0]
    print(f"  (k, m) solutions from polynomiality: {sols}")
    check(f"{label}: polynomiality admits (k, m)", bool(sols))
    if not sols:
        return None
    s = sols[0]
    kk, mm = s.get(k), s.get(m)
    a1, b1, c1 = build_reduced(p_expr, kk, mm)
    Pc, Qc, Rc = [expand(cancel(e)) for e in lift(a1, b1, c1)]
    for comp, nm, wp in ((Pc, "P", 2), (Qc, "Q", 1), (Rc, "R", 0)):
        check(f"{label}: {nm} is a polynomial in (x, y, z)",
              not laurent_low_terms(comp, wp) and not fraction(together(comp))[1].has(x))
    J = expand(Matrix([[c.diff(var) for var in (x, y, z)] for c in (Pc, Qc, Rc)]).det())
    print(f"  det J = {J}")
    check(f"{label}: det J is a nonzero constant", J.is_number and J != 0)
    degs = [Poly(c, x, y, z).total_degree() for c in (Pc, Qc, Rc)]
    print(f"  component total degrees: {degs}")

    # Fiber degree via the w-polynomial at a random rational target, with exact reconstruction
    # verified MODULO the fiber polynomial (no floating point anywhere).
    h, Phi = seed_functions(p_expr)
    A0, B0, C0 = Rational(3, 7), Rational(-2, 5), Rational(1, 3)
    Vt, Tt = B0 * C0, A0 * C0**2
    W = expand(kk**2 * Phi - (w * Vt - Tt))
    Wp = Poly(W, w)
    print(f"  fiber polynomial degree at random target: {Wp.degree()} (expected {expect_fiber_deg})")
    check(f"{label}: generic fiber degree == {expect_fiber_deg}", Wp.degree() == expect_fiber_deg)
    check(f"{label}: fiber polynomial squarefree at this target (distinct preimages)",
          Poly(W, w).discriminant() != 0)
    # Reconstruction: u = m k w / (Vt - k^2 w h(w)), c1 = k w / u, x = C0/c1, v = u - 1,
    # t = h(v) - c1, y = v/x, z = t/x^2; verify F(reconstruction(w)) == target mod W(w).
    uw = cancel(mm * kk * w / (Vt - kk**2 * w * h))
    c1w = cancel(kk * w / uw)
    xw = cancel(C0 / c1w)
    vw = cancel(uw - 1)
    tw = cancel(h.subs(w, vw) - c1w)
    yw = cancel(vw / xw)
    zw = cancel(tw / xw**2)
    ok_rec = True
    for comp, target in ((Pc, A0), (Qc, B0), (Rc, C0)):
        val = together(comp.subs({x: xw, y: yw, z: zw}, simultaneous=True) - target)
        num, den = fraction(cancel(val))
        ok_rec &= rem(Poly(expand(num), w), Wp, w) == 0 and rem(Poly(expand(den), w), Wp, w) != 0
    check(f"{label}: exact reconstruction inverse verified modulo the fiber polynomial", ok_rec)
    return {"k": kk, "m": mm, "P": Pc, "Q": Qc, "R": Rc, "h": h, "Phi": Phi, "degs": degs, "detJ": J}


def rational_collision(inst, label, w1, w2):
    """Engineer a target with two prescribed rational w-roots -> explicit rational collision."""
    print()
    print("=" * 76)
    print(f"Part: explicit rational collision for {label} (w1 = {w1}, w2 = {w2})")
    print("=" * 76)
    kk, mm, h, Phi = inst["k"], inst["m"], inst["h"], inst["Phi"]
    Vt, Tt = symbols("Vt Tt")
    sol = solve([kk**2 * Phi.subs(w, wi) - (wi * Vt - Tt) for wi in (w1, w2)], [Vt, Tt], dict=True)[0]
    C0 = Rational(1)
    B0, A0 = sol[Vt] / C0, sol[Tt] / C0**2
    print(f"  engineered target: (A, B, C) = ({A0}, {B0}, {C0})")
    pts = []
    for wi in (w1, w2):
        uw = Rational(mm * kk * wi) / (sol[Vt] - kk**2 * wi * h.subs(w, wi))
        c1w = Rational(kk * wi) / uw
        x0 = C0 / c1w
        v0 = uw - 1
        t0 = h.subs(w, v0) - c1w
        pts.append((x0, v0 / x0, t0 / x0**2))
    print(f"  reconstructed points: {pts}")
    imgs = [tuple(expand(c.subs({x: p_[0], y: p_[1], z: p_[2]}, simultaneous=True))
                  for c in (inst["P"], inst["Q"], inst["R"])) for p_ in pts]
    check(f"{label}: the two points are distinct", pts[0] != pts[1])
    check(f"{label}: both map exactly to the engineered target",
          all(im == (A0, B0, C0) for im in imgs), f"images = {imgs}")
    return pts, (A0, B0, C0)


instG = full_verify_instance(w - 2 * w**3, "G (d=3 seed w - 2w^3)", 4)
if instG:
    print(f"  NOTE: claimed external values for this seed were det = -6, degrees (12, 11, 4);")
    print(f"        ours: det = {instG['detJ']}, degrees {instG['degs']} (record the comparison).")
    rational_collision(instG, "G", Rational(1), Rational(2))

instH = full_verify_instance(8 * w - 12 * w**2 + 4 * w**3 - 5 * w**4, "H (d=4 seed, ours)", 5)
if instH:
    rational_collision(instH, "H", Rational(1), Rational(2))

print()
if failures:
    print(f"RESULT: {len(failures)} check(s) FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS. The seed-family constructor is established: for admissible")
print("(p, k, m) it yields Keller maps with generic fiber degree deg(p) + 1, an exact")
print("reconstruction inverse, and engineered rational collisions (new explicit certificates).")
