"""Tables, figures and number macros of the next-matching preprint, generated from the archived artifacts.

Run from anywhere: python make_tables_figures.py

Reads (all under problems/combinatorics/bougard-joret/experiments/):
  EXP-003-triangle-free-next-matching/artifacts/certificate.json
  EXP-003-triangle-free-next-matching/artifacts/independent-audit.json
  EXP-004-bracket-endpoint/artifacts/cfg-d7.jsonl, cfg-d8.jsonl, models-check.json
Writes next to this file:
  numbers.tex                 \\newcommand macros for every number the prose quotes from an artifact
  tables/*.tex                 booktabs tables
  figures/*.pdf                vector figures (matplotlib)

Two small blocks hold published values typed from primary sources (they are not artifacts of this
programme): AEY_Z_BOUNDS_SOURCE and BET_TABLE3 below, each with the passage it was read from.
The script runs no search and no enumeration: it only reads, tabulates and plots.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EXP = REPO / "problems/combinatorics/bougard-joret/experiments"
E3 = EXP / "EXP-003-triangle-free-next-matching/artifacts"
E4 = EXP / "EXP-004-bracket-endpoint/artifacts"
TAB = HERE / "tables"
FIG = HERE / "figures"

# BET (Banak, Ekim, Taskin), arXiv:2304.01729v1 full text, Table 3 ("Iterative Formulation performance
# summary"), rows with m = d + 1, read on 2026-11-14 from https://arxiv.org/html/2304.01729 .
# Columns: d, PreUB, (LB, UB, time) of the Iterative method, (LB, UB, time) of Iterative + Orbital Branching.
BET_TABLE3 = [
    (7, 59, (58, 58, 0), (58, 58, 0)),
    (8, 76, (74, 74, 3), (74, 74, 4)),
    (9, 94, (92, 92, 2), (92, 92, 11)),
    (10, 115, (112, 112, 100), (112, 112, 79)),
    (11, 137, (134, 134, 176), (134, 134, 146)),
    (12, 162, (158, 159, 1800), (158, 158, 1623)),
    (13, 188, (184, 185, 1800), (184, 185, 1800)),
]

plt.rcParams.update({
    "pdf.fonttype": 42, "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
    "legend.fontsize": 7.5, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "figure.dpi": 100,
})
NAVY, GREY, RED = "#19377d", "#666666", "#b03a2e"


def lf_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def tex_int(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def cfg_label(c: str) -> str:
    return "none" if c == "" else c


CFG_ORDER = ["", "-", "0", "0,0", "0,1", "0,2", "-,0", "-,-"]


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    cert = json.loads((E3 / "certificate.json").read_text(encoding="utf-8"))
    audit = json.loads((E3 / "independent-audit.json").read_text(encoding="utf-8"))
    cfg = {7: load_jsonl(E4 / "cfg-d7.jsonl"), 8: load_jsonl(E4 / "cfg-d8.jsonl")}
    models = json.loads((E4 / "models-check.json").read_text(encoding="utf-8"))

    degrees = [r["d"] for r in cert["degrees"]]
    assert degrees == list(range(7, 31))
    assert cert["status"] == "PASS" and audit["status"] == "PASS"

    # ---- consistency of the artifacts with the formulas the prose uses -------------------------------
    cand = {r["d"]: r["equality_type_candidates"] for r in cert["degrees"]}
    for d in degrees:
        assert cand[d] == math.comb(2 * d + 1, 3)
        assert all(r["equality_type_survivors"] == 0 for r in cert["degrees"])
    assert sum(cand.values()) == cert["summary"]["equality_type_candidates"]
    allc = {r["d"]: r for r in audit["five_type_controls"]}
    for d, r in allc.items():
        assert r["all_positive_compositions"] == math.comb(2 * d + 2, 4) and r["survivors"] == []
    n_all = sum(r["all_positive_compositions"] for r in allc.values())

    g_by = {(g["d"], g["kind"]): g for g in audit["graphs"]}
    assert len(audit["graphs"]) == 48
    for d in degrees:
        q, p = g_by[(d, "known-extremizer")], g_by[(d, "subdivided-crown")]
        assert q["edge_count"] == d * d + d + 2 and p["edge_count"] == d * d + d + 1
        assert q["matching_number"] == p["matching_number"] == d + 1
        assert q["complement_alpha"] == p["complement_alpha"] == 2
        assert q["complement_connectivity"] == d + 1 and p["complement_connectivity"] == d + 2
    n_flow = cert["summary"]["flow_checked_graphs"]
    n_cuts = audit["summary"]["rejected_cuts"]

    # ---- Table A: the 48 saved graphs ------------------------------------------------------------------
    rows = []
    for d in degrees:
        q, p = g_by[(d, "known-extremizer")], g_by[(d, "subdivided-crown")]
        flow = "yes" if d <= 18 else "no"
        rows.append(f"{d} & {2*d+3} & {q['edge_count']} & {q['matching_number']} & {q['complement_connectivity']} & "
                    f"{p['edge_count']} & {p['matching_number']} & {p['complement_connectivity']} & "
                    f"{d+2} & {flow} \\\\")
    write(TAB / "tab-graphs.tex",
          "\\begin{tabular}{rrrrrrrrrc}\n\\toprule\n"
          " & & \\multicolumn{3}{c}{$Q_d$ (shared-neighbourhood maximizer)} & "
          "\\multicolumn{3}{c}{$P_d$ (subdivided crown)} & & \\\\\n"
          "\\cmidrule(lr){3-5}\\cmidrule(lr){6-8}\n"
          "$d$ & $n$ & $\\e$ & $\\nu$ & $\\kappa(\\overline{\\cdot})$ & $\\e$ & $\\nu$ & $\\kappa(\\overline{\\cdot})$ & "
          "$d+2$ & flow \\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")

    # ---- Table B: five-type controls -------------------------------------------------------------------
    rows = []
    for d in sorted(allc):
        r = allc[d]
        rows.append(f"{d} & {2*d+3} & {tex_int(r['all_positive_compositions'])} & "
                    f"{tex_int(r['compositions_with_singletons'])} & {len(r['survivors'])} & {tex_int(cand[d])} \\\\")
    for d in (11, 20, 30):
        rows.append(f"{d} & {2*d+3} & -- & -- & -- & {tex_int(cand[d])} \\\\")
    write(TAB / "tab-types.tex",
          "\\begin{tabular}{rrrrrr}\n\\toprule\n"
          " & & \\multicolumn{3}{c}{independent audit (all positive compositions)} & main run \\\\\n"
          "\\cmidrule(lr){3-5}\\cmidrule(lr){6-6}\n"
          "$d$ & $n$ & compositions & with a singleton & survivors & designated singleton \\\\\n\\midrule\n"
          + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")

    # ---- Table C: EXP-004 configuration split ------------------------------------------------------------
    rows, stats = [], {}
    for d in (7, 8):
        by = {(r["config"], r["mode"]): r for r in cfg[d]}
        k2 = [r for r in cfg[d] if r["mode"] == "k2d"]
        stats[d] = {"unsat": sum(r["result"] == "unsat" for r in k2),
                    "unknown": sum(r["result"] == "unknown" for r in k2),
                    "min": min(r["seconds"] for r in k2), "max_unsat": max(r["seconds"] for r in k2 if r["result"] == "unsat"),
                    "total": sum(r["seconds"] for r in cfg[d])}
        assert len(k2) == 8
        for c in CFG_ORDER:
            k, f = by[(c, "k2d")], by.get((c, "free"))
            fs = (f"{f['result'].upper()} & {f['seconds']:.1f}" if f else "-- & --")
            rows.append(f"{d} & {cfg_label(c)} & {k['result'].upper()} & {k['seconds']:.1f} & {k['timeout']} & {fs} \\\\")
        if d == 7:
            rows.append("\\midrule")
    write(TAB / "tab-sat.tex",
          "\\begin{tabular}{rlrrrrr}\n\\toprule\n"
          " & & \\multicolumn{3}{c}{$K_{2,d}$-free search} & \\multicolumn{2}{c}{free control} \\\\\n"
          "\\cmidrule(lr){3-5}\\cmidrule(lr){6-7}\n"
          "$d$ & configuration & result & seconds & limit (s) & result & seconds \\\\\n\\midrule\n"
          + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")

    # ---- Table D: the models returned by the free controls ---------------------------------------------------
    rows = []
    for m in models:
        assert m["valid_extremal"] and m["theorem_holds"] and m["triangles"] == 0
        rows.append(f"{m['d']} & {cfg_label(m['config'])} & {m['order']} & {m['edges']} & {m['max_degree']} & "
                    f"{m['k2d_pairs']} & {m['complement_connectivity']} & {m['d']+1} \\\\")
    write(TAB / "tab-models.tex",
          "\\begin{tabular}{rlrrrrrr}\n\\toprule\n"
          "$d$ & configuration & order & edges & $\\Delta$ & pairs with $d$ common neighbours & "
          "$\\kappa(\\overline F)$ & $d+1$ \\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")

    # ---- Table E: records (scripts, hashes, run times) ------------------------------------------------------
    h = audit["sha256_lf"]
    h4 = {n: lf_sha(E4 / n) for n in ("cfg-d7.jsonl", "cfg-d8.jsonl", "models-check.json")}
    short = lambda s: s[:16]  # noqa: E731
    write(TAB / "tab-records.tex",
          "\\begin{tabular}{llll}\n\\toprule\n"
          "record & file & SHA-256 (first 16 digits) & origin \\\\\n\\midrule\n"
          f"EXP-003 & \\texttt{{run.py}} & \\texttt{{{short(h['run.py'])}}} & recorded by \\texttt{{audit.py}} \\\\\n"
          f"EXP-003 & \\texttt{{audit.py}} & \\texttt{{{short(h['audit.py'])}}} & recorded by \\texttt{{audit.py}} \\\\\n"
          f"EXP-003 & \\texttt{{proof.md}} & \\texttt{{{short(h['proof.md'])}}} & recorded by \\texttt{{audit.py}} \\\\\n"
          f"EXP-003 & \\texttt{{certificate.json}} & \\texttt{{{short(h['certificate.json'])}}} & recorded by \\texttt{{audit.py}} \\\\\n"
          f"EXP-003 & \\texttt{{EXP-001 run.py}} & \\texttt{{{short(cert['source_sha256']['EXP-001-tree-strip/run.py'])}}} & recorded in \\texttt{{certificate.json}} \\\\\n"
          f"EXP-004 & \\texttt{{cfg-d7.jsonl}} & \\texttt{{{short(h4['cfg-d7.jsonl'])}}} & computed here \\\\\n"
          f"EXP-004 & \\texttt{{cfg-d8.jsonl}} & \\texttt{{{short(h4['cfg-d8.jsonl'])}}} & computed here \\\\\n"
          f"EXP-004 & \\texttt{{models-check.json}} & \\texttt{{{short(h4['models-check.json'])}}} & computed here \\\\\n"
          "\\bottomrule\n\\end{tabular}\n")

    # ---- Table F: AEY bounds on Z(d) and whether they already give d + 1 < Z(d) -------------------------------
    # AEY Lemma 4.5 (Z(d) >= d + 1 for d >= 4), Lemma 4.6 (d even: Z = floor(5d/4); d odd:
    # floor(5(d-1)/4) <= Z <= floor(5(d+1)/4)), read on the final published text.
    rows = []
    for d in range(7, 15):
        if d % 2 == 0:
            lo = hi = (5 * d) // 4
        else:
            lo, hi = max(d + 1, (5 * (d - 1)) // 4), (5 * (d + 1)) // 4
        rng = f"{lo}" if lo == hi else f"{lo}--{hi}"
        status = "yes" if lo >= d + 2 else "no"
        rows.append(f"{d} & {d+1} & {rng} & {status} \\\\")
    write(TAB / "tab-z.tex",
          "\\begin{tabular}{rrcc}\n\\toprule\n$d$ & $d+1$ & range of $Z(d)$ proved by AEY & gives $d+1<Z(d)$? \\\\\n\\midrule\n"
          + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")

    # ---- Table G: BET Table 3, m = d + 1 -------------------------------------------------------------------
    rows = []
    for d, pre, it, ob in BET_TABLE3:
        ours = d * d + d + 2
        rows.append(f"{d} & {pre} & {it[0]} & {it[1]} & {it[2]} & {ob[0]} & {ob[1]} & {ob[2]} & {ours} \\\\")
    write(TAB / "tab-bet.tex",
          "\\begin{tabular}{rrrrrrrrr}\n\\toprule\n"
          " & & \\multicolumn{3}{c}{iterative method} & \\multicolumn{3}{c}{iterative with orbital branching} & \\\\\n"
          "\\cmidrule(lr){3-5}\\cmidrule(lr){6-8}\n"
          "$d$ & initial bound & lower & upper & time & lower & upper & time & $d^2+d+2$ \\\\\n\\midrule\n"
          + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")

    # ---- numbers.tex --------------------------------------------------------------------------------------------
    b7 = {r["config"]: r for r in cfg[7] if r["mode"] == "k2d"}
    b8 = {r["config"]: r for r in cfg[8] if r["mode"] == "k2d"}
    k7 = [r for r in cfg[7] if r["mode"] == "k2d"]
    k8 = [r for r in cfg[8] if r["mode"] == "k2d"]
    unknown = [r for r in k8 if r["result"] == "unknown"]
    assert len(unknown) == 1 and unknown[0]["config"] == "-,-"
    max8 = max(r["seconds"] for r in k8 if r["result"] == "unsat")
    free_sat = [(r["d"], r["config"]) for d in cfg for r in cfg[d] if r["mode"] == "free" and r["result"] == "sat"]
    ratios = [b8[c]["seconds"] / b7[c]["seconds"] for c in CFG_ORDER
              if b7[c]["seconds"] >= 1.0 and b8[c]["result"] != "unknown"]
    nums = {
        "ratioLow": f"{min(ratios):.1f}", "ratioHigh": f"{max(ratios):.1f}", "nRatios": len(ratios),
        "ratioUnknownLow": f"{unknown[0]['seconds'] / b7['-,-']['seconds']:.1f}",
        "nDegrees": len(degrees), "nGraphs": len(audit["graphs"]), "nFlow": n_flow, "nCuts": n_cuts,
        "nCandidates": tex_int(cert["summary"]["equality_type_candidates"]), "nAllComp": tex_int(n_all),
        "satSevenUnsat": sum(r["result"] == "unsat" for r in k7), "satEightUnsat": sum(r["result"] == "unsat" for r in k8),
        "satSevenMin": f"{min(r['seconds'] for r in k7):.1f}", "satSevenMax": f"{max(r['seconds'] for r in k7):.1f}",
        "satEightMin": f"{min(r['seconds'] for r in k8):.1f}", "satEightMax": f"{max8:.1f}",
        "satUnknownSec": f"{unknown[0]['seconds']:.1f}", "satUnknownLimit": unknown[0]["timeout"],
        "satSevenTotal": f"{stats[7]['total']:.1f}", "satEightTotal": f"{stats[8]['total']:.1f}",
        "nFreeSat": len(free_sat), "nModels": len(models),
        "nCfgRuns": len(cfg[7]) + len(cfg[8]),
        "nxVersion": audit["networkx_version"],
        "hashRun": h["run.py"], "hashAudit": h["audit.py"], "hashProof": h["proof.md"], "hashCert": h["certificate.json"],
        "hashOneRun": cert["source_sha256"]["EXP-001-tree-strip/run.py"],
        "hashCfgSeven": h4["cfg-d7.jsonl"], "hashCfgEight": h4["cfg-d8.jsonl"], "hashModels": h4["models-check.json"],
        "excessAtNineteen": next(r["bougard_upper"] - math.ceil((2 * r["d"] + 3) * (r["d"] + 2) / 2)
                                 for r in cert["degrees"] if r["d"] == 8),
        "boundaryEdges": audit["boundary_d6_edges"],
    }
    body = "% generated by make_tables_figures.py from the archived artifacts; do not edit\n"
    for k, v in nums.items():
        body += f"\\newcommand{{\\{k}}}{{{v}}}\n"
    write(HERE / "numbers.tex", body)

    # ---- Figure 2: five-type constraint enumerations --------------------------------------------------------
    fig, ax = plt.subplots(figsize=(5.6, 3.1))
    ax.semilogy(degrees, [cand[d] for d in degrees], "o-", color=NAVY, ms=3.5, lw=1.2,
                label="main run: first type fixed to size 1 ($\\binom{2d+1}{3}$)")
    ds = sorted(allc)
    ax.semilogy(ds, [allc[d]["all_positive_compositions"] for d in ds], "s--", color=GREY, ms=4.5, lw=1.2,
                label="independent audit: all compositions ($\\binom{2d+2}{4}$)")
    ax.semilogy(ds, [allc[d]["compositions_with_singletons"] for d in ds], "^:", color=RED, ms=4.5, lw=1.2,
                label="independent audit: compositions with a singleton")
    ax.axhline(1, color="black", lw=0.8)
    ax.text(30, 1.35, "survivors: 0 at every $d$ tested", ha="right", va="bottom", fontsize=7.5)
    ax.set_xlabel("degree bound $d$ (order $n=2d+3$)")
    ax.set_ylabel("tuples examined")
    ax.set_ylim(0.7, 1e6)
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "fig-types.pdf", metadata={"CreationDate": None, "Creator": None, "Producer": None})
    plt.close(fig)

    # ---- Figure 3: configuration-split search times --------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.0), sharex=True)
    for ax, d in zip(axes, (7, 8)):
        by = {(r["config"], r["mode"]): r for r in cfg[d]}
        for i, c in enumerate(CFG_ORDER):
            r = by[(c, "k2d")]
            unk = r["result"] == "unknown"
            ax.barh(i, r["seconds"], color="white" if unk else NAVY, edgecolor=RED if unk else NAVY,
                    hatch="///" if unk else None, height=0.6)
            ax.text(r["seconds"] * 1.15, i, ("UNKNOWN" if unk else "UNSAT"), va="center", fontsize=6.5)
            f = by.get((c, "free"))
            if f:
                ax.plot(f["seconds"], i, "D" if f["result"] == "sat" else "X", color=RED, ms=6.5, mfc="white" if f["result"] == "sat" else RED, mec="black", mew=0.8, zorder=5)
        ax.set_xscale("log")
        ax.set_xlim(0.05, 4e4)
        ax.set_yticks(range(len(CFG_ORDER)))
        ax.set_yticklabels([cfg_label(c) for c in CFG_ORDER] if d == 7 else [])
        ax.invert_yaxis()
        ax.set_title(f"$d={d}$")
        ax.set_xlabel("seconds (log scale)")
    axes[0].set_ylabel("defect configuration")
    fig.tight_layout()
    fig.savefig(FIG / "fig-sat.pdf", metadata={"CreationDate": None, "Creator": None, "Producer": None})
    plt.close(fig)

    # ---- Figure 4: growth of the search time from d = 7 to d = 8 -------------------------------------------------------
    fig, ax = plt.subplots(figsize=(4.4, 3.4))
    lim = [0.1, 5e3]
    ax.loglog(lim, lim, color=GREY, lw=0.8, ls="--")
    for c in CFG_ORDER:
        x, y = b7[c]["seconds"], b8[c]["seconds"]
        unk = b8[c]["result"] == "unknown"
        ax.plot(x, y, marker="^" if unk else "o", color=RED if unk else NAVY, ms=5.5, mfc="white" if unk else NAVY, ls="")
        ax.annotate(cfg_label(c), (x, y), textcoords="offset points", xytext=(4, -9 if c in ("", "0") else 3), fontsize=6.5)
    ax.set_xlim(*lim)
    ax.set_ylim(*lim)
    ax.set_xlabel("seconds at $d=7$")
    ax.set_ylabel("seconds at $d=8$ (triangle: limit reached)")
    ax.text(0.12, 0.17 * 3, "$y=x$", fontsize=7, color=GREY)
    fig.tight_layout()
    fig.savefig(FIG / "fig-growth.pdf", metadata={"CreationDate": None, "Creator": None, "Producer": None})
    plt.close(fig)

    # ---- Figure 5: the excess over the degree-sum prediction ---------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    pred = {r["d"]: math.ceil((2 * r["d"] + 3) * (r["d"] + 2) / 2) for r in cert["degrees"]}
    low = [r["bougard_lower"] - pred[r["d"]] for r in cert["degrees"]]
    up = [r["bougard_upper"] - pred[r["d"]] for r in cert["degrees"]]
    assert low == [r["excess_lower"] for r in cert["degrees"]]
    ax.step(degrees, up, where="mid", color=NAVY, lw=1.4, label="exact value $d^2+4d+2$ (this paper)")
    ax.step(degrees, low, where="mid", color=GREY, lw=1.4, ls="--", label="lower endpoint $d^2+4d+1$ (excluded)")
    ax.plot(degrees, up, "o", color=NAVY, ms=3)
    ax.plot(degrees, low, "s", color=GREY, ms=3)
    ax.set_xlabel("degree bound $d$ (parameters $(2d+3,2,d+2)$)")
    ax.set_ylabel("edges above $\\lceil nk/2\\rceil$")
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "fig-excess.pdf", metadata={"CreationDate": None, "Creator": None, "Producer": None})
    plt.close(fig)

    print("tables:", sorted(p.name for p in TAB.glob("*.tex")))
    print("figures:", sorted(p.name for p in FIG.glob("*.pdf")))
    print("numbers:", {k: nums[k] for k in ("nGraphs", "nCandidates", "nAllComp", "satSevenUnsat", "satEightUnsat")})


if __name__ == "__main__":
    main()
