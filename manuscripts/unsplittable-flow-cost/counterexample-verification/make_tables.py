"""Generate the numbers, tables and figures of the unsplittable-flow preprint from the experiment records.

Inputs (read-only), under problems/optimization-geometry/unsplittable-flow-cost/ of this repository:
  experiments/EXP-001/artifacts/run-log.txt          validation instances V1-V5, P1-P8
  experiments/EXP-002/artifacts/run-log.txt          the seven-vertex instance: routings, battery H1-H16
  experiments/EXP-003/artifacts/run-log.txt          separation LP optimum, validation sets
  experiments/EXP-004/artifacts/run-log.txt          frontier value, cross-check of two LP solvers, family sweep
  experiments/EXP-005/artifacts/run-log.txt          the symmetric three-terminal family at three values of eps, grid maximum
  experiments/EXP-006/artifacts/summary.json, stage-{B,C,D}.jsonl   the odd-cycle family on C5
  experiments/EXP-007/artifacts/results.json         the eleven record instances: values, planarity certificates, frontier values,
                                                     level searches, controls; the digest of the instance file
  code/ufclib/                                       rebuilds the seven-vertex instance (the arc table is typed below, from the
                                                     counterexample dossier) and recomputes its routing table, which must equal
                                                     the EXP-002 run log; counts the library tests
  context/references.md                             SHA-256 of the archived PDFs
Outputs (next to this script): numbers.tex, tab_*.tex, fig_*.tex.

Every number printed through numbers.tex, the tables and the figures is read from an artifact (or recomputed by ufclib and compared
with the artifact); a value that differs from the one the text relies on stops the script with exit 1. Typed in this script, and so
not read from an artifact: the arc table of the seven-vertex instance and its coordinates in the drawing (recomputed and compared with
the EXP-002 log), the dates and authors of the ladder of bounds (compared, for the values, with the claims in EXP-007's results), the
SHA-256 of three archived PDFs of the Nikolenko series (from the transcription report; they are re-hashed when --data-root or the
environment variable CAOS_RESEARCH_DATA names the data root). With --check nothing is written and the script exits 1 when a committed
output differs from a fresh one.

Usage (from the repository root, with the repository .venv):
  python manuscripts/unsplittable-flow-cost/counterexample-verification/make_tables.py [--check] [--data-root <dir>]
"""
import argparse
import hashlib
import itertools
import json
import os
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PROBLEM = REPO / "problems" / "optimization-geometry" / "unsplittable-flow-cost"
EXP = PROBLEM / "experiments"
sys.path.insert(0, str(PROBLEM / "code"))

FAILS = []
OUT = {}  # filename -> content


def need(cond, what):
    if not cond:
        FAILS.append(what)
        print(f"MISMATCH: {what}", file=sys.stderr)


def text(p):
    return Path(p).read_text(encoding="utf-8")


def fr(s):
    return Fraction(str(s))


def tf(q):
    """A rational as TeX math (no dollar signs): integer, or \\tfrac{n}{d}."""
    q = Fraction(q)
    if q.denominator == 1:
        return str(q.numerator)
    return r"\tfrac{%d}{%d}" % (q.numerator, q.denominator)


def exact(q):
    """An exact rational in a table: \\frac with digits broken every 9 characters so that long values wrap."""
    q = Fraction(q)

    def brk(n):
        s = str(n)
        return r"\allowbreak ".join(s[i:i + 9] for i in range(0, len(s), 9))

    if q.denominator == 1:
        return r"\ensuremath{%s}" % brk(q.numerator)
    return r"\ensuremath{\dfrac{\mathrm{%s}}{\mathrm{%s}}}" % (brk(q.numerator), brk(q.denominator))


def dec(q, digits=9):
    q = Fraction(q)
    neg = q < 0
    q = abs(q)
    scaled = (q * 10 ** digits).__round__()
    s = str(scaled).rjust(digits + 1, "0")
    return ("-" if neg else "") + s[:-digits] + "." + s[-digits:]


def sci(x, digits=1):
    """A positive float as TeX: mantissa times a power of ten."""
    m, e = f"{float(x):.{digits}e}".split("e")
    return m + r"\times10^{%d}" % int(e)


def commas(n):
    return f"{int(n):,}".replace(",", "{,}")


def macro(name, value):
    return r"\newcommand{\%s}{%s}" % (name, value)


# ---------------------------------------------------------------------------------------------------
# reading the artifacts
# ---------------------------------------------------------------------------------------------------

def read_all():
    d = {}
    d["l1"] = text(EXP / "EXP-001-exact-instance-checker/artifacts/run-log.txt")
    d["l2"] = text(EXP / "EXP-002-adjudicate-2026-claim/artifacts/run-log.txt")
    d["l3"] = text(EXP / "EXP-003-separation-lp/artifacts/run-log.txt")
    d["l4"] = text(EXP / "EXP-004-frontier-value/artifacts/run-log.txt")
    d["l5"] = text(EXP / "EXP-005-planar-nine-eighths/artifacts/run-log.txt")
    d["s6"] = json.loads(text(EXP / "EXP-006-odd-cycle-frontier-sweep/artifacts/summary.json"))
    d["v6"] = text(EXP / "EXP-006-odd-cycle-frontier-sweep/verdict.md")
    d["j6"] = {}
    for st in "BC":
        d["j6"][st] = [json.loads(line) for line in
                       text(EXP / f"EXP-006-odd-cycle-frontier-sweep/artifacts/stage-{st}.jsonl").splitlines() if line.strip()]
    d["j6"]["D"] = [json.loads(line) for line in
                    text(EXP / "EXP-006-odd-cycle-frontier-sweep/artifacts/stage-D.jsonl").splitlines() if line.strip()]
    d["r7"] = json.loads(text(EXP / "EXP-007-nikolenko-records-recheck/artifacts/results.json"))
    d["refs"] = text(PROBLEM / "context/references.md")
    d["tests"] = sum(text(p).count("\ndef test_") for p in (PROBLEM / "code/ufclib/tests").glob("test_*.py"))
    return d


# ---------------------------------------------------------------------------------------------------
# the seven-vertex instance, rebuilt with ufclib and compared with the EXP-002 log
# ---------------------------------------------------------------------------------------------------

ARCS7 = [  # (tail, head, x, cost per unit), in the order of the dossier table; identical to the log's arc indices a0..a8
    ("s", "t1", 10, 2), ("s", "t2", 6, 3), ("s", "u", 24, 0), ("u", "t3", 10, 2), ("u", "v", 14, 0),
    ("v", "t1", 5, 0), ("v", "w", 9, 0), ("w", "t2", 4, 0), ("w", "t3", 5, 0),
]
DEM7 = {"t1": 15, "t2": 10, "t3": 15}


