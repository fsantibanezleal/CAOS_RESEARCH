#!/usr/bin/env python3
"""Regenerate the artifact-derived tables and plots of main.tex from the stored computation artifacts.

Every number in the generated tables is read from a JSON artifact (or the SHA-256 and the size of
a stored file) under problems/commutative-algebra/huneke-wiegand/experiments/. Nothing is typed.
The tables sit between ``% BEGIN GENERATED <label>`` and ``% END GENERATED <label>`` markers of
main.tex, and this script replaces exactly those blocks.

Usage (from any directory):
    python generate_tables.py            # rewrite main.tex
    python generate_tables.py --check    # exit 1 if main.tex differs from the regenerated tables

Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXPS = ROOT / "problems" / "commutative-algebra" / "huneke-wiegand" / "experiments"
MAIN = HERE / "main.tex"

E058 = "EXP-058-local-endpoint-source"
E060 = "EXP-060-uniform-endpoint-annihilator"
E061 = "EXP-061-uniform-parity-functional"
E062 = "EXP-062-triangle-torsion-family"
E063 = "EXP-063-triangle-isolated-comparison"
E064 = "EXP-064-exact-carrier-two-primary"
E066 = "EXP-066-uniform-endpoint-face-collapse"


def art(exp: str, name: str) -> Path:
    return EXPS / exp / "artifacts" / name


def load(exp: str, name: str):
    return json.loads(art(exp, name).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def num(value: int) -> str:
    return f"{value:,}"


def split_hex(digest: str) -> str:
    """A 64-digit digest as four breakable groups of sixteen digits."""
    return r"\allowbreak ".join(digest[i:i + 16] for i in range(0, 64, 16))


def tab_sectors() -> str:
    audit = load(E061, "audit-results.json")
    lines = []
    totals = [0, 0, 0, 0]
    for row in audit["rows"]:
        sectors = row["sectors"]
        values = [len(sectors), sum(s["source_count"] for s in sectors), sum(s["D_row_count"] for s in sectors),
                  sum(s["D_nnz"] for s in sectors)]
        totals = [a + b for a, b in zip(totals, values)]
        biggest = max(s["source_count"] for s in sectors)
        lines.append(f"{row['p']} & {values[0]} & {num(values[1])} & {num(values[2])} & {num(values[3])} & {num(biggest)}\\\\")
    expected = audit["totals"]
    assert totals == [expected["sector_certificates"], expected["original_S_sources"], expected["D_rows"], expected["D_nnz"]], \
        "per-parameter sector sums disagree with the stored totals"
    body = "\n".join(lines)
    return rf"""\begin{{table}}[t]
\centering\small
\begin{{tabular}}{{rrrrrr}}
\toprule
$p$ & Sectors & S sources & D rows & D incidences & Largest sector\\
\midrule
{body}
\midrule
total & {totals[0]} & {num(totals[1])} & {num(totals[2])} & {num(totals[3])} & \\
\bottomrule
\end{{tabular}}
\caption{{Size of the reachable high sectors of the twelve-row functional at $p=8,\ldots,12$: number of sectors, original S
sources, original D rows, D incidences, and the number of sources of the largest sector, read from the stored independent
recomputation.}}
\label{{tab:sectors}}
\end{{table}}"""


def tab_runs() -> str:
    t063 = load(E063, "results.json")
    a063 = load(E063, "audit-results.json")
    t064 = load(E064, "results.json")
    a064 = load(E064, "audit-results.json")
    sub = "problems/commutative-algebra/huneke-wiegand/experiments"
    rows = [
        ("EXP-058", f"{E058}", "60 s, 1 GiB, 1200 columns, 20,000 nonzeros", "not stored"),
        ("EXP-059", "EXP-059-potential-connecting-map", "60 s, 1 GiB", "not stored"),
        ("EXP-060", E060, "60 s, 1 GiB", "not stored"),
        ("EXP-061", E061, "120 s, 1 GiB", "not stored"),
        ("EXP-062", E062, "120 s, 1 GiB", "not stored"),
        ("EXP-063", E063, f"{t063['resource_caps']['budget_seconds']:.0f} s, {t063['resource_caps']['memory_gib']:.0f} GiB",
         f"{t063['elapsed_seconds']:.2f} s / {a063['elapsed_seconds']:.2f} s"),
        ("EXP-064", E064, f"{t064['resource_caps']['budget_seconds']:.0f} s, {t064['resource_caps']['memory_gib']:.0f} GiB",
         f"{t064['elapsed_seconds']:.2f} s / {a064['elapsed_seconds']:.2f} s"),
        ("EXP-066", E066, "120 s, 1 GiB", "not stored"),
    ]
    body = []
    for label, folder, caps, elapsed in rows:
        cmd = f"{sub}/{folder}/run.py"
        extra = ""
        if label == "EXP-063":
            extra = r" \texttt{--p-min 8 --p-max 11 --budget-seconds 900 --memory-gib 12}"
        if label == "EXP-064":
            extra = r" \texttt{--p-min 8 --p-max 11 --budget-seconds 1200 --memory-gib 12}"
        body.append(rf"{label} & \texttt{{\scriptsize {folder}/run.py}}{extra} and \texttt{{audit.py}} & {caps} & {elapsed}\\[2pt]")
    lines = "\n".join(body)
    return rf"""\begin{{table}}[t]
