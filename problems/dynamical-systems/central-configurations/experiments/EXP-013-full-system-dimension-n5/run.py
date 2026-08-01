"""EXP-013: the full-system shot (exact staircase dimension of the n = 5
spatial Dziobek cut), with the declared menu fallback.

P1: Singular std() of {15 stripped products, CM, sat} at 600 s; dimension read
BOTH from our independent-set staircase on the parsed leading ideal AND from
Singular's own dim() report; they must agree.
P2 (only if P1 caps): the 26-subideal growth menu at 120 s each.
"""
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
W = "/root/exp013"
GENS10 = [rvar(i, j) for i in range(1, 6) for j in range(i + 1, 6)]
T = sp.Symbol("t")
GENS = GENS10 + [T]
GEN_NAMES = [str(g) for g in GENS]
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


def singular_run(name, eq_exprs, cap, want_dim=False):
    polys = ",\n".join(str(sp.expand(e)).replace("**", "^").replace(" ", "")
                       for e in eq_exprs)
    dim_line = "ideal S=std(I);\nint d=dim(S);\nstring(\"SINGDIM=\",d);\nideal L=lead(S);\n" \
        if want_dim else "ideal L=lead(std(I));\n"
    script = (f"ring r=0,({','.join(GEN_NAMES)}),dp;\nshort=0;\n"
              f"ideal I={polys};\n{dim_line}L;\nquit;\n")
    sf = ART / f"{name}.sing"
    sf.write_text(script, encoding="utf-8", newline="\n")
    win = str(sf).replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {W} && cp '{win}' {W}/{name}.sing")
    t0 = time.time()
    r = wsl(f"cd {W} && timeout {cap} Singular -q {name}.sing && echo SING_OK",
            timeout=cap + 120)
    secs = time.time() - t0
    if "SING_OK" not in r.stdout:
        return "cap-or-error", [], None, secs
    (ART / f"{name}.out").write_text(r.stdout, encoding="utf-8")
    syms = {g: sp.Symbol(g) for g in GEN_NAMES}
    leads = []
    singdim = None
    for line in r.stdout.splitlines():
        line = line.strip()
        if line.startswith("SINGDIM="):
            singdim = int(line.split("=")[1])
        if "=" in line and line.startswith("L["):
            mono = line.split("=", 1)[1].replace("^", "**")
            p = sp.Poly(sp.sympify(mono, locals=syms), *[syms[g] for g in GEN_NAMES])
            leads.append(list(p.monoms()[0]))
    return "ok", leads, singdim, secs


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
    log("EXP-013 runner start")
    hs = [strip_monomial_factors(v, GENS10)[0] for v in dziobek_products5().values()]
    names = list(dziobek_products5().keys())
    cm = sp.expand(cayley_menger_spatial5())
    sat = T * sp.prod(GENS10) - 1
    full = hs + [cm, sat]

    st, leads, singdim, secs = singular_run("full-system", full, 600, want_dim=True)
    if st == "ok":
        (ART / "full-leads.json").write_text(json.dumps(leads), encoding="utf-8")
        d, wit = staircase_dim(leads, len(GENS))
        agree = (singdim is None) or (d == singdim)
        record("p1-full-system", "decided" if agree else "ENGINE-DISAGREEMENT",
               f"{secs:.0f}s; leads {len(leads)}; our staircase dim={d} "
               f"(independent set {wit}); Singular dim={singdim}; agree={agree}")
        log("runner done (P1 path)")
        return 0

    record("p1-full-system", "inconclusive-cap", f"{secs:.0f}s at 600s cap")
    log("P1 capped; running the declared P2 menu")
    quads = list(combinations(range(1, 6), 4))
    menu = []
    for qi, qj in combinations(range(5), 2):
        ti, tj = "".join(map(str, quads[qi])), "".join(map(str, quads[qj]))
        hi = [hs[k] for k, nm in enumerate(names) if nm.startswith(f"h{ti}_")]
        hj = [hs[k] for k, nm in enumerate(names) if nm.startswith(f"h{tj}_")]
        menu.append((f"dl-{ti}-{tj}", hi + hj + [sat]))
    for q in quads:
        tag = "".join(map(str, q))
        hq = [hs[k] for k, nm in enumerate(names) if nm.startswith(f"h{tag}_")]
        menu.append((f"lcm-{tag}", hq + [cm, sat]))
    for qi, qj in combinations(range(5), 2):
        ti, tj = "".join(map(str, quads[qi])), "".join(map(str, quads[qj]))
        ki = names.index(f"h{ti}_ab")
        kj = names.index(f"h{tj}_ab")
        menu.append((f"pcm-{ti}-{tj}", [hs[ki], hs[kj], cm, sat]))
    menu.append(("all15-nocm", hs + [sat]))

    union = []
    done = 0
    for name, eqs in menu:
        st, leads, _, secs = singular_run(name, eqs, 120)
        if st == "ok":
            done += 1
            union.extend(leads)
            log(f"  {name}: ok {secs:.0f}s, {len(leads)} leads")
        else:
            log(f"  {name}: {st} {secs:.0f}s")
    dedup = [list(x) for x in {tuple(l) for l in union}]
    (ART / "menu-union-leads.json").write_text(json.dumps(dedup), encoding="utf-8")
    d, wit = staircase_dim(dedup, len(GENS))
    record("p2-menu-bound", "decided",
           f"completed {done}/26; union {len(dedup)} leads; d_pgb={d}; set {wit}")
    log("runner done (P2 path)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