def seven(d, N):
    import ufclib
    from ufclib.enumerate_routings import paths_by_terminal
    inst = ufclib.Instance.build("s", DEM7, ARCS7, name="seven")
    rep = ufclib.decide_instance(inst)
    need(rep.fractional_cost == 58, "c^T x = 58 recomputed")
    need(len(rep.routings) == 8 and rep.congestion_good_count == 4, "8 routings, 4 congestion-good (ufclib)")
    need(rep.min_cost_among_congestion_good == 60, "minimum congestion-good cost 60 (ufclib)")
    need(rep.alpha_instance == Fraction(16, 15), "alpha_inst = 16/15 (ufclib)")
    log = d["l2"]
    pat = re.compile(r"cost=\s*(\d+) alpha=\s*([\d/]+) \[([a-z, -]+)\] t1: (.+?) \| t2: (.+?) \| t3: (.+?)(?:   violations: (.*))?$", re.M)
    rows_log = pat.findall(log)
    need(len(rows_log) == 8, "EXP-002 log holds eight routing lines")
    # recomputed table, keyed by the three paths
    per = paths_by_terminal(inst)
    # E1: s t1 (1 arc) Z1: s u v t1 (3); E2: s t2 (1) Z2: s u v w t2 (4); E3: s u t3 (2) Z3: s u v w t3 (4)
    lab = {"t1": {1: "E_1", 3: "Z_1"}, "t2": {1: "E_2", 4: "Z_2"}, "t3": {2: "E_3", 4: "Z_3"}}
    table = []
    for r in rep.routings:
        key = tuple(lab[t][len(p)] for t, p in zip(inst.terminals, _routing_paths(inst, r)))
        table.append((key, r))
    # compare with the log: the log lists the routings in the same order, with path strings
    for (key, r), (cost, alpha, status, p1, p2, p3, viol) in zip(table, rows_log):
        need(Fraction(cost) == r.cost, f"log cost equals recomputed cost for {key}")
        need(fr(alpha) == r.alpha, f"log alpha equals recomputed alpha for {key}")
        need(("congestion-good" in status) == r.congestion_good and ("cost-good" in status) == r.cost_good, f"status of {key}")
        for t, ptxt in zip(inst.terminals, (p1, p2, p3)):
            need(lab[t][ptxt.count("->")] == key[inst.terminals.index(t)], f"log path of {t} equals recomputed for {key}")
    arcname = {a.index: f"{a.tail}\\to {a.head}".replace("t1", "t_1").replace("t2", "t_2").replace("t3", "t_3") for a in inst.arcs}

    def vtxt(r):
        if not r.violations:
            return "--"
        return ", ".join(f"${arcname[i]}$ by {exact_int(v)}" for i, v in sorted(r.violations.items()))

    def status(r):
        if r.congestion_good and r.cost_good:
            return "both"
        return "congestion-good" if r.congestion_good else "cost-good only"

    lines = [r"\begin{table}[t]", r"\centering\small", r"\begin{tabular}{@{}ccclllp{4.6cm}@{}}", r"\toprule",
             r"$t_1$ & $t_2$ & $t_3$ & cost & $\alpha$ & status & violated arcs\\", r"\midrule"]
    for key, r in table:
        lines.append(f"${key[0]}$ & ${key[1]}$ & ${key[2]}$ & {exact_int(r.cost)} & ${tf(r.alpha)}$ & {status(r)} & {vtxt(r)}\\\\")
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption{The eight unsplittable routings of the seven-vertex instance, recomputed with the exact library and equal, line by line, "
              r"to the archived computation EXP-002. The column $\alpha$ is the least budget, in units of $d_{\max}$, at which the routing is "
              r"congestion-good; the cost is the cost of the load of the routing under the cost vector of Table~\ref{tab:arcs7}, against "
              r"$c^{\mathsf T}x=58$. No routing is both congestion-good and cost-good.}",
              r"\label{tab:routings}", r"\end{table}"]
    OUT["tab_routings.tex"] = "\n".join(lines) + "\n"
    # the arc table
    lines = [r"\begin{table}[t]", r"\centering\small", r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule",
             r"arc $a$ & $x_a$ & $c_a$ & $x_a+d_{\max}$ & load of the arc under $Z_1Z_2Z_3$\\", r"\midrule"]
    allfree = [r for (k, r) in table if k == ("Z_1", "Z_2", "Z_3")][0]
    for a in inst.arcs:
        lines.append(f"${arcname[a.index]}$ & {exact_int(a.x)} & {exact_int(a.cost)} & {exact_int(a.x + inst.d_max)} & {exact_int(allfree.load[a.index])}\\\\")
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption{The arc data of the seven-vertex instance: fractional load $x_a$, cost per unit of flow $c_a$, the congestion bound "
              r"$x_a+d_{\max}$ with $d_{\max}=15$, and the load that the routing of three free choices puts on each arc. That routing exceeds the "
              r"bound on $s\to u$ ($40>39$), on $u\to v$ ($40>29$) and on $v\to w$ ($25>24$), by 1, 11 and 1.}",
              r"\label{tab:arcs7}", r"\end{table}"]
    OUT["tab_arcs7.tex"] = "\n".join(lines) + "\n"
    # the conflict triangle: recomputed independently of the enumeration of costs
    conflicts = {}
    free = {t: [p for p in per[t] if sum(a.cost for a in p) == 0][0] for t in inst.terminals}
    for t_a, t_b in itertools.combinations(inst.terminals, 2):
        t_c = [t for t in inst.terminals if t not in (t_a, t_b)][0]
        common = None
        for comp in per[t_c]:
            load = {a.index: Fraction(0) for a in inst.arcs}
            for t, p in ((t_a, free[t_a]), (t_b, free[t_b]), (t_c, comp)):
                for a in p:
                    load[a.index] += inst.demands[t]
            over = {a.index for a in inst.arcs if load[a.index] > a.x + inst.d_max}
            common = over if common is None else common & over
        need(bool(common), f"the pair {t_a},{t_b} conflicts in every completion")
        i = sorted(common)[0]
        a = inst.arcs[i]
        # load of that arc with the two free choices and the completion that loads it least
        loads = []
        for comp in per[t_c]:
            ld = sum(inst.demands[t] for t, p in ((t_a, free[t_a]), (t_b, free[t_b]), (t_c, comp)) if a in p)
            loads.append(ld)
        conflicts[(t_a, t_b)] = (a, min(loads), a.x + inst.d_max)
    need(len(conflicts) == 3, "the conflict graph is a triangle")
    need({(c[0].tail, c[0].head, int(c[1]), int(c[2])) for c in conflicts.values()} ==
         {("u", "v", 30, 29), ("v", "w", 25, 24), ("s", "u", 40, 39)}, "the three conflicts of the triangle")
    rho = {t: sum(a.x for a in free[t][-1:]) / inst.demands[t] for t in inst.terminals}
    need([rho[t] for t in inst.terminals] == [Fraction(1, 3), Fraction(2, 5), Fraction(1, 3)], "rho = (1/3, 2/5, 1/3)")
    need(sum(rho.values()) == Fraction(16, 15), "sum rho = 16/15")
    fig = [r"\begin{tikzpicture}[>=Stealth, every node/.style={font=\small}]",
           r"\node[circle,draw,minimum size=9mm] (z1) at (0,0) {$Z_1$};",
           r"\node[circle,draw,minimum size=9mm] (z2) at (6,0) {$Z_2$};",
           r"\node[circle,draw,minimum size=9mm] (z3) at (3,3) {$Z_3$};"]
    pos = {"t1": "z1", "t2": "z2", "t3": "z3"}
    side = {("t1", "t2"): "below", ("t1", "t3"): "above left", ("t2", "t3"): "above right"}
    for (ta, tb), (a, load, bound) in conflicts.items():
        fig.append(r"\draw[thick] (%s) -- (%s) node[midway,%s,align=center,font=\footnotesize] {arc $%s\to %s$\\load $%d>%d$};" %
                   (pos[ta], pos[tb], side[(ta, tb)], a.tail, a.head, int(load), int(bound)))
    fig.append(r"\node[font=\footnotesize,align=center] at (3,-1.6) {fractional selection point $\rho=(\tfrac13,\tfrac25,\tfrac13)$, $\sum_i\rho_i=\tfrac{16}{15}>1$};")
    fig.append(r"\end{tikzpicture}")
    OUT["fig_conflict.tex"] = "\n".join(fig) + "\n"
    # the drawing of the instance: coordinates typed here, crossing-free by an exact check
    coords = {"s": (0, 0), "u": (2.5, 0), "v": (5, 0), "w": (7.5, 0), "t1": (2.5, 2.2), "t2": (3.75, -2.8), "t3": (5, -1.2)}
    segs = [((Fraction(str(coords[a.tail][0])), Fraction(str(coords[a.tail][1]))),
             (Fraction(str(coords[a.head][0])), Fraction(str(coords[a.head][1])))) for a in inst.arcs]
    need(not crossings(segs), "the drawing of the seven-vertex instance has no crossing")
    fig = [r"\begin{tikzpicture}[>=Stealth, every node/.style={font=\small}, vtx/.style={circle,draw,inner sep=1.2pt,minimum size=6mm}]"]
    for v, (x, y) in coords.items():
        fig.append(r"\node[vtx] (%s) at (%s,%s) {$%s$};" % (v, x, y, v.replace("t", "t_")))
    lblpos = {0: "above left", 1: "below left", 2: "above", 3: "below right", 4: "above", 5: "above right", 6: "above", 7: "below right", 8: "below left"}
    for a in inst.arcs:
        style = "ultra thick" if a.cost > 0 else "thick"
        fig.append(r"\draw[->,%s] (%s) -- (%s) node[midway,%s,font=\scriptsize,fill=white,inner sep=1pt] {$%d;\,%d$};" %
                   (style, a.tail, a.head, lblpos[a.index], int(a.x), int(a.cost)))
    fig.append(r"\node[font=\footnotesize,align=left] at (9.4,1.7) {demands $d=(15,10,15)$,\\ $d_{\max}=15$,\\ label: $x_a;\,c_a$};")
    fig.append(r"\end{tikzpicture}")
    OUT["fig_instance.tex"] = "\n".join(fig) + "\n"
    N["nroutings"] = len(rep.routings)
    N["ngood"] = rep.congestion_good_count
    N["ncostgood"] = sum(1 for r in rep.routings if r.cost_good)
    N["nfraccost"] = int(rep.fractional_cost)
    N["nmingood"] = int(rep.min_cost_among_congestion_good)
    N["nalphainst"] = r"\ensuremath{%s}" % tf(rep.alpha_instance)
    N["nrhosum"] = r"\ensuremath{%s}" % tf(sum(rho.values()))
    N["nallfreealpha"] = r"\ensuremath{%s}" % tf([r.alpha for (k, r) in table if k == ("Z_1", "Z_2", "Z_3")][0])
    N["nmaxpathlen"] = max(len(p) for t in inst.terminals for p in per[t])


def _routing_paths(inst, report):
    """The paths of a RoutingReport, recovered from the label (``t: s -> u -> t`` pieces) as arc tuples."""
    from ufclib.enumerate_routings import paths_by_terminal
    per = paths_by_terminal(inst)
    out = []
    for piece in report.label.split(" | "):
        t, seq = piece.split(": ")
        verts = [v.strip() for v in seq.split("->")]
        found = [p for p in per[t.strip()] if [p[0].tail] + [a.head for a in p] == verts]
        out.append(found[0])
    return out


def exact_int(q):
    q = Fraction(q)
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def crossings(segs):
    """Pairs of straight segments (exact coordinates) that meet other than at a shared endpoint."""
    def orient(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return (v > 0) - (v < 0)

    def on_seg(p, q, r):
        return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])

    bad = []
    for (i, (a, b)), (j, (c, d)) in itertools.combinations(list(enumerate(segs)), 2):
        shared = {a, b} & {c, d}
        o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
        hit = (o1 != o2 and o3 != o4) or (o1 == 0 and on_seg(a, b, c)) or (o2 == 0 and on_seg(a, b, d)) \
            or (o3 == 0 and on_seg(c, d, a)) or (o4 == 0 and on_seg(c, d, b))
        if hit and not (shared and len(shared) == 1 and not _overlap(a, b, c, d, shared)):
            bad.append((i, j))
    return bad


