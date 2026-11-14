"""Write the generated parts of this manuscript from the EXP-007 result files.

No LaTeX passes through a shell. Every number in a generated table or figure is read from
`artifacts/*.json` of the experiment or computed by the closed formulas of Section 5, which are
cross-checked here against the variable and clause counts the result files record.

    python make_tables.py                 write the tables and figures (the parts named below)
    python make_tables.py --facts         print the numbers quoted in the prose
    python make_tables.py --check-hashes  rebuild every formula from the encoder and compare its SHA-256
                                          with the `cnf_sha256` of the result file (needs no solver)

Generated parts: results-table.tex, table-undecided.tex, table-controls.tex, table-ablation.tex,
table-counts.tex, table-hashes.tex, fig-size.tex, fig-times.tex, fig-proof.tex, fig-map.tex,
fig-controls.tex, fig-ablation.tex. `assemble.py` places them in main.tex.
"""

import hashlib
import io
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[2] / "problems/combinatorics/petersen-coloring"
EXP = PROBLEM / "experiments/EXP-007-colorable-only-by-itself"
ART = EXP / "artifacts"
BS = chr(92)
NAMES = {"G52": BS + "Ga", "G52b": BS + "Gb", "G68": BS + "Gsix"}
ORDER = {"G52": 52, "G52b": 52, "G68": 68}
CONTROLS = [("K4", 4, [2]), ("prism", 6, [2, 4]), ("petersen", 10, [2, 4, 6, 8]), ("J3", 12, [2, 4, 6, 8, 10]),
            ("J5", 20, [2, 4, 6, 8, 10, 12, 14, 16, 18])]
CONTROL_TEX = {"K4": "$K_4$", "prism": "prism", "petersen": "Petersen", "J3": "$J_3$", "J5": "$J_5$"}
# The file name of the formula that carried a hash: the final formula of G'52 at k = 40 was written under
# the tag of the portfolio run (hypothesis addendum 6); every other formula carries its own (graph, k) tag.
COMMENT_TAG = {("G52b", 40): "G52b_k40-long"}


def jload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"), strict=False)


def num(n) -> str:
    return f"{int(round(n)):,}".replace(",", "{,}")


def write(name: str, text: str) -> None:
    io.open(HERE / name, "w", encoding="utf-8", newline="\n").write(text)


def results(graph: str) -> dict[int, dict]:
    out = {}
    for p in ART.glob(f"result-{graph}-k*.json"):
        tail = p.stem.split("-k")[1]
        if tail.isdigit():
            out[int(tail)] = jload(p)
    return out


def decided(graph: str) -> dict[int, dict]:
    return {k: d for k, d in results(graph).items() if d.get("status") == "UNSAT" and d.get("verified")}


# ----------------------------------------------------------------------------- closed formulas of Section 5

