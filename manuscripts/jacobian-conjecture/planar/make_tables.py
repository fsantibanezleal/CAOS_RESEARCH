#!/usr/bin/env python3
"""Generate the chart-atlas table and the reproducibility table of the planar manuscript.

Every cell of the atlas table is pinned to a quotation from the experiment record it comes from.
The script refuses to write a table when a quotation is missing from its record, so a cell cannot
drift from the archive. A cell that no record holds is printed as "n/r" (not recorded) and listed
on standard output. The reproducibility table lists, per algorithm, the entry point, the artifact
and its SHA-256 (first 16 hexadecimal digits); where the experiment record states the hash, the
script compares it with the file on disk.

The tables of the Case 1 certificate (EXP-146: the tree, the gates, the planted defects, the constants at several primes) are
generated from that record's artifacts/results.json and artifacts/mutants.json, and a fixed list of the figures the text quotes
(primes, total, branch and Singular times, node shapes and counts) is compared with them; the text itself is not read.

Usage (from any directory):
    python make_tables.py            # writes tab_atlas.tex, tab_repro.tex and the generated tables next to this file
    python make_tables.py --check    # verifies the quotations and hashes, writes nothing
"""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
REPO = HERE.parents[2]
EXPS = REPO / "problems" / "algebraic-geometry" / "jacobian-conjecture" / "experiments"

NR = "n/r"