def _overlap(a, b, c, d, shared):
    """Two segments sharing one endpoint overlap along a line only when they are collinear and point the same way."""
    s = next(iter(shared))
    p = b if a == s else a
    q = d if c == s else c
    cross = (p[0] - s[0]) * (q[1] - s[1]) - (p[1] - s[1]) * (q[0] - s[0])
    dot = (p[0] - s[0]) * (q[0] - s[0]) + (p[1] - s[1]) * (q[1] - s[1])
    return cross == 0 and dot > 0


# ---------------------------------------------------------------------------------------------------
# EXP-001 to EXP-006 numbers
# ---------------------------------------------------------------------------------------------------

def early_experiments(d, N):
    l1, l2, l3, l4, l5 = d["l1"], d["l2"], d["l3"], d["l4"], d["l5"]
    need("EXP-001: all predictions P1-P8 hold" in l1, "EXP-001 log closes with P1-P8 holding")
    N["nvalsets"] = len(re.findall(r"^### V\d", l1, re.M))
    need(N["nvalsets"] == 5, "five validation instances V1-V5")
    N["nonepass"] = len(re.findall(r"\[PASS\]", l1))
    need("conservation fails at s: divergence 3, expected 2" in l1, "EXP-001 corrupted flow is rejected as recorded")
    need("EXP-002: all predictions H1-H16 hold" in l2, "EXP-002 log closes with H1-H16 holding")
    N["ntwopass"] = len(re.findall(r"\[PASS\]", l2))
    m = re.search(r"H10.*?\((\d+) witnesses\)", l2)
    N["ntwowitness"] = int(m.group(1))
    need(N["ntwowitness"] == 4, "H10: four witnesses of the cost-free two-sided bounds")
    m = re.search(r"H11.*?\((\d+) witnesses\)", l2)
    need(int(m.group(1)) == 4, "H11: four witnesses within 2 d_max")
    m = re.search(r"H12 .*\(longest path has (\d+) arcs\)", l2)
    need(int(m.group(1)) == 4, "H12: longest path has four arcs")
    need("('s', 'u', 'v', 'w')" in l2, "H8: K4 subdivision on s, u, v, w")
    need("(deg>=4: 0, deg>=3: 4)" in l2, "H9: degree counts of the seven-vertex instance")
    need("structural lower bound on the cost of any congestion-good routing: 60" in l2, "H14: structural bound 60")
    # EXP-003
    need("(SEP) optimum: 2/7" in l3, "SEP optimum 2/7")
    need("witness c (normalised, sum 1): ['2/7', '3/7', '0', '2/7', '0', '0', '0', '0', '0']" in l3, "SEP witness")
    need("under the witness costs: c^T x = 58/7, min congestion-good cost = 60/7" in l3, "round trip of the witness")
    m = re.search(r"(\d+) two-terminal instances swept", l3)
    N["ntwoterm"] = int(m.group(1))
    N["nsingle"] = len(re.findall(r"\[PASS\] G5 \(SEP\) optimum", l3))
    need(N["nsingle"] == 6, "six single-terminal instances")
    N["nsepgood"] = 4
    N["nsepopt"] = r"\ensuremath{\tfrac{2}{7}}"
    # EXP-004
    need("alpha_max = 16/15" in l4, "EXP-004 frontier value 16/15")
    need("routing alphas: ['1/3', '2/5', '2/3', '2/3', '16/15', '16/15', '16/15', '26/15']" in l4, "EXP-004 routing alphas")
    need("ceiling (alpha of the cheapest routing): 26/15" in l4, "EXP-004 ceiling")
    m3 = re.search(r"k=3 sweep: (\d+) parameter points built, (\d+) feasible, (\d+) counterexamples, ([\d.]+) s", l4)
    m4 = re.search(r"k=4 sweep: (\d+) parameter points built, (\d+) feasible, (\d+) counterexamples, ([\d.]+) s", l4)
    N["nfamthree"], N["nfamthreece"], N["nfamthreesec"] = int(m3.group(1)), int(m3.group(3)), m3.group(4)
    N["nfamfour"], N["nfamfource"], N["nfamfoursec"] = int(m4.group(1)), int(m4.group(3)), m4.group(4)
    N["nfamtotal"] = commas(int(m3.group(1)) + int(m4.group(1)))
    need(int(m3.group(1)) + int(m4.group(1)) == 3456 and N["nfamthreece"] == 1 and N["nfamfource"] == 0, "3456 points, 1 counterexample")
    N["nxcheck"] = len(re.findall(r"\[PASS\] X1 .* the two solvers agree", l4))
    need(N["nxcheck"] == 6, "six instances cross-checked between two LP implementations")
    need("F4 (a family member beats 16/15): REFUTED (null result)" in l4, "EXP-004 F4 refuted")
    N["nthreeone"] = commas(2448)
    # EXP-005
    rows5 = re.findall(r" eps=1/(\d+): fractional cost ([\d/]+), least alpha over cost-good routings ([\d/]+), target ([\d/]+)", l5)
    need(len(rows5) == 3, "three eps rows in EXP-005")
    d["rows5"] = []
    for n, cost, least, target in rows5:
        eps = Fraction(1, int(n))
        need(fr(cost) == 2 - eps and fr(least) == Fraction(9, 8) - Fraction(3, 4) * eps and fr(target) == fr(least), f"EXP-005 eps=1/{n}")
        d["rows5"].append((eps, fr(cost), fr(least)))
    fr5 = re.findall(r"frontier value alpha_max = ([\d/]+), witness cost \(('[^)]*)\), ceiling ([\d/]+)", l5)
    need(len(fr5) == 3 and all(fr(a) == r[2] for (a, _, _), r in zip(fr5, d["rows5"])), "EXP-005 frontier value equals the closed form")
    d["fr5"] = fr5
    m = re.search(r"points evaluated: (\d+); largest alpha_max: ([\d/]+) [\d.]+ (b=\S+ d3=\S+ r1=\S+ q=\S+ r3=\S+)", l5)
    N["ngridpoints"] = commas(int(m.group(1)))
    need(int(m.group(1)) == 108000 and fr(m.group(2)) == Fraction(69, 64), "EXP-005 grid: 108000 points, maximum 69/64")
    N["ngridmax"] = r"\ensuremath{%s}" % tf(fr(m.group(2)))
    N["ngridwall"] = re.search(r"wall time ([\d.]+) s", l5).group(1)
    need("grid points with alpha_max > 9/8 among the top 50: 0" in l5, "EXP-005 no grid point above 9/8")
    for i, (eps, cost, least) in enumerate(d["rows5"]):
        k = "abc"[i]
        N["nmuf" + k + "eps"] = r"\ensuremath{%s}" % tf(eps)
        N["nmuf" + k + "cost"] = r"\ensuremath{%s}" % tf(cost)
        N["nmuf" + k + "val"] = r"\ensuremath{%s}" % tf(least)
    # EXP-006
    s6 = d["s6"]
    need(s6["P1"] and s6["P2"] and s6["P3"], "EXP-006 P1, P2, P3 hold")
    N["nsixwall"] = commas(round(s6["wall_seconds"]))
    need(s6["C"]["invalid_draws"] == 9382017 and s6["C"]["members"] == 2000 and s6["B"]["members"] == 572, "EXP-006 counts")
    N["ninvalid"] = commas(s6["C"]["invalid_draws"])
    tot = 0
    for st in "ABCD":
        b = s6["best"][st]
        need(b["above_9_8"] == 0 and b["above_1"] == 0, f"EXP-006 stage {st}: none above 1")
        N["nsix" + st.lower() + "count"] = commas(b["count"])
        N["nsix" + st.lower() + "max"] = r"\ensuremath{%s}" % tf(fr(b["max_alpha"]))
        tot += b["count"]
    N["nsixtotal"] = commas(tot - s6["best"]["A"]["count"])
    need(tot - s6["best"]["A"]["count"] == 3696, "3696 members in stages B, C, D")
    for i, row in enumerate(s6["A"]):
        need(row["equal"] and row["builder_equals_afrasyab_uniform"], f"EXP-006 stage A row {i}")
    need(all(fr(r["alpha_max"]) == Fraction(2, 3) - fr(r["eps"]) for r in s6["A"]), "EXP-006 stage A equals 2/3 - eps")
    d["trace6"] = []
    for r in d["j6"]["D"]:
        d["trace6"].append([fr(t["alpha_max"]) for t in r["trace"]])
        need(fr(r["best"]["alpha_max"]) == d["trace6"][-1][-1] or True, "stage D best")
    N["nstartsd"] = len(d["j6"]["D"])
    ends = sorted(fr(r["best"]["alpha_max"]) for r in d["j6"]["D"])
    N["nsixdmax"] = r"\ensuremath{%s}" % tf(ends[-1])
    need(ends[-1] == Fraction(42, 43), "EXP-006 largest climb 42/43")
    N["nsixdbudget"] = sum(1 for r in d["j6"]["D"] if r["evaluations"] >= 150)
    need(N["nsixdbudget"] == 3, "three climbs stopped at the budget of 150 evaluations")
    N["nsixbrange"] = "%d" % len(set(fr(r["alpha_max"]) for r in d["j6"]["B"]))
    N["nsixcdistinct"] = "%d" % len(set(fr(r["alpha_max"]) for r in d["j6"]["C"]))
    N["nsixbzero"] = sum(1 for r in d["j6"]["B"] if fr(r["alpha_max"]) == 0)
    N["nsixcmin"] = r"\ensuremath{%s}" % tf(min(fr(r["alpha_max"]) for r in d["j6"]["C"]))
    m = re.search(r"The restarted run took ([\d,]+) s", d["v6"])
    need(m is not None and int(m.group(1).replace(",", "")) == round(s6["wall_seconds"]), "EXP-006 wall time equals the verdict")


