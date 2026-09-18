"""EXP-017b: loci bounds in the s-variable model (no clearing, bilinear
entries). Smokes: dim 4 in the enlarged ring; entrywise agreement with
EXP-016 at W1. Then the four bound rungs at 600 s / 120 s fallback."""
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
W = "/root/exp017b"
RESULTS = {}

DNAMES = ["r12", "d1A", "d1B", "d2A", "d2B", "wA", "wB", "cs", "cx"]
HNAMES = ["h1", "e12", "f"]
MASS_CLASS = {1: "m1", 2: "m2", 3: "mA", 4: "mA", 5: "mB", 6: "mB"}
BLOCK = [(1, 3), (1, 5), (2, 3), (2, 5), (3, 5), (3, 6)]
PAIR2NAME = {(1, 2): "r12", (1, 3): "d1A", (1, 4): "d1A", (1, 5): "d1B",
             (1, 6): "d1B", (2, 3): "d2A", (2, 4): "d2A", (2, 5): "d2B",
             (2, 6): "d2B", (3, 4): "wA", (5, 6): "wB", (3, 5): "cs",
             (4, 6): "cs", (3, 6): "cx", (4, 5): "cx"}


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


def enumerate_svars():
    """Distinct unordered name pairs (a, b), a < b lexicographically, with
    s_{ab} standing for a^-3 - b^-3."""
    pairs = set()
    for (i, j) in BLOCK:
        for k in range(1, 7):
            if k in (i, j):
                continue
            a, b = rname(i, k), rname(j, k)
            if a != b:
                pairs.add(tuple(sorted((a, b))))
    return sorted(pairs)


SPAIRS = enumerate_svars()
SNAMES = [f"s_{a}_{b}" for a, b in SPAIRS]
GEN_NAMES = DNAMES + HNAMES + SNAMES + ["t"]
SYM = {n: sp.Symbol(n) for n in GEN_NAMES}


def svar(a, b):
    """s for a^-3 - b^-3 with sign handling."""
    if a == b:
        return sp.Integer(0)
    if (a, b) in [tuple(p) for p in SPAIRS]:
        return SYM[f"s_{a}_{b}"]
    return -SYM[f"s_{b}_{a}"]


def shape_ideal_s():
    r12, d1A, d1B, d2A, d2B, wA, wB, cs, cx = (SYM[n] for n in DNAMES)
    h1, e12, f = (SYM[n] for n in HNAMES)
    t = SYM["t"]
    SH = [4 * h1**2 - (4 * d1A**2 - wA**2),
          e12**2 - r12**2,
          4 * f**2 - (4 * cs**2 - (wA - wB) ** 2),
          4 * (h1 - e12) ** 2 - (4 * d2A**2 - wA**2),
          4 * (h1 + f) ** 2 - (4 * d1B**2 - wB**2),
          4 * (h1 - e12 + f) ** 2 - (4 * d2B**2 - wB**2),
          cx**2 - cs**2 - wA * wB,
          r12 - 1]
    for (a, b) in SPAIRS:
        A, B = SYM[a], SYM[b]
        SH.append(SYM[f"s_{a}_{b}"] * A**3 * B**3 - (B**3 - A**3))
    sat = t * sp.prod([SYM[n] for n in DNAMES]) * f - 1
    return [sp.expand(e) for e in SH] + [sat]


def deltas_heights():
    V = sp.Symbol("Vdummy")
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


def build_J_s():
    """Entries bilinear in (s, heights); scaled by 2 to clear the /2 widths."""
    D = deltas_heights()
    rows = []
    for (i, j) in BLOCK:
        cols = {"m1": sp.Integer(0), "m2": sp.Integer(0),
                "mA": sp.Integer(0), "mB": sp.Integer(0)}
        for k in range(1, 7):
            if k in (i, j):
                continue
            cols[MASS_CLASS[k]] += svar(rname(i, k), rname(j, k)) * D(i, j, k)
        rows.append([sp.expand(2 * cols[c]) for c in ("m1", "m2", "mA", "mB")])
    return sp.Matrix(rows)


def witness_values():
    a1, a2, u, v, p, q = 3, -1, 2, 1, 1, -2
    base = {
        "r12": sp.Integer(a1 - a2),
        "d1A": sp.sqrt(u**2 + (a1 - v) ** 2), "d1B": sp.sqrt(p**2 + (a1 - q) ** 2),
        "d2A": sp.sqrt(u**2 + (a2 - v) ** 2), "d2B": sp.sqrt(p**2 + (a2 - q) ** 2),
        "wA": sp.Integer(2 * u), "wB": sp.Integer(2 * p),
        "cs": sp.sqrt((u - p) ** 2 + (v - q) ** 2),
        "cx": sp.sqrt((u + p) ** 2 + (v - q) ** 2),
        "h1": sp.Integer(a1 - v), "e12": sp.Integer(a1 - a2), "f": sp.Integer(v - q),
    }
    sub = {SYM[k]: val for k, val in base.items()}
    for (a, b) in SPAIRS:
        sub[SYM[f"s_{a}_{b}"]] = base[a] ** -3 - base[b] ** -3
    return sub


