"""EXP-012: the partial-GB engine spike (Singular over QQ vs the EXP-011 wall).

P1 controls (toy + EXP-011 job 3 exact reproduction), P2 A/B on the archived
15 EXP-011 jobs, P3 the lighter 16-subideal menu, P4 union staircase bound.
Singular is verdict-grade (QQ); msolve -g is mod-p and used as a recorded
cross-check on the toy control only.
"""
import json
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
E11 = HERE.parent / "EXP-011-spatial-dziobek-dimension-n5"
sys.path.insert(0, str(HERE.parents[1] / "code"))
from cclib import (cayley_menger_spatial5, dziobek_products5, rvar,  # noqa: E402
                   strip_monomial_factors)

ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = ART / "run-log.txt"
W = "/root/exp012"
CAP = 120
GENS10 = [rvar(i, j) for i in range(1, 6) for j in range(i + 1, 6)]
T = sp.Symbol("t")
GENS = GENS10 + [T]
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


def singular_leads(name, gen_names, eq_strs, cap=CAP):
    """Run lead(std(I)) over QQ in Singular under `timeout`; return
    (status, leads as exponent tuples, seconds)."""
    polys = ",\n".join(e.replace("**", "^").replace(" ", "") for e in eq_strs)
    script = (f"ring r=0,({','.join(gen_names)}),dp;\nshort=0;\n"
              f"ideal I={polys};\nideal L=lead(std(I));\nL;\nquit;\n")
    sf = ART / f"{name}.sing"
    sf.write_text(script, encoding="utf-8", newline="\n")
    win = str(sf).replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {W} && cp '{win}' {W}/{name}.sing")
    t0 = time.time()
    r = wsl(f"cd {W} && timeout {cap} Singular -q {name}.sing && echo SING_OK",
            timeout=cap + 120)
    secs = time.time() - t0
    if "SING_OK" not in r.stdout:
        return "cap-or-error", [], secs
    (ART / f"{name}.out").write_text(r.stdout, encoding="utf-8")
    syms = {g: sp.Symbol(g) for g in gen_names}
    leads = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if "=" not in line or not line.startswith("L["):
            continue
        mono = line.split("=", 1)[1].replace("^", "**")
        expr = sp.sympify(mono, locals=syms)
        p = sp.Poly(expr, *[syms[g] for g in gen_names])
        leads.append(list(p.monoms()[0]))
    return "ok", leads, secs


def staircase_dim(leads, ngens):
    sups = [frozenset(i for i, e in enumerate(l) if e > 0) for l in leads]
    sups = [s for s in sups if s]
    for size in range(ngens, -1, -1):
        for S in combinations(range(ngens), size):
            Sset = set(S)
            if all(not sup <= Sset for sup in sups):
                return size, list(S)
    return -1, []


def sympy_grevlex_leads(eq_strs, gen_names, syms=None):
    """Correct grevlex lead extraction. CAUTION (the bug EXP-012's control
    caught in the EXP-011 harvester): sp.groebner(...).polys default to LEX
    ordering regardless of the basis order, so monoms()[0] returns the LEX
    lead; monoms(order='grevlex') must be requested explicitly."""
    syms = syms or {g: sp.Symbol(g) for g in gen_names}
    gens = [syms[g] for g in gen_names]
    eqs = [sp.sympify(e, locals=syms) for e in eq_strs]
    gb = sp.groebner(eqs, *gens, order="grevlex")
    return sorted(tuple(p.monoms(order="grevlex")[0]) for p in gb.polys)


