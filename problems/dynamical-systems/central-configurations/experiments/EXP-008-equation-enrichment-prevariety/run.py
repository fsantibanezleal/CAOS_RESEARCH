"""EXP-008: does ADDING valid equations shrink the n = 4 prevariety and rescue the
hard equal-valuation case?

Builds four systems (A1 baseline, A2 +e_IU, A3 +Dziobek, A4 +both) by appending
cclib-generated polynomials to gfan's own `_nbody` output in the same ring, runs the
tropical prevariety per valuation, and decides every comet EXACTLY (EXP-007
instrument). Deterministic; artifacts and hashes persisted.
"""
import json
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "code"))
sys.path.insert(0, str(HERE.parent / "EXP-004-valuation-equation-screening"))
from cclib import dziobek4, e_iu, rvar  # noqa: E402
from cclib.exact_lp import decide_pointed  # noqa: E402
from comet_analysis import components, parse_sections  # noqa: E402

ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = ART / "run-log.txt"
W = "/root/exp008"
HEAVY = "/mnt/e/_Datos/caos-research/central-configurations/EXP-008"
CAP = 600
RESULTS = {}

VALUATIONS = {"equal": [0, 0, 0, 0], "arith": [0, 1, 2, 3]}


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def wsl(cmd, timeout=None):
    return subprocess.run(["wsl", "-d", "Ubuntu-24.04", "--", "bash", "-lc", cmd],
                          capture_output=True, text=True, timeout=timeout)


def gfan_poly(expr, masses):
    """cclib polynomial -> gfan syntax, with the mass symbols kept symbolic."""
    e = sp.expand(expr)
    return str(e).replace("**", "^").replace(" ", "")


def build_systems():
    """Return {label: [extra polynomial strings]} for the four systems."""
    m = sp.symbols("m1 m2 m3 m4", positive=True)
    iu = e_iu(4, list(m))
    dz = list(dziobek4().values())
    return {
        "A1": [],
        "A2": [gfan_poly(iu, m)],
        "A3": [gfan_poly(d, m) for d in dz],
        "A4": [gfan_poly(iu, m)] + [gfan_poly(d, m) for d in dz],
    }


def make_input(label, extras, vals):
    """gfan _nbody output with the extra polynomials appended, masses valued."""
    base = wsl(f"gfan _nbody -N4 --masses --alsosymmetric --cayleymenger2").stdout
    body = base.strip()
    assert body.endswith("}"), "unexpected gfan system format"
    if extras:
        body = body[:-1].rstrip() + ",\n" + ",\n".join(extras) + "\n}"
    # substitute the masses by their valuations in Q(t)
    body = body.replace("Q[m1,m2,m3,m4,", "Q(t)[")
    import re
    # Uniform t^v substitution (including t^0): gfan's parser rejects the bare "1"
    # coefficient form that a v = 0 shortcut would produce (EXP-008 first-run catch).
    #
    # SECOND catch: under --bits 0 (arbitrary precision) gfan 0.7 fails to parse an
    # input that MIXES t^0 with positive t-powers ("Unknown variable:1"), while the
    # identical file parses under --bits 64. We therefore shift all valuations by a
    # constant so that none is zero. This is mathematically free: every polynomial of
    # the system is homogeneous in the masses (the AC equations are linear in them,
    # e_IU is quadratic, Cayley-Menger and Dziobek carry none), so the shift
    # multiplies each polynomial by a unit t^c, and multiplying by a unit leaves its
    # tropical hypersurface, hence the whole prevariety, unchanged.
    shift = 1 - min(vals) if min(vals) <= 0 else 0
    for i, v in enumerate(vals, start=1):
        body = re.sub(rf"\bm{i}\b", f"t^{v + shift}", body)
    path = ART / f"in-{label}.txt"
    path.write_text(body + "\n", encoding="utf-8")
    win = str(path).replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {W} {HEAVY} && cp '{win}' {W}/in-{label}.txt")
    return f"{W}/in-{label}.txt"


def decide_file(local_out):
    rays, cones = parse_sections(local_out)
    comps = components(rays, cones)
    pointed = unpointed = 0
    for comp in comps:
        gens = [[Fraction(x) for x in rays[i][1:]] for i in comp if rays[i][0] == 0]
        if not gens:
            pointed += 1
            continue
        res = decide_pointed(gens)
        if res.pointed:
            pointed += 1
        else:
            unpointed += 1
    return len(comps), pointed, unpointed


def main():
    LOG.write_text("", encoding="utf-8")
    log("EXP-008 start")
    systems = build_systems()
    log(f"systems built: " + ", ".join(f"{k}(+{len(v)} eqs)" for k, v in systems.items()))
    table = {}
    for vname, vals in VALUATIONS.items():
        for sname, extras in systems.items():
            label = f"n4-{sname}-{vname}"
            path = make_input(label, extras, vals)
            t0 = time.time()
            r = wsl(f"cd {W} && timeout {CAP} gfan _tropicalprevariety --usevaluation "
                    f"-j8 --mint --minx --bits 0 < {path} > {W}/out-{label}.out "
                    f"2> {W}/err-{label}.txt && echo OK", timeout=CAP + 120)
            secs = time.time() - t0
            if "OK" not in r.stdout:
                err = wsl(f"tail -2 {W}/err-{label}.txt").stdout.strip()
                table[label] = {"status": "cap-or-error", "seconds": round(secs, 1),
                                "err": err[:200]}
                log(f"{label}: CAP-OR-ERROR ({secs:.0f} s) {err[:120]}")
                continue
            out = wsl(f"cat {W}/out-{label}.out").stdout
            local = ART / f"out-{label}.out"
            local.write_text(out, encoding="utf-8")
            fvec = ""
            lines = out.splitlines()
            for i, ln in enumerate(lines):
                if ln.strip() == "F_VECTOR" and i + 1 < len(lines):
                    fvec = lines[i + 1].strip()
                    break
            ncom, npt, nunpt = decide_file(str(local))
            table[label] = {"status": "ok", "f_vector": fvec, "comets": ncom,
                            "pointed": npt, "unpointed": nunpt,
                            "seconds": round(secs, 1)}
            log(f"{label}: fvec [{fvec}] comets {ncom} pointed {npt} unpointed {nunpt} "
                f"({secs:.0f} s)")
            (ART / "table.json").write_text(json.dumps(table, indent=2), encoding="utf-8")
    (ART / "table.json").write_text(json.dumps(table, indent=2), encoding="utf-8")
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
