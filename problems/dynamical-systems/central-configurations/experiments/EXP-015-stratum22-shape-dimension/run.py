"""EXP-015: shape-variety dimension of the k = 2, p = 2 stratum.

Smoke: exact rational witness satisfies E1..E5 (all polynomials in r^2);
perturbed tuple violates. P1/P2: Singular std + two-way dimension. P3: gauged
variant (r12 = 1)."""
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
W = "/root/exp015"
CAP = 300
NAMES = ["r12", "d1A", "d1B", "d2A", "d2B", "wA", "wB", "cs", "cx"]
SYMS = {n: sp.Symbol(n) for n in NAMES}
T = sp.Symbol("t")
GEN_NAMES = NAMES + ["t"]
RESULTS = {}


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


def build_eqs():
    r12, d1A, d1B, d2A, d2B, wA, wB, cs, cx = (SYMS[n] for n in NAMES)
    A1 = d1A**2 - wA**2 / 4
    A2 = d2A**2 - wA**2 / 4
    B1 = d1B**2 - wB**2 / 4
    B2 = d2B**2 - wB**2 / 4
    H = cs**2 - (wA - wB) ** 2 / 4
    E1 = cx**2 - cs**2 - wA * wB
    E2 = (A1 + A2 - r12**2) ** 2 - 4 * A1 * A2
    E3 = (A1 + H - B1) ** 2 - 4 * A1 * H
    E4 = (A2 + H - B2) ** 2 - 4 * A2 * H
    E5 = (B1 + B2 - r12**2) ** 2 - 4 * B1 * B2
    eqs = [sp.expand(4 * E1), sp.expand(16 * E2), sp.expand(16 * E3),
           sp.expand(16 * E4), sp.expand(16 * E5)]
    return eqs


def witness_squares():
    """(a1,a2,u,v,p,q) = (3,-1,2,1,1,-2): exact squared distances."""
    a1, a2, u, v, p, q = 3, -1, 2, 1, 1, -2
    sq = {
        "r12": (a1 - a2) ** 2,
        "d1A": u**2 + (a1 - v) ** 2, "d1B": p**2 + (a1 - q) ** 2,
        "d2A": u**2 + (a2 - v) ** 2, "d2B": p**2 + (a2 - q) ** 2,
        "wA": (2 * u) ** 2, "wB": (2 * p) ** 2,
        "cs": (u - p) ** 2 + (v - q) ** 2, "cx": (u + p) ** 2 + (v - q) ** 2,
    }
    return {SYMS[k]: sp.Rational(val) for k, val in sq.items()}


def smoke(eqs):
    sq = witness_squares()
    sub = {s: v for s, v in sq.items()}
    even_eval = []
    for e in eqs:
        pe = sp.Poly(e, *[SYMS[n] for n in NAMES])
        val = sp.Integer(0)
        for mono, coeff in zip(pe.monoms(), pe.coeffs()):
            term = coeff
            ok = True
            for n, ex in zip(NAMES, mono):
                if ex % 2 != 0:
                    ok = False
                    break
                term *= sub[SYMS[n]] ** (ex // 2)
            if not ok:
                even_eval.append(None)
                break
            val += term
        else:
            even_eval.append(val)
    all_even = all(v is not None for v in even_eval)
    ok_wit = all_even and all(v == 0 for v in even_eval)
    bad = dict(sub)
    bad[SYMS["cx"]] = bad[SYMS["cx"]] + 1
    viol = False
    for e in eqs:
        pe = sp.Poly(e, *[SYMS[n] for n in NAMES])
        val = sp.Integer(0)
        for mono, coeff in zip(pe.monoms(), pe.coeffs()):
            term = coeff
            for n, ex in zip(NAMES, mono):
                term *= bad[SYMS[n]] ** (sp.Rational(ex, 2))
            val += term
        if val != 0:
            viol = True
            break
    ok = ok_wit and viol
    record("smoke-witness", "pass" if ok else "FAIL",
           f"all-even-monomials:{all_even} witness-zero:{ok_wit} perturbed-violates:{viol}")
    return ok


def singular_dim(name, eqs, extra, cap):
    polys = ",\n".join(str(sp.expand(e)).replace("**", "^").replace(" ", "")
                       for e in eqs + extra)
    script = (f"ring r=0,({','.join(GEN_NAMES)}),dp;\nshort=0;\n"
              f"ideal I={polys};\nideal S=std(I);\n"
              f"string(\"SINGDIM=\",dim(S));\nideal L=lead(S);\nL;\nquit;\n")
    sf = ART / f"{name}.sing"
    sf.write_text(script, encoding="utf-8", newline="\n")
    win = str(sf).replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {W} && cp '{win}' {W}/{name}.sing")
    t0 = time.time()
    r = wsl(f"cd {W} && timeout {cap} Singular -q {name}.sing && echo SING_OK",
            timeout=cap + 120)
    secs = time.time() - t0
    if "SING_OK" not in r.stdout:
        return "cap-or-error", None, None, secs
    (ART / f"{name}.out").write_text(r.stdout, encoding="utf-8")
    syms = {g: sp.Symbol(g) for g in GEN_NAMES}
    leads = []
    singdim = None
    for line in r.stdout.splitlines():
        line = line.strip()
        if line.startswith("SINGDIM="):
            singdim = int(line.split("=")[1])
        elif line.startswith("L[") and "=" in line:
            mono = line.split("=", 1)[1].replace("^", "**")
            pp = sp.Poly(sp.sympify(mono, locals=syms), *[syms[g] for g in GEN_NAMES])
            leads.append(list(pp.monoms()[0]))
    sups = [frozenset(i for i, e in enumerate(l) if e > 0) for l in leads]
    sups = [s for s in sups if s]
    ours = None
    for size in range(len(GEN_NAMES), -1, -1):
        for S in combinations(range(len(GEN_NAMES)), size):
            Sset = set(S)
            if all(not sup <= Sset for sup in sups):
                ours = size
                break
        if ours is not None:
            break
    return "ok", ours, singdim, secs


def main():
    log("EXP-015 runner start")
    eqs = build_eqs()
    if not smoke(eqs):
        log("SMOKE FAILED; stopping")
        return 1
    sat = T * sp.prod([SYMS[n] for n in NAMES]) - 1

    st, ours, sd, secs = singular_dim("shape-ungauged", eqs, [sat], CAP)
    if st == "ok":
        agree = ours == sd
        record("p2-ungauged-dim", "decided" if agree else "ENGINE-DISAGREEMENT",
               f"{secs:.0f}s; ours={ours} singular={sd} agree={agree}")
    else:
        record("p2-ungauged-dim", "inconclusive-cap", f"{secs:.0f}s")

    st, ours, sd, secs = singular_dim("shape-gauged", eqs, [SYMS["r12"] - 1, sat], CAP)
    if st == "ok":
        agree = ours == sd
        record("p3-gauged-dim", "decided" if agree else "ENGINE-DISAGREEMENT",
               f"{secs:.0f}s; ours={ours} singular={sd} agree={agree}")
    else:
        record("p3-gauged-dim", "inconclusive-cap", f"{secs:.0f}s")

    log("runner done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