# Each row: experiment id, cells (basis, scc, factorization, residual, certificate, controls, time) as
# LaTeX, and quotations [(text that must occur in verdict.md)] that pin the numbers of the row.
ROWS = [
    ("101", "pinned 125-row chart", NR,
     r"$(st-8)^6\bigl(2^{15}s^9-(st-8)^7\bigr)/2^{39}$",
     r"curve $2^{15}s^9=(st-8)^7$",
     "low-rank factorization and direct $125\\times125$ determinant agree", NR,
     "inside a 5-min budget",
     ["combined perturbation rank is \\(97\\)", "five-minute budget", "(st-8)^6"]),
    ("102", "third augmented minor chosen by modular pivots at $(s,t)=(8,9)$", NR,
     "not reached", "curve points", "exact rank $124/125$ and nonzero minor at one point only",
     "modulus $2147483629$", "stopped at 304 s (5-min limit)",
     ["stopped at 304 seconds", "2147483629"]),
    ("103", "four row charts of a $289\\times125$ scaled matrix; one passes the endpoint test", NR,
     "support $[1628,1646]$ (modular) against bounds $[1547,1646]$", "81 low coefficients",
     "none (endpoint test failed)", "modulus $998244353$", NR,
     ["[1547,1646]", "[1628,1646]", "998244353"]),
    ("104", "first chart and an independent chart at $u=2$", NR,
     "$21-96u^9-1024u^{18}$ (primitive)", "none on the curve",
     "exact support $[1628,1646]$; gcd $1$ of the two minors",
     "100 exact values; moduli $998244353$, $1004535809$", NR,
     ["[1628,1646]", "100 integer points", "1004535809"]),
    ("105", "same two charts", "connected mod-9 weights",
     "$F=21-96z-1024z^2$, $G=(8z+1)^{14}$", "none (slice closed)",
     "integer Bezout identity, constant $17^{14}$", "15 exact integer determinants, 2 checks", NR,
     ["17^{14}", "15 exact integer determinants"]),
    ("106", "no new basis", NR, "grading $w_{p,q}\\equiv q-p+1 \\pmod 9$", "none (no certificate)",
     "grading of 23 directions", "modulus $998244353$ (ranks)", NR,
     ["All 23 remaining nonconstant directions", "q-p+1"]),
    ("107", "same two charts, third direction $(0,7)$", NR,
     "chart of bidegree $(14,12)$, 45 terms; $G$ unchanged", "degree-12 fibre $Q(y)$ at $z=-1/8$",
     "modular pilot only", "modulus $998244353$; off-grid checks", NR,
     ["45 terms", "bidegree \\((14,12)\\)", "degree-12"]),
    ("108", "third 125-row chart at the fibre", NR,
     "$H(y)$ of degree 13 (four factors)", "none (slice closed)",
     "integer Bezout identity, 61-digit constant", "29 exact determinants, 2 controls", NR,
     ["29 interpolation", "3036277895244878564727703434378848855121939007419328699039744"]),
    ("110", "pinned point, three random rational points", NR, "rank $124$, augmented rank $125$",
     "none (audit)", "generic rank only", "exact rational run exceeded 20 min", "$>$20 min",
     ["20-minute"]),
    ("111", "forced-only 289 rows against the complete 302 rows", NR, "rank bound from $[P,1]=0$",
     "none (audit)", "rank profile $124/125$ in both systems", "4 points, 2 primes", "3.6 s",
     ["302 rows", "3.6 seconds"]),
    ("112", "pinned 125-row chart, constant column removed", "36",
     "$\\det A_0(1+\\varepsilon_{(1,0)})^3\\det C_{36}$", "24 parameters in $C_{36}$",
     "none (compression)", "exact", "5.3 s",
     ["5.3 seconds", "largest strongly connected block is 36"]),
    ("113", "pinned chart", "36", "triples $T_A$, $T_B$ generate the graph", "none (audit)",
     "positive and negative controls", "exact", "4.1 s",
     ["4.1 seconds", "SCC compression"]),
    ("114", "pinned chart on $T_A$ and $T_B$", "36",
     "$T_A$: degrees $3,12,6$; $T_B$: $G_{54}H_{63}$", "residual factor loci", "none",
     "exact", "143.3 s",
     ["T_B"]),
    ("115", "good-prime alternative minors replace 68, 34, 34 pinned rows", NR,
     "$G_{54}$ irreducible; $H_{63}=LQ$", "$G$, $L$, $Q$ (proper intersections)",
     "none contained in the rank-deficient locus", "$p=1009$", "2.7 s",
     ["2.7 seconds", "68, 34", "p=1009"]),
    ("116", "302-by-124 quotient (kernel $[P,P]=0$)", "51 (blocks 51, 11, 10, 9, 8, 7)",
     "rank profile $112/113$ at the origin", "51-block determinant", "none",
     "exact", "about 210 s (exploratory)",
     ["The largest cyclic block has size 51", "about 210 seconds"]),
    ("117", "quotient chart", "51",
     "$b^{32}F_{28}\\prod_{c}(ca^3+78125b^7)$", "$b=0$ and nine points", "five direct $124\\times124$ controls",
     "exact", "212.2 s",
     ["212.2 seconds", "five direct 124-by-124 determinant controls"]),
    ("118", "alternative 124-row basis", NR, "$a^{107}$ (quotient); $b^{95}$ on $a=0$",
     "none ($d=0$ plane closed)", "12 component controls at good primes", "two primes", "9.97 s",
     ["1,293 support equations", "12 independent component controls"]),
    ("119", "first alternative basis on $d=1$ (302-by-125)", "26",
     "$B^{36}K(X,B)\\prod(cX+78125B^7)$, 114 monomials", "three finite intersections",
     "five direct $125\\times125$ controls", "exact", "93.75 s",
     ["93.75 seconds", "The largest block is 26", "114 monomials"]),
    ("120", "independent $G$-basis", "25", "$X^{30}LQR$, 21 monomials",
     "$L$ and $Q$ zero-dimensional", "$G$ closed by four unit ideals; five direct controls",
     "exact", "28.85 s", ["28.85 seconds", "21 monomials"]),
    ("121", "shared $L/Q$ basis, 68 rows from the pinned one", "26",
     "$A^{87}R_{\\mathrm{fin}}(A^3,B)$, 23 monomials", "none ($T_B$ closed)",
     "unit ideals on $L$ and $Q$ (gcd certificates)", "$p=1013$ ($L$), $p=1033$ ($Q$)", "44.57 s",
     ["44.57 seconds", "size 26", "p=1033"]),
    ("122", "shared basis of EXP-121", "26 (34 after enlargement)", "24 directions restored",
     "none (audit)", "no direction lifts for free", "exact", "45.15 s",
     ["45.15 seconds", "the smallest enlarged SCC, 34"]),
    ("123", "shared basis, $d=1$", "as EXP-122",
     "$A^{87}(R+YS)$, $\\gcd(R,S)=1$", "rational graph, base locus, $A=0$",
     "four direct $125\\times125$ controls", "exact", "131.86 s",
     ["131.86 seconds", "Four independent rational controls"]),
    ("124", "alternative basis, one row from the shared one", "87 cyclic components",
     "$A^{90}N$, $N=F_3F_6F_7$", "three plane curves", "20 sampled points per prime",
     "$p=1009,1013$", "32.86 s", ["32.86 seconds", "87 cyclic components", "1009 and 1013"]),
    ("125", "new basis on $F_3$", "32", "$(5B+4)Q_6^2Q_9Q_{15}$", "$Q_9Q_{15}=0$, 24 values",
     "four direct controls; four points per curve", "$p=739,811$", "43.82 s",
     ["43.82 seconds", "size 32", "739 and 811"]),
    ("126", "$F_6$ basis (equal to $F_3$ basis)", "32", "norm of degree 74: $D_2D_3^4D_6^2Q_{18}Q_{30}$",
     "$Q_{18}Q_{30}=0$, 48 values", "Sylvester resultant and multiplication norm", "exact", "5.78 s",
     ["5.78 seconds", "32-vertex largest cyclic block"]),
    ("127", "new basis on $F_7$", "31", "norm of degree 58: $B^{16}E_3E_9E_{12}E_{18}$",
     "$E_3E_9E_{18}=0$, 30 values", "resultant and quotient determinant agree", "exact", NR,
     ["block of size 31"]),
    ("128", "none (quotient algebra)", NR, "five factors of degrees $9,15,18,30,3$",
     "75 points, not 102", "CRT idempotents", "exact", NR,
     ["9,\\ 15,\\ 18,\\ 30,\\ 3", "not 102"]),
    ("129", "two bases on $F_7$", "32 and 31", "two sections $k_1,k_2$", "none ($AS\\ne0$ closed)",
     "norm gcds and Bezout identities", "two probes per block", NR,
     ["no single sampled row basis covers all", "two exact maximal-minor sections"]),
    ("130", "$F_3$ basis with one row replaced", "33", "$A^{86}H(X,B,Y)$, $\\deg_YH=2$",
     "none ($A\\ne0$ closed)", "Bezout identities, resultants, norms, direct determinant",
     "two primes per block", NR,
     ["reduced the largest component to 33"]),
    ("131", "two bases of the $302\\times125$ matrix at $A=0$", NR,
     "$(5B+4)^3(25B^2-20B+16)^3$ and $B^{95}(\\cdots)$", "none ($A=0$ closed)",
     "extended Euclid, identity of $\\mathbb Q[B,C]$", "$p=1009$; four rational controls", NR,
     ["four rational \\((B,C)\\) controls", "Two row bases"]),
    ("132", "three sections on $A=0,d=1$ with $T=\\varepsilon_{(2,8)}$", "106 singleton blocks",
     "$P$, $Q$, $R=B^{105}C$", "none (direct $A=0$ boundary)", "Bezout identity in $\\mathbb Q[B]$",
     "$p=1009,1153$; $109,127$", "116.18 s",
     ["116.18 seconds", "1009 and 1153", "109 and 127"]),
    ("133", "five accepted sections", "at most 7 (joint)", "degrees in $T$ per section",
     "none (preflight)", "modular controls", "$p=1009,1153$", "10.21 s",
     ["10.21 seconds", "1009 and 1153"]),
    ("134", "EXP-124 section", "33", "graph identity", "inconclusive at the gate",
     "none", "exact", "stopped at 240 s",
     ["240-second", "size 33"]),
    ("135", "EXP-124 section, $(2,8)$ added", "33",
     "$\\det(H+TK_T)=\\det H$", "none (one section)", "136,500 controls, 885-bit bound",
     "30 primes (897 bits)", NR,
     ["136,500", "885-bit", "897 bits"]),
]

HEADERS = ["EXP", "row basis", "largest SCC", "determinant", "residual left", "closure", "primes, controls", "time"]

REPRO = [
    # algorithm, experiment, entry point, artifact (relative to the experiment folder), hash-in-record
    ("A1", "EXP-020", "run.py", "artifacts/output-A-2026-07-21.txt", None),
    ("A2", "EXP-042", "run.py", "artifacts/output-AB-2026-07-22.txt", None),
    ("A3", "EXP-037", "run.py", "artifacts/output-AB-2026-07-22.txt", None),
    ("A4", "EXP-103", "run.py", "artifacts/results.json", "1DF6079D51ADF46D"),
    ("A4", "EXP-104", "run.py", "artifacts/results.json", "99761ED83060E633"),
    ("A4", "EXP-105", "run.py", "artifacts/results.json", "A688644B113DD9CD"),
    ("A4", "EXP-106", "run.py", "artifacts/results.json", "0CBD7E19C962829C"),
    ("A4", "EXP-107", "run.py", "artifacts/results.json", "40583A2BB6343A63"),
    ("A4", "EXP-108", "exact\\_lift.py", "artifacts/exact-results.json", "E2613D21D333CA6A"),
    ("A5", "EXP-135", "certificate.py", "artifacts/certificate.json", "B426FE41C7DC835D"),
    ("A6", "EXP-141", "cert.py (run, verify)", "artifacts/gates-output.txt", None),
    ("A6", "EXP-142", "branches.py, gates.py", "artifacts/gates-output.txt", None),
    ("A7", "EXP-146", "run.py, chaincert.py", "artifacts/results.json", None),
    ("A7", "EXP-146", "run.py, chaincert.py", "artifacts/slp-plus.json", None),
    ("A7", "EXP-146", "run.py, chaincert.py", "artifacts/slp-minus.json", None),
]

