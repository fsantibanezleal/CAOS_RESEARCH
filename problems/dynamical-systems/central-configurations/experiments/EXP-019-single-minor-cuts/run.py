"""EXP-019: single-minor incremental cuts (CM/Krull endgame).

Builds the height-ring shape ideal + cleared mass matrix (EXP-017's
cross-validated construction), picks the smallest 4x4 and two smallest 3x3
minors, verifies each is nonzero at W1, then three Singular runs at 1800 s:
dim(SH+g4), dim(SH+g3), dim(SH+g3+g3'). Two-way dimension agreement."""
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
W = "/root/exp019"
CAP = 1800
DNAMES = ["r12", "d1A", "d1B", "d2A", "d2B", "wA", "wB", "cs", "cx"]
HNAMES = ["h1", "e12", "f"]
GEN_NAMES = DNAMES + HNAMES + ["t"]
SYM = {n: sp.Symbol(n) for n in GEN_NAMES}
MASS_CLASS = {1: "m1", 2: "m2", 3: "mA", 4: "mA", 5: "mB", 6: "mB"}
BLOCK = [(1, 3), (1, 5), (2, 3), (2, 5), (3, 5), (3, 6)]
PAIR2NAME = {(1, 2): "r12", (1, 3): "d1A", (1, 4): "d1A", (1, 5): "d1B",
             (1, 6): "d1B", (2, 3): "d2A", (2, 4): "d2A", (2, 5): "d2B",
             (2, 6): "d2B", (3, 4): "wA", (5, 6): "wB", (3, 5): "cs",
             (4, 6): "cs", (3, 6): "cx", (4, 5): "cx"}
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


def rname(i, j):
    return PAIR2NAME[(min(i, j), max(i, j))]


def shape_ideal():
    r12, d1A, d1B, d2A, d2B, wA, wB, cs, cx = (SYM[n] for n in DNAMES)
    h1, e12, f = (SYM[n] for n in HNAMES)
    t = SYM["t"]
    SH = [4 * h1**2 - (4 * d1A**2 - wA**2), e12**2 - r12**2,
          4 * f**2 - (4 * cs**2 - (wA - wB) ** 2),
          4 * (h1 - e12) ** 2 - (4 * d2A**2 - wA**2),
          4 * (h1 + f) ** 2 - (4 * d1B**2 - wB**2),
          4 * (h1 - e12 + f) ** 2 - (4 * d2B**2 - wB**2),
          cx**2 - cs**2 - wA * wB, r12 - 1,
          t * sp.prod([SYM[n] for n in DNAMES]) * f - 1]
    return [sp.expand(e) for e in SH]


def deltas():
    V = sp.Symbol("Vd")
    h1, e12, f = (SYM[n] for n in HNAMES)
    u, p = SYM["wA"] / 2, SYM["wB"] / 2
    POS = {1: (sp.Integer(0), h1 + V), 2: (sp.Integer(0), h1 - e12 + V),
           3: (u, V), 4: (-u, V), 5: (p, V - f), 6: (-p, V - f)}

    def D(i, j, k):
        (xi, yi), (xj, yj), (xk, yk) = POS[i], POS[j], POS[k]
        d = sp.expand(xi * (yj - yk) + xj * (yk - yi) + xk * (yi - yj))
        assert V not in d.free_symbols
        return d
    return D


def build_J():
    D = deltas()
    rows = []
    for (i, j) in BLOCK:
        dens = set()
        for k in range(1, 7):
            if k not in (i, j):
                dens.add(rname(i, k))
                dens.add(rname(j, k))
        lcm = sp.prod([SYM[n] ** 3 for n in sorted(dens)])
        cols = {"m1": sp.Integer(0), "m2": sp.Integer(0),
                "mA": sp.Integer(0), "mB": sp.Integer(0)}
        for k in range(1, 7):
            if k in (i, j):
                continue
            sik, sjk = SYM[rname(i, k)], SYM[rname(j, k)]
            cols[MASS_CLASS[k]] += (lcm / sik**3 - lcm / sjk**3) * D(i, j, k)
        rows.append([sp.expand(cols[c]) for c in ("m1", "m2", "mA", "mB")])
    return sp.Matrix(rows)


def witness_sub():
    a1, a2, u, v, p, q = 3, -1, 2, 1, 1, -2
    vals = {"r12": a1 - a2, "wA": 2 * u, "wB": 2 * p,
            "h1": a1 - v, "e12": a1 - a2, "f": v - q}
    rads = {"d1A": u**2 + (a1 - v) ** 2, "d1B": p**2 + (a1 - q) ** 2,
            "d2A": u**2 + (a2 - v) ** 2, "d2B": p**2 + (a2 - q) ** 2,
            "cs": (u - p) ** 2 + (v - q) ** 2, "cx": (u + p) ** 2 + (v - q) ** 2}
    sub = {SYM[k]: sp.Integer(val) for k, val in vals.items()}
    sub.update({SYM[k]: sp.sqrt(val) for k, val in rads.items()})
    return sub


