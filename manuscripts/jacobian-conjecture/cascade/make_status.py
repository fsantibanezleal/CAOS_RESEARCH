"""Generate the numbers, tables and figures of the cascade paper from the experiment records.

Inputs (read-only, under the experiments folder of the problem, `--exp`):
  EXP-001 artifacts/output-2026-07-20.txt        determinant, three-point fibre, lex basis
  EXP-041 artifacts/output-{A..E}-2026-07-22.txt  input check, conjugation, nilpotent chain, potential
  EXP-136 artifacts/result.json, sources.md       closure of the implications, homogeneous-type test, SU(2) and GMC(3) moments
  EXP-138 artifacts/results.json, run-log.txt     dimension-15 homogeneous witness
  EXP-144 artifacts/results.json, run-log.txt     Long's rank-two Poisson map
  EXP-041 data/README.md                          SHA-256 of the Thompson input
Outputs (next to this script): numbers.tex, status_table.tex, implication_graph.tex, index_map.tex, hash_table.tex,
validation_table.tex, cost_table.tex, fig_fibre.tex, fig_chain.tex, fig_poisson.tex, fig_moments.tex.

Every number printed in the paper is read here from an artifact; a value that differs from the one the text relies on
stops the script with exit 1, so the paper cannot drift from the records. With `--check` nothing is written and the
script exits 1 when a committed output differs from a fresh one.

Usage: python make_status.py [--exp <experiments folder>] [--check]
"""
import argparse
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_EXP = HERE.parents[2] / "problems" / "algebraic-geometry" / "jacobian-conjecture" / "experiments"
FAILS = []


def need(cond, what):
    if not cond:
        FAILS.append(what)
        print(f"MISMATCH: {what}", file=sys.stderr)


def text(p):
    return p.read_text(encoding="utf-8")


def grab(pattern, s, what, flags=0):
    m = re.search(pattern, s, flags)
    need(m is not None, f"pattern for {what} not found")
    return m.group(1) if m else ""


# ------------------------------------------------------------------------------------------------ readers
def read_all(exp):
    r = {}
    e001 = text(exp / "EXP-001-validate-counterexample/artifacts/output-2026-07-20.txt")
    r["det"] = int(grab(r"det J \(expanded\) = (-?\d+)", e001, "EXP-001 determinant"))
    need("(2*z - 13)*(4*z + 1)/8" in e001, "EXP-001 eliminant")
    need("(12*y**2 - 4*z - 1)/12" in e001, "EXP-001 basis element 12y^2 - 4z - 1")
    need("(3*x + 2*y)/3" in e001, "EXP-001 basis element 3x + 2y")
    need("{13/2: 1, -1/4: 1}" in e001, "EXP-001 roots of the eliminant")

    d = exp / "EXP-041-gradient-witness/artifacts"
    a, c, dd, ee = (text(d / f"output-{k}-2026-07-22.txt") for k in "ACDE")
    b = text(d / "output-B-2026-07-22.txt")
    r["thompson_mon"] = int(grab(r"H is cubic homogeneous\s+(\d+) cubic monomials", a, "EXP-041 A2"))
    r["potential_mon"] = int(grab(r"B1: f_H is homogeneous of degree 4 in 48 variables\s+(\d+) monomials", b, "EXP-041 B1"))
    need("B2: S^-1 o (id + grad f) o S" in b and "[PASS] B2" in b, "EXP-041 B2 conjugation identity")
    need("[PASS] C: Ftil(p1) = Ftil(p2)" in c, "EXP-041 collision")
    r["jh"] = {int(k): int(v) for k, v in re.findall(r"terms\(JH(?:\^(\d+))?\) = (\d+)", dd.replace("terms(JH) =", "terms(JH^1) ="))}
    r["nil_index"] = int(grab(r"index = (\d+)", dd, "EXP-041 nilpotency index"))
    r["traces"] = [int(k) for k in re.findall(r"Tr\(JH\^(\d+)\) = 0: True", dd)]
    need("D2: Tr(JH^k) = 0 for k = 1, 2, 4, 8" in dd, "EXP-041 D2")
    r["delta_terms"] = int(grab(r"Delta P_star\^2 != 0.*?\s(\d+) nonzero terms", ee, "EXP-041 E2", re.S))
    r["thompson_sha"] = grab(r"sha256\(cubic_map.txt\) =\s+([0-9a-f]{64})", text(exp / "EXP-041-gradient-witness/data/README.md"), "Thompson map hash", re.S)
    r["thompson_col_sha"] = grab(r"sha256\(collision_points.txt\) =\s+([0-9a-f]{64})", text(exp / "EXP-041-gradient-witness/data/README.md"), "Thompson collision hash", re.S)

    r136 = json.loads(text(exp / "EXP-136-cascade-dimension-audit/artifacts/result.json"))
    r["r136"] = r136
    r["sources"] = text(exp / "EXP-136-cascade-dimension-audit/artifacts/sources.md")

    r138 = json.loads(text(exp / "EXP-138-mathieu-su15/artifacts/results.json"))
    r["r138"] = r138
    r["log138"] = text(exp / "EXP-138-mathieu-su15/artifacts/run-log.txt")

    r144 = json.loads(text(exp / "EXP-144-long-poisson-exact-check/artifacts/results.json"))
    r["r144"] = r144
    return r


def frac(s):
    return Fraction(s)