SCRIPT_FILES = {
    "EXP-020": "run.py",
    "EXP-042": "run.py",
    "EXP-037": "run.py",
    "EXP-103": "run.py",
    "EXP-104": "run.py",
    "EXP-105": "run.py",
    "EXP-106": "run.py",
    "EXP-107": "run.py",
    "EXP-108": "exact_lift.py",
    "EXP-135": "certificate.py",
    "EXP-141": "cert.py",
    "EXP-142": "branches.py",
    "EXP-146": ("run.py", "chaincert.py"),
}


def norm(text):
    return re.sub(r"\s+", " ", text)


def exp_dir(num):
    found = sorted(EXPS.glob(f"EXP-{num}-*"))
    if not found:
        raise SystemExit(f"missing experiment folder EXP-{num}")
    return found[0]


def verify_rows():
    bad = []
    for row in ROWS:
        num, quotes = row[0], row[-1]
        text = norm((exp_dir(num) / "verdict.md").read_text(encoding="utf-8"))
        for q in quotes:
            if norm(q) not in text:
                bad.append((num, q))
    return bad


ARTCHECK = [
    # (exp, artifact, description, predicate on the parsed json)
    ("114", "artifacts/results.json", "elapsed 143.3 s", lambda d: abs(d["elapsed_seconds"] - 143.3) < 0.05),
    ("118", "artifacts/results.json", "elapsed 9.97 s", lambda d: abs(d["elapsed_seconds"] - 9.97) < 0.005),
    ("129", "artifacts/results.json", "largest SCC 32 and 31",
     lambda d: d["exact_atlas"][0]["cyclic_component_sizes"][0] == 32 and d["exact_atlas"][1]["cyclic_component_sizes"][0] == 31),
]


def verify_artifacts():
    import json
    bad = []
    for num, art, desc, pred in ARTCHECK:
        d = json.loads((exp_dir(num) / art).read_text(encoding="utf-8"))
        if not pred(d):
            bad.append((num, desc))
    # EXP-118: the file must be the one the verdict names as final
    v = norm((exp_dir("118") / "verdict.md").read_text(encoding="utf-8")).upper()
    if sha(exp_dir("118") / "artifacts/results.json") not in v:
        bad.append(("118", "results.json hash is not the one the verdict names"))
    return bad


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def verify_repro():
    bad = []
    out = []
    for alg, exp, entry, art, expected in REPRO:
        num = exp.split("-")[1]
        d = exp_dir(num)
        scripts = SCRIPT_FILES[exp]
        for script in ((scripts,) if isinstance(scripts, str) else scripts):
            if not (d / script).exists():
                bad.append((exp, f"entry point {script} missing"))
        digest = "n/r"
        if art is not None:
            p = d / art
            if not p.exists():
                bad.append((exp, f"artifact {art} missing"))
            else:
                digest = sha(p)[:16]
                if expected is not None and digest != expected:
                    bad.append((exp, f"hash {digest} differs from the record {expected}"))
        out.append((alg, exp, entry, art, digest))
    return bad, out