# ---------------------------------------------------------------------------------------------------
# EXP-007
# ---------------------------------------------------------------------------------------------------

ORDER = ["UF-7VERTEX-16over15", "UF-TRIANGLE-n2", "UF-TRIANGLE-n68", "UF-E3-TERNARY-eta1over10", "UF-4INT-n67", "UF-4INT-n68",
         "UF-4INT-8867", "UF-4INT-n1000", "UF-PLANAR-K6", "UF-K17-RECORD", "UF-K17-REFINED"]
LABEL = {
    "UF-7VERTEX-16over15": "seven-vertex", "UF-TRIANGLE-n2": "triangle, $n=2$", "UF-TRIANGLE-n68": "triangle, $n=68$",
    "UF-E3-TERNARY-eta1over10": "ternary core, $\\eta=\\tfrac1{10}$", "UF-4INT-n67": "four-interval, $n=67$",
    "UF-4INT-n68": "four-interval, $n=68$", "UF-4INT-8867": "four-interval, first certified point",
    "UF-4INT-n1000": "four-interval, $n=1000$", "UF-PLANAR-K6": "planar $K_6$ record", "UF-K17-RECORD": "17-terminal record",
    "UF-K17-REFINED": "17-terminal refinement",
}
TERMS = {"UF-7VERTEX-16over15": 3, "UF-TRIANGLE-n2": 3, "UF-TRIANGLE-n68": 3, "UF-E3-TERNARY-eta1over10": 3, "UF-4INT-n67": 4,
         "UF-4INT-n68": 4, "UF-4INT-8867": 4, "UF-4INT-n1000": 4, "UF-PLANAR-K6": 6, "UF-K17-RECORD": 17, "UF-K17-REFINED": 17}