def smoke_p0b(Js):
    sys.path.insert(0, str(HERE.parents[1] / "code"))
    sys.path.insert(0, str(HERE.parent / "EXP-016-stratum22-rank-analysis"))
    from run import mass_matrix_at  # noqa: E402
    J16, _ = mass_matrix_at((3, -1, 2, 1, 1, -2))
    wv = witness_values()
    ok = True
    for e in range(6):
        for c in range(4):
            ours = sp.radsimp(Js[e, c].subs(wv, simultaneous=True))
            ref = sp.radsimp(2 * J16[e, c])
            if sp.simplify(ours - ref) != 0:
                ok = False
                log(f"  P0b mismatch row {e} col {c}")
    return ok


def singular_dim(name, eqs, cap):
    gens = [SYM[g] for g in GEN_NAMES]

    def clean(e):
        p = sp.Poly(sp.expand(e), *gens)
        _, pc = p.clear_denoms()
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
            timeout=cap + 120)
    secs = time.time() - t0
    bad = "error occurred" in r.stdout or r.stdout.strip().startswith("?")
    if "SING_OK" not in r.stdout or bad:
        return "cap-or-error", None, None, secs, []
    (ART / f"{name}.out").write_text(r.stdout[:2000000], encoding="utf-8")
    leads = []
    singdim = None
    for line in r.stdout.splitlines():
        line = line.strip()
        if line.startswith("SINGDIM="):
            singdim = int(line.split("=")[1])
        elif line.startswith("L[") and "=" in line:
            mono = line.split("=", 1)[1].replace("^", "**")
            pp = sp.Poly(sp.sympify(mono, locals=SYM), *[SYM[g] for g in GEN_NAMES])
            leads.append(list(pp.monoms()[0]))
    return "ok", staircase(leads), singdim, secs, leads


def staircase(leads):
    sups = [frozenset(i for i, e in enumerate(l) if e > 0) for l in leads]
    sups = [s for s in sups if s]
    n = len(GEN_NAMES)
    for size in range(n, -1, -1):
        for S in combinations(range(n), size):
            Sset = set(S)
            if all(not sup <= Sset for sup in sups):
                return size
    return -1


def bound_rung(tag, SHs, minors, threshold, cap_full=600, cap_sub=120):
    st, ours, sd, secs, _ = singular_dim(f"{tag}-full", SHs + minors, cap_full)
    if st == "ok":
        agree = ours == sd
        met = sd is not None and sd <= threshold
        record(tag, "decided" if agree else "ENGINE-DISAGREEMENT",
               f"FULL {secs:.0f}s; dim={sd} (ours {ours}); threshold {threshold}; "
               f"bound {'MET' if met else 'NOT MET'}")
        return
    log(f"  {tag}: full capped ({secs:.0f}s); pgb over {len(minors)} minors")
    union, done = [], 0
    for idx, mnr in enumerate(minors):
        st, _, _, secs, leads = singular_dim(f"{tag}-sub{idx}", SHs + [mnr], cap_sub)
        if st == "ok":
            done += 1
            union.extend(leads)
    if union:
        dedup = [list(x) for x in {tuple(l) for l in union}]
        d = staircase(dedup)
        met = d <= threshold
        record(tag, "decided-pgb",
               f"fallback {done}/{len(minors)}; union bound {d}; threshold "
               f"{threshold}; bound {'MET' if met else 'NOT MET (pgb may be weak)'}")
    else:
        record(tag, "inconclusive-cap", f"full and all {len(minors)} subideals capped")


def main():
    log(f"EXP-017b runner start; {len(SPAIRS)} s-variables: {SNAMES}")
    SHs = shape_ideal_s()

    st, ours, sd, secs, _ = singular_dim("p0a-shape-s", SHs, 600)
    if st == "ok" and ours == sd == 4:
        record("p0a-shape-dim", "pass", f"dim=4 two-way in {secs:.0f}s")
    else:
        record("p0a-shape-dim", "FAIL-or-cap", f"st={st} ours={ours} sing={sd} {secs:.0f}s")
        return 1

    Js = build_J_s()
    if not smoke_p0b(Js):
        record("p0b-cross-validation", "FAIL", "s-model J != EXP-016 J at W1")
        return 1
    record("p0b-cross-validation", "pass", "entrywise agreement at W1 (factor 2)")

    def minors_of(size):
        out = []
        for rows in combinations(range(6), size):
            for cols in combinations(range(4), size):
                m = sp.expand(Js[list(rows), list(cols)].det())
                if m != 0:
                    out.append(m)
        return out

    for tag, size, thr in [("p1-delta4", 4, 3), ("p2-delta3", 3, 2),
                           ("p3-delta2", 2, 1)]:
        t0 = time.time()
        mm = minors_of(size)
        log(f"{size}x{size} minors: {len(mm)} nonzero in {time.time()-t0:.0f}s")
        bound_rung(tag, SHs, mm, thr)

    entries = [sp.expand(Js[e, c]) for e in range(6) for c in range(4)
               if Js[e, c] != 0]
    bound_rung("p4-delta1", SHs, entries, 0)

    log("runner done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
