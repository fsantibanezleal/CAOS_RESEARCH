"""Replay of the six-gate program for the tau = 6 rational record, in exact integer arithmetic.

The rational census (scripts/rational_census.py, context/2026-08-25-rational-ladder.md) reports the
tau = 6 rational record 8x^6 - 10x^4 + 2x^2 but does not store the straight-line program that
computes it. This script executes the program

    g1 = x*x ; g2 = g1 + g1 ; g3 = g2 - 1 ; g4 = g3*g3 ; g5 = g4 - g1 ; g6 = g2*g5

gate by gate with tclib's exact polynomial arithmetic (coefficient tuples of Python ints, constant
term first), prints each gate value, the final polynomial, its distinct integer roots (tclib) and
its distinct rational roots (rational root theorem over Z with Fraction, no floating point), and
compares the polynomial with the record as the records give it: the literal in
scripts/audit_paper_claims.py and the formula in the context note.

What it shows: the six-gate program computes the record, so tau(record) <= 6. It does not show
tau(record) >= 6; that is the census's classification (exhaustive enumeration, last-gate lemma at
depth 6, see rational_census.py).

Exit status: 0 when every comparison holds, 1 otherwise.
"""
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from tclib.enum import padd, psub, pmul, integer_roots, divisors  # noqa: E402

X = (0, 1)
ONE = (1,)

# (name, op, left, right); an operand is "x", "1" or the name of an earlier gate.
PROGRAM = [
    ("g1", "*", "x", "x"),
    ("g2", "+", "g1", "g1"),
    ("g3", "-", "g2", "1"),
    ("g4", "*", "g3", "g3"),
    ("g5", "-", "g4", "g1"),
    ("g6", "*", "g2", "g5"),
]
OPS = {"+": padd, "-": psub, "*": pmul}


def fmt(f):
    if not f:
        return "0"
    terms = []
    for k in range(len(f) - 1, -1, -1):
        c = f[k]
        if c == 0:
            continue
        mon = "" if k == 0 else ("x" if k == 1 else f"x^{k}")
        terms.append(f"{c}{mon}" if k == 0 else (f"{c}*{mon}" if abs(c) != 1 else (mon if c == 1 else f"-{mon}")))
    return " + ".join(terms).replace("+ -", "- ")


def rational_roots(f):
    """Distinct rational roots of nonzero integer polynomial f, exact (rational root theorem)."""
    m = 0
    while f[m] == 0:
        m += 1
    roots = {Fraction(0)} if m > 0 else set()
    g = f[m:]
    if len(g) > 1:
        for p in divisors(g[0]):
            for q in divisors(g[-1]):
                for s in (1, -1):
                    r = Fraction(s * p, q)
                    acc = Fraction(0)
                    for c in reversed(g):
                        acc = acc * r + c
                    if acc == 0:
                        roots.add(r)
    return roots


def run():
    vals = {"x": X, "1": ONE}
    for name, op, a, b in PROGRAM:
        vals[name] = OPS[op](vals[a], vals[b])
        print(f"{name} = {a} {op} {b:<3} -> {fmt(vals[name])}   coefficients {vals[name]}")
    return vals[PROGRAM[-1][0]]


def record_from_audit():
    src = open(os.path.join(HERE, "audit_paper_claims.py"), encoding="utf-8").read()
    m = re.search(r"^_rp = \(([-0-9, ]+)\)", src, re.M)
    return tuple(int(t) for t in m.group(1).split(",")) if m else None


def note_has_formula():
    path = os.path.join(HERE, "..", "context", "2026-08-25-rational-ladder.md")
    return "8x^6 - 10x^4 + 2x^2 = 2x^2 (x-1)(x+1)(2x-1)(2x+1)" in open(path, encoding="utf-8").read()


def main():
    print(f"gates: {len(PROGRAM)}")
    f = run()
    print(f"polynomial (constant term first): {f}")
    print(f"polynomial: {fmt(f)}")
    zi = sorted(integer_roots(f))
    zq = sorted(rational_roots(f))
    print(f"integer roots ({len(zi)}): {zi}")
    print(f"rational roots ({len(zq)}): {[str(r) for r in zq]}")
    record = record_from_audit()
    print(f"record literal in scripts/audit_paper_claims.py: {record}")
    # (2x)(x-1)(x+1)(2x-1)(2x+1) * x, expanded, as an independent algebraic check
    fac = pmul(pmul(pmul((0, 2), (0, 1)), pmul((-1, 1), (1, 1))), pmul((-1, 2), (1, 2)))
    checks = [
        ("program has 6 gates", len(PROGRAM) == 6),
        ("program polynomial equals the record literal", f == record),
        ("program polynomial equals 2x^2(x-1)(x+1)(2x-1)(2x+1) expanded", f == fac),
        ("context note carries the record formula", note_has_formula()),
        ("integer roots are [-1, 0, 1]", zi == [-1, 0, 1]),
        ("rational roots are 0, +-1/2, +-1", zq == [Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1)]),
    ]
    ok = True
    for label, res in checks:
        print(f"{'ok  ' if res else 'FAIL'} {label}")
        ok &= bool(res)
    print("replay: ok" if ok else "replay: FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