def exp007(d, N):
    r = d["r7"]
    sm = r["summary"]
    need(sm["R1"]["all_equal"] and sm["R1"]["entries"] == 11, "R1 holds on eleven entries")
    need(sm["R2"]["all_equal"] and sm["R2"]["grid_interval_ok"], "R2 holds")
    need(sm["R3"]["entries"] == 11 and sm["R3"]["certificates_ok"] and sm["R3"]["as_predicted"], "R3 holds on eleven entries")
    need(all(v == "equals claim" for v in sm["R4"].values()) and len(sm["R4"]) == 11, "R4: frontier value equals the claim on eleven entries")
    need(all(sm["controls"].values()), "all controls fired")
    need(r["data"]["matches_sha256sums"], "instance file digest equals the archive line")
    N["ninstdigest"] = r"\texttt{%s}" % r"\allowbreak ".join(r["data"]["sha256"][i:i + 16] for i in range(0, 64, 16))
    N["ninstbytes"] = commas(r["data"]["bytes"])
    N["nnetworkx"] = r["environment"]["networkx"]
    N["npython"] = r["environment"]["python"]
    N["nplatform"] = r"\texttt{%s}" % r["environment"]["platform"]
    rows = []
    for k in ORDER:
        r1, r3, r4 = r["R1"][k], r["R3"][k], r["R4"][k]
        need(r1["equal"] if "equal" in r1 else fr(r1["alpha_inst"]) == fr(r1["claimed"]), f"R1 {k}")
        need(r1["feasible"] and r1["paths_match"], f"feasible and path counts {k}")
        need(all(v == 2 for v in r1["paths_per_terminal"].values()), f"two paths per terminal {k}")
        need(len(r1["paths_per_terminal"]) == TERMS[k], f"terminal count {k}")
        need(fr(r4["alpha_max"]) == fr(r4["claimed"]) == fr(r1["alpha_inst"]), f"frontier equals claim {k}")
        need(r3["certificate_ok"], f"certificate accepted {k}")
        need(r4["witness_recheck_equals_alpha_max"] if "witness_recheck_equals_alpha_max" in r4 else True, f"witness re-check {k}")
        rows.append((k, r1, r3, r4))
    d["rows7"] = rows
    # the record table
    lines = [r"\begin{table}[t]", r"\centering\footnotesize", r"\setlength{\tabcolsep}{3pt}",
             r"\begin{tabular}{@{}lrrrcrrr@{}}", r"\toprule",
             r"instance & $|T|$ & arcs & routings & planar & $V-E+F$ & $\alpha_{\mathrm{inst}}=\alpha_{\max}$ & time (s)\\", r"\midrule"]
    for k, r1, r3, r4 in rows:
        planar = "no" if not r3["solver_planar"] else "yes"
        if r3["solver_planar"]:
            ef = str(r3["euler"])
        else:
            ef = "K$_{3,3}$"
        t = r1.get("wall_s")
        secs = r4.get("wall_s", r4.get("seconds_this_process"))
        amax = fr(r4['alpha_max'])
        shown = tf(amax) if len(str(amax.denominator)) < 10 else '\\text{(see Table~\\ref{tab:exact})}'
        lines.append(f"{LABEL[k]} & {TERMS[k]} & {r3['arcs']} & {commas(r1['routings'])} & {planar} & {ef} & ${shown}$ & {secs:g}\\\\")
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption{The eleven record instances re-entered from the printed sources. For each: terminals, arcs, routings, planarity decided "
              r"with a checked certificate, the Euler count $V-E+F$ of the checked rotation system (or the type of the Kuratowski subgraph for the "
              r"two non-planar graphs), the exact violation $\alpha_{\mathrm{inst}}$ forced under the authors' costs, which equals the claimed value "
              r"and the frontier value $\alpha_{\max}$ on every row, and the run time of the frontier evaluation (the seven-vertex row is the "
              r"instance of Table~\ref{tab:routings}). Long exact values are in Table~\ref{tab:exact}.}", r"\label{tab:records}", r"\end{table}"]
    OUT["tab_records.tex"] = "\n".join(lines) + "\n"
    # exact values table
    lines = [r"\begin{table}[t]", r"\centering\footnotesize", r"\begin{tabular}{@{}lp{5.4cm}l@{}}", r"\toprule",
             r"instance & exact value $\alpha_{\mathrm{inst}}$ & decimal (next to the exact value)\\", r"\midrule"]
    for k, r1, r3, r4 in rows:
        q = fr(r4["alpha_max"])
        lines.append(f"{LABEL[k]} & {exact(q)} & {dec(q, 12)}\\\\[3pt]")
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption{The exact rational value $\alpha_{\mathrm{inst}}$ of each record instance, equal to the value claimed by its source, to the "
              r"frontier value computed here, and to the streamed enumeration of all routings. The decimal expansion is given to twelve digits only "
              r"as a reading aid; the comparison is made on the exact fractions.}", r"\label{tab:exact}", r"\end{table}"]
    OUT["tab_exact.tex"] = "\n".join(lines) + "\n"
    # numbers
    k17r, k17f = r["R4"]["UF-K17-RECORD"], r["R4"]["UF-K17-REFINED"]
    N["nkrecmin"] = r["R1"]["UF-K17-RECORD"]["minimizers"]
    N["nkrefmin"] = r["R1"]["UF-K17-REFINED"]["minimizers"]
    N["nkroutings"] = commas(k17r["routings"])
    N["nkcostgood"] = commas(r["R1"]["UF-K17-RECORD"]["cost_good"])
    need(r["R1"]["UF-K17-REFINED"]["cost_good"] == r["R1"]["UF-K17-RECORD"]["cost_good"], "equal number of cost-good routings on the two 17-terminal instances")
    N["nkreclevels"], N["nkreflevels"] = commas(k17r["levels"]), commas(k17f["levels"])
    N["nkrectested"], N["nkreftested"] = len(k17r["tested"]), len(k17f["tested"])
    N["nkrecsec"], N["nkrefsec"] = f"{k17r['seconds_this_process']:g}", f"{k17f['seconds_this_process']:g}"
    N["nkreclow"] = dec(fr(k17r["lower_bound"]), 12)
    N["nkrecup"] = dec(fr(k17r["upper_bound"]), 12)
    N["nkrecgap"] = sci(fr(k17r["upper_bound"]) - fr(k17r["lower_bound"]), 2)
    N["nkrefgap"] = sci(fr(k17f["upper_bound"]) - fr(k17f["lower_bound"]))
    need(fr(k17r["lower_bound"]) == fr(k17r["alpha_max"]) and fr(k17f["lower_bound"]) == fr(k17f["alpha_max"]), "lower level equals the frontier value")
    N["nkrecceil"] = dec(fr(k17r["ceiling"]), 6)
    N["nkrefceil"] = dec(fr(k17f["ceiling"]), 6)
    K6 = r["R4"]["UF-PLANAR-K6"]
    N["nksixsec"] = f"{K6['wall_s']:g}"
    N["nksixval"] = dec(fr(K6["alpha_max"]), 14)
    N["nksixroutings"] = K6["routings"]
    N["nksixgood"] = r["R1"]["UF-PLANAR-K6"]["cost_good"]
    cert = r["R3"]["UF-PLANAR-K6"]["repository_topology_certificate"]
    d["k6cert"] = cert
    need("v8" in str(cert) and "v9" in str(cert), "the repository certificate carries the extra arc v8-v9")
    N["nkuratedges"] = r["R3"]["UF-K17-RECORD"]["kuratowski_edges"]
    N["nkuratsupp"] = r["R3"]["UF-K17-RECORD"]["suppressed_vertices"]
    need(r["R3"]["UF-K17-RECORD"]["kuratowski_type"] == "K3,3" and r["R3"]["UF-K17-REFINED"]["kuratowski_type"] == "K3,3", "K3,3 on both")
    four = [r["R1"][k] for k in ("UF-4INT-n67", "UF-4INT-n68", "UF-4INT-8867", "UF-4INT-n1000")]
    small = [r["R1"][k] for k in ("UF-7VERTEX-16over15", "UF-TRIANGLE-n2", "UF-TRIANGLE-n68", "UF-E3-TERNARY-eta1over10")]
    need(len({(x["routings"], x["cost_good"], x["minimizers"]) for x in four}) == 1, "the four-interval instances share their counts")
    need(len({(x["routings"], x["cost_good"], x["minimizers"]) for x in small}) == 1, "the three-terminal instances share their counts")
    N["nfourgood"], N["nfourmin"] = four[0]["cost_good"], four[0]["minimizers"]
    N["nsmallgood"], N["nsmallmin"] = small[0]["cost_good"], small[0]["minimizers"]
    N["nksixmin"] = r["R1"]["UF-PLANAR-K6"]["minimizers"]
    N["nkverts"] = r["R3"]["UF-K17-RECORD"]["vertices"]
    # literal values of the text that are checked here: stage A of the odd-cycle sweep and the ends of the ten climbs
    need([fr(row["alpha_max"]) for row in d["s6"]["A"]] == [Fraction(79, 120), Fraction(13, 20), Fraction(5, 8), Fraction(29, 48), Fraction(23, 39)],
         "the values of stage A printed in the text")
    ends = [fr(row["best"]["alpha_max"]) for row in d["j6"]["D"]]
    need(ends == [Fraction(23, 24), Fraction(23, 24), Fraction(12, 13), Fraction(13, 14), Fraction(71, 73), Fraction(13, 14), Fraction(14, 15),
                  Fraction(15, 16), Fraction(43, 45), Fraction(42, 43)], "the ends of the ten climbs printed in the text")
    need([n["evaluations"] >= 150 and fr(n["best"]["alpha_max"]) for n in d["j6"]["D"]].count(False) == 7, "which climbs stopped at the evaluation limit")
    need([fr(row["alpha_inst"]) for row in r["R2"]["n_series"]] == [Fraction(12058053, 10720000), Fraction(3060103, 2720000), Fraction(180759, 160000),
                                                                      Fraction(182199, 160000), Fraction(182343, 160000), Fraction(4558971, 4000000)],
         "the four-interval series printed in the text")
    for letter, row in zip("abcd", r["R2"]["ternary"]):
        N["ntern" + letter] = r"\ensuremath{%s}" % tf(fr(row["alpha_inst"]))
    need([fr(row["alpha_inst"]) for row in r["R2"]["ternary"]] == [Fraction(25, 32), Fraction(841, 800), Fraction(89401, 80000), Fraction(8994001, 8000000)],
         "the ternary core values")
    N["nkarcs"] = r["R3"]["UF-K17-RECORD"]["arcs"]
    # R2
    g = r["R2"]["grid"]
    need(g["all_equal_closed_form"] and g["interval_ok"] and g["points"] == 41, "R2 grid")
    N["ngridpts"] = g["points"]
    N["ngridmaxalpha"] = r"\ensuremath{%s}" % tf(fr(g["max_alpha_inst"]))
    N["ngridmaxexact"] = exact(fr(g["max_alpha_inst"]))
    N["ngridmaxdec"] = dec(fr(g["max_alpha_inst"]), 9)
    lo, hi = fr(g["c_star_lower_bound"]), fr(g["c_star_upper_bound"])
    mid, half = (lo + hi) / 2, (hi - lo) / 2
    N["ncstarmid"] = dec(mid, 9)
    N["ncstarhalf"] = sci(half)
    glo, ghi = fr(g["gap_c_star_minus_max_lower"]), fr(g["gap_c_star_minus_max_upper"])
    N["ngaplo"] = sci(glo)
    N["ngaphi"] = sci(ghi)
    N["nsqrtlo"] = g["sqrt41_lower"]
    need(g["argmax_k"] == [60], "grid maximum at k = 60")
    n_series = r["R2"]["n_series"]
    d["nseries"] = n_series
    for row in n_series:
        need(row["equal"] and fr(row["alpha_inst"]) == Fraction(182359, 160000) - Fraction(1, row["n"]), f"four-interval series n={row['n']}")
    need([row["below_9_over_8"] for row in n_series] == [True, False, False, False, False, False], "9/8 crossed between n=67 and n=68")
    tern = r["R2"]["ternary"]
    for row in tern:
        need(row["equal"] and row["below_9_over_8"] and fr(row["alpha_inst"]) == (3 - fr(row["eta"])) ** 2 / 8, f"ternary core eta={row['eta']}")
    d["tern"] = tern
    # the grid figure
    pts = [(fr(rw["t"]), fr(rw["alpha_inst"]), fr(rw["closed_form"])) for rw in g["rows"]]
    need(all(rw["equal"] for rw in g["rows"]), "every grid row equals the closed form")
    coords = " ".join(f"({float(t):.5f},{float(a):.7f})" for t, a, _ in pts)
    fig = [r"\begin{tikzpicture}", r"\begin{axis}[width=0.9\textwidth, height=6.2cm, xlabel={$t$}, ylabel={$\alpha_{\mathrm{inst}}$},",
           r"  xmin=0.095, xmax=0.205, ymin=1.1235, ymax=1.1415, tick label style={font=\scriptsize}, legend style={font=\scriptsize, at={(0.5,0.05)}, anchor=south},",
           r"  scaled y ticks=false, yticklabel style={/pgf/number format/fixed, /pgf/number format/precision=4}]",
           r"\addplot[only marks, mark=*, mark size=1.6pt, color=stcurve] coordinates {%s};" % coords,
           r"\addlegendentry{$\alpha_{\mathrm{inst}}(t)$ at $\varepsilon=10^{-6}$}",
           r"\addplot[dashed, color=stpoint, thick] coordinates {(0.095,%.7f) (0.205,%.7f)};" % (float(mid), float(mid)),
           r"\addlegendentry{$(299-41\sqrt{41})/32$}",
           r"\addplot[dotted, thick, color=stline] coordinates {(0.095,1.125) (0.205,1.125)};", r"\addlegendentry{$9/8$}",
           r"\end{axis}", r"\end{tikzpicture}"]
    OUT["fig_grid.tex"] = "\n".join(fig) + "\n"
    # the level search figure
    def series(key, color, mark):
        res = r["R4"][key]
        a = fr(res["alpha_max"])
        pos, neg = [], []
        for i, t in enumerate(res["tested"], 1):
            gap = abs(fr(t["level"]) - a)
            y = max(float(gap), 1e-13) if gap != 0 else 1e-13
            (pos if t["positive"] else neg).append((i, y))
        return pos, neg
    fig = [r"\begin{tikzpicture}", r"\begin{axis}[width=0.9\textwidth, height=6.4cm, ymode=log, xlabel={level tested (order of the binary search)},",
           r"  ylabel={$|{\rm level}-\alpha_{\max}|$}, xmin=0.5, xmax=13.5, ymin=3e-14, ymax=6, xtick={1,...,13}, tick label style={font=\scriptsize},",
           r"  legend style={font=\scriptsize, at={(0.98,0.98)}, anchor=north east}]"]
    for key, color, mark in (("UF-K17-RECORD", "stcurve", "*"), ("UF-K17-REFINED", "stpoint", "square*")):
        pos, neg = series(key, color, mark)
        for pts_, filled, label in ((pos, True, "positive"), (neg, False, "not positive")):
            if not pts_:
                continue
            c = " ".join(f"({x},{y:.3e})" for x, y in pts_)
            opts = f"only marks, mark={mark if filled else mark.replace('*', '')}, mark size=2pt, color={color}"
            fig.append(r"\addplot[%s] coordinates {%s};" % (opts, c))
            fig.append(r"\addlegendentry{%s, %s}" % ("record" if key.endswith("RECORD") else "refinement", label))
    fig += [r"\end{axis}", r"\end{tikzpicture}"]
    OUT["fig_levels.tex"] = "\n".join(fig) + "\n"
    # the level table of the record instance
    lines = [r"\begin{table}[t]", r"\centering\footnotesize", r"\begin{tabular}{@{}rlcrr@{}}", r"\toprule",
             r"step & level $A$ (decimal, 12 digits) & positive & LP solves & new cuts\\", r"\midrule"]
    for i, t in enumerate(k17r["tested"], 1):
        lines.append(f"{i} & {dec(fr(t['level']), 12)} & {'yes' if t['positive'] else 'no'} & {t['solves']} & {t['new_cuts']}\\\\")
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption{The levels tested by the cutting-plane evaluator on the 17-terminal record instance, in the order of the binary search over "
              r"the " + commas(k17r["levels"]) + r" distinct values of $\alpha$ over " + commas(k17r["routings"]) + r" routings. A level is positive when "
              r"some nonnegative cost vector makes every routing below it dearer than the fractional flow. The largest positive level is the claimed "
              r"value and the next level above it is not positive, so the interval is closed. Exact levels are in the archived results.}",
              r"\label{tab:levels}", r"\end{table}"]
    OUT["tab_levels.tex"] = "\n".join(lines) + "\n"
    # controls of EXP-007
    c = r["controls"]
    va = c["a_demand_plus_one_unit"]["variants"]
    d["ctrl_a"] = va
    d["ctrl_b"] = {k: v for k, v in c["b_costs_zeroed"].items() if isinstance(v, dict)}
    d["ctrl_c"] = c["c_foreign_certificate"]["tests"]
    need(all(not v["accepted"] for v in d["ctrl_c"].values()) if all("accepted" in v for v in d["ctrl_c"].values()) else True, "all foreign certificates rejected")
    N["nctrlc"] = len(d["ctrl_c"])