def tex_atlas():
    lines = []
    lines.append("% generated by make_tables.py; do not edit")
    lines.append("{\\scriptsize")
    lines.append("\\setlength{\\tabcolsep}{3pt}")
    lines.append("\\begin{longtable}{@{}P{0.9cm}P{2.6cm}P{1.7cm}P{3.4cm}P{2.7cm}P{3.2cm}P{2.6cm}P{1.7cm}@{}}")
    lines.append("\\caption{Chart atlas: one row per record from EXP-101 to EXP-135 that selects a chart, certifies a stratum or audits the system (EXP-109 has no record). ``SCC'' is the largest cyclic block of the support graph of the selected minor. Each cell is read from the record of the row; n/r marks a cell the record does not state.}\\label{tab:atlas}\\\\")
    lines.append("\\toprule")
    lines.append(" & ".join(f"\\textbf{{{h}}}" for h in HEADERS) + " \\\\")
    lines.append("\\midrule\\endfirsthead")
    lines.append("\\toprule")
    lines.append(" & ".join(f"\\textbf{{{h}}}" for h in HEADERS) + " \\\\")
    lines.append("\\midrule\\endhead")
    lines.append("\\bottomrule\\endfoot")
    for row in ROWS:
        num = row[0]
        cells = row[1:-1]
        lines.append(f"{num} & " + " & ".join(cells) + " \\\\")
    lines.append("\\end{longtable}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def run_times():
    """(exp, seconds, stopped) read from the time cell of each atlas row that states a number of seconds."""
    out = []
    for row in ROWS:
        cell = row[-2]
        m = re.search(r"([0-9]+(?:\.[0-9]+)?) s", cell)
        if m:
            out.append((row[0], float(m.group(1)), "stopped" in cell))
    return out


def tex_times(times):
    import math
    lines = ["% generated by make_tables.py; do not edit",
             "\\begin{tikzpicture}[x=0.36cm,y=0.9cm,font=\\scriptsize]",
             "  \\draw[->] (0,0) -- (%.1f,0);" % (len(times) + 0.6),
             "  \\draw[->] (0,0) -- (0,3.2);"]
    for k in range(0, 4):
        lines.append("  \\draw (0,%d) -- (-0.15,%d) node[left]{$10^{%d}$};" % (k, k, k))
    for i, (num, sec, stopped) in enumerate(times):
        h = math.log10(sec)
        style = "red!60!black,fill=red!25" if stopped else "blue!60!black,fill=blue!20"
        lines.append("  \\draw[%s] (%.2f,0) rectangle (%.2f,%.3f);" % (style, i + 0.7, i + 1.3, h))
        lines.append("  \\node[rotate=90,anchor=east] at (%.2f,-0.05) {%s};" % (i + 1.0, num))
    lines.append("  \\node[rotate=90] at (-2.0,1.6) {seconds};")
    lines.append("\\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def tex_repro(rows):
    lines = []
    lines.append("% generated by make_tables.py; do not edit")
    lines.append("{\\footnotesize")
    lines.append("\\begin{tabular}{@{}llP{2.9cm}P{3.6cm}l@{}}")
    lines.append("\\toprule")
    lines.append("\\textbf{Algorithm} & \\textbf{Record} & \\textbf{Entry point} & \\textbf{Artifact} & \\textbf{SHA-256 (first 16 digits)} \\\\")
    lines.append("\\midrule")
    for alg, exp, entry, art, digest in rows:
        a = "n/r" if art is None else "\\path{" + art + "}"
        d = "n/r" if digest == "n/r" else "\\texttt{" + digest + "}"
        lines.append(f"{alg} & {exp} & \\texttt{{{entry}}} & {a} & {d} \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("}")
    return "\n".join(lines) + "\n"



def simple_table(d, placement="tbp"):
    head = " & ".join(h if h.startswith("\\textbf") else "\\textbf{%s}" % h for h in d["head"])
    lines = ["% generated by make_tables.py; do not edit",
             "\\begin{table}[%s]" % placement, "\\centering",
             "\\caption{%s}\\label{%s}" % (d["caption"], d["label"]),
             "{\\footnotesize", "\\begin{tabular}{@{}%s@{}}" % d["spec"], "\\toprule", head + " \\\\", "\\midrule"]
    for r in d["rows"]:
        lines.append(" & ".join(r) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}}", "\\end{table}"]
    return "\n".join(lines) + "\n"


def long_table(d):
    """A captioned longtable (breaks across pages); the depth check counts it as a table."""
    cols = d["spec"]
    head = " & ".join(h if h.startswith("\\textbf") else "\\textbf{%s}" % h for h in d["head"])
    lines = ["% generated by make_tables.py; do not edit",
             "{\\footnotesize", "\\begin{longtable}{@{}%s@{}}" % cols,
             "\\caption{%s}\\label{%s}\\\\" % (d["caption"], d["label"]),
             "\\toprule", head + " \\\\", "\\midrule\\endfirsthead",
             "\\toprule", head + " \\\\", "\\midrule\\endhead", "\\bottomrule\\endfoot"]
    for r in d["rows"]:
        lines.append(" & ".join(r) + " \\\\")
    lines += ["\\end{longtable}", "}"]
    return "\n".join(lines) + "\n"


ABLATION = dict(
    label="tab:ablation",
    caption="Ablation of the ingredients: what each one buys, from the records. Each row compares the ingredient with the alternative the record measured.",
    spec="P{2.1cm}P{2.3cm}P{2.4cm}P{5.4cm}P{1.5cm}",
    head=["Ingredient", "Kept", "Removed or replaced", "Measured effect", "Records"],
    rows=[
        ["similarity filter", "filtered window", "full window", "$(48,64)$: $111$ against $2142$ unknowns; $2.4$ to $3.6$ s per sample", "045, 047"],
        ["similarity filter", "open pair, $N=108$", "unfiltered histogram", "$143$ unknowns and about $320$ equations, $1.2$ to $1.4$ s, against $5992$ unknowns in $535$ classes", "043, 050"],
        ["pair shape", "$Q$ constrained", "$Q$ free", "same first inconsistent window $N=3$ on four samples; unknowns $7$ to $3$--$4$", "038"],
        ["classwise transport", "minimal $P$-class diagonal", "monolithic test", "same outcome on every tested sample", "037"],
        ["half-plane restriction", "$H$-certificate", "full-window certificate", "at $(2,2,2)$, $N=9$: left-null space of dimension $20$, two pairing-nonzero certificates, one kills the odd resonance", "048"],
        ["SCC block product", "block product", "dense pullback", "$5.3$ s for the $125\\times125$ determinant against a dense pullback of rank $121$ that passed $5$ min", "102, 112"],
        ["graded reduction", "mod-$9$ weights removed", "dense three-variable expansion", "width $14$ in $z=u^9$; a $16\\times64$ transform grid", "106, 107"],
        ["exact interpolation", "$100$ integer points", "modular support", "$[1628,1646]$ against bounds $[1547,1646]$: an $81$-degree cancellation", "103, 104"],
        ["basis choice", "basis chosen on the residual", "inherited basis", "inherited bases vanish on $A=0$; one basis cannot cover $F_7$ (two sections needed); a default targeted basis passed $300$ s against largest block $33$ after one row replaced", "129, 130, 132"],
        ["low-rank transfer", "rank factorization, CRT", "dense $33\\times33$ symbolic determinant", "the dense route reached its $240$ s limit; the transfer proves the identity", "134, 135"],
        ["subfield reduction", "quintic subfield", "degree-$35$ field", "both unknown at six hours; certificates still above $94{,}000$ digits", "139, 140, 143"],
        ["exact chain levels", "levels $1$ and $2$ from exact supports", "bounds from the inputs alone", "bounds computed from the inputs alone are loose from level $1$ (a level-$1$ member of $q_0$-degree $7$ against a bound $8$); with two exact levels and weights in $\\{0,\\dots,3\\}$ every later pivot attains its bound ($688=688$)", "146"],
        ["monomial coordinate", "$w_1=l$, the $q_5$ coefficient of $E_3$", "$q_0$ coordinates", "in $q_0$ coordinates the case $l\\ne0$ fails because the degree in the Rabinowitsch variable drops by $212$ unseen; in $w_1$ the shared factor is the monomial $w_1^{212}$, its order bounded below by the propagated (composed) bound and divided out exactly, so the node certifies at degree $476$ with two nonzero constants of two", "146"],
        ["second split", "$w_2$ at the node $w_1=0$", "one split only", "the node $w_1=0$ has $0$ of $4$ nonzero constants and a squared common factor; the split on $w_2$ certifies both children ($3$ of $4$ and $6$ of $6$ nonzero)", "146"],
        ["single prime", "one prime, a second prime and Singular as checks", "multi-modular cofactors", "trees of $252$ s and $102$ s against more than $20{,}000$ primes per branch with no coordinate reconstructible (above $94{,}000$ digits)", "143, 146"],
    ])

NOTATION = dict(
    label="tab:notation",
    caption="Notation. The symbol $L$ is the operator $J(P,\\cdot)$ in Sections~\\ref{sec:theory} and~\\ref{sec:design} and the number field $\\Q[y]/(P)$ in Sections~\\ref{sec:methods}, \\ref{sec:chaintheory} and~\\ref{sec:helali}; the symbol $R$ has the per-section meanings of its rows.",
    spec="P{4.6cm}P{9.0cm}",
    head=["Symbol", "Meaning"],
    rows=[
        ["$J(P,Q)$", "Jacobian determinant $P_xQ_y-P_yQ_x$; a Keller pair has $J(P,Q)\\in\\C^\\times$"],
        ["$L$, $L_{\\mathrm{top}}$", "the operator $J(P,\\cdot)$ and its top-weight part $J(P_{\\mathrm{top}},\\cdot)$"],
        ["$N(P)$", "Newton polygon: convex hull of the support of $P$ with the origin"],
        ["$(u,v,d)$, $a$, $b$", "shape $P=x+a\\,x^uy^v+b\\,x^d$ and its coefficients"],
        ["$w=(v,1-u)$", "weights of $(x,y)$; $P=x+a\\,x^uy^v$ is homogeneous of weight $v$"],
        ["$T$", "total-degree top form of $P$"],
        ["$M_N$, $c$, $\\pi$", "completion matrix at window $N$, a left-null covector, and its pairing $c^Te$ with the constant right-hand side"],
        ["$B=\\gcd(\\deg P,\\deg Q)$", "gcd of the degrees of a counterexample (Table~\\ref{tab:ladder}); also the coordinate $B$ of the atlas"],
        ["$H$", "$y$-heavy half-plane $\\{i\\le j\\}$ of rows; also the eliminant $H(a_7)$ in Section~\\ref{sec:helali}"],
        ["$\\varepsilon$, $[M\\mid b]$", "the $51$ interior coefficients and the augmented matrix ($302\\times125$) of the Case 1 system"],
        ["$A,B,C,X,Y,d$", "normalized parameters of the atlas: $X=A^3$, $Y=A^2C$, $d=1+\\varepsilon_{(1,0)}$"],
        ["$R,S,F_3,F_6,F_7$", "polynomials of the shared determinant $A^{87}(R+YS)$ and the factors of the graph numerator (Section~\\ref{sec:atlas}; in Section~\\ref{sec:theory} $R$ is the tail $P-P_{\\mathrm{top}}$)"],
        ["$K$, $L$, $P$", "$K=\\Q[a_7]/(H)$ (degree $35$); $L=\\Q[y]/(P)$ with $P=y^5-y^4+3y^3+3y^2+26$ (Section~\\ref{sec:helali})"],
        ["$R$, $\\phi$, $(p,r)$", "in Sections~\\ref{sec:methods}, \\ref{sec:chaintheory} and~\\ref{sec:helali}: $R=\\mathbb Z[y]/(P)$ (not the tail, nor the polynomial $R$ of the atlas); the ring map $\\phi_{p,r}:R\\to\\mathbb F_p$, $y\\mapsto r$, with $P(r)=0$ modulo $p$ (Section~\\ref{sec:chaintheory})"],
        ["$I_\\pm$", "the branch ideals $q_1=\\pm c$ of Case 1 in $L[q_0,q_2,q_3,q_4,q_5]$, nine equations each"],
        ["$\\operatorname{Res}_{x;m,n}$", "the Sylvester resultant for the formal degrees $m,n$ in $x$, a determinant of the coefficients"],
        ["$B_h(w)$, $W$", "the proven bound $\\max_{a\\in\\operatorname{supp}h}w\\cdot a\\le B_h(w)$ for a weight $w$ of the weight set $W$ (components in $\\{0,..,3\\}$, the split variable in $\\{-3,..,3\\}$)"],
        ["$V_i$, $\\ell_i$", "the univariate member $U_i/w^{\\ell_i}$ of a node and the proven lower bound $\\ell_i=-B_{U_i}(-e_w)$ of its order in the split variable $w$"],
        ["\\texttt{t}, \\texttt{t.nz}, \\texttt{t.z}", "node ids of a branch tree: \\texttt{t} is the root; a split appends \\texttt{.nz} for the child $w\\ne0$ and \\texttt{.z} for the child $w=0$ (so \\texttt{t.z.nz} is the child $w_2\\ne0$ of the node $w_1=0$)"],
        ["$E_k$", "the $k$-th equation of the Case 1 system of EXP-142"],
        ["$l_{k.j}$", "the $j$-th member, counted from $0$, formed at resultant level $k$ of a node"],
        ["{[MV]}, [D], [C], [U]", "machine-verified, derived, conjectural, not confirmed on a primary source"],
    ])

WINDOW = [(5, 420), (6, 1260), (7, 13860), (8, 180180), (9, 180180), (10, 3063060), (11, 58198140)]
CHAIN = [121, 111, 101, 91, 81, 74, 67, 60, 54, 49, 45, 42, 40, 39, 39]


def tex_window():
    import math
    pts = [(n, math.log10(c)) for n, c in WINDOW]
    path = "--".join("(%d,%.3f)" % p for p in pts)
    lines = ["% generated by make_tables.py; do not edit",
             "\\begin{tikzpicture}[x=1.2cm,y=0.55cm,font=\\scriptsize]",
             "  \\draw[->] (4.6,0)--(11.6,0) node[right]{$N$};",
             "  \\draw[->] (4.6,0)--(4.6,8.4) node[above]{$\\log_{10}c_N$};"]
    for n, _ in WINDOW:
        lines.append("  \\draw (%d,0)--(%d,-0.15) node[below]{%d};" % (n, n, n))
    for k in (2, 4, 6, 8):
        lines.append("  \\draw (4.6,%d)--(4.45,%d) node[left]{%d};" % (k, k, k))
    lines.append("  \\draw[thick,blue!60!black] %s;" % path)
    for n, y in pts:
        lines.append("  \\fill[blue!60!black] (%d,%.3f) circle (0.07);" % (n, y))
    lines.append("\\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def tex_chain():
    path = "--".join("(%d,%d)" % (i + 1, d) for i, d in enumerate(CHAIN))
    lines = ["% generated by make_tables.py; do not edit",
             "\\begin{tikzpicture}[x=0.55cm,y=0.036cm,font=\\scriptsize]",
             "  \\draw[->] (0,0)--(16,0) node[right]{step};",
             "  \\draw[->] (0,0)--(0,130) node[above]{dimension};"]
    for s_ in (1, 3, 5, 7, 9, 11, 13, 15):
        lines.append("  \\draw (%d,0)--(%d,-3) node[below]{%d};" % (s_, s_, s_))
    for d_ in (0, 39, 80, 121):
        lines.append("  \\draw (0,%d)--(-0.15,%d) node[left]{%d};" % (d_, d_, d_))
    lines.append("  \\draw[thick,blue!60!black] %s;" % path)
    lines.append("  \\draw[dashed,gray] (0,39)--(15.6,39);")
    lines.append("\\end{tikzpicture}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------------------------------------------
# EXP-146: the single-prime resultant-chain certificate. Everything below reads the record's artifacts.
# ---------------------------------------------------------------------------------------------------------------

def load146(name):
    import json
    return json.loads((exp_dir("146") / "artifacts" / name).read_text(encoding="utf-8"))


def n_(x):
    """An integer with LaTeX thousands separators, in math mode."""
    return "$" + "{:,}".format(x).replace(",", "{,}") + "$"


def tt(x):
    return "\\texttt{" + x + "}"


def var_math(v):
    return "$" + v[0] + "_" + v[1:] + "$"


def memtex(x):
    """A member id as math: E3 -> $E_{3}$, l1.0 -> $l_{1.0}$ (the letter l is unreadable beside a digit in typewriter type)."""
    return "$%s_{%s}$" % (x[0], x[1:])


def node_label(b, nid):
    return ("$I_+$ " if b == "plus" else "$I_-$ ") + tt(nid)


def run_length(vals):
    out = []
    for v in vals:
        if out and out[-1][0] == v:
            out[-1][1] += 1
        else:
            out.append([v, 1])
    return ", ".join(str(v) if k == 1 else "%d$\\times$%s" % (k, v) for v, k in out)


def tex_tree(res):
    lines = ["% generated by make_tables.py from EXP-146 results.json; do not edit",
             "\\begin{table}[tbp]", "\\centering",
             "\\caption{The certificate trees of Case 1 (EXP-146), one row per node of each branch ideal. A pivot is written "
             "variable, member, formal degree. The degrees are those of the univariate members $V_i$ after the division by $w^{\\ell_i}$, "
             "with $\\ell_i$ the proven order, both listed in the member order of the node; the node ids are \\texttt{t} (root), \\texttt{t.nz} ($w_1\\ne0$), \\texttt{t.z} ($w_1=0$), \\texttt{t.z.nz} ($w_1=0$, $w_2\\ne0$) and \\texttt{t.z.z} ($w_1=0$, $w_2=0$); a node is certified when one of its final constants is nonzero "
             "modulo $p_1$. Both branches have the same shape; the split roots are those of the leading coefficient $w$ modulo $p_1$.}"
             "\\label{tab:tree}",
             "{\\scriptsize", "\\setlength{\\tabcolsep}{3pt}",
             "\\begin{tabular}{@{}P{1.4cm}P{3.8cm}P{2.7cm}P{1.4cm}P{1.3cm}P{2.6cm}P{0.9cm}@{}}",
             "\\toprule",
             "\\textbf{Node} & \\textbf{Pivots} & \\textbf{Degrees of $V_i$ (last variable)} & \\textbf{$\\ell_i$} & \\textbf{Nonzero} & "
             "\\textbf{Outcome} & \\textbf{Time (s)} \\\\", "\\midrule"]
    for b in ("plus", "minus"):
        for n in res["branches"][b]["nodes"]:
            piv = "; ".join("%s: %s, %d" % (var_math(s["x"]), memtex(s["pivot"]), s["n"]) for s in n["steps"])
            mem = n["last"]["members"]
            lastx = n["last"]["x"]
            deg = "%s: %s" % (var_math(lastx), run_length([m["d"] for m in mem]))
            ell = run_length([m["L"] for m in mem])
            nz = "%d of %d" % (n["nonzero_constants"], n["pairs_total"])
            if n["status"] == "split":
                sp = n["split"]
                out = "split on $%s_%s$ (root %s), gcd degree %d" % (sp["w"][0], sp["w"][1:], n_(sp["root"]), n["gcd"]["gcd_degree"])
            else:
                out = "certified"
            lines.append(" & ".join([node_label(b, n["id"]), piv, deg, ell, nz, out, "%.1f" % n["seconds"]]) + " \\\\")
        if b == "plus":
            lines.append("\\midrule")
    lines += ["\\bottomrule", "\\end{tabular}", "}", "\\end{table}"]
    return "\n".join(lines) + "\n"


def tex_gates(res):
    g = res["gates"]
    g4 = g["G4"]
    sc = res["singular"]
    r2, comp, g3 = g["G2_random"], g["G2_composition"], g["G3"]
    vd = ", ".join(str(g4["branch_subset_nonemptiness"]["p1"]["drop%d" % i]["vdim"]) for i in (3, 5, 6, 7, 10, 11))
    rows = [
        ("G0", "inputs",
         "both branch files regenerated from the archived system; SHA-256 beginning %s and %s, equal to the archived files"
         % (tt(g["G0"]["sha_rerun_plus"][:16]), tt(g["G0"]["sha_rerun_minus"][:16]))),
        ("G1", "ring maps",
         "$P(r_1)=0$ modulo $p_1$ and $P(r_2)=0$ modulo $p_2$, both primes below $2^{29}$; %d equations and %s integer coefficients per branch"
         % (g["G1"]["inputs"]["plus"]["equations"], n_(g["G1"]["inputs"]["plus"]["coefficients"]))),
        ("G2 (random)", "bound engine against exact resultants",
         "%s pairs kept of $2{,}000$ drawn; %s proven-zero coefficients, all zero; on the %s pairs with a nonzero resultant, %s weights compared and %d violations"
         % (n_(r2["cases"]), n_(r2["proven_zero_checked"]), n_(r2["weight_checked_pairs"]), n_(r2["weights_checked"]), r2["violations"])),
        ("G2 (composed)", "two propagated steps against the exact second resultant",
         "%d pairs kept; %s weights, %d violations; the order lower bound of the split variable checked in %d of %d split cases; "
         "%d proven-zero coefficients, all zero"
         % (comp["composition_cases"], n_(comp["composition_weights"]), comp["composition_violations"], comp["composition_order_checked"],
            comp["composition_split_cases"], comp["composition_proven_zero_checked"])),
        ("G3", "degree-drop image formula",
         "%d cases (drop $1$ in %d, drop $2$ in %d); %d mismatches against the exact formal resultant"
         % (g3["cases"], g3["drops"]["1"], g3["drops"]["2"], g3["mismatches"])),
        ("G4", "controls",
         "planted unit systems certified (one with a known exact constant); planted common-root systems and the planted split system not certified; "
         "%d of 6 branch controls finished and not certified, %d inconclusive at the $300$ s limit, %d crashed; "
         "each of the six systems is zero-dimensional at $p_1$ and $p_2$ (vdim %s) and the full subset has dimension $-1$"
         % (g4["branch_controls_finished"], g4["branch_controls_inconclusive"], g4["branch_controls_crashed"], vd)),
        ("G2 (real), G5", "exact levels against bounds and images",
         "%d exact polynomials (levels $1$ and $2$ of the five nodes of each branch); %d violations of the bound, %d mismatches of the image"
         % (g["G2_real_system"]["exact_levels_checked"], g["G2_real_system"]["violations"], g["G5"]["mismatches"])),
        ("Replay", "every leaf at $(p_2,r_2)$",
         "%d of %d leaves certified, no problem reported"
         % (sum(1 for b in ("plus", "minus") for v in res["replay"][b].values() if v["certified"] and not v["problems"]),
            sum(len(res["replay"][b]) for b in ("plus", "minus")))),
        ("Singular", "second implementation at $(p_1,r_1)$",
         "per branch %d digests and %d constants compared, %d mismatches, %d sign flips"
         % (sc["plus"]["digests_compared"], sc["plus"]["constants_compared"],
            len(sc["plus"]["digest_mismatches"]) + len(sc["plus"]["constant_mismatches"]), sc["plus"]["sign_flips"])),
    ]
    lines = ["% generated by make_tables.py from EXP-146 results.json; do not edit",
             "\\begin{table}[tbp]", "\\centering",
             "\\caption{The gates and independent checks of the Case 1 certificate (EXP-146), with the counts the run recorded. Every row passed; "
             "the third column states what was measured.}\\label{tab:gates}",
             "{\\footnotesize", "\\begin{tabular}{@{}P{1.9cm}P{3.4cm}P{9.5cm}@{}}", "\\toprule",
             "\\textbf{Gate} & \\textbf{Object} & \\textbf{Measured} \\\\", "\\midrule"]
    for a, b, c in rows:
        lines.append("%s & %s & %s \\\\" % (a, b, c))
    lines += ["\\bottomrule", "\\end{tabular}", "}", "\\end{table}"]
    return "\n".join(lines) + "\n"


def tex_mutants():
    m = load146("mutants.json")["mutants"]
    desc = [
        ("M1_res_bound_minus_1_G2_random", "every entry of the bound table lowered by $1$", "random pairs"),
        ("M1b_res_bound_minus_1_second_step_composition", "the same in the second composed step", "composed pairs"),
        ("M1c_res_bound_minus_1_second_step_w0_kept", "as the previous row, with the entry at $w=0$ left unlowered", "composed pairs"),
        ("M2_degree_drop_factor_removed_G3_60", "degree-drop factor removed", "$60$ cases"),
        ("M2_degree_drop_factor_removed_G3_500", "degree-drop factor removed", "$500$ cases"),
    ]
    rows = []
    for key, what, where in desc:
        d = m[key]
        if "violations" in d:
            rows.append((what, where, "%s (weight and order checks; %s weights checked)" % (n_(d["violations"]), n_(d["weights_checked"])), d["gate_fails"]))
        else:
            rows.append((what, where, "%d of %d cases" % (d["mismatches"], d["cases"]), d["gate_fails"]))
    lines = ["% generated by make_tables.py from EXP-146 mutants.json; do not edit",
             "\\begin{table}[tbp]", "\\centering",
             "\\caption{Planted defects of the bound engine and of the degree-drop formula, and what the gates measured on each (EXP-146). "
             "A violation counts a weight, or an order lower bound, at which a lowered bound falls below the exact value; every defect makes its gate fail.}"
             "\\label{tab:mutants}",
             "{\\footnotesize", "\\begin{tabular}{@{}P{5.6cm}P{2.6cm}P{3.6cm}P{1.8cm}@{}}", "\\toprule",
             "\\textbf{Defect} & \\textbf{Inputs} & \\textbf{Detected} & \\textbf{Gate fails} \\\\", "\\midrule"]
    for what, where, det, fails in rows:
        lines.append("%s & %s & %s & %s \\\\" % (what, where, det, "yes" if fails else "no"))
    lines += ["\\bottomrule", "\\end{tabular}", "}", "\\end{table}"]
    return "\n".join(lines) + "\n"


def tex_consts(res):
    import tables_data as td
    lines = ["% generated by make_tables.py from EXP-146 results.json and the third-prime values of tables_data.py; do not edit",
             "\\begin{table}[tbp]", "\\centering",
             "\\caption{The final constants of the leaves at three primes. $p_1=536870909$ is the prime of the tree and $p_2=536870879$ the prime of the replay "
             "(both read from the record); $p_3$ is a third prime at which the leaves were recomputed by scripts that do not use the experiment's code "
             "(plus branch $p_3=268435399$, minus branch $p_3=399999949$; n/r marks a leaf that was not recomputed). The pair "
             "$(V_{l_{3.4}},V_{l_{3.0}})$ of the node \\texttt{t.z.nz} gives zero at every prime, consistent with an exact zero; the last column counts the primes at which the constant is nonzero.}"
             "\\label{tab:consts}",
             "{\\footnotesize", "\\begin{tabular}{@{}llrrrr@{}}", "\\toprule",
             "\\textbf{Branch} & \\textbf{Leaf, pair} & \\textbf{$p_1$} & \\textbf{$p_2$} & \\textbf{$p_3$} & \\textbf{nonzero} \\\\", "\\midrule"]
    for b in ("plus", "minus"):
        third = td.THIRD[b]["leaves"]
        for nid in ("t.nz", "t.z.nz", "t.z.z"):
            node = [n for n in res["branches"][b]["nodes"] if n["id"] == nid][0]
            rep = {c["i"]: c["c"] for c in res["replay"][b][nid]["constants"]}
            t3 = dict(third.get(nid, []))
            for pr in node["last"]["pairs"]:
                c3 = n_(t3[pr["i"]]) if pr["i"] in t3 else "n/r"
                nzl = [pr["c"] != 0, rep[pr["i"]] != 0] + ([t3[pr["i"]] != 0] if pr["i"] in t3 else [])
                lines.append("%s & %s, %s & %s & %s & %s & %d of %d \\\\" % (
                    "$I_+$" if b == "plus" else "$I_-$", tt(nid), memtex(pr["i"]), n_(pr["c"]), n_(rep[pr["i"]]), c3,
                    sum(nzl), len(nzl)))
        if b == "plus":
            lines.append("\\midrule")
    lines += ["\\bottomrule", "\\end{tabular}", "}", "\\end{table}"]
    return "\n".join(lines) + "\n"


def verify_exp146():
    """Compare the numbers the text and the tables quote with the EXP-146 record. Returns a list of failures."""
    import tables_data as td
    bad = []
    res = load146("results.json")
    if res["verdict"] != "CONFIRMED":
        bad.append(("146", "verdict is not CONFIRMED"))
    if [res["branches"][b]["certified"] for b in ("plus", "minus")] != [True, True]:
        bad.append(("146", "a branch is not certified"))
    if res["primes"] != {"p1": 536870909, "r1": 505390653, "p2": 536870879, "r2": 12005842}:
        bad.append(("146", "primes differ from the ones quoted"))
    if round(res["seconds_total"]) != 1854 or round(res["branches"]["plus"]["seconds"]) != 252 or round(res["branches"]["minus"]["seconds"]) != 102:
        bad.append(("146", "run times differ from 1,854 s, 252 s, 102 s"))
    if res["singular"]["plus"]["seconds"] != 12.4 or res["singular"]["minus"]["seconds"] != 3.5:
        bad.append(("146", "Singular times differ from 12.4 s and 3.5 s"))
    log = (exp_dir("146") / "artifacts" / "run-log.txt").read_text(encoding="utf-8")
    if "(1392 s)" not in log:
        bad.append(("146", "G4 time 1392 s not in run-log.txt"))
    shape = {"t": (688, 0), "t.nz": (476, 212), "t.z": (14, 0), "t.z.nz": (12, 2), "t.z.z": (1, 0)}
    for b in ("plus", "minus"):
        for n in res["branches"][b]["nodes"]:
            d0, l0 = shape[n["id"]]
            m0 = n["last"]["members"][0]
            if (m0["d"], m0["L"]) != (d0, l0):
                bad.append(("146", "%s %s first member degree or L differ" % (b, n["id"])))
        nzs = {n["id"]: (n["nonzero_constants"], n["pairs_total"]) for n in res["branches"][b]["nodes"]}
        if nzs != {"t": (0, 2), "t.nz": (2, 2), "t.z": (0, 4), "t.z.nz": (3, 4), "t.z.z": (6, 6)}:
            bad.append(("146", "%s nonzero-constant counts differ" % b))
        if sum(1 for n in res["branches"][b]["nodes"] for s in n["steps"] for m in s["members"] if m["kind"] == "res") != 91:
            bad.append(("146", "%s chain resultant count differs from 91" % b))
    for b, leaves in td.THIRD_P1.items():
        for nid, vals in leaves.items():
            node = [n for n in res["branches"][b]["nodes"] if n["id"] == nid][0]
            if [p["c"] for p in node["last"]["pairs"]] != vals:
                bad.append(("146", "%s %s: constants at p1 differ from the review's" % (b, nid)))
    for b in ("plus", "minus"):
        for nid, pairs in td.THIRD[b]["leaves"].items():
            node = [n for n in res["branches"][b]["nodes"] if n["id"] == nid][0]
            if [i for i, _ in pairs] != [p["i"] for p in node["last"]["pairs"]]:
                bad.append(("146", "%s %s: pair ids of the third-prime list differ" % (b, nid)))
    arch = exp_dir("146") / "independent-checks" / "third-prime"
    texts = {"plus": (arch / "plus" / "out-p3.txt").read_text(encoding="utf-8") + (arch / "plus" / "out-tnz-p3.txt").read_text(encoding="utf-8"),
             "minus": (arch / "minus" / "run4.txt").read_text(encoding="utf-8")}
    for b in ("plus", "minus"):
        for nid, pairs in td.THIRD[b]["leaves"].items():
            for pid, v in pairs:
                if v != 0 and str(v) not in texts[b]:
                    bad.append(("146", "%s %s %s: p3 constant %d not in the archived third-prime output" % (b, nid, pid, v)))
    g = res["gates"]
    if not all(g[k]["pass"] for k in ("G0", "G1", "G2_random", "G2_composition", "G3", "G4", "G2_real_system", "G5")):
        bad.append(("146", "a gate did not pass"))
    if g["G2_real_system"]["exact_levels_checked"] != 118 or g["G5"]["exact_levels_checked"] != 118:
        bad.append(("146", "exact polynomial count differs from 118"))
    if (res["singular"]["plus"]["digests_compared"], res["singular"]["plus"]["constants_compared"]) != (153, 18):
        bad.append(("146", "Singular digest and constant counts differ from 153 and 18"))
    return bad


def write_generated():
    import tables_data as td
    for name, d in (("tab_exclusions.tex", td.EXCLUSIONS), ("tab_ladder.tex", td.LADDER), ("tab_cost.tex", td.COST),
                    ("tab_ablation.tex", ABLATION), ("tab_notation.tex", NOTATION)):
        (HERE / name).write_text(long_table(d) if d["label"] == "tab:ablation" else simple_table(d), encoding="utf-8")
    (HERE / "fig_window.tex").write_text(tex_window(), encoding="utf-8")
    (HERE / "fig_chain.tex").write_text(tex_chain(), encoding="utf-8")
    res146 = load146("results.json")
    (HERE / "tab_tree.tex").write_text(tex_tree(res146), encoding="utf-8")
    (HERE / "tab_gates.tex").write_text(tex_gates(res146), encoding="utf-8")
    (HERE / "tab_mutants.tex").write_text(tex_mutants(), encoding="utf-8")
    (HERE / "tab_consts.tex").write_text(tex_consts(res146), encoding="utf-8")


def main():
    check_only = "--check" in sys.argv
    bad = verify_rows()
    bad2, repro = verify_repro()
    bad2 = bad2 + verify_artifacts() + verify_exp146()
    for item in bad + bad2:
        print("FAIL", item)
    if bad or bad2:
        raise SystemExit(1)
    nr = [(r[0], HEADERS[i + 1]) for r in ROWS for i, c in enumerate(r[1:-1]) if c == NR]
    print(f"{len(ROWS)} atlas rows verified; cells not recorded (n/r): {len(nr)}")
    for num, col in nr:
        print(f"  EXP-{num}: {col}")
    if check_only:
        return
    (HERE / "tab_atlas.tex").write_text(tex_atlas(), encoding="utf-8")
    (HERE / "tab_repro.tex").write_text(tex_repro(repro), encoding="utf-8")
    (HERE / "fig_times.tex").write_text(tex_times(run_times()), encoding="utf-8")
    write_generated()
    print("wrote tab_atlas.tex, tab_repro.tex and the generated tables")


if __name__ == "__main__":
    main()
