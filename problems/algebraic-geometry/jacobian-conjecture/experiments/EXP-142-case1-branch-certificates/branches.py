"""EXP-142: split Case 1 at q1 = +c and q1 = -c, exactly (hypothesis.md).

Reads EXP-141's equations E''_e over L = Q[y]/(P) (cert.py build output, `--src <work>/eqs.json`), checks exactly
that E2 = a2 (q1^2 - c^2)^2 in L[q1] with c in L below (found by PARI nffactor), and writes, for sigma = +1 and -1,
the branch system { E''_e(q0, sigma*c, q2, q3, q4, q5) } made primitive over Z, in cert.py format
(`<out>/branch_plus/eqs.json`, `<out>/branch_minus/eqs.json`; names q0, q2, q3, q4, q5; equations that vanish
identically on the branch are dropped and listed).

Usage: python branches.py --src <EXP-141 work>/eqs.json --out <work root>
"""
import argparse
import json
from math import gcd, lcm
from pathlib import Path

from flint import fmpq, fmpq_poly

P = fmpq_poly([26, 0, 3, 3, -1, 1])
C = fmpq_poly([fmpq(-639627376, 2128893), fmpq(-5999168, 163761), fmpq(1956896, 2128893),
               fmpq(-89962304, 2128893), fmpq(5290384, 2128893)])
NAMES = ["q0", "q2", "q3", "q4", "q5"]


def el(cs):
    return fmpq_poly([fmpq(c) for c in cs])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    E = json.loads(Path(a.src).read_text(encoding="utf-8"))["eqs"]
    # E2 = a2 s^2 + a1 s + a0 with s = q1^2, and nothing else
    d2 = {tuple(m): el(cs) for m, cs in E[1]}
    assert set(d2) <= {(0, 0, 0, 0, 0, 0), (0, 2, 0, 0, 0, 0), (0, 4, 0, 0, 0, 0)}, "E2 is not a polynomial in q1^2"
    a0, a1, a2 = (d2.get((0, 2 * j, 0, 0, 0, 0), fmpq_poly([0])) for j in range(3))
    c2 = (C * C) % P
    ok1 = ((a1 + 2 * a2 * c2) % P) == 0
    ok0 = ((a0 - a2 * c2 * c2) % P) == 0
    nz = (a2 % P) != 0 and (C % P) != 0
    print(f"E2 = a2 (q1^2 - c^2)^2 in L[q1]: {ok1 and ok0}; a2 != 0 and c != 0: {nz}")
    if not (ok1 and ok0 and nz):
        raise SystemExit("factorisation check failed")
    for sigma, tag in ((1, "plus"), (-1, "minus")):
        cc = (sigma * C) % P
        pw = [fmpq_poly([1])]
        for _ in range(max(m[1] for e in E for m, _ in e)):
            pw.append((pw[-1] * cc) % P)
        out, dropped = [], []
        for idx, e in enumerate(E):
            acc = {}
            for m, cs in e:
                key = (m[0], m[2], m[3], m[4], m[5])
                acc[key] = (acc.get(key, fmpq_poly([0])) + el(cs) * pw[m[1]]) % P
            rows = [(k, [acc[k][i] for i in range(5)]) for k in sorted(acc) if acc[k] != 0]
            if not rows:
                dropped.append(idx + 1)
                continue
            den = 1
            for _, cs in rows:
                for x in cs:
                    den = lcm(den, int(x.q))
            ints = [(k, [int(x * den) for x in cs]) for k, cs in rows]
            g = 0
            for _, cs in ints:
                for x in cs:
                    g = gcd(g, x)
            out.append({"from": idx + 1, "terms": [[list(k), [x // g for x in cs]] for k, cs in ints]})
        W = Path(a.out) / f"branch_{tag}"
        W.mkdir(parents=True, exist_ok=True)
        (W / "eqs.json").write_text(json.dumps({"nvars": 5, "names": NAMES, "eqs": [o["terms"] for o in out],
                                                "from": [o["from"] for o in out]}), encoding="utf-8")
        digs = [max(len(str(abs(x))) for _, cs in o["terms"] for x in cs) for o in out]
        print(f"branch q1 = {sigma:+d}c: equations kept {[o['from'] for o in out]} (vanishing: {dropped}); "
              f"terms {[len(o['terms']) for o in out]}; max digits {digs}")


if __name__ == "__main__":
    main()