def singular_dim(name, eqs, cap):
    gens_syms = [SYM[g] for g in GEN_NAMES]

    def clean(e):
        pl = sp.Poly(sp.expand(e), *gens_syms)
        _, pc = pl.clear_denoms()
        return pc.as_expr()

    polys = ",\n".join(str(sp.expand(clean(e))).replace("**", "^").replace(" ", "")
                       for e in eqs)
    script = (f"ring r=0,({','.join(GEN_NAMES)}),dp;\nshort=0;\n"
              f"ideal I={polys};\nideal S=std(I);\n"
              f"string(\"SINGDIM=\",dim(S));\nideal L=lead(S);\nL;\nquit;\n")
    sf = ART / f"{name}.sing"
    sf.write_text(script, encoding="utf-8", newline="\n")
    win = str(sf).replace("\\", "/").replace("E:/", "/mnt/e/")
    wsl(f"mkdir -p {W} && cp '{win}' {W}/{name}.sing")
    t0 = time.time()
    r = wsl(f"cd {W} && timeout {cap} Singular -q {name}.sing && echo SING_OK",
            timeout=cap + 180)
    secs = time.time() - t0
    if "SING_OK" not in r.stdout or "error occurred" in r.stdout:
        return "cap-or-error", None, None, secs
    (ART / f"{name}.out").write_text(r.stdout[:2000000], encoding="utf-8")
    leads = []
    sd = None
    for line in r.stdout.splitlines():
        line = line.strip()
        if line.startswith("SINGDIM="):
            sd = int(line.split("=")[1])
        elif line.startswith("L[") and "=" in line:
            mono = line.split("=", 1)[1].replace("^", "**")
            pp = sp.Poly(sp.sympify(mono, locals=SYM), *gens_syms)
            leads.append(list(pp.monoms()[0]))
    sups = [frozenset(i for i, e in enumerate(l) if e > 0) for l in leads]
    sups = [s for s in sups if s]
    ours = None
    for size in range(len(GEN_NAMES), -1, -1):
        for S in combinations(range(len(GEN_NAMES)), size):
            if all(not sup <= set(S) for sup in sups):
                ours = size
                break
        if ours is not None:
            break
    return "ok", ours, sd, secs


def main():
    log("EXP-019 runner start")
    SH = shape_ideal()
    J = build_J()
    gens_syms = [SYM[g] for g in GEN_NAMES]

    def nterms(e):
        return len(sp.Poly(e, *gens_syms).terms()) if e != 0 else 0

    g4 = sp.expand(J[[0, 1, 2, 3], [0, 1, 2, 3]].det())
    m3 = []
    for rr in combinations(range(6), 3):
        for cc in combinations(range(4), 3):
            m = sp.expand(J[list(rr), list(cc)].det())
            if m != 0:
                m3.append((nterms(m), rr, cc, m))
    m3.sort(key=lambda x: x[0])
    picked = []
    seen_rows = set()
    for n_, rr, cc, m in m3:
        if tuple(rr) in seen_rows:
            continue
        picked.append((n_, rr, cc, m))
        seen_rows.add(tuple(rr))
        if len(picked) == 2:
            break
    (g3n, g3r, g3c, g3), (g3pn, g3pr, g3pc, g3p) = picked
    log(f"g4 terms {nterms(g4)}; g3 rows{g3r} cols{g3c} terms {g3n}; "
        f"g3' rows{g3pr} cols{g3pc} terms {g3pn}")

    wv = witness_sub()
    for nm, g in [("g4", g4), ("g3", g3), ("g3p", g3p)]:
        val = sp.radsimp(g.subs(wv, simultaneous=True))
        if sp.simplify(val) == 0:
            record(f"smoke-{nm}-nonzero-at-W1", "FAIL", "vanishes at the rank-4 witness: bug")
            return 1
    record("smoke-minors-nonzero-at-W1", "pass", "all three chosen minors nonzero at W1")

    st, ours, sd, secs = singular_dim("p1-sh-g4", SH + [g4], CAP)
    if st == "ok":
        record("p1-k4-cut", "decided" if ours == sd else "ENGINE-DISAGREEMENT",
               f"{secs:.0f}s; dim={sd} (ours {ours}); k=4 {'CLOSED' if sd is not None and sd <= 3 else 'NOT closed (component finding!)' }")
    else:
        record("p1-k4-cut", "inconclusive-cap", f"{secs:.0f}s")

    st, ours, sd, secs = singular_dim("p2-sh-g3", SH + [g3], CAP)
    if st == "ok":
        record("p2-first-3x3-cut", "decided" if ours == sd else "ENGINE-DISAGREEMENT",
               f"{secs:.0f}s; dim={sd} (ours {ours})")
        if sd is not None and sd <= 3:
            st2, ours2, sd2, secs2 = singular_dim("p3-sh-g3-g3p", SH + [g3, g3p], CAP)
            if st2 == "ok":
                record("p3-k3-cut", "decided" if ours2 == sd2 else "ENGINE-DISAGREEMENT",
                       f"{secs2:.0f}s; dim={sd2} (ours {ours2}); k=3 {'CLOSED' if sd2 is not None and sd2 <= 2 else 'NOT closed'}")
            else:
                record("p3-k3-cut", "inconclusive-cap", f"{secs2:.0f}s")
    else:
        record("p2-first-3x3-cut", "inconclusive-cap", f"{secs:.0f}s")

    log("runner done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
