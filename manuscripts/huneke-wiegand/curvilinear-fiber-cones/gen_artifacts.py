"""Transcribe the archived computation artifacts into the LaTeX fragments of main.tex.

No computation of mathematics happens here: every number is read from a committed artifact of
EXP-025, EXP-026 or EXP-069 (paths below) and written into ``generated/``. The block layout of
the strip figure is drawn from the closed formulas of the offset bases and its sizes are asserted
against the artifact rows. Run from anywhere:

    python manuscripts/huneke-wiegand/curvilinear-fiber-cones/gen_artifacts.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXPS = ROOT / "problems/commutative-algebra/huneke-wiegand/experiments"
E25 = EXPS / "EXP-025-curvilinear-primary-structure"
E26 = EXPS / "EXP-026-grevlex-staircase"
E69 = EXPS / "EXP-069-staircase-certificate-second-solver"
OUT = HERE / "generated"
SAMPLES = (4, 5, 6, 17, 73, 151, 300)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(name: str, text: str) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(text, encoding="utf-8", newline="\n")


def tt(value: str) -> str:
    return "\\texttt{" + value.replace("_", "\\_") + "}"


def thin(n: int) -> str:
    return f"{n:,}".replace(",", "\\,")


def intervals(values: set[int]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for v in sorted(values):
        if out and out[-1][1] == v - 1:
            out[-1] = (out[-1][0], v)
        else:
            out.append((v, v))
    return out


def blocks(p: int) -> list[tuple[int, int]]:
    return [(0, 0), (1, p), (3 * p, 4 * p - 2), (6 * p, 8 * p - 2), (8 * p, 10 * p - 2), (10 * p, 10 * p),
            (11 * p - 1, 12 * p - 1), (13 * p + 1, 14 * p - 2), (14 * p, 15 * p - 1), (16 * p, 16 * p),
            (17 * p - 1, 18 * p - 1)]


def main() -> None:
    r26 = load(E26 / "artifacts/results.json")
    a26 = load(E26 / "artifacts/audit.json")
    s26 = load(E26 / "artifacts/symbolic-certificate.json")
    b26 = load(E26 / "artifacts/attempt-1-budget.json")
    r25 = load(E25 / "artifacts/results.json")
    a25 = load(E25 / "artifacts/audit.json")
    r69 = load(E69 / "artifacts/results.json")
    rows = {row["p"]: row for row in r26["rows"]}
    assert r26["status"] == "PASS" and len(rows) == 297 == r26["completed_rows"]
    assert a26["status"] == "PASS" and s26["leaf_query_count"] == 16 and r69["summary"]["P1_same_obligations"]

    # ---- numbers.tex
    sm = r69["summary"]
    nums = {
        "ExpTwentyFiveSweepSeconds": f"{r25['elapsed_seconds']:.2f}",
        "ExpTwentySixSweepSeconds": f"{r26['elapsed_seconds']:.3f}",
        "ExpTwentySixAuditSeconds": f"{a26['elapsed_seconds']:.3f}",
        "ExpTwentySixCertificateSeconds": f"{s26['elapsed_seconds']:.3f}",
        "FirstAttemptSeconds": f"{b26['elapsed_seconds']:.2f}",
        "FirstAttemptRows": str(b26["completed_rows"]),
        "FirstAttemptLastP": str(b26["rows"][-1]["p"]),
        "CvcTotalSeconds": f"{sm['cvc5_total_seconds']:.2f}",
        "ZthreeRoundTripSeconds": f"{sm['z3_roundtrip_total_seconds']:.2f}",
        "SolverWallSeconds": f"{sm['wall_seconds']:.1f}",
        "SolverZthree": sm["solvers"]["z3"],
        "SolverCvc": sm["solvers"]["cvc5"],
        "SolverLimit": str(sm["solvers"]["tlimit_ms_per_leaf"] // 1000),
    }
    write("numbers.tex", "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in nums.items()))

    # ---- table of results
    lines = ["\\begin{tabular}{@{}rrrrrrrrr@{}}", "\\toprule",
             "$p$ & $q$ & $|G_p|$ & $\\dim(\\Cfiber_p)_2$ & $\\dim(\\Cfiber_p)_3$ & quadrics & binomials & zero & cubics, quartics\\\\",
             "\\midrule"]
    for p in SAMPLES:
        r = rows[p]
        h = r["hilbert_dimensions_0_to_6"]
        qp = r["quadratic_profile"]
        pr = r["reduced_basis_degree_profile"]
        assert h[:5] == [1, 10 * p, 22 * p, 24 * p - 1, 24 * p] and h[5:] == [24 * p, 24 * p]
        assert qp["total"] == 50 * p * p - 17 * p and 2 * qp["binomial"] == 77 * p * p - 49 * p + 2
        assert 2 * qp["monomial_zero"] == 23 * p * p + 15 * p - 2
        assert pr["3"] == 5 * p - 1 and pr["4"] == p - 2 and pr["5"] == 0 and pr["6"] == 0
        assert r["reduced_basis_total"] == 50 * p * p - 11 * p - 3
        lines.append(f"{p} & {thin(r['q'])} & {thin(r['variable_count'])} & {thin(h[2])} & {thin(h[3])} & "
                     f"{thin(qp['total'])} & {thin(qp['binomial'])} & {thin(qp['monomial_zero'])} & "
                     f"{pr['3']}, {pr['4']}\\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    write("table-results.tex", "\n".join(lines) + "\n")

    # ---- table of totals and row hashes
    lines = ["\\begin{tabular}{@{}rrl@{}}", "\\toprule",
             "$p$ & basis size & row hash (first 16 hex digits)\\\\", "\\midrule"]
    for p in SAMPLES:
        r = rows[p]
        lines.append(f"{p} & {thin(r['reduced_basis_total'])} & {tt(r['row_hash'][:16])}\\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    write("table-rowhashes.tex", "\n".join(lines) + "\n")

    # ---- aggregates (full 64 digits) and artifact manifest
    agg = [("primary sweep, computation EXP-025", r25["campaign_aggregate"]),
           ("primary recomputation, computation EXP-025", a25["audit_aggregate"]),
           ("Gr\\\"obner sweep, computation EXP-026", r26["campaign_aggregate"]),
           ("clique recomputation, computation EXP-026", a26["audit_aggregate"]),
           ("Presburger obligations, computation EXP-026", s26["query_aggregate"])]
    lines = ["\\begin{tabular}{@{}ll@{}}", "\\toprule", "computation & SHA-256 aggregate\\\\", "\\midrule"]
    for name, h in agg:
        assert len(h) == 64
        lines.append(f"{name} & \\texttt{{\\scriptsize {h}}}\\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    write("table-aggregates.tex", "\n".join(lines) + "\n")

    files = [(E25 / "artifacts/results.json", "EXP-025 results.json"),
             (E26 / "artifacts/results.json", "EXP-026 results.json"),
             (E26 / "artifacts/audit.json", "EXP-026 audit.json"),
             (E26 / "artifacts/symbolic-certificate.json", "EXP-026 symbolic-certificate.json"),
             (E69 / "artifacts/results.json", "EXP-069 results.json")]
    man = ["\\begin{tabular}{@{}lrl@{}}", "\\toprule", "artifact & bytes & SHA-256\\\\", "\\midrule"]
    for path, label in files:
        data = path.read_bytes()
        man.append(f"{label} & {thin(len(data))} & \\texttt{{\\scriptsize {hashlib.sha256(data).hexdigest()}}}\\\\")
    man += ["\\bottomrule", "\\end{tabular}"]
    write("table-manifest.tex", "\n".join(man) + "\n")


    # ---- premise hashes of the sweeps
    lines = ["\\begin{tabular}{@{}ll@{}}", "\\toprule", "premise file & SHA-256\\\\", "\\midrule"]
    for rel, h in r26["premise_hashes"].items():
        short = rel.split("experiments/")[1]
        for drop in ("-one-cubic-defining-ideal", "-extremal-betti-data", "-curvilinear-primary-structure"):
            short = short.replace(drop, "")
        lines.append(f"{tt(short)} & \\texttt{{\\scriptsize {h}}}\\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    write("table-premises.tex", "\n".join(lines) + "\n")


    # ---- obligations table
    kinds = {"cubic-completeness": "cubic family complete", "cubic-soundness": "cubic family sound",
             "quartic-completeness": "quartic family complete", "quartic-soundness": "quartic family sound"}
    leaves69 = {leaf["label"]: leaf for leaf in r69["leaves"]}
    lines = ["\\begin{tabular}{@{}llrrrl@{}}", "\\toprule",
             "obligation & content & Z3 (s) & Z3 on export (s) & cvc5 (s) & query digest\\\\", "\\midrule"]
    for leaf in s26["leaves"]:
        lab = leaf["label"]
        l69 = leaves69[lab]
        assert l69["digest_match"] and l69["stored_sha256"] == leaf["query_sha256"]
        assert leaf["result"] == l69["cvc5"]["result"] == l69["z3"]["result"] == "unsat"
        kind = kinds.get(lab, "tail standard, equal offset, smaller")
        lines.append(f"{tt(lab)} & {kind} & {leaf['elapsed_seconds']:.2f} & {l69['z3']['seconds']:.2f} & "
                     f"{l69['cvc5']['seconds']:.2f} & {tt(leaf['query_sha256'][:12])}\\\\")
    lines += ["\\midrule",
              f"total elapsed & & {s26['elapsed_seconds']:.2f} & {sm['z3_roundtrip_total_seconds']:.2f} & "
              f"{sm['cvc5_total_seconds']:.2f} & \\\\",
              "\\bottomrule", "\\end{tabular}"]
    write("table-obligations.tex", "\n".join(lines) + "\n")

    # ---- controls of EXP-069
    lines = ["\\begin{tabular}{@{}llllll@{}}", "\\toprule",
             "control & obligation perturbed & cvc5 model & Z3 & evaluator, perturbed & same model, original\\\\",
             "\\midrule"]
    for c in r69["controls"]:
        model = ", ".join(f"{k.replace('_', ' ')}={v}" for k, v in c["cvc5"]["model"].items())
        assert c["cvc5"]["result"] == c["z3"]["result"] == "sat"
        lines.append(f"{c['control']} & {tt(c['label'])} & {model} & {c['z3']['result']} & "
                     f"{str(c['evaluator']['verdict']).lower()} & "
                     f"{str(c['evaluator']['model_on_unperturbed_obligation']).lower()}\\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    write("table-controls069.tex", "\n".join(lines) + "\n")

    # ---- figure bodies
    frac = {}
    for p in SAMPLES:
        h = rows[p]["hilbert_dimensions_0_to_6"]
        lay = [1, h[1] - 1, h[2] - h[1], h[3] - h[2], h[4] - h[3]]
        assert lay == [1, 10 * p - 1, 12 * p, 2 * p - 1, 1] and sum(lay) == 24 * p
        frac[p] = [x / (24 * p) for x in lay]
    sym = ",".join(str(p) for p in SAMPLES)
    body = [f"\\begin{{tikzpicture}}\\begin{{axis}}[ybar stacked, width=0.9\\linewidth, height=6.2cm, "
            f"symbolic x coords={{{sym}}}, xtick=data, bar width=14pt, ymin=0, ymax=1, "
            "ylabel={share of $24p$}, xlabel={$p$}, legend style={at={(0.5,-0.28)},anchor=north,legend columns=5,"
            "font=\\footnotesize}, ymajorgrids, "
            "cycle list={{fill=layerA},{fill=layerB},{fill=layerC},{fill=layerD},{fill=layerE}}]"]
    names = ["degree 0", "degree 1", "degree 2", "degree 3", "degree 4"]
    for i in range(5):
        pts = " ".join(f"({p},{frac[p][i]:.5f})" for p in SAMPLES)
        body.append(f"\\addplot+[draw=none] coordinates {{{pts}}};")
    body.append("\\legend{" + ",".join(names) + "}\\end{axis}\\end{tikzpicture}")
    write("fig-layers.tex", "\n".join(body) + "\n")

    def series(fn) -> str:
        return " ".join(f"({p},{fn(rows[p])})" for p in SAMPLES)

    body = ["\\begin{tikzpicture}\\begin{axis}[width=0.9\\linewidth, height=6.4cm, xmode=log, ymode=log, "
            "xlabel={$p$}, ylabel={elements of the reduced basis}, legend pos=north west, "
            "legend style={font=\\footnotesize}, ymajorgrids, xmajorgrids]",
            f"\\addplot+[mark=*] coordinates {{{series(lambda r: r['reduced_basis_degree_profile']['2'])}}};",
            f"\\addplot+[mark=square*] coordinates {{{series(lambda r: r['reduced_basis_degree_profile']['3'])}}};",
            f"\\addplot+[mark=triangle*] coordinates {{{series(lambda r: r['reduced_basis_degree_profile']['4'])}}};",
            "\\legend{degree two, degree three, degree four}\\end{axis}\\end{tikzpicture}"]
    write("fig-profile.tex", "\n".join(body) + "\n")

    def frac_of(r, key):
        qp = r["quadratic_profile"]
        return f"{qp[key] / qp['total']:.5f}"

    body = ["\\begin{tikzpicture}\\begin{axis}[width=0.9\\linewidth, height=5.8cm, xmode=log, xlabel={$p$}, "
            "ylabel={share of the quadrics}, ymin=0, ymax=1, legend pos=north east, "
            "legend style={font=\\footnotesize}, ymajorgrids, xmajorgrids]",
            f"\\addplot+[mark=*] coordinates {{{series(lambda r: frac_of(r, 'binomial'))}}};",
            f"\\addplot+[mark=square*] coordinates {{{series(lambda r: frac_of(r, 'monomial_zero'))}}};",
            "\\addplot+[dashed,no marks] coordinates {(4,0.77) (300,0.77)};",
            "\\addplot+[dashed,no marks] coordinates {(4,0.23) (300,0.23)};",
            "\\legend{binomials, zero relations, limit $77/100$, limit $23/100$}\\end{axis}\\end{tikzpicture}"]
    write("fig-split.tex", "\n".join(body) + "\n")

    labs = [leaf["label"] for leaf in s26["leaves"]]
    symx = ",".join(labs)

    def tm(x: float) -> str:
        return f"{max(x, 0.001):.4f}"

    s26t = {leaf["label"]: leaf["elapsed_seconds"] for leaf in s26["leaves"]}
    body = [f"\\begin{{tikzpicture}}\\begin{{axis}}[ybar, width=\\linewidth, height=7.2cm, symbolic x coords={{{symx}}}, "
            "xtick=data, x tick label style={rotate=60,anchor=east,font=\\scriptsize}, ymode=log, ymin=0.0008, "
            "ymax=100, bar width=3.2pt, enlarge x limits=0.04, ylabel={seconds}, ymajorgrids, "
            "legend style={at={(0.5,1.02)},anchor=south,legend columns=3,font=\\footnotesize}]"]
    body.append("\\addplot+[draw=none] coordinates {" + " ".join(f"({l},{tm(s26t[l])})" for l in labs) + "};")
    body.append("\\addplot+[draw=none] coordinates {" + " ".join(f"({l},{tm(leaves69[l]['z3']['seconds'])})" for l in labs) + "};")
    body.append("\\addplot+[draw=none] coordinates {" + " ".join(f"({l},{tm(leaves69[l]['cvc5']['seconds'])})" for l in labs) + "};")
    body.append("\\legend{Z3 original, Z3 on the export, cvc5}\\end{axis}\\end{tikzpicture}")
    write("fig-times.tex", "\n".join(body) + "\n")

    # ---- strip figure for p = 4 (sizes asserted against the artifact row)
    p = 4
    q = 24 * p
    g: set[int] = set()
    for a, b in blocks(p):
        g |= set(range(a, b + 1))
    e2 = set(range(0, 2 * p + 1)) | set(range(3 * p, 5 * p - 1)) | set(range(6 * p, q))
    e3 = set(range(q)) - {6 * p - 1}
    e4 = set(range(q))
    h = rows[p]["hilbert_dimensions_0_to_6"]
    assert [len(g), len(e2), len(e3), len(e4)] == [h[1], h[2], h[3], h[4]]
    body = ["\\begin{tikzpicture}[x=0.115cm,y=0.62cm]"]
    for row, (name, s) in enumerate([("$E_1=G_4$", g), ("$E_2$", e2), ("$E_3$", e3), ("$E_4$", e4)]):
        y = -row
        body.append(f"\\node[anchor=east,font=\\footnotesize] at (-2,{y}) {{{name}}};")
        for a, b in intervals(s):
            body.append(f"\\fill[stripcol] ({a},{y - 0.3}) rectangle ({b + 1},{y + 0.3});")
    body.append(f"\\draw[->] (0,-3.7) -- ({q + 3},-3.7);")
    for tick in range(0, q + 1, 12):
        body.append(f"\\draw ({tick},-3.7) -- ({tick},-3.85) node[below,font=\\scriptsize] {{{tick}}};")
    body.append(f"\\draw[dashed] ({6 * p - 1},0.5) -- ({6 * p - 1},-3.6);")
    body.append(f"\\node[font=\\scriptsize,anchor=south] at ({6 * p - 1},0.5) {{$6p-1$}};")
    body.append("\\end{tikzpicture}")
    write("fig-strips.tex", "\n".join(body) + "\n")
    print("generated:", ", ".join(sorted(x.name for x in OUT.iterdir())))


if __name__ == "__main__":
    main()
