"""EXP-014: the incremental cut. One Singular script: recompute the products
basis S (sanity: 2436 leads), check NF(cm, S) != 0, then T = std(S, cm) under
an 1800 s cap; dimension read two ways with required agreement."""
import json
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "code"))
from cclib import (cayley_menger_spatial5, dziobek_products5, rvar,  # noqa: E402
                   strip_monomial_factors)

ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = ART / "run-log.txt"
W = "/root/exp014"
CAP = 1800
GENS10 = [rvar(i, j) for i in range(1, 6) for j in range(i + 1, 6)]
T = sp.Symbol("t")
GEN_NAMES = [str(g) for g in GENS10 + [T]]
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


def staircase_dim(leads, ngens):
    sups = [frozenset(i for i, e in enumerate(l) if e > 0) for l in leads]
    sups = [s for s in sups if s]
    for size in range(ngens, -1, -1):
        for S in combinations(range(ngens), size):
            Sset = set(S)
            if all(not sup <= Sset for sup in sups):
                return size, list(S)
    return -1, []


def main():
    log("EXP-014 runner start")
    hs = [strip_monomial_factors(v, GENS10)[0] for v in dziobek_products5().values()]
    cm = sp.expand(cayley_menger_spatial5())
    sat = T * sp.prod(GENS10) - 1

    def s(e):
        return str(sp.expand(e)).replace("**", "^").replace(" ", "")

    prods = ",\n".join(s(e) for e in hs + [sat])
    script = (
        f"ring r=0,({','.join(GEN_NAMES)}),dp;\nshort=0;\n"
        f"ideal P={prods};\n"
        f"ideal S=std(P);\n"
        f"string(\"SLEADS=\",size(S));\n"
        f"poly cm={s(cm)};\n"
        f"poly nfcm=reduce(cm,S);\n"
        f"string(\"NFZERO=\",(nfcm==0));\n"
        f"ideal Tt=std(S,cm);\n"
        f"string(\"TDIM=\",dim(Tt));\n"
        f"string(\"TSIZE=\",size(Tt));\n"
        f"ideal L=lead(Tt);\nL;\nquit;\n"
    )
    sf = ART / "incremental.sing"
    sf.write_text(script, encoding="utf-8", newline="\n")
    win = str(sf).replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {W} && cp '{win}' {W}/incremental.sing")
    t0 = time.time()
    r = wsl(f"cd {W} && timeout {CAP + 60} Singular -q incremental.sing && echo SING_OK",
            timeout=CAP + 240)
    secs = time.time() - t0
    (ART / "incremental.out").write_text(r.stdout[-2000000:], encoding="utf-8")

    sleads = nfzero = tdim = tsize = None
    syms = {g: sp.Symbol(g) for g in GEN_NAMES}
    leads = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if line.startswith("SLEADS="):
            sleads = int(line.split("=")[1])
        elif line.startswith("NFZERO="):
            nfzero = int(line.split("=")[1])
        elif line.startswith("TDIM="):
            tdim = int(line.split("=")[1])
        elif line.startswith("TSIZE="):
            tsize = int(line.split("=")[1])
        elif line.startswith("L[") and "=" in line:
            mono = line.split("=", 1)[1].replace("^", "**")
            p = sp.Poly(sp.sympify(mono, locals=syms), *[syms[g] for g in GEN_NAMES])
            leads.append(list(p.monoms()[0]))

    if sleads is not None:
        ok = sleads == 2436
        record("smoke-products-basis", "pass" if ok else "FAIL",
               f"size(S)={sleads} (EXP-013 archived 2436)")
        if not ok:
            return 1
    else:
        record("smoke-products-basis", "inconclusive-cap", f"{secs:.0f}s, no S size printed")
        return 1

    if nfzero is not None:
        record("p1-nf-nonzero", "pass" if nfzero == 0 else "FAIL",
               f"reduce(cm,S)==0 evaluates to {nfzero} (0 means NONzero normal form)")
        if nfzero != 0:
            log("NF(cm,S) is ZERO: pipeline bug per the hypothesis; stopping")
            return 1

    if "SING_OK" not in r.stdout or tdim is None:
        record("p2-incremental-std", "inconclusive-cap",
               f"{secs:.0f}s at {CAP}s cap; NF stage {'done' if nfzero is not None else 'unknown'}")
        log("runner done (capped)")
        return 0

    (ART / "cut-leads.json").write_text(json.dumps(leads), encoding="utf-8")
    d, wit = staircase_dim(leads, len(GEN_NAMES))
    agree = d == tdim
    record("p2-incremental-std", "decided", f"completed in {secs:.0f}s; basis size {tsize}")
    record("p3-cut-dimension", "decided" if agree else "ENGINE-DISAGREEMENT",
           f"our staircase dim={d} (independent set {wit}); Singular dim={tdim}; agree={agree}")
    log("runner done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