def controls():
    st, leads, secs = singular_leads("ctl-toy", ["x", "y"], ["x**2-y", "y**2-x"], 60)
    toy_ok = st == "ok" and sorted(map(tuple, leads)) == [(0, 2), (2, 0)]
    sympy_leads = sympy_grevlex_leads(["x**2-y", "y**2-x"], ["x", "y"])
    toy_ok = toy_ok and sympy_leads == [(0, 2), (2, 0)]
    prime = 1073741827
    ms_in = f"x,y\n{prime}\nx^2-y,\ny^2-x\n"
    (ART / "ctl-toy.ms").write_text(ms_in, encoding="utf-8", newline="\n")
    win = str(ART / "ctl-toy.ms").replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {W} && cp '{win}' {W}/ctl-toy.ms")
    r = wsl(f"cd {W} && timeout 60 msolve -g 1 -f ctl-toy.ms -o ctl-toy.gb && cat ctl-toy.gb")
    ms_ok = ("x^2" in r.stdout and "y^2" in r.stdout)
    record("p1a-toy-three-engines", "pass" if (toy_ok and ms_ok) else "FAIL",
           f"singular {sorted(map(tuple, leads))}; sympy {sympy_leads}; msolve mod {prime}: {ms_ok}")

    job = json.loads((E11 / "artifacts" / "pgb-job-3.json").read_text(encoding="utf-8"))
    st, leads, secs = singular_leads("ctl-job3", job["gens"], job["eqs"], CAP)
    # The EXP-011 archive (pgb-union.json) is NOT the reference: EXP-012's
    # first control run exposed that the EXP-011 harvester extracted LEX leads
    # of a grevlex basis (sympy gb.polys default to lex). The reference is a
    # fresh sympy grevlex-correct recomputation of the same job.
    try:
        ref = sympy_grevlex_leads(job["eqs"], job["gens"])
        same = st == "ok" and sorted(map(tuple, leads)) == ref
        detail = (f"singular {st} in {secs:.0f}s, {len(leads)} leads; "
                  f"sympy grevlex-correct recomputation {len(ref)} leads; exact match: {same}")
    except Exception as exc:  # noqa: BLE001
        same = False
        detail = f"sympy recomputation failed: {exc}"
    record("p1b-job3-exact-reproduction", "pass" if same else "FAIL", detail)
    return toy_ok and ms_ok and same


def main():
    log("EXP-012 runner start")
    if not controls():
        log("CONTROLS FAILED; stopping before any menu time")
        return 1

    union = []
    completed_ab = 0
    times = {}
    for i in range(15):
        job = json.loads((E11 / "artifacts" / f"pgb-job-{i}.json").read_text(encoding="utf-8"))
        st, leads, secs = singular_leads(f"ab-{i}", job["gens"], job["eqs"], CAP)
        times[f"ab-{i}"] = round(secs, 1)
        if st == "ok":
            completed_ab += 1
            union.extend(leads)
            log(f"  A/B subideal {i}: ok {secs:.0f}s, {len(leads)} leads")
        else:
            log(f"  A/B subideal {i}: {st} {secs:.0f}s")
    record("p2-ab-singular", "decided",
           f"completed {completed_ab}/15 at {CAP}s caps (sympy baseline 1/15); times {times}")

    hs = [strip_monomial_factors(v, GENS10)[0] for v in dziobek_products5().values()]
    names = list(dziobek_products5().keys())
    cm = sp.expand(cayley_menger_spatial5())
    sat = T * sp.prod(GENS10) - 1
    gen_names = [str(g) for g in GENS]
    quads = list(combinations(range(1, 6), 4))
    menu = []
    for qi, q in enumerate(quads):
        tag = "".join(map(str, q))
        idxs = [k for k, nm in enumerate(names) if nm.startswith(f"h{tag}_")]
        menu.append((f"local-{tag}", [hs[k] for k in idxs] + [sat]))
    for qi, qj in combinations(range(5), 2):
        ti, tj = "".join(map(str, quads[qi])), "".join(map(str, quads[qj]))
        ki = names.index(f"h{ti}_ab")
        kj = names.index(f"h{tj}_ab")
        menu.append((f"pair-{ti}-{tj}", [hs[ki], hs[kj], sat]))
    menu.append(("cm-only", [cm, sat]))

    completed_v2 = 0
    for name, eqs in menu:
        st, leads, secs = singular_leads(f"v2-{name}", gen_names,
                                         [str(sp.expand(e)) for e in eqs], CAP)
        times[f"v2-{name}"] = round(secs, 1)
        if st == "ok":
            completed_v2 += 1
            union.extend(leads)
            log(f"  v2 {name}: ok {secs:.0f}s, {len(leads)} leads")
        else:
            log(f"  v2 {name}: {st} {secs:.0f}s")
    record("p3-menu-v2", "decided", f"completed {completed_v2}/16 at {CAP}s caps")

    dedup = [list(x) for x in {tuple(l) for l in union}]
    (ART / "union-leads.json").write_text(json.dumps(dedup), encoding="utf-8")
    d, witness = staircase_dim(dedup, len(GENS))
    record("p4-union-bound", "decided",
           f"union leads {len(dedup)} from {completed_ab + completed_v2} subideals; "
           f"d_pgb={d}; independent set {witness}")
    (ART / "times.json").write_text(json.dumps(times, indent=2), encoding="utf-8")
    log("runner done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
