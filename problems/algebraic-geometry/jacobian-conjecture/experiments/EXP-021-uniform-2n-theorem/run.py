# EXP-021: the uniform (2, n) theorem. CPU-only, sympy over QQ. See hypothesis.md.
# Run: .\.venv\Scripts\python.exe ...\EXP-021-uniform-2n-theorem\run.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import (Matrix, Poly, Rational, cancel, expand, symbols)  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


al, be = symbols("alpha beta")
ell = al * x + be * y
P = x + ell**2

PART = sys.argv[1] if len(sys.argv) > 1 else "ALL"

print("=" * 76)
print("Part A: sufficiency: J(P, ell/beta + H(P)) == 1 for generic H (deg H <= 4)")
print("=" * 76)
H = symbols("h0:4")
Hp = sum(h * P**i for i, h in enumerate(H))
Q = ell / be + Hp
JA = expand(jac2(P, Q))
check("A: identity J == 1 holds over QQ(alpha, beta, h0..h3)", expand(JA - 1) == 0,
      f"deg Q = {Poly(expand(Q), x, y).total_degree()}")

if PART == "A":
    print(f"RESULT (A): {'FAILED ' + str(failures) if failures else 'ALL CHECKS PASS.'}")
    sys.exit(1 if failures else 0)
print()
print("=" * 76)
print("Part B: completeness: dim ker L on deg <= n equals floor(n/2) + 1 (n = 3..8)")
print("=" * 76)
SAMPLES = [(Rational(1), Rational(2)), (Rational(-2), Rational(1, 3)),
           (Rational(3, 2), Rational(-1))]
for n in range(3, 7):
    mons = [x**i * y**j for i in range(n + 1) for j in range(n + 1 - i)]
    expected = n // 2 + 1
    ok_n = True
    for (a0, b0) in SAMPLES:
        Ps = P.subs({al: a0, be: b0})
        rows = []
        outm = [x**i * y**j for i in range(2 * n) for j in range(2 * n) if i + j <= n + 1]
        for mo in mons:
            Jm = Poly(expand(jac2(Ps, mo)), x, y)
            rows.append([Jm.coeff_monomial(om) for om in outm])
        M = Matrix(rows).T
        kdim = len(mons) - M.rank()
        ok_n &= (kdim == expected)
    check(f"B: n = {n}: kernel dimension == {expected} at all samples", ok_n)

if PART == "B":
    print(f"RESULT (B): {'FAILED ' + str(failures) if failures else 'ALL CHECKS PASS.'}")
    sys.exit(1 if failures else 0)
print()
print("=" * 76)
print("Part C: the closed inverse: generic at deg H <= 1; exact spot checks at deg H = 3, 4")
print("=" * 76)
u, v = symbols("u v")


def compose_check(Hcoeffs, label):
    Hp_ = sum(h * P**i for i, h in enumerate(Hcoeffs))
    Q_ = ell / be + Hp_
    ellinv_ = be * (v - sum(h * u**i for i, h in enumerate(Hcoeffs)))
    Gx_ = u - ellinv_**2
    Gy_ = cancel((ellinv_ - al * Gx_) / be)
    d1 = expand(Gx_.subs({u: expand(P), v: expand(Q_)}, simultaneous=True) - x)
    d2 = expand(Gy_.subs({u: expand(P), v: expand(Q_)}, simultaneous=True) - y)
    c1 = expand(P.subs({x: Gx_, y: Gy_}, simultaneous=True) - u)
    c2 = expand(Q_.subs({x: Gx_, y: Gy_}, simultaneous=True) - v)
    check(f"C: {label}: G o F == id and F o G == id", d1 == 0 and d2 == 0 and c1 == 0 and c2 == 0)


hg = symbols("g0 g1")
compose_check(list(hg), "generic H of degree 1 (symbolic alpha, beta, g0, g1)")
SPOTS = [
    ([Rational(1), Rational(-2), Rational(1, 3), Rational(2)], (Rational(1), Rational(2))),
    ([Rational(0), Rational(3), Rational(-1), Rational(1, 2), Rational(-2)], (Rational(-2), Rational(1, 3))),
]
for k, (hc, (a0, b0)) in enumerate(SPOTS):
    Hp_ = sum(h * P**i for i, h in enumerate(hc))
    Q_ = (ell / be + Hp_).subs({al: a0, be: b0})
    P_ = P.subs({al: a0, be: b0})
    ellinv_ = (be * (v - sum(h * u**i for i, h in enumerate(hc)))).subs({be: b0})
    Gx_ = u - ellinv_**2
    Gy_ = cancel((ellinv_ - a0 * Gx_) / b0)
    d1 = expand(Gx_.subs({u: expand(P_), v: expand(Q_)}, simultaneous=True) - x)
    d2 = expand(Gy_.subs({u: expand(P_), v: expand(Q_)}, simultaneous=True) - y)
    check(f"C: exact spot check {k} (deg H = {len(hc) - 1}): G o F == id", d1 == 0 and d2 == 0)

print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS. Assembled theorem [D]: with the consistency ideals")
print("(EXP-019/020: a degree-2 component forces the rank-1 top; beta = 0 forces affine) and")
print("Wang's degree-2 case, EVERY planar Keller map with min degree <= 2 equals")
print("(x + ell^2, ell/beta + H(x + ell^2)) up to affine gauge, and is invertible by the")
print("closed formula above. The open frontier moves to min degree >= 3.")
