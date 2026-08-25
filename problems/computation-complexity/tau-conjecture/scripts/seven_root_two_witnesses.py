"""Two structurally different 10-gate programs with 7 distinct integer roots.

Witness A (round 8, EXP-007, stated in prose there): the exhaustive 8-gate
six-rooter q(q-2)(q-6) with q = x^2 - x, times (x - 4). Folding-based; the
root set is the INTERVAL {-2,...,4}.

Witness B (this round): x^2 (x^2-1)(x^2-4)(x^2-16). Squaring-based; the root
set is a TOWER {0,+-1,+-2,+-4}.

Both are executed here as data, gate by gate, and their root sets and
heights are recomputed from the expanded coefficients.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import padd, psub, pmul, integer_roots

X = ("x",)
C = lambda k: ("c", k)
R = lambda i: ("r", i)


def run(slp):
    regs = []

    def val(ref):
        if ref[0] == "x":
            return (0, 1)
        if ref[0] == "c":
            return () if ref[1] == 0 else (ref[1],)
        return regs[ref[1]]

    for op, a, b in slp:
        u, v = val(a), val(b)
        regs.append({"+": padd, "-": psub, "*": pmul}[op](u, v))
    return regs[-1], len(slp)


WITNESS_A = [
    ("*", X, X),          # 0: x^2
    ("-", R(0), X),       # 1: q = x^2 - x
    ("+", C(1), C(1)),    # 2: 2
    ("*", R(2), R(2)),    # 3: 4
    ("-", R(1), R(2)),    # 4: q - 2
    ("-", R(4), R(3)),    # 5: q - 6      (= (q-2) - 4, no constant 6 needed)
    ("*", R(4), R(5)),    # 6: (q-2)(q-6)
    ("*", R(6), R(1)),    # 7: q(q-2)(q-6)      <- the exhaustive 8-gate six-rooter
    ("-", X, R(3)),       # 8: x - 4
    ("*", R(7), R(8)),    # 9: times (x - 4)
]

WITNESS_B = [
    ("*", X, X),          # 0: y = x^2
    ("+", R(0), C(-1)),   # 1: y - 1
    ("+", C(1), C(1)),    # 2: 2
    ("*", R(2), R(2)),    # 3: 4
    ("-", R(0), R(3)),    # 4: y - 4
    ("*", R(3), R(3)),    # 5: 16
    ("-", R(0), R(5)),    # 6: y - 16
    ("*", R(0), R(1)),    # 7: y(y-1)
    ("*", R(4), R(6)),    # 8: (y-4)(y-16)
    ("*", R(7), R(8)),    # 9
]

out = {}
for name, slp, shape in [("A interval {-2..4}", WITNESS_A, "folding q = x^2 - x, plus a linear factor"),
                         ("B tower {0,+-1,+-2,+-4}", WITNESS_B, "repeated squaring 2 -> 4 -> 16")]:
    p, g = run(slp)
    r = sorted(integer_roots(p))
    h = max(abs(c) for c in p)
    print(f"{name:<26} gates={g:<3} z={len(r):<3} height={h:<5} roots={r}")
    print(f"{'':<26} shape: {shape}")
    out[name] = {"gates": g, "z": len(r), "height": h, "roots": r, "coefficients": list(p)}

# The 8-gate six-rooter inside witness A must itself be the census record.
six, _ = run(WITNESS_A[:8])
sr = sorted(integer_roots(six))
print()
print(f"inner 8-gate factor: z={len(sr)} roots={sr} height={max(abs(c) for c in six)}"
      f"  matches EXP-006 record set: {sr == [-2,-1,0,1,2,3]}")

os.makedirs("experiments/EXP-013-additive-residual/artifacts", exist_ok=True)
with open("experiments/EXP-013-additive-residual/artifacts/seven_root_witnesses.json", "w") as fh:
    json.dump(out, fh, indent=2)
