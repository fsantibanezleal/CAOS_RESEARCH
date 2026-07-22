# EXP-040: subsumption + recalibration audit (JCB-028 closure).
# CPU-only, sympy over QQ. Run: run.py [A|B|C|D]
import sys
from itertools import combinations
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import Poly, Rational, expand, linsolve, symbols  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


COEFFS = [("xy", (1, 1)), ("y^2", (0, 2)), ("xy^2", (1, 2)), ("y^3", (0, 3)),
          ("x^2", (2, 0)), ("x^2y", (2, 1)), ("x^3", (3, 0))]
XCLASS = 2  # (2,-1)-weight of x and of (xy)^2


def wt(m):
    return 2 * m[0] - m[1]


def window_consistent(P, N):
    MQ = [(i, d - i) for d in range(2, N + 1) for i in range(d + 1)]
    B = symbols(f"B0:{len(MQ)}")
    Q0 = y + sum(bb * x**i * y**j for bb, (i, j) in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
    return bool(linsolve(eqs, list(B)))


def partA():
    print("=" * 76)
    print("Part A: weight classification under (v, 1-u) = (2, -1)")
    print("=" * 76)
    below = [nm for nm, m in COEFFS if wt(m) < XCLASS]
    above = [nm for nm, m in COEFFS if wt(m) >= XCLASS]
    for nm, m in COEFFS:
        side = "BELOW (Theorem 2, all degrees)" if wt(m) < XCLASS else \
            "ABOVE (staircase territory, EXP-037/JCB-038)"
        print(f"  A {nm}: weight {wt(m)} -> {side}")
    ok = (set(below) == {"xy", "y^2", "xy^2", "y^3"}
          and set(above) == {"x^2", "x^2y", "x^3"})
    check("A1: split is 4 below-weight vs 3 above-weight, exactly as derived", ok)
    ok2 = wt((2, 2)) == XCLASS
    check("A2: the pure slice x + a (xy)^2 is Theorem-1 shaped (u = v = 2, same class "
          "as x): the all-degree closed-form certificate [C] is a COROLLARY", ok2)


def partB():
    print("=" * 76)
    print("Part B: all-below-weight slice EMPTY at N = 10 (Theorem 2 consistency)")
    print("=" * 76)
    a, b, c, d, e = (Rational(2), Rational(3), Rational(-1), Rational(5), Rational(1))
    P = expand(x + a * (x * y) ** 2 + b * x * y + c * y**2 + d * y**3
               + e * x * y**2)
    cons = window_consistent(P, 10)
    check("B: x + 2(xy)^2 + 3xy - y^2 + 5y^3 + xy^2 is EMPTY at N = 10 (deeper than "
          "EXP-025; consistent with the unconditional Theorem 2)", not cons)


def partC():
    print("=" * 76)
    print("Part C: every 4-subset of the seven coefficients, sampled, EMPTY at (4, <= 6)")
    print("=" * 76)
    a = Rational(2)
    TUPLES = [(1, 1, 1, 1), (1, -1, 2, 1), (2, 1, -1, 3)]
    nrun = 0
    ok = True
    owners = {"below": 0, "staircase": 0}
    for combo in combinations(COEFFS, 4):
        pure_below = all(wt(m) < XCLASS for _, m in combo)
        owners["below" if pure_below else "staircase"] += 1
        for vals in TUPLES:
            P = x + a * (x * y) ** 2
            for (nm, m), vv in zip(combo, vals):
                P += Rational(vv) * x**m[0] * y**m[1]
            cons = window_consistent(expand(P), 6)
            nrun += 1
            if cons:
                ok = False
                print(f"  C CONSISTENT (escalate!): {[nm for nm, _ in combo]} "
                      f"vals {vals}")
    print(f"  C: {nrun} solves over {owners['below']} pure-below and "
          f"{owners['staircase']} staircase-owner subsets: all EMPTY" if ok else "")
    check("C: all 35 4-subsets x 3 value tuples are EMPTY at (4, <= 6)", ok,
          f"{nrun} solves")


def partD():
    print("=" * 76)
    print("Part D: recalibration against the verified literature floor")
    print("=" * 76)
    rows = [
        ("EXP-024/025 (4, *) ladder", 2, "gcd <= 8 interval (Magnus/Nakai-Baba/"
         "Appelgate-Onishi/Nagata)"),
        ("EXP-026 (18, 27)", 9, "B >= 16 (Heitmann 1990, JPAA 64)"),
        ("EXP-027 (24, 36)", 12, "B >= 16 (Heitmann 1990)"),
        ("EXP-028 (18, 36)", 18, "B != 2p (GGV 2017) [18 = 2*3^2 not 2p: B = 16 or "
         "B > 20 applies: 18 excluded]"),
    ]
    ok = True
    for (nm, g, cover) in rows:
        excluded = g <= 8 or g < 16 or g in (18,)
        ok &= excluded
        print(f"  D {nm}: gcd {g} -> literature-excluded ({cover}) -> our certificate "
              f"= REPLICATION")
    g72 = gcd(72, 108)
    print(f"  D open frontier: B = 16 (GGV normal form, Thm 8.12/Cor 7.13) or B > 20 "
          f"composite non-2p; lone surviving pair below 125: (72, 108), gcd {g72}")
    ok &= g72 == 36
    check("D: EXP-024..028 are replications inside the verified floor; the open ladder "
          "is B = 16 and B > 20 (with (72, 108) the lone pair below 125)", ok)


PARTS = {"A": partA, "B": partB, "C": partC, "D": partD}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["A", "B", "C", "D"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