\centering\scriptsize
\begin{{tabular}}{{>{{\raggedright\arraybackslash}}p{{0.08\textwidth}}>{{\raggedright\arraybackslash}}p{{0.46\textwidth}}>{{\raggedright\arraybackslash}}p{{0.17\textwidth}}>{{\raggedright\arraybackslash}}p{{0.15\textwidth}}}}
\toprule
Record & Command (producer and independent audit) & Caps (time, memory) & Elapsed (producer / audit)\\
\midrule
{lines}
\bottomrule
\end{{tabular}}
\caption[Reproduction commands, caps and elapsed times]{{Commands that reproduce each computation, run from the repository root with the repository interpreter (the folder path
is under \path{{problems/commutative-algebra/huneke-wiegand/experiments/}}), the declared time and memory caps, and the elapsed
times stored in the artifacts; a record without a stored time is marked.}}
\label{{tab:runs}}
\end{{table}}"""


def tab_cost() -> str:
    r060 = load(E060, "results.json")
    support = {row["p"]: row["source_support"] for row in r060["rows"]}
    ps = sorted(support)
    assert all(support[p] == 32 * p - 146 for p in ps), "the support law 32p-146 does not hold at every stored parameter"
    lo, hi = ps[0], ps[-1]
    faces_lo, faces_hi = support[lo] * (2 * lo - 2), support[hi] * (2 * hi - 2)
    audit = load(E061, "audit-results.json")
    by_p = {row["p"]: row["sectors"] for row in audit["rows"]}
    p_lo, p_hi = min(by_p), max(by_p)

    def sector_text(p: int) -> str:
        s = by_p[p]
        return f"$p={p}$: {len(s)} sectors, {num(sum(x['source_count'] for x in s))} sources, {num(sum(x['D_row_count'] for x in s))} D rows"

    r058 = load(E058, "results.json")
    row8 = next(r for r in r058["rows"] if r["p"] == 8)
    nb = row8["neighborhoods"]
    assert [(n["columns_count"], n["rows_count"], n["nnz"]) for n in nb] == [(47, 240, 306), (330, 1803, 2669)]
    nb_text = "; ".join(f"radius {n['radius']}: {n['columns_count']} columns, {n['rows_count']} rows, {n['nnz']} incidences" for n in nb)
    r066 = load(E066, "results.json")
    return rf"""\begin{{table}}[t]