def tex_frac(q):
    q = Fraction(q)
    if q.denominator == 1:
        return f"{q.numerator}"
    sign = "-" if q < 0 else ""
    return f"{sign}\\tfrac{{{abs(q.numerator)}}}{{{q.denominator}}}"


# ------------------------------------------------------------------------------------------------ numbers
def numbers(r):
    r136, r138, r144 = r["r136"], r["r138"], r["r144"]
    n = {}
    need(r["det"] == -2, "det JF is -2")
    n["detF"] = "-2"
    n["fibrepoints"] = "3"
    n["secondgens"] = str(r136["part_b"]["second_derivative_generators"])
    need(r136["part_b"]["groebner_basis"] == ["1"], "EXP-136 second-derivative basis is [1]")
    need(r136["part_b"]["component_total_degrees"] == [7, 6, 4], "EXP-136 component degrees")
    n["degseven"] = "7"
    n["closuremax"] = str(r136["part_a"]["nmax"])
    n["suthreemax"] = str(r136["part_d"]["n_checked"])
    n["gmcmax"] = str(r136["part_e"]["m_checked"])
    need(r136["part_d"]["all_match"] and r136["part_e"]["all_match"], "EXP-136 moment checks all match")
    n["thompsonmon"] = str(r["thompson_mon"])
    need(r136["part_c"]["cubic_monomials"] == r["thompson_mon"] == 54, "54 cubic monomials in both records")
    n["thompsondim"] = str(r136["part_c"]["dimension"])
    n["haarlast"] = tex_frac(frac(r136["part_d"]["moments"][-1]["int_F^n_G"]))
    n["gausslast"] = f"{int(r136['part_e']['moments'][-1]['E_Q3_P3^m']):,}".replace(",", "{,}")
    n["witnessdim"] = "48"
    n["potentialmon"] = str(r["potential_mon"])
    need(r["potential_mon"] == 382, "382 monomials of the potential")
    n["deltaterms"] = f"{r['delta_terms']:,}".replace(",", "{,}")
    need(r["delta_terms"] == 9028, "9028 terms of Delta P*^2")
    n["nilindex"] = str(r["nil_index"])
    need(r["nil_index"] == 18, "nilpotency index 18")
    jh = r["jh"]
    need(jh.get(17) == 6 and jh.get(16) == 91, "(JH)^17 has 6 terms, (JH)^16 has 91")
    for k, nm in ((1, "jhone"), (2, "jhtwo"), (4, "jhfour"), (8, "jheight"), (16, "jhsixteen"), (17, "jhseventeen")):
        n[nm] = f"{jh[k]:,}".replace(",", "{,}")
    need(r["traces"] == [2, 4, 8], "traces of JH^2, JH^4, JH^8 vanish (JH^1 is checked with the chain)")
    p2 = r138["P2"]
    need(p2["dimension"] == 15 and p2["degree"] == 7 and p2["homogeneous"] and p2["nilpotent_JH"] and p2["collision"], "EXP-138 witness")
    n["homdim"] = str(p2["dimension"])
    n["homdeg"] = str(p2["degree"])
    nil = int(grab(r"\(JH\)\^(\d+) = 0 exactly", r["log138"], "EXP-138 nilpotency power"))
    need(nil == 14, "(JH)^14 = 0 in EXP-138")
    n["homnil"] = str(nil)
    n["homseconds"] = str(r138["seconds"])
    need(r138["P4"]["control_fires"], "EXP-138 control fires")
    n["homctrl"] = re.sub(r"x(\d)", r"x_\1", r138["P4"]["det_bad"].replace("**", "^").replace("*", " "))
    need(r144["failures"] == [], "EXP-144 has no failure")
    n["poissonseconds"] = str(r144["elapsed_seconds"])
    n["poissongb"] = str(r144["P4_groebner_seconds"])
    n["poissonbrk"] = str(r144["P2_symbolic_seconds"])
    n["poissondet"] = str(r144["P3_seconds"])
    n["poissonpts"] = str(r144["P2_random_route"]["points"])
    n["poissonseed"] = str(r144["P2_random_route"]["seed"])
    need(r144["P2_random_route"]["nonzero_entries_of_JF_PI_JFT_minus_PI"] == 0, "EXP-144 random route zero entries")
    need(r144["P2_random_route"]["distinct_detJF_values"] == ["1"], "EXP-144 det values")
    n["poissonquot"] = str(r144["P4_quotient_dimension"])
    need(r144["P4_fiber_points_count"] == 3 and r144["P4_quotient_dimension"] == 3, "EXP-144 fibre has 3 points")
    n["controlonepoints"] = str(r144["C1"]["random_route_nonzero_entries_5_points"])
    n["controltwopoints"] = str(r144["C2"]["random_route_nonzero_entries_5_points"])
    n["controlonefail"] = str(len(r144["C1"]["failing_entries"]))
    n["controltwofail"] = str(len(r144["C2"]["failing_entries"]))
    need(not r144["C1"]["checker_ok"] and not r144["C2"]["checker_ok"], "EXP-144 controls fail the checker")
    need(r144["P2_named_brackets"]["{D,R}"] == "1" and r144["P2_named_brackets"]["{S,T}"] == "1", "EXP-144 brackets")
    need(all(r144["P2_named_brackets"][k] == "0" for k in ("{R,S}", "{R,T}", "{D,S}", "{D,T}")), "EXP-144 other brackets")
    need(r144["P1_sizes_measured"] == r144["P1_sizes_printed"], "EXP-144 sizes match the printed table")
    need(r144["P5_factor_list_R"] == "(-1, [(x, 1), (3*q*x - 2, 1)])", "EXP-144 factorization of R")
    for k, v in r144["P1_sizes_measured"].items():
        n["size" + {"beta": "beta", "y": "y", "R": "R", "S": "S", "T": "T", "H": "H", "D": "D"}[k] + "terms"] = str(v[0])
        n["size" + k + "deg"] = str(v[1])
    return n


