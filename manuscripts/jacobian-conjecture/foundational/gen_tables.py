#!/usr/bin/env python3
"""Regenerate the numbers, tables and figure data of main.tex from the experiment artifacts.

Every generated file below is written from the stored output of an archived computation; no
number is typed by hand. The script exits nonzero when an artifact is missing or a pattern it
expects is absent.

  EXP-001 artifacts/output-2026-07-20.txt        determinant, three-point fiber, eliminant
  EXP-004 artifacts/output-2026-07-20.txt        instances, collision certificates
  EXP-006 artifacts/output-2026-07-20.txt        equivariant enumeration statistics
  EXP-007 artifacts/output-2026-07-20.txt        discriminant, escape and collision targets
  EXP-008 artifacts/output-2026-07-20.txt        degree law, fifth instance, tails
  EXP-009 artifacts/output-2026-07-20.txt        reductions modulo 13 and 101
  EXP-010 artifacts/output-2026-07-21.txt        rigidity sweeps
  EXP-011 artifacts/output-2026-07-21.txt        real census
  EXP-012 artifacts/output-{AB,C,D,E}-2026-07-21.txt and verdict.md   weighted landscape

Written files (next to main.tex): numbers.tex, tab-instances.tex, tab-collisions.tex,
tab-census.tex, tab-landscape.tex, fig-degrees.tex, fig-fiber.tex, fig-wall.tex.

Usage:
    python gen_tables.py            rewrite the generated files
    python gen_tables.py --check    exit 1 when a generated file differs from the regeneration
"""
import argparse
import glob
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROB = HERE.parents[2] / "problems" / "algebraic-geometry" / "jacobian-conjecture"
EXPS = PROB / "experiments"


def art(exp, pattern):
    """Return the text of the single artifact file matching pattern inside experiment exp."""
    hits = sorted(glob.glob(str(EXPS / f"{exp}-*" / pattern)))
    if len(hits) != 1:
        sys.exit(f"gen_tables: expected one file for {exp} {pattern}, found {hits}")
    return Path(hits[0]).read_text(encoding="utf-8")


def need(pattern, text, what, flags=0):
    m = re.search(pattern, text, flags)
    if not m:
        sys.exit(f"gen_tables: pattern for {what} not found: {pattern}")
    return m


def frac_tex(s):
    """Format a rational such as -1/15 as LaTeX."""
    s = s.strip()
    m = re.fullmatch(r"(-?)(\d+)/(\d+)", s)
    if m:
        return f"{'-' if m.group(1) else ''}\\tfrac{{{m.group(2)}}}{{{m.group(3)}}}"
    return s


def point_tex(s):
    parts = [p.strip() for p in s.strip("()").split(",")]
    return "(" + ",\\,".join(frac_tex(p) for p in parts) + ")"


def points_in(s):
    return re.findall(r"\(([^()]*)\)", s)


def poly_tex(s, var="w"):
    """Format a polynomial printed as in the artifacts, ascending in the variable."""
    s = s.replace("**", "^").replace("*", "")
    terms = {}
    for sign, coef, pw in re.findall(r"([+-]?)\s*(\d*)" + var + r"(?:\^(\d+))?", s):
        c = int(coef) if coef else 1
        terms[int(pw) if pw else 1] = -c if sign == "-" else c
    out = ""
    for pw in sorted(terms):
        c = terms[pw]
        mono = var if pw == 1 else f"{var}^{{{pw}}}"
        mag = "" if abs(c) == 1 else str(abs(c))
        if not out:
            out = ("-" if c < 0 else "") + mag + mono
        else:
            out += (" - " if c < 0 else " + ") + mag + mono
    return out


def tail_tex(s):
    s = s.strip()
    if s == "0":
        return "affine"
    return "$" + s.replace("**", "^") + "$"


