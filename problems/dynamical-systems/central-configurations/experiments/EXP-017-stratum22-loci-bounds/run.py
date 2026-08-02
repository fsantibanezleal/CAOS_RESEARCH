"""EXP-017: determinantal-loci dimension bounds in the enlarged ghost-free ring.

P0a: gauged shape dimension = 4 in the new ring. P0b: the enlarged-ring mass
matrix agrees with EXP-016's coordinate-built matrix at witness W1. P1..P4:
dim(SH + minors of size s) <= s - 2 for s = 5(all-entries read as 1x1)...
precisely: 4x4 <= 3, 3x3 <= 2, 2x2 <= 1, entries <= 0. Full std at 300 s,
per-minor pgb fallback at 60 s.
"""
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
W = "/root/exp017"
RESULTS = {}

DNAMES = ["r12", "d1A", "d1B", "d2A", "d2B", "wA", "wB", "cs", "cx"]
HNAMES = ["h1", "e12", "f"]
GEN_NAMES = DNAMES + HNAMES + ["t"]
SYM = {n: sp.Symbol(n) for n in GEN_NAMES}
MASS_CLASS = {1: "m1", 2: "m2", 3: "mA", 4: "mA", 5: "mB", 6: "mB"}
BLOCK = [(1, 3), (1, 5), (2, 3), (2, 5), (3, 5), (3, 6)]
# quotient-distance name for each body pair
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


def shape_ideal():
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
    sat = t * sp.prod([SYM[n] for n in DNAMES]) * f - 1
    return [sp.expand(e) for e in SH] + [sat]


def deltas_heights():
    """Delta_ijk as polynomials in wA, wB, h1, e12, f via a cancelling dummy."""
    V = sp.Symbol("Vdummy")
    h1, e12, f = (SYM[n] for n in HNAMES)
    wA, wB = SYM["wA"], SYM["wB"]
    u, p = wA / 2, wB / 2
    POS = {1: (sp.Integer(0), h1 + V), 2: (sp.Integer(0), h1 - e12 + V),
           3: (u, V), 4: (-u, V), 5: (p, V - f), 6: (-p, V - f)}

    def D(i, j, k):
        (xi, yi), (xj, yj), (xk, yk) = POS[i], POS[j], POS[k]
        d = sp.expand(xi * (yj - yk) + xj * (yk - yi) + xk * (yi - yj))
        assert V not in d.free_symbols, f"dummy did not cancel in Delta_{i}{j}{k}"
        return d
    return D


def build_J_cleared():
    """Rows cleared by the LCM of their inverse-cube denominators."""
    D = deltas_heights()
    rows = []
    row_lcms = []
    for (i, j) in BLOCK:
        dens = set()
        for k in range(1, 7):
            if k in (i, j):
                continue
            dens.add(rname(i, k))
            dens.add(rname(j, k))
        lcm = sp.prod([SYM[n] ** 3 for n in sorted(dens)])
        row_lcms.append(lcm)
        cols = {"m1": sp.Integer(0), "m2": sp.Integer(0),
                "mA": sp.Integer(0), "mB": sp.Integer(0)}
        for k in range(1, 7):
            if k in (i, j):
                continue
            sik, sjk = SYM[rname(i, k)], SYM[rname(j, k)]
            term = (lcm / sik**3 - lcm / sjk**3) * D(i, j, k)
            cols[MASS_CLASS[k]] += term
        rows.append([sp.expand(cols[c]) for c in ("m1", "m2", "mA", "mB")])
    return sp.Matrix(rows), row_lcms


def witness_values():
    """Exact values at W1 = (a1,a2,u,v,p,q) = (3,-1,2,1,1,-2)."""
    a1, a2, u, v, p, q = 3, -1, 2, 1, 1, -2
    import math
    vals = {
        "r12": a1 - a2,
        "d1A": sp.sqrt(u**2 + (a1 - v) ** 2), "d1B": sp.sqrt(p**2 + (a1 - q) ** 2),
        "d2A": sp.sqrt(u**2 + (a2 - v) ** 2), "d2B": sp.sqrt(p**2 + (a2 - q) ** 2),
        "wA": 2 * u, "wB": 2 * p,
        "cs": sp.sqrt((u - p) ** 2 + (v - q) ** 2),
        "cx": sp.sqrt((u + p) ** 2 + (v - q) ** 2),
        "h1": a1 - v, "e12": a1 - a2, "f": v - q,
    }
    return {SYM[k]: sp.nsimplify(val) for k, val in vals.items()}