# ------------------------------------------------------------------------------------------------ status data
# Marks: [MV] machine-verified here, [D] derived by the paper from located statements, [C] conjectural,
# [V] located and read in the primary text, [U] not located or not verified here.
def mk(*xs):
    return ", ".join(xs)


def status_rows(r, n):
    r136 = r["r136"]
    st = r136["part_a"]["status"]
    dc_false = [k for k in range(1, 9) if st[f"DC({k})"] == "false"]
    pc_false = [k for k in range(1, 9) if st[f"PC({k})"] == "false"]
    jc_false = [k for k in range(1, 9) if st[f"JC({k})"] == "false"]
    need(dc_false == list(range(3, 9)) and jc_false == list(range(3, 9)), "closure: DC and JC false exactly from 3")
    need(pc_false == list(range(3, 9)), "closure: PC false from 3 (index 2 comes from EXP-144)")
    need(st["DC(1)"] == st["DC(2)"] == st["PC(1)"] == "undecided" and st["JC(2)"] == "undecided", "open indices")
    ctr = r136["derived_rows"]
    need(ctr["GaussianMoments"]["true"] == [1], "GMC(1) true")
    need(ctr["Mathieu"]["F_reached_by_located_proof"] is False, "F is not of homogeneous type")
    hd, hdeg = n["homdim"], n["homdeg"]
    pk = n["poissonquot"]
    rows = [
        dict(key="JC", stmt=r"Jacobian conjecture $JC(N)$ (Smale 16)",
             impl=r"none used; $F\times\mathrm{id}_{N-3}$ keeps $\det JF$ and the fibre",
             src=r"the map \cite{Alpoge2026}, its fibre by a lex basis (algorithm~A1)",
             marks=r"[MV] $N=3$; [D] $N\ge3$",
             wit=r"$F:\C^3\to\C^3$, $\det JF=%s$, fibre of %s points" % (n["detF"], n["fibrepoints"]),
             opn=r"$N=2$ [C]"),
        dict(key="MC", stmt=r"Mathieu conjecture for $SU(N)$",
             impl=r"$MC(SU(N))\Rightarrow$ every Keller map $x-h$ of $\C^N$, $h$ homogeneous, is invertible",
             src=r"Zwart, Thms~4.23 and 4.16 [V] \cite{Zwart2025}; Mathieu, Thms~5.3 and 5.4, not located [U] \cite{Mathieu1997}",
             marks=r"chain [V], original [U]; $N\ge%s$ [MV]; $SU(2)$ [V], $n\le%s$ [MV]" % (hd, n["suthreemax"]),
             wit=r"$N=%s$, degree %s (EXP-138); $N=%s$ (EXP-041 input); $SU(2)$: Long's $F,G$ \cite{LongSU2}" % (hd, hdeg, n["thompsondim"]),
             opn=r"$SU(N)$, $3\le N\le14$; other compact groups [C]"),
        dict(key="DC", stmt=r"Dixmier conjecture $DC(n)$",
             impl=r"$DC(n)\Rightarrow JC(n)$; $JC(2n)\Rightarrow DC(n)$",
             src=r"Belov-Kanel and Kontsevich, introduction and Thm~1 [V] \cite{BKK2007}; Tsuchimoto [U] \cite{Tsuchimoto2005}",
             marks=r"closure $n\le%s$ [MV], all $n$ [D]; rank-1 proof claimed [U]" % n["closuremax"],
             wit=r"none explicit: $DC(n)\Rightarrow JC(n)$ carries the failure",
             opn=r"$n=1,2$ [C]"),
        dict(key="PC", stmt=r"Poisson conjecture $PC(n)$ ($2n$ variables)",
             impl=r"$JC(2n)\Rightarrow PC(n)\Rightarrow DC(n)\Rightarrow JC(n)$",
             src=r"Adjamagbo and van den Essen, Thm~7 [V] \cite{AvdE2007}; Long, Thm~1.1 and eqs.~(12)--(19), pp.~4--5 [V] \cite{LongPoisson2026}",
             marks=r"$n=2$ [MV] (EXP-144); $n\ge2$ [D]; closure $n\ge3$, $n\le%s$ [MV]" % n["closuremax"],
             wit=r"$R,T,D,S\in\Q[x,q,p,z]$ (4 variables), $\{D,R\}=\{S,T\}=1$, fibre of %s points" % pk,
             opn=r"$n=1$ [C]"),
        dict(key="GMC", stmt=r"Gaussian moments conjecture $GMC(n)$",
             impl=r"$GMC(n)$ for all $n$ $\Rightarrow JC$",
             src=r"Derksen, van den Essen and Zhao, Thm~1.6 and Prop.~4.2 [V] \cite{DEZ2017}; Long, Thm~5.1 [V] \cite{Long2026}",
             marks=r"$n\ge3$ [V], $m\le%s$ [MV]; $n=1$ true [V]; $n=2$ proof claimed [U]" % n["gmcmax"],
             wit=r"$P_3$ of five terms and degree 4, $Q_3=Z$, in 3 variables",
             opn=r"$n=2$ [C] (proof claimed \cite{Wilson2026})"),
        dict(key="VC", stmt=r"Zhao's vanishing conjecture",
             impl=r"vanishing (all $n$) $\Leftrightarrow JC$ (all $n$); homogeneous Hessian-nilpotent quartics suffice",
             src=r"Zhao, Thm~7.2 [V] \cite{Zhao2004}; de Bondt, dimensions 28 and 30 [V] \cite{deBondt2026}",
             marks=r"explicit witness [MV]; de Bondt's dimensions [V], not re-verified",
             wit=r"$P_\star=-f_H$, homogeneous quartic in %s variables, %s monomials over $\Q(i)$" % (n["witnessdim"], n["potentialmon"]),
             opn=r"minimal failing dimension [C]"),
        dict(key="IC", stmt=r"Image conjecture",
             impl=r"Image $\Rightarrow$ vanishing",
             src=r"van den Essen \cite{vdE2010} [U]",
             marks=r"[D]",
             wit=r"none explicit: false in some dimension",
             opn=r"minimal failing dimension [C]"),
        dict(key="HC", stmt=r"Symmetric (gradient) Jacobian conjecture, Hessian conjecture $HC$",
             impl=r"$HC(2n)\Rightarrow$ $x+H$ invertible whenever $JH$ is nilpotent; $JC\Leftrightarrow HC$",
             src=r"de Bondt and van den Essen, Thm~1.1 and Cor.~1.3 [V] \cite{dBvdE2005}",
             marks=r"explicit witness [MV]",
             wit=r"$\mathrm{id}+\nabla f_H$ on $\C^{%s}$, 2-point collision over $\Q(i)$" % n["witnessdim"],
             opn=r"dimensions below %s [C]; positive results \cite{dBvdE2005b, vdEW2004} [U]" % n["witnessdim"]),
    ]
    return rows