# ---------------------------------------------------------------- parsing of the artifacts
def parse_instances():
    t4 = art("EXP-004", "artifacts/output-2026-07-20.txt")
    inst = {}
    cur = None
    for line in t4.splitlines():
        m = re.match(r"^(P\d)[^:]*: p = (.*), k = (\d+), q_tail = (.*)$", line)
        if m:
            cur = m.group(1)
            inst[cur] = {"p": m.group(2), "k": m.group(3), "tail": m.group(4)}
            continue
        if cur is None:
            continue
        m = re.match(r"\s*m = (-?\d+), beta = (-?\d+), predicted det = (-?\d+)", line)
        if m:
            inst[cur].update(m=m.group(1), beta=m.group(2), det=m.group(3))
        m = re.match(r"\s*component total degrees: \[(\d+), (\d+), (\d+)\]", line)
        if m:
            inst[cur]["deg"] = m.groups()
        m = re.match(r"\[PASS\] .*generic fiber degree == (\d+)", line)
        if m:
            inst[cur]["fdeg"] = m.group(1)
        m = re.match(r"\s*engineered target: (\(.*\))\s*$", line)
        if m:
            inst[cur]["target"] = m.group(1)
        m = re.match(r"\s*collision points: \[(.*)\]\s*$", line)
        if m:
            inst[cur]["pts"] = points_in(m.group(1))
    for key in ("P2", "P3", "P4", "P5"):
        for fld in ("p", "k", "det", "deg", "fdeg", "target", "pts"):
            if fld not in inst.get(key, {}):
                sys.exit(f"gen_tables: EXP-004 instance {key} lacks {fld}")
    t8 = art("EXP-008", "artifacts/output-2026-07-20.txt")
    m = need(r"the d = 5 instance \(seed (.*), k = (\d+)\)", t8, "EXP-008 seed")
    p5 = {"p": m.group(1), "k": m.group(2), "tail": "0"}
    m = need(r"m = (-?\d+), beta = (-?\d+), predicted det = (-?\d+), degrees = \[(\d+), (\d+), (\d+)\]",
             t8, "EXP-008 instance")
    p5.update(m=m.group(1), beta=m.group(2), det=m.group(3), deg=m.groups()[3:])
    p5["fdeg"] = need(r"P5d5: generic fiber degree == (\d+)", t8, "EXP-008 fiber degree").group(1)
    m = need(r"engineered target: (\(.*?\)); collision points: \[(.*)\]", t8, "EXP-008 collision")
    p5["target"], p5["pts"] = m.group(1), points_in(m.group(2))
    inst["P5d5"] = p5
    return inst


def parse_degree_law():
    t8 = art("EXP-008", "artifacts/output-2026-07-20.txt")
    law = []
    for d, a, b, c, a2, b2, c2 in re.findall(
            r"\[PASS\] d = (\d): degrees == \((\d+), (\d+), (\d+)\)  degrees = \[(\d+), (\d+), (\d+)\]", t8):
        if (a, b, c) != (a2, b2, c2):
            sys.exit("gen_tables: degree law line inconsistent")
        law.append((int(d), int(a), int(b), int(c)))
    tails = re.findall(r"q-tail v\^(\d): degrees \[(\d+), (\d+), (\d+)\] strictly", t8)
    if len(law) != 4 or len(tails) != 2:
        sys.exit("gen_tables: degree law or tail lines missing")
    return law, [(int(e), int(a), int(b), int(c)) for e, a, b, c in tails]


def parse_census():
    t11 = art("EXP-011", "artifacts/output-2026-07-21.txt")
    rows = []
    for tgt, sg, nw, esc, ng in re.findall(
            r"target \((.*?)\): D sign ([+\-0]), real W-roots (\d+) \(escapes (\d+)\), Groebner real points (\d+)",
            t11):
        rows.append((tgt, sg, int(nw), int(esc), int(ng)))
    if len(rows) != 6:
        sys.exit("gen_tables: EXP-011 expected six census rows")
    grid = need(r"on the 3x3x4 grid \((\d+) targets", t11, "grid size").group(1)
    seen = need(r"\{1: (\d+), 3: (\d+)\}", t11, "census counts")
    return rows, int(grid), (int(seen.group(1)), int(seen.group(2)))


