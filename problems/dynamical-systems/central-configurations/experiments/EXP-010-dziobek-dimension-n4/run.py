"""EXP-010: Dziobek-variety dimension calibration at n = 4.

Object: D4 = V(h_ab, h_bc, h_ac, CM) in the r-torus (Rabinowitsch t).
Instrument: recorded random integer linear sections keep every msolve call
zero-dimensional (P1: 3-sections nonempty + degree; P2: 4-sections empty;
P4: degree agreement across draws). P3 (deterministic grevlex staircase
dimension) runs in a capped subprocess via p3_dim.py.

Smoke gate BEFORE any solver time: square passes h+CM, tetrahedron passes h
but fails CM, the 3-4-5 rectangle passes CM but fails h.
"""
import json
import random
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "code"))
from cclib import (cayley_menger_planar4, dziobek4, rvar,  # noqa: E402
                   strip_monomial_factors)

ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = ART / "run-log.txt"
W = "/root/exp010"
CAP_SECTION = 900
CAP_P3 = 1800
SEED = 20260801
GENS6 = [rvar(i, j) for i in range(1, 5) for j in range(i + 1, 5)]
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
    """Stripped Dziobek differences + planar CM + Rabinowitsch; these exact
    polynomials go to msolve, the smoke test, and P3 alike."""
    h = dziobek4()
    eqs = [strip_monomial_factors(v, GENS6) for v in h.values()]
    eqs.append(sp.expand(cayley_menger_planar4()))
    sat = T * sp.prod(GENS6) - 1
    return eqs, sat


def _zero_mod_square(expr):
    """Exact membership of the EXP-001 square: substitute sides A, diagonals
    A*S2 symbolically, then reduce modulo the defining relations
    8A^3 = 4 + S2 and S2^2 = 2 (the side satisfies a^3 = (4 + sqrt(2))/8).
    Zero remainder is a polynomial-arithmetic certificate, no radicals."""
    A, S2 = sp.symbols("A S2")
    sub = {rvar(1, 2): A, rvar(2, 3): A, rvar(3, 4): A, rvar(1, 4): A,
           rvar(1, 3): A * S2, rvar(2, 4): A * S2}
    p = sp.expand(expr.subs(sub, simultaneous=True))
    _, rem = sp.reduced(p, [8 * A**3 - 4 - S2, S2**2 - 2], A, S2, order="lex")
    return sp.expand(rem) == 0


def smoke(eqs):
    """Three-way discrimination; every acceptance is exact rational or exact
    polynomial-reduction arithmetic."""
    tetra = {g: sp.Integer(1) for g in GENS6}
    rect = {rvar(1, 2): sp.Integer(3), rvar(3, 4): sp.Integer(3),
            rvar(2, 3): sp.Integer(4), rvar(1, 4): sp.Integer(4),
            rvar(1, 3): sp.Integer(5), rvar(2, 4): sp.Integer(5)}
    hs, cm = eqs[:3], eqs[3]

    sq_h = all(_zero_mod_square(v) for v in hs)
    sq_cm = _zero_mod_square(cm)
    te_h = all(v.subs(tetra, simultaneous=True) == 0 for v in hs)
    te_cm = cm.subs(tetra, simultaneous=True)
    re_h = [v.subs(rect, simultaneous=True) for v in hs]
    re_cm = cm.subs(rect, simultaneous=True)

    ok = (sq_h and sq_cm and te_h and te_cm != 0
          and re_cm == 0 and any(v != 0 for v in re_h))
    detail = (f"square h=0:{sq_h} cm=0:{sq_cm}; tetra h=0:{te_h} cm={te_cm}; "
              f"rect cm={re_cm} some-h!=0:{any(v != 0 for v in re_h)}")
    record("smoke-three-way", "pass" if ok else "FAIL", detail)
    return ok


def draw_sections(rng, count):
    secs = []
    for _ in range(count):
        c0 = rng.randint(-10**6, 10**6)
        cs = [rng.randint(-10**6, 10**6) for _ in GENS6]
        secs.append(sp.Integer(c0) + sum(sp.Integer(c) * g for c, g in zip(cs, GENS6)))
    return secs


def write_input(name, eqs):
    gens = GENS6 + [T]
    text = ",".join(str(g) for g in gens) + "\n0\n" + ",\n".join(ms(e) for e in eqs) + "\n"
    (ART / f"{name}.ms").write_text(text, encoding="utf-8", newline="\n")
    win = str(ART / f"{name}.ms").replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {W} && cp '{win}' {W}/{name}.ms")
    return f"{W}/{name}.ms"


def run_msolve(name, path, cap):
    t0 = time.time()
    r = wsl(f"cd {W} && timeout {cap} msolve -P 2 -f {path} -o {W}/{name}.out && echo OK",
            timeout=cap + 180)
    secs = time.time() - t0
    if "OK" not in r.stdout:
        return None, secs, (r.stdout + r.stderr)[-300:]
    out = wsl(f"cat {W}/{name}.out").stdout
    (ART / f"{name}.out").write_text(out, encoding="utf-8")
    return out, secs, ""


def dim_of(text):
    t = text.strip()
    return int(t[1:t.index(",")]) if t.startswith("[") and "," in t else None


def complex_count(text):
    """Degree of the RUR eliminant = number of complex solutions (with
    multiplicity) of the sectioned 0-dim system. In msolve's -P output the
    eliminant appears as the first dense coefficient list of length > 1; its
    length minus one is the degree. Raw output is archived either way."""
    import re
    best = None
    for m in re.finditer(r"\[([-0-9,\s/^]+)\]", text):
        body = m.group(1)
        if "/" in body or "^" in body:
            continue
        try:
            coeffs = [int(x) for x in body.replace(" ", "").split(",") if x]
        except ValueError:
            continue
        if len(coeffs) > 2 and (best is None or len(coeffs) > best):
            best = len(coeffs)
    return None if best is None else best - 1


def main():
    log(f"EXP-010 runner start; seed {SEED}")
    eqs, sat = build_system()
    if not smoke(eqs):
        log("SMOKE FAILED: no solver time is spent; aborting per hypothesis.")
        return 1

    rng = random.Random(SEED)
    draws = {}
    plan = [("p1-draw1", 3), ("p1-draw2", 3), ("p2-draw1", 4), ("p2-draw2", 4)]
    for name, d in plan:
        secs = draw_sections(rng, d)
        draws[name] = [str(s) for s in secs]
        (ART / "draws.json").write_text(json.dumps(draws, indent=2), encoding="utf-8")
        path = write_input(name, eqs + [sat] + secs)
        log(f"{name}: {d} sections drawn, msolve launching (cap {CAP_SECTION}s)")
        out, secs_t, err = run_msolve(name, path, CAP_SECTION)
        if out is None:
            record(name, "inconclusive-cap", f"{secs_t:.0f}s; {err}")
            continue
        dim = dim_of(out)
        cc = complex_count(out)
        record(name, "decided", f"dim={dim} complex-count={cc} in {secs_t:.0f}s")

    log(f"P3: grevlex staircase dimension in subprocess (cap {CAP_P3}s)")
    try:
        r = subprocess.run([sys.executable, str(HERE / "p3_dim.py")],
                           capture_output=True, text=True, timeout=CAP_P3)
        record("p3-staircase-dim", "decided" if r.returncode == 0 else "error",
               (r.stdout + r.stderr).strip()[-500:])
    except subprocess.TimeoutExpired:
        record("p3-staircase-dim", "inconclusive-cap", f"{CAP_P3}s sympy cap")

    log("runner done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