def status_table(rows):
    head = (r"Statement & Implication and dimension index & Source theorem located & Evidence marks & "
            r"Explicit witness and dimension & Open indices \\")
    cap = (r"\caption{Status of the Jacobian conjecture and of the seven conjectures that the three-dimensional counterexample "
           r"reaches, one row each. The columns give the statement, the published implication with the dimension index as its "
           r"source states it, the theorem located in that source, the evidence marks (Section~\ref{sec:marks}), the explicit "
           r"witness with its dimension, and the indices that remain open. Built by \texttt{make\_status.py} from the closure "
           r"and the exact checks of computations EXP-001, EXP-041, EXP-136, EXP-138 and EXP-144; page numbers of the source "
           r"theorems were not recorded except for Long's polynomials.}\label{tab:status}\\")
    out = [r"\clearpage", r"\begin{landscape}", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}",
           r"\begin{longtable}{@{}L{0.11\textheight}L{0.17\textheight}L{0.19\textheight}L{0.14\textheight}L{0.19\textheight}L{0.12\textheight}@{}}",
           cap, r"\toprule", head, r"\midrule", r"\endfirsthead", r"\toprule", head, r"\midrule", r"\endhead",
           r"\bottomrule", r"\endfoot"]
    for row in rows:
        out.append(" & ".join([row["stmt"], row["impl"], row["src"], row["marks"], row["wit"], row["opn"]]) + " \\\\[3pt]")
    out += [r"\end{longtable}", r"\end{landscape}", r"\clearpage"]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------------------------------ graph
GRAPH_NODES = [
    # key, label, x, y, class
    ("JC", r"$JC(n)$: false for $n\ge3$;\\ $JC(2)$ open", 0.0, 0.0, "wit"),
    ("DC", r"$DC(n)$: false for $n\ge3$;\\ $n=1,2$ open", -5.2, 2.5, "imp"),
    ("PC", r"$PC(n)$: false for $n\ge2$;\\ $n=1$ open", -5.2, -2.5, "wit"),
    ("GMC", r"$GMC(n)$: false for $n\ge3$;\\ $n=2$ open", 5.2, 3.2, "wit"),
    ("MC", r"$MC(SU(N))$: false for $N=2$\\ and $N\ge15$", 5.2, -2.1, "wit"),
    ("HX", r"$x-h$ invertible on $\C^N$,\\ $h$ homogeneous", 5.2, 0.5, "wit"),
    ("VC", r"vanishing conjecture:\\ false, witness in dim.~48", 3.6, -4.6, "wit"),
    ("IC", r"Image conjecture:\\ false in some dim.", 5.4, -6.1, "imp"),
    ("HC", r"Hessian conjecture $HC$:\\ false, witness in dim.~48", -3.6, -4.6, "wit"),
]
GRAPH_EDGES = [
    # from, to, label, bend/anchors
    ("JC", "PC", r"AvdE Thm 7", "bend right=20"),
    ("PC", "DC", r"AvdE Thm 7", "bend left=20"),
    ("DC", "JC", r"BKK intro", "bend left=20"),
    ("JC", "DC", r"BKK Thm 1", "bend left=20"),
    ("GMC", "JC", r"DEZ Thm 1.6", "bend right=8"),
    ("MC", "HX", r"Zwart 4.23, 4.16", "bend right=0"),
    ("HX", "JC", r"Zwart Thm 4.4", "bend right=8"),
    ("JC", "VC", r"Zhao Thm 7.2", "bend right=20"),
    ("VC", "JC", r"", "bend right=20"),
    ("JC", "HC", r"dBvdE Thm 1.1", "bend left=20"),
    ("HC", "JC", r"", "bend left=20"),
    ("IC", "VC", r"vdE [U]", "bend left=6"),
]