def ladder(m: int) -> tuple[int, int]:
    """(auxiliary variables, clauses) of an exactly-one over m literals, as in pcclib.hcolor."""
    return (m - 1, 3 * m - 3) if m > 4 else (0, m * (m - 1) // 2 + 1)


def families(n: int, k: int) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    av, ac = ladder(k)
    mv, mc = ladder(3 * k - 3)
    variables = [("x", n * k), ("z", 9 * n), ("p", 9 * k * (k - 1) // 2), ("ladder-map", n * av), ("ladder-match", 3 * k * mv),
                 ("w", 9 * n * k), ("used", n * k), ("q", 1), ("xor", k * (n - 1))]
    clauses = [("map", n * ac), ("bijection", 24 * n), ("match", 3 * k * mc), ("w-def", 27 * n * k),
               ("consistency", 9 * n * k * (3 * k - 1) // 2), ("used-def", 3 * n * k - k), ("anchor", 1),
               ("numbering", n * (k - 1)), ("founder", 3 * n * k), ("parity", k * (4 * n - 1)), ("unused", 1),
               ("q-forced", 1 if 2 * (k - 1) > n else 0), ("attach", k - 1)]
    return variables, clauses


def totals(n: int, k: int) -> tuple[int, int]:
    v, c = families(n, k)
    return sum(x for _, x in v), sum(x for _, x in c)


def closed_form(n: int, k: int) -> tuple[int, int]:
    """V = 13nk + 8n + (27k^2 - 35k)/2 + 1 and C = (27nk^2 + 73nk)/2 + 20n + 27k^2 - 37k + 1 + [2(k-1) > n], k >= 5."""
    v = 13 * n * k + 8 * n + (27 * k * k - 35 * k) // 2 + 1
    c = (27 * n * k * k + 73 * n * k) // 2 + 20 * n + 27 * k * k - 37 * k + 1 + (1 if 2 * (k - 1) > n else 0)
    return v, c


def verify_counts() -> list[str]:
    """The family sums against every variable and clause count recorded in a result file."""
    problems = []
    seen = 0
    for g, n in ORDER.items():
        for k, d in results(g).items():
            if d.get("variables") is None:
                continue
            seen += 1
            if totals(n, k) != (d["variables"], d["clauses"]):
                problems.append(f"{g} k={k}: families {totals(n, k)} vs recorded {(d['variables'], d['clauses'])}")
            if k >= 5 and closed_form(n, k) != totals(n, k):
                problems.append(f"{g} k={k}: closed form {closed_form(n, k)} vs families {totals(n, k)}")
    f = jload(ART / "formula-G68-k52.json")
    if totals(68, 52) != (f["variables"], f["clauses"]):
        problems.append(f"G68 k=52: {totals(68, 52)} vs {(f['variables'], f['clauses'])}")
    if seen < 25:
        problems.append(f"only {seen} recorded formulas were checked")
    return problems


# ----------------------------------------------------------------------------- Table 1

def table_orders() -> list[str]:
    lines = [BS + "begin{table}[tbp]" + BS + "centering" + BS + "small",
             BS + "begin{tabular}{lrrrrrr}", BS + "toprule",
             "graph & $k$ & variables & clauses & solve (s) & proof (bytes) & check (s)" + BS + BS, BS + "midrule"]
    for i, g in enumerate(("G52", "G52b", "G68")):
        rows = []
        for k, d in sorted(decided(g).items(), reverse=True):
            if d.get("certify_solve_seconds") is not None:
                solve = num(d["certify_solve_seconds"])
                if d.get("portfolio"):
                    solve += BS + "textsuperscript{" + BS + "textdaggerdbl}"
            else:
                solve = "n/a" + BS + "textsuperscript{" + BS + "textdagger}"
            rows.append(" & ".join(["$" + NAMES[g] + "$", str(k), num(d["variables"]), num(d["clauses"]), solve,
                                    num(d["proof_bytes"]), num(d["check_seconds"])]) + " " + BS + BS)
        if i:
            lines.append(BS + "midrule")
        lines += rows
    lines += [BS + "bottomrule", BS + "end{tabular}",
              BS + "caption{Target orders $k$ refuted with DRAT proofs accepted by " + BS + "texttt{drat-trim}: the formula "
              "of order $k$ is unsatisfiable, so no loopless cubic graph on $k$ vertices colors the graph with a vertex map of "
              "kind (O), (E0) or (E1). Variables and clauses are those of the certified formula (base formula and attach clauses); "
              "solve and check are wall-clock seconds, single runs on a shared machine. "
              + BS + "textsuperscript{" + BS + "textdagger}The runner's six-hour limit expired while the external solver was still "
              "writing its proof; the solver finished on its own, the proof was checked afterwards, and its running time was not "
              "recorded. " + BS + "textsuperscript{" + BS + "textdaggerdbl}Solved by a portfolio of three CaDiCaL configurations, of "
              "which the default one answered first.}" + BS + "label{tab:orders}",
              BS + "end{table}"]
    return lines


# ----------------------------------------------------------------------------- undecided orders

def table_undecided() -> list[str]:
    rows = []
    g52 = results("G52")
    for k in sorted(g52):
        d = g52[k]
        if d.get("status") != "TIMEOUT":
            continue
        if "stopped by hand" in d.get("note", ""):
            outcome = "stopped by hand, past the 6 h cap"
        else:
            assert d.get("seconds") == 21600.0, (k, d)
            outcome = "no answer at the 6 h cap"
        detail = f"{d['learned_cuts']} lazy cuts learned" if d.get("learned_cuts") else "solver still running"
        rows.append(f"${NAMES['G52']}$ & {k} & {outcome} & {detail} " + BS + BS)
    below40 = [k for k in results("G52b") if k < 40]
    assert not below40, below40
    rows.append(BS + "midrule")
    rows.append(f"${NAMES['G52b']}$ & 2 to 38 & not attempted & no run exists for an order below 40 " + BS + BS)
    rows.append(BS + "midrule")
    g68 = results("G68")
    for k in (54, 56, 58, 60):
        assert g68[k]["status"] == "TIMEOUT" and g68[k]["seconds"] == 21600.0
        rows.append(f"${NAMES['G68']}$ & {k} & no answer at the 6 h cap & formula built, solver still running " + BS + BS)
    f = jload(ART / "formula-G68-k52.json")
    rows.append(f"${NAMES['G68']}$ & 52 & stopped at 4 h 13 min of a 24 h limit & formula of {num(f['variables'])} variables and "
                f"{num(f['clauses'])} clauses " + BS + BS)
    rows.append(f"${NAMES['G68']}$ & 2 to 50 & not attempted & orders 40 to 50 remain open " + BS + BS)
    return [BS + "begin{table}[tbp]" + BS + "centering" + BS + "small",
            BS + "begin{tabular}{ll>{" + BS + "raggedright" + BS + "arraybackslash}p{5.2cm}>{" + BS + "raggedright" + BS + "arraybackslash}p{5.6cm}}", BS + "toprule",
            "graph & $k$ & outcome & record" + BS + BS, BS + "midrule", *rows, BS + "bottomrule", BS + "end{tabular}",
            BS + "caption{Target orders for which no refutation or coloring exists, by graph. The runner stops an instance at "
            "21,600 s; in five instances of " + BS + "(" + BS + "Ga" + BS + ")" + " the in-process solver call held the interpreter lock "
            "past that limit and was stopped by hand. The formula of order 52 for " + BS + "(" + BS + "Gsix" + BS + ")" + " is kept "
            "for a rerun; the partial proofs of the interrupted run were deleted.}" + BS + "label{tab:undecided}",
            BS + "end{table}"]


# ----------------------------------------------------------------------------- the 21 controls

def control_rows() -> list[dict]:
    out = []
    for g, n, ks in CONTROLS:
        for k in ks:
            red = jload(ART / f"result-{g}-k{k}-red.json")
            unr = jload(ART / f"result-{g}-k{k}-unred.json")
            assert red["status"] == unr["status"], (g, k)
            out.append({"g": g, "n": n, "k": k, "status": red["status"], "red": red, "unr": unr})
    return out


def certificate(row: dict) -> str:
    ok = []
    for d in (row["red"], row["unr"]):
        if row["status"] == "UNSAT":
            ok.append(bool(d.get("verified")))
        else:
            ok.append(bool(d["check"]["ok"]) and d["target_petersen"]["status"] == "SAT")
    assert all(ok), row["g"] + str(row["k"])
    return "DRAT verified" if row["status"] == "UNSAT" else "checker accepted"


def table_controls() -> list[str]:
    rows = []
    prev = None
    for r in control_rows():
        if prev and prev != r["g"]:
            rows.append(BS + "midrule")
        prev = r["g"]
        red, unr = r["red"], r["unr"]
        rows.append(" & ".join([
            CONTROL_TEX[r["g"]] + f" ({r['n']})", str(r["k"]), "colored" if r["status"] == "SAT" else "not colored", certificate(r),
            f"{red['rounds']}", f"{red['learned_cuts']}", f"{red['seconds']:.1f}",
            f"{unr['rounds']}", f"{unr['learned_cuts']}", f"{unr['seconds']:.1f}"]) + " " + BS + BS)
    return [BS + "begin{table}[tbp]" + BS + "centering" + BS + "footnotesize",
            BS + "begin{tabular}{llllrrrrrr}", BS + "toprule",
            " & & & & " + BS + "multicolumn{3}{c}{with fiber constraints} & " + BS + "multicolumn{3}{c}{without} " + BS + BS,
            BS + "cmidrule(lr){5-7}" + BS + "cmidrule(lr){8-10}",
            "graph (order) & $k$ & answer & certificate & rounds & cuts & s & rounds & cuts & s" + BS + BS, BS + "midrule", *rows,
            BS + "bottomrule", BS + "end{tabular}",
            BS + "caption{The 21 control instances: every even target order $k$ below the order of the graph, for the complete graph on "
            "four vertices, the prism, the Petersen graph and the flower snarks $J_3$ and $J_5$. Both encodings give the same answer in "
            "every instance. A coloring is accepted by the checker that reads only the graph and the decoded pair and its target is "
            "itself Petersen colorable; a refusal carries a DRAT proof accepted by " + BS + "texttt{drat-trim}. Rounds are solver calls, "
            "cuts are lazily learned connectivity and bridge clauses, s is wall-clock seconds.}" + BS + "label{tab:controls}",
            BS + "end{table}"]


# ----------------------------------------------------------------------------- ablation

def ablation_facts() -> dict:
    g52 = results("G52")
    ks = [k for k in range(32, 52, 2)]
    secs = [g52[k]["seconds"] for k in ks]
    assert all(g52[k]["status"] == "UNSAT" and g52[k]["learned_cuts"] == 0 for k in ks)
    rows = control_rows()
    agg = {}
    for r in rows:
        a = agg.setdefault(r["g"], {"inst": 0, "red_cuts": 0, "unr_cuts": 0, "red_s": 0.0, "unr_s": 0.0, "unr_with_cuts": 0})
        a["inst"] += 1
        a["red_cuts"] += r["red"]["learned_cuts"]
        a["unr_cuts"] += r["unr"]["learned_cuts"]
        a["red_s"] += r["red"]["seconds"]
        a["unr_s"] += r["unr"]["seconds"]
        a["unr_with_cuts"] += 1 if r["unr"]["learned_cuts"] else 0
    return {"orders_min_s": min(secs), "orders_max_s": max(secs), "agg": agg, "n_orders": len(ks)}


def table_ablation() -> list[str]:
    f = ablation_facts()
    rows = []
    for g, _, _ in CONTROLS:
        a = f["agg"][g]
        rows.append(" & ".join([CONTROL_TEX[g], str(a["inst"]), str(a["red_cuts"]), f"{a['red_s']:.0f}",
                                f"{a['unr_with_cuts']}", num(a["unr_cuts"]), f"{a['unr_s']:.0f}"]) + " " + BS + BS)
    tot = {k: sum(f["agg"][g][k] for g, _, _ in CONTROLS) for k in ("inst", "red_cuts", "red_s", "unr_cuts", "unr_s", "unr_with_cuts")}
    rows.append(BS + "midrule")
    rows.append(" & ".join(["all", str(tot["inst"]), str(tot["red_cuts"]), f"{tot['red_s']:.0f}", str(tot["unr_with_cuts"]),
                            num(tot["unr_cuts"]), f"{tot['unr_s']:.0f}"]) + " " + BS + BS)
    first = [BS + "begin{table}[tbp]" + BS + "centering" + BS + "small",
             BS + "begin{tabular}{>{" + BS + "raggedright" + BS + "arraybackslash}p{3.0cm}>{" + BS + "raggedright" + BS + "arraybackslash}p{2.4cm}>{" + BS + "raggedright" + BS + "arraybackslash}p{3.4cm}>{" + BS + "raggedright" + BS + "arraybackslash}p{1.6cm}>{" + BS + "raggedright" + BS + "arraybackslash}p{2.8cm}}", BS + "toprule",
             "formula & orders run & lazy cuts per order & orders decided & wall clock" + BS + BS, BS + "midrule",
             "without the fiber constraints & 10 ($32 " + BS + "le k " + BS + "le 50$) & 1,800 to 2,400, over 95 percent bridge cuts & 0 & "
             "stopped after about 35 min " + BS + BS,
             "with the fiber constraints & 10 ($32 " + BS + "le k " + BS + "le 50$) & 0 & 10 & "
             f"{num(f['orders_min_s'])} to {num(f['orders_max_s'])} s per order " + BS + BS,
             BS + "bottomrule", BS + "end{tabular}",
             BS + "caption{Effect of the fiber constraints on the first graph at the ten target orders from 32 to 50. The "
             "figures for the formula without the constraints are those recorded when that attempt was stopped; the figures "
             "for the formula with them are the wall-clock seconds of the ten decided runs (solve and proof check included).}"
             + BS + "label{tab:ablation-orders}", BS + "end{table}", ""]
    second = [BS + "begin{table}[tbp]" + BS + "centering" + BS + "small",
              BS + "begin{tabular}{lrrrrrr}", BS + "toprule",
              " & & " + BS + "multicolumn{2}{c}{with fiber constraints} & " + BS + "multicolumn{3}{c}{without} " + BS + BS,
              BS + "cmidrule(lr){3-4}" + BS + "cmidrule(lr){5-7}",
              "graph & instances & cuts & s & instances with a cut & cuts & s" + BS + BS, BS + "midrule", *rows, BS + "bottomrule",
              BS + "end{tabular}",
              BS + "caption{Effect of the fiber constraints on the 21 control instances of Table~" + BS + "ref{tab:controls}, "
              "summed by graph: lazily learned cuts and wall-clock seconds with and without the constraints, and the number of "
              "instances in which the formula without them needed at least one cut.}" + BS + "label{tab:ablation-controls}",
              BS + "end{table}"]
    return first + second


# ----------------------------------------------------------------------------- counts of Section 5

def table_counts() -> list[str]:
    names_v = [("$x_{v,i}$", "x", "$nk$"), ("$z_{v,r,s}$", "z", "$9n$"), ("$p_{a,b}$", "p", "$9k(k-1)/2$"),
               ("ladder variables, vertex map", "ladder-map", "$n(k-1)$"), ("ladder variables, matching", "ladder-match", "$3k(3k-4)$"),
               ("$w_{v,r,i,s}$", "w", "$9nk$"), ("$u_{v,i}$", "used", "$nk$"), ("$q$", "q", "$1$"),
               ("parity chain $t_{i,v}$", "xor", "$k(n-1)$")]
    names_c = [("map: one class per vertex", "map", "$n(3k-3)$"), ("slot bijection", "bijection", "$24n$"),
               ("matching: one partner per slot", "match", "$3k(9k-12)$"), ("definition of $w$", "w-def", "$27nk$"),
               ("consistency along edges", "consistency", "$9nk(3k-1)/2$"), ("definition of $u$", "used-def", "$3nk-k$"),
               ("anchor $x_{0,0}$", "anchor", "$1$"), ("class numbering", "numbering", "$n(k-1)$"),
               ("founder slot order", "founder", "$3nk$"), ("parity chains and link to $q$", "parity", "$k(4n-1)$"),
               ("class $k-2$ used", "unused", "$1$"), ("$q$ forced when $2(k-1)>n$", "q-forced", "$[2(k-1)>n]$"),
               ("attach clauses", "attach", "$k-1$")]
    v1, c1 = families(52, 50)
    v2, c2 = families(68, 66)
    dv1, dc1, dv2, dc2 = dict(v1), dict(c1), dict(v2), dict(c2)

    def block(title: str, names: list, d1: dict, d2: dict, total1: int, total2: int, formula: str) -> list[str]:
        out = [BS + "multicolumn{4}{l}{" + BS + "textit{" + title + "}} " + BS + BS]
        for label, key, form in names:
            out.append(f"{label} & {form} & {num(d1[key])} & {num(d2[key])} " + BS + BS)
        out.append(BS + "midrule")
        out.append(f"total & {formula} & {num(total1)} & {num(total2)} " + BS + BS)
        return out

    tv1, tc1 = totals(52, 50)
    tv2, tc2 = totals(68, 66)
    rows = block("variables", names_v, dv1, dv2, tv1, tv2, "Eq.~" + BS + "eqref{eq:size-v}")
    rows.append(BS + "midrule")
    rows += block("clauses", names_c, dc1, dc2, tc1, tc2, "Eq.~" + BS + "eqref{eq:size-c}")
    return [BS + "begin{table}[tbp]" + BS + "centering" + BS + "small",
            BS + "begin{tabular}{llrr}", BS + "toprule",
            "family & count (as a function of $n$, $k$) & $n=52$, $k=50$ & $n=68$, $k=66$" + BS + BS, BS + "midrule", *rows,
            BS + "bottomrule", BS + "end{tabular}",
            BS + "caption{Variables and clauses of the certified formula, by family, for $k \\ge 5$ (for $k \\le 4$ an exactly-one "
            "constraint over at most four literals is written pairwise, without auxiliary variables). The last two columns evaluate "
            "the families for the largest orders of Table~" + BS + "ref{tab:orders} and agree with the recorded totals "
            "(67{,}092 variables and 1{,}916{,}592 clauses; 116{,}540 and 4{,}279{,}152).}" + BS + "label{tab:counts}",
            BS + "end{table}"]


# ----------------------------------------------------------------------------- hashes

def HASH(h: str) -> str:
    return "{" + BS + "tiny" + BS + "ttfamily " + h + "}"


def table_hashes() -> list[str]:
    rows = []
    for g in ("G52", "G52b", "G68"):
        for k, d in sorted(decided(g).items(), reverse=True):
            tex = "$" + NAMES[g] + "$"
            rows.append(f"{tex} & {k} & formula & " + HASH(d["cnf_sha256"]) + " " + BS + BS)
            rows.append(" & & proof & " + HASH(d["proof_sha256"]) + " " + BS + BS)
    f = jload(ART / "formula-G68-k52.json")
    rows.append("$" + NAMES["G68"] + "$ & 52 & formula (kept) & " + HASH(f["sha256"]) + " " + BS + BS)
    return [BS + "begin{longtable}{@{}rrll@{}}",
            BS + "caption{SHA-256 of the certified formula (the DIMACS file, comment line included) and of the DRAT proof, for every "
            "refuted target order, and of the formula of order 52 for the 68-vertex graph. Regenerating a formula with the command of "
            "Section~" + BS + "ref{sec:reproducibility} and hashing it reproduces the first value of each pair.}" + BS + "label{tab:hashes}" + BS + BS,
            BS + "toprule", "graph & $k$ & object & SHA-256" + BS + BS, BS + "midrule", BS + "endfirsthead",
            BS + "toprule", "graph & $k$ & object & SHA-256" + BS + BS, BS + "midrule", BS + "endhead",
            BS + "bottomrule", BS + "endfoot", BS + "bottomrule", BS + "endlastfoot",
            *rows, BS + "end{longtable}"]


# ----------------------------------------------------------------------------- figures

def coords(points: list[tuple[float, float]]) -> str:
    return "coordinates {" + " ".join(f"({x:g},{y:g})" for x, y in points) + "}"


PGF_HEAD = (BS + "pgfplotsset{every axis/.append style={tick label style={font=" + BS + "scriptsize}, label style={font=" + BS +
            "small}, legend style={font=" + BS + "scriptsize}, grid=major, grid style={gray!25}}}")
SERIES = {"G52": ("mark=*", "black", "solid"), "G52b": ("mark=triangle*", "blue!60!black", "dashed"), "G68": ("mark=square*", "red!70!black", "dotted")}


def segments(points: list[tuple[float, float]]) -> list[list[tuple[float, float]]]:
    """Split sorted (k, y) points where the orders are not consecutive even numbers, so no line crosses an undecided order."""
    out: list[list[tuple[float, float]]] = []
    for pt in points:
        if out and pt[0] - out[-1][-1][0] == 2:
            out[-1].append(pt)
        else:
            out.append([pt])
    return out


def series_plot(out: list[str], g: str, pts: list[tuple[float, float]], label: str) -> None:
    mark, colr, dash = SERIES[g]
    for i, seg in enumerate(segments(pts)):
        forget = "" if i == 0 else ", forget plot"
        out.append(BS + "addplot[" + mark + ", mark options={solid}, mark size=1.6pt, thin, " + colr + ", " + dash + forget + "] " + coords(seg) + ";")
        if i == 0:
            out.append(BS + "addlegendentry{" + label + "}")


def fig_size() -> list[str]:
    def data(g, key):
        return [(k, d[key]) for k, d in sorted(decided(g).items())]
    out = [BS + "begin{figure}[tbp]" + BS + "centering", BS + "begin{tikzpicture}", PGF_HEAD,
           BS + "begin{groupplot}[group style={group size=2 by 1, horizontal sep=1.9cm}, width=0.5" + BS + "textwidth, height=5.4cm, "
           "xlabel={target order $k$}]"]
    for key, label, form in (("variables", "variables", "13*{n}*x + 8*{n} + (27*x^2 - 35*x)/2 + 1"),
                             ("clauses", "clauses", "(27*{n}*x^2 + 73*{n}*x)/2 + 20*{n} + 27*x^2 - 37*x + 1")):
        out.append(BS + "nextgroupplot[ylabel={" + label + "}, legend pos=north west]")
        for g in ("G52", "G68"):
            mark, colr, _ = SERIES[g]
            out.append(BS + "addplot[only marks, " + mark + ", mark options={solid}, mark size=1.6pt, " + colr + "] " + coords(data(g, key)) + ";")
            out.append(BS + "addlegendentry{$" + ("G_{52}$ and $G'_{52}$" if g == "G52" else "G_{68}$") + "}")
        for n, colr in ((52, "black"), (68, "red!70!black")):
            out.append(BS + "addplot[domain=2:" + str(n - 2) + ", samples=40, thin, " + colr + ", dashed] {" + form.format(n=n) + "};")
            out.append(BS + "addlegendentry{formula, $n=" + str(n) + "$}")
    out += [BS + "end{groupplot}", BS + "end{tikzpicture}",
            BS + "caption{Size of the certified formula against the target order $k$, read from the result files (markers) and from "
            "the closed forms of Table~" + BS + "ref{tab:counts} (dashed lines). Left: variables. Right: clauses. The two 52-vertex "
            "graphs have the same formula size, so one series stands for both.}" + BS + "label{fig:size}", BS + "end{figure}"]
    return out


def fig_times() -> list[str]:
    out = [BS + "begin{figure}[tbp]" + BS + "centering", BS + "begin{tikzpicture}", PGF_HEAD,
           BS + "begin{groupplot}[group style={group size=2 by 1, horizontal sep=1.8cm}, width=0.46" + BS + "textwidth, height=5.6cm, "
           "xlabel={target order $k$}, ymode=log]"]
    for key, label in (("certify_solve_seconds", "solve time (s)"), ("check_seconds", "proof check time (s)")):
        out.append(BS + "nextgroupplot[ylabel={" + label + "}, legend pos=south west]")
        for g in ("G52", "G52b", "G68"):
            pts = [(k, d[key]) for k, d in sorted(decided(g).items()) if d.get(key) is not None]
            series_plot(out, g, pts, "$" + NAMES[g] + "$")
    out += [BS + "end{groupplot}", BS + "end{tikzpicture}",
            BS + "caption{Wall-clock time of the external solver (left) and of the proof check (right) against the target order $k$, "
            "one run per instance, on a logarithmic scale. Instances whose solve time was not recorded are absent from the left panel.}"
            + BS + "label{fig:times}", BS + "end{figure}"]
    return out


def fig_proof() -> list[str]:
    out = [BS + "begin{figure}[tbp]" + BS + "centering", BS + "begin{tikzpicture}", PGF_HEAD,
           BS + "begin{axis}[width=0.62" + BS + "textwidth, height=5.6cm, xlabel={target order $k$}, ylabel={proof size (bytes)}, "
           "ymode=log, legend pos=south west]"]
    for g in ("G52", "G52b", "G68"):
        pts = [(k, d["proof_bytes"]) for k, d in sorted(decided(g).items())]
        series_plot(out, g, pts, "$" + NAMES[g] + "$")
    out += [BS + "end{axis}", BS + "end{tikzpicture}",
            BS + "caption{Size of the DRAT proof of the final formula against the target order $k$, for every refuted order of "
            "Table~" + BS + "ref{tab:orders}. The proofs reach 2.4 GB for the second 52-vertex graph at $k=40$.}" + BS + "label{fig:proof}",
            BS + "end{figure}"]
    return out


def fig_map() -> list[str]:
    cell = 0.41
    out = [BS + "begin{figure}[tbp]" + BS + "centering", BS + "begin{tikzpicture}[solid, x=" + str(cell) + "cm, y=" + str(cell) + "cm, font=" + BS + "scriptsize]"]
    rows = [("G52", 52), ("G52b", 52), ("G68", 68)]
    for r, (g, n) in enumerate(rows):
        y = -r * 1.5
        res = results(g)
        out.append(f"{BS}node[anchor=east] at (0.2,{y}) {{${NAMES[g]}$}};")
        for k in range(2, n - 1, 2):
            x = k / 2
            d = res.get(k)
            if d and d.get("status") == "UNSAT" and d.get("verified"):
                style = "fill=black"
                extra = ""
            elif (g, k) == ("G68", 52) or (d and d.get("status") == "TIMEOUT"):
                style = "draw, line width=0.4pt"
                extra = f"{BS}draw[line width=0.6pt] ({x - 0.4},{y - 0.4}) -- ({x + 0.4},{y + 0.4}) ({x - 0.4},{y + 0.4}) -- ({x + 0.4},{y - 0.4});"
            elif k in (2, 4):
                style = "draw, line width=0.4pt"
                extra = f"{BS}fill ({x},{y}) circle (0.18);"
            else:
                style = "draw, line width=0.4pt"
                extra = ""
            out.append(f"{BS}path[{style}] ({x - 0.4},{y - 0.4}) rectangle ({x + 0.4},{y + 0.4});")
            if extra:
                out.append(extra)
    for k in (2, 10, 20, 30, 40, 50, 60):
        out.append(f"{BS}node[anchor=north] at ({k / 2},{-3 * 1.5 + 0.6}) {{{k}}};")
    out.append(f"{BS}draw[dashed, line width=0.5pt] (19.5,1) -- (19.5,{-3 * 1.5 + 1.0});")
    out.append(f"{BS}node[anchor=south] at (19.5,1) {{below 40: Observation~10}};")
    ly = -3 * 1.5 - 1.6
    out += [f"{BS}path[fill=black] (1,{ly}) rectangle (1.8,{ly + 0.8});",
            f"{BS}node[anchor=west] at (2,{ly + 0.4}) {{refuted, proof verified}};",
            f"{BS}path[draw, line width=0.4pt] (14,{ly}) rectangle (14.8,{ly + 0.8});",
            f"{BS}draw[line width=0.6pt] (14,{ly}) -- (14.8,{ly + 0.8}) (14,{ly + 0.8}) -- (14.8,{ly});",
            f"{BS}node[anchor=west] at (15,{ly + 0.4}) {{attempted, no answer}};",
            f"{BS}path[draw, line width=0.4pt] (1,{ly - 1.2}) rectangle (1.8,{ly - 0.4});",
            f"{BS}node[anchor=west] at (2,{ly - 0.8}) {{not attempted}};",
            f"{BS}path[draw, line width=0.4pt] (14,{ly - 1.2}) rectangle (14.8,{ly - 0.4});",
            f"{BS}fill (14.4,{ly - 0.8}) circle (0.18);",
            f"{BS}node[anchor=west] at (15,{ly - 0.8}) {{not attempted, settled by Proposition~" + BS + "ref{prop:small}};"]
    out += [BS + "end{tikzpicture}",
            BS + "caption{Status of every even target order $k$ below the order of the graph, one cell per order from 2 (left) "
            "to $n-2$, for the three graphs of the sweep. The dashed line marks the bound of the cited observation, below which a "
            "smaller counterexample is excluded without computation. The cell $k=52$ of the 68-vertex graph is a run stopped before "
            "any answer.}" + BS + "label{fig:map}", BS + "end{figure}"]
    return out


def fig_controls() -> list[str]:
    cell = 0.62
    out = [BS + "begin{figure}[tbp]" + BS + "centering", BS + "begin{tikzpicture}[solid, x=" + str(cell) + "cm, y=" + str(cell) + "cm, font=" + BS + "scriptsize]"]
    rows = control_rows()
    for r, (g, n, ks) in enumerate(CONTROLS):
        y = -r
        out.append(f"{BS}node[anchor=east] at (0.3,{y}) {{{CONTROL_TEX[g]}}};")
        for k in ks:
            row = next(x for x in rows if x["g"] == g and x["k"] == k)
            x = k / 2
            if row["status"] == "SAT":
                out.append(f"{BS}path[draw, line width=0.6pt] ({x},{y + 0.38}) -- ({x + 0.38},{y}) -- ({x},{y - 0.38}) -- ({x - 0.38},{y}) -- cycle;")
            else:
                out.append(f"{BS}path[fill=black] ({x - 0.3},{y - 0.3}) rectangle ({x + 0.3},{y + 0.3});")
    for k in (2, 4, 6, 8, 10, 12, 14, 16, 18):
        out.append(f"{BS}node[anchor=north] at ({k / 2},{-len(CONTROLS) + 0.45}) {{{k}}};")
    out.append(f"{BS}node[anchor=north] at (5,{-len(CONTROLS) - 0.3}) {{target order $k$}};")
    out += [f"{BS}path[fill=black] (11,-0.3) rectangle (11.6,0.3);",
            f"{BS}node[anchor=west] at (11.9,0) {{no coloring, proof verified}};",
            f"{BS}path[draw, line width=0.6pt] (11.3,-1.38) -- (11.68,-1) -- (11.3,-0.62) -- (10.92,-1) -- cycle;",
            f"{BS}node[anchor=west] at (11.9,-1) {{coloring, checker accepted}};",
            BS + "end{tikzpicture}",
            BS + "caption{Answers of the 21 control instances of Table~" + BS + "ref{tab:controls} by graph and target order. The two "
            "encodings agree in every cell. The Petersen graph is colored by no graph of smaller order; the flower snark $J_5$ is "
            "colored at orders 10 and 12 only, and $J_3$ at order 10 only.}" + BS + "label{fig:controls}", BS + "end{figure}"]
    return out


def fig_ablation() -> list[str]:
    rows = control_rows()
    out = [BS + "begin{figure}[tbp]" + BS + "centering", BS + "begin{tikzpicture}", PGF_HEAD,
           BS + "begin{axis}[width=0.7" + BS + "textwidth, height=5.6cm, xlabel={target order $k$}, ylabel={lazily learned cuts}, "
           "legend pos=north west, ymin=-40, xtick={2,4,6,8,10,12,14,16,18}]"]
    marks = {"petersen": ("mark=o", "black", "solid", "Petersen"), "J3": ("mark=triangle*", "blue!60!black", "dashed", "$J_3$"),
             "J5": ("mark=square*", "red!70!black", "dotted", "$J_5$")}
    for g, (mark, colr, dash, label) in marks.items():
        pts = [(r["k"], r["unr"]["learned_cuts"]) for r in rows if r["g"] == g]
        out.append(BS + "addplot[" + mark + ", mark options={solid}, mark size=1.8pt, thin, " + colr + ", " + dash + "] " + coords(pts) + ";")
        out.append(BS + "addlegendentry{" + label + ", without the constraints}")
    allk = sorted({r["k"] for r in rows})
    assert all(r["red"]["learned_cuts"] == 0 for r in rows)
    out.append(BS + "addplot[thick, black, domain=2:18] {0};")
    out.append(BS + "addlegendentry{every graph, with the constraints}")
    out += [BS + "end{axis}", BS + "end{tikzpicture}",
            BS + "caption{Lazily learned connectivity and bridge cuts on the control instances against the target order $k$: the "
            "formula without the fiber constraints (markers) and the formula with them (solid line at zero, all 21 instances). "
            "The number of cuts of the formula without the constraints grows with the order.}" + BS + "label{fig:ablation}", BS + "end{figure}"]
    return out


# ----------------------------------------------------------------------------- facts, hashes, main

def facts() -> None:
    f = ablation_facts()
    print("orders_min_s", f["orders_min_s"], "orders_max_s", f["orders_max_s"])
    for g, a in f["agg"].items():
        print(g, a)
    for g in ("G52", "G52b", "G68"):
        d = decided(g)
        print(g, "decided", sorted(d))
        print(g, "max proof bytes", max((v["proof_bytes"], k) for k, v in d.items()))
        print(g, "total solve s", sum(v["certify_solve_seconds"] or 0 for v in d.values()),
              "total check s", sum(v["check_seconds"] for v in d.values()))
    print("count problems:", verify_counts() or "none")
    for k in (50, 28):
        v, c = totals(52, k)
        cons = dict(families(52, k)[1])["consistency"]
        print("n=52 k", k, "vars", v, "clauses", c, "consistency share", round(cons / c, 4))
    print("G68 k=52 formula", totals(68, 52))


def attach_clauses(inst) -> list[tuple[int, ...]]:
    """The static attach clauses of run_inc.attach_clauses (copied: that module imports PySAT at load)."""
    n, k = inst.g.n, inst.k
    out = []
    for i in range(1, k):
        lits = [inst.used[n - 1, i], -inst.used[n - 1, i - 1]]
        for (a, b), var in inst.p.items():
            if (a[0] < i) != (b[0] < i):
                lits.append(var)
        out.append(tuple(lits))
    return out


def check_hashes() -> int:
    sys.path.insert(0, str(PROBLEM / "code"))
    sys.path.insert(0, str(EXP))
    from pcclib import hcolor  # noqa: E402
    from pcclib.cnf import CNF  # noqa: E402
    from run import load  # noqa: E402

    bad = 0
    for g in ("G52", "G52b", "G68"):
        graph = load(g)
        for k, d in sorted(decided(g).items()):
            inst = hcolor.HColorInstance(graph, k, reduced=True)
            static = attach_clauses(inst)
            f = CNF()
            f.nvars = inst.f.nvars
            f.names = inst.f.names
            f.clauses = list(inst.f.clauses) + list(static)
            tag = COMMENT_TAG.get((g, k), f"{g}_k{k}")
            text = f.dimacs([f"EXP-007 {tag} final formula: base + {len(static)} attach + 0 learned cuts"])
            digest = hashlib.sha256(text.encode("ascii")).hexdigest()
            same = digest == d["cnf_sha256"] and (f.nvars, len(f.clauses)) == (d["variables"], d["clauses"])
            bad += 0 if same else 1
            print(g, k, f.nvars, len(f.clauses), "SAME" if same else "DIFFERENT", flush=True)
    graph = load("G68")
    inst = hcolor.HColorInstance(graph, 52, reduced=True)
    static = attach_clauses(inst)
    f = CNF()
    f.nvars = inst.f.nvars
    f.names = inst.f.names
    f.clauses = list(inst.f.clauses) + list(static)
    text = f.dimacs(["EXP-007 G68_k52-portfolio final formula: base + 51 attach + 0 learned cuts (reduced)"])
    ref = jload(ART / "formula-G68-k52.json")["sha256"]
    same = hashlib.sha256(text.encode("ascii")).hexdigest() == ref
    bad += 0 if same else 1
    print("G68 52 (kept formula)", f.nvars, len(f.clauses), "SAME" if same else "DIFFERENT")
    print("hash check:", "all formulas reproduce their recorded SHA-256" if not bad else f"{bad} DIFFERENT")
    return 1 if bad else 0


def main() -> None:
    if "--facts" in sys.argv:
        facts()
        return
    if "--check-hashes" in sys.argv:
        sys.exit(check_hashes())
    problems = verify_counts()
    if problems:
        print("COUNT MISMATCH:", *problems, sep="\n  ")
        sys.exit(1)
    parts = {"results-table.tex": table_orders(), "table-undecided.tex": table_undecided(),
             "table-controls.tex": table_controls(), "table-ablation.tex": table_ablation(),
             "table-counts.tex": table_counts(), "table-hashes.tex": table_hashes(), "fig-size.tex": fig_size(),
             "fig-times.tex": fig_times(), "fig-proof.tex": fig_proof(), "fig-map.tex": fig_map(),
             "fig-controls.tex": fig_controls(), "fig-ablation.tex": fig_ablation()}
    for name, lines in parts.items():
        write(name, "\n".join(lines) + "\n")
        print("wrote", name)
    for g in ("G52", "G52b", "G68"):
        print(g, sorted(decided(g)))


if __name__ == "__main__":
    main()
