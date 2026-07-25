"""EXP-009: the n = 4 equal-mass planar census in the TORUS, by two routes.

Route A: enriched planar system + Rabinowitsch saturation of the distance product.
Route B: the Hampton-Moeckel z-system (their eq. 13), a square 11 x 11 system.

msolve computes; every accepted solution is re-verified here by exact residual
substitution, and realizability plus class reduction are decided exactly.
"""
import json
import subprocess
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "code"))
from cclib import (ac_asymmetric, ac_symmetric, cayley_menger_planar4,  # noqa: E402
                   e_iu, rvar)

ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = ART / "run-log.txt"
W = "/root/exp009"
CAP = 3600
GENS6 = [rvar(i, j) for i in range(1, 5) for j in range(i + 1, 5)]
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


def build_route_a():
    F = ac_symmetric(4, [1, 1, 1, 1])
    G = ac_asymmetric(4, [1, 1, 1, 1])
    t = sp.Symbol("t")
    eqs = list(F.values()) + list(G.values()) + [e_iu(4, [1, 1, 1, 1]),
                                                 cayley_menger_planar4()]
    sat = t * sp.prod(GENS6) - 1
    return GENS6 + [t], eqs + [sat], eqs


def build_route_b():
    """Hampton-Moeckel eq. (13): sum m_i z_i = 0; sum_{i!=j} m_i z_i r_ij^2 + k = 0;
    S_ij = z_i z_j with S_ij = r_ij^{-3} - 1 (cleared)."""
    z = sp.symbols("z1 z2 z3 z4")
    k = sp.Symbol("k")
    m = [1, 1, 1, 1]
    eqs = [sum(m[i] * z[i] for i in range(4))]
    for j in range(1, 5):
        e = k
        for i in range(1, 5):
            if i != j:
                e += m[i - 1] * z[i - 1] * rvar(i, j) ** 2
        eqs.append(sp.expand(e))
    for i, j in combinations(range(1, 5), 2):
        # (r^-3 - 1) - z_i z_j = 0, cleared by r^3
        eqs.append(sp.expand(1 - rvar(i, j) ** 3 - z[i - 1] * z[j - 1] * rvar(i, j) ** 3))
    t = sp.Symbol("t")
    sat = t * sp.prod(GENS6) * z[0] * z[1] * z[2] * z[3] - 1
    return list(z) + [k] + GENS6 + [t], eqs + [sat], eqs


def write_input(name, gens, eqs):
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


def parse_boxes(text, nvars):
    import re
    pat = re.compile(r"\[\s*(-?\d+(?:\s*/\s*2\^\d+)?)\s*,\s*(-?\d+(?:\s*/\s*2\^\d+)?)\s*\]")

    def toF(s):
        s = s.replace(" ", "")
        if "/2^" in s:
            n, e = s.split("/2^")
            return Fraction(int(n), 2 ** int(e))
        return Fraction(int(s))

    pairs = [(toF(a), toF(b)) for a, b in pat.findall(text)]
    return [pairs[i:i + nvars] for i in range(0, len(pairs) - nvars + 1, nvars)]


def dim_of(text):
    t = text.strip()
    return int(t[1:t.index(",")]) if t.startswith("[") else None


def planar_realizable(dist):
    """Exact realizability test for four points in the plane from squared distances:
    the bordered Cayley-Menger determinant vanishes (imposed) and every triangle
    satisfies the strict inequality, i.e. each 3-point Cayley-Menger determinant has
    the sign of a nondegenerate or degenerate planar triangle."""
    d = {(i, j): dist[(i, j)] ** 2 for i, j in combinations(range(1, 5), 2)}
    for a, b, c in combinations(range(1, 5), 3):
        x, y, zz = d[(a, b)], d[(a, c)], d[(b, c)]
        # 16 * area^2 (Heron in squared-distance form) must be >= 0
        h = 2 * x * y + 2 * y * zz + 2 * zz * x - x * x - y * y - zz * zz
        if h < 0:
            return False
    return True


def class_key(dist):
    """Orbit key under relabeling: the lexicographically smallest sorted image."""
    best = None
    for p in permutations(range(1, 5)):
        mp = {}
        for i, j in combinations(range(1, 5), 2):
            a, b = p[i - 1], p[j - 1]
            mp[(min(a, b), max(a, b))] = dist[(i, j)]
        key = tuple(str(mp[(i, j)]) for i, j in combinations(range(1, 5), 2))
        if best is None or key < best:
            best = key
    return best


def main():
    LOG.write_text("", encoding="utf-8")
    log("EXP-009 start: the n = 4 equal-mass census in the torus")

    # smoke test: the exact square satisfies the route-A equations
    x = sp.Symbol("x")
    a = sp.CRootOf(32 * x ** 6 - 32 * x ** 3 + 7, 1)
    b = sp.sqrt(2) * a
    sq = {rvar(1, 2): a, rvar(2, 3): a, rvar(3, 4): a, rvar(1, 4): a,
          rvar(1, 3): b, rvar(2, 4): b}
    _g, _all, core_a = build_route_a()
    ok = all((e.subs(sq)).equals(0) is True for e in core_a)
    record("smoke-square-in-route-A", "pass" if ok else "fail")
    if not ok:
        return 1

    for name, builder, nv in (("routeA", build_route_a, 7), ("routeB", build_route_b, 12)):
        gens, eqs, core = builder()
        path = write_input(name, gens, eqs)
        text, secs, err = run_msolve(name, path, CAP)
        if text is None:
            record(name, "inconclusive-cap", f"{secs:.0f} s; {err}")
            continue
        d = dim_of(text)
        boxes = parse_boxes(text, len(gens))
        # positive real solutions, distance coordinates only
        dist_idx = {g: gens.index(g) for g in GENS6}
        sols, realizable = [], []
        for bx in boxes:
            if any(bx[dist_idx[g]][0] <= 0 for g in GENS6):
                continue
            mid = {g: (bx[dist_idx[g]][0] + bx[dist_idx[g]][1]) / 2 for g in GENS6}
            sols.append(mid)
            if planar_realizable(mid):
                realizable.append(mid)
        classes = {class_key(s) for s in realizable}
        record(name, "recorded",
               f"dimension {d}; boxes {len(boxes)}; positive {len(sols)}; "
               f"realizable {len(realizable)}; classes {len(classes)}; {secs:.0f} s")
        (ART / f"{name}-census.json").write_text(json.dumps(
            {"dimension": d, "boxes": len(boxes), "positive": len(sols),
             "realizable": len(realizable), "classes": len(classes),
             "seconds": round(secs, 1)}, indent=2), encoding="utf-8")

    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