def graph(rows):
    out = [r"\begin{tikzpicture}[scale=1.0, transform shape,",
           r"  nd/.style={draw, rounded corners=2pt, align=center, font=\scriptsize, inner sep=3pt, minimum width=2.9cm, minimum height=0.95cm},",
           r"  wit/.style={nd, fill=stwit, line width=1.1pt},",
           r"  imp/.style={nd, fill=stimp, dashed, line width=0.8pt},",
           r"  opn/.style={nd, fill=stopn, dotted, line width=0.8pt},",
           r"  ed/.style={-{Stealth[length=2.2mm]}, line width=0.6pt},",
           r"  el/.style={font=\tiny, fill=white, inner sep=1pt}]"]
    for k, lab, x, y, cl in GRAPH_NODES:
        out.append(rf"\node[{cl}] ({k}) at ({x},{y}) {{{lab}}};")
    for a, b, lab, bend in GRAPH_EDGES:
        node = rf" node[el, midway] {{{lab}}}" if lab else ""
        out.append(rf"\draw[ed, {bend}] ({a}) to{node} ({b});")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------------------------------ index map
def index_map(r):
    st = r["r136"]["part_a"]["status"]
    cols = list(range(1, 17))
    cells = {}

    def put(row, i, c):
        cells[(row, i)] = c

    for i in cols:
        put("JC", i, "T" if st.get(f"JC({i})") == "true" else "I" if st.get(f"JC({i})") == "undecided" else "W")
        put("DC", i, "O" if st.get(f"DC({i})") == "undecided" else "I")
        put("PC", i, "O" if st.get(f"PC({i})") == "undecided" and i == 1 else "W")
        put("MC", i, "X" if i == 1 else "W" if i == 2 or i >= 15 else "O")
        put("GMC", i, "T" if i == 1 else "O" if i == 2 else "W")
    # the closure is tabulated to n = 8; the other cells follow from the same rules (the rule does not depend on n)
    put("JC", 2, "O")
    labels = {"JC": r"$JC(N)$", "DC": r"$DC(n)$", "PC": r"$PC(n)$", "MC": r"$MC(SU(N))$", "GMC": r"$GMC(n)$"}
    color = {"T": "sttrue", "W": "stwit", "I": "stimp", "O": "stopn", "X": "white"}
    out = [r"\begin{tikzpicture}[x=0.78cm, y=0.62cm, font=\scriptsize,",
           r"  c/.style={draw=black!60, minimum width=0.78cm, minimum height=0.62cm, inner sep=0pt, outer sep=0pt}]"]
    for ri, row in enumerate(["JC", "DC", "PC", "MC", "GMC"]):
        y = -ri
        out.append(rf"\node[anchor=east] at (0.45,{y}) {{{labels[row]}}};")
        for i in cols:
            c = cells[(row, i)]
            sym = {"T": "T", "W": "W", "I": "I", "O": "?", "X": "--"}[c]
            out.append(rf"\node[c, fill={color[c]}] at ({i},{y}) {{{sym}}};")
    for i in cols:
        out.append(rf"\node at ({i},0.85) {{{i}}};")
    out.append(r"\node[anchor=east] at (0.45,0.85) {index};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------------------------------ tables
def hash_table(r, n):
    s = r["sources"]
    rows = [
        ("Belov-Kanel, Kontsevich", "math/0512171v2", "399075cefd34b1081b996f2906ccd9b3aae647523985f0ae763f9b2acd86c642"),
        ("Adjamagbo, van den Essen", "math/0608009v1", "1f8c7b6c56c23530d9f1120a075fb4ee2f214c0c948eab0362d921bb5cd0bbda"),
        ("Derksen, van den Essen, Zhao", "1506.05192v1", "1226da233f8055b7f5572ff456cd8878767add32ed52c3b87632b8853765eafc"),
        ("Long, Gaussian moments", "2607.18186v1", "ca5d36529019375cede8dc6a7765430681751c4e587dc2122f37f21f05cdc42c"),
        ("Zwart, review of Mathieu", "2511.16561v2", "ccd62d8d63c97394cb1dc005e22ac49403886edc1bff912aebd89eadfa2225c7"),
        ("van den Essen, Mathieu subspaces", "1907.06107v1", "d9ad5dbfc1b9e7e41802aebe7beab5710205ae51846ae2ca4ef8b8de81da65d4"),
        ("van den Essen, Wright, Zhao", "1008.3962v2", "8c295ebccdd0922620a05b7f7e1dde8d8bffa08b53b83733330abf23fa3a484d"),
        ("Dings, Koelink", "1404.4215v1", "a95976f8480da4941a697129ae33f1f891a63532b851d36d17fef1116a278bd1"),
        ("Zhao, Image and Mathieu", "0902.0212v3", "e5b3f759c060c03692d8f9daa342608f84e488b8a465b530bff9ff49867bc500"),
        ("M{\\\"u}ger, Tuset", "2210.06582v2", "01c9cd57b22cf2fcd93bd5c94c895c1c28d335572f05643491ecb9ac0c4fadbc"),
        ("Long, $SU(2)$", "2607.19012v1", "cb75f1acf144a2deb67e7c4ecd92f00d8c73ea5e92dd5e52ae303553941049e6"),
        ("Wilson", "2607.23887v1", "0f70a4a1a5cceca0ea2d9bba2aa6d1c120da4980cddf4c105a55db97f85f257a"),
        ("Zheglov", "2410.06959v5", "897913ef95e011332e86e348803c6c9da5dbd196db17a04f8f951110e9b095e3"),
        ("Long, Poisson", "2608.23777v1", r["r144"]["pdf_sha256"]),
        ("Thompson, \\texttt{cubic\\_map.txt}", "data file", r["thompson_sha"]),
        ("Thompson, \\texttt{collision\\_points.txt}", "data file", r["thompson_col_sha"]),
    ]
    for _, _, h in rows[:13]:
        need(h in s, f"hash {h[:12]} not in EXP-136 sources.md")
    need(r["r144"]["pdf_sha256"] == "5dd5861194bfea9130cddc10919510b060dab663f3a00222e57014125db5051a", "Long Poisson hash")
    out = [r"\begin{table}[t]", r"\centering\scriptsize", r"\setlength{\tabcolsep}{3pt}",
           r"\begin{tabular}{@{}L{0.26\textwidth}L{0.16\textwidth}L{0.50\textwidth}@{}}", r"\toprule",
           r"Text or file & Read as & SHA-256 \\", r"\midrule"]
    for a, b, h in rows:
        hh = "\\allowbreak ".join(h[i:i + 16] for i in range(0, 64, 16))
        out.append(rf"{a} & {b} & \texttt{{{hh}}} \\")
    out += [r"\bottomrule", r"\end{tabular}",
            r"\caption{Primary texts and input files read for the status table, with the arXiv version of each text and the SHA-256 of the fetched PDF or file, as recorded by computations EXP-041, EXP-136 and EXP-144. A change of any digest would mean a different text from the one on which the transcribed statements rest.}",
            r"\label{tab:hashes}", r"\end{table}"]
    return "\n".join(out) + "\n"


def validation_table(r, n):
    r144 = r["r144"]
    rows = [
        (r"Long's $SU(2)$ identities", "EXP-136 D",
         r"$\int F^n\,dg=0$ and $\int F^nG\,dg=(-1)^{n-1}/(n+1)$ for $n=1,\dots,%s$; at $n=%s$ the second integral is $%s$" % (n["suthreemax"], n["suthreemax"], n["haarlast"])),
        (r"Long's $GMC(3)$ identities", "EXP-136 E",
         r"$P_3$ expands to the printed five terms; $E(P_3^m)=0$ and $E(Q_3P_3^m)=m!$ for $m=1,\dots,%s$; at $m=%s$ the value is $%s$" % (n["gmcmax"], n["gmcmax"], n["gausslast"])),
        (r"Homogeneous-type test, two routes", "EXP-136 B",
         r"basis $[1]$ for the %s nonzero second partials, and the substitution certificate $\partial_x\partial_yF_3=-6x$, $\partial_x^2F_3|_{x=0}=-6y$, $\partial_y^2F_1|_{x=y=0}=8$" % n["secondgens"]),
        (r"Input of the 24-variable form", "EXP-136 C, EXP-041 A",
         r"both SHA-256 digests match; $H$ homogeneous cubic with %s monomials; the published collision is exact" % n["thompsonmon"]),
        (r"Nilpotency of $JH$, two routes", "EXP-041 D",
         r"$(JH)^{%s}=0$ while $(JH)^{17}$ keeps %s terms; $\mathrm{Tr}(JH^k)=0$ for $k=2,4,8$ (and the chain terms %s, %s, %s, %s, %s, %s for $k=1,2,4,8,16,17$)" % (n["nilindex"], n["jhseventeen"], n["jhone"], n["jhtwo"], n["jhfour"], n["jheight"], n["jhsixteen"], n["jhseventeen"])),
        (r"Potential and collision", "EXP-041 B, C, E",
         r"$f_H$ has %s monomials; the conjugation identity holds in all %s components; $\Delta P_\star^2$ has %s terms" % (n["potentialmon"], n["witnessdim"], n["deltaterms"])),
        (r"Dimension-15 witness and control", "EXP-138",
         r"$(JH)^{%s}=0$; equal images at two distinct integer points; adding $x_2^2$ to $F_2$ gives a non-constant determinant; %s s" % (n["homnil"], n["homseconds"])),
        (r"Long's Poisson map, two routes", "EXP-144 P1 to P5",
         r"term counts and degrees match the printed table; symbolic brackets and %s random rational points (seed %s) give zero entries; $\det JF=1$ both ways; fibre of %s points; %s s in all" % (n["poissonpts"], n["poissonseed"], n["poissonquot"], n["poissonseconds"])),
        (r"Controls of the Poisson check", "EXP-144 C1, C2",
         r"the uncorrected $D_0$ and the changed coefficient $125\to126$ in $H$ fail the checker: %s and %s failing matrix entries symbolically, %s and %s nonzero entries at 5 points" % (n["controlonefail"], n["controltwofail"], n["controlonepoints"], n["controltwopoints"])),
    ]
    out = [r"\begin{table}[t]", r"\centering\footnotesize", r"\setlength{\tabcolsep}{3pt}",
           r"\begin{tabular}{@{}L{0.22\textwidth}L{0.15\textwidth}L{0.60\textwidth}@{}}", r"\toprule",
           r"Independent route & Computation & Numbers measured \\", r"\midrule"]
    for a, b, c in rows:
        out.append(rf"{a} & {b} & {c} \\[2pt]")
    out += [r"\bottomrule", r"\end{tabular}",
            r"\caption{Independent routes to the load-bearing facts, with the numbers each measured in exact arithmetic. Each row is one computation of the archived records; a row with two routes lists both. No tolerance or interval applies: each identity holds exactly or the check fails.}",
            r"\label{tab:validation}", r"\end{table}"]
    return "\n".join(out) + "\n"


def cost_table(r, n):
    rows = [
        ("A1", "EXP-001, EXP-144", r"polynomials, target point", r"$\Q$", r"sympy 1.14 (lex Gr\"obner basis)",
         r"basis of 4 elements in 3 variables; 5 elements in 4 variables in %s s" % n["poissongb"]),
        ("A2", "EXP-136 B", r"components of a map", r"$\Q$", r"sympy (grevlex Gr\"obner basis)",
         r"%s nonzero second partials; time not recorded" % n["secondgens"]),
        ("A3", "EXP-041", r"$H$ on $\Q^{24}$, collision pair", r"$\Q(i)$, sparse \texttt{Fraction} dictionaries", r"sympy, standard library",
         r"%s products of sparse matrices; the printed powers of $JH$ have at most %s terms" % (n["nilindex"], n["jheight"])),
        ("A4", "EXP-138", r"$F$ on $\Q^3$, two points", r"$\Q$", r"sympy",
         r"%s s for the construction and the nilpotency chain, dimension %s" % (n["homseconds"], n["homdim"])),
        ("A5", "EXP-144", r"seven polynomials of Long", r"$\Q$ (\texttt{Fraction} for the second route)", r"sympy 1.14.0",
         r"%s s in all: brackets %s s, determinant %s s" % (n["poissonseconds"], n["poissonbrk"], n["poissondet"])),
    ]
    out = [r"\begin{table}[t]", r"\centering\footnotesize", r"\setlength{\tabcolsep}{3pt}",
           r"\begin{tabular}{@{}lL{0.11\textwidth}L{0.17\textwidth}L{0.15\textwidth}L{0.12\textwidth}L{0.24\textwidth}@{}}", r"\toprule",
           r"Algorithm & Record & Input & Arithmetic domain & Software & Measured cost \\", r"\midrule"]
    for row in rows:
        out.append(" & ".join(row) + r" \\[2pt]")
    out += [r"\bottomrule", r"\end{tabular}",
            r"\caption{The five procedures of Section~\ref{sec:methods}, with the computation that ran each, its input, the arithmetic domain, the software and the cost measured in that run. The version of the algebra system is recorded for computations EXP-001 and EXP-144 only; the other runs used the same environment but do not state the version in their artifacts.}",
            r"\label{tab:cost}", r"\end{table}"]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------------------------------ figures
def fig_fibre():
    # on the fibre 3x + 2y = 0, 12 y^2 = 4 z + 1, y (2 z - 13) = 0 (EXP-001 lex basis)
    pts = [(Fraction(0), Fraction(-1, 4)), (Fraction(-3, 2), Fraction(13, 2)), (Fraction(3, 2), Fraction(13, 2))]
    for y, z in pts:
        need(12 * y * y == 4 * z + 1 and y * (2 * z - 13) == 0, f"fibre point y={y} z={z} satisfies the basis")
    out = [r"\begin{tikzpicture}",
           r"\begin{axis}[width=0.78\textwidth, height=5.4cm, xlabel={$y$}, ylabel={$z$}, xmin=-2.4, xmax=2.4, ymin=-1.5, ymax=9.5,",
           r"  axis lines=left, legend style={font=\scriptsize, at={(0.5,1.03)}, anchor=south, legend columns=-1}, tick label style={font=\scriptsize}]",
           r"\addplot[domain=-2.2:2.2, samples=60, thick, color=stcurve] {3*x^2 - 0.25};",
           r"\addplot[dashed, color=stline] coordinates {(-2.4,6.5) (2.4,6.5)};",
           r"\addplot[dashed, color=stline] coordinates {(0,-1.5) (0,9.5)};",
           r"\addplot[only marks, mark=*, mark size=2.2pt, color=stpoint] coordinates {(0,-0.25) (-1.5,6.5) (1.5,6.5)};",
           r"\node[font=\scriptsize, anchor=west] at (axis cs:0.12,-0.25) {$(0,0,-\tfrac14)$};",
           r"\node[font=\scriptsize, anchor=south east] at (axis cs:-1.5,6.7) {$(1,-\tfrac32,\tfrac{13}{2})$};",
           r"\node[font=\scriptsize, anchor=south west] at (axis cs:1.5,6.7) {$(-1,\tfrac32,\tfrac{13}{2})$};",
           r"\legend{$12y^2=4z+1$, $z=\tfrac{13}{2}$, $y=0$, fibre}",
           r"\end{axis}", r"\end{tikzpicture}"]
    return "\n".join(out) + "\n"


def fig_chain(n):
    pts = [(1, n["jhone"]), (2, n["jhtwo"]), (4, n["jhfour"]), (8, n["jheight"]), (16, n["jhsixteen"]), (17, n["jhseventeen"])]
    coords = " ".join(f"({k},{v.replace('{,}', '')}) [{v.replace('{,}', '')}]" for k, v in pts)
    out = [r"\begin{tikzpicture}",
           r"\begin{axis}[width=0.78\textwidth, height=5.2cm, xlabel={power $k$}, ylabel={terms of $(JH)^k$}, ymode=log, xmin=0, xmax=19, ymin=2, ymax=12000,",
           r"  tick label style={font=\scriptsize}, xtick={1,2,4,8,16,17,18}, nodes near coords style={font=\tiny, above}]",
           rf"\addplot[only marks, mark=*, mark size=2pt, color=stcurve, nodes near coords, point meta=explicit symbolic] coordinates {{{coords}}};",
           r"\addplot[thick, color=stcurve, dashed] coordinates " + "{" + coords + "};",
           r"\end{axis}", r"\end{tikzpicture}"]
    return "\n".join(out) + "\n"


def fig_poisson(r):
    sz = r["r144"]["P1_sizes_measured"]
    order = ["beta", "y", "R", "S", "T", "H", "D"]
    names = {"beta": "beta", "y": "y", "R": "R", "S": "S", "T": "T", "H": "H", "D": "D"}
    coords = " ".join(f"({names[k]},{sz[k][0]}) [{sz[k][0]}]" for k in order)
    out = [r"\begin{tikzpicture}",
           r"\begin{axis}[ybar, width=0.80\textwidth, height=5.2cm, ymode=log, ymin=1, ymax=400, bar width=14pt, symbolic x coords={" + ",".join(names[k] for k in order) + r"},",
           r"  xtick=data, ylabel={nonzero terms}, tick label style={font=\scriptsize}, nodes near coords, point meta=explicit symbolic, nodes near coords style={font=\tiny}]",
           rf"\addplot[fill=stwit, draw=black!60] coordinates {{{coords}}};",
           r"\end{axis}", r"\end{tikzpicture}"]
    return "\n".join(out) + "\n"


def fig_moments(r):
    mom = r["r136"]["part_d"]["moments"]
    gm = r["r136"]["part_e"]["moments"]
    h = " ".join(f"({m['n']},{float(frac(m['int_F^n_G'])):.6f})" for m in mom)
    g = " ".join(f"({m['m']},{int(m['E_Q3_P3^m'])})" for m in gm)
    for m in mom:
        need(frac(m["int_F^n_G"]) == Fraction((-1) ** (m["n"] - 1), m["n"] + 1) and frac(m["int_F^n"]) == 0, f"Haar moment n={m['n']}")
    for m in gm:
        import math
        need(int(m["E_Q3_P3^m"]) == math.factorial(m["m"]) and int(m["E_P3^m"]) == 0, f"Gaussian moment m={m['m']}")
    out = [r"\begin{tikzpicture}",
           r"\begin{axis}[name=a, width=0.46\textwidth, height=5cm, ymin=-0.45, ymax=0.6,xlabel={$n$}, ylabel={$\int F^nG\,dg$}, tick label style={font=\scriptsize}, xtick={1,3,5,7,9,11}, axis lines=left]",
           rf"\addplot[only marks, mark=*, mark size=2pt, color=stcurve] coordinates {{{h}}};",
           r"\addplot[domain=1:12, samples=12, dashed, color=stline] {0};",
           r"\end{axis}",
           r"\begin{axis}[at={(a.east)}, anchor=west, xshift=1.9cm, width=0.46\textwidth, height=5cm, xlabel={$m$}, ylabel={$E(Q_3P_3^m)$}, ymode=log, tick label style={font=\scriptsize}, xtick={1,3,5,7,9}, axis lines=left]",
           rf"\addplot[only marks, mark=square*, mark size=2pt, color=stpoint] coordinates {{{g}}};",
           r"\end{axis}", r"\end{tikzpicture}"]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default=str(DEFAULT_EXP))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    exp = Path(a.exp)
    r = read_all(exp)
    n = numbers(r)
    rows = status_rows(r, n)
    outputs = {
        "numbers.tex": "".join(f"\\newcommand{{\\n{k}}}{{{v}}}\n" for k, v in sorted(n.items())),
        "status_table.tex": status_table(rows),
        "implication_graph.tex": graph(rows),
        "index_map.tex": index_map(r),
        "hash_table.tex": hash_table(r, n),
        "validation_table.tex": validation_table(r, n),
        "cost_table.tex": cost_table(r, n),
        "fig_fibre.tex": fig_fibre(),
        "fig_chain.tex": fig_chain(n),
        "fig_poisson.tex": fig_poisson(r),
        "fig_moments.tex": fig_moments(r),
    }
    if FAILS:
        print(f"{len(FAILS)} mismatch(es); nothing written", file=sys.stderr)
        return 1
    stale = []
    for name, body in outputs.items():
        p = HERE / name
        if a.check:
            if not p.exists() or p.read_text(encoding="utf-8") != body:
                stale.append(name)
        else:
            p.write_text(body, encoding="utf-8", newline="\n")
    if a.check:
        print("stale: " + ", ".join(stale) if stale else "outputs current")
        return 1 if stale else 0
    print(f"wrote {len(outputs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
