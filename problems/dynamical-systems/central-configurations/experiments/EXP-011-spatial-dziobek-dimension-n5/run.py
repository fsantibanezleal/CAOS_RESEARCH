"""EXP-011: spatial Dziobek dimension at n = 5 (the reshaped lane's scaling test).

Cut: 15 stripped Dziobek products + spatial Cayley-Menger, torus-saturated,
11 variables (10 distances + Rabinowitsch t). Rungs: P1 three-way smoke gate
(exact rational / polynomial-reduction arithmetic), P2 codim-5 emptiness probes
(300 s caps), P3 codim-4 cap-signature control (300 s caps), P4 partial-GB
union bound via pgb_worker.py (120 s per subideal).
"""
import json
import random
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
W = "/root/exp011"
CAP_SECTION = 300
CAP_PGB = 120
SEED = 20260811
GENS10 = [rvar(i, j) for i in range(1, 6) for j in range(i + 1, 6)]
T = sp.Symbol("t")
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


def ms(e):
    return str(sp.expand(e)).replace("**", "^").replace(" ", "")


def build_system():
    hs = [strip_monomial_factors(v, GENS10)[0] for v in dziobek_products5().values()]
    cm = sp.expand(cayley_menger_spatial5())
    sat = T * sp.prod(GENS10) - 1
    return hs, cm, sat


def smoke(hs, cm):
    w = sp.Symbol("w")
    bip = {g: sp.Integer(1) for g in GENS10}
    bip[rvar(4, 5)] = w
    rel = [w**2 - sp.Rational(8, 3)]

    def zero_mod_bip(e):
        p = sp.expand(e.subs(bip, simultaneous=True))
        _, rem = sp.reduced(p, rel, w)
        return sp.expand(rem) == 0

    ones = {g: sp.Integer(1) for g in GENS10}
    pos = [0, 3, 7, 12, 20]
    coll = {rvar(i + 1, j + 1): sp.Integer(abs(pos[j] - pos[i]))
            for i in range(5) for j in range(i + 1, 5)}

    bip_h = all(zero_mod_bip(h) for h in hs)
    bip_cm = zero_mod_bip(cm)
    ones_cm = cm.subs(ones, simultaneous=True)
    coll_cm = cm.subs(coll, simultaneous=True)
    coll_viol = sum(1 for h in hs if h.subs(coll, simultaneous=True) != 0)

    ok = (bip_h and bip_cm and ones_cm != 0 and coll_cm == 0 and coll_viol > 0)
    record("p1-smoke-three-way", "pass" if ok else "FAIL",
           f"bipyramid h=0:{bip_h} cm=0:{bip_cm}; all-ones cm={ones_cm}; "
           f"collinear cm={coll_cm} products-violated:{coll_viol}/15")
    return ok


def draw_sections(rng, count):
    secs = []
    for _ in range(count):
        c0 = rng.randint(-10**6, 10**6)
        cs = [rng.randint(-10**6, 10**6) for _ in GENS10]
        secs.append(sp.Integer(c0) + sum(sp.Integer(c) * g for c, g in zip(cs, GENS10)))
    return secs


def write_input(name, eqs):
    gens = GENS10 + [T]
    text = ",".join(str(g) for g in gens) + "\n0\n" + ",\n".join(ms(e) for e in eqs) + "\n"
    (ART / f"{name}.ms").write_text(text, encoding="utf-8", newline="\n")
    win = str(ART / f"{name}.ms").replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {W} && cp '{win}' {W}/{name}.ms")
    return f"{W}/{name}.ms"


def run_msolve(name, path, cap):
    t0 = time.time()
    r = wsl(f"cd {W} && timeout {cap} msolve -f {path} -o {W}/{name}.out && echo OK",
            timeout=cap + 180)
    secs = time.time() - t0
    if "OK" not in r.stdout:
        return None, secs, (r.stdout + r.stderr)[-300:]
    out = wsl(f"cat {W}/{name}.out").stdout
    (ART / f"{name}.out").write_text(out, encoding="utf-8")
    return out, secs, ""


def classify(out_text):
    t = out_text.strip()
    if t.startswith("[-1]"):
        return "empty"
    return "nonempty-or-other"


def staircase_dim_from_leads(leads, ngens):
    supports = [frozenset(i for i, e in enumerate(lead) if e > 0) for lead in leads]
    supports = [s for s in supports if s]  # a constant leading term would mean 1 in the ideal
    best = -1
    for size in range(ngens, -1, -1):
        for S in combinations(range(ngens), size):
            Sset = set(S)
            if all(not sup <= Sset for sup in supports):
                return size, list(S)
    return best, []


def main():
    log(f"EXP-011 runner start; seed {SEED}")
    hs, cm, sat = build_system()
    if not smoke(hs, cm):
        log("SMOKE FAILED; aborting before any solver time")
        return 1

    rng = random.Random(SEED)
    draws = {}
    plan = [("p2-draw1", 5), ("p2-draw2", 5), ("p3-draw1", 4), ("p3-draw2", 4)]
    base = hs + [cm, sat]
    for name, d in plan:
        secs = draw_sections(rng, d)
        draws[name] = [str(s) for s in secs]
        (ART / "draws.json").write_text(json.dumps(draws, indent=2), encoding="utf-8")
        path = write_input(name, base + secs)
        log(f"{name}: {d} sections, msolve launching (cap {CAP_SECTION}s)")
        out, secs_t, err = run_msolve(name, path, CAP_SECTION)
        if out is None:
            record(name, "inconclusive-cap", f"{secs_t:.0f}s; {err}")
            continue
        record(name, f"decided-{classify(out)}", f"{secs_t:.0f}s; head: {out.strip()[:60]}")

    log("P4: partial-GB union bound (15 subideals, 120 s each)")
    gens = GENS10 + [T]
    union = []
    completed = 0
    for idx, h in enumerate(hs):
        job = {"gens": [str(g) for g in gens],
               "eqs": [str(sp.expand(h)), str(sp.expand(cm)), str(sp.expand(sat))],
               "order": "grevlex"}
        jf = ART / f"pgb-job-{idx}.json"
        jf.write_text(json.dumps(job), encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, str(HERE / "pgb_worker.py"), str(jf)],
                               capture_output=True, text=True, timeout=CAP_PGB)
            if r.returncode == 0:
                data = json.loads(r.stdout)
                union.extend(data["leads"])
                completed += 1
                log(f"  subideal {idx}: gb {data['gb_size']}, leads {len(data['leads'])}")
            else:
                log(f"  subideal {idx}: error {r.stderr.strip()[-120:]}")
        except subprocess.TimeoutExpired:
            log(f"  subideal {idx}: cap {CAP_PGB}s")
    if union:
        dedup = [list(x) for x in {tuple(l) for l in union}]
        d_pgb, witness = staircase_dim_from_leads(dedup, len(gens))
        record("p4-partial-gb", "decided",
               f"subideals completed {completed}/15; union leads {len(dedup)}; "
               f"d_pgb={d_pgb}; independent set {witness}")
        (ART / "pgb-union.json").write_text(json.dumps(dedup), encoding="utf-8")
    else:
        record("p4-partial-gb", "inconclusive-cap", f"0/15 subideals completed")

    log("runner done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
