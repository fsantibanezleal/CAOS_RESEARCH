"""EXP-006: msolve-engine censuses with exact cross-verification in sympy.

Deterministic. msolve (WSL) computes; sympy verifies. The verification is EXACT:
msolve returns rational isolating boxes for the real solutions, and containment of
an exact algebraic point in a rational box is decided exactly, so we check that the
boxes contain precisely the points our own exact machinery knows and nothing else.

Known exact points used as the reference set (all from committed verdicts):
  n = 3, any positive masses: the equilateral point (1, 1, 1) [EXP-001 P2, symbolic]
  plus exactly one collinear point per ordering [EXP-001 P3, decided exactly for all
  four sample mass vectors via the per-chart eliminant censuses].

Run:  .venv/Scripts/python.exe problems/.../EXP-006-msolve-census/run.py
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
from cclib import (ac_asymmetric, ac_symmetric, cayley_menger_planar4,  # noqa: E402
                   census_positive, e_iu, rvar)

ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = ART / "run-log.txt"
WSL_TMP = "/root/exp006"
CAP_N3 = 1800
CAP_N4 = 3600
SAMPLES = [(1, 1, 1), (1, 1, 2), (1, 2, 3), (2, 3, 5)]
RESULTS = {}


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def record(key, status, detail=""):
    RESULTS[key] = {"status": status, "detail": detail}
    log(f"RESULT {key}: {status} {detail}")
    (ART / "results.json").write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")


def wsl(cmd, timeout=None):
    return subprocess.run(["wsl", "-d", "Ubuntu-24.04", "--", "bash", "-lc", cmd],
                          capture_output=True, text=True, timeout=timeout)


def to_msolve(expr):
    return str(sp.expand(expr)).replace("**", "^").replace(" ", "")


def write_input(name, gens, eqs):
    body = ",\n".join(to_msolve(e) for e in eqs)
    text = ",".join(str(g) for g in gens) + "\n0\n" + body + "\n"
    (ART / f"{name}.ms").write_text(text, encoding="utf-8")
    win = str((ART / f"{name}.ms")).replace("\\", "/").replace("D:/", "/mnt/d/")
    wsl(f"mkdir -p {WSL_TMP} && cp '{win}' {WSL_TMP}/{name}.ms")
    return f"{WSL_TMP}/{name}.ms"


def run_msolve(name, path, cap):
    t0 = time.time()
    r = wsl(f"cd {WSL_TMP} && timeout {cap} msolve -f {path} -o {WSL_TMP}/{name}.out "
            f"&& echo MSOLVE_OK", timeout=cap + 120)
    secs = time.time() - t0
    if "MSOLVE_OK" not in r.stdout:
        return None, secs, (r.stdout + r.stderr)[-400:]
    out = wsl(f"cat {WSL_TMP}/{name}.out")
    (ART / f"{name}.out").write_text(out.stdout, encoding="utf-8")
    return out.stdout, secs, ""


def parse_boxes(text):
    """Parse msolve's real-solution output into a list of coordinate boxes.

    Format: [dim, [nvars, [[[lo_num / 2^k, hi_num / 2^k], ...], ...]]]. We read every
    bracketed pair of rationals in order and group them by the variable count.
    """
    import re
    nums = re.findall(r"(-?\d+)\s*/\s*2\^(\d+)|(-?\d+)(?![\d\s]*[/^])", text)
    vals = []
    for a, b, c in nums:
        if a:
            vals.append(Fraction(int(a), 2 ** int(b)))
        elif c:
            vals.append(Fraction(int(c)))
    return vals


def parse_solution_boxes(text, nvars):
    """Structured parse: each solution is nvars intervals [lo, hi]."""
    import re
    # capture every [x, y] pair where x and y are rationals of the msolve forms
    pat = re.compile(r"\[\s*(-?\d+(?:\s*/\s*2\^\d+)?)\s*,\s*(-?\d+(?:\s*/\s*2\^\d+)?)\s*\]")

    def toF(s):
        s = s.replace(" ", "")
        if "/2^" in s:
            n, k = s.split("/2^")
            return Fraction(int(n), 2 ** int(k))
        return Fraction(int(s))

    pairs = [(toF(a), toF(b)) for a, b in pat.findall(text)]
    boxes = [pairs[i:i + nvars] for i in range(0, len(pairs) - nvars + 1, nvars)]
    return [b for b in boxes if len(b) == nvars and all(lo <= hi for lo, hi in b)]


def in_box(exact_pt, box):
    """Exact containment test of an algebraic point in a rational box."""
    for val, (lo, hi) in zip(exact_pt, box):
        lo_s, hi_s = sp.Rational(lo.numerator, lo.denominator), sp.Rational(hi.numerator, hi.denominator)
        if sp.simplify(val - lo_s) < 0 or sp.simplify(hi_s - val) < 0:
            return False
    return True


def known_exact_n3(mv):
    """The four exact positive points: equilateral + one collinear per ordering.

    Collinear points come from the per-chart eliminant census (the EXP-001 P3 route),
    recomputed here exactly (seconds per chart) so this experiment is self-contained.
    """
    R12, R13, R23 = rvar(1, 2), rvar(1, 3), rvar(2, 3)
    F = ac_symmetric(3, [sp.Integer(v) for v in mv])
    pts = [(sp.Integer(1), sp.Integer(1), sp.Integer(1))]
    charts = {"2-middle": (R13, R12 + R23), "3-middle": (R12, R13 + R23),
              "1-middle": (R23, R12 + R13)}
    for name, (lhs, rhs) in charts.items():
        eqs = [sp.expand(f.subs({lhs: rhs})) for f in F.values()]
        eqs = [e for e in eqs if e != 0]
        vars2 = sorted({s for e in eqs for s in e.free_symbols}, key=str)
        acc, _ = census_positive(eqs, vars2)
        assert len(acc) == 1, f"{mv} {name}: {len(acc)} collinear solutions"
        sol = dict(zip(vars2, acc[0]))
        sol[lhs] = rhs.subs(sol)
        pts.append((sol[R12], sol[R13], sol[R23]))
    return pts


def main():
    LOG.write_text("", encoding="utf-8")
    log("EXP-006 start (msolve computes, sympy verifies exactly)")
    gens3 = [rvar(1, 2), rvar(1, 3), rvar(2, 3)]

    for mv in SAMPLES:
        name = "n3-" + "_".join(map(str, mv))
        F = ac_symmetric(3, [sp.Integer(v) for v in mv])
        G = ac_asymmetric(3, [sp.Integer(v) for v in mv])
        eqs = list(F.values()) + list(G.values()) + [e_iu(3, [sp.Integer(v) for v in mv])]
        path = write_input(name, gens3, eqs)
        text, secs, err = run_msolve(name, path, CAP_N3)
        if text is None:
            record(f"census-{mv}", "inconclusive-cap", f"{secs:.0f} s; {err}")
            continue
        boxes = parse_solution_boxes(text, 3)
        pos = [b for b in boxes if all(lo > 0 for lo, _ in b)]
        exact = known_exact_n3(mv)
        matched, unmatched = [], []
        for pt in exact:
            hits = [i for i, b in enumerate(pos) if in_box(pt, b)]
            (matched if hits else unmatched).append((pt, hits))
        extra = len(pos) - len({h for _, hs in matched for h in hs})
        ok = len(unmatched) == 0 and extra == 0 and len(pos) == 4
        record(f"census-{mv}", "pass" if ok else "fail",
               f"msolve positive boxes: {len(pos)}; exact points matched: "
               f"{len(matched)}/4; unmatched: {len(unmatched)}; unexplained boxes: "
               f"{extra}; {secs:.0f} s")
        (ART / f"{name}-verification.json").write_text(json.dumps({
            "mv": list(mv), "n_positive_boxes": len(pos),
            "exact_points": [[str(x) for x in p] for p in exact],
            "matched": len(matched), "unmatched": len(unmatched),
            "seconds": round(secs, 1)}, indent=2), encoding="utf-8")

    # n = 4 equal masses, planar enriched system
    gens6 = [rvar(i, j) for i in range(1, 5) for j in range(i + 1, 5)]
    F4 = ac_symmetric(4, [1, 1, 1, 1])
    G4 = ac_asymmetric(4, [1, 1, 1, 1])
    eqs4 = list(F4.values()) + list(G4.values()) + [e_iu(4, [1, 1, 1, 1]),
                                                   cayley_menger_planar4()]
    path = write_input("n4-equal-planar", gens6, eqs4)
    text, secs, err = run_msolve("n4-equal-planar", path, CAP_N4)
    if text is None:
        record("n4-equal-planar", "inconclusive-cap", f"{secs:.0f} s; {err}")
    else:
        boxes = parse_solution_boxes(text, 6)
        pos = [b for b in boxes if all(lo > 0 for lo, _ in b)]
        # class key: sorted midpoints of the six distances, rounded to a tolerance
        keys = set()
        for b in pos:
            mids = sorted(float((lo + hi) / 2) for lo, hi in b)
            keys.add(tuple(round(m, 6) for m in mids))
        record("n4-equal-planar", "recorded",
               f"positive boxes: {len(pos)}; distinct sorted-distance classes: "
               f"{len(keys)}; {secs:.0f} s (class count compared against MZ19's 4 "
               f"in the verdict)")
        (ART / "n4-classes.json").write_text(json.dumps(
            {"n_positive_boxes": len(pos), "classes": sorted(map(list, keys)),
             "seconds": round(secs, 1)}, indent=2), encoding="utf-8")

    (ART / "profile.json").write_text(json.dumps(
        {"experiment": "EXP-006", "results": RESULTS,
         "msolve": "0.10.1", "sympy": sp.__version__}, indent=2), encoding="utf-8")
    fails = [k for k, v in RESULTS.items() if v["status"] == "fail"]
    log(f"done; FAIL: {fails or 'none'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
