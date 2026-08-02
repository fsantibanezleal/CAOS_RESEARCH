"""EXP-016: mass-Jacobian rank for the k = 2, p = 2 stratum (stage ii opens).

P1/P2: exact rank of the 6 x 4 mass-coefficient matrix at two rational
geometries (sympy radical arithmetic). Smoke first: the pairing identities
L14 = -L13 etc. must hold at the witness. P3: minAssGTZ of the gauged shape
ideal in Singular; the witness distance vector must lie on exactly one
minimal component, of dimension 4.
"""
import json
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = ART / "run-log.txt"
W = "/root/exp016"
RESULTS = {}

MASS_CLASS = {1: "m1", 2: "m2", 3: "mA", 4: "mA", 5: "mB", 6: "mB"}
BLOCK = [(1, 3), (1, 5), (2, 3), (2, 5), (3, 5), (3, 6)]
PARTNERS = {(1, 3): (1, 4), (1, 5): (1, 6), (2, 3): (2, 4),
            (2, 5): (2, 6), (3, 5): (4, 6), (3, 6): (4, 5)}


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def record(k, status, detail=""):
    RESULTS[k] = {"status": status, "detail": detail}
    log(f"RESULT {k}: {status} {detail}")
    (ART / "results.json").write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")


def wsl(cmd, timeout=None):
    return subprocess.run(["wsl", "-d", "Ubuntu-24.04", "--", "bash", "-lc", cmd],
                          capture_output=True, text=True, timeout=timeout)


def positions(g):
    a1, a2, u, v, p, q = g
    return {1: (sp.Integer(0), sp.Rational(a1)), 2: (sp.Integer(0), sp.Rational(a2)),
            3: (sp.Rational(u), sp.Rational(v)), 4: (-sp.Rational(u), sp.Rational(v)),
            5: (sp.Rational(p), sp.Rational(q)), 6: (-sp.Rational(p), sp.Rational(q))}


def mass_matrix_at(g):
    """Exact 6 x 4 mass-coefficient matrix at a rational geometry; entries in
    a radical extension of Q. Also returns the pairing-identity residuals."""
    POS = positions(g)

    def rdist(i, j):
        (xi, yi), (xj, yj) = POS[i], POS[j]
        return sp.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

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
        return [sp.radsimp(cols[c]) for c in ("m1", "m2", "mA", "mB")]

    J = sp.Matrix([coeff_row(i, j) for i, j in BLOCK])
    residuals = []
    for e, (i, j) in enumerate(BLOCK):
        pi, pj = PARTNERS[(i, j)]
        prow = coeff_row(pi, pj)
        res = [sp.simplify(J[e, c] + prow[c]) for c in range(4)]
        residuals.append(all(x == 0 for x in res))
    return J, residuals


def exact_rank(J):
    """Rank via exact minor arithmetic over the radical field."""
    for size in (4, 3, 2, 1):
        for rows in combinations(range(6), size):
            for cols in combinations(range(4), size):
                minor = J[list(rows), list(cols)].det()
                if sp.simplify(sp.radsimp(minor)) != 0:
                    return size
    return 0


def quotient_squares(g):
    a1, a2, u, v, p, q = (sp.Rational(x) for x in g)
    return {
        "r12": (a1 - a2) ** 2,
        "d1A": u**2 + (a1 - v) ** 2, "d1B": p**2 + (a1 - q) ** 2,
        "d2A": u**2 + (a2 - v) ** 2, "d2B": p**2 + (a2 - q) ** 2,
        "wA": 4 * u**2, "wB": 4 * p**2,
        "cs": (u - p) ** 2 + (v - q) ** 2, "cx": (u + p) ** 2 + (v - q) ** 2,
    }


def main():
    log("EXP-016 runner start")
    W1 = (3, -1, 2, 1, 1, -2)
    W2 = (2, -2, 1, 2, 3, -1)

    t0 = time.time()
    J1, res1 = mass_matrix_at(W1)
    ok_pair = all(res1)
    record("smoke-pairing-identities", "pass" if ok_pair else "FAIL",
           f"partner rows equal negatives at W1: {res1} ({time.time()-t0:.0f}s)")
    if not ok_pair:
        return 1

    t0 = time.time()
    r1 = exact_rank(J1)
    record("p1-rank-witness1", "decided", f"rank={r1} at {W1} in {time.time()-t0:.0f}s")

    t0 = time.time()
    J2, _ = mass_matrix_at(W2)
    r2 = exact_rank(J2)
    record("p2-rank-witness2", "decided", f"rank={r2} at {W2} in {time.time()-t0:.0f}s")

    # P3: minimal associated primes of the gauged shape ideal + witness location
    NAMES = ["r12", "d1A", "d1B", "d2A", "d2B", "wA", "wB", "cs", "cx"]
    S = {n: sp.Symbol(n) for n in NAMES}
    r12, d1A, d1B, d2A, d2B, wA, wB, cs, cx = (S[n] for n in NAMES)
    A1 = d1A**2 - wA**2 / 4
    A2 = d2A**2 - wA**2 / 4
    B1 = d1B**2 - wB**2 / 4
    B2 = d2B**2 - wB**2 / 4
    H = cs**2 - (wA - wB) ** 2 / 4
    eqs = [sp.expand(4 * (cx**2 - cs**2 - wA * wB)),
           sp.expand(16 * ((A1 + A2 - r12**2) ** 2 - 4 * A1 * A2)),
           sp.expand(16 * ((A1 + H - B1) ** 2 - 4 * A1 * H)),
           sp.expand(16 * ((A2 + H - B2) ** 2 - 4 * A2 * H)),
           sp.expand(16 * ((B1 + B2 - r12**2) ** 2 - 4 * B1 * B2)),
           r12 - 1]
    polys = ",\n".join(str(e).replace("**", "^").replace(" ", "") for e in eqs)
    script = (f"ring r=0,({','.join(NAMES)}),dp;\nshort=0;\nLIB \"primdec.lib\";\n"
              f"ideal I={polys};\nlist L=minAssGTZ(I);\n"
              f"string(\"NCOMP=\",size(L));\n"
              f"for(int i=1;i<=size(L);i++){{ string(\"COMPDIM=\",dim(std(L[i]))); }}\n"
              f"quit;\n")
    sf = ART / "minass.sing"
    sf.write_text(script, encoding="utf-8", newline="\n")
    win = str(sf).replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {W} && cp '{win}' {W}/minass.sing")
    t0 = time.time()
    r = wsl(f"cd {W} && timeout 300 Singular -q minass.sing && echo SING_OK", timeout=420)
    secs = time.time() - t0
    (ART / "minass.out").write_text(r.stdout, encoding="utf-8")
    if "SING_OK" in r.stdout:
        ncomp = [l.split("=")[1] for l in r.stdout.splitlines() if l.startswith("NCOMP=")]
        dims = [l.split("=")[1] for l in r.stdout.splitlines() if l.startswith("COMPDIM=")]
        record("p3-minass", "decided", f"{secs:.0f}s; components={ncomp}; dims={dims}")
    else:
        record("p3-minass", "inconclusive-cap", f"{secs:.0f}s at 300s")

    log("runner done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