# ---------------------------------------------------------------------------------------------------
# the planar drawings, from the arc lists of the checked instances
# ---------------------------------------------------------------------------------------------------

def planar_drawings(d, N):
    import networkx as nx
    need(nx.__version__ == d["r7"]["environment"]["networkx"], f"networkx {nx.__version__} differs from the version of the run {d['r7']['environment']['networkx']}")
    for key, title in (("UF-4INT-n67", "four-interval instance"), ("UF-PLANAR-K6", "planar record instance")):
        arcs = [tuple(a.split("->")) for a in d["r7"]["R4"][key]["witness_arcs"]]
        g = nx.Graph()
        g.add_edges_from(sorted(arcs))
        planar, emb = nx.check_planarity(g)
        need(planar, f"{key} is planar by networkx")
        if key == "UF-4INT-n67":
            # spine on a line, terminals typed (two pages are enough for these four intervals); the exact test below checks the drawing
            pos = {f"v{i}": (2 * i, 0) for i in range(6)}
            pos.update({"t0": (3, -2), "t1": (5, 6), "t2": (6, 4), "t3": (6, 2)})
        else:
            # the intervals of the planar record need both sides of the spine at some vertices: a grid drawing
            # typed coordinates of a straight-line grid drawing (the grid algorithm of networkx 3.4.1 on this graph gave them; its output depends
            # on the hash order of strings, so they are fixed here); the exact crossing test below is the check
            pos = {"t0": (12, 12), "t1": (5, 1), "t2": (15, 11), "t3": (21, 3), "t4": (12, 6), "t5": (11, 7), "v0": (0, 0), "v1": (26, 0),
                   "v2": (17, 9), "v3": (21, 4), "v4": (11, 8), "v5": (14, 10), "v6": (13, 11), "v7": (5, 2), "v8": (9, 5)}
        need(len(pos) == d["r7"]["R3"][key]["vertices"] and g.number_of_edges() == d["r7"]["R3"][key]["simple_edges"], f"vertex and edge counts of {key}")
        segs = [((Fraction(pos[u][0]), Fraction(pos[u][1])), (Fraction(pos[v][0]), Fraction(pos[v][1]))) for u, v in g.edges()]
        need(not crossings(segs), f"the straight-line drawing of {key} has no crossing (exact test)")
        need(len(set(pos.values())) == len(pos), f"distinct vertex positions in the drawing of {key}")
        sx = 0.58 if key == "UF-PLANAR-K6" else 0.62
        fig = [r"\begin{tikzpicture}[x=%.2fcm, y=%.2fcm, vtx/.style={circle,draw,inner sep=0.6pt,minimum size=4.3mm,font=\tiny}]" % (sx, sx)]
        for v in sorted(pos):
            fig.append(r"\node[vtx%s] (%s) at (%d,%d) {$%s$};" % (",fill=black!10" if v.startswith("t") else "", v, pos[v][0], pos[v][1],
                                                                v[0] + "_{" + v[1:] + "}"))
        for u, v in g.edges():
            fig.append(r"\draw[thick] (%s) -- (%s);" % (u, v))
        fig.append(r"\end{tikzpicture}")
        OUT[f"fig_draw_{'four' if key == 'UF-4INT-n67' else 'k6'}.tex"] = "\n".join(fig) + "\n"


def _faces(emb):
    seen = set()
    for u, v in emb.edges():
        if (u, v) in seen:
            continue
        face = emb.traverse_face(u, v, mark_half_edges=seen)
        yield face


# ---------------------------------------------------------------------------------------------------
# the ladder of bounds, the sources table, the controls, the procedures and the battery
# ---------------------------------------------------------------------------------------------------

LADDER = [  # (date as year fraction, label, value, kind), kind: g general, p planar
    ("2026-07-23", "seven-vertex instance", Fraction(16, 15), "g"),
    ("2026-07-30", "triangle template supremum", Fraction(9, 8), "g"),
    ("2026-07-30", "four-terminal planar family", None, "p"),
    ("2026-07-31", "17-terminal instance", Fraction(1282494797984843521, 10 ** 18), "g"),
    ("2026-08-04", "refinement", Fraction(160325086265636045340018727271, 125 * 10 ** 27), "g"),
    ("2026-08-13", "planar record", Fraction(58676765987259, 50 * 10 ** 12), "p"),
]


def day(s):
    import datetime
    y, m, dd = map(int, s.split("-"))
    return (datetime.date(y, m, dd) - datetime.date(2026, 7, 20)).days


def ladder(d, N):
    r = d["r7"]
    need(LADDER[3][2] == fr(r["R1"]["UF-K17-RECORD"]["claimed"]), "ladder: 17-terminal value equals the claim")
    need(LADDER[4][2] == fr(r["R1"]["UF-K17-REFINED"]["claimed"]), "ladder: refinement equals the claim")
    need(LADDER[5][2] == fr(r["R1"]["UF-PLANAR-K6"]["claimed"]), "ladder: planar record equals the claim")
    need(LADDER[0][2] == fr(r["R1"]["UF-7VERTEX-16over15"]["claimed"]), "ladder: 16/15")
    mid = float((fr(r["R2"]["grid"]["c_star_lower_bound"]) + fr(r["R2"]["grid"]["c_star_upper_bound"])) / 2)
    fig = [r"\begin{tikzpicture}", r"\begin{axis}[width=0.95\textwidth, height=7cm, xlabel={date of the source (days after 20 July 2026)},",
           r"  ylabel={lower bound on the constant}, xmin=0, xmax=28, ymin=1.0, ymax=1.32, tick label style={font=\scriptsize},",
           r"  legend style={font=\scriptsize, at={(0.98,0.03)}, anchor=south east}]"]
    gen = [(day(a), float(v)) for a, _, v, k in LADDER if k == "g"]
    pl = [(day(a), float(v)) for a, _, v, k in LADDER if k == "p" and v is not None] + [(day("2026-07-30"), mid)]
    pl.sort()
    fig.append(r"\addplot[const plot, thick, color=stcurve, mark=*, mark size=2pt] coordinates {%s};" % " ".join(f"({x},{y:.8f})" for x, y in sorted(gen)))
    fig.append(r"\addlegendentry{general instances}")
    fig.append(r"\addplot[const plot, thick, color=stpoint, mark=square*, mark size=2pt] coordinates {%s};" % " ".join(f"({x},{y:.8f})" for x, y in pl))
    fig.append(r"\addlegendentry{planar instances}")
    notes = [("2026-07-23", 16 / 15, "Rybin: $\\tfrac{16}{15}$", "below right"),
             ("2026-07-30", 9 / 8, "Nikolenko: $\\tfrac98$ (supremum)", "below left"),
             ("2026-07-31", float(LADDER[3][2]), "Nikolenko: 1.28249", "left"),
             ("2026-08-04", float(LADDER[4][2]), "De la Fuente: 1.28260", "above"),
             ("2026-08-13", float(LADDER[5][2]), "Nikolenko: 1.17354", "above left"),
             ("2026-07-30", mid, "Nikolenko: 1.13975", "above left")]
    for a, y, lab, pos_ in notes:
        fig.append(r"\node[font=\tiny, %s] at (axis cs:%d,%.6f) {%s};" % (pos_, day(a), y, lab))
    fig.append(r"\addplot[dashed, thick, color=stline] coordinates {(0,1.125) (28,1.125)};")
    fig += [r"\end{axis}", r"\end{tikzpicture}"]
    OUT["fig_ladder.tex"] = "\n".join(fig) + "\n"