def parse_wall():
    t7 = art("EXP-007", "artifacts/output-2026-07-20.txt")
    m = need(r"disc_w\(W\) = -16\*C\*\*2\*\((.*)\)\s*$", t7, "discriminant surface", re.M)
    expr = m.group(1)
    if not re.fullmatch(r"[0-9ABC+\-*() ]+", expr):
        sys.exit("gen_tables: unexpected characters in the discriminant surface")
    dval = int(need(r"D\(-16, -16, 1\) != 0.*D = (\d+)", t7, "D at the collision target").group(1))
    esc = need(r"exact fiber of F over \(0, 1, 1\): \[\((.*?)\)\]", t7, "escape fiber").group(1)
    return expr, dval, esc


def sigma(expr, A, B, C):
    return eval(expr, {"__builtins__": {}}, {"A": A, "B": B, "C": C})


def wall_branches(expr, c=1.0, n=240):
    """Branches A_pm(B) of Sigma(A, B, c) = 0 (quadratic in A), with the cusp B_star."""
    def coeffs(B):
        s0, s1, sm = sigma(expr, 0.0, B, c), sigma(expr, 1.0, B, c), sigma(expr, -1.0, B, c)
        c2 = (s1 + sm) / 2 - s0
        c1 = (s1 - sm) / 2
        return c2, c1, s0

    def disc(B):
        c2, c1, c0 = coeffs(B)
        return c1 * c1 - 4 * c2 * c0

    lo, hi = 0.0, 3.0
    if disc(lo) <= 0 or disc(hi) >= 0:
        sys.exit("gen_tables: cusp bracket failed")
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if disc(mid) > 0 else (lo, mid)
    bstar = lo
    return coeffs, bstar


