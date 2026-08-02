"""EXP-018: the regular hexagon as stratum witness. Pure exact radical
arithmetic; no engines, no caps needed."""
import json
import sys
import time
from itertools import combinations
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
RESULTS = {}

MASS_CLASS = {1: "m1", 2: "m2", 3: "mA", 4: "mA", 5: "mB", 6: "mB"}
BLOCK = [(1, 3), (1, 5), (2, 3), (2, 5), (3, 5), (3, 6)]

s3 = sp.sqrt(3)
POS = {1: (sp.Integer(0), sp.Integer(1)), 2: (sp.Integer(0), sp.Integer(-1)),
       3: (s3 / 2, sp.Rational(1, 2)), 4: (-s3 / 2, sp.Rational(1, 2)),
       5: (s3 / 2, sp.Rational(-1, 2)), 6: (-s3 / 2, sp.Rational(-1, 2))}


def record(k, status, detail=""):
    RESULTS[k] = {"status": status, "detail": detail}
    print(f"RESULT {k}: {status} {detail}", flush=True)
    (ART / "results.json").write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")


def rdist(i, j):
    (xi, yi), (xj, yj) = POS[i], POS[j]
    return sp.sqrt(sp.expand((xi - xj) ** 2 + (yi - yj) ** 2))


def Delta(i, j, k):
    (xi, yi), (xj, yj), (xk, yk) = POS[i], POS[j], POS[k]
    return sp.Matrix([[1, 1, 1], [xi, xj, xk], [yi, yj, yk]]).det()


def coeff_row(i, j):
    cols = {"m1": sp.Integer(0), "m2": sp.Integer(0),
            "mA": sp.Integer(0), "mB": sp.Integer(0)}
    for k in range(1, 7):
        if k in (i, j):
            continue
        s = rdist(i, k) ** -3 - rdist(j, k) ** -3
        cols[MASS_CLASS[k]] += s * Delta(i, j, k)
    return [sp.radsimp(sp.expand(cols[c])) for c in ("m1", "m2", "mA", "mB")]


def main():
    t0 = time.time()
    J = sp.Matrix([coeff_row(i, j) for i, j in BLOCK])
    # P1: equal masses (1,1,1,1) must annihilate every block equation exactly
    ones = sp.Matrix([1, 1, 1, 1])
    Lvals = [sp.simplify(sp.radsimp(x)) for x in (J * ones)]
    p1 = all(v == 0 for v in Lvals)
    record("p1-hexagon-is-stratum-cc", "pass" if p1 else "FAIL",
           f"L-block at equal masses: {Lvals} ({time.time()-t0:.0f}s)")
    if not p1:
        return 1

    # P2: exact rank of J
    t0 = time.time()
    rank = 0
    witness_minor = None
    for size in (4, 3, 2, 1):
        found = False
        for rows in combinations(range(6), size):
            for cols in combinations(range(4), size):
                minor = sp.simplify(sp.radsimp(J[list(rows), list(cols)].det()))
                if minor != 0:
                    rank = size
                    witness_minor = (rows, cols, str(minor))
                    found = True
                    break
            if found:
                break
        if found:
            break
    record("p2-rank-at-hexagon", "decided",
           f"rank={rank}; nonzero minor rows{witness_minor[0]} cols{witness_minor[1]} = "
           f"{witness_minor[2][:80]} ({time.time()-t0:.0f}s)")
    (ART / "mass-matrix.txt").write_text(sp.srepr(J), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