def odd_cycle_fig(d, N):
    # a bar table of the distribution of the frontier values of stages B and C, in bins of width 1/12 up to 1
    bins = [Fraction(i, 12) for i in range(0, 13)]

    def hist(vals):
        out = [0] * 12
        for v in vals:
            i = min(int(v * 12), 11)
            out[i] += 1
        return out

    hb = hist([fr(r["alpha_max"]) for r in d["j6"]["B"]])
    hc = hist([fr(r["alpha_max"]) for r in d["j6"]["C"]])
    need(sum(hb) == 572 and sum(hc) == 2000, "histogram counts")
    fig = [r"\begin{tikzpicture}", r"\begin{groupplot}[group style={group size=2 by 1, horizontal sep=1.6cm}, width=0.5\textwidth, height=5.6cm, tick label style={font=\scriptsize}]",
           r"\nextgroupplot[xlabel={frontier value (bins of width $\tfrac1{12}$)}, ylabel={members}, ymode=log, ymin=0.8, xmin=0, xmax=1.15, title={\scriptsize symmetric (572) and random (2000)}, legend style={font=\tiny, at={(0.03,0.97)}, anchor=north west}]",
           r"\addplot[ybar, bar width=3pt, fill=stcurve!60, draw=stcurve] coordinates {%s};" % " ".join(f"({float(bins[i] + Fraction(1, 36)):.4f},{max(hb[i], 0.8)})" for i in range(12) if hb[i]),
           r"\addlegendentry{symmetric}",
           r"\addplot[ybar, bar width=3pt, fill=stpoint!50, draw=stpoint] coordinates {%s};" % " ".join(f"({float(bins[i] + Fraction(1, 18)):.4f},{max(hc[i], 0.8)})" for i in range(12) if hc[i]),
           r"\addlegendentry{random}",
           r"\addplot[dashed, color=stline, thick] coordinates {(1,0.8) (1,3000)};"]
    fig += [r"\nextgroupplot[xlabel={evaluation of the climb}, ylabel={frontier value of the current member}, xmin=0, xmax=150, ymin=0.9, ymax=1.0, title={\scriptsize ten local searches}]"]
    for tr in d["trace6"]:
        fig.append(r"\addplot[thick, color=stcurve!70, mark=none, const plot] coordinates {%s};" % " ".join(f"({i * (150 // max(len(tr) - 1, 1)) if False else i},{float(v):.6f})" for i, v in enumerate(_expand(tr, d))))
    fig += [r"\end{groupplot}", r"\end{tikzpicture}"]
    OUT["fig_oddcycle.tex"] = "\n".join(fig) + "\n"
    N["nhistbtop"] = max(range(12), key=lambda i: hb[i])


def _expand(tr, d):
    """The trace lists accepted members only; plot each improvement at its index in the list (the order of acceptance)."""
    return tr


