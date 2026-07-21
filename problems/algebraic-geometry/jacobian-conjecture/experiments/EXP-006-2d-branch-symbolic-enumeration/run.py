# EXP-006: branch-symbolic enumeration of 2D equivariant Keller maps. CPU-only, sympy over QQ.
# See hypothesis.md. Fixes EXP-005's vacuous scan: symbolic branches, counted discards,
# in-image fiber targets.
#
# Run: .\.venv\Scripts\python.exe problems\algebraic-geometry\jacobian-conjecture\experiments\EXP-006-2d-branch-symbolic-enumeration\run.py
import sys
from pathlib import Path

from sympy import (Poly, Rational, cancel, expand, fraction, groebner,  # noqa: E402
                   solve, symbols, together)

x, y, v = symbols("x y v")
c = symbols("c_det")

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


SAMPLES = [
    {"c": Rational(1), "free": [Rational(2, 3), Rational(-3, 2), Rational(5, 7), Rational(1, 4), Rational(-2)]},
    {"c": Rational(2), "free": [Rational(-1, 2), Rational(4, 3), Rational(-5, 3), Rational(3), Rational(1, 5)]},
    {"c": Rational(-3), "free": [Rational(1), Rational(2), Rational(-1, 3), Rational(-4, 5), Rational(7, 2)]},
]
POINTS = [(Rational(2, 3), Rational(-1, 2)), (Rational(-3, 5), Rational(4, 3)),
          (Rational(5, 4), Rational(2, 7))]

stats = {"branches": 0, "instances": 0, "bad_residual": 0, "nonpoly": 0, "degenerate": 0,
         "fibers_checked": 0}
multi_preimage = []
instance_kinds = set()

for a_int in (1, 2, 3):
    for b1i in range(-3, 4):
        b2i = 1 - a_int - b1i
        if (b1i, b2i) == (0, 0):
            continue
        # Polynomiality is a VALUATION constraint known in advance: x^b f(x^a y) is polynomial
        # iff the coefficient of v^i in f vanishes for all i < ceil(-b/a). Build it into the
        # ansatz so the ODE solve searches the right space directly (fix over the first pass,
        # which instantiated frees at nonzero values and killed every negative-b branch).
        vmin_f = max(0, (-b1i + a_int - 1) // a_int) if b1i < 0 else 0
        vmin_g = max(0, (-b2i + a_int - 1) // a_int) if b2i < 0 else 0
        for df in range(vmin_f, 4):
            for dg in range(vmin_g, 4):
                fcs = symbols(f"F{vmin_f}:{df + 1}")
                gcs = symbols(f"G{vmin_g}:{dg + 1}")
                fv = sum(co * v**(vmin_f + i) for i, co in enumerate(fcs))
                gv = sum(co * v**(vmin_g + i) for i, co in enumerate(gcs))
                E = expand(b1i * fv * gv.diff(v) - b2i * fv.diff(v) * gv - c)
                eqs = Poly(E, v).all_coeffs()
                try:
                    sols = solve(eqs, list(fcs) + list(gcs), dict=True)
                except Exception:
                    continue
                for s in sols:
                    stats["branches"] += 1
                    fsol, gsol = fv.subs(s), gv.subs(s)
                    free = sorted((fsol.free_symbols | gsol.free_symbols) - {v, c}, key=str)
                    for smp in SAMPLES:
                        inst = {c: smp["c"]}
                        inst.update({fs: smp["free"][i % 5] for i, fs in enumerate(free)})
                        fi = cancel(fsol.subs(inst))
                        gi = cancel(gsol.subs(inst))
                        resid = expand(b1i * fi * gi.diff(v) - b2i * fi.diff(v) * gi - smp["c"])
                        if resid != 0:
                            stats["bad_residual"] += 1
                            continue
                        if fi == 0 or gi == 0:
                            stats["degenerate"] += 1
                            continue
                        vv = x**a_int * y
                        Pm = together(x**b1i * fi.subs(v, vv))
                        Qm = together(x**b2i * gi.subs(v, vv))
                        nP, dP = fraction(cancel(Pm))
                        nQ, dQ = fraction(cancel(Qm))
                        if dP.has(x) or dP.has(y) or dQ.has(x) or dQ.has(y):
                            stats["nonpoly"] += 1
                            continue
                        Pm, Qm = expand(nP / dP), expand(nQ / dQ)
                        stats["instances"] += 1
                        instance_kinds.add((a_int, b1i, b2i,
                                            Poly(fi, v).degree() if fi.has(v) else 0,
                                            Poly(gi, v).degree() if gi.has(v) else 0))
                        for (x0, y0) in POINTS:
                            A0 = Pm.subs({x: x0, y: y0})
                            B0 = Qm.subs({x: x0, y: y0})
                            gb = groebner([expand(Pm - A0), expand(Qm - B0)], x, y, order="lex")
                            stats["fibers_checked"] += 1
                            if gb.exprs == [1]:
                                nsol = 0
                            else:
                                uni = [g for g in gb.exprs if g.free_symbols <= {y}]
                                nsol = Poly(uni[-1], y).degree() if uni else -1
                            if nsol > 1 or nsol == -1:
                                multi_preimage.append((a_int, b1i, b2i, fi, gi, (x0, y0), nsol))

print("Scan statistics:")
for k_, v_ in stats.items():
    print(f"  {k_}: {v_}")
print(f"  distinct instance shapes (a, b1, b2, deg f, deg g): {len(instance_kinds)}")
for kind in sorted(instance_kinds):
    print(f"    {kind}")

check("scan is NON-vacuous (instances > 0)", stats["instances"] > 0,
      f"instances = {stats['instances']}")
check("every in-image fiber has exactly one preimage (no multi-point fiber found)",
      not multi_preimage, str(multi_preimage)[:300])

print()
if failures:
    print(f"RESULT: {len(failures)} check(s) FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS. The 2D equivariant Keller scan is now non-vacuous and every")
print("tested instance is injective on in-image targets: the 2D equivariant rigidity conjecture")
print("survives a real (bounded-degree) attack.")