def smoke_p0b(Jc, row_lcms):
    """Compare cleared enlarged-ring rows against EXP-016's coordinate rows."""
    sys.path.insert(0, str(HERE.parents[1] / "code"))
    sys.path.insert(0, str(HERE.parent / "EXP-016-stratum22-rank-analysis"))
    from run import mass_matrix_at  # noqa: E402  (EXP-016's exact builder)
    J16, _ = mass_matrix_at((3, -1, 2, 1, 1, -2))
    wv = witness_values()
    ok = True
    for e in range(6):
        lcm_val = row_lcms[e].subs(wv, simultaneous=True)
        for c in range(4):
            ours = sp.radsimp(Jc[e, c].subs(wv, simultaneous=True))
            ref = sp.radsimp(J16[e, c] * lcm_val)
            if sp.simplify(ours - ref) != 0:
                ok = False
                log(f"  P0b mismatch at row {e} col {c}")
    return ok


def singular_dim(name, eqs, cap):
    polys = ",\n".join(str(sp.expand(e)).replace("**", "^").replace(" ", "")
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
    if "SING_OK" not in r.stdout:
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
    ours = staircase(leads)
    return "ok", ours, singdim, secs, leads


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


def bound_rung(tag, SH, minors, threshold, cap_full=300, cap_sub=60):
    st, ours, sd, secs, _ = singular_dim(f"{tag}-full", SH + minors, cap_full)
    if st == "ok":
        agree = ours == sd
        met = sd is not None and sd <= threshold
        record(f"{tag}", "decided" if agree else "ENGINE-DISAGREEMENT",
               f"FULL basis {secs:.0f}s; dim={sd} (ours {ours}); "
               f"threshold {threshold}; bound {'MET' if met else 'NOT MET'}")
        return
    log(f"  {tag}: full std capped ({secs:.0f}s); pgb fallback over {len(minors)} minors")
    union = []
    done = 0
    for idx, mnr in enumerate(minors):
        st, _, _, secs, leads = singular_dim(f"{tag}-sub{idx}", SH + [mnr], cap_sub)
        if st == "ok":
            done += 1
            union.extend(leads)
    if union:
        dedup = [list(x) for x in {tuple(l) for l in union}]
        d = staircase(dedup)
        met = d <= threshold
        record(f"{tag}", "decided-pgb",
               f"fallback: {done}/{len(minors)} subideals; union dim bound {d}; "
               f"threshold {threshold}; bound {'MET' if met else 'NOT MET (pgb may be weak)'}")
    else:
        record(f"{tag}", "inconclusive-cap", f"full and all {len(minors)} subideals capped")


def main():
    log("EXP-017 runner start")
    SH = shape_ideal()

    st, ours, sd, secs, _ = singular_dim("p0a-shape", SH, 300)
    if st == "ok" and ours == sd == 4:
        record("p0a-shape-dim", "pass", f"dim=4 two-way in {secs:.0f}s")
    else:
        record("p0a-shape-dim", "FAIL", f"st={st} ours={ours} singular={sd}")
        return 1

    t0 = time.time()
    Jc, row_lcms = build_J_cleared()
    sizes = [[len(sp.Poly(Jc[e, c], *[SYM[g] for g in GEN_NAMES]).terms())
              if Jc[e, c] != 0 else 0 for c in range(4)] for e in range(6)]
    log(f"J built in {time.time()-t0:.0f}s; entry term counts: {sizes}")
    (ART / "entry-sizes.json").write_text(json.dumps(sizes), encoding="utf-8")

    if not smoke_p0b(Jc, row_lcms):
        record("p0b-cross-validation", "FAIL", "enlarged-ring J != EXP-016 J at W1")
        return 1
    record("p0b-cross-validation", "pass", "entrywise agreement with EXP-016 at W1")

    gens = [SYM[g] for g in GEN_NAMES]

    def minors_of(size):
        out = []
        for rows in combinations(range(6), size):
            for cols in combinations(range(4), size):
                out.append(sp.expand(Jc[list(rows), list(cols)].det()))
        return [m for m in out if m != 0]

    t0 = time.time()
    m4 = minors_of(4)
    log(f"4x4 minors: {len(m4)} nonzero in {time.time()-t0:.0f}s")
    bound_rung("p1-delta4", SH, m4, 3)

    t0 = time.time()
    m3 = minors_of(3)
    log(f"3x3 minors: {len(m3)} nonzero in {time.time()-t0:.0f}s")
    bound_rung("p2-delta3", SH, m3, 2)

    t0 = time.time()
    m2 = minors_of(2)
    log(f"2x2 minors: {len(m2)} nonzero in {time.time()-t0:.0f}s")
    bound_rung("p3-delta2", SH, m2, 1)

    entries = [sp.expand(Jc[e, c]) for e in range(6) for c in range(4)
               if Jc[e, c] != 0]
    bound_rung("p4-delta1", SH, entries, 0)

    log("runner done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