def build_numbers(inst):
    out = []

    def mac(name, val):
        out.append(f"\\newcommand{{\\{name}}}{{{val}}}")

    t1 = art("EXP-001", "artifacts/output-2026-07-20.txt")
    mac("numDetF", need(r"det J \(expanded\) = (-?\d+)", t1, "determinant").group(1))
    t6 = art("EXP-006", "artifacts/output-2026-07-20.txt")
    for key, name in (("branches", "numBranches"), ("instances", "numEnumInst"), ("bad_residual", "numBadResidual"),
                      ("fibers_checked", "numEnumFibers")):
        mac(name, need(rf"{key}: (\d+)", t6, key).group(1))
    mac("numShapes", need(r"distinct instance shapes .*: (\d+)", t6, "shapes").group(1))
    t10 = art("EXP-010", "artifacts/output-2026-07-21.txt")
    mac("numRigCases", need(r"holds for (\d+) \(weights x exponents\) cases", t10, "rigidity cases").group(1))
    pairs = sorted(set(re.findall(r"\(w1,w2\)=\((\d+),(\d+)\)", t10)))
    mac("numWeightPairs", len(pairs))
    mac("weightPairs", ",\\ ".join(f"({a},{b})" for a, b in pairs))
    mac("numSweepDeg", need(r"\(df,dg <= (\d+)\)", t10, "bidegree bound").group(1))
    mac("numKillDeg", need(r"degrees up to (\d+)", t10, "kill factor bound").group(1))
    t11, grid, seen = parse_census()[0], parse_census()[1], parse_census()[2]
    mac("numGrid", grid)
    mac("numGridNoPlane", grid * 3 // 4)
    mac("numGridPlane", grid // 4)
    mac("numCensusOne", seen[0])
    mac("numCensusThree", seen[1])
    t7 = art("EXP-007", "artifacts/output-2026-07-20.txt")
    mac("numDcollision", need(r"D\(-16, -16, 1\) != 0.*D = (\d+)", t7, "D collision").group(1))
    t9 = art("EXP-009", "artifacts/output-2026-07-20.txt")
    mac("numDetModThirteen", need(r"det mod 13 = (\d+)", t9, "det mod 13").group(1))
    mac("numDetModHundred", need(r"det mod 101 = (\d+)", t9, "det mod 101").group(1))
    pts13 = need(r"reduced points mod 13: \[(.*?)\]; reduced target: (\(.*?\))", t9, "mod 13 points")
    p13 = points_in(pts13.group(1))
    mac("ptModThirteenA", "(" + p13[0] + ")")
    mac("ptModThirteenB", "(" + p13[1] + ")")
    mac("ptModThirteenT", pts13.group(2))
    pts101 = need(r"reduced points mod 101: \[(.*?)\]; reduced target: (\(.*?\))", t9, "mod 101 points")
    p101 = points_in(pts101.group(1))
    mac("ptModHundredA", "(" + p101[0] + ")")
    mac("ptModHundredB", "(" + p101[1] + ")")
    mac("ptModHundredT", pts101.group(2))
    ab = art("EXP-012", "artifacts/output-AB-2026-07-21.txt")
    mac("numLemmaCases", need(r"for (\d+) \(m, o\) cases", ab, "lemma cases").group(1))
    c = art("EXP-012", "artifacts/output-C-2026-07-21.txt")
    mac("numBridgeInst", need(r"fiber-tested: (\d+)", c, "bridge instances").group(1))
    d = art("EXP-012", "artifacts/output-D-2026-07-21.txt")
    mac("numRigidInst", need(r"fiber-tested: (\d+)", d, "rigid instances").group(1))
    e = art("EXP-012", "artifacts/output-E-2026-07-21.txt")
    mac("numAdmissCond", need(r"low-weight polynomiality conditions: (\d+)", e, "conditions").group(1))
    v12 = art("EXP-012", "verdict.md")
    mac("numPatterns", need(r"across\s+(\d+) sparse patterns", v12, "patterns").group(1))
    mac("numSeedDegMax", need(r"seed degree up to (\d+)", e, "seed degree bound") .group(1) if re.search(r"seed degree up to (\d+)", e) else need(r"seed degree <= (\d+)", e, "seed degree bound").group(1))
    law, tails = parse_degree_law()
    mac("numDegreeMax", max(x[0] for x in law))
    # the fifth instance
    mac("numPfiveDet", inst["P5d5"]["det"])
    expr_w, _, _ = parse_wall()
    coeffs_w, bstar_w = wall_branches(expr_w)
    c2w, c1w, c0w = coeffs_w(bstar_w)
    mac("numWallCuspA", f"{-c1w / (2 * c2w):.4f}")
    mac("numWallCuspB", f"{bstar_w:.4f}")
    return "\n".join(out) + "\n"


def build_tab_instances(inst):
    rows = [("P2", "F", "2"), ("P3", "G_3", "3"), ("P4", "G_4", "4"), ("P5d5", "G_5", "5"), ("P5", "F^{\\mathrm{tail}}", "2")]
    lines = [
        "\\begin{tabular}{llrrrccc}", "\\toprule",
        "Instance & Seed $p$ & $d$ & $k$ & Section tail & $\\det$ & Component degrees & Fiber degree \\\\",
        "\\midrule",
    ]
    for key, name, d in rows:
        r = inst[key]
        deg = "(" + ",\\,".join(r["deg"]) + ")"
        lines.append(f"${name}$ & ${poly_tex(r['p'])}$ & {d} & {r['k']} & {tail_tex(r['tail'])} & ${r['det']}$ & ${deg}$ & {r['fdeg']} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines) + "\n"


def build_tab_collisions(inst):
    rows = [("P2", "F", "2"), ("P3", "G_3", "3"), ("P4", "G_4", "4"), ("P5d5", "G_5", "5"), ("P5", "F^{\\mathrm{tail}}", "2")]
    lines = [
        "\\begin{tabular}{lcll}", "\\toprule",
        "Instance & Target $(A,B,C)$ & First preimage $(x,y,z)$ & Second preimage $(x,y,z)$ \\\\",
        "\\midrule",
    ]
    for key, name, _ in rows:
        r = inst[key]
        a, b = r["pts"]
        lines.append(f"${name}$ & ${point_tex(r['target'])}$ & ${point_tex(a)}$ & ${point_tex(b)}$ \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines) + "\n"


def build_tab_census():
    rows, grid, seen = parse_census()
    expr, dval, esc = parse_wall()
    t1 = art("EXP-001", "artifacts/output-2026-07-20.txt")
    n_pre = len(re.findall(r"\[PASS\] F\(.*\) == \(-1/4, 0, 0\)", t1))
    lines = [
        "\\begin{tabular}{lcccc}", "\\toprule",
        "Target $(A,B,C)$ & Sign of $D$ & Real roots of $W$ & Real preimages (Gr\\\"obner) & Escaping roots \\\\",
        "\\midrule",
    ]
    for tgt, sg, nw, esc_n, ng in rows:
        sign = {"+": "$+$", "-": "$-$", "0": "$0$"}[sg]
        lines.append(f"${point_tex('(' + tgt + ')')}$ & {sign} & {nw} & {ng} & {esc_n} \\\\")
    lines += [
        "\\midrule",
        f"$(0,\\,1,\\,1)$ & $0$ & n/a & 1 (rational fiber) & n/a \\\\",
        f"$(-\\tfrac14,\\,0,\\,0)$ & plane $C=0$ & n/a & {n_pre} (Gr\\\"obner fiber) & n/a \\\\",
        "\\bottomrule", "\\end{tabular}",
    ]
    return "\n".join(lines) + "\n"


def build_tab_landscape():
    ab = art("EXP-012", "artifacts/output-AB-2026-07-21.txt")
    c = art("EXP-012", "artifacts/output-C-2026-07-21.txt")
    d = art("EXP-012", "artifacts/output-D-2026-07-21.txt")
    e = art("EXP-012", "artifacts/output-E-2026-07-21.txt")
    inst_c = need(r"fiber-tested: (\d+)", c, "bridge").group(1)
    inst_d = need(r"fiber-tested: (\d+)", d, "rigid").group(1)
    cond = need(r"low-weight polynomiality conditions: (\d+)", e, "conditions").group(1)
    need(r"o = \(-2, -2, 1\) class is EMPTY", d, "empty class")
    need(r"admissibility system is EMPTY", e, "empty system")
    need(r"B: m = 4: J2 == \(-1\) c1\^4 D identically", ab, "m = 4 pairing")
    lines = [
        "\\begin{tabular}{c>{\\raggedright\\arraybackslash}p{0.17\\textwidth}>{\\raggedright\\arraybackslash}p{0.27\\textwidth}>{\\raggedright\\arraybackslash}p{0.36\\textwidth}}", "\\toprule",
        "$m$ & Output weights $o$ & Class & Outcome \\\\", "\\midrule",
        f"1 & $(-1,-1,1)$ & reduced pair is a planar Keller map & {inst_c} instances, every in-image fiber has at most one point \\\\",
        "2 & $(-2,-1,1)$ & the mechanism of Section~\\ref{sec:family} & the seed family of Table~\\ref{tab:instances} \\\\",
        "3 & $(-2,-2,1)$ & lattice-level scan & empty class (valuation argument) \\\\",
        f"3 & $(-3,-1,1)$ & lattice-level scan & {inst_d} instances, every in-image fiber has at most one point \\\\",
        f"4 & $(-3,-2,1)$ & potential form $V'=k^2p(w)+\\mu s^2$ & empty system ({cond} conditions, Gr\\\"obner basis $[1]$) \\\\",
        "\\bottomrule", "\\end{tabular}",
    ]
    return "\n".join(lines) + "\n"


def build_fig_degrees():
    law, tails = parse_degree_law()
    coords = [[], [], []]
    for d, a, b, c in law:
        for i, val in enumerate((a, b, c)):
            coords[i].append(f"({d},{val})")
    out = []
    marks = ["square*", "triangle*", "o"]
    names = ["first component", "second component", "third component"]
    for i in range(3):
        out.append(f"\\addplot+[only marks, mark={marks[i]}, mark size=2.4pt] coordinates {{{' '.join(coords[i])}}};")
        out.append(f"\\addlegendentry{{{names[i]}}}")
    out.append("\\addplot[dashed, domain=2:5, samples=2, gray] {5*x-3};")
    out.append("\\addplot[dashed, domain=2:5, samples=2, gray] {5*x-4};")
    out.append("\\addplot[dashed, domain=2:5, samples=2, gray] {4};")
    for e, a, b, c in tails:
        out.append(f"\\addplot+[only marks, mark=diamond*, mark size=3pt, black] coordinates {{(2,{a}) (2,{b}) (2,{c})}};")
        out.append(f"\\node[font=\\scriptsize, anchor=west] at (axis cs:2.08,{a}) {{tail $v^{e}$: ${a}$}};")
    return "\n".join(out) + "\n"


def build_fig_fiber():
    rows, _, _ = parse_census()
    wanted = [("-16, -16, 1", "three real roots"), ("10, 0, 1", "one real root")]
    out = []
    styles = ["solid", "dashed", "dotted"]
    for (tgt, label), st in zip(wanted, styles):
        if not any(r[0] == tgt for r in rows):
            sys.exit(f"gen_tables: target {tgt} not in the census")
        A, B, C = [float(Fraction(s.strip())) for s in tgt.split(",")]
        out.append(f"\\addplot[thick, {st}, domain=-1.6:2.0, samples=90] {{4*(x^2-x^3) - x*({B})*({C}) + ({A})*({C})^2}};")
        out.append(f"\\addlegendentry{{$({tgt.replace(' ', '')})$: {label}}}")
    expr, _, esc = parse_wall()
    out.append("\\addplot[thick, dashdotted, domain=-1.6:2.0, samples=90] {4*(x^2-x^3) - x*(1)*(1) + (0)*(1)^2};")
    out.append("\\addlegendentry{$(0,1,1)$: a double root}")
    out.append("\\addplot[black, forget plot, domain=-1.6:2.0, samples=2] {0};")
    return "\n".join(out) + "\n"


def build_fig_wall():
    expr, dval, esc = parse_wall()
    coeffs, bstar = wall_branches(expr)
    rows, _, _ = parse_census()

    def branch(bmin, n):
        up, dn = [], []
        smax = math.sqrt(bstar - bmin)
        for i in range(n + 1):
            s = smax * i / n
            B = bstar - s * s
            c2, c1, c0 = coeffs(B)
            r = math.sqrt(max(c1 * c1 - 4 * c2 * c0, 0.0))
            up.append((B, (-c1 + r) / (2 * c2)))
            dn.append((B, (-c1 - r) / (2 * c2)))
        return up, dn

    pts = []
    for tgt, sg, nw, esc_n, ng in rows:
        A, B, C = [float(Fraction(s.strip())) for s in tgt.split(",")]
        pts.append((A * C * C, B * C, sg))
    pts.append((0.0, 1.0, "0"))

    def panel(bmin, n, xlim, ylim, width, labels):
        up, dn = branch(bmin, n)
        poly = " ".join(f"({a:.5f},{b:.5f})" for b, a in dn[::-1]) + " " + \
            " ".join(f"({a:.5f},{b:.5f})" for b, a in up[1:])
        lines = [
            r"\begin{tikzpicture}\begin{axis}[width=" + width + r", height=6.6cm, xlabel={$A'$}, ylabel={$B'$},",
            f"  xmin={xlim[0]}, xmax={xlim[1]}, ymin={ylim[0]}, ymax={ylim[1]},",
            r"  tick label style={font=\scriptsize}, label style={font=\small}, clip=true]",
            r"\addplot[fill=black!10, draw=none] coordinates {" + poly + r"} -- cycle;",
            r"\addplot[thick, black] coordinates {" + " ".join(f"({a:.5f},{b:.5f})" for b, a in up) + "};",
            r"\addplot[thick, black] coordinates {" + " ".join(f"({a:.5f},{b:.5f})" for b, a in dn) + "};",
        ]
        for sg, mk, fillc in (("+", "triangle*", "black"), ("-", "square*", "white"), ("0", "star", "black")):
            sel = " ".join(f"({a:.5f},{b:.5f})" for a, b, s in pts if s == sg)
            if sel:
                lines.append(r"\addplot[only marks, mark=" + mk + r", mark size=3pt, mark options={fill=" + fillc +
                             r"}, draw=black] coordinates {" + sel + "};")
        c2k, c1k, c0k = coeffs(bstar)
        lines.append(r"\addplot[only marks, mark=x, mark size=4pt, thick, black] coordinates {" +
                     f"({-c1k / (2 * c2k):.5f},{bstar:.5f})" + "};")
        for (x, y, text) in labels:
            lines.append(r"\node[font=\scriptsize, align=center] at (axis cs:" + f"{x},{y}) {{{text}}};")
        lines.append(r"\end{axis}\end{tikzpicture}")
        return "\n".join(lines)

    glob = panel(-18.0, 260, (-50, 14), (-18, 24), r"0.52\linewidth",
                 [(-4, -8, r"3 real\\preimages"), (-33, 8, "1 real preimage")])
    zoom = panel(-0.6, 120, (-0.15, 0.55), (-0.6, 2.4), r"0.44\linewidth",
                 [(0.40, 0.3, r"1 real\\preimage"), (-0.02, 0.2, "3")])
    return glob + "\n" + r"\hfill" + "\n" + zoom + "\n"


def build_fig_window():
    t6 = art("EXP-006", "artifacts/output-2026-07-20.txt")
    v6 = art("EXP-006", "verdict.md")
    m = need(r"a in \{(\d),(\d),(\d)\}, b1 in \[(-?\d),(\d)\]", v6, "enumeration window")
    amin, amax = int(m.group(1)), int(m.group(3))
    bmin, bmax = int(m.group(4)), int(m.group(5))
    shapes = [tuple(int(c) for c in s) for s in
              re.findall(r"^\s+\((\d), (-?\d), (-?\d), (\d), (\d)\)\s*$", t6, re.M)]
    if len(shapes) != int(need(r"distinct instance shapes .*: (\d+)", t6, "shape count").group(1)):
        sys.exit("gen_tables: shape lines do not match the shape count")
    cells = " ".join(f"({a},{b})" for a in range(amin, amax + 1) for b in range(bmin, bmax + 1))
    found = " ".join(f"({a},{b1})" for a, b1, b2, df, dg in shapes)
    out = [
        r"\addplot[only marks, mark=*, mark size=1.2pt, gray] coordinates {" + cells + "};",
        r"\addplot[only marks, mark=square*, mark size=3.2pt, black] coordinates {" + found + "};",
    ]
    for a, b1, b2, df, dg in shapes:
        out.append(r"\node[font=\scriptsize, anchor=west] at (axis cs:" + f"{a + 0.08},{b1 + 0.0}) {{$(\\deg f,\\deg g)=({df},{dg})$}};")
    return "\n".join(out) + "\n"


FILES = {
    "fig-window.tex": lambda inst: build_fig_window(),
    "numbers.tex": lambda inst: build_numbers(inst),
    "tab-instances.tex": lambda inst: build_tab_instances(inst),
    "tab-collisions.tex": lambda inst: build_tab_collisions(inst),
    "tab-census.tex": lambda inst: build_tab_census(),
    "tab-landscape.tex": lambda inst: build_tab_landscape(),
    "fig-degrees.tex": lambda inst: build_fig_degrees(),
    "fig-fiber.tex": lambda inst: build_fig_fiber(),
    "fig-wall.tex": lambda inst: build_fig_wall(),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    inst = parse_instances()
    bad = []
    for name, fn in FILES.items():
        text = fn(inst)
        path = HERE / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                bad.append(name)
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
            print(f"wrote {name}")
    if bad:
        print("out of date:", ", ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
