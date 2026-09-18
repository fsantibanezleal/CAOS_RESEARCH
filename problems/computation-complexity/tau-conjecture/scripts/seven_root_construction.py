"""TCB-032 upper bound: an explicit 10-gate program with 7 distinct integer roots.

The census scans give LOWER bounds (nine gates cannot reach seven roots).
Only a construction can give the upper bound. This script states the program
as data, runs it through the same exact arithmetic the census uses, and
checks the gate count, the value, and the root set independently.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import padd, psub, pmul, integer_roots

X = ("x",)
FREE = {-1: ("c", -1), 0: ("c", 0), 1: ("c", 1)}


def run(slp):
    """Execute a constant-free SLP. Returns (value, gate_count)."""
    regs = []

    def val(ref):
        kind = ref[0]
        if kind == "x":
            return (0, 1)
        if kind == "c":
            return () if ref[1] == 0 else (ref[1],)
        return regs[ref[1]]

    for op, a, b in slp:
        u, v = val(a), val(b)
        if op == "+":
            regs.append(padd(u, v))
        elif op == "-":
            regs.append(psub(u, v))
        elif op == "*":
            regs.append(pmul(u, v))
        else:
            raise ValueError(op)
    return regs[-1], len(slp)


def R(i):
    return ("r", i)


# p(x) = x^2 (x^2 - 1)(x^2 - 4)(x^2 - 16)
# Every constant is a repeated squaring of 2, which is why the tower is cheap:
# 4 and 16 cost one gate each once 2 exists, and both are perfect squares, so
# each contributes a genuine pair of integer roots.
SLP = [
    ("*", X, X),            # 0: y = x^2
    ("+", R(0), FREE[-1]),  # 1: y - 1
    ("+", FREE[1], FREE[1]),# 2: 2
    ("*", R(2), R(2)),      # 3: 4
    ("-", R(0), R(3)),      # 4: y - 4
    ("*", R(3), R(3)),      # 5: 16
    ("-", R(0), R(5)),      # 6: y - 16
    ("*", R(0), R(1)),      # 7: y(y - 1)
    ("*", R(4), R(6)),      # 8: (y - 4)(y - 16)
    ("*", R(7), R(8)),      # 9: p
]

poly, gates = run(SLP)
roots = sorted(integer_roots(poly))

# Independent expansion of the intended product, built from scratch.
y = pmul((0, 1), (0, 1))
want = pmul(pmul(y, psub(y, (1,))), pmul(psub(y, (4,)), psub(y, (16,))))

print("gates                :", gates)
print("polynomial           :", poly)
print("matches x^2(x^2-1)(x^2-4)(x^2-16):", poly == want)
print("degree               :", len(poly) - 1)
print("distinct integer roots:", roots, "->", len(roots))

# The census ladder this bound sits on, for the record.
print()
print("census (exhaustive, EXP-001..011): z_max(1..8) = 1,2,3,3,4,5,5,6")
print("this construction                : z(tau=10) >= 7")

result = {
    "slp": [[o, list(a), list(b)] for o, a, b in SLP],
    "gates": gates,
    "coefficients": list(poly),
    "roots": roots,
    "z": len(roots),
    "verified_against_independent_expansion": poly == want,
}
os.makedirs("experiments/EXP-013-additive-residual/artifacts", exist_ok=True)
with open("experiments/EXP-013-additive-residual/artifacts/seven_root_10gate.json", "w") as fh:
    json.dump(result, fh, indent=2)