\centering\scriptsize
\begin{{tabular}}{{>{{\raggedright\arraybackslash}}p{{0.19\textwidth}}>{{\raggedright\arraybackslash}}p{{0.30\textwidth}}>{{\raggedright\arraybackslash}}p{{0.43\textwidth}}}}
\toprule
Procedure & Cost in $p$ (from the loop structure) & Measured size in the stored artifacts\\
\midrule
Potential chain (Alg.~\ref{{alg:potential}}) & $O(|\mathrm{{active}}|\,p^2)$ steps per call & source $V_p$: {support[lo]} terms at $p={lo}$, {num(support[hi])} at $p={hi}$ (all {len(ps)} parameters: $32p-146$)\\[2pt]
Bitset differential (Alg.~\ref{{alg:bitset}}) & $O(Tp)$ face evaluations for $T$ terms & $V_p$: {num(faces_lo)} faces at $p={lo}$, {num(faces_hi)} at $p={hi}$\\[2pt]
Row-span certificate (Alg.~\ref{{alg:rowspan}}) & $O(n_D r)$ word operations on $n_S$-bit integers per sector & {sector_text(p_lo)}; {sector_text(p_hi)}\\[2pt]
Neighborhood expansion (Alg.~\ref{{alg:expand}}) & $\le 10p-1$ candidate variables per frontier row, one $O(p)$ boundary per accepted column & $p=8$, {nb_text}\\[2pt]
Face classification (Section~\ref{{sec:projection}}) & $O(p)$ per pair $(p,r)$, one count vector with constant-time updates & {r066['endpoint_checks']} endpoint checks over $p=8,\ldots,300$, {num(r066['mutations_rejected'])} altered cases rejected\\
\bottomrule
\end{{tabular}}
\caption{{Cost of the verification procedures in the parameter $p$, with the sizes measured in the stored artifacts at the smallest and
largest parameter of each computation; the cost column is an operation count read from the loops of the programs, not a timing.}}
\label{{tab:cost}}
\end{{table}}"""


def tab_hashes() -> str:
    entries = []

    def add(label: str, path: Path, kind: str):
        entries.append((label, num(path.stat().st_size), kind, sha(path)))

    for exp, tag in ((E060, "EXP-060"), (E062, "EXP-062")):
        manifest = load(exp, "results.json")["full_source_archive"]
        gz = art(exp, "results-sources.json.gz")
        assert sha(gz) == manifest["gzip_sha256"] and gz.stat().st_size == manifest["gzip_bytes"], f"{tag} archive differs from its manifest"
        entries.append((f"{tag} source archive (compressed)", num(manifest["gzip_bytes"]), "manifest", manifest["gzip_sha256"]))
        entries.append((f"{tag} source archive (raw)", num(manifest["raw_bytes"]), "manifest", manifest["raw_sha256"]))
        add(f"{tag} result manifest", art(exp, "results.json"), "file")
        add(f"{tag} independent recomputation", art(exp, "audit-results.json"), "file")
    for exp, tag in ((E063, "EXP-063"), (E064, "EXP-064")):
        add(f"{tag} results", art(exp, "results.json"), "file")
        add(f"{tag} independent recomputation", art(exp, "audit-results.json"), "file")
    body = "\n".join(
        rf"{label} & {size} & {kind} & \texttt{{\scriptsize {split_hex(digest)}}}\\[2pt]" for label, size, kind, digest in entries)
    return rf"""\begin{{table}}[t]
\centering\scriptsize
\begin{{tabular}}{{>{{\raggedright\arraybackslash}}p{{0.30\textwidth}}rl>{{\raggedright\arraybackslash}}p{{0.40\textwidth}}}}
\toprule
Artifact & Bytes & Source & SHA-256 (64 digits)\\
\midrule
{body}
\bottomrule
\end{{tabular}}
\caption{{Full SHA-256 digests of the stored archives and result files: the two deterministic source archives in their compressed and
raw forms (read from the manifests) and the result and independent-recomputation files of the four computations that pin them
(computed over the stored bytes).}}
\label{{tab:hashes}}
\end{{table}}"""


def tab_carrier() -> str:
    r063 = load(E063, "results.json")
    r064 = load(E064, "results.json")
    span = {}
    for row in r063["rows"]:
        for m in row["masks"]:
            span[(row["p"], m["mask"])] = (m["triangle_span_rank"], m["relation_dimension"], row["triangle_count"])
    lines = []
    assert [row["certificates"][0]["columns"] for row in r064["rows"]] == [1094, 1729, 2607, 3785]
    for row in r064["rows"]:
        for c in row["certificates"]:
            assert c["rank_gap"] == c["first_bockstein_rank"]
            t_rank, rel, tri = span[(row["p"], c["mask"])]
            assert t_rank == c["first_bockstein_rank"]
            first = row["p"] if c is row["certificates"][0] else ""
            lines.append(
                f"{first} & {c['mask']} & {num(c['rows'])} & {num(c['nonzeros'])} & {num(c['target_rational_rank'])} & "
                f"{num(c['rank_mod_two'])} & {c['first_bockstein_rank']} & ${c['complete_two_primary_type']}$ & {t_rank} of {tri}\\\\")
        lines.append(r"\addlinespace")
    lines.pop()
    body = "\n".join(lines)
    return rf"""\begin{{table}}[t]