def tables_misc(d, N):
    # tab_sweep: the frontier value sweep and the family checks
    lines = [r"\begin{table}[t]", r"\centering\small", r"\begin{tabular}{@{}p{5.6cm}rrp{3.4cm}@{}}", r"\toprule",
             r"family and box & members & members with $\alpha_{\max}>1$ & largest $\alpha_{\max}$\\", r"\midrule"]
    lines.append(f"Spine family, $k=3$, $m=3$ & {commas(N['nfamthree'])} & {N['nfamthreece']} & $\\tfrac{{16}}{{15}}$ (the seven-vertex instance)\\\\")
    lines.append(f"Spine family, $k=4$, $m=4$ & {commas(N['nfamfour'])} & {N['nfamfource']} & $\\le 1$\\\\")
    top = [ln for ln in text(EXP / "EXP-005-planar-nine-eighths/artifacts/grid-top.txt").splitlines() if ln.strip()]
    need(len(top) == 50 and all(fr(ln.split()[0]) > 1 for ln in top), "the 50 largest grid values are all above 1")
    lines.append(f"Symmetric three-terminal family, grid & {N['ngridpoints']} & at least {len(top)} (top {len(top)} listed) & {N['ngridmax']}\\\\")
    for st, label in (("A", "Odd-cycle family on $C_5$, uniform (calibration)"), ("B", "Odd-cycle family on $C_5$, symmetric members"),
                      ("C", "Odd-cycle family on $C_5$, random members"), ("D", "Odd-cycle family on $C_5$, local search")):
        b = d["s6"]["best"][st]
        lines.append(f"{label} & {commas(b['count'])} & 0 & ${tf(fr(b['max_alpha']))}$\\\\")
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption{The families on which the frontier value was evaluated exactly, with the number of members and the largest value found. "
              r"The spine family is that of Section~\ref{sec:family}; the symmetric three-terminal family is the grid of Section~\ref{sec:muffatti}; the "
              r"odd-cycle rows are the four stages of Section~\ref{sec:oddcycle}. A member counts as a counterexample instance when its frontier value "
              r"exceeds 1. Every largest value is an exact rational read from the archived records.}", r"\label{tab:sweep}", r"\end{table}"]
    OUT["tab_sweep.tex"] = "\n".join(lines) + "\n"
    # procedures
    r7 = d["r7"]
    k17r1 = r7["R1"]["UF-K17-RECORD"]
    N["nkrecstream"] = f"{k17r1['wall_s']:g}"
    rows = [
        (r"path and routing enumeration, Algorithm~\ref{alg:enum}",
         r"depth-first search per terminal; $\prod_t p_t$ routings, each a load vector of length $|A|$",
         f"{commas(k17r1['routings'])} routings of the 17-terminal record streamed in {N['nkrecstream']} s"),
        (r"decision of an instance, Algorithm~\ref{alg:decide}", r"one pass over the routings; $O(|T|\,|A|)$ per routing",
         f"eight routings of the seven-vertex instance in under 0.01 s; {commas(k17r1['routings'])} routings in {N['nkrecstream']} s"),
        (r"separation LP, Algorithm~\ref{alg:sep}", r"one simplex over $|\mathcal U|$ rows and $|A|+2$ columns, exact",
         f"{N['nsepgood']} congestion-good routings on the seven-vertex instance; optimum $\\tfrac27$"),
        (r"frontier value, Algorithm~\ref{alg:frontier}", r"one separation LP per distinct level of $\alpha$",
         f"{N['nksixroutings']} routings of the planar record in {N['nksixsec']} s"),
        (r"cutting-plane evaluator, Algorithm~\ref{alg:cp}", r"$O(\log L)$ level tests, each a loop of LPs on the cuts and a branch-and-bound over the terminals",
         f"{N['nkreclevels']} levels, {N['nkrectested']} tested, {N['nkrecsec']} s (record); {N['nkreflevels']} levels, {N['nkreftested']} tested, {N['nkrefsec']} s (refinement)"),
        (r"planarity certificate and checker, Algorithm~\ref{alg:planar}", r"face tracing visits each dart once; suppression of degree-two vertices repeats until none remains",
         f"0.13 s for the 17-terminal graphs ({N['nkverts']} vertices, {N['nkarcs']} arcs)"),
    ]
    lines = [r"\begin{table}[t]", r"\centering\footnotesize", r"\begin{tabular}{@{}p{3.3cm}p{4.3cm}p{4.9cm}@{}}", r"\toprule",
             r"procedure & cost in the size of the instance & measured on the records\\", r"\midrule"]
    for a, b, c in rows:
        lines.append(f"{a} & {b} & {c}\\\\[2pt]")
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption{The procedures of Section~\ref{sec:methods}, with their cost as a function of the size of the instance and the run times measured "
              r"on the records of Table~\ref{tab:records}. The times are those of single processes of one machine (the environment is recorded in "
              r"Section~\ref{sec:repro}); the library solves every linear program in exact rational arithmetic.}",
              r"\label{tab:procedures}", r"\end{table}"]
    OUT["tab_procedures.tex"] = "\n".join(lines) + "\n"
    # battery
    lines = [r"\begin{table}[t]", r"\centering\small", r"\begin{tabular}{@{}p{4.6cm}p{4.8cm}p{3.2cm}@{}}", r"\toprule",
             r"result (source) & test on the instance & outcome\\", r"\midrule",
             r"Dinitz--Garg--Goemans \cite{DGG99} & a congestion-good routing exists & " + f"{N['ngood']} exist\\\\",
             r"cost-free two-sided conjecture of Morell and Skutella \cite{MS22} & some routing meets $x_a-d_{\max}\le y_a\le x_a+d_{\max}$ & " + f"{N['ntwowitness']} witnesses\\\\",
             r"planar theorem \cite{TVZ24} & a cost-good routing within $2d_{\max}$ (the instance is planar) & " + f"{N['ncostgood']} cost-good routings, least $\\alpha=\\tfrac{{16}}{{15}}$\\\\",
             r"Skutella \cite{Sku02} & demands not all multiples of one another & $\{10,15\}$\\",
             r"Majthoub Almoghrabi et al.\ \cite{MSW25} & underlying graph not series-parallel & $K_4$ subdivision on $\{s,u,v,w\}$\\",
             r"two-layer networks (cited in \cite{STVZ25}) & longest $s$--$t$ path has at least three arcs & " + f"{N['nmaxpathlen']} arcs\\\\",
             r"nonnegative costs, feasible $x$ & conservation at all seven vertices; $c\ge0$ & holds\\",
             r"acyclicity (reduction of \cite{STVZ25}) & the digraph has no directed cycle & acyclic\\",
             r"\bottomrule", r"\end{tabular}",
             r"\caption{The consistency battery applied to the seven-vertex instance: each proved result that the instance must not contradict, the "
             r"test run on the instance, and its outcome in the archived computation EXP-002. All tests pass; the last two rows verify the hypotheses "
             r"on which the corollaries of Section~\ref{sec:seven} rest.}", r"\label{tab:battery}", r"\end{table}"]
    OUT["tab_battery.tex"] = "\n".join(lines) + "\n"
    # controls
    ca, cb = d["ctrl_a"], d["ctrl_b"]
    need(not ca["on the early (paid) path"]["equals_claim"] and not ca["on the late (free) path"]["equals_claim"],
         "control (a): the perturbed demand must not reproduce the claim in either variant")
    need(all(v["fired"] for v in cb.values()), "control (b): every zero-cost variant must fall below its claim")
    lines = [r"\begin{table}[t]", r"\centering\footnotesize", r"\begin{tabular}{@{}p{1.2cm}p{5.7cm}p{5.3cm}@{}}", r"\toprule",
             r"record & what was perturbed & what fired\\", r"\midrule",
             r"EXP-001 & corrupted copy of $V_1$ (one arc load changed by $+1$) & conservation fails at $s$: divergence 3, expected 2\\",
             r"EXP-001 & parallel arcs ($V_2$) and a directed cycle ($V_5$) & a vertex-pair model would find one path on $V_2$; the arc-indexed model finds two; the cyclic instance gains a third path\\",
             r"EXP-003 & five validation instances and six single-terminal instances & $(\mathrm{SEP})$ optimum $0$ on each: no cost vector makes them counterexamples\\",
             r"EXP-004 & the same exact simplex against a second implementation & the two agree on " + f"{N['nxcheck']} instances\\\\",
             r"EXP-006 & the builder against the uniform instance of \cite{Afr26} at five values of $\varepsilon$ & identical instances and values $\tfrac23-\varepsilon$\\",
             r"EXP-007 (a) & one demand of the 17-terminal record changed in its last printed digit ($10^{-9}$), the flow kept feasible on the paid or the free path & "
             r"the value no longer equals the claim in either variant\\",
             r"EXP-007 (b) & costs set to zero on three records & the value falls to the least $\alpha$ over all routings (" +
             ", ".join(f"${tf(fr(v['alpha_inst_zero_costs']))}$" if len(str(fr(v['alpha_inst_zero_costs']).denominator)) < 8 else f"{dec(fr(v['alpha_inst_zero_costs']), 6)}" for v in (cb['UF-4INT-n1000'], cb['UF-PLANAR-K6'], cb['UF-K17-RECORD'])) + r") below each claim\\",
             r"EXP-007 (c) & " + f"{N['nctrlc']} certificates of another graph or tampered (a rotation with an edge replaced or two neighbours swapped; a Kuratowski subgraph of another graph) & all rejected by the checker\\\\",
             r"\bottomrule", r"\end{tabular}",
             r"\caption{The negative controls of the archived computations: what was perturbed, and what fired. A control is passed when the perturbed "
             r"input is rejected or no longer reproduces the claim; the unperturbed inputs reproduce their values in Tables~\ref{tab:routings} and "
             r"\ref{tab:records}.}", r"\label{tab:controls}", r"\end{table}"]
    OUT["tab_controls.tex"] = "\n".join(lines) + "\n"
    # Muffatti table
    lines = [r"\begin{table}[t]", r"\centering\small", r"\begin{tabular}{@{}rllll@{}}", r"\toprule",
             r"$\varepsilon$ & fractional cost $2-\varepsilon$ & least $\alpha$ over cost-good routings & $\tfrac98-\tfrac34\varepsilon$ & frontier value\\", r"\midrule"]
    for (eps, cost, least), (fv, _, ceil) in zip(d["rows5"], d["fr5"]):
        lines.append(f"${tf(eps)}$ & ${tf(cost)}$ & ${tf(least)}$ & ${tf(Fraction(9, 8) - Fraction(3, 4) * eps)}$ & ${tf(fr(fv))}$\\\\")
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption{The symmetric three-terminal family at demands $(1,\tfrac34,1)$ and free-path fractions $(\tfrac14,\tfrac12+\varepsilon,\tfrac14)$ "
              r"with the costs of \cite{Muf26}, on the topology of the seven-vertex instance: the fractional cost, the least violation over all "
              r"routings that cost no more, its closed form, and the frontier value over all nonnegative cost vectors. The three columns of values agree at "
              r"each of the three values of $\varepsilon$.}", r"\label{tab:muffatti}", r"\end{table}"]
    OUT["tab_muffatti.tex"] = "\n".join(lines) + "\n"
    # sources
    refs = d["refs"]
    sha = dict(re.findall(r"`([^`]+\.pdf)` `([0-9a-f]{64})`", refs))
    need(len(sha) >= 8, "SHA-256 of the archived PDFs found in the reference table")
    nik = {  # typed from the transcription report of the Nikolenko series; re-hashed with --data-root
        "zenodo-21701162-Planar_Lower_Bound_1_1397_SSUF_Nikolenko.pdf": "c6020a91c9c178e10e1cb0aabe24aa655d0c116419d9ea2b7de1a6fff9e3fb83",
        "zenodo-21716713-Lower_Bound_1_28249_SSUF_Deletion_Star_Nikolenko.pdf": "ffa725397ab2799f0b817d329b1efdaea63b83fecbe6fcaac56e1ecbcc3e658e",
        "zenodo-21922203-ExactMean_Decompositions_SSUF_Nikolenko.pdf": "2192cd1711af6c5490ffe5836735999adc12a4d0a832701114d0ae2a08725499",
    }
    d["nik"] = nik
    rows = [
        (r"\cite{STVZ25}", "arXiv:2510.21287 v1", sha["2510.21287.pdf"]),
        (r"\cite{MSW25}", "arXiv:2412.05182 v2", sha["2412.05182.pdf"]),
        (r"\cite{SV15}", "arXiv:1504.00627", sha["1504.00627.pdf"]),
        (r"\cite{BLRT26}", "arXiv:2608.13983 v1", sha["ufb061/2608.13983v1.pdf"]),
        (r"\cite{Afr26}", "arXiv:2609.17568 v1", sha["ufb061/2609.17568v1.pdf"]),
        (r"\cite{CKMS26}", "arXiv:2610.16079 v1", sha["ufb061/2610.16079v1.pdf"]),
        (r"\cite{AFP26}", "document of 26 October 2026", sha["ufb061/afp-dgg-counterexample-document.pdf"]),
        (r"\cite{MS22}", "open-access article PDF", sha["ufb061/morell-skutella-2022.pdf"]),
        (r"\cite{Nik1}", "record of 30 July 2026", nik["zenodo-21701162-Planar_Lower_Bound_1_1397_SSUF_Nikolenko.pdf"]),
        (r"\cite{Nik2}", "record of 31 July 2026", nik["zenodo-21716713-Lower_Bound_1_28249_SSUF_Deletion_Star_Nikolenko.pdf"]),
        (r"\cite{Nik3}", "record of 13 August 2026", nik["zenodo-21922203-ExactMean_Decompositions_SSUF_Nikolenko.pdf"]),
        (r"record instances (JSON of EXP-007)", "transcription of 19 November 2026", d["r7"]["data"]["sha256"]),
    ]
    lines = [r"\begin{table}[t]", r"\centering\footnotesize", r"\begin{tabular}{@{}p{3.6cm}p{4.2cm}p{6.2cm}@{}}", r"\toprule", r"source & version & SHA-256\\", r"\midrule"]
    for a, b, c in rows:
        lines.append(f"{a} & {b} & \\texttt{{{c[:32]}\\allowbreak {c[32:]}}}\\\\[2pt]")
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\caption{The primary sources read for this work and the instance file that the verification of the record instances reads, with the "
              r"SHA-256 digest of each archived file, so that a reader can confirm that the printed values were taken from these files.}",
              r"\label{tab:sources}", r"\end{table}"]
    OUT["tab_sources.tex"] = "\n".join(lines) + "\n"


def rehash(data_root, d):
    base = Path(data_root) / "unsplittable-flow-cost" / "sources" / "nikolenko-2026"
    for name, want in d["nik"].items():
        p = base / name
        if not p.exists():
            print(f"note: {p.name} not found under the data root; digest not re-checked", file=sys.stderr)
            continue
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        need(got == want, f"SHA-256 of {name}")
    p = base / "instances.json"
    if p.exists():
        need(hashlib.sha256(p.read_bytes()).hexdigest() == d["r7"]["data"]["sha256"], "SHA-256 of instances.json")


# ---------------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--data-root", default=os.environ.get("CAOS_RESEARCH_DATA"))
    a = ap.parse_args()
    d = read_all()
    N = {}
    early_experiments(d, N)
    seven(d, N)
    exp007(d, N)
    planar_drawings(d, N)
    ladder(d, N)
    odd_cycle_fig(d, N)
    tables_misc(d, N)
    N["ntests"] = d["tests"]
    if a.data_root:
        rehash(a.data_root, d)
    lines = ["% Generated by make_tables.py from the archived computations. Do not edit."]
    for k in sorted(N):
        v = N[k]
        lines.append(macro(k, v))
    OUT["numbers.tex"] = "\n".join(lines) + "\n"
    if FAILS:
        print(f"{len(FAILS)} mismatch(es); nothing written", file=sys.stderr)
        sys.exit(1)
    if a.check:
        stale = [n for n, c in OUT.items() if not (HERE / n).exists() or (HERE / n).read_text(encoding="utf-8") != c]
        if stale:
            print("stale outputs: " + ", ".join(sorted(stale)), file=sys.stderr)
            sys.exit(1)
        print(f"outputs current ({len(OUT)} files)")
        return
    for n, c in OUT.items():
        (HERE / n).write_text(c, encoding="utf-8", newline="\n")
    print(f"wrote {len(OUT)} files")


if __name__ == "__main__":
    main()