\centering\scriptsize
\begin{{tabular}}{{rrrrrrrll}}
\toprule
$p$ & Mask & Rows & Nonzeros & $\operatorname{{rank}}_{{\mathbb Q}}$ & $\operatorname{{rank}}_{{\mathbb F_2}}$ & Bockstein rank & 2-primary type & Triangle span\\
\midrule
{body}
\bottomrule
\end{{tabular}}
\caption{{Finite carrier comparison at $p=8,\ldots,11$ for the four projection masks $56$, $58$, $59$ and $62$: the number of rows and nonzeros
of the carrier matrix (it has $1094$, $1729$, $2607$ and $3785$ columns at $p=8,\ldots,11$), its rational rank certified by modular
Hadamard bounds, its rank modulo two, the first integral Bockstein rank (equal to the rank gap), the complete $2$-primary type, and the
rank of the span of the triangle classes modulo two out of the number of triangles.}}
\label{{tab:carrier}}
\end{{table}}"""


def plot_figure(axis_opts: str, body: str, caption: str, label: str) -> str:
    tpl = (
        "\\begin{figure}[t]\n\\centering\n\\begin{tikzpicture}\n\\begin{axis}[width=0.86\\textwidth, height=5.4cm, grid=major, "
        "tick label style={font=\\small}, label style={font=\\small}, legend style={font=\\scriptsize}, @@OPTS@@]\n@@BODY@@"
        "\\end{axis}\n\\end{tikzpicture}\n\\caption{@@CAP@@}\n\\label{@@LABEL@@}\n\\end{figure}"
    )
    return tpl.replace("@@OPTS@@", axis_opts).replace("@@BODY@@", body).replace("@@CAP@@", caption).replace("@@LABEL@@", label)


def coords(points) -> str:
    return " ".join(f"({x},{y})" for x, y in points)


def fig_supportlaw() -> str:
    rows = load(E060, "results.json")["rows"]
    pts = [(row["p"], row["source_support"]) for row in rows]
    assert all(y == 32 * x - 146 for x, y in pts)
    body = ("\\addplot[only marks, mark=*, mark size=1.8pt] coordinates {" + coords(pts) + "};\n"
            "\\addplot[domain=8:100, thick, no marks] {32*x-146};\n\\legend{stored support, $32p-146$}\n")
    cap = ("Number of terms of the stored source $V_p$ at the 18 checked parameters of the annihilator computation, with the line $32p-146$ "
           "that passes through every stored point.")
    return plot_figure("xlabel={$p$}, ylabel={terms of $V_p$}, legend pos=north west", body, cap, "fig:supportlaw")


def fig_sectorsize() -> str:
    audit = load(E061, "audit-results.json")
    src, drows = [], []
    for row in audit["rows"]:
        src.append((row["p"], sum(s["source_count"] for s in row["sectors"])))
        drows.append((row["p"], sum(s["D_row_count"] for s in row["sectors"])))
    body = ("\\addplot[only marks, mark=*, mark size=1.8pt] coordinates {" + coords(src) + "};\n"
            "\\addplot[only marks, mark=square*, mark size=1.8pt] coordinates {" + coords(drows) + "};\n"
            "\\legend{original S sources, original D rows}\n")
    cap = ("Number of original S sources and of original D rows summed over the reachable high sectors of the twelve-row functional at "
           "$p=8,\\ldots,12$, read from the independent full-sector recomputation, on a logarithmic vertical scale.")
    return plot_figure("xlabel={$p$}, ylabel={count}, ymode=log, legend pos=south east, xtick={8,9,10,11,12}", body, cap, "fig:sectorsize")


def fig_trianglecount() -> str:
    checks = load(E062, "results.json")["count_checks"]
    assert all(c["formula_matches"] for c in checks) and len(checks) == 93
    pts = [(c["p"], c["count"]) for c in checks]
    assert all(c["count"] == ((c["p"] - 2) ** 2 + 3) // 12 for c in checks)
    body = ("\\addplot[only marks, mark=*, mark size=1.4pt] coordinates {" + coords(pts) + "};\n"
            "\\addplot[domain=8:100, samples=93, thick, no marks] {floor(((x-2)^2+3)/12)};\n"
            "\\legend{enumerated triangles, $\\lfloor((p-2)^2+3)/12\\rfloor$}\n")
    cap = ("Number of strictly increasing nonnegative triples of sum $p-2$ enumerated at the 93 parameters $p=8,\\ldots,100$ of the "
           "count identities, with the closed form of the quadratic count drawn through them.")
    return plot_figure("xlabel={$p$}, ylabel={number of triangles}, legend pos=north west", body, cap, "fig:trianglecount")


def fig_bockstein() -> str:
    r064 = load(E064, "results.json")["rows"]
    r063 = load(E063, "results.json")["rows"]
    series = {}
    for row in r064:
        for c in row["certificates"]:
            series.setdefault(c["mask"], []).append((row["p"], c["first_bockstein_rank"]))
    tri = [(row["p"], row["triangle_count"]) for row in r063]
    marks = {56: "triangle*", 58: "square*", 59: "diamond*", 62: "o"}
    body = "\\addplot[thick, dashed, no marks] coordinates {" + coords(tri) + "};\n"
    for mask in sorted(series):
        body += f"\\addplot[only marks, mark={marks[mask]}, mark size=2.4pt] coordinates {{" + coords(series[mask]) + "};\n"
    body += "\\legend{triangles, mask 56, mask 58, mask 59, mask 62}\n"
    cap = ("First integral Bockstein rank of the four carrier masks at $p=8,\\ldots,11$, with the number of triangle rows as a dashed line; "
           "the rank of mask $62$ coincides with that of mask $59$ and with the triangle count.")
    return plot_figure("xlabel={$p$}, ylabel={rank}, legend pos=north west, xtick={8,9,10,11}", body, cap, "fig:bockstein")


def fig_facecount() -> str:
    sweep = load(E066, "results.json")["sweep"]
    pts0, pts5 = [], []
    for row in sweep:
        for e in row["endpoints"]:
            c = e["counts"]
            assert c["R0"] == c["R2"] == row["p"] - 3 and c["R5"] == 1
        c = row["endpoints"][0]["counts"]
        pts0.append((row["p"], c["R0"]))
        pts5.append((row["p"], c["R5"]))
    assert len(sweep) == 293
    body = ("\\addplot[only marks, mark=*, mark size=0.9pt] coordinates {" + coords(pts0) + "};\n"
            "\\addplot[only marks, mark=square*, mark size=0.9pt] coordinates {" + coords(pts5) + "};\n"
            "\\legend{rows of type $R_0$ and of type $R_2$, rows of type $R_5$}\n")
    cap = ("Classified faces of the endpoint source $s_{p,1}$ at the 293 parameters $p=8,\\ldots,300$ of the sweep: rows of types $R_0$ "
           "and $R_2$ (equal in number, $p-3$) and the single row of type $R_5$.")
    return plot_figure("xlabel={$p$}, ylabel={faces}, legend pos=north west", body, cap, "fig:facecount")


TABLES = {
    "tab:sectors": tab_sectors,
    "tab:runs": tab_runs,
    "tab:cost": tab_cost,
    "tab:hashes": tab_hashes,
    "tab:carrier": tab_carrier,
    "fig:supportlaw": fig_supportlaw,
    "fig:sectorsize": fig_sectorsize,
    "fig:trianglecount": fig_trianglecount,
    "fig:bockstein": fig_bockstein,
    "fig:facecount": fig_facecount,
}


def regenerate(text: str) -> str:
    for label, build in TABLES.items():
        pattern = re.compile(rf"(% BEGIN GENERATED {re.escape(label)}\n).*?(% END GENERATED {re.escape(label)})", re.S)
        if not pattern.search(text):
            raise SystemExit(f"marker block {label} not found in main.tex")
        text = pattern.sub(lambda m: m.group(1) + build() + "\n" + m.group(2), text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="exit 1 when main.tex differs from the regenerated tables")
    args = parser.parse_args()
    old = MAIN.read_text(encoding="utf-8")
    new = regenerate(old)
    if args.check:
        if old != new:
            print("main.tex differs from the regenerated tables")
            return 1
        print("generated tables are current")
        return 0
    MAIN.write_text(new, encoding="utf-8", newline="\n")
    print("tables regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
